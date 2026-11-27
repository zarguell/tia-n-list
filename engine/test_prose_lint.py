#!/usr/bin/env python3
"""Prose-gate contract suite — deterministic lint + quarantine (store-health LEAF-3).

The shipped evidence: analysis/25-year-old-curl-vulnerability-cve-2026-8932-
ai-discovered-flaw.md reads exactly "Analyst note based on event content.
Watch for updates." — the generic filler prompts/tia-hourly.md bans, and the
prompt's em-dash ban had no enforcement either. KEV records have a hard
verify gate; this suite pins the prose twin:

  1. the literal filler FAILS lint_analysis (the specificity check is the
     filler-killer: no CVE, no 2+ digit number, no version token);
  2. structure + banned strings: an em dash, a heading, an over-long
     paragraph count, a >6000-char body and AI-slop phrases (case-
     insensitive, curly apostrophes included) each fail;
  3. a GOOD grounded analysis (CVE ids, numbers, 3 paragraphs, no banned
     strings) passes clean, at every legal paragraph count;
  4. lint_digest: a digest without a stories/ link fails, banned strings
     fail, a real-shaped digest passes (no length/paragraph bounds);
  5. quarantine_analysis on a fixture store: a violating analysis lands in
     .rejects/, the story json's "analysis" key is cleared (re-queue path:
     merge.emit_needs queues on a missing analysis file), other fields are
     preserved, clean/missing analyses are untouched;
  6. ssg.run_prose_gate: quarantines live cards only (orphan files left
     alone), returns today's digest violations (fail-closed for the caller),
     skips silently when no digest exists;
  7. `the event (reference|references|referenced|referencing)` is a HARD
     violation (2026-10-26 audit Issue 8 + Rec 4) — all four word forms,
     case-insensitive, in lint_analysis and through the quarantine path —
     while the REST of the internal-bookkeeping family stays WARN-only.

Run: python3 engine/test_prose_lint.py   (exit 0 = pass)
"""
import glob
import json
import os
import sys
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prose_lint  # noqa: E402
import ssg  # noqa: E402

FAILS = []


def check(name, cond):
    print(("  ok  " if cond else "  FAIL") + f" {name}")
    if not cond:
        FAILS.append(name)


_FILLER = ("The reporting outlet confirms the detail and does not "
           "attribute it to unnamed sources, which keeps this in the "
           "confirmed-fact column rather than the rumor one for now.")


