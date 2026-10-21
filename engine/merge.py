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
import sys
from datetime import datetime, timedelta, timezone

from build_registry import (clean_title, tokens, domain_of,
                            STOP as BR_STOP, CYBER_STOP as BR_CYBER_STOP)
from score import (hot_score, SB_DEFAULTS as _SB_DEFAULTS,
                   backfill_score_breakdown, update_peak)
import lifecycle

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
EVENTS = os.path.join(DATA, "events")
STORIES = os.path.join(DATA, "stories")
QUEUE = os.path.join(DATA, "new-events.json")
MANIFEST = os.path.join(DATA, "manifest.json")
ANALYSIS_DIR = os.path.join(DATA, "analysis")
NEEDS = os.path.join(DATA, "needs-analysis.json")
CTI_DIR = os.path.join(DATA, "cti")
HOT_THRESHOLD = 3.3      # analysis-queue gate on the 0-10 scale (was 2.0 on 0-6); deliberately below the display 5.0 for coverage
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)

# Collector channels (x-collector, social-collector) feed events that may
# ATTACH to stories but never MINT them — social amplifies, feeds create.
# Unmatched social events park in social-pending.json and retry every merge
# until a feed-minted story corroborates them or the TTL expires them.
# 2026-09 incident: masto link-posts minted ~1.6k stories/month (2.4x the
# entire Miniflux category), and the triage drops that rejected them left
# ~4.5k zero-event shells in the store.
SOCIAL_PREFIXES = ("masto:", "x:", "bsky:")
PENDING = os.path.join(DATA, "social-pending.json")
SOCIAL_TTL_H = 48


def parse_utc(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)


def _load_json_or_default(path, default):
    """Fail-open JSON load: corrupt/empty/unreadable file warns to stderr
    and falls back to default so one bad file can't stall the hourly run."""
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        print(f"WARN: skipping corrupt file {path}: {exc}", file=sys.stderr)
        return default


def load_stories():
    out = {}
    for f in glob.glob(os.path.join(STORIES, "*.json")):
        try:
            with open(f) as fh:
                s = json.load(fh)
        except (json.JSONDecodeError, ValueError, OSError) as exc:
            print(f"WARN: skipping corrupt story file {f}: {exc}", file=sys.stderr)
            continue
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
            urls.add(norm_url(e["url"]))
    return urls


# Tokens that recur in many titles without discriminating the story (template
# boilerplate). A token match must share at least one NON-generic token.
# BR_STOP/BR_CYBER_STOP (build_registry) are the tokenizer-side stop lists;
# the entity dup probe strips them from capitalized-word candidates.
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
SERIES_RE = re.compile(r"\b[A-Za-z]+[0-9]*-\d{2,6}(?:-\d{2,7})?\b")   # AV26-797, CVE-2026-1234, Storm-0324
# Vendor advisory ids proper (AV26-905) — CVE ids match SERIES_RE too, so the
# catch-all guard below keys on the AV prefix specifically.
AV_CODE_RE = re.compile(r"\bAV\d{2}-\d+\b", re.I)
# "Patches 13 Vulnerabilities" catch-all shape: a roundup headline counting
# vulns. Focused single-advisory disclosures must never absorb into one.
CATCHALL_RE = re.compile(r"\bpatches?\b.{0,20}\b\d+\s+vulnerabilit", re.I)

# URL params that carry feed/campaign tracking, never article identity.
TRACKING_PARAM_RE = re.compile(
    r"(?:utm_[a-z]+|fbclid|gclid|igshid|si|mc_[a-z]+|cmpid|ref|referrer)", re.I)


def norm_url(url):
    """Canonical form for same-article identity. Feed republishing mutates
    URLs (scheme, www., ?utm_source=Mastodon, fragments, trailing slash) and
    the raw-lowercase URL cache missed every variant — 2026-09-16: three
    Oracle CPU events linked cspusep2026.html through utm/proxy variants and
    the 100-point URL identity never fired. Scheme+www lowered, path case
    preserved, tracking params and fragments dropped, trailing slash gone.
    Shared identity key for the story URL cache; never used for display."""
    if not url:
        return ""
    u = url.strip()
    u = re.sub(r"^[a-z][a-z0-9+.-]*://", "", u, flags=re.I)      # scheme
    host, _, path = u.partition("/")
    host = re.sub(r"^www\.", "", host.lower())
    path = path.split("#", 1)[0]
    if "?" in path:
        base, q = path.split("?", 1)
        keep = [p for p in q.split("&")
                if p and not TRACKING_PARAM_RE.fullmatch(p.split("=", 1)[0])]
        path = base + ("?" + "&".join(keep) if keep else "")
    return (host + "/" + path).rstrip("/") or host

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


MONTH_PERIOD_RE = re.compile(
    r"\b(january|february|april|june|july|august|september|october|november|"
    r"december|q[1-4]|h1|h2|week[- ]?\d+)\b", re.I)
WEEK_N_RE = re.compile(r"week[- ]?(\d+)", re.I)


def period_tokens(title):
    """Report-period tokens in a title: month names, quarters, halves, and
    explicit week-N markers. 'march' and 'may' are excluded — verb-ambiguous
    ('the march of ransomware', 'actors may abuse') would misfire."""
    return {m.group(0).lower() for m in MONTH_PERIOD_RE.finditer(title or "")}


def distinct_periods(a, b):
    """Both titles name a report period and none are shared -> different
    installments of the same recurring series (ASEC monthly reports, DFIR
    week-N series), never one story.

    2026-10-03 (2nd day): title_discriminators strips month tokens, so
    'ASEC ... July 2026' vs 'ASEC ... August 2026' scored jaccard 1.0 and the
    duplicate-suspects probe flagged the pair; the auditor dismissed it as a
    month-token artifact both days. Period tokens are the exception to that
    stripping: when present on BOTH sides they discriminate, exactly like
    distinct_series_codes.

    Week numbers discriminate even when the coarser period is shared
    (2026-10-17 owner decision 84991a8ec82c): 'Ransom & Dark Web Week 3,
    October 2026' vs '... Week 2, October 2026' share 'october', so the
    set-disjoint test above passes them — but different week numbers of one
    recurring series are different installments, never one story."""
    pa, pb = period_tokens(a), period_tokens(b)
    if pa and pb and not (pa & pb):
        return True
    wa = {m.group(1) for m in WEEK_N_RE.finditer(a or "")}
    wb = {m.group(1) for m in WEEK_N_RE.finditer(b or "")}
    return bool(wa and wb and not (wa & wb))


