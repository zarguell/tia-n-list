#!/usr/bin/env python3
"""Judgment-layer audit contract suite (2026-08-24).

The triage-drift incident (Aug 17-24) produced duplicates the output-level
audit could not see. This suite pins the audit_checks contracts so the
auditor catches that failure class same-day:

  1. dedup_invariants FAILs on: multi-referenced events, merged_into cycles,
     events inside redirect shells, same-base slug duplicates; distinct
     advisory codes exonerate same-base collisions; ghosts stay informational.
  2. duplicate_suspects finds real near-dups, excludes actor-only matches
     (one shared token) and distinct-advisory pairs.
  3. language_scan flags CJK/Cyrillic bleed, ignores accents/emoji.
  4. triage_telemetry detects WARN drift, silent drift (runs, no decisions),
     and permissive triage; clean 24h passes.
  5. digest_overrides aggregates across digests.

Run: python3 engine/test_audit.py   (exit 0 = pass)
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_checks as jc  # noqa: E402

NOW = datetime(2026, 8, 24, 13, 0, tzinfo=timezone.utc)
failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


def story(sid, events=(), merged_into=None, title=None, last_seen="2026-08-24T00:00:00Z",
          first_seen="2026-08-20T00:00:00Z"):
    return {"id": sid, "title": title or sid, "events": [{"event_id": e} for e in events],
            "merged_into": merged_into, "last_seen": last_seen, "first_seen": first_seen}


# ── 1. dedup_invariants ───────────────────────────────────────────────────────
ok, detail, ghosts = jc.dedup_invariants({
    "clean-a": story("clean-a", ["e1"], title="Citrix NetScaler flaw exploited"),
    "clean-b": story("clean-b", ["e2"], title="Clop ransomware hits Acme Corp"),
})
check("clean store passes", (ok, ghosts), (True, 0))

ok, d, _ = jc.dedup_invariants({
    "a": story("a", ["e1"]), "b": story("b", ["e1"]),
})
check("multi-referenced event fails", ok, False)

ok, d, _ = jc.dedup_invariants({
    "a": story("a", [], merged_into="b"),
    "b": story("b", [], merged_into="a"),
})
check("redirect cycle fails", ok, False)

ok, d, _ = jc.dedup_invariants({
    "shell": story("shell", ["e1"], merged_into="live"),
    "live": story("live", ["e1", "e2"]),
})
check("event inside redirect shell fails", ok, False)

ok, d, _ = jc.dedup_invariants({
    "foo-2": story("foo-2", ["e1"], title="Critical WordPress Pods flaw exploited"),
    "foo": story("foo", ["e2"], title="Critical WordPress Pods flaw exploited in attacks"),
})
check("same-base duplicate fails", ok, False)

ok, d, ghosts = jc.dedup_invariants({
    "apple-security-advisory-av26-839": story("apple-security-advisory-av26-839", ["e1"],
                                              title="Apple security advisory (AV26-839)"),
    "apple-security-advisory-av26-823": story("apple-security-advisory-av26-823", ["e2"],
                                              title="Apple security advisory (AV26-823)"),
    "ghost": story("ghost", [], title="dropped long ago"),
})
check("distinct advisory codes exonerate; ghost informational only", (ok, ghosts), (True, 1))

# ── 2. duplicate_suspects ────────────────────────────────────────────────────
stories = {
    "chrome-151-a": story("chrome-151-a", ["e1"], title="Google Chrome 151 Update Fixes 5 High Severity Flaws"),
    "chrome-151-b": story("chrome-151-b", ["e2"], title="Google Chrome 151 Patches Critical Use-After-Free Vulnerability"),
    "clop-aol": story("clop-aol", ["e3"], title="Clop ransomware strikes AOL.com"),
    "clop-fis": story("clop-fis", ["e4"], title="Clop ransomware targets FIS Global"),
    "av-791": story("av-791", ["e5"], title="HashiCorp security advisory AV26-791 critical flaws"),
    "av-797": story("av-797", ["e6"], title="HashiCorp security advisory AV26-797 critical flaws"),
    "old": story("old", ["e7"], title="Google Chrome 151 Update Fixes 5 High Severity Flaws",
                 last_seen="2025-01-01T00:00:00Z"),
}
s = jc.duplicate_suspects(stories, NOW)
pairs = {frozenset((x["a"], x["b"])) for x in s}
check("real near-dup suspected", frozenset(("chrome-151-a", "chrome-151-b")) in pairs, True)
check("actor-only match not suspected", frozenset(("clop-aol", "clop-fis")) in pairs, False)
check("distinct advisory codes not suspected", frozenset(("av-791", "av-797")) in pairs, False)
check("stale story outside window", any("old" in p for p in pairs), False)

# ── 3. language_scan ─────────────────────────────────────────────────────────
tmp = tempfile.mkdtemp()
os.makedirs(os.path.join(tmp, "analysis"))
os.makedirs(os.path.join(tmp, "digests"))
open(os.path.join(tmp, "analysis", "clean.md"), "w").write(
    "Plain English with café, naïve, and emoji 🔴 headline. Fine.")
open(os.path.join(tmp, "analysis", "bleed.md"), "w").write(
    "The actor conducted 勒索 for payment via bitcoin.")
open(os.path.join(tmp, "digests", "2026-08-23.md"), "w").write(
    "Cyrillic bleed: атака on utility.")
hits = jc.language_scan(tmp)
check("cjk and cyrillic flagged, accents/emoji ignored",
      (len(hits), "bleed.md" in hits[0], "2026-08-23.md" in hits[1]), (2, True, True))

# ── 4. triage_telemetry ──────────────────────────────────────────────────────
tlog = tempfile.mkdtemp()
tdir = tempfile.mkdtemp()
today = NOW.strftime("%Y-%m-%d")
open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n"
    "triage applied: 4 kept/moved, 1 dropped, 5 merges, needs-analysis 1\n"
    "  WARN: 2 decision entries could not be parsed\n")
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("drift WARN detected", any("unparsed" in p for p in problems), True)

open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n"
    "triage applied: 0 kept/moved, 0 dropped, 0 merges\n")
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("silent drift detected", any("silent drift" in p for p in problems), True)

open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n")
json.dump({"decisions": [{"action": "keep"} for _ in range(20)]},
          open(os.path.join(tdir, "decisions-x.json"), "w"))
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("permissive triage detected", any("permissive" in p for p in problems), True)

open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n")
json.dump({"decisions": [{"action": "keep"} for _ in range(14)] +
                    [{"action": "drop"} for _ in range(6)]},
          open(os.path.join(tdir, "decisions-x.json"), "w"))
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("healthy triage passes", problems, [])
check("ratio reported", "keep/drop 14/6 (70% keep)" in info, True)

# ── 5. digest_overrides ──────────────────────────────────────────────────────
ddir = os.path.join(tmp, "digests")
json.dump({"stories": [], "overrides": [
    {"slug": "a", "action": "wildcard", "why": "regional scoop"}]},
    open(os.path.join(ddir, "2026-08-23.json"), "w"))
json.dump({"stories": []}, open(os.path.join(ddir, "2026-08-24.json"), "w"))
ov = jc.digest_overrides(tmp)
check("overrides aggregated newest-first",
      [(o["digest"], o["action"]) for o in ov], [("2026-08-23", "wildcard")])

print()
if failures:
    print(f"FAIL: {len(failures)} audit checks failed")
    sys.exit(1)
print("ALL PASS")
