#!/usr/bin/env python3
"""Tia Storyline — hourly ingest: miniflux (incremental) + reddit RSS.

Watermark dedup lives in engine/data/state.json (last miniflux entry id + seen
reddit URLs). New events are written to data/events/ (md + json) and their ids
queued in data/new-events.json for merge.py to cluster. Miniflux read-state is
NOT the tracker — the watermark is the source of truth.

Usage: python3 ingest.py [--hours N]
"""
import html
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from build_registry import clean_title, domain_of  # noqa: E402

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
EVENTS = os.path.join(DATA, "events")
STATE = os.path.join(DATA, "state.json")
QUEUE = os.path.join(DATA, "new-events.json")
REDDIT = os.path.join(DATA, "reddit.json")
REDDIT_RSS = "https://www.reddit.com/r/cybersecurity/.rss?limit=100"
UA = "tia-storyline/1.0"
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
LOOKBACK_H = 48
REDDIT_WINDOW = 500

SCRIPT_RANGES = [("ko", re.compile(r"[\uAC00-\uD7AF]")), ("ja", re.compile(r"[\u3040-\u30FF]")),
                 ("zh", re.compile(r"[\u4E00-\u9FFF]")), ("ru", re.compile(r"[\u0400-\u04FF]")),
                 ("ar", re.compile(r"[\u0600-\u06FF]")), ("he", re.compile(r"[\u0590-\u05FF]")),
                 ("el", re.compile(r"[\u0370-\u03FF]")), ("hi", re.compile(r"[\u0900-\u097F]"))]


def detect_lang(text):
    """Dominant non-Latin script -> language code; 'en' for Latin content."""
    counts = {name: len(rx.findall(text)) for name, rx in SCRIPT_RANGES}
    total = sum(counts.values())
    if total == 0:
        return "en"
    best = max(counts, key=counts.get)
    return best if counts[best] / max(1, len(text)) > 0.08 else "en"


def norm_dt(s):
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def strip_html(content, max_chars=1500):
    # Some feeds (e.g. CCyber advisories via malware.news) deliver their body
    # ENTITY-ENCODED — literal "&lt;div&gt;" text, not tags, sometimes double-
    # encoded ("&amp;nbsp;") — so unescape until stable BEFORE the tag regexes,
    # or the junk lands in content_md and shows up in card snippets.
    text = content or ""
    while True:
        nxt = html.unescape(text)
        if nxt == text:
            break
        text = nxt
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"</?(p|div|li|h[1-6]|tr|blockquote)\b[^>]*>", "\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


MARKETING_BLOCKS = [
    # malware.news affiliate block ("Introduction to Malware Binary Triage (IMBT)
    # Course ... no extra cost to you.")
    re.compile(r"(?:Key Points\s+)?Introduction to Malware Binary Triage \(IMBT\)"
               r" Course.*?no extra cost to you\.?\s*", re.S | re.I),
    re.compile(r"\b(?:Get|Save)\s+\d+%\s+off using coupon code[^\n]*", re.I),
    re.compile(r"\bcoupon code:?\s+[A-Z0-9]+\b[^\n]*", re.I),
    re.compile(r"\bMWNEWS\d+\b[^\n]*", re.I),
    re.compile(r"\baffiliate link[^\n]*", re.I),
    re.compile(r"^\s*Key Points\s+", re.I),
    # SecurityWeek nav + newsletter block
    re.compile(r"SECURITYWEEK NETWORK:.*?what are you looking for\??\s*", re.S | re.I),
    re.compile(r"SecurityWeek Daily Briefing Newsletter.*?Unsubscribe at any time\.?\s*(Close\s*)?", re.S | re.I),
    re.compile(r"SecurityWeek Email Briefing.*?Unsubscribe at any time\.?\s*(Close\s*)?", re.S | re.I),
    # generic newsletter/read-more boilerplate across outlets
    re.compile(r"\bSubscribe to the \w+(?: Email)? Briefing\b[^\n]*", re.I),
    re.compile(r"\b(?:Sign up|Subscribe) to our (?:free |daily )?newsletter\b[^\n]*", re.I),
    re.compile(r"\bAdvertisement\.? Scroll to continue reading\.?\s*", re.I),
    re.compile(r"^\s*(?:Advertisement|Advertisement\.)\s*$", re.I),
    re.compile(r"\bUnsubscribe at any time\.?\s*(Close\s*)?", re.I),
    re.compile(r"^\s*Close\s*$", re.I),
]


