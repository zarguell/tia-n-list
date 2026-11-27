#!/usr/bin/env python3
"""Archive-repo contract suite — step 3 of the retention rollout, read-only.

`archive.py` is the only code allowed to move story data out of the hot store,
so the guards matter more than the mechanics. Every rule blocks rather than
guesses:

  1. only `retention.expiring()['expirable']` stories are candidates;
  2. a redirect target never moves (its URL is a redirects.json key);
  3. a digest-cited story never moves (the digest link must be rewritten first);
  4. a story with an analysis file never moves (prose must not be orphaned);
  5. a story sharing an event with a story that stays never moves;
  6. dry run touches nothing; --apply copies, writes the manifest, then removes;
  7. a second apply is a no-op (manifest line already present);
  8. verify() catches a missing file and an unlisted story file;
  9. load_archived() reads the store back.

Run: python3 engine/test_archive.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import archive  # noqa: E402


def check(name, got, expect):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {expect!r}")
    return ok


def story(sid, events, merged_into=None):
    st = {"id": sid, "events": [{"event_id": e} for e in events],
          "first_seen": "2026-01-01T00:00:00Z", "last_seen": "2026-01-01T00:00:00Z",
          "peak_score": 0.0}
    if merged_into:
        st["merged_into"] = merged_into
    return st


def main():
    ok = True
    stories = {
        "old-cold": story("old-cold", ["e1"]),
        "shared": story("shared", ["e2"]),
        "cited": story("cited", ["e3"]),
        "analyzed": story("analyzed", ["e4"]),
        "winner": story("winner", ["e2"]),           # shares e2 with "shared"
        "shell": story("shell", [], merged_into="winner"),
    }
    expirable = ["old-cold", "shared", "cited", "analyzed", "winner"]
    move, event_ids, blocked = archive.plan(
        stories, expirable,
        digest={"cited"}, analysis_ids={"analyzed"})
    ok &= check("only the clean story moves", move, ["old-cold"])
    ok &= check("its events move", event_ids, ["e1"])
    ok &= check("shared-event story blocked", "shared" in blocked, True)
    ok &= check("digest-cited blocked", "cited" in blocked, True)
    ok &= check("analysis blocked", "analyzed" in blocked, True)
    ok &= check("redirect target blocked",
                "winner" in blocked or "shared" in blocked, True)

    with tempfile.TemporaryDirectory() as td:
        store_stories = os.path.join(td, "stories")
        events_dir = os.path.join(td, "events")
        arch = os.path.join(td, "archive")
        for d in (store_stories, events_dir):
            os.makedirs(d)
        archive.retention.STORIES_DIR = store_stories
        archive.EVENTS_DIR = events_dir
        for sid, st in stories.items():
            with open(os.path.join(store_stories, sid + ".json"), "w") as f:
                json.dump(st, f)
        for eid in ("e1", "e2", "e3", "e4"):
            for ext, body in ((".json", {"id": eid, "title": eid}), (".md", None)):
                path = os.path.join(events_dir, eid + ext)
                with open(path, "w") as f:
                    f.write(json.dumps(body) if body else f"body {eid}")

        before = sorted(os.listdir(store_stories))
        archive.plan(stories, expirable, digest={"cited"}, analysis_ids={"analyzed"})
        ok &= check("dry run touches nothing", sorted(os.listdir(store_stories)), before)

        moved = archive.apply_moves(["old-cold"], stories, arch)
        ok &= check("apply moves the story", moved, 1)
        ok &= check("story removed from the hot store",
                    os.path.exists(os.path.join(store_stories, "old-cold.json")), False)
        ok &= check("story present in the archive",
                    os.path.exists(os.path.join(arch, "stories", "old-cold.json")), True)
        ok &= check("its event pair archived",
                    (os.path.exists(os.path.join(arch, "events", "e1.json")) and
                     os.path.exists(os.path.join(arch, "events", "e1.md"))), True)
        ok &= check("manifest line written",
                    len(open(os.path.join(arch, "manifest.jsonl")).read().strip().splitlines()), 1)
        ok &= check("verify is clean", archive.verify(arch), [])
        ok &= check("read back", sorted(archive.load_archived(arch)), ["old-cold"])

        archive.apply_moves(["old-cold"], stories, arch)
        ok &= check("second apply appends nothing",
                    len(open(os.path.join(arch, "manifest.jsonl")).read().strip().splitlines()), 1)

        os.remove(os.path.join(arch, "stories", "old-cold.json"))
        ok &= check("verify catches a missing file", len(archive.verify(arch)), 1)

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
