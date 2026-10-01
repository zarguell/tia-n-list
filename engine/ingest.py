#!/usr/bin/env python3
"""Tia Storyline — hourly ingest: native RSS polling + reddit RSS.

Leaf A (docs/vps-migration.md): miniflux replaced by a stdlib poller over
engine/feeds/cyber.opml (the 57 cyber feeds). Dedup = bounded seen-ring of
content-hashed feed+guid + a one-time cutover timestamp (the miniflux backlog
is never re-ingested). Event ids: rss:<sha1>. The two ex-crawler hosts
(bleepingcomputer, securityweek) still get best-effort full-article text;
the other 55 feeds consume RSS content as-is — exactly what miniflux stored.

Watermark/dedup lives in engine/data/state.json (rss_seen ring, rss_cutover_ts,
seen_reddit). New events are written to data/events/ (md + json) and their ids
queued in data/new-events.json for merge.py to cluster.

Usage: python3 ingest.py [--hours N]
"""
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

from build_registry import clean_title, domain_of  # noqa: E402

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
EVENTS = os.path.join(DATA, "events")
STATE = os.path.join(DATA, "state.json")
QUEUE = os.path.join(DATA, "new-events.json")
REDDIT = os.path.join(DATA, "reddit.json")
# Reddit is a FULL source now, not just a hot-score signal: posts with an
# outbound article link are promoted to events (queued for merge clustering
# like miniflux entries); link-less posts stay signal-only.
REDDIT_FEEDS = (
    ("cybersecurity", "https://www.reddit.com/r/cybersecurity/.rss?limit=100"),
    ("netsec", "https://www.reddit.com/r/netsec/.rss?limit=100"),
)
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
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except ValueError:
        return s          # malformed feed date — pass through, never crash ingest


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


# --- native RSS polling (replaces miniflux — docs/vps-migration.md leaf A) ---

FEEDS_OPML = os.path.join(ENGINE, "feeds", "cyber.opml")
FETCH_WORKERS = 8          # IO-only parallelism (AGENTS rule: never parallel pi)
FETCH_TIMEOUT = 15
RSS_WINDOW = 2000          # seen-guid ring buffer
# Feeds whose content miniflux historically upgraded via its crawler — keep
# fetching best-effort full article text for just these (55/57 feeds consumed
# RSS content as-is; their scraper config: SecurityWeek div.zox-post-body,
# BleepingComputer default readability).
FULL_TEXT_HOSTS = ("bleepingcomputer.com", "securityweek.com")


def _load_feed_urls(path=None):
    """OPML -> [(xml_url, title)] — the cyber category export, checked in."""
    path = path or FEEDS_OPML          # module attr at CALL time (tests patch it)
    tree = ET.parse(path)
    out = []
    for o in tree.iter("outline"):
        url = o.get("xmlUrl")
        if url:
            out.append((url, o.get("title") or o.get("text") or url))
    if not out:
        raise RuntimeError(f"no feeds in {path}")
    return out


