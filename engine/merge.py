#!/usr/bin/env python3
"""Tia Storyline — incremental cluster + real scoring + analysis trigger.

Consumes data/new-events.json (ids written by ingest.py), merges each new event
into an existing story (URL match, then focused title-CVE match, then specific
token similarity) or creates a new story, recomputes all scores with the real
signal formula, updates the manifest, and emits data/needs-analysis.json for the
hourly LLM pass.

Usage: python3 merge.py
"""
import glob
import json
import os
import re
from datetime import datetime, timezone

from build_registry import QUALITY, DEFAULT_QUALITY, clean_title, tokens, domain_of, provisional_score

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
EVENTS = os.path.join(DATA, "events")
STORIES = os.path.join(DATA, "stories")
QUEUE = os.path.join(DATA, "new-events.json")
MANIFEST = os.path.join(DATA, "manifest.json")
ANALYSIS_DIR = os.path.join(DATA, "analysis")
NEEDS = os.path.join(DATA, "needs-analysis.json")
HOT_THRESHOLD = 2.0
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)


def parse_utc(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)


def load_stories():
    out = {}
    for f in glob.glob(os.path.join(STORIES, "*.json")):
        s = json.load(open(f))
        out[s["id"]] = s
    return out


def load_events():
    out = {}
    for f in glob.glob(os.path.join(EVENTS, "*.json")):
        e = json.load(open(f))
        out[e["id"]] = e
    return out


def story_event_urls(story):
    urls = set()
    for ref in story.get("events", []):
        e = events.get(ref["event_id"])
        if e and e["url"]:
            urls.add(e["url"].lower())
    return urls


# Tokens that recur in many titles without discriminating the story (template
# boilerplate). A token match must share at least one NON-generic token.
GENERIC = {"cisa", "urges", "immediate", "patching", "patch", "patches", "added",
           "kev", "actively", "critical", "zero", "day", "days", "flaws", "flaw",
           "bugs", "bug", "vulnerability", "vulnerabilities", "advisory",
           "advisories", "warns", "warn", "warning", "alerts", "alert", "exploited",
           "exploit", "exploits", "exploitation", "updated", "update", "updates",
           "fixes", "fixed", "released", "release", "announces", "announced",
           "confirmed", "confirms", "reported", "reports", "details", "detail",
           "analysis", "exposed", "exposes", "targeted", "target", "targets",
           "threat", "threats", "security", "malware", "ransomware", "campaign",
           "campaigns", "attack", "attacks", "attackers", "breach", "breaches",
           "data", "leak", "leaks", "researchers", "research", "company",
           "companies", "users", "user", "organizations", "federal", "states",
           "global", "latest", "major", "massive", "large", "scale", "backdoor",
           "backdoors", "active", "ongoing", "continues", "continued", "steals",
           "steal", "theft", "thefts", "fraud", "phishing", "scam", "scams"}


DATE_STOP = {"january", "february", "march", "april", "may", "june", "july", "august",
             "september", "october", "november", "december", "monday", "tuesday",
             "wednesday", "thursday", "friday", "saturday", "sunday"}
SERIES_RE = re.compile(r"\b[A-Za-z]+[0-9]*-\d{2,6}\b")   # AV26-797, CVE-2026-1234


def _norm_tokens(title):
    t = title.lower()
    t = re.sub(r"https?://\S+", "", t)         # strip URLs (junk tokens)
    t = re.sub(r"\b\d{4}\b", "", t)            # strip years (2026 shared everywhere)
    t = re.sub(r"\bnon-", "non", t)            # non-mobile != mobile
    t = re.sub(r"\bun-", "un", t)
    t = re.sub(r"\bde-", "de", t)
    return tokens(t)


def _series_codes(title):
    return {m.group(0).upper() for m in SERIES_RE.finditer(title)}


