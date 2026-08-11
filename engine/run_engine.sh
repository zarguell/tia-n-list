#!/bin/bash
# Tia Storyline — deterministic hourly pass (the LLM analysis pass runs after,
# consuming data/needs-analysis.json, then re-runs ssg + pushes).
set -euo pipefail
cd "$(dirname "$0")"
PY=~/.local/venvs/tia-engine/bin/python
$PY ingest.py "$@"
$PY merge.py
$PY ssg.py
