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

The cold tier (the freeze half): peak_score — the high-water mark the
store-health root made every rescoring path write — is what finally makes
"cooled story" distinguishable from "never mattered". By 2026-09-24 the
store held ~10.2k stories of which ~8.2k had peak_score 0, and the SSG full
build rendered every one of them while merge's rescoring loop touched every
one of them every hour, all for pages nothing ever linked. freeze_sweep
moves such stories to a cold tier (data/frozen.json):

  - freeze_sweep: old enough, never crossed peak 3.0 (deliberately below
    the 3.3 warm band), single-source, no analysis, not digest-referenced
    -> frozen. merge stops rescoring/matching/needs-emitting them; SSG
    stops rendering them.
  - unfreeze_strong / unfreeze_ids: the exits. A new event whose CVE set
    or exact URL hits a frozen story is strong evidence it matters again
    (merge calls it per incoming event; trivial no-op while frozen.json is
    empty). An explicit LLM keep/merge decision naming a frozen story is
    editorial corroboration (triage calls unfreeze_ids).

A frozen story is never deleted: its json stays exactly as frozen (score,
peak and breakdown frozen in time), so an unfreeze resumes with history
intact and a re-freeze is idempotent. A story thawed by a strong event can
be re-frozen by the same hour's sweep if the new evidence raised no peak —
that oscillation is by design: the sweep is the last word, and the next
strong event re-opens the story.
"""
import glob
import json
import os
import re
from datetime import datetime, timezone

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DIGESTS = os.path.join(DATA, "digests")
STORIES = os.path.join(DATA, "stories")
# sibling of stories/ (derived the same way STORIES is derived from DATA), so
# repointing STORIES in tests moves the event dir with it
EVENTS = os.path.join(os.path.dirname(STORIES), "events")

# Cold-tier thresholds. FREEZE_PEAK sits deliberately BELOW the warm band
# (hot_score bands: warm >= 3.3): a story that ever got warm keeps its page
# and its place in the store forever; freezing is for stories that never
# mattered at all. The other two keep obviously-live stories out: a week of
# silence before anything freezes, and multi-source pickup is attention.
FREEZE_PEAK = 3.0
FREEZE_MIN_AGE_DAYS = 7
FREEZE_MAX_SOURCES = 1
FREEZE_FILE = os.path.join(DATA, "frozen.json")   # {"updated": iso, "ids": [...]}

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


# ---- cold tier: freeze / unfreeze -----------------------------------------

def age_days(iso, now=None):
    """Age of an ISO-8601 timestamp (Z or offset form) in float days.

    Missing or unparseable input returns 0.0 — a story whose clock cannot be
    read is treated as brand-new, so a corrupt first_seen can never freeze
    anything (fail-warm, never fail-frozen).
    """
    if now is None:
        now = datetime.now(timezone.utc)
    try:
        dt = datetime.fromisoformat(
            (iso or "").replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, TypeError, AttributeError):
        return 0.0
    return (now - dt).total_seconds() / 86400.0


def frozen_ids():
    """The frozen set, from data/frozen.json. Tolerant loader: a missing,
    empty or corrupt file means NOTHING is frozen (fail-warm — one bad file
    must never widen the freeze), and non-string ids are dropped."""
    try:
        data = json.load(open(FREEZE_FILE))
    except (OSError, ValueError):
        return set()
    ids = data.get("ids") if isinstance(data, dict) else None
    if not isinstance(ids, list):
        return set()
    return {i for i in ids if isinstance(i, str)}


def _save_frozen(ids):
    json.dump({"updated": datetime.now(timezone.utc).strftime(
                  "%Y-%m-%dT%H:%M:%SZ"),
               "ids": sorted(ids)},
              open(FREEZE_FILE, "w"), indent=1)


def freeze_sweep(stories, referenced=None, log=print):
    """Move never-mattered stories to the cold tier. Returns the NEWLY
    frozen ids (the pre-existing frozen set is not re-reported).

    Eligibility (ALL must hold — each criterion independently blocks):
    not merged_into, not already frozen, not digest-referenced (live URLs),
    no truthy "analysis" key (a written analysis = someone cared), age over
    FREEZE_MIN_AGE_DAYS, peak_score under FREEZE_PEAK, and n_sources within
    FREEZE_MAX_SOURCES. Saves frozen.json once at the end; logs one summary
    line (count + first few ids), never per-id spam — this runs hourly.
    """
    if referenced is None:
        referenced = referenced_story_ids()
    frozen = frozen_ids()
    newly = []
    for sid, s in stories.items():
        if (sid in frozen or sid in referenced or s.get("merged_into")
                or s.get("analysis")):
            continue
        if age_days(s.get("first_seen") or "") <= FREEZE_MIN_AGE_DAYS:
            continue
        if float(s.get("peak_score") or 0) >= FREEZE_PEAK:
            continue
        if int(s.get("n_sources") or 0) > FREEZE_MAX_SOURCES:
            continue
        newly.append(sid)
    if newly:
        frozen.update(newly)
        _save_frozen(frozen)
        log(f"lifecycle: froze {len(newly)} cold stories "
            f"(peak<{FREEZE_PEAK}, age>{FREEZE_MIN_AGE_DAYS}d, "
            f"n_sources<={FREEZE_MAX_SOURCES}, no analysis): "
            f"{', '.join(sorted(newly)[:3])}{'...' if len(newly) > 3 else ''}")
    return set(newly)


# Per-run index over the frozen set (story cves + event-file urls), rebuilt
# only when the frozen set changes. merge.py calls unfreeze_strong once per
# incoming event; without this index every call would re-read every frozen
# story's event files (8k+ after the first sweep) — with it, per-event cost
# is two set lookups.
_STRONG_CACHE = {"key": None, "cves": {}, "urls": {}, "stale": set()}


def _story_event_urls(sid):
    """Event urls for one story, read from the event jsons (the story json
    carries only refs). Tolerant: a missing/corrupt event file contributes
    nothing — the URL escape hatch just won't fire for it."""
    try:
        s = json.load(open(os.path.join(STORIES, sid + ".json")))
    except (OSError, ValueError):
        return set()
    urls = set()
    for ref in s.get("events", []):
        try:
            e = json.load(open(os.path.join(EVENTS, ref["event_id"] + ".json")))
        except (OSError, ValueError, TypeError, KeyError):
            continue
        if e.get("url"):
            urls.add(e["url"].strip())
    return urls


