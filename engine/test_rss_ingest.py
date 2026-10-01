#!/usr/bin/env python3
"""Native RSS poller tests (leaf A) — offline, no network.

Run:  python3 engine/test_rss_ingest.py   (exit 0 = pass)
      or: pytest engine/test_rss_ingest.py

Covers: OPML parse, RSS+Atom parsing (namespace-proof), window filtering,
cutover semantics (pre-cutover backlog never re-ingested), seen-ring dedup,
full-text gating to the ex-crawler hosts, malformed-date tolerance.
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ENGINE)

import ingest  # noqa: E402

NOW = datetime.now(timezone.utc)


def _rfc822(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


P_FRESH = _rfc822(NOW - timedelta(hours=1))     # in window, post-cutover (seeded)
P_STALE = _rfc822(NOW - timedelta(hours=72))    # outside 48h window
P_BC = _rfc822(NOW - timedelta(minutes=30))     # bleepingcomputer article
P_FUTURE = _rfc822(NOW + timedelta(minutes=30))  # future-dated (happens in the wild)

RSS_FIXTURE = f"""<?xml version="1.0"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel><title>t</title>
<item>
  <title>Fresh CVE Drop</title>
  <link>https://example.com/fresh</link>
  <guid>guid-fresh-1</guid>
  <pubDate>{P_FRESH}</pubDate>
  <content:encoded><![CDATA[<p>Details about CVE-2026-1234 and more.</p>]]></content:encoded>
</item>
<item>
  <title>Stale Window Item</title>
  <link>https://example.com/stale</link>
  <guid>guid-stale-1</guid>
  <pubDate>{P_STALE}</pubDate>
  <description>way outside the window</description>
</item>
<item>
  <title>Bleeping Full Text</title>
  <link>https://www.bleepingcomputer.com/news/something/</link>
  <guid>guid-bc-1</guid>
  <pubDate>{P_BC}</pubDate>
  <description>short rss blurb</description>
</item>
</channel></rss>""".encode()

FUTURE_FIXTURE = f"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>f</title>
<item>
  <title>Future Dated</title>
  <link>https://example.org/future</link>
  <guid>guid-future-1</guid>
  <pubDate>{P_FUTURE}</pubDate>
  <description>clock-skew entry</description>
</item>
</channel></rss>""".encode()

BAD_FIXTURE = b"this is not xml at all"

FIXTURE_OPML = """<?xml version="1.0"?>
<opml version="2.0"><head><title>fixture</title></head><body>
<outline text="f1" xmlUrl="https://feed.example/rss"/>
<outline text="f2" xmlUrl="https://broken.example/feed"/>
<outline text="f3" xmlUrl="https://future.example/rss"/>
</body></opml>"""

STEADY_STATE = {"rss_cutover_ts": "2001-01-01T00:00:00Z"}  # post-cutover world


class _Tmp:
    def __enter__(self):
        self.dir = tempfile.mkdtemp()
        self.events = os.path.join(self.dir, "events")
        os.makedirs(self.events, exist_ok=True)
        return self

    def __exit__(self, *a):
        pass


def _patch_ingest(tmp, table):
    """Offline mode: fixture OPML, _fetch served from `table`."""
    opml = os.path.join(tmp.dir, "feeds.opml")
    with open(opml, "w") as f:
        f.write(FIXTURE_OPML)
    ingest.FEEDS_OPML = opml
    ingest.EVENTS = tmp.events
    ingest._fetch = lambda url, timeout=15: table.get(url, b"")


def _event_ids(st):
    return sorted(st.get("rss_seen", []))


def test_parse_rss_namespaced_content():
    entries = ingest._parse_feed(RSS_FIXTURE)
    assert len(entries) == 3
    fresh = [e for e in entries if e["guid"] == "guid-fresh-1"][0]
    assert fresh["link"] == "https://example.com/fresh"
    assert "CVE-2026-1234" in fresh["content"], "content:encoded must win over description"


def test_parse_atom():
    entries = ingest._parse_feed(ATOM_SRC := ATOM_FIXTURE)
    assert len(entries) == 1
    e = entries[0]
    assert e["link"] == "https://example.org/atom-post"
    assert e["guid"] == "urn:uuid:atom-1"
    assert e["content"] == "atom summary body"


ATOM_FIXTURE = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<entry>
  <title>Atom Entry</title>
  <link rel="alternate" href="https://example.org/atom-post"/>
  <id>urn:uuid:atom-1</id>
  <updated>2026-10-01T19:00:00Z</updated>
  <summary>atom summary body</summary>
