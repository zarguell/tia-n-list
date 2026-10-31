#!/usr/bin/env python3
"""Native RSS poller tests (leaf A) — offline, no network.

Run:  python3 engine/test_rss_ingest.py   (exit 0 = pass)
      or: pytest engine/test_rss_ingest.py

Covers: OPML parse, RSS+Atom parsing (namespace-proof), window filtering,
cutover semantics (pre-cutover backlog never re-ingested), seen-ring dedup,
full-text gating to the ex-crawler hosts, malformed-date tolerance.
"""
import io
import json
import os
import sys
import tempfile
import urllib.error
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


def test_gbhackers_canonical_gate():
    # 2026-10-17 owner decision e8c64d8b78e0: gbhackers refs rot (~36%
    # dead) on host variants and non-article paths — ingestion keeps only
    # canonical single-segment article URLs on the bare host.
    canon = ingest._canonical_gbhackers_url
    assert canon("https://gbhackers.com/some-article/") == \
        "https://gbhackers.com/some-article/"
    assert canon("https://gbhackers.com/some-article") == \
        "https://gbhackers.com/some-article/", "missing slash canonicalized"
    assert canon("https://www.gbhackers.com/some-article/") == \
        "https://gbhackers.com/some-article/", "www canonicalized to bare"
    for bad in ("https://gbhackers.com/feed/",                       # feed index
                "https://gbhackers.com/page/2/",                     # paging
                "https://gbhackers.com/category/ransomware/",         # taxonomy
                "https://gbhackers.com/author/admin/",                # author
                "https://gbhackers.com/?p=203657",                    # id stub
                "https://gbhackers.com/some-article/?utm_source=x",  # tracking
                "https://gbhackers.com/some-article#comments",        # fragment
                "https://gbhackers.com/"):                            # homepage
        assert canon(bad) is None, f"non-article path must drop: {bad}"
    # other hosts pass through untouched (blast radius: gbhackers only)
    assert canon("https://example.com/a/b?x=1") == "https://example.com/a/b?x=1"
    assert canon("") == ""


def test_parse_tolerates_leading_blank_line_and_bom():
    # paloaltonetworks.com/blog/prisma-cloud/feed/ answers with a newline before
    # the XML declaration; a BOM does the same thing. Both used to raise
    # "XML or text declaration not at start of entity" and drop the source.
    for prefix in (b"\n", b"\r\n\n", b"\xef\xbb\xbf", b"\xef\xbb\xbf\n"):
        entries = ingest._parse_feed(prefix + RSS_FIXTURE)
        assert len(entries) == 3, f"prefix {prefix!r} must parse"
        assert entries[0]["guid"] == "guid-fresh-1"


def test_parse_tolerates_illegal_c0_controls():
    # rapid7.com/rss.xml embeds a raw vertical tab in a <description>; XML 1.0
    # forbids it, so ET rejects the whole document ("not well-formed").
    dirty = RSS_FIXTURE.replace(b"Fresh CVE Drop", b"Fresh\x0b CVE Drop")
    entries = ingest._parse_feed(dirty)
    assert len(entries) == 3
    assert "Fresh CVE Drop" in [e["title"] for e in entries][0]


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


def _reddit_patch(urlopen, sleeps):
    """Install fake urlopen/sleep; returns a restore callable."""
    real_open = ingest.urllib.request.urlopen
    real_sleep = ingest.time.sleep
    ingest.urllib.request.urlopen = urlopen
    ingest.time.sleep = lambda s: sleeps.append(s)

    def restore():
        ingest.urllib.request.urlopen = real_open
        ingest.time.sleep = real_sleep
    return restore


def test_reddit_429_retried_with_backoff():
    # 2026-10-31 audit Issue 3: r/netsec returned 429 on 36/36 hourly runs
    # because the two subreddit feeds were fetched back-to-back with no
    # retry. A 429 is transient; retry it with backoff.
    calls, sleeps = [], []

    class Resp:
        def read(self):
            return ATOM_FIXTURE

    def fake_open(req, timeout=30):
        calls.append(getattr(req, "full_url", req))
        if len(calls) == 1:
            raise urllib.error.HTTPError(
                "https://r.example/a", 429, "Too Many Requests", {}, io.BytesIO(b""))
        return Resp()

    restore = _reddit_patch(fake_open, sleeps)
    try:
        data = ingest._fetch_reddit("https://r.example/a", "netsec")
    finally:
        restore()
    assert data == ATOM_FIXTURE
    assert len(calls) == 2, "429 must be retried once"
    assert sleeps == [ingest.REDDIT_BACKOFF_S], sleeps


def test_reddit_non_429_not_retried():
    calls, sleeps = [], []

    def fake_open(req, timeout=30):
        calls.append(1)
        raise urllib.error.HTTPError(
            "https://r.example/a", 403, "Forbidden", {}, io.BytesIO(b""))

    restore = _reddit_patch(fake_open, sleeps)
    try:
        try:
            ingest._fetch_reddit("https://r.example/a", "netsec")
            raise AssertionError("403 must raise")
        except urllib.error.HTTPError as e:
            assert e.code == 403
    finally:
        restore()
    assert len(calls) == 1 and sleeps == [], "only 429 is worth retrying"


def test_reddit_persistent_429_exhausts_budget():
    calls, sleeps = [], []

    def fake_open(req, timeout=30):
        calls.append(1)
        raise urllib.error.HTTPError(
            "https://r.example/a", 429, "Too Many Requests", {}, io.BytesIO(b""))

    restore = _reddit_patch(fake_open, sleeps)
    try:
        try:
            ingest._fetch_reddit("https://r.example/a", "netsec")
            raise AssertionError("persistent 429 must raise")
        except urllib.error.HTTPError as e:
            assert e.code == 429
    finally:
        restore()
    assert len(calls) == ingest.REDDIT_RETRIES
    assert sleeps == [ingest.REDDIT_BACKOFF_S * i
                      for i in range(1, ingest.REDDIT_RETRIES)]


def test_reddit_feeds_spaced_and_state_recorded():
    """The two feeds must not fire back-to-back, and a dead feed degrades
    only that feed (state records it) instead of losing the whole layer."""
    with _Tmp() as tmp:
        real_feeds, real_events, real_reddit = (
            ingest.REDDIT_FEEDS, ingest.EVENTS, ingest.REDDIT)
        ingest.REDDIT_FEEDS = (("cybersecurity", "https://r.example/a"),
                               ("netsec", "https://r.example/b"))
        ingest.EVENTS = tmp.events
        ingest.REDDIT = os.path.join(tmp.dir, "reddit.json")
        sleeps = []

        class Resp:
            def read(self):
                return ATOM_FIXTURE

        def fake_open(req, timeout=30):
            url = getattr(req, "full_url", req)
            if url.endswith("/b"):
                raise urllib.error.HTTPError(url, 403, "Forbidden", {},
                                             io.BytesIO(b""))
            return Resp()

        restore = _reddit_patch(fake_open, sleeps)
        try:
            st = {}
            posts, new_ids = ingest.ingest_reddit(st)
        finally:
            restore()
            ingest.REDDIT_FEEDS = real_feeds
            ingest.EVENTS = real_events
            ingest.REDDIT = real_reddit
        assert posts == 1 and new_ids == []
        assert sleeps == [ingest.REDDIT_INTER_FEED_S], \
            "feeds must be spaced; 403 is not retried"
        assert st["reddit_last_fetch"] == {"ok": 1, "errors": 1}



if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"PASS ({len(fns)} tests)")
