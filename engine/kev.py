"""Tia N. List — KEV catalog section (/kev/).

Renders the kevrichment data (kevrichment/data/) as part of the Tia site:
dashboard, per-CVE detail pages, pipeline runs, schema reference, and the
kev-index.json consumed by the dashboard's client-side table.

Security contract (2026-08-12 audit, S1-S3):
- S1: every URL rendered from data (sources_consulted, public_poc_urls,
  vendor_advisory_url) passes the http/https allowlist (store.safe_url);
  target=_blank links carry rel="noopener noreferrer".
- S2: kev-index.json is FETCHED by the page script, never inlined into a
  <script> tag; rows are built with createElement + textContent only; unknown
  enum values map to safe labels (never interpolated raw).
- S3: engine/tests/verify-kev.js asserts the above behaviorally in CI.
- CVE-ID shape gate on every path/URL construction (page paths, index rows,
  feed links, sitemap URLs).
- Date helpers return '' on parse failure, never the raw string.

No markup lives here: all HTML/XML/CSS is in templates/ (kev_index.html,
kev_cve.html, kev_pipeline.html, kev_schema.html, style.css).
"""
import glob
import json
import os
import re
import shutil
from datetime import datetime, timezone

try:
    from store import safe_url          # ssg.py runs with engine/ on sys.path
except ImportError:
    from engine.store import safe_url   # pytest from repo root imports engine.kev

ENGINE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENGINE)
KEV_DIR = os.path.normpath(os.path.join(ENGINE, "..", "kevrichment", "data"))

CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,7}$")

# Enum labels: raw data values mapped to safe display strings. Unknown values
# fall through to a fixed "unknown" label (S2: never interpolate raw enums).
_AUTO_LABEL = {"yes": "yes", "no": "no", "unknown": "unknown"}
_EXPLOIT_LABEL = {"active": "active", "unknown": "unknown", "none": "no"}
_POC_LABEL = {"yes": "yes", "no": "no", "unknown": "unknown", "unclear": "unknown"}

_BOD_TIMELINE = {
    "3_days_forensic_triage": "3 days + forensic",
    "3_days": "3 days",
    "14_days": "14 days",
    "60_days": "60 days",
    "defer_to_next_upgrade": "next upgrade",
}


# ---------------------------------------------------------------------------
# Data loading (all CVE-ID path/URL construction goes through gate_cve)
# ---------------------------------------------------------------------------

def gate_cve(cve_id):
    """Return the normalized CVE-ID if it matches the shape gate, else None."""
    if not isinstance(cve_id, str):
        return None
    c = cve_id.strip().upper()
    return c if CVE_RE.match(c) else None


def load_index():
    with open(os.path.join(KEV_DIR, "index.json")) as f:
        return json.load(f)


def kev_id_set():
    """Set of normalized CVE-IDs that have a kevrichment record (for the
    story-side cross-link join)."""
    return {gate_cve(e.get("cve_id")) for e in load_index().get("cves", [])
            if gate_cve(e.get("cve_id"))}


