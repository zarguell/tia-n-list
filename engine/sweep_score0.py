#!/usr/bin/env python3
"""Score-0 duplicate backlog sweep (2026-10-20 owner decision eda9f1100d5d,
audit Rec 3).

Auto-merges score-0.0 duplicate pairs the probe keeps flagging but the human
2-merge/day budget never reaches (the Trezor / BambooToken / NightmareStresser
backlog). A pair merges only when ALL hold: both stories' current score is
0.0; title jaccard >= 0.5; neither has an analysis file; neither is referenced
by any published digest (md slate links + json stories/overrides); no distinct
CVE sets. Merges go through repair_dedupe's mechanical path (the loser keeps
its json with merged_into + empty events so the old URL redirects, the winner
absorbs the events), then the derived-fields sweep and a rescore run on the
winners. Capped (10 merges/invocation) and idempotent — a second run
immediately after merges nothing.

The daily audit (audit.py) invokes the sweep before its adjudication section;
the hourly pipeline never runs it. needs-analysis is not re-emitted here —
the next hourly run re-queues any winner that crossed the analysis gate.

Usage:
  python3 engine/sweep_score0.py [--dry-run] [--cap N]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge import (load_events, load_stories, score0_sweep_candidates,  # noqa: E402
                   sweep_score0_merges)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="list candidate pairs, merge nothing")
    ap.add_argument("--cap", type=int, default=10,
                    help="max merges this invocation (default 10)")
    args = ap.parse_args()

    stories = load_stories()
    candidates = score0_sweep_candidates(stories)
    print(f"score-0 sweep: {len(candidates)} candidate pair(s)")
    for c in candidates:
        print(f"  {c['a']} + {c['b']} (jaccard {c['jaccard']})")
    if args.dry_run:
        print("dry-run: nothing written")
        return
    log = sweep_score0_merges(stories, load_events(), cap=args.cap)
    print(f"score-0 sweep: {len([l for l in log if l.startswith('merge ')])} merge(s)")
    for line in log:
        print(" ", line)


if __name__ == "__main__":
    main()
