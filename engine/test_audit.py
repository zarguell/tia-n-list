#!/usr/bin/env python3
"""Judgment-layer audit contract suite (2026-08-24).

The triage-drift incident (Aug 17-24) produced duplicates the output-level
audit could not see. This suite pins the audit_checks contracts so the
auditor catches that failure class same-day:

  1. dedup_invariants FAILs on: multi-referenced events, merged_into cycles,
     events inside redirect shells, same-base slug duplicates; distinct
     advisory codes exonerate same-base collisions; ghosts stay informational.
  2. duplicate_suspects finds real near-dups, excludes actor-only matches
     (one shared token) and distinct-advisory pairs.
  3. language_scan flags CJK/Cyrillic bleed, ignores accents/emoji.
  4. triage_telemetry detects WARN drift, silent drift (runs, no decisions),
     and permissive triage; clean 24h passes.
  5. digest_overrides aggregates across digests.

Run: python3 engine/test_audit.py   (exit 0 = pass)
"""
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_checks as jc  # noqa: E402

NOW = datetime(2026, 8, 24, 13, 0, tzinfo=timezone.utc)
failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


def story(sid, events=(), merged_into=None, title=None, last_seen="2026-08-24T00:00:00Z",
          first_seen="2026-08-20T00:00:00Z"):
    return {"id": sid, "title": title or sid, "events": [{"event_id": e} for e in events],
            "merged_into": merged_into, "last_seen": last_seen, "first_seen": first_seen}


# ── 1. dedup_invariants ───────────────────────────────────────────────────────
ok, detail, ghosts = jc.dedup_invariants({
    "clean-a": story("clean-a", ["e1"], title="Citrix NetScaler flaw exploited"),
    "clean-b": story("clean-b", ["e2"], title="Clop ransomware hits Acme Corp"),
})
check("clean store passes", (ok, ghosts), (True, 0))

ok, d, _ = jc.dedup_invariants({
    "a": story("a", ["e1"]), "b": story("b", ["e1"]),
})
check("multi-referenced event fails", ok, False)

ok, d, _ = jc.dedup_invariants({
    "a": story("a", [], merged_into="b"),
    "b": story("b", [], merged_into="a"),
})
check("redirect cycle fails", ok, False)

ok, d, _ = jc.dedup_invariants({
    "shell": story("shell", ["e1"], merged_into="live"),
    "live": story("live", ["e1", "e2"]),
})
check("event inside redirect shell fails", ok, False)

ok, d, _ = jc.dedup_invariants({
    "foo-2": story("foo-2", ["e1"], title="Critical WordPress Pods flaw exploited"),
    "foo": story("foo", ["e2"], title="Critical WordPress Pods flaw exploited in attacks"),
})
check("same-base duplicate fails", ok, False)

ok, d, ghosts = jc.dedup_invariants({
    "apple-security-advisory-av26-839": story("apple-security-advisory-av26-839", ["e1"],
                                              title="Apple security advisory (AV26-839)"),
    "apple-security-advisory-av26-823": story("apple-security-advisory-av26-823", ["e2"],
                                              title="Apple security advisory (AV26-823)"),
    "ghost": story("ghost", [], title="dropped long ago"),
})
check("distinct advisory codes exonerate; ghost informational only", (ok, ghosts), (True, 1))

ok, d, _ = jc.dedup_invariants({
    "jetbrains-security-advisory-av26-891": story(
        "jetbrains-security-advisory-av26-891", ["e1"],
        title="JetBrains September 2026 Security Advisory"),
    "jetbrains-security-advisory-av26-825": story(
        "jetbrains-security-advisory-av26-825", ["e2"],
        title="JetBrains security advisory (AV26-825)"),
})
check("advisory id in the slug exonerates a one-sided title", ok, True)

ok, d, _ = jc.dedup_invariants({
    "orphan-shell": story("orphan-shell", [], merged_into="missing-target"),
    "live": story("live", ["e1"]),
})
check("dangling redirect shell fails", ok, False)
check("dangling redirect names the dead target", "missing-target" in d, True)

# ── 1c. id_hygiene (2026-10-06): stem!=id twins and duplicate ids ──────────
# load_all_stories keys by id so it collapses duplicates — id_hygiene counts
# FILES, hence the tmp-dir fixture (same pattern as the language_scan tests).
def _hyg_dir(files):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "stories"))
    for stem, sid in files:
        json.dump({"id": sid, "title": stem, "events": []},
                  open(os.path.join(d, "stories", stem + ".json"), "w"))
    return d


