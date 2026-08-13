#!/usr/bin/env python3
"""Determinism tests for the KEV-candidates pipeline: the exploitation
backfill classifier and the per-CVE timeline aggregation.

Run: python3 engine/test_cve_timeline.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.

Contracts defended:
  1. classify_event: negation never matches ("no evidence of in-the-wild
     exploitation", "not yet added to KEV"); focused events (<=2 CVEs)
     attribute all CVEs; roundups (>2 CVEs) attribute only CVEs co-located
     with the phrase in the same sentence.
  2. cve_timeline.build: first_reported = min story first_seen across
     canonical stories; first_exploit_report = min flagged-event date;
     merged-away shells are excluded; KEV deltas are signed.
  3. The same inputs always produce the same rows (determinism).
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import backfill_exploitation as bf  # noqa: E402
import cve_timeline as tl  # noqa: E402


# ---------------------------------------------------------------------------
# backfill classifier
# ---------------------------------------------------------------------------

def test_negation_never_matches():
    assert bf.classify_event(
        "CVE-2026-1111 VMware Advisory",
        "There is no evidence of in-the-wild exploitation of CVE-2026-1111.") == {}
    assert bf.classify_event(
        "CVE-2026-1112 Advisory",
        "CVE-2026-1112 has not yet been added to the KEV catalog.") == {}


def test_focused_event_attributes_all_cves():
    flags = bf.classify_event(
        "Hackers Exploit Critical VMware vCenter Flaw",
        "CVE-2026-59310 is being actively exploited in attacks across 47 countries.")
    assert flags.get("CVE-2026-59310", {}).get("status") == "exploited"
    assert flags["CVE-2026-59310"]["source"] == "backfill"
    # two-CVE focused events attribute both
    flags = bf.classify_event(
        "Two flaws exploited in the wild",
        "CVE-2026-1113 and CVE-2026-1114 are actively exploited, per CISA.")
    assert set(flags) == {"CVE-2026-1113", "CVE-2026-1114"}


def test_roundup_requires_sentence_colocation():
    body = ("Patch Tuesday fixes 200 CVEs. CVE-2026-2221 is being actively "
            "exploited in the wild. CVE-2026-2222 addresses a memory corruption "
            "issue with no exploitation observed.")
    flags = bf.classify_event("CVE-2026-2221 CVE-2026-2222 CVE-2026-2223 Patch Tuesday",
                              body)
    assert flags.get("CVE-2026-2221", {}).get("status") == "exploited"
    # 2222/2223 are NOT in the exploit sentence -> not attributed
    assert "CVE-2026-2222" not in flags
    assert "CVE-2026-2223" not in flags


def test_kev_confirmation_is_exploited():
    flags = bf.classify_event(
        "CISA Adds SolarWinds Serv-U CVE-2026-28318 to KEV",
        "CISA added CVE-2026-28318 to the KEV catalog after confirmed exploitation.")
    assert flags.get("CVE-2026-28318", {}).get("status") == "exploited"


def test_suspected_tier():
    flags = bf.classify_event(
        "CVE-2026-3333 public PoC released",
        "A public exploit for CVE-2026-3333 was released on GitHub.")
    assert flags.get("CVE-2026-3333", {}).get("status") == "suspected"


# ---------------------------------------------------------------------------
# timeline aggregation (fixture store in a temp dir)
# ---------------------------------------------------------------------------

FIXTURES = {
    "stories/cve-a.json": {
        "id": "cve-a", "title": "A", "first_seen": "2026-07-30T00:00:00Z",
        "last_seen": "2026-07-30T00:00:00Z", "cves": ["CVE-2026-59310"],
        "score": 5.0, "events": [], "merged_into": None},
    "stories/cve-b.json": {
        "id": "cve-b", "title": "B", "first_seen": "2026-08-12T11:51:45Z",
        "last_seen": "2026-08-13T09:00:00Z", "cves": ["CVE-2026-59310"],
        "score": 6.0, "events": []},
    "stories/shell.json": {   # merged-away -> excluded from the join
        "id": "shell", "title": "S", "first_seen": "2026-06-01T00:00:00Z",
        "last_seen": "2026-06-01T00:00:00Z", "cves": ["CVE-2026-59310"],
        "score": 0.0, "events": [], "merged_into": "cve-a"},
    "events/e1.json": {
        "id": "e1", "title": "first", "published_at": "2026-07-30T00:00:00Z",
        "cves": ["CVE-2026-59310"], "kind": "original",
        "exploitation": {"CVE-2026-59310": {"status": "suspected",
                                            "evidence": "PoC", "source": "backfill"}}},
    "events/e2.json": {
        "id": "e2", "title": "exploit report", "published_at": "2026-08-12T12:27:22Z",
        "cves": ["CVE-2026-59310"], "kind": "update",
        "exploitation": {"CVE-2026-59310": {"status": "exploited",
                                            "evidence": "implants", "source": "backfill"}}},
}


def _rows():
    with tempfile.TemporaryDirectory() as tmp:
        for rel, obj in FIXTURES.items():
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            json.dump(obj, open(p, "w"))
        # point the module at the fixture store (monkeypatch disk paths)
        old = (tl.STORIES, tl.EVENTS, tl.ANALYSIS, tl.NVD_CACHE, tl.KEV_INDEX)
        tl.STORIES = os.path.join(tmp, "stories")
        tl.EVENTS = os.path.join(tmp, "events")
        tl.ANALYSIS = os.path.join(tmp, "analysis")
        tl.NVD_CACHE = os.path.join(tmp, "nvd-published.json")
        tl.KEV_INDEX = os.path.join(tmp, "kev-index.json")
        try:
            yield tl.build(nvd={"CVE-2026-59310": "2026-07-30"})
        finally:
            (tl.STORIES, tl.EVENTS, tl.ANALYSIS,
             tl.NVD_CACHE, tl.KEV_INDEX) = old


def test_build_min_aggregation_and_merged_exclusion():
    for rows in _rows():
        r = rows["CVE-2026-59310"]
        # merged shell (2026-06-01) excluded -> first_reported from cve-a
        assert r["first_reported"] == "2026-07-30T00:00:00Z"
        # only exploited flags anchor the first-exploit date (e1 suspected ignored)
        assert r["first_exploit_report"] == "2026-08-12T12:27:22Z"
        assert r["n_stories"] == 2
        assert r["exploit_status"] == "exploited"
        assert r["disclose"] == "2026-07-30"
        assert r["on_kev"] is False
        assert r["kev_delta_days"] is None
        assert r["gap_disclose_report"] == 0
        # candidate name = exploit-report title (the dedicated coverage)
        assert r["name"] == "exploit report"


def test_index_rows_include_on_kev_with_name():
    for rows in _rows():
        # simulate a crossing: on-KEV row keeps its kev record name
        rows["CVE-2026-59310"]["on_kev"] = True
        rows["CVE-2026-59310"]["kev_date_added"] = "2026-08-09"
        rows["CVE-2026-59310"]["exploit_to_kev_days"] = -3
        ix = {r["id"]: r for r in tl.index_rows(rows)}
        assert set(ix) == {"CVE-2026-59310"}
        assert ix["CVE-2026-59310"]["onKev"] is True
        assert ix["CVE-2026-59310"]["kevAdded"] == "2026-08-09"
        assert ix["CVE-2026-59310"]["exploitToKev"] == -3
        assert ix["CVE-2026-59310"]["name"] == "exploit report"


def test_build_kev_crossing_delta_signed():
    for rows in _rows():
        rows["CVE-2026-59310"]["on_kev"] = True
        rows["CVE-2026-59310"]["kev_date_added"] = "2026-08-09"
        rows["CVE-2026-59310"]["kev_delta_days"] = tl._days_between(
            "2026-07-30T00:00:00Z", "2026-08-09")
        rows["CVE-2026-59310"]["exploit_to_kev_days"] = tl._days_between(
            "2026-08-12T12:27:22Z", "2026-08-09")
        r = rows["CVE-2026-59310"]
        assert r["kev_delta_days"] == 10          # 08-09 - 07-30
        assert r["exploit_to_kev_days"] == -3     # KEV before the exploit report
        # candidates() excludes on-KEV rows; crossings() includes them
        assert tl.candidates(rows) == []
        assert [c["cve"] for c in tl.crossings(rows, days=30,
                                                today="2026-08-13")] == ["CVE-2026-59310"]


def test_coverage_without_exploitation_is_not_lead_time():
    """The user contract (2026-08-13): coverage timing must never be presented
    as exploitation lead time, and CVEs without an exploitation flag are
    EXCLUDED from the tracking page entirely (patch-record mentions are
    clutter). kev_delta_days stays a coverage fact; exploit_to_kev_days = None;
    index_rows drops the row."""
    for rows in _rows():
        r = rows["CVE-2026-59310"]
        r["on_kev"] = True
        r["kev_date_added"] = "2026-08-09"
        r["kev_delta_days"] = tl._days_between("2026-07-30T00:00:00Z", "2026-08-09")
        r["exploit_events"] = []          # strip the exploitation flags
        r["first_exploit_report"] = ""
        r["exploit_status"] = None
        r["exploit_to_kev_days"] = None
        assert r["kev_delta_days"] == 10
        assert r["exploit_to_kev_days"] is None
        assert r not in tl.flagged(rows)
        ix = {x["id"]: x for x in tl.index_rows(rows)}
        assert "CVE-2026-59310" not in ix


def test_determinism():
    a = [json.dumps(v, sort_keys=True) for v in _rows()]
    b = [json.dumps(v, sort_keys=True) for v in _rows()]
    assert a == b


if __name__ == "__main__":
    failures = []
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as e:  # noqa: BLE001
                failures.append((name, e))
                print(f"FAIL {name}: {e}")
    if failures:
        print(f"{len(failures)} failure(s)")
        sys.exit(1)
    print("all cve_timeline tests pass")
