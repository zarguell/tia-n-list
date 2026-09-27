#!/usr/bin/env python3
"""Low-trust source contract suite (2026-09-27 threadlinqs incident).

An AI-drafted aggregator (threadlinqs) reposted the Sep-22 CISA KEV adds on
Sep-27; the toots minted a single-source story, the digest brief read
stale_days=0, and the daily digest headlined "added to KEV today". This suite
pins the demotion contract (amplify-never-establish, NOT a block):

  1. triage.apply() denies NEW-story mints from low-trust keeps, but still
     allows attaching the same event to an existing story.
  2. digest_candidates.build_rows() never lets a low-trust event set the
     development clock (evolved/stale_days), while keeping it in ev_dates.

Run: python3 engine/test_lowtrust.py   (exit 0 = pass)
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

LT = {"low_trust": True,
      "low_trust_reason": "source reliability: AI-drafted aggregator"}


# ── 1. triage.apply(): low-trust keeps may not mint ──────────────────────────
tmp = tempfile.mkdtemp()
try:
    for var, sub in [("EVENTS", "events"), ("STORIES", "stories"),
                     ("ANALYSIS", "analysis"), ("TRIAGE", "triage")]:
        d = os.path.join(tmp, sub)
        os.makedirs(d)
        setattr(triage, var, d)
    setattr(triage, "STATE", os.path.join(tmp, "triage", "state.json"))
    setattr(triage, "NEEDS", os.path.join(tmp, "needs-analysis.json"))
    setattr(triage, "DATA", tmp)

    # e_lt: low-trust toot, no story anywhere. e_real: normal event already
    # attached to an existing story (the attach target).
    json.dump({"id": "e_lt", "title": "KEV list today", "source": "intel.threadlinqs.com",
               "url": "https://intel.threadlinqs.com/threat/TL-1",
               "published_at": "2026-09-27T03:52:12Z", "cves": [], "kind": "pending",
               **LT},
              open(os.path.join(tmp, "events", "e_lt.json"), "w"))
    json.dump({"id": "e_real", "title": "Real advisory", "source": "vendor.example",
               "url": "https://vendor.example/a",
               "published_at": "2026-09-26T10:00:00Z", "cves": [], "kind": "original"},
              open(os.path.join(tmp, "events", "e_real.json"), "w"))
    json.dump({"id": "existing", "title": "Story existing",
               "first_seen": "2026-09-26T10:00:00Z", "last_seen": "2026-09-26T10:00:00Z",
               "sources": ["vendor.example"], "n_sources": 1, "cves": [], "score": 5.0,
               "reddit_signal": {"posts": 0, "best_score": 0},
               "events": [{"event_id": "e_real", "label": "original"}]},
              open(os.path.join(tmp, "stories", "existing.json"), "w"))

    import store as store_mod
    store_mod.load_events = lambda: {
        "e_lt": json.load(open(os.path.join(tmp, "events", "e_lt.json"))),
        "e_real": json.load(open(os.path.join(tmp, "events", "e_real.json")))}
    import score as score_mod
    score_mod.hot_score = lambda s, ev, rd: {"score": 5.0}

    decfile = os.path.join(tmp, "decisions.json")
    json.dump({"decisions": [
        {"event_id": "e_lt", "action": "keep", "story": "NEW",
         "story_title": "Mint me"},
        {"event_id": "e_lt", "action": "keep", "story": "existing"}]},
        open(decfile, "w"))
    triage.apply(decfile)

    slugs = sorted(f[:-5] for f in os.listdir(os.path.join(tmp, "stories")))
    check("low-trust keep with NEW mints nothing", slugs, ["existing"])
    st = json.load(open(os.path.join(tmp, "stories", "existing.json")))
    check("low-trust keep attaches to existing story",
          [r["event_id"] for r in st["events"]], ["e_real", "e_lt"])
    ev = json.load(open(os.path.join(tmp, "events", "e_lt.json")))
    check("low-trust tag survives apply", ev.get("low_trust"), True)
finally:
    shutil.rmtree(tmp)


# ── 2. digest freshness: low-trust events never set the dev clock ────────────
def _story(events):
    return {"id": "s", "title": "S", "score": 5.0, "cves": [],
            "sources": ["a.example"], "n_sources": 1,
            "reddit_signal": {"posts": 0, "best_score": 0}, "events": events}


def _ev(eid, iso, low=False):
    e = {"id": eid, "title": f"T {eid}", "source": "a.example", "url": "",
         "published_at": iso, "cves": [], "kind": "update"}
    if low:
        e.update(LT)
    return e


rows = digest_candidates.build_rows(
    {"s": _story([{"event_id": "e_old", "label": "update"},
                  {"event_id": "e_lt", "label": "update"}])},
    {"e_old": _ev("e_old", "2026-09-22T10:00:00Z"),
     "e_lt": _ev("e_lt", "2026-09-27T03:52:12Z", low=True)},
    {}, {}, lambda s: s,
    since=datetime(2026, 9, 26, tzinfo=timezone.utc),
    recent_cutoff="2026-09-24", today="2026-09-27", last_digest="2026-09-26")
r = rows[0]
check("low-trust-only since last digest: not evolved", r["evolved"], False)
check("low-trust event excluded from dev date", r["newest_development_at"],
      "2026-09-22")
check("low-trust event still visible in event count", r["n_events"], 2)

rows = digest_candidates.build_rows(
    {"s": _story([{"event_id": "e_old", "label": "update"},
                  {"event_id": "e_lt", "label": "update"},
                  {"event_id": "e_real", "label": "update"}])},
    {"e_old": _ev("e_old", "2026-09-22T10:00:00Z"),
     "e_lt": _ev("e_lt", "2026-09-27T03:52:12Z", low=True),
     "e_real": _ev("e_real", "2026-09-27T09:00:00Z")},
    {}, {}, lambda s: s,
    since=datetime(2026, 9, 26, tzinfo=timezone.utc),
    recent_cutoff="2026-09-24", today="2026-09-27", last_digest="2026-09-26")
r = rows[0]
check("real same-day event still evolves the story", r["evolved"], True)
check("dev date comes from the real event", r["newest_development_at"],
      "2026-09-27")

# ── 3. provenance: verified primary-source attribution upgrades a low-trust ──
# event (2026-09-27 threadlinqs follow-up): the toot said "watchTowr reports
# X"; triage verified watchtowr.com carries X; the event may then mint (with
# the PRIMARY domain credited to the story) and counts as a development.
tmp = tempfile.mkdtemp()
try:
    for var, sub in [("EVENTS", "events"), ("STORIES", "stories"),
                     ("ANALYSIS", "analysis"), ("TRIAGE", "triage")]:
        d = os.path.join(tmp, sub)
        os.makedirs(d)
        setattr(triage, var, d)
    setattr(triage, "STATE", os.path.join(tmp, "triage", "state.json"))
    setattr(triage, "NEEDS", os.path.join(tmp, "needs-analysis.json"))
    setattr(triage, "DATA", tmp)

    json.dump({"id": "e_prov", "title": "watchTowr says X", "source": "intel.threadlinqs.com",
               "url": "https://intel.threadlinqs.com/threat/TL-9",
               "published_at": "2026-09-27T10:00:00Z", "cves": [], "kind": "pending",
               **LT},
              open(os.path.join(tmp, "events", "e_prov.json"), "w"))

    import store as store_mod2
    store_mod2.load_events = lambda: {
        "e_prov": json.load(open(os.path.join(tmp, "events", "e_prov.json")))}
    import score as score_mod2
    score_mod2.hot_score = lambda s, ev, rd: {"score": 5.0}

    decfile = os.path.join(tmp, "decisions.json")
    json.dump({"decisions": [{
        "event_id": "e_prov", "action": "keep", "story": "NEW",
        "story_title": "Verified zero-day",
        "provenance": {"url": "https://watchtowr.com/netscaler-rce",
                       "source": "watchtowr.com", "evidence": "watchtowr blog says X",
                       "verified": True}}]}, open(decfile, "w"))
    triage.apply(decfile)

    slugs = sorted(f[:-5] for f in os.listdir(os.path.join(tmp, "stories")))
    check("verified provenance mints where unverified could not", len(slugs), 1)
    st = json.load(open(os.path.join(tmp, "stories", slugs[0] + ".json")))
    check("primary domain credited to story sources",
          st["sources"], ["intel.threadlinqs.com", "watchtowr.com"])
    ev = json.load(open(os.path.join(tmp, "events", "e_prov.json")))
    check("provenance stamped on event", ev["provenance"]["source"], "watchtowr.com")
    check("provenance kept original event url", ev["url"],
          "https://intel.threadlinqs.com/threat/TL-9")
finally:
    shutil.rmtree(tmp)

# provenance carry-through in normalization (drift tolerance: unknown keys
# must not be silently dropped from the documented schema)
_dec, _mg, _ig = triage._normalize_decisions({
    "decisions": [{"event_id": "e1", "action": "keep", "story": "s1",
                   "provenance": {"url": "https://cisa.gov/x", "verified": True}},
                  {"event_id": "e2", "action": "keep", "story": "s2",
                   "provenance": "not a dict"}]})
check("provenance object carried through", _dec[0]["provenance"].get("verified"), True)
check("non-dict provenance neutralized", _dec[1]["provenance"], {})

# digest freshness: a verified-provenance low-trust event counts as a dev
rows = digest_candidates.build_rows(
    {"s": _story([{"event_id": "e_old", "label": "update"},
                  {"event_id": "e_pv", "label": "update"}])},
    {"e_old": _ev("e_old", "2026-09-22T10:00:00Z"),
     "e_pv": dict(_ev("e_pv", "2026-09-27T10:00:00Z", low=True),
                  provenance={"url": "https://watchtowr.com/x", "verified": True})},
    {}, {}, lambda s: s,
    since=datetime(2026, 9, 26, tzinfo=timezone.utc),
    recent_cutoff="2026-09-24", today="2026-09-27", last_digest="2026-09-26")
r = rows[0]
check("verified provenance counts as development", r["evolved"], True)
check("verified provenance sets dev date", r["newest_development_at"], "2026-09-27")

# ── 4. cold-story social revival guard (2026-09-27 Cisco SD-WAN incident) ────
# A single tweet re-sharing Rapid7's May analysis bumped the 130-day-cold
# Cisco SD-WAN story (CVE-2026-20182) to score 8.7 and onto the digest slate
# as fresh. Contract: mechanical attach refuses a social event published more
# than TIA_SOCIAL_REVIVE_GAP_DAYS (default 3) after the story's newest
# non-social event; active stories accept social events normally.
import merge as merge_mod  # noqa: E402

story = {"id": "cisco", "title": "Cisco SD-WAN zero-day",
         "sources": ["bleepingcomputer.com"], "n_sources": 1, "cves": ["CVE-2026-20182"],
         "score": 8.7, "reddit_signal": {"posts": 0, "best_score": 0},
         "events": [{"event_id": "feed_old", "label": "original"}]}
events_mock = {
    "feed_old": {"id": "feed_old", "title": "t", "source": "bleepingcomputer.com",
                 "url": "", "published_at": "2026-05-16T00:00:00Z", "cves": []},
}
merge_mod.events = events_mock
merge_mod.story_url_cache = {}

echo = {"id": "x:2104239914539782488", "title": "old flaw resurfaced",
        "source": "www.rapid7.com", "url": "https://www.rapid7.com/blog/old",
        "published_at": "2026-09-27T16:01:05Z", "cves": []}
fresh_tweet = {**echo, "id": "x:1", "published_at": "2026-05-17T00:00:00Z"}
feed_event = {"id": "mf:new", "title": "New advisory", "source": "vendor.example",
              "url": "https://vendor.example/new", "published_at": "2026-09-27T16:01:05Z",
              "cves": []}

check("echo cannot revive a 130-day-cold story",
      merge_mod._attach_event(echo["id"], echo, story), False)
check("refused echo left no event ref on the story",
      [r["event_id"] for r in story["events"]], ["feed_old"])
check("social event within the gap on an active story attaches",
      merge_mod._attach_event(fresh_tweet["id"], fresh_tweet, story), True)
check("feed events always attach (never blocked by the guard)",
      merge_mod._attach_event(feed_event["id"], feed_event, story), True)
check("non-social events are exempt from the guard",
      merge_mod._social_revive_blocked(feed_event, story), False)

# digest dev clock: an already-attached legacy echo cannot extend freshness
rows = digest_candidates.build_rows(
    {"s": _story([{"event_id": "feed_old", "label": "original"},
                  {"event_id": "echo", "label": "update"}])},
    {"feed_old": _ev("feed_old", "2026-05-16T00:00:00Z"),
     "echo": dict(_ev("echo", "2026-09-27T16:01:05Z"), id="x:echo")},
    {}, {}, lambda s: s,
    since=datetime(2026, 9, 26, tzinfo=timezone.utc),
    recent_cutoff="2026-09-24", today="2026-09-27", last_digest="2026-09-26")
r = rows[0]
check("legacy echo does not evolve a cold story", r["evolved"], False)
check("legacy echo does not set the dev date", r["newest_development_at"], "2026-05-16")

print()
if failures:
    print(f"FAILED: {failures}")
    sys.exit(1)
print("all low-trust contract checks passed")
