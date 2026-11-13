"""Tests for the daily bulk EPSS refresh (kevrichment/epss.py)."""
import gzip
import importlib.util
import io
import json
import os
import sys
from datetime import date
from unittest import mock

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "epss", os.path.join(HERE, "..", "epss.py"))
epss = importlib.util.module_from_spec(spec)
sys.modules["epss"] = epss
spec.loader.exec_module(epss)


def _gz_bytes(score_date, rows):
    buf = io.StringIO()
    buf.write(f"#model_version:v2026.01,score_date:{score_date}\n")
    buf.write("cve,epss,percentile\n")
    for cve, e, p in rows:
        buf.write(f"{cve},{e},{p}\n")
    return gzip.compress(buf.getvalue().encode())


def _mk_record(tmp_path, cve, **extra):
    d = tmp_path / "data" / "cves"
    d.mkdir(parents=True, exist_ok=True)
    rec = {"cve_id": cve, "cvss_v3_base_score": 7.5, **extra}
    (d / f"{cve}.json").write_text(json.dumps(rec, indent=1))
    return d


def test_parse_extracts_date_and_scores(tmp_path):
    p = tmp_path / "bulk.csv.gz"
    p.write_bytes(_gz_bytes("2026-09-23",
                            [("CVE-2026-0001", "0.5", "0.9"),
                             ("CVE-2026-0002", "0.01", "0.2")]))
    date_, scores = epss.parse(str(p))
    assert date_ == "2026-09-23"
    assert scores["CVE-2026-0001"] == ("0.5", "0.9")


def test_fetch_uses_header_date_as_truth(monkeypatch, tmp_path):
    epss.CACHE_DIR = str(tmp_path / "epss")
    payload = _gz_bytes("2026-09-22", [("CVE-2026-0001", "0.5", "0.9")])
    resp = mock.Mock(content=payload)      # raise_for_status() is a no-op Mock
    monkeypatch.setattr(epss.requests, "get",
                        mock.Mock(return_value=resp))
    date_, path = epss.fetch(today=date(2026, 9, 24))
    assert date_ == "2026-09-22"     # publication lags wall clock: date is truth
    assert path.endswith("epss_scores-2026-09-22.csv.gz")
    date2, path2 = epss.fetch(today=date(2026, 9, 24))
    assert path == path2


def test_enrich_preserves_fields_and_computes_delta(tmp_path):
    d = _mk_record(tmp_path, "CVE-2026-0001", kev_date_added="2026-09-01",
                   kevrichment_research={"preconditions": "x"})
    epss.CVE_DIR = str(d)
    scores = {"CVE-2026-0001": ("0.55", "0.91")}
    prev = {"CVE-2026-0001": ("0.05", "0.4")}
    changed, total = epss.enrich("2026-09-23", scores, prev)
    assert (changed, total) == (1, 1)
    rec = json.loads((d / "CVE-2026-0001.json").read_text())
    assert rec["epss"] == 0.55 and rec["epss_date"] == "2026-09-23"
    assert rec["epss_delta_7d"] == 0.5
    # untouched fields survive
    assert rec["kevrichment_research"] == {"preconditions": "x"}
    assert rec["kev_date_added"] == "2026-09-01"
    # second run: idempotent
    changed2, _ = epss.enrich("2026-09-23", scores, prev)
    assert changed2 == 0


def test_enrich_writes_canonical_formatting(tmp_path):
    """Regression (2026-11-13): this writer used indent=1 while every other
    writer of data/cves/*.json uses indent=2, so each daily refresh
    re-indented all ~1,780 records (~171k changed lines) and packed ~30 MB/
    month of git history for a handful of changed score fields per record.
    The fixture is written with indent=1 on purpose: enrich() must normalize
    it, not preserve it."""
    d = _mk_record(tmp_path, "CVE-2026-0001", kev_date_added="2026-09-01")
    epss.CVE_DIR = str(d)
    changed, _ = epss.enrich("2026-09-23",
                             {"CVE-2026-0001": ("0.55", "0.91")}, {})
    assert changed == 1
    p = d / "CVE-2026-0001.json"
    rec = json.loads(p.read_text())
    assert p.read_text() == json.dumps(rec, indent=2)