ok, detail = jc.id_hygiene(_hyg_dir([("story-a", "story-a"),
                                     ("story-b", "story-b")]))
check("clean store passes id_hygiene", ok, True)

ok, detail = jc.id_hygiene(_hyg_dir([("legacy-slug-name", "real-id"),
                                     ("good", "good")]))
check("stem mismatch detected", ok, False)
check("stem mismatch names the file", "legacy-slug-name.json" in detail, True)

ok, detail = jc.id_hygiene(_hyg_dir([("slug-a", "shared"),
                                     ("slug-b", "shared")]))
check("duplicate ids detected", ok, False)
check("duplicate detail names the id", "shared" in detail, True)

# ── 2. duplicate_suspects ────────────────────────────────────────────────────
stories = {
    "chrome-151-a": story("chrome-151-a", ["e1"], title="Google Chrome 151 Update Fixes 5 High Severity Flaws"),
    "chrome-151-b": story("chrome-151-b", ["e2"], title="Google Chrome 151 Patches Critical Use-After-Free Vulnerability"),
    "clop-aol": story("clop-aol", ["e3"], title="Clop ransomware strikes AOL.com"),
    "clop-fis": story("clop-fis", ["e4"], title="Clop ransomware targets FIS Global"),
    "av-791": story("av-791", ["e5"], title="HashiCorp security advisory AV26-791 critical flaws"),
    "av-797": story("av-797", ["e6"], title="HashiCorp security advisory AV26-797 critical flaws"),
    "old": story("old", ["e7"], title="Google Chrome 151 Update Fixes 5 High Severity Flaws",
                 last_seen="2025-01-01T00:00:00Z"),
}
s = jc.duplicate_suspects(stories, NOW)
pairs = {frozenset((x["a"], x["b"])) for x in s}
check("real near-dup suspected", frozenset(("chrome-151-a", "chrome-151-b")) in pairs, True)
check("actor-only match not suspected", frozenset(("clop-aol", "clop-fis")) in pairs, False)
check("distinct advisory codes not suspected", frozenset(("av-791", "av-797")) in pairs, False)
check("stale story outside window", any("old" in p for p in pairs), False)

# ── 2b. distinct_periods (2026-10-03): recurring-series installments are not
# duplicate suspects. title_discriminators strips month tokens, so different
# months of the same monthly report scored jaccard 1.0 and were flagged —
# dismissed by the auditor two days running.
check("asec july vs august exonerated",
      any("asec" in p for p in pairs), False)
series = {
    "asec-july": story("asec-july", ["e10"],
                       title="ASEC StringTie Malware Trends Report July 2026"),
    "asec-aug": story("asec-aug", ["e11"],
                      title="ASEC StringTie Malware Trends Report August 2026"),
    "asec-july-2": story("asec-july-2", ["e12"],
                         title="ASEC StringTie Malware Trends July 2026 Update"),
}
s2 = jc.duplicate_suspects(series, NOW)
pairs2 = {frozenset((x["a"], x["b"])) for x in s2}
check("different-month installments not suspected",
      frozenset(("asec-july", "asec-aug")) in pairs2, False)
check("same-month near-dup still suspected",
      frozenset(("asec-july", "asec-july-2")) in pairs2, True)
check("distinct_periods flags disjoint months",
      jc.distinct_periods("Report July 2026", "Report August 2026"), True)
check("distinct_periods shared month is not distinct",
      jc.distinct_periods("Report July 2026", "July 2026 update"), False)
check("distinct_periods needs both sides",
      jc.distinct_periods("Report July 2026", "Report on ASEC trends"), False)
check("period tokens: verb-ambiguous march/may excluded",
      jc.period_tokens("Actors may march through the network in June"), {"june"})
check("period tokens: week-N and quarters", jc.period_tokens("DFIR week-3 Q3 h1 report"),
      {"week-3", "q3", "h1"})