def _strong_index(frozen, stories):
    """CVE sets + event-file urls per frozen story, plus stale ids (frozen
    but story file gone — tombstoned out from under the freeze). Keyed by the
    frozen set so merge's `frozen -= unfreeze_strong(...)` pattern rebuilds
    exactly when membership changes."""
    key = (frozenset(frozen), STORIES)   # path in the key: repointed stores in tests rebuild
    if _STRONG_CACHE["key"] == key:
        return _STRONG_CACHE
    cves, urls, stale = {}, {}, set()
    for sid in frozen:
        s = stories.get(sid)
        if s is None or not os.path.exists(os.path.join(STORIES, sid + ".json")):
            stale.add(sid)
            continue
        cves[sid] = {c.upper() for c in (s.get("cves") or [])}
        urls[sid] = _story_event_urls(sid)
    _STRONG_CACHE.update(key=key, cves=cves, urls=urls, stale=stale)
    return _STRONG_CACHE


def unfreeze_strong(ev, stories, log=print):
    """Thaw frozen stories a new event STRONGLY matches. Returns the ids
    removed from the frozen set this call — strong matches (the event's CVE
    set intersects the story's cves, or its exact URL matches one of the
    story's event-file urls) plus stale ids whose story file is gone — so
    callers can do `frozen -= unfreeze_strong(ev, stories)`. Saves
    frozen.json only when something actually changed.

    Trivial when frozen.json is empty (the fresh-clone steady state: return
    set() before any work beyond the one small read).
    """
    frozen = frozen_ids()
    if not frozen:
        return set()
    idx = _strong_index(frozen, stories)
    ev_cves = {c.upper() for c in (ev.get("cves") or [])}
    ev_url = (ev.get("url") or "").strip()
    hit = {sid for sid in frozen
           if (ev_cves and ev_cves & idx["cves"].get(sid, set()))
           or (ev_url and ev_url in idx["urls"].get(sid, set()))}
    out = hit | idx["stale"]
    if not out:
        return set()
    _save_frozen(frozen - out)
    for sid in sorted(hit):
        why = "cve" if ev_cves and ev_cves & idx["cves"].get(sid, set()) else "url"
        log(f"lifecycle: unfroze {sid} (strong event {why}-match)")
    if idx["stale"]:
        log(f"lifecycle: dropped {len(idx['stale'])} stale frozen id(s) "
            f"(story file gone)")
    return out


def unfreeze_ids(ids, log=print):
    """Editorial unfreeze: remove ids from the frozen set (triage apply —
    an LLM keep/merge explicitly naming a frozen story is corroboration
    stronger than any score). Returns the ids that were actually frozen."""
    frozen = frozen_ids()
    hit = {i for i in ids if i in frozen}
    if hit:
        _save_frozen(frozen - hit)
        log(f"lifecycle: editorially unfroze {len(hit)} story id(s)")
    return hit
