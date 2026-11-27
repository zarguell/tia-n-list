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
import hashlib
import json
import os
import sqlite3
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


EVENTS_CACHE = os.path.join(DATA, ".events-cache.sqlite3")


def _fingerprint():
    """(fingerprint, filenames) for the event store, from ONE scandir pass.

    mtime_ns + size of every .json/.md file: editing either side invalidates,
    adding or deleting a file changes the digest. ~88.8k entries on
    2026-11-27 costs ~0.1 s, against 16.3 s to parse every file (measured).
    """
    parts = []
    for entry in os.scandir(EVENTS_DIR):
        if not entry.name.endswith((".json", ".md")):
            continue
        try:
            st = entry.stat()
        except OSError:
            continue
        parts.append(f"{entry.name}:{st.st_mtime_ns}:{st.st_size}")
    parts.sort()
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return digest, [p.split(":", 1)[0] for p in parts]


def _read_events_files():
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


def _cache_read(digest):
    """Events from the derived cache, or None when it is missing/stale/damaged."""
    try:
        with sqlite3.connect(f"file:{EVENTS_CACHE}?mode=ro", uri=True) as db:
            row = db.execute("SELECT value FROM meta WHERE key='fingerprint'").fetchone()
            if not row or row[0] != digest:
                return None
            events = {}
            for eid, meta_json, content_md in db.execute(
                    "SELECT id, meta, content_md FROM events"):
                meta = json.loads(meta_json)
                meta["content_md"] = content_md
                events[eid] = meta
            return events
    except (sqlite3.Error, OSError, ValueError):
        return None


def _cache_write(digest, events):
    """Atomically replace the cache. Failure is a no-op: files stay the truth."""
    tmp = EVENTS_CACHE + ".tmp"
    try:
        with sqlite3.connect(tmp) as db:
            db.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)")
            db.execute("CREATE TABLE events (id TEXT PRIMARY KEY, meta TEXT, content_md TEXT)")
            db.execute("INSERT INTO meta VALUES ('fingerprint', ?)", (digest,))
            db.executemany(
                "INSERT INTO events VALUES (?, ?, ?)",
                ((eid, json.dumps({k: v for k, v in meta.items() if k != "content_md"}),
                  meta.get("content_md") or "") for eid, meta in events.items()))
            db.commit()
        os.replace(tmp, EVENTS_CACHE)
    except (sqlite3.Error, OSError):
        try:
            os.remove(tmp)
        except OSError:
            pass


def load_events(use_cache=True):
    """All events as {id: {...meta, content_md, url}} — content merged from the
    .md sidecar, url scheme-filtered.

    Performance (2026-11-27): 44,402 events = 88,806 files, 16.3 s per call,
    and 14 call sites across the hourly passes (merge twice, triage, cti,
    ssg, ...). The files stay the source of truth; a derived sqlite cache
    keyed on a scandir fingerprint makes a warm call ~0.4 s. Any sqlite
    problem falls back to reading every file, so a corrupt or unreadable
    cache can never blind the pipeline.
    """
    if not use_cache:
        return _read_events_files()
    digest, _ = _fingerprint()
    events = _cache_read(digest)
    if events is not None:
        return events
    events = _read_events_files()
    _cache_write(digest, events)
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
