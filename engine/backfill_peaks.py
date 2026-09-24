#!/usr/bin/env python3
"""One-time peak_score backfill for the story store.

Story jsons gained peak_score/peak_at (score.update_peak, written by the
merge + triage-apply rescoring paths) so the store can tell "was hot, cooled"
from "never mattered" — the cold-tier lifecycle freeze and any best-of
surface need the high-water mark, not today's decayed score. Stories scored
before the field existed carry at most their current decayed value.

For each active story (no merged_into), this raises peak_score to the honest
maximum of:
  - its recorded peak_score (if any),
  - its current score,
  - its undecayed score (breakdown with recency = 1.0 — score.undecayed_score).

peak_at for backfilled stories is stamped with the story's last_seen — the
moment the peak was most plausibly reached; the exact clock is gone.
merged_into shells are left untouched. Dry run by default; --apply writes.

Usage: python3 engine/backfill_peaks.py [--apply]
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import undecayed_score  # noqa: E402

STORIES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "data", "stories")


def main():
    apply = "--apply" in sys.argv
    touched = already = 0
    for p in sorted(glob.glob(os.path.join(STORIES, "*.json"))):
        try:
            s = json.load(open(p))
        except Exception as e:
            print(f"WARN: skipping corrupt story {p}: {e}")
            continue
        if s.get("merged_into"):
            continue
        peak = float(s.get("peak_score") or 0.0)
        cand = max(peak, float(s.get("score") or 0.0),
                   undecayed_score(s.get("score_breakdown")))
        if cand <= peak + 1e-9:
            if "peak_score" not in s:
                s["peak_score"] = round(cand, 2)
                s["peak_at"] = s.get("last_seen") or s.get("first_seen") or ""
                already += 1
                if apply:
                    json.dump(s, open(p, "w"), indent=1)
            continue
        s["peak_score"] = round(cand, 2)
        s["peak_at"] = s.get("last_seen") or s.get("first_seen") or ""
        touched += 1
        if apply:
            json.dump(s, open(p, "w"), indent=1)
    verb = "backfilled" if apply else "WOULD backfill (dry run)"
    print(f"peak backfill: {touched} stories {verb}, "
          f"{already} first-touch stamps, "
          f"total scanned: {len(glob.glob(os.path.join(STORIES, '*.json')))}")
    if not apply:
        print("dry run: re-run with --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
