#!/usr/bin/env python3
"""Tia N. List — daily CTI pass, deterministic front half.

1. Extract IOC candidates and diff against the curated set: writes only NEW
   candidates to data/iocs-candidates.json for the LLM curation audit.
2. Qualify cases needing CTI records (multi-source, not yet covered) and write
   data/cti-queue.json for the LLM record-authoring step.

Queue-staleness contract (2026-10-15 audit Rec 1 / 10-14 Rec 2): PHASE1
writes the queue BEFORE PHASE2 authors records, so a queue committed
without a refresh overstates the uncovered backlog by the records PHASE2
just wrote (33 committed vs 23 genuine on 10-16) and can spuriously trip
the audit's >20 re-run trigger. PHASE3 therefore re-runs ONLY the queue
step as its final pre-commit step, after PHASE2's records are on disk:

    python3 engine/cti_pass.py --refresh-queue

--refresh-queue recomputes data/cti-queue.json from the stories + cti/
dirs and touches nothing else (the IOC candidates file is PHASE2's input,
never rewritten after the fact). compute_queue()/write_queue() are the
tested seam: PHASE1 -> write records -> re-run the queue step must drop
the covered ids (see engine/test_cti_pass.py).

Usage: python3 cti_pass.py [--refresh-queue]
"""
import glob
import json
import os
import sys

import ioc as ioc_mod

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
EVENTS = os.path.join(DATA, "events")
STORIES = os.path.join(DATA, "stories")
CTI = os.path.join(DATA, "cti")
MIN_SCORE = 1.7  # 0-10 scale (was 1.0 on 0-6); low coverage bar, multi-source is the real gate
MIN_SOURCES = 2


def load_events():
    """Merged events (meta + content_md) so IOC extraction sees article text."""
    from store import load_events as _load
    return _load()


def load_story_cards(events=None, stories_dir=STORIES):
    cards = []
    for f in glob.glob(os.path.join(stories_dir, "*.json")):
        s = json.load(open(f))
        cards.append({"id": s["id"], "title": s.get("title", ""),
                      "score": s.get("score", 0.0), "n_sources": s.get("n_sources", 0),
                      "events": s.get("events", [])})
    return cards


def covered_ids(cti_dir=CTI):
    """Story ids with a CTI record on disk (any *.json basename)."""
    return {os.path.splitext(os.path.basename(f))[0]
            for f in glob.glob(os.path.join(cti_dir, "*.json"))}


def compute_queue(cards, covered):
    """Cases needing CTI records: uncovered, multi-source, above the bar.

    Pure function of (cards, covered) — the re-runnable queue step (see
    the module docstring): recompute after PHASE2's records land and the
    just-covered ids drop out."""
    return [{"id": c["id"], "title": c["title"], "score": c["score"],
              "n_sources": c["n_sources"]}
             for c in cards
             if c["id"] not in covered and c["n_sources"] >= MIN_SOURCES and c["score"] >= MIN_SCORE]


def write_queue(cards=None, stories_dir=STORIES, cti_dir=CTI, queue_path=None):
    """Recompute + write the CTI queue file; returns the queue list.

    PHASE1 calls it before PHASE2, PHASE3 calls it again after PHASE2's
    records land (--refresh-queue), so the committed queue never contains
    just-authored records. Writes ONLY the queue file."""
    if cards is None:
        cards = load_story_cards(stories_dir=stories_dir)
    queue = compute_queue(cards, covered_ids(cti_dir))
    json.dump({"stories": queue},
              open(queue_path or os.path.join(DATA, "cti-queue.json"), "w"), indent=1)
    return queue


def main():
    if "--refresh-queue" in sys.argv:
        queue = write_queue()
        print(f"cases needing CTI records: {len(queue)} (refreshed post-PHASE2; "
              f"uncovered, >= {MIN_SOURCES} sources, score >= {MIN_SCORE})")
        return
    events = load_events()
    cards = load_story_cards(events)

    # 1. new IOC candidates (diff against the curated set)
    from datetime import datetime, timezone
    curated_path = os.path.join(DATA, "iocs-curated.json")
    curated_values = {c["value"] for c in json.load(open(curated_path))} if os.path.exists(curated_path) else set()
    all_iocs = ioc_mod.build_index(cards, events)
    new = [i for i in all_iocs if i["value"] not in curated_values]
    json.dump({"generated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
               "candidates": [{
        "value": i["value"], "type": i["type"], "stories": i["stories"]} for i in new]},
        open(os.path.join(DATA, "iocs-candidates.json"), "w"), indent=1)

    # 2. cases needing CTI records
    queue = write_queue(cards)

    print(f"new IOC candidates: {len(new)} (of {len(all_iocs)} total)")
    print(f"cases needing CTI records: {len(queue)} (uncovered, >= {MIN_SOURCES} sources, score >= {MIN_SCORE})")


if __name__ == "__main__":
    main()
