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
CPE), Vulnrichment SSVC decisions, and the ``kevrichment_research`` enrichment
block.

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

# 3. Run (standalone mode — no Hermes agent required)
python main.py

# 4. Run (agent mode — requires Hermes agent context)
python main.py --agent
```

**Standalone mode** uses the GitHub API (public, rate-limited) and direct URL
construction for research.  **Agent mode** uses Hermes ``web_search`` /
``web_extract`` tools for richer multi-source research.

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
- **SSVC coverage**: Not every KEV CVE has a corresponding Vulnrichment
  entry.  Missing values default to ``"unknown"``.
- **GitHub API rate limits**: Standalone mode is subject to unauthenticated
  GitHub API rate limits (60 requests/hour).
- **NVD API**: May return empty results for very recent CVEs before NVD
  enrichment completes.

## License

MIT
