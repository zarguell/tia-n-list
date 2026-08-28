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

from build_registry import clean_title, tokens, domain_of
from score import hot_score, SB_DEFAULTS as _SB_DEFAULTS, backfill_score_breakdown

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
EVENTS = os.path.join(DATA, "events")
STORIES = os.path.join(DATA, "stories")
QUEUE = os.path.join(DATA, "new-events.json")
MANIFEST = os.path.join(DATA, "manifest.json")
ANALYSIS_DIR = os.path.join(DATA, "analysis")
NEEDS = os.path.join(DATA, "needs-analysis.json")
HOT_THRESHOLD = 3.3      # analysis-queue gate on the 0-10 scale (was 2.0 on 0-6); deliberately below the display 5.0 for coverage
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
    """Merged events (meta + content_md from the .md sidecar) so hot_score's
    content signals actually see article text. See engine/store.py."""
    from store import load_events as _load
    return _load()


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
SERIES_RE = re.compile(r"\b[A-Za-z]+[0-9]*-\d{2,6}\b")   # AV26-797, CVE-2026-1234, Storm-0324

# Threat actors that anchor "same actor, many victims" claim series. A title
# token matches after stripping a leading "the" ("TheGentlemen" == "The
# Gentlemen" == "Gentlemen"). Tokens <4 chars never survive tokens() (e.g. INC
# Ransom's "inc") and common words ("play", "storm", "hive") are safe because
# _is_claim() must pass on BOTH titles before the actor path fires. Add new
# actors here (token form, lowercase); the claim gate keeps the list honest.
ACTOR_TOKENS = frozenset("""
    gentlemen clop storm shinyhunters deadlock aeternum qilin lockbit blackbasta
    akira ransomhub hunters blackcat alphv lynx medusa 8base play noescape funksec
    killsec darkvault mosey bashe handala gunra intelbroker rhysida ciphbit
    karakurt monti spacecobra hive vice cuba abyss ransomhouse majinahanashi
    threeam wazawaza
""".split())
# "this is a ransomware/breach claim" signal (order-independent, either side)
RANSOM_SIGNAL_RE = re.compile(
    r"\b(ransomware|ransom|extortion|locker|data\s+breach|breach|leak|exfiltrat|"
    r"stolen\s+data|brick)\b", re.I)
CLAIM_VERB_RE = re.compile(
    r"\b(attack(s|ed)?|target(s|ed)?|hit(s)?|strike(s|n)?|claim(s|ed)?|"
    r"compromise(s|d)?|victim(s)?|leak(s|ed)?|encrypt(s|ed)?|demand(s)?|"
    r"hack(s|ed|ing)?|breach(es|ed)?|disrupt(s|ed)?|extort(s|ed)?)\b", re.I)
ACTOR_WINDOW_DAYS = 14      # merge same-actor claims only into an ACTIVE series


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


# Title-verb filler that inflates similarity between unrelated headlines
# ("X Lets Attackers Gain..." vs "Y Lets Hackers Gain..."). Not story signal.
# Shared by merge-adjacent consumers (repair_dedupe, audit duplicate suspects).
FILLER = {"lets", "let", "gain", "gains", "using", "use", "used", "new", "via",
          "could", "can", "from", "into", "your", "you", "their", "its", "how",
          "why", "what", "before", "after", "amid"}


def title_discriminators(title):
    """Meaningful title tokens: [REDACTED], generic/boilerplate/filler-stripped."""
    return _norm_tokens(title) - GENERIC - DATE_STOP - FILLER


def title_jaccard(a, b):
    """Discriminator-token Jaccard similarity of two titles (0..1)."""
    A = title_discriminators(a or "")
    B = title_discriminators(b or "")
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def distinct_series_codes(a, b):
    """Both titles carry advisory/vuln series codes (AV26-815, CVE-2026-19598)
    and none are shared -> different advisories, never merge (guards dedup
    suspects and repair merges against truncated-slug collisions)."""
    ca, cb = _series_codes(a or ""), _series_codes(b or "")
    return bool(ca and cb and not (ca & cb))


def _actor_norm(tokens_set):
    """Normalize actor tokens across title forms: 'thegentlemen' == 'gentlemen'.
    (bare 'the' never survives tokens(), so only a leading-'the' strip is needed)"""
    return {(t[3:] if t.startswith("the") and len(t) > 4 else t) for t in tokens_set}


