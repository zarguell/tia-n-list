# CTI Record Authoring Contract (Tia N. List daily pass)

Work ONLY inside `/home/coder/workspace/tia-n-list`. All paths below are relative to that directory.
You are authoring CTI records for a curated threat-intel story store. Precision over recall: an honest empty array is better than a guessed value. NEVER invent facts, technique ids, IOCs, or detection logic that the source material does not support.

## Per-case inputs (read ALL of them before writing)
- `engine/data/stories/<id>.json` — story metadata (title, cves, sources, events list)
- `engine/data/events/<event_id>.md` — full article text for each event in the story
- `engine/data/events/<event_id>.json` — metadata incl. the source `url` (use for references)
- `engine/data/analysis/<id>.md` — distilled analyst analysis (best starting point)

## Output 1 — `engine/data/cti/<id>.json` (REQUIRED for every case)
EXACT schema (keys in this order):
```json
{"story_id": "<id>", "title": "<story title from story json>",
 "actors": [...], "malware": [...], "campaigns": [...], "cves": [from the story json's cves],
 "victim_sectors": [...], "geography": [...],
 "attack": [{"id": "T1059", "tactic": "execution", "name": "Command and Scripting Interpreter"}],
 "references": [<unique source URLs from the event .json files>], "updated_at": "<now ISO UTC, e.g. 2026-08-14T12:00:00Z>",
 "detections": {"sigma": false, "yara": false}}
```
Rules:
- ATT&CK techniques MUST come from `engine/data/attack/techniques.json` (field `techniques`, entries have `id`, `tactic`, `name`). Copy id + tactic + name VERBATIM. 1–6 techniques the story actually describes; `[]` if none. NEVER invent a technique id.
- `actors`/`malware`/`campaigns`/`victim_sectors`/`geography`: only what the story supports; empty arrays where nothing applies.
- `references`: dedupe the event .json `url` fields.
- `updated_at`: today's UTC ISO timestamp (2026-08-14).
- `detections`: set true only after you actually author + validate the corresponding rule (below).
- For policy/legal stories with no attacker behavior (e.g. government memos), `attack: []` and empty malware/actors arrays are HONEST and correct.

## Output 2 (OPTIONAL) — `engine/data/cti/<id>.sigma`
Author ONLY if the story has concrete telemetry-level detail: a specific process name/path, command line, network destination (IP/domain/port), auth event, or file artifact the attacker produced. If the story only names a vulnerability or a family without observable behavior, DO NOT force a rule.
- Valid Sigma YAML: `title`, `id` (fresh uuid4), `status: experimental`, `description`, `references` (the source URLs), `author: Tia N. List`, `date: 2026/08/14`, `tags` (`attack.t####` lowercase — ONLY techniques present in this record's `attack` array, or their T####.001 children), `logsource` (one of: `category: process_creation, product: windows` | `category: network_connection, product: windows` | `category: authentication` | `category: file_event, product: windows` — match the actual behavior), `detection` (named `selection_*` fields + `condition`), `falsepositives` (honest and specific), `level: high` or `medium`.
- After writing, run `sigma check engine/data/cti/<id>.sigma`. It MUST report 0 errors and 0 condition errors. Fix until clean. NOTE: sigma-cli's bundled ATT&CK data is older than the project whitelist — if it flags a tag that EXISTS in `engine/data/attack/techniques.json`, the project whitelist wins and the issue is advisory; do NOT drop the tag.
- Do NOT write `.splunk` or `.kql` files — the build derives them from the `.sigma` deterministically.
- Set `"detections": {"sigma": true, "yara": false}` on the record.

## Output 3 (OPTIONAL, highest bar) — `engine/data/cti/<id>.yara`
Author ONLY if the case has hardcoded strings / hashes / distinctive binary artifacts with real technical detail (e.g. a C2 domain string, a registry key, a persistence name baked into a known binary). Most cases will NOT get a YARA rule. If the detail is not real, skip it.
- YARA-X syntax, following the existing house style (see `engine/data/cti/captivecrunch-midnight-blizzard-sub-cluster-weaponizes-hotel-wi.yara`): `rule <Name> { meta: author = "Tia N. List", date = "2026-08-14", status = "experimental", description = "...", reference = "...", falsepositives = "..."  strings: $x = "..." ascii [nocase]  condition: ... }`
- Every string in `strings:` MUST be used in `condition` (YARA-X rejects unused patterns).
- Compile-validate:
  `/home/coder/.local/venvs/tia-engine/bin/python -c "import sys; sys.path.insert(0,'engine'); import yara; print(yara.validate_yara('engine/data/cti/<id>.yara'))"`
  MUST print `[]`. Fix until clean.
- Set `"detections": {"sigma": <true if you wrote a sigma>, "yara": true}`.

## Hard constraints
- Do NOT touch anything outside `engine/data/cti/` (no edits to stories/, events/, analysis/, iocs-*.json, cti-queue.json, engine/*.py).
- Do NOT re-author a case that already has a `.json`/`.sigma`/`.yara` in `engine/data/cti/` — check first (none of your assigned cases should exist; if one does, SKIP it and say so).
- Skip formatters, linters, and project-wide test suites. Per-file `sigma check` / yara validation only.
- Report per case: which files you wrote, sigma/yara status, and the techniques you chose.
