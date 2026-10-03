#!/usr/bin/env python3
"""Re-report penalty contract suite (2026-10-03, audit rec #2 — 3rd day).

Outlet echoes of already-carried coverage (no new CVEs, reworded same
headline) reset the 36h decay clock and stacked 48h velocity, keeping
echo-only stories on the digest slate until an agent demoted them by hand —
the audit attributed most of the ~340 digest demote overrides and 8 slugs
overridden >= 3 times to this single class. The contracts pinned here:

  1. score.is_rereport: founding events are never echoes; same-CVE reworded
     headlines are; events bringing a NEW CVE are developments even when the
     headline is near-identical; CVE-less stories classify on title overlap.
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

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {failures}")
    sys.exit(1)
print("all checks passed")