# ── 2c. non-generic token gate (2026-10-13 owner decision ed5750725299) ──────
# All 10 suspects on 10-13 were cross-product "remote code execution"
# boilerplate collisions (Frappe LMS / IBM MQ / Issabel PBX / ArubaOS-CX /
# Forgejo / UANIA OS); the Midnight Mimosa pair the auditor merged the same
# day is the genuine class that must still surface.
rce_noise = {
    "frappe-lms": story("frappe-lms", ["e20"],
                        title="Frappe LMS Remote Code Execution Vulnerabilities"),
    "ibm-mq": story("ibm-mq", ["e21"],
                    title="Critical IBM MQ Remote Code Execution Vulnerabilities"),
    "issabel": story("issabel", ["e22"],
                     title="Issabel PBX remote code execution exploited in active attacks"),
    "aruba": story("aruba", ["e23"],
                   title="HPE patches critical ArubaOS-CX remote code execution flaw"),
}
check("generic-token RCE collisions no longer suspected (10-13's 10 rows)",
      jc.duplicate_suspects(rce_noise, NOW), [])

mimosa = {
    "bitdefender-mimosa": story(
        "bitdefender-mimosa", ["e30"],
        title="Bitdefender reports Midnight Mimosa malware in cheap MediaTek Android firmware"),
    "mimosa-android": story(
        "mimosa-android", ["e31"],
        title="Midnight Mimosa: ad-fraud malware preinstalled in cheap Android phone firmware"),
}
s_mimosa = jc.duplicate_suspects(mimosa, NOW)
# 2d. identity-anchor redesign (2026-10-17 owner decision 84991a8ec82c):
# the 10-13 generic-token gate still surfaced 10 unrelated pairs on 10-17
# (all manually dismissed). Replicas of the false classes must stay out;
# anchored genuine pairs (shared CVE, shared event) must surface.
def _cstory(sid, evs, title, cves=()):
    s = story(sid, evs, title=title)
    s["cves"] = list(cves)
    return s


false_pairs = {
    # Ivanti-vs-Citrix/Fortinet (must not surface per the card): outlet
    # roundup shares the vendor token, CVE sets are asymmetric.
    "ivanti-a": _cstory("ivanti-a", ["e40"],
                          title="Ivanti Patches Critical Flaws Across Enterprise Security Products"),
    "ivanti-b": _cstory("ivanti-b", ["e41"],
                          title="Citrix, Fortinet, Ivanti Patch 29 Vulnerabilities Across Their Products",
                          cves=["CVE-2026-104935", "CVE-2026-106173"]),
    # Ampath-vs-AdaptHealth: different victims, CVE-empty both sides.
    "ampath": _cstory("ampath", ["e42"],
                        title="Ampath Patient Records Data Breach"),
    "adapt": _cstory("adapt", ["e43"],
                       title="AdaptHealth Breach Exposes 4.1M Patient Records"),
    # Apache-vs-Next.js: different products, CVE-empty both sides.
    "apache": _cstory("apache", ["e44"],
                        title="Apache HTTP Server Flaws Enable Remote Code Execution and Denial-of-Service Attacks"),
    "nextjs": _cstory("nextjs", ["e45"],
                        title="Next.js Patches Critical Remote Code Execution and Denial of Service Flaws"),
    # kernel CVE pair: disjoint CVE sets, same subsystem phrasing.
    "kern-a": _cstory("kern-a", ["e46"],
                        title="CVE-2026-89521 Linux Kernel Core Scheduling Race Condition",
                        cves=["CVE-2026-89521"]),
    "kern-b": _cstory("kern-b", ["e47"],
                        title="Linux Kernel Race Condition in net/smc Subsystem",
                        cves=["CVE-2026-80980"]),
}
s_false = jc.duplicate_suspects(false_pairs, NOW)
pairs_false = {frozenset((x["a"], x["b"])) for x in s_false}
check("Ivanti-vs-Citrix/Fortinet must not surface",
      frozenset(("ivanti-a", "ivanti-b")) in pairs_false, False)
check("Ampath-vs-AdaptHealth must not surface",
      frozenset(("ampath", "adapt")) in pairs_false, False)
check("Apache-vs-Next.js must not surface",
      frozenset(("apache", "nextjs")) in pairs_false, False)
check("disjoint-CVE kernel pair must not surface",
      frozenset(("kern-a", "kern-b")) in pairs_false, False)

