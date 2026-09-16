#!/usr/bin/env python3
"""One-time backfill of the ingest-time catalog fingerprint (kev_seq /
kev_catalog_count) onto existing kevrichment records.

Records enriched before the fingerprint existed carry only the date-only
kev_date_added, so same-day additions sort alphabetically and the KEV feed
published the day's FIRST addition on top — burying later ones where
pubDate-based RSS readers never see them (2026-09-16: CVE-2026-87886, the
day's last KEV addition, rendered at the bottom of the day's trio).

CISA's catalog JSON is newest-DAY-first, and within a day's block entries
sit in insertion order (oldest first — verified live 2026-09-16), so an
entry's position in the CURRENT snapshot preserves its true insertion order
relative to its same-day siblings. This pass stamps that position
(kev_seq) plus the snapshot count (kev_catalog_count) onto every record
that lacks them, then rebuilds data/index.json through
schema.sort_index_entries. Records absent from the catalog (removed KEV
entries, non-KEV vulnrichment-scan records) are left untouched and keep
sorting by dateAdded alone.

Idempotent: records already carrying kev_seq are skipped unless --force.
All-or-nothing planning: every planned write is validated before the first
file is touched. Safe to re-run.

Output: human lines, then ONE JSON summary line (last line):

  {"catalog_count": N, "stamped": n1, "already": n2, "absent": n3,
   "index_entries": n4, "index_skipped": [...]}

Exit codes: 0 ok · 2 validation abort (nothing written) · 3 catalog fetch failed.
"""
import argparse
import glob
import json
import os
import sys

KEV = os.path.dirname(os.path.abspath(__file__))
if KEV not in sys.path:
    sys.path.insert(0, KEV)

import ingest  # noqa: E402 — seam reuse: fetch_kev (single upstream touchpoint)
from schema import sort_index_entries  # noqa: E402
import ssvc_refresh  # noqa: E402 — seam reuse: rebuild_index (same shape)

DEFAULT_REPO = os.path.dirname(KEV)


def plan_backfill(records_dir, seq_by_cve, catalog_count, force=False):
    """Compute (summary, plans, fatal). plans = [(cve_id, path, record)]."""
    summary = {"catalog_count": catalog_count, "stamped": 0,
               "already": 0, "absent": 0}
    plans, fatal = [], []
    for path in sorted(glob.glob(os.path.join(records_dir, "CVE-*.json"))):
        cve_id = os.path.basename(path)[:-len(".json")]
        try:
            with open(path) as f:
                rec = json.load(f)
        except (OSError, ValueError) as e:
            fatal.append(f"{cve_id}: unreadable record ({e})")
            continue
        if rec.get("cve_id") != cve_id:
            fatal.append(f"{cve_id}: cve_id mismatch inside file")
            continue
        if not force and isinstance(rec.get("kev_seq"), int) \
                and rec.get("kev_catalog_count") is not None:
            summary["already"] += 1
            continue
        if cve_id not in seq_by_cve:
            summary["absent"] += 1  # dropped from KEV / non-KEV scan record
            continue
        new_rec = dict(rec)
        new_rec["kev_seq"] = seq_by_cve[cve_id]
        new_rec["kev_catalog_count"] = catalog_count
        plans.append((cve_id, path, new_rec))
        summary["stamped"] += 1
    return summary, plans, fatal


def _validate_plans(plans):
    bad = []
    for cve_id, _path, new_rec in plans:
        if new_rec.get("cve_id") != cve_id:
            bad.append(f"{cve_id}: plan would change cve_id")
        if not isinstance(new_rec.get("kev_seq"), int) \
                or new_rec.get("kev_catalog_count") is None:
            bad.append(f"{cve_id}: plan missing kev_seq/kev_catalog_count")
        try:
            json.dumps(new_rec)
        except (TypeError, ValueError) as e:
            bad.append(f"{cve_id}: planned record not JSON-serializable ({e})")
    return bad


def apply_plans(plans):
    written = 0
    for _cve_id, path, new_rec in plans:
        tmp = path + ".seq-tmp"
        with open(tmp, "w") as f:
            json.dump(new_rec, f, indent=2)
        os.replace(tmp, path)
        written += 1
    return written


def load_catalog(catalog_path=None):
    """Fetch the live catalog, or load --catalog PATH (offline/tests)."""
    if catalog_path:
        with open(catalog_path) as f:
            return json.load(f)
    return ingest.fetch_kev()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--repo", default=DEFAULT_REPO,
                   help="tia-n-list repo root (default: this checkout)")
    p.add_argument("--catalog", default=None,
                   help="local catalog JSON instead of fetching from CISA")
    p.add_argument("--force", action="store_true",
                   help="re-stamp records that already carry kev_seq")
    p.add_argument("--dry-run", action="store_true",
                   help="plan + report, write nothing")
    args = p.parse_args(argv)

    try:
        catalog = load_catalog(args.catalog)
    except Exception as e:  # noqa: BLE001 — fetch failure is the caller's retry signal
        print(f"ABORT: catalog fetch failed: {e}")
        return 3
    vulnerabilities = catalog.get("vulnerabilities", [])
    seq_by_cve = {e.get("cveID"): i for i, e in enumerate(vulnerabilities)}
    catalog_count = catalog.get("count", len(vulnerabilities))

    records_dir = os.path.join(args.repo, "kevrichment", "data", "cves")
    summary, plans, fatal = plan_backfill(records_dir, seq_by_cve,
                                          catalog_count, force=args.force)

    rc = 0
    if fatal:
        print(f"ABORT: {len(fatal)} unreadable/mismatched record(s) — "
              f"nothing written:")
        for f_ in fatal[:10]:
            print(f"  ✗ {f_}")
        rc = 2
    else:
        bad = _validate_plans(plans)
        if bad:
            print(f"ABORT: {len(bad)} invalid plan(s) — nothing written:")
            for b in bad[:10]:
                print(f"  ✗ {b}")
            rc = 2

    if rc == 0 and not args.dry_run:
        for cve_id, _path, new_rec in plans:
            print(f"  ↻ {cve_id}: kev_seq={new_rec['kev_seq']} "
                  f"count={new_rec['kev_catalog_count']}")
        apply_plans(plans)
        entries, skipped = ssvc_refresh.rebuild_index(repo=args.repo)
        summary["index_entries"] = entries
        summary["index_skipped"] = skipped
        print(f"Index: {entries} entries" +
              (f"; skipped: {skipped}" if skipped else ""))
    elif args.dry_run:
        for cve_id, _path, new_rec in plans:
            print(f"  DRY {cve_id}: kev_seq={new_rec['kev_seq']} "
                  f"count={new_rec['kev_catalog_count']}")

    print(json.dumps(summary))
    return rc


if __name__ == "__main__":
    sys.exit(main())