def strip_marketing(text):
    """Deterministically remove known marketing/affiliate boilerplate from article
    bodies (e.g. the malware.news course promo appended to every post)."""
    if not text:
        return text
    for rx in MARKETING_BLOCKS:
        text = rx.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"last_miniflux_id": 0, "seen_reddit": []}


def save_state(st):
    json.dump(st, open(STATE, "w"), indent=1)


def ingest_miniflux(st, hours):
    # imported here so engine modules that only need strip_html (tests, ssg
    # lint paths) don't require the local miniflux client on import
    sys.path.insert(0, "/usr/local/bin")
    from miniflux import MinifluxClient  # noqa: E402
    client = MinifluxClient()
    now = int(time.time())
    max_id = st.get("last_miniflux_id", 0)
    new_ids = []
    window = hours * 3600
    # paginate backwards until the window overlaps the watermark (a late-categorized
    # entry can have id > watermark but published_at older than the window)
    oldest_seen = None
    while True:
        entries = list(client.iter_entries(category_id=4, after=now - window))
        if not entries:
            break
        ids = [e["id"] for e in entries]
        if min(ids) <= max_id:
            break
        window *= 2                       # widen until overlap
        if window > 30 * 24 * 3600:
            break
    for e in sorted(entries, key=lambda x: x["id"]):
        if e["id"] <= max_id:
            continue
        max_id = max(max_id, e["id"])
        eid = f"mf:{e['id']}"
        title = clean_title(e.get("title") or "")
        url = e.get("url") or ""
        body = strip_marketing(strip_html(e.get("content")))
        cves = sorted({c.upper() for c in CVE_RE.findall(title + " " + body)})
        meta = {"id": eid, "title": title, "kind": "pending",
                "source": domain_of(url), "url": url,
                "published_at": norm_dt(e.get("published_at") or datetime.now(timezone.utc).isoformat()),
                "cves": cves, "lang": detect_lang(title + " " + body)}
        with open(os.path.join(EVENTS, eid + ".md"), "w") as f:
            f.write(body + "\n")
        json.dump(meta, open(os.path.join(EVENTS, eid + ".json"), "w"), indent=1)
        new_ids.append(eid)
    st["last_miniflux_id"] = max_id
    return new_ids


def ingest_reddit(st):
    posts = []
    req = urllib.request.Request(REDDIT_RSS, headers={"User-Agent": UA})
    try:
        root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:
        print(f"reddit RSS failed: {e}", file=sys.stderr)
        return
    ns = {"a": "http://www.w3.org/2005/Atom"}
    seen_set = set(st.get("seen_reddit", []))
    seen_list = st.get("seen_reddit", [])
    for e in root.findall("a:entry", ns):
        title = (e.findtext("a:title", default="", namespaces=ns) or "").strip()
        pid = (e.findtext("a:id", default="", namespaces=ns) or "").strip()
        content = e.findtext("a:content", default="", namespaces=ns) or ""
        links = [l for l in re.findall(r'href="([^"]+)"', content) if "reddit.com" not in l]
        key = pid or (links[0] if links else title[:40])
        if key in seen_set:
            continue
        seen_set.add(key)
        seen_list.append(key)
        pub = e.findtext("a:published", default="", namespaces=ns)
        posts.append({"id": pid, "title": title,
                      "article_url": links[0] if links else None,
                      "published_at": norm_dt(pub) if pub else None})
    # trim from the FRONT (insertion order), not set order
    if len(seen_list) > REDDIT_WINDOW:
        seen_list = seen_list[-REDDIT_WINDOW:]
        seen_set = set(seen_list)
    st["seen_reddit"] = seen_list
    json.dump(posts, open(REDDIT, "w"), indent=1)
    return len(posts)


def main():
    hours = LOOKBACK_H
    if "--hours" in sys.argv:
        hours = int(sys.argv[sys.argv.index("--hours") + 1])
    st = load_state()
    new_ids = ingest_miniflux(st, hours)
    reddit_n = ingest_reddit(st)
    save_state(st)
    # append to any unconsumed queue (merge may have failed between runs)
    prev = json.load(open(QUEUE)) if os.path.exists(QUEUE) else {"events": []}
    merged_q = list(dict.fromkeys(prev.get("events", []) + new_ids))
    queue = {"date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "events": merged_q}
    json.dump(queue, open(QUEUE, "w"), indent=1)
    print(f"miniflux new events: {len(new_ids)} | reddit posts: {reddit_n} | watermark: {st['last_miniflux_id']} | queue: {len(merged_q)}")


if __name__ == "__main__":
    main()
