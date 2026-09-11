#!/usr/bin/env python3
"""cleanup_ghosts contract suite (2026-09-11).

Ghosts (eventless, non-redirect stories) render no page, so they are dead
weight once nothing points at them. This pins the delete-safety gate: keep
anything referenced by a digest/CTI/queue, any redirect target, any live
story, and (by default) any story that still has an analysis.

Run: python3 engine/test_cleanup_ghosts.py   (exit 0 = pass)
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cleanup_ghosts as cg  # noqa: E402

NOW = datetime(2026, 9, 11, tzinfo=timezone.utc)
failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


def mkstory(root, sid, **kw):
    st = {"id": sid, "title": sid, "events": [], "first_seen": "2026-01-01T00:00:00Z",
          "last_seen": "2026-01-01T00:00:00Z", "sources": [], "n_sources": 0, "cves": []}
    st.update(kw)
    with open(os.path.join(root, "stories", sid + ".json"), "w") as fh:
        json.dump(st, fh)


def setup():
    root = tempfile.mkdtemp()
    for d in ("stories", "analysis", "digests", "cti"):
        os.makedirs(os.path.join(root, d))
    mkstory(root, "ghost-old")                                   # deletable
    mkstory(root, "ghost-young", first_seen="2026-09-10T00:00:00Z",
            last_seen="2026-09-10T00:00:00Z")                    # too fresh
    mkstory(root, "ghost-ref")                                   # digest ref
    mkstory(root, "ghost-ana")                                   # has analysis
    mkstory(root, "ghost-target")                                # redirect target
    mkstory(root, "ghost-cti")                                   # cti record
    mkstory(root, "ghost-queue")                                 # cti-queue
    mkstory(root, "live", events=[{"event_id": "e1", "label": "original"}])
    mkstory(root, "shell", merged_into="ghost-target")           # not a ghost
    with open(os.path.join(root, "digests", "2026-09-01.md"), "w") as fh:
        fh.write("see [x](stories/ghost-ref/) for detail\n")
    with open(os.path.join(root, "analysis", "ghost-ana.md"), "w") as fh:
        fh.write("analysis body\n")
    with open(os.path.join(root, "cti", "rec.json"), "w") as fh:
        json.dump({"story_id": "ghost-cti"}, fh)
    with open(os.path.join(root, "cti-queue.json"), "w") as fh:
        json.dump({"stories": [{"id": "ghost-queue", "title": "q"}]}, fh)
    with open(os.path.join(root, "needs-analysis.json"), "w") as fh:
        json.dump({"stories": []}, fh)
    return root


root = setup()
deletable, stats = cg.find_ghosts(root, days=90, now=NOW)
check("only the old unreferenced ghost is deletable",
      [sid for _, sid in deletable], ["ghost-old"])
check("ghost census", stats, {"ghosts": 7, "referenced": 4, "analyzed": 1, "young": 1})
check("live story and redirect shell are not ghosts", stats["ghosts"], 7)

deletable, stats = cg.find_ghosts(root, days=90, include_analyzed=True, now=NOW)
check("include-analyzed frees the analyzed ghost",
      [sid for _, sid in deletable], ["ghost-ana", "ghost-old"])
check("analyzed counter zeroed when included", stats["analyzed"], 0)

deletable, stats = cg.find_ghosts(root, days=0, now=NOW)
check("days=0 frees the fresh ghost too",
      [sid for _, sid in deletable], ["ghost-old", "ghost-young"])

check("undated story counts as old",
      cg.age_days({"first_seen": "", "last_seen": ""}, NOW) > 10 ** 5, True)
check("age uses the newer of first/last seen",
      cg.age_days({"first_seen": "2026-01-01T00:00:00Z",
                   "last_seen": "2026-08-01T00:00:00Z"}, NOW), 41.0)

# dry-run through main() must not delete
sys.argv = ["cleanup_ghosts.py", "--dry-run", "--days", "90"]
cg.DATA = root
cg.main()
check("dry-run leaves files in place",
      os.path.exists(os.path.join(root, "stories", "ghost-old.json")), True)

sys.argv = ["cleanup_ghosts.py", "--days", "90"]
cg.main()
check("real run removes the ghost",
      os.path.exists(os.path.join(root, "stories", "ghost-old.json")), False)
check("real run keeps the referenced ghost",
      os.path.exists(os.path.join(root, "stories", "ghost-ref.json")), True)

print()
if failures:
    print(f"FAIL: {len(failures)} cleanup_ghosts checks failed")
    sys.exit(1)
print("ALL PASS")
