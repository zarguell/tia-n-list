#!/usr/bin/env python3
"""Archive repo writer — the cold hand of the retention policy.

`retention.py` decides *what* may leave the published site; this module moves
the DATA out of the hot store and into an archive repo, and nothing else. It
never deletes before the copy is durable, and it refuses to move anything a
live page still depends on.

Layout of the archive repo (all data, no build, never published):

    manifest.jsonl              one appended line per archived story
    stories/<id>.json           the story record as it left the store
    events/<event-id>.json      only events no live story references
    events/<event-id>.md
    analysis/<id>.md            only when the story brought one (blocked today)

Safety rules, each of which BLOCKS a story rather than guessing:

  * not in `retention.expiring()['expirable']`      (tier/horizon disqualified)
  * is a redirect target (`merged_into` value)       its URL is a map key
  * is a digest citation                            the digest link must be
                                                    rewritten first (step 3)
  * has an analysis file                            prose we must not orphan
  * shares an event with a story staying put        the .md/.json is still read

Default is a DRY RUN. `--apply` requires --archive-root and copies, then
removes from the hot store, appending the manifest line first, so an
interrupted run leaves the archive complete and the store merely untouched.

Usage:
  python3 engine/archive.py                        # dry run, report only
  python3 engine/archive.py --json                 # machine-readable
  python3 engine/archive.py --archive-root DIR --apply
  python3 engine/archive.py --archive-root DIR --verify
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import date, datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ENGINE)

import retention  # noqa: E402
import store  # noqa: E402

ARCHIVE_ENV = "TIA_ARCHIVE_ROOT"

# The hot store's event directory. A module attribute (not a parameter) so tests
# can point it at a tmp store the way they already do for retention.STORIES_DIR.
EVENTS_DIR = store.EVENTS_DIR


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def event_refs(stories):
    """{event_id: {story ids that reference it}} across the whole store."""
    refs = {}
    for sid, st in stories.items():
        for e in st.get("events") or []:
            eid = e.get("event_id")
            if eid:
                refs.setdefault(eid, set()).add(sid)
    return refs


# Per-story guards, as a table (house style: registries, not branches).
# Each entry: (name, applies(context), reason to report). A story blocks on the
# FIRST rule that applies, so the reason names the most fundamental obstacle.
_STORY_GUARDS = (
    ("missing", lambda c: c["sid"] not in c["stories"], "story file missing"),
    ("target", lambda c: c["sid"] in c["targets"],
     "redirect target (its URL is a map key)"),
    ("digest", lambda c: c["sid"] in c["digest"],
     "digest-cited (link rewrite lands with step 3)"),
    ("analysis", lambda c: c["sid"] in c["analysis_ids"], "has an analysis file"),
)


def _blocked_reason(sid, ctx):
    """Why a candidate may not move, or None when it is clean."""
    case = dict(ctx, sid=sid)
    for _name, applies, reason in _STORY_GUARDS:
        if applies(case):
            return reason
    return None


def _shares_stored_event(story, refs, candidates):
    """True when any of the story's events is also read by a story that stays."""
    return any(refs.get(e.get("event_id"), set()) - candidates
               for e in story.get("events") or [] if e.get("event_id"))


def _split_candidates(expirable, ctx):
    """(clean ids, {blocked id: reason}) — per-story guards only."""
    clean, blocked = [], {}
    for sid in sorted(expirable):
        reason = _blocked_reason(sid, ctx)
        if reason:
            blocked[sid] = reason
        else:
            clean.append(sid)
    return clean, blocked


def _split_shared(clean, stories, refs):
    """(ids whose events are exclusive, ids blocked by a shared event)."""
    staying = set(clean)
    exclusive, shared = [], []
    for sid in clean:
        target = shared if _shares_stored_event(stories[sid], refs, staying) else exclusive
        target.append(sid)
    return exclusive, shared


