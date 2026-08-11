#!/usr/bin/env python3
"""Tia N. List — CTI & Detection tier 1: record processing + ATT&CK coverage matrix.

Deterministic layer on top of LLM-authored CTI records (engine/data/cti/<slug>.json):
validates ATT&CK ids against the framework whitelist, computes confidence, and
aggregates technique coverage for the matrix renderer.

Coverage states:
  detection  - technique has >= 1 case AND a published detection (sigma/yara) — green
  case       - technique appears in >= 1 case, no detection published yet — amber (GAP)
  none       - technique not covered by any case — gray
"""
import glob
import json
import os

ENGINE = os.path.dirname(os.path.abspath(__file__))
CTI_DIR = os.path.join(ENGINE, "data", "cti")
ATTACK_FILE = os.path.join(ENGINE, "data", "attack", "techniques.json")

TACTIC_ORDER = ["reconnaissance", "resource-development", "initial-access", "execution",
                "persistence", "privilege-escalation", "stealth", "defense-impairment",
                "credential-access", "discovery", "lateral-movement", "collection",
                "command-and-control", "exfiltration", "impact"]


def load_techniques():
    data = json.load(open(ATTACK_FILE))
    return {t["id"]: t for t in data["techniques"]}


def load_records():
    records = {}
    if os.path.isdir(CTI_DIR):
        for f in glob.glob(os.path.join(CTI_DIR, "*.json")):
            r = json.load(open(f))
            records[r.get("story_id", os.path.basename(f)[:-5])] = r
    return records


def validate_records(records):
    """Return invalid technique ids (not in the whitelist) and schema errors."""
    tech = load_techniques()
    errs = []
    for sid, r in records.items():
        for t in r.get("attack", []):
            if t.get("id") not in tech:
                errs.append(f"cti {sid}: unknown technique {t.get('id')}")
        for key in ("story_id", "title", "actors", "malware", "campaigns", "cves",
                    "victim_sectors", "geography", "attack", "references", "detections"):
            if key not in r:
                errs.append(f"cti {sid}: missing key {key}")
    return errs


def confidence(record, card):
    """Deterministic confidence: reviewed (analysis exists) > corroborated
    (>=2 sources) > reported."""
    if card and card.get("analysis_html"):
        return "reviewed"
    if card and card.get("n_sources", 0) >= 2:
        return "corroborated"
    return "reported"


def build_matrix(records, cards_by_id):
    """Tactic-ordered matrix: each technique with state + the cases covering it."""
    tech = load_techniques()
    technique_cases = {}
    for sid, r in records.items():
        for t in r.get("attack", []):
            technique_cases.setdefault(t["id"], []).append({
                "story_id": sid,
                "title": r.get("title", sid),
            })
    matrix = []
    for tactic in TACTIC_ORDER:
        cols = [t for t in tech.values() if t["tactic"] == tactic]
        if not cols:
            continue
        rows = []
        for t in cols:
            cases = technique_cases.get(t["id"], [])
            detection = any(r.get("detections", {}).get("sigma") or
                            r.get("detections", {}).get("yara")
                            for r in (records.get(c["story_id"], {}) for c in cases))
            state = "detection" if detection else ("case" if cases else "none")
            rows.append({"id": t["id"], "name": t["name"], "state": state,
                         "n_cases": len(cases), "cases": cases})
        matrix.append({"tactic": tactic,
                       "tactic_name": cols[0]["tactic_name"],
                       "n_covered": sum(1 for r in rows if r["state"] != "none"),
                       "techniques": rows})
    return matrix


def all_covered(matrix):
    """Flat list of covered techniques (id, name, tactic, cases) for the detail section."""
    order = {tac: i for i, tac in enumerate(TACTIC_ORDER)}
    out = []
    for tactic in matrix:
        for t in tactic["techniques"]:
            if t["state"] != "none":
                out.append({**t, "tactic_name": tactic["tactic_name"]})
    out.sort(key=lambda t: (order.get(t["tactic_name"].lower(), 99), t["id"]))
    return out
