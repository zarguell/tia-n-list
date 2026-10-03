#!/usr/bin/env python3
"""URL-identity mint guard + stale-NEW tag contract (2026-10-03 Sandworm incident).

A Mastodon repost of the Aug-10 SecurityWeek piece "Novel Private APN Pivot
Let Hackers Sabotage Second Polish Energy Facility" minted a brand-new story
(never covered -> digest brief tagged it NEW, score 3.3); the digest agent
promoted it and headlined a 54-day-old article as [NEW]. The daily checker
FAILed it and the wrapper published anyway.

Two deterministic contracts came out of that incident:

  1. triage.apply() redirects a keep naming NEW (or an unknown story) to the
     story that already carries the event's article URL — URL identity beats
     a reworded repost title. A genuinely fresh URL still mints.
  2. digest_candidates.build_rows() tags a never-covered story CATCH-UP when
     its newest development is stale — a new slug made of old news is never
     [NEW].

Run: python3 engine/test_url_mint_guard.py   (exit 0 = pass)
"""
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


import triage  # noqa: E402
import digest_candidates  # noqa: E402

ARTICLE = "https://www.securityweek.com/novel-private-apn-pivot-let-hackers-sabotage-second-polish-energy-facility/"


def _mkstore():
    tmp = tempfile.mkdtemp()
    for var, sub in [("EVENTS", "events"), ("STORIES", "stories"),
                     ("ANALYSIS", "analysis"), ("TRIAGE", "triage")]:
        d = os.path.join(tmp, sub)
        os.makedirs(d)
        setattr(triage, var, d)
    setattr(triage, "STATE", os.path.join(tmp, "triage", "state.json"))
    setattr(triage, "NEEDS", os.path.join(tmp, "needs-analysis.json"))
    setattr(triage, "DATA", tmp)
    import store as store_mod
    import score as score_mod
    store_mod.load_events = lambda: {}
    score_mod.hot_score = lambda s, ev, rd: {"score": 5.0}
    return tmp


def _event(tmp, eid, url, title, iso):
    ev = {"id": eid, "title": title, "source": "www.securityweek.com",
          "url": url, "published_at": iso, "cves": [], "kind": "pending"}
    json.dump(ev, open(os.path.join(triage.EVENTS, eid + ".json"), "w"))
    return ev


def _story(sid, title, event_ids, iso):
    s = {"id": sid, "title": title,
         "first_seen": iso, "last_seen": iso,
         "sources": ["www.securityweek.com"], "n_sources": 1, "cves": [],
         "score": 0.4, "reddit_signal": {"posts": 0, "best_score": 0},
         "events": [{"event_id": e, "label": "original"} for e in event_ids]}
    json.dump(s, open(os.path.join(triage.STORIES, sid + ".json"), "w"))
    return s


# ── 1. keep -> NEW with an already-carried article URL attaches, never mints ──
tmp = _mkstore()
try:
    _event(tmp, "e_aug", ARTICLE,
           "Novel Private APN Pivot Let Hackers Sabotage Second Polish Energy Facility",
           "2026-08-10T10:01:52Z")
    _story("august-apn-story", "CERT Polska confirms Siemens PLC sabotage",
           ["e_aug"], "2026-08-09T00:00:00Z")
    _event(tmp, "e_repost", ARTICLE,
           "Poland's power grid hit again! Russian APT Sandworm launched a novel APN pivot attack",
           "2026-10-03T07:24:05Z")

    decfile = os.path.join(tmp, "decisions.json")
    json.dump({"decisions": [
        {"event_id": "e_repost", "action": "keep", "story": "NEW",
         "story_title": "Sandworm Sabotages Second Polish Energy Facility via APN Pivot"}]},
        open(decfile, "w"))
    triage.apply(decfile)

    slugs = sorted(f[:-5] for f in os.listdir(triage.STORIES))
    check("repost keep->NEW mints no duplicate story", slugs, ["august-apn-story"])
    st = json.load(open(os.path.join(triage.STORIES, "august-apn-story.json")))
    check("repost event attached to the URL owner",
          [r["event_id"] for r in st["events"]], ["e_aug", "e_repost"])
