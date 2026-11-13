#!/usr/bin/env python3
"""Daily bulk EPSS refresh (FIRST / Empirical Security).

Downloads the full EPSS score database once a day (the whole corpus is a
~2.6MB gzip — orders of magnitude cheaper and fresher than per-CVE API
lookups, which would freeze stale values into published pages) and merges
the scores into the per-CVE enrichment records this package maintains.

Design notes:
  - The bulk artifact is CACHED, never committed: data/epss/ holds up to
    CACHE_KEEP_DAYS dated snapshots so 7-day deltas come free from files
    we already have. The hourly kev pipeline may rebuild records from
    sources and drop the epss fields (build_cve_record constructs fresh);
    the next daily refresh restores them — self-healing by design.
  - Merge is read-modify-write on the epss* keys only; agent-researched
    fields are never touched.
  - Every stored value carries its score date. Consumers (score.py, the
    /kev/ pages) must treat EPSS as a daily series, not a constant.

Usage:  python kevrichment/epss.py        (idempotent per score_date)
Output: final line `epss: <score_date> refreshed <changed>/<total> records
        (cache <k> files)` — parsed by the epss-refresh cron job.
"""
import csv
import glob
import gzip
import io
import json
import os
import re
from datetime import datetime, timedelta, timezone

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CVE_DIR = os.path.join(HERE, "data", "cves")
CACHE_DIR = os.path.join(HERE, "data", "epss")
EPSS_URL = "https://epss.cyentia.com/epss_scores-current.csv.gz"  # 301 -> epss.empiricalsecurity.com
CACHE_KEEP_DAYS = 35
# Published trend series (data/epss-history.json) for the site's per-CVE EPSS
# panel. The snapshot cache itself is never committed (2.6 MB/day); this is a
# compact downsample: HISTORY_DAYS points, scores scaled to integers.
HISTORY_PATH = os.path.join(HERE, "data", "epss-history.json")
HISTORY_DAYS = 21
HISTORY_SCALE = 1000
DELTA_DAYS = 7
TIMEOUT = 120

_HEADER_DATE = re.compile(r"score_date:(\d{4}-\d{2}-\d{2})")


def _cache_path(score_date):
    return os.path.join(CACHE_DIR, f"epss_scores-{score_date}.csv.gz")


def fetch(today=None):
    """Download today's bulk file into the cache; returns (score_date, path).

    Idempotent: if today's snapshot is already cached, no download."""
    today = today or datetime.now(timezone.utc).date()
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = os.path.join(CACHE_DIR, ".fetch.tmp")
    resp = requests.get(EPSS_URL, timeout=TIMEOUT)
    resp.raise_for_status()
    with open(tmp, "wb") as f:
        f.write(resp.content)
    score_date, _scores = parse(tmp)
    path = _cache_path(score_date)
    os.replace(tmp, path)
    if score_date != today.isoformat():
        # model publication lags/gaps happen; the score_date IS the truth —
        # the caller's daily guard keys on it, not the wall clock
        print(f"epss: note — latest published score_date {score_date} "
              f"(today {today.isoformat()})")
    _prune_cache()
    return score_date, path


def parse(path):
    """Parse a cached bulk file -> (score_date, {cve: (epss, percentile)}).

    File format: a `#model_version:..,score_date:YYYY-MM-DD` meta line, then
    a `cve,epss,percentile` header and one row per CVE."""
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        head = f.readline(512)
    m = _HEADER_DATE.search(head)
    score_date = m.group(1) if m else ""
    scores = {}
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(
                line for line in f if not line.startswith("#")):
            cve = (row.get("cve") or "").strip()
            if cve:
                scores[cve] = (row.get("epss") or "", row.get("percentile") or "")
    return score_date, scores


def _prior_snapshot(score_date):
    """Newest cached snapshot at least DELTA_DAYS old, for the 7d delta."""
    try:
        cutoff = (datetime.strptime(score_date, "%Y-%m-%d").date()
                  - timedelta(days=DELTA_DAYS)).isoformat()
    except ValueError:
        return None, {}
    best, best_scores = None, {}
    for p in sorted(glob.glob(os.path.join(CACHE_DIR, "epss_scores-*.csv.gz"))):
        d = os.path.basename(p)[len("epss_scores-"):-len(".csv.gz")]
        if d <= cutoff and (best is None or d > best):
            best, best_scores = d, parse(p)[1]
    return best, best_scores