# ── entity-based duplicate probe + score-0 backlog sweep (2026-10-20 owner
# decision eda9f1100d5d, audit Issue 3 / Recs 2 & 3). The title-jaccard probe
# (audit_checks.duplicate_suspects, floor 0.5) cannot see reworded headlines:
# the live residual pairs OpenCode (jaccard 0.17–0.25), AOMEI, Ahold Delhaize
# and NightmareStresser are real duplicates it misses. entity_dup_suspects
# surfaces them REPORT-ONLY for the daily adjudication; sweep_score0_merges
# drains the score-0.0 backlog (Trezor / BambooToken / NightmareStresser)
# through the same mechanical merge path repair_dedupe uses. Neither runs in
# the hourly pipeline.

# Entity candidates come in two strengths. STRONG: internal-capital compounds
# and acronyms (NightmareStresser, BambooToken, AOMEI, API) — real incident
# identity in any headline case — plus every capitalized word in a
# SENTENCE-CASE headline, where capitalization marks proper nouns only
# ("Ahold Delhaize discloses...", "Trezor: 347,000 users targeted...").
# LOOSE: every capitalized word — title-case headlines ("Ahold Delhaize
# Pulls E-Commerce Systems Offline...") capitalize phrasing too, so their
# plain-capitalized words are phrasing, not entities. A pair shares an entity
# only on a word that is capitalized on BOTH sides and STRONG on at least
# one: the Ahold pair matches on the sentence-case side's proper nouns, while
# two title-case headlines sharing only "Authentication Bypass" never match.
_ENTITY_WORD_RE = re.compile(r"[A-Za-z0-9]+")

# Day ordinals that differ across both titles ("October 5th" vs "7th",
# "week ending October 18th" vs "11th") mark different installments of a
# recurring series — the daily-podcast/weekly-newsletter class the auditor
# keeps dismissing. Probe-local twin of merge.distinct_periods' logic, which
# only sees month/week tokens and not day-of-month ones.
_DAY_ORDINAL_RE = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)\b", re.I)

# Acronyms/words that survive the capitalization rules but are metric,
# protocol, technique or ecosystem vocabulary — never incident identity.
# 'Eclipse Jetty: 82 CVEs, 92% unpatched' would otherwise pair unrelated
# advisories on 'cves'; two stories sharing only 'Linux' (or 'Google') are
# two different stories. Products (NightmareStresser, AOMEI, Drupal) and
# victims (Ahold Delhaize) stay.
ENTITY_BOILERPLATE = frozenset("""
    cve cves cvss kev ioc iocs poc rce ddos dos tls ssl vpn mfa llm ssh av
    linux windows android apple google microsoft macos ios
    group post blog info full supply chain
""".split())


def _entity_tokens(title, extra_stop=frozenset()):
    """(strong, loose) entity candidate sets for a headline (entity dup probe).

    Capitalized words of the ORIGINAL title (len >= 3, hyphen-adjacent
    fragments excluded — same shape rule as audit_checks._distinctive_entities),
    lowercased, boilerplate-stripped (STOP/CYBER_STOP/GENERIC/DATE_STOP/
    FILLER + ENTITY_BOILERPLATE + the caller's `extra_stop`, the probe's
    SUSPECT_GENERIC). See the strength comments above `_ENTITY_WORD_RE`.

    Unlike tokens() there is NO length-4 floor: 'API' survives, and that
    shared token is what lifts the reworded OpenCode pair ('...API keys...'
    vs 'API Key Breach Response Guidance') to the 2-distinctive-token bar."""
    strong, loose = set(), set()
    t = title or ""
    stop = (BR_STOP | BR_CYBER_STOP | GENERIC | DATE_STOP | FILLER
            | ENTITY_BOILERPLATE | extra_stop)
    words = _ENTITY_WORD_RE.findall(t)
    alpha = [w for w in words if w.isalpha() and len(w) >= 3]
    sentence_case = bool(alpha) and (
        sum(1 for w in alpha if w[0].isupper()) / len(alpha)) <= 0.5
    for m in _ENTITY_WORD_RE.finditer(t):
        w = m.group(0)
        if len(w) < 3:
            continue
        s, e = m.span()
        if (s > 0 and t[s - 1] == "-") or (e < len(t) and t[e] == "-"):
            continue                     # hyphen-compound fragment: phrasing
        if not w[0].isupper():
            continue
        lw = w.lower()
        if lw in stop:
            continue
        loose.add(lw)
        if (w[0].isupper() and any(c.isupper() for c in w[1:])) or w.isupper() \
                or sentence_case:
            strong.add(lw)
    return strong, loose


