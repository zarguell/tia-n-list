"""Tia N. List — Mega Patch Tracker (/megapatch/).

Renders the monthly mega-patch releases collected by the cronman `megapatch`
job (committed data in engine/data/megapatch/). Microsoft Patch Tuesday is the
first tracker.

Page types (owner-specified):
  /megapatch/                                  dashboard: trackers, last + next
  /megapatch/microsoft-patch-tuesday/          the latest release
  /megapatch/microsoft-patch-tuesday/<slug>/   that month's release (archive)

Contract:
- Data is committed source (`engine/data/megapatch/`); this module only reads.
- The per-CVE table (~1.4k rows) is served as JSON and built client-side with
  createElement + textContent (same security contract as /kev/): no data string
  is ever interpolated into HTML.
- Every release/slug used in a path passes the shape gate; dates render '' on
  parse failure, never the raw string.
- No markup here; templates live in engine/templates/megapatch_*.html.
"""
import json
import os
import re
from datetime import datetime

try:
    from store import safe_url          # ssg.py runs with engine/ on sys.path
except ImportError:
    from engine.store import safe_url   # pytest from the repo root

ENGINE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENGINE)
DATA = os.path.join(ENGINE, "data", "megapatch")
CVE_INDEX = os.path.join(DATA, "cve-index.json")
TRACK = "microsoft-patch-tuesday"

BASE_URL = "https://zarguell.github.io/tia-n-list"
# Monthly releases are "YYYY-Mon"; Red Hat's weekly rollups are "YYYY-Www".
RELEASE_RE = re.compile(r"^\d{4}-(?:[A-Z][a-z]{2}|W\d{2})$")
TRACK_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,60}$")
SLUG_RE = re.compile(r"^(?:[a-z]{3}-\d{4}|w\d{2}-\d{4})$")
CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,7}$")

_SEV_CLASS = {"critical": "sev-crit", "important": "sev-high",
              "moderate": "sev-med", "low": "sev-low"}


def sev_class(severity):
    return _SEV_CLASS.get((severity or "").strip().lower(), "sev-low")


def gate_slug(slug):
    return slug if isinstance(slug, str) and SLUG_RE.match(slug) else None


def gate_track(track):
    return track if isinstance(track, str) and TRACK_RE.match(track) else None


def fmt_date(iso, long=False):
    """'2026-10-13' -> '13 October 2026' ('' on parse failure)."""
    try:
        d = datetime.strptime(str(iso)[:10], "%Y-%m-%d")
    except (ValueError, TypeError):
        return ""
    return d.strftime("%-d %B %Y") if long else d.strftime("%Y-%m-%d")


def pct(value):
    """EPSS percentile 0-1 -> '96th' ('' when unknown)."""
    try:
        n = float(value)
    except (TypeError, ValueError):
        return ""
    v = int(round(n * 100))
    suffix = "th" if 11 <= v % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(v % 10, "th")
    return f"{v}{suffix}"


def cvss_num(value):
    try:
        return f"{float(value):.1f}"
    except (TypeError, ValueError):
        return ""


def load_index():
    path = os.path.join(DATA, "index.json")
    try:
        with open(path) as f:
            idx = json.load(f)
    except (OSError, ValueError):
        return {"schema": 1, "vendors": []}
    if not isinstance(idx, dict):
        return {"schema": 1, "vendors": []}
    return idx


def cve_index():
    """CVE -> tracked releases (written by the megapatch job). This is the
    bidirectional join: story pages ask it "does this CVE ship in a mega
    patch?". Missing/corrupt file -> {} (fresh clone, job not run yet)."""
    try:
        with open(CVE_INDEX) as f:
            idx = json.load(f)
    except (OSError, ValueError):
        return {}
    cves = idx.get("cves") if isinstance(idx, dict) else None
    if not isinstance(cves, dict):
        return {}
    out = {}
    for cve, entries in cves.items():
        if not CVE_RE.match(str(cve)) or not isinstance(entries, list):
            continue
        clean = [e for e in entries if isinstance(e, dict) and gate_slug(e.get("slug"))]
        if clean:
            out[cve] = clean
    return out


