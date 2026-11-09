#!/usr/bin/env python3
"""Contract of store.write_json: readers never observe a partial record.

The store is read and written concurrently all day (hourly merge and triage
apply rewrite story json while ssg, cti_pass and audit read it). A plain
`json.dump(obj, open(path, "w"))` truncates the file before writing, so a
reader can catch a zero-length record and die with
`JSONDecodeError: Expecting value: line 1 column 1`, which aborted the
publishing job on 2026-11-01 (cti), 2026-11-05 (cti) and 2026-11-09
(story-desk, `ABORT: ssg failed, not pushing`).

This test is the pin: one thread rewrites the record in a tight loop, one
thread reads it back, and every read must parse and carry a complete payload.
"""
import json
import os
import sys
import tempfile
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from store import write_json

WRITER_RUNS = 300


def main():
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "story.json")
    payload = {"id": "story", "events": [{"event_id": f"e{i}"} for i in range(50)]}
    write_json(path, payload)

    torn = []
    stop = threading.Event()

    def reader():
        while not stop.is_set():
            try:
                with open(path) as fh:
                    json.load(fh)
            except ValueError as exc:      # JSONDecodeError on a truncated file
                torn.append(repr(exc))

    t = threading.Thread(target=reader, daemon=True)
    t.start()
    for i in range(WRITER_RUNS):
        write_json(path, dict(payload, generation=i))
    stop.set()
    t.join()

    leftovers = [f for f in os.listdir(tmpdir) if f.endswith(".tmp")]
    print(f"reads torn: {len(torn)} (want 0)")
    print(f"temp files left behind: {leftovers} (want [])")
    print(f"final record generation: {json.load(open(path))['generation']} "
          f"(want {WRITER_RUNS - 1})")
    ok = not torn and not leftovers \
        and json.load(open(path))["generation"] == WRITER_RUNS - 1
    print("ALL PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