genuine = {
    # GhostAction class: pre-merge pair sharing an event surfaces even
    # when the headlines were reworded past the similarity gates.
    "ghost-a": _cstory("ghost-a", ["e50"],
                         title="GhostAction breach claim hits hospital extranet"),
    "ghost-b": _cstory("ghost-b", ["e50", "e51"],
                         title="Unrelated phrasing on an infrastructure outage report"),
    # same-CVE pair with matching titles: the shared CVE anchors it.
    "cve-a": _cstory("cve-a", ["e52"],
                       title="Acme router CVE-2026-1234 remote code flaw",
                       cves=["CVE-2026-1234"]),
    "cve-b": _cstory("cve-b", ["e53"],
                       title="Acme router CVE-2026-1234 remote code bug fix",
                       cves=["CVE-2026-1234"]),
}
s_gen = jc.duplicate_suspects(genuine, NOW)
pairs_gen = {frozenset((x["a"], x["b"])) for x in s_gen}
check("shared-event pair surfaces despite reworded titles",
      frozenset(("ghost-a", "ghost-b")) in pairs_gen, True)
check("shared-CVE pair with matching titles surfaces",
      frozenset(("cve-a", "cve-b")) in pairs_gen, True)
row = next(x for x in s_gen
           if frozenset((x["a"], x["b"])) == frozenset(("ghost-a", "ghost-b")))
check("shared-event row is flagged", row.get("shared_events"), True)

# week-number installments discriminate even when the month is shared
# (Ransom Week 2 vs Week 3, October 2026: jaccard 1.0, no anchor).
check("distinct week numbers exonerate (shared month)",
      jc.distinct_periods("Ransom & Dark Web Issues Week 3, October 2026",
                          "Ransom & Dark Web Issues Week 2, October 2026"), True)
check("same week number is not distinct",
      jc.distinct_periods("Ransom & Dark Web Issues Week 3, October 2026",
                          "Ransom Week 3 roundup, October 2026"), False)
check("genuine same-story pair (Midnight Mimosa pre-merge) still surfaces",
      {frozenset((x["a"], x["b"])) for x in s_mimosa},
      {frozenset(("bitdefender-mimosa", "mimosa-android"))})

# ── 1b. roundup_family (fragmentation classifier) ────────────────────────────
check("dedicated Microsoft PT roundup",
      jc.roundup_family("Microsoft's September 2026 Patch Tuesday fixes two zero-day flaws"),
      "microsoft")
check("date-first Microsoft PT roundup",
      jc.roundup_family("September 2026 Microsoft Patch Tuesday: record CVE count"),
      "microsoft")
check("comma AFTER Patch Tuesday is still dedicated",
      jc.roundup_family("Microsoft Patch Tuesday: 974 CVEs, plus Adobe fixes"), "microsoft")
check("chipmaker advisory without month ref is its own story, not a roundup",
      jc.roundup_family("Chipmaker Patch Tuesday: Nvidia, AMD, Arm Issue Security Advisories"),
      None)
check("dedicated non-Microsoft roundup WITH month ref stays in other family",
      jc.roundup_family("September 2026 Patch Tuesday: virtualization and middleware critical RCEs"),
      "other")
check("legacy CVE enumeration is not a numbered roundup (2026-09-22 audit FP)",
      jc.roundup_family("Legacy Windows CVEs (CVE-2011-3402, CVE-2013-3918) under active exploitation"),
      None)
check("numbered Windows roundup with month ref still classified",
      jc.roundup_family("Adobe Fixes 130 Vulnerabilities Affecting Windows, September Release"),
      "other")
check("ICS roundup family",
      jc.roundup_family("ICS Patch Tuesday: Siemens and Schneider fix flaws"), "ics")
check("multi-topic digest is not a roundup",
      jc.roundup_family("WeChat 0-click worm, Hacking Customer Service AI agents, "
                        "Biggest Microsoft Patch Tuesday"), None)
check("'V8 flaws' is not a numbered Windows roundup",
      jc.roundup_family("Proofpoint identified BlueMoon, an exploit kit chaining "
                        "two Chrome/V8 flaws with a Windows privilege escalation."), None)
check("meta-story mentioning Windows flaws is not a roundup",
      jc.roundup_family("Expects More Security Updates From AI-Discovered Flaws"), None)