def plan(stories, expirable, digest=None, analysis_ids=None):
    """(story ids to move, event ids to move, {blocked id: reason}). Pure.

    Two phases, because the second depends on the whole candidate set: first
    the per-story guards, then the shared-event filter. An event shared with a
    story that stays must not move, and the story that owns it cannot go either
    — its page would lose the text it renders.
    """
    ctx = {
        "stories": stories,
        "targets": {st["merged_into"] for st in stories.values() if st.get("merged_into")},
        "digest": digest or set(),
        "analysis_ids": analysis_ids or set(),
    }
    clean, blocked = _split_candidates(expirable, ctx)
    moving, shared = _split_shared(clean, stories, event_refs(stories))
    blocked.update({sid: "shares an event with a story that stays" for sid in shared})
    kept = {e["event_id"] for sid in moving
            for e in stories[sid].get("events") or [] if e.get("event_id")}
    return moving, sorted(kept), blocked


def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def _manifest_ids(archive_root):
    """Ids already recorded (so a re-run appends nothing)."""
    path = os.path.join(archive_root, "manifest.jsonl")
    done = set()
    if not os.path.exists(path):
        return done
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                done.add(json.loads(line)["id"])
            except (ValueError, KeyError):
                continue
    return done


def _archive_files(sid, st, archive_root):
    """Copy the story record and its exclusive event files; return manifest files."""
    entries = []
    with open(os.path.join(retention.STORIES_DIR, sid + ".json"), "rb") as f:
        raw = f.read()
    rel = f"stories/{sid}.json"
    _write(os.path.join(archive_root, rel), raw)
    entries.append({"path": rel, "sha256": _sha(os.path.join(archive_root, rel))})
    for e in st.get("events") or []:
        eid = e.get("event_id")
        for ext in (".json", ".md"):
            src = os.path.join(EVENTS_DIR, str(eid) + ext)
            if not eid or not os.path.exists(src):
                continue
            with open(src, "rb") as f:
                data = f.read()
            rel = f"events/{eid}{ext}"
            _write(os.path.join(archive_root, rel), data)
            entries.append({"path": rel, "sha256": _sha(os.path.join(archive_root, rel))})
    return entries


def _unlink_story(sid, st):
    """Remove the hot-store originals — only after the manifest line exists."""
    try:
        os.remove(os.path.join(retention.STORIES_DIR, sid + ".json"))
    except OSError:
        pass
    for e in st.get("events") or []:
        for ext in (".json", ".md"):
            try:
                os.remove(os.path.join(EVENTS_DIR, str(e.get("event_id")) + ext))
            except OSError:
                pass


def apply_moves(move, stories, archive_root, tier_of=None):
    """Copy, record, then unlink — in that order, per story.

    A crash between the steps leaves the archive complete and the store
    intact: the copy and manifest line are durable before anything is removed,
    and a re-run skips ids the manifest already names.
    """
    done = _manifest_ids(archive_root)
    manifest = os.path.join(archive_root, "manifest.jsonl")
    for sid in move:
        st = stories[sid]
        if sid not in done:
            line = {"ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "id": sid, "tier": (tier_of or {}).get(sid, ""),
                    "events": [e.get("event_id") for e in st.get("events") or []
                               if e.get("event_id")],
                    "files": _archive_files(sid, st, archive_root)}
            with open(manifest, "a", encoding="utf-8") as f:
                f.write(json.dumps(line, sort_keys=True) + "\n")
        _unlink_story(sid, st)
    print(f"archive: moved {len(move)} story file(s) into {archive_root} "
          f"(manifest {manifest})")
    return len(move)


def _entry_problems(archive_root, entry):
    """Missing file or sha256 drift for one manifest file entry."""
    path = os.path.join(archive_root, entry["path"])
    if not os.path.exists(path):
        return [entry["path"]]
    if _sha(path) != entry["sha256"]:
        return [f"{entry['path']} (sha256 mismatch)"]
    return []


def _record_problems(archive_root, line):
    """(listed id or None, problems) for one manifest line."""
    try:
        rec = json.loads(line)
    except ValueError:
        return None, ["unparseable manifest line"]
    problems = []
    for entry in rec.get("files", []):
        problems += _entry_problems(archive_root, entry)
    return rec.get("id"), problems