def para(text, words=40):
    """One grounded paragraph of realistic analyst prose (numbers + CVE id in
    the first), padded to ~words words. No banned strings, no em dashes."""
    return " ".join([text] + [_FILLER] * max(1, words // 20))


GOOD = "\n\n".join([
    para("Attackers exploited CVE-2026-1234 in the file converter service, "
         "reaching 4,100 hosts before the vendor shipped a fixed 2.3.1 "
         "build on September 12."),
    para("The vendor advisory pins exploitation to a deserialization bug "
         "reachable without authentication; telemetry from three national "
         "CERTs shows scans ramping since the PoC landed."),
    para("Watch for 2.3.1 adoption among internet-exposed instances and "
         "rotate the service credentials; the advisory lists no private-key "
         "exposure, so patching is the full remediation."),
])

# --- 1: the literal shipped filler fails (specificity) -----------------------
filler = ("Story 25-year-old-curl-vulnerability-cve-2026-8932-ai-discovered-"
          "flaw. Score 6.8. Analyst note based on event content. Watch for "
          "updates.")
v = prose_lint.lint_analysis(filler)
check("literal filler fails lint_analysis", bool(v))
# the SPEC-mandated literal: the bare filler sentence (the shipped file adds
# the story slug + score, whose CVE/6.8 tokens ground it — structure fails it)
check("bare filler sentence fails on missing grounding specifically",
      any("no grounding" in m for m in
          prose_lint.lint_analysis("Analyst note based on event content. "
                                   "Watch for updates.")))
check("boilerplate 'analyst note based on event content' is slop-listed",
      any("AI-slop phrase" in m for m in prose_lint.lint_analysis(
          GOOD.replace("The reporting outlet confirms",
                       "Analyst note based on event content, and the "
                       "reporting outlet confirms"))))
check("filler fails on length too (too short)",
      any("length" in m for m in v))
check("story id prefixes messages when given",
      all(m.startswith("sid:") for m in prose_lint.lint_analysis(filler,
                                                                 story="sid")))

# --- 1b: bare internal event ids are a HARD violation --------------------------
# 2026-10-25 audit Issue 1 + Rec 1: 11 published analyses printed the
# pipeline's own identifiers (`masto:`, `mf:`, `rd:`, …) — the front page hero
# analysis led its second sentence with one. The TRIAGE_BOOKKEEPING WARN never
# matched the id shape, so the class recurred; this one quarantines.
for _prefix, _id in (("masto", "masto:117498992322565382"),
                     ("mf", "mf:164959"),
                     ("rd", "rd:8f2c41a0"),
                     ("x", "x:1770000000000000000"),
                     ("desk", "desk:481"),
                     ("rss", "rss:aa3b91"),
                     ("bsky", "bsky:3kzv4wz2k7c2b")):
    check(f"bare {_prefix}: id is a hard violation",
          any("internal event id" in m for m in prose_lint.lint_analysis(
              GOOD.replace("Attackers exploited CVE-2026-1234",
                           f"Attackers exploited CVE-2026-1234 (event {_id})"))))
    check(f"{_prefix}: helper names the offending token",
          prose_lint.internal_id_hits(
              f"the new event {_id} reinforces it") == [_id])
check("clean prose has no internal-id violation",
      not any("internal event id" in m
              for m in prose_lint.lint_analysis(GOOD))
      and prose_lint.internal_id_hits(GOOD) == [])
check("ids quoted inside code spans stay legal (genuine payloads)",
      prose_lint.internal_id_hits("the relay wrote `masto:117498992322565382`")
      == []
      and prose_lint.internal_id_hits(
          "```\nmasto:117498992322565382\n```") == [])
check("two-letter prefixes only match as a whole token (no prose words)",
      prose_lint.internal_id_hits("box:123 and standard:7 and deskx:9") == []
      and prose_lint.internal_id_hits("see x:123 now") == ["x:123"])
check("an id-bearing analysis is quarantined by the prose gate",
      prose_lint.internal_id_hits("The new event (masto:117498992322565382) "
                                 "reinforces active exploitation")
      == ["masto:117498992322565382"])

# --- 2: banned strings + structure, one violation at a time ------------------
emdash = GOOD.replace("September 12", "September\u201412")
v = prose_lint.lint_analysis(emdash)
check("em dash (U+2014) anywhere fails",
      any("em dash" in m for m in v))
check("clean paragraphs do not false-positive the em-dash check",
      not any("em dash" in m for m in prose_lint.lint_analysis(GOOD)))

heading = "# Critical bug\n\n" + GOOD
v = prose_lint.lint_analysis(heading)
check("heading-led analysis fails",
      any("markdown heading" in m for m in v))

one = GOOD.split("\n\n")[0]
v = prose_lint.lint_analysis(one)
check("1-paragraph analysis has NO hard violations (grounded, clean)",
      v == [])
# 2026-10-18 audit (decision 7925e9ba91b6): the 1-paragraph WARN was pure
# log flood (325/day) with no editorial consequence — it is no longer
# emitted, but a REAL prose-lint error in a 1-paragraph body still fails.
check("1-paragraph analysis is no longer SOFT-flagged (log-flood fix)",
      prose_lint.soft_paras(one) == [])
check("1-paragraph analysis with a real lint error STILL fails hard",
      any("em dash" in m for m in prose_lint.lint_analysis(
          one.replace("September 12", "September\u201412")))
      and prose_lint.soft_paras(one) == [])

five = "\n\n".join(
    [para(f"Point {i}: the count reached 4,100 hosts on day {i}.", 35)
     for i in range(5)])
check("5-paragraph analysis is SOFT-flagged, not hard-failed",
      any("5 paragraph" in m for m in prose_lint.soft_paras(five))
      and prose_lint.lint_analysis(five) == [])

long_text = "\n\n".join(
    f"Iteration {i} of the reporting cycle brought 4,100 additional scanned "
    f"hosts into view. {_FILLER * 14}" for i in range(3))
check("fixture is actually >6000 chars", len(long_text) > 6000)
v = prose_lint.lint_analysis(long_text)
check(">6000 char analysis fails",
      any("length" in m for m in v))

slop = GOOD.replace("The reporting outlet confirms",
                    "It's worth noting that the reporting outlet confirms")
v = prose_lint.lint_analysis(slop)
check("slop phrase fails (case-insensitive)",
      any("AI-slop phrase" in m for m in v))
curly = GOOD.replace("The reporting outlet confirms",
                     "In today\u2019s landscape the reporting outlet confirms")
v = prose_lint.lint_analysis(curly)
check("curly-apostrophe slop fails",
      any("AI-slop phrase" in m for m in v))
check("grounding accepts each shape",
      prose_lint.lint_analysis(GOOD) == []
      and not any("no grounding" in m for m in
                  prose_lint.lint_analysis(para("Version 3.14 fixed it.", 30)))
      and not any("no grounding" in m for m in
                  prose_lint.lint_analysis(para("About 42 organizations hit.", 30))))
# NOTE (decision e732e816ab3e): "About 42 organizations hit." is NOT grounding
# once the stage-2 specificity rule is on — a bare 2-digit number was exactly
# the hole. Section 5d pins that; the stage-1 arm above still accepts it so the
# shipped default does not change behaviour.

# --- 3: the GOOD analysis passes clean ----------------------------------------
check("good grounded analysis passes clean",
      prose_lint.lint_analysis(GOOD) == [])
two = "\n\n".join(GOOD.split("\n\n")[:2])
four = GOOD + "\n\n" + para("A fourth paragraph keeps the same grounded "
                            "register: 4,100 hosts, CVE-2026-1234, version "
                            "2.3.1, nothing invented.")
check("2 and 4 paragraphs both legal",
      prose_lint.lint_analysis(two) == []
      and prose_lint.lint_analysis(four) == [])

# --- 3b: significance-aware depth floor (2026-10-31 audit Issue 4) -----------
# The 200-char floor let a 406-char single-paragraph analysis ship for the
# score-6.0 / 30-source Ivanti zero-day. Depth now scales with significance.
thin = para("Attackers exploited CVE-2026-104935 in Ivanti Connect Secure, "
            "reaching 30 sources before the vendor shipped a fixed build on "
            "October 13.", 20)
check("thin fixture is a 1-paragraph sub-900-char note",
      len(thin) < prose_lint.SIGNIFICANT_MIN_LEN
      and len(thin.split("\n\n")) == 1)
check("significant story below the depth floor is a hard violation",
      any("significant story" in m
          for m in prose_lint.depth_violations(thin, 6.0)))
check("low-score story keeps the short-note house style",
      prose_lint.depth_violations(thin, 1.0) == [])
check("grounded 3-paragraph significant analysis passes the depth floor",
      len(GOOD) >= prose_lint.SIGNIFICANT_MIN_LEN
      and prose_lint.depth_violations(GOOD, 6.0) == [])
check("depth floor is inclusive at the score threshold",
      prose_lint.depth_violations(thin, prose_lint.SIGNIFICANT_SCORE) != []
      and prose_lint.depth_violations(thin,
                                      prose_lint.SIGNIFICANT_SCORE - 0.1) == [])

# --- 4: lint_digest ------------------------------------------------------------
GOOD_DIGEST = (
    "The day's defining story is [the BIG-IP zero-day](stories/big-ip-cve/) "
    "under active exploitation; Shadowserver counts more than 14,700 exposed "
    "IPs worldwide. Also covered: [the SAP supply-chain takedown]"
    "(stories/sap-npm-attack/) with 1,006 repositories pulled, and a quieter "
    "[Patch Tuesday roundup](stories/patch-tuesday/) closing the day.")
check("real-shaped digest passes clean",
      prose_lint.lint_digest(GOOD_DIGEST) == [])
v = prose_lint.lint_digest(GOOD_DIGEST.replace("](", "](https://example.test/"))
check("digest without a stories/ link fails",
      any("no stories/ link" in m for m in v))
v = prose_lint.lint_digest(GOOD_DIGEST.replace("The day's defining",
                                               "In today's news, the defining"))
check("banned phrase fails in digests", any("AI-slop" in m for m in v))
v = prose_lint.lint_digest(GOOD_DIGEST.replace("worldwide", "worldwide\u2014today"))
check("em dash fails in digests", any("em dash" in m for m in v))
long_digest = GOOD_DIGEST + " " + para("Historical background section: the "
                                       "platform has existed since 2021 and "
                                       "grew through 4,100 shadow domains.", 400)
check("digest has no length bounds",
      len(long_digest) > 3000 and prose_lint.lint_digest(long_digest) == [])

# --- 5: quarantine_analysis on a fixture store --------------------------------
with tempfile.TemporaryDirectory() as td:
    stories_dir = os.path.join(td, "stories")
    analysis_dir = os.path.join(td, "analysis")
    os.makedirs(stories_dir)
    os.makedirs(analysis_dir)
    log = []
    story = {"id": "bad-story", "title": "t", "score": 5.0,
             "analysis": {"updated_at": "2026-09-20T00:00:00Z",
                          "score": 5.0}}
    json.dump(story, open(os.path.join(stories_dir, "bad-story.json"), "w"),
              indent=1)
    open(os.path.join(analysis_dir, "bad-story.md"), "w").write(filler)
    v = prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                       {"id": "bad-story"}, log=log.append)
    rejects = os.path.join(analysis_dir, ".rejects")
    names = os.listdir(rejects)
    check("violating analysis moved into .rejects/",
          len(v) > 0 and len(names) == 1
          and names[0].startswith("bad-story-") and names[0].endswith(".md"))
    check("original analysis path gone",
          not os.path.exists(os.path.join(analysis_dir, "bad-story.md")))
    st = json.load(open(os.path.join(stories_dir, "bad-story.json")))
    check("story analysis key cleared, other fields preserved",
          "analysis" not in st and st["title"] == "t" and st["score"] == 5.0)
    check("WARN logged per quarantined file",
          len(log) == 1 and ".rejects/" in log[0] and "bad-story" in log[0])

    # clean analysis: untouched, no reject churn, no log
    log.clear()
    open(os.path.join(analysis_dir, "clean-story.md"), "w").write(GOOD)
    json.dump({"id": "clean-story", "analysis": {"updated_at": "z"}},
              open(os.path.join(stories_dir, "clean-story.json"), "w"))
    v = prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                       {"id": "clean-story"}, log=log.append)
    check("clean analysis untouched",
          v == [] and log == []
          and os.path.exists(os.path.join(analysis_dir, "clean-story.md"))
          and len(os.listdir(rejects)) == 1)

    # missing analysis file: no-op
    v = prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                       {"id": "never-analyzed"}, log=log.append)
    check("missing analysis file is a silent no-op",
          v == [] and log == []
          and len(os.listdir(rejects)) == 1)

    # timestamped rejects never collide across re-violations (agent rewrites
    # the analysis, violates again next hour -> a NEW reject file, no clobber)
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    open(os.path.join(analysis_dir, "twice-story.md"), "w").write(filler)
    prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                   {"id": "twice-story"}, now=now)
    open(os.path.join(analysis_dir, "twice-story.md"), "w").write(filler)
    prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                   {"id": "twice-story"},
                                   now=now + timedelta(seconds=1))
    twice = [n for n in os.listdir(rejects) if n.startswith("twice-story")]
    check("repeat violations land under fresh timestamps", len(twice) == 2)

    # significance-aware depth floor: the same thin body is a hard violation
    # for a score-6.0 story and a legitimate short note for a cold one.
    open(os.path.join(analysis_dir, "thin-significant.md"), "w").write(thin)
    json.dump({"id": "thin-significant", "score": 6.0},
              open(os.path.join(stories_dir, "thin-significant.json"), "w"))
    v = prose_lint.quarantine_analysis(
        stories_dir, analysis_dir,
        {"id": "thin-significant", "score": 6.0}, log=log.append)
    check("thin analysis of a significant story is quarantined",
          any("significant story" in m for m in v)
          and not os.path.exists(os.path.join(analysis_dir,
                                              "thin-significant.md")))
    open(os.path.join(analysis_dir, "thin-low.md"), "w").write(thin)
    json.dump({"id": "thin-low", "score": 1.0},
              open(os.path.join(stories_dir, "thin-low.json"), "w"))
    v = prose_lint.quarantine_analysis(
        stories_dir, analysis_dir, {"id": "thin-low", "score": 1.0},
        log=log.append)
    check("thin analysis of a low-score story is untouched",
          v == [] and os.path.exists(os.path.join(analysis_dir,
                                                  "thin-low.md")))

