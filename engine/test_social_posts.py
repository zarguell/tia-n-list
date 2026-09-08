#!/usr/bin/env python3
"""Social-signal loader contract — load_social_posts combines every
platform signal file and keeps only article-bearing posts.

Background: the social layer grew reddit.json -> x.json -> masto.json
(X list + Mastodon tags joined 2026-09-08). Every platform file shares
the load-bearing field article_url, matched against story event URLs in
score.hot_score. Missing files contribute nothing; malformed entries are
skipped so one bad record can't blind the score.

Run: python3 engine/test_social_posts.py   (exit 0 = pass)
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import store  # noqa: E402

FAILURES = []


def check(name, got, expect):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}"
          + ("" if ok else f"  got {got!r} want {expect!r}"))
    if not ok:
        FAILURES.append(name)


def main():
    tmp = tempfile.mkdtemp()
    store.DATA = tmp
    json.dump([{"id": "r1", "article_url": "https://a.example/1"},
               {"id": "r2"}],  # no article_url -> dropped
              open(os.path.join(tmp, "reddit.json"), "w"))
    json.dump([{"id": "t3", "article_url": "https://b.example/2"}],
              open(os.path.join(tmp, "x.json"), "w"))
    json.dump([{"id": "m4", "article_url": "https://c.example/3"},
               "not-a-dict"],
              open(os.path.join(tmp, "masto.json"), "w"))
    # bsky.json absent entirely -> contributes nothing
    got = store.load_social_posts()
    check("combines all three present files", len(got), 3)
    check("article-bearers only",
          sorted(p["id"] for p in got), ["m4", "r1", "t3"])
    os.remove(os.path.join(tmp, "x.json"))
    with open(os.path.join(tmp, "reddit.json"), "w") as f:
        f.write("{broken json")
    got2 = store.load_social_posts()
    check("broken file + missing file = masto survivors only",
          [p["id"] for p in got2], ["m4"])

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {FAILURES}")
        sys.exit(1)
    print("ALL PASS")


if __name__ == "__main__":
    main()
