#!/usr/bin/env python3
"""Daily SSVC refresh — reconcile kevrichment records with cisagov/vulnrichment.

SSVC data is captured ONCE at first ingest (main.py -> ingest.fetch_vulnrichment);
after that _cve_needs_research skips the CVE forever, while CISA keeps revising
vulnrichment entries ("data updated" commits). Records can also carry
agent-authored vulnrichment blocks (burndown rewrites whole records) that never
matched upstream — 2026-09-08: CVE-2026-81963 shipped automatable=unknown /
technical_impact=unknown while upstream said no/total (and stayed wrong for
days, materially under-stating its BOD 26-04 timeline). This pass re-fetches
upstream SSVC for every record and updates the vulnrichment + bod_26_04 blocks
deterministically — no agent, no research-field changes, last_researched
untouched.

Rules:

- A field is updated only when upstream actually states it. Keys absent
  upstream extract as "unknown" and NEVER overwrite an existing value.
- 404 (no vulnrichment file) or no CISA-ADP SSVC options yet -> untouched.
- Network error after retries -> untouched, counted in ``fetch_errors``;
  when errors are the majority the run exits nonzero so the caller retries
  next hour instead of marking the day refreshed.
- exploitation_status syncs upstream exactly like the deterministic ingest
  would have written it (KEV membership is NOT pinned to "active" — the
  corpus already publishes upstream none/poc values for KEV records).
- bod_26_04 is recomputed from the final SSVC values via
  schema.compute_bod_timeline (in_kev = the record's own kev_date_added).
- All-or-nothing: every planned write is validated before the first file is
  touched; a validation abort leaves the tree untouched. A crash mid-write
  is safe anyway: the next run recomputes everything (idempotent).
- vulnrichment.refreshed = reconciliation timestamp, written only when a
  record's values actually changed (proof of upstream verification).

Output: human lines on stdout, then ONE JSON summary line (last line):

  {"checked": N, "upstream_ok": n1, "upstream_absent": n2, "fetch_errors": n3,
   "changed": M, "cves_changed": ["CVE-...", ...]}

Exit codes: 0 ok · 2 validation abort (nothing written) · 3 majority fetch
errors (nothing written).
"""
import glob
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

KEV = os.path.dirname(os.path.abspath(__file__))
if KEV not in sys.path:
    sys.path.insert(0, KEV)

import ingest  # noqa: E402 — seam reuse: _vulnrichment_path, _extract_ssvc_from_dict
from schema import build_index_entry, compute_bod_timeline  # noqa: E402

DEFAULT_REPO = os.path.dirname(KEV)          # tia-n-list repo root
DEFAULT_DELAY = 0.25                          # seconds between raw fetches
ATTEMPTS = 3                                  # per-CVE fetch attempts
BACKOFF = 2.0                                 # seconds, linear

# Upstream SSVC vocabulary (values already lowercased by extraction). Anything
# outside these sets is treated as "not stated" and never written.
ALLOWED = {
    "automatable": {"yes", "no"},
    "technical_impact": {"total", "partial"},
    "exploitation": {"active", "poc", "none"},
}
# upstream extraction key -> record field name
FIELD_MAP = (
    ("automatable", "automatable"),
    ("technical_impact", "technical_impact"),
    ("exploitation", "exploitation_status"),
)
RECORD_KEYS = ("automatable", "technical_impact", "exploitation_status")


# ---------------------------------------------------------------------------
# Upstream fetch
# ---------------------------------------------------------------------------