# --- 5b: subject grounding for non-CVE stories + retry cap -------------------
# (2026-09-25: the kubernetes/GCP research disclosure has no CVE id — the
# numeric grounding rule was structurally unpassable, and the requeue loop
# re-analyzed it hourly for 10+ hours.)

NOCVE = ("Varonis research shows a Kubernetes YAML file with limited "
         "namespace access can escalate to full GCP organization ownership "
         "through service account keys and GitOps controllers like the "
         "Google Kubernetes Config Connector. The controller authenticates "
         "to the cloud provider on behalf of developers, so the escalation "
         "needs no stolen key material at all. Watch for Google's response: "
         "either documented key rotation guidance or a config change that "
         "separates namespace identity from organization ownership.")
K8S_TITLE = "A Single Kubernetes YAML can hand an attacker full GCP org ownership"

check("non-CVE analysis grounded by naming the story subject",
      prose_lint.lint_analysis(NOCVE, subject_title=K8S_TITLE) == [])
check("same text without a title still fails grounding",
      any("no grounding" in m for m in prose_lint.lint_analysis(NOCVE)))
check("wrong-subject title does not ground",
      any("no grounding" in m for m in prose_lint.lint_analysis(
          NOCVE, subject_title="Cisco SD-WAN Controller peering authentication")))
