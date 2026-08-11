#!/usr/bin/env python3
"""Tia N. List — YARA detection content (tier 5).

Selective by design: only families with real technical detail (hardcoded
strings, hashes, distinctive behaviors) get a rule. Every rule is compiled
with yara-x (minimum YARA-X version, per the design decision) and carries the
honest status: experimental, derived from our case analysis — NOT validated
against live samples unless a sample's provenance is documented.

Files per case (engine/data/cti/):
  <slug>.yara   YARA-X rule(s)
"""
import os

try:
    import yara_x
except ImportError:
    yara_x = None


def validate_yara(path):
    """Compile-validate a .yara file; returns a list of errors ([] = valid).
    A missing yara-x library is reported as an error — validation must be
    explicit, not silently skipped."""
    if yara_x is None:
        return ["yara-x not installed (pip install yara-x)"]
    try:
        src = open(path).read()
    except OSError as e:
        return [str(e)]
    try:
        yara_x.compile(src)
    except Exception as e:
        return [f"{os.path.basename(path)}: {e}"]
    return []
