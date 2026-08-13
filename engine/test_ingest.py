#!/usr/bin/env python3
"""Ingest normalization regression suite — strip_html must produce plain text
from ANY feed encoding: raw HTML, entity-encoded HTML, double-encoded entities.

Background (2026-08-13): CCyber advisories arrive via malware.news with their
body ENTITY-ENCODED — literal "&lt;div&gt; &lt;div&gt;" text, no real tags, and
sometimes double-encoded ("&amp;nbsp;"). The old strip_html only matched real
"<...>" tags, so the junk survived into content_md and showed up in story card
snippets on /stories/. unescape-until-stable + tag strip fixes all three cases.

Run: python3 engine/test_ingest.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ingest import strip_html  # noqa: E402


def check(name, got, expect, sub=None):
    if sub is not None:
        ok = sub not in got
        detail = f"  contains forbidden {sub!r}: {got[:120]!r}" if not ok else ""
    else:
        ok = got == expect
        detail = f"  got {got[:120]!r} want {expect[:120]!r}" if not ok else ""
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{detail}")
    return ok


def main():
    ok = True

    # 1. real HTML tags (pre-existing behavior)
    ok &= check("raw html stripped",
                strip_html("<p>Hello <strong>world</strong></p>"), "Hello world")

    # 2. entity-encoded HTML (the CCyber/malware.news case)
    ok &= check("entity-encoded tags stripped",
                strip_html("&lt;div&gt; &lt;p&gt;&lt;strong&gt;Serial&lt;/strong&gt; AV26-815&lt;br /&gt;body"),
                "Serial AV26-815 body")

    # 3. double-encoded entities ("&amp;nbsp;" -> nbsp -> space)
    got = strip_html("Date: August&amp;nbsp;10, 2026")
    ok &= check("double-encoded nbsp becomes space", got, "Date: August 10, 2026")

    # 4. the real stored payload (regression anchor)
    real = ("&lt;div&gt; &lt;div&gt; &lt;div&gt;&lt;p&gt;&lt;strong&gt;Serial Number:&lt;/strong&gt; "
            "AV26-815&lt;br /&gt;&lt;strong&gt;Date:&lt;/strong&gt; August 13, 2026&lt;/p&gt; As of")
    got = strip_html(real)
    ok &= check("real CCyber payload clean", got, None, sub="&lt;")
    ok &= check("real CCyber payload has no tags", got, None, sub="<")

    # 5. plain text passes through untouched
    ok &= check("plain text untouched",
                strip_html("As of August 12, 2026, WebPros is affected"), None, sub="&lt;")

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