def match_scores(ev, story):
    """Score how strongly this event belongs to this story (0 = no match)."""
    if ev["url"] and ev["url"].lower() in story_url_cache.get(story["id"], set()):
        return 100.0
    ev_title_cves = {c.upper() for c in CVE_RE.findall(ev["title"])}
    if ev_title_cves and story.get("cves") and len(ev_title_cves) <= 2:
        if ev_title_cves & set(story["cves"]):
            return 50.0
    ev_disc = _norm_tokens(ev["title"]) - GENERIC - DATE_STOP
    st_disc = _norm_tokens(story["title"]) - GENERIC - DATE_STOP
    if len(ev_disc) >= 2 and len(st_disc) >= 2:
        shared = ev_disc & st_disc
        if len(shared) >= 2:                      # need >= 2 real discriminators
            # distinct advisory/vuln series codes (AV26-797 vs AV26-791) block merging
            ev_codes = _series_codes(ev["title"])
            st_codes = _series_codes(story["title"])
            if ev_codes and st_codes and not (ev_codes & st_codes):
                return 0.0
            j = len(shared) / len(ev_disc | st_disc)
            if j >= 0.4:
                return j * 10.0
    return 0.0


def match_story(ev, stories):
    """Best-match across ALL stories (not first-match-wins); None if no real match."""
    best, best_score = None, 0.0
    for sid in list(stories.keys()):
        sc = match_scores(ev, stories[sid])
        if sc > best_score:
            best, best_score = sid, sc
    return best


def real_score(s):
    """Recency x breadth x quality x 2 + velocity + reddit + cve (cap 6)."""
    last = datetime.fromisoformat(s["last_seen"].replace("Z", "+00:00"))
    hours = max(0, (datetime.now(timezone.utc) - last).total_seconds() / 3600)
    recency = 2.718 ** (-hours / 36)
    breadth = min(3.0, 1 + 0.5 * (s.get("n_sources", 1) - 1))
    q = max((QUALITY.get(d, DEFAULT_QUALITY) for d in s.get("sources", [])), default=DEFAULT_QUALITY)
    n48 = 0
    for ref in s.get("events", []):
        e = events.get(ref["event_id"])
        if e:
            dt = datetime.fromisoformat(e["published_at"].replace("Z", "+00:00"))
            if (datetime.now(timezone.utc) - dt).total_seconds() < 172800:
                n48 += 1
    velocity = min(2.0, 0.6 * n48)
    # reddit signal: prefer the persisted match (stable across runs), refresh it
    sig = s.get("reddit_signal") or {}
    matched_at = sig.get("matched_at", "")
    fresh_signal = (datetime.fromisoformat(matched_at.replace("Z", "+00:00"))
                    if matched_at else datetime.min.replace(tzinfo=timezone.utc))
    rmatch = 0.0
    if (datetime.now(timezone.utc) - fresh_signal).total_seconds() < 7 * 86400:
        rmatch = 0.4
    else:
        ev_urls = {e["url"].lower() for ref in s.get("events", [])
                   if (e := events.get(ref["event_id"])) and e["url"]}
        rt = tokens(s["title"])
        for r in reddit_posts:
            if r.get("article_url") and r["article_url"].lower() in ev_urls:
                rmatch = 0.4
                break
            rr = tokens(r.get("title", ""))
            if len(rt) >= 2 and len(rr) >= 2 and len(rt & rr) / len(rt | rr) >= 0.5:
                rmatch = 0.3
                break
        if rmatch:
            s["reddit_signal"] = {"posts": 1, "best_score": 0,
                                  "matched_at": datetime.now(timezone.utc).isoformat()}
    cve = 0.5 if s.get("cves") else 0.0
    return round(min(6.0, recency * breadth * q * 2 + velocity + rmatch + cve), 1)


