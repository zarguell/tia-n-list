# kevrichment

**KEV** (Known Exploited Vulnerabilities) + **Vulnrichment** enrichment pipeline.

Agentically researches each CVE in the CISA KEV catalog, merges in SSVC
decisions from the CISA Vulnrichment project, and publishes a structured JSON
schema that downstream consumers can use to make patching-priority decisions.

## Problem

[BOD 26-04](https://www.cisa.gov/bod-26-04) requires federal agencies to
remediate KEV-listed vulnerabilities by their CISA-assigned due date.  But
the raw KEV catalog does not answer crucial triage questions:

- Is the vulnerable component enabled by default, or is a specific
  configuration required?
- Does a public PoC exist today?
- What network preconditions must be met for exploitation?
- What does the SSVC decision tree (Vulnrichment) say about this CVE?

**kevrichment** answers those questions by combining three data sources and
adding agentic web research for each CVE.

### Scope

The pipeline **processes only KEV-listed CVEs** — it does not scan every CVE
in NVD.  The KEV catalog identifies the subset of vulnerabilities known to be
actively exploited in the wild; BOD 26-04 ties remediation timelines directly
to these entries.

**Non-KEV "hidden" risk**: Some CVEs not in the KEV catalog still have
``automatable=yes`` and ``technical_impact=total`` per CISA Vulnrichment.
Under BOD 26-04, these would require **3-day remediation** if present on a
publicly exposed asset — even though CISA hasn't added them to the KEV (yet).
Use ``--scan-vulnrichment`` to identify these alongside your KEV processing.

## Schema

### Two-level design

Consumers fetch the lightweight **index.json** to filter on priority dimensions,
then selectively fetch individual CVE records.

```
data/
├── index.json              ←  lightweight manifest (all CVEs)
├── cves/
│   ├── CVE-2024-1709.json  ←  detailed per-CVE record
│   └── …
└── runs/
    └── TIMESTAMP.json      ←  per-run statistics
latest.json                 ←  copy of the most recent run log
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

Consumers filter by `automatable`, `technical_impact`, `exploitation_status`,
or `public_poc_exists`, then fetch only the CVE files matching their criteria.

### Per-CVE record (`data/cves/CVE-YYYY-XXXX.json`)

The full record includes all KEV fields, NVD data (description, CWE, CVSS,
CPE), Vulnrichment SSVC decisions, BOD 26-04 remediation timeline, and the
``kevrichment_research`` enrichment block.

#### ``bod_26_04`` fields

Computed from the SSVC ``automatable`` and ``technical_impact`` values:

| Field | Values | Interpretation |
|-------|--------|----------------|
| `timeline_if_publicly_exposed` | `3_days_forensic_triage` / `14_days` / `60_days` / `defer_to_next_upgrade` | Remediation deadline if the vulnerable asset is accessible from the internet |
| `timeline_if_not_publicly_exposed` | same values | Remediation deadline for internal-only assets |
| `three_day_qualifying` | `true` / `false` | ``true`` when ALL four BOD 26-04 risk factors are present |
| `requires_forensic_analysis_if_public` | `true` / `false` | Whether forensic triage is mandated when asset is publicly exposed (only 3-day bucket) |
| `requires_forensic_analysis_if_not_public` | `true` / `false` | Same for non-public assets |

#### ``kevrichment_research`` fields

| Field | Values | Interpretation |
|-------|--------|----------------|
| `vulnerable_component` | string | The specific component or feature affected (not just the product name) |
| `vulnerable_component_enabled_by_default` | `yes` / `no` / `unknown` | Whether the vulnerable component ships enabled in a default installation |
| `preconditions_for_exploit` | string | Structured summary: network access requirements, auth requirements, CVSS-derived conditions |
| `public_poc_exists` | `yes` / `no` / `unknown` | Whether public exploit code or a PoC repo was found |
| `public_poc_urls` | string[] | URLs to identified PoC repositories |
| `vendor_advisory_url` | string | Link to vendor security advisory or patch notes |
| `exploit_complexity_notes` | string | Free-text notes on exploitation difficulty & CVSS attack complexity |
| `kevrichment_summary` | string | One-line summary combining all findings |
| `hunting_hypothesis` | string | Natural-language hypothesis describing what defenders should monitor for, derived from preconditions, PoC availability, and exploit complexity |

## Static file API (GitHub Pages)

The entire ``data/`` directory is designed to be served as a static file API
from GitHub Pages — no server-side logic required.

### Setup

1. Push the `kevrichment` repository to GitHub.
2. Go to **Settings &gt; Pages** and set the source to deploy from the
   repository root (or from `docs/`).
3. Ensure `data/index.json` is committed.

Consumers then access:

```
https://<org>.github.io/kevrichment/data/index.json
https://<org>.github.io/kevrichment/data/cves/CVE-2024-1709.json
https://<org>.github.io/kevrichment/latest.json
```

Because the schema is purely JSON, consumers can use any HTTP client — no
authentication or SDK required.

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
python main.py                                   # standalone (requests-based research)
python main.py --scan-vulnrichment               # also finds non-KEV 3-day CVEs
python main.py --agent                           # agent mode (web_search + web_extract)
python main.py --agent --scan-vulnrichment --cve-count 10 --nvd-api-key XXXXX
```

**Standalone mode** uses the GitHub API (public, rate-limited) and direct URL
construction for research.  **Agent mode** uses Hermes ``web_search`` /
``web_extract`` tools for richer multi-source research.

**Vulnrichment scan** (``--scan-vulnrichment``) samples recent vulnrichment
additions to find non-KEV CVEs with ``automatable=yes`` + ``technical_impact=total``.
These are the "hidden" 3-day CVEs — they'd require immediate remediation if
deployed on a publicly exposed asset, even though CISA hasn't added them to
the KEV (yet).

### Daily cron

Schedule a daily run to keep pace with the KEV update cadence (CISA typically
updates weekdays):

```cron
0 6 * * * cd /opt/kevrichment && .venv/bin/python main.py 2>&1 | logger -t kevrichment
```

The run log is written to `data/runs/TIMESTAMP.json` and `latest.json`.

## Known limitations

- **POC scope**: Processes only the 5 most recent KEV entries per run.  This
  is intentional for measuring token usage and wall-clock time before scaling.
- **Research accuracy**: Web-search results and precondition synthesis are
  generated by an LLM-driven research agent or by static heuristic fallbacks.
  They are **not a substitute** for manual analyst review.
- **SIGMA queries**: The ``hunting_hypothesis`` field is natural-language only.
  Structured SIGMA rule generation is a planned future enhancement.
- **SSVC coverage**: Only ~45% of CVEs have SSVC data from CISA Vulnrichment.
  KEV entries are more likely to have SSVC, but ``"unknown"`` values are still
  possible.  The ``bod_26_04`` timeline computation treats unknown SSVC as
  ``"60_days"`` / ``"defer_to_next_upgrade"`` (conservative).
- **GitHub API rate limits**: Standalone mode is subject to unauthenticated
  GitHub API rate limits (60 requests/hour).
- **NVD API**: May return empty results for very recent CVEs before NVD
  enrichment completes.

## License

MIT
