"""Tests for schema.compute_bod_timeline against BOD 26-04 Table 1 (June 10, 2026).

Each row of the official 16-row table is encoded as a case:
  (publicly exposed?, in KEV?, automatable?, technical impact) -> (public timeline, non-public timeline)
"""
import pytest

from schema import compute_bod_timeline

# (in_kev, automatable, technical_impact) -> (timeline_if_publicly_exposed, timeline_if_not_publicly_exposed)
TABLE_ROWS = [
    # Row 1: Yes/Yes/Yes/Total  -> 3 days & forensic triage (public), row 9 (non-public)
    (True, "yes", "total", "3_days_forensic_triage", "3_days_forensic_triage"),
    # Row 2: Yes/Yes/Yes/Partial -> 3 days (no forensic); row 10 -> 14 days
    (True, "yes", "partial", "3_days", "14_days"),
    # Row 3: Yes/Yes/No/Total  -> 3 days & forensic triage; row 11 -> 14 days
    (True, "no", "total", "3_days_forensic_triage", "14_days"),
    # Row 4: Yes/Yes/No/Partial -> 14 days; row 12 -> 14 days
    (True, "no", "partial", "14_days", "14_days"),
    # Row 5: Yes/No/Yes/Total  -> 3 days (no forensic); row 13 -> 60 days
    (False, "yes", "total", "3_days", "60_days"),
    # Row 6: Yes/No/Yes/Partial -> 14 days; row 14 -> 60 days
    (False, "yes", "partial", "14_days", "60_days"),
    # Row 7: Yes/No/No/Total  -> 14 days; row 15 -> fix on system upgrade
    (False, "no", "total", "14_days", "defer_to_next_upgrade"),
    # Row 8: Yes/No/No/Partial -> 60 days; row 16 -> fix on system upgrade
    (False, "no", "partial", "60_days", "defer_to_next_upgrade"),
]


@pytest.mark.parametrize("in_kev,auto,impact,pub,non_pub", TABLE_ROWS)
def test_table_rows(in_kev, auto, impact, pub, non_pub):
    result = compute_bod_timeline(automatable=auto, technical_impact=impact, in_kev=in_kev)
    assert result["timeline_if_publicly_exposed"] == pub
    assert result["timeline_if_not_publicly_exposed"] == non_pub


def test_cve_2026_20349_kev_automatable_partial():
    """CVE-2026-20349: KEV + automatable=yes + technical_impact=partial."""
    result = compute_bod_timeline(automatable="yes", technical_impact="partial", in_kev=True)
    assert result["timeline_if_publicly_exposed"] == "3_days"
    assert result["timeline_if_not_publicly_exposed"] == "14_days"
    assert result["three_day_qualifying"] is True
    # Partial control only — no forensic triage required
    assert result["requires_forensic_analysis_if_public"] is False
    assert result["requires_forensic_analysis_if_not_public"] is False


def test_three_day_qualifying_only_for_public_three_day_buckets():
    assert compute_bod_timeline("yes", "total", True)["three_day_qualifying"] is True
    assert compute_bod_timeline("yes", "partial", True)["three_day_qualifying"] is True
    assert compute_bod_timeline("no", "partial", True)["three_day_qualifying"] is False
    assert compute_bod_timeline("no", "partial", False)["three_day_qualifying"] is False


def test_forensic_triage_only_for_total_control_rows():
    # KEV + total control -> forensic triage required (public and non-public)
    result = compute_bod_timeline("yes", "total", True)
    assert result["requires_forensic_analysis_if_public"] is True
    assert result["requires_forensic_analysis_if_not_public"] is True
    # KEV + automatable + partial -> 3 days but NO forensic triage
    result = compute_bod_timeline("yes", "partial", True)
    assert result["requires_forensic_analysis_if_public"] is False
    # Non-KEV + automatable + total -> plain 3 days, NO forensic triage (row 5)
    result = compute_bod_timeline("yes", "total", False)
    assert result["requires_forensic_analysis_if_public"] is False
    assert result["requires_forensic_analysis_if_not_public"] is False


def test_unknown_ssvc_treated_as_no_conservative():
    """Unknown SSVC values must land in the slowest bucket for the combination."""
    # KEV + unknown/unknown -> row 4/12 bucket (14 days), not 60/defer
    result = compute_bod_timeline("unknown", "unknown", True)
    assert result["timeline_if_publicly_exposed"] == "14_days"
    assert result["timeline_if_not_publicly_exposed"] == "14_days"
    # Non-KEV + unknown/unknown -> row 8/16 bucket (60 days / defer)
    result = compute_bod_timeline("unknown", "unknown", False)
    assert result["timeline_if_publicly_exposed"] == "60_days"
    assert result["timeline_if_not_publicly_exposed"] == "defer_to_next_upgrade"
