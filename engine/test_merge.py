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
import json
import tempfile
import io
import contextlib

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
merge.story_url_cache = {"u2": {merge.norm_url(u)}}
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

print("== advisory-code catch-all guard (2026-10-17 decision 584241d6a901) ==")
# A focused single-advisory disclosure (one AV id, CVEs disjoint from the
# story's) never absorbs into a "patches N vulnerabilities" catch-all —
# the PAN-OS AV26-905/CVE-2026-0310 story must not merge into the
# CVE-2026-0322 catch-all. A genuine multi-advisory roundup still merges.
catchall = story("palo-alto-networks-patches-13-vulnerabilities",
                 "Palo Alto Networks Patches 13 Vulnerabilities",
                 cves=["CVE-2026-0322"])
focused = ev("z", "Palo Alto Networks security advisory (AV26-905)",
               )
focused["cves"] = ["CVE-2026-0310"]
check("focused AV26-905 disclosure vs CVE-2026-0322 catch-all -> 0.0",
      merge.match_scores(focused, catchall), 0.0)
own = story("palo-alto-networks-security-advisory-av26-905-cve-2026-0310-buff",
             "Palo Alto Networks Security Advisory AV26-905: CVE-2026-0310 Buffer Overflow in PAN-OS",
             cves=["CVE-2026-0310"])
check("focused disclosure still matches its own advisory story -> 50.0",
      merge.match_scores(focused, own), 50.0)
roundup = ev("z", "Palo Alto Networks security advisories (AV26-1041) (AV26-1056)")
roundup["cves"] = ["CVE-2026-0322"]
check("multi-advisory roundup on the catch-all CVE still merges -> 50.0",
      merge.match_scores(roundup, catchall), 50.0)
same_cve = ev("z", "CVE-2026-0322: Actively Exploited PAN-OS RCE Flaw Enables Root Access")
same_cve["cves"] = ["CVE-2026-0322"]
check("same-CVE focused event still merges into the catch-all -> 50.0",
      merge.match_scores(same_cve, catchall), 50.0)
plain = story("plain", "Palo Alto Networks PAN-OS update released")
check("guard is catch-all-shaped only: plain story unaffected",
      merge.match_scores(focused, plain) > 0.0, True)

print("== normalized URL identity (2026-09-16 cspusep2026 class) ==")
# feed republishing mutates URLs: scheme, www., utm params, fragments,
# trailing slash — all one article, all one story
check("norm_url collapses tracking/www/scheme variants",
      merge.norm_url("HTTPS://WWW.Oracle.com/security-alerts/cspusep2026.html?utm_source=Mastodon&x=1#f"),
      "oracle.com/security-alerts/cspusep2026.html?x=1")
check("norm_url drops trailing slash", merge.norm_url("https://a.b/c/"), "a.b/c")
check("norm_url keeps non-tracking params",
      merge.norm_url("https://a.b/p?page=2&fbclid=zz"), "a.b/p?page=2")
check("norm_url empty-safe", merge.norm_url(""), "")
CANON = "https://www.oracle.com/security-alerts/cspusep2026.html"
merge.story_url_cache = {"cpu": {merge.norm_url(CANON)}}
check("utm-variant of the advisory URL still 100.0",
      merge.match_scores({**ev("z", "Oracle CPU marathon"),
                          "url": "https://oracle.com/security-alerts/cspusep2026.html?utm_source=Mastodon"},
                         story("cpu", "Oracle September 2026 CPU")), 100.0)
merge.story_url_cache = {}

print("== metadata-CVE affinity + pollution guard ==")
check("metadata cves match when title names none",
      merge.match_scores({**ev("z", "Oracle ships its biggest patch drop of the quarter"),
                          "cves": ["CVE-2026-87286"]},
                         story("cpu", "Oracle September 2026 CPU", cves=["CVE-2026-87286"])), 50.0)
check("title CVEs still preferred over metadata",
      merge.match_scores(ev("z", "FortiGate RCE CVE-2026-99999 exploited"),
                         story("f", "FortiGate CVE-2026-99999", cves=["CVE-2026-99999"])), 50.0)