def entity_dup_suspects(stories, now, *, exclude=None, max_out=10,
                        max_age_days=45, window_days=10):
    """Entity-based near-duplicate LIVE story pairs, REPORT-ONLY (2026-10-20
    owner decision eda9f1100d5d, audit Issue 3 / Rec 2): the pairs the
    title-jaccard probe (duplicate_suspects, floor 0.5) cannot see because the
    headlines were reworded past it. It NEVER merges anything.

    A pair surfaces only when ALL hold (the audit's Rec 2 predicate):
      - both stories LIVE (not merged_into, have events) and recently active
        (last_seen within max_age_days — the duplicate_suspects pool),
      - they share a victim/actor entity: a named entity both headlines
        capitalize (_entity_tokens) or a known threat-actor token
        (ACTOR_TOKENS, leading-'the' normalized),
      - >= 2 shared DISTINCTIVE title tokens — non-generic (the same
        SUSPECT_GENERIC strip duplicate_suspects applies), counting
        discriminator tokens AND shared named entities (tokens() drops
        sub-4-char words like 'api', so the entity set is what lets the
        reworded OpenCode pair reach the bar),
      - first_seen within `window_days` of each other (the audit's ~10 days),
      - NOT distinct CVE sets: both empty or intersecting. Pairs where BOTH
        sides carry disjoint CVE sets are different disclosures, exonerated;
      - distinct advisory/series codes or disjoint report periods exonerate
        (the same recurring-series guards duplicate_suspects applies).

    `exclude` is the set of already-surfaced pair keys (frozenset of the two
    story ids) — audit.py passes the title probe's output so the adjudication
    section shows each pair once. Shared-event pairs keep surfacing via
    duplicate_suspects exactly as today."""
    from audit_checks import SUSPECT_GENERIC   # lazy: audit_checks imports merge
    generic_stop = GENERIC | SUSPECT_GENERIC
    cutoff = (now - timedelta(days=max_age_days)).strftime("%Y-%m-%dT%H:%M:%S")
    pool = sorted((s for s in stories.values()
                   if not s.get("merged_into") and s.get("events")
                   and s.get("last_seen", "") >= cutoff),
                  key=lambda s: s["id"])
    titles = [s.get("title", "") for s in pool]
    disc = [title_discriminators(t) for t in titles]
    ents = [_entity_tokens(t, generic_stop) for t in titles]
    strong = [e[0] for e in ents]
    loose = [e[1] for e in ents]
    story_cves = [{str(c).upper() for c in (s.get("cves") or [])}
                  for s in pool]
    out = []
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            if exclude and frozenset((pool[i]["id"], pool[j]["id"])) in exclude:
                continue
            actor = ((_actor_norm(disc[i]) & ACTOR_TOKENS)
                     & (_actor_norm(disc[j]) & ACTOR_TOKENS))
            # shared victim/actor entity: capitalized on BOTH sides, strong
            # (acronym/compound or sentence-case proper noun) on at least one
            shared_ent = ((strong[i] & loose[j]) | (loose[i] & strong[j]))
            shared_ent = (shared_ent | actor)
            if not shared_ent:
                continue
            oi = set(_DAY_ORDINAL_RE.findall(titles[i]))
            oj = set(_DAY_ORDINAL_RE.findall(titles[j]))
            if oi and oj and not (oi & oj):
                continue              # recurring series, different installments
            shared_tok = (disc[i] & disc[j]) - SUSPECT_GENERIC
            distinctive = shared_tok | shared_ent
            if len(distinctive) < 2:
                continue
            ci, cj = story_cves[i], story_cves[j]
            if ci and cj and not (ci & cj):
                continue              # both sides carry disjoint CVE sets
            ta, tb = titles[i], titles[j]
            if distinct_series_codes(ta, tb) or distinct_periods(ta, tb):
                continue
            try:
                gap = abs((parse_utc(pool[i]["first_seen"])
                           - parse_utc(pool[j]["first_seen"])).days)
            except (KeyError, ValueError, TypeError):
                continue
            if gap > window_days:
                continue
            inter = len(disc[i] & disc[j])
            jj = inter / len(disc[i] | disc[j]) if (disc[i] | disc[j]) else 0.0
            newest = max(pool[i]["first_seen"], pool[j]["first_seen"])
            out.append({"a": pool[i]["id"], "b": pool[j]["id"],
                        "jaccard": round(jj, 2),
                        "title_a": ta[:70], "title_b": tb[:70],
                        "shared_entities": sorted(shared_ent),
                        "shared_tokens": len(shared_tok),
                        "first_seen_gap_days": gap,
                        "newest_first_seen": newest})
    # Newest pair first: the probe exists to catch reworded duplicates BEFORE
    # the digest links them, so today's pairs outrank the deep backlog (which
    # the score-0 sweep and the daily merge budget drain over time). Entity
    # count breaks ties (stronger identity anchor first), then jaccard.
    out.sort(key=lambda x: (x["newest_first_seen"],
                            -len(x["shared_entities"]),
                            -x["jaccard"], x["a"], x["b"]), reverse=True)
    return out[:max_out]


# ── score-0 duplicate backlog sweep (2026-10-20 owner decision eda9f1100d5d,
# audit Rec 3). Trezor (3 live stories), BambooToken (3) and NightmareStresser
# (2) are all score 0.0, flagged by the probe on consecutive days, never
# merged because the human 2-merge/day budget goes to visible pairs. The
# sweep auto-merges ONLY predicate-meeting pairs, is capped per invocation
# and idempotent; the daily audit invokes it before adjudication. The hourly
# pipeline NEVER does.
SCORE0_SWEEP_CAP = 10
SCORE0_SWEEP_MAX_AGE_DAYS = 45

# Digest-reference scan: markdown slate links (](stories/<slug>/)) in the
# published .md, plus the .json sidecars' `stories` (the linked slate) and
# `overrides[].slug` (the digest agent's promote/demote edits). Anything the
# digest machinery ever touched is off-limits to an unattended merge.
DIGEST_LINK_RE = re.compile(r"stories/([a-z0-9-]+)/")


def digest_referenced_slugs(digest_dir=None):
    """Every story slug any published digest references (md links + json
    slate/overrides). Missing/corrupt sidecars contribute nothing."""
    digest_dir = digest_dir or os.path.join(DATA, "digests")
    out = set()
    for f in glob.glob(os.path.join(digest_dir, "*.md")):
        try:
            with open(f) as fh:
                out |= set(DIGEST_LINK_RE.findall(fh.read()))
        except OSError:
            continue
    for f in glob.glob(os.path.join(digest_dir, "*.json")):
        d = _load_json_or_default(f, {})
        if not isinstance(d, dict):
            continue
        out |= {str(x) for x in d.get("stories", []) if isinstance(x, str)}
        out |= {str(o["slug"]) for o in d.get("overrides", [])
                if isinstance(o, dict) and o.get("slug")}
    return out


