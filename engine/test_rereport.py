#!/usr/bin/env python3
"""Re-report penalty contract suite (2026-10-03, audit rec #2 — 3rd day).

Outlet echoes of already-carried coverage (no new CVEs, reworded same
headline) reset the 36h decay clock and stacked 48h velocity, keeping
echo-only stories on the digest slate until an agent demoted them by hand —
the audit attributed most of the ~340 digest demote overrides and 8 slugs
overridden >= 3 times to this single class. The contracts pinned here:

  1. score.is_rereport: founding events are never echoes; same-CVE reworded
     headlines are; events bringing a NEW CVE are developments even when the
     headline is near-identical; CVE-less stories classify on title overlap;
     `rd:` repost stubs classify on the DELTA they carry (a new CVE, actor,
     victim count, or IOC) and are otherwise zero-delta echoes.
  2. score.hot_score: echoes count zero velocity and never move the decay
     anchor — a story bumped only by echoes decays from its last genuine
     development; one genuine development re-warms it.
  3. digest_candidates.build_rows: echo events keep n_events (display) but
     never set evolved/newest_development_at.

Run: python3 engine/test_rereport.py   (exit 0 = pass)
"""
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


import score  # noqa: E402
import digest_candidates  # noqa: E402

score._cve_store = {"CVE-2026-1234": {"cvss": 9.8, "kev": True},
                    "CVE-2026-5678": {"cvss": 7.5, "kev": False}}

BASE = datetime(2026, 10, 3, 12, 0, tzinfo=timezone.utc)


def iso(hours_before):
    return (BASE - timedelta(hours=hours_before)).isoformat().replace(
        "+00:00", "Z")


def ev(eid, title, published, cves=()):
    return {"id": eid, "title": title, "published_at": published,
            "cves": list(cves), "url": f"https://example.com/{eid}",
            "source": "example.com", "kind": "update", "lang": "en",
            "content_md": ""}


# ── 1. is_rereport classification ────────────────────────────────────────────
orig = ev("e1", "FortiMail zero-day used to hack government mail servers",
          iso(72), ["CVE-2026-1234"])
check("founding event is never a re-report", score.is_rereport(orig, []), False)

echo = ev("e2", "Hackers abuse FortiMail zero-day in government email attacks",
          iso(24), ["CVE-2026-1234"])
check("same-CVE reworded headline (48h later) is a re-report",
      score.is_rereport(echo, [orig]), True)

same_day = ev("e2b", "Hackers abuse FortiMail zero-day in government email attacks",
              iso(71), ["CVE-2026-1234"])
check("same-day burst is legitimate velocity, not an echo",
      score.is_rereport(same_day, [orig]), False)

newcve = ev("e3", "FortiMail zero-day now also hitting finance sector",
            iso(12), ["CVE-2026-1234", "CVE-2026-5678"])
check("event bringing a NEW CVE is a development",
      score.is_rereport(newcve, [orig]), False)

fresh = ev("e4", "KillSec ransomware claims 40 GB of hospital records",
           iso(6))
check("different headline is not a re-report",
      score.is_rereport(fresh, [orig]), False)

breach = ev("e5", "KillSec ransomware claims hospital breach", iso(30))
breach2 = ev("e6", "KillSec ransomware claims hospital breach", iso(4))
check("CVE-less re-share of the same headline is a re-report",
      score.is_rereport(breach2, [breach]), True)

victim2 = ev("e6b", "KillSec ransomware claims school breach", iso(4))
check("CVE-less NEW victim is a development, not an echo",
      score.is_rereport(victim2, [breach]), False)

# section 2/3 marker
def _story(events):
    return {"id": "s", "title": events[0]["title"],
            "sources": ["example.com"], "n_sources": 1,
            "cves": sorted({c for e in events for c in e["cves"]}),
            "last_seen": max(e["published_at"] for e in events),
            "reddit_signal": {"posts": 0, "best_score": 0},
            "events": [{"event_id": e["id"], "label": "update"} for e in events]}


def _score(events):
    return score.hot_score(_story(events),
                           {e["id"]: e for e in events}, [], now=BASE)


# FortiMail: genuine dev 72h ago + fresh echo 24h ago - no velocity, decayed
forti = [orig, echo]
sc = _score(forti)
check("echo-only bump adds no velocity", sc["velocity"], 0.0)
check("echo counted in rereports", sc["rereports"], 1)
check("decay anchors to the genuine development (72h, not 24h)",
      sc["recency"] < 0.15, True)

