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
from datetime import datetime, timedelta, timezone

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

def _days_ago(days):
    """ISO date relative to today (UTC).

    feed_items/kev_sitemap_entries gate on a rolling 90-day window, so test
    fixtures must NOT carry absolute dates: the old 2026-08-01/2026-08-10
    fixtures hit the window edge on 2026-10-31 and would all have aged out by
    2026-11-08, turning CI red on every push (2026-10-31 deploy-watch
    incident) even though production code was unchanged."""
    return (datetime.now(timezone.utc).date() - timedelta(days=days)).isoformat()


def _synthetic_index():
    return {"cves": [
        {"cve_id": "CVE-2026-9001", "kev_date_added": _days_ago(30),
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
        {"cve_id": f"CVE-2026-{9000 + i}", "kev_date_added": _days_ago(30),
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
        {"cve_id": "CVE-2026-9001", "kev_date_added": _days_ago(30)},
        {"cve_id": "bad-id", "kev_date_added": _days_ago(30)},
        {"cve_id": "CVE-2025-9001", "kev_date_added": "2025-01-01"},
    ]}
    entries = kev.kev_sitemap_entries(index)
    paths = [p for p, _ in entries]
    assert "kev/" in paths and "kev/pipeline.html" in paths
    assert "kev/cves/CVE-2026-9001/" in paths
    assert "kev/cves/CVE-2025-9001/" not in paths  # outside window
    assert not any(p.startswith("kev/cves/bad") for p in paths)


# ---------------------------------------------------------------------------
# CISA catalog link (every KEV detail page links out to CISA)
# ---------------------------------------------------------------------------

def test_cisa_catalog_url_exact():
    assert kev.cisa_catalog_url("CVE-2026-85880") == (
        "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"
        "?search=CVE-2026-85880&field_date_added_wrapper=all&field_cve="
        "&sort_by=field_date_added&items_per_page=20&url=")


def test_cisa_catalog_url_rejects_malformed():
    assert kev.cisa_catalog_url("bad-id") == ""
    assert kev.cisa_catalog_url(None) == ""
    assert kev.cisa_catalog_url("cve-2026-85880") == kev.cisa_catalog_url("CVE-2026-85880")


def test_cve_view_includes_cisa_url():
    v = kev.cve_view({"cve_id": "CVE-2026-85880"}, [])
    assert v["cisa_url"] == kev.cisa_catalog_url("CVE-2026-85880")
    v = kev.cve_view({"cve_id": "bad-id"}, [])
    assert v["cisa_url"] == ""


# ---------------------------------------------------------------------------
# Feed ordering + pubDate: same-day KEV additions in true insertion order
# ---------------------------------------------------------------------------

def test_feed_items_same_day_order_follows_kev_seq(monkeypatch):
    # 2026-09-16 regression: 87886 was the day's LAST KEV addition but the
    # date-only sort left it at the bottom of the trio (alphabetical order).
    # Catalog stamps: the day's batch is listed insertion-order, so 87886
    # carries the highest seq and must render first.
    monkeypatch.setattr(kev, "load_cve", lambda cid: {"cve_id": cid})
    index = {"cves": [
        {"cve_id": "CVE-2026-58704", "kev_date_added": _days_ago(30),
         "vendor_project": "V", "product": "P",
         "kev_catalog_count": 1713, "kev_seq": 0},
        {"cve_id": "CVE-2026-87886", "kev_date_added": _days_ago(30),
         "vendor_project": "V", "product": "P",
         "kev_catalog_count": 1713, "kev_seq": 2},
        {"cve_id": "CVE-2026-76460", "kev_date_added": _days_ago(30),
         "vendor_project": "V", "product": "P",
         "kev_catalog_count": 1713, "kev_seq": 1},
    ]}
    items = kev.feed_items(index, days=90)
    assert [i["title"].split(":")[0] for i in items] == \
        ["CVE-2026-87886", "CVE-2026-76460", "CVE-2026-58704"]


def test_feed_items_pubdate_uses_ingest_time(monkeypatch):
    monkeypatch.setattr(kev, "load_cve", lambda cid: {"cve_id": cid})
    added = _days_ago(30)
    index = {"cves": [{"cve_id": "CVE-2026-76460",
                       "kev_date_added": added,
                       "vendor_project": "V", "product": "P",
                       "last_researched": f"{added}T19:24:18Z"}]}
    (it,) = kev.feed_items(index, days=90)
    assert "19:24:18" in it["pub_date"]


def test_feed_items_pubdate_falls_back_to_add_date(monkeypatch):
    monkeypatch.setattr(kev, "load_cve", lambda cid: {"cve_id": cid})
    index = {"cves": [{"cve_id": "CVE-2026-9001",
                       "kev_date_added": _days_ago(30),
                       "vendor_project": "V", "product": "P"}]}
    (it,) = kev.feed_items(index, days=90)
    assert "00:00:00" in it["pub_date"]


# ---------------------------------------------------------------------------
# Remediation deadlines (2026-11-13): CISA's own due date + countdown buckets
# ---------------------------------------------------------------------------

def test_due_iso_and_days_left():
    today = datetime(2026, 11, 13, tzinfo=timezone.utc).date()
    assert kev.due_iso({"kev_due_date": "2026-11-12"}) == "2026-11-12"
    assert kev.due_iso({}) == ""
    assert kev.due_iso(None) == ""
    assert kev.days_left("2026-11-12", today) == -1
    assert kev.days_left("2026-11-13", today) == 0
    assert kev.days_left("2026-11-20", today) == 7
    assert kev.days_left("", today) is None
    assert kev.days_left("not-a-date", today) is None


def test_deadline_state_thresholds():
    assert kev.deadline_state(None) == "none"
    assert kev.deadline_state(-40) == "overdue"
    assert kev.deadline_state(0) == "urgent"
    assert kev.deadline_state(kev.DEADLINE_URGENT_DAYS) == "urgent"
    assert kev.deadline_state(kev.DEADLINE_URGENT_DAYS + 1) == "soon"
    assert kev.deadline_state(kev.DEADLINE_SOON_DAYS + 1) == "horizon"
    assert kev.deadline_state(kev.DEADLINE_HORIZON_DAYS + 1) == "later"


def test_deadline_label_is_human():
    assert kev.deadline_label(None) == ""
    assert kev.deadline_label(0) == "due today"
    assert kev.deadline_label(3) == "3d left"
    assert kev.deadline_label(-12) == "12d overdue"


def test_enrich_deadlines_joins_records_without_guessing():
    today = datetime(2026, 11, 13, tzinfo=timezone.utc).date()
    rows = [{"id": "CVE-2026-0001"}, {"id": "CVE-2026-0002"}, {"id": "CVE-2026-0003"}]
    records = {
        "CVE-2026-0001": {"kev_due_date": "2026-11-12"},   # yesterday
        "CVE-2026-0002": {"kev_due_date": None},           # no date
        # CVE-2026-0003 has no record at all
    }
    kev.enrich_deadlines(rows, records, today=today)
    assert (rows[0]["due"], rows[0]["days"], rows[0]["state"], rows[0]["countdown"]) == \
        ("2026-11-12", -1, "overdue", "1d overdue")
    assert (rows[1]["due"], rows[1]["days"], rows[1]["state"]) == ("", None, "none")
    assert (rows[2]["due"], rows[2]["state"]) == ("", "none")
    assert kev.deadline_summary(rows)["overdue"] == 1
    assert kev.deadline_summary(rows)["none"] == 2


def test_sitemap_lists_the_deadline_board():
    paths = [p for p, _ in kev.kev_sitemap_entries({"cves": []})]
    assert "kev/deadlines/" in paths


# ---------------------------------------------------------------------------
# EPSS trend (2026-11-13): committed 21-day series -> sparkline geometry
# ---------------------------------------------------------------------------

def test_epss_trend_geometry():
    t = kev.epss_trend([None, None, 10, 12, None, 14, 20], scale=1000,
                       width=132, height=26, pad=3)
    assert t["days"] == 4 and t["rising"] is True
    assert abs(t["first"] - 0.010) < 1e-9 and abs(t["last"] - 0.020) < 1e-9
    assert abs(t["delta"] - 0.010) < 1e-9
    pts = t["points"].split(" ")
    assert len(pts) == 4
    # x maps day index -> [pad, width-pad]: values live at indices 2,3,5,6 of 7
    assert abs(float(pts[0].split(",")[0]) - (3 + 126 * (2 / 6))) < 0.2
    assert abs(float(pts[-1].split(",")[0]) - (132 - 3)) < 0.2
    # y is inverted (bigger value -> smaller y)
    ys = [float(p.split(",")[1]) for p in pts]
    assert ys[0] > ys[-1]


def test_epss_trend_needs_two_points():
    assert kev.epss_trend([]) is None
    assert kev.epss_trend([None, None]) is None
    assert kev.epss_trend([None, 5, None]) is None


def test_epss_trend_flat_series_does_not_divide_by_zero():
    t = kev.epss_trend([7, 7, 7])
    assert t["first"] == t["last"] == 0.007 and t["delta"] == 0
    assert t["rising"] is False
    ys = {p.split(",")[1] for p in t["points"].split(" ")}
    assert len(ys) == 1          # flat line


def test_load_epss_history_is_tolerant(tmp_path):
    empty = tmp_path / "missing.json"
    assert kev.load_epss_history(str(empty)) == ([], {})
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    assert kev.load_epss_history(str(bad)) == ([], {})
    odd = tmp_path / "odd.json"
    odd.write_text('{"dates": "x", "series": []}')
    assert kev.load_epss_history(str(odd)) == ([], {})
    good = tmp_path / "good.json"
    good.write_text('{"dates": ["2026-11-11"], "series": {"CVE-2026-0001": [16]}}')
    dates, series = kev.load_epss_history(str(good))
    assert dates == ["2026-11-11"] and series["CVE-2026-0001"] == [16]


def test_epss_view_joins_record_and_history(monkeypatch):
    monkeypatch.setattr(kev, "_EPSS_CACHE", {"data": (
        ["2026-11-10", "2026-11-11", "2026-11-12"],
        {"CVE-2026-0001": [100, 110, 130]})}, raising=False)
    rec = {"cve_id": "CVE-2026-0001", "epss": 0.013,
           "epss_percentile": 0.9, "epss_date": "2026-11-12"}
    v = kev._epss_view(rec)
    assert v["score"] == 0.013 and v["pct"] == 0.9
    assert v["trend"]["first"] == 0.1 and v["trend"]["last"] == 0.13
    assert v["trend"]["from_date"] == "2026-11-10"
    # a record with no EPSS at all renders nothing (no empty panel)
    assert kev._epss_view({"cve_id": "CVE-2026-0002"}) is None
