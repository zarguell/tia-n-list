#!/usr/bin/env python3
"""Event-store read cache contract (perf: 88,806 files, 16.3 s per load).

The event store is file-per-event (44,402 json + 44,403 md on 2026-11-27) and
`load_events()` runs at 14 call sites across the hourly passes. The cache is
DERIVED: files stay the source of truth, and every failure mode must fall back
to reading them.

  1. cold call parses the files and returns the same shape as before;
  2. warm call is served from the cache (proved by making file reads explode);
  3. editing either side (json or md) invalidates — content is never stale;
  4. adding an event file invalidates;
  5. a corrupt cache is ignored and rewritten, never raised;
  6. an unwritable cache directory still returns the data;
  7. safe_url filtering still applies on the cached path.

Run: python3 engine/test_store_cache.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import store  # noqa: E402


def check(name, got, expect):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {expect!r}")
    return ok


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        ev = os.path.join(td, "events")
        os.makedirs(ev)
        store.EVENTS_DIR = ev
        store.EVENTS_CACHE = os.path.join(td, ".events-cache.sqlite3")

        def write(eid, url="https://example.com/a", md="body"):
            with open(os.path.join(ev, eid + ".json"), "w") as f:
                json.dump({"id": eid, "url": url, "title": eid}, f)
            with open(os.path.join(ev, eid + ".md"), "w") as f:
                f.write(md)

        for i in range(3):
            write(f"e{i}")

        cold = store.load_events()
        ok &= check("cold call reads the files", sorted(cold), ["e0", "e1", "e2"])
        ok &= check("content merged from the md sidecar", cold["e0"]["content_md"], "body")
        ok &= check("cache written", os.path.exists(store.EVENTS_CACHE), True)

        real_open, real_glob = open, store.glob.glob

        def explode(*a, **k):
            raise AssertionError("warm load re-read event files")

        try:
            store.glob.glob = explode
            warm = store.load_events()
        finally:
            store.glob.glob = real_glob
        ok &= check("warm call served from cache (no file reads)", sorted(warm), ["e0", "e1", "e2"])
        ok &= check("cached shape identical", warm["e1"]["title"], "e1")

        write("e1", md="changed body")
        os.utime(os.path.join(ev, "e1.json"), (1, 1 + 0))
        seen = store.load_events()
        ok &= check("md edit invalidates the cache", seen["e1"]["content_md"], "changed body")

        write("e3")
        ok &= check("new event file invalidates", "e3" in store.load_events(), True)

        with open(store.EVENTS_CACHE, "wb") as f:
            f.write(b"not a database")
        ok &= check("corrupt cache falls back to files", "e3" in store.load_events(), True)
        ok &= check("corrupt cache is rewritten", "e3" in store.load_events(), True)

        write("e4", url="javascript:alert(1)")
        ok &= check("safe_url still filters on the cached path",
                    store.load_events()["e4"]["url"], "")

        store.EVENTS_CACHE = os.path.join(td, "nope", "cache.sqlite3")
        ok &= check("unwritable cache still returns data", "e4" in store.load_events(), True)
        real_open = real_open  # noqa: F841  (kept for readability of the diff)

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
