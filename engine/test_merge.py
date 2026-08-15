#!/usr/bin/env python3
"""Merge clustering contract suite — actor-anchored victim-claim series (2026-08-15).

The user's complaint: a burst of TheGentlemen data-leak-site claims
("TheGentlemen Ransomware Attack on <victim>") each became its own story
because the token matcher needs >= 2 shared discriminators and the titles share
only the actor name ("ransomware"/"attack"/"targets" are generic/cyber-stopped,
and the victim names differ). The fix adds a NARROW actor-series path: same
threat-actor token (leading-"the" normalized, so "TheGentlemen" == "The
Gentlemen"), BOTH titles must look like ransomware/breach victim claims, the
claim must be temporally near an ACTIVE series (14d window), and distinct
advisory/vuln series codes still block.

The general >= 2-discriminator Jaccard bar is deliberately NOT loosened — it
was tuned against false merges (LoadMaster->SharePoint, HashiCorp AV26-797->
791, mobile->non-mobile, Stormcast Tue->Mon). This suite pins both sides.

Run: python3 engine/test_merge.py   (exit 0 = pass)
Wired into CI (site-deploy.yml).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import merge  # noqa: E402

failures = []


def check(name, got, want):
    ok = (got == want) if (isinstance(want, tuple) or isinstance(got, str)
                           or isinstance(want, str)) else (abs(got - want) < 1e-9)
    print(f"  {'PASS' if ok else 'FAIL'} {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


def ev(eid, title, published="2026-08-15T00:05:53Z"):
    return {"id": eid, "title": title, "url": f"https://malware.news/t/{eid}",
            "published_at": published, "cves": []}


def story(sid, title, last_seen="2026-08-15T00:05:53Z", n_events=1,
          merged_into=None, cves=None):
    return {"id": sid, "title": title, "cves": cves or [],
            "events": [{"event_id": f"e{i}", "label": "original"} for i in range(n_events)],
            "last_seen": last_seen, "sources": ["malware.news"], "n_sources": 1,
            **({"merged_into": merged_into} if merged_into else {})}


# --- fixtures from the real 2026-08-15 batch (verbatim titles) ---
GENTLEMEN = [
    ("mf:160296", "TheGentlemen Ransomware Attack on I.P.S. Srl", "2026-08-15T00:05:53Z"),
    ("mf:160299", "The Gentlemen Ransomware Attack on Vector Two Technology", "2026-08-15T00:06:00Z"),
    ("mf:160300", "TheGentlemen Ransomware Attack on ACLI Italy", "2026-08-15T00:06:04Z"),
    ("mf:160301", "TheGentlemen Ransomware Attack Targets Avanta Maroc", "2026-08-15T00:06:08Z"),
    ("mf:160302", "TheGentlemen Ransomware Group Attacks Plaza Auto Mall", "2026-08-15T00:06:13Z"),
    ("mf:160303", "TheGentlemen Targets KFC Kosova in Ransomware Attack", "2026-08-15T00:06:16Z"),
    ("mf:160304", "TheGentlemen Ransomware Attack on Safeware Inc", "2026-08-15T00:06:19Z"),
]
ANALYSIS = "TheGentlemen Ransomware Maintains Suite of EDR Killers (ESET details)"
CLOP = "Clop Ransomware Targets Zebra.com in Major Data Breach"
STORM = "Storm Ransomware Targets Canadian Iron Foundry Integra Castings"

print("== actor-series path ==")
merge.story_url_cache = {}
s_ipssrl = story("i-p-s-srl", GENTLEMEN[0][1])
check("gentlemen claim vs gentlemen claim -> 45.0",
      merge.match_scores(ev(*GENTLEMEN[1]), s_ipssrl), 45.0)
check("cross-form (TheGentlemen vs The Gentlemen) -> 45.0",
      merge.match_scores(ev(*GENTLEMEN[6]), story("x", GENTLEMEN[1][1])), 45.0)
check("different actors (Clop vs Storm) -> 0.0",
      merge.match_scores(ev("z", CLOP), story("s", STORM)), 0.0)
check("analysis vs claim (EDR-killers) -> 0.0",
      merge.match_scores(ev("z", ANALYSIS), s_ipssrl), 0.0)
check("claim vs analysis -> 0.0",
      merge.match_scores(ev(*GENTLEMEN[2]), story("edr", ANALYSIS)), 0.0)
check("window: 10-day gap -> 35.0 (45 - gap)",
      merge.match_scores(ev("z", GENTLEMEN[0][1], "2026-08-25T00:00:00Z"),
                         story("x", GENTLEMEN[0][1], "2026-08-15T00:00:00Z")), 35.0)
check("window: 20-day gap -> 0.0 (stale series)",
      merge.match_scores(ev("z", GENTLEMEN[0][1], "2026-09-04T00:00:00Z"),
                         story("x", GENTLEMEN[0][1], "2026-08-15T00:00:00Z")), 0.0)
check("redirect shell never matches -> 0.0",
      merge.match_scores(ev(*GENTLEMEN[3]),
                         story("old", GENTLEMEN[0][1], merged_into="canonical")), 0.0)
check("distinct series codes block actor path (Storm-0324 vs Storm-0539) -> 0.0",
      merge.match_scores(ev("z", "Storm-0324 ransomware targets KFC Kosova"),
                         story("x", "Storm-0539 ransomware targets Plaza Auto Mall")), 0.0)

print("== existing paths untouched ==")
merge.story_url_cache = {}
u = "https://example.com/unique-story"
s_with_url = story("u2", "Title")
s_with_url["events"] = [{"event_id": "x", "label": "original"}]
merge.story_url_cache = {"u2": {u}}
check("URL match still 100.0",
      merge.match_scores({**ev("z", "Unrelated Title"), "url": u}, s_with_url), 100.0)
merge.story_url_cache = {}
check("focused title-CVE match still 50.0",
      merge.match_scores(ev("z", "FortiGate RCE CVE-2026-99999 exploited in attacks"),
                         story("f", "FortiGate CVE-2026-99999", cves=["CVE-2026-99999"])), 50.0)
check("generic Jaccard still 10.0 on 2+ shared discriminators",
      merge.match_scores(ev("z", "FortiGate firewall flaw exploited in attacks"),
                         story("f", "FortiGate firewall flaws under attack")), 10.0)
check("LoadMaster -> SharePoint still 0.0 (no shared discriminators)",
      merge.match_scores(ev("z", "Progress LoadMaster command injection CVE-2026-12345"),
                         story("sp", "Microsoft SharePoint RCE exploited")), 0.0)
check("HashiCorp AV26-797 vs AV26-791 distinct codes -> 0.0",
      merge.match_scores(ev("z", "HashiCorp security advisory (AV26-797)"),
                         story("h", "HashiCorp security advisory (AV26-791)")), 0.0)

print("== batch convergence (the real 7-event burst) ==")
# Simulate merge.py main(): events processed in order, one story created, the
# rest fold into it via the actor path.
stories = {}
for eid, title, pub in GENTLEMEN:
    e = ev(eid, title, pub)
    t = merge.match_story(e, stories)
    if t is None:
        slug = title.lower().replace(" ", "-")
        stories[slug] = story(slug, title, last_seen=pub)
    else:
        stories[t]["events"].append({"event_id": eid, "label": "update"})
        stories[t]["last_seen"] = pub
live = [s for s in stories.values()]
check("burst collapses to exactly 1 story", len(live), 1)
check("series story holds all 7 events", len(live[0]["events"]), 7)

# cross-batch: a later claim must converge on the MOST complete series story
series = story("series", GENTLEMEN[0][1], last_seen="2026-08-15T00:06:19Z", n_events=7)
solo = story("solo", GENTLEMEN[4][1], last_seen="2026-08-15T00:06:13Z")
pick = merge.match_story(ev("later", "TheGentlemen Ransomware Attack on Next Victim",
                            "2026-08-16T00:00:00Z"),
                         {"series": series, "solo": solo})
check("later claim converges on the 7-event series", pick, "series")

print()
if failures:
    print(f"FAILED: {len(failures)}: {failures}")
    sys.exit(1)
print("ALL PASS")