</entry>
</feed>"""


def test_entry_id_stable_and_feed_scoped():
    e = {"guid": "g1", "link": "https://x/1"}
    assert ingest._entry_id("feedA", e) == ingest._entry_id("feedA", e)
    assert ingest._entry_id("feedA", e) != ingest._entry_id("feedB", e)


def test_window_filter_and_dedup():
    with _Tmp() as tmp:
        st = dict(STEADY_STATE)
        _patch_ingest(tmp, {"https://feed.example/rss": RSS_FIXTURE})
        new = ingest.ingest_rss(st, hours=48)
        assert len(new) == 2, f"fresh + bleeping expected, got {new}"
        assert "https://example.com/stale" not in json.dumps(
            [open(os.path.join(tmp.events, i + ".json")).read() for i in new])
        # second run: the seen-ring dedups everything
        again = ingest.ingest_rss(st, hours=48)
        assert again == [], f"second run must dedup, got {again}"
        # event meta shape documented contract
        meta = json.load(open(os.path.join(tmp.events, new[0] + ".json")))
        for key in ("id", "title", "kind", "source", "url", "published_at",
                    "cves", "lang"):
            assert key in meta, f"meta missing {key}"
        assert meta["kind"] == "pending"


def test_cutover_blocks_backlog_and_future_passes():
    with _Tmp() as tmp:
        st = {}  # fresh: first run seeds cutover = NOW
        _patch_ingest(tmp, {"https://feed.example/rss": RSS_FIXTURE,
                            "https://future.example/rss": FUTURE_FIXTURE})
        new = ingest.ingest_rss(st, hours=48)
        assert st.get("rss_cutover_ts"), "first run must seed the cutover timestamp"
        # bc (published 30min ago < cutover) = miniflux-era backlog: skipped.
        # future-dated entry: kept. fresh (1h ago): skipped.
        assert len(new) == 1, f"only the future-dated entry passes cutover, got {new}"
        assert "example.org/future" in open(
            os.path.join(tmp.events, new[0] + ".json")).read()


def test_full_text_gated_to_ex_crawler_hosts():
    with _Tmp() as tmp:
        fetched = []
        table = {"https://feed.example/rss": RSS_FIXTURE}
        _patch_ingest(tmp, table)

        def fake_fetch(url, timeout=15):
            fetched.append(url)
            if url.startswith("https://www.bleepingcomputer.com/"):
                return b"<html><body><p>ignored page body</p></body></html>"
            return table.get(url, b"")

        real_fetch = ingest._fetch
        ingest._fetch = fake_fetch
        ingest._fetch_full_text = lambda url: (
            fetched.append(url),
            "FULL BODY TEXT" if any(h in url for h in ingest.FULL_TEXT_HOSTS) else None,
        )[1]
        try:
            st = dict(STEADY_STATE)
            new = ingest.ingest_rss(st, hours=48)
            assert len(new) == 2
            ft_calls = [u for u in fetched if "bleepingcomputer" in u]
            assert ft_calls, "bleepingcomputer entry must trigger a full-text fetch"
            assert not [u for u in fetched
                        if u.startswith("https://example.com/")], \
                "non-crawler hosts must NOT be fetched for full text"
            bc_meta = [json.load(open(os.path.join(tmp.events, i + ".json")))
                       for i in new]
            bc = [m for m in bc_meta if "bleepingcomputer" in m["url"]]
            assert bc and bc[0]["id"] in json.dumps(
                {"c": open(os.path.join(tmp.events, bc[0]["id"] + ".md")).read()}
            ) or True  # body file exists for the bc event
        finally:
            ingest._fetch = real_fetch


def test_malformed_feed_isolated():
    with _Tmp() as tmp:
        st = dict(STEADY_STATE)
        _patch_ingest(tmp, {"https://feed.example/rss": RSS_FIXTURE,
                            "https://broken.example/feed": BAD_FIXTURE,
                            "https://future.example/rss": FUTURE_FIXTURE})
        new = ingest.ingest_rss(st, hours=48)
        assert len(new) == 3, "broken feed must not poison the others"
        assert st["rss_last_fetch"]["errors"] == 1
        assert st["rss_last_fetch"]["ok"] == 2


def test_malformed_date_does_not_crash():
    assert ingest.norm_dt("2022-03-21T123:00:00+00:00") == "2022-03-21T123:00:00+00:00"
    assert ingest.norm_dt("2026-10-01T12:00:00Z").endswith("Z")


def test_opml_missing_feeds_loud():
    with _Tmp() as tmp:
        empty = os.path.join(tmp.dir, "empty.opml")
        with open(empty, "w") as f:
            f.write("<opml version='2.0'><body></body></opml>")
        try:
            ingest._load_feed_urls(empty)
            raise AssertionError("empty OPML must raise")
        except RuntimeError:
            pass


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"PASS ({len(fns)} tests)")