# KillSec: claim 30h ago + identical re-share 4h ago - same contract, no CVEs
kill = [breach, breach2]
sc = _score(kill)
check("founding event inside 48h still counts velocity", sc["velocity"], 0.5)
check("CVE-less re-share counted", sc["rereports"], 1)

# one fresh GENUINE development re-warms: full velocity, fresh clock
# a genuine development: brings a NEW CVE to the story (real "story grows"
# events) — same-CVE reworded follow-ups intentionally decay instead
dev = ev("e7", "FortiMail zero-day now chained with second flaw for RCE",
         iso(2), ["CVE-2026-1234", "CVE-2026-5678"])
sc2 = _score(forti + [dev])
check("genuine development restores velocity", sc2["velocity"], 0.5)
check("genuine development anchors recency (2h)",
      sc2["recency"] > 0.9, True)
check("revised rereport count", sc2["rereports"], 1)


def _rows(events):
    return digest_candidates.build_rows(
        {"s": _story(events)},
        {e["id"]: e for e in events}, {}, {}, lambda s: s,
        since=datetime(2026, 10, 3, tzinfo=timezone.utc),
        recent_cutoff="2026-10-01", today="2026-10-03", last_digest="2026-10-02")[0]


r = _rows(forti)
check("echo bump does not evolve the story", r["evolved"], False)
check("echo bump does not move newest_development_at",
      r["newest_development_at"], orig["published_at"][:10])
check("echoes stay visible in n_events", r["n_events"], 2)

r = _rows(forti + [dev])
check("genuine development still evolves the story", r["evolved"], True)
check("development date comes from the real dev",
      r["newest_development_at"], dev["published_at"][:10])

# ── 4. re-report caps for outlet re-reports (2026-10-13 owner decision
# fc3f6e00a8d9): the min_gap_h burst skip is age-gated (first-day stories
# only) and the canonical story headline is an identity of its own. ─────────

# first-day: a pickup mimicking the canonical headline is legitimate burst
# velocity — the burst protection still applies while the story is young.
d1 = ev("d1", "Let's Encrypt cuts default certificate validity to 64 days", iso(6))
d2 = ev("d2", "Let's Encrypt cuts default certificate validity to 64 days", iso(5))
check("day-1 pickup of the canonical headline is burst velocity, not an echo",
      score.is_rereport(d2, [d1]), False)

# day-2: the SAME pickup shape lands within 24h of yesterday's re-tell of
# covered material — no longer skipped, it matches and caps the clock.
o1 = ev("o1", "Let's Encrypt cuts default certificate validity to 64 days", iso(50))
o2 = ev("o2", "Let's Encrypt reduces certificate lifetime to 64 days", iso(30))
o3 = ev("o3", "Let's Encrypt reduces certificate lifetime to 64 days", iso(20))
check("day-2 pickup matching only the close (yesterday) re-tell is a re-report",
      score.is_rereport(o3, [o1, o2]), True)

# canonical-headline echo: a reworded re-tell that overlaps the STORY title
# (what the coverage actually says) but no single prior event.
c1 = ev("c1", "The Gentlemen post new healthcare claims on leak site", iso(70))
c2 = ev("c2", "MoneyGram and Sant Pau records listed in hospital ransomware claim",
        iso(20))
STORY_T = "Hospital ransomware claim lists MoneyGram and Sant Pau records"
check("reworded re-tell alone does not match the priors (back-compat)",
      score.is_rereport(c2, [c1]), False)
check("...but the canonical story headline identifies it as covered material",
      score.is_rereport(c2, [c1], story_title=STORY_T), True)
c3 = ev("c3", "Hospital ransomware claim lists MoneyGram records", iso(20),
        ["CVE-2026-5678"])
check("a NEW CVE stays a development even against the canonical headline",
      score.is_rereport(c3, [c1], story_title=STORY_T), False)

# ── 5. no-new-delta echo condition (2026-10-17 owner decision f5f2bc09664a,
# audit Rec 2 re-report leg): a same-CVE disclosure is an echo ONLY with no
# new CVE, no new actor attribution, and no new exploitation confirmation.
# Attribution or in-the-wild proof emerging later is a development. ─────────

a1 = ev("a1", "FortiMail zero-day used to hack government mail servers",
         iso(72), ["CVE-2026-1234"])
