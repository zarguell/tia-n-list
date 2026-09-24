#!/usr/bin/env python3
"""Store-health L1 contract suite — social mint bar + orphan tombstones.

The 2026-09 incident: social-collector link-posts minted ~1.6k stories in
one month (2.4x the whole Miniflux category) because merge minted a story
for every unmatched event, and every triage drop that rejected one left its
zero-event shell behind (4,486 by 2026-09-24). This suite pins:

  1. merge._attach_event is the single attach path — updates kind, unions
     sources/cves, extends last_seen/first_seen, and refuses to touch an
     already-placed event (returns False);
  2. merge social-pending helpers round-trip and the park decision is
     prefix-based (masto:/x:/bsky: only — mf:/rd:/plain events still mint);
  3. lifecycle.tombstone_orphans deletes zero-event non-merged shells (dry
     run reports without deleting), spares merged_into redirects and
     digest-referenced ids;
  4. lifecycle.referenced_story_ids finds ids in digest md/json links;
  5. triage._pending_discard removes decided ids and tolerates a
     missing/corrupt pending file;
  6. repair_shells end-to-end on a fixture store (dry run vs --apply).

Run: python3 engine/test_shells.py   (exit 0 = pass)
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lifecycle  # noqa: E402
import merge  # noqa: E402
import triage  # noqa: E402

FAILS = []


def check(name, cond):
    print(("  ok  " if cond else "  FAIL") + f" {name}")
    if not cond:
        FAILS.append(name)


# --- 1: _attach_event -------------------------------------------------------
merge.story_url_cache = {}
s = {"id": "story-a", "title": "t", "sources": ["a.com"], "n_sources": 1,
     "cves": ["CVE-2026-0001"], "first_seen": "2026-09-20T00:00:00Z",
     "last_seen": "2026-09-20T00:00:00Z",
     "events": [{"event_id": "mf:1", "label": "original"}]}
ev = {"id": "mf:2", "published_at": "2026-09-21T10:00:00Z",
      "url": "https://b.com/x", "cves": ["CVE-2026-0002"]}
check("attach returns True and appends",
      merge._attach_event("mf:2", ev, s) and
      s["events"][-1]["event_id"] == "mf:2" and ev["kind"] == "update")
check("sources/cves unioned, n_sources derived",
      s["sources"] == ["a.com", "b.com"] and s["n_sources"] == 2
      and s["cves"] == ["CVE-2026-0001", "CVE-2026-0002"])
check("last_seen extended, first_seen kept",
      s["last_seen"] == "2026-09-21T10:00:00Z"
      and s["first_seen"] == "2026-09-20T00:00:00Z")
check("url cached for future matching",
      merge.norm_url("https://b.com/x") in merge.story_url_cache.get("story-a", set()))
check("re-attach refused (already placed)",
      merge._attach_event("mf:2", ev, s) is False)

# --- 2: pending helpers + prefix set ---------------------------------------
with tempfile.TemporaryDirectory() as td:
    merge.PENDING = os.path.join(td, "social-pending.json")
    check("load missing pending -> []", merge._load_pending() == [])
    merge._save_pending([{"id": "masto:1", "since": "2026-09-21T00:00:00Z"}])
    check("pending round-trip",
          merge._load_pending() == [{"id": "masto:1",
                                     "since": "2026-09-21T00:00:00Z"}])
check("collector prefixes are the park set",
      merge.SOCIAL_PREFIXES == ("masto:", "x:", "bsky:"))
check("feed prefixes not parked",
      not any(e.startswith(merge.SOCIAL_PREFIXES)
              for e in ("mf:159825", "rd:t3_abc", "evt-123")))

# --- 3/4: lifecycle tombstones + referenced ids ----------------------------
with tempfile.TemporaryDirectory() as td:
    stories_dir = os.path.join(td, "stories")
    digests_dir = os.path.join(td, "digests")
    os.makedirs(stories_dir)
    os.makedirs(digests_dir)
    lifecycle.STORIES = stories_dir
    lifecycle.DIGESTS = digests_dir

    def write(sid, body):
        json.dump(body, open(os.path.join(stories_dir, sid + ".json"), "w"),
                  indent=1)

    write("shell-1", {"id": "shell-1", "events": []})
    write("shell-2", {"id": "shell-2", "events": []})
    write("redirect", {"id": "redirect", "merged_into": "live",
                       "events": []})
    write("live", {"id": "live", "n_sources": 2,
                   "events": [{"event_id": "mf:1", "label": "original"}]})
    open(os.path.join(digests_dir, "2026-09-23.md"), "w").write(
        "see [the story](/stories/shell-2/) and "
        "(stories/live) for details")

    referenced = lifecycle.referenced_story_ids()
    check("digest links (slash and bare md forms) resolved",
          {"shell-2", "live"} <= referenced)

    removed = lifecycle.tombstone_orphans({}, referenced=referenced,
                                          dry_run=True)
    stories = {sid: json.load(open(os.path.join(stories_dir, sid + ".json")))
               for sid in ("shell-1", "shell-2", "redirect", "live")}
    removed = lifecycle.tombstone_orphans(stories, referenced=referenced,
                                          dry_run=True)
    check("dry run reports unreferenced shells only",
          removed == ["shell-1"])
    check("dry run deletes nothing",
          len(glob.glob(os.path.join(stories_dir, "*.json"))) == 4)
    removed = lifecycle.tombstone_orphans(stories, referenced=referenced)
    check("apply removes exactly shell-1", removed == ["shell-1"])
    check("file gone for tombstoned shell",
          not os.path.exists(os.path.join(stories_dir, "shell-1.json")))
    check("redirect shell spared",
          os.path.exists(os.path.join(stories_dir, "redirect.json")))
    check("digest-referenced shell spared",
          os.path.exists(os.path.join(stories_dir, "shell-2.json")))
    check("memory dict shrunk too", "shell-1" not in stories)

# --- 5: triage._pending_discard --------------------------------------------
with tempfile.TemporaryDirectory() as td:
    triage.PENDING = os.path.join(td, "social-pending.json")
    json.dump([{"id": "masto:1"}, {"id": "masto:2"}, {"id": "x:9"}],
              open(triage.PENDING, "w"))
    triage._pending_discard(["masto:1", "x:9", "never-there"])
    check("decided ids removed",
          triage._pending_discard and json.load(open(triage.PENDING))
          == [{"id": "masto:2"}])
    os.remove(triage.PENDING)
    triage._pending_discard(["masto:1"])          # must not raise
    check("missing pending file tolerated", True)
    open(triage.PENDING, "w").write("{corrupt")
    triage._pending_discard(["masto:1"])          # must not raise
    check("corrupt pending file tolerated", True)

# --- 6: repair_shells end-to-end -------------------------------------------
with tempfile.TemporaryDirectory() as td:
    engine_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_engine = os.path.join(td, "engine")
    os.makedirs(os.path.join(tmp_engine, "data"))
    os.symlink(stories_dir := os.path.join(td, "store"),
               os.path.join(tmp_engine, "data", "stories"))
    os.makedirs(stories_dir)
    for sid in ("gone", "kept-redirect"):
        json.dump({"id": sid, "events": [], **({"merged_into": "x"}
                   if sid == "kept-redirect" else {})},
                  open(os.path.join(stories_dir, sid + ".json"), "w"))
    for f in ("repair_shells.py", "lifecycle.py"):
        shutil.copy(os.path.join(engine_dir, f),
                    os.path.join(tmp_engine, f))
    r = subprocess.run([sys.executable,
                        os.path.join(tmp_engine, "repair_shells.py")],
                       capture_output=True, text=True)
    check("repair dry run exits 0", r.returncode == 0)
    check("dry run leaves files",
          os.path.exists(os.path.join(stories_dir, "gone.json")))
    r = subprocess.run([sys.executable,
                        os.path.join(tmp_engine, "repair_shells.py"),
                        "--apply"], capture_output=True, text=True)
    check("repair --apply exits 0", r.returncode == 0)
    check("orphan removed, redirect kept",
          not os.path.exists(os.path.join(stories_dir, "gone.json"))
          and os.path.exists(os.path.join(stories_dir, "kept-redirect.json")))

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} check(s): {', '.join(FAILS)}")
    sys.exit(1)
print("all store-health L1 contract checks passed")
