"""Helper functions for the kevrichment static site generator."""

import html as html_mod
from datetime import datetime
from urllib.parse import urlparse

from site_templates import T

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