# ── 3. language_scan ─────────────────────────────────────────────────────────
tmp = tempfile.mkdtemp()
os.makedirs(os.path.join(tmp, "analysis"))
os.makedirs(os.path.join(tmp, "digests"))
open(os.path.join(tmp, "analysis", "clean.md"), "w").write(
    "Plain English with café, naïve, and emoji 🔴 headline. Fine.")
open(os.path.join(tmp, "analysis", "bleed.md"), "w").write(
    "The actor conducted 勒索 for payment via bitcoin.")
open(os.path.join(tmp, "digests", "2026-08-23.md"), "w").write(
    "Cyrillic bleed: атака on utility.")
hits = jc.language_scan(tmp)
check("cjk and cyrillic flagged, accents/emoji ignored",
      (len(hits), "bleed.md" in hits[0], "2026-08-23.md" in hits[1]), (2, True, True))

# ── 3b. backticked code spans are exempt (2026-10-13 owner decision
# 19fa08f9defd): the ARTEX CJK IOC quoted in `…` passes, the same string in
# prose still fails — the pin that keeps the exemption from swallowing bleed.
tmp_spans = tempfile.mkdtemp()
os.makedirs(os.path.join(tmp_spans, "analysis"))
os.makedirs(os.path.join(tmp_spans, "digests"))
open(os.path.join(tmp_spans, "analysis", "ioc.md"), "w").write(
    "Sweep page titles for `ARTEX-自主渗透测试控制台` exactly, and check "
    "`基盤` fences too.\n\nSecond paragraph stays plain English.")
open(os.path.join(tmp_spans, "analysis", "prose-bleed.md"), "w").write(
    "The write-up quotes the console name 勒索 demand in running prose.")
open(os.path.join(tmp_spans, "digests", "2026-10-13.md"), "w").write(
    "Digest naming `ARTEX-自主渗透测试控制台` in a code span. Only.")
spans_hits = jc.language_scan(tmp_spans)
check("CJK in backticked code spans passes",
      any("ioc.md" in h for h in spans_hits), False)
check("digest code span passes too",
      any("2026-10-13.md" in h for h in spans_hits), False)
check("CJK in prose still fails",
      (len(spans_hits), "prose-bleed.md" in spans_hits[0]), (1, True))
check("prose hit context still shows the bleed word", "勒索" in spans_hits[0], True)

# the real day-6 driver: the ARTEX analysis is clean once its two backticked
# IOC occurrences are exempted (no store content edits — check semantics only)
artex_dir = os.path.dirname(os.path.abspath(__file__))
check("store-wide scan has no non-span bleed left (ARTEX file exempt)",
      [h for h in jc.language_scan(os.path.join(artex_dir, "data"))
       if "unknown-threat-actor-uses-ai-driven-artex" in h], [])

# ── 4. triage_telemetry ──────────────────────────────────────────────────────
tlog = tempfile.mkdtemp()
tdir = tempfile.mkdtemp()
today = NOW.strftime("%Y-%m-%d")
open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n"
    "triage applied: 4 kept/moved, 1 dropped, 5 merges, needs-analysis 1\n"
    "  WARN: 2 decision entries could not be parsed\n")
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("drift WARN detected", any("unparsed" in p for p in problems), True)

open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n"
    "triage applied: 0 kept/moved, 0 dropped, 0 merges\n")
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("silent drift detected", any("silent drift" in p for p in problems), True)

open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n")
json.dump({"decisions": [{"action": "keep"} for _ in range(20)]},
          open(os.path.join(tdir, "decisions-x.json"), "w"))
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("permissive triage detected", any("permissive" in p for p in problems), True)

open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n"
    "  WARN: keep -> unknown story oracle-september-2026-cpu-patches-672-cves for mf:163813; "
    "minting once — further keeps naming it consolidate here\n"
    "  WARN: keep -> unknown story oracle-september-2026-cpu-patches-672-cves for masto:11727707; "
    "minting once — further keeps naming it consolidate here\n")
json.dump({"decisions": [{"action": "keep"} for _ in range(14)] +
                    [{"action": "drop"} for _ in range(6)]},
          open(os.path.join(tdir, "decisions-x.json"), "w"))
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("unknown-story WARN detected", any("keep->unknown-story" in p for p in problems), True)

