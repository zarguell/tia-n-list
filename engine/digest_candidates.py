#!/usr/bin/env python3
"""Tia N. List — daily digest coverage-delta candidates.

Computes, deterministically, what today's daily digest should cover. The digest
is a coverage-delta brief, not a "today's articles" dump:

- YESTERDAY'S COVERAGE — the stories the last digest actually discussed
  (baseline for one-line [UPDATE] deltas).
- EVOLVED — live stories with a genuine development since the last digest,
  ranked by score.
- UNCOVERED — hot stories (score >= ANALYSIS_GATE) not covered in the last
  COVERAGE_WINDOW digests (never covered, or not since).

WHAT COUNTS AS A DEVELOPMENT (the "is this actually new?" check):

A story evolves only when something *happened* since the last digest boundary:
a new event that is a genuine development, or a CISA KEV add. Two freshness
traps are handled deterministically:

1. RECAP ARTICLES: outlets re-report older developments for days. An event is
   a recap — not a development — when the story is KEV-anchored, the event
   explicitly mentions the KEV catalog, and it was published >= RECAP_DAYS
   after the CVE's `dateAdded`. Its development date collapses to the KEV add
   date, so a recap can never re-evolve a story or extend its freshness.
2. ANALYSIS MARKERS: `analysis.updated_at` churns whenever the hourly engine
   touches a story (including recap-driven rewrites), so it is NOT a
   development signal. It stays visible as substance, but does not evolve a
   story.

Per story the brief emits `dev=` (newest genuine development date) and a
CATCH-UP flag: hot stories whose newest development is >= CATCHUP_DAYS old
have nothing new for today and must not be headlined as if they do (e.g. a
"winsock added to the KEV" headline three days after CISA listed it).

Coverage history is read from data/digests/*.json `stories` arrays (new-format
digests starting 2026-08-12) UNION `stories/<slug>/` links in the .md
sidecars (backlog-era digests predate the stories array). Merged-away shells
resolve to their canonical story so a digest never links a redirect.

Output: the brief on stdout (what the digest agent reads), machine-readable
JSON at data/digest-candidates.json (gitignored).

Usage: python3 digest_candidates.py [--date YYYY-MM-DD] [--kev-data DIR]
"""
import argparse
import glob
import json
import os
import re
from datetime import datetime, time, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
STORIES_DIR = os.path.join(DATA, "stories")
EVENTS_DIR = os.path.join(DATA, "events")
DIGESTS_DIR = os.path.join(DATA, "digests")
KEV_DATA_DIR = os.path.normpath(os.path.join(ENGINE, "..", "kevrichment", "data"))
OUT_JSON = os.path.join(DATA, "digest-candidates.json")

ANALYSIS_GATE = 3.3  # merge.py's analysis-queue threshold on the 0-10 scale (was 2.0); the digest's coverage bar
COVERAGE_WINDOW = 3  # a story covered within the last N digests counts as covered
RECAP_DAYS = 2       # an event about a KEV add published >= N days after the add is a recap, not a development
CATCHUP_DAYS = 2     # newest genuine development >= N days before the digest date -> CATCH-UP (nothing new)
BENCH_MAX = 12         # wildcard discovery slate cap
BENCH_SCORE_FLOOR = 1.0  # below this a non-slate story is noise, not a near-miss
NEAR_GATE = 0.7         # fraction of ANALYSIS_GATE that counts as a near-miss on the bench

STORY_LINK_RE = re.compile(r"stories/([a-z0-9][a-z0-9-]*)/?")
CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,7}$")
KEV_RE = re.compile(r"\bKEV\b|Known Exploited Vulnerabilit", re.IGNORECASE)


def parse_utc(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)


def load_stories(stories_dir=STORIES_DIR):
    out = {}
    for f in glob.glob(os.path.join(stories_dir, "*.json")):
        s = json.load(open(f))
        out[s["id"]] = s
    return out


def load_events(events_dir=EVENTS_DIR):
    """Event meta keyed by event_id (file basename == the id, e.g. mf:160047)."""
    out = {}
    for f in glob.glob(os.path.join(events_dir, "*.json")):
        eid = os.path.splitext(os.path.basename(f))[0]
        out[eid] = json.load(open(f))
    return out


def digest_dates(digests_dir=DIGESTS_DIR):
    return sorted(os.path.splitext(os.path.basename(f))[0]
                  for f in glob.glob(os.path.join(digests_dir, "*.json")))


def kev_date_map(kev_data_dir):
    """cve_id -> kev_date_added (date) for KEV-listed CVEs, from the kevrichment
    index (the same source kev.py renders). Missing dir/index -> {}."""
    out = {}
    path = os.path.join(kev_data_dir, "index.json")
    if not os.path.exists(path):
        return out
    try:
        idx = json.load(open(path))
    except (OSError, ValueError):
        return out
    for e in idx.get("cves", []):
        cid = e.get("cve_id")
        added = e.get("kev_date_added")
        if (isinstance(cid, str) and CVE_RE.match(cid)
                and isinstance(added, str) and added):
            try:
                out[cid] = datetime.fromisoformat(added).date()
            except ValueError:
                pass
    return out