check("filler still fails even with the subject title",
      any("no grounding" in m for m in prose_lint.lint_analysis(
          "Analyst note based on event content. Watch for updates.",
          subject_title=K8S_TITLE)))

# --- 5c: single-token subjects + title-less gates (2026-10-04 audit #3) ----
# "France tax office breached via stolen staff passwords" yields exactly
# one subject token (["France"]): under the old >=2 bar it could never
# ground, so the story was structurally unpassable. The UK-act rejects
# passed lint WITH the title but were quarantined WITHOUT one, because
# ssg.run_prose_gate dropped the card title at the call site.
FR_TITLE = "France tax office breached via stolen staff passwords"
FR_TEXT = ("France's tax office was breached via stolen staff passwords, "
           "and the security team missed red flags initially. The incident "
           "is a reminder that credential compromise at government agencies "
           "carries high impact, especially when detection lags. Watch for "
           "follow-up reports on data scope and exfiltration.")
check("single-token subject grounds with one hit",
      prose_lint.lint_analysis(FR_TEXT, subject_title=FR_TITLE) == [])
check("single-token subject still fails when unnamed",
      any("no grounding" in m for m in prose_lint.lint_analysis(
          "A government agency was breached via stolen staff passwords, "
          "and the security team missed red flags initially. Credential "
          "compromise carries high impact when detection lags behind. "
          "Watch for follow-up reports on data scope and exfiltration.",
          subject_title=FR_TITLE)))
check("tokenless title never grounds (no vacuous pass)",
      not prose_lint._names_subject(FR_TEXT, "breached via stolen staff")
      and not prose_lint._names_subject(FR_TEXT, ""))

with tempfile.TemporaryDirectory() as td:
    stories_dir = os.path.join(td, "stories")
    analysis_dir = os.path.join(td, "analysis")
    os.makedirs(stories_dir)
    os.makedirs(analysis_dir)
    log = []
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    for i in range(prose_lint.MAX_ANALYSIS_QUARANTINES):
        open(os.path.join(analysis_dir, "cap-story.md"), "w").write(filler)
        prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                       {"id": "cap-story"},
                                       now=now + timedelta(seconds=i),
                                       log=log.append)
    rejects = os.path.join(analysis_dir, ".rejects")
    check("cap marker written after MAX quarantines",
          os.path.exists(os.path.join(rejects, "cap-story.capped")))
    check("CAPPED logged on the final attempt",
          any("CAPPED" in m for m in log))
    # the cap counts prior rejects: a 4th quarantine still moves the file
    # (evidence preserved) but the marker is what stops the requeue loop
    open(os.path.join(analysis_dir, "cap-story.md"), "w").write(filler)
    prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                   {"id": "cap-story"},
                                   now=now + timedelta(seconds=9),
                                   log=log.append)
    check("post-cap violations still quarantined for evidence",
          len([n for n in os.listdir(rejects) if n.startswith("cap-story-")])
          == prose_lint.MAX_ANALYSIS_QUARANTINES + 1)

# --- 5d: specificity stage 2 (decision e732e816ab3e, 2026-10-21 audit
# Issue 4 + Rec 7). The stage-1 gate above is grounded by ANY 2+ digit number
# (NUM2_RE), so a stub whose only digits were YEARS cleared it and shipped as
# a newest analysis at score 4.5. Stage 2 requires real specificity and ships
# DISARMED (warn) so the backlog is measured before anything is quarantined.
#
# The negative fixture is the stored stub verbatim (508 bytes; the live file
# was re-analysed on 2026-10-21T18:20Z and now carries version tokens, so the
# historical text is pinned here). The positive fixture is read from the real
# store: chrome-156 (build number, 353 fixes, CVEs).
BRONZE_STUB = (
    "BRONZE SANDCASTLE, a suspected China-linked APT, has been using "
    "legitimate Windows applications and malicious DLLs to run encrypted "
    "payloads inside trusted processes, then stealing Active Directory "
    "databases. Investigations from August 2025 through August 2026 "
    "identified victims in the Philippines, Taiwan, and Afghanistan. The "
    "approach minimizes file-system artifacts, making detection by "
    "conventional scanning difficult. Watch for further victim reports and "
    "attribution updates from threat-intel vendors.")
YEAR_ONLY = ("In August 2025 a suspected intrusion cluster targeted utilities "
             "across Europe and Asia, and the campaign ran on through 2026 "
             "with 40 victims. The group moves quietly and the public "
             "reporting stays thin. Watch for further victim reports and "
             "attribution updates from threat-intel vendors.")
ANALYSIS_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "data", "analysis")
CHROME156 = os.path.join(
    ANALYSIS_DATA, "chrome-156-security-update-fixes-critical-vulnerabilities.md")

check("stage-2 specificity ships DISARMED by default (warn, no quarantine)",
      prose_lint.SPECIFICITY_STAGE == "warn")
check("bronze-sandcastle stub fails stage-2 specificity",
      len(prose_lint.specificity_hits(BRONZE_STUB)) == 1)
check("the stub's only digits are years (so the stage-1 gate passed it)",
      prose_lint.NUM2_RE.search(BRONZE_STUB)
      and not prose_lint.CVE_RE.search(BRONZE_STUB)
      and not prose_lint.ATTACK_RE.search(BRONZE_STUB)
      and not prose_lint.VERSION_RE.search(BRONZE_STUB)
      and not prose_lint._has_ioc(BRONZE_STUB))
check("disarmed stage keeps the stub unquarantined (legacy arm unchanged)",
      prose_lint.lint_analysis(BRONZE_STUB) == [])
check("bare years no longer clear the stage-2 rule",
      any("no specificity" in m
          for m in prose_lint.specificity_hits(YEAR_ONLY)))
check("any 2-digit number no longer clears the stage-2 rule",
      any("no specificity" in m for m in prose_lint.specificity_hits(
          "About 42 organizations were hit in the campaign.")))
