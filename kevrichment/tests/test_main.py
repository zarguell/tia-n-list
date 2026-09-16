"""Tests for main.py orchestration error handling."""
import pytest

import main


def test_run_pipeline_raises_on_kev_fetch_failure(monkeypatch, tmp_path):
    """run_pipeline must raise KevrichmentError, not call sys.exit, on KEV fetch failure."""
    monkeypatch.setattr(main, "fetch_kev", lambda: (_ for _ in ()).throw(ConnectionError("network down")))
    monkeypatch.setattr(main, "_save_run_log", lambda run_log: None)
    monkeypatch.setattr(main, "_ensure_dirs", lambda: None)
    monkeypatch.setattr(main, "_load_index", lambda: {"cves": []})
    monkeypatch.setattr(main, "get_kev_source_date", lambda d: "1970-01-01")

    with pytest.raises(main.KevrichmentError):
        main.run_pipeline()


def test_kevrichment_error_is_exception_subclass():
    assert issubclass(main.KevrichmentError, Exception)


def test_build_cve_record_carries_catalog_fingerprint():
    """kev_seq/kev_catalog_count flow record -> index entry (feed ordering)."""
    from schema import build_cve_record, build_index_entry
    rec = build_cve_record(
        "CVE-2026-87886",
        {"dateAdded": "2026-09-16", "vendorProject": "V", "product": "P",
         "shortDescription": "", "requiredAction": "", "dueDate": "",
         "vulnerabilityName": "n"},
        None, {}, {}, {"timestamp": "t"},
        kev_seq=0, kev_catalog_count=1713)
    assert rec["kev_seq"] == 0
    assert rec["kev_catalog_count"] == 1713
    entry = build_index_entry(rec)
    assert entry["kev_seq"] == 0
    assert entry["kev_catalog_count"] == 1713


def test_build_cve_record_defaults_without_fingerprint():
    """Non-KEV scan records (no catalog entry) carry None, not a guess."""
    from schema import build_cve_record, build_index_entry
    rec = build_cve_record(
        "CVE-2026-0001",
        {"dateAdded": "", "vendorProject": "", "product": "",
         "shortDescription": "", "requiredAction": "", "dueDate": "",
         "vulnerabilityName": "Non-KEV (vulnrichment scan)"},
        None, {}, {}, {"timestamp": "t"}, in_kev=False)
    assert rec["kev_seq"] is None
    assert rec["kev_catalog_count"] is None
    assert build_index_entry(rec)["kev_seq"] is None