a2 = ev("a2", "LockBit claims the FortiMail zero-day in government attacks",
         iso(24), ["CVE-2026-1234"])
check("same-CVE event naming a NEW actor is a development, not an echo",
      score.is_rereport(a2, [a1]), False)
a3 = ev("a3", "FortiMail zero-day fallout spreads, LockBit link unconfirmed",
         iso(12), ["CVE-2026-1234"])
check("same actor already in priors stays an echo",
      score.is_rereport(a3, [a1, a2]), True)

w1 = ev("w1", "FortiMail zero-day used to hack government mail servers",
         iso(72), ["CVE-2026-1234"])
w2 = ev("w2", "FortiMail zero-day now actively exploited in the wild",
         iso(24), ["CVE-2026-1234"])
check("same-CVE event with FRESH in-the-wild confirmation is a development",
      score.is_rereport(w2, [w1]), False)
w3 = ev("w3", "more FortiMail zero-day exploitation in the wild reported",
         iso(12), ["CVE-2026-1234"])
check("in-the-wild already in priors stays an echo",
      score.is_rereport(w3, [w1, w2]), True)
check("plain reworded re-tell still an echo (no-delta control)",
      score.is_rereport(echo, [orig]), True)

# hot_score level: story_title comes from the story itself, so an echo-only
# day-2 bump adds no velocity and the decay anchor stays on the development.
hd = [ev("h1", "Denmark CPR data breach exposed 8.8 million records", iso(60)),
      ev("h2", "Denmark CPR data breach exposed 8.8 million records, report says",
         iso(4))]
sch = _score(hd)
check("echo-only day-2 bump adds no velocity (hot_score)", sch["velocity"], 0.0)
check("echo-only day-2 bump counted as re-report", sch["rereports"], 1)
check("decay anchors to the genuine development (60h, not 4h)",
      sch["recency"] < 0.2, True)

# ── 6. zero-delta repost stubs (2026-10-18 owner decision 6aad368c1a1b,
# audit Rec 1a): an `rd:` Reddit link-post is 134-138c of boilerplate around
# the outlet headline and must not promote a story's rank unless it brings a
# new CVE, actor, victim count, or IOC. ────────────────────────────────────


def rd(eid, title, published, cves=(), body=""):
    """An `rd:` Reddit link-post stub: real headline, boilerplate content."""
    return {"id": eid, "title": title, "published_at": published,
            "cves": list(cves),
            "url": f"https://www.bleepingcomputer.com/{eid}",
            "source": "bleepingcomputer.com", "kind": "update", "lang": "en",
            "content_md": ("submitted by /u/someone [link] [comments]\n\n"
                           f"via reddit r/cybersecurity: {title}\n{body}")}


rbase = ev("rb1", "Candiru spyware campaign hit Middle East journalists",
           iso(60))
rstub = rd("rd:t3_a",
           "Targeted ads installed Candiru spyware in zero-click attacks",
           iso(2))
check("repost stub with no delta is a re-report (echo)",
      score.is_rereport(rstub, [rbase]), True)
sc_plain = _score([rbase])
sc_stub = _score([rbase, rstub])
check("a story whose only new event is an rd: stub does not gain rank",
      sc_stub["score"], sc_plain["score"])
check("...the stub adds zero velocity", sc_stub["velocity"], 0.0)
check("...the decay anchor stays on the genuine development",
      sc_stub["recency"], sc_plain["recency"])
check("...and the stub earns no pickup", sc_stub["pickup"], 0.0)

# the same stub WITH a genuine delta is a development and re-warms the story
rlock = rd("rd:t3_b", "LockBit claims the Candiru spyware campaign", iso(2))
check("...but the same stub naming a NEW actor is a development",
      score.is_rereport(rlock, [rbase]), False)
check("a stub with a new actor DOES promote the rank",
      _score([rbase, rlock])["score"] > sc_plain["score"], True)
rcve = rd("rd:t3_c", "Candiru spyware zero-day tracked as CVE-2026-4242",
          iso(2), ["CVE-2026-4242"])
check("a stub carrying a NEW CVE is a development",
      score.is_rereport(rcve, [rbase]), False)

# victim count: a grown count is a development, the same count is an echo
vprior = ev("rv1", "Candiru spyware campaign linked to 900 victims", iso(30))
vmore = rd("rd:t3_d", "Candiru spyware campaign linked to 4,100 victims",
           iso(2))