def _fetch(url, timeout=FETCH_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _child_text(el, localname):
    """Namespace-proof text lookup by local tag name (content:encoded etc.)."""
    for child in el.iter():
        if child.tag.rsplit("}", 1)[-1] == localname and child.text:
            return child.text.strip()
    return ""


def _parse_feed(xml_bytes):
    """RSS 2.0 + Atom -> entry dicts (stdlib ET, same style as ingest_reddit)."""
    root = ET.fromstring(xml_bytes)
    entries = []
    for el in root.iter():
        local = el.tag.rsplit("}", 1)[-1]
        if local == "item":                                   # RSS 2.0
            link = _child_text(el, "link")
            entries.append({
                "guid": _child_text(el, "guid") or link,
                "link": link,
                "title": _child_text(el, "title"),
                "published": _child_text(el, "pubDate") or _child_text(el, "date"),
                "content": _child_text(el, "encoded") or _child_text(el, "description"),
            })
        elif local == "entry":                                # Atom
            link = ""
            for l in el.iter():
                if l.tag.rsplit("}", 1)[-1] == "link" and l.get("rel") in (None, "alternate"):
                    link = l.get("href") or ""
                    break
            entries.append({
                "guid": _child_text(el, "id") or link,
                "link": link,
                "title": _child_text(el, "title"),
                "published": _child_text(el, "published") or _child_text(el, "updated"),
                "content": _child_text(el, "content") or _child_text(el, "summary"),
            })
    return entries


def _parse_datetime(s):
    """RFC822 (RSS) or ISO8601 (Atom) -> aware datetime | None."""
    if not s:
        return None
    s = s.strip()
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        pass
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def _entry_id(feed_url, e):
    raw = f"{feed_url}|{e['guid'] or e['link']}"
    return "rss:" + hashlib.sha1(raw.encode()).hexdigest()[:16]


def _fetch_full_text(url):
    """Readability-lite for the two ex-crawler hosts: join article <p> text.
    Best-effort — None on any failure, caller falls back to RSS content."""
    try:
        page = _fetch(url).decode("utf-8", "replace")
    except Exception:
        return None
    page = re.sub(r"<(script|style|nav|footer|header|form)[^>]*>.*?</\1>",
                  " ", page, flags=re.S | re.I)
    paras = [re.sub(r"<[^>]+>", " ", p)
             for p in re.findall(r"<p[^>]*>(.*?)</p>", page, flags=re.S | re.I)]
    paras = [re.sub(r"\s+", " ", p).strip() for p in paras]
    paras = [p for p in paras if len(p) > 40]
    return "\n\n".join(paras)[:6000] if paras else None


def _poll_feed(feed_url, hours):
    """Fetch + parse one feed -> (entries within window, error|None)."""
    try:
        entries = _parse_feed(_fetch(feed_url))
    except Exception as e:
        return [], str(e)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    keep = []
    for e in entries:
        dt = _parse_datetime(e["published"])
        e["dt"] = dt
        # date-less entries: keep (the seen-ring dedups them)
        if dt is None or dt >= cutoff:
            keep.append(e)
    return keep, None


def ingest_rss(st, hours):
    """Poll cyber.opml natively. Dedup = seen-ring of content-hashed
    feed+guid + one-time cutover timestamp (pre-cutover backlog is never
    re-ingested). Writes events identically to the old miniflux path."""
    feeds = _load_feed_urls()
    seen_list = list(st.get("rss_seen", []))
    seen_set = set(seen_list)
    now = datetime.now(timezone.utc)
    if not st.get("rss_cutover_ts"):
        st["rss_cutover_ts"] = now.isoformat().replace("+00:00", "Z")
    cutoff = datetime.fromisoformat(st["rss_cutover_ts"].replace("Z", "+00:00"))

    new_ids, errors, candidates = [], [], []
    with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as pool:
        results = pool.map(lambda u: _poll_feed(u, hours), [f for f, _ in feeds])
        for (feed_url, _t), (entries, err) in zip(feeds, results):
            if err:
                errors.append(f"{domain_of(feed_url)}: {err}")
            for e in entries:
                e["feed"] = feed_url
                candidates.append(e)

    for e in sorted(candidates, key=lambda x: x.get("dt") or now):
        eid = _entry_id(e["feed"], e)
        if eid in seen_set:
            continue
        seen_set.add(eid)
        seen_list.append(eid)
        dt = e.get("dt")
        if dt is not None and dt < cutoff:
            continue                       # pre-cutover backlog — never re-ingest
        title = clean_title(e["title"] or "")
        url = e["link"] or ""
        content = e["content"] or ""
        host = domain_of(url).lower()
        if url and any(h in host for h in FULL_TEXT_HOSTS):
            full = _fetch_full_text(url)
            if full:
                content = full
        body = strip_marketing(strip_html(content))
        cves = sorted({c.upper() for c in CVE_RE.findall(title + " " + body)})
        meta = {"id": eid, "title": title, "kind": "pending",
                "source": domain_of(url), "url": url,
                "published_at": norm_dt(e["dt"].isoformat()) if e.get("dt")
                else now.isoformat().replace("+00:00", "Z"),
                "cves": cves, "lang": detect_lang(title + " " + body)}
        with open(os.path.join(EVENTS, eid + ".md"), "w") as f:
            f.write(body + "\n")
        json.dump(meta, open(os.path.join(EVENTS, eid + ".json"), "w"),
                  indent=1)
        new_ids.append(eid)

    if len(seen_list) > RSS_WINDOW:
        seen_list = seen_list[-RSS_WINDOW:]
    st["rss_seen"] = seen_list
    st["rss_last_fetch"] = {"ok": len(feeds) - len(errors), "errors": len(errors)}
    if errors:
        print(f"rss fetch errors ({len(errors)}): " + "; ".join(errors[:3]),
              file=sys.stderr)
    return new_ids



def ingest_reddit(st):
    """Fetch all reddit feeds; write data/reddit.json (signal layer) AND
    promote link-posts to events (queued for merge like miniflux entries).
    Returns (post_count, new_event_ids)."""
    posts = []          # signal layer (reddit.json shape)
    new_ids = []        # promoted event ids for the merge queue
    ns = {"a": "http://www.w3.org/2005/Atom"}
    seen_set = set(st.get("seen_reddit", []))
    seen_list = st.get("seen_reddit", [])
    seen_urls = set()
    for sub, feed in REDDIT_FEEDS:
        req = urllib.request.Request(feed, headers={"User-Agent": UA})
        try:
            root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
        except Exception as e:
            print(f"reddit RSS failed ({sub}): {e}", file=sys.stderr)
            continue
        for e in root.findall("a:entry", ns):
            title = (e.findtext("a:title", default="", namespaces=ns) or "").strip()
            pid = (e.findtext("a:id", default="", namespaces=ns) or "").strip()
            content = e.findtext("a:content", default="", namespaces=ns) or ""
            links = [l for l in re.findall(r'href="([^"]+)"', content)
                     if "reddit.com" not in l]
            key = pid or (links[0] if links else title[:40])
            if key in seen_set:
                continue
            seen_set.add(key)
            seen_list.append(key)
            pub = e.findtext("a:published", default="", namespaces=ns)
            article_url = links[0] if links else None
            # one event per article per run — two subs posting the same
            # link must not double-count
            if article_url and article_url.lower() in seen_urls:
                article_url_dupe = True
            else:
                article_url_dupe = False
            if article_url:
                seen_urls.add(article_url.lower())
            posts.append({"id": pid, "title": title, "sub": sub,
                          "article_url": article_url,
                          "published_at": norm_dt(pub) if pub else None})
            # ── promotion: link-posts become events ──
            if not article_url or article_url_dupe:
                continue
            eid = "rd:" + re.sub(r"[^A-Za-z0-9_-]", "",
                                 pid or article_url)[:40]
            if not eid[3:]:
                continue
            body = strip_html(content, max_chars=800)
            ev = {"id": eid,
                  "title": clean_title(title) or title[:140],
                  "kind": "pending",
                  "source": domain_of(article_url),
                  "url": article_url,
                  "published_at": norm_dt(pub) if pub
                  else datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                  "cves": sorted({c.upper() for c in CVE_RE.findall(
                      title + " " + body)}),
                  "lang": detect_lang(title + " " + body)}
            with open(os.path.join(EVENTS, eid + ".md"), "w") as f:
                f.write((body + "\n\n" if body else "") +
                        f"via reddit r/{sub}: {title}\n")
            json.dump(ev, open(os.path.join(EVENTS, eid + ".json"), "w"),
                      indent=1)
            new_ids.append(eid)
    # trim from the FRONT (insertion order), not set order
    if len(seen_list) > REDDIT_WINDOW:
        seen_list = seen_list[-REDDIT_WINDOW:]
        seen_set = set(seen_list)
    st["seen_reddit"] = seen_list
    json.dump(posts, open(REDDIT, "w"), indent=1)
    return len(posts), new_ids


def main():
    hours = LOOKBACK_H
    if "--hours" in sys.argv:
        hours = int(sys.argv[sys.argv.index("--hours") + 1])
    st = load_state()
    new_ids = ingest_rss(st, hours)
    reddit_n, reddit_event_ids = ingest_reddit(st)
    save_state(st)
    # append to any unconsumed queue (merge may have failed between runs)
    prev = json.load(open(QUEUE)) if os.path.exists(QUEUE) else {"events": []}
    merged_q = list(dict.fromkeys(
        prev.get("events", []) + new_ids + reddit_event_ids))
    queue = {"date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "events": merged_q}
    json.dump(queue, open(QUEUE, "w"), indent=1)
    fetch = st.get("rss_last_fetch", {})
    print(f"rss new events: {len(new_ids)} | reddit posts: {reddit_n} "
          f"(+{len(reddit_event_ids)} promoted) | feeds: "
          f"{fetch.get('ok', '?')}/{fetch.get('ok', 0) + fetch.get('errors', 0)} ok "
          f"| queue: {len(merged_q)}")


if __name__ == "__main__":
    main()