check("a CVE id grounds",
      prose_lint.specificity_hits("CVE-2026-113341 was patched.") == [])
check("an ATT&CK technique id grounds",
      prose_lint.specificity_hits("The actor used T1566.001 to land it.") == []
      and prose_lint.specificity_hits("Spearphishing (T1566) seeded it.") == [])
check("a version token grounds",
      prose_lint.specificity_hits("Chrome 156.0.8078.47 fixed it.") == [])
check("an IOC grounds (live, defanged domain, IPv4, hash)",
      prose_lint.specificity_hits("Beaconing to cdn-metrics.top.") == []
      and prose_lint.specificity_hits("Block americanprgoress[.]top.") == []
      and prose_lint.specificity_hits("C2 at 185.220.101.4 answered.") == []
      and prose_lint.specificity_hits(
          "Hash 8858ea412dc306b3558885af18006c5ca24689e8875733b5e13b3c2692e603cb.")
      == [])
check("file names are not IOCs (cmd.exe, claude.json)",
      prose_lint.specificity_hits("It spawned cmd.exe and read claude.json.")
      != [])
check("a tool named in the EVENT text grounds",
      prose_lint.specificity_hits(
          "The loader, CLEANGULP, ran from a scheduled task.",
          source_text="UTA0565 installed CLEANGULP on the cloned sites.") == [])
check("the same tool name does not ground without event backing",
      prose_lint.specificity_hits(
          "The loader, CLEANGULP, ran from a scheduled task.") != [])
check("naming the subject still grounds a non-CVE research piece",
      prose_lint.specificity_hits(NOCVE, subject_title=K8S_TITLE) == [])
check("chrome-156 analysis (build, 353 fixes, CVEs) grounds under stage 2",
      os.path.exists(CHROME156)
      and prose_lint.specificity_hits(open(CHROME156).read()) == []
      and prose_lint.lint_analysis(open(CHROME156).read()) == [])

# stage 1 reports over the whole store without touching a file
with tempfile.TemporaryDirectory() as td:
    stories_dir = os.path.join(td, "stories")
    analysis_dir = os.path.join(td, "analysis")
    digests_dir = os.path.join(td, "digests")
    for d in (stories_dir, analysis_dir, digests_dir):
        os.makedirs(d)
    # no title at all: the year-only text names no subject, so the
    # subject-naming alternative (deliberately kept) cannot rescue it.
    json.dump({"id": "stub-story", "title": ""},
              open(os.path.join(stories_dir, "stub-story.json"), "w"), indent=1)
    open(os.path.join(analysis_dir, "stub-story.md"), "w").write(YEAR_ONLY)
    log = []
    prose_lint.quarantine_analysis(
        stories_dir, analysis_dir,
        {"id": "stub-story", "title": ""}, log=log.append)
    check("stage-1 WARN names the analysis that would newly fail",
          any("specificity (kept, stage=warn)" in m for m in log))
    check("stage-1 WARN never quarantines (file still shipped)",
          os.path.exists(os.path.join(analysis_dir, "stub-story.md"))
          and not os.path.exists(os.path.join(analysis_dir, ".rejects")))
    check("store-wide backlog count reports the file",
          prose_lint.specificity_backlog(
              analysis_dir, {"stub-story": {"title": ""}})
          == ["stub-story"])
    # ssg.run_prose_gate logs the count (the flip-to-hard signal)
    ssg.STORIES_DIR, ssg.ANALYSIS_DIR, ssg.DIGESTS_DIR = (stories_dir,
                                                          analysis_dir,
                                                          digests_dir)
    gate_log = []
    ssg.run_prose_gate({"stub-story": {
        "id": "stub-story", "title": "",
        "score": 1.0, "events": [{"title": "Utilities hit",
                                   "snippet": "A cluster hit utilities."}]}},
        today="2026-10-21", log=gate_log.append)
    check("prose gate reports the shipped stage-2 backlog count",
          any("1 of 1 shipped analysis" in m for m in gate_log))
    check("prose gate still does not quarantine at stage=warn",
          os.path.exists(os.path.join(analysis_dir, "stub-story.md")))

# flipping the stage makes the same text a HARD (quarantining) violation
try:
    prose_lint.SPECIFICITY_STAGE = "hard"
    check("flipped to hard, the year-only text is a hard violation",
          any("no specificity" in m
              for m in prose_lint.lint_analysis(YEAR_ONLY)))
    check("flipped to hard, the bronze stub is a hard violation",
          any("no specificity" in m
              for m in prose_lint.lint_analysis(BRONZE_STUB)))
    check("flipped to hard, the chrome-156 analysis still passes",
          prose_lint.lint_analysis(open(CHROME156).read()) == [])
finally:
    prose_lint.SPECIFICITY_STAGE = "warn"