def fetch_upstream_ssvc(cve_id, attempts=ATTEMPTS, backoff=BACKOFF):
    """Fetch + extract upstream SSVC options for one CVE.

    Returns ``("ok", options_dict)``, ``("absent", None)`` (404 or no SSVC
    options yet — a legitimate state, not an error), or ``("error", None)``
    (network/parse failure after retries).
    """
    path = ingest._vulnrichment_path(cve_id)
    if not path:
        return "absent", None
    url = f"{ingest.VULNRICHMENT_RAW}/{path}"
    last_exc = None
    for i in range(attempts):
        try:
            resp = requests.get(url, headers={"User-Agent": ingest.USER_AGENT},
                                timeout=15)
            if resp.status_code == 404:
                return "absent", None
            resp.raise_for_status()
            return "ok", ingest._extract_ssvc_from_dict(resp.json())
        except (requests.RequestException, json.JSONDecodeError, ValueError) as e:
            last_exc = e
            if i < attempts - 1:
                time.sleep(backoff * (i + 1))
    print(f"  [WARN] vulnrichment fetch failed for {cve_id}: {last_exc}",
          file=sys.stderr)
    return "error", None


# ---------------------------------------------------------------------------
# Planning (pure — no writes)
# ---------------------------------------------------------------------------

def _record_triple(rec):
    v = rec.get("vulnrichment") or {}
    return tuple(str(v.get(k, "unknown")).lower() for k in RECORD_KEYS)


def plan_refresh(repo=None, records_dir=None, fetch=None, now=None,
                 delay=DEFAULT_DELAY, limit=None, only=None):
    """Compute the update plan for every record under data/cves/.

    Returns ``(summary, plans, fatal)``: ``plans`` is a list of
    ``(cve_id, path, new_record, old_triple, new_triple)``; ``fatal`` holds
    validation-failure strings (unreadable records) — any fatal aborts the
    whole run BEFORE any write (all-or-nothing).
    """
    repo = repo or DEFAULT_REPO
    records_dir = records_dir or os.path.join(repo, "kevrichment", "data", "cves")
    fetch = fetch or fetch_upstream_ssvc
    now = now or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    only = set(only or [])

    summary = {"checked": 0, "upstream_ok": 0, "upstream_absent": 0,
               "fetch_errors": 0, "changed": 0, "cves_changed": []}
    plans = []
    fatal = []

    for path in sorted(glob.glob(os.path.join(records_dir, "CVE-*.json"))):
        cve_id = os.path.basename(path)[:-len(".json")]
        if only and cve_id not in only:
            continue
        try:
            with open(path) as f:
                rec = json.load(f)
        except (OSError, ValueError) as e:
            fatal.append(f"{cve_id}: unreadable record ({e})")
            continue
        if rec.get("cve_id") != cve_id:
            fatal.append(f"{cve_id}: cve_id mismatch inside file")
            continue
        summary["checked"] += 1

        status, ssvc = fetch(cve_id)
        if status == "error":
            summary["fetch_errors"] += 1
            continue
        if status == "absent" or not ssvc:
            summary["upstream_absent"] += 1
            continue
        summary["upstream_ok"] += 1

        old_triple = _record_triple(rec)
        new_triple = list(old_triple)
        for up_key, rec_key in FIELD_MAP:
            val = str(ssvc.get(up_key, "")).strip().lower()
            if val in ALLOWED[up_key]:
                new_triple[RECORD_KEYS.index(rec_key)] = val
        new_triple = tuple(new_triple)

        in_kev = bool(rec.get("kev_date_added"))
        new_bod = compute_bod_timeline(new_triple[0], new_triple[1], in_kev)
        old_bod = rec.get("bod_26_04") or {}
        bod_same = all(old_bod.get(k) == v for k, v in new_bod.items())

        if new_triple == old_triple and bod_same:
            continue
        if limit and len(plans) >= limit:
            continue

        vuln = dict(rec.get("vulnrichment") or {})
        vuln.update(dict(zip(RECORD_KEYS, new_triple)))
        vuln["refreshed"] = now
        new_rec = dict(rec)
        new_rec["vulnrichment"] = vuln
        new_rec["bod_26_04"] = new_bod
        plans.append((cve_id, path, new_rec, old_triple, new_triple))
        time.sleep(delay)

    summary["changed"] = len(plans)
    summary["cves_changed"] = [p[0] for p in plans]
    return summary, plans, fatal


# ---------------------------------------------------------------------------
# Apply (validated, then atomic per-record writes + index rebuild)
# ---------------------------------------------------------------------------

