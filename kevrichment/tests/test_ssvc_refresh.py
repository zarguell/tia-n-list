"""Daily SSVC refresh (ssvc_refresh.py) — deterministic upstream reconciliation.

2026-09-08: CVE-2026-81963 shipped agent-authored vulnrichment values
(automatable=unknown, technical_impact=unknown, exploitation_status=active)
while upstream said no/total/active — and nothing ever re-checked. These
tests pin the refresh rules: only stated upstream fields are written, absent
values never clobber real ones, bod_26_04 is recomputed, writes are
all-or-nothing, and majority fetch failure refuses the whole run.

All network mocked (injected ``fetch`` / monkeypatched module fetcher).
"""
import json

import ssvc_refresh as sr
from schema import compute_bod_timeline


def _rec(cve, auto="unknown", ti="unknown", explo="unknown",
         kev_date="2026-09-08", **over):
    rec = {
        "schema_version": "1.0",
        "cve_id": cve,
        "last_researched": "2026-09-08T19:41:33Z",
        "kev_date_added": kev_date,
        "kev_vendor_project": "Acme",
        "kev_product": "Widget",
        "kev_vulnerability_name": "Acme Widget Bug",
        "cwe": [],
        "vulnrichment": {
            "automatable": auto,
            "technical_impact": ti,
            "exploitation_status": explo,
        },
        # bod consistent with the record's own values, as the pipeline writes it
        "bod_26_04": compute_bod_timeline(auto, ti, bool(kev_date)),
        "kevrichment_research": {"hunting_hypothesis": "Hunt for x"},
        "research_meta": {"timestamp": "2026-09-08T19:41:33Z",
                          "sources_consulted": []},
    }
    rec.update(over)
    return rec


def _write(tmp_path, rec):
    d = tmp_path / "kevrichment" / "data" / "cves"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{rec['cve_id']}.json"
    p.write_text(json.dumps(rec, indent=2))
    return p


def _fetch(auto="no", ti="total", explo="active"):
    """Stub upstream fetcher in the shape fetch_upstream_ssvc returns."""
    def fetch(cve_id):
        opts = {}
        if auto is not None:
            opts["automatable"] = auto
        if ti is not None:
            opts["technical_impact"] = ti
        if explo is not None:
            opts["exploitation"] = explo
        return "ok", opts
    return fetch


# ── planning ────────────────────────────────────────────────────────────────

def test_stated_upstream_fields_update_the_record(tmp_path):
    """The CVE-2026-81963 shape: unknowns replaced by upstream no/total."""
    _write(tmp_path, _rec("CVE-2026-81963", explo="active"))

    summary, plans, fatal = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), delay=0)

    assert fatal == []
    assert summary["changed"] == 1
    cve, _p, _new_rec, old, new = plans[0]
    assert (cve, old, new) == ("CVE-2026-81963",
                               ("unknown", "unknown", "active"),
                               ("no", "total", "active"))


def test_bod_26_04_recomputed_kev_total_control(tmp_path):
    """KEV + TI=total -> public 3-day forensic triage (was 14/14 unknowns)."""
    _write(tmp_path, _rec("CVE-2026-81963", explo="active"))

    _summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), delay=0)

    bod = plans[0][2]["bod_26_04"]
    assert bod["timeline_if_publicly_exposed"] == "3_days_forensic_triage"
    assert bod["timeline_if_not_publicly_exposed"] == "14_days"
    assert bod["three_day_qualifying"] is True
    assert bod["requires_forensic_analysis_if_public"] is True


def test_refreshed_stamp_written_on_change(tmp_path):
    _write(tmp_path, _rec("CVE-2026-0001"))
    summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), now="2026-09-15T10:00:00Z",
        delay=0)
    assert summary["changed"] == 1
    assert plans[0][2]["vulnrichment"]["refreshed"] == "2026-09-15T10:00:00Z"


def test_stale_missing_ssvc_notes_pruned_others_kept(tmp_path):
    """CVE-2026-81963 published 'unknown' notes next to refreshed values."""
    _write(tmp_path, _rec("CVE-2026-81963", explo="active", **{
        "qc_notes": [
            {"severity": "warn", "check": "component_extraction",
             "field": "kevrichment_research.vulnerable_component",
             "detail": "keep me"},
            {"severity": "info", "check": "missing_ssvc",
             "field": "vulnrichment.automatable", "detail": "stale"},
            {"severity": "info", "check": "missing_ssvc",
             "field": "vulnrichment.technical_impact", "detail": "stale"},
            {"severity": "info", "check": "missing_ssvc",
             "field": "vulnrichment.exploitation_status", "detail": "stale too"},
        ]}))

    _summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), delay=0)

    notes = plans[0][2]["qc_notes"]
    assert [n["detail"] for n in notes] == ["keep me"]