def _unlisted_story_files(archive_root, listed):
    """stories/*.json present in the archive but absent from the manifest."""
    stories_dir = os.path.join(archive_root, "stories")
    if not os.path.isdir(stories_dir):
        return []
    return [f"stories/{name}" for name in sorted(os.listdir(stories_dir))
            if name.endswith(".json") and name[:-5] not in listed]


def verify(archive_root):
    """Manifest entries without files (or sha drift), plus unlisted story files."""
    manifest_path = os.path.join(archive_root, "manifest.jsonl")
    if not os.path.exists(manifest_path):
        return ["manifest.jsonl missing"]
    problems, listed = [], set()
    with open(manifest_path, encoding="utf-8") as f:
        for line in f:
            sid, found = _record_problems(archive_root, line)
            problems += found
            if sid:
                listed.add(sid)
    return problems + _unlisted_story_files(archive_root, listed)


def load_archived(archive_root):
    """{id: story} read back from the archive repo (tests + restore)."""
    out = {}
    stories_dir = os.path.join(archive_root, "stories")
    if not os.path.isdir(stories_dir):
        return out
    for name in sorted(os.listdir(stories_dir)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(stories_dir, name), encoding="utf-8") as f:
            out[name[:-5]] = json.load(f)
    return out


def _parser():
    ap = argparse.ArgumentParser(description="archive aged-out stories (dry run by default)")
    ap.add_argument("--archive-root", default=os.environ.get(ARCHIVE_ENV))
    ap.add_argument("--apply", action="store_true", help="copy + remove (default: report only)")
    ap.add_argument("--verify", action="store_true", help="check an existing archive repo")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--today", help="YYYY-MM-DD override (tests)")
    return ap


def _analysis_ids():
    directory = os.path.join(ENGINE, "data", "analysis")
    if not os.path.isdir(directory):
        return set()
    return {os.path.splitext(n)[0] for n in os.listdir(directory)}


def _tier_of(stories):
    return {sid: tier for sid, (tier, _) in retention.classify_all(stories).items()}


def _cmd_verify(args):
    if not args.archive_root:
        print(f"need --archive-root or ${ARCHIVE_ENV}", file=sys.stderr)
        return 2
    problems = verify(args.archive_root)
    print(f"verify {args.archive_root}: {len(problems)} problem(s)")
    for problem in problems[:20]:
        print(f"  {problem}")
    return 0 if not problems else 1


def _candidate_plan(today):
    stories = retention.load_stories()
    expirable = retention.expiring(stories, today=today)["expirable"]
    move, event_ids, blocked = plan(stories, expirable, digest=set(),
                                    analysis_ids=_analysis_ids())
    return stories, expirable, move, event_ids, blocked


def _report(expirable, move, event_ids, blocked):
    print(f"dry run — expirable {len(expirable)}, would move {len(move)} story(ies), "
          f"{len(event_ids)} event file pair(s); blocked {len(blocked)}")
    for sid, why in list(blocked.items())[:5]:
        print(f"  blocked {sid}: {why}")


def _cmd_sweep(args):
    today = date.fromisoformat(args.today) if args.today else None
    stories, expirable, move, event_ids, blocked = _candidate_plan(today)
    if args.json:
        print(json.dumps({"expirable": len(expirable), "would_move": move,
                          "events": len(event_ids), "blocked": blocked}, indent=1))
        return 0
    _report(expirable, move, event_ids, blocked)
    if not args.archive_root:
        print(f"  (set --archive-root or ${ARCHIVE_ENV} to apply)")
        return 0
    if not args.apply:
        return 0
    apply_moves(move, stories, args.archive_root, tier_of=_tier_of(stories))
    return 0


def main(argv=None):
    args = _parser().parse_args(argv)
    return _cmd_verify(args) if args.verify else _cmd_sweep(args)


if __name__ == "__main__":
    raise SystemExit(main())