def emit_needs(stories):
    queue = []
    for s in stories.values():
        if s["score"] < HOT_THRESHOLD:
            continue
        analysis_path = os.path.join(ANALYSIS_DIR, s["id"] + ".md")
        marker = (s.get("analysis") or {}).get("updated_at", "")
        if not os.path.exists(analysis_path):
            queue.append(s["id"])
            continue
        if not marker:                       # analysis file exists but no marker: use mtime
            marker = datetime.fromtimestamp(os.path.getmtime(analysis_path),
                                             tz=timezone.utc).isoformat()
        newest = max((events.get(ref["event_id"])["published_at"]
                      for ref in s.get("events", []) if ref["event_id"] in events), default="")
        if newest and parse_utc(newest) > parse_utc(marker):
            queue.append(s["id"])
    json.dump({"updated_at": datetime.now(timezone.utc).isoformat(), "stories": queue},
              open(NEEDS, "w"), indent=1)
    return len(queue)


def main():
    global events, reddit_posts, story_url_cache
    events = load_events()
    stories = load_stories()
    reddit_posts = json.load(open(os.path.join(DATA, "reddit.json"))) if os.path.exists(os.path.join(DATA, "reddit.json")) else []
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {"stories_per_day": {}}
    story_url_cache = {sid: story_event_urls(s) for sid, s in stories.items()}

    queue = json.load(open(QUEUE)) if os.path.exists(QUEUE) else {"events": []}
    new_ids = queue.get("events", [])
    created = merged = 0
    for eid in new_ids:
        ev = events.get(eid)
        if not ev:
            continue
        target = match_story(ev, stories)
        day = ev["published_at"][:10]
        if target:
            s = stories[target]
            refs = [r["event_id"] for r in s["events"]]
            if eid in refs:                      # already processed — never touch kind
                continue
            ev["kind"] = "update"
            s["events"].append({"event_id": eid, "label": "update"})
            if ev["published_at"] > s.get("last_seen", ""):
                s["last_seen"] = ev["published_at"]
            domains = [domain_of(ev["url"])] if ev["url"] else []
            s["sources"] = list(dict.fromkeys(s.get("sources", []) + [d for d in domains if d]))
            s["n_sources"] = len(s["sources"])
            s["cves"] = sorted(set(s.get("cves", [])) | set(ev["cves"]))
            s["first_seen"] = min(s.get("first_seen", ev["published_at"]), ev["published_at"])
            if ev["url"]:
                story_url_cache.setdefault(target, set()).add(ev["url"].lower())
            merged += 1
        else:
            ev["kind"] = "original"
            slug = build_slug(ev["title"], stories)
            s = {"id": slug, "title": clean_title(ev["title"]),
                 "first_seen": ev["published_at"], "last_seen": ev["published_at"],
                 "sources": [domain_of(ev["url"])] if ev["url"] else [],
                 "n_sources": 1 if ev["url"] else 0,
                 "cves": ev["cves"], "score": 0.0,
                 "reddit_signal": {"posts": 0, "best_score": 0},
                 "events": [{"event_id": eid, "label": "original"}]}
            stories[slug] = s
            story_url_cache[slug] = {ev["url"].lower()} if ev["url"] else set()
            created += 1
        json.dump(ev, open(os.path.join(EVENTS, eid + ".json"), "w"), indent=1)
        manifest.setdefault("stories_per_day", {}).setdefault(day, [])
        target_slug = target or (next(s for s in stories.values() if s["events"][-1]["event_id"] == eid)["id"])
        if target_slug not in manifest["stories_per_day"][day]:
            manifest["stories_per_day"][day].append(target_slug)

    for s in stories.values():
        s["score"] = real_score(s)
        json.dump(s, open(os.path.join(STORIES, s["id"] + ".json"), "w"), indent=1)

    json.dump(manifest, open(MANIFEST, "w"), indent=1)
    needs = emit_needs(stories)
    json.dump({"date": queue.get("date", ""), "events": []}, open(QUEUE, "w"), indent=1)
    print(f"new events: {len(new_ids)} | merged: {merged} | created: {created} | needs analysis: {needs}")
    print(f"stories total: {len(stories)}")


def build_slug(title, stories):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:64].rstrip("-")
    if slug in stories:
        slug = slug + "-" + str(len(stories) + 1)
    return slug


if __name__ == "__main__":
    main()
