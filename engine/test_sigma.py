#!/usr/bin/env python3
"""Sigma gate-parity suite — author-time check must equal the publish gate.

2026-09-10: the CTI agent authored 6 Sigma rules and self-validated with
sigma.validate_sigma() (YAML shape + required keys only), reporting "all
validated clean (OK)". The publish gate in ssg.py used `sigma check`
(spec-grade) and rejected 2 of them for the non-existent `|isnot` modifier.
Agent green, gate red, site unpublished for hours (and every hourly TIA run
kept aborting on the same two files until they were fixed).

Contracts locked here:
  1. sigma.validate() catches a real spec violation (`|isnot`) that the
     structural check misses — i.e. it IS the spec-grade check;
  2. sigma.validate() accepts a well-formed rule (no false red);
  3. ssg.py's publish gate calls sigma.validate() — not the raw CLI helper or
     the structural fallback — so the two can never diverge again.

Run: python3 engine/test_sigma.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sigma  # noqa: E402

ENGINE = os.path.dirname(os.path.abspath(__file__))

GOOD_RULE = """title: Test Rule
id: 11111111-2222-3333-4444-555555555555
status: experimental
description: A structurally and spec-valid rule.
references:
  - https://example.com
author: Tia N. List
date: 2026-09-10
tags:
  - attack.t1190
logsource:
  category: network_connection
  product: windows
detection:
  selection:
    dst_port: 8443
  filter_local:
    src_ip: '127.0.0.1'
  condition: selection and not filter_local
falsepositives:
  - Legitimate admin access
level: high
"""

# The exact mistake that broke the 2026-09-10 publish. `isnot` is not a Sigma
# modifier (negation belongs in the condition as `not <selection>`); the
# structural check happily passes it.
BAD_RULE = GOOD_RULE.replace(
    "  selection:\n    dst_port: 8443\n",
    "  selection:\n    dst_port: 8443\n    src_ip|isnot: '127.0.0.1'\n")


def check(name, got, expect, detail=""):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {expect!r} {detail}")
    return ok


def main():
    ok = True
    cli = sigma._sigma_exe()
    print(f"sigma-cli: {cli or 'MISSING (spec checks skipped)'}")

    with tempfile.TemporaryDirectory() as tmp:
        good = os.path.join(tmp, "good.sigma")
        bad = os.path.join(tmp, "bad.sigma")
        open(good, "w").write(GOOD_RULE)
        open(bad, "w").write(BAD_RULE)

        ok &= check("structural check passes the bad rule (the trap)",
                    sigma.validate_sigma(bad) == [], True)
        ok &= check("validate() passes a good rule", sigma.validate(good), [])
        if cli:
            bad_errs = sigma.validate(bad)
            ok &= check("validate() rejects |isnot", len(bad_errs) > 0, True)
            ok &= check("error names the bad modifier",
                        any("isnot" in e for e in bad_errs), True,
                        detail=f"got: {[e[:60] for e in bad_errs]}")
        else:
            print("  [SKIP] spec-grade assertions (sigma-cli unavailable)")

    # The publish gate must call the shared validator, not a private path.
    ssg_src = open(os.path.join(ENGINE, "ssg.py")).read()
    lint_block = ssg_src[ssg_src.index("sigma_errs = []"):]
    ok &= check("ssg.py gate uses sigma_mod.validate()",
                bool(re.search(r"sigma_mod\.validate\(", lint_block)), True)
    ok &= check("ssg.py gate no longer picks its own check",
                bool(re.search(r"sigma_mod\.(check_with_cli|validate_sigma)\(",
                               lint_block)), False)

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
