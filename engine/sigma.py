#!/usr/bin/env python3
"""Tia N. List — Sigma detection content (tier 3).

Validation for authored Sigma YAML rules and their Splunk/KQL variants.
Sigma rules are derived from our case analysis — the review taxonomy is
honest about that: every rule carries a status (experimental/draft/reviewed)
and we do NOT claim validation against live telemetry.

Files per case (engine/data/cti/):
  <slug>.sigma   generic Sigma YAML  (the authored source of truth)
  <slug>.splunk  Splunk SPL variant  (DERIVED at build via sigma convert)
  <slug>.kql     KQL variant         (DERIVED at build via sigma convert)

Variants are never hand-written: sigma-cli (SigmaHQ) converts the generic
rule deterministically, so the SPL/KQL can never drift from the Sigma.
"""
import os
import re
import shutil
import subprocess
import uuid

REQUIRED_KEYS = {"title", "id", "status", "description", "logsource", "detection",
                 "level", "date"}


def _sigma_exe():
    return shutil.which("sigma")


def run_cli(args):
    """Run the sigma CLI; returns subprocess result or None if unavailable."""
    exe = _sigma_exe()
    if not exe:
        return None
    return subprocess.run([exe, *args], capture_output=True, text=True)


def check_with_cli(path):
    """Spec-grade validation via `sigma check`. Returns (errors, None) or
    (None, 'missing') when the CLI isn't installed (caller falls back)."""
    r = run_cli(["check", path])
    if r is None:
        return None, "missing"
    errs = []
    if r.returncode != 0:
        errs.append((r.stdout or "") + (r.stderr or ""))
    return errs, None


def convert_variants(sigma_path):
    """Derive (splunk, kql) from a Sigma rule via sigma convert.
    Returns (None, None) when the CLI isn't installed; a member is None when
    its conversion failed (rule not expressible for that backend)."""
    splunk = run_cli(["convert", "-t", "splunk", "-p", "splunk_windows", sigma_path])
    kql = run_cli(["convert", "-t", "kusto", sigma_path])
    if splunk is None or kql is None:
        return None, None
    return ((splunk.stdout or "").strip() if splunk.returncode == 0 else None,
            (kql.stdout or "").strip() if kql.returncode == 0 else None)


def validate_sigma(path):
    """Return a list of errors for a Sigma YAML file (empty = valid shape)."""
    errs = []
    try:
        import yaml
    except ImportError:
        return ["PyYAML not installed"]
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"invalid YAML: {e}"]
    if not isinstance(data, dict):
        return ["top level is not a mapping"]
    for k in REQUIRED_KEYS:
        if k not in data:
            errs.append(f"missing required key: {k}")
    if "id" in data:
        try:
            uuid.UUID(data["id"])
        except (ValueError, AttributeError):
            errs.append(f"id is not a valid UUID: {data['id']!r}")
    tags = data.get("tags", [])
    for t in tags:
        if isinstance(t, str) and t.startswith("attack.") and not re.match(r"attack\.t\d{4}(\.\d{3})?$", t):
            errs.append(f"malformed attack tag: {t}")
    if "detection" in data:
        d = data["detection"]
        if not isinstance(d, dict) or "condition" not in d:
            errs.append("detection block missing 'condition'")
    return errs


def validate_variant(path, kind):
    """Light check on Splunk/KQL variants: non-empty, no forbidden chars."""
    if not os.path.exists(path):
        return [f"{kind} variant missing"]
    with open(path) as f:
        body = f.read().strip()
    errs = []
    if not body:
        errs.append(f"{kind} variant is empty")
    if "\x00" in body:
        errs.append(f"{kind} variant contains NUL bytes")
    return errs