def _validate_plans(plans):
    """Re-check every planned record; returns a list of fatal strings."""
    bad = []
    for cve_id, _path, new_rec, _old, new_triple in plans:
        if new_rec.get("cve_id") != cve_id:
            bad.append(f"{cve_id}: plan would change cve_id")
        for k, v in zip(RECORD_KEYS, new_triple):
            allowed = ALLOWED[FIELD_MAP[RECORD_KEYS.index(k)][0]] | {"unknown"}
            if v not in allowed:
                bad.append(f"{cve_id}: {k}={v!r} outside SSVC vocabulary")
        try:
            json.dumps(new_rec)
        except (TypeError, ValueError) as e:
            bad.append(f"{cve_id}: planned record not JSON-serializable ({e})")
    return bad


def apply_plans(plans):
    """Write planned records atomically (tmp + replace). Returns #written."""
    written = 0
    for cve_id, path, new_rec, _old, _new in plans:
        tmp = path + ".ssvc-tmp"
        with open(tmp, "w") as f:
            json.dump(new_rec, f, indent=2)
        os.replace(tmp, path)
        written += 1
    return written


def rebuild_index(repo=None, records_dir=None):
    """Rebuild kevrichment/data/index.json from the corpus (kev-verify shape)."""
    repo = repo or DEFAULT_REPO
    records_dir = records_dir or os.path.join(repo, "kevrichment", "data", "cves")
    index_path = os.path.join(repo, "kevrichment", "data", "index.json")
    prev = {}
    try:
        with open(index_path) as f:
            prev = json.load(f)
    except (OSError, ValueError):
        pass
    entries, skipped = [], []
    for path in sorted(glob.glob(os.path.join(records_dir, "CVE-*.json"))):
        try:
            with open(path) as f:
                rec = json.load(f)
            entries.append(build_index_entry(rec))
        except (OSError, ValueError, KeyError) as e:
            skipped.append(f"{os.path.basename(path)}: {e}")
    entries.sort(key=lambda e: e.get("kev_date_added", "") or "", reverse=True)
    index = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kev_source_date": prev.get("kev_source_date", ""),
        "total_cves_processed": len(entries),
        "cves": entries,
    }
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
    return len(entries), skipped


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    import argparse
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--repo", default=DEFAULT_REPO,
                   help="tia-n-list repo root (default: this checkout)")
    p.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                   help="seconds between upstream fetches")
    p.add_argument("--limit", type=int, default=None,
                   help="stop after N planned changes (smoke tests)")
    p.add_argument("--only", default="",
                   help="comma-separated CVE ids to refresh (default: all)")
    p.add_argument("--dry-run", action="store_true",
                   help="plan + report, write nothing")
    args = p.parse_args(argv)
    only = [c.strip() for c in args.only.split(",") if c.strip()]

    summary, plans, fatal = plan_refresh(
        repo=args.repo, delay=0.0 if args.delay <= 0 else args.delay,
        limit=args.limit, only=only)

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
        elif summary["checked"] and summary["fetch_errors"] * 2 > summary["checked"]:
            print(f"ABORT: {summary['fetch_errors']}/{summary['checked']} "
                  f"fetches failed (majority) — nothing written, upstream "
                  f"likely unreachable")
            rc = 3

    if rc == 0 and not args.dry_run:
        for cve_id, _path, new_rec, old, new in plans:
            print(f"  ↻ {cve_id}: " +
                  ", ".join(f"{k} {o}→{n}" for k, o, n
                            in zip(RECORD_KEYS, old, new) if o != n))
        apply_plans(plans)
        entries, skipped = rebuild_index(repo=args.repo)
        print(f"Index: {entries} entries" +
              (f"; skipped: {skipped}" if skipped else ""))
    elif args.dry_run:
        for cve_id, _path, _rec, old, new in plans:
            print(f"  DRY {cve_id}: " +
                  ", ".join(f"{k} {o}→{n}" for k, o, n
                            in zip(RECORD_KEYS, old, new) if o != n))

    print(json.dumps(summary))
    return rc


if __name__ == "__main__":
    sys.exit(main())