open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=5 created=4 needs_analysis=1)\n")
json.dump({"decisions": [{"action": "keep"} for _ in range(14)] +
                    [{"action": "drop"} for _ in range(6)]},
          open(os.path.join(tdir, "decisions-x.json"), "w"))
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("healthy triage passes", problems, [])
check("ratio reported", "keep/drop 14/6 (70% keep)" in info, True)

# Narration that merely quotes a WARN phrase must not trip the invariant:
# on 2026-09-26 and 2026-09-27 the hourly agent narrated "no keep/drop
# decisions recognized" into this log and triage_drift FAILED twice with no
# real WARN line present (both matches were agent prose).
open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=0 created=0 needs_analysis=1)\n"
    "STEP 1 — Triage gate: 0 new events in the 48h window, so decisions array "
    "is empty; the script emitted a false-positive \"no keep/drop decisions "
    "recognized\" WARN because the array is empty, but ignored=0.\n")
json.dump({"decisions": [], "merges": []},
          open(os.path.join(tdir, "decisions-x.json"), "w"))
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("narration of a WARN phrase does not trip triage_drift",
      any("no decisions recognized" in p for p in problems), False)

open(os.path.join(tlog, today + ".log"), "w").write(
    "2026-08-24T11:00:12Z TIA pi judgment (new=0 created=0 needs_analysis=1)\n"
    "  WARN: no keep/drop decisions recognized — schema mismatch? Expected "
    "top-level 'decisions' array with event_id/action/story keys\n")
problems, info = jc.triage_telemetry(tlog, tdir, NOW)
check("real WARN line still trips triage_drift",
      any("no decisions recognized" in p for p in problems), True)

# ── 5. digest_overrides ──────────────────────────────────────────────────────
ddir = os.path.join(tmp, "digests")
json.dump({"stories": [], "overrides": [
    {"slug": "a", "action": "wildcard", "why": "regional scoop"}]},
    open(os.path.join(ddir, "2026-08-23.json"), "w"))
json.dump({"stories": []}, open(os.path.join(ddir, "2026-08-24.json"), "w"))
ov = jc.digest_overrides(tmp)
check("overrides aggregated newest-first",
      [(o["digest"], o["action"]) for o in ov], [("2026-08-23", "wildcard")])

# ── 6. ingest_noise (2026-09-16 gamefan/thehackerwire incident class) ────────
NOW2 = datetime(2026, 9, 16, 13, 0, tzinfo=timezone.utc)


def _mk_noise_dir(tmp, events, decisions, raw_toots=None):
    edir = os.path.join(tmp, "events"); os.makedirs(edir)
    tdir = os.path.join(tmp, "triage"); os.makedirs(tdir)
    for eid, ev in events.items():
        meta = {"id": eid, "source": ev["source"],
                "published_at": ev.get("published_at", "")}
        if ev.get("excluded"):
            meta["excluded"] = True
        json.dump(meta, open(os.path.join(edir, eid + ".json"), "w"))
        open(os.path.join(edir, eid + ".md"), "w").write("x" * ev.get("md_len", 2000))
    for ts, dec in decisions.items():
        json.dump({"decisions": dec},
                  open(os.path.join(tdir, f"decisions-{ts}.json"), "w"))
    if raw_toots is None:
        return None
    rdir = os.path.join(tmp, "raw"); os.makedirs(rdir)
    with open(os.path.join(rdir, "toots-20260916.jsonl"), "w") as f:
        for r in raw_toots:
            f.write(json.dumps(r) + "\n")
    return os.path.join(rdir, "toots-*.jsonl")


ev, dec, toots = {}, {}, []
for i in range(30):  # junk source at 93% drop, attributed to a tag-spam author
    eid = f"masto:100{i:02d}"
    ev[eid] = {"source": "spam.example", "published_at": "2026-08-01T00:00:00Z"}
    dec[eid] = "drop" if i < 28 else "keep"
    toots.append({"id": f"100{i:02d}", "author": "spam@bot.example"})
for i in range(12):  # kept-stub source: kept but content-free
    ev[f"s{i}"] = {"source": "stub.example", "published_at": "2026-08-01T00:00:00Z",
                   "md_len": 150}
    dec[f"s{i}"] = "keep"
for i in range(60):  # flood entrant: brand-new source, half the store
    ev[f"f{i}"] = {"source": "flood.example", "published_at": "2026-09-15T00:00:00Z"}
