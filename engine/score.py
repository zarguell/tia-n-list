#!/usr/bin/env python3
"""Tia Storyline — CVSS-inspired hot scoring.

Each factor is explicit with a defined range; the base is multiplied by a
recency temporal factor and community signal is added, then capped to the
site's 0-10 display scale. Bands (aligned to the heat classes in ssg.py):
0-3.2 new | 3.3-4.9 warm | 5.0-7.4 hot | 7.5+ hottest.

Severity is the dominant axis: a story gets hot on how bad it is, not on
how many outlets mention it (2026-08-13 rebalance — traction-only stories
used to cross the hot line at severity's 0.5 floor).

Factors:
  breadth   0.5-2.0  distinct sources (capped low; repetition != significance)
  authority 1.0-2.0  best outlet weight (reuters > securityweek/thn/bleeping ...)
  severity  0.5-5.0  real CVSS base score (kevrichment NVD store, falling back
                     to the engine NVD cache), KEV status, content signals
                     (zero-day, ransomware, OT/ICS, APT, actively exploited,
                     supply chain, security-control bypass, breach scale)
  velocity  0-2.0    events in the last 48h
  pickup    0-0.6    how fast the second source arrived (exp decay on hours)
  recency   temporal multiplier (half-life 36h)
  reddit    community, added post-multiplier (0.3/0.4, cap 1.5)
"""
import glob
import json
import os
import re
from datetime import datetime, timezone

AUTHORITY = {"reuters.com": 2.0, "apnews.com": 1.9, "bbc.com": 1.9, "bloomberg.com": 1.9,
             "securityweek.com": 1.8, "thehackernews.com": 1.8, "bleepingcomputer.com": 1.8,
             "krebsonsecurity.com": 1.7, "wired.com": 1.7, "arstechnica.com": 1.7,
             "theregister.com": 1.5, "darkreading.com": 1.5, "cyberscoop.com": 1.5,
             "recordedfuture.com": 1.5, "thedfirreport.com": 1.7, "gbhackers.com": 1.2,
             "malware.news": 1.2}
DEFAULT_AUTHORITY = 1.0

KEV_DIR = "/home/coder/workspace/kevrichment/data/cves"

SIGNALS = [
    (re.compile(r"\bzero[- ]day\b", re.I), 0.3),
    (re.compile(r"\b(ransomware|ransom)\b", re.I), 0.3),
    (re.compile(r"\b(critical infrastructure|industrial control|scada|power plant|utility|ot network|water system)\b", re.I), 0.3),
    (re.compile(r"\b(apt\d+|state-sponsored|threat actor|hacking group)\b", re.I), 0.2),
    (re.compile(r"\bactively exploited\b", re.I), 0.3),
    (re.compile(r"\bsupply[- ]chain\b", re.I), 0.3),
    # security-control bypass research (VBS/HVCI/EDR/Defender...): defense
    # evasion is significance, but only when a control term follows within
    # 60 chars — "2FA bypass"/"captcha bypass"/"patch bypasses" never fire
    (re.compile(r"\bbypass(?:es|ing|ed)?\b.{0,60}\b(hvci|vbs|defender|edr|endpoint|antivirus|smart ?screen|uac|applocker|secure boot|bitlocker|sandbox|code integrity|integrity)\b", re.I), 0.3),
    # breach scale: optional magnitude + "+" so "2,500+ organizations" and
    # "2,488 Organizations" count (2026-08-15: LiteLLM blast radius missed)
    (re.compile(r"\b\d[\d,.]*\+?\s*(million|billion|thousand)?\s*(records?|accounts?|users?|organizations?|companies?)\b", re.I), 0.2),
]
SIGNAL_CAP = 1.5

_cve_store = None


def _load_cve_store():
    """CVSS base score + KEV status per CVE from kevrichment's local NVD store,
    falling back to engine/data/nvd-info.json (CVSS for store CVEs not yet
    enriched by kevrichment — e.g. fresh research CVEs). KEV status is
    kevrichment-only; the fallback never asserts kev."""
    global _cve_store
    if _cve_store is not None:
        return _cve_store
    store = {}
    if os.path.isdir(KEV_DIR):
        for f in glob.glob(os.path.join(KEV_DIR, "*.json")):
            cve = os.path.basename(f)[:-5].upper()
            d = json.load(open(f))
            store[cve] = {"cvss": d.get("cvss_v3_base_score"),
                          "kev": bool(d.get("kev_date_added"))}
    nvd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "data", "nvd-info.json")
    if os.path.exists(nvd_path):
        nvd = json.load(open(nvd_path))
        for cve, info in nvd.items():
            cvss = (info.get("cvss") or {}).get("score")
            if cve.upper() not in store and cvss:
                store[cve.upper()] = {"cvss": cvss, "kev": False}
    _cve_store = store
    return store


