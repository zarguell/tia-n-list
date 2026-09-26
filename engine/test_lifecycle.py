#!/usr/bin/env python3
"""Cold-tier freeze contract suite — lifecycle + hooks (store-health L2).

The 2026-09 numbers that motivated this leaf: ~10.2k stories in the store,
~8.2k of them with peak_score 0, every one re-scored by merge.py hourly and
rendered by ssg.py on every build — all paying for stories that never
mattered. peak_score (the store-health root's high-water mark) is what makes
"cooled" distinguishable from "never mattered"; this suite pins the freeze
lifecycle built on it:

  1. freeze_sweep eligibility matrix: age, peak, n_sources, analysis,
     merged_into, digest-reference and already-frozen each INDEPENDENTLY
     block freezing; a story meeting every bar freezes; the sweep saves
     frozen.json once and returns only the newly frozen ids;
  2. frozen.json round-trip + tolerant loader: missing, corrupt,
     wrong-shape and non-string ids all mean "nothing frozen" (fail-warm);
  3. unfreeze_strong: a new event whose CVE set intersects the story's cves
     thaws it; an exact URL match against the story's event-file urls thaws
     it; a weak-only event does not; stale ids (story file gone) are
     dropped; empty/missing frozen.json is a fast no-op that writes nothing;
  4. editorial unfreeze_ids thaws only actually-frozen ids, and
     triage.collect() never offers a frozen story as a keep target;
  5. merge.emit_needs(exclude=frozen) never queues a frozen story;
  6. ssg.load_stories drops frozen stories from the cards (they render no
     page and appear in no feed/index/hot list).

Run: python3 engine/test_lifecycle.py   (exit 0 = pass)
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lifecycle  # noqa: E402
import merge  # noqa: E402
import store as store_mod  # noqa: E402
import triage  # noqa: E402
import ssg  # noqa: E402

FAILS = []


def check(name, cond):
    print(("  ok  " if cond else "  FAIL") + f" {name}")
    if not cond:
        FAILS.append(name)


NOW = datetime.now(timezone.utc)
OLD = (NOW - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
RECENT = (NOW - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")


def eligible_story(sid, **over):
    """A story that meets every freeze bar (old, never warm, single-source,
    no analysis, live) — tests then break ONE criterion at a time."""
    s = {"id": sid, "title": sid, "first_seen": OLD, "last_seen": OLD,
         "n_sources": 1, "sources": ["a.example"], "cves": [],
         "peak_score": 0, "score": 0.0,
         "events": [{"event_id": f"evt-{sid}", "label": "original"}]}
    s.update(over)
    return s


def setup_store(td):
    """Point every lifecycle path at a tmp store; reset the strong-index
    cache (keyed on the frozen set + STORIES path, so a repoint is enough)."""
    dirs = {name: os.path.join(td, name) for name in
            ("stories", "events", "digests")}
    for d in dirs.values():
        os.makedirs(d)
    lifecycle.STORIES = dirs["stories"]
    lifecycle.DIGESTS = dirs["digests"]
    lifecycle.EVENTS = dirs["events"]
    lifecycle.FREEZE_FILE = os.path.join(td, "frozen.json")
    lifecycle._STRONG_CACHE.update(key=None, cves={}, urls={}, stale=set())
    return dirs


# --- 1: freeze eligibility matrix -------------------------------------------
with tempfile.TemporaryDirectory() as td:
    dirs = setup_store(td)
    log = []

    def write_story(s):
        json.dump(s, open(os.path.join(dirs["stories"], s["id"] + ".json"), "w"),
                  indent=1)

    stories = {}
    cases = {
        "ok-old-cold": {},                                     # freezes
        "block-age": {"first_seen": RECENT},                   # too young
        "block-age-badts": {"first_seen": "not-a-date"},       # unreadable clock -> age 0
        "block-peak": {"peak_score": 3.0},                     # reached the warm band
        "block-nsources": {"n_sources": 2},
        "block-analysis": {"analysis": {"updated_at": "2026-09-01T00:00:00Z"}},
        "block-merged": {"merged_into": "live-elsewhere"},
    }
    for sid, over in cases.items():
        s = eligible_story(sid, **over)
        stories[sid] = s
        write_story(s)
    # digest-referenced block: a digest md links the story
    open(os.path.join(dirs["digests"], "2026-09-20.md"), "w").write(
        "see [the story](/stories/block-digest/) for detail")
    s = eligible_story("block-digest")
    stories["block-digest"] = s
    write_story(s)

    newly = lifecycle.freeze_sweep(stories, log=log.append)
    check("only the fully-eligible story froze", newly == {"ok-old-cold"})
    check("frozen.json written once with the frozen id",
          lifecycle.frozen_ids() == {"ok-old-cold"})
    check("summary logged, not per-id spam",
          len(log) == 1 and "1 cold stories" in log[0] and "ok-old-cold" in log[0])

    # already-frozen + digest-reference via the real referenced_story_ids path
    log.clear()
    newly = lifecycle.freeze_sweep(stories, log=log.append)
    check("second sweep re-freezes nothing (already frozen)",
          newly == set() and lifecycle.frozen_ids() == {"ok-old-cold"})
    check("no log line when nothing froze", log == [])
    stories["block-digest"]["peak_score"] = 2.0   # would freeze if not referenced
    newly = lifecycle.freeze_sweep(stories)
    check("digest-referenced story spared", "block-digest" not in newly
          and lifecycle.frozen_ids() == {"ok-old-cold"})
    # falsy analysis marker does NOT block (only truthy = someone wrote one)
    stories["falsy-analysis"] = eligible_story("falsy-analysis", analysis={})
    newly = lifecycle.freeze_sweep(stories)
    check("empty analysis marker does not block", newly == {"falsy-analysis"})

# --- 2: frozen file round-trip + tolerant loader ----------------------------
with tempfile.TemporaryDirectory() as td:
    setup_store(td)
    check("missing frozen.json -> empty", lifecycle.frozen_ids() == set())
    open(lifecycle.FREEZE_FILE, "w").write("{corrupt")
    check("corrupt frozen.json -> empty", lifecycle.frozen_ids() == set())
    json.dump({"updated": "2026-09-24T00:00:00Z", "ids": "not-a-list"},
              open(lifecycle.FREEZE_FILE, "w"))
    check("wrong shape (ids not a list) -> empty", lifecycle.frozen_ids() == set())
    json.dump({"ids": ["a-story", 3, None, "b-story"]},
              open(lifecycle.FREEZE_FILE, "w"))
    check("non-string ids dropped",
          lifecycle.frozen_ids() == {"a-story", "b-story"})
    lifecycle._save_frozen({"z-story", "a-story"})
    data = json.load(open(lifecycle.FREEZE_FILE))
    check("round-trip: sorted ids + updated stamp",
          data["ids"] == ["a-story", "z-story"] and data["updated"].endswith("Z"))

# --- 3: unfreeze_strong -------------------------------------------------------
with tempfile.TemporaryDirectory() as td:
    dirs = setup_store(td)

    def wstory(sid, cves=(), events=("evt-x",)):
        s = eligible_story(sid, cves=list(cves),
                           events=[{"event_id": e, "label": "original"}
                                   for e in events])
        json.dump(s, open(os.path.join(dirs["stories"], sid + ".json"), "w"))
        return s

    wstory("frozen-cve", cves=["CVE-2026-1111"])
    wstory("frozen-url", events=("evt-u",))
    json.dump({"id": "evt-u", "url": "https://x.example/article"},
              open(os.path.join(dirs["events"], "evt-u.json"), "w"))
    wstory("frozen-quiet")
    stories = {sid: json.load(open(os.path.join(dirs["stories"], sid + ".json")))
               for sid in ("frozen-cve", "frozen-url", "frozen-quiet")}
    lifecycle._save_frozen(set(stories))

    # empty-store bail first: no frozen.json at all -> fast no-op, no write
    os.remove(lifecycle.FREEZE_FILE)
    check("no frozen.json -> fast no-op",
          lifecycle.unfreeze_strong({"id": "mf:1", "url": "https://y.example/",
                                     "cves": ["CVE-2026-1111"]}, stories) == set()
          and not os.path.exists(lifecycle.FREEZE_FILE))

    # weak-only event: touches nothing, writes nothing
    lifecycle._save_frozen(set(stories))
    before = open(lifecycle.FREEZE_FILE).read()
    check("weak-only event leaves the freeze untouched",
          lifecycle.unfreeze_strong({"id": "mf:2",
                                     "url": "https://other.example/z",
                                     "cves": ["CVE-2026-9999"]},
                                    stories) == set()
          and open(lifecycle.FREEZE_FILE).read() == before)

    # CVE intersection thaws
    out = lifecycle.unfreeze_strong({"id": "mf:3", "url": "",
                                     "cves": ["cve-2026-1111"]}, stories)
    check("CVE intersection unfreezes (case-insensitive)",
          out == {"frozen-cve"} and lifecycle.frozen_ids() == {"frozen-url",
                                                               "frozen-quiet"})
    # exact URL match via the story's event-file url thaws
    out = lifecycle.unfreeze_strong({"id": "mf:4",
                                     "url": "https://x.example/article",
                                     "cves": []}, stories)
    check("exact URL match (via event file) unfreezes",
          out == {"frozen-url"} and lifecycle.frozen_ids() == {"frozen-quiet"})
    # stale id: story file deleted out from under the freeze
    os.remove(os.path.join(dirs["stories"], "frozen-quiet.json"))
    out = lifecycle.unfreeze_strong({"id": "mf:5", "url": "", "cves": []}, stories)
    check("stale frozen id dropped, frozen.json now empty",
          out == {"frozen-quiet"} and lifecycle.frozen_ids() == set())

# --- 4: editorial unfreeze + triage collect exclusion -----------------------
with tempfile.TemporaryDirectory() as td:
    dirs = setup_store(td)
    lifecycle._save_frozen({"frozen-story", "other-frozen"})
    check("unfreeze_ids removes only actually-frozen ids",
          lifecycle.unfreeze_ids(["frozen-story", "never-was"]) == {"frozen-story"}
          and lifecycle.frozen_ids() == {"other-frozen"})

    # triage.collect() must not offer frozen candidates
    triage_dir = os.path.join(td, "triage")
    os.makedirs(triage_dir)
    triage.STORIES = dirs["stories"]
    triage.TRIAGE = triage_dir
    triage.STATE = os.path.join(triage_dir, "state.json")
    store_mod.EVENTS_DIR = dirs["events"]
    json.dump({"id": "mf:live", "title": "live event", "url": "https://a.example/l",
               "published_at": RECENT, "cves": [], "source": "a.example",
               "kind": "original", "content_md": "live event body"},
              open(os.path.join(store_mod.EVENTS_DIR, "mf:live.json"), "w"))
    json.dump(eligible_story("live-recent", first_seen=RECENT,
                             last_seen=RECENT, n_sources=2, peak_score=5.0),
              open(os.path.join(triage.STORIES, "live-recent.json"), "w"))
    json.dump(eligible_story("frozen-cand", first_seen=RECENT,
                             last_seen=RECENT, n_sources=2, peak_score=5.0),
              open(os.path.join(triage.STORIES, "frozen-cand.json"), "w"))
    lifecycle._save_frozen({"frozen-cand", "never-was"})
    triage.collect()
    ctx_path = os.path.join(triage_dir, f"context-{triage.RUN_TAG}.json")
    ctx = json.load(open(ctx_path))
    cands = {c["id"] for c in ctx["candidate_stories"]}
    check("collect offers the live story, never the frozen one",
          "live-recent" in cands and "frozen-cand" not in cands)

# --- 5: emit_needs excludes frozen ------------------------------------------
with tempfile.TemporaryDirectory() as td:
    merge.NEEDS = os.path.join(td, "needs-analysis.json")
    merge.ANALYSIS_DIR = os.path.join(td, "analysis")
    os.makedirs(merge.ANALYSIS_DIR)
    hot = {"id": "hot-live", "score": 5.0, "events": []}
    hotfrozen = {"id": "hot-frozen", "score": 5.0, "events": []}
    n = merge.emit_needs({"hot-live": hot, "hot-frozen": hotfrozen},
                         exclude={"hot-frozen"})
    check("frozen hot story not queued, live one is",
          n == 1 and json.load(open(merge.NEEDS))["stories"] == ["hot-live"])

# --- 5b: emit_needs skips .capped stories (2026-09-25 retry cap) ------------
with tempfile.TemporaryDirectory() as td:
    merge.NEEDS = os.path.join(td, "needs-analysis.json")
    merge.ANALYSIS_DIR = os.path.join(td, "analysis")
    os.makedirs(os.path.join(merge.ANALYSIS_DIR, ".rejects"))
    hot = {"id": "hot-capped", "score": 5.0, "events": []}
    open(os.path.join(merge.ANALYSIS_DIR, ".rejects", "hot-capped.capped"), "w").close()
    n = merge.emit_needs({"hot-capped": hot})
    check("capped story not requeued", n == 0
          and json.load(open(merge.NEEDS))["stories"] == [])

# --- 6: ssg.load_stories drops frozen from cards ------------------------------
with tempfile.TemporaryDirectory() as td:
    sdir = os.path.join(td, "stories")
    os.makedirs(sdir)
    adir = os.path.join(td, "analysis")
    os.makedirs(adir)
    ssg.STORIES_DIR = sdir
    ssg.ANALYSIS_DIR = adir
    live = eligible_story("live-card", peak_score=6.0, score=6.0,
                          events=[{"event_id": "evt-live", "label": "original"}])
    cold = eligible_story("frozen-card", peak_score=0, score=0.0)
    json.dump(live, open(os.path.join(sdir, "live-card.json"), "w"))
    json.dump(cold, open(os.path.join(sdir, "frozen-card.json"), "w"))
    lifecycle.FREEZE_FILE = os.path.join(td, "frozen.json")
    lifecycle._save_frozen({"frozen-card"})
    ev = {"id": "evt-live", "content_md": "body text here", "kind": "original",
          "title": "t", "source": "a.example", "url": "https://a.example/1",
          "published_at": OLD}
    cards = ssg.load_stories({"evt-live": ev})
    ids = {c["id"] for c in cards}
    check("frozen story renders no card", ids == {"live-card"})

# --- digest slate excludes frozen (parent-join fix) ------------------------
import digest_candidates  # noqa: E402

with tempfile.TemporaryDirectory() as td:
    sd = os.path.join(td, "stories")
    os.makedirs(sd)
    json.dump({"id": "frozen-story", "score": 2.9,
               "events": [{"event_id": "e1"}]},
              open(os.path.join(sd, "frozen-story.json"), "w"))
    json.dump({"id": "live-story", "score": 3.5,
               "events": [{"event_id": "e2"}]},
              open(os.path.join(sd, "live-story.json"), "w"))
    orig = lifecycle.frozen_ids
    lifecycle.frozen_ids = lambda: {"frozen-story"}
    try:
        out = digest_candidates.load_stories(sd)
    finally:
        lifecycle.frozen_ids = orig
    check("digest slate excludes frozen stories",
          "frozen-story" not in out and "live-story" in out)

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} check(s): {', '.join(FAILS)}")
    sys.exit(1)
print("all store-health L2 cold-tier contract checks passed")
