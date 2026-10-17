#!/usr/bin/env python3
"""IOC extractor precision suite (2026-10-17, audit Rec 4 — never dispositioned).

The candidate pool was dominated by source links, victim brands, version
numbers and code fragments, while genuine defanged C2s present in the same
events were not emitted (Step 1 kept 0 IOCs for consecutive runs). Contracts:

  1. Tier-A (defanged) observables always emit: hxxp URLs, [.] hosts/IPs —
     the defang IS the IOC assertion (live exemplar: the volmira[.]site C2
     in masto:117309402320564407, previously silent).
  2. Version-shaped IPv4 never emits ("Prior to 11.1.0.2", "version 8.4.0.2").
  3. Source links never emit: bare outlet/vendor-blog/aggregator domains
     (news.ycombinator.com et al.) and markdown link-label fragments
     ("news.ycombinator" from [news.ycombinator](https://...)).
  4. Code-fragment filenames never emit (installer-3.9.2-lts.dmg, page.aspx).
  5. Bare IOC-shaped domains with no URL scheme still emit (no over-strip).

Run:  python3 engine/test_ioc.py   (exit 0 = pass)
      or: pytest engine/test_ioc.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ioc  # noqa: E402

failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


# ── 1. Tier-A: defanged C2s emit ──────────────────────────────────────────
volmira = ("via Mastodon https://hindsig.ht/unfurl/?url="
           "hxxps://volmira[.]site/api/ext?p=98d8049e")
r = ioc.extract_from_text(volmira)
check("defanged hxxp C2 emits its host", r.get("volmira.site"), "domain")

r = ioc.extract_from_text("beacon at 185.220.101[.]4 every hour")
check("defanged IPv4 emits", r.get("185.220.101.4"), "ipv4")

r = ioc.extract_from_text("stage-two hosted on shadowc2[.]net/path")
check("defanged bare host emits", r.get("shadowc2.net"), "domain")

# ── 2. version numbers never emit ─────────────────────────────────────────
r = ioc.extract_from_text(
    "Dell OpenManage Managed Node for RHEL Prior to 11.1.0.2 fixes flaws")
check("version 'Prior to 11.1.0.2' is not an IOC", "11.1.0.2" in r, False)
r = ioc.extract_from_text(
    "Switchvox version 8.4.0.2, released July 14, fixes the RCE flaw")
check("version 'version 8.4.0.2' is not an IOC", "8.4.0.2" in r, False)

# ── 3. source links never emit ────────────────────────────────────────────
r = ioc.extract_from_text(
    "as reported by news.ycombinator.com and the vendor blog at "
    "blog.trailofbits.com this week")
check("bare aggregator domain is not an IOC",
      "news.ycombinator.com" in r, False)
check("bare vendor-blog domain is not an IOC",
      "blog.trailofbits.com" in r, False)
r = ioc.extract_from_text(
    "read more [news.ycombinator](https://news.ycombinator.com/item?id=1)")
check("markdown link-label fragment is not an IOC",
      "news.ycombinator" in r, False)

# ── 4. code fragments never emit ──────────────────────────────────────────
r = ioc.extract_from_text(
    "grab zk-call-messenger-installer-3.9.2-lts.dmg and open page.aspx?id=1")
check("versioned installer filename is not an IOC",
      "zk-call-messenger-installer-3.9.2-lts.dmg" in r, False)
check("aspx page is not an IOC",
      any(v.endswith(".aspx") for v in r), False)

# ── 5. bare IOC-shaped domains still emit (no over-strip) ─────────────────
r = ioc.extract_from_text("the malware connects to evil-c2-server.com daily")
check("bare C2-shaped domain still emits",
      r.get("evil-c2-server.com"), "domain")
r = ioc.extract_from_text(
    "indicators 9.9.9.9 aside, reachable at 203.0.113.9 over TLS")
check("TEST-NET documentation IP stays excluded",
      "203.0.113.9" in r, False)

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {failures}")
    sys.exit(1)
print("all ioc precision checks passed")


def test_ioc_precision_suite():
    assert not failures
