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
import contextlib
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
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


def _ghost_candidates(stories_dir):
    """[(path, story)] for every eventless, non-redirect story file."""
    out = []
    for p in sorted(glob.glob(os.path.join(stories_dir, "*.json"))):
        s = _read_json(p)
        if s and not s.get("merged_into") and not s.get("events"):
            out.append((p, s))
    return out


def _analysis_ids(data_dir):
    return {os.path.splitext(os.path.basename(p))[0]
            for p in glob.glob(os.path.join(data_dir, "analysis", "*.md"))}


def _keep_reason(sid, story, refs, analyzed, days, now):
    """Why this ghost must be kept now, or None when it is deletable."""
    if sid in refs:
        return "referenced"
    if sid in analyzed:
        return "analyzed"
    if age_days(story, now) < days:
        return "young"
    return None


def find_ghosts(data_dir, days=DEFAULT_DAYS, include_analyzed=False, now=None):
    """(deletable paths, stats). A ghost is deletable when it has no events,
    is not a redirect shell, is unreferenced, is past the retention window,
    and (unless include_analyzed) has no analysis file."""
    now = now or datetime.now(timezone.utc)
    refs = referenced_ids(data_dir)
    analyzed = set() if include_analyzed else _analysis_ids(data_dir)
    stats = {"ghosts": 0, "referenced": 0, "analyzed": 0, "young": 0}
    deletable = []
    for p, s in _ghost_candidates(os.path.join(data_dir, "stories")):
        sid = s.get("id") or os.path.splitext(os.path.basename(p))[0]
        stats["ghosts"] += 1
        reason = _keep_reason(sid, s, refs, analyzed, days, now)
        if reason is None:
            deletable.append((p, sid))
        else:
            stats[reason] += 1
    return deletable, stats


def _days_arg(args):
    """Retention window from --days N, or None on a malformed value."""
    if "--days" not in args:
        return DEFAULT_DAYS
    i = args.index("--days") + 1
    if i >= len(args) or not args[i].isdigit():
        return None
    return int(args[i])


def _report(deletable, stats, days, dry):
    print(f"ghosts: {stats['ghosts']} total | {len(deletable)} deletable "
          f"(>{days}d, unreferenced) | kept: {stats['referenced']} referenced, "
          f"{stats['analyzed']} analyzed, {stats['young']} younger than {days}d")
    for _, sid in deletable[:20]:
        print(f"  {'DRY rm' if dry else 'rm'} {sid}")
    if len(deletable) > 20:
        print(f"  ... and {len(deletable) - 20} more")
    if dry:
        print("dry-run: nothing removed")


def _remove(deletable):
    removed = 0
    for p, _ in deletable:
        with contextlib.suppress(OSError):
            os.remove(p)
            removed += 1
    return removed


def main():
    args = sys.argv[1:]
    days = _days_arg(args)
    if days is None:
        print("usage: cleanup_ghosts.py [--days N] [--dry-run] [--include-analyzed]")
        return 2
    dry = "--dry-run" in args
    deletable, stats = find_ghosts(DATA, days, "--include-analyzed" in args)
    _report(deletable, stats, days, dry)
    if dry:
        return 0
    removed = _remove(deletable)
    if removed:
        print(f"cleanup_ghosts: removed {removed} ghost stories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