def _is_claim(title):
    """Victim-claim phrasing (ransomware/extortion/breach signal + a claim verb),
    order-independent — both halves must be present for a series merge."""
    t = title or ""
    return bool(RANSOM_SIGNAL_RE.search(t) and CLAIM_VERB_RE.search(t))


def _actor_series_score(ev, story, ev_disc, st_disc):
    """Same threat actor + both titles are victim claims + temporally near ->
    one series story (45.0, decaying with the gap so the freshest series wins).
    Never into a redirect shell; distinct advisory/vuln series codes still block."""
    if story.get("merged_into"):
        return 0.0
    actor = _actor_norm(ev_disc) & _actor_norm(st_disc) & ACTOR_TOKENS
    if not actor:
        return 0.0
    if not (_is_claim(ev["title"]) and _is_claim(story.get("title", ""))):
        return 0.0
    ev_codes = _series_codes(ev["title"])
    st_codes = _series_codes(story.get("title", ""))
    if ev_codes and st_codes and not (ev_codes & st_codes):
        return 0.0
    try:
        gap = max(0, (parse_utc(ev["published_at"]) -
                      parse_utc(story.get("last_seen", ev["published_at"]))).days)
    except Exception:
        return 0.0
    if gap > ACTOR_WINDOW_DAYS:
        return 0.0
    return 45.0 - gap


def match_scores(ev, story):
    """Score how strongly this event belongs to this story (0 = no match)."""
    if ev["url"] and ev["url"].lower() in story_url_cache.get(story["id"], set()):
        return 100.0
    ev_title_cves = {c.upper() for c in CVE_RE.findall(ev["title"])}
    if ev_title_cves and story.get("cves") and len(ev_title_cves) <= 2:
        if ev_title_cves & set(story["cves"]):
            return 50.0
    ev_disc = _norm_tokens(ev["title"]) - GENERIC - DATE_STOP
    st_disc = _norm_tokens(story.get("title", "")) - GENERIC - DATE_STOP
    if len(ev_disc) >= 2 and len(st_disc) >= 2:
        shared = ev_disc & st_disc
        if len(shared) >= 2:                      # need >= 2 real discriminators
            # distinct advisory/vuln series codes (AV26-797 vs AV26-791) block merging
            ev_codes = _series_codes(ev["title"])
            st_codes = _series_codes(story.get("title", ""))
            if ev_codes and st_codes and not (ev_codes & st_codes):
                return 0.0
            j = len(shared) / len(ev_disc | st_disc)
            if j >= 0.4:
                return j * 10.0
    return _actor_series_score(ev, story, ev_disc, st_disc)


def match_story(ev, stories):
    """Best-match across ALL stories (not first-match-wins); None if no real match.
    Ties break toward the newer / more complete story so actor-series events
    converge on one canonical story deterministically."""
    best, best_score, best_key = None, 0.0, None
    for sid in list(stories.keys()):
        s = stories[sid]
        if s.get("merged_into"):
            continue               # never deposit events into a redirect shell
        sc = match_scores(ev, s)
        if sc <= 0:
            continue
        key = (s.get("last_seen", ""), len(s.get("events", [])))
        if sc > best_score or (sc == best_score and key > best_key):
            best, best_score, best_key = sid, sc, key
    return best


def real_score(s):
    """CVSS-inspired hot score (see score.py) — real CVSS severity, KEV status,
    content signals, pickup speed, velocity, breadth, authority, recency, reddit."""
    return hot_score(s, events, reddit_posts)


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
        target_slug = target or (next(s for s in stories.values() if s["events"] and s["events"][-1]["event_id"] == eid)["id"])
        if target_slug not in manifest["stories_per_day"][day]:
            manifest["stories_per_day"][day].append(target_slug)

    for s in stories.values():
        try:
            sc = real_score(s)
            s["score"] = sc["score"]
            s["score_breakdown"] = {k: v for k, v in sc.items() if k != "score"}
        except Exception as e:
            # One story's scoring failure must not abort the whole merge nor
            # leave an empty score_breakdown (which crashes the SSG render and
            # blocks the publish). Preserve the existing breakdown/score; else
            # fall back to a safe zero breakdown with every template key.
            print(f"  WARN: score {s['id']}: {e}")
            s.setdefault("score_breakdown", dict(_SB_DEFAULTS))
            s.setdefault("score", 0.0)
        # Crash-safety: guarantee every template key exists, so a stale or
        # missing-key breakdown can never take down the build.
        backfill_score_breakdown(s)
        s.setdefault("score", 0.0)
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
