#!/usr/bin/env python3
"""Triage gate contract suite — schema-drift tolerance + no-duplicate-twin apply.

The 2026-08-17..24 incident: the hourly model wrote decision files in drifted
shapes (top-level "events" or "keep"/"drop", per-event "story_id", string
exploitation values). triage.apply() silently discarded them or minted "-2"
twin stories because keeps with no recognized "story" created a NEW story
while the mechanical story kept the event. This suite pins:

  1. _normalize_decisions recovers every drift variant seen in the wild.
  2. apply() never leaves one event in two active stories.
  3. apply() reuses the mechanical sole-holder story instead of minting -2.
  4. emptied shells redirect (merged_into) instead of ghosting.

Run: python3 engine/test_triage.py   (exit 0 = pass)
Wired into CI (site-deploy.yml).
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


import triage  # noqa: E402

# ── 1. normalize: documented schema + drift variants ─────────────────────────
dec, merges, ign = triage._normalize_decisions({
    "decisions": [{"event_id": "e1", "action": "keep", "story": "s1",
                   "exploitation": {"CVE-2026-1": {"status": "exploited", "evidence": "x"}}}],
    "merges": [{"from": "a", "into": "b"}]})
check("canonical schema parsed", (len(dec), len(merges), ign), (1, 1, 0))
check("exploitation object kept", dec[0]["exploitation"]["CVE-2026-1"]["status"], "exploited")

dec, merges, ign = triage._normalize_decisions({
    "events": [{"id": "e2", "action": "keep", "story_id": "s2",
                "rationale": "r", "exploitation": {"CVE-2026-2": "suspected"}}]})
check("events/story_id drift parsed", (len(dec), ign), (1, 0))
check("story_id -> story", dec[0]["story"], "s2")
check("string exploitation normalized", dec[0]["exploitation"]["CVE-2026-2"]["status"], "suspected")

dec, merges, ign = triage._normalize_decisions(
    {"keep": [{"id": "e3", "story": "s3"}], "drop": [{"id": "e4"}]})
check("keep/drop lists parsed", ([d["action"] for d in dec], ign), (["keep", "drop"], 0))

dec, merges, ign = triage._normalize_decisions(
    {"decisions": [{"title": "no id"}, {"event_id": "e5", "action": "maybe"}]})
check("junk entries counted, not applied", (len(dec), ign), (0, 2))

# ── 2-4. end-to-end apply on a sandbox store ─────────────────────────────────
tmp = tempfile.mkdtemp()
try:
    for var, sub in [("EVENTS", "events"), ("STORIES", "stories"),
                     ("ANALYSIS", "analysis"), ("TRIAGE", "triage")]:
        d = os.path.join(tmp, sub)
        os.makedirs(d)
        setattr(triage, var, d)
    setattr(triage, "STATE", os.path.join(tmp, "triage", "state.json"))
    setattr(triage, "NEEDS", os.path.join(tmp, "needs-analysis.json"))
    setattr(triage, "DATA", tmp)

    # mechanical state: story "mech" holds ONLY e1 (merge.py's fresh mint);
    # story "dup" holds e2, same slug-base twin pattern
    for eid in ("e1", "e2"):
        json.dump({"id": eid, "title": f"T {eid}", "source": "x", "url": "",
                   "published_at": "2026-08-24T10:00:00Z", "cves": [], "kind": "original"},
                  open(os.path.join(tmp, "events", f"{eid}.json"), "w"))
    for sid, evs in [("mech", ["e1"]), ("existing", ["e9"]), ("dup", ["e2"])]:
        json.dump({"id": sid, "title": f"Story {sid}", "first_seen": "2026-08-20T00:00:00Z",
                   "last_seen": "2026-08-24T10:00:00Z", "sources": ["x"], "n_sources": 1,
                   "cves": [], "score": 5.0, "reddit_signal": {"posts": 0, "best_score": 0},
                   "events": [{"event_id": e, "label": "original"} for e in evs]},
                  open(os.path.join(tmp, "stories", f"{sid}.json"), "w"))
    json.dump({"id": "e9", "title": "T e9", "source": "x", "url": "",
               "published_at": "2026-08-20T00:00:00Z", "cves": [], "kind": "original"},
              open(os.path.join(tmp, "events", "e9.json"), "w"))

    # contamination probe: mech also absorbed a stale event e_stale (newer
    # timestamp + CVE) that a later strip must roll back out of derived fields
    json.dump({"id": "e_stale", "title": "T stale", "source": "y", "url": "",
               "published_at": "2026-08-24T23:00:00Z", "cves": ["CVE-2026-99999"],
               "kind": "update"}, open(os.path.join(tmp, "events", "e_stale.json"), "w"))
    mech = json.load(open(os.path.join(tmp, "stories", "mech.json")))
    mech["events"].append({"event_id": "e_stale", "label": "update"})
    mech["cves"] = ["CVE-2026-99999"]
    mech["last_seen"] = "2026-08-24T23:00:00Z"
    json.dump(mech, open(os.path.join(tmp, "stories", "mech.json"), "w"))

    # drifted decisions: top-level "events", "story_id", one NEW for an event
    # merge.py already placed, one merge for the twin
    decfile = os.path.join(tmp, "decisions.json")
    json.dump({"events": [
        {"id": "e_stale", "action": "keep", "story_id": "existing"},
        {"id": "e1", "action": "keep", "story_id": "existing"},
        {"id": "e2", "action": "keep", "story_id": "NEW",
         "story_title": "Clean Title"}],
        "merges": [{"from": "dup", "into": "mech"}]}, open(decfile, "w"))

    # stub the heavy store/score rescore tail with real-module equivalents
    import store as store_mod
    store_mod.load_events = lambda: {
        e["id"]: e for e in (json.load(open(os.path.join(tmp, "events", f"{e}.json")))
                             for e in ("e1", "e2", "e9"))}
    import score as score_mod
    score_mod.hot_score = lambda s, ev, rd: {"score": 5.0}

    triage.apply(decfile)

    st = {sid: json.load(open(os.path.join(tmp, "stories", f"{sid}.json")))
          for sid in ("mech", "existing", "dup")}
    check("e1 reassigned to existing (e2 joins via later merge)",
          [r["event_id"] for r in st["existing"]["events"]],
          ["e9", "e_stale", "e1", "e2"])
    check("stale derived fields rolled back on strip",
          (st["mech"]["last_seen"], st["mech"]["cves"]),
          ("2026-08-24T10:00:00Z", []))
    check("e1 stripped from mechanical story", st["mech"]["events"], [])
    check("emptied mech redirects", st["mech"].get("merged_into"), "existing")
    check("no -2 twin minted", sorted(os.listdir(os.path.join(tmp, "stories"))),
          ["dup.json", "existing.json", "mech.json"])
    # merge targeted mech, which had just become a shell -> resolved to existing
    check("merge into shell resolves through redirect", st["dup"].get("merged_into"), "existing")
    check("e2 landed on the live canonical story",
          sorted(r["event_id"] for r in st["existing"]["events"]),
          ["e1", "e2", "e9", "e_stale"])
finally:
    shutil.rmtree(tmp)

print()
if failures:
    print(f"FAIL: {len(failures)} triage checks failed")
    sys.exit(1)
print("ALL PASS")
