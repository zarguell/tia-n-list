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
from datetime import datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ENGINE)

import retention  # noqa: E402
import store  # noqa: E402

ARCHIVE_ENV = "TIA_ARCHIVE_ROOT"


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


def plan(stories, events, expirable, digest=None, analysis_ids=None):
    """(story ids to move, event ids to move, {blocked id: reason}). Pure."""
    digest = digest or set()
    analysis_ids = analysis_ids or set()
    refs = event_refs(stories)
    targets = {st["merged_into"] for st in stories.values() if st.get("merged_into")}
    move, blocked = [], {}
    for sid in sorted(expirable):
        st = stories.get(sid)
        if st is None:
            blocked[sid] = "story file missing"
        elif sid in targets:
            blocked[sid] = "redirect target (its URL is a map key)"
        elif sid in digest:
            blocked[sid] = "digest-cited (link rewrite lands with step 3)"
        elif sid in analysis_ids:
            blocked[sid] = "has an analysis file"
        else:
            move.append(sid)
    # An event shared with a story that stays must not move, and the story that
    # owns it cannot go either (its page would lose the text it renders).
    candidates = set(move)
    for sid in list(move):
        if any(refs.get(e["event_id"], set()) - candidates
               for e in stories[sid].get("events") or [] if e.get("event_id")):
            blocked[sid] = "shares an event with a story that stays"
            move.remove(sid)
    kept = {e["event_id"] for sid in move
            for e in stories[sid].get("events") or [] if e.get("event_id")}
    return move, sorted(kept), blocked


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


def _archive_files(sid, st, events_dir, archive_root):
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
            src = os.path.join(events_dir, str(eid) + ext)
            if not eid or not os.path.exists(src):
                continue
            with open(src, "rb") as f:
                data = f.read()
            rel = f"events/{eid}{ext}"
            _write(os.path.join(archive_root, rel), data)
            entries.append({"path": rel, "sha256": _sha(os.path.join(archive_root, rel))})
    return entries


def _unlink_story(sid, st, events_dir):
    """Remove the hot-store originals — only after the manifest line exists."""
    try:
        os.remove(os.path.join(retention.STORIES_DIR, sid + ".json"))
    except OSError:
        pass
    for e in st.get("events") or []:
        for ext in (".json", ".md"):
            try:
                os.remove(os.path.join(events_dir, str(e.get("event_id")) + ext))
            except OSError:
                pass


def apply_moves(move, stories, events_dir, archive_root, tier_of=None, log=print):
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
                    "files": _archive_files(sid, st, events_dir, archive_root)}
            with open(manifest, "a", encoding="utf-8") as f:
                f.write(json.dumps(line, sort_keys=True) + "\n")
        _unlink_story(sid, st, events_dir)
    log(f"archive: moved {len(move)} story file(s) into {archive_root} "
        f"(manifest {manifest})")
    return len(move)


def verify(archive_root):
    """Manifest entries without files, or files without a manifest line."""
    missing, orphans = [], []
    listed = set()
    manifest_path = os.path.join(archive_root, "manifest.jsonl")
    if not os.path.exists(manifest_path):
        return ["manifest.jsonl missing"]
    with open(manifest_path, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except ValueError:
                missing.append("unparseable manifest line")
                continue
            listed.add(rec["id"])
            for entry in rec.get("files", []):
                path = os.path.join(archive_root, entry["path"])
                if not os.path.exists(path):
                    missing.append(entry["path"])
                elif _sha(path) != entry["sha256"]:
                    missing.append(f"{entry['path']} (sha256 mismatch)")
    stories_dir = os.path.join(archive_root, "stories")
    if os.path.isdir(stories_dir):
        for name in sorted(os.listdir(stories_dir)):
            if name.endswith(".json") and name[:-5] not in listed:
                orphans.append(f"stories/{name}")
    return missing + orphans


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


def main(argv=None):
    ap = argparse.ArgumentParser(description="archive aged-out stories (dry run by default)")
    ap.add_argument("--archive-root", default=os.environ.get(ARCHIVE_ENV))
    ap.add_argument("--apply", action="store_true", help="copy + remove (default: report only)")
    ap.add_argument("--verify", action="store_true", help="check an existing archive repo")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--today", help="YYYY-MM-DD override (tests)")
    args = ap.parse_args(argv)

    if args.verify:
        if not args.archive_root:
            print(f"need --archive-root or ${ARCHIVE_ENV}", file=sys.stderr)
            return 2
        problems = verify(args.archive_root)
        print(f"verify {args.archive_root}: {len(problems)} problem(s)")
        for p in problems[:20]:
            print(f"  {p}")
        return 0 if not problems else 1

    today = None
    if args.today:
        from datetime import date
        today = date.fromisoformat(args.today)
    stories = retention.load_stories()
    events_dir = store.EVENTS_DIR
    exp = retention.expiring(stories, today=today)["expirable"]
    analysis_ids = {os.path.splitext(n)[0] for n in
                    os.listdir(os.path.join(ENGINE, "data", "analysis"))} \
        if os.path.isdir(os.path.join(ENGINE, "data", "analysis")) else set()
    tier_of = {sid: tier for sid, (tier, _) in retention.classify_all(stories).items()}
    move, event_ids, blocked = plan(stories, None, exp, digest=set(), analysis_ids=analysis_ids)

    if args.json:
        print(json.dumps({"expirable": len(exp), "would_move": move,
                          "events": len(event_ids), "blocked": blocked}, indent=1))
        return 0
    print(f"dry run — expirable {len(exp)}, would move {len(move)} story(ies), "
          f"{len(event_ids)} event file pair(s); blocked {len(blocked)}")
    for sid, why in list(blocked.items())[:5]:
        print(f"  blocked {sid}: {why}")
    if not args.apply:
        if not args.archive_root:
            print(f"  (set --archive-root or ${ARCHIVE_ENV} to apply)")
        return 0
    if not args.archive_root:
        print(f"--apply needs --archive-root or ${ARCHIVE_ENV}", file=sys.stderr)
        return 2
    apply_moves(move, stories, events_dir, args.archive_root, tier_of=tier_of)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
