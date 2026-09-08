#!/usr/bin/env python3
"""Reddit promotion regression suite — link-posts must become events
(queued for merge like miniflux entries), self-posts stay signal-only.

Background (2026-09-08): reddit was demoted to a hot-score subsignal
(reddit.json only). Promoted to a full source: ingest_reddit now writes
events (rd:<id>) for posts with an outbound article link so reddit
pickups land in story timelines and genuinely-new links become story
candidates — same treatment as X (x-collector) and miniflux.

Run: python3 engine/test_reddit_promote.py   (exit 0 = pass)
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ingest  # noqa: E402

FAILURES = []


def check(name, got, expect):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}"
          + ("" if ok else f"  got {got!r} want {expect!r}"))
    if not ok:
        FAILURES.append(name)


FAKE_FEED = ("""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>t3_abc123</id>
    <title>Vendor discloses critical RCE in gateway appliance</title>
    <content type="html">&lt;p&gt;&lt;a href="https://example.com/advisory"&gt;advisory&lt;/a&gt;&lt;/p&gt;</content>
    <published>2026-09-08T10:00:00Z</published>
  </entry>
  <entry>
    <id>t3_def456</id>
    <title>Discussion: is a career in IR still worth it?</title>
    <content type="html">&lt;a href="https://www.reddit.com/r/cybersecurity/comments/xyz"&gt;self post&lt;/a&gt;</content>
    <published>2026-09-08T09:00:00Z</published>
  </entry>
</feed>""")


def main():
    global FAILURES
    tmp = tempfile.mkdtemp()
    data = os.path.join(tmp, "data")
    events = os.path.join(data, "events")
    os.makedirs(events)
    ingest.DATA = data
    ingest.EVENTS = events
    ingest.STATE = os.path.join(data, "state.json")
    ingest.QUEUE = os.path.join(data, "new-events.json")
    ingest.REDDIT = os.path.join(data, "reddit.json")
    ingest.REDDIT_FEEDS = (("cybersecurity", "https://fake.local/rss"),)

    real_urlopen = ingest.urllib.request.urlopen
    real_et = ingest.ET.fromstring

    def fake_fromstring(data_bytes):
        return real_et(data_bytes)

    try:
        ingest.ET.fromstring = fake_fromstring

        class FakeResp:
            def __init__(self, payload):
                self._p = payload

            def read(self):
                return self._p.encode()

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        ingest.urllib.request.urlopen = \
            lambda req, timeout=30: FakeResp(FAKE_FEED)

        print("== first run: link post promoted, self post signal-only")
        st = ingest.load_state()
        n, ids = ingest.ingest_reddit(st)
        check("posts fetched", n, 2)
        check("one event promoted", ids, ["rd:t3_abc123"])
        ev = json.load(open(os.path.join(events, "rd:t3_abc123.json")))
        check("event url = article", ev["url"], "https://example.com/advisory")
        check("event source = article domain", ev["source"], "example.com")
        check("event kind pending", ev["kind"], "pending")
        check("self post did NOT become an event",
              os.path.exists(os.path.join(events, "rd:t3_def456.json")),
              False)
        sig = json.load(open(ingest.REDDIT))
        check("both posts in signal file", len(sig), 2)
        check("signal post keeps sub tag", sig[0].get("sub"), "cybersecurity")
        check("event md written",
              os.path.exists(os.path.join(events, "rd:t3_abc123.md")), True)

        ingest.save_state(st)  # main() persists the watermark between runs
        print("== second run: seen dedupe — nothing re-promoted")
        st = ingest.load_state()
        n2, ids2 = ingest.ingest_reddit(st)
        check("no new posts on rerun", n2, 0)
        check("no new events on rerun", ids2, [])
    finally:
        ingest.urllib.request.urlopen = real_urlopen
        ingest.ET.fromstring = real_et

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {FAILURES}")
        sys.exit(1)
    print("ALL PASS")


if __name__ == "__main__":
    main()
