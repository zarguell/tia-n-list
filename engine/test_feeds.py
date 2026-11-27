#!/usr/bin/env python3
"""Feed window contract suite — feed-all is count-capped, newest-first.

2026-11-27: /feeds/feed-all.xml carried EVERY event ever published — 17,352
items / 12.8 MB — while being rebuilt hourly. A reader polling hourly
downloaded the whole 12.8 MB per change (~9 GB/month per subscriber), so
eleven such readers would exhaust GitHub Pages' entire 100 GB/month soft
bandwidth budget with nothing in the telemetry to show it (the site has no
analytics). The feed is a follow stream; /stories/ and the per-event pages are
the archive. Contract:

  1. feed-all carries at most FEED_ALL_LIMIT items;
  2. the cap keeps the NEWEST items — never the oldest;
  3. ordering stays newest-first after the cap;
  4. the cap is global across stories (a story with many updates competes for
     the window instead of being handed its own quota);
  5. under-limit corpora are passed through whole (the cap never pads or cuts
     a feed that fits);
  6. the rendered XML stays inside a byte budget — the regression guard is the
     bandwidth bill, not just the count;
  7. feed-hot keeps every qualifying story: the cap belongs to feed-all only.

Run: python3 engine/test_feeds.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import os
import sys
from email.utils import parsedate_to_datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ssg  # noqa: E402

# The rendered feed must stay well under a megabyte even at the cap. Measured
# 2026-11-27: ~731 bytes per item in the real corpus, so 500 items ≈ 365 KB.
# 512 KiB leaves room for longer snippets without admitting a 12 MB feed back.
FEED_ALL_BYTE_BUDGET = 512 * 1024


def card(sid, events, score=6.0):
    """Minimal card shape feed_all_items/feed_hot_items consume."""
    return {"id": sid, "title": f"Story {sid}", "url": f"stories/{sid}/",
            "score": score, "last_seen": "2026-11-27T00:00:00Z",
            "snippet": f"Snippet for {sid}.", "events": events}


def event(sid, n, published):
    return {"title": f"Story {sid} event {n}", "url": f"stories/{sid}/#{n}",
            "pub_date": ssg.rfc2822(published), "published_at": published,
            "snippet": f"Snippet for {sid} event {n}."}


def iso(day, hour=0):
    return f"2026-11-{day:02d}T{hour:02d}:00:00Z"


def check(name, got, expect, detail=""):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {expect!r} {detail}")
    return ok


def main():
    ok = True
    limit = ssg.FEED_ALL_LIMIT

    # ---- 1. cap holds, and the constant stays in a sane band ----
    # A count cap, not a day window: the bound must survive a doubling of the
    # publishing rate, so assert the knob itself cannot be raised to "all".
    ok &= check("FEED_ALL_LIMIT is a real bound", 1 <= limit <= 2000, True,
                f"limit={limit}")
    big = [card(f"s{i}",
                [event(f"s{i}", j, iso(1 + (i * 3 + j) % 27, (i + j) % 24))
                 for j in range(3)])
           for i in range(600)]                     # 1,800 events, all > limit
    items = ssg.feed_all_items(big)
    ok &= check("feed-all capped at the limit", len(items), limit)
    ok &= check("feed-all keeps one item per event", len(items) == limit, True)

    # ---- 2/3. the window is the newest items, still newest-first ----
    stamps = [i["pub_date"] for i in items]
    parsed = [parsedate_to_datetime(s) for s in stamps]
    ok &= check("feed-all is newest-first after the cap",
                all(a >= b for a, b in zip(parsed, parsed[1:])), True)
    all_stamps = sorted((parsedate_to_datetime(e["pub_date"])
                         for c in big for e in c["events"]), reverse=True)
    ok &= check("feed-all window is the newest tail, not the oldest head",
                parsed[0] == all_stamps[0] and parsed[-1] == all_stamps[limit - 1],
                True, f"newest={parsed[0]} oldest_kept={parsed[-1]}")

    # ---- 4. global window: one noisy story cannot reserve a quota ----
    noisy = [card("noisy", [event("noisy", j, iso(27, j % 24)) for j in range(limit * 2)])]
    quiet = [card(f"q{i}", [event(f"q{i}", 0, iso(2, 0))]) for i in range(50)]
    mixed = ssg.feed_all_items(noisy + quiet)
    ok &= check("global window: only the newest limit events survive",
                len(mixed), limit)
    ok &= check("global window excludes older stories when the noisy one fills it",
                all(i["link"].startswith("stories/noisy/") for i in mixed), True,
                f"kept={sorted({i['link'].split('/')[1] for i in mixed})[:3]}")

    # ---- 5. under-limit corpora pass through untouched ----
    small = [card(f"t{i}", [event(f"t{i}", 0, iso(1 + i, 0))]) for i in range(5)]
    got = ssg.feed_all_items(small)
    ok &= check("under-limit feed is not padded or trimmed", len(got), 5)
    ok &= check("under-limit feed is newest-first",
                [i["link"] for i in got],
                [f"stories/t{i}/#0" for i in range(4, -1, -1)])

    # ---- 6. rendered XML byte budget (the actual regression: 12.8 MB) ----
    rendered = ssg.env.get_template("feed.xml").render(feed={
        "title": "Tia N. List — Every article",
        "description": f"The newest {limit} articles, newest first.",
        "self": "/feeds/feed-all.xml",
        "last_build": ssg.format_datetime(ssg.datetime.now(ssg.timezone.utc)),
        "entries": items,
    })
    n_bytes = len(rendered.encode("utf-8"))
    ok &= check(f"rendered feed-all under {FEED_ALL_BYTE_BUDGET // 1024} KiB",
                n_bytes < FEED_ALL_BYTE_BUDGET, True, f"bytes={n_bytes}")
    ok &= check("rendered feed-all has exactly one <item> per entry",
                rendered.count("<item>"), limit)

    # ---- 7. feed-hot is untouched by the cap ----
    hot_cards = [card(f"h{i}", [event(f"h{i}", 0, iso(1 + i % 25, i % 24))],
                      score=ssg.HOT_THRESHOLD + 1) for i in range(60)]
    hot_cards.append(card("cold", [event("cold", 0, iso(1, 0))],
                          score=ssg.HOT_THRESHOLD - 1))
    hot = ssg.feed_hot_items(hot_cards)
    ok &= check("feed-hot keeps every hot story (no cap applied)", len(hot), 60)
    ok &= check("feed-hot still drops sub-threshold stories",
                any("cold" in i["link"] for i in hot), False)

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
