#!/usr/bin/env python3
"""Story desk contract suite — deterministic queue + sidecar apply.

The desk is the editorial line made mechanical: a story that crosses into
hot (or joins KEV, or was born long after its CVE was disclosed) gets a
written desk pass. The LLM worker produces a SCHEMA'D SIDECAR, never store
edits; this suite pins the deterministic half:

  1. triggers: crossover (score >= 5.0), recent KEV listing, late-birth
     (born >= 14d after earliest CVE disclosure, warm+ only) — each
     independently queues; desk_reviewed_at, merged_into and the cold
     tier independently block;
  2. priority: KEV-listed first, then score desc; queue capped;
  3. take: pops the top N, writes a batch file, shrinks the queue;
  4. apply: valid sidecar -> backfill events with true published dates,
     ids desk:<sha1-12>, kind/label backfill, refs inserted AFTER the
     original in chronological position (June reads before September),
     sources unioned, desk_reviewed_at set, queue entry dropped;
  5. validation: future-dated findings, unparseable dates, unsafe urls,
     missing fields -> REJECTED, nothing applied, story left queued;
  6. no sidecar = honest "no findings": marker still set (one-shot),
     queue entry dropped, zero events created.

Run: python3 engine/test_desk_queue.py   (exit 0 = pass)
"""
import glob
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "desk_queue", os.path.join(HERE, "desk_queue.py"))
dq = importlib.util.module_from_spec(spec)
sys.modules["desk_queue"] = dq
spec.loader.exec_module(dq)

FAILS = []


def check(name, cond):
    print(("  ok  " if cond else "  FAIL") + f" {name}")
    if not cond:
        FAILS.append(name)


def story(sid, score=0.0, peak=0.0, cves=None, first="2026-09-20", **kw):
    return {"id": sid, "title": sid, "score": score, "peak_score": peak,
            "first_seen": first + "T00:00:00Z", "n_sources": 1,
            "sources": ["a.com"], "cves": cves or [],
            "events": kw.get("events", []), **kw}


# --- 1/2: triggers + priority ------------------------------------------------
stories = {
    "hot-cross": story("hot-cross", score=5.2),
    "kev-new": story("kev-new", score=4.0, cves=["CVE-2026-1001"]),
    "late-warm": story("late-warm", score=3.5, peak=4.0,
                       cves=["CVE-2026-1002"], first="2026-09-20"),
    "late-cold": story("late-cold", score=0.5, peak=1.0,
                       cves=["CVE-2026-1002"], first="2026-09-20"),
    "reviewed": story("reviewed", score=6.0, desk_reviewed_at="2026-09-23T00:00:00Z"),
    "merged": story("merged", score=6.0, merged_into="hot-cross"),
}
kev_dates = {"CVE-2026-1001": "2026-09-23",      # 1d before 'today' 2026-09-24
             "CVE-2026-1002": "2026-06-15"}      # disclosed ~3 months before birth
cve_pub = {"CVE-2026-1002": "2026-06-15"}

q = dq.compute_queue(stories, kev_dates, cve_pub, "2026-09-24", frozen=set())
ids = [e["id"] for e in q]
check("crossover queues", "hot-cross" in ids)
check("recent-KEV queues", "kev-new" in ids)
check("late-birth warm queues", "late-warm" in ids)
check("late-birth cold does NOT queue", "late-cold" not in ids)
check("reviewed one-shot blocked", "reviewed" not in ids)
check("merged blocked", "merged" not in ids)
check("kev reason outranks score in priority",
      q[0]["id"] == "kev-new" and q[0]["reasons"] == ["kev"])
check("late-birth reason tagged",
      next(e for e in q if e["id"] == "late-warm")["reasons"] == ["late-birth"])

frozen_q = dq.compute_queue(stories, kev_dates, cve_pub, "2026-09-24",
                            frozen={"hot-cross", "kev-new", "late-warm"})
check("frozen stories never queue", frozen_q == [])

many = {f"s{i}": story(f"s{i}", score=9.0) for i in range(80)}
check("queue capped", len(dq.compute_queue(many, {}, {}, "2026-09-24",
                                           frozen=set())) == dq.QUEUE_CAP)

