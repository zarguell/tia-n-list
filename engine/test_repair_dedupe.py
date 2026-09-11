#!/usr/bin/env python3
"""repair_dedupe orphan-shell heal contract (2026-09-11).

The `.json`-suffixed story refs made triage mint `<slug>-2` twins, move a
shell's events into them, then the twins were dropped while the tracked shell
kept the dangling pointer. heal_orphan_shells() re-homes a stranded matching
event onto the shell, clears the pointer, and leaves healthy redirects alone.

Run: python3 engine/test_repair_dedupe.py   (exit 0 = pass)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repair_dedupe as rd  # noqa: E402

failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


def story(sid, events=(), merged_into=None, title=None):
    return {"id": sid, "title": title or sid,
            "events": [{"event_id": e} for e in events],
            "merged_into": merged_into}


stories = {
    "jfrog-shell": story(
        "jfrog-shell", merged_into="jfrog-shell-2",
        title="JFrog Artifactory Vulnerabilities Actively Exploited in the Wild"),
    "shield-shell": story(
        "shield-shell", merged_into="shield-shell-2",
        title="ShieldCrash Zero-Day Bypasses Microsoft Defender Patches"),
    "stable": story("stable", ["live-evt"], title="Stable story"),
    "live-target": story("live-target", ["x"], title="Live target"),
    "kept-shell": story("kept-shell", merged_into="live-target", title="Kept shell"),
}
events = {
    "stranded-jfrog": {
        "id": "stranded-jfrog",
        "title": "JFrog Artifactory Vulnerabilities Actively Exploited in the Wild",
        "excluded": False,
    },
    "stranded-other": {
        "id": "stranded-other", "title": "Unrelated topic", "excluded": False,
    },
    "stranded-excluded": {
        "id": "stranded-excluded", "title": "JFrog Artifactory Vulnerabilities",
        "excluded": True,
    },
}
log = []
rd.heal_orphan_shells(stories, events, log)

check("dangling pointer cleared", "merged_into" not in stories["jfrog-shell"], True)
check("matching stranded event recovered",
      [r["event_id"] for r in stories["jfrog-shell"]["events"]], ["stranded-jfrog"])
check("non-matching orphan becomes an eventless live story",
      (stories["shield-shell"].get("merged_into"), stories["shield-shell"]["events"]),
      (None, []))
check("healthy redirect left alone", stories["kept-shell"]["merged_into"], "live-target")
check("excluded event is never recovered",
      any(r["event_id"] == "stranded-excluded"
          for s in stories.values() for r in s.get("events", [])), False)
check("live story's events untouched",
      [r["event_id"] for r in stories["stable"]["events"]], ["live-evt"])
check("heal is logged", len(log), 2)

print()
if failures:
    print(f"FAIL: {len(failures)} repair checks failed")
    sys.exit(1)
print("ALL PASS")
