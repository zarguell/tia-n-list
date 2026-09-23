"""Determinism tests for engine/snapshots.py (2026-09-22 audit: snapshot_pin
MISMATCH — duplicate (type, name) STIX objects preserved records-dict
insertion order through the sort, and that order follows unsorted glob
order in load_records, so every build hashed differently)."""
import hashlib
import json
import os
import random
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import snapshots


def _records():
    # Two stories naming the same malware/actor, like the real CTI data
    # (ShinyHunters x6, Contagious Interview x5, ...).
    def rec(sid, attack):
        return {"attack": attack, "malware": ["Vidar"],
                "campaigns": ["Contagious Interview"],
                "actors": ["ShinyHunters"], "confidence": "reviewed",
                "updated_at": "2026-09-22T10:00:00Z"}
    return {
        "story-b": rec("story-b", [{"id": "T1190"}]),
        "story-a": rec("story-a", [{"id": "T1068"}]),
        "story-c": rec("story-c", [{"id": "T1190"}, {"id": "T1068"}]),
    }


def _iocs():
    return [{"type": "ipv4", "value": "1.2.3.4",
             "first_seen": "2026-09-20", "last_seen": "2026-09-22",
             "status": "active", "confidence": "corroborated",
             "n_sources": 2, "stories": ["story-a"]}]


def _bundle(records):
    return snapshots.build_bundle(_iocs(), records, "https://x/", "2026-09-22")


def _sha(bundle):
    return hashlib.sha256(json.dumps(bundle, indent=1).encode()).hexdigest()


def test_build_bundle_deterministic_under_record_reordering():
    """Same records, five shuffled insertion orders -> byte-identical hash."""
    hashes = set()
    items = list(_records().items())
    for seed in range(5):
        shuffled = dict(random.Random(seed).sample(items, len(items)))
        hashes.add(_sha(_bundle(shuffled)))
    assert len(hashes) == 1, f"non-deterministic bundle: {hashes}"


def test_build_bundle_sort_is_total():
    """No two adjacent objects tie on the full sort key (type, name, id)."""
    bundle = _bundle(_records())
    keys = [(o["type"], o.get("name", ""), o["id"]) for o in bundle["objects"]]
    assert keys == sorted(keys)
    assert len(set(keys)) == len(keys)


def test_write_snapshot_manifest_matches_bundle_file():
    """Manifest pin matches the deployed bytes (the audit's exact check)."""
    tmp = tempfile.mkdtemp()
    out = os.path.join(tmp, "2026-09-22")
    manifest = snapshots.write_snapshot(_iocs(), _records(),
                                        "https://x/", out, "2026-09-22")
    raw = open(os.path.join(out, "stix-bundle.json")).read()
    assert hashlib.sha256(raw.encode()).hexdigest() == \
        manifest["files"]["stix-bundle.json"]["sha256"]


if __name__ == "__main__":
    test_build_bundle_deterministic_under_record_reordering()
    test_build_bundle_sort_is_total()
    test_write_snapshot_manifest_matches_bundle_file()
    print("test_snapshots: 3 passed")
