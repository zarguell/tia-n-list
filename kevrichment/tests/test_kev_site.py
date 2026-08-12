"""Regression tests for the ported /kev/ site controls (engine/kev.py).

Carries the safe_url allowlist cases from the deleted kevrichment test_build_site.py
(scheme rejection + quote escaping) plus the kev.py CVE-ID shape gate, date
helpers, enum label mapping, and feed window logic. Runs in CI via
site-deploy.yml (python -m pytest kevrichment/tests/test_kev_site.py) from the
repo root; imports engine.kev as a namespace package (`from engine import kev`).

Network-free: feed_items uses a synthetic index and a monkeypatched load_cve.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from engine import kev
from engine.store import safe_url


# ---------------------------------------------------------------------------
# S1: safe_url allowlist (migrated from kevrichment/tests/test_build_site.py)
# ---------------------------------------------------------------------------

def test_safe_url_rejects_javascript_scheme():
    assert safe_url("javascript:alert(1)") == ""


def test_safe_url_rejects_data_scheme():
    assert safe_url("data:text/html,<script>alert(1)</script>") == ""


def test_safe_url_rejects_file_scheme():
    assert safe_url("file:///etc/passwd") == ""


def test_safe_url_accepts_https():
    assert safe_url("https://example.com/x") == "https://example.com/x"


def test_safe_url_accepts_http():
    assert safe_url("http://example.com/x") == "http://example.com/x"


def test_safe_url_handles_none_and_empty():
    assert safe_url(None) == ""
    assert safe_url("") == ""


# ---------------------------------------------------------------------------
# CVE-ID shape gate (S0: every path/URL construction)
# ---------------------------------------------------------------------------

def test_gate_cve_normalizes():
    assert kev.gate_cve(" cve-2026-8037 ") == "CVE-2026-8037"


def test_gate_cve_rejects_malformed():
    for bad in ["", "CVE-2026", "CVE-2026-803", "CVE-2026-80370000",
                "../../etc/passwd", "CVE-2026-8037/x", None, 123]:
        assert kev.gate_cve(bad) is None, bad


def test_index_rows_drop_malformed_and_trim():
    index = {"cves": [
        {"cve_id": "CVE-2026-0001", "vendor_project": "  Acme ", "product": " Widget  ",
         "automatable": "yes", "exploitation_status": "active", "public_poc_exists": "yes",
         "three_day_qualifying": True, "timeline_if_publicly_exposed": "3_days",
         "kev_date_added": "2026-08-01", "cvss_v3_base_score": 9.8},
        {"cve_id": "not-a-cve"},
        {"cve_id": "CVE-2026-0002", "exploitation_status": "bogus-value",
         "public_poc_exists": "unclear"},
    ]}
    rows = kev.index_rows(index)
    assert len(rows) == 2
    assert rows[0]["vendor"] == "Acme" and rows[0]["product"] == "Widget"
    assert rows[1]["exploit"] == "unknown" and rows[1]["poc"] == "unknown"
    assert rows[0]["threeDay"] is True
    assert rows[0]["timeline"] == "3 days"
    assert rows[0]["dateAdded"] == "2026-08-01"


# ---------------------------------------------------------------------------
# Date helpers: '' on failure, never the raw string
# ---------------------------------------------------------------------------

def test_fmt_date_parses_and_fails_clean():
    assert kev.fmt_date("2026-08-07T00:00:00Z") == "2026-08-07"
    assert kev.fmt_date("2026-08-07") == "2026-08-07"
    assert kev.fmt_date("") == ""
    assert kev.fmt_date("not-a-date") == ""
    assert kev.fmt_date(None) == ""


def test_fmt_ts_parses_and_fails_clean():
    assert kev.fmt_ts("2026-08-08T13:48:31Z") == "2026-08-08 13:48 UTC"
    assert kev.fmt_ts("garbage") == ""
    assert kev.fmt_ts(None) == ""


def test_src_tag_normalizes_blobs():
    assert kev.src_tag("hermes") == "agent"
    assert kev.src_tag("HERMES agent analysis") == "agent"
    assert kev.src_tag("deterministic fallback") == "deterministic"
    # older records carry URL blobs in the source field - never render as chips
    assert kev.src_tag("Check Point Research (https://research.checkpoint.com/2020/x)") == ""
    assert kev.src_tag(None) == ""


# ---------------------------------------------------------------------------
# Feed: window, cap, empty-date exclusion, plain-text descriptions
# ---------------------------------------------------------------------------

def _synthetic_index():
    return {"cves": [
        {"cve_id": "CVE-2026-9001", "kev_date_added": "2026-08-10",
         "vendor_project": "VendorA", "product": "ProdA",
         "public_poc_exists": "yes", "three_day_qualifying": True},
        # non-KEV vulnrichment-scan entry: empty kev_date_added -> excluded
        {"cve_id": "CVE-2026-9002", "kev_date_added": "",
         "vendor_project": "V", "product": "P"},
        # outside the 90-day window
        {"cve_id": "CVE-2025-9003", "kev_date_added": "2025-01-01",
         "vendor_project": "Old", "product": "Old"},
    ]}


def test_feed_items(monkeypatch):
    def fake_load_cve(cid):
        return {"cve_id": cid, "kev_vulnerability_name": "Bad vuln",
                "kevrichment_research": {"kevrichment_summary": "  A summary.  "},
                "kev_short_description": "Short desc"}
    monkeypatch.setattr(kev, "load_cve", fake_load_cve)
    items = kev.feed_items(_synthetic_index())
    assert len(items) == 1
    it = items[0]
    assert it["title"] == "CVE-2026-9001: Bad vuln"
    assert it["link"] == "https://zarguell.github.io/tia-n-list/kev/cves/CVE-2026-9001/"
    assert it["pub_date"].endswith("+0000")
    assert "A summary." in it["description"]
    assert "PoC: yes" in it["description"] and "3-day: yes" in it["description"]


def test_feed_items_cap(monkeypatch):
    monkeypatch.setattr(kev, "load_cve", lambda cid: {"cve_id": cid})
    index = {"cves": [
        {"cve_id": f"CVE-2026-{9000 + i}", "kev_date_added": "2026-08-01",
         "vendor_project": "V", "product": "P"} for i in range(1, 11)]}
    items = kev.feed_items(index, cap=5)
    assert len(items) == 5


def test_feed_items_fallback_to_short_description(monkeypatch):
    monkeypatch.setattr(kev, "load_cve", lambda cid: {"cve_id": cid,
                                                      "kev_vulnerability_name": "",
                                                      "kev_short_description": "SHORT"})
    items = kev.feed_items(_synthetic_index())
    assert "SHORT" in items[0]["description"]


# ---------------------------------------------------------------------------
# Sitemap entries: bounded, gated
# ---------------------------------------------------------------------------

def test_kev_sitemap_entries_bounded_and_gated():
    index = {"cves": [
        {"cve_id": "CVE-2026-9001", "kev_date_added": "2026-08-10"},
        {"cve_id": "bad-id", "kev_date_added": "2026-08-10"},
        {"cve_id": "CVE-2025-9001", "kev_date_added": "2025-01-01"},
    ]}
    entries = kev.kev_sitemap_entries(index)
    paths = [p for p, _ in entries]
    assert "kev/" in paths and "kev/pipeline.html" in paths
    assert "kev/cves/CVE-2026-9001/" in paths
    assert "kev/cves/CVE-2025-9001/" not in paths  # outside window
    assert not any(p.startswith("kev/cves/bad") for p in paths)