def load_coverage(stories, canonical, digests_dir=DIGESTS_DIR):
    """slug -> last digest date that covered it (json stories array ∪ .md links).

    Every covered slug resolves through `canonical` so a digest that linked a
    pre-merge shell still credits the live story it merged into (coverage
    tracking survives triage merges)."""
    dates = digest_dates(digests_dir)
    covered = {}  # slug -> date
    for d in dates:
        jpath = os.path.join(digests_dir, d + ".json")
        mpath = os.path.join(digests_dir, d + ".md")
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


def _is_kev_recap(event, kev_added):
    """True when the event is an outlet re-report of an older KEV add: the story
    is KEV-anchored, the event text mentions the KEV catalog, and it was
    published >= RECAP_DAYS after the add. Recaps are not developments."""
    if kev_added is None:
        return False
    try:
        pub = parse_utc(event["published_at"]).date()
    except (KeyError, ValueError):
        return False
    if (pub - kev_added).days < RECAP_DAYS:
        return False
    text = (event.get("title") or "") + " " + (event.get("content_md") or "")
    return bool(KEV_RE.search(text))


def build_rows(stories, events, kev_map, coverage, canonical, since, recent_cutoff, today, last_digest):
    """Per-story rows with the freshness check. `today` = digest date (str)."""
    today_d = parse_utc(today + "T00:00:00Z").date()
    rows = []
    for slug, s in stories.items():
        if s.get("merged_into"):
            continue  # redirect shells are never digest candidates
        cves = [c for c in s.get("cves", []) if isinstance(c, str)]
        kev_added = max((kev_map[c] for c in cves if c in kev_map), default=None)
        kev_dt = (datetime.combine(kev_added, time.min, tzinfo=timezone.utc)
                  if kev_added is not None else None)

        ev_dates = []   # raw article publish dates (display)
        dev_dates = []  # genuine development dates (recaps collapsed to the KEV add)
        for ref in s.get("events", []):
            e = events.get(ref["event_id"])
            if not e or not e.get("published_at"):
                continue
            try:
                pub = parse_utc(e["published_at"])
            except ValueError:
                continue
            ev_dates.append(pub)
            if _is_kev_recap(e, kev_added):
                dev_dates.append(kev_dt)
            else:
                dev_dates.append(pub)
        if kev_dt is not None:
            dev_dates.append(kev_dt)  # the KEV add itself is a development

        new_events = sum(1 for dt in dev_dates if dt > since)
        an = s.get("analysis") or {}
        an_at = parse_utc(an["updated_at"]) if an.get("updated_at") else None
        evolved = new_events > 0  # developments only; article dates + analysis churn don't evolve

        newest_dev = max(dev_dates) if dev_dates else None
        stale_days = (today_d - newest_dev.date()).days if newest_dev is not None else None
        catchup = stale_days is not None and stale_days >= CATCHUP_DAYS

        last_covered = coverage.get(slug)
        covered_recently = last_covered is not None and last_covered >= recent_cutoff
        if last_covered is None:
            tag = "NEW"
        elif last_covered == last_digest:
            tag = "UPDATE"
        elif covered_recently:
            tag = "REVISIT"
        else:
            tag = "REVISIT"
        rows.append({
            "slug": slug,
            "title": s.get("title", ""),
            "score": s.get("score", 0.0),
            "hot": s.get("score", 0.0) >= ANALYSIS_GATE,
            "n_events": len(ev_dates),
            "new_events_since": new_events,
            "newest_event_at": max(ev_dates).strftime("%Y-%m-%d") if ev_dates else None,
            "newest_development_at": newest_dev.strftime("%Y-%m-%d") if newest_dev else None,
            "stale_days": stale_days,
            "catchup": catchup,
            "kev_added": kev_added.isoformat() if kev_added else None,
            "has_analysis": an_at is not None,
            "analysis_at": an_at.strftime("%Y-%m-%d") if an_at else None,
            "last_covered": last_covered,
            "covered_recently": covered_recently,
            "tag": tag,
            "evolved": evolved,
            "n_sources": s.get("n_sources", 0),
            "cves": cves,
        })
    return rows