def coverage_map(cards):
    """CVE -> story refs from the loaded story cards (newsroom coverage)."""
    out = {}
    for card in cards or []:
        ref = {"id": card.get("id", ""), "title": card.get("title", ""),
               "url": f"stories/{card.get('id', '')}/",
               "first_seen": card.get("first_seen", "")}
        cves = card.get("cves") or []
        if isinstance(cves, str):          # legacy records store the list as JSON
            try:
                cves = json.loads(cves)
            except ValueError:
                cves = []
        for cve in cves:
            cve = str(cve).upper()
            if CVE_RE.match(cve):
                out.setdefault(cve, []).append(ref)
    return out


def release_coverage(rec, cov):
    """The release's CVEs our newsroom covered, with story links (server-side;
    the client table only counts them)."""
    rows = [r for r in rec.get("rows") or [] if r.get("cve") in cov]
    rows.sort(key=lambda r: (-float(r.get("score") or 0), r["cve"]))
    return [{
        "cve": r["cve"],
        "title": r.get("title", ""),
        "family": r.get("family", ""),
        "severity": r.get("severity", ""),
        "score": r.get("score", 0),
        "stories": cov[r["cve"]][:4],
    } for r in rows]


def load_release(slug, track=None):
    slug = gate_slug(slug)
    track = gate_track(track) if track else TRACK
    if not slug or not track:
        return None
    release = release_from_slug(slug)
    if not release or not RELEASE_RE.match(release):
        return None
    path = os.path.join(DATA, track, release + ".json")
    try:
        with open(path) as f:
            rec = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(rec, dict) or not _release_ok(rec):
        return None
    return rec


def release_from_slug(slug):
    """'oct-2026' -> '2026-Oct', 'w45-2026' -> '2026-W45' (data files are keyed
    by the vendor release id)."""
    slug = gate_slug(slug)
    if not slug:
        return None
    first, year = slug.split("-")
    if first.startswith("w"):
        return f"{year}-{first.upper()}"
    return f"{year}-{first.capitalize()}"


def _release_ok(rec):
    return bool(RELEASE_RE.match(str(rec.get("release") or "")) and
                gate_slug(rec.get("slug")))


def table_rows(rec):
    """Client-table projection: only the fields the table renders."""
    keys = ("cve", "title", "family", "severity", "cvss", "epss_pct", "kev",
            "automatable", "exploited", "more_likely", "remote_unauth",
            "media", "score", "why")
    out = []
    for r in rec.get("rows") or []:
        if not CVE_RE.match(str(r.get("cve") or "")):
            continue
        row = {k: r.get(k) for k in keys}
        row["why"] = [str(x)[:80] for x in (r.get("why") or [])][:5]
        out.append(row)
    return out


def release_url(slug, track=None):
    slug = gate_slug(slug)
    track = gate_track(track) if track else TRACK
    return f"megapatch/{track}/{slug}/" if slug else f"megapatch/{track}/"


def _month_row(month, track=None):
    """Normalize one index month entry for the templates."""
    counts = month.get("counts") or {}
    tracking = month.get("tracking") or {}
    days = int(tracking.get("days") or 0)
    snaps = int(tracking.get("snapshots") or 0)
    # Display state comes from the job (it knows the release day); fall back to
    # the old booleans for indexes written before `state` existed.
    state = tracking.get("state")
    if not state:
        state = ("backfilled" if month.get("backfilled")
                 else "active" if tracking.get("active") else "closed")
    day = int(tracking.get("day") if tracking.get("day") is not None else min(snaps, days))
    return {
        "release": month.get("release", ""),
        "slug": gate_slug(month.get("slug")),
        "label": month.get("label", ""),
        "published": month.get("published", ""),
        "published_human": fmt_date(month.get("published"), long=True),
        "headline": month.get("headline", ""),
        "cve_count": counts.get("total", 0),
        "cvss": counts.get("total", 0),
        "critical": counts.get("critical", 0),
        "kev": counts.get("kev", 0),
        "backfilled": bool(month.get("backfilled")),
        "channel": month.get("channel", ""),
        "tracking_enabled": tracking.get("enabled", True) is not False,
        "state": state,
        "tracking_days": days,
        "tracking_snaps": snaps,
        "tracking_last": tracking.get("last", ""),
        "tracking_day": day,
        "tracking_active": bool(tracking.get("active")),
        "track": track or TRACK,
        "url": release_url(month.get("slug"), track),
    }


