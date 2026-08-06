# AGENTS.md — kevrichment daily run

Operational runbook for the kevrichment pipeline: enrich CISA KEV entries with
web research, publish structured JSON, deploy the static dashboard.

This file is the authoritative procedure for the daily run. It lives in a
**public repository** — do not add personal data, credentials, or internal
infrastructure details to any file here.

## What this repo is

- **Data**: `data/cves/CVE-*.json` (per-CVE enriched records), `data/index.json`
  (lightweight filter manifest), `data/runs/*.json` (per-run stats), `latest.json`
  (last run, gitignored).
- **Schema**: see `README.md` for the full field reference. Key research fields
  live in `kevrichment_research`; provenance in `research_meta`.
- **Site**: `build_site.py` generates `site/` (gitignored; GitHub Actions builds
  and deploys it to Pages on push to `master`). The site reads **only from
  `data/index.json`** — never from individual CVE files.

## Daily run — four phases

Run from the repo root. Deliver a summary report at the end (counts, research
done, errors, whether the site will update).

### Phase 1 — Deterministic pipeline

```bash
python main.py --cve-count 2000 --qc 2>&1
```

- Fetches KEV + NVD + Vulnrichment, processes the newest KEV entries, runs QC.
- **Newly processed CVEs** (not `SKIP`) are the ones listed in the `Processing`
  section and counted in `Processed: N`. These are your research targets.
- Usually 0–2 CVEs/day; most entries skip because their KEV date is unchanged.

### Phase 2 — Agent research on newly processed CVEs

For **each newly processed CVE** (usually a handful), read
`data/cves/<CVE_ID>.json` and enrich the `kevrichment_research` block with
live web research. Use `web_search`; fall back to `web_extract`, `read` on
direct URLs, or the GitHub API when search is flaky.

For each CVE:

1. **Vendor advisory** — search `"<vendor> <CVE_ID> advisory patch"`. Real
   advisory URL (NOT nvd.nist.gov) → `research.vendor_advisory_url`.
2. **PoC search** — search `"<CVE_ID> exploit poc github"`. Functional
   public PoC repo (github.com, exploit-db.com) → `public_poc_exists = "yes"`
   + URLs in `public_poc_urls`. Only set `"yes"` when a reproducible public
   artifact is confirmed — not for blog descriptions of exploitation.
3. **Component info** — `"<vendor> <product> <component> vulnerability"` for
   additional sources (security blogs, vendor KBs).
4. **Default enablement** — if `vulnerable_component_enabled_by_default` is
   `"unknown"` and the component is ≥3 chars, search
   `'"<component>" "enabled by default"'`.
5. **Sources** — merge all new URLs into `research_meta.sources_consulted`
   (deduplicated; target ≥4 sources). Set `research.preconditions_source`
   and `research.hunting_hypothesis_source` to `"hermes"`.
6. Save the full record back to `data/cves/<CVE_ID>.json` (write the whole
   file with `json.dumps(record, indent=2)` — never chain field-level patches;
   they corrupt JSON).

### Phase 3 — Rebuild index, build site, commit, push

1. **Rebuild `data/index.json`** — required whenever CVE files changed. The
   site generator only sees the index:

```bash
python3 -c "
import json, sys
from pathlib import Path
sys.path.insert(0, '.')
from schema import build_index_entry
cves = [json.load(open(p)) for p in sorted(Path('data/cves').glob('CVE-*.json'))]
entries, skipped = [], []
for rec in cves:
    try:
        entries.append(build_index_entry(rec))
    except KeyError as e:
        skipped.append(f'{rec.get(\"cve_id\",\"?\")}: {e}')
entries.sort(key=lambda e: e.get('kev_date_added','') or '', reverse=True)
json.dump({'last_updated': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'kev_source_date': json.load(open('data/index.json')).get('kev_source_date',''),
           'total_cves_processed': len(entries), 'cves': entries},
          open('data/index.json','w'), indent=2)
print(f'Index: {len(entries)} entries' + (f'; skipped: {skipped}' if skipped else ''))
"
```

2. **Stage precisely** — check `git status` first. Stage **only your batch
   files by explicit path**, plus the rebuilt index and run log:

