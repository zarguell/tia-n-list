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

    # --- weekend severity signals (2026-08-15) --------------------------
    # scale: "+" forms and org/company units (LiteLLM "2,500+ Organizations")
    evs_scale1 = [ev("x1", iso(1))]
    s_scale1 = story("scale1", ["example.com"], [],
                     "Breach Exposes 2,500+ Organizations and 434,000 CI/CD Pipelines",
                     evs_scale1, iso(1))
    r5 = score.hot_score(s_scale1, {e["event_id"]: e for e in evs_scale1}, [], now=base)
    ok &= check("scale signal fires on 'N+ organizations'",
                r5["severity"] >= 0.7, True)
    ok &= check("scale signal fires on bare 'N organizations'",
                score.hot_score(story("scale2", ["example.com"], [],
                                      "2,488 Organizations Exposed in Cloud Config Leak",
                                      [ev("x2", iso(1))], iso(1)),
                                {"x2": ev("x2", iso(1))}, [], now=base)["severity"] >= 0.7, True)
    # supply chain (LiteLLM blast radius)
    ok &= check("supply-chain signal fires",
                score.hot_score(story("sc1", ["example.com"], [],
                                      "LiteLLM Supply-Chain Breach Blast Radius",
                                      [ev("x3", iso(1))], iso(1)),
                                {"x3": ev("x3", iso(1))}, [], now=base)["severity"] >= 0.8, True)
    # security-control bypass — the VBS/HVCI research-drop body (verbatim)
    vbs_text = ("A newly disclosed Windows attack technique, dubbed \"Download More RAM,\" "
                "can undermine Virtualization-Based Security (VBS), bypass "
                "Hypervisor-Protected Code Integrity (HVCI), and disable endpoint "
                "protections including Microsoft Defender and third-party EDR products.")
    ok &= check("bypass signal fires on VBS/HVCI body",
                score.hot_score(story("bp1", ["example.com"], [],
                                      "Download More RAM Attack Bypasses Windows VBS",
                                      [ev("x4", iso(1), vbs_text)], iso(1)),
                                {"x4": ev("x4", iso(1), vbs_text)}, [], now=base)["severity"] >= 0.8, True)
    # bypass negatives — common non-control "bypass" uses never fire
    for neg_title, neg_text in [
        ("Two-Factor Authentication Bypass Phishing Kit Steals OTPs", ""),
        ("Vendor patch bypasses the workaround in the latest release", ""),
        ("Captcha bypass service advertises on Telegram", ""),
        ("MFA bypass phishing kit targets banking customers", ""),
    ]:
        neg = score.hot_score(story("neg", ["example.com"], [], neg_title,
                                    [ev("n1", iso(1), neg_text)], iso(1)),
                              {"n1": ev("n1", iso(1), neg_text)}, [], now=base)
        ok &= check(f"bypass does not fire: {neg_title[:40]}",
                    neg["severity"], 0.5)

    # --- high-impact weights (2026-10-13 owner decision fc3f6e00a8d9) ------
    # The recurring "score under-ranks high-impact" promotes: a CVSS the
    # coverage states must band like a stored one, unpatched CVSS >= 9.0
    # gets explicit weight, confirmed in-the-wild exploitation gets
    # explicit weight. Controls keep the old numbers.
    w1 = ev("w1", iso(1), "the flaw is unpatched and cvss 10")
    s_stated = story("stated", ["example.com"], ["CVE-2026-00001"],
                     "CVE-2026-00001 Erlang OTP client auth bypass (CVSS 10)",
                     [w1], iso(1))
    rw = score.hot_score(s_stated, {"w1": w1}, [], now=base)
    ok &= check("text-stated CVSS 10 bands like a stored CVE (store lacks it)",
                rw["severity"] >= 4.5, True)
    ok &= check("unpatched CVSS >= 9.0 carries the impact weight (4.5 + 0.4)",
                rw["severity"], 4.9)

    s_stated_fixed = story("stated-fixed", ["example.com"], ["CVE-2026-00001"],
                           "CVE-2026-00001 Erlang OTP client auth bypass (CVSS 10)",
                           [ev("w1b", iso(1), "the flaw is patched in this release")], iso(1))
    rf = score.hot_score(s_stated_fixed,
                         {"w1b": ev("w1b", iso(1), "the flaw is patched in this release")},
                         [], now=base)
    ok &= check("patched CVSS 10 gets no unpatched weight (control)",
                rf["severity"], 4.5)

    wild_ev = ev("w2", iso(1), "the flaw is actively exploited in the wild")
    s_wild = story("wild", ["example.com"], [], "Router Flaw Under Attack",
                   [wild_ev], iso(1))
    neutral_ev = ev("w3", iso(1), "attackers probe devices at scale")
    s_neutral = story("neutral", ["example.com"], [], "Router Flaw Under Attack",
                      [neutral_ev], iso(1))
    rwild = score.hot_score(s_wild, {"w2": wild_ev}, [], now=base)
    rneutral = score.hot_score(s_neutral, {"w3": neutral_ev}, [], now=base)
    ok &= check("in-the-wild exploitation carries explicit weight",
                round(rwild["severity"] - rneutral["severity"], 2), 0.7)
    ok &= check("severity still caps at 5.0 with weights",
                score.hot_score(s_severe, {e["event_id"]: e for e in evs_severe},
                                [], now=base)["severity"] <= 5.0, True)

    # --- corroborated no-CVE novelty (2026-10-17 owner decision f5f2bc09664a)
    # audit Rec 3: multi-source first-of-kind TTP coverage with no CVE sat
    # at the 0.5 floor beside routine traction. Two sources + TTP terms
    # earns half a severity step; every control below must stay floored.
    nov_ev = [ev("v1", iso(3), "tox-c2 loader drops the payload"),
              ev("v2", iso(2), "researchers detail the c2 loader")]
    s_nov = story("nov", ["example.com", "example.org"], [],
                  "Avisloader Windows Malware Uses Tox C2 to Survive Takedown",
                  nov_ev, iso(2))
    rnov = score.hot_score(s_nov, {e["event_id"]: e for e in nov_ev}, [],
                           now=base)
    ok &= check("corroborated no-CVE TTP earns the novelty bonus",
                (rnov["novelty"], rnov["severity"]), (0.5, 1.0))
    plain_ev = [ev("p1", iso(3), "routine patch release notes"),
                ev("p2", iso(2), "vendor posts the update")]
    rplain = score.hot_score(
        story("plain", ["example.com", "example.org"], [],
              "Vendor Releases Routine Security Update", plain_ev, iso(2)),
        {e["event_id"]: e for e in plain_ev}, [], now=base)
    ok &= check("multi-source traction without TTP terms earns nothing",
                (rplain["novelty"], rplain["severity"]), (0.0, 0.5))
    solo = score.hot_score(
        story("solo", ["example.com"], [],
              "Avisloader Windows Malware Uses Tox C2 to Survive Takedown",
              [ev("v1", iso(3), "tox-c2 loader drops the payload")], iso(3)),
        {"v1": ev("v1", iso(3), "tox-c2 loader drops the payload")},
        [], now=base)
    ok &= check("single-source TTP earns nothing (uncorroborated)",
                (solo["novelty"], solo["severity"]), (0.0, 0.5))
    cve_tt = score.hot_score(
        story("cvett", ["example.com", "example.org"], ["CVE-2026-99999"],
              "Tox C2 Loader Exploits CVE-2026-99999", nov_ev, iso(2)),
        {e["event_id"]: e for e in nov_ev}, [], now=base)
    ok &= check("CVE-carrying TTP earns nothing (severity already prices it)",
                cve_tt["novelty"], 0.0)
    ok &= check("traction-only still floored with novelty live",
                r1["severity"], 0.5)

    # --- A4: engine NVD cache merges into the CVE store (kev stays kev-only)
    saved_store = score._cve_store
    score._cve_store = None
    merged = score._load_cve_store()
    vbs_info = merged.get("CVE-2026-23670")
    ok &= check("nvd-cache fallback supplies CVSS for fresh CVEs",
                vbs_info is not None and bool(vbs_info.get("cvss")), True)
    ok &= check("nvd-cache fallback never asserts kev",
                vbs_info is None or vbs_info.get("kev"), False)
    score._cve_store = saved_store

    # --- A5: incoherent event-sink penalty (2026-10-23 audit Issue 1 + Rec
    # 2, owner decision 065758633baa). A broad pile of unrelated headlines
    # must not be paid breadth/velocity for its size; a coherent multi-outlet
    # incident must keep them.
    def _evt(eid, title, hours_before, text=""):
        return {"event_id": eid, "published_at": iso(hours_before),
                "url": f"https://outlet.example/{eid}", "content_md": text,
                "kind": "original", "lang": "en", "source": "example.com",
                "title": title}

    # negative: the `machine-speed-attacks-...` sink shape — the title is the
    # founding event's headline, and the other events are unrelated stories
    # (botnet writeup, CVE advisory, breach claim, RAT research, job ads)
    sink_title = "Machine speed attacks require machine speed detection and response"
    sink_evs = [_evt("s0", sink_title, 10),
                _evt("s1", "Egyptian botnet spreads through pirated software", 20),
                _evt("s2", "Signal RingRTC CVE-2026-113380 patched", 21),
                _evt("s3", "GitLab security advisory AV26-1074", 22),
                _evt("s4", "PingCAP breach claim under investigation", 23),
                _evt("s5", "DarkCore RAT research notes", 24),
                _evt("s6", "K0T steals FortiGate credentials", 25),
                _evt("s7", "Senior security engineer, remote, apply now", 26),
                _evt("s8", "Staff incident response analyst, hybrid", 27)]
    sink = {"id": "sink", "title": sink_title,
            "sources": [f"outlet{i}.example" for i in range(24)],
            "n_sources": 24, "cves": [],
            "events": [{"event_id": e["event_id"], "label": "update"}
                       for e in sink_evs],
            "last_seen": iso(10),
            "reddit_signal": {"posts": 0, "best_score": 0}}
    r_sink = score.hot_score(sink, {e["event_id"]: e for e in sink_evs}, [],
                             now=base)
    ok &= check("event sink is flagged incoherent", r_sink["incoherent"], True)
    ok &= check("breadth+velocity reward is cancelled (penalty visible)",
                r_sink["incoherent_penalty"],
                round(r_sink["breadth"] + r_sink["velocity"], 2))
    # same story with the size floor lifted (penalty cannot fire): the paid
    # score must be strictly higher than the penalised one
    saved_min = score.INCOHERENT_MIN_EVENTS
    score.INCOHERENT_MIN_EVENTS = 999          # simulate "coherent"
    r_paid = score.hot_score(sink, {e["event_id"]: e for e in sink_evs}, [],
                             now=base)
    score.INCOHERENT_MIN_EVENTS = saved_min
    ok &= check("incoherence removes the reward (paid score is higher)",
                (r_paid["incoherent"], r_paid["score"] > r_sink["score"]),
                (False, True))
    ok &= check("penalised sink drops below the hot gate",
                r_sink["score"] < 5.0, True)

    # positive: a coherent multi-outlet incident — every event headline echoes
    # the story's own discriminators, so breadth/velocity still pay
    good_title = "Chrome 156 Security Update Fixes Critical Vulnerabilities"
    good_evs = [_evt(f"g{i}",
                     f"Chrome 156 Security Update Fixes {i + 3} Critical "
                     f"Vulnerabilities", 5 + i)
                for i in range(10)]
    good = {"id": "good", "title": good_title,
            "sources": [f"outlet{i}.example" for i in range(10)],
            "n_sources": 10, "cves": [],
            "events": [{"event_id": e["event_id"], "label": "original"}
                       for e in good_evs],
            "last_seen": iso(5),
            "reddit_signal": {"posts": 0, "best_score": 0}}
    r_good = score.hot_score(good, {e["event_id"]: e for e in good_evs}, [],
                             now=base)
    ok &= check("coherent multi-outlet incident is not flagged",
                (r_good["incoherent"], r_good["incoherent_penalty"]),
                (False, 0.0))
    ok &= check("coherent incident keeps its breadth/velocity reward",
                (r_good["breadth"], r_good["velocity"]), (2.0, 2.0))
    ok &= check("coherent incident scores above the penalised sink",
                r_good["score"] > r_sink["score"], True)

    # guard: a small reworded story is never flagged (below the size floor)
    small_evs = [_evt("m0", "HPE patches critical RCE flaws in AOS-CX", 3),
                 _evt("m1", "Aruba networking bug lets attackers run code", 4)]
    small = {"id": "small", "title": "HPE patches critical RCE vulnerabilities in AOS-CX",
             "sources": ["example.com", "example.org"], "n_sources": 2,
             "cves": [], "events": [{"event_id": e["event_id"], "label": "update"}
                                    for e in small_evs],
             "last_seen": iso(3),
             "reddit_signal": {"posts": 0, "best_score": 0}}
    r_small = score.hot_score(small, {e["event_id"]: e for e in small_evs}, [],
                              now=base)
    ok &= check("small story never trips the incoherence floor",
                (r_small["incoherent"], r_small["incoherent_penalty"]),
                (False, 0.0))

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
