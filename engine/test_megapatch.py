#!/usr/bin/env python3
"""Determinism tests for the Mega Patch Tracker renderer (engine/megapatch.py).

Run: python3 engine/test_megapatch.py   (exit 0 = pass)
Wired into CI (site-deploy.yml).

Contracts defended:
  1. Path construction from release slugs is shape-gated (no traversal, no
     arbitrary strings in URLs/paths).
  2. Date/percentile helpers return '' on bad input, never the raw value.
  3. The served table JSON drops invalid CVE ids and caps the chips.
  4. The story <-> release join (coverage_map/release_coverage) is exact.
  5. render_site writes the three page types + the table JSON from committed
     data, and the templates render with the real field contract.
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import megapatch as mp  # noqa: E402

import jinja2  # noqa: E402

ENGINE = os.path.dirname(os.path.abspath(__file__))


def _row(cve, **kw):
    base = {
        "cve": cve, "title": "A vulnerability", "family": "Windows",
        "severity": "Critical", "impact": "Remote Code Execution",
        "cvss": 9.8, "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "epss": 0.5, "epss_pct": 0.9, "kev": False, "exploited": False,
        "disclosed": False, "automatable": "yes", "technical_impact": "total",
        "exploitation": "none", "kbs": ["5000001"], "media": 0,
        "score": 70.0, "why": ["CVSS 9.8", "automatable"],
    }
    base.update(kw)
    return base


def _record():
    rows = [_row("CVE-2026-1001"), _row("CVE-2026-1002", severity="Important",
                                        kev=True, media=2)]
    return {
        "schema": 1, "vendor": "Microsoft", "track": "microsoft-patch-tuesday",
        "track_label": "Patch Tuesday", "release": "2026-Oct",
        "slug": "oct-2026", "label": "October 2026", "published": "2026-10-13",
        "doc": {"url": "https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/2026-Oct",
                "initial_release": "2026-10-13T07:00:00",
                "current_release": "2026-11-07T14:41:55"},
        "collected_at": "2026-11-10T00:00:00Z", "updated_at": "2026-11-10T00:00:00Z",
        "next": {"release": "2026-Nov", "date": "2026-11-10", "label": "November 2026"},
        "stated_total": 1474, "excluded": {"Mariner": 1274, "Browser": 757},
        "doc_total": 3490,
        "counts": {"total": 2, "critical": 1, "important": 1, "moderate": 0,
                   "low": 0, "kev": 1, "exploited": 0, "disclosed": 0,
                   "automatable": 2, "tech_total": 2, "epss_ge_10": 1,
                   "epss_ge_50": 1, "media": 1, "with_kb": 2},
        "families": [{"name": "Windows", "count": 2, "updates": 1,
                      "type": "Cumulative"}],
        "notable": [{"cve": "CVE-2026-1001", "title": "Windows foo",
                     "flags": ["Exploitation Detected"]}],
        "cnas": [], "blogs": [],
        "severity": [{"name": "Critical", "count": 1}, {"name": "Important", "count": 1}],
        "impacts": [{"name": "Remote Code Execution", "count": 2}],
        "top": [dict(_row("CVE-2026-1001"), products=["Windows 11"],
                     cwes=["CWE-122: Heap-based Buffer Overflow"],
                     kb_urls=["https://support.microsoft.com/help/5000001"],
                     media_stories=[], ssvc_source="derived")],
        "rows": rows,
        "analysis": {"headline": "A test headline", "summary": ["One paragraph."],
                     "themes": [{"title": "Theme", "detail": "Detail.",
                                 "cves": ["CVE-2026-1001"]}],
                     "data_vs_prose": "Data text.", "watchlist": [
                         {"cve": "CVE-2026-1002", "why": "Watch it."}],
                     "patch_note": "Patch Windows.", "source": "agent"},
        "tracking": {"days": 7, "start": "2026-10-13", "end": "2026-10-20",
                     "snapshots": [{"date": "2026-10-14", "day": 1, "kev": 1,
                                    "kev_added": ["CVE-2026-1002"],
                                    "epss_moves": [], "media_new": [],
                                    "media_total": 1, "max_score": 70.0}]},
    }


def _write_fixture(root, record=None):
    track = os.path.join(root, "microsoft-patch-tuesday")
    os.makedirs(track, exist_ok=True)
    record = record or _record()
    with open(os.path.join(track, "2026-Oct.json"), "w") as f:
        json.dump(record, f)
    with open(os.path.join(track, "..", "cve-index.json"), "w") as f:
        json.dump({"schema": 1, "cves": {
            "CVE-2026-1001": [{"release": "2026-Oct", "slug": "oct-2026",
                               "label": "October 2026", "published": "2026-10-13"}],
        }}, f)
    index = {"schema": 1, "updated_at": "2026-11-10T00:00:00Z", "vendors": [{
        "slug": "microsoft-patch-tuesday", "vendor": "Microsoft",
        "label": "Patch Tuesday", "cadence": "Second Tuesday",
        "source": "MSRC CVRF v3.0",
        "next": {"release": "2026-Nov", "date": "2026-11-10",
                 "label": "November 2026"},
        "months": [{"release": "2026-Oct", "slug": "oct-2026",
                    "label": "October 2026", "published": "2026-10-13",
                    "counts": record["counts"], "headline": "A test headline",
                    "tracking": {"days": 7, "snapshots": 1,
                                 "last": "2026-10-14", "active": False}}],
    }]}
    with open(os.path.join(root, "index.json"), "w") as f:
        json.dump(index, f)


def check(label, got, want):
    ok = got == want
    print(("  ok  " if ok else "  FAIL ") + label + ("" if ok else f" -> {got!r} != {want!r}"))
    return ok


# ---------------------------------------------------------------------------

def test_gate_slug():
    ok = check("valid slug", mp.gate_slug("oct-2026"), "oct-2026")
    ok &= check("rejects traversal", mp.gate_slug("../../etc/passwd"), None)
    ok &= check("rejects uppercase", mp.gate_slug("Oct-2026"), None)
    ok &= check("rejects short year", mp.gate_slug("oct-26"), None)
    ok &= check("rejects non-string", mp.gate_slug(None), None)
    ok &= check("release from slug", mp.release_from_slug("oct-2026"), "2026-Oct")
    ok &= check("bad slug -> no release", mp.release_from_slug("nope"), None)
    ok &= check("release url", mp.release_url("oct-2026"),
                "megapatch/microsoft-patch-tuesday/oct-2026/")
    ok &= check("bad slug -> latest url", mp.release_url("x"),
                "megapatch/microsoft-patch-tuesday/")
    assert ok


def test_helpers():
    ok = check("long date", mp.fmt_date("2026-10-13", long=True), "13 October 2026")
    ok &= check("short date", mp.fmt_date("2026-10-13"), "2026-10-13")
    ok &= check("bad date -> empty", mp.fmt_date("nope"), "")
    ok &= check("none date -> empty", mp.fmt_date(None), "")
    ok &= check("pct 1st", mp.pct(0.01), "1st")
    ok &= check("pct 2nd", mp.pct(0.02), "2nd")
    ok &= check("pct 3rd", mp.pct(0.03), "3rd")
    ok &= check("pct 11th", mp.pct(0.11), "11th")
    ok &= check("pct 96th", mp.pct(0.9603), "96th")
    ok &= check("pct None -> empty", mp.pct(None), "")
    ok &= check("cvss one decimal", mp.cvss_num("9"), "9.0")
    ok &= check("cvss bad -> empty", mp.cvss_num("x"), "")
    ok &= check("severity class", mp.sev_class("Critical"), "sev-crit")
    ok &= check("severity unknown -> low", mp.sev_class("weird"), "sev-low")
    assert ok


def test_table_rows_shape_gate():
    rec = {"rows": [_row("CVE-2026-1001"), _row("not-a-cve"),
                    _row("CVE-2026-1002", why=["a"] * 20)]}
    rows = mp.table_rows(rec)
    ok = check("invalid CVE dropped", len(rows), 2)
    ok &= check("why capped", len(rows[1]["why"]), 5)
    ok &= check("table keys", sorted(rows[0]),
                sorted(["cve", "title", "family", "severity", "cvss", "epss_pct",
                        "kev", "automatable", "exploited", "more_likely",
                        "remote_unauth", "media", "score", "why"]))
    assert ok


def test_cve_index_gate():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "cve-index.json")
        with open(path, "w") as f:
            json.dump({"cves": {
                "CVE-2026-1001": [{"slug": "oct-2026", "label": "October 2026"}],
                "CVE-2026-1002": [{"slug": "../../evil", "label": "x"}],
                "bad": [{"slug": "oct-2026"}],
            }}, f)
        old = mp.CVE_INDEX
        mp.CVE_INDEX = path
        try:
            mp.cve_index.cache_clear() if hasattr(mp.cve_index, "cache_clear") else None
            idx = mp.cve_index()
        finally:
            mp.CVE_INDEX = old
        ok = check("valid entry kept", "CVE-2026-1001" in idx, True)
        ok &= check("bad slug entry dropped", "CVE-2026-1002" in idx, False)
        ok &= check("non-CVE key dropped", "bad" in idx, False)
        assert ok
    # missing file -> {} (fresh clone)
    old = mp.CVE_INDEX
    mp.CVE_INDEX = "/nonexistent/cve-index.json"
    try:
        assert mp.cve_index() == {}
    finally:
        mp.CVE_INDEX = old


def test_coverage_join():
    cards = [
        {"id": "story-a", "title": "A", "first_seen": "2026-10-13T00:00:00Z",
         "cves": ["CVE-2026-1002", "CVE-2026-9999"]},
        {"id": "story-b", "title": "B", "first_seen": "2026-10-14T00:00:00Z",
         "cves": "[\"CVE-2026-1002\"]"},
    ]
    cov = mp.coverage_map(cards)
    ok = check("coverage keys", sorted(cov), ["CVE-2026-1002", "CVE-2026-9999"])
    ok &= check("two stories", len(cov["CVE-2026-1002"]), 2)
    rec = {"rows": [_row("CVE-2026-1001"), _row("CVE-2026-1002", score=10)]}
    ranked = mp.release_coverage(rec, cov)
    ok &= check("only covered rows", [r["cve"] for r in ranked], ["CVE-2026-1002"])
    ok &= check("story refs carried", len(ranked[0]["stories"]), 2)
    assert ok


def test_month_row_tracking_states():
    base = {"release": "2026-Nov", "slug": "nov-2026",
            "label": "November 2026", "published": "2026-11-10", "counts": {}}
    starts = mp._month_row(dict(base, tracking={"days": 7, "state": "starts",
                                                "day": 0, "snapshots": 0}))
    ok = check("release day is 'starts', not closed", starts["state"], "starts")
    ok &= check("release day is day 0", starts["tracking_day"], 0)
    active = mp._month_row(dict(base, tracking={"days": 7, "state": "active",
                                                "day": 3, "snapshots": 3}))
    ok &= check("active day from the job", (active["state"], active["tracking_day"]),
                ("active", 3))
    old = mp._month_row(dict(base, tracking={"days": 7, "snapshots": 0}))
    ok &= check("legacy index falls back to closed", old["state"], "closed")
    assert ok


def test_sitemap_entries():
    idx = {"vendors": [{"months": [
        {"release": "2026-Oct", "slug": "oct-2026", "published": "2026-10-13"},
        {"release": "2026-Sep", "slug": "../../x", "published": "2026-09-08"},
    ]}]}
    entries = mp.sitemap_entries(idx)
    ok = check("index + latest + valid month", entries,
               [("megapatch/", ""), ("megapatch/microsoft-patch-tuesday/", ""),
                ("megapatch/microsoft-patch-tuesday/oct-2026/", "2026-10-13")])
    assert ok


def test_render_site_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        _write_fixture(tmp)
        old_data, old_engine = mp.DATA, mp.ENGINE
        mp.DATA = tmp
        mp.ENGINE = ENGINE
        written = {}

        def write(rel, content):
            written[rel] = content

        try:
            env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(os.path.join(ENGINE, "templates")),
                autoescape=True)
            env.globals["site_url"] = mp.site_url
            cards = [{"id": "story-a", "title": "Story A",
                      "first_seen": "2026-10-13T00:00:00Z",
                      "cves": ["CVE-2026-1002"]}]
            n = mp.render_site(env, write, cards)
        finally:
            mp.DATA, mp.ENGINE = old_data, old_engine

        ok = check("one release rendered", n, 1)
        ok &= check("index page written", "megapatch/index.html" in written, True)
        ok &= check("latest page written",
                    "megapatch/microsoft-patch-tuesday/index.html" in written, True)
        ok &= check("archive page written",
                    "megapatch/microsoft-patch-tuesday/oct-2026/index.html" in written,
                    True)
        ok &= check("table json written",
                    "megapatch/microsoft-patch-tuesday/oct-2026.json" in written, True)
        table = json.loads(written["megapatch/microsoft-patch-tuesday/oct-2026.json"])
        ok &= check("table has 2 rows", len(table), 2)
        html = written["megapatch/microsoft-patch-tuesday/oct-2026/index.html"]
        ok &= check("stats rendered", "1459" not in html and ">2<" in html, True)
        ok &= check("analysis rendered", "A test headline" in html, True)
        ok &= check("coverage join rendered", "Story A" in html, True)
        ok &= check("tracking rendered", "Day 1" in html, True)
        ok &= check("no origin-absolute URLs", 'href="/' not in html, True)
        ok &= check("base-relative data fetch",
                    "fetch('megapatch/microsoft-patch-tuesday/oct-2026.json')" in html,
                    True)
        assert ok


def test_backfilled_release_is_an_archive_not_tracked():
    """A retro-collected release must not pretend to have been followed for a
    week: the page says it was backfilled and shows no tracking timeline."""
    with tempfile.TemporaryDirectory() as tmp:
        rec = _record()
        rec["backfilled"] = True
        rec["tracking"]["enabled"] = False
        rec["tracking"]["snapshots"] = []
        _write_fixture(tmp, rec)
        old_data = mp.DATA
        mp.DATA = tmp
        written = {}
        try:
            env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(os.path.join(ENGINE, "templates")),
                autoescape=True)
            env.globals["site_url"] = mp.site_url
            mp.render_site(env, lambda rel, content: written.__setitem__(rel, content), [])
        finally:
            mp.DATA = old_data
        html = written["megapatch/microsoft-patch-tuesday/oct-2026/index.html"]
        ok = check("backfilled badge", "backfilled</span>" in html, True)
        ok &= check("says not tracked", "Not tracked." in html, True)
        ok &= check("no tracking timeline", "Tracking — 0 of 7 days" not in html, True)
        assert ok


def test_multi_vendor_render():
    """Two trackers: each gets a latest page, a month page, a table JSON and
    a sitemap entry; the dashboard lists both."""
    with tempfile.TemporaryDirectory() as tmp:
        ms = _record()
        _write_fixture(tmp, ms)
        # second vendor (Oracle shape: channel, CVSS-derived severity)
        ora = _record()
        ora.update({"vendor": "Oracle", "track": "oracle-critical-patch-update",
                    "track_label": "Critical Patch Update", "channel": "CSPU",
                    "channel_label": "Critical Security Patch Update",
                    "slug": "oct-2026", "release": "2026-Oct",
                    "severity_basis": "cvss"})
        ora["rows"] = [_row("CVE-2026-1001", remote_unauth=True,
                            severity="High", media=0)]
        ora["top"] = [dict(ora["rows"][0], products=[], cwes=[], kb_urls=[],
                           media_stories=[], ssvc_source="derived")]
        ora["counts"] = dict(ora["counts"], remote_unauth=1, kev=0, media=0)
        ora["impacts"] = [{"name": "Unknown", "count": 1}]
        os.makedirs(os.path.join(tmp, "oracle-critical-patch-update"))
        with open(os.path.join(tmp, "oracle-critical-patch-update",
                               "2026-Oct.json"), "w") as f:
            json.dump(ora, f)
        idx = json.load(open(os.path.join(tmp, "index.json")))
        idx["vendors"].append({
            "slug": "oracle-critical-patch-update", "vendor": "Oracle",
            "label": "Critical Patch Update", "cadence": "Monthly",
            "source": "Oracle", "severity_basis": "cvss",
            "next": {"release": "2026-Nov", "date": "2026-11-17",
                     "label": "November 2026"},
            "months": [dict(idx["vendors"][0]["months"][0],
                            slug="oct-2026", release="2026-Oct",
                            channel="CSPU", counts=ora["counts"])],
        })
        with open(os.path.join(tmp, "index.json"), "w") as f:
            json.dump(idx, f)

        old_data = mp.DATA
        mp.DATA = tmp
        written = {}
        try:
            env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(os.path.join(ENGINE, "templates")),
                autoescape=True)
            env.globals["site_url"] = mp.site_url
            n = mp.render_site(env, lambda rel, c: written.__setitem__(rel, c), [])
        finally:
            mp.DATA = old_data
        ok = check("both releases rendered", n, 2)
        ok &= check("oracle latest page",
                    "megapatch/oracle-critical-patch-update/index.html" in written, True)
        ok &= check("oracle table json",
                    "megapatch/oracle-critical-patch-update/oct-2026.json" in written, True)
        index = written["megapatch/index.html"]
        ok &= check("dashboard lists both vendors",
                    "Microsoft" in index and "Oracle" in index, True)
        ora_html = written["megapatch/oracle-critical-patch-update/oct-2026/index.html"]
        ok &= check("channel tag rendered", "CSPU" in ora_html, True)
        ok &= check("cvss severity note", "CVSS-derived" in ora_html, True)
        ok &= check("impact chart hidden when unknown",
                    ">Impact<" not in ora_html, True)
        ok &= check("nav points at oracle track",
                    'href="megapatch/oracle-critical-patch-update/"' in ora_html, True)
        assert ok


def main():
    ok = True
    for fn in (test_gate_slug, test_helpers, test_table_rows_shape_gate,
               test_cve_index_gate, test_coverage_join, test_sitemap_entries,
               test_month_row_tracking_states, test_multi_vendor_render,
               test_render_site_end_to_end,
               test_backfilled_release_is_an_archive_not_tracked):
        print(fn.__name__)
        fn()
    print("megapatch renderer: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