def build_bench(rows, slate, stories, events):
    """Wildcard discovery bench: live stories OUTSIDE the deterministic slate
    (not evolved, not hot-uncovered, not in yesterday's coverage) that carry
    at least one weirdness flag. Slate scores are advisory priors; the bench
    is where the digest agent looks for stories the proxy score under-ranks:
    multi-outlet bursts, CVE clusters, regional (translated) scoops, near-gate
    scores. Ranked by flag count then score, capped at BENCH_MAX."""
    out = []
    for r in rows:
        if r["slug"] in slate or r["score"] < BENCH_SCORE_FLOOR or not r["n_events"]:
            continue  # slate members, sub-floor noise, and emptied ghosts never bench
        flags = []
        if r["n_sources"] >= 5:
            flags.append("burst")
        if len(r["cves"]) >= 3:
            flags.append("cve-rich")
        if r["score"] >= ANALYSIS_GATE * NEAR_GATE and not r["hot"]:
            flags.append("near-gate")
        s = stories.get(r["slug"], {})
        if any(events.get(ref.get("event_id"), {}).get("translated_from")
               for ref in s.get("events", [])):
            flags.append("regional")
        if flags:
            out.append({"slug": r["slug"], "title": r["title"], "score": r["score"],
                        "n_sources": r["n_sources"], "flags": flags,
                        "last_covered": r["last_covered"]})
    out.sort(key=lambda b: (-len(b["flags"]), -b["score"]))
    return out[:BENCH_MAX]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="digest date (default: today UTC)")
    ap.add_argument("--kev-data", default=KEV_DATA_DIR, help="kevrichment data dir (index.json)")
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
    kev_map = kev_date_map(args.kev_data)

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

    rows = build_rows(stories, events, kev_map, coverage, canonical,
                      since, recent_cutoff, today, last_digest)
    by_score = sorted(rows, key=lambda r: -r["score"])
    evolved = [r for r in by_score if r["evolved"]]
    uncovered = [r for r in by_score if r["hot"] and not r["covered_recently"]]
    yesterday_rows = sorted(
        (r for r in rows if r["slug"] in yesterday), key=lambda r: -r["score"])
    slate = ({r["slug"] for r in evolved} | {r["slug"] for r in uncovered} | yesterday)
    bench = build_bench(rows, slate, stories, events)

    def flag(r):
        parts = []
        if r["catchup"]:
            parts.append("CATCH-UP")
        if r["stale_days"] is not None and r["stale_days"] >= 1:
            parts.append(f"dev={r['newest_development_at']} ({r['stale_days']}d old)")
        elif r["newest_development_at"]:
            parts.append(f"dev={r['newest_development_at']}")
        return (" " + " ".join(parts)).rstrip()

    def fmt(r):
        ev = f"+{r['new_events_since']}ev" if r["new_events_since"] else "   "
        an = f"an={r['analysis_at']}" if r["has_analysis"] else "an=-   "
        cov = r["last_covered"] or "never"
        return (f"[{r['tag']:<7}] {r['score']:4.1f}  {ev}  {an}  "
                f"cov={cov:<10} {r['slug']}")

    print(f"Tia N. List — daily digest coverage brief")
    print(f"Date: {today} | Last digest: {last_digest} "
          f"({len(yesterday)} stories) | Delta boundary: after {since:%Y-%m-%d}T00:00Z")
    print(f"Coverage window: stories not covered since {recent_cutoff} count as uncovered")
    print(f"Freshness: dev= newest genuine development (recap articles about older KEV adds "
          f"don't count); CATCH-UP = newest development >= {CATCHUP_DAYS} days old — nothing new today")
    print(f"Scores are ADVISORY priors (severity/velocity/breadth proxy), not editorial "
          f"verdicts: promote/demote freely, log every deviation in the digest json overrides\n")

    print(f"YESTERDAY'S COVERAGE ({len(yesterday_rows)}) — baseline for [UPDATE] deltas")
    for r in yesterday_rows:
        mark = "EVOLVED" if r["evolved"] else "static "
        print(f" {mark} {r['score']:4.1f} +{r['new_events_since']}ev "
              f"{r['slug']}{flag(r)} — {r['title'][:80]}")
    print()

    print(f"EVOLVED SINCE LAST DIGEST ({len(evolved)}) — genuine developments (new events or KEV adds), score desc")
    for r in evolved:
        print(" " + fmt(r) + flag(r) + f" — {r['title'][:70]}")
    print()

    print(f"HOT & UNCOVERED ({len(uncovered)}) — score >= {ANALYSIS_GATE}, not covered since {recent_cutoff}")
    for r in uncovered:
        print(" " + fmt(r) + flag(r) + f" — {r['title'][:70]}")

    print(f"\nBENCH ({len(bench)}) — outside the slate, flagged for wildcard consideration "
          f"(burst >=5 sources, cve-rich >=3 CVEs, regional = non-EN origin, near-gate score). "
          f"Wildcard picks may also come from anywhere in the store.")
    for b in bench:
        cov = b["last_covered"] or "never"
        print(f"  {b['score']:4.1f} [{','.join(b['flags']):<24}] cov={cov:<10} "
              f"{b['slug']} — {b['title'][:60]}")

    payload = {
        "date": today,
        "last_digest": last_digest,
        "delta_boundary": since.isoformat(),
        "coverage_window": COVERAGE_WINDOW,
        "recap_days": RECAP_DAYS,
        "catchup_days": CATCHUP_DAYS,
        "yesterday": yesterday_rows,
        "evolved": evolved,
        "uncovered": uncovered,
        "bench": bench,
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
