#!/usr/bin/env python3
"""Tia N. List — daily digest coverage-delta candidates.

Computes, deterministically, what today's daily digest should cover. The digest
is a coverage-delta brief, not a "today's articles" dump:

- YESTERDAY'S COVERAGE — the stories the last digest actually discussed
  (baseline for one-line [UPDATE] deltas).
- EVOLVED — live stories with new events or a fresh analysis since the last
  digest, ranked by score.
- UNCOVERED — hot stories (score >= ANALYSIS_GATE) not covered in the last
  COVERAGE_WINDOW digests (never covered, or not since).

Coverage history is read from data/digests/*.json `stories` arrays (new-format
digests starting 2026-08-12) UNION `stories/<slug>/` links in the .md
sidecars (backlog-era digests predate the stories array). Merged-away shells
resolve to their canonical story so a digest never links a redirect.

Output: the brief on stdout (what the digest agent reads), machine-readable
JSON at data/digest-candidates.json (gitignored).

Usage: python3 digest_candidates.py [--date YYYY-MM-DD]
"""
import argparse
import glob
import json
import os
import re
from datetime import datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
STORIES_DIR = os.path.join(DATA, "stories")
EVENTS_DIR = os.path.join(DATA, "events")
DIGESTS_DIR = os.path.join(DATA, "digests")
OUT_JSON = os.path.join(DATA, "digest-candidates.json")

ANALYSIS_GATE = 2.0  # merge.py's analysis-queue threshold; the digest's coverage bar
COVERAGE_WINDOW = 3  # a story covered within the last N digests counts as covered

STORY_LINK_RE = re.compile(r"stories/([a-z0-9][a-z0-9-]*)/?")


def parse_utc(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)


def load_stories():
    out = {}
    for f in glob.glob(os.path.join(STORIES_DIR, "*.json")):
        s = json.load(open(f))
        out[s["id"]] = s
    return out


def load_events():
    """Event meta keyed by event_id (file basename == the id, e.g. mf:160047)."""
    out = {}
    for f in glob.glob(os.path.join(EVENTS_DIR, "*.json")):
        eid = os.path.splitext(os.path.basename(f))[0]
        out[eid] = json.load(open(f))
    return out


def digest_dates():
    return sorted(os.path.splitext(os.path.basename(f))[0]
                  for f in glob.glob(os.path.join(DIGESTS_DIR, "*.json")))


