#!/usr/bin/env python3
"""Retention policy: how long a story's page stays published.

The site is a research archive, so "delete old pages" is not a size knob — it
is an editorial promise. This module is the policy in one place, and a report
that says what the policy costs before anything is deleted:

  A  keep long       peak_score >= 7.5 at ANY point, or cited by an immutable
                     published artifact (a CTI case). 5 years.
  B  keep medium     digest-cited, or peak_score >= 5.0 at any point. 3 years.
  C  keep short      everything else. 6 months.

Two invariants make the tiers safe:

  * MONOTONE — a tier is a function of the high-water mark (`peak_score`,
    written by score.update_peak and never decreased) and of citations (which
    are permanent once published), never of the current decaying score. A
    story that was hot once stays A forever, no matter how cold it gets.
  * FAIL SAFE — an unreadable, missing or out-of-range peak is treated as
    "unknown", which promotes the story to A and flags it in the report. The
    store once held ~8.2k stories with no peak at all (before the 2026-09
    backfill), so absence must never be read as "never mattered".

Nothing here deletes or moves anything. `report()` prices the policy against
the real store; the archive sweep is a separate, flag-gated step that will run
only after these numbers are accepted.
"""
import glob
import json
import os
from collections import Counter
from datetime import datetime, timedelta, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
STORIES_DIR = os.path.join(DATA, "stories")
CTI_DIR = os.path.join(DATA, "cti")

# --- policy knobs (owner decision: docs/retention.md) -----------------------
TIER_A_PEAK = 7.5          # the "hottest" display band (ssg.heat) — peak, not score
TIER_B_PEAK = 5.0          # the "hot" display band
# Owner decision 2026-11-27: A and B both 3 years (the plateau that keeps
# ~28.5k stories, ~2.5x today, inside GitHub Pages' 1 GB with room to spare),
# C six months. Changing these is a policy change: update retention.md too.
TIER_YEARS = {"A": 3, "B": 3, "C": 0.5}
TIER_RANK = {"A": 0, "B": 1, "C": 2}
PEAK_MAX = 10.0


def peak_of(story):
    """(peak, known?) — unknown is distinct from zero, deliberately."""
    raw = story.get("peak_score")
    if raw is None:
        return 0.0, False
    try:
        peak = float(raw)
    except (TypeError, ValueError):
        return 0.0, False
    if peak < 0 or peak > PEAK_MAX:
        return 0.0, False
    return peak, True


def classify(story, immutable_cited=False, digest_cited=False):
    """(tier, reason) for one story. Pure: depends only on stored facts.

    immutable_cited  the story has a published CTI case (immutable artifact)
    digest_cited     a daily digest page links the story
    """
    peak, known = peak_of(story)
    # Order matters: an immutable citation outranks a digest citation (digest
    # pages are regenerated every build and can be rewritten; a CTI case, and
    # the STIX snapshot built from it, is published and immutable). Checking
    # digest first silently demoted 354/month of CTI-cited stories to B.
    if not known:
        return "A", "peak unknown (fail-safe: keep)"
    if peak >= TIER_A_PEAK:
        return "A", f"peak {peak:g} >= {TIER_A_PEAK:g}"
    if immutable_cited:
        return "A", "cti-cited (immutable)"
    if digest_cited:
        return "B", "digest-cited"
    if peak >= TIER_B_PEAK:
        return "B", f"peak {peak:g} >= {TIER_B_PEAK:g}"
    return "C", f"peak {peak:g} < {TIER_B_PEAK:g}, uncited"


def _immutable_cited():
    ids = set()
    for path in glob.glob(os.path.join(CTI_DIR, "*.json")):
        try:
            sid = json.load(open(path)).get("story_id")
        except (OSError, ValueError):
            continue
        if sid:
            ids.add(sid)
    return ids


def _digest_cited():
    import lifecycle
    return lifecycle.referenced_story_ids()


def load_stories():
    stories = {}
    for path in glob.glob(os.path.join(STORIES_DIR, "*.json")):
        try:
            st = json.load(open(path))
        except (OSError, ValueError):
            continue
        if st.get("id"):
            stories[st["id"]] = st
    return stories


def classify_all(stories=None, immutable=None, digest=None):
    """{id: (tier, reason)} for every non-merged story."""
    stories = load_stories() if stories is None else stories
    immutable = _immutable_cited() if immutable is None else immutable
    digest = _digest_cited() if digest is None else digest
    out = {}
    for sid, st in stories.items():
        if st.get("merged_into"):
            continue                      # redirect shells: one map key, no page
        out[sid] = classify(st, sid in immutable, sid in digest)
    return out


def _date(value):
    """ISO date (or datetime) -> date; None when unparseable (fail safe)."""
    text = str(value or "")[:10]
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        return None


def expires_at(story, tier):
    """The date a tier's horizon runs out, measured from LAST activity.

    last_seen, not first_seen: a story that keeps receiving events is live
    coverage and must not expire on its birthday. None = never expires here
    (unparseable date or a tier with no horizon).
    """
    years = TIER_YEARS.get(tier)
    if years is None:
        return None
    seen = _date(story.get("last_seen")) or _date(story.get("first_seen"))
    if seen is None:
        return None
    return seen + timedelta(days=round(years * 365))


