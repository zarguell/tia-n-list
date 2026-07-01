#!/usr/bin/env python3
"""Static site generator for kevrichment — builds a searchable HTML dashboard from CVE JSON data."""

import json, os, glob, sys, html as html_mod
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

# ── Design Tokens ──────────────────────────────────────────────────────────
# Dark dashboard: Linear.app surface model + Sentry severity colors
T = {
    "bg": "#0a0b0d",
    "surface": "#131416",
    "surface_hover": "#1a1b1f",
    "surface_elevated": "#1e1f23",
    "border": "rgba(255,255,255,0.06)",
    "border_visible": "rgba(255,255,255,0.10)",
    "text_primary": "#f0f1f3",
    "text_secondary": "#9ba1a6",
    "text_muted": "#7a8087",
    "accent": "#8b80e0",
    "accent_hover": "#9d94e8",
    "red": "#f04438",
    "amber": "#f79009",
    "green": "#17b26a",
    "blue": "#53b1fd",
    "lime": "#c2ef4e",
    "font": "Inter, system-ui, -apple-system, sans-serif",
    "font_mono": "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace",
    "radius": "6px",
    "radius_card": "8px",
}

# ── HTML Templates ─────────────────────────────────────────────────────────

PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — kevrichment</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{font-size:16px;scroll-behavior:smooth}}
body{{background:{bg};color:{text_primary};font-family:{font};line-height:1.5;-webkit-font-smoothing:antialiased}}
a{{color:{accent};text-decoration:none;transition:color 150ms ease}}
a:hover{{color:{accent_hover}}}
code,.cve-id{{font-family:{font_mono};font-size:0.875em}}
a.cve-id-link{{color:inherit;text-decoration:none}}
a.cve-id-link:focus-visible{{outline:2px solid {accent};outline-offset:2px;border-radius:2px}}
::selection{{background:{accent};color:#fff}}
.container{{max-width:1280px;margin:0 auto;padding:0 16px}}
.header{{position:sticky;top:0;z-index:100;background:{bg};border-bottom:1px solid {border};backdrop-filter:blur(12px);padding:12px 0}}
.header-inner{{display:flex;align-items:center;justify-content:space-between;max-width:1280px;margin:0 auto;padding:0 16px}}
.header-title{{font-size:1.25rem;font-weight:600;color:{text_primary};display:flex;align-items:center;gap:8px}}
.header-title small{{font-size:0.75rem;font-weight:400;color:{text_muted};margin-left:8px}}
.header-ts{{font-size:0.75rem;color:{text_muted}}}
.card{{background:{surface};border:1px solid {border};border-radius:{radius_card};padding:20px;margin-bottom:16px;transition:border-color 150ms ease}}
.card:hover{{border-color:{border_visible}}}
.card-title{{font-size:1rem;font-weight:600;margin-bottom:12px;color:{text_primary};display:flex;align-items:center;gap:8px}}
.badge{{display:inline-flex;align-items:center;padding:2px 8px;border-radius:9999px;font-size:0.75rem;font-weight:500;line-height:1.4}}
.badge-sm{{padding:1px 6px;font-size:0.6875rem}}
.cvss-badge{{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;font-size:0.8125rem;font-weight:600;font-family:{font_mono};color:#fff;flex-shrink:0}}
.cvss-badge-sm{{width:28px;height:28px;font-size:0.6875rem}}
table{{width:100%;border-collapse:collapse}}
th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid {border};font-size:0.875rem}}
th{{color:{text_muted};font-weight:500;cursor:pointer;user-select:none;white-space:nowrap;position:relative}}
th:hover{{color:{text_primary}}}
th.sorted{{color:{accent}}}
th.sorted::after{{content:' ▲';font-size:0.625rem}}
th.sorted.desc::after{{content:' ▼'}}
td{{color:{text_secondary}}}
tr:hover td{{background:{surface_hover}}}
.btn{{display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:{radius};font-size:0.8125rem;font-weight:500;border:none;cursor:pointer;transition:all 150ms ease;text-decoration:none;color:{text_primary};background:{surface};border:1px solid {border}}}
.btn:hover{{background:{surface_hover};border-color:{border_visible}}}
.btn-accent{{background:{accent};border-color:{accent};color:#fff}}
.btn-accent:hover{{background:{accent_hover};border-color:{accent_hover}}}
.btn-sm{{padding:4px 10px;font-size:0.75rem}}
.chip{{display:inline-flex;align-items:center;gap:4px;padding:4px 12px;border-radius:9999px;font-size:0.75rem;font-weight:500;cursor:pointer;border:1px solid {border};background:transparent;color:{text_secondary};transition:all 150ms ease;user-select:none}}
.chip:hover{{border-color:{accent};color:{text_primary}}}
.chip.active{{background:{accent};border-color:{accent};color:#fff}}
.search-input{{width:100%;padding:10px 14px;border-radius:{radius};border:1px solid {border};background:{surface};color:{text_primary};font-size:0.875rem;font-family:{font};outline:none;transition:border-color 150ms ease}}
.search-input:focus{{border-color:{accent}}}
.search-input::placeholder{{color:{text_muted}}}
.stats-bar{{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px}}
.stat-card{{background:{surface};border:1px solid {border};border-radius:{radius_card};padding:14px 18px;flex:1;min-width:140px}}
.stat-value{{font-size:1.5rem;font-weight:600;color:{text_primary}}}
.stat-label{{font-size:0.75rem;color:{text_muted};margin-top:2px}}
.filter-bar{{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:16px}}
.filter-bar .search-wrap{{flex:1;min-width:200px}}
.pagination{{display:flex;gap:4px;align-items:center;justify-content:center;padding:16px 0}}
.page-btn{{padding:6px 12px;border-radius:{radius};font-size:0.8125rem;border:1px solid {border};background:transparent;color:{text_secondary};cursor:pointer;transition:all 150ms ease}}
.page-btn:hover{{border-color:{accent};color:{text_primary}}}
.page-btn.active{{background:{accent};border-color:{accent};color:#fff}}
.page-btn:disabled{{opacity:0.3;cursor:default}}
.footer{{text-align:center;padding:24px 0;font-size:0.75rem;color:{text_muted};border-top:1px solid {border};margin-top:32px}}
.footer a{{color:{text_muted}}}
.footer a:hover{{color:{accent}}}
h1{{font-size:1.5rem;font-weight:600;margin-bottom:4px;display:flex;align-items:center;gap:12px}}
h2{{font-size:1.125rem;font-weight:600;margin-bottom:12px;color:{text_primary}}}
.section-label{{font-size:0.6875rem;text-transform:uppercase;letter-spacing:0.05em;color:{text_muted};margin-bottom:4px}}
.field-row{{display:flex;padding:8px 0;border-bottom:1px solid {border};font-size:0.8125rem}}
.field-row:last-child{{border-bottom:none}}
.field-label{{color:{text_muted};width:180px;flex-shrink:0;font-weight:500}}
.field-value{{color:{text_secondary};word-break:break-word}}
.field-value a{{color:{accent}}}
.kv-row{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:4px}}
.expand-toggle{{color:{accent};cursor:pointer;font-size:0.8125rem;display:inline-flex;align-items:center;gap:4px}}
.expand-toggle:hover{{color:{accent_hover}}}
.expandable{{display:none;margin-top:8px}}
.expandable.open{{display:block}}
.qc-error{{border-left:3px solid {red};padding-left:12px}}
.qc-warn{{border-left:3px solid {amber};padding-left:12px}}
.qc-info{{border-left:3px solid {blue};padding-left:12px}}

/* ── CVE Detail Page ─────────────────────────────────────────── */
.cve-hero{{display:flex;align-items:center;flex-wrap:wrap;gap:12px;padding:16px 0 4px}}
.cve-hero-id{{font-family:{font_mono};font-size:1.5rem;font-weight:600}}
.cve-hero-badges{{display:flex;align-items:center;gap:6px;flex-wrap:wrap;flex:1}}
.cve-hero-meta{{font-size:0.8125rem;color:{text_muted};padding-bottom:16px;border-bottom:1px solid {border};margin-bottom:16px}}
.cve-hero-meta span{{display:inline-block}}
.cve-hero-meta .sep{{color:{border_visible};margin:0 8px}}
.cve-detail-grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}}
.cve-col{{display:flex;flex-direction:column;gap:12px}}

/* Collapsible card */
.cve-collapse{{}}
.cve-collapse-trigger{{cursor:pointer;user-select:none;display:flex;align-items:center;gap:6px}}
.cve-collapse-trigger:hover .cve-collapse-title{{color:{accent_hover}}}
.cve-collapse-title{{font-size:0.875rem;font-weight:600;color:{text_primary};transition:color 150ms ease}}
.cve-collapse-icon{{font-size:0.625rem;color:{text_muted};transition:transform 200ms ease;display:inline-flex;flex-shrink:0;width:16px;justify-content:center}}
.cve-collapse.collapsed .cve-collapse-icon{{transform:rotate(-90deg)}}
.cve-collapse.collapsed .cve-collapse-body{{display:none}}
.cve-collapse-body{{padding-top:4px}}
.cve-collapse-body .field-row:first-child{{padding-top:0}}
.cve-collapse-body .field-row:last-child{{padding-bottom:0}}

/* Hunting Hypothesis callout */
.hh-callout{{background:{accent}11;border:1px solid {accent}33;border-left:4px solid {accent};border-radius:{radius_card};padding:16px 20px;margin-bottom:0;position:relative}}
.hh-callout-label{{font-size:0.625rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:{accent};margin-bottom:6px;display:flex;align-items:center;gap:4px}}

/* Inline detail pills */
.detail-pill{{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border-radius:9999px;font-size:0.75rem;font-weight:500;background:{surface};border:1px solid {border};color:{text_secondary};line-height:1.4}}
.detail-pill.key{{border-color:{accent}44;color:{accent}}}
.detail-pill-row{{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}}

/* Tight field rows for compact layout */
.field-row-compact{{display:flex;gap:8px;padding:5px 0;border-bottom:1px solid {border};font-size:0.8125rem;align-items:baseline}}
.field-row-compact:last-child{{border-bottom:none}}
.field-row-compact .field-label{{color:{text_muted};width:130px;flex-shrink:0;font-weight:500;font-size:0.75rem}}
.field-row-compact .field-value{{color:{text_secondary};word-break:break-word;font-size:0.8125rem}}
.field-row-compact .field-value a{{color:{accent}}}

/* Source tags */
.source-badge{{font-size:0.625rem;padding:1px 5px;border-radius:4px;background:{surface_hover};color:{text_muted};margin-left:6px;white-space:nowrap}}
.source-hermes{{background:{accent}22;color:{accent}}}

@media(max-width:768px){{
  .cve-detail-grid{{grid-template-columns:1fr}}
  .cve-hero-id{{font-size:1.25rem}}
  .hh-callout{{padding:12px 14px}}
  .stats-bar{{flex-direction:column}}
  .filter-bar{{flex-direction:column}}
  .filter-bar .search-wrap{{width:100%}}
  .field-label{{width:120px}}
  td:nth-child(n+4):nth-child(-n+6),th:nth-child(n+4):nth-child(-n+6){{display:none}}
  .mobile-card{{display:block;padding:12px;background:{surface};border:1px solid {border};border-radius:{radius_card};margin-bottom:8px}}
  .mobile-card .mc-row{{display:flex;justify-content:space-between;padding:4px 0;font-size:0.8125rem}}
  .mobile-card .mc-label{{color:{text_muted}}}
  .mobile-card .mc-value{{color:{text_secondary};text-align:right}}
  table thead{{display:none}}
  table tbody tr{{display:block;padding:12px;background:{surface};border:1px solid {border};border-radius:{radius_card};margin-bottom:8px}}
  table tbody td{{display:flex;justify-content:space-between;padding:4px 0;border:none;font-size:0.8125rem}}
  table tbody td::before{{content:attr(data-label);color:{text_muted};font-weight:500;flex-shrink:0;margin-right:12px;min-width:80px}}
  table tbody td:first-child{{padding-top:0}}
  table tbody td:last-child{{padding-bottom:0}}
}}
</style>
</head>
<body>
"""

PAGE_FOOT = """
<div class="footer">
<p>kevrichment — CVE enrichment pipeline &middot; Generated {now}</p>
<p style="margin-top:4px"><a href="https://github.com/zarguell/kevrichment">GitHub</a></p>
</div>
</body>
</html>"""

NAV = """<div class="header">
<div class="header-inner">
<a href="{root}/index.html" class="header-title" style="text-decoration:none">
kevrichment <small>CVE enrichment</small>
</a>
<span class="header-ts">{ts}</span>
</div>
</div>"""

SCHEMA_HEADER = """<div style="display:flex;gap:12px;align-items:center;margin-bottom:16px;flex-wrap:wrap">
<a href="./index.html" class="btn btn-sm">&larr; Dashboard</a>
<a href="./schema.html" class="btn btn-sm btn-accent">Schema</a>
<a href="./pipeline.html" class="btn btn-sm">Pipeline</a>
</div>"""


# ── Helpers ────────────────────────────────────────────────────────────────

def esc(s):
    return html_mod.escape(str(s or ""))


def safe_url(s):
    """Escape a URL for safe use in href= attributes.

    Returns '#' for any URL whose scheme is not http/https. This prevents
    javascript:, data:, file:, and other executable schemes from reaching the
    rendered page (XSS defense for URLs sourced from upstream data).
    """
    s = str(s or "")
    if not s.strip():
        return "#"
    try:
        scheme = urlparse(s).scheme.lower()
    except (ValueError, TypeError, AttributeError):
        return "#"
    if scheme not in ("http", "https"):
        return "#"
    return html_mod.escape(s, quote=True)


def fmt_date(iso_str):
    if not iso_str:
        return ""
    try:
        d = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return d.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return str(iso_str)

def fmt_ts(iso_str):
    if not iso_str:
        return ""
    try:
        d = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return d.strftime("%Y-%m-%d %H:%M UTC")
    except (ValueError, TypeError):
        return str(iso_str)

def cvss_color(score):
    if score is None:
        return T["text_muted"]
    try:
        s = float(score)
        if s >= 9.0:
            return T["red"]
        elif s >= 7.0:
            return T["amber"]
        elif s >= 4.0:
            return T["blue"]
        else:
            return T["green"]
    except (ValueError, TypeError):
        return T["text_muted"]

def cvss_badge(score, small=False):
    if score is None:
        score_disp = "N/A"
        color = T["text_muted"]
    else:
        try:
            s = float(score)
            score_disp = f"{s:.1f}"
        except (ValueError, TypeError):
            score_disp = str(score)
        color = cvss_color(score)
    cls = "cvss-badge-sm" if small else "cvss-badge"
    return f'<span class="{cls}" style="background:{color}">{esc(score_disp)}</span>'

def severity_badge(label, color, small=False):
    cls = "badge badge-sm" if small else "badge"
    return f'<span class="{cls}" style="background:{color}22;color:{color};border:1px solid {color}44">{esc(label)}</span>'

def field_row(label, value):
    return f'<div class="field-row"><span class="field-label">{esc(label)}</span><span class="field-value">{value}</span></div>'

def card(title, content, extra_class=""):
    return f'<div class="card {extra_class}"><div class="card-title">{esc(title)}</div>{content}</div>'


# ── Data Loading ───────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent / "data"
CVE_DIR = DATA_DIR / "cves"
RUNS_DIR = DATA_DIR / "runs"
OUTPUT_DIR = Path(__file__).parent / "site"

def load_index():
    with open(DATA_DIR / "index.json") as f:
        return json.load(f)

def load_cve(cve_id):
    path = CVE_DIR / f"{cve_id}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None

def load_runs():
    runs = []
    for p in sorted(glob.glob(str(RUNS_DIR / "*.json"))):
        with open(p) as f:
            runs.append(json.load(f))
    return sorted(runs, key=lambda r: r.get("run_id", ""), reverse=True)

def safe_load_cves(index_data, limit=None):
    """Load full CVE records for all entries in the index."""
    cves = []
    entries = index_data.get("cves", [])
    if limit:
        entries = entries[:limit]
    for entry in entries:
        rec = load_cve(entry["cve_id"])
        if rec:
            cves.append(rec)
    return cves

def validate_schema():
    """Validate all CVE records against the expected schema. Exits with code 1 on failure."""
    errors = []

    try:
        index = load_index()
    except Exception as e:
        print(f"\n❌ SCHEMA VALIDATION FAILED — cannot load index.json: {e}")
        sys.exit(1)

    entries = index.get("cves", [])
    if not entries:
        print("\n❌ SCHEMA VALIDATION FAILED — no 'cves' in index.json or empty")
        sys.exit(1)

    required_fields = [
        "kev_date_added",
        "kev_vendor_project",
        "kev_product",
        "kev_short_description",
        "kev_required_action",
    ]

    for entry in entries:
        cve_id = entry.get("cve_id")
        if not cve_id:
            errors.append(("INDEX", "(entry)", "Entry missing 'cve_id'"))
            continue

        cve_path = CVE_DIR / f"{cve_id}.json"
        if not cve_path.exists():
            errors.append(("MISSING", cve_id, "CVE JSON file not found"))
            continue

        try:
            with open(cve_path) as f:
                rec = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(("PARSE", cve_id, f"Invalid JSON: {e}"))
            continue
        except Exception as e:
            errors.append(("PARSE", cve_id, f"Cannot read: {e}"))
            continue

        if "cve_id" not in rec:
            errors.append(("SCHEMA", cve_id, "Missing required 'cve_id' key"))
            continue
        if rec["cve_id"] != cve_id:
            errors.append(("SCHEMA", cve_id, f"'cve_id' value mismatch: file says '{rec['cve_id']}'"))

        if "schema_version" not in rec:
            errors.append(("SCHEMA", cve_id, "Missing 'schema_version'"))

        for field in required_fields:
            if field not in rec:
                errors.append(("SCHEMA", cve_id, f"Missing '{field}'"))

        if "id" in rec and "cve_id" in rec:
            errors.append(("LEGACY", cve_id, "Has both old 'id' and new 'cve_id' — remove 'id'"))

    if errors:
        print("\n❌ SCHEMA VALIDATION FAILED")
        print(f"   {len(errors)} error(s) found:\n")
        for category, cve_id, msg in errors:
            label = f"{cve_id:25s}" if cve_id else " " * 25
            print(f"  [{category:7s}] {label} {msg}")
        print("\nAborting build. Fix the issues above and commit the fixes.")
        sys.exit(1)

    print(f"✓ Schema validation passed: {len(entries)} CVE records OK")




# ── Page Generators ────────────────────────────────────────────────────────

def gen_dashboard(index_data):
    """Generate the main dashboard page."""
    entries = index_data.get("cves", [])
    last_updated = index_data.get("last_updated", "")
    total = index_data.get("total_cves_processed", len(entries))

    # Compute stats
    active_exploit = sum(1 for e in entries if e.get("exploitation_status") == "active")
    three_day = sum(1 for e in entries if e.get("three_day_qualifying"))
    automatable = sum(1 for e in entries if e.get("automatable") == "yes")

    # Build embedded data for client-side JS (keep it compact)
    table_data = []
    for e in entries:
        table_data.append({
            "id": e["cve_id"],
            "vendor": e.get("vendor_project", ""),
            "product": e.get("product", ""),
            "cvss": e.get("cvss_v3_base_score"),
            "auto": e.get("automatable", "unknown"),
            "exploit": e.get("exploitation_status", "unknown"),
            "poc": e.get("public_poc_exists", "unknown"),
            "threeDay": e.get("three_day_qualifying", False),
            "timeline": e.get("timeline_if_publicly_exposed", ""),
            "dateAdded": e.get("kev_date_added", ""),
            "published": e.get("cve_published", ""),
        })

    data_json = json.dumps(table_data)

    parts = [PAGE_HEAD.format(**T, title="Dashboard")]
    parts.append(NAV.format(root='.', ts=fmt_ts(last_updated) if last_updated else ""))

    parts.append('<div class="container" style="padding-top:20px">')
    parts.append(SCHEMA_HEADER)
    parts.append(f"<h1>KEV Catalog <span style=\"font-size:0.875rem;font-weight:400;color:{T['text_muted']}\">{total} CVEs</span></h1>")

    # Stats bar
    parts.append('<div class="stats-bar">')
    parts.append(f'<div class="stat-card"><div class="stat-value">{total}</div><div class="stat-label">Total CVEs</div></div>')
    parts.append(f'<div class="stat-card"><div class="stat-value" style="color:{T["red"]}">{active_exploit}</div><div class="stat-label">Active Exploitation</div></div>')
    parts.append(f'<div class="stat-card"><div class="stat-value" style="color:{T["amber"]}">{three_day}</div><div class="stat-label">3-Day Qualifying</div></div>')
    parts.append(f'<div class="stat-card"><div class="stat-value" style="color:{T["blue"]}">{automatable}</div><div class="stat-label">Automatable</div></div>')
    parts.append('</div>')

    # Filter bar
    parts.append('<div class="filter-bar">')
    parts.append('<div class="search-wrap"><input type="text" id="searchInput" class="search-input" placeholder="Search CVE ID, vendor, product\u2026"></div>')
    parts.append(f'<button class="chip active" data-filter="auto" data-value="all" onclick="toggleFilter(this,\'auto\')">All</button>')
    parts.append(f'<button class="chip" data-filter="auto" data-value="yes" onclick="toggleFilter(this,\'auto\')">Automatable</button>')
    parts.append(f'<button class="chip" data-filter="exploit" data-value="active" onclick="toggleFilter(this,\'exploit\')">Active Exploit</button>')
    parts.append(f'<button class="chip" data-filter="threeDay" data-value="true" onclick="toggleFilter(this,\'threeDay\')">3-Day</button>')
    parts.append(f'<button class="chip" data-filter="poc" data-value="yes" onclick="toggleFilter(this,\'poc\')">Has PoC</button>')
    parts.append(f'<span id="filterCount" style="font-size:0.75rem;color:{T["text_muted"]};margin-left:auto"></span>')
    parts.append('</div>')

    # Table
    parts.append(f'<div style="overflow-x:auto;border:1px solid {T["border"]};border-radius:{T["radius_card"]};background:{T["surface"]}">')
    parts.append('<table id="cveTable">')
    parts.append('<thead><tr>')
    for col in ["CVE ID", "Vendor", "Product", "CVSS", "Auto", "Exploit", "PoC", "3-Day", "Timeline", "Date Added", "Published"]:
        parts.append(f'<th onclick="sortTable(\'{col}\')" data-col="{col}">{col}</th>')
    parts.append('</tr></thead>')
    parts.append('<tbody id="cveTableBody"></tbody>')
    parts.append('</table>')
    parts.append('</div>')

    # Pagination
    parts.append('<div class="pagination" id="pagination"></div>')

    # Embedded data + client JS
    parts.append(f'<script>var CVE_DATA = {data_json};</script>')
    parts.append("""
<script>
var currentPage = 1, pageSize = 50, sortCol = 'Published', sortAsc = false;
var filters = { auto: 'all', exploit: 'all', threeDay: 'all', poc: 'all' };

function toggleFilter(btn, filter) {
  var val = btn.getAttribute('data-value');
  if (filters[filter] === val) { return; }
  filters[filter] = val;
  document.querySelectorAll('[data-filter="'+filter+'"]').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  currentPage = 1;
  renderTable();
}

function getFilteredData() {
  var q = document.getElementById('searchInput').value.toLowerCase().trim();
  var data = CVE_DATA.filter(function(row) {
    if (filters.auto !== 'all' && row.auto !== filters.auto) return false;
    if (filters.exploit !== 'all' && row.exploit !== filters.exploit) return false;
    if (filters.threeDay !== 'all' && (row.threeDay !== true)) return false;
    if (filters.poc !== 'all' && row.poc !== filters.poc) return false;
    if (q && row.id.toLowerCase().indexOf(q) === -1 && row.vendor.toLowerCase().indexOf(q) === -1 && row.product.toLowerCase().indexOf(q) === -1) return false;
    return true;
  });
  document.getElementById('filterCount').textContent = data.length + ' of ' + CVE_DATA.length + ' shown';
  return data;
}

function sortTable(col) {
  var colMap = {'CVE ID':'id','Vendor':'vendor','Product':'product','CVSS':'cvss','Auto':'auto','Exploit':'exploit','PoC':'poc','3-Day':'threeDay','Timeline':'timeline','Date Added':'dateAdded','Published':'published'};
  var key = colMap[col];
  if (!key) return;
  if (sortCol === col) { sortAsc = !sortAsc; } else {
    sortCol = col;
    sortAsc = (col === 'Date Added' || col === 'Published' || col === 'CVSS') ? false : true;
  }
  document.querySelectorAll('th').forEach(function(t) { t.classList.remove('sorted','desc'); });
  var th = document.querySelector('th[data-col="'+col+'"]');
  if (th) { th.classList.add('sorted'); if (!sortAsc) th.classList.add('desc'); }
  renderTable();
}

function renderTable() {
  var data = getFilteredData();
  // Sort
  var keyMap = {'id':'id','vendor':'vendor','product':'product','cvss':'cvss','auto':'auto','exploit':'exploit','poc':'poc','threeDay':'threeDay','timeline':'timeline','dateAdded':'dateAdded','published':'published'};
  var key = keyMap[sortCol] || 'id';
  data.sort(function(a,b) {
    var av = a[key], bv = b[key];
    if (key === 'cvss') { av = av || 0; bv = bv || 0; }
    if (typeof av === 'string') av = av.toLowerCase();
    if (typeof bv === 'string') bv = bv.toLowerCase();
    if (av < bv) return sortAsc ? -1 : 1;
    if (av > bv) return sortAsc ? 1 : -1;
    return 0;
  });

  // Paginate
  var start = (currentPage - 1) * pageSize;
  var page = data.slice(start, start + pageSize);
  var totalPages = Math.ceil(data.length / pageSize) || 1;

  var tbody = document.getElementById('cveTableBody');
  tbody.innerHTML = '';
  page.forEach(function(r) {
    var cvssColor = '#7a8087';
    var cvssDisp = 'N/A';
    if (r.cvss !== null && r.cvss !== undefined) {
      var s = parseFloat(r.cvss);
      cvssDisp = s.toFixed(1);
      if (s >= 9.0) cvssColor = '#f04438';
      else if (s >= 7.0) cvssColor = '#f79009';
      else if (s >= 4.0) cvssColor = '#53b1fd';
      else cvssColor = '#17b26a';
    }
    var threeD = r.threeDay ? '<span style="color:#f04438;font-weight:600">YES</span>' : '<span style="color:#7a8087">no</span>';
    var tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.addEventListener('click', function() { window.location.href = 'cves/' + r.id + '.html'; });
    tr.innerHTML = '<td data-label="CVE ID"><a href="cves/' + r.id + '.html" class="cve-id-link"><code class="cve-id">' + esc(r.id) + '</code></a></td>'
      + '<td data-label="Vendor">' + esc(r.vendor) + '</td>'
      + '<td data-label="Product">' + esc(r.product) + '</td>'
      + '<td data-label="CVSS"><span style="display:inline-flex;align-items:center;gap:6px"><span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:' + cvssColor + ';color:#fff;text-align:center;line-height:28px;font-size:0.6875rem;font-weight:600;font-family:JetBrains Mono,monospace">' + cvssDisp + '</span></span></td>'
      + '<td data-label="Auto">' + severityBadge(r.auto) + '</td>'
      + '<td data-label="Exploit">' + severityBadge(r.exploit) + '</td>'
      + '<td data-label="PoC">' + pocBadge(r.poc) + '</td>'
      + '<td data-label="3-Day" style="text-align:center">' + threeD + '</td>'
      + '<td data-label="Timeline">' + esc(r.timeline.replace(/_/g,' ')) + '</td>'
      + '<td data-label="Date Added">' + fmtDate(r.dateAdded) + '</td>'
      + '<td data-label="Published">' + fmtDate(r.published) + '</td>';
    tbody.appendChild(tr);
  });

  // Pagination buttons
  var pg = document.getElementById('pagination');
  pg.innerHTML = '';
  pg.appendChild(createPageBtn('\u00ab', 1, currentPage === 1));
  pg.appendChild(createPageBtn('\u2039', Math.max(1, currentPage-1), currentPage === 1));
  var startP = Math.max(1, currentPage - 2);
  var endP = Math.min(totalPages, currentPage + 2);
  for (var i = startP; i <= endP; i++) {
    pg.appendChild(createPageBtn(i, i, currentPage === i));
  }
  pg.appendChild(createPageBtn('\u203a', Math.min(totalPages, currentPage+1), currentPage === totalPages));
  pg.appendChild(createPageBtn('\u00bb', totalPages, currentPage === totalPages));
}

function createPageBtn(label, page, disabled) {
  var btn = document.createElement('button');
  btn.className = 'page-btn' + (disabled && typeof label === 'number' ? ' active' : '');
  btn.textContent = label;
  btn.disabled = disabled && typeof label !== 'number';
  if (!disabled || typeof label === 'number') {
    btn.addEventListener('click', function() { currentPage = page; renderTable(); });
  }
  return btn;
}

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function fmtDate(d) {
  if (!d) return '<span style="color:#7a8087">\u2014</span>';
  return esc(d.substring(0,10));
}
function severityBadge(v) {
  if (v === 'yes') return '<span class="badge badge-sm" style="background:#f0443822;color:#f04438;border:1px solid #f0443844">yes</span>';
  if (v === 'active') return '<span class="badge badge-sm" style="background:#f0443822;color:#f04438;border:1px solid #f0443844">active</span>';
  return '<span class="badge badge-sm" style="background:#7a808722;color:#9ba1a6;border:1px solid #7a808744">'+v+'</span>';
}
function pocBadge(v) {
  if (v === 'yes') return '<span class="badge badge-sm" style="background:#f7900922;color:#f79009;border:1px solid #f7900944">yes</span>';
  if (v === 'no') return '<span class="badge badge-sm" style="background:#17b26a22;color:#17b26a;border:1px solid #17b26a44">no</span>';
  return '<span class="badge badge-sm" style="background:#7a808722;color:#9ba1a6;border:1px solid #7a808744">'+v+'</span>';
}
document.addEventListener('DOMContentLoaded', function() {
  renderTable();
  document.getElementById('searchInput').addEventListener('input', function() { currentPage = 1; renderTable(); });
});
</script>""")

    parts.append('</div>')  # close container
    parts.append(PAGE_FOOT.format(now=fmt_ts(last_updated) if last_updated else ""))
    return "\n".join(parts)


def _collapse_card(title, body, collapsed=True):
    """A card with collapsible body. Click title to toggle."""
    state = " collapsed" if collapsed else ""
    return (f'<div class="card cve-collapse{state}">'
            f'<div class="cve-collapse-trigger card-title" onclick="this.parentElement.classList.toggle(&apos;collapsed&apos;)">'
            f'<span class="cve-collapse-icon">&#9660;</span>'
            f'<span class="cve-collapse-title">{esc(title)}</span>'
            f'</div>'
            f'<div class="cve-collapse-body">{body}</div>'
            f'</div>')

def _compact_row(label, value):
    return f'<div class="field-row-compact"><span class="field-label">{esc(label)}</span><span class="field-value">{value}</span></div>'

def _detail_pill(label, color="default"):
    c = T["accent"] if color == "key" else T["text_secondary"]
    bd = f'{T["accent"]}44' if color == "key" else T["border"]
    return f'<span class="detail-pill{" key" if color == "key" else ""}">{esc(label)}</span>'

def gen_cve_detail(cve_record):
    """Generate a per-CVE detail page with two-column layout and collapsible sections."""
    c = cve_record
    cve_id = c["cve_id"]
    research = c.get("kevrichment_research", {})
    bod = c.get("bod_26_04", {})
    vuln = c.get("vulnrichment", {})
    meta = c.get("research_meta", {})
    qc = c.get("qc_notes", [])

    parts = [PAGE_HEAD.format(**T, title=cve_id)]
    parts.append(NAV.format(root='..', ts=""))

    parts.append('<div class="container" style="padding-top:12px">')
    parts.append('<a href="../index.html" class="btn btn-sm" style="margin-bottom:8px">&larr; Dashboard</a>')

    # ── Hero strip ────────────────────────────────────────────────────────
    cvss = c.get("cvss_v3_base_score")
    parts.append('<div class="cve-hero">')
    parts.append(f'<span class="cve-hero-id"><code>{esc(cve_id)}</code></span>')
    if cvss is not None:
        parts.append(cvss_badge(cvss, small=False))
    parts.append('<span class="cve-hero-badges">')
    if bod.get("three_day_qualifying"):
        parts.append(f'<span class="badge" style="background:{T["red"]};color:#fff">3-Day Required</span>')
    if research.get("public_poc_exists") == "yes":
        parts.append(f'<span class="badge" style="background:{T["amber"]};color:#000">PoC Available</span>')
    if c.get("kev_date_added"):
        parts.append(f'<span class="badge" style="background:{T["lime"]}22;color:{T["lime"]};border:1px solid {T["lime"]}44">KEV</span>')
    auto = vuln.get("automatable", "")
    if auto == "yes":
        parts.append(f'<span class="badge" style="background:{T["red"]}22;color:{T["red"]};border:1px solid {T["red"]}44">Automatable</span>')
    expl = vuln.get("exploitation_status", "")
    if expl == "active":
        parts.append(f'<span class="badge" style="background:{T["red"]}22;color:{T["red"]};border:1px solid {T["red"]}44">Active Exploitation</span>')
    parts.append('</span>')
    parts.append('</div>')  # cve-hero

    # Meta line
    parts.append('<div class="cve-hero-meta">')
    parts.append(f'<span>{esc(c.get("kev_vendor_project", ""))}</span>')
    parts.append(f'<span class="sep">&middot;</span>')
    parts.append(f'<span>{esc(c.get("kev_product", ""))}</span>')
    parts.append(f'<span class="sep">&middot;</span>')
    parts.append(f'<span>Added {fmt_date(c.get("kev_date_added", ""))}</span>')
    pub = c.get("cve_published", "")
    if pub:
        parts.append(f'<span class="sep">&middot;</span>')
        parts.append(f'<span>Published {fmt_date(pub)}</span>')
    parts.append('</div>')

    # ── Two-column grid ───────────────────────────────────────────────────
    parts.append('<div class="cve-detail-grid">')

    # ========================= LEFT COLUMN ================================
    parts.append('<div class="cve-col">')

    # --- KEV + NVD (combined, collapsed) ---
    kn_rows = _compact_row("Vendor", esc(c.get("kev_vendor_project", "")))
    kn_rows += _compact_row("Product", esc(c.get("kev_product", "")))
    kn_rows += _compact_row("Vulnerability Name", esc(c.get("kev_vulnerability_name", "")))
    kn_rows += _compact_row("Date Added", fmt_date(c.get("kev_date_added", "")))
    kn_rows += _compact_row("Due Date", fmt_date(c.get("kev_due_date", "")))
    kn_rows += _compact_row("Required Action", esc(c.get("kev_required_action", "")))
    cwe_list = c.get("cwe", [])
    if cwe_list:
        cwe_badges = " ".join(f'<span class="badge badge-sm" style="background:{T["blue"]}22;color:{T["blue"]};border:1px solid {T["blue"]}44">{esc(w)}</span>' for w in set(cwe_list))
    else:
        cwe_badges = '<span style="color:' + T["text_muted"] + '">none</span>'
    kn_rows += _compact_row("CWE", cwe_badges)
    kn_rows += _compact_row("Published", fmt_date(c.get("cve_published", "")))
    vector = c.get("cvss_v3_vector", "")
    if vector:
        kn_rows += _compact_row("CVSS Vector", f'<code style="font-size:0.7rem">{esc(vector[:80])}</code>')
    # Collapsible long description
    kev_desc = c.get("kev_short_description", "")
    nvd_desc = c.get("nvd_description", "")
    desc_body = ""
    if kev_desc:
        desc_body += _compact_row("KEV Description", esc(kev_desc))
    if nvd_desc:
        desc_body += _compact_row("NVD Description", esc(nvd_desc))
    if desc_body:
        kn_rows += f'<div class="cve-collapse collapsed" style="margin-top:2px">'
        kn_rows += f'<div class="cve-collapse-trigger" onclick="this.parentElement.classList.toggle(\'collapsed\')" style="display:flex;align-items:center;gap:4px;padding:4px 0;cursor:pointer">'
        kn_rows += f'<span class="cve-collapse-icon">&#9660;</span>'
        kn_rows += f'<span class="cve-collapse-title" style="font-size:0.75rem;color:{T["text_muted"]}">Descriptions</span>'
        kn_rows += f'</div><div class="cve-collapse-body" style="padding-top:2px">{desc_body}</div></div>'
    parts.append(_collapse_card("Details", kn_rows, collapsed=False))

    # --- Compliance (Vulnrichment + BOD 26-04, collapsed) ---
    comp_rows = ""
    for k in ["automatable", "technical_impact", "exploitation_status"]:
        v = vuln.get(k, "unknown")
        color = T["red"] if v == "active" or v == "yes" or v == "total" else T["green"] if v == "no" else T["text_muted"]
        comp_rows += _compact_row(k.replace("_", " ").title(), severity_badge(v, color, small=True))
    comp_rows += _compact_row("3-Day Qualifying", "Yes" if bod.get("three_day_qualifying") else "No")
    comp_rows += _compact_row("Public Timeline", esc(bod.get("timeline_if_publicly_exposed", "").replace("_", " ")))
    comp_rows += _compact_row("Non-Public Timeline", esc(bod.get("timeline_if_not_publicly_exposed", "").replace("_", " ")))
    comp_rows += _compact_row("Forensic (Public)", "Required" if bod.get("requires_forensic_analysis_if_public") else "Not required")
    comp_rows += _compact_row("Forensic (Non-Public)", "Required" if bod.get("requires_forensic_analysis_if_not_public") else "Not required")
    parts.append(_collapse_card("Compliance (SSVC + BOD 26-04)", comp_rows, collapsed=True))

    # --- Research Metadata (collapsed) ---
    meta_rows = ""
    meta_rows += _compact_row("Last Researched", fmt_ts(meta.get("timestamp", "")))
    meta_rows += _compact_row("Wall Time", f'{meta.get("wall_time_seconds", 0)}s')
    meta_rows += _compact_row("Searches", str(meta.get("searches_performed", 0)))
    meta_rows += _compact_row("Component Default", esc(research.get("vulnerable_component_enabled_by_default", "unknown")))
    sources = meta.get("sources_consulted", [])
    if sources:
        src_links = "<br>".join(f'<a href="{safe_url(s)}" target="_blank" rel="noopener" style="font-size:0.75rem">{esc(s)}</a>' for s in sources if s)
        meta_rows += _compact_row("Sources", src_links)
    parts.append(_collapse_card("Research Metadata", meta_rows, collapsed=True))

    # QC notes (if any)
    if qc:
        qc_rows = ""
        for n in qc:
            sev = n.get("severity", "info")
            css_class = "qc-error" if sev == "error" else "qc-warn" if sev == "warn" else "qc-info"
            qc_rows += f'<div class="{css_class}" style="padding:5px 0;font-size:0.75rem;color:{T["text_secondary"]}">'
            qc_rows += f'<span class="badge badge-sm" style="background:{T["red"] if sev == "error" else T["amber"] if sev == "warn" else T["blue"]}22;color:{T["red"] if sev == "error" else T["amber"] if sev == "warn" else T["blue"]};border:1px solid {T["red"] if sev == "error" else T["amber"] if sev == "warn" else T["blue"]}44">{esc(sev)}</span> '
            qc_rows += f'<strong>{esc(n.get("check", ""))}:</strong> {esc(n.get("detail", ""))}'
            if n.get("auto_fixed"):
                qc_rows += ' <span style="color:' + T["green"] + '">(auto-fixed)</span>'
            qc_rows += '</div>'
        parts.append(f'<div class="card"><div class="card-title" style="font-size:0.875rem">QC Notes</div>{qc_rows}</div>')

    parts.append('</div>')  # left col

    # ========================= RIGHT COLUMN ================================
    parts.append('<div class="cve-col">')

    # --- Hunting Hypothesis (always visible, callout) ---
    hh = research.get("hunting_hypothesis", "")
    if hh:
        hh_source = research.get("hunting_hypothesis_source", "")
        source_tag = f'<span class="source-badge {"source-hermes" if hh_source == "hermes" else ""}">{esc(hh_source)}</span>' if hh_source else ''
        parts.append('<div class="hh-callout">'
                     f'<div class="hh-callout-label">&#127919; Hunting Hypothesis{source_tag}</div>'
                     f'<div style="font-size:0.875rem;line-height:1.6;color:{T["text_primary"]}">{esc(hh)}</div>'
                     '</div>')

    # --- Research Details (preconditions collapsible) ---
    rd_rows = ""
    comp = research.get("vulnerable_component", "")
    if comp:
        rd_rows += _compact_row("Component", esc(comp))
        # Source tag inline
        comp_src = research.get("vulnerable_component_source", "")
        if comp_src:
            rd_rows = rd_rows.replace('</span></div>', f'</span><span class="source-badge {"source-hermes" if comp_src == "hermes" else ""}">{esc(comp_src)}</span></div>')

    # Preconditions (collapsible if > 200 chars)
    pre = research.get("preconditions_for_exploit", "")
    if pre:
        if len(pre) > 200:
            pre_id = f"pre_{cve_id.replace('-','_')}"
            rd_rows += f'<div class="field-row-compact"><span class="field-label">Preconditions</span><span class="field-value">'
            rd_rows += f'<span id="{pre_id}short">{esc(pre[:180])}&hellip;</span>'
            rd_rows += f'<span id="{pre_id}full" style="display:none">{esc(pre)}</span>'
            rd_rows += f' <span class="expand-toggle" onclick="document.getElementById(\'{pre_id}full\').style.display=\'inline\';document.getElementById(\'{pre_id}short\').style.display=\'none\';this.style.display=\'none\'">show more</span>'
            rd_rows += f'</span></div>'
            # source
            pre_src = research.get("preconditions_source", "")
            if pre_src:
                rd_rows = rd_rows.replace('</span></div>', f'</span><span class="source-badge {"source-hermes" if pre_src == "hermes" else ""}">{esc(pre_src)}</span></div>')
        else:
            rd_rows += _compact_row("Preconditions", esc(pre))
            pre_src = research.get("preconditions_source", "")
            if pre_src:
                rd_rows = rd_rows.replace('</span></div>', f'</span><span class="source-badge {"source-hermes" if pre_src == "hermes" else ""}">{esc(pre_src)}</span></div>')

    delivery = research.get("delivery_mechanism", "")
    if delivery:
        if len(delivery) > 200:
            del_id = f"del_{cve_id.replace('-','_')}"
            rd_rows += f'<div class="field-row-compact"><span class="field-label">Delivery</span><span class="field-value">'
            rd_rows += f'<span id="{del_id}short">{esc(delivery[:180])}&hellip;</span>'
            rd_rows += f'<span id="{del_id}full" style="display:none">{esc(delivery)}</span>'
            rd_rows += f' <span class="expand-toggle" onclick="document.getElementById(\'{del_id}full\').style.display=\'inline\';document.getElementById(\'{del_id}short\').style.display=\'none\';this.style.display=\'none\'">show more</span>'
            rd_rows += f'</span></div>'
        else:
            rd_rows += _compact_row("Delivery", esc(delivery))

    poc = research.get("public_poc_exists", "unknown")
    poc_urls = research.get("public_poc_urls", [])
    poc_color = T["green"] if poc == "yes" else T["text_muted"] if poc == "no" else T["amber"]
    rd_rows += _compact_row("Public PoC", severity_badge(poc, poc_color, small=True))
    if poc_urls:
        url_links = "<br>".join(f'<a href="{safe_url(u)}" target="_blank" rel="noopener" style="font-size:0.75rem">{esc(u)}</a>' for u in poc_urls if u)
        rd_rows += _compact_row("PoC URLs", url_links)

    advisory = research.get("vendor_advisory_url", "")
    if advisory:
        rd_rows += _compact_row("Advisory", f'<a href="{safe_url(advisory)}" target="_blank" rel="noopener" style="font-size:0.75rem">{esc(advisory)}</a>')

    expl_notes = research.get("exploit_complexity_notes", "")
    if expl_notes:
        rd_rows += _compact_row("Exploit Notes", esc(expl_notes))

    parts.append(_collapse_card("Research Details", rd_rows, collapsed=False))

    # --- Summary (collapsed) ---
    summary = research.get("kevrichment_summary", "")
    if summary:
        parts.append(_collapse_card("Summary", f'<div style="font-size:0.8125rem;line-height:1.6;color:{T["text_secondary"]};padding:4px 0">{esc(summary)}</div>', collapsed=True))

    parts.append('</div>')  # right col
    parts.append('</div>')  # cve-detail-grid

    parts.append('</div>')  # container
    parts.append(PAGE_FOOT.format(now=""))
    return "\n".join(parts)


def gen_schema_page():
    """Generate the schema reference page with example from a sample CVE."""
    # Load sample CVE for example display
    sample = load_cve("CVE-2023-4863")
    sample_json = json.dumps(sample, indent=2) if sample else "{}"

    sections = [
        ("Top-Level", [
            ("schema_version", "string", "Schema version identifier", "kevrichment"),
            ("cve_id", "string", "CVE identifier (CVE-YYYY-NNNNN)", "KEV"),
            ("cve_published", "ISO 8601", "When the CVE was published by NVD", "NVD"),
            ("last_researched", "ISO 8601", "When this record was last enriched", "kevrichment"),
        ]),
        ("KEV Catalog Fields", [
            ("kev_date_added", "date", "When CISA added this to KEV", "CISA KEV"),
            ("kev_vendor_project", "string", "Vendor/project name", "CISA KEV"),
            ("kev_product", "string", "Product name", "CISA KEV"),
            ("kev_short_description", "string", "CISA's short vulnerability description", "CISA KEV"),
            ("kev_required_action", "string", "Required remediation action per CISA", "CISA KEV"),
            ("kev_due_date", "date", "CISA-assigned remediation due date", "CISA KEV"),
            ("kev_vulnerability_name", "string", "Formal vulnerability name", "CISA KEV"),
        ]),
        ("NVD Fields", [
            ("nvd_description", "string", "EN-language description from NVD", "NVD"),
            ("cwe", "string[]", "CWE weakness identifiers", "NVD"),
            ("cvss_v3_base_score", "float (0-10)", "CVSS v3 base score", "NVD"),
            ("cvss_v3_vector", "string", "Full CVSS v3 vector string", "NVD"),
            ("cpe_affected", "string[]", "Affected CPE URIs", "NVD"),
        ]),
        ("Vulnrichment (SSVC)", [
            ("vulnrichment.automatable", "'yes' | 'no' | 'unknown'", "Whether exploitation can be automated per SSVC", "CISA Vulnrichment"),
            ("vulnrichment.technical_impact", "'total' | 'partial' | 'unknown'", "SSVC technical impact assessment", "CISA Vulnrichment"),
            ("vulnrichment.exploitation_status", "'active' | 'unknown'", "Whether exploitation has been detected", "CISA Vulnrichment"),
        ]),
        ("BOD 26-04 Timeline", [
            ("bod_26_04.timeline_if_publicly_exposed", "string", "Remediation timeline for internet-facing assets", "kevrichment"),
            ("bod_26_04.timeline_if_not_publicly_exposed", "string", "Remediation timeline for internal assets", "kevrichment"),
            ("bod_26_04.three_day_qualifying", "bool", "All BOD 26-04 risk factors present", "kevrichment"),
            ("bod_26_04.requires_forensic_analysis_if_public", "bool", "Forensic triage required (public assets)", "kevrichment"),
        ]),
        ("kevrichment Research", [
            ("kevrichment_research.vulnerable_component", "string", "Specific component/feature affected", "Research"),
            ("vulnerable_component_enabled_by_default", "'yes' | 'no' | 'unknown'", "Whether component is default-enabled", "Research"),
            ("delivery_mechanism", "string", "How attacker delivers the exploit", "Research"),
            ("preconditions_for_exploit", "string", "Deployment conditions needed for exploitation", "Hermes AI / Deterministic"),
            ("public_poc_exists", "'yes' | 'no' | 'unknown'", "Whether public exploit/PoC was found", "Research"),
            ("public_poc_urls", "string[]", "URLs to discovered PoC repositories", "Research"),
            ("vendor_advisory_url", "string", "Link to vendor security advisory", "Research"),
            ("hunting_hypothesis", "string", "Specific attacker behavior/TTP to monitor for", "Hermes AI / Deterministic"),
            ("kevrichment_summary", "string", "One-line summary of findings", "Research"),
        ]),
        ("Research Metadata", [
            ("research_meta.timestamp", "ISO 8601", "When research was performed", "kevrichment"),
            ("research_meta.wall_time_seconds", "float", "Elapsed research time", "kevrichment"),
            ("research_meta.searches_performed", "int", "Number of web searches", "kevrichment"),
            ("research_meta.sources_consulted", "string[]", "URLs visited during research", "kevrichment"),
        ]),
        ("QC Notes", [
            ("qc_notes[].severity", "'error' | 'warn' | 'info'", "QC check severity", "kevrichment"),
            ("qc_notes[].check", "string", "QC check identifier", "kevrichment"),
            ("qc_notes[].field", "string", "JSON path to affected field", "kevrichment"),
            ("qc_notes[].detail", "string", "Human-readable QC finding", "kevrichment"),
            ("qc_notes[].auto_fixed", "bool", "Whether issue was auto-corrected", "kevrichment"),
        ]),
    ]

    parts = [PAGE_HEAD.format(**T, title="Schema")]
    parts.append(NAV.format(root='.', ts=""))
    parts.append('<div class="container" style="padding-top:20px">')
    parts.append('<a href="./index.html" class="btn btn-sm" style="margin-bottom:16px">&larr; Dashboard</a>')
    parts.append("<h1>Schema Reference</h1>")
    parts.append(f'<p style="color:{T["text_muted"]};font-size:0.875rem;margin-bottom:20px">Full field reference for the kevrichment CVE enrichment schema. Version {sample.get("schema_version", "1.0") if sample else "1.0"}.</p>')

    for section_name, fields in sections:
        rows = ""
        for name, ftype, desc, source in fields:
            rows += "<tr>"
            rows += f'<td style="padding:8px 12px;border-bottom:1px solid {T["border"]};font-family:{T["font_mono"]};font-size:0.8125rem;color:{T["text_primary"]}">{esc(name)}</td>'
            rows += f'<td style="padding:8px 12px;border-bottom:1px solid {T["border"]};font-size:0.8125rem;color:{T["text_secondary"]}">{esc(ftype)}</td>'
            rows += f'<td style="padding:8px 12px;border-bottom:1px solid {T["border"]};font-size:0.8125rem;color:{T["text_secondary"]}">{esc(desc)}</td>'
            rows += f'<td style="padding:8px 12px;border-bottom:1px solid {T["border"]};font-size:0.8125rem">{severity_badge(source, T["accent"] if "Hermes" in source else T["blue"] if source != "kevrichment" else T["text_muted"], small=True)}</td>'
            rows += "</tr>"

        parts.append(f'<div class="card"><div class="card-title">{esc(section_name)}</div>')
        parts.append(f'<table style="width:100%"><thead><tr>')
        parts.append(f'<th style="color:{T["text_muted"]};font-weight:500;font-size:0.75rem;text-transform:uppercase;padding:8px 12px">Field</th>')
        parts.append(f'<th style="color:{T["text_muted"]};font-weight:500;font-size:0.75rem;text-transform:uppercase;padding:8px 12px">Type</th>')
        parts.append(f'<th style="color:{T["text_muted"]};font-weight:500;font-size:0.75rem;text-transform:uppercase;padding:8px 12px">Description</th>')
        parts.append(f'<th style="color:{T["text_muted"]};font-weight:500;font-size:0.75rem;text-transform:uppercase;padding:8px 12px">Source</th>')
        parts.append(f'</tr></thead><tbody>{rows}</tbody></table></div>')

    # Example JSON
    parts.append(f'<div class="card"><div class="card-title" style="cursor:pointer" onclick="this.nextElementSibling.classList.toggle(\'open\')">Sample CVE Record <span style="font-size:0.75rem;color:{T["text_muted"]}">(click to expand)</span></div>')
    parts.append(f'<pre class="expandable open" style="font-family:{T["font_mono"]};font-size:0.75rem;color:{T["text_secondary"]};overflow-x:auto;padding:12px;background:{T["bg"]};border-radius:{T["radius"]};line-height:1.4">{esc(sample_json)}</pre>')
    parts.append('</div>')

    parts.append('</div>')
    parts.append(PAGE_FOOT.format(now=""))
    return "\n".join(parts)


def gen_pipeline_page():
    """Generate the pipeline runs history page."""
    runs = load_runs()
    parts = [PAGE_HEAD.format(**T, title="Pipeline")]
    parts.append(NAV.format(root='.', ts=""))
    parts.append('<div class="container" style="padding-top:20px">')
    parts.append('<a href="./index.html" class="btn btn-sm" style="margin-bottom:16px">&larr; Dashboard</a>')
    parts.append("<h1>Pipeline Runs</h1>")
    parts.append(f'<p style="color:{T["text_muted"]};font-size:0.875rem;margin-bottom:20px">{len(runs)} runs recorded.</p>')

    if runs:
        parts.append(f'<div style="overflow-x:auto;border:1px solid {T["border"]};border-radius:{T["radius_card"]};background:{T["surface"]}">')
        parts.append('<table>')
        parts.append(f'<thead><tr>')
        for h in ["Run ID", "CVEs Proc.", "Time", "Avg/CVE", "Tokens", "Errors", "Health"]:
            parts.append(f'<th style="padding:10px 12px;font-size:0.75rem;text-transform:uppercase">{h}</th>')
        parts.append('</tr></thead><tbody>')

        for r in runs:
            err_count = len(r.get("errors", []))
            health = T["green"] if err_count == 0 else T["red"]
            health_label = "OK" if err_count == 0 else f"{err_count} errors"
            parts.append("<tr>")
            parts.append(f'<td style="padding:10px 12px;font-size:0.8125rem"><code>{esc(r.get("run_id", ""))}</code></td>')
            parts.append(f'<td style="padding:10px 12px;font-size:0.8125rem">{r.get("cves_processed", 0)}</td>')
            parts.append(f'<td style="padding:10px 12px;font-size:0.8125rem">{r.get("total_wall_time_seconds", 0)}s</td>')
            parts.append(f'<td style="padding:10px 12px;font-size:0.8125rem">{r.get("avg_time_per_cve_seconds", "-")}s</td>')
            parts.append(f'<td style="padding:10px 12px;font-size:0.8125rem">{r.get("avg_tokens_per_cve", "-") or "-"}</td>')
            parts.append(f'<td style="padding:10px 12px;font-size:0.8125rem">{err_count}</td>')
            parts.append(f'<td style="padding:10px 12px;font-size:0.8125rem">{severity_badge(health_label, health, small=True)}</td>')
            parts.append("</tr>")

            # QC summary sub-row
            qc = r.get("qc_report", {})
            if qc:
                parts.append("<tr>")
                parts.append(f'<td colspan="7" style="padding:4px 12px 10px 24px;font-size:0.75rem;color:{T["text_muted"]}">')
                by_check = qc.get("by_check", {})
                check_parts = []
                for check_name, check_stats in by_check.items():
                    counts = f'E:{check_stats.get("errors",0)} W:{check_stats.get("warnings",0)} I:{check_stats.get("infos",0)}'
                    check_parts.append(f'{esc(check_name)} ({counts})')
                if check_parts:
                    parts.append("QC: " + " | ".join(check_parts))
                parts.append("</td></tr>")

        parts.append("</tbody></table></div>")

    # QC summary across all runs
    parts.append('<div style="margin-top:24px"><h2>Data Quality Overview</h2></div>')
    total_qc = {"errors": 0, "warnings": 0, "infos": 0, "auto_fixed": 0}
    for r in runs:
        qc = r.get("qc_report", {})
        total_qc["errors"] += qc.get("errors", 0) if isinstance(qc.get("errors"), int) else 0
        total_qc["warnings"] += qc.get("warnings", 0) if isinstance(qc.get("warnings"), int) else 0
        total_qc["infos"] += qc.get("infos", 0) if isinstance(qc.get("infos"), int) else 0
        total_qc["auto_fixed"] += qc.get("auto_fixed", 0) if isinstance(qc.get("auto_fixed"), int) else 0

    if any(total_qc.values()):
        parts.append(f'<div class="stats-bar">')
        parts.append(f'<div class="stat-card"><div class="stat-value" style="color:{T["red"]}">{total_qc["errors"]}</div><div class="stat-label">Errors</div></div>')
        parts.append(f'<div class="stat-card"><div class="stat-value" style="color:{T["amber"]}">{total_qc["warnings"]}</div><div class="stat-label">Warnings</div></div>')
        parts.append(f'<div class="stat-card"><div class="stat-value" style="color:{T["blue"]}">{total_qc["infos"]}</div><div class="stat-label">Infos</div></div>')
        parts.append(f'<div class="stat-card"><div class="stat-value" style="color:{T["green"]}">{total_qc["auto_fixed"]}</div><div class="stat-label">Auto-Fixed</div></div>')
        parts.append('</div>')

    parts.append('</div>')
    parts.append(PAGE_FOOT.format(now=""))
    return "\n".join(parts)


# ── Main ───────────────────────────────────────────────────────────────────

def generate_site():
    """Main orchestrator — load data and generate all pages."""
    validate_schema()
    print("Loading index...")
    index = load_index()
    total = index.get("total_cves_processed", 0)
    print(f"  {total} CVEs in index")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "cves").mkdir(parents=True, exist_ok=True)

    # Dashboard
    print("Generating dashboard (index.html)...")
    html = gen_dashboard(index)
    with open(OUTPUT_DIR / "index.html", "w") as f:
        f.write(html)

    # Per-CVE detail pages
    entries = index.get("cves", [])
    print(f"Generating {len(entries)} CVE detail pages...")
    count = 0
    for entry in entries:
        cve_id = entry["cve_id"]
        rec = load_cve(cve_id)
        if rec:
            html = gen_cve_detail(rec)
            with open(OUTPUT_DIR / "cves" / f"{cve_id}.html", "w") as f:
                f.write(html)
            count += 1
        if count % 200 == 0:
            print(f"  {count}/{len(entries)}...")

    print(f"  Generated {count} detail pages")

    # Schema page
    print("Generating schema page...")
    html = gen_schema_page()
    with open(OUTPUT_DIR / "schema.html", "w") as f:
        f.write(html)

    # Pipeline page
    print("Generating pipeline page...")
    html = gen_pipeline_page()
    with open(OUTPUT_DIR / "pipeline.html", "w") as f:
        f.write(html)

    # .nojekyll
    (OUTPUT_DIR / ".nojekyll").touch()

    print(f"\nDone! Site generated in {OUTPUT_DIR}")
    print(f"  {OUTPUT_DIR / 'index.html'}")
    print(f"  {OUTPUT_DIR / 'cves/'}  ({count} pages)")
    print(f"  {OUTPUT_DIR / 'schema.html'}")
    print(f"  {OUTPUT_DIR / 'pipeline.html'}")
    print(f"  {OUTPUT_DIR / '.nojekyll'}")


if __name__ == "__main__":
    if "--validate" in sys.argv:
        validate_schema()
    else:
        generate_site()
