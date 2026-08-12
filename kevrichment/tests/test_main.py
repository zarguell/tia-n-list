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
