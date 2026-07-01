"""Tests for build_site.py helpers and design tokens."""
import build_site


def test_safe_url_rejects_javascript_scheme():
    assert build_site.safe_url("javascript:alert(1)") == "#"


def test_safe_url_rejects_data_scheme():
    assert build_site.safe_url("data:text/html,<script>alert(1)</script>") == "#"


def test_safe_url_rejects_file_scheme():
    assert build_site.safe_url("file:///etc/passwd") == "#"


def test_safe_url_accepts_https():
    assert build_site.safe_url("https://example.com/x") == "https://example.com/x"


def test_safe_url_accepts_http():
    assert build_site.safe_url("http://example.com/y") == "http://example.com/y"


def test_safe_url_handles_none():
    assert build_site.safe_url(None) == "#"


def test_safe_url_handles_empty():
    assert build_site.safe_url("") == "#"


def test_safe_url_html_escapes_quotes_in_safe_urls():
    assert build_site.safe_url('https://example.com/?a="b"') == 'https://example.com/?a=&quot;b&quot;'


def _relative_luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _contrast_ratio(fg, bg):
    l1, l2 = _relative_luminance(fg), _relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def test_accent_meets_wcag_aa_on_bg():
    assert _contrast_ratio(build_site.T["accent"], build_site.T["bg"]) >= 4.5


def test_text_muted_meets_wcag_aa_on_bg():
    assert _contrast_ratio(build_site.T["text_muted"], build_site.T["bg"]) >= 4.5


def test_accent_hover_meets_wcag_aa_on_bg():
    assert _contrast_ratio(build_site.T["accent_hover"], build_site.T["bg"]) >= 4.5


def test_dashboard_renders_cve_id_as_keyboard_focusable_anchor():
    html = build_site.gen_dashboard(
        {"last_updated": "", "total_cves_processed": 0, "cves": []}
    )
    # The CVE-ID cell must build an <a href="cves/{id}.html"> so Tab+Enter works.
    assert 'href="cves/\' + r.id + \'.html"' in html


def test_safe_url_handles_none_input():
    """safe_url must return safe fallback for None (missing JSON field).

    Callers pass r.get('field') which returns None when the key is absent.
    urlparse(None) raises AttributeError — the narrowed except must catch it.
    """
    assert build_site.safe_url(None) == "#"


def test_dashboard_sort_uses_data_keys_not_display_names():
    """sortCol must store data keys ('published') not display names ('Published').

    Regression test: the old code stored display names in sortCol but looked them
    up in a keyMap keyed by data names — the lookup always failed and fell back to
    sorting by 'id' for every column click.
    """
    html = build_site.gen_dashboard(
        {"last_updated": "", "total_cves_processed": 0, "cves": []}
    )
    # Initial sortCol must be a data key, not a display name
    assert "sortCol = 'published'" in html
    assert "sortCol = 'Published'" not in html
    # The broken keyMap lookup must be gone
    assert "keyMap[sortCol]" not in html


def test_dashboard_sort_parses_cve_id_numerically():
    """CVE ID sort must parse CVE-YYYY-NNNN and compare numerically.

    Regression test: lexicographic string sort puts CVE-2026-20253 before
    CVE-2026-999 (because '2' < '9'), which is wrong. The fix adds a regex
    match that extracts year and sequence number for numeric comparison.
    """
    html = build_site.gen_dashboard(
        {"last_updated": "", "total_cves_processed": 0, "cves": []}
    )
    assert "CVE-(\\d{4})-(\\d+)" in html
