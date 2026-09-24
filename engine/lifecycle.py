#!/usr/bin/env python3
"""Store lifecycle: which stories exist, and for how long.

The story store only ever grew: every triage drop that emptied a candidate
left its zero-event json behind (4,486 shells by 2026-09-24, ~300 stories/day
at peak). SSG already refused to render orphaned stories, so no published URL
ever pointed at one — but the store paid for the dead weight in every
merge/collect/audit scan. This module is the lifecycle home:

  - tombstone_orphans: delete zero-event candidate shells (never rendered,
    so the URL-stability rule does not apply; digest-referenced ids are
    spared and reported). Called by triage apply after every run and
    store-wide by repair_shells.py.
  - referenced_story_ids: story ids any published digest page still links —
    the "never delete" guard for live URLs.

merged_into shells are NOT orphans: they redirect live URLs and stay.
The cold-tier freeze (peak_score-based) lands in a follow-up leaf.
"""
import glob
import json
import os
import re

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DIGESTS = os.path.join(DATA, "digests")
STORIES = os.path.join(DATA, "stories")

STORY_LINK_RE = re.compile(r"stories/([a-z0-9][a-z0-9-]*)/?")
# bare story ids as json values (digest feature metadata carries the id it
# links); bounded by the store so arbitrary strings never match
ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{4,}")


def referenced_story_ids():
    """Story ids any published digest page still links.

    Digests are the only published surface that links arbitrary stories
    (features + per-day pages); a link into a deleted page 404s and fails
    the SSG backlink lint, so these ids are never tombstoned. The merge
    manifest is deliberately NOT consulted: it records every slug on its
    mint day, which would guard every shell forever.
    """
    refs = set()
    for path in glob.glob(os.path.join(DIGESTS, "*.md")):
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        refs.update(STORY_LINK_RE.findall(text))
    for path in glob.glob(os.path.join(DIGESTS, "*.json")):
        try:
            data = json.load(open(path))
        except (OSError, ValueError):
            continue
        _collect_ids(data, refs)
    return refs


def _collect_ids(node, out):
    if isinstance(node, str):
        out.update(STORY_LINK_RE.findall(node))
        if ID_RE.fullmatch(node) and os.path.exists(
                os.path.join(STORIES, node + ".json")):
            out.add(node)
    elif isinstance(node, list):
        for v in node:
            _collect_ids(v, out)
    elif isinstance(node, dict):
        for v in node.values():
            _collect_ids(v, out)
    return


def orphan_ids(stories):
    """Zero-event candidate shells: never rendered, never redirecting."""
    return sorted(sid for sid, s in stories.items()
                  if not s.get("merged_into") and not s.get("events"))


def tombstone_orphans(stories, referenced=None, dry_run=False, log=print):
    """Delete zero-event candidate shells from the store (memory + disk).

    Returns the sorted ids removed (or that WOULD be removed on a dry run).
    merged_into redirect shells and digest-referenced ids are never touched.
    """
    if referenced is None:
        referenced = referenced_story_ids()
    removed = []
    for sid in orphan_ids(stories):
        if sid in referenced:
            log(f"lifecycle: spared digest-referenced shell {sid}")
            continue
        removed.append(sid)
        if dry_run:
            continue
        del stories[sid]
        try:
            os.remove(os.path.join(STORIES, sid + ".json"))
        except OSError as e:
            log(f"lifecycle: could not remove {sid}: {e}")
    return removed
