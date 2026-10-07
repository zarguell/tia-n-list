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
import hashlib
import os
import re
import shutil
import subprocess
import sys
import uuid

REQUIRED_KEYS = {"title", "id", "status", "description", "logsource", "detection",
                 "level", "date"}

def _sigma_exe():
    exe = shutil.which("sigma")
    if exe:
        return exe
    # PATH-independent fallback: when ssg runs under the tia venv, sigma ships
    # in the same bin/ as the interpreter (VPS has no /usr/local/bin/sigma).
    candidate = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "sigma")
    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
        return candidate
    return None


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


CACHE_VERSION = 1
RECEIPT_NAME = ".sigma-validate-receipt.json"


def source_sha256(path):
    """Content hash of a rule file (cache key that survives clean clones —
    mtimes are useless: Actions checks out every file at the same time)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def variant_header(slug, kind, digest):
    """Header stamped on derived variants so a build can verify freshness
    without invoking the CLI (kind: "Splunk SPL" or "KQL")."""
    return (f"# {slug} — {kind} variant (derived from {slug}.sigma "
            f"via sigma convert)\n# source-sha256: {digest} "
            f"v{CACHE_VERSION}\n")


def variant_fresh_text(text, digest):
    """True when variant text carries the current source hash + version."""
    for line in (text or "").splitlines()[:4]:
        m = re.match(r"# source-sha256: ([0-9a-f]{64}) v(\d+)",
                       line.strip())
        if m:
            return m.group(1) == digest and int(m.group(2)) == CACHE_VERSION
    return False


def cli_version():
    """sigma-cli version string, or "missing"/"unknown" (part of the
    validation receipt key: a pin change must invalidate it)."""
    r = run_cli(["--version"])
    if r is None:
        return "missing"
    if r.returncode != 0:
        return "unknown"
    return ((r.stdout or "").strip().splitlines() or ["unknown"])[0][:80]


def validation_receipt(files):
    """Receipt proving these {slug: sha256} validated clean under the
    current CLI (written by the VPS lint-only gate, consumed by the remote
    build — trust transfer so 136 CLI re-validations are skipped for
    identical content)."""
    return {"version": CACHE_VERSION, "cli": cli_version(),
            "files": dict(files), "errors": []}


def receipt_covers(receipt, files, cli):
    """True when every current file hash is receipted clean under the same
    version + CLI. Any doubt returns False (caller validates fully —
    failure mode is slowness, never unsoundness). Pure."""
    try:
        if not isinstance(receipt, dict):
            return False
        if receipt.get("version") != CACHE_VERSION:
            return False
        if receipt.get("cli") != cli:
            return False
        if receipt.get("errors"):
            return False
        covered = receipt.get("files") or {}
        return all(covered.get(s) == h for s, h in files.items())
    except Exception:
        return False


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


def validate(path):
    """THE gate-grade Sigma check — one function, so the author-time check and
    the publish gate can never disagree.

    2026-09-10: the CTI agent self-validated with validate_sigma() (YAML shape
    + required keys only), reported "6 Sigma rules, all validated clean (OK)",
    and the publish gate — which uses `sigma check` — then rejected 2 rules
    using the non-existent `|isnot` modifier. The agent saw green, the gate
    saw red, and the site stayed unpublished for hours. Anything an author is
    told to run must be this function.

    Falls back to the structural check only when sigma-cli is absent.
    """
    cli_errs, missing = check_with_cli(path)
    if cli_errs is None and missing:
        return validate_sigma(path)
    return cli_errs or []


def validate_sigma(path):
    """Structural fallback (YAML shape + required keys) — used only when
    sigma-cli is unavailable. NOT a substitute for validate()."""
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