def load_cve(cve_id):
    c = gate_cve(cve_id)
    if not c:
        return None
    path = os.path.join(KEV_DIR, "cves", c + ".json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def load_runs():
    runs = []
    for p in sorted(glob.glob(os.path.join(KEV_DIR, "runs", "*.json"))):
        with open(p) as f:
            runs.append(json.load(f))
    return sorted(runs, key=lambda r: r.get("run_id", ""), reverse=True)


# ---------------------------------------------------------------------------
# Shaping helpers (no markup; '' on failure, never the raw input)
# ---------------------------------------------------------------------------

def fmt_date(iso):
    """YYYY-MM-DD from an ISO string; '' if unparseable/empty."""
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(str(iso).replace("Z", "+00:00")).date().isoformat()
    except (ValueError, TypeError):
        return ""


def fmt_ts(iso):
    """Readable UTC timestamp; '' if unparseable/empty."""
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00")).astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except (ValueError, TypeError):
        return ""


def label(value, mapping):
    """Safe enum label: known value mapped, everything else 'unknown'."""
    if isinstance(value, str) and value.lower() in mapping:
        return mapping[value.lower()]
    return "unknown"


def cvss_color(score):
    try:
        s = float(score)
    except (TypeError, ValueError):
        return ""
    if s >= 9.0:
        return "sev-crit"
    if s >= 7.0:
        return "sev-high"
    if s >= 4.0:
        return "sev-med"
    return "sev-low"


def timeline_label(value):
    return _BOD_TIMELINE.get(value, "")


# ---------------------------------------------------------------------------
# Index rows for the client-side table (kev-index.json)
# ---------------------------------------------------------------------------

def index_rows(index):
    """Compact rows for kev/kev-index.json. Every cve_id passes the shape gate;
    rows with a malformed id are dropped (defense in depth)."""
    rows = []
    for e in index.get("cves", []):
        c = gate_cve(e.get("cve_id"))
        if not c:
            continue
        rows.append({
            "id": c,
            "vendor": (e.get("vendor_project") or "").strip(),
            "product": (e.get("product") or "").strip(),
            "cvss": e.get("cvss_v3_base_score"),
            "auto": label(e.get("automatable"), _AUTO_LABEL),
            "exploit": label(e.get("exploitation_status"), _EXPLOIT_LABEL),
            "poc": label(e.get("public_poc_exists"), _POC_LABEL),
            "threeDay": bool(e.get("three_day_qualifying")),
            "timeline": timeline_label(e.get("timeline_if_publicly_exposed")),
            "dateAdded": fmt_date(e.get("kev_date_added")),
            "published": fmt_date(e.get("cve_published")),
        })
    return rows


# ---------------------------------------------------------------------------
# Feed items (M4: feeds/feed-kev.xml) — newest KEV additions, 90-day window
# ---------------------------------------------------------------------------

def feed_items(index, days=90, cap=100):
    """RSS items for the KEV feed: entries with a truthy kev_date_added within
    the last `days`, newest first, capped. Title/description come from the
    per-CVE records (kev_vulnerability_name / kevrichment_summary), which the
    index does not carry. Descriptions are PLAIN TEXT (feed.xml autoescapes;
    no |safe). Non-KEV (vulnrichment-scan) entries have empty kev_date_added
    and are excluded by the truthy guard."""
    from datetime import timedelta
    today = datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=days)

    items = []
    for e in index.get("cves", []):
        c = gate_cve(e.get("cve_id"))
        added = fmt_date(e.get("kev_date_added"))
        if not c or not added:
            continue  # empty kev_date_added (non-KEV scan entries) excluded here
        try:
            d = datetime.fromisoformat(added).date()
        except ValueError:
            continue
        if d < cutoff:
            continue
        rec = load_cve(c) or {}
        research = rec.get("kevrichment_research") or {}
        name = rec.get("kev_vulnerability_name") or ""
        summary = (research.get("kevrichment_summary") or "").strip()
        short = rec.get("kev_short_description") or ""
        desc = summary or short
        status = []
        if e.get("public_poc_exists") == "yes":
            status.append("PoC: yes")
        if e.get("three_day_qualifying"):
            status.append("3-day: yes")
        vendor = (e.get("vendor_project") or "").strip()
        product = (e.get("product") or "").strip()
        title = f"{c}: {name[:100]}" if name else f"{c}: {short[:100]}"
        items.append({
            "title": title,
            "link": site_url(f"kev/cves/{c}/"),
            "pub_date": rfc2822(f"{added}T00:00:00Z"),
            "iso": f"{added}T00:00:00Z",
            "description": f"{vendor} / {product} · {desc.strip()[:280]}" + (f" · {' · '.join(status)}" if status else ""),
        })
    items.sort(key=lambda i: i["iso"], reverse=True)
    for it in items:
        del it["iso"]
    return items[:cap]


def rfc2822(iso):
    from email.utils import format_datetime
    return format_datetime(datetime.fromisoformat(iso.replace("Z", "+00:00")))