def expiring(stories=None, today=None, immutable=None, digest=None):
    """What a sweep would expire, bucketed by what still blocks it.

    Read-only. Buckets:
      expirable      horizon elapsed, no live citation at all -> a sweep may
                     remove the page (the archive repo keeps the data)
      needs-digest   horizon elapsed but a digest page still links it: the
                     link must be rewritten to the archive host first
      immutable      tier A (an immutable citation or a hottest peak): never
      inside         horizon not elapsed
      unknown-date   no parseable last_seen: never expire (fail safe)
      merged         redirect shell: one redirects.json key, not a page
    """
    stories = load_stories() if stories is None else stories
    today = today or datetime.now(timezone.utc).date()
    immutable = _immutable_cited() if immutable is None else immutable
    digest = _digest_cited() if digest is None else digest
    buckets = {k: [] for k in ("expirable", "needs-digest", "immutable",
                               "inside", "unknown-date", "merged")}
    for sid, st in stories.items():
        if st.get("merged_into"):
            buckets["merged"].append(sid)
            continue
        tier, _ = classify(st, sid in immutable, sid in digest)
        if tier == "A":
            buckets["immutable"].append(sid)
            continue
        when = expires_at(st, tier)
        if when is None:
            buckets["unknown-date"].append(sid)
        elif when > today:
            buckets["inside"].append(sid)
        elif sid in digest:
            buckets["needs-digest"].append(sid)
        else:
            buckets["expirable"].append(sid)
    return {k: sorted(v) for k, v in buckets.items()}


def _monthly_rates(tiers, stories, months=3):
    """({tier: stories/month}, [recent month strings]) from first_seen."""
    per = Counter()
    for sid, (tier, _) in tiers.items():
        per[(tier, (stories[sid].get("first_seen") or "")[:7])] += 1
    recent = sorted({m for _, m in per if m})[-months:]
    if not recent:
        return {t: 0.0 for t in TIER_RANK}, []
    rate = {t: sum(per[(t, m)] for m in recent) / len(recent) for t in TIER_RANK}
    return rate, recent


def _plateau(rate):
    """stories retained at steady state = rate x horizon in months."""
    return {t: rate.get(t, 0.0) * TIER_YEARS[t] * 12 for t in TIER_YEARS}


def report(stories=None):
    """Counts per tier, monthly rates and the steady-state page estimate."""
    stories = load_stories() if stories is None else stories
    tiers = classify_all(stories)
    rate, recent = _monthly_rates(tiers, stories)
    live = _plateau(rate)
    unknown = sum(1 for _, reason in tiers.values() if reason.startswith("peak unknown"))
    return {
        "total": len(tiers),
        "tiers": dict(Counter(t for t, _ in tiers.values())),
        "recent_months": recent,
        "per_month": rate,
        "steady_state_stories": live,
        "steady_state_total": sum(live.values()),
        "unknown_peak": unknown,
        "horizons_years": dict(TIER_YEARS),
    }


def main(argv=None):
    import argparse
    import sys
    ap = argparse.ArgumentParser(description="retention policy report (read-only)")
    ap.add_argument("--report", action="store_true", help="print the pricing report")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--expiring", action="store_true",
                    help="what a sweep would expire today (read-only)")
    ap.add_argument("--horizons", metavar="A,B,C",
                    help="explore other horizons in years, e.g. 3,3,0.5")
    args = ap.parse_args(argv)
    if not (args.report or args.expiring):
        ap.print_help()
        return 2
    if args.horizons:
        a, b, c = (float(x) for x in args.horizons.split(","))
        TIER_YEARS.update({"A": a, "B": b, "C": c})
    if args.expiring:
        buckets = expiring()
        if args.json:
            print(json.dumps({k: len(v) for k, v in buckets.items()},
                             indent=1, sort_keys=True))
            return 0
        print("dry run — nothing is deleted; the archive repo keeps the data")
        for name in ("expirable", "needs-digest", "immutable", "inside",
                     "unknown-date", "merged"):
            print(f"  {name:13} {len(buckets[name]):6d}")
        if buckets["expirable"]:
            print(f"  e.g. expirable: {', '.join(buckets['expirable'][:3])}")
        return 0
    rep = report()
    if args.json:
        print(json.dumps(rep, indent=1, sort_keys=True))
        return 0
    print(f"stories classified: {rep['total']}  (recent months: {', '.join(rep['recent_months'])})")
    print(f"{'tier':4} {'keep':>6} {'live':>7} {'stories/mo':>11} {'steady-state':>13}")
    for t in ("A", "B", "C"):
        print(f"{t:4} {rep['horizons_years'][t]:6.1f}y {rep['tiers'].get(t, 0):7d} "
              f"{rep['per_month'][t]:11.0f} {rep['steady_state_stories'][t]:13.0f}")
    print(f"{'':4} {'':6} {'':7} {'':11} {rep['steady_state_total']:13.0f}  <= pages at plateau")
    if rep["unknown_peak"]:
        print(f"fail-safe: {rep['unknown_peak']} story(ies) with an unknown peak kept as A")
    print("today: see `python3 engine/stage_pages.py <dir>` for the staged file count")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
