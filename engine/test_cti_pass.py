#!/usr/bin/env python3
"""cti_pass queue-refresh contract suite (2026-10-17 decisions batch).

Queue-staleness bug (10-15 Rec 1 / 10-14 Rec 2): PHASE1 writes
data/cti-queue.json BEFORE PHASE2 authors records, and PHASE3 committed
that pre-PHASE2 state — the committed "uncovered" count overstated real
work by the batch PHASE2 just wrote (33 committed vs 23 genuine on 10-16)
and could spuriously trip the audit's >20 re-run trigger.

Fix contract pinned here: PHASE1 -> write CTI records -> re-run the queue
step (write_queue(), i.e. `cti_pass.py --refresh-queue`) MUST drop the
covered ids while keeping genuinely uncovered ones, and the refresh MUST
NOT touch the IOC candidates file (PHASE2's input). Below-bar stories
(single-source, under-scored) never queue.

Run: python3 engine/test_cti_pass.py   (exit 0 = pass)
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cti_pass as cp  # noqa: E402

FAILS = []


def check(name, cond):
    print(("  ok  " if cond else "  FAIL") + f" {name}")
    if not cond:
        FAILS.append(name)


def mkstory(sdir, sid, n_sources=2, score=5.0):
    with open(os.path.join(sdir, sid + ".json"), "w") as fh:
        json.dump({"id": sid, "title": f"Title {sid}", "score": score,
                   "n_sources": n_sources, "events": []}, fh)


root = tempfile.mkdtemp()
sdir = os.path.join(root, "stories")
cdir = os.path.join(root, "cti")
os.makedirs(sdir)
os.makedirs(cdir)
qpath = os.path.join(root, "cti-queue.json")
# PHASE2's input — the refresh step must leave it byte-identical.
ioc_sentinel = os.path.join(root, "iocs-candidates.json")
with open(ioc_sentinel, "w") as fh:
    json.dump({"generated": "2026-10-17", "candidates": [{"value": "evil.example"}]}, fh)
before = open(ioc_sentinel, "rb").read()

mkstory(sdir, "case-a", n_sources=2, score=5.0)   # queued, then covered
mkstory(sdir, "case-b", n_sources=3, score=8.0)   # queued, stays uncovered
mkstory(sdir, "single-source", n_sources=1, score=9.0)  # below source bar
mkstory(sdir, "low-score", n_sources=4, score=0.5)      # below score bar

# PHASE1: queue step on a store with no records.
q1 = cp.write_queue(stories_dir=sdir, cti_dir=cdir, queue_path=qpath)
check("PHASE1 queues the two eligible cases",
      sorted(e["id"] for e in q1) == ["case-a", "case-b"])
check("PHASE1 queue file matches the returned queue",
      json.load(open(qpath))["stories"] == q1)
check("below-bar stories never queue",
      all(e["id"] not in ("single-source", "low-score") for e in q1))

# PHASE2: author a record for case-a (record basename == story id).
with open(os.path.join(cdir, "case-a.json"), "w") as fh:
    json.dump({"story_id": "case-a", "title": "Title case-a"}, fh)
check("covered_ids sees the just-written record", cp.covered_ids(cdir) == {"case-a"})

# PHASE3: re-run ONLY the queue step.
q2 = cp.write_queue(stories_dir=sdir, cti_dir=cdir, queue_path=qpath)
check("refresh drops the just-covered id",
      sorted(e["id"] for e in q2) == ["case-b"])
check("refreshed queue file excludes the covered id",
      [e["id"] for e in json.load(open(qpath))["stories"]] == ["case-b"])
check("refresh leaves the IOC candidates file untouched",
      open(ioc_sentinel, "rb").read() == before)

# compute_queue is pure: same inputs, same outputs, no I/O.
cards = cp.load_story_cards(stories_dir=sdir)
check("compute_queue pure recompute agrees",
      cp.compute_queue(cards, {"case-a"}) == q2)

if FAILS:
    print(f"{len(FAILS)} FAILURES: {FAILS}")
    sys.exit(1)
print("all cti-pass queue-refresh contract checks passed")