def candidate_feed_items(rows=None, cap=200):
    """RSS items for the KEV-candidates feed: every CVE currently flagged as
    exploited that is not yet on the CISA KEV catalog, newest exploitation
    report first. Mirrors the /kev/candidates/ page — the LIVE candidate set,
    so an item drops out when CISA lists the CVE (page and feed entry vanish
    together). Title = CVE + vulnerability name; pub_date = the first
    exploitation report (the intel date); description is plain text (feed.xml
    autoescapes) and keeps coverage (first reported) distinct from the
    exploitation date."""
    import cve_timeline as tl_mod
    if rows is None:
        rows = tl_mod.build(today=datetime.now(timezone.utc).date())
    items = []
    for r in rows.values():
        if r["on_kev"] or r["exploit_status"] != "exploited":
            continue
        expl = (r["first_exploit_report"] or r["first_reported"] or "").strip()
        if not expl:
            continue
        name = (r.get("name") or "").strip()
        cvss = r.get("nvd_cvss") or {}
        score = cvss.get("score")
        severity = (cvss.get("severity") or "").strip()
        auto = "yes" == str((r.get("nvd_ssvc") or {}).get("automatable", "")).lower()
        bits = []
        if r.get("first_reported"):
            bits.append(f"First reported {r['first_reported'][:10]}")
        if r.get("disclose"):
            bits.append(f"Disclosed {r['disclose'][:10]}")
        if score is not None:
            try:
                score_s = f"{score:.1f}"
            except (TypeError, ValueError):
                score_s = str(score)
            bits.append(f"CVSS {score_s}" + (f" {severity}" if severity else ""))
        if auto:
            bits.append("Automatable")
        iso = f"{expl[:10]}T00:00:00Z"
        items.append({
            "title": f"{r['cve']}: {name[:100]}" if name else r["cve"],
            "link": site_url(f"kev/candidates/{r['cve']}/"),
            "pub_date": rfc2822(iso),
            "iso": iso,
            "description": " · ".join(bits),
        })
    items.sort(key=lambda i: i["iso"], reverse=True)
    for it in items:
        del it["iso"]
    return items[:cap]


def site_url(path):
    return "https://zarguell.github.io/tia-n-list/" + path.lstrip("/")


# ---------------------------------------------------------------------------
# Detail-page view shaping
# ---------------------------------------------------------------------------

def src_tag(value):
    """Normalize a provenance source field to a short tag: 'agent' for
    agent-produced research (incl. legacy 'hermes'/'hermes-agent' values),
    'deterministic' for the fallback, '' for anything else (older records
    carry URL blobs here - never render those as chips)."""
    if not isinstance(value, str):
        return ""
    v = value.strip().lower()
    if v in ("hermes", "hermes-agent", "agent", "agent-web-research",
             "automated enrichment (agent)", "research", "web_search"):
        return "agent"
    if "hermes" in v or "agent" in v:
        return "agent"
    if "deterministic" in v or "heuristic" in v:
        return "deterministic"
    return ""