def test_enrich_skips_unknown_cves(tmp_path):
    d = _mk_record(tmp_path, "CVE-2026-0002")
    epss.CVE_DIR = str(d)
    changed, total = epss.enrich("2026-09-23",
                                 {"CVE-9999-9999": ("0.1", "0.1")}, {})
    assert (changed, total) == (0, 1)
    rec = json.loads((d / "CVE-2026-0002.json").read_text())
    assert "epss" not in rec


def test_prior_snapshot_picks_newest_within_window(tmp_path):
    epss.CACHE_DIR = str(tmp_path / "epss")
    os.makedirs(epss.CACHE_DIR)
    for d, rows in (("2026-09-10", [("CVE-2026-0001", "0.05", "0.4")]),
                    ("2026-09-01", [("CVE-2026-0001", "0.02", "0.2")]),
                    ("2026-09-23", [("CVE-2026-0001", "0.55", "0.9")])):
        with open(epss._cache_path(d), "wb") as f:
            f.write(_gz_bytes(d, rows))
    date_, scores = epss._prior_snapshot("2026-09-23")
    assert date_ == "2026-09-10"         # >= 7d old, newest such
    assert scores["CVE-2026-0001"] == ("0.05", "0.4")


def test_output_line_format(tmp_path, monkeypatch, capsys):
    epss.CVE_DIR = str(tmp_path / "cves")
    epss.CACHE_DIR = str(tmp_path / "epss")
    os.makedirs(epss.CVE_DIR)
    os.makedirs(epss.CACHE_DIR)
    monkeypatch.setattr(epss, "fetch", lambda today=None: ("2026-09-23", "x"))
    monkeypatch.setattr(epss, "parse", lambda p: ("2026-09-23", {}))
    monkeypatch.setattr(epss, "_prior_snapshot", lambda d: (None, {}))
    epss.main()
    out = capsys.readouterr().out.strip().splitlines()[-1]
    assert out == ("epss: 2026-09-23 refreshed 0/0 records "
                   "(cache 0 files, no prior snapshot)")


def test_write_history_from_cache(tmp_path, monkeypatch):
    """The committed 21-day series the /kev/ CVE pages chart: built from the
    untracked snapshot cache, integers scaled by HISTORY_SCALE, nulls for CVEs
    absent on a day, and write-if-changed so a quiet day adds no git churn."""
    cache = tmp_path / "epss"
    cache.mkdir()
    for d, rows in (("2026-11-10", [("CVE-2026-0001", "0.10", "0.5")]),
                    ("2026-11-11", [("CVE-2026-0001", "0.20", "0.6")]),
                    ("2026-11-12", [("CVE-2026-0001", "0.30", "0.7")])):
        with open(cache / f"epss_scores-{d}.csv.gz", "wb") as f:
            f.write(_gz_bytes(d, rows))
    cves = tmp_path / "cves"
    cves.mkdir()
    (cves / "CVE-2026-0001.json").write_text("{}")
    (cves / "CVE-2026-0002.json").write_text("{}")      # never scored
    out = tmp_path / "epss-history.json"

    monkeypatch.setattr(epss, "CACHE_DIR", str(cache))
    monkeypatch.setattr(epss, "HISTORY_PATH", str(out))
    n = epss.write_history(days=21, cve_dir=str(cves))
    assert n == 2
    doc = json.loads(out.read_text())
    assert doc["scale"] == 1000
    assert doc["dates"] == ["2026-11-10", "2026-11-11", "2026-11-12"]
    assert doc["series"]["CVE-2026-0001"] == [100, 200, 300]
    assert doc["series"]["CVE-2026-0002"] == [None, None, None]

    # write-if-changed: identical input must not rewrite the file
    stamp = out.stat().st_mtime_ns
    epss.write_history(days=21, cve_dir=str(cves))
    assert out.stat().st_mtime_ns == stamp

    # empty cache -> no file written, 0 returned
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setattr(epss, "CACHE_DIR", str(empty))
    out2 = tmp_path / "none.json"
    monkeypatch.setattr(epss, "HISTORY_PATH", str(out2))
    assert epss.write_history(cve_dir=str(cves)) == 0
    assert not out2.exists()
