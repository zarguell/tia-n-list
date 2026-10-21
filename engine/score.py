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

Zero-delta demotion (2026-10-20 owner decision ed6b7366c2ec, audit Rec 1):
when a story's only recent movement is outlet re-reports that add no new
CVE, actor, victim count, or IOC — and it has no genuine development inside
the 48h window — the score is halved and the breakdown says so (`zero_delta`
+ `zero_delta_penalty`). Re-report events already earn no velocity/recency
(2026-10-03); the demotion closes the residual slate ride (a big story's
decayed base still crossed the digest's 3.3 gate with a reddit bump) and
makes the demotion explainable instead of a daily hand-override.
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

KEV_DIR = os.environ.get("TIA_KEV_DIR") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "kevrichment", "data", "cves")
# (was hardcoded /home/coder/workspace/... — a dead path on this host, which
# silently disabled KEV lookup: stories showed kev:false for CVEs CISA listed)

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

# ── high-impact weights (2026-10-13 owner decision fc3f6e00a8d9, audit Rec 2)
# The digest agent's recurring "score under-ranks high-impact" promotes (35
# overrides, 13 since Oct 1) name two classes the proxy lets drift: confirmed
# in-the-wild exploitation and unpatched CVSS >= 9.0 flaws. Both get explicit
# extra weight in severity (outside SIGNAL_CAP so the shared signal bucket
# can't absorb them). CVSS stated in the coverage text counts too: the local
# NVD store misses research CVEs, and the underrank class is exactly that —
# erlang/OTP "CVSS 10" scored sev 1.0 from the store and landed at 2.8.
CVSS_TEXT_RE = re.compile(
    r"cvss(?:\s*v(?:3(?:\.1)?)?)?\s*[: ]?\s*(\d{1,2}(?:\.\d)?)", re.I)
IN_WILD_RE = re.compile(
    r"\b(?:in-the-wild|in the wild|actively exploited|being exploited|"
    r"exploited in the wild|exploitation (?:has been|is being|was) "
    r"(?:observed|confirmed|detected))\b", re.I)
UNPATCHED_RE = re.compile(
    r"\bunpatched\b|\bno (?:patch|fix)(?:es)?\b|"
    r"\b(?:patch|fix)(?:es)? (?:is |are )?not (?:yet )?(?:available|out)\b|"
    r"\bwithout (?:a |an )?(?:patch|fix)\b|"
    r"\b(?:awaiting|pending) (?:a )?(?:patch|fix)\b", re.I)
IMPACT_IN_WILD = 0.4        # weight for confirmed in-the-wild exploitation
IMPACT_UNPATCHED_9 = 0.4    # weight for an unpatched CVSS >= 9.0 flaw

# ── novelty floor for corroborated no-CVE TTP coverage (2026-10-17 owner
# decision f5f2bc09664a, audit Rec 3): the proxy scores every no-CVE story
# at the 0.5 severity floor, so multi-source first-of-kind technique/tool
# coverage (pwn2own results, C2 loaders, signed-driver abuse) ranks WITH
# routine patch-release traction until a digest agent hand-promotes it —
# all three recent wildcards (pwn2own-ireland-2026, fake-lastpass
# authenticator, avisloader) sat at the floor. Corroboration (n_sources
# >= 2) + attacker-TTP vocabulary = genuine novelty, worth half a severity
# step outside the shared signal bucket. Traction-only stories carry no TTP
# terms, so the 2026-08-13 traction contract is untouched.
NOVELTY_TTP_RE = re.compile(
    r"\b(pwn2own|command[\s-]?and[\s-]?control|\bc2\b|loader|stealer|"\
    r"infostealer|dropper|clipper|signed[\s-]?driver|edr[\s-]?"\
    r"(killer|bypass|evasion)|defense evasion|privilege escalation|"\
    r"living[\s-]?off[\s-]?the[\s-]?land)\b", re.I)
NOVELTY_MULTI_SOURCE = 0.5  # severity bonus for corroborated no-CVE novelty