def cve_view(rec, mentioned, tia_timeline=None):
    """Precompute the detail-page context from a record. All strings here are
    plain values; escaping happens in the template (autoescape).
    ``tia_timeline`` = cve_timeline row for the Tia-coverage panel, or None."""
    research = rec.get("kevrichment_research") or {}
    bod = rec.get("bod_26_04") or {}
    vuln = rec.get("vulnrichment") or {}
    meta = rec.get("research_meta") or {}
    qc = rec.get("qc_notes") or []
    c = gate_cve(rec.get("cve_id")) or ""
    sources = [u for u in (meta.get("sources_consulted") or [])
               if isinstance(u, str) and safe_url(u)]
    poc_urls = [u for u in (research.get("public_poc_urls") or [])
                if isinstance(u, str) and safe_url(u)]
    advisory = safe_url(research.get("vendor_advisory_url") or "") if isinstance(
        research.get("vendor_advisory_url"), str) else ""
    cwes = sorted({w for w in rec.get("cwe") or [] if w})

    return {
        "cve_id": c,
        "schema_version": rec.get("schema_version", ""),
        "cvss": rec.get("cvss_v3_base_score"),
        "cvss_vector": rec.get("cvss_v3_vector", ""),
        "vendor": rec.get("kev_vendor_project", ""),
        "product": rec.get("kev_product", ""),
        "vuln_name": rec.get("kev_vulnerability_name", ""),
        "date_added": fmt_date(rec.get("kev_date_added")),
        "due_date": fmt_date(rec.get("kev_due_date")),
        "required_action": rec.get("kev_required_action", ""),
        "published": fmt_date(rec.get("cve_published")),
        "kev_desc": rec.get("kev_short_description", ""),
        "nvd_desc": rec.get("nvd_description", ""),
        "cwes": cwes,
        "last_researched": fmt_ts(rec.get("last_researched") or meta.get("timestamp")),
        "wall_time": meta.get("wall_time_seconds"),
        "searches": meta.get("searches_performed"),
        "sources": sources,
        # SSVC + BOD
        "automatable": label(vuln.get("automatable"), _AUTO_LABEL),
        "tech_impact": vuln.get("technical_impact") or "unknown",
        "exploitation": label(vuln.get("exploitation_status"), _EXPLOIT_LABEL),
        "three_day": bool(bod.get("three_day_qualifying")),
        "timeline_public": timeline_label(bod.get("timeline_if_publicly_exposed")),
        "timeline_nonpublic": timeline_label(bod.get("timeline_if_not_publicly_exposed")),
        "forensic_public": bool(bod.get("requires_forensic_analysis_if_public")),
        "forensic_nonpublic": bool(bod.get("requires_forensic_analysis_if_not_public")),
        # Research
        "component": research.get("vulnerable_component", ""),
        "component_default": research.get("vulnerable_component_enabled_by_default") or "unknown",
        "component_source": src_tag(research.get("vulnerable_component_source")),
        "preconditions": research.get("preconditions_for_exploit", ""),
        "preconditions_source": src_tag(research.get("preconditions_source")),
        "delivery": research.get("delivery_mechanism", ""),
        "poc": label(research.get("public_poc_exists"), _POC_LABEL),
        "poc_urls": poc_urls,
        "advisory": advisory,
        "exploit_notes": research.get("exploit_complexity_notes", ""),
        "hunting": research.get("hunting_hypothesis", ""),
        "hunting_source": src_tag(research.get("hunting_hypothesis_source")),
        "summary": research.get("kevrichment_summary", ""),
        "qc": qc,
        "mentioned": mentioned,
        "tia_timeline": tia_timeline,
    }


# ---------------------------------------------------------------------------
# KEV candidates section (per-CVE timeline pages)
# ---------------------------------------------------------------------------

def candidate_view(row):
    """Shape a cve_timeline row for cve_timeline.html (safe scalars only)."""
    return {
        "cve": row["cve"],
        "name": row.get("name", ""),
        "exploit_status": row["exploit_status"],
        "on_kev": row["on_kev"],
        "disclose": row["disclose"] or "",
        "nvd_desc": row.get("nvd_desc", ""),
        "nvd_last_modified": row.get("nvd_last_modified", ""),
        "nvd_cvss": row.get("nvd_cvss") or {},
        "nvd_ssvc": row.get("nvd_ssvc") or {},
        "nvd_cwes": row.get("nvd_cwes") or [],
        "nvd_references": [u for u in row.get("nvd_references") or []
                           if safe_url(u)],
        "bod": row.get("bod"),
        "first_reported": row["first_reported"],
        "first_exploit_report": row["first_exploit_report"],
        "kev_date_added": row["kev_date_added"],
        "gap_disclose_report": row.get("gap_disclose_report"),
        "gap_report_exploit": row.get("gap_report_exploit"),
        "gap_exploit_kev": row.get("exploit_to_kev_days"),
        "n_stories": row["n_stories"],
        "n_exploit_events": row["n_exploit_events"],
        "stories": [{"id": s["id"], "title": s.get("title", ""),
                     "url": f"stories/{s['id']}/",
                     "has_analysis": s["has_analysis"]} for s in row["stories"]],
        "exploit_events": [{
            "date": e["date"], "source": e["source"],
            "url": e["url"] if safe_url(e["url"]) else "",
            "status": e["status"], "evidence": e["evidence"],
        } for e in row["exploit_events"]],
    }