check("disjoint advisory codes block polluted story cves (metadata path)",
      merge.match_scores({**ev("z", "Check Point VPN advisory (AV26-918)"),
                          "cves": ["CVE-2026-85102"]},
                         story("july", "Check Point advisory (AV26-902)",
                               cves=["CVE-2026-85102"])), 0.0)
check("3+ metadata cves (roundup) do not snap to one story",
      merge.match_scores({**ev("z", "This month in vendor patches"),
                          "cves": ["CVE-2026-1", "CVE-2026-2", "CVE-2026-3"]},
                         story("m", "Some patch roundup", cves=["CVE-2026-2"])), 0.0)

print("== advisory ids in the slug ==")
check("av26-891 vs av26-825 in the slug are distinct advisories",
      merge.distinct_advisory_ids("jetbrains-security-advisory-av26-891",
                                  "jetbrains-security-advisory-av26-825"), True)
check("same advisory id is not distinct",
      merge.distinct_advisory_ids("x-av26-891", "x-av26-891"), False)
check("bare slug-index suffix is not an advisory code",
      merge.distinct_advisory_ids("foo-5000", "foo-6000"), False)
check("index suffix vs advisory is not a two-sided match",
      merge.distinct_advisory_ids("foo-5000", "foo-av26-891"), False)

print("== full advisory-code capture (2026-10-04 audit fix) ==")
# SERIES_RE's own comment cites CVE-2026-1234 as a match, and
# distinct_series_codes' docstring cites CVE-2026-19598 as a code — but the
# old regex captured only the year segment (CVE-2026), which made the
# advisory-code guard inert for every CVE/EUVD-titled pair: the duplicate
# suspects probe flagged advisory-distinct pairs it was documented to
# exonerate, and match_scores mechanically attached EUVD-2026-92047
# (LaraDashboard) to EUVD-2026-85013 (Manalyze) at 4.44 (2026-10-04 audit).
merge.story_url_cache = {}
check("SERIES_RE captures the full CVE number (comment example)",
      tuple(merge._series_codes("Gravity Forms patched (CVE-2026-1234)")),
      ("CVE-2026-1234",))
check("different full CVEs are distinct series codes",
      merge.distinct_series_codes("CVE-2026-95273 path traversal in changedetection.io",
                                  "CVE-2026-95272: path traversal in changedetection.io"), True)
check("the same full code is not distinct",
      merge.distinct_series_codes("CVE-2026-95273 x", "CVE-2026-95273 y"), False)
check("CVE slug counts as advisory id (docstring example cve-2024-37079)",
      merge.distinct_advisory_ids("flaw-cve-2024-37079-details",
                                  "flaw-cve-2024-37078-details"), True)
check("cross-EUVD event no longer attaches to unrelated product story",
      merge.match_scores(
          ev("z", "🚨 EUVD-2026-92047 📊 Score: 6.3/10 (CVSS v3.1) 📦 Product: laradashboard 🏢 Vendor: laradashboard 📅 Updated: 2026-10-03"),
          story("m", "EUVD-2026-85013 📊 Score: 4.8/10 (CVSS v3.1) 📦 Product: Manalyze 🏢 Vendor: JusticeRage")), 0.0)
check("same-full-code event still title-matches its story",
      merge.match_scores(
          ev("z", "EUVD-2026-85013 Manalyze flaw exploited in attacks update"),
          story("m", "EUVD-2026-85013 Manalyze flaw exploited in attacks")) > 0, True)

print("== discriminator token floor (score.py coherence consumer) ==")
# score.py's coherence test passes minlen=3 so 3-char PRODUCT names survive;
# every dedup/merge consumer keeps the 4-char floor (widening it would change
# duplicate_suspects/entity_dup recall — do not let this default drift).
check("default floor still drops 3-char tokens (dedup behaviour unchanged)",
      tuple(sorted(merge.title_discriminators(
          "PHP warns admins of flaws in version 9.2"))),
      ("admins", "version"))
check("minlen=3 keeps the 3-char product names PHP and SQL",
      tuple(sorted(merge.title_discriminators("PHP and the SQL flaw", 3))),
      ("php", "sql"))

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