# --- 6: ssg.run_prose_gate ------------------------------------------------------
with tempfile.TemporaryDirectory() as td:
    stories_dir = os.path.join(td, "stories")
    analysis_dir = os.path.join(td, "analysis")
    digests_dir = os.path.join(td, "digests")
    for d in (stories_dir, analysis_dir, digests_dir):
        os.makedirs(d)
    ssg.STORIES_DIR = stories_dir
    ssg.ANALYSIS_DIR = analysis_dir
    ssg.DIGESTS_DIR = digests_dir
    log = []
    # live card with a bad analysis + an orphan analysis with NO card
    json.dump({"id": "live-story", "title": "t"},
              open(os.path.join(stories_dir, "live-story.json"), "w"))
    json.dump({"id": "orphan-story", "title": "t",
               "analysis": {"updated_at": "z"}},
              open(os.path.join(stories_dir, "orphan-story.json"), "w"))
    open(os.path.join(analysis_dir, "live-story.md"), "w").write(filler)
    open(os.path.join(analysis_dir, "orphan-story.md"), "w").write(filler)
    # titled card whose CVE-less analysis names its subject (2026-10-04
    # audit #3: the gate dropped the title, quarantining analyses that
    # pass lint with it — the UK-act loop). Must survive the gate.
    json.dump({"id": "titled-story", "title": K8S_TITLE},
              open(os.path.join(stories_dir, "titled-story.json"), "w"))
    open(os.path.join(analysis_dir, "titled-story.md"), "w").write(NOCVE)
    open(os.path.join(digests_dir, "2026-09-24.md"), "w").write(GOOD_DIGEST)
    errs = ssg.run_prose_gate({"live-story": {"id": "live-story"},
                               "titled-story": {"id": "titled-story",
                                                  "title": K8S_TITLE}},
                              today="2026-09-24", log=log.append)
    check("live card's bad analysis quarantined",
          not os.path.exists(os.path.join(analysis_dir, "live-story.md"))
          and os.path.exists(os.path.join(analysis_dir, ".rejects",
                                          os.listdir(os.path.join(
                                              analysis_dir, ".rejects"))[0])))
    check("orphan analysis (no card) left alone",
          os.path.exists(os.path.join(analysis_dir, "orphan-story.md")))
    check("live story json marker cleared, orphan marker kept",
          "analysis" not in json.load(
              open(os.path.join(stories_dir, "live-story.json")))
          and "analysis" in json.load(
              open(os.path.join(stories_dir, "orphan-story.json"))))
    check("good digest returns no errors", errs == [])
    check("titled card's subject-named analysis survives the gate",
          os.path.exists(os.path.join(analysis_dir, "titled-story.md"))
          and not [n for n in os.listdir(os.path.join(
              analysis_dir, ".rejects")) if n.startswith("titled-story")])
    log.clear()

    # bad digest today: fail-closed payload for the caller
    open(os.path.join(digests_dir, "2026-09-25.md"), "w").write(
        "A narrative day without a single story link and no coverage.")
    errs = ssg.run_prose_gate({}, today="2026-09-25", log=log.append)
    check("bad digest returns PROSE FAIL payload",
          len(errs) == 1 and errs[0].startswith("digest 2026-09-25.md:")
          and "no stories/ link" in errs[0])

    # no digest today: skip silently
    errs = ssg.run_prose_gate({}, today="2026-09-26", log=log.append)
    check("absent digest skips silently", errs == [] and log == [])


    # raw HTML in prose (2026-10-07: literal <img src=x> in a backfill event
    # red-ed every deploy for 12h — the rendered page trips the fail-closed
    # link lint). Payloads in code spans are safe; bare placeholders stay
    # allowed; href/src tags and active elements fail.
    check("bare img payload fails raw_html_hits",
          prose_lint.raw_html_hits("payloads such as 1<img src=x onerror=...> pass") != [])
    check("code-span payload passes raw_html_hits",
          prose_lint.raw_html_hits("payloads such as `1<img src=x onerror=...>` pass") == [])
    check("placeholder tags pass raw_html_hits",
          prose_lint.raw_html_hits("keys <ip> and <session_id> here") == [])
    check("script tag fails raw_html_hits",
          prose_lint.raw_html_hits("then <script>alert(1)</script> ran") != [])
    check("html payload fails lint_analysis (quarantine path)",
          any("raw HTML" in m for m in prose_lint.lint_analysis(
              "CVE-2026-0000 is bad, versions 1.2.3 affected. Payload 1<img src=x> runs.")))
    log.clear()

# --- 7: internal triage bookkeeping = DISTINCT WARN, never a hard fail -----
# (2026-10-17 audit Issue 2 / Rec 4b. The two shipped analyses below leaked
# pipeline bookkeeping into published prose and "pass the soft lint, which
# only WARNs" — this rule makes the leak visible per occurrence without
# quarantining the 27 stored analyses that use the same phrasing.)
#
# UPDATE (2026-10-26 audit Issue 8 + Rec 4 / section 7b below): the
# `the event references|reference|…` arm was PROMOTED to a hard violation.
# The fixtures stay verbatim as the text that shipped, so the same two
# analyses now split one sentence off to the hard gate (the reference arm)
# and keep the REST of the family WARN-only.
BLOCKSTRAP_ANALYSIS = (
    "CVE-2026-103849, named BlockStrap, is a maximum-severity remote code "
    "execution vulnerability in Adobe Commerce and Magento through version "
    "2.4.9. The flaw allows template-engine directive injection. The event "
    "references BleepingComputer coverage and attaches to the existing "
    "critical Magento story.\n\n"
    "This is a serious server-side vulnerability for a widely deployed "
    "e-commerce platform. Adobe shipped the APSB26-153 fix on October 13, so "
    "apply the patched release and watch for reports of in-the-wild "
    "exploitation. Do not treat this as routine maintenance: the maximum "
    "severity and broad version range demand rapid response.")
FASTAPIADMIN_ANALYSIS = (
    "CVE-2026-111641 is an authentication bypass in FastapiAdmin through "
    "version 30, allowing unauthenticated access according to the event "
    "reference to radar.offseq.com. The event is the original mint for this "
    "new story. The vulnerability affects an administration interface for a "
    "Python web framework, which increases the risk for deployed "
    "instances.\n\n"
    "The claim is tied to a named vulnerability and a primary source URL. "
    "Watch for detailed advisory publication, proof-of-concept releases, and "
    "whether the project issues an immediate patch. The new story is "
    "appropriate because no existing cluster covers this CVE.")

check("BlockStrap analysis hard-fails ONLY the promoted reference arm",
      prose_lint.lint_analysis(BLOCKSTRAP_ANALYSIS) == [
          "internal triage bookkeeping 'The event references' (published "
          "prose names the story and its reporting, never the "
          "ingest/triage state; rewrite the sentence to name the report "
          "itself)"])
check("FastapiAdmin analysis hard-fails ONLY the promoted reference arm",
      prose_lint.lint_analysis(FASTAPIADMIN_ANALYSIS) == [
          "internal triage bookkeeping 'the event reference' (published "
          "prose names the story and its reporting, never the "
          "ingest/triage state; rewrite the sentence to name the report "
          "itself)"])
