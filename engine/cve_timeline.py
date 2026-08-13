#!/usr/bin/env python3
"""Tia N. List — per-CVE timeline aggregation (KEV candidates section).

Deterministic join of the story store, the event exploitation flags (backfill
or triage), the NVD publish-date cache, and the kevrichment KEV index. Emits
one row per CVE that appears in the story store:

    cve                 CVE-2026-59310
    first_reported      min story first_seen (earliest coverage)
    first_exploit_report min event published_at with an exploited flag
    exploit_events      [event refs with status/evidence, sorted by date]
    disclose            NVD published date (or kevrichment cve_published)
    on_kev              bool — present in the kevrichment KEV index
    kev_date_added      YYYY-MM-DD when on KEV
    kev_delta_days      signed days (KEV added - first_reported); COVERAGE
                        timing only — never presented as exploitation lead
                        time (see exploit_to_kev_days)
    exploit_to_kev_days signed days (KEV added - first exploit report)
    status              "on-kev" | "candidate"
    exploit_status      "exploited" | "suspected" | None (flag presence)
    stories             [canonical story refs sorted by first_seen]
    max_score           highest story score
    has_analysis        any story carries an analysis write-up

Conventions mirror digest_candidates.py: canonical stories only (merged-away
shells are skipped — their cves are emptied anyway), CVE-IDs pass the shape
gate, and all inputs are loaded from disk (no markup, no LLM).
"""
import glob
import json
import os
import re
from datetime import date, datetime, timedelta, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
STORIES = os.path.join(DATA, "stories")
EVENTS = os.path.join(DATA, "events")
ANALYSIS = os.path.join(DATA, "analysis")
NVD_CACHE = os.path.join(DATA, "nvd-info.json")
KEV_INDEX = os.path.normpath(os.path.join(ENGINE, "..", "kevrichment", "data", "index.json"))
KEV_REC_DIR = os.path.normpath(os.path.join(ENGINE, "..", "kevrichment", "data", "cves"))

CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,7}$")
STATUSES = ("exploited", "suspected")


def gate_cve(c):
    c = (c or "").strip().upper()
    return c if CVE_RE.match(c) else None


def _load_stories():
    out = {}
    for p in glob.glob(os.path.join(STORIES, "*.json")):
        s = json.load(open(p))
        if s.get("merged_into"):
            continue
        out[s["id"]] = s
    return out


def _load_events():
    out = {}
    for p in glob.glob(os.path.join(EVENTS, "*.json")):
        e = json.load(open(p))
        out[e["id"]] = e
    return out


def _load_kev_index():
    if not os.path.exists(KEV_INDEX):
        return {"cves": []}
    return json.load(open(KEV_INDEX))


def load_nvd_info():
    """{cve: {"published": "YYYY-MM-DD", "description": "<en text>"}}."""
    if os.path.exists(NVD_CACHE):
        return json.load(open(NVD_CACHE))
    return {}


def _days_between(a_iso, b_iso):
    """Signed whole days between two ISO/date strings; None if unparseable."""
    try:
        a = date.fromisoformat((a_iso or "")[:10])
        b = date.fromisoformat((b_iso or "")[:10])
    except (ValueError, TypeError):
        return None
    return (b - a).days


def _min_iso(*vals):
    vals = [v for v in vals if v]
    return min(vals) if vals else None