noise_events = {eid: {**meta, "excluded": dec[eid] == "drop"}
                for eid, meta in ev.items() if eid in dec}
noise_events.update({eid: meta for eid, meta in ev.items() if eid not in dec})
noise_decs = {
    "2026-09-16T1100": [{"event_id": e, "action": a} for e, a in dec.items()],
    "2026-09-16T1000": [],
    # non-hourly filename: must be IGNORED (a parsed drop here would make it
    # "31 decisions" and skew every count below)
    "frag2": [{"event_id": "masto:10000", "action": "drop"}],
}
rglob = _mk_noise_dir(os.path.join(tmp, "noise"), noise_events, noise_decs, toots)
p, info = jc.ingest_noise(os.path.join(tmp, "noise"), NOW2, raw_glob=rglob)
check("junk source flagged", any(x.startswith("junk source spam.example") for x in p), True)
check("tag-spam author flagged",
      any(x.startswith("tag-spam author spam@bot.example: 30 decisions") for x in p),
      True)
check("kept-stub source flagged",
      any(x.startswith("kept-stub source stub.example") for x in p), True)
check("flood entrant flagged",
      any(x.startswith("flood entrant flood.example") for x in p), True)
check("info tables present", len(info["sources"]) > 0 and len(info["authors"]) > 0, True)

# 2026-10-18 decision 64afd59af45e (audit Issue 1): `rd:` Reddit link-post
# stubs are content-free BY CONSTRUCTION, and their `source` is
# domain_of(article_url) — so the LINKED host (bleepingcomputer.com in the
# live FAIL) was being blamed for Reddit's boilerplate. They stay decisions,
# but never count as kept-stubs.
rd_events = {f"rd:t3_{i:02d}": {"source": "bleepingcomputer.com",
                                "published_at": "2026-08-01T00:00:00Z",
                                "md_len": 150} for i in range(12)}
rd_decs = {"2026-09-16T1100": [{"event_id": e, "action": "keep"}
                               for e in rd_events]}
_mk_noise_dir(os.path.join(tmp, "rdstubs"), rd_events, rd_decs)
p3, info3 = jc.ingest_noise(os.path.join(tmp, "rdstubs"), NOW2)
check("rd: link-post stubs are not counted as kept-stubs",
      any(x.startswith("kept-stub source bleepingcomputer.com") for x in p3),
      False)
check("...and the source's kept-stub rate reads 0",
      [r for r in info3["sources"]
       if r["name"] == "bleepingcomputer.com"][0]["kept_stub_pct"], 0)

clean_events = {f"g{i}": {"source": "fine.example",
                          "published_at": "2026-08-01T00:00:00Z"}
                for i in range(30)}
clean_decs = {"2026-09-16T1100": [
    {"event_id": f"g{i}", "action": "keep" if i < 20 else "drop"}
    for i in range(30)]}
_mk_noise_dir(os.path.join(tmp, "clean"), clean_events, clean_decs)
p2, _ = jc.ingest_noise(os.path.join(tmp, "clean"), NOW2)
check("healthy store passes", p2, [])

# ── 7. automation_status (2026-10-03): job-log run status replaces the
# OpenHands service API that never existed on this host (keyless vacuous
# pass, 3 days running).
NOW3 = datetime(2026, 10, 3, 13, 30, tzinfo=timezone.utc)
tmp3 = tempfile.mkdtemp()
try:
    def _log(name, lines):
        p = os.path.join(tmp3, name)
        open(p, "w").write("\n".join(lines) + "\n")
        return p

    st, d = jc.automation_status(
        _log("ok.log", [
            "2026-10-03T13:09:01Z PHASE3 publish",
            "2026-10-03T13:09:03Z DONE"]), NOW3)
    check("bare DONE completes", (st, d), ("COMPLETED", "completed 2026-10-03T13:09"))

    st, d = jc.automation_status(
        _log("fail.log", [
            "2026-10-03T11:00:00Z DONE",
            "2026-10-03T12:00:00Z DONE (publish failed)"]), NOW3)
    check("parered DONE is a failure (latest terminal wins)", st, "FAILED")

    st, d = jc.automation_status(
        _log("skip.log", ["2026-10-03T11:16:01Z DONE",
                          "2026-10-03T11:16:01Z NOTIFY: sent"]), NOW3)
    check("DONE beats later non-terminal lines", st, "COMPLETED")

    st, _ = jc.automation_status(
        _log("stale.log", ["2026-10-01T11:16:01Z DONE"]), NOW3)
    check("silent > 24h is stale", st, "STALE")

    st, _ = jc.automation_status(os.path.join(tmp3, "missing.log"), NOW3)
    check("missing log is MISSING", st, "MISSING")

    st, _ = jc.automation_status(
        _log("midrun.log", ["2026-10-03T13:20:00Z PHASE1 ingest"]), NOW3)
    check("no terminal line is MISSING (crashed mid-run)", st, "MISSING")