def load_sweep_exclusions(path=None):
    """Pair exclusions the unattended score-0 sweep must honor (set of
    frozenset slugs).

    Committed code-side (engine/sweep_exclusions.json), so it survives data
    churn: each entry is a pair a daily audit DISMISSED — e.g. the DDoSia
    witha.name host-list releases are successive installments of one actor
    feed, not one story. Without this, an unattended sweep re-litigates the
    auditor's adjudication and merges what a human rejected three times.
    The audit followup appends on each new dismissal, so dismissals become
    durable automatically. Missing/corrupt file = no exclusions.
    """
    path = path or os.path.join(ENGINE, "sweep_exclusions.json")
    raw = _load_json_or_default(path, [])
    out = set()
    for x in raw if isinstance(raw, list) else []:
        if isinstance(x, dict) and x.get("a") and x.get("b"):
            out.add(frozenset((str(x["a"]), str(x["b"]))))
    return out


def score0_sweep_candidates(stories, *, analysis_dir=None, digest_dir=None,
                            max_age_days=SCORE0_SWEEP_MAX_AGE_DAYS, now=None,
                            exclusions=None):
    """Score-0.0 duplicate pairs meeting EVERY sweep predicate, merge-ready.

    Pool: LIVE stories (not merged_into, have events) whose current score is
    0.0 and whose last_seen is recent (bounded scan, same 45-day window as
    duplicate_suspects). A pair is a candidate only when title jaccard >= 0.5,
    NEITHER side has an analysis file (data/analysis/<id>.md), NEITHER is
    referenced by any published digest (see digest_referenced_slugs), the CVE
    sets are not distinct (both empty or intersecting), BOTH sides share a
    victim/actor entity anchor (the entity probe's strong/loose token sets or
    a known actor token — without it, unrelated victims collide on
    boilerplate at exactly the 0.5 floor: the DDoSia host-list releases,
    Adapthealth-vs-Ampath), the recurring-series guards (distinct series
    codes / report periods / slug advisory ids) do not fire, and >= 2 shared
    distinctive (non-generic) tokens overlap. Returns [{a, b, jaccard}]
    sorted by (-jaccard, a, b).
    """
    from audit_checks import SUSPECT_GENERIC   # lazy: audit_checks imports merge
    now = now or datetime.now(timezone.utc)
    if exclusions is None:
        exclusions = load_sweep_exclusions()
    cutoff = (now - timedelta(days=max_age_days)).strftime("%Y-%m-%dT%H:%M:%S")
    analysis_dir = analysis_dir or ANALYSIS_DIR
    referenced = digest_referenced_slugs(digest_dir)
    pool = []
    for s in stories.values():
        if s.get("merged_into") or not s.get("events"):
            continue
        if float(s.get("score") or 0.0) != 0.0:
            continue
        if s.get("last_seen", "") < cutoff:
            continue
        if s["id"] in referenced:
            continue
        if os.path.exists(os.path.join(analysis_dir, s["id"] + ".md")):
            continue
        pool.append(s)
    pool.sort(key=lambda s: s["id"])
    titles = [s.get("title", "") for s in pool]
    disc = [title_discriminators(t) for t in titles]
    ents = [_entity_tokens(t, GENERIC | SUSPECT_GENERIC) for t in titles]
    cves = [{str(c).upper() for c in (s.get("cves") or [])} for s in pool]
    out = []
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            inter = len(disc[i] & disc[j])
            union = len(disc[i] | disc[j])
            jj = inter / union if union else 0.0
            if jj < 0.5:
                continue
            if not ((ents[i][0] & ents[j][1]) or (ents[i][1] & ents[j][0])) \
                    and not ((_actor_norm(disc[i]) & ACTOR_TOKENS)
                             & (_actor_norm(disc[j]) & ACTOR_TOKENS)):
                continue              # no shared victim/actor entity anchor
            if (cves[i] | cves[j]) and not (cves[i] & cves[j]):
                continue              # distinct CVE sets: different disclosures
            ta, tb = titles[i], titles[j]
            if distinct_series_codes(ta, tb) or distinct_periods(ta, tb) \
                    or distinct_advisory_ids(pool[i]["id"], pool[j]["id"]):
                continue
            if len((disc[i] & disc[j]) - SUSPECT_GENERIC) < 2:
                continue              # boilerplate-only overlap, no real signal
            if frozenset((pool[i]["id"], pool[j]["id"])) in exclusions:
                continue              # audit-dismissed pair (sweep_exclusions)
            out.append({"a": pool[i]["id"], "b": pool[j]["id"],
                        "jaccard": round(jj, 2)})
    out.sort(key=lambda x: (-x["jaccard"], x["a"], x["b"]))
    return out


