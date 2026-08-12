"""
Quality control layer for kevrichment CVE records.

Two-pass architecture:
  **Pass 1 — Detect:** Run all checks, collect notes.
  **Pass 2 — Fix:** Apply auto-fixes for unambiguous issues.

Each check produces zero or more QC notes with:
  ``severity``  — ``"error"`` | ``"warn"`` | ``"info"``
  ``check``     — check name
  ``field``     — the field with the issue
  ``detail``    — human-readable description
  ``auto_fixed`` — whether the issue was automatically corrected
"""

import json
import os
import re

# ---------------------------------------------------------------------------
#  Per-CVE QC
# ---------------------------------------------------------------------------

def run_qc(cve_record):
    """Run all QC checks on a single CVE record.

    Returns the (possibly auto-fixed) record and embeds ``qc_notes``.
    """
    notes = []

    _check_precondition_contradictions(cve_record, notes)
    _check_component_extraction(cve_record, notes)
    _check_hypothesis_redundancy(cve_record, notes)
    _check_advisory_fallback(cve_record, notes)
    _check_ssvc_completeness(cve_record, notes)

    cve_record["qc_notes"] = notes
    return cve_record


# ------------------------------------------------------------------
#  Individual checks
# ------------------------------------------------------------------

def _check_precondition_contradictions(record, notes):
    """Detect contradictions between natural-language preconditions and CVSS."""
    r = record.get("kevrichment_research", {})
    pre = r.get("preconditions_for_exploit", "")
    cvss = record.get("cvss_v3_vector", "")

    if not pre or not cvss:
        return

    # preconditions_for_exploit can be a list if the enrichment produced multiple
    # statements; flatten to string for string-level analysis.
    if isinstance(pre, list):
        pre = "; ".join(p.strip() for p in pre if isinstance(p, str))
    elif not isinstance(pre, str):
        pre = str(pre)

    cvss_vals = {}
    for part in cvss.split("/"):
        if ":" in part:
            k, v = part.split(":", 1)
            cvss_vals[k] = v

    av = cvss_vals.get("AV")
    pr = cvss_vals.get("PR")
    ui = cvss_vals.get("UI")

    fixes = []
    pre_lower = pre.lower()

    # -- Attack Vector contradictions --
    if av == "N" and "local shell" in pre_lower:
        fixes.append((pre[pre_lower.index("local shell"):pre_lower.index("local shell") + 50].partition(";")[0] + "; ",
                       "CVSS says AV:N (network) but precondition says 'Local shell'; removed"))
    if av in ("L", "P", "A") and "network reachability" in pre_lower:
        fixes.append((pre[pre_lower.index("network reachability"):pre_lower.index("network reachability") + 60].partition(";")[0] + "; ",
                       f"CVSS says AV:{av} but precondition says 'Network reachability'; removed"))

    # -- Privileges contradictions --
    if pr == "N" and "credentials required" in pre_lower:
        notes.append({
            "severity": "info",
            "check": "precondition_contradiction",
            "field": "kevrichment_research.preconditions_for_exploit",
            "detail": "CVSS says PR:N but precondition mentions credential requirement — may need auth despite no privileges",
            "auto_fixed": False,
        })

    # -- User Interaction contradictions --
    if ui == "R" and "no explicit interaction" in pre_lower:
        fixes.append((pre[pre_lower.index("no explicit interaction"):pre_lower.index("no explicit interaction") + 65].partition(";")[0] + "; ",
                       "CVSS says UI:R (interaction required) but precondition says no interaction; removed"))
    if ui == "N" and "user must interact" in pre_lower:
        fixes.append((pre[pre_lower.index("user must interact"):pre_lower.index("user must interact") + 60].partition(";")[0] + "; ",
                       "CVSS says UI:N (no interaction) but precondition says user interaction required; removed"))

    # -- Component/product applicability --
    if not any(word in pre_lower for word in
               ("run", "accessible", "vulnerable version", "affected")):
        notes.append({
            "severity": "info",
            "check": "precondition_contradiction",
            "field": "kevrichment_research.preconditions_for_exploit",
            "detail": "Preconditions don't mention deployment applicability (component/product version)",
            "auto_fixed": False,
        })

    # Apply auto-fixes
    fixed_pre = pre
    for pattern, detail in fixes:
        if pattern in fixed_pre:
            fixed_pre = fixed_pre.replace(pattern, "")
    if fixed_pre != pre:
        r["preconditions_for_exploit"] = fixed_pre.strip().strip(";").strip()
        notes.append({
            "severity": "warn",
            "check": "precondition_contradiction",
            "field": "kevrichment_research.preconditions_for_exploit",
            "detail": "; ".join(d for _, d in fixes),
            "auto_fixed": True,
        })


