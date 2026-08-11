#!/usr/bin/env python3
"""Tia N. List — daily CTI pass, deterministic front half.

1. Extract IOC candidates and diff against the curated set: writes only NEW
   candidates to data/iocs-candidates.json for the LLM curation audit.
2. Qualify cases needing CTI records (multi-source, not yet covered) and write
   data/cti-queue.json for the LLM record-authoring step.

Usage: python3 cti_pass.py
"""
import glob
import json
import os

import ioc as ioc_mod

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
EVENTS = os.path.join(DATA, "events")
STORIES = os.path.join(DATA, "stories")
CTI = os.path.join(DATA, "cti")
MIN_SCORE = 1.0
MIN_SOURCES = 2


def load_events():
    events = {}
    for f in glob.glob(os.path.join(EVENTS, "*.json")):
        e = json.load(open(f))
        events[e["id"]] = e
    return events


def load_story_cards(events):
    cards = []
    for f in glob.glob(os.path.join(STORIES, "*.json")):
        s = json.load(open(f))
        cards.append({"id": s["id"], "title": s.get("title", ""),
                      "score": s.get("score", 0.0), "n_sources": s.get("n_sources", 0),
                      "events": s.get("events", [])})
    return cards


def main():
    events = load_events()
    cards = load_story_cards(events)

    # 1. new IOC candidates (diff against the curated set)
    curated_path = os.path.join(DATA, "iocs-curated.json")
    curated_values = {c["value"] for c in json.load(open(curated_path))} if os.path.exists(curated_path) else set()
    all_iocs = ioc_mod.build_index(cards, events)
    new = [i for i in all_iocs if i["value"] not in curated_values]
    json.dump({"generated": "2026-08-12", "candidates": [{
        "value": i["value"], "type": i["type"], "stories": i["stories"]} for i in new]},
        open(os.path.join(DATA, "iocs-candidates.json"), "w"), indent=1)

    # 2. cases needing CTI records
    covered = {os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(CTI, "*.json"))}
    queue = [{"id": c["id"], "title": c["title"], "score": c["score"],
              "n_sources": c["n_sources"]}
             for c in cards
             if c["id"] not in covered and c["n_sources"] >= MIN_SOURCES and c["score"] >= MIN_SCORE]
    json.dump({"stories": queue}, open(os.path.join(DATA, "cti-queue.json"), "w"), indent=1)

    print(f"new IOC candidates: {len(new)} (of {len(all_iocs)} total)")
    print(f"cases needing CTI records: {len(queue)} (uncovered, >= {MIN_SOURCES} sources, score >= {MIN_SCORE})")


if __name__ == "__main__":
    main()