def sweep_score0_merges(stories, events=None, *, stories_dir=None,
                        analysis_dir=None, digest_dir=None,
                        cap=SCORE0_SWEEP_CAP, reddit_posts=None,
                        now=None, log=None, exclusions=None):
    """Unattended, bounded, idempotent merge sweep for the score-0 duplicate
    backlog (2026-10-20 owner decision eda9f1100d5d, audit Rec 3). Merges at
    most `cap` candidate pairs (see score0_sweep_candidates) via the SAME
    mechanical path repair_dedupe/triage use: the loser keeps its json with
    merged_into + empty events so the old URL redirects, the winner absorbs
    the events, then the derived-fields sweep (last_seen/cves/sources rolled
    onto the current event set) and a rescore run on the winners. needs-
    analysis is NOT re-emitted here — the next hourly run re-queues any
    winner that crossed the analysis gate. Idempotent: merged shells drop out
    of the candidate pool, so an immediate second run merges nothing.
    Returns the merge log (one line per merge)."""
    from repair_dedupe import canon, merge_story, recompute_derived_fields
    log = log if log is not None else []
    events = load_events() if events is None else events
    stories_dir = stories_dir or STORIES
    candidates = score0_sweep_candidates(
        stories, analysis_dir=analysis_dir, digest_dir=digest_dir, now=now,
        exclusions=exclusions)
    for c in candidates:
        if len(log) >= cap:
            break
        a, b = stories.get(c["a"]), stories.get(c["b"])
        if not a or not b:
            continue
        if a.get("merged_into") or b.get("merged_into"):
            continue                  # already merged earlier in this sweep
        ca = {str(x).upper() for x in (a.get("cves") or [])}
        cb = {str(x).upper() for x in (b.get("cves") or [])}
        if (ca | cb) and not (ca & cb):
            continue                  # winner absorbed CVEs mid-sweep
        group = canon([a, b])
        loser = b if group["id"] == a["id"] else a
        merge_story(stories, loser["id"], group["id"], log)
    merged_ids = set()
    for line in log:
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "merge":
            merged_ids.update((parts[1], parts[3]))
    if not merged_ids:
        return log
    recomputed = recompute_derived_fields(stories, events, only=merged_ids)
    if recomputed:
        log.append(f"derived fields recomputed on {recomputed} swept stories")
    if reddit_posts is None:
        from store import load_social_posts
        reddit_posts = load_social_posts()
    for sid in sorted(merged_ids):
        s = stories[sid]
        try:
            json.dump(s, open(os.path.join(stories_dir, sid + ".json"), "w"),
                      indent=1)
            if s.get("merged_into"):
                continue              # shell: redirect json only
            sc = hot_score(s, events, reddit_posts)
            s["score"] = sc["score"]
            s["score_breakdown"] = {k: v for k, v in sc.items() if k != "score"}
        except Exception as e:
            # One story's scoring failure must not wipe a valid breakdown or
            # write an empty one (same fallback as the hourly merge).
            print(f"  WARN: score {sid}: {e}")
            s.setdefault("score", 0.0)
        backfill_score_breakdown(s)
        s.setdefault("score", 0.0)
        json.dump(s, open(os.path.join(stories_dir, sid + ".json"), "w"),
                  indent=1)
    return log


def _advisory_id_codes(story_id):
    """Series codes carried by a story id/slug, but only when the code's
    prefix itself contains a digit (av26-891, cve-2024-37079). A bare slug
    index suffix (foo-5000) is NOT an advisory: its prefix is letters only,
    so genuine same-base duplicates still merge."""
    out = set()
    for m in SERIES_RE.finditer(story_id or ""):
        code = m.group(0).upper()
        if any(ch.isdigit() for ch in code.rsplit("-", 1)[0]):
            out.add(code)
    return out


def distinct_advisory_ids(a_id, b_id):
    """Both story ids carry an advisory-series code and none are shared ->
    different advisories, never duplicates. Catches the JetBrains
    av26-891 / av26-825 false positive, where the advisory number lives only
    in the slug and one of the two titles omits it entirely, so the title
    guard (distinct_series_codes) cannot see it."""
    ca, cb = _advisory_id_codes(a_id), _advisory_id_codes(b_id)
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
    nu = norm_url(ev["url"])
    if nu and nu in story_url_cache.get(story["id"], set()):
        return 100.0
    ev_title_cves = {c.upper() for c in CVE_RE.findall(ev["title"])}
    # metadata CVEs (ingest/backfill) stand in only when the title names none
    ev_cves = ev_title_cves or {c.upper() for c in (ev.get("cves") or [])}
    if ev_cves and story.get("cves") and len(ev_cves) <= 2:
        # story cves are a DERIVED union and can carry a CVE from an event
        # that was since reassigned (2026-09-16: the N-central July story
        # held 86218). Disjoint advisory codes in the titles block even CVE
        # overlap, same as the title path below.
        ev_codes = _series_codes(ev["title"])
        st_codes = _series_codes(story.get("title", ""))
        if not (ev_codes and st_codes and not (ev_codes & st_codes)):
            if ev_cves & set(story["cves"]):
                return 50.0
    # Advisory-code catch-all guard (2026-10-17 owner decision 584241d6a901):
    # a focused single-advisory disclosure (exactly one AV id, CVEs disjoint
    # from the story's) never absorbs into a "patches N vulnerabilities"
    # catch-all — the PAN-OS AV26-905/CVE-2026-0310 story must not merge into
    # the CVE-2026-0322 catch-all. Genuine multi-advisory roundups (several
    # AV ids, or CVEs overlapping the story's) still merge, as does a
    # same-CVE focused event (handled by the 50.0 path above).
    ev_av = {m.group(0).upper() for m in AV_CODE_RE.finditer(ev["title"])}
    if len(ev_av) == 1 and CATCHALL_RE.search(story.get("title", "")):
        st_av = ({m.group(0).upper()
                  for m in AV_CODE_RE.finditer(story.get("title", ""))}
                 | _advisory_id_codes(story.get("id", "")))
        if not (ev_av & st_av) and not (ev_cves & set(story.get("cves") or [])):
            return 0.0
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