print("== write-time double-reference guard (2026-10-13 decisions batch) ==")
# Seed the double-reference class: event mf:1 already lives in story "alpha".
# The writers (merge queue attach, social replay attach, mint, desk backfill)
# must refuse to place it into a second ACTIVE story.
guard_stories = {
    "alpha": {"id": "alpha", "title": "Alpha holds it",
              "events": [{"event_id": "mf:1", "label": "original"}],
              "sources": ["a.com"], "n_sources": 1, "cves": [],
              "first_seen": "2026-08-15T00:05:53Z",
              "last_seen": "2026-08-15T00:05:53Z"},
    "beta": {"id": "beta", "title": "Beta must not take it",
             "events": [], "sources": [], "n_sources": 0, "cves": [],
             "first_seen": "2026-08-15T00:05:53Z",
             "last_seen": "2026-08-15T00:05:53Z"},
    "shell": {"id": "shell", "title": "merged away",
              "events": [{"event_id": "mf:9", "label": "original"}],
              "sources": [], "n_sources": 0, "cves": [],
              "merged_into": "alpha",
              "first_seen": "2026-08-15T00:05:53Z",
              "last_seen": "2026-08-15T00:05:53Z"},
}
check("owner story detected", merge.event_owner(guard_stories, "mf:1"), "alpha")
check("own ref is not an owner (exclude)",
      merge.event_owner(guard_stories, "mf:1", exclude="alpha") is None, True)
check("merged shell is not an active owner",
      merge.event_owner(guard_stories, "mf:9") is None, True)
check("unreferenced event has no owner",
      merge.event_owner(guard_stories, "mf:404") is None, True)

guard_ev = {"id": "mf:1", "title": "reworded pickup of the same event",
            "url": "https://a.com/mf-1", "published_at": "2026-08-16T00:05:53Z",
            "cves": []}
merge.story_url_cache = {}
check("attach into a second story is rejected",
      merge._attach_event("mf:1", guard_ev, guard_stories["beta"],
                          guard_stories), False)
check("rejected attach left no double reference",
      tuple(r["event_id"] for r in guard_stories["beta"]["events"]), ())
check("owner still holds exactly one ref",
      tuple(r["event_id"] for r in guard_stories["alpha"]["events"]),
      ("mf:1",))
check("guard passes when the event is unowned (normal attach) (back-compat)",
      merge._attach_event("mf:7", {"id": "mf:7", "title": "fresh event",
                                   "url": "https://a.com/mf-7",
                                   "published_at": "2026-08-16T01:00:00Z",
                                   "cves": []},
                          guard_stories["beta"], guard_stories), True)
check("3-arg call (no stories passed) keeps the old contract",
      merge._attach_event("mf:8", {"id": "mf:8", "title": "unit test path",
                                   "url": "https://a.com/mf-8",
                                   "published_at": "2026-08-16T02:00:00Z",
                                   "cves": []},
                          guard_stories["beta"]), True)

