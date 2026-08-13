# Tia N. List

Story-centric cybersecurity news + remediation site. Stories are first-class
entities with timelines (original reporting → updates from multiple sources),
hot-scored by a custom static site generator (no Hugo), with RSS feeds
(daily digest / hot stories / every article / KEV catalog) and a CTI &
detection tier (ATT&CK coverage matrix, IOC feeds + STIX snapshots, Sigma/SPL/
KQL/YARA rules).

The **KEV catalog section** (`/kev/`) is powered by the kevrichment pipeline in
`kevrichment/` — per-CVE enrichment of the CISA KEV catalog (PoC availability,
exploitation preconditions, BOD 26-04 remediation timelines, hunting
hypotheses). Story pages link their CVEs straight to the matching `/kev/cves/`
page when a record exists.

## Structure

- `engine/ssg.py` — static site generator (logic only; all markup in `engine/templates/`)
- `engine/templates/` — Jinja2 templates + design system (`style.css`, light default,
  dark toggle)
- `engine/data/events/<id>.md` + `<id>.json` — hybrid store: markdown content + JSON metadata
- `engine/data/stories/<id>.json` — story metadata + ordered event refs
- `engine/digest_candidates.py` — coverage-delta brief for the daily digest (yesterday's
  coverage ∪ evolved stories ∪ hot-uncovered), consumed by the digest automation
- `engine/kev.py` — /kev/ section generator (reads `kevrichment/data/`)
- `kevrichment/` — kevrichment pipeline (see its AGENTS.md): deterministic KEV+NVD+
  Vulnrichment enrichment, committed `data/` (index.json + per-CVE records), daily
  automation runbook. Its dashboard was ported into the Tia design system; the old
  generator (`build_site.py`) is gone.

## Regenerate

```bash
uv venv ~/.local/venvs/tia-engine && uv pip install jinja2 markdown bleach   # once
~/.local/venvs/tia-engine/bin/python engine/ssg.py          # full site
~/.local/venvs/tia-engine/bin/python engine/ssg.py --kev    # kev section only (automation verify)
```

Generated site lands at the repo root (GitHub Pages serves `/`). CI builds it
on every push; lint gates (link resolution, path-absolute, chips, CTI, Sigma,
YARA) fail the build on any violation.