finally:
    import shutil as _sh
    _sh.rmtree(tmp3, ignore_errors=True)

# ── 7b. RUNNING heuristic + live-process cross-check (2026-10-13, owner
# decision 321115dd4f0a): a fresh log mid-run used to report MISSING and fail
# automation_runs while the run was healthy. RUNNING requires BOTH a fresh
# log AND a confirmed live process — fresh + no live run stays MISSING (a
# crash inside stale_hours leaves a fresh log too), and a log untouched for
# hours with no terminal line stays MISSING even if the probe claims live.
tmp4 = tempfile.mkdtemp()
proc4 = tempfile.mkdtemp()
try:
    def _log4(name, lines):
        p = os.path.join(tmp4, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write("\n".join(lines) + "\n")
        return p

    midrun = _log4("daily-digest/latest.log",
                   ["2026-10-03T13:20:00Z PHASE2 compose"])
    st, d = jc.automation_status(midrun, NOW3, live_check=lambda p: True)
    check("fresh log + live run is RUNNING", st, "RUNNING")
    check("RUNNING detail names the in-flight run",
          d.startswith("in progress"), True)

    st, d = jc.automation_status(midrun, NOW3, live_check=lambda p: False)
    check("fresh log + no live run stays MISSING (just crashed)",
          (st, "no live run" in d), ("MISSING", True))

    crashed = _log4("cti-pass/latest.log",
                    ["2026-10-01T11:00:00Z PHASE2 compose"])
    os.utime(crashed, (NOW3.timestamp() - 3 * 86400,) * 2)
    st, d = jc.automation_status(crashed, NOW3, live_check=lambda p: True)
    check("log untouched for hours with no terminal line is MISSING "
          "(genuinely crashed, cross-check never consulted)",
          (st, "no terminal line (crashed mid-run?)" == d), ("MISSING", True))

    # live_run_for_log itself: fd-scan on a fake /proc root against the
    # CRONMAN_LOCK_DIR lock file (job name = the log's parent directory).
    lockdir = tempfile.mkdtemp()
    old_env = os.environ.get("CRONMAN_LOCK_DIR")
    os.environ["CRONMAN_LOCK_DIR"] = lockdir
    try:
        check("no holder -> not live",
              jc.live_run_for_log(
                  os.path.join(tmp4, "daily-digest", "latest.log"),
                  proc_root=proc4), False)
        lock = os.path.join(lockdir, "daily-digest.lock")
        open(lock, "w").close()
        piddir = os.path.join(proc4, "4242")
        os.makedirs(os.path.join(piddir, "fd"))
        os.symlink(lock, os.path.join(piddir, "fd", "7"))
        check("open fd on the job lock -> live run",
              jc.live_run_for_log(
                  os.path.join(tmp4, "daily-digest", "latest.log"),
                  proc_root=proc4), True)
        other = os.path.join(lockdir, "other-job.lock")
        open(other, "w").close()
        os.unlink(os.path.join(piddir, "fd", "7"))
        os.symlink(other, os.path.join(piddir, "fd", "7"))
        check("fd on a DIFFERENT job's lock is not this job's run",
              jc.live_run_for_log(
                  os.path.join(tmp4, "daily-digest", "latest.log"),
                  proc_root=proc4), False)
    finally:
        if old_env is None:
            os.environ.pop("CRONMAN_LOCK_DIR", None)
        else:
            os.environ["CRONMAN_LOCK_DIR"] = old_env
finally:
    import shutil as _sh
    _sh.rmtree(tmp4, ignore_errors=True)
    _sh.rmtree(proc4, ignore_errors=True)

print()
if failures:
    print(f"FAIL: {len(failures)} audit checks failed")
    sys.exit(1)
print("ALL PASS")
