#!/usr/bin/env python3
"""Story desk — deterministic queue + apply for deep-dive passes.

The pipeline had hourly ingest, a daily digest, and a conservative CTI
pass, but nothing that went DEEP on a single story: backfilling the
history it missed, or writing the deliberate post a hot story deserves
(the Threadlinqs comparison, 2026-09-24: they carried June GreyNoise
telemetry for a CVE we first touched on KEV day).

This module is the deterministic half; the LLM worker lives in cronman
(jobs/story_desk.py, free-model ladder). Contract:

  build          recompute engine/data/desk-queue.json from triggers
  take N         pop the top N stories into a batch file (stdout: JSON)
  apply <sid>    validate the worker's sidecar, create backfill events,
                 mark the story reviewed, drop it from the queue

Triggers (one-shot per story via the desk_reviewed_at marker):
  crossover   score >= 5.0 — the editorial line: hot gets a written post
  kev         a story CVE joined CISA KEV in the last 2 days
  late-birth  story born >= 14d after its earliest CVE's NVD disclosure
              (warm+ only — the cold tier already excludes the rest)

Backfill events carry their TRUE published date (kind/label "backfill"),
so the timeline reads honestly — ssg sorts events by published_at, and a
June advisory lands where it belongs. Story first_seen/last_seen are
coverage-bookkeeping and deliberately untouched. Agent output is a
SCHEMA'D SIDECAR, never direct store edits — the same contract as triage
decisions: the deterministic engine applies, the agent only judges.

Usage:
  python3 engine/desk_queue.py build
  python3 engine/desk_queue.py take 4
  python3 engine/desk_queue.py apply <story-id>
"""
import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lifecycle  # noqa: E402
import store as store_mod  # noqa: E402

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
STORIES = os.path.join(DATA, "stories")
EVENTS = os.path.join(DATA, "events")
DESK_DIR = os.path.join(DATA, "desk")
QUEUE = os.path.join(DATA, "desk-queue.json")

HOT_LINE = 5.0            # the editorial line: hot gets a written post
KEV_RECENT_DAYS = 2
LATE_BIRTH_DAYS = 14
WARM_FLOOR = 3.3          # late-birth candidates must at least be warm
QUEUE_CAP = 60

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_queue():
    try:
        d = json.load(open(QUEUE))
        return d if isinstance(d, dict) else {"stories": []}
    except (OSError, ValueError):
        return {"stories": []}


def _save_queue(q):
    json.dump(q, open(QUEUE, "w"), indent=1)


def _kev_dates():
    """cve -> KEV dateAdded, from the kevrichment index (kev.py's source)."""
    out = {}
    idx = os.path.normpath(os.path.join(ENGINE, "..", "kevrichment",
                                        "data", "index.json"))
    try:
        for e in json.load(open(idx)).get("cves", []):
            if isinstance(e, dict) and e.get("cve_id") and e.get("kev_date_added"):
                out[e["cve_id"]] = e["kev_date_added"]
    except (OSError, ValueError):
        pass
    return out


def _cve_published():
    """cve -> NVD published date, from the per-CVE enrichment records."""
    out = {}
    for p in glob.glob(os.path.join(ENGINE, "..", "kevrichment", "data",
                                    "cves", "*.json")):
        try:
            d = json.load(open(p))
        except (OSError, ValueError):
            continue
        if d.get("cve_id") and d.get("cve_published"):
            out[d["cve_id"]] = d["cve_published"][:10]
    return out


def _days_between(iso_a, iso_b):
    """Whole days iso_a -> iso_b (negative when b precedes a). Never raises."""
    def d(iso):
        try:
            return datetime.fromisoformat(iso[:10]).date()
        except (ValueError, TypeError):
            return None
    a, b = d(iso_a), d(iso_b)
    if not a or not b:
        return None
    return (a - b).days


def compute_queue(stories, kev_dates, cve_pub, today, frozen=None):
    """Pure trigger evaluation -> sorted queue entries. Frozen and merged
    stories never queue; the desk does not resurrect the cold tier."""
    frozen = frozen if frozen is not None else lifecycle.frozen_ids()
    today = today or _now_iso()[:10]
    entries = []
    for sid, s in stories.items():
        if s.get("merged_into") or sid in frozen:
            continue
        if s.get("desk_reviewed_at"):
            continue                      # one-shot: the desk already went
        reasons = []
        if float(s.get("score") or 0) >= HOT_LINE:
            reasons.append("crossover")
        for c in (s.get("cves") or []):
            kd = kev_dates.get(c)
            if kd and _days_between(today, kd) is not None \
                    and 0 <= _days_between(today, kd) <= KEV_RECENT_DAYS:
                reasons.append("kev")
                break
        if not reasons:
            age_gap = None
            for c in (s.get("cves") or []):
                pub = cve_pub.get(c)
                if pub:
                    gap = _days_between(s.get("first_seen", ""), pub)
                    if gap is not None and (age_gap is None or gap > age_gap):
                        age_gap = gap
            if age_gap is not None and age_gap >= LATE_BIRTH_DAYS \
                    and float(s.get("peak_score") or 0) >= WARM_FLOOR:
                reasons.append("late-birth")
        if reasons:
            entries.append({"id": sid, "reasons": reasons,
                            "score": float(s.get("score") or 0)})
    entries.sort(key=lambda e: (0 if "kev" in e["reasons"] else 1, -e["score"]))
    return entries[:QUEUE_CAP]


