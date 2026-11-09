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
DATA = os.path.join(ENGINE, "data")
EVENTS_DIR = os.path.join(ENGINE, "data", "events")


def safe_url(url):
    """Return url only if it has an http(s) scheme; '' otherwise."""
    if not url:
        return ""
    try:
        return url if urlsplit(url).scheme in ("http", "https") else ""
    except ValueError:
        return ""


def write_json(path, obj, indent=1):
    """Write a JSON record atomically (temp file in the same directory, then
    os.replace).

    The store is read and written concurrently all day: the hourly merge and
    triage apply rewrite story/event json while ssg, cti_pass, audit and the
    snapshot writer read it. A plain `json.dump(obj, open(path, "w"))`
    truncates the file first, so a reader can observe a zero-length record and
    die with `JSONDecodeError: Expecting value: line 1 column 1` — which
    aborts the publishing job mid-run (`ABORT: ssg failed, not pushing`:
    2026-11-01 cti, 2026-11-05 cti, 2026-11-09 story-desk). os.replace is
    atomic within a filesystem, so readers see either the old record or the
    new one, never a partial file.

    fsync is deliberately skipped: the requirement here is reader
    atomicity, not power-loss durability, and the hourly run rewrites
    thousands of records.
    """
    tmp = f"{path}.tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, indent=indent)
    os.replace(tmp, path)
    return path


def load_events():
    """All events as {id: {...meta, content_md, url}} — content merged from the
    .md sidecar, url scheme-filtered."""
    import sys
    events = {}
    for path in sorted(glob.glob(os.path.join(EVENTS_DIR, "*.json"))):
        eid = os.path.splitext(os.path.basename(path))[0]
        try:
            meta = json.load(open(path))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"WARN: skipping corrupt event file {path}: {exc}", file=sys.stderr)
            continue
        md_path = os.path.join(EVENTS_DIR, eid + ".md")
        md_text = open(md_path).read() if os.path.exists(md_path) else ""
        meta["content_md"] = md_text
        meta["url"] = safe_url(meta.get("url") or "")
        events[eid] = meta
    return events


def load_social_posts():
    """Reddit + X signal posts, combined (data/reddit.json + data/x.json).

    The load-bearing field is article_url: score.hot_score matches it
    against story event URLs for pickup signal. Social posts never create
    stories — they amplify or attach. Missing files contribute nothing;
    malformed entries are skipped so one bad record can't blind the score.
    """
    posts = []
    for name in ("reddit.json", "x.json", "masto.json"):
        try:
            with open(os.path.join(DATA, name)) as f:
                for entry in json.load(f):
                    if isinstance(entry, dict) and entry.get("article_url"):
                        posts.append(entry)
        except (OSError, ValueError):
            continue
    return posts
