#!/usr/bin/env python3
"""Tia Storyline — hourly ingest: miniflux (incremental) + reddit RSS.

Watermark dedup lives in engine/data/state.json (last miniflux entry id + seen
reddit URLs). New events are written to data/events/ (md + json) and their ids
queued in data/new-events.json for merge.py to cluster. Miniflux read-state is
NOT the tracker — the watermark is the source of truth.

Usage: python3 ingest.py [--hours N]
"""
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

sys.path.insert(0, "/home/coder/.local/opt/miniflux")
from miniflux import MinifluxClient  # noqa: E402

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


def norm_dt(s):
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def strip_html(content, max_chars=1500):
    text = re.sub(r"<br\s*/?>", "\n", content or "")
    text = re.sub(r"</?(p|div|li|h[1-6]|tr|blockquote)\b[^>]*>", "\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"last_miniflux_id": 0, "seen_reddit": []}


def save_state(st):
    json.dump(st, open(STATE, "w"), indent=1)


def ingest_miniflux(st, hours):
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
        body = strip_html(e.get("content"))
        cves = sorted({c.upper() for c in CVE_RE.findall(title + " " + body)})
        meta = {"id": eid, "title": title, "kind": "pending",
                "source": domain_of(url), "url": url,
                "published_at": norm_dt(e.get("published_at") or datetime.now(timezone.utc).isoformat()),
                "cves": cves}
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