def test_missing_ssvc_note_kept_while_field_still_unknown(tmp_path):
    """Upstream fixing only some fields keeps the remaining honest notes."""
    _write(tmp_path, _rec("CVE-2026-0040", **{
        "qc_notes": [
            {"severity": "info", "check": "missing_ssvc",
             "field": "vulnrichment.automatable", "detail": "now stated"},
            {"severity": "info", "check": "missing_ssvc",
             "field": "vulnrichment.technical_impact", "detail": "still unknown"},
        ]}))
    _summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(auto="no", ti=None, explo=None),
        delay=0)
    notes = plans[0][2]["qc_notes"]
    assert [n["detail"] for n in notes] == ["still unknown"]


def test_absent_upstream_never_clobbers(tmp_path):
    """404 / no SSVC options yet -> record untouched, not an error."""
    p = _write(tmp_path, _rec("CVE-2026-0002"))

    summary, plans, fatal = sr.plan_refresh(
        repo=str(tmp_path), fetch=lambda cve: ("absent", None), delay=0)

    assert (summary["upstream_absent"], summary["changed"]) == (1, 0)
    assert plans == [] and fatal == []
    assert "refreshed" not in json.loads(p.read_text())["vulnrichment"]


def test_unstated_upstream_field_keeps_existing_value(tmp_path):
    """Upstream stating ONLY exploitation must not blank the other fields."""
    _write(tmp_path, _rec("CVE-2026-0003", auto="yes", ti="partial",
                          explo="poc"))
    summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(auto=None, ti=None, explo="poc"),
        delay=0)
    assert summary["changed"] == 0, "full agreement -> no write"

    _write(tmp_path, _rec("CVE-2026-0004", auto="yes", ti="partial"))
    summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(auto=None, ti=None, explo="poc"),
        delay=0)
    assert summary["changed"] == 1
    v = plans[0][2]["vulnrichment"]
    assert (v["automatable"], v["technical_impact"],
            v["exploitation_status"]) == ("yes", "partial", "poc")


def test_out_of_vocabulary_upstream_value_ignored(tmp_path):
    _write(tmp_path, _rec("CVE-2026-0031"))
    summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path),
        fetch=_fetch(auto="sometimes", ti="enormous", explo="maybe"),
        delay=0)
    assert summary["changed"] == 0, "nothing stated in vocab -> no write"


def test_no_change_writes_nothing(tmp_path):
    """Upstream agreeing with the record -> no plan, no refreshed stamp."""
    p = _write(tmp_path, _rec("CVE-2026-0005", auto="no", ti="total",
                              explo="active"))
    before = p.read_text()

    summary, plans, fatal = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), delay=0)

    assert (summary["changed"], plans, fatal) == (0, [], [])
    assert p.read_text() == before


def test_unreadable_record_is_fatal(tmp_path):
    d = tmp_path / "kevrichment" / "data" / "cves"
    d.mkdir(parents=True, exist_ok=True)
    (d / "CVE-2026-0006.json").write_text("{not json")
    _write(tmp_path, _rec("CVE-2026-0007"))

    summary, plans, fatal = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), delay=0)

    assert len(fatal) == 1 and "CVE-2026-0006" in fatal[0]
    assert summary["changed"] == 1   # the good record still planned …
    assert all("CVE-2026-0006" not in p[0] for p in plans)


def test_fetch_errors_counted_not_planned(tmp_path):
    _write(tmp_path, _rec("CVE-2026-0008"))
    _write(tmp_path, _rec("CVE-2026-0009"))

    summary, plans, fatal = sr.plan_refresh(
        repo=str(tmp_path), fetch=lambda cve: ("error", None), delay=0)

    assert summary["checked"] == 2 and summary["fetch_errors"] == 2
    assert (plans, fatal) == ([], [])


def test_non_kev_record_recomputes_bod_without_kev(tmp_path):
    from schema import compute_bod_timeline
    _write(tmp_path, _rec("CVE-2026-0010", kev_date="", auto="yes",
                          ti="total"))

    summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(auto="yes", ti="total",
                                         explo="poc"), delay=0)

    assert summary["changed"] == 1
    assert plans[0][2]["bod_26_04"] == compute_bod_timeline(
        "yes", "total", False)


