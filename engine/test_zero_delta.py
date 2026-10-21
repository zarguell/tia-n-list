#!/usr/bin/env python3
"""Zero-delta demotion contract suite (2026-10-20 owner decision ed6b7366c2ec,
audit Rec 1, option "score-pe" — "address the real root causes and close them
out").

544 of 657 all-time digest overrides are demotes and the dominant reason is
"new events restate covered facts" — the daily digest agent demotes these BY
HAND every day. The 2026-10-03 re-report leg stopped echoes EARNING velocity
and recency, and PR #155 (6aad368c1a1b) neutralized rd: repost stubs, but a
story whose only recent movement is delta-free outlet re-reports kept riding
the slate on its decayed base with no explanation in the breakdown. The
contracts pinned here:

  1. an echo-only story (founding + outlet re-reports restating the same
     facts, nothing genuine inside the 48h window) is DEMOTED: the decayed
     score is halved, the breakdown carries zero_delta=true +
     zero_delta_penalty, and the factors (velocity/pickup/recency) are
     untouched — the demotion is a visible final-score factor, not a fudge;
  2. one later re-report that still carries a delta (a new victim count)
     leaves the story unpenalized;
  3. rd: repost stubs stay exactly as pinned by 6aad368c1a1b: a stub-only
     story's score is UNCHANGED (neutral plumbing — neither gain nor
     trigger), and a stub carrying a real delta is still a development;
  4. a genuine development inside the window (a new CVE, a new angle)
     leaves the story untouched — the trigger is strictly "nothing genuine
     in the recent window";
  5. scoring is deterministic: same input twice, same output dict.

Run: /home/zach/.local/venvs/tia-engine/bin/python engine/test_zero_delta.py
     (exit 0 = pass)
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

score._cve_store = {"CVE-2026-1234": {"cvss": 9.8, "kev": True},
                    "CVE-2026-5678": {"cvss": 7.5, "kev": False}}

BASE = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)


def iso(hours_before):
    return (BASE - timedelta(hours=hours_before)).isoformat().replace(
        "+00:00", "Z")


def ev(eid, title, published, cves=(), content=""):
    return {"id": eid, "title": title, "published_at": published,
            "cves": list(cves), "url": f"https://example.com/{eid}",
            "source": "example.com", "kind": "update", "lang": "en",
            "content_md": content}


def rd(eid, title, published, cves=()):
    """An `rd:` Reddit link-post stub: real headline, boilerplate content."""
    return {"id": eid, "title": title, "published_at": published,
            "cves": list(cves),
            "url": f"https://www.bleepingcomputer.com/{eid}",
            "source": "bleepingcomputer.com", "kind": "update", "lang": "en",
            "content_md": ("submitted by /u/someone [link] [comments]\n\n"
                           f"via reddit r/cybersecurity: {title}")}


def _story(events):
    return {"id": "s", "title": events[0]["title"],
            "sources": ["example.com"], "n_sources": 1,
            "cves": sorted({c for e in events for c in e["cves"]}),
            "last_seen": max(e["published_at"] for e in events),
            "reddit_signal": {"posts": 0, "best_score": 0},
            "events": [{"event_id": e["id"], "label": "update"}
                       for e in events]}


def _score(events):
    return score.hot_score(_story(events),
                           {e["id"]: e for e in events}, [], now=BASE)


# ── fixtures ────────────────────────────────────────────────────────────────
# founding event: genuine development, 60h old (outside the 48h window)
FOUND = ev("f1", "Acme mail flaw CVE-2026-1234 hit government email servers",
           iso(60), ["CVE-2026-1234"])
# ordinary outlet re-reports: reworded same-fact headlines, same CVE, no new
# actor / victim count / IOC — zero-delta echoes of covered material
ECHO1 = ev("e2", "Government email servers hit by Acme flaw CVE-2026-1234",
           iso(20), ["CVE-2026-1234"])
ECHO2 = ev("e3", "Acme mail flaw CVE-2026-1234 used in email server attacks",
           iso(2), ["CVE-2026-1234"])

# ── 1. echo-only story is demoted, visibly ─────────────────────────────────
control = _score([FOUND])           # founding alone: nothing recent, but no
                                    # echoes either — never penalized
check("control (founding only) is not flagged",
      control["zero_delta"], False)
check("control carries no penalty", control["zero_delta_penalty"], 0.0)
check("control counts no re-reports", control["rereports"], 0)

r = _score([FOUND, ECHO1, ECHO2])
check("echo-only story is flagged zero_delta", r["zero_delta"], True)
check("the penalty is a positive amount", r["zero_delta_penalty"] > 0, True)
check("the penalty never exceeds the pre-penalty score",
      r["zero_delta_penalty"] <= control["score"], True)
check("penalized score sits below its own decayed value",
      r["score"] < control["score"], True)
check("the demotion is the halving factor (modulo rounding)",
      abs(r["score"] - control["score"] / 2) <= 0.11, True)
check("echo-only story is held below the digest hot gate (3.3)",
      r["score"] < 3.3, True)
check("both echoes counted in the existing rereports counter",
      r["rereports"], 2)
check("the demotion does not fudge velocity", r["velocity"],
      control["velocity"])
check("the demotion does not fudge pickup", r["pickup"], control["pickup"])
check("the demotion does not fudge recency", r["recency"],
      control["recency"])
check("the demotion does not fudge severity", r["severity"],
      control["severity"])
check("decay still anchors to the genuine development (60h, not 2h)",
      r["recency"] < 0.2, True)

# ── 2. a re-report that still carries a delta blocks the trigger ────────────
# same echo shape, but the newest event adds a NEW victim count: a real
# development by the house delta definition (pinned classification: still a
# re-report, so no velocity — but the story is not echo-only).
VICTIM = ev("v1", "Acme mail flaw CVE-2026-1234 now linked to 4,100 accounts",
            iso(2), ["CVE-2026-1234"])
rv = _score([FOUND, ECHO1, VICTIM])
check("new-victim-count re-report blocks the demotion",
      rv["zero_delta"], False)
check("new-victim-count story carries no penalty",
      rv["zero_delta_penalty"], 0.0)
check("delta-carrying re-report still earns no velocity (classification "
      "unchanged)", rv["velocity"], 0.0)
check("unpenalized story keeps its full decayed score",
      rv["score"], control["score"])

# ── 3. rd: stub path stays exactly as pinned (6aad368c1a1b) ────────────────
STUB = rd("rd:t3_a",
          "Government email servers hit by Acme flaw CVE-2026-1234", iso(2))
rs = _score([FOUND, STUB])
check("a story whose only new event is an rd: stub keeps its score",
      rs["score"], control["score"])
check("...and is NOT flagged (stubs neither gain nor trigger)",
      rs["zero_delta"], False)
check("the stub is still counted as a re-report", rs["rereports"], 1)
check("the stub still adds zero velocity", rs["velocity"], 0.0)

# a stub WITH a genuine delta is still a development that re-warms the story
SACTOR = rd("rd:t3_b", "LockBit claims the Acme mail flaw attacks", iso(2))
ra = _score([FOUND, SACTOR])
check("a stub naming a NEW actor is a development, not an echo",
      score.is_rereport(SACTOR, [FOUND]), False)
check("...so the story re-warms instead of being flagged",
      (ra["zero_delta"], ra["score"] > control["score"]), (False, True))

# ── 4. a genuine development inside the window leaves the story untouched ──
DEV = ev("d1", "Acme mail flaw CVE-2026-1234 now chained with second flaw",
         iso(2), ["CVE-2026-1234", "CVE-2026-5678"])
rd_ = _score([FOUND, ECHO1, DEV])
check("genuine development inside the window blocks the demotion",
      rd_["zero_delta"], False)
check("developed story carries no penalty", rd_["zero_delta_penalty"], 0.0)
check("developed story restores velocity", rd_["velocity"], 0.5)
check("developed story outranks its echo-only twin",
      rd_["score"] > r["score"], True)

# ── 5. determinism: same input twice, same output ──────────────────────────
story_a, events_a = _story([FOUND, ECHO1, ECHO2]), {
    e["id"]: e for e in [FOUND, ECHO1, ECHO2]}
first = score.hot_score(story_a, events_a, [], now=BASE)
second = score.hot_score(story_a, events_a, [], now=BASE)
check("same input twice, identical output dict", first, second)
check("...including the zero-delta fields",
      (first["zero_delta"], first["zero_delta_penalty"]),
      (second["zero_delta"], second["zero_delta_penalty"]))

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {failures}")
    sys.exit(1)
print("all checks passed")
