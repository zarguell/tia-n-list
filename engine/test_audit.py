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

clean_events = {f"g{i}": {"source": "fine.example",
                          "published_at": "2026-08-01T00:00:00Z"}
                for i in range(30)}
clean_decs = {"2026-09-16T1100": [
    {"event_id": f"g{i}", "action": "keep" if i < 20 else "drop"}
    for i in range(30)]}
_mk_noise_dir(os.path.join(tmp, "clean"), clean_events, clean_decs)
p2, _ = jc.ingest_noise(os.path.join(tmp, "clean"), NOW2)
check("healthy store passes", p2, [])

print()
if failures:
    print(f"FAIL: {len(failures)} audit checks failed")
    sys.exit(1)
print("ALL PASS")