# ── zero-delta repost stubs (2026-10-18 owner decision 6aad368c1a1b, audit
# Rec 1a). `rd:` Reddit link-posts are content-free stubs: 134-138c of
# "submitted by /u/… [link] [comments]" boilerplate wrapped around the
# outlet's headline (the stub's `source` is domain_of(article_url), so a link
# post to a BleepingComputer article was even scored against
# bleepingcomputer.com). They keep landing as the NEWEST event on already
# covered stories — 26/26 of the 2026-10-18 digest demotes, 18/18 the day
# before — and resurfaced those stories on the slate. A repost stub is a
# development ONLY when it carries a new CVE (settled by is_rereport before
# this leg), a new actor attribution, a new victim count, or a new IOC;
# otherwise it scores as ZERO-DELTA: no velocity, no recency, no pickup, no
# novelty, no rank promotion.
REPOST_STUB_RE = re.compile(r"^rd:")
# "victim count" = a number attached to a victim-bearing noun. Same shape as
# SIGNALS' breach-scale rule, widened to the nouns real breach coverage names
# ("2,500+ organizations", "8.8 million records", "4,100 victims").
VICTIM_COUNT_RE = re.compile(
    r"\b\d[\d,.]*\+?\s*(?:million|billion|thousand)?\s*"
    r"(?:records?|accounts?|users?|customers?|patients?|employees?|"
    r"organizations?|organisations?|companies?|victims?|hosts?|devices?|"
    r"members?|subscribers?|people)\b", re.I)

# ── zero-delta demotion (2026-10-20 owner decision ed6b7366c2ec, audit
# Rec 1). The 2026-10-03 re-report leg stopped echoes EARNING velocity and
# recency, but a big story's decayed base still rode the digest slate (the
# hot gate sits at 3.3 and the decaying base + reddit bump crossed it for
# days) — 544 of 657 all-time digest overrides are demotes and the dominant
# reason is still "new events restate covered facts", demoted BY HAND every
# day. So: when the story's only recent movement is outlet re-reports that
# carry no delta (the _repost_delta test — new actor / new victim count /
# new IOC; a new CVE is settled by is_rereport) and there is NO genuine
# development inside the recent window, the score is halved:
# ZERO_DELTA_FACTOR is applied on top of the 36h decay, so a stale echo-only
# story lands at most ~1.5 (its recency is already <= e**(-48/36) ~= 0.26)
# — under the digest's hot gate, under the bench's near-gate flag, and
# visible in the breakdown as zero_delta + zero_delta_penalty instead of a
# daily hand-override.
# Conservative by construction: any genuine development inside the window
# (a non-re-report event — new CVE, new angle, anything is_rereport does
# not flag) leaves the story untouched; a re-report that still carries a
# delta (new actor/victim/IOC) leaves it untouched too; and rd: repost
# stubs stay exactly as pinned by 6aad368c1a1b — neutral plumbing that
# neither gains nor triggers rank (a stub-only story's score is unchanged).
# Founding events are never re-reports, so a story is always at least half
# a window old before this can fire.
VELOCITY_WINDOW_H = 48      # the velocity factor's window == the recent
                            # window the demotion trigger draws from
ZERO_DELTA_FACTOR = 0.5     # keep half the (already decayed) score

# Keys the SSG "Why this score" template renders from a score breakdown.
# A story missing any of these raises a jinja UndefinedError that aborts the
# whole site build, so the store writers (merge / repair_dedupe / triage)
# backfill defensively. recency is a temporal MULTIPLIER, so its neutral
# fallback is 1.0 (no decay), not 0.0 (which would zero the score).
SB_KEYS = ("base", "breadth", "authority", "severity", "velocity",
           "pickup", "recency", "reddit", "kev", "epss", "n_sources")
SB_DEFAULTS = {k: (1.0 if k == "recency" else (False if k == "kev"
             else (0 if k == "n_sources" else 0.0))) for k in SB_KEYS}