def _load_stories_raw():
    """Active story dicts by id (raw store read; merged/frozen filtered in
    compute_queue)."""
    out = {}
    for p in glob.glob(os.path.join(STORIES, "*.json")):
        try:
            s = json.load(open(p))
        except (OSError, ValueError):
            continue
        if isinstance(s, dict) and s.get("id"):
            out[s["id"]] = s
    return out


def build():
    q = {"updated": _now_iso(),
         "stories": compute_queue(_load_stories_raw(), _kev_dates(),
                                  _cve_published(), _now_iso()[:10])}
    _save_queue(q)
    by = {}
    for e in q["stories"]:
        for r in e["reasons"]:
            by[r] = by.get(r, 0) + 1
    print("desk queue: {} stories ({})".format(
        len(q["stories"]),
        ", ".join(f"{k} {v}" for k, v in sorted(by.items())) or "none"))
    return q


def take(n):
    q = _load_queue()
    batch, rest = q["stories"][:n], q["stories"][n:]
    q["stories"] = rest
    _save_queue(q)
    os.makedirs(DESK_DIR, exist_ok=True)
    ts = _now_iso().replace(":", "").replace("-", "")
    path = os.path.join(DESK_DIR, f"batch-{ts}.json")
    json.dump(batch, open(path, "w"), indent=1)
    print(json.dumps(batch))
    return batch


def _validate_finding(f):
    """A backfill finding must be fully sourced and time-sane. Returns a
    violation string or None."""
    if not isinstance(f, dict):
        return "finding is not an object"
    for k in ("title", "published_at", "url", "source_domain", "summary_md"):
        if not str(f.get(k) or "").strip():
            return f"missing field {k}"
    if not re.match(r"^\d{4}-\d{2}-\d{2}T", f["published_at"]):
        return f"bad published_at {f['published_at']!r}"
    try:
        dt = datetime.fromisoformat(f["published_at"].replace("Z", "+00:00"))
    except ValueError:
        return f"unparseable published_at {f['published_at']!r}"
    if dt > datetime.now(timezone.utc):
        return f"published_at in the future: {f['published_at']}"
    if not str(f["url"]).lower().startswith(("http://", "https://")):
        return f"unsafe url {f['url']!r}"
    return None


def _insert_chronological(story, ref, ev):
    """Insert an event ref among the story's updates in true-date order —
    the ORIGINAL stays first (it is what we ingested first), backfills slot
    by their real date so the timeline reads June-before-September."""
    others = [r for r in story["events"] if r is not ref]
    def pub(r):
        try:
            with open(os.path.join(EVENTS, r["event_id"] + ".json")) as f:
                return json.load(f).get("published_at", "")
        except (OSError, ValueError):
            return ""
    tail = others[1:] + [ref]
    tail.sort(key=lambda r: pub(r) or "9999")
    story["events"] = others[:1] + tail


def apply(sid):
    """Validate + apply the worker's sidecar for one story. Deterministic:
    the agent never touches the store directly. Marks desk_reviewed_at even
    with no findings (an honest empty result IS the deliverable)."""
    sp = os.path.join(STORIES, sid + ".json")
    if not os.path.exists(sp):
        print(f"applied {sid}: story missing — skipped")
        return
    story = json.load(open(sp))
    side = os.path.join(DESK_DIR, sid + ".backfill.json")
    created = 0
    if os.path.exists(side):
        try:
            findings = json.load(open(side)).get("findings") or []
        except ValueError as e:
            print(f"applied {sid}: REJECTED sidecar ({e}) — left queued")
            return
        for i, f in enumerate(findings):
            v = _validate_finding(f)
            if v:
                print(f"applied {sid}: REJECTED finding {i} ({v}) — "
                      f"left queued")
                return
        for f in findings:
            h = hashlib.sha1(
                (f["url"] + f["published_at"]).encode()).hexdigest()[:12]
            eid = f"desk:{h}"
            meta = {"id": eid, "title": f["title"].strip(),
                    "url": store_mod.safe_url(f["url"]),
                    "source": f["source_domain"].strip(),
                    "published_at": f["published_at"], "kind": "backfill",
                    "lang": "en", "cves": [], "added_at": _now_iso()}
            if not meta["url"]:
                continue                  # scheme-filtered out
            json.dump(meta, open(os.path.join(EVENTS, eid + ".json"), "w"),
                      indent=1)
            with open(os.path.join(EVENTS, eid + ".md"), "w") as fh:
                fh.write(f["summary_md"].strip() + "\n")
            ref = {"event_id": eid, "label": "backfill"}
            if not any(r["event_id"] == eid for r in story.get("events", [])):
                _insert_chronological(story, ref, meta)
                created += 1
    story["desk_reviewed_at"] = _now_iso()
    json.dump(story, open(sp, "w"), indent=1)
    q = _load_queue()
    q["stories"] = [e for e in q.get("stories", []) if e.get("id") != sid]
    _save_queue(q)
    print(f"applied {sid}: {created} backfill event(s)")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build":
        build()
    elif cmd == "take":
        take(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif cmd == "apply":
        if len(sys.argv) < 3:
            print("usage: desk_queue.py apply <story-id>", file=sys.stderr)
            sys.exit(1)
        apply(sys.argv[2])
    else:
        print("usage: desk_queue.py build | take N | apply <story-id>",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