def test_only_filters_records(tmp_path):
    _write(tmp_path, _rec("CVE-2026-0011"))
    _write(tmp_path, _rec("CVE-2026-0012"))
    summary, _plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), delay=0, only=["CVE-2026-0011"])
    assert summary["checked"] == 1
    assert summary["cves_changed"] == ["CVE-2026-0011"]


# ── apply + index ───────────────────────────────────────────────────────────

def test_apply_plans_writes_validated_json(tmp_path):
    p = _write(tmp_path, _rec("CVE-2026-0013"))
    _summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), now="2026-09-15T10:00:00Z",
        delay=0)
    assert sr._validate_plans(plans) == []
    assert sr.apply_plans(plans) == 1
    on_disk = json.loads(p.read_text())
    assert on_disk["vulnrichment"] == {
        "automatable": "no", "technical_impact": "total",
        "exploitation_status": "active", "refreshed": "2026-09-15T10:00:00Z"}
    assert on_disk["kevrichment_research"] == {   # research fields untouched
        "hunting_hypothesis": "Hunt for x"}
    assert on_disk["last_researched"] == "2026-09-08T19:41:33Z"


def test_rebuild_index_reflects_refreshed_values(tmp_path):
    _write(tmp_path, _rec("CVE-2026-0014"))
    _write(tmp_path, _rec("CVE-2026-0015", kev_date="2026-09-01"))
    _summary, plans, _f = sr.plan_refresh(
        repo=str(tmp_path), fetch=_fetch(), delay=0)
    sr.apply_plans(plans)

    entries, skipped = sr.rebuild_index(repo=str(tmp_path))

    assert (entries, skipped) == (2, [])
    idx = json.loads(
        (tmp_path / "kevrichment" / "data" / "index.json").read_text())
    by_id = {e["cve_id"]: e for e in idx["cves"]}
    assert by_id["CVE-2026-0014"]["automatable"] == "no"
    assert by_id["CVE-2026-0014"]["technical_impact"] == "total"
    assert by_id["CVE-2026-0014"]["three_day_qualifying"] is True
    assert idx["total_cves_processed"] == 2
    # newest kev_date first — kev-verify ordering
    assert idx["cves"][0]["cve_id"] == "CVE-2026-0014"


# ── CLI exit codes ──────────────────────────────────────────────────────────

def _last_json(out):
    return json.loads(out.strip().splitlines()[-1])


def test_main_exit_0_writes_and_summarizes(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(sr, "fetch_upstream_ssvc", _fetch())
    p = _write(tmp_path, _rec("CVE-2026-0020"))

    rc = sr.main(["--repo", str(tmp_path)])

    out = capsys.readouterr().out
    assert rc == 0
    assert _last_json(out)["changed"] == 1
    assert "refreshed" in json.loads(p.read_text())["vulnrichment"]


def test_main_dry_run_reports_without_writing(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(sr, "fetch_upstream_ssvc", _fetch())
    p = _write(tmp_path, _rec("CVE-2026-0021"))
    before = p.read_text()

    rc = sr.main(["--repo", str(tmp_path), "--dry-run"])

    out = capsys.readouterr().out
    assert rc == 0
    assert _last_json(out)["changed"] == 1
    assert p.read_text() == before


def test_main_exit_2_on_fatal_writes_nothing(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(sr, "fetch_upstream_ssvc", _fetch())
    d = tmp_path / "kevrichment" / "data" / "cves"
    d.mkdir(parents=True, exist_ok=True)
    (d / "CVE-2026-0016.json").write_text("{broken")
    p = _write(tmp_path, _rec("CVE-2026-0017"))
    before = p.read_text()

    rc = sr.main(["--repo", str(tmp_path), "--dry-run"])

    out = capsys.readouterr().out
    assert rc == 2
    assert "ABORT" in out
    assert p.read_text() == before


def test_main_exit_3_on_majority_fetch_errors(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(sr, "fetch_upstream_ssvc",
                        lambda cve, attempts=3, backoff=2.0: ("error", None))
    p = _write(tmp_path, _rec("CVE-2026-0018"))
    _write(tmp_path, _rec("CVE-2026-0019"))
    before = p.read_text()

    rc = sr.main(["--repo", str(tmp_path)])

    out = capsys.readouterr().out
    assert rc == 3
    assert "ABORT" in out
    assert p.read_text() == before