def emit_needs(stories, exclude=None):
    """Analysis-queue emit. `exclude` is the frozen set: a cold-tier story
    never queues analysis work (its peak never crossed the bar anyway, but
    the explicit filter keeps the freeze contract local and testable)."""
    exclude = exclude or set()
    queue = []
    for s in stories.values():
        if s["id"] in exclude:
            continue
        if s["score"] < HOT_THRESHOLD:
            continue
        # 2026-09-25: a story that failed the analysis gate MAX times carries
        # a .capped marker — requeuing it hourly just burns an agent run on a
        # structurally unpassable analysis (a no-CVE research story under the
        # old grounding rule thrashed 10+ times). Flagged for drop review.
        if os.path.exists(os.path.join(ANALYSIS_DIR, ".rejects",
                                       s["id"] + ".capped")):
            continue
        analysis_path = os.path.join(ANALYSIS_DIR, s["id"] + ".md")
        # 2026-10-02: a quarantined analysis must not requeue on every new
        # event for the same story (the zammad story burned an agent run per
        # hour for 7 hours: new X posts kept arriving, each re-queued a
        # structurally unpassable analysis). Retry only when genuinely new
        # material arrived AFTER the last rejection.
        prior_rejects = glob.glob(os.path.join(ANALYSIS_DIR, ".rejects",
                                               s["id"] + "-*.md"))
        if prior_rejects and not os.path.exists(analysis_path):
            newest_evt = max((events.get(ref["event_id"])["published_at"]
                              for ref in s.get("events", [])
                              if ref["event_id"] in events), default="")
            last_reject = max(os.path.getmtime(r) for r in prior_rejects)
            newest_dt = parse_utc(newest_evt) if newest_evt else None
            if not newest_dt or newest_dt.timestamp() <= last_reject:
                continue
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


def _load_pending():
    """Parked social events: [{id, since}]. Missing/corrupt file -> empty
    (they just stop retrying; the events stay on disk for triage)."""
    if not os.path.exists(PENDING):
        return []
    return _load_json_or_default(PENDING, [])


def _save_pending(pending):
    json.dump(pending, open(PENDING, "w"), indent=1)


def _iso(s):
    return datetime.fromisoformat((s or "").replace("Z", "+00:00"))


def _social_revive_blocked(ev, s):
    """True when a social event would mechanically revive a story that was
    already cold when the post was published. Social amplifies active
    coverage; it does not resurrect archived stories (2026-09-27: a single
    tweet re-sharing Rapid7's May analysis bumped the 130-day-cold Cisco
    SD-WAN story to score 8.7 and onto the digest slate as fresh). The gap
    is measured from the story's newest NON-social event; editorial triage
    keeps bypass this via apply()'s own attach path."""
    if not str(ev.get("id", "")).startswith(SOCIAL_PREFIXES):
        return False
    gap = int(os.environ.get("TIA_SOCIAL_REVIVE_GAP_DAYS", "3"))
    newest_feed = ""
    for r in s.get("events", []):
        e = (events or {}).get(r["event_id"])
        if e and not str(e.get("id", "")).startswith(SOCIAL_PREFIXES):
            newest_feed = max(newest_feed, e.get("published_at", ""))
    if not newest_feed:
        return False          # no feed coverage yet — nothing to revive from
    try:
        cold = (_iso(ev["published_at"]) - _iso(newest_feed)).days
    except (KeyError, ValueError):
        return False
    return cold > gap


def event_owner(stories, eid, exclude=None):
    """The ACTIVE story already referencing event id `eid` (other than
    `exclude`), or None. The write-time double-reference guard (2026-10-13
    owner decision 3937e99cf1aa): the merge/backfill writers used to append a
    ref after checking only the TARGET story, so a stale queue entry or a
    sidecar URL collision could put one event into two active stories — the
    dedup_invariants multi-ref class repair_dedupe cleans up after the fact.
    Merged-away shells are not active owners (their refs belong to the
    canonical story); repair_dedupe stays the historical cleanup path."""
    for sid, s in stories.items():
        if sid == exclude or s.get("merged_into"):
            continue
        if any(r.get("event_id") == eid for r in s.get("events", [])):
            return sid
    return None


# ── story-title hygiene (2026-10-18 owner decision 6cb97b2fc92b, audit
# Issue 3 / Rec 5). A story's title was pinned to the FOUNDING event's raw
# headline, so `we-ve-just-released-freerdp-3-32-0-…` rendered — on the story
# page AND its CTI case page — as "We've just released # FreeRDP 3.32.0 …
# Check it out at https:// fre" while the story's newer threataft.com event
# carried a clean, specific title. Raw debris never renders as a story title
# when a clean candidate exists.
TITLE_URL_DEBRIS_RE = re.compile(r"https?://\s*\S*")        # URL / cut-off URL
TITLE_HASHTAG_DEBRIS_RE = re.compile(r"(?<![A-Za-z0-9])#\s*(?=\w)")
# clean_title's emoji strip can leave zero-width residue behind: the
# FreeRDP toot's "\U0001F5A5\uFE0F" is a pictograph + U+FE0F and only the
# pictograph matches EMOJI_RE. A published title must not start with an
# invisible variation selector.
TITLE_ZW_RESIDUE = "\ufe0f\u200b\u200c\u200d\u2060\ufeff"


def strip_title_debris(title):
    """Remove raw toot/aggregator debris from a headline: `#` hashtag MARKERS
    (the word stays — dropping it mangles the headline, "a huge # feature"
    must not become "a huge") and `https://` fragments, including the
    truncated `https:// fre` shape a cut-off toot leaves."""
    t = TITLE_URL_DEBRIS_RE.sub("", title or "")
    t = TITLE_HASHTAG_DEBRIS_RE.sub("", t)
    return re.sub(r"\s+", " ", t).strip()


def _display_title(title):
    """A story title fit to publish: emoji/marker-stripped, debris-stripped,
    no leading/trailing zero-width residue."""
    return clean_title(strip_title_debris(title)).strip(TITLE_ZW_RESIDUE).strip()


def _raw_title(title):
    """True when a headline carries raw toot/aggregator debris (a hashtag
    marker or a URL / truncated-URL fragment) — see strip_title_debris."""
    t = title or ""
    return bool(TITLE_URL_DEBRIS_RE.search(t)
                or TITLE_HASHTAG_DEBRIS_RE.search(t))