print("== corrupt-JSON hardening (fail-open loads) ==")
# One bad file must not stall the hourly pipeline: stories skip-and-warn,
# MANIFEST/QUEUE fall back to the same defaults main() used for missing files.
_orig_stories, _orig_manifest, _orig_queue = merge.STORIES, merge.MANIFEST, merge.QUEUE
try:
    with tempfile.TemporaryDirectory() as td:
        good = {"id": "good-story", "title": "Good", "events": []}
        with open(os.path.join(td, "good.json"), "w") as f:
            json.dump(good, f)
        open(os.path.join(td, "empty.json"), "w").close()  # zero-length -> JSONDecodeError
        with open(os.path.join(td, "corrupt.json"), "w") as f:
            f.write("{not json")
        merge.STORIES = td
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            loaded = merge.load_stories()
        check("empty+corrupt story files skipped, good kept", ",".join(sorted(loaded.keys())), "good-story")
        check("story warning names the bad file", str("empty.json" in err.getvalue() and "corrupt.json" in err.getvalue()), "True")
    with tempfile.TemporaryDirectory() as td:
        bad_manifest = os.path.join(td, "manifest.json")
        with open(bad_manifest, "w") as f:
            f.write("{oops")
        merge.MANIFEST = bad_manifest
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            got = merge._load_json_or_default(merge.MANIFEST, {"stories_per_day": {}})
        check("corrupt MANIFEST falls back to default", json.dumps(got, sort_keys=True), json.dumps({"stories_per_day": {}}, sort_keys=True))
        check("manifest warning names the file", str(bad_manifest in err.getvalue()), "True")
        empty_manifest = os.path.join(td, "empty-manifest.json")
        open(empty_manifest, "w").close()
        with contextlib.redirect_stderr(io.StringIO()):
            check("empty MANIFEST falls back to default",
                  json.dumps(merge._load_json_or_default(empty_manifest, {"stories_per_day": {}}), sort_keys=True),
                  json.dumps({"stories_per_day": {}}, sort_keys=True))
    with tempfile.TemporaryDirectory() as td:
        bad_queue = os.path.join(td, "new-events.json")
        with open(bad_queue, "w") as f:
            f.write("")  # empty queue file
        merge.QUEUE = bad_queue
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            got = merge._load_json_or_default(merge.QUEUE, {"events": []})
        check("corrupt/empty QUEUE falls back to empty", json.dumps(got, sort_keys=True), json.dumps({"events": []}, sort_keys=True))
        check("queue warning names the file", str(bad_queue in err.getvalue()), "True")
finally:
    merge.STORIES, merge.MANIFEST, merge.QUEUE = _orig_stories, _orig_manifest, _orig_queue

print("== story-title hygiene (2026-10-18 decisions batch 6cb97b2fc92b) ==")
# The FreeRDP regression (audit Issue 3 / Rec 5): the story title stayed
# pinned to the FOUNDING toot's raw headline while the story's newer
# threataft.com event carried a clean title. A raw toot/aggregator title is
# replaced by the newest clean event title; a clean (analyst-set) title is
# never touched.
RAW = ("We've just released # FreeRDP 3.32.0 This one is a huge # feature "
       "and # CVE release, update highly recommended! Check it out at "
       "https:// fre")
CLEAN = "FreeRDP 3.32.0 fixes CVE-2026-111380 (8.8) in macOS/iOS"
check("raw toot debris detected", merge._raw_title(RAW), True)
check("a clean headline is not raw", merge._raw_title(CLEAN), False)
check("hashtag markers stripped, words kept",
      merge.strip_title_debris("a huge # feature and #CVE fix"),
      "a huge feature and CVE fix")
check("truncated https:// fragment stripped",
      merge.strip_title_debris("Update now https:// fre"), "Update now")
check("full URL stripped",
      merge.strip_title_debris("Advisory at https://example.com/a"),
      "Advisory at")
check("emoji-strip residue never leads a published title",
      merge._display_title("\U0001F5A5\uFE0F FreeRDP 3.32.0"), "FreeRDP 3.32.0")

_t_events = {
    "masto:old": {"id": "masto:old", "title": RAW,
                  "published_at": "2026-09-23T07:51:53Z",
                  "url": "https://freerdp.com/"},
    "masto:new": {"id": "masto:new", "title": CLEAN,
                  "published_at": "2026-10-17T12:35:58Z",
                  "url": "https://threataft.com/articles/freerdp-cluster"},
}
_t_story = {"id": "freerdp", "title": RAW, "cves": [], "n_sources": 1,
            "sources": ["freerdp.com"], "first_seen": "2026-09-23T07:51:53Z",
            "last_seen": "2026-10-17T12:35:58Z",
            "events": [{"event_id": "masto:old", "label": "original"},
                       {"event_id": "masto:new", "label": "update"}]}
check("raw founding title replaced by the newest clean event title",
      merge.preferred_title(_t_story, _t_events), CLEAN)
check("clean (analyst-set) title is never touched",
      merge.preferred_title(dict(_t_story, title="Analyst picked this"),
                            _t_events) is None, True)
check("no clean candidate -> debris stripped from the current title",
      merge.preferred_title(
          dict(_t_story, events=[{"event_id": "masto:old"}]), _t_events),
      ("We've just released FreeRDP 3.32.0 This one is a huge feature and "
       "CVE release, update highly recommended! Check it out at"))
