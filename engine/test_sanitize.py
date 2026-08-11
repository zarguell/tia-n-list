#!/usr/bin/env python3
"""Sanitizer regression suite — every payload must come out with no live
handlers, no active-element tags, and no dangerous URL schemes.

Run: python3 engine/test_sanitize.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh. The 2026-08-11 audit
proved the old regex sanitizer bypassable; this suite guards the bleach
allowlist against regressions, INCLUDING the audit's verified bypasses:
slash-prefixed handlers, entity-encoded schemes, non-href active attributes.
"""
import html.parser
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ssg as ssg_mod  # noqa: E402


class Scanner(html.parser.HTMLParser):
    """Collect start tags + their attributes (handles <svg/onload=...> as
    <svg> with an onload attribute — the browser semantics)."""

    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_startendtag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


ACTIVE_TAGS = {"script", "style", "iframe", "object", "embed", "svg", "math",
               "form", "meta", "link", "base"}
DANGEROUS_ATTRS = {"action", "formaction", "xlink:href"}


def live_content(out):
    """Return (tag, attr, value) of any live active content in sanitized HTML."""
    bad = []
    s = Scanner()
    try:
        s.feed(out)
    except Exception:
        return [("PARSE", "", out[:60])]
    for tag, attrs in s.tags:
        t = tag.lower()
        if t in ACTIVE_TAGS:
            bad.append((t, "", ""))
        for k, v in attrs.items():
            kl, vl = k.lower(), (v or "").lstrip().lower()
            if kl.startswith("on"):
                bad.append((t, kl, v[:40]))
            if kl in DANGEROUS_ATTRS or kl == "href":
                if vl.startswith(("javascript:", "vbscript:", "data:")):
                    bad.append((t, kl, v[:40]))
    return bad


PAYLOADS = [
    # audit-verified regex bypasses (2026-08-11)
    "<svg/onload=alert(1)>",
    "<img src=x /onerror=alert(1)>",
    '<a href="jav&#x61;script:alert(1)">x</a>',
    '<a href="javascript&colon;alert(1)">x</a>',
    '<a href="java&#115;cript:alert(1)">x</a>',
    '<form action="javascript:alert(1)"><button>go</button></form>',
    '<svg><a xlink:href="javascript:alert(1)">x</a></svg>',
    # classic corpus
    "<script>alert(1)</script>",
    "<script src=x></script>",
    "<style>body{display:none}</style>",
    "<iframe src=x></iframe>",
    "<object data=x></object>",
    "<embed src=x>",
    '<img src=x onerror=alert(1)>',
    '<a href="javascript:alert(1)">x</a>',
    '<a href="vbscript:msgbox(1)">x</a>',
    '<a href="data:text/html,<script>alert(1)</script>">x</a>',
    '<a href="JaVaScRiPt:alert(1)">x</a>',
    '<a href="  javascript:alert(1)">x</a>',
    '<a href="java&#x09;script:alert(1)">x</a>',          # tab inside scheme
    '<div onmouseover="alert(1)">hover</div>',
    "<svg><script>alert(1)</script></svg>",
    '<math><mtext></mtext><annotation-xml encoding="text/html"><script>alert(1)</script></annotation-xml></math>',
]

# prose that QUOTES handler syntax must survive intact (the regex sanitizer
# corrupted text nodes; bleach only filters inside tags)
PROSE = 'The payload was an "onclick=alert(1)" string and a javascript: URL.'


def main():
    fails = []
    for p in PAYLOADS:
        out = ssg_mod.sanitize(p)
        bad = live_content(out)
        if bad:
            fails.append((p, out, bad))
    out = ssg_mod.sanitize(PROSE)
    if "onclick=alert(1)" not in out or "javascript:" not in out:
        fails.append(("PROSE-KEEP", PROSE, out))
    if fails:
        print(f"SANITIZER FAIL ({len(fails)}/{len(PAYLOADS) + 1}):")
        for p, out, bad in fails:
            print(f"  payload: {p!r}\n    -> {out!r}\n    live: {bad}")
        sys.exit(1)
    print(f"sanitizer: {len(PAYLOADS)} payloads + prose all clean")
    # bleach must be present (CI installs it; a missing dep = hard fail, not silent)
    assert ssg_mod.bleach, "bleach import missing"


if __name__ == "__main__":
    main()