# ---------------------------------------------------------------------------
# Site rendering
# ---------------------------------------------------------------------------

def render_site(env, write, cards):
    """Render /kev/ pages + kev-index.json. `cards` = the story cards (for the
    Mentioned-in reverse join, computed identically to the full build)."""
    env.globals.setdefault("cvss_color", cvss_color)
    env.globals.setdefault("timeline_label", timeline_label)
    index = load_index()
    rows = index_rows(index)
    total = len(rows)
    active = sum(1 for r in rows if r["exploit"] == "active")
    three_day = sum(1 for r in rows if r["threeDay"])
    automatable = sum(1 for r in rows if r["auto"] == "yes")
    generated = fmt_date(index.get("last_updated")) or ""

    # cve -> [story ids] (Mentioned-in join; story cves are CVE_RE-validated at
    # ingestion, upper-cased, so the join keys match gate_cve output)
    cve_stories = {}
    for card in cards:
        for c in card.get("cves") or []:
            g = gate_cve(c)
            if g:
                cve_stories.setdefault(g, []).append(card["id"])

    write("kev/kev-index.json", json.dumps(rows, ensure_ascii=True))

    write("kev/index.html", env.get_template("kev_index.html").render(
        active="kev", kev_section="catalog", og_url=site_url("kev/"),
        total=total, active_exploit=active, three_day=three_day,
        automatable=automatable, generated=generated))

    # Per-CVE detail pages (the record is loaded from disk per entry; rows
    # already passed the shape gate, so the id is safe for path construction)
    import cve_timeline as tl_mod
    tl_rows = tl_mod.build(today=datetime.now(timezone.utc).date())   # per-CVE timeline join for the Tia-coverage panel
    for r in rows:
        rec = load_cve(r["id"]) or {}
        if not rec:
            continue
        mentioned = [{"id": sid, "url": f"stories/{sid}/"}
                     for sid in sorted(cve_stories.get(r["id"], []))]
        v = cve_view(rec, mentioned, tl_rows.get(r["id"]))
        write(f"kev/cves/{r['id']}/index.html",
              env.get_template("kev_cve.html").render(
                  active="kev", kev_section="catalog", rec=v,
                  og_url=site_url(f"kev/cves/{r['id']}/")))

    runs = load_runs()
    run_view = []
    for run in runs:
        qc = run.get("qc_report") or {}
        by_check = qc.get("by_check") or {}
        run_view.append({
            "run_id": run.get("run_id", ""),
            "processed": run.get("cves_processed", 0),
            "skipped": run.get("cves_skipped", 0),
            "wall_time": run.get("total_wall_time_seconds", 0),
            "avg_time": run.get("avg_time_per_cve_seconds"),
            "tokens": run.get("avg_tokens_per_cve"),
            "errors": len(run.get("errors") or []),
            "qc": {"errors": qc.get("errors", 0), "warnings": qc.get("warnings", 0),
                   "infos": qc.get("infos", 0), "auto_fixed": qc.get("auto_fixed", 0),
                   "by_check": sorted(
                       ({"name": k, "errors": v.get("errors", 0),
                         "warnings": v.get("warnings", 0), "infos": v.get("infos", 0)}
                        for k, v in by_check.items()), key=lambda x: x["name"])},
        })
    write("kev/pipeline.html", env.get_template("kev_pipeline.html").render(
        active="kev", kev_section="pipeline", og_url=site_url("kev/pipeline.html"), runs=run_view))

    sample = load_cve("CVE-2023-4863") or {}
    write("kev/schema.html", env.get_template("kev_schema.html").render(
        active="kev", kev_section="schema", og_url=site_url("kev/schema.html"),
        schema_version=sample.get("schema_version", "1.0"),
        sample_json=json.dumps(sample, indent=2, ensure_ascii=True)))

    # KEV candidates section (/kev/candidates/) — deterministic per-CVE
    # timeline join: story store + exploitation flags + NVD + KEV index.
    # Candidates = CVEs we reported that the kevrichment KEV index lacks;
    # crossings = recent KEV additions we reported (the time-to-KEV tracker).
    # KEV tracking section (/kev/candidates/) — deterministic per-CVE
    # timeline join: story store + exploitation flags + NVD + KEV index.
    # The page tracks EXPLOITATION intel only: rows without an exploitation
    # flag (patch-record mentions) are excluded. Candidates = flagged CVEs
    # the kevrichment KEV index lacks; crossings = flagged KEV additions we
    # reported within 30 days (the time-to-KEV tracker, sortable in-table).
    cands = [r for r in tl_mod.flagged(tl_rows) if not r["on_kev"]]
    flagged_rows = tl_mod.flagged(tl_rows)
    crossings = tl_mod.crossings(tl_rows)
    exploited_n = len(cands)
    on_kev_n = len(flagged_rows) - len(cands)
    write("kev/candidates/kev-candidates-index.json",
          json.dumps(tl_mod.index_rows(tl_rows), ensure_ascii=True))
    write("kev/candidates/index.html",
          env.get_template("kev_candidates.html").render(
              active="kev", kev_section="candidates", og_url=site_url("kev/candidates/"),
              exploited_n=exploited_n,
              total_n=len(flagged_rows), on_kev_n=on_kev_n, crossings_n=len(crossings),
              generated=datetime.now(timezone.utc).date().isoformat()))
    for r in cands:
        v = candidate_view(r)
        write(f"kev/candidates/{r['cve']}/index.html",
              env.get_template("cve_timeline.html").render(
                  active="kev", kev_section="candidates", rec=v,
                  og_url=site_url(f"kev/candidates/{r['cve']}/")))

    # Prune stale candidate timeline pages: CVEs flagged in earlier builds but
    # no longer candidates (gate drops, attribution fixes, KEV crossings) leave
    # orphaned pages with outdated content. Keep the dashboard files; only the
    # per-CVE dirs are candidates for removal. Deterministic and idempotent —
    # a dir is removed iff its CVE is not in the current rendered set.
    cand_ids = {r["cve"] for r in cands}
    cand_out = os.path.join(ROOT, "kev", "candidates")
    for d in glob.glob(os.path.join(cand_out, "CVE-*")):
        if os.path.isdir(d) and os.path.basename(d) not in cand_ids:
            shutil.rmtree(d, ignore_errors=True)
            print(f"  kev/candidates/{os.path.basename(d)}/ (stale, removed)")

    return total


