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
  5. keeps naming an unknown (LLM-invented) story id mint ONCE and further
     keeps naming the same id consolidate into that story (2026-09-16:
     four Oracle CPU keeps fragmented into four 1-event stories).
  6. collect() surfaces CVE-sharing and title-overlap stories as candidates
     even when they fell out of the recency top-40 (the Oracle fragments
     were invisible to the LLM because candidates are recency-ranked).

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

# ── 1b. story refs: agents write the FILE they read, not the bare id ────────
# 2026-09-11: nine keep decisions carried a ".json" suffix, triage saw
# "unknown story", minted nine "-2" twins, and the duplicates broke the digest
# backlink lint -> publish aborted every hour while they stayed uncommitted.
for raw, want in (("foo.json", "foo"),
                  ("engine/data/stories/bar.json", "bar"),
                  ("  baz.json  ", "baz"),
                  ('"qux.json"', "qux"),
                  ("plain", "plain"),
                  ("NEW", "NEW")):
    check(f"story ref {raw!r} -> {want!r}", triage._clean_story_ref(raw), want)
check("non-string story ref untouched", triage._clean_story_ref(None), None)

_nd, _nm, _ = triage._normalize_decisions({
    "decisions": [{"event_id": "e6", "action": "keep", "story": "foo.json"},
                  {"event_id": "e7", "action": "keep", "story_id": "bar.json"}],
    "merges": [{"from": "dup.json", "into": "engine/data/stories/mech.json"}]})
check("decision story refs de-suffixed", [d["story"] for d in _nd], ["foo", "bar"])
check("merge refs de-suffixed", _nm[0], {"from": "dup", "into": "mech"})

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

# ── 5. hallucinated story ids: one mint, every keep consolidates into it ────
# 2026-09-16: the LLM kept four Oracle CPU events into a story id it invented
# (`oracle-september-2026-cpu-patches-672-cves` — not in candidates). apply()
# minted a separate story PER EVENT, the CPU coverage fragmented across four
# 1-event stories, and the story missed the daily digest. Contract: the first
# keep naming an unknown id mints ONCE (honouring story_title); every further
# keep naming the same id absorbs into that same story.
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

    GHOST = "oracle-september-2026-cpu-patches-672-cves"
    for eid in ("o1", "o2", "o3"):
        json.dump({"id": eid, "title": f"Oracle CPU coverage {eid}",
                   "source": "x", "url": f"https://x.test/{eid}",
                   "published_at": "2026-09-15T21:00:00Z", "cves": [],
                   "kind": "original"},
                  open(os.path.join(tmp, "events", f"{eid}.json"), "w"))
    decfile = os.path.join(tmp, "decisions.json")
    json.dump({"decisions": [
        {"event_id": "o1", "action": "keep", "story": GHOST,
         "story_title": "Oracle September 2026 CPU patches 672 CVEs"},
        {"event_id": "o2", "action": "keep", "story": GHOST},
        {"event_id": "o3", "action": "keep", "story": GHOST}],
        "merges": []}, open(decfile, "w"))

    import store as store_mod
    store_mod.load_events = lambda: {
        e["id"]: e for e in (json.load(open(os.path.join(tmp, "events", f"{e}.json")))
                             for e in ("o1", "o2", "o3"))}
    import score as score_mod
    score_mod.hot_score = lambda s, ev, rd: {"score": 5.0}

    triage.apply(decfile)

    files = sorted(os.listdir(os.path.join(tmp, "stories")))
    check("exactly ONE story minted for the hallucinated id", len(files), 1)
    minted = json.load(open(os.path.join(tmp, "stories", files[0])))
    check("minted title from the decision's story_title",
          minted["title"], "Oracle September 2026 CPU patches 672 CVEs")
    check("all three events landed in the one minted story",
          sorted(r["event_id"] for r in minted["events"]), ["o1", "o2", "o3"])
finally:
    shutil.rmtree(tmp)

# ── 6. collect(): affinity candidates beat the recency top-40 ───────────────
# 2026-09-16: candidates were the 40 most-recently-seen live stories, so a
# fragment that went quiet overnight was never shown to the LLM — coverage of
# the same story kept minting NEW fragments. Contract: stories sharing a CVE
# with an incoming event, or overlapping its title (>= 0.25 jaccard), appear
# as candidates even when recency excluded them.
from datetime import datetime, timezone as _tz  # noqa: E402
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
    NOW = datetime(2026, 9, 16, 12, 0, tzinfo=_tz.utc)
    triage.NOW = NOW

    def wstory(sid, title, last_seen, cves=None):
        json.dump({"id": sid, "title": title, "first_seen": last_seen,
                   "last_seen": last_seen, "cves": cves or [], "score": 0.0,
                   "sources": ["x"], "n_sources": 1,
                   "reddit_signal": {"posts": 0, "best_score": 0},
                   "events": [{"event_id": sid + "-e", "label": "original"}]},
                  open(os.path.join(tmp, "stories", f"{sid}.json"), "w"))

    # 40 decoys, all fresher than the two targets: recency top-40 = decoys only
    for i in range(40):
        wstory(f"decoy{i:02d}", f"Unrelated story number {i} about other things",
               "2026-09-16T11:00:00Z")
    # quiet targets: > 3d old, score 0 — invisible to the recency/threshold fill
    wstory("oracle-cpu-fragment", "Oracle September 2026 CPU addresses 672 CVEs",
           "2026-09-11T21:00:00Z", cves=["CVE-2026-87286"])
    wstory("zeta-ransomware-spree", "Zeta Corp ransomware spree widens",
           "2026-09-12T09:00:00Z")

    events = {
        "new-cve-event": {"id": "new-cve-event", "title": "Oracle CPU coverage",
                          "url": "https://x.test/a", "source": "x",
                          "published_at": "2026-09-16T10:00:00Z",
                          "cves": ["CVE-2026-87286"], "excluded": False},
        "new-zeta-event": {"id": "new-zeta-event",
                           "title": "Zeta Corp ransomware hits fourth hospital",
                           "url": "https://x.test/b", "source": "x",
                           "published_at": "2026-09-16T10:30:00Z",
                           "cves": [], "excluded": False},
    }
    import store as store_mod
    store_mod.load_events = lambda: events
    triage.collect()

    ctx_path = os.path.join(tmp, "triage", f"context-{triage.RUN_TAG}.json")
    ctx = json.load(open(ctx_path))
    ids = [c["id"] for c in ctx["candidate_stories"]]
    check("CVE-sharing story surfaced as candidate",
          "oracle-cpu-fragment" in ids, True)
    check("title-overlap story surfaced as candidate", "zeta-ransomware-spree" in ids, True)
    check("recency fill still present", sum(1 for i in ids if i.startswith("decoy")) == 40, True)
    check("new events in context",
          sorted(e["id"] for e in ctx["new_events"]),
          ["new-cve-event", "new-zeta-event"])
finally:
    shutil.rmtree(tmp)

print()
if failures:
    print(f"FAIL: {len(failures)} triage checks failed")
    sys.exit(1)
print("ALL PASS")