finally:
    shutil.rmtree(tmp)

# ── 2. keep -> NEW with a genuinely fresh URL still mints ────────────────────
tmp = _mkstore()
try:
    _event(tmp, "e_new", "https://www.securityweek.com/brand-new-intrusion/",
           "Brand new intrusion disclosed", "2026-10-03T09:00:00Z")
    decfile = os.path.join(tmp, "decisions.json")
    json.dump({"decisions": [
        {"event_id": "e_new", "action": "keep", "story": "NEW",
         "story_title": "Brand new intrusion"}]}, open(decfile, "w"))
    triage.apply(decfile)
    slugs = sorted(f[:-5] for f in os.listdir(triage.STORIES))
    check("fresh-URL keep->NEW still mints", slugs, ["brand-new-intrusion"])
finally:
    shutil.rmtree(tmp)

# ── 3. the steal path: event already attached, keep -> NEW keeps it there ────
tmp = _mkstore()
try:
    _event(tmp, "e_aug", ARTICLE, "APN pivot article", "2026-08-10T10:01:52Z")
    _story("august-apn-story", "CERT Polska confirms Siemens PLC sabotage",
           ["e_aug"], "2026-08-09T00:00:00Z")
    # the mechanical merge attached the repost before triage ran
    ev = _event(tmp, "e_repost", ARTICLE, "reworded repost headline",
                "2026-10-03T07:24:05Z")
    st = json.load(open(os.path.join(triage.STORIES, "august-apn-story.json")))
    st["events"].append({"event_id": "e_repost", "label": "update"})
    json.dump(st, open(os.path.join(triage.STORIES, "august-apn-story.json"), "w"))

    decfile = os.path.join(tmp, "decisions.json")
    json.dump({"decisions": [
        {"event_id": "e_repost", "action": "keep", "story": "NEW",
         "story_title": "Sandworm Sabotages Second Polish Energy Facility"}]},
        open(decfile, "w"))
    triage.apply(decfile)
    slugs = sorted(f[:-5] for f in os.listdir(triage.STORIES))
    check("attached event is not stolen into a NEW mint", slugs, ["august-apn-story"])
    st = json.load(open(os.path.join(triage.STORIES, "august-apn-story.json")))
    check("event stays in the owner story",
          sorted(r["event_id"] for r in st["events"]), ["e_aug", "e_repost"])
finally:
    shutil.rmtree(tmp)

# ── 4. digest brief: never-covered + stale -> CATCH-UP, fresh -> NEW ─────────
def _row(events, evs):
    return digest_candidates.build_rows(
        {"s": {"id": "s", "title": "S", "score": 3.3, "cves": [],
               "sources": ["securityweek.com"], "n_sources": 1,
               "reddit_signal": {"posts": 0, "best_score": 0},
               "events": events}},
        evs, {}, {}, lambda s: s,
        since=datetime(2026, 10, 3, tzinfo=timezone.utc),
        recent_cutoff="2026-10-01", today="2026-10-03", last_digest="2026-10-02")[0]


r = _row([{"event_id": "e_old", "label": "original"}],
         {"e_old": {"id": "e_old", "title": "Old article", "source": "securityweek.com",
                    "url": "https://x.example/a", "published_at": "2026-08-10T10:01:52Z",
                    "cves": [], "kind": "original"}})
check("never-covered stale story is CATCH-UP, not NEW", r["tag"], "CATCH-UP")

r = _row([{"event_id": "e_fresh", "label": "original"}],
         {"e_fresh": {"id": "e_fresh", "title": "Today's article", "source": "securityweek.com",
                      "url": "https://x.example/b", "published_at": "2026-10-03T09:00:00Z",
                      "cves": [], "kind": "original"}})
check("never-covered fresh story stays NEW", r["tag"], "NEW")

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {failures}")
    sys.exit(1)
print("all checks passed")
