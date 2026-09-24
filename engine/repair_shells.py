#!/usr/bin/env python3
"""One-time orphaned-shell repair for the story store (store-health L1).

The 2026-05..09 era left thousands of shells behind: drops stripped the
last event from a minted candidate and its json rode every hourly commit
forever (~4.5k shells by 2026-09-24). This removes them store-wide.
Deliberately a standalone sweep, not a triage.apply() step: apply runs
inside cronman's guarded tia-agent stage, where _restore_deleted_data
restores any tracked deletion and records agent-deleted-tracked-data
(engine/lifecycle.tombstone_orphans docstring has the incident detail).
Run this between the guard and the publish (or let the deletions ride the
next publish commit) — never leave a swept tree to be restored from HEAD.

Shells never rendered a page (SSG skips orphaned stories), so no published
URL is affected; digest-referenced ids are spared and reported.
merged_into redirect shells are NOT orphans and are kept.

Dry run by default; --apply writes.

Usage: python3 engine/repair_shells.py [--apply]
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lifecycle  # noqa: E402


def main():
    apply = "--apply" in sys.argv
    stories = {}
    for p in sorted(glob.glob(os.path.join(lifecycle.STORIES, "*.json"))):
        sid = os.path.basename(p)[:-5]
        try:
            stories[sid] = json.load(open(p))
        except Exception as e:
            print(f"WARN: skipping corrupt story {p}: {e}")
    removed = lifecycle.tombstone_orphans(stories, dry_run=not apply)
    print(f"repair_shells: {len(removed)} orphaned shell(s) "
          f"{'removed' if apply else 'WOULD be removed (dry run)'}")
    for sid in removed[:20]:
        print(f"  - {sid}")
    if len(removed) > 20:
        print(f"  … and {len(removed) - 20} more")
    if not apply:
        print("dry run: re-run with --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