def backfill_score_breakdown(story):
    """Guarantee story['score_breakdown'] carries every key the SSG 'Why this
    score' template renders, so a stale or exception-produced breakdown can
    never raise jinja UndefinedError and abort the build. Preserves existing
    values; backfills only missing keys from SB_DEFAULTS."""
    sb = story.get("score_breakdown")
    if not isinstance(sb, dict):
        sb = {}
        story["score_breakdown"] = sb
    for k in SB_KEYS:
        if k not in sb:
            sb[k] = SB_DEFAULTS[k]
    return story


def update_peak(story, sc):
    """High-water mark: the best score a story has ever reached.

    The published score decays with a 36h half-life, so a cooled story is
    indistinguishable from one that never mattered — nothing downstream
    (cold-tier freezing, best-of surfaces, REVISIT picks) can tell them
    apart. peak_score/peak_at are written by every store rescoring path
    (merge + triage apply) and never decrease. Callers pass the hot_score
    dict (or a bare number) on SUCCESS paths only — the exception fallbacks
    that preserve stale breakdowns must not touch the peak either.
    """
    score = float(sc.get("score", 0.0)) if isinstance(sc, dict) else float(sc)
    peak = float(story.get("peak_score") or 0.0)
    if score > peak:
        story["peak_score"] = round(min(10.0, score), 2)
        story["peak_at"] = datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
    elif "peak_score" not in story:
        # First touch on a pre-peak story: stamp the current (decayed) value
        # so the field exists everywhere; backfill_peaks.py raises old peaks.
        story["peak_score"] = round(min(10.0, peak), 2)


def undecayed_score(breakdown):
    """The score a breakdown would produce with recency = 1.0 (no decay).

    score = (breadth + authority + severity + velocity + pickup) * recency
    + community, and the breakdown carries `base` = the parenthesized sum,
    so the undecayed value is base + reddit. Used by the one-off peak
    backfill to give pre-existing stories an honest high-water mark.
    """
    if not isinstance(breakdown, dict):
        return 0.0
    base = breakdown.get("base")
    if base is None:
        base = sum(breakdown.get(k, 0.0) or 0.0 for k in
                   ("breadth", "authority", "severity", "velocity", "pickup"))
    reddit = breakdown.get("reddit") or 0.0
    return round(min(10.0, float(base) + float(reddit)), 2)


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


def _cvss_band(best):
    """Severity band for a CVSS base score (0.5-4.5 of the 0-5 severity
    factor). Factored out of _cvss_severity so hot_score can apply the SAME
    band to a CVSS the coverage text states but the local store lacks
    (2026-10-13 decision fc3f6e00a8d9 — see CVSS_TEXT_RE)."""
    if best >= 9.0:
        return 4.5
    if best >= 7.0:
        return 3.5
    if best >= 4.0:
        return 2.5
    if best > 0:
        return 1.5
    return 1.0            # CVE present but not in the local store


def _cvss_severity(cves):
    """(cvss-band score, kev flag, epss bonus) across the story's CVEs.

    The EPSS bonus comes from the kevrichment records (daily bulk refresh,
    kevrichment/epss.py): +0.4 at exploitation probability >= 0.5, +0.2 at
    >= 0.1 — a CVE the model expects to be exploited any day now is worth
    more attention than its CVSS alone admits. Records without an enriched
    score (not yet refreshed) contribute 0."""
    store = _load_cve_store()
    if not cves:
        return 0.5, False, 0.0
    best = 0.0
    kev = False
    epss = 0.0
    for c in cves:
        info = store.get(c.upper())
        if info:
            best = max(best, info.get("cvss") or 0.0)
            kev = kev or info.get("kev")
            e = info.get("epss")
            if isinstance(e, (int, float)):
                epss = max(epss, e)
    bonus = 0.4 if epss >= 0.5 else (0.2 if epss >= 0.1 else 0.0)
    return _cvss_band(best), kev, bonus


def _victim_counts(text):
    """Normalized victim-count phrases in a text (a set, for delta compare)."""
    return {re.sub(r"\s+", " ", m.group(0).lower().strip())
            for m in VICTIM_COUNT_RE.finditer(text or "")}