def _cvss_severity(cves):
    store = _load_cve_store()
    if not cves:
        return 0.5, False
    best = 0.0
    kev = False
    for c in cves:
        info = store.get(c.upper())
        if info:
            best = max(best, info.get("cvss") or 0.0)
            kev = kev or info.get("kev")
    if best >= 9.0:
        s = 4.5
    elif best >= 7.0:
        s = 3.5
    elif best >= 4.0:
        s = 2.5
    elif best > 0:
        s = 1.5
    else:
        s = 1.0            # CVE present but not in the local store
    return s, kev


def hot_score(story, events, reddit_posts, now=None):
    """Compute the CVSS-inspired hot score for a story. Returns a dict with the
    final score and every factor, for transparent display."""
    if now is None:
        now = datetime.now(timezone.utc)
    parse = lambda iso: datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)

    # breadth (repetition is weak evidence — cap low)
    breadth = 0.5 + 0.5 * min(3, max(0, story.get("n_sources", 0) - 1))

    # authority
    authority = max((AUTHORITY.get(d, DEFAULT_AUTHORITY) for d in story.get("sources", [])),
                    default=DEFAULT_AUTHORITY)

    # severity (real CVSS + KEV + content signals) — the dominant axis
    cves = story.get("cves", [])
    sev, kev = _cvss_severity(cves)
    title = (story.get("title") or "").lower()
    body_text = " ".join(events.get(r["event_id"], {}).get("content_md", "") for r in story.get("events", []))[:4000].lower()
    text = title + " " + body_text
    signals = sum(w for rx, w in SIGNALS if rx.search(text))
    severity = min(5.0, sev + (0.5 if kev else 0.0) + min(SIGNAL_CAP, signals))

    # velocity (events in last 48h)
    n48 = 0
    for ref in story.get("events", []):
        e = events.get(ref["event_id"])
        if e:
            dt = parse(e["published_at"])
            if (now - dt).total_seconds() < 172800:
                n48 += 1
    velocity = min(2.0, 0.5 * n48)

    # pickup speed: hours between the first and second event
    pickup = 0.0
    ts = sorted(parse(events[ref["event_id"]]["published_at"])
                for ref in story.get("events", []) if ref["event_id"] in events)
    if len(ts) >= 2:
        gap_h = max(0.0, (ts[1] - ts[0]).total_seconds() / 3600)
        pickup = 0.6 * (2.718 ** (-gap_h / 24))

    base = breadth + authority + severity + velocity + pickup

    # recency temporal multiplier
    last = parse(story.get("last_seen") or "")
    hours = max(0, (now - last).total_seconds() / 3600)
    recency = 2.718 ** (-hours / 36)

    # reddit community signal
    rmatch = 0.0
    sig = story.get("reddit_signal") or {}
    matched_at = sig.get("matched_at", "")
    if matched_at:
        try:
            fresh = parse(matched_at)
            if (now - fresh).total_seconds() < 7 * 86400:
                rmatch = 0.4
        except ValueError:
            pass
    if not rmatch:
        ev_urls = {e["url"].lower() for ref in story.get("events", [])
                   if (e := events.get(ref["event_id"])) and e["url"]}
        for r in reddit_posts:
            if r.get("article_url") and r["article_url"].lower() in ev_urls:
                rmatch = 0.4
                break
    reddit = min(1.5, rmatch)

    score = round(min(10.0, base * recency + reddit), 1)
    return {
        "score": score,
        "base": round(base, 2),
        "breadth": round(breadth, 2),
        "authority": round(authority, 2),
        "severity": round(severity, 2),
        "velocity": round(velocity, 2),
        "pickup": round(pickup, 2),
        "recency": round(recency, 2),
        "reddit": round(reddit, 2),
        "kev": kev,
        "n_sources": story.get("n_sources", 0),
    }
