#!/usr/bin/env python3
"""
kevrichment — CISA KEV + Vulnrichment enrichment pipeline.

Orchestrates ingest, agentic research, and output-schema publication.

Usage
-----
    python main.py                          # standalone mode (requests-based)
    python main.py --agent                  # agent mode (requires hermes_tools)

In agent mode the research engine uses Hermes ``web_search`` / ``web_extract``
tools for richer web research.  In standalone mode it falls back to the GitHub
API and direct URL heuristics.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from ingest import (
    fetch_kev,
    get_latest_kev_entries,
    get_kev_source_date,
    fetch_vulnrichment,
    fetch_nvd,
)
from research import ResearchEngine, research_cve
from schema import (
    build_cve_record,
    build_index_entry,
    build_run_log,
    validate_cve_record,
)

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
CVES_DIR = DATA_DIR / "cves"
RUNS_DIR = DATA_DIR / "runs"
INDEX_PATH = DATA_DIR / "index.json"
LATEST_PATH = BASE_DIR / "latest.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_dirs():
    for d in (DATA_DIR, CVES_DIR, RUNS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def _load_index():
    if INDEX_PATH.exists():
        with open(INDEX_PATH) as f:
            return json.load(f)
    return {"last_updated": "", "kev_source_date": "", "total_cves_processed": 0, "cves": []}


def _save_index(data):
    with open(INDEX_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Index saved ({len(data['cves'])} entries)")


def _cve_needs_research(cve_id, kev_date_added, existing_index):
    """Skip if the CVE file exists and its KEV date hasn't changed."""
    for entry in existing_index.get("cves", []):
        if entry["cve_id"] == cve_id:
            cve_file = BASE_DIR / entry.get("file", "")
            if cve_file.exists() and entry.get("kev_date_added") == kev_date_added:
                return False
    return True


def _load_run_log(run_id):
    return {
        "run_id": run_id,
        "cves_processed": 0,
        "cves_skipped": 0,
        "skip_reason": "",
        "total_wall_time_seconds": 0,
        "total_tokens_used": None,
        "avg_time_per_cve_seconds": 0,
        "avg_tokens_per_cve": None,
        "errors": [],
    }


def _save_cve(record):
    path = CVES_DIR / f"{record['cve_id']}.json"
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    print(f"  ✓ Saved: {path.name}")


