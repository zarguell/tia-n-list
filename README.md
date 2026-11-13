# Tia N. List

Story-centric cybersecurity news and remediation tracker. Stories are
first-class entities with timelines (original reporting → updates from multiple
outlets), hot-scored by a custom static site generator (no Hugo), and published
with RSS feeds, a CTI/detection tier, an enriched KEV catalog and a
vendor-patch tracker.

Everything is static: the hourly jobs commit data, CI renders the site from that
data on every push, and GitHub Pages serves it.

## What's on the site

| Path | What it is |
|---|---|
| `/` `/stories/` | Hot ranking, then the full archive — every story with its timeline |
| `/daily/` | Daily briefs: landscape analysis plus the stories that moved |
| `/kev/` | CISA KEV catalog, enriched per CVE (PoC, exploitation preconditions, SSVC, BOD 26-04 timelines, hunting hypotheses) |
| `/kev/deadlines/` | Remediation deadline board — every KEV entry counting down to CISA's due date, bucketed past-due / ≤2d / ≤7d / ≤30d |
| `/kev/candidates/` | Exploited CVEs CISA has not listed yet |
| `/cti/` | ATT&CK coverage matrix, per-case detections (Sigma/SPL/KQL/YARA), IOC sets and immutable daily STIX snapshots |
| `/megapatch/` | Vendor patch trackers (Microsoft, Adobe, Oracle, Cisco, Red Hat, SUSE, Siemens): per-release CVE tables with filtering, vendor-advisory links and an all-fields CSV export |
| `/feeds/sources/` | Every publication feed we poll, with 30-day activity — and the list itself as a downloadable OPML |
| `/methodology/` `/about/` | How the process works, and why it exists |

## Structure

- `engine/ssg.py` — site generator (logic only; all markup in `engine/templates/`)
- `engine/templates/` — Jinja2 templates + design system (`style.css`, light default, dark toggle)
- `engine/kev.py` — `/kev/` section: dashboard, deadline board, per-CVE pages, candidates, pipeline/schema pages
- `engine/megapatch.py` — `/megapatch/` section: release pages, tracker indexes, per-release JSON
- `engine/cti.py`, `engine/ioc.py`, `engine/sigma.py` — ATT&CK matrix, IOC extraction, detection-variant derivation
- `engine/ingest.py` — hourly RSS polling of `engine/feeds/cyber.opml` (48 sources) + Reddit/X/Mastodon legs
- `engine/merge.py`, `engine/triage.py`, `engine/score.py` — clustering, editorial decisions, hot scoring
- `engine/store.py` — the one loader for the event store (content is markdown, metadata is JSON)
- `engine/stage_pages.py` — stages only the published surface for the Pages artifact and fails the build on a dangling reference
- `engine/feeds/cyber.opml` — the source list the ingest pass polls, published at `/feeds/sources/`

Data lives beside the code:

- `engine/data/events/<id>.json` + `<id>.md` — the article store (markdown body, JSON metadata)
- `engine/data/stories/<id>.json` — story metadata and ordered event refs
- `engine/data/{analysis,digests,cti,audit}…` — analyst prose, daily briefs, CTI records, audit reports
- `kevrichment/data/cves/CVE-*.json` — per-CVE enrichment; `index.json` feeds the dashboard;
  `epss-history.json` is the compact 21-day EPSS series the CVE pages chart
- `engine/data/megapatch/<track>/<release>.json` — normalized vendor releases

Settled reference conditions (owner decisions that later audits should not
re-raise as rot) live in `known-ref-states.md`.

## Regenerate

```bash
uv venv ~/.local/venvs/tia-engine && uv pip install jinja2 "markdown==3.10.3" bleach
~/.local/venvs/tia-engine/bin/python engine/ssg.py            # full site
~/.local/venvs/tia-engine/bin/python engine/ssg.py --kev      # /kev/ only (automation pre-push verify)
~/.local/venvs/tia-engine/bin/python engine/ssg.py --megapatch  # /megapatch/ only
~/.local/venvs/tia-engine/bin/python engine/ssg.py --lint-only  # source-level lints, no render
```

A full build also derives the Sigma/Splunk/KQL variants, which needs the pinned
detection stack (`sigma-cli`, `pysigma`, `pyparsing`, the Splunk/Kusto backends,
`yara-x` — exact pins in `.github/workflows/site-deploy.yml`). Without it the
build skips derivation and only re-renders committed variants.

Generated site lands at the repo root (GitHub Pages serves `/`; all generated
paths are gitignored). CI builds on every push and fails on any lint violation:
link resolution, path-absolute URLs, chip contents, CTI joins, Sigma parity,
YARA, prose.

## Pipeline

The jobs that feed this repo live in the `cronman` repo (see its README and
`AGENTS.md`): hourly ingest → merge → triage → analysis → publish, a KEV
catalog watch, daily KEV enrichment and EPSS refresh, a five-minute megapatch
watcher during vendor disclosure windows, the morning digest, plus audit and
autodiag passes. Every job commits data here; CI does the rendering.

## Tests

```bash
.venv/bin/python -m pytest kevrichment/tests       # pipeline + site unit tests
for f in engine/test_*.py; do python3 "$f" || break; done   # engine contract suites
NODE_PATH=… node engine/tests/verify-kev.js        # jsdom suites (CI runs these)
```