def _vendor_view(vendor):
    """Normalize one index vendor entry (months, latest, next) for templates."""
    # indexes written before multi-vendor carry no slug: they are the
    # Microsoft tracker by definition
    track = gate_track(vendor.get("slug")) or TRACK
    if not track:
        return None
    months = [_month_row(m, track) for m in (vendor.get("months") or [])
              if gate_slug(m.get("slug"))]
    months.sort(key=lambda m: m["published"], reverse=True)
    if months:
        months = months[: span_of(months)]
    latest = months[0] if months else None
    nxt = vendor.get("next") or {}
    return {
        "track": track,
        "vendor": vendor.get("vendor", ""),
        "label": vendor.get("label", ""),
        "cadence": vendor.get("cadence", ""),
        "source": vendor.get("source", ""),
        "severity_basis": vendor.get("severity_basis", ""),
        "months": months,
        "latest": latest,
        "next": nxt,
        "next_human": fmt_date(nxt.get("date"), long=True),
        "next_label": nxt.get("label", ""),
    }


def span_of(months, limit=36):
    """Cap the archive list (the page lists recent releases; data keeps all)."""
    return min(len(months), limit)


def render_site(env, write, cards=None):
    """Render /megapatch/ pages + the per-release table JSON for every
    tracker. Returns the number of releases rendered."""
    env.globals.setdefault("mp_sev_class", sev_class)
    env.globals.setdefault("mp_fmt_date", fmt_date)
    env.globals.setdefault("mp_pct", pct)
    env.globals.setdefault("mp_cvss", cvss_num)

    index = load_index()
    raw = index.get("vendors") if isinstance(index.get("vendors"), list) else []
    vendors = [v for v in (_vendor_view(x) for x in raw) if v]
    cov = coverage_map(cards)

    write("megapatch/index.html", env.get_template("megapatch_index.html").render(
        active="megapatch", mp_section="index", vendors=vendors,
        release_count=sum(len(v["months"]) for v in vendors),
        index_updated=index.get("updated_at", ""),
        og_url=site_url("megapatch/")))

    rendered = 0
    for v in vendors:
        track = v["track"]
        for m in v["months"]:
            rec = load_release(m["slug"], track)
            if not rec:
                continue
            # the client table is fetched, never inlined (security contract S2)
            write(f"megapatch/{track}/{m['slug']}.json",
                  json.dumps(table_rows(rec), ensure_ascii=True))
            view = dict(rec, coverage=release_coverage(rec, cov),
                        show_impacts=any(i.get("name") != "Unknown"
                                         for i in rec.get("impacts") or []))
            html = env.get_template("megapatch_release.html").render(
                active="megapatch", mp_section="release", mp_track=track,
                rel=view, month=m, months=v["months"], latest=v["latest"],
                vendor=v, is_latest=bool(v["latest"] and m["slug"] == v["latest"]["slug"]),
                next_release=v["next"], next_human=v["next_human"],
                og_url=site_url(release_url(m["slug"], track)))
            write(f"megapatch/{track}/{m['slug']}/index.html", html)
            rendered += 1

        if v["latest"]:
            rec = load_release(v["latest"]["slug"], track)
            if rec:
                view = dict(rec, coverage=release_coverage(rec, cov),
                            show_impacts=any(i.get("name") != "Unknown"
                                             for i in rec.get("impacts") or []))
                write(f"megapatch/{track}/index.html",
                      env.get_template("megapatch_release.html").render(
                          active="megapatch", mp_section="release", mp_track=track,
                          rel=view, month=v["latest"], months=v["months"],
                          latest=v["latest"], vendor=v, is_latest=True,
                          next_release=v["next"], next_human=v["next_human"],
                          og_url=site_url(f"megapatch/{track}/")))
    return rendered


def sitemap_entries(index=None):
    """[(path, lastmod)] for the sitemap template — every tracker."""
    index = index if index is not None else load_index()
    entries = [("megapatch/", "")]
    raw = index.get("vendors") if isinstance(index.get("vendors"), list) else []
    for vendor in raw:
        v = _vendor_view(vendor)
        if not v:
            continue
        entries.append((f"megapatch/{v['track']}/", ""))
        for m in v["months"]:
            entries.append((f"megapatch/{v['track']}/{m['slug']}/",
                            fmt_date(m["published"])))
    return entries


def site_url(path):
    return BASE_URL + "/" + path.lstrip("/")