def build(events=None, stories=None, kev_index=None, nvd=None):
    """Aggregate per-CVE timeline rows. All inputs optional (disk-loaded)."""
    stories = stories if stories is not None else _load_stories()
    events = events if events is not None else _load_events()
    kev_index = kev_index if kev_index is not None else _load_kev_index()
    nvd = nvd if nvd is not None else load_nvd_info()
    kev_by_id = {gate_cve(e.get("cve_id")): e for e in kev_index.get("cves", [])
                 if gate_cve(e.get("cve_id"))}

    # cve -> story refs (canonical only)
    story_refs = {}
    for sid, s in stories.items():
        for c in s.get("cves") or []:
            g = gate_cve(c)
            if g:
                story_refs.setdefault(g, []).append({
                    "id": sid, "title": s.get("title", ""),
                    "first_seen": s.get("first_seen", ""),
                    "score": s.get("score", 0.0),
                    "has_analysis": os.path.exists(
                        os.path.join(ANALYSIS, sid + ".md")),
                })
    for refs in story_refs.values():
        refs.sort(key=lambda r: (r["first_seen"], r["id"]))

    # cve -> flagged event refs (exploitation map, CVE-keyed)
    ev_refs = {}
    for eid, e in events.items():
        ex = e.get("exploitation") or {}
        for c, f in ex.items():
            g = gate_cve(c)
            if not g or f.get("status") not in STATUSES:
                continue
            ev_refs.setdefault(g, []).append({
                "id": eid, "date": e.get("published_at", ""),
                "source": e.get("source", ""), "title": e.get("title", ""),
                "url": e.get("url", ""), "status": f["status"],
                "evidence": f.get("evidence", ""),
            })
    for refs in ev_refs.values():
        refs.sort(key=lambda r: (r["date"], r["id"]))

    # kev per-CVE records (for the vulnerability-name column on on-KEV rows)
    kev_rec_cache = {}

    def _candidate_name(c, refs, ex_refs):
        """Best identifier for a candidate: the NVD description (a proper
        vulnerability name, never an article headline), else the earliest
        story whose title names the CVE, else the earliest EXPLOITED report
        title, else the earliest story."""
        nv = nvd.get(c) or {}
        desc = (nv.get("description") or "").strip()
        if desc:
            return desc[:180]
        cid = c.lower()
        for r in refs:
            if cid in (r["title"] or "").lower():
                return r["title"]
        if ex_refs:
            for r in ex_refs:
                if r["status"] == "exploited":
                    return r["title"] or ""
            return ex_refs[0]["title"] or ""
        return refs[0]["title"] if refs else ""

    def _kev_name(c):
        if c not in kev_rec_cache:
            p = os.path.join(KEV_REC_DIR, c + ".json")
            kev_rec_cache[c] = json.load(open(p)) if os.path.exists(p) else {}
        rec = kev_rec_cache[c]
        name = (rec.get("kev_vulnerability_name") or "").strip()
        if name:
            return name
        vendor = ((krec or {}).get("vendor_project") or "").strip()
        product = ((krec or {}).get("product") or "").strip()
        return (vendor + " " + product).strip()

    rows = {}
    for c, refs in story_refs.items():
        krec = kev_by_id.get(c)
        on_kev = krec is not None
        kev_added = (krec or {}).get("kev_date_added") or ""
        first_reported = _min_iso(*(r["first_seen"] for r in refs))
        ex_refs = ev_refs.get(c, [])
        first_exploit = _min_iso(
            *(r["date"] for r in ex_refs if r["status"] == "exploited"))
        exploit_status = None
        if any(r["status"] == "exploited" for r in ex_refs):
            exploit_status = "exploited"
        elif ex_refs:
            exploit_status = "suspected"
        disclose = ((nvd.get(c) or {}).get("published") or ""
                    or (krec or {}).get("cve_published") or "")
        rows[c] = {
            "cve": c,
            "first_reported": first_reported or "",
            "first_exploit_report": first_exploit or "",
            "disclose": (disclose or "")[:10],
            "on_kev": on_kev,
            "kev_date_added": kev_added,
            "kev_delta_days": _days_between(first_reported, kev_added),
            "exploit_to_kev_days": _days_between(first_exploit, kev_added),
            "gap_disclose_report": _days_between((disclose or "")[:10], first_reported),
            "gap_report_exploit": _days_between(first_reported, first_exploit),
            "status": "on-kev" if on_kev else "candidate",
            "exploit_status": exploit_status,
            "name": (_kev_name(c) if on_kev else
                     _candidate_name(c, refs, ev_refs.get(c, []))),
            "nvd_desc": (nvd.get(c) or {}).get("description") or "",
            "stories": refs,
            "n_stories": len(refs),
            "n_exploit_events": len(ex_refs),
            "exploit_events": ex_refs,
            "max_score": max((r["score"] for r in refs), default=0.0),
            "has_analysis": any(r["has_analysis"] for r in refs),
        }
    return rows


def candidates(rows, exploit_only=False):
    """Candidate rows (not on KEV), exploit-flagged first, newest first."""
    out = [r for r in rows.values() if not r["on_kev"]
           and (r["exploit_status"] is not None or not exploit_only)]
    out.sort(key=lambda r: (r["first_exploit_report"] or "", r["first_reported"] or ""),
             reverse=True)
    return out


def crossings(rows, days=30, today=None):
    """On-KEV CVEs we reported that crossed within the last N days (signed
    report->KEV delta; era-correct by construction — recent crossing window)."""
    if today is None:
        today = datetime.now(timezone.utc).date()
    elif isinstance(today, str):
        today = date.fromisoformat(today)
    cutoff = today - timedelta(days=days)
    out = []
    for r in rows.values():
        if not r["on_kev"] or not r["kev_date_added"]:
            continue
        try:
            added = date.fromisoformat(r["kev_date_added"])
        except ValueError:
            continue
        if added >= cutoff:
            out.append(r)
    out.sort(key=lambda r: r["kev_date_added"], reverse=True)
    return out


def flagged(rows):
    """Rows with an OBSERVED-exploitation flag — the page's inclusion gate.
    "suspected" (public PoC/exploit code) is not exploitation: CVEs with no
    first exploit report are excluded (patch-record mentions and suspected-only
    rows are clutter)."""
    return [r for r in rows.values() if r["exploit_status"] == "exploited"]


def index_rows(rows):
    """Compact rows for kev/kev-candidates-index.json (client-side table).
    ONLY CVEs with an exploitation flag — the page tracks exploitation intel,
    not patch-record mentions. on-KEV + candidate rows, view toggled client-side.
    Every field is a safe scalar."""
    out = []
    for r in flagged(rows):
        out.append({
            "id": r["cve"],
            "name": r["name"],
            "firstReported": r["first_reported"],
            "firstExploit": r["first_exploit_report"],
            "disclose": r["disclose"],
            "onKev": r["on_kev"],
            "kevAdded": r["kev_date_added"],
            "exploitToKev": r["exploit_to_kev_days"],
            "status": r["exploit_status"] or "",
            "stories": r["n_stories"],
            "score": round(r["max_score"], 1),
            "analysis": r["has_analysis"],
        })
    out.sort(key=lambda r: (r["firstExploit"] or "", r["firstReported"] or ""),
             reverse=True)
    return out


if __name__ == "__main__":
    rows = build()
    cands = candidates(rows)
    expl = [r for r in cands if r["exploit_status"] == "exploited"]
    susp = [r for r in cands if r["exploit_status"] == "suspected"]
    cross = crossings(rows)
    print(f"story CVEs: {len(rows)} | on KEV: {sum(1 for r in rows.values() if r['on_kev'])}")
    print(f"candidates: {len(cands)} (exploited {len(expl)}, suspected {len(susp)}, "
          f"unflagged {len(cands) - len(expl) - len(susp)})")
    print(f"crossings (30d): {len(cross)}")
    for r in expl[:6]:
        print(f"  {r['cve']} exploited {r['first_exploit_report'][:10]} "
              f"(reported {r['first_reported'][:10]}) | {r['stories'][0]['title'][:60]}")