_social_newer = dict(_t_events,
                     **{"rss:later": {"id": "rss:later",
                                      "title": CLEAN,
                                      "published_at": "2026-10-18T10:00:00Z"}})
check("newest clean title wins across routes",
      merge.preferred_title(_t_story, _social_newer), CLEAN)

# the attach seam applies the rule (the FreeRDP story heals on its next
# event); the global events map is what _attach_event already uses elsewhere
_orig_events = globals().get("merge").events if hasattr(merge, "events") else None
merge.events = _t_events
merge.story_url_cache = {}
_attach_story = {"id": "freerdp", "title": RAW, "events": [], "sources": [],
                 "n_sources": 0, "cves": [],
                 "first_seen": "2026-09-23T07:51:53Z",
                 "last_seen": "2026-09-23T07:51:53Z"}
_attached = merge._attach_event("masto:new", dict(_t_events["masto:new"],
                                                  cves=[]), _attach_story)
check("attach refreshes a raw story title",
      (_attached, _attach_story["title"]), (True, CLEAN))
merge.events = _orig_events if _orig_events is not None else {}

# ── retroactive title heal (2026-10-19 owner decision ad4c5d039830,
# completing 6cb97b2fc92b). The 2026-10-18 rule ran only inside
# _attach_event, so a story that received no new event stayed raw forever
# (the Chrome 153 driver). heal_raw_titles() reconciles every live story —
# and its CTI record title — after scoring.
print("== retroactive title heal ==")
_h_dir = tempfile.mkdtemp()
_h_events = {
    "he:1": {"id": "he:1",
             "title": "A clean event headline about the FreeRDP release",
             "published_at": "2026-10-17T10:00:00Z"},
    "he:2": {"id": "he:2", "title": "raw # debris https:// example.com trunca",
             "published_at": "2026-10-18T10:00:00Z"},
}
_h_stories = {
    "healed": {"id": "healed", "title": "raw founding # toot https:// example.com",
               "events": [{"event_id": "he:1"}, {"event_id": "he:2"}],
               "sources": [], "cves": [], "last_seen": "2026-10-18T10:00:00Z"},
    "already-clean": {"id": "already-clean",
                      "title": "Analyst picked this headline",
                      "events": [{"event_id": "he:1"}],
                      "sources": [], "cves": []},
    "shell": {"id": "shell", "title": "raw # shell debris https:// x.y",
              "events": [], "merged_into": "healed"},
}
os.makedirs(os.path.join(_h_dir, "cti"), exist_ok=True)
json.dump({"story_id": "healed", "title": "raw # debris https:// x.y",
           "references": []},
          open(os.path.join(_h_dir, "cti", "healed.json"), "w"))
json.dump({"story_id": "already-clean", "title": "Analyst case title",
           "references": []},
          open(os.path.join(_h_dir, "cti", "already-clean.json"), "w"))
_h_n, _h_c = merge.heal_raw_titles(_h_stories, _h_events, stories_dir=_h_dir,
                                   cti_dir=os.path.join(_h_dir, "cti"))
check("raw live story healed; clean title untouched",
      (_h_stories["healed"]["title"], _h_stories["already-clean"]["title"]),
      ("A clean event headline about the FreeRDP release",
       "Analyst picked this headline"))
check("merged redirect shell is not healed",
      _h_stories["shell"]["title"], "raw # shell debris https:// x.y")
check("heal counts stories and cti records", (_h_n, _h_c), (1, 1))
check("raw CTI record title healed to the story title",
      json.load(open(os.path.join(_h_dir, "cti", "healed.json")))["title"],
      "A clean event headline about the FreeRDP release")
check("clean CTI record title untouched",
      json.load(open(os.path.join(_h_dir, "cti", "already-clean.json")))["title"],
      "Analyst case title")
check("heal is idempotent (second pass heals nothing)",
      merge.heal_raw_titles(_h_stories, _h_events, stories_dir=_h_dir,
                            cti_dir=os.path.join(_h_dir, "cti")), (0, 0))

print()
if failures:
    print(f"FAILED: {len(failures)}: {failures}")
    sys.exit(1)
print("ALL PASS")