def preferred_title(story, events_by_id=None):
    """The story's display title after an event attaches, or None to keep it.

    Deterministic rule (2026-10-18 owner decision 6cb97b2fc92b, audit Issue 3 /
    Rec 5): a CLEAN story title — including triage's analyst-set
    `story_title` — is never touched. When the story title is a raw founding
    toot/aggregator headline, prefer the newest clean event title, non-social
    routes first (an outlet's clean headline beats a social repost of it); if
    no event has a clean title, strip the raw debris so it never renders.
    """
    if events_by_id is None:
        events_by_id = globals().get("events") or {}
    cur = (story.get("title") or "").strip()
    if not cur or not _raw_title(cur):
        return None
    cands = [events_by_id[r["event_id"]]
             for r in story.get("events", [])
             if r.get("event_id") in events_by_id
             and (events_by_id[r["event_id"]].get("title") or "").strip()]
    cands.sort(key=lambda e: e.get("published_at") or "", reverse=True)
    for e in cands:                       # newest non-social clean title
        if not str(e.get("id", "")).startswith(SOCIAL_PREFIXES) \
                and not _raw_title(e.get("title")):
            return _display_title(e["title"])
    for e in cands:                       # then any route's clean title
        if not _raw_title(e.get("title")):
            return _display_title(e["title"])
    t = _display_title(cur)
    return t if t and t != cur else None


def heal_raw_titles(stories, events_by_id=None, stories_dir=None, cti_dir=None):
    """Retroactive title heal for stories that predate the attach-time rule
    (2026-10-19 owner decision ad4c5d039830, completing 6cb97b2fc92b): the
    2026-10-18 title rule ran ONLY inside _attach_event, so a story that
    received no new event after it landed (e.g. the Chrome 153 story, newest
    event 2026-10-18T02:19Z, before the 14:40Z merge) kept its raw founding
    toot headline forever — the audit's 236 live debris titles on 10-19.

    `preferred_title` is applied to EVERY live story here, not only at attach
    time (a clean or analyst-set title returns None and is never touched),
    and the healed title is written back to the story json. For a story that
    has a CTI record, a record title that is itself raw debris is healed to
    the story's title: the CTI case page renders the record title verbatim,
    so leaving it would keep the debris published. Returns
    (stories_healed, cti_records_healed); pure except for the file writes.
    """
    if events_by_id is None:
        events_by_id = globals().get("events") or {}
    stories_dir = stories_dir or STORIES
    if cti_dir is None:
        cti_dir = CTI_DIR
    healed = cti_healed = 0
    for s in stories.values():
        if s.get("merged_into"):
            continue               # redirect shells render nothing to heal
        t = preferred_title(s, events_by_id)
        if t:
            s["title"] = t
            json.dump(s, open(os.path.join(stories_dir, s["id"] + ".json"), "w"),
                      indent=1)
            healed += 1
        p = os.path.join(cti_dir, s["id"] + ".json")
        if not os.path.exists(p):
            continue
        try:
            r = json.load(open(p))
        except (json.JSONDecodeError, ValueError, OSError):
            continue
        if _raw_title(r.get("title")):
            r["title"] = s["title"]
            json.dump(r, open(p, "w"), indent=1)
            cti_healed += 1
    return healed, cti_healed


def _attach_event(eid, ev, s, stories=None):
    """Merge an event into an existing story as an update. Shared by the
    new-event queue and the social-pending replay (identical semantics:
    never touch kind of an already-placed event). Returns False when the
    event was already in the story, is a cold-story social revival, or —
    when `stories` is passed (the hourly does) — another ACTIVE story
    already references it (write-time double-reference guard)."""
    refs = [r["event_id"] for r in s["events"]]
    if eid in refs:                      # already processed — never touch kind
        return False
    if stories is not None:
        owner = event_owner(stories, eid, exclude=s["id"])
        if owner:
            print(f"  WARN: attach rejected: {eid} already referenced by "
                  f"story {owner} (double-reference guard)")
            return False
    if _social_revive_blocked(ev, s):
        return False
    ev["kind"] = "update"
    s["events"].append({"event_id": eid, "label": "update"})
    if ev["published_at"] > s.get("last_seen", ""):
        s["last_seen"] = ev["published_at"]
    # Unverified low-trust events attach (amplify) but never credit their
    # domain as a story source; verified provenance credits the primary.
    if ev.get("low_trust") and not ev.get("provenance"):
        domains = []
    else:
        domains = [domain_of(ev["url"])] if ev["url"] else []
    s["sources"] = list(dict.fromkeys(s.get("sources", []) + [d for d in domains if d]))
    s["n_sources"] = len(s["sources"])
    s["cves"] = sorted(set(s.get("cves", [])) | set(ev["cves"]))
    s["first_seen"] = min(s.get("first_seen", ev["published_at"]), ev["published_at"])
    if ev["url"]:
        story_url_cache.setdefault(s["id"], set()).add(norm_url(ev["url"]))
    # Title hygiene (2026-10-18 owner decision 6cb97b2fc92b, audit Issue 3 /
    # Rec 5): the story title was pinned to the FOUNDING event's headline, so
    # `we-ve-just-released-freerdp-3-32-0-…` rendered — on the story page and
    # its CTI case page — as "We've just released # FreeRDP 3.32.0 … Check it
    # out at https:// fre" while a newer event carried a clean title.
    t = preferred_title(s)
    if t:
        s["title"] = t
    return True