bs_hits = prose_lint.triage_bookkeeping_hits(BLOCKSTRAP_ANALYSIS)
fa_hits = prose_lint.triage_bookkeeping_hits(FASTAPIADMIN_ANALYSIS)
check("BlockStrap bookkeeping flagged per occurrence (1 left after the "
      "reference arm moved to HARD)", len(bs_hits) == 1)
check("BlockStrap still flags 'attaches to the existing' as WARN",
      any("'attaches to the existing'" in m for m in bs_hits))
check("FastapiAdmin bookkeeping flagged per occurrence (3 left)",
      len(fa_hits) == 3)
check("FastapiAdmin flags mint/cluster + 'new story' bookkeeping",
      any("is the original mint" in m for m in fa_hits)
      and any("no existing cluster covers" in m for m in fa_hits)
      and any("The new story is appropriate" in m for m in fa_hits))
check("the promoted arm lives in exactly ONE place (never WARN + HARD)",
      not any("event reference" in m.lower()
              for m in bs_hits + fa_hits))
check("clean grounded analysis has no bookkeeping hits",
      prose_lint.triage_bookkeeping_hits(GOOD) == [])
check("bookkeeping rule is case-insensitive",
      prose_lint.triage_bookkeeping_hits(
          GOOD + " THE NEW STORY IS APPROPRIATE for the wire report.") != [])
# The exact ship-blocking case for the REMAINING family: a bookkeeping leak
# must NOT quarantine (that is the whole point of WARN vs a hard rule).
# BLOCKSTRAP_ANALYSIS minus its promoted reference sentence is the fixture.
WARN_ONLY_ANALYSIS = BLOCKSTRAP_ANALYSIS.replace(
    "The event references BleepingComputer coverage and attaches to the "
    "existing",
    "BleepingComputer covered the flaw and the report attaches to the "
    "existing")
check("WARN-only fixture really carries no promoted construction",
      prose_lint.event_reference_hits(WARN_ONLY_ANALYSIS) == []
      and len(prose_lint.triage_bookkeeping_hits(WARN_ONLY_ANALYSIS)) == 1)
with tempfile.TemporaryDirectory() as td:
    stories_dir = os.path.join(td, "stories")
    analysis_dir = os.path.join(td, "analysis")
    os.makedirs(stories_dir)
    os.makedirs(analysis_dir)
    log = []
    json.dump({"id": "leak-story", "title": "BlockStrap Magento RCE",
               "analysis": {"updated_at": "z"}},
              open(os.path.join(stories_dir, "leak-story.json"), "w"))
    open(os.path.join(analysis_dir, "leak-story.md"), "w").write(
        WARN_ONLY_ANALYSIS)
    v = prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                       {"id": "leak-story"}, log=log.append)
    check("bookkeeping leak does NOT quarantine (no hard violations)",
          v == [] and os.path.exists(
              os.path.join(analysis_dir, "leak-story.md"))
          and not os.path.exists(os.path.join(analysis_dir, ".rejects")))
    check("bookkeeping leak logged as a distinct WARN (not 'soft')",
          len(log) == 1 and "triage-bookkeeping (kept)" in log[0]
          and "leak-story" in log[0])
    check("bookkeeping WARN is per occurrence",
          log[0].count("internal triage bookkeeping") == 1)
    check("story json analysis marker untouched by the WARN",
          "analysis" in json.load(
              open(os.path.join(stories_dir, "leak-story.json"))))
    log.clear()

# --- 7b: `the event references …` is a HARD violation -------------------------
# 2026-10-26 audit Issue 8 + Rec 4: the applied card e8f2664e00bd (PR #150)
# shipped the whole bookkeeping family WARN-only; `prose_lint` logged it and
# shipped the file by design, so the class became routine — 17 analyses in ONE
# lint run. The narrow construction is promoted to hard (quarantine + requeue),
# the wide family above stays WARN. Pinned here: all four word forms, the
# case-insensitivity, the narrow scope (no near-miss false positives), and the
# quarantine/requeue half.
for _form in ("reference", "references", "referenced", "referencing"):
    check(f"'the event {_form}' is flagged by event_reference_hits",
          len(prose_lint.event_reference_hits(
              f"The report arrived and the event {_form} a vendor advisory."))
          == 1)
for _shape in ("The event references a wire report.",
               "THE EVENT REFERENCE to radar.offseq.com",
               "The Event Referenced the advisory."):
    check(f"case-insensitive match: {_shape[:34]!r}",
          any("internal triage bookkeeping" in m for m in
              prose_lint.event_reference_hits(_shape)))
check("the promoted construction is a HARD violation in lint_analysis",
      any("internal triage bookkeeping" in m
          and "the event references" in m.lower()
          for m in prose_lint.lint_analysis(
              GOOD.replace("The reporting outlet confirms",
                           "The event references a vendor advisory. The "
                           "reporting outlet confirms"))))
check("the message names the phrase and says what to do",
      "'the event references'" in prose_lint.event_reference_hits(
          "the event references a blog post")[0]
      and "rewrite the sentence" in prose_lint.event_reference_hits(
          "the event references a blog post")[0])
check("near-misses do NOT match (narrow scope)",
      prose_lint.event_reference_hits(
          "An event reference table lists 4,100 rows. The events referenced "
          "in the log match CVE-2026-1234. The event data was scrubbed "
          "within 3 hours. A reference to the event appears below.") == [])
check("the rest of the family is NOT event_reference_hits",
      prose_lint.event_reference_hits(
          "it attaches to the existing story, is the original mint, no "
          "existing cluster covers it, the new story is appropriate") == [])
check("clean prose has no event-reference violation",
      prose_lint.event_reference_hits(GOOD) == []
      and prose_lint.lint_analysis(GOOD) == [])
