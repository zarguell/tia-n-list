#!/usr/bin/env python3
"""Tia N. List — shared store loaders.

The hybrid store splits content (data/events/<id>.md) from metadata
(data/events/<id>.json). Every consumer that needs article TEXT — IOC
extraction, hot-score content signals, snippet generation — must load the
merged view, not the bare JSON. This module is that single implementation:
the ssg used to be the only place that merged, which silently blinded
ioc.build_index (cti_pass) and hot_score (merge) — see the 2026-08-11 audit.

URLs are scheme-filtered here (http/https only) so feed-controlled values can
never become javascript:/data: hrefs anywhere downstream.
"""
import glob
import json
import os
from urllib.parse import urlsplit

ENGINE = os.path.dirname(os.path.abspath(__file__))
EVENTS_DIR = os.path.join(ENGINE, "data", "events")


def safe_url(url):
    """Return url only if it has an http(s) scheme; '' otherwise."""
    if not url:
        return ""
    try:
        return url if urlsplit(url).scheme in ("http", "https") else ""
    except ValueError:
        return ""


def load_events():
    """All events as {id: {...meta, content_md, url}} — content merged from the
    .md sidecar, url scheme-filtered."""
    events = {}
    for path in sorted(glob.glob(os.path.join(EVENTS_DIR, "*.json"))):
        eid = os.path.splitext(os.path.basename(path))[0]
        meta = json.load(open(path))
        md_path = os.path.join(EVENTS_DIR, eid + ".md")
        md_text = open(md_path).read() if os.path.exists(md_path) else ""
        meta["content_md"] = md_text
        meta["url"] = safe_url(meta.get("url") or "")
        events[eid] = meta
    return events