def main():
    global events, reddit_posts, story_url_cache
    events = load_events()
    stories = load_stories()
    from store import load_social_posts
    reddit_posts = load_social_posts()
    manifest = (_load_json_or_default(MANIFEST, {"stories_per_day": {}})
                if os.path.exists(MANIFEST) else {"stories_per_day": {}})
    story_url_cache = {sid: story_event_urls(s) for sid, s in stories.items()}
    # Cold tier, loaded once per run: frozen stories are invisible to
    # matching/needs/rescoring below. unfreeze_strong thaws on strong event
    # evidence and writes through to frozen.json, so the local set mirrors it.
    frozen = lifecycle.frozen_ids()

    queue = (_load_json_or_default(QUEUE, {"events": []})
             if os.path.exists(QUEUE) else {"events": []})
    new_ids = queue.get("events", [])
    created = merged = parked = expired = 0
    pending = _load_pending()
    cutoff = (datetime.now(timezone.utc)
              - timedelta(hours=SOCIAL_TTL_H)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Replay parked social events before today's queue (oldest first): attach
    # when a corroborating story now exists, expire them past the TTL. An
    # attach here is exactly the feed-corroboration the mint bar demands.
    still = []
    for p in pending:
        eid = p.get("id")
        ev = events.get(eid)
        if not ev or ev.get("excluded"):
            continue                   # gone, or triage already decided
        if ev.get("published_at", "") < cutoff:
            ev["excluded"] = True
            ev["exclude_reason"] = (f"social: no feed corroboration "
                                    f"within {SOCIAL_TTL_H}h")
            json.dump(ev, open(os.path.join(EVENTS, eid + ".json"), "w"),
                      indent=1)
            expired += 1
            continue
        frozen -= lifecycle.unfreeze_strong(ev, stories)
        target = match_story(ev, stories)
        if target in frozen:
            target = None       # still frozen = weak similarity: park, don't thaw
        if target and _attach_event(eid, ev, stories[target], stories):
            merged += 1
            day = ev["published_at"][:10]
            manifest.setdefault("stories_per_day", {}).setdefault(day, [])
            if target not in manifest["stories_per_day"][day]:
                manifest["stories_per_day"][day].append(target)
            continue
        still.append(p)
    pending = still

    for eid in new_ids:
        ev = events.get(eid)
        if not ev:
            continue
        frozen -= lifecycle.unfreeze_strong(ev, stories)
        target = match_story(ev, stories)
        if target in frozen:
            # unfreeze_strong already ran for THIS event, so a still-frozen
            # target is weak similarity only — never thaw a cold story by
            # accident; fall through to the mint/park logic.
            target = None
        day = ev["published_at"][:10]
        if target:
            if not _attach_event(eid, ev, stories[target], stories):
                continue
            merged += 1
        elif eid.startswith(SOCIAL_PREFIXES):
            # Social amplifies, feeds create: park it instead of minting.
            # The event file is still written so the triage collect window
            # can see it (an explicit LLM keep materializes the story).
            ev.setdefault("kind", "original")
            json.dump(ev, open(os.path.join(EVENTS, eid + ".json"), "w"),
                      indent=1)
            if not any(p.get("id") == eid for p in pending):
                pending.append({"id": eid, "since": ev["published_at"]})
                parked += 1
            continue
        elif ev.get("low_trust") and not ev.get("provenance"):
            # Low-trust feeds amplify, never create (2026-09-27 threadlinqs
            # incident: an AI-drafted repost minted a single-source story the
            # digest headlined as "added to KEV today" 5 days late). Social
            # events already park above; non-social low-trust events stay
            # unattached for the triage window (triage can attach them to an
            # existing story but cannot mint from one either). VERIFIED
            # provenance (primary source confirmed by triage) exempts.
            continue
        else:
            owner = event_owner(stories, eid)
            if owner:
                # write-time guard: the event already lives in an active
                # story (stale queue entry / earlier placement) — never mint
                # a second story around it.
                print(f"  WARN: mint rejected: {eid} already referenced by "
                      f"story {owner} (double-reference guard)")
                continue
            ev["kind"] = "original"
            slug = build_slug(ev["title"], stories)
            s = {"id": slug, "title": _display_title(ev["title"]),
                 "first_seen": ev["published_at"], "last_seen": ev["published_at"],
                 "sources": [domain_of(ev["url"])] if ev["url"] else [],
                 "n_sources": 1 if ev["url"] else 0,
                 "cves": ev["cves"], "score": 0.0,
                 "reddit_signal": {"posts": 0, "best_score": 0},
                 "events": [{"event_id": eid, "label": "original"}]}
            stories[slug] = s
            story_url_cache[slug] = {norm_url(ev["url"])} if ev["url"] else set()
            created += 1
        json.dump(ev, open(os.path.join(EVENTS, eid + ".json"), "w"), indent=1)
        manifest.setdefault("stories_per_day", {}).setdefault(day, [])
        target_slug = target or (next(s for s in stories.values() if s["events"] and s["events"][-1]["event_id"] == eid)["id"])
        if target_slug not in manifest["stories_per_day"][day]:
            manifest["stories_per_day"][day].append(target_slug)

    for s in stories.values():
        if s["id"] in frozen:
            continue    # frozen: score/peak stay as frozen — skips the bulk of hourly CPU
        try:
            sc = real_score(s)
            s["score"] = sc["score"]
            s["score_breakdown"] = {k: v for k, v in sc.items() if k != "score"}
            update_peak(s, sc)
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

    # Retroactive title heal (2026-10-19 owner decision ad4c5d039830):
    # reconcile EVERY live story (and its CTI record title) after scoring, so
    # a story that received no new event since the 2026-10-18 rule landed
    # still heals and no raw toot/aggregator debris renders. Idempotent —
    # preferred_title returns None for an already-clean title.
    _healed, _cti_healed = heal_raw_titles(stories, events)
    if _healed or _cti_healed:
        print(f"title heal: {_healed} stories, {_cti_healed} CTI records")

    _save_pending(pending)
    json.dump(manifest, open(MANIFEST, "w"), indent=1)
    needs = emit_needs(stories, exclude=frozen)
    json.dump({"date": queue.get("date", ""), "events": []}, open(QUEUE, "w"), indent=1)
    print(f"new events: {len(new_ids)} | merged: {merged} | created: {created} "
          f"| social parked: {parked} | social expired: {expired} "
          f"| needs analysis: {needs}")
    print(f"stories total: {len(stories)}")
    # Cold-tier sweep LAST (after persist): anything that never mattered now
    # leaves the paid set — next run's matching/rescoring/rendering skips it.
    lifecycle.freeze_sweep(stories)


def build_slug(title, stories):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:64].rstrip("-")
    if slug in stories:
        slug = slug + "-" + str(len(stories) + 1)
    return slug


if __name__ == "__main__":
    main()
