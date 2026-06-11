"""
Output schema builder and validator for kevrichment.
Defines the two-level data schema (index + per-CVE records).
"""

SCHEMA_VERSION = "1.0"

REQUIRED_CVE_FIELDS = [
    "schema_version",
    "cve_id",
    "last_researched",
    "kev_date_added",
    "kev_vendor_project",
    "kev_product",
]


def build_cve_record(cve_id, kev_entry, nvd_data, vulnrichment_data, research_data, research_meta, in_kev=True):
    """Build a complete per-CVE record from all data sources."""
    nvd_desc = ""
    cwe = []
    cvss_v3_base = None
    cvss_v3_vector = ""
    cpe_affected = []

    if nvd_data:
        vulns = nvd_data.get("vulnerabilities", [])
        if vulns:
            cve_item = vulns[0].get("cve", {})

            # Description
            for d in cve_item.get("descriptions", []):
                if d.get("lang") == "en":
                    nvd_desc = d.get("value", "")
                    break

            # CWE
            for w in cve_item.get("weaknesses", []):
                for desc in w.get("description", []):
                    val = desc.get("value", "")
                    if val.startswith("CWE-"):
                        cwe.append(val)

            # CVSS (prefer v3.1 over v3.0)
            metrics = cve_item.get("metrics", {})
            cvss_v3 = (metrics.get("cvssMetricV31") or metrics.get("cvssMetricV30") or [{}])[0]
            if cvss_v3:
                cd = cvss_v3.get("cvssData", {})
                cvss_v3_base = cd.get("baseScore")
                cvss_v3_vector = cd.get("vectorString", "")

            # CPE
            for cfg in cve_item.get("configurations", []):
                for node in cfg.get("nodes", []):
                    for cpe in node.get("cpeMatch", []):
                        if cpe.get("vulnerable", False):
                            cpe_affected.append(cpe.get("criteria", ""))

    record = {
        "schema_version": SCHEMA_VERSION,
        "cve_id": cve_id,
        "last_researched": research_meta.get("timestamp", ""),
        "kev_date_added": kev_entry.get("dateAdded", ""),
        "kev_vendor_project": kev_entry.get("vendorProject", ""),
        "kev_product": kev_entry.get("product", ""),
        "kev_short_description": kev_entry.get("shortDescription", ""),
        "kev_required_action": kev_entry.get("requiredAction", ""),
        "kev_due_date": kev_entry.get("dueDate", ""),
        "kev_vulnerability_name": kev_entry.get("vulnerabilityName", ""),
        "nvd_description": nvd_desc,
        "cwe": cwe,
        "cvss_v3_base_score": cvss_v3_base,
        "cvss_v3_vector": cvss_v3_vector,
        "cpe_affected": cpe_affected,
        "vulnrichment": {
            "automatable": vulnrichment_data.get("automatable", "unknown"),
            "technical_impact": vulnrichment_data.get("technical_impact", "unknown"),
            "exploitation_status": vulnrichment_data.get("exploitation", "unknown"),
        },
        "bod_26_04": compute_bod_timeline(
            automatable=vulnrichment_data.get("automatable", "unknown"),
            technical_impact=vulnrichment_data.get("technical_impact", "unknown"),
            in_kev=in_kev,
        ),
        "kevrichment_research": research_data,
        "research_meta": research_meta,
    }
    return record


def build_index_entry(cve_record):
    """Build a lightweight index entry from a full CVE record."""
    research = cve_record.get("kevrichment_research", {})
    bod = cve_record.get("bod_26_04", {})
    return {
        "cve_id": cve_record["cve_id"],
        "kev_date_added": cve_record["kev_date_added"],
        "vendor_project": cve_record["kev_vendor_project"],
        "product": cve_record["kev_product"],
        "automatable": cve_record["vulnrichment"]["automatable"],
        "technical_impact": cve_record["vulnrichment"]["technical_impact"],
        "exploitation_status": cve_record["vulnrichment"]["exploitation_status"],
        "three_day_qualifying": bod.get("three_day_qualifying", False),
        "requires_forensic_analysis_if_public": bod.get("requires_forensic_analysis_if_public", False),
        "requires_forensic_analysis_if_not_public": bod.get("requires_forensic_analysis_if_not_public", False),
        "timeline_if_publicly_exposed": bod.get("timeline_if_publicly_exposed", "unknown"),
        "timeline_if_not_publicly_exposed": bod.get("timeline_if_not_publicly_exposed", "unknown"),
        "public_poc_exists": research.get("public_poc_exists", "unknown"),
        "last_researched": cve_record["last_researched"],
        "file": f"data/cves/{cve_record['cve_id']}.json",
    }