def _ioc_values(text):
    """IOC values named in a text (public IPs / hosts / hashes, precision-
    filtered by engine/ioc). Lazy import: score is imported by merge and
    triage, so it must not grow a module-level dependency of its own."""
    if not text:
        return set()
    import ioc
    return set(ioc.extract_from_text(text))


def _actor_tokens(disc):
    """The title's discriminators that name a known threat actor."""
    from merge import ACTOR_TOKENS, _actor_norm
    return _actor_norm(disc) & ACTOR_TOKENS


def _prior_actor_tokens(prior_events):
    """Actor tokens named by the story's prior event titles."""
    from merge import title_discriminators, ACTOR_TOKENS, _actor_norm
    out = set()
    for p in prior_events:
        out |= (_actor_norm(title_discriminators(p.get("title") or ""))
                & ACTOR_TOKENS)
    return out


def _repost_delta(event, prior_events, disc):
    """True when a repost stub still carries a genuine new development: a new
    actor attribution, a new victim count, or a new IOC. A new CVE is settled
    by is_rereport before this runs. False = zero-delta echo (see
    REPOST_STUB_RE)."""
    if _actor_tokens(disc) - _prior_actor_tokens(prior_events):
        return True
    text = (event.get("title") or "") + " " + (event.get("content_md") or "")
    prior_text = " ".join((p.get("title") or "") + " "
                          + (p.get("content_md") or "")
                          for p in prior_events)
    if _victim_counts(text) - _victim_counts(prior_text):
        return True               # a new victim count
    return bool(_ioc_values(text) - _ioc_values(prior_text))


def _echo_is_zero_delta(event, prior_events):
    """True when a re-report event adds NOTHING the story doesn't carry.

    is_rereport() has already settled identity (the event re-tells covered
    material); this is the delta question, answered by _repost_delta — the
    exact test the rd: stub leg uses, generalized to EVERY outlet re-report
    (2026-10-20 owner decision ed6b7366c2ec). One delta engine, two
    application points: new actor attribution, new victim count, or new IOC
    means the echo still carries a development; a new CVE is settled before
    this runs (is_rereport returns False for new-CVE events).
    """
    from merge import title_discriminators
    disc = title_discriminators(event.get("title") or "")
    return not _repost_delta(event, prior_events, disc)


