# kevrichment

**KEV** (Known Exploited Vulnerabilities) + **Vulnrichment** enrichment pipeline.

Researches each CVE in the CISA KEV catalog, merges in SSVC decisions from the CISA Vulnrichment project, and publishes a structured JSON schema that downstream consumers can use to make patching-priority decisions under [BOD 26-04](https://www.cisa.gov/bod-26-04).

## Problem

BOD 26-04 requires federal agencies to remediate KEV-listed vulnerabilities by their CISA-assigned due date. But the raw KEV catalog does not answer crucial triage questions:

- Is the vulnerable component enabled by default, or does it require specific configuration?
- Does a public PoC exist today?
- What network preconditions must be met for exploitation?
- What does the SSVC decision tree (Vulnrichment) say about this CVE?

**kevrichment** answers those questions by combining three data sources (KEV, NVD, Vulnrichment) with agentic web research for each CVE.

### Scope

The pipeline **processes only KEV-listed CVEs** — it does not scan every CVE in NVD. The KEV catalog identifies vulnerabilities known to be actively exploited in the wild; BOD 26-04 ties remediation timelines directly to these entries.

**Non-KEV "hidden" risk**: Some CVEs not in the KEV catalog still have ``automatable=yes`` and ``technical_impact=total`` per CISA Vulnrichment. Under BOD 26-04, these would require **3-day remediation** if present on a publicly exposed asset — even though CISA hasn't added them to the KEV (yet). Use ``--scan-vulnrichment`` to identify these alongside your KEV processing.

## Schema

### Two-level design

Consumers fetch the lightweight **index.json** to filter on priority dimensions, then selectively fetch individual CVE records.

```
data/
├── index.json              ←  lightweight manifest (all CVEs)
├── cves/
│   ├── CVE-2024-1709.json  ←  detailed per-CVE record
│   └── …
└── runs/
    └── TIMESTAMP.json      ←  per-run statistics
```

### index.json

| Field | Type | Description |
|-------|------|-------------|
| `last_updated` | ISO8601 | When this index was last written |
| `kev_source_date` | date | CISA KEV catalog version date |
| `total_cves_processed` | int | Total distinct CVEs in the index |
| `cves[]` | array | Lightweight entries (see below) |

Each entry in `cves[]`:

```json
{
  "cve_id": "CVE-2024-1709",
  "kev_date_added": "2024-02-22",
  "vendor_project": "ConnectWise",
  "product": "ScreenConnect",
  "automatable": "yes",
  "technical_impact": "total",
  "exploitation_status": "active",
  "public_poc_exists": "yes",
  "last_researched": "2026-06-11T08:00:00Z",
  "file": "data/cves/CVE-2024-1709.json"
}
```

Consumers filter by `automatable`, `technical_impact`, `exploitation_status`, or `public_poc_exists`, then fetch only the CVE files matching their criteria.

### Per-CVE record (`data/cves/CVE-YYYY-XXXX.json`)

The full record includes KEV fields, NVD data (description, CWE, CVSS, CPE), Vulnrichment SSVC decisions, BOD 26-04 remediation timeline, and the ``kevrichment_research`` enrichment block.

#### ``bod_26_04`` fields

| Field | Values | Meaning |
|-------|--------|---------|
| `timeline_if_publicly_exposed` | `3_days_forensic_triage` / `14_days` / `60_days` / `defer_to_next_upgrade` | Remediation deadline for internet-facing assets |
| `timeline_if_not_publicly_exposed` | same values | Remediation deadline for internal-only assets |
| `three_day_qualifying` | `true` / `false` | All four BOD 26-04 risk factors present |
| `requires_forensic_analysis_if_public` | `true` / `false` | Forensic triage mandated when public |
| `requires_forensic_analysis_if_not_public` | `true` / `false` | Same for non-public assets |

#### ``kevrichment_research`` fields

| Field | Values | Description |
|-------|--------|-------------|
| `vulnerable_component` | string | The specific component or feature affected (not just the product name) |
| `vulnerable_component_enabled_by_default` | `yes` / `no` / `unknown` | Whether the vulnerable component ships enabled in a default installation |
| `delivery_mechanism` | string or null | How an attacker delivers the exploit — extracted from the NVD description (e.g. "crafted HTML page", "POST /api/endpoint requests") |
| `preconditions_for_exploit` | string | What must be true in your deployment for this CVE to be exploitable (product-class-aware, optionally AI-analyzed) |
| `preconditions_source` | `"hermes"` or absent | Set to `"hermes"` when AI-generated; absent when using the deterministic fallback |
| `public_poc_exists` | `yes` / `no` / `unknown` | Whether public exploit code or a PoC repo was found |
| `public_poc_urls` | string[] | URLs to identified PoC repositories |
| `vendor_advisory_url` | string | Link to vendor security advisory or patch notes |
| `exploit_complexity_notes` | string | Notes on exploitation difficulty, PoC availability, CVSS attack complexity |
| `kevrichment_summary` | string | One-line summary combining all findings |
| `hunting_hypothesis` | string | Specific attacker behavior or TTP to monitor for (AI-generated via Hermes agent, or deterministic fallback) |
| `hunting_hypothesis_source` | `"hermes"` or absent | Set to `"hermes"` when AI-generated; absent when deterministic |

### Output sourcing

The `preconditions_for_exploit` and `hunting_hypothesis` fields have two production paths:

- **Hermes analysis** (recommended): The Hermes agent reads each CVE's collected data (NVD, CWE, CVSS, Vulnrichment, PoC findings, component extraction) and generates genuine analyst-quality output. The `*_source` field is set to `"hermes"`.
- **Deterministic fallback**: When the agent hasn't analyzed a CVE yet, the pipeline uses product-class-aware heuristics (CWE → vulnerability class mapping, CVSS → attack surface, prepositional delivery pattern extraction). The `*_source` field is absent.

Downstream consumers can use the `*_source` fields to distinguish analyst-reviewed content from best-effort heuristics.

## Running locally

```bash
# 1. Clone
git clone https://github.com/zarguell/kevrichment.git
cd kevrichment

# 2. Install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Run
python main.py                                                     # deterministic pipeline (default: 5 most recent KEV entries)
python main.py --cve-count 2000                                    # process all KEV entries
python main.py --no-incremental                                    # re-research all selected CVEs
python main.py --scan-vulnrichment                                 # also find non-KEV 3-day CVEs
python main.py --qc                                                # run quality control checks
python main.py --qc-only                                           # QC on existing data only (no research)
python main.py --agent                                             # Hermes-agent web search mode
python main.py --cve-count 2000 --scan-vulnrichment --qc --agent   # full pipeline
```

## Daily automation

A Hermes cron job runs the deterministic pipeline daily at **07:00 UTC**:

1. Fetch fresh KEV + NVD + Vulnrichment data
2. Run QC checks
3. Git commit and push any data changes
4. Report new CVEs needing AI analysis (those without `source: "hermes"`)

To trigger AI analysis on new CVEs, tell the Hermes agent: *"analyze new CVEs"*.

## Static file API (GitHub Pages)

The entire ``data/`` directory can be served as a static file API — no server-side logic required.

1. Push the repo to GitHub
2. Go to **Settings > Pages** and deploy from the repository root (`/`) on the default branch
3. Consumers access:

```
https://<org>.github.io/kevrichment/data/index.json
https://<org>.github.io/kevrichment/data/cves/CVE-2024-1709.json
https://<org>.github.io/kevrichment/latest.json
```

## Known limitations

- **Research accuracy**: Web-search results, precondition synthesis, and hunting hypotheses are generated by an LLM-driven agent or by deterministic heuristics. They are **not a substitute** for manual analyst review.
- **SSVC coverage**: Only ~45% of CVEs have SSVC data from CISA Vulnrichment. KEV entries are more likely to have SSVC, but ``"unknown"`` values are still possible. The ``bod_26_04`` timeline computation treats unknown SSVC conservatively (``"60_days"`` / ``"defer_to_next_upgrade"``).
- **GitHub API rate limits**: PoC searches use the public GitHub API (60 req/hour unauthenticated). Large backfills will hit this limit — re-run or use a token.
- **NVD API**: Requires an API key for sustained runs (>5 req/30s). Set the `NVD_API_KEY` environment variable.
- **SIGMA queries**: The ``hunting_hypothesis`` field is natural-language only. Structured SIGMA rule generation is a planned future enhancement.
- **Component extraction**: The heuristic component extractor may return the product name when the description doesn't specify a sub-component clearly.

## License

MIT