def build_run_log(run_id, stats):
    """Build a per-run stats record."""
    processed = max(stats.get("cves_processed", 0), 1)
    return {
        "run_id": run_id,
        "cves_processed": stats.get("cves_processed", 0),
        "cves_skipped": stats.get("cves_skipped", 0),
        "skip_reason": stats.get("skip_reason", ""),
        "total_wall_time_seconds": stats.get("total_wall_time", 0),
        "total_tokens_used": stats.get("total_tokens", None),
        "avg_time_per_cve_seconds": round(stats.get("total_wall_time", 0) / processed, 1),
        "avg_tokens_per_cve": round(stats.get("total_tokens", 0) / processed)
            if stats.get("total_tokens") else None,
        "errors": stats.get("errors", []),
    }


def validate_cve_record(record):
    """Validate that a CVE record has all required fields."""
    missing = [f for f in REQUIRED_CVE_FIELDS if f not in record]
    if missing:
        raise ValueError(f"Missing required fields in {record.get('cve_id', '?')}: {missing}")
    if record.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"Unknown schema version: {record.get('schema_version')}")
    return True


# ---------------------------------------------------------------------------
# BOD 26-04 Remediation Timeline
# ---------------------------------------------------------------------------

def compute_bod_timeline(automatable, technical_impact, in_kev):
    """Compute BOD 26-04 remediation timelines based on SSVC + KEV status.

    Returns a dict with:

    ==========================================  =============================
    Field                                       Description
    ==========================================  =============================
    ``timeline_if_publicly_exposed``            ``3_days_forensic_triage`` |
                                                ``14_days`` | ``60_days`` |
                                                ``defer_to_next_upgrade``
    ``timeline_if_not_publicly_exposed``        Same values for internal-
                                                only assets
    ``three_day_qualifying``                    ``true`` when ALL four BOD
                                                26-04 risk factors are
                                                present for a publicly-
                                                exposed asset
    ``requires_forensic_analysis_if_public``    ``true`` when the public
                                                timeline includes forensic
                                                triage (only 3-day bucket)
    ``requires_forensic_analysis_if_not_public`` Same for non-public assets
    ==========================================  =============================

    Reference: BOD 26-04 Table 1 (June 10, 2026).
    """
    auto = str(automatable).lower() == "yes"
    total = str(technical_impact).lower() == "total"

    if in_kev:
        # --- KEV entries ---
        if auto and total:
            pub = "3_days_forensic_triage"
            non_pub = "60_days"
        elif auto or total:
            pub = "14_days"
            non_pub = "60_days" if (auto or total) else "defer_to_next_upgrade"
        else:
            pub = "60_days"
            non_pub = "defer_to_next_upgrade"
    else:
        # --- Non-KEV entries (vulnrichment-scan supplemental) ---
        if auto and total:
            pub = "3_days_forensic_triage"   # would be 3-day if KEV was yes
            non_pub = "60_days"
        elif auto or total:
            pub = "14_days"
            non_pub = "60_days"
        else:
            pub = "60_days"
            non_pub = "defer_to_next_upgrade"

    return {
        "timeline_if_publicly_exposed": pub,
        "timeline_if_not_publicly_exposed": non_pub,
        "three_day_qualifying": pub == "3_days_forensic_triage",
        "requires_forensic_analysis_if_public": pub == "3_days_forensic_triage",
        "requires_forensic_analysis_if_not_public": non_pub == "3_days_forensic_triage",
    }