def _save_run_log(run_log):
    run_id = run_log["run_id"]
    path = RUNS_DIR / f"{run_id}.json"
    with open(path, "w") as f:
        json.dump(run_log, f, indent=2)
    with open(LATEST_PATH, "w") as f:
        json.dump(run_log, f, indent=2)
    print(f"  ✓ Run log: {path}")
    print(f"  ✓ latest.json updated")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(research_engine=None, nvd_api_key=None):
    """Execute the full kevrichment pipeline.

    Parameters
    ----------
    research_engine : ResearchEngine or None
        Pass a pre-configured engine (with Hermes tools) for agent mode.
        ``None`` uses a default standalone engine.
    nvd_api_key : str or None
        NVD API 2.0 key.  Falls back to ``NVD_API_KEY`` env var in
        :func:`ingest.fetch_nvd` if not provided here.
    """
    run_id = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"╔══ kevrichment run {run_id} ══╗\n")

    _ensure_dirs()
    run_log = _load_run_log(run_id)
    existing_index = _load_index()
    wall_start = time.time()

    # ---- 1.  Fetch KEV ---------------------------------------------------
    print("[1/4] Fetching CISA KEV …")
    try:
        kev_data = fetch_kev()
    except Exception as e:
        print(f"  ✗ Fatal: KEV fetch failed — {e}")
        run_log["errors"].append(f"KEV fetch: {e}")
        _save_run_log(run_log)
        sys.exit(1)

    kev_source_date = get_kev_source_date(kev_data)
    total_entries = len(kev_data.get("vulnerabilities", []))
    print(f"  Source: {kev_source_date}  |  Total entries: {total_entries}")

    # ---- 2.  Select 5 most recent ----------------------------------------
    print("\n[2/4] Top 5 most recently added KEV entries …")
    latest = get_latest_kev_entries(kev_data, count=5)
    for i, e in enumerate(latest, 1):
        print(f"  {i:>2}. {e['cveID']:20s}  {e.get('vendorProject','?'):20s}  "
              f"{e.get('product','?'):25s}  added {e.get('dateAdded','?')}")

    # ---- 3.  Process each CVE --------------------------------------------
    print("\n[3/4] Processing …")
    updated_entries = []
    cves_processed = 0
    cves_skipped = 0
    errors = []

    if research_engine is None:
        research_engine = ResearchEngine()  # standalone mode

    for i, entry in enumerate(latest, 1):
        cve_id = entry["cveID"]
        kev_date = entry.get("dateAdded", "")

        print(f"\n  ── {i}/{len(latest)}  {cve_id} ──")
        print(f"  {entry.get('vulnerabilityName','')}")

        # Incremental check
        if not _cve_needs_research(cve_id, kev_date, existing_index):
            print(f"  → SKIP (no KEV update since last research)")
            for idx_entry in existing_index.get("cves", []):
                if idx_entry["cve_id"] == cve_id:
                    updated_entries.append(idx_entry)
                    break
            cves_skipped += 1
            continue

        t0 = time.time()

        # Vulnrichment
        print(f"  • Vulnrichment …", end=" ")
        vuln = fetch_vulnrichment(cve_id)
        if vuln:
            print(f"auto={vuln.get('automatable','?')}  impact={vuln.get('technical_impact','?')}  "
                  f"exploit={vuln.get('exploitation','?')}")
        else:
            print("(none)")

        # NVD
        print(f"  • NVD …", end=" ")
        nvd = fetch_nvd(cve_id, api_key=nvd_api_key)
        print("ok" if nvd else "failed")

        # Extract description from NVD
        desc = ""
        if nvd:
            for d in (nvd.get("vulnerabilities") or [{}])[0].get("cve", {}).get("descriptions", []):
                if d.get("lang") == "en":
                    desc = d.get("value", "")
                    break

        # Research
        print(f"  • Research …")
        research_data = research_engine.research(
            cve_id, entry.get("vendorProject", ""), entry.get("product", ""),
            desc, nvd_data=nvd, vulnrichment_data=vuln,
        )
        wall = time.time() - t0
        print(f"    Component: {research_data['vulnerable_component'][:80]}")
        print(f"    PoC: {research_data['public_poc_exists']:>4s}  "
              f"Default: {research_data['vulnerable_component_enabled_by_default']:>8s}  "
              f"({wall:.1f}s)")

        # Research meta
        sources = list(research_data.get("public_poc_urls", []))
        if research_data.get("vendor_advisory_url"):
            sources.append(research_data["vendor_advisory_url"])
        research_meta = {
            "timestamp": run_id,
            "wall_time_seconds": round(wall, 1),
            "tokens_used": None,
            "searches_performed": 1 + bool(research_data.get("public_poc_urls")),
            "sources_consulted": list(set(sources)),
        }

        # Build record
        record = build_cve_record(cve_id, entry, nvd, vuln, research_data, research_meta)
        try:
            validate_cve_record(record)
        except ValueError as e:
            print(f"  ✗ Validation failed: {e}")
            errors.append(str(e))
            continue

        _save_cve(record)
        updated_entries.append(build_index_entry(record))
        cves_processed += 1

    # ---- 4.  Write outputs -----------------------------------------------
    print(f"\n[4/4] Writing output artifacts …")

    # Merge new entries into the existing index (replace old entries for same CVE)
    existing_cves = existing_index.get("cves", [])
    existing_by_id = {e["cve_id"]: e for e in existing_cves}
    for entry in updated_entries:
        existing_by_id[entry["cve_id"]] = entry
    merged_cves = list(existing_by_id.values())

    index_data = {
        "last_updated": run_id,
        "kev_source_date": kev_source_date,
        "total_cves_processed": len(merged_cves),
        "cves": merged_cves,
    }
    _save_index(index_data)

    total_wall = time.time() - wall_start
    run_log.update({
        "cves_processed": cves_processed,
        "cves_skipped": cves_skipped,
        "skip_reason": "no KEV date change since last research" if cves_skipped else "",
        "total_wall_time_seconds": round(total_wall, 1),
        "total_tokens_used": None,
        "avg_time_per_cve_seconds": round(total_wall / max(cves_processed, 1), 1),
        "errors": errors,
    })
    _save_run_log(run_log)

    print(f"\n╔══ Summary ══╗")
    print(f"  Processed:  {cves_processed}")
    print(f"  Skipped:    {cves_skipped}")
    print(f"  Errors:     {len(errors)}")
    print(f"  Wall time:  {total_wall:.1f}s  "
          f"({total_wall/max(cves_processed,1):.1f}s avg/CVE)")
    print(f"  Index CVEs: {len(merged_cves)}")
    return run_log


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def cli_main():
    """Console-script entry point (also ``python main.py``)."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="kevrichment",
        description="CISA KEV + Vulnrichment enrichment — agentic research pipeline",
    )
    parser.add_argument(
        "--agent", action="store_true",
        help="Enable Hermes-agent web-search tools (requires hermes_tools package)",
    )
    parser.add_argument(
        "--cve-count", type=int, default=5,
        help="Number of most-recent KEV entries to process (default: 5)",
    )
    parser.add_argument(
        "--no-incremental", action="store_true",
        help="Re-research all selected CVEs regardless of KEV date",
    )
    parser.add_argument(
        "--nvd-api-key", type=str, default=None,
        help="NVD API 2.0 key (also read from NVD_API_KEY env var). Without one, "
             "rate limit is 5 req/30s — fine for POC, unreliable for CI.",
    )
    args = parser.parse_args()

    nvd_api_key = args.nvd_api_key or os.environ.get("NVD_API_KEY")

    if args.agent:
        try:
            from hermes_tools import web_search, web_extract
            engine = ResearchEngine(web_search=web_search, web_extract=web_extract)
            print("  [agent-mode: Hermes tools loaded]\n")
        except ImportError:
            print("  [WARN] --agent specified but hermes_tools unavailable; falling back to standalone\n")
            engine = None
    else:
        engine = None

    run_pipeline(research_engine=engine, nvd_api_key=nvd_api_key)


if __name__ == "__main__":
    cli_main()