def load_coverage(stories, canonical):
    """slug -> last digest date that covered it (json stories array ∪ .md links).

    Every covered slug resolves through `canonical` so a digest that linked a
    pre-merge shell still credits the live story it merged into (coverage
    tracking survives triage merges)."""
    dates = digest_dates()
    covered = {}  # slug -> date
    for d in dates:
        jpath = os.path.join(DIGESTS_DIR, d + ".json")
        mpath = os.path.join(DIGESTS_DIR, d + ".md")
        slugs = set()
        try:
            slugs.update(json.load(open(jpath)).get("stories", []))
        except Exception:
            pass
        if os.path.exists(mpath):
            slugs.update(STORY_LINK_RE.findall(open(mpath).read()))
        for slug in slugs:
            covered[canonical(slug)] = d
    return covered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="digest date (default: today UTC)")
    args = ap.parse_args()
    today = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    dates = digest_dates()
    prior = [d for d in dates if d < today]
    if not prior:
        print("No prior digest to diff against; nothing to compute.")
        return
    last_digest = prior[-1]
    since = parse_utc(last_digest + "T00:00:00Z")
    recent_cutoff = dates[-COVERAGE_WINDOW] if len(dates) >= COVERAGE_WINDOW else dates[0]

    stories = load_stories()
    events = load_events()

    # canonical resolution: shell -> story it merged into
    def canonical(slug, seen=None):
        seen = seen or set()
        if slug in seen or slug not in stories:
            return slug
        seen.add(slug)
        target = stories[slug].get("merged_into")
        return canonical(target, seen) if target else slug

    coverage = load_coverage(stories, canonical)

    # yesterday's coverage = canonical slugs whose last covered date is the last digest
    yesterday = {slug for slug, d in coverage.items() if d == last_digest}

    # per-story signals
    rows = []
    for slug, s in stories.items():
        if s.get("merged_into"):
            continue  # redirect shells are never digest candidates
        ev_dates = []
        for ref in s.get("events", []):
            e = events.get(ref["event_id"])
            if e and e.get("published_at"):
                try:
                    ev_dates.append(parse_utc(e["published_at"]))
                except ValueError:
                    pass
        new_events = sum(1 for dt in ev_dates if dt > since)
        an = s.get("analysis") or {}
        an_at = parse_utc(an["updated_at"]) if an.get("updated_at") else None
        evolved = new_events > 0 or (an_at is not None and an_at > since)
        last_covered = coverage.get(slug)
        covered_recently = last_covered is not None and last_covered >= recent_cutoff
        if last_covered is None:
            tag = "NEW"
        elif last_covered == last_digest:
            tag = "UPDATE"
        elif covered_recently:
            tag = "REVISIT"  # covered inside the window but not yesterday
        else:
            tag = "REVISIT"  # covered before, not since
        rows.append({
            "slug": slug,
            "title": s.get("title", ""),
            "score": s.get("score", 0.0),
            "hot": s.get("score", 0.0) >= ANALYSIS_GATE,
            "n_events": len(ev_dates),
            "new_events_since": new_events,
            "newest_event_at": max(ev_dates).strftime("%Y-%m-%d") if ev_dates else None,
            "has_analysis": an_at is not None,
            "analysis_at": an_at.strftime("%Y-%m-%d") if an_at else None,
            "last_covered": last_covered,
            "covered_recently": covered_recently,
            "tag": tag,
            "evolved": evolved,
            "n_sources": s.get("n_sources", 0),
            "cves": s.get("cves", []),
        })

    by_score = sorted(rows, key=lambda r: -r["score"])
    evolved = [r for r in by_score if r["evolved"]]
    uncovered = [r for r in by_score if r["hot"] and not r["covered_recently"]]
    yesterday_rows = sorted(
        (r for r in rows if r["slug"] in yesterday), key=lambda r: -r["score"])

    def fmt(r):
        ev = f"+{r['new_events_since']}ev" if r["new_events_since"] else "   "
        an = f"an={r['analysis_at']}" if r["has_analysis"] else "an=-   "
        cov = r["last_covered"] or "never"
        return (f"[{r['tag']:<7}] {r['score']:4.1f}  {ev}  {an}  "
                f"cov={cov:<10} {r['slug']}")

    print(f"Tia N. List — daily digest coverage brief")
    print(f"Date: {today} | Last digest: {last_digest} "
          f"({len(yesterday)} stories) | Delta boundary: after {since:%Y-%m-%d}T00:00Z")
    print(f"Coverage window: stories not covered since {recent_cutoff} count as uncovered\n")

    print(f"YESTERDAY'S COVERAGE ({len(yesterday_rows)}) — baseline for [UPDATE] deltas")
    for r in yesterday_rows:
        mark = "EVOLVED" if r["evolved"] else "static "
        print(f" {mark} {r['score']:4.1f} +{r['new_events_since']}ev "
              f"{r['slug']} — {r['title'][:80]}")
    print()

    print(f"EVOLVED SINCE LAST DIGEST ({len(evolved)}) — new events or fresh analysis, score desc")
    for r in evolved:
        print(" " + fmt(r) + f" — {r['title'][:70]}")
    print()

    print(f"HOT & UNCOVERED ({len(uncovered)}) — score >= {ANALYSIS_GATE}, not covered since {recent_cutoff}")
    for r in uncovered:
        print(" " + fmt(r) + f" — {r['title'][:70]}")

    payload = {
        "date": today,
        "last_digest": last_digest,
        "delta_boundary": since.isoformat(),
        "coverage_window": COVERAGE_WINDOW,
        "yesterday": yesterday_rows,
        "evolved": evolved,
        "uncovered": uncovered,
    }
    with open(OUT_JSON, "w") as fh:
        json.dump(payload, fh, indent=1)
    print(f"\nwrote {OUT_JSON}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # tolerate `digest_candidates.py | head` style piping
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 1)
        os.close(devnull)
