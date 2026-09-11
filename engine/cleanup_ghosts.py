#!/usr/bin/env python3
"""Remove dead-weight "ghost" stories from the store.

A ghost is a story whose events were all dropped by triage while the story
JSON stayed behind: eventless, and not a redirect shell. It renders no page
(ssg skips eventless stories), so it is pure store weight — but it is only
SAFE to delete when nothing still points at it:

  * not a redirect target (another story's ``merged_into`` would dangle)
  * not referenced by a digest (narrative link or ``stories`` list)
  * not referenced by a CTI record, the CTI queue, or needs-analysis

Stories that still have an analysis file are KEPT by default — a written
analysis means the story was real coverage, and keeping it keeps the pair
consistent. Pass ``--include-analyzed`` to delete those too. Age is
``max(first_seen, last_seen)``; an undated story counts as old.

Run hourly from the tia-kev job: it self-gates on the store (no state file),
deleting a ghost only once it crosses the retention window. ``--dry-run``
previews. Never deletes a live story (one with events).

Usage: python3 cleanup_ghosts.py [--days N] [--dry-run] [--include-analyzed]
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
STORIES = os.path.join(DATA, "stories")
ANALYSIS = os.path.join(DATA, "analysis")
DIGESTS = os.path.join(DATA, "digests")
CTI = os.path.join(DATA, "cti")
DEFAULT_DAYS = 90
DIGEST_LINK_RE = re.compile(r"\]\(stories/([^/]+)/\)")


def _read_json(path):
    """Fail-open JSON read: corrupt/empty/unreadable -> None."""
    try:
        with open(path) as fh:
            return json.load(fh)
    except (json.JSONDecodeError, ValueError, OSError):
        return None


def _digest_refs(data_dir):
    """Story ids a digest points at: narrative links (.md) and metadata
    stories lists (.json)."""
    refs = set()
    for f in glob.glob(os.path.join(data_dir, "digests", "*.md")):
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                refs.update(DIGEST_LINK_RE.findall(fh.read()))
        except OSError:
            pass
    for f in glob.glob(os.path.join(data_dir, "digests", "*.json")):
        refs.update((_read_json(f) or {}).get("stories", []) or [])
    return refs


def _cti_refs(data_dir):
    """Story ids named by a CTI record (audit store_invariants checks these)."""
    return {d["story_id"] for d in
            (_read_json(f) for f in glob.glob(os.path.join(data_dir, "cti", "*.json")))
            if d and d.get("story_id")}


def _queue_refs(data_dir):
    """Story ids in needs-analysis.json / cti-queue.json (str or {id})."""
    refs = set()
    for name in ("needs-analysis.json", "cti-queue.json"):
        data = _read_json(os.path.join(data_dir, name)) or {}
        for item in data.get("stories", []) or []:
            refs.add(item if isinstance(item, str) else item.get("id"))
    refs.discard(None)
    return refs


def _redirect_targets(data_dir):
    """Story ids other stories redirect to — deleting one would dangle."""
    return {d["merged_into"] for d in
            (_read_json(f) for f in glob.glob(os.path.join(data_dir, "stories", "*.json")))
            if d and d.get("merged_into")}


def referenced_ids(data_dir):
    """Every story id still pointed at by something other than the story
    file itself: digest links + metadata, CTI records, cti-queue,
    needs-analysis, and redirect targets."""
    return (_digest_refs(data_dir) | _cti_refs(data_dir)
            | _queue_refs(data_dir) | _redirect_targets(data_dir))


def age_days(story, now):
    """Days since the story was last relevant: max(first_seen, last_seen).
    An undated story is treated as maximally old (clearly dead weight)."""
    stamp = max(story.get("last_seen") or "", story.get("first_seen") or "")
    if not stamp:
        return 10 ** 6
    try:
        dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (now - dt).total_seconds() / 86400.0
    except (ValueError, TypeError):
        return 10 ** 6


def find_ghosts(data_dir, days=DEFAULT_DAYS, include_analyzed=False, now=None):
    """(deletable paths, stats). A ghost is deletable when it has no events,
    is not a redirect shell, is unreferenced, is past the retention window,
    and (unless include_analyzed) has no analysis file."""
    now = now or datetime.now(timezone.utc)
    stories_dir = os.path.join(data_dir, "stories")
    refs = referenced_ids(data_dir)
    base = {os.path.splitext(os.path.basename(p))[0]
            for p in glob.glob(os.path.join(stories_dir, "*.json"))}
    analyzable = {os.path.splitext(os.path.basename(p))[0]
                  for p in glob.glob(os.path.join(data_dir, "analysis", "*.md"))}
    deletable, stats = [], {"ghosts": 0, "referenced": 0, "analyzed": 0,
                            "young": 0}
    for p in sorted(glob.glob(os.path.join(stories_dir, "*.json"))):
        s = _read_json(p)
        if not s or s.get("merged_into") or s.get("events"):
            continue
        sid = s.get("id") or os.path.splitext(os.path.basename(p))[0]
        stats["ghosts"] += 1
        if sid in refs:
            stats["referenced"] += 1
            continue
        if sid in analyzable and not include_analyzed:
            stats["analyzed"] += 1
            continue
        if age_days(s, now) < days:
            stats["young"] += 1
            continue
        deletable.append((p, sid))
    return deletable, stats


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    include_analyzed = "--include-analyzed" in args
    days = DEFAULT_DAYS
    if "--days" in args:
        try:
            days = int(args[args.index("--days") + 1])
        except (IndexError, ValueError):
            print("usage: cleanup_ghosts.py [--days N] [--dry-run] [--include-analyzed]")
            return 2
    deletable, stats = find_ghosts(DATA, days, include_analyzed)
    print(f"ghosts: {stats['ghosts']} total | {len(deletable)} deletable "
          f"(>{days}d, unreferenced) | kept: {stats['referenced']} referenced, "
          f"{stats['analyzed']} analyzed, {stats['young']} younger than {days}d")
    for _, sid in deletable[:20]:
        print(f"  {'DRY rm' if dry else 'rm'} {sid}")
    if len(deletable) > 20:
        print(f"  ... and {len(deletable) - 20} more")
    if dry:
        print("dry-run: nothing removed")
        return 0
    removed = 0
    for p, _ in deletable:
        try:
            os.remove(p)
            removed += 1
        except OSError as exc:
            print(f"WARN: could not remove {p}: {exc}", file=sys.stderr)
    if removed:
        print(f"cleanup_ghosts: removed {removed} ghost stories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
