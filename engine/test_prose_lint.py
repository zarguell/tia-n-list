#!/usr/bin/env python3
"""Prose-gate contract suite — deterministic lint + quarantine (store-health LEAF-3).

The shipped evidence: analysis/25-year-old-curl-vulnerability-cve-2026-8932-
ai-discovered-flaw.md reads exactly "Analyst note based on event content.
Watch for updates." — the generic filler prompts/tia-hourly.md bans, and the
prompt's em-dash ban had no enforcement either. KEV records have a hard
verify gate; this suite pins the prose twin:

  1. the literal filler FAILS lint_analysis (the specificity check is the
     filler-killer: no CVE, no 2+ digit number, no version token);
  2. structure + banned strings: an em dash, a heading, a single paragraph,
     a >6000-char body and AI-slop phrases (case-insensitive, curly
     apostrophes included) each fail;
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
     skips silently when no digest exists.

Run: python3 engine/test_prose_lint.py   (exit 0 = pass)
"""
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
check("1-paragraph analysis is SOFT-flagged instead",
      any("1 paragraph" in m for m in prose_lint.soft_paras(one)))

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
    open(os.path.join(digests_dir, "2026-09-24.md"), "w").write(GOOD_DIGEST)
    errs = ssg.run_prose_gate({"live-story": {"id": "live-story"}},
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

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} check(s): {', '.join(FAILS)}")
    sys.exit(1)
print("all store-health LEAF-3 prose-gate contract checks passed")