# --- 3-6: take/apply end-to-end on a fixture store ---------------------------
with tempfile.TemporaryDirectory() as td:
    data = os.path.join(td, "data")
    stories_dir = os.path.join(data, "stories")
    events_dir = os.path.join(data, "events")
    desk_dir = os.path.join(data, "desk")
    for d in (stories_dir, events_dir, desk_dir):
        os.makedirs(d)
    dq.STORIES, dq.EVENTS, dq.DESK_DIR = stories_dir, events_dir, desk_dir
    dq.QUEUE = os.path.join(data, "desk-queue.json")

    sid = "zyxel-like"
    st = story(sid, score=6.0, cves=["CVE-2026-1001"],
               events=[{"event_id": "mf:1", "label": "original"},
                       {"event_id": "mf:2", "label": "update"}])
    json.dump(st, open(os.path.join(stories_dir, sid + ".json"), "w"))
    for eid, pub in (("mf:1", "2026-09-21T10:00:00Z"),
                     ("mf:2", "2026-09-23T09:00:00Z")):
        json.dump({"id": eid, "published_at": pub,
                   "url": f"https://a.com/{eid}"},
                  open(os.path.join(events_dir, eid + ".json"), "w"))
    dq._save_queue({"updated": "x", "stories": [
        {"id": sid, "reasons": ["crossover"], "score": 6.0},
        {"id": "other", "reasons": ["crossover"], "score": 5.1}]})

    batch = dq.take(1)
    check("take returns the batch", isinstance(batch, list) and batch
          and batch[0]["id"] == "zyxel-like")
    q_after = dq._load_queue()
    check("take pops from queue", [e["id"] for e in q_after["stories"]] == ["other"])
    check("take wrote batch file",
          len(glob.glob(os.path.join(desk_dir, "batch-*.json"))) == 1)

    # rejection: future-dated finding -> nothing applied, still queued elsewhere
    bad = {"findings": [{"title": "t", "published_at": "2099-01-01T00:00:00Z",
                         "url": "https://ok.com/a", "source_domain": "ok.com",
                         "summary_md": "s"}]}
    json.dump(bad, open(os.path.join(desk_dir, sid + ".backfill.json"), "w"))
    dq.apply(sid)
    st_now = json.load(open(os.path.join(stories_dir, sid + ".json")))
    check("future-dated finding REJECTED, nothing applied",
          len(st_now["events"]) == 2 and not st_now.get("desk_reviewed_at"))
    os.remove(os.path.join(desk_dir, sid + ".backfill.json"))

    # acceptance: valid sidecar
    good = {"findings": [
        {"title": "June GreyNoise telemetry on Zyxel scanning",
         "published_at": "2026-06-18T00:00:00Z",
         "url": "https://greynoise.com/blog/zyxel-june", "source_domain":
         "greynoise.com", "summary_md": "Greynoise saw mass scanning in June."},
        {"title": "Vendor advisory", "published_at": "2026-06-10T00:00:00Z",
         "url": "https://zyxel.com/advisory", "source_domain": "zyxel.com",
         "summary_md": "Zyxel disclosed the buffer overflow."},
    ]}
    json.dump(good, open(os.path.join(desk_dir, sid + ".backfill.json"), "w"))
    dq.apply(sid)
    st_now = json.load(open(os.path.join(stories_dir, sid + ".json")))
    evs = {r["event_id"]: r for r in st_now["events"]}
    desk_evs = [e for e in st_now["events"] if e["event_id"].startswith("desk:")]
    check("two backfill events created", len(desk_evs) == 2)
    check("desk_reviewed_at marker set", bool(st_now.get("desk_reviewed_at")))
    check("queue entry dropped", [e["id"] for e in dq._load_queue()["stories"]]
          == ["other"])
    check("event files written (json + md sidecars)",
          all(os.path.exists(os.path.join(events_dir, e["event_id"] + ext))
              for e in desk_evs for ext in (".json", ".md")))
    order = [r["event_id"] for r in st_now["events"]]
    june = [r["event_id"] for r in desk_evs
            if json.load(open(os.path.join(events_dir, r["event_id"]
                                           + ".json")))["published_at"].startswith("2026-06-10")]
    check("original stays first", order[0] == "mf:1")
    check("older backfill (Jun 10) slots before Sep 23 update",
          order.index(june[0]) < order.index("mf:2"))
    check("backfill event kind/label",
          json.load(open(os.path.join(events_dir, desk_evs[0]["event_id"]
                                      + ".json")))["kind"] == "backfill"
          and desk_evs[0]["label"] == "backfill")

    # no sidecar = honest no-findings: still one-shot
    sid2 = "no-findings"
    json.dump(story(sid2, score=5.5),
              open(os.path.join(stories_dir, sid2 + ".json"), "w"))
    dq._save_queue({"updated": "x", "stories":
                    [{"id": sid2, "reasons": ["crossover"], "score": 5.5}]})
    dq.apply(sid2)
    st2 = json.load(open(os.path.join(stories_dir, sid2 + ".json")))
    check("no findings still marks reviewed (one-shot)",
          bool(st2.get("desk_reviewed_at"))
          and dq._load_queue()["stories"] == [])

    # --- write-time double-reference guard (2026-10-13 owner decision
    # 3937e99cf1aa): a backfill finding whose desk:<sha1(url+published_at)>
    # id is already referenced by ANOTHER active story must be rejected —
    # no second ref, no clobbering the owner's event file. Seed the
    # double-reference: "other-owner" already carries the exact id this
    # sidecar would mint.
    sid3 = "dup-guard"
    json.dump(story(sid3, score=5.4),
              open(os.path.join(stories_dir, sid3 + ".json"), "w"))
    f3 = {"title": "Owned elsewhere", "published_at": "2026-05-01T00:00:00Z",
          "url": "https://owned.example/prior", "source_domain": "owned.example",
          "summary_md": "The other story's backfill."}
    eid3 = "desk:" + hashlib.sha1(
        (f3["url"] + f3["published_at"]).encode()).hexdigest()[:12]
    other = story("other-owner", score=1.0,
                  events=[{"event_id": eid3, "label": "backfill"}])
    json.dump(other, open(os.path.join(stories_dir, "other-owner.json"), "w"))
    json.dump({"id": eid3, "published_at": f3["published_at"],
               "title": "original owner's event", "kind": "backfill"},
              open(os.path.join(events_dir, eid3 + ".json"), "w"))
    json.dump({"findings": [f3]},
              open(os.path.join(desk_dir, sid3 + ".backfill.json"), "w"))
    dq.apply(sid3)
    st3 = json.load(open(os.path.join(stories_dir, sid3 + ".json")))
    o3 = json.load(open(os.path.join(stories_dir, "other-owner.json")))
    check("double-referenced backfill finding rejected (no ref added)",
          st3["events"] == [])
    check("owner story keeps its single ref",
          [r["event_id"] for r in o3["events"]] == [eid3])
    check("owner's event file not clobbered by the rejected finding",
          json.load(open(os.path.join(events_dir, eid3 + ".json")))["title"]
          == "original owner's event")
    check("guard still marks the story reviewed (one-shot moves on)",
          bool(st3.get("desk_reviewed_at"))
          and dq._load_queue()["stories"] == [])

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} check(s): {', '.join(FAILS)}")
    sys.exit(1)
print("all story-desk contract checks passed")
