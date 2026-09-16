"""kev_seq_backfill: fingerprint stamping + index rebuild (offline).

Uses a local --catalog snapshot; no network. Mirrors the 2026-09-16 live
case: three same-day KEV additions whose alphabetical order inverted the
real insertion order in the published feed.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import kev_seq_backfill as backfill

CATALOG = {"count": 1713, "catalogVersion": "2026.09.16", "vulnerabilities": [
    {"cveID": "CVE-2026-58704", "dateAdded": "2026-09-16"},
    {"cveID": "CVE-2026-76460", "dateAdded": "2026-09-16"},
    {"cveID": "CVE-2026-87886", "dateAdded": "2026-09-16"},
]}


def _rec(cid, date="2026-09-16"):
    return {"schema_version": "1.0", "cve_id": cid,
            "last_researched": "2026-09-16T14:14:38Z",
            "kev_date_added": date,
            "kev_vendor_project": "V", "kev_product": "P",
            "cve_published": "", "kev_seq": None,
            "kev_catalog_count": None}


def _corpus(tmp_path, extra_unreadable=False):
    cves = tmp_path / "kevrichment" / "data" / "cves"
    cves.mkdir(parents=True)
    for cid in ("CVE-2026-58704", "CVE-2026-76460",
                "CVE-2026-87886", "CVE-2026-0001"):
        rec = _rec(cid)
        if cid == "CVE-2026-0001":  # non-KEV vulnrichment-scan record
            rec["kev_date_added"] = ""
        (cves / f"{cid}.json").write_text(json.dumps(rec))
    if extra_unreadable:
        (cves / "CVE-2026-9999.json").write_text("{not json")
    cat = tmp_path / "catalog.json"
    cat.write_text(json.dumps(CATALOG))
    return str(tmp_path), str(cat)


def test_plan_stamps_missing_only(tmp_path):
    repo, _ = _corpus(tmp_path)
    seq = {e["cveID"]: i for i, e in enumerate(CATALOG["vulnerabilities"])}
    summary, plans, fatal = backfill.plan_backfill(
        os.path.join(repo, "kevrichment", "data", "cves"), seq, 1713)
    assert fatal == []
    assert summary["stamped"] == 3 and summary["absent"] == 1
    by_id = {c: r["kev_seq"] for c, _p, r in plans}
    assert by_id == {"CVE-2026-87886": 2, "CVE-2026-76460": 1,
                     "CVE-2026-58704": 0}


def test_plan_skips_already_stamped_unless_force(tmp_path):
    repo, _ = _corpus(tmp_path)
    d = os.path.join(repo, "kevrichment", "data", "cves")
    seq = {e["cveID"]: i for i, e in enumerate(CATALOG["vulnerabilities"])}
    summary, plans, _fatal = backfill.plan_backfill(d, seq, 1713)
    assert summary["stamped"] == 3
    backfill.apply_plans(plans)  # planning is pure — apply, then re-plan
    summary2, plans2, _ = backfill.plan_backfill(d, seq, 1713)
    assert summary2["stamped"] == 0 and summary2["already"] == 3
    # --force re-stamps
    summary3, plans3, _ = backfill.plan_backfill(d, seq, 1713, force=True)
    assert summary3["stamped"] == 3


def test_main_end_to_end_stamps_and_sorts_index(tmp_path):
    repo, cat = _corpus(tmp_path)
    rc = backfill.main(["--repo", repo, "--catalog", cat])
    assert rc == 0
    d = os.path.join(repo, "kevrichment", "data", "cves")
    stamped = {c: json.load(open(os.path.join(d, f"{c}.json")))["kev_seq"]
               for c in ("CVE-2026-58704", "CVE-2026-76460", "CVE-2026-87886")}
    assert stamped == {"CVE-2026-87886": 2, "CVE-2026-76460": 1,
                       "CVE-2026-58704": 0}
    index = json.load(open(os.path.join(repo, "kevrichment", "data",
                                        "index.json")))
    order = [e["cve_id"] for e in index["cves"]]
    assert order[:3] == ["CVE-2026-87886", "CVE-2026-76460", "CVE-2026-58704"]
    assert order[-1] == "CVE-2026-0001"  # empty dateAdded sinks to the bottom
    assert index["total_cves_processed"] == 4


def test_main_dry_run_writes_nothing(tmp_path):
    repo, cat = _corpus(tmp_path)
    rc = backfill.main(["--repo", repo, "--catalog", cat, "--dry-run"])
    assert rc == 0
    d = os.path.join(repo, "kevrichment", "data", "cves")
    rec = json.load(open(os.path.join(d, "CVE-2026-87886.json")))
    assert rec["kev_seq"] is None
    assert not os.path.exists(os.path.join(repo, "kevrichment", "data",
                                           "index.json"))


def test_main_unreadable_record_aborts_without_writing(tmp_path):
    repo, cat = _corpus(tmp_path, extra_unreadable=True)
    rc = backfill.main(["--repo", repo, "--catalog", cat])
    assert rc == 2
    d = os.path.join(repo, "kevrichment", "data", "cves")
    rec = json.load(open(os.path.join(d, "CVE-2026-87886.json")))
    assert rec["kev_seq"] is None  # all-or-nothing: nothing written


def test_main_missing_catalog_is_rc3(tmp_path):
    repo, _ = _corpus(tmp_path)
    rc = backfill.main(["--repo", repo, "--catalog",
                        str(tmp_path / "nope.json")])
    assert rc == 3
