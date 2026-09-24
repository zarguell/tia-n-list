#!/usr/bin/env python3
"""Peak-score contract suite — the high-water mark (store-health root).

The published score decays with a 36h half-life, so the store could not tell
"was hot, cooled" from "never mattered" (10k stories, 8k at score 0). This
suite pins the peak_score contract the lifecycle freeze and best-of surfaces
build on:

  1. update_peak raises peak_score/peak_at when the score beats the peak,
     and NEVER lowers it when the score decays;
  2. first touch on a pre-peak story stamps the field (no story without
     peak_score after any rescoring path);
  3. the exception fallback paths' rule: update_peak is a success-path-only
     call — a bare number is accepted, and a 0 score never erases a peak;
  4. undecayed_score recomputes the no-decay score from a breakdown
     (base + reddit, capped 10), and falls back to summing factors when
     `base` is missing (old breakdowns);
  5. merged_into shells are skipped by the backfill; the backfill raises
     peaks to max(peak, score, undecayed) and stamps peak_at from last_seen.

Run: python3 engine/test_peak_score.py   (exit 0 = pass)
"""
import glob
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score  # noqa: E402

FAILS = []


def check(name, cond):
    print(("  ok  " if cond else "  FAIL") + f" {name}")
    if not cond:
        FAILS.append(name)


# --- 1/2/3: update_peak monotonicity + first touch -------------------------
s = {"id": "story-a", "score": 0.0}
score.update_peak(s, {"score": 6.4})
check("peak raised on hot score", s["peak_score"] == 6.4)
check("peak_at stamped", bool(s.get("peak_at")))
score.update_peak(s, {"score": 0.4})
check("decay never lowers peak", s["peak_score"] == 6.4)
score.update_peak(s, 7.1)                      # bare-number form
check("bare-number score accepted", s["peak_score"] == 7.1)
check("score capped at 10",
      (lambda st: (score.update_peak(st, {"score": 99.0}),
                   st["peak_score"] == 10.0)[1])({"id": "x", "peak_score": 9.9}))

fresh = {"id": "story-b", "score": 0.0}
score.update_peak(fresh, {"score": 0.0})
check("first touch stamps field on a cold story",
      fresh.get("peak_score") == 0.0 and "peak_score" in fresh)

# --- 4: undecayed_score ----------------------------------------------------
sb = {"base": 5.2, "breadth": 1.0, "authority": 1.8, "severity": 1.9,
      "velocity": 0.5, "pickup": 0.0, "recency": 0.12, "reddit": 0.7,
      "kev": True, "n_sources": 3}
check("undecayed = base + reddit", score.undecayed_score(sb) == 5.9)
legacy = {"breadth": 1.0, "authority": 1.0, "severity": 2.0,
          "velocity": 0.0, "pickup": 0.0, "recency": 0.05, "reddit": 0.0}
check("legacy breakdown (no base) sums factors",
      score.undecayed_score(legacy) == 4.0)
check("undecayed capped at 10",
      score.undecayed_score({**sb, "base": 9.8, "reddit": 1.5}) == 10.0)
check("non-dict breakdown -> 0.0", score.undecayed_score(None) == 0.0)

# --- 5: backfill_peaks.py end-to-end on a temp store -----------------------
with tempfile.TemporaryDirectory() as td:
    stories = os.path.join(td, "stories")
    os.makedirs(stories)
    hot_cooled = {"id": "hot-cooled", "title": "t", "last_seen":
                  "2026-09-01T00:00:00Z", "first_seen": "2026-09-01T00:00:00Z",
                  "score": 0.2, "score_breakdown": sb}
    never = {"id": "never", "title": "t", "last_seen": "2026-09-20T00:00:00Z",
             "first_seen": "2026-09-20T00:00:00Z", "score": 0.0,
             "score_breakdown": dict(score.SB_DEFAULTS)}
    shell = {"id": "shell", "merged_into": "hot-cooled", "events": [],
             "score": 0.0}
    for st in (hot_cooled, never, shell):
        json.dump(st, open(os.path.join(stories, st["id"] + ".json"), "w"),
                  indent=1)
    engine_dir = os.path.dirname(os.path.abspath(__file__))
    # run the script against a fixture store: copy the two modules into a
    # temp engine/ and symlink data/stories (the script derives its store
    # path from __file__)
    tmp_engine = os.path.join(td, "engine")
    os.makedirs(tmp_engine, exist_ok=True)
    for f in ("backfill_peaks.py", "score.py"):
        subprocess.run(["cp", os.path.join(engine_dir, f),
                        os.path.join(tmp_engine, f)], check=True)
    os.makedirs(os.path.join(tmp_engine, "data"), exist_ok=True)
    os.symlink(stories, os.path.join(tmp_engine, "data", "stories"))
    r = subprocess.run([sys.executable,
                        os.path.join(tmp_engine, "backfill_peaks.py")],
                       capture_output=True, text=True)
    check("backfill dry run exits 0", r.returncode == 0)
    after = json.load(open(os.path.join(stories, "hot-cooled.json")))
    check("dry run writes nothing", "peak_score" not in after)
    r = subprocess.run([sys.executable,
                        os.path.join(tmp_engine, "backfill_peaks.py"),
                        "--apply"], capture_output=True, text=True)
    check("backfill --apply exits 0", r.returncode == 0)
    after = json.load(open(os.path.join(stories, "hot-cooled.json")))
    check("cooled-hot story peak = undecayed 5.9", after["peak_score"] == 5.9)
    check("peak_at stamped from last_seen",
          after["peak_at"] == "2026-09-01T00:00:00Z")
    never_after = json.load(open(os.path.join(stories, "never.json")))
    check("cold story keeps ~0 peak", never_after["peak_score"] == 0.0)
    shell_after = json.load(open(os.path.join(stories, "shell.json")))
    check("merged_into shell untouched", "peak_score" not in shell_after)

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} check(s): {', '.join(FAILS)}")
    sys.exit(1)
print("all peak-score contract checks passed")