def is_rereport(event, prior_events, *, low_jaccard=0.25, high_jaccard=0.55,
                min_gap_h=24, story_title=None):
    """True when `event` re-reports coverage the story already carries.

    Two identity signals, combined to fit the two echo shapes:
      - CVE-anchored (event's CVEs all already carried by the priors): the
        CVE set IS the disclosure identity, so ANY shared discriminator
        token with a prior event settles it. Same-CVE coverage days later
        is a re-report even when fully reworded; severity keeps KEV/CVSS
        and the digest's own KEV-recap clock still surfaces genuine KEV
        developments, while editorial wildcards remain the path for same-
        CVE stories that genuinely deserve the slate.
      - CVE-less (breach/claim stories): the headline is the only identity,
        so require near-identical wording (jaccard >= high_jaccard, >= 2
        shared tokens). A new victim or new claim shares the actor tokens
        but adds its own — that is a development, not an echo.
    Plus: the matched prior must be >= min_gap_h older — the first-day
    multi-outlet burst is legitimate pickup velocity, not echoes.

    Founding events (no priors) are never re-reports. KEV-add events are
    deliberately NOT special-cased here: severity carries the KEV flag
    regardless, and digest_candidates appends the KEV add date itself, so a
    suppressed KEV echo cannot hide a KEV development from the digest.

    2026-10-03 audit (2nd day recommending): this class explains most of the
    ~340 digest demote overrides (8 slugs overridden >= 3 times) — echoes
    reset the decay clock (merge stamps last_seen on every attach) and add
    48h velocity, so echo-only stories stayed on the slate until demoted by
    hand. Still dominant on 2026-10-13 (235 re-report/no-delta demotes, 77
    since Oct 1), so two legs were added (owner decision fc3f6e00a8d9):
      - the min_gap_h skip now protects ONLY first-day stories: while the
        story's own non-backfill material is younger than min_gap_h the
        burst rule works as before; once it is older, priors within 24h of
        the event are evaluated like any other (a day-2 pickup no longer
        dodges the identity floors just because it landed within 24h of
        yesterday's re-tell),
      - `story_title`: the canonical STORY headline is also an identity — a
        reworded outlet re-tell overlapping it (>= 2 shared discriminators,
        >= high_jaccard) is an echo of covered material even when no single
        prior matches. Off unless the caller passes it (hot_score does;
        digest_candidates keeps its EVOLVED semantics unchanged).
    Plus the zero-delta repost leg (2026-10-18 owner decision 6aad368c1a1b,
    audit Rec 1a): an `rd:` Reddit link-post is judged on the DELTA it
    carries, never on title overlap — its content is boilerplate, so how its
    headline tokenizes says nothing about whether the story developed. A stub
    with no new CVE, actor, victim count, or IOC is a zero-delta echo.

    Pure: both arguments are event dicts; tokenization reuses merge's
    discriminator sets (lazy import — merge imports this module).
    """
    if not prior_events:
        return False
    from merge import title_discriminators, CVE_RE
    try:
        ev_dt = datetime.fromisoformat(
            (event.get("published_at") or "").replace("Z", "+00:00"))
    except ValueError:
        ev_dt = None
    ev_cves = {c.upper() for c in (event.get("cves") or [])}
    ev_cves |= {c.upper() for c in CVE_RE.findall(event.get("title") or "")}
    prior_cves = set()
    for p in prior_events:
        prior_cves |= {c.upper() for c in (p.get("cves") or [])}
        prior_cves |= {c.upper() for c in CVE_RE.findall(p.get("title") or "")}
    new_cves = ev_cves - prior_cves
    if ev_cves and new_cves:
        return False              # brings a new CVE: a development, not an echo
    disc = title_discriminators(event.get("title") or "")
    # Zero-delta repost stub leg (2026-10-18 owner decision 6aad368c1a1b — see
    # REPOST_STUB_RE). Placed before the title floors on purpose: the stub is
    # content-free, so it must not earn velocity/pickup/recency by resembling
    # anything, and it must not dodge the rule by tokenizing thinly either.
    if REPOST_STUB_RE.match(event.get("id") or event.get("event_id") or ""):
        if _repost_delta(event, prior_events, disc):
            return False          # a genuine delta: a development
        return True               # content-free stub, no delta: zero-delta echo
    floor = low_jaccard if ev_cves else high_jaccard
    min_shared = 1 if ev_cves else 2
    if len(disc) < min_shared:
        return False
    if ev_cves and not new_cves:
        # No-new-delta echo condition (2026-10-17 owner decision f5f2bc09664a,
        # audit Rec 2 re-report leg): a same-CVE disclosure is an echo ONLY
        # when it brings no new CVE, no new actor attribution, and no new
        # exploitation confirmation. Attribution or in-the-wild proof
        # emerging days later is a development the dev-clock must not erase;
        # a reworded outlet re-tell with none of the three stays an echo.
        if _actor_tokens(disc) - _prior_actor_tokens(prior_events):
            return False          # new actor attribution: a development
        ev_title = event.get("title") or ""
        if IN_WILD_RE.search(ev_title) and not any(
                IN_WILD_RE.search(p.get("title") or "")
                for p in prior_events):
            return False          # fresh exploitation confirmation: ditto
    # First-day burst protection: priors within min_gap_h are skipped ONLY
    # while the story's own founding material (desk backfills excluded — a
    # June backfill must not age a day-old story past the window) is younger
    # than min_gap_h. An old story gets no skip: day-2+ pickups of covered
    # material must clear the identity floors below.
    young = False
    if ev_dt is not None:
        founding = []
        for p in prior_events:
            if p.get("kind") == "backfill":
                continue
            try:
                founding.append(datetime.fromisoformat(
                    (p.get("published_at") or "").replace("Z", "+00:00")))
            except ValueError:
                continue
        if founding:
            young = (ev_dt - min(founding)).total_seconds() < min_gap_h * 3600
    for p in prior_events:
        if ev_dt is not None:
            try:
                p_dt = datetime.fromisoformat(
                    (p.get("published_at") or "").replace("Z", "+00:00"))
            except ValueError:
                p_dt = None
            if p_dt is None:
                continue
            if young and (ev_dt - p_dt).total_seconds() < min_gap_h * 3600:
                continue          # same-day burst: legitimate velocity
        pdisc = title_discriminators(p.get("title") or "")
        shared = disc & pdisc
        if ev_cves:
            # CVE identity already settles this is the same disclosure; any
            # shared token confirms it is not a tokenization fluke.
            if shared:
                return True
            continue
        if len(shared) < min_shared:
            continue
        union = disc | pdisc
        if union and len(shared) / len(union) >= floor:
            return True
    # Canonical-headline echo leg (old stories only — a first-day pickup
    # that resembles the canonical headline is normal coverage).
    if story_title and ev_dt is not None and not young and not new_cves:
        std = title_discriminators(story_title)
        if std:
            shared_t = disc & std
            if len(shared_t) >= 2 \
                    and len(shared_t) / len(disc | std) >= high_jaccard:
                return True
    return False


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
    sev, kev, epss_bonus = _cvss_severity(cves)
    title = (story.get("title") or "").lower()
    # Repost stubs are excluded from the scoring text (2026-10-18 decision
    # 6aad368c1a1b): their "content" is the outlet headline wrapped in Reddit
    # boilerplate, so it must not mint severity signals or the corroborated-
    # novelty bonus for a story the stub did not develop.
    body_text = " ".join(
        events.get(r["event_id"], {}).get("content_md", "")
        for r in story.get("events", [])
        if not REPOST_STUB_RE.match(r["event_id"] or ""))[:4000].lower()
    text = title + " " + body_text
    # CVSS the coverage states but the local NVD store lacks (research CVEs
    # missing from kevrichment/nvd-info) — same band, so an "unpatched CVSS
    # 10" story can no longer sit at sev 1.0 and under-rank (2026-10-13).
    text_cvss = max((float(m) for m in CVSS_TEXT_RE.findall(text)), default=0.0)
    if text_cvss:
        sev = max(sev, _cvss_band(text_cvss))
    signals = sum(w for rx, w in SIGNALS if rx.search(text))
    # high-impact weights (2026-10-13 owner decision fc3f6e00a8d9): explicit
    # extra weight for confirmed in-the-wild exploitation and unpatched
    # CVSS >= 9.0 flaws — the classes the digest agent keeps hand-promoting
    # as "score under-ranks high-impact" (35 overrides, 13 since Oct 1).
    impact = 0.0
    if kev or IN_WILD_RE.search(text):
        impact += IMPACT_IN_WILD
    if sev >= 4.5 and UNPATCHED_RE.search(text):
        impact += IMPACT_UNPATCHED_9
    # corroborated no-CVE novelty floor (2026-10-17, audit Rec 3 — see
    # NOVELTY_TTP_RE): outside SIGNAL_CAP so the shared signal bucket can't
    # absorb it, inside the 5.0 severity cap like every other weight.
    novelty = (NOVELTY_MULTI_SOURCE
               if (not cves and story.get("n_sources", 0) >= 2
                   and NOVELTY_TTP_RE.search(text)) else 0.0)
    severity = min(5.0, sev + (0.5 if kev else 0.0) + min(SIGNAL_CAP, signals)
                   + epss_bonus + impact + novelty)

    # velocity (events in last 48h) + the decay clock: RE-REPORT events
    # don't count (2026-10-03). Outlet echoes of already-carried coverage
    # used to reset the 36h half-life and stack velocity, keeping echo-only
    # stories on the digest slate until a manual demote; the dev clock now
    # runs on genuine developments only. Every story has >= 1 development
    # (founding events are never re-reports); events missing from `events`
    # keep the old behavior (skipped entirely).
    refs = sorted(
        (r for r in story.get("events", []) if r["event_id"] in events),
        key=lambda r: events[r["event_id"]].get("published_at") or "")
    dev_dts, n_rereports, n48 = [], 0, 0
    zd48 = False       # a zero-delta outlet echo inside the window
    zd_only = True     # every in-window re-report so far carried no delta
    prior = []
    for ref in refs:
        e = events[ref["event_id"]]
        dt = parse(e["published_at"])
        if is_rereport(e, prior, story_title=story.get("title")):
            n_rereports += 1
            in48 = (now - dt).total_seconds() < VELOCITY_WINDOW_H * 3600
            if in48:
                if REPOST_STUB_RE.match(e.get("id") or e.get("event_id") or ""):
                    pass    # stubs are neutral: pinned to neither gain nor
                            # trigger rank (6aad368c1a1b) — no delta by
                            # construction (is_rereport settled it)
                elif _echo_is_zero_delta(e, prior):
                    zd48 = True   # an outlet echo restating covered facts
                else:
                    zd_only = False   # a re-report still carrying a real
                                      # delta: leave the story alone
        else:
            dev_dts.append(dt)
            if (now - dt).total_seconds() < VELOCITY_WINDOW_H * 3600:
                n48 += 1
        prior.append(e)
    velocity = min(2.0, 0.5 * n48)

    # zero-delta demotion (2026-10-20 owner decision ed6b7366c2ec — see
    # ZERO_DELTA_FACTOR): the story's only recent movement is delta-free
    # outlet echoes and nothing genuine happened inside the window, so the
    # decayed base no longer rides the slate at full weight. The trigger is
    # the n48==0 check; zd48 requires an echo to demote FOR; zd_only keeps
    # delta-carrying re-reports out of the trigger. n_rereports (above)
    # already counts every echo, zero-delta ones included — the breakdown
    # tells the whole story: rereports N, zero_delta true, penalty X.
    zero_delta = zd48 and zd_only and n48 == 0

    # pickup speed: hours between the first and second GENUINE development —
    # echo events earn no pickup (2026-10-18 decision 6aad368c1a1b: a
    # zero-delta repost must never promote the rank), matching the velocity
    # and decay-anchor semantics above.
    pickup = 0.0
    ts = sorted(dev_dts)
    if len(ts) >= 2:
        gap_h = max(0.0, (ts[1] - ts[0]).total_seconds() / 3600)
        pickup = 0.6 * (2.718 ** (-gap_h / 24))

    base = breadth + authority + severity + velocity + pickup

    # recency temporal multiplier — anchored to the newest GENUINE
    # development, not the newest echo (2026-10-03 re-report penalty)
    try:
        last_dev = max(dev_dts) if dev_dts else parse(story.get("last_seen") or "")
    except ValueError:
        last_dev = parse(story.get("last_seen") or "")
    hours = max(0, (now - last_dev).total_seconds() / 3600)
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

    pre = min(10.0, base * recency + reddit)
    score = round(pre, 1)
    zero_delta_penalty = 0.0
    if zero_delta:
        zero_delta_penalty = round(pre * (1.0 - ZERO_DELTA_FACTOR), 2)
        score = round(pre * ZERO_DELTA_FACTOR, 1)
    return {
        "score": score,
        "base": round(base, 2),
        "breadth": round(breadth, 2),
        "authority": round(authority, 2),
        "severity": round(severity, 2),
        "velocity": round(velocity, 2),
        "pickup": round(pickup, 2),
        "recency": round(recency, 2),
        "rereports": n_rereports,
        "zero_delta": zero_delta,
        "zero_delta_penalty": zero_delta_penalty,
        "novelty": round(novelty, 2),
        "reddit": round(reddit, 2),
        "kev": kev,
        "epss": round(epss_bonus, 2),
        "n_sources": story.get("n_sources", 0),
    }
