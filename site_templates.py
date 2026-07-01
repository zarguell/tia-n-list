"""Design tokens and page templates for the kevrichment static site generator."""

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