# Self-healing half: a live analysis carrying the construction is quarantined
# to .rejects/ and the story json's analysis marker is cleared, which re-queues
# it through merge.emit_needs (queues on a missing analysis file).
with tempfile.TemporaryDirectory() as td:
    stories_dir = os.path.join(td, "stories")
    analysis_dir = os.path.join(td, "analysis")
    os.makedirs(stories_dir)
    os.makedirs(analysis_dir)
    log = []
    json.dump({"id": "ref-story", "title": "BlockStrap Magento RCE",
               "analysis": {"updated_at": "z"}},
              open(os.path.join(stories_dir, "ref-story.json"), "w"))
    open(os.path.join(analysis_dir, "ref-story.md"), "w").write(
        BLOCKSTRAP_ANALYSIS)
    v = prose_lint.quarantine_analysis(stories_dir, analysis_dir,
                                       {"id": "ref-story"}, log=log.append)
    check("event-reference leak quarantines the analysis",
          bool(v) and not os.path.exists(
              os.path.join(analysis_dir, "ref-story.md"))
          and len(glob.glob(os.path.join(analysis_dir, ".rejects",
                                         "ref-story-*.md"))) == 1)
    check("quarantine names the promoted construction",
          any("internal triage bookkeeping" in m for m in v)
          and any("quarantined to .rejects" in m for m in log))
    check("quarantined story is re-queued (analysis marker cleared)",
          "analysis" not in json.load(
              open(os.path.join(stories_dir, "ref-story.json"))))
    log.clear()

# --- 10: malformed compound / dropped word (2026-10-26 audit Issue 4) --------
# The published 2026-10-26 digest read "... makes this a patch immediately item
# for any estate running AOS-8": a malformed compound that no gate saw, because
# banned strings and grounding say nothing about word order. Contract: the
# adverb-in-the-attributive-slot shape is a HARD violation for digests (which
# fail the build closed) and for analyses (quarantine + requeue is
# self-healing), and the legal near-misses never fire.
SHIPPED = ("No exploitation telemetry is reported yet, but the unauthenticated "
           "path to admin makes this a patch immediately item for any estate "
           "running AOS-8.")
hits = prose_lint.malformed_compound_hits(SHIPPED)
check("the shipped 2026-10-26 sentence is flagged", len(hits) == 1)
check("the message names the phrase and the adverb",
      "'a patch immediately item'" in hits[0] and "'immediately'" in hits[0]
      if hits else False)
check("the corrected sentence passes",
      prose_lint.malformed_compound_hits(
          SHIPPED.replace("a patch immediately item", "an immediate patch"))
      == [])
check("hyphenated legal variant passes",
      prose_lint.malformed_compound_hits(
          "makes this a patch-immediately item") == [])
check("malformed compound fails lint_digest",
      any("malformed compound" in m
          for m in prose_lint.lint_digest(
              GOOD_DIGEST + " " + SHIPPED)))
check("clean digest has no malformed-compound violation",
      prose_lint.lint_digest(GOOD_DIGEST) == [])
check("malformed compound fails lint_analysis (hard, quarantine path)",
      any("malformed compound" in m
          for m in prose_lint.lint_analysis(GOOD + "\n\n" + SHIPPED)))
# Negatives: the legal shapes that a loose rule would wrongly flag. Sources:
# the false positives an earlier draft produced over the 2,627-file store, plus
# -ly adjectives in the attributive slot.
for legal in ("a monthly patch for every estate",
              "a missed July update shipped late",
              "a weekly issue roundup",
              "a fully remote attacker",
              "a newly discovered flaw",
              "a friendly item in the queue",
              "a costly mistake",
              "a quickly fixed bug in 2.3.1"):
    check(f"legal phrase not flagged: {legal!r}",
          prose_lint.malformed_compound_hits(legal) == [])
check("code-span example stays legal",
      prose_lint.malformed_compound_hits(
          "the phrase `a patch immediately item` is banned") == [])
check("capitalized July cannot fake an adverb",
      prose_lint.malformed_compound_hits("a routine July item") == [])

# --- 10b: the head must be noun-only (2026-11-26 review) --------------------
# An earlier draft listed the verb-shaped plurals fixes/issues/steps/actions/
# matters/concerns/tasks as heads, so ordinary grammatical prose — article +
# subject + adverb + VERB — tripped a HARD rule. That is not academic: the
# digest arm fails the build closed (site-deploy refuses to publish) and the
# analysis arm quarantines + requeues up to MAX_ANALYSIS_QUARANTINES times,
# so a false positive costs a publish or an analysis. Each sentence below was
# flagged by the pre-review module and must stay legal.
for grammatical in ("a reboot immediately fixes the bug",
                    "a restart usually fixes the appliance",
                    "a patch typically fixes the issue",
                    "a hotfix immediately fixes the crash",
                    "an update usually issues a new token",
                    "a decision usually matters under review",
                    "a leak usually concerns the vendor",
                    "an analyst usually tasks the vendor",
                    "a bad revert quickly steps on the next release"):
    check(f"grammatical subject+adverb+verb not flagged: {grammatical!r}",
          prose_lint.malformed_compound_hits(grammatical) == [])
# ...while every retained head still fires, singular and plural, so the prune
# narrowed the head set without hollowing the rule out.
for defective in ("makes this a patch immediately item",
                  "makes this a patch immediately items",
                  "makes this a patch immediately issue",
                  "makes this a patch immediately priority",
                  "makes this a patch immediately problems",
                  "makes this a patch immediately step",
                  "makes this a patch immediately fix"):
    check(f"defective compound still flagged: {defective!r}",
          len(prose_lint.malformed_compound_hits(defective)) == 1)
# The log hint must not fabricate an article + plural (the pre-review message
# rendered the nonsense "e.g. 'an immediate fixes'").
hint = prose_lint.malformed_compound_hits(SHIPPED)[0]
check("hint quotes the canonical repair, not a fabricated phrase",
      "'an immediate patch'" in hint and "an immediate item" not in hint)
# Documented gap, pinned so a future widening has to say so out loud: the
# article must be lowercase, so a sentence-initial 'A' escapes the rule.
check("sentence-initial 'A' escapes (documented gap)",
      prose_lint.malformed_compound_hits(
          "A patch immediately item ships today.") == [])


print()
if FAILS:
    print(f"FAILED: {len(FAILS)} check(s): {', '.join(FAILS)}")
    sys.exit(1)
print("all store-health LEAF-3 prose-gate contract checks passed")