def _prune_cache():
    cutoff = (datetime.now(timezone.utc).date()
              - timedelta(days=CACHE_KEEP_DAYS)).isoformat()
    for p in glob.glob(os.path.join(CACHE_DIR, "epss_scores-*.csv.gz")):
        d = os.path.basename(p)[len("epss_scores-"):-len(".csv.gz")]
        if d < cutoff:
            os.remove(p)


def enrich(score_date, scores, prev_scores):
    """Merge epss fields into kevrichment/data/cves/*.json (read-modify-write
    on epss* keys only). Returns (changed, total)."""
    changed = 0
    total = 0
    for path in sorted(glob.glob(os.path.join(CVE_DIR, "*.json"))):
        total += 1
        try:
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
        except (OSError, ValueError):
            continue
        cve = rec.get("cve_id") or os.path.basename(path)[:-5]
        cur = scores.get(cve)
        if cur is None:
            continue                      # not in today's corpus — leave as-is
        epss, pct = cur
        prev = prev_scores.get(cve, ("", ""))[0]
        fields = {
            "epss": float(epss) if epss else None,
            "epss_percentile": float(pct) if pct else None,
            "epss_date": score_date,
        }
        if prev:
            try:
                fields["epss_prev"] = float(prev)
                fields["epss_delta_7d"] = round(fields["epss"] - float(prev), 5)
            except ValueError:
                pass
        if all(rec.get(k) == v for k, v in fields.items()):
            continue
        rec.update(fields)
        with open(path, "w", encoding="utf-8") as f:
            # Canonical serialization (indent=2), matching every other writer
            # of these records (main.py, kev_seq_backfill.py, burndown.py).
            # indent=1 here re-indented all ~1,780 files on each daily
            # refresh — ~171k changed lines and ~30 MB/month of git history
            # for a few changed score fields per record (2026-11-13).
            json.dump(rec, f, indent=2)
        changed += 1
    return changed, total


def write_history(days=HISTORY_DAYS, cve_dir=None):
    """Write the committed 21-day EPSS series for the CVEs we publish.

    The site builds from a clean clone, so it cannot read the untracked
    snapshot cache — this file is the small, reviewable projection the /kev/
    CVE pages use for their EPSS trend. Values are integers scaled by
    HISTORY_SCALE (0.0162 -> 16); a CVE missing from a snapshot is null.

    Returns the number of series written (0 when there is no cache at all).
    """
    cve_dir = cve_dir or CVE_DIR
    snaps = sorted(glob.glob(os.path.join(CACHE_DIR, "epss_scores-*.csv.gz")))
    snaps = snaps[-days:]
    if not snaps:
        return 0
    dates, per_date = [], []
    for path in snaps:
        date_, scores = parse(path)
        dates.append(date_)
        per_date.append(scores)
    cves = sorted(os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(cve_dir, "CVE-*.json")))
    series = {}
    for cve in cves:
        row = []
        for scores in per_date:
            hit = scores.get(cve)
            row.append(int(round(float(hit[0]) * HISTORY_SCALE)) if hit else None)
        series[cve] = row
    doc = {"schema": 1, "scale": HISTORY_SCALE, "dates": dates, "series": series}
    text = json.dumps(doc, separators=(",", ":"), sort_keys=True) + "\n"
    try:
        if open(HISTORY_PATH, encoding="utf-8").read() == text:
            return len(series)          # write-if-changed: no daily churn
    except OSError:
        pass
    tmp = HISTORY_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, HISTORY_PATH)
    return len(series)


def main():
    score_date, path = fetch()
    scores = parse(path)[1]
    prev_date, prev_scores = _prior_snapshot(score_date)
    changed, total = enrich(score_date, scores, prev_scores)
    series = write_history()
    cached = len(glob.glob(os.path.join(CACHE_DIR, "epss_scores-*.csv.gz")))
    print(f"epss: {score_date} history: {series} series in "
          f"{os.path.basename(HISTORY_PATH)}")
    print(f"epss: {score_date} refreshed {changed}/{total} records "
          f"(cache {cached} files"
          f"{f', delta vs {prev_date}' if prev_date else ', no prior snapshot'})")


if __name__ == "__main__":
    main()