def _check_component_extraction(record, notes):
    """Check if component extraction fell back to product or has verb artifacts."""
    r = record.get("kevrichment_research", {})
    comp = r.get("vulnerable_component", "")
    product = record.get("kev_product", "")

    if not comp or comp == product or product in comp:
        notes.append({
            "severity": "warn",
            "check": "component_extraction",
            "field": "kevrichment_research.vulnerable_component",
            "detail": (f"Component '{comp}' matches or contains product name '{product}' "
                       f"— no specific component identified"),
            "auto_fixed": False,
        })
        return

    # Verb artifact detection
    verb_pat = re.compile(
        r'\b(allow|could|may|that|which|permit|enable|affect|result|lead)\b',
        re.IGNORECASE,
    )
    m = verb_pat.search(comp)
    if m:
        truncated = comp[:m.start()].strip().rstrip(",; ").strip()
        if len(truncated) > 3:
            r["vulnerable_component"] = truncated
            notes.append({
                "severity": "error",
                "check": "component_extraction",
                "field": "kevrichment_research.vulnerable_component",
                "detail": f"Component contained verb artifacts ('{comp}'); truncated to '{truncated}'",
                "auto_fixed": True,
            })
        else:
            notes.append({
                "severity": "error",
                "check": "component_extraction",
                "field": "kevrichment_research.vulnerable_component",
                "detail": f"Component contains verb artifacts ('{comp}') but cannot auto-fix cleanly",
                "auto_fixed": False,
            })


def _check_hypothesis_redundancy(record, notes):
    """Flag redundant vendor/product repetition in hunting hypothesis."""
    r = record.get("kevrichment_research", {})
    hyp = r.get("hunting_hypothesis", "")
    vendor = record.get("kev_vendor_project", "")
    product = record.get("kev_product", "")
    comp = r.get("vulnerable_component", product)

    if not hyp:
        return

    full_name = f"{vendor} {product}"
    count = hyp.count(full_name)
    if count > 1:
        notes.append({
            "severity": "info",
            "check": "hunting_hypothesis_redundancy",
            "field": "kevrichment_research.hunting_hypothesis",
            "detail": f"'{full_name}' appears {count} times in hunting hypothesis",
            "auto_fixed": False,
        })

    # Check redundant "X component of Y X" pattern
    if f"the {comp} component of {vendor} {product}" in hyp and (comp == product or product in comp):
        notes.append({
            "severity": "info",
            "check": "hunting_hypothesis_redundancy",
            "field": "kevrichment_research.hunting_hypothesis",
            "detail": f"Hypothesis reads as 'the {comp} component of {vendor} {product}' where component==product",
            "auto_fixed": False,
        })


def _check_advisory_fallback(record, notes):
    """Flag when advisory URL is the NVD fallback."""
    r = record.get("kevrichment_research", {})
    url = r.get("vendor_advisory_url", "")
    if "nvd.nist.gov/vuln/detail/" in url:
        notes.append({
            "severity": "info",
            "check": "advisory_fallback",
            "field": "kevrichment_research.vendor_advisory_url",
            "detail": "URL is NVD detail page (fallback) — no vendor-specific advisory found",
            "auto_fixed": False,
        })


def _check_ssvc_completeness(record, notes):
    """Flag missing SSVC values."""
    v = record.get("vulnrichment", {})
    for field in ("automatable", "technical_impact", "exploitation_status"):
        val = v.get(field, "unknown")
        if val in ("unknown", "", None):
            notes.append({
                "severity": "info",
                "check": "missing_ssvc",
                "field": f"vulnrichment.{field}",
                "detail": f"SSVC '{field}' is unknown — no Vulnrichment data for this CVE",
                "auto_fixed": False,
            })


# ---------------------------------------------------------------------------
#  QC report
# ---------------------------------------------------------------------------

def qc_summary(cve_records):
    """Build a summary report over all QC'd records."""
    all_notes = []
    counts = {"error": 0, "warn": 0, "info": 0}
    auto_fixed = 0

    for rec in cve_records:
        for n in rec.get("qc_notes", []):
            all_notes.append(n)
            counts[n.get("severity", "info")] += 1
            if n.get("auto_fixed"):
                auto_fixed += 1

    return {
        "total_cves_qcd": len(cve_records),
        "total_notes": len(all_notes),
        "errors": counts["error"],
        "warnings": counts["warn"],
        "infos": counts["info"],
        "auto_fixed": auto_fixed,
        "by_check": _group_notes(all_notes),
    }


def _group_notes(notes):
    groups = {}
    sev_map = {"error": "errors", "warn": "warnings", "info": "infos"}
    for n in notes:
        ck = n.get("check", "unknown")
        g = groups.setdefault(ck, {"count": 0, "errors": 0, "warnings": 0, "infos": 0})
        g["count"] += 1
        key = sev_map.get(n.get("severity", "info"), "infos")
        g[key] += 1
    return groups


# ---------------------------------------------------------------------------
#  Pipeline entry point
# ---------------------------------------------------------------------------

def run_qc_pipeline(cve_dir=None):
    """Run QC on all CVE JSON files in a directory.

    Scans ``data/cves/``, runs checks, writes back auto-fixed files,
    and returns ``(report, records)``.
    """
    if cve_dir is None:
        base = os.path.dirname(os.path.abspath(__file__))
        cve_dir = os.path.join(base, "data", "cves")

    records = []
    for fname in sorted(os.listdir(cve_dir)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(cve_dir, fname)
        with open(path) as f:
            record = json.load(f)

        record = run_qc(record)
        records.append(record)

        # Persist auto-fixes
        with open(path, "w") as f:
            json.dump(record, f, indent=2)

    report = qc_summary(records)
    return report, records