check("a stub carrying a NEW victim count is a development (count grew)",
      score.is_rereport(vmore, [vprior]), False)
vsame = rd("rd:t3_e", "Ads pushed Candiru spyware to 900 victims", iso(2))
check("a victim count already in the priors stays an echo (reworded stub)",
      score.is_rereport(vsame, [vprior]), True)

# IOC: a new observable is a development, a known one is an echo
iprior = ev("ri1", "Candiru spyware C2 server found at 45.153.160.10",
            iso(30))
inew = rd("rd:t3_f", "Candiru spyware C2 server found at 91.219.236.77",
          iso(2))
check("a stub naming a NEW IOC is a development (different C2 IP)",
      score.is_rereport(inew, [iprior]), False)
isame = rd("rd:t3_g",
           "Candiru spyware drops second-stage loader from 45.153.160.10",
           iso(2))
check("an IOC already in the priors stays an echo",
      score.is_rereport(isame, [iprior]), True)

# novelty: an rd: stub's boilerplate-wrapped headline must never mint the
# corroborated-novelty bonus for a story it did not develop.
nov_prior = ev("nz1", "Fake LastPass authenticator pushes malware at users",
               iso(20))
nov_stub = rd("rd:t3_h", "Tox C2 loader dropper used by the stealer", iso(2))


def _nov_story(events):
    s = _story(events)
    s["sources"] = ["example.com", "example.org"]
    s["n_sources"] = 2
    return s


sc_nov = score.hot_score(_nov_story([nov_prior, nov_stub]),
                         {e["id"]: e for e in [nov_prior, nov_stub]},
                         [], now=BASE)
check("an rd: stub never mints the corroborated-novelty bonus",
      sc_nov["novelty"], 0.0)
nov_dev = ev("nz2", "Tox C2 loader dropper used by the stealer", iso(20))
check("a genuine TTP development still earns novelty (control)",
      score.hot_score(_nov_story([nov_dev]), {"nz2": nov_dev}, [],
                      now=BASE)["novelty"], 0.5)

# ── 5. covered-advisory re-tells (2026-10-23 audit Recommendation 3 / owner
# decision 2e4fa50d91a0). The 2026-10-23 demote class (Splunk, Onamae,
# Claude-Code campaigns, Cisco UCM, Node.js, Oracle CPU, GitLab
# CVE-2026-110264) all showed zero_delta:false because an outlet re-tell that
# names the already-covered CVE only in its BODY — or a founding event whose
# body names it while its title does not — was read as a NEW disclosure.
print("== covered-advisory re-tells ==")


def ev_body(eid, title, published, cves=(), body=""):
    e = ev(eid, title, published, cves)
    e["content_md"] = body
    return e


founding_body = ev_body(
    "g1", "GitLab fixes dangerous pre-auth RCE after ten years in code",
    iso(60), (), "GitLab patched CVE-2026-4321: a CVSS 10 pre-auth RCE.")
check("founding event is never a re-report (body-named CVE too)",
      score.is_rereport(founding_body, [], story_title="Pre-auth RCE in GitLab fixed"), False)

body_echo = ev_body(
    "g2", "Patch now: the GitLab regex engine flaw is being patched everywhere",
    iso(20), (), "The GitLab issue is CVE-2026-4321, a CVSS 10 pre-auth RCE.")
check("body-named COVERED cve + reworded headline is a re-report",
      score.is_rereport(body_echo, [founding_body],
                        story_title="Pre-auth RCE in GitLab fixed after ten years"), True)

body_new = ev_body(
    "g3", "GitLab also fixes an unrelated SSRF in the same release",
    iso(20), (), "Separately tracked as CVE-2026-9999, an SSRF in GitLab.")
check("body-named NEW cve is still a development",
      score.is_rereport(body_new, [founding_body],
                        story_title="Pre-auth RCE in GitLab fixed after ten years"), False)

# story-level identity: the story itself carries the CVE, so an outlet re-tell
# that names it later is an echo even when no single prior names it
story_carry = ev_body(
    "g4", "Splunk fixes 31 Splunk vulnerabilities in Enterprise and Splunk SOAR",
    iso(26), (), "Splunk shipped SVD-2026-1001 covering CVE-2026-7777.")