def kev_sitemap_entries(index, days=90):
    """(path, lastmod) pairs for the sitemap: section pages + CVE pages with
    kev_date_added within the last `days` (bounded), plus the KEV-candidates
    section and recently-flagged candidate timeline pages (bounded)."""
    from datetime import timedelta
    today = datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=days)
    entries = [("kev/", ""), ("kev/candidates/", ""),
               ("kev/pipeline.html", ""), ("kev/schema.html", "")]
    for e in index.get("cves", []):
        c = gate_cve(e.get("cve_id"))
        added = fmt_date(e.get("kev_date_added"))
        if not c or not added:
            continue
        try:
            d = datetime.fromisoformat(added).date()
        except ValueError:
            continue
        if d >= cutoff:
            entries.append((f"kev/cves/{c}/", added))
    try:
        import cve_timeline as tl_mod
        for r in tl_mod.build().values():
            if r["on_kev"] or not r["first_exploit_report"]:
                continue
            try:
                d = datetime.fromisoformat(r["first_exploit_report"][:10]).date()
            except ValueError:
                continue
            if d >= cutoff:
                entries.append((f"kev/candidates/{r['cve']}/",
                                r["first_exploit_report"][:10]))
    except Exception:  # noqa: BLE001 — sitemap must never break the build
        pass
    return entries