```bash
git status                      # look for orphaned pre-existing modifications
git add data/cves/CVE-XXXX-XXXX.json data/cves/CVE-YYYY-YYYY.json data/index.json
git diff --cached --stat        # file count should match your batch + index + run log
```

   Never `git add data/` wholesale — it sweeps in unrelated QC-scanner changes
   and orphaned files from a previous failed commit. If pre-existing
   modifications exist, either include them (flag in the commit message) or
   `git stash push -- <paths>` them aside.

3. **Verify record quality before commit** — for every batch CVE:

   - JSON valid: `python3 -m json.tool data/cves/<CVE_ID>.json > /dev/null`
   - `hunting_hypothesis`: 130–200 chars, single sentence, starts with
     `Monitor for` / `Hunt for` / `Look for`, **never contains `designed to`**
     (always boilerplate), no CVSS/PoC/precondition rehash, names the specific
     component + attack vector + technique.
   - `vulnerable_component`: specific function/module/endpoint, NOT just the
     product name.
   - `vendor_advisory_url`: vendor advisory, not the NVD page.
   - `preconditions_for_exploit`: ≥80 chars, includes version range / auth /
     network requirements; cross-check UI/PR against the CVSS vector.
   - `kevrichment_summary`: 2–4 sentences (type, component, impact, status).
   - `last_researched` (top-level) == `research_meta.timestamp`.
   - `cwe` deduplicated; `research_meta.sources_consulted` ≥ 4; both
     `*_source` fields == `"hermes"`.
   - Stale `qc_notes` cleared when enrichment resolved the flagged issue
     (checks `component_extraction`, `advisory_fallback`,
     `precondition_contradiction` are stale once fields are fixed).
   - `public_poc_exists` consistent with `public_poc_urls`.

   Clean up any temp helper scripts (`verify_*.py`, `update_*.py`, `_*.py`)
   from the repo root and `data/cves/` — never commit them.

4. **Commit and push**:

```bash
git commit -m "daily update $(date -u +%Y-%m-%d)"
git push origin master
```

### Phase 4 — Report

Summary: CVEs processed, which got agent research, new advisories/PoCs found,
any errors, whether the site will update (push → GH Actions deploy).

## Tool failure fallbacks (condensed)

- **`web_search` returns empty results** → search again with different terms;
  go direct with `web_extract`/`read` on known URLs (NVD, vendor pages, GitHub).
- **NVD blocked (Cloudflare/503)** → use `web_search` snippets for the
  description; SentinelOne vuln database, OpenCVE, or the GitHub Advisory
  Database as mirrors.
- **`web_extract` credit-exhausted (HTTP 402)** → `read` the URL directly or
  use the GitHub search API: `https://api.github.com/search/repositories?q=<CVE_ID>`.
- **GitHub PoC discovery** → star count and file types (`.py`/`.cpp`/`.go`)
  distinguish functional exploits from docs; forks suggest reliability.
- **Vendor page JS-heavy/blocked** (Fortiguard WAF, Packet Storm TOS) →
  use NVD's references table for the advisory URL; skip Packet Storm.

## Known pitfalls (learned)

- **`build_site.py` reads only `data/index.json`** — skipping the index
  rebuild in Phase 3 silently ships a stale site with a green Actions run.
- **Whole-directory `git add data/`** sweeps in QC-scanner noise and orphaned
  enrichments from failed prior commits. Stage explicit paths.
- **Field-level `patch()` on JSON** strips commas and corrupts files — always
  rewrite the whole record.
- **`vendor`/`product` root fields** are often left empty by research —
  populate them from the KEV catalog data during verification.
- **Non-KEV entries** (from `--scan-vulnrichment`) have
  `kev_vulnerability_name: "Non-KEV (vulnrichment scan)"` and empty
  `kev_date_added` — they are valid data but not KEV catalog entries; don't
  confuse them when reporting counts.
- **Hypotheses starting `Monitor for crafted` / `Monitor for local attempts`**
  trigger template detectors; prefer `Hunt for` / `Look for` openings with the
  same specific content.
