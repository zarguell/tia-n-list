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
