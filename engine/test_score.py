#!/usr/bin/env python3
"""Hot-score contract suite — the 0-10 rebalance (2026-08-13).

The user's complaint: too much is considered hot; a story was hot because it
was NEW and MENTIONED, not because it was significant. This suite pins the
contracts that fix that:

  1. traction-only stories (fresh, multi-source, no CVEs, no content signals,
     weak outlets) never cross the hot threshold — repetition is not heat;
  2. the SAME traction profile with a severe CVE + KEV + zero-day signal IS
     hot — severity is the dominant axis;
  3. the old 6.0 cap no longer compresses the top (maxed stories exceed 6.0);
  4. the 10.0 cap holds and factor ranges stay inside their documented bands;
  5. recency still cools a hot story off.

Run: python3 engine/test_score.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score  # noqa: E402

NOW = "2026-08-13T12:00:00Z"

# fixture CVE store: a severe, KEV-listed CVE (deterministic — no network)
score._cve_store = {"CVE-2026-99999": {"cvss": 9.8, "kev": True}}


def ev(eid, published, text=""):
    return {"event_id": eid, "published_at": published,
            "url": f"https://example.com/{eid}", "content_md": text,
            "kind": "original", "lang": "en", "source": "example.com",
            "title": text[:80]}


def story(sid, sources, cves, title, evs, last_seen):
    return {"id": sid, "title": title, "sources": sources, "cves": cves,
            "n_sources": len(sources), "events": [{"event_id": e["event_id"],
                                                   "label": "original"} for e in evs],
            "last_seen": last_seen, "reddit_signal": {"posts": 0, "best_score": 0}}


def check(name, got, expect):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got} want {expect}")
    return ok


def main():
    ok = True
    from datetime import datetime, timedelta, timezone
    base = datetime.fromisoformat(NOW.replace("Z", "+00:00"))

    def iso(hours_before):
        return (base - timedelta(hours=hours_before)).isoformat().replace("+00:00", "Z")

    # --- fixtures -----------------------------------------------------
    # traction-only: two weak outlets, no CVE, no signals, fresh
    evs_traction = [ev("t1", iso(2), "article about routine patch release"),
                    ev("t2", iso(1), "follow-up coverage of the patch release")]
    s_traction = story("traction", ["gbhackers.com", "malware.news"], [],
                       "Vendor Releases Routine Security Update",
                       evs_traction, iso(1))

    # same traction profile + severe CVE (CVSS 9.8, KEV) + zero-day signal
    evs_severe = [ev("s1", iso(2), "article about the flaw"),
                  ev("s2", iso(1), "follow-up coverage of the flaw")]
    s_severe = story("severe", ["gbhackers.com", "malware.news"], ["CVE-2026-99999"],
                     "Zero-Day Flaw Actively Exploited in the Wild",
                     evs_severe, iso(1))

    # maxed-out: high authority, many sources/events, KEV CVE
    evs_max = [ev(f"m{i}", iso(2 + i * 0.1), "coverage") for i in range(4)]
    s_max = story("maxed", ["reuters.com", "securityweek.com", "thehackernews.com"],
                  ["CVE-2026-99999"], "Zero-Day Ransomware Attack Exploits Critical Flaw",
                  evs_max, iso(0.1))

    # --- contracts ----------------------------------------------------
    r1 = score.hot_score(s_traction, {e["event_id"]: e for e in evs_traction}, [], now=base)
    ok &= check("traction-only is NOT hot (< 5.0)",
                r1["score"] < 5.0, True)
    ok &= check("traction-only severity sits at the 0.5 floor",
                r1["severity"], 0.5)

    r2 = score.hot_score(s_severe, {e["event_id"]: e for e in evs_severe}, [], now=base)
    ok &= check("same traction + severe CVE IS hot (>= 5.0)",
                r2["score"] >= 5.0, True)
    ok &= check("severity factor caps at 5.0",
                r2["severity"] <= 5.0, True)
    ok &= check("breadth factor caps at 2.0",
                r2["breadth"] <= 2.0, True)

    # maxed story breaks the old 6.0 cap and respects the new 10.0 one
    r3 = score.hot_score(s_max, {e["event_id"]: e for e in evs_max}, [], now=base)
    ok &= check("maxed story exceeds the old 6.0 cap",
                r3["score"] > 6.0, True)
    ok &= check("10.0 cap holds",
                r3["score"] <= 10.0, True)

    # recency still cools: same story judged 72h later drops
    later = base + timedelta(hours=72)
    r4 = score.hot_score(s_severe, {e["event_id"]: e for e in evs_severe}, [],
                         now=later)
    ok &= check("recency decay drops a hot story",
                r4["score"] < r2["score"], True)

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