# ── 6. KEV addition is a delta, never an echo ─────────────────────────────────
print("== KEV addition is a development ==")
kev_prior = ev_body("k1", "Nextcloud Collabora flaw exploited in the wild",
                    iso(120), ["CVE-2026-110447"], "Attackers exploit it.")
kev_add = ev_body("k2", "Added to CISA's Known Exploited Vulnerabilities catalog: "
                        "CVE-2026-110447",
                  iso(10), ["CVE-2026-110447"], "Due date Oct 26.")
check("a CISA KEV addition is a development, not a re-report",
      score.is_rereport(kev_add, [kev_prior], story_title="Nextcloud Collabora Online Active Exploitation"), False)
check("a second KEV mention IS a re-report (the development is spent)",
      score.is_rereport(ev_body("k2b", "Added to the KEV catalog: CVE-2026-110447",
                                iso(8), ["CVE-2026-110447"], "Due Oct 26."),
                        [kev_prior, kev_add],
                        story_title="Nextcloud Collabora Online Active Exploitation"), True)
plain_echo = ev_body("k3", "Nextcloud Collabora flaw exploited in the wild, ",
                     iso(10), ["CVE-2026-110447"], "Attackers exploit it.")
check("control: a plain re-tell with no delta stays a re-report",
      score.is_rereport(plain_echo, [kev_prior],
                        story_title="Nextcloud Collabora Online Active Exploitation"), True)


def _kev_story(evs):
    return {"id": "kevstory", "title": "Nextcloud Collabora Online Active Exploitation",
            "sources": ["example.com", "example.org"],
            "n_sources": 2, "cves": ["CVE-2026-110447"],
            "events": [{"event_id": e["id"], "label": "update"} for e in evs],
            "last_seen": evs[-1]["published_at"],
            "reddit_signal": {"posts": 0, "best_score": 0}}


kev_sc = score.hot_score(_kev_story([kev_prior, kev_add]),
                         {e["id"]: e for e in [kev_prior, kev_add]},
                         [], now=BASE)
check("a story bumped by a KEV addition is not demoted",
      (kev_sc["zero_delta"], kev_sc["zero_delta_penalty"]), (False, 0.0))
check("the KEV addition is the decay anchor (fresh recency, not the founding)",
      kev_sc["recency"] > 0.7, True)
check("the KEV addition still earns no echo velocity (first-hand only)",
      kev_sc["velocity"], 0.5)

# ── 7. end-to-end: a newest event that merely restates a covered advisory
# sets zero_delta (2026-10-23 audit Rec 3, owner decision 2e4fa50d91a0) ───────
print("== covered-advisory re-tell demotes the story ==")


def _adv_story(evs):
    return {"id": "adv", "title": "GitLab patches a critical regex RCE flaw",
            "sources": ["example.com"], "n_sources": 1, "cves": [],
            "events": [{"event_id": e["id"], "label": "update"} for e in evs],
            "last_seen": evs[-1]["published_at"],
            "reddit_signal": {"posts": 0, "best_score": 0}}


adv_found = ev_body("a1", "GitLab patches a critical regex engine RCE flaw",
                    iso(60), (), "The bug is CVE-2026-4242.")
adv_echo = ev_body("a2", "GitLab fixes a critical regex engine RCE (much later)",
                   iso(3), (), "Tracked as CVE-2026-4242 by GitLab.")
check("the re-tell is classified as a re-report",
      score.is_rereport(adv_echo, [adv_found],
                        story_title="GitLab patches a critical regex RCE flaw"),
      True)
adv_sc = score.hot_score(_adv_story([adv_found, adv_echo]),
                         {e["id"]: e for e in [adv_found, adv_echo]},
                         [], now=BASE)
check("...and the story is demoted zero_delta with a visible penalty",
      (adv_sc["zero_delta"], adv_sc["zero_delta_penalty"] > 0), (True, True))
adv_dev = ev_body("a3", "GitLab patches a critical regex engine RCE (much later)",
                  iso(3), (), "The bug is CVE-2026-4242; CVE-2026-5252 also "
                              "fixed in the same release.")
adv_sc2 = score.hot_score(_adv_story([adv_found, adv_dev]),
                          {e["id"]: e for e in [adv_found, adv_dev]},
                          [], now=BASE)
check("a re-tell that brings a NEW CVE keeps the story's score",
      (adv_sc2["zero_delta"], adv_sc2["score"] > adv_sc["score"]), (False, True))

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {failures}")
    sys.exit(1)
print("all checks passed")
