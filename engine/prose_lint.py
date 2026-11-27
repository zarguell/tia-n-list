#!/usr/bin/env python3
"""Deterministic prose-quality lint for analyses + the daily digest.

KEV records have a hard verify gate; prose had none, and the gap shipped:
analysis/25-year-old-curl-vulnerability-cve-2026-8932-ai-discovered-flaw.md
reads exactly "Analyst note based on event content. Watch for updates." — the
generic filler prompts/tia-hourly.md bans ("GROUND EVERY CLAIM in the event
content ... no generic filler"), and its em-dash ban ("NO em dashes (U+2014
banned anywhere)") was equally unenforced. This module is the prose twin of
the KEV verify gate:

  - lint_analysis / lint_digest: pure text in, human-readable violations out
    (no I/O — audit-grade, like bin/kev-verify.py's deterministic checks);
  - quarantine_analysis: the analysis enforcement half. A violating analysis
    is MOVED to data/analysis/.rejects/<id>-<UTC timestamp>.md (never
    deleted — evidence + re-review) and the story json's "analysis" key is
    cleared. That re-queues the story: merge.emit_needs queues any story
    whose analysis FILE is missing (`if not os.path.exists(analysis_path):
    queue.append(s["id"])`), so the story is re-analyzed next hour under the
    prompt that already bans all of this — self-healing, no build failure.

ssg.py wires both: analyses quarantine with a WARN (non-fatal, live cards
only), the digest fails the build closed — the digest is the flagship
artifact and daily_digest's recover sweep would republish a bad one in a
loop; a failed publish records telemetry and pages via autodiag instead of
shipping slop.

Specificity is STAGED (decision e732e816ab3e, 2026-10-21 audit Issue 4 +
Rec 7): the MIN_LEN + grounding gate above accepts any 2+ digit number, so a
stub whose only digits were years cleared it. Stage 2 (specificity_hits)
requires a CVE id, an ATT&CK technique id, a version token, an IOC, or a
tool/malware/actor designation drawn from the event's own text (plus the
existing subject-naming alternative). It ships in SPECIFICITY_STAGE="warn"
first: the rule is reported per analysis and counted over the whole store,
but does NOT quarantine until the backlog is re-analysed and the stage flips
to "hard".

A third, DISTINCT class is WARN-only: internal triage bookkeeping in
analysis prose (TRIAGE_BOOKKEEPING / triage_bookkeeping_hits). It narrates
the ingest object ("The event references …", "attaches to the existing
story", "is the original mint", "no existing cluster covers this CVE")
instead of the real-world subject a reader sees. 2026-10-17 audit Issue 2
flagged the newest analyses leaking exactly this for the desk; Rec 4b asked
for a lint rule to catch recurrence. It is a distinct WARN, NOT a hard
violation, because the family is wide (100+ stored analyses say "the event
…") and the re-analysis prompt does not ban the phrasing — quarantining on
it would pull every affected live card and requeue against a prompt that
reproduces it until the retry cap, for prose a reader still understands.

One arm of that WARN family was PROMOTED to hard: the precise `the event
(reference|references|referenced|referencing)` construction (EVENT_REFERENCE_RE
/ event_reference_hits, 2026-10-26 audit Issue 8 + Rec 4). The applied card
e8f2664e00bd (PR #150) deliberately shipped the whole family WARN-only; the
audit's remaining ask was a hard gate on the single construction it actually
saw, and 17 of them shipped in ONE lint run. Only that shape is hard — the rest
of the family ("attaches to the existing", "is the original mint", "no existing
cluster covers", "the new story is appropriate") stays WARN, because THOSE are
the wide phrasings (100+ stored analyses say "the event …") whose mass
quarantine is the flood risk documented below. Flipping just the observed
construction keeps the rule narrow, mechanical (rewrite the sentence to name
the report), and bounded by the store it was measured on.

A fourth class IS hard: bare internal event/channel ids (`masto:`, `mf:`, `rd:`,
`x:`, `desk:`, `rss:`, `bsky:`) printed in analysis prose (INTERNAL_ID_RE /
internal_id_hits, 2026-10-25 audit Issue 1 + Rec 1). The bookkeeping WARN above
saw the sentences but not the id shape, so 11 published analyses — the front
page hero among them — kept printing triage identifiers a reader cannot
resolve. Unlike its WARN sibling the class is narrow and mechanical (delete the
parenthesis, keep the sentence), so it quarantines like any other hard error;
ids quoted inside code spans stay legal.

A fifth class is also hard: a malformed attributive compound / dropped word
(MALFORMED_COMPOUND_RE / malformed_compound_hits, 2026-10-26 audit Issue 4).
The published 2026-10-26 digest said "makes this a patch immediately item for
any estate running AOS-8" — the compound adjective lost its hyphen and left
the adverb `immediately` in the attributive slot, and NOTHING in this gate
looked at word order (banned strings and grounding cannot), so it shipped and
the audit could only repair it by hand. The rule matches article + word +
lowercase `-ly` adverb + generic head noun, excludes the `-ly` adjectives that
are legal attributives, and fires for both digests (fail closed, like the
coverage-link invariant) and analyses (quarantine + requeue).

The scope is deliberately tighter than "an adverb between two nouns", because
this class is HARD on both paths: see MALFORMED_COMPOUND_HEAD for why a head
must be a noun-only word ("a reboot immediately fixes the bug" is English, not
a defect), and why the article is lowercase-only (sentence-initial `A patch
immediately item` still escapes — a documented gap, not a claimed catch).
"""
import glob
import json
import os
import re
from datetime import datetime, timezone

# Banned strings, case-insensitive. The em dash is hard-banned by
# prompts/tia-hourly.md ("NO em dashes (U+2014 banned anywhere)") and
# prompts/daily-digest.md ("NO em dashes (U+2014 banned)"). The slop list is
# deliberately SHORT and high-precision — only phrases that are near-certain
# filler in security prose; every false positive erodes trust in the gate.
EM_DASH = "\u2014"
SLOP = [
    "it's worth noting",
    "in today's",
    "ever-evolving",
    "delve into",
    "delves into",
    "underscores the importance",
    "analyst note based on event content",
    "serves as a stark reminder",
    "in the realm of",
    "testament to",
    "rapidly evolving landscape",
]

# Internal triage bookkeeping (2026-10-17 audit Issue 2 / Rec 4b). Published
# analysis prose narrates the STORY a reader sees, never the ingest object:
# "The event references BleepingComputer coverage and attaches to the
# existing critical Magento story", "The event is the original mint for this
# new story", "no existing cluster covers this CVE". These are meta-sentences
# about the pipeline's own triage (references / cluster minting), and the soft
# paragraph rule never saw them. WARN-only (see triage_bookkeeping_hits):
# reported per occurrence, but NOT a hard violation, because the family is
# broad and the analysis prompt does not ban the wording — see the module
# docstring. One pattern per observed construction; deliberately
# high-precision. EXCEPTION: the `the event (reference|references|referenced|
# referencing)` construction was promoted to a HARD violation (2026-10-26
# audit Issue 8 + Rec 4) and lives in EVENT_REFERENCE_RE below, so that arm
# is deliberately absent from this tuple.
# NOTE: the "the event (reference|references|referenced|referencing)" arm
# that used to open this tuple is now the HARD EVENT_REFERENCE_RE below
# (2026-10-26 audit Issue 8 + Rec 4) — it lives in exactly one place, so it
# is never double-reported as a WARN alongside the quarantine.
TRIAGE_BOOKKEEPING = (
    # "attaches to the existing critical Magento story"
    r"\battaches? to the existing\b",
    # "The event is the original mint for this new story"
    r"\bis the original mint\b",
    # "no existing cluster covers this CVE"
    r"\bno existing cluster covers\b",
    # FastapiAdmin's other bookkeeping sentence: "The new story is
    # appropriate because …"
    r"\bthe new story is appropriate\b",
)

# Bare internal event/channel ids (2026-10-25 audit Issue 1 + Rec 1). The
# bookkeeping WARN above catches the SENTENCES that narrate ingest state; it
# never matched the id SHAPE, so 11 published analyses kept printing the
# pipeline's own identifiers in prose — including the front page hero
# analysis, whose second sentence read "The new event
# (masto:117498992322565382) reinforces active exploitation". A reader has no
# way to resolve `masto:`/`mf:`/`rd:` and every such token is triage state,
# not the real-world subject, so this is a HARD violation (quarantine +
# requeue) unlike its WARN-only sibling: the class is narrow and mechanical
# (remove the parenthesis, keep the sentence) and the prompt already bans
# narrating ingest objects. Code spans are stripped first, so an id quoted as
# part of a genuine payload stays legal.
#
# The prefix must start a token (`(?<![A-Za-z0-9_])`): bare `x:123` is a real
# id, but the same text inside `box:123` or `standard:7` is a word, not an
# identifier — without that guard the two-letter prefixes match inside prose.
INTERNAL_ID_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:masto|mf|rd|x|desk|rss|bsky):[0-9A-Za-z_]+")

# Malformed attributive compound / dropped word (2026-10-26 audit Issue 4).
# The published 2026-10-26 digest read "the unauthenticated path to admin makes
# this a patch immediately item for any estate running AOS-8": the compound
# adjective lost its hyphen, leaving the adverb `immediately` in the attributive
# slot between the modifier noun (`patch`) and the head noun (`item`). No claim
# was false, so nothing in the pipeline saw it — banned strings and grounding
# cannot catch word order, and the audit could only repair the sentence by hand
# (its corrective license needs a contradicting source, which a grammar defect
# never supplies).
#
# The detectable shape is narrow and mechanical: article + word + LOWERCASE
# `-ly` adverb + generic head noun. Precision notes, all of them load-bearing:
#   * the head-noun list is deliberately small and generic (item/issue/thing/
#     priority...). Wide nouns are where false positives live ("a monthly
#     patch", "a missed July update");
#   * the adverb must be lowercase, so a capitalized `July` cannot fake `-ly`;
#   * LY_ADJECTIVES excludes the adjectives that end in `-ly` (monthly, weekly,
#     daily, friendly, likely, ...), which are legal attributives;
#   * scanning all 2,627 stored digest/analysis files (2026-11-26) returned
#     exactly one hit on the pre-fix store — the defect above — and zero after
#     the digest was corrected. That precision is why the rule is HARD for the
#     digest, which fails the build closed by design (ship-clean gate; only
#     TODAY's digest is re-linted, so historical digests are never re-checked),
#     and hard for analyses, where quarantine + requeue is self-healing.
#   * a head must be a NOUN-ONLY word. The same word order is grammatical when
#     the head doubles as a third-person verb — "a reboot immediately fixes the
#     bug", "a restart usually fixes the appliance", "a decision usually
#     matters", "an update usually issues a token" — and a regex that only sees
#     article + word + -ly adverb + head cannot tell the two apart, so the
#     verb-shaped plurals (fixes, issues, steps, actions, matters, concerns,
#     tasks) are NOT heads. Singular heads are safe: English has no "a <noun>
#     <adverb> <verb>" shape, so "a patch immediately fix" is always a defect.
#     (2026-11-26 review: an earlier draft carried the verb plurals and flagged
#     four of those five sentences; the corpus had zero instances either way,
#     so this arm is pure precision — a false positive here fails a build.)
MALFORMED_COMPOUND_HEAD = (
    "item", "items", "issue", "thing", "things", "one",
    "task", "priority", "priorities", "problem", "problems",
    "concern", "matter", "step", "action", "fix",
)
LY_ADJECTIVES = frozenset({
    "monthly", "weekly", "daily", "hourly", "yearly", "timely",
    "friendly", "likely", "unlikely", "costly", "lovely", "lively",
    "lonely", "elderly", "silly", "deadly", "holy", "curly",
    "early", "only", "family", "orderly", "scholarly", "chilly",
    "burly", "jolly", "kindly", "sickly", "stately", "unruly",
})
MALFORMED_COMPOUND_RE = re.compile(
    r"\b(?:a|an)\s+[A-Za-z][\w'-]*\s+([a-z]+ly)\s+(" +
    "|".join(MALFORMED_COMPOUND_HEAD) + r")\b")


# Structure contract: prompts/tia-hourly.md promises "2-4 short plain
# paragraphs", no headings. Length bounds keep auto-extracted stubs (too
# short) and prompt-dumped novellas (too long) out of the analyst voice.
# PARAGRAPH COUNT IS SOFT (soft_paras, WARN only, never quarantines): the
# real-store smoke showed 121 of 158 shipped analyses are dense single-
# paragraph notes — mostly grounded, house-style writing. Enforcing 2-4 as
# hard would quarantine 86% of the store for structure alone and flood the
# re-analysis queue; the hard floor that actually separates filler from
# analysis is MIN_LEN + grounding. 2026-10-18 audit (decision 7925e9ba91b6):
# even as a WARN the under-minimum arm flooded the logs (325 WARNs in one
# cronman run, 25 in the digest log, every day) with zero editorial
# consequence, so 1-paragraph notes are no longer reported at all — only an
# OVER-LONG body (> MAX_PARAS) is soft-flagged. Hard prose errors still
# fail via lint_analysis, unchanged.
MIN_PARAS, MAX_PARAS = 2, 4
MIN_LEN, MAX_LEN = 200, 6000

# Significance floor (2026-10-31 audit Issue 4): a fallback model rung wrote
# 383-475B single-paragraph analyses for score-6.0 zero-days (Ivanti ICS
# CVE-2026-104935, 30 sources) while score-0.6 fragments got 454-578B — the
# 200-char floor cannot tell depth from significance. Stories at/above the
# significant score must read like an analyst note: >= 3 paragraphs and
# >= 900 chars. The bar is hard (quarantine + requeue) because the hourly
# agent will simply redo it; only 4 live analyses fail it today, and the
# existing MAX_ANALYSIS_QUARANTINES cap still bounds retries.
SIGNIFICANT_SCORE = 5.0
SIGNIFICANT_MIN_LEN = 900
SIGNIFICANT_MIN_PARAS = 3

# Specificity (the filler-killer), stage 1: a grounded analysis names a CVE,
# a multi-digit number or a version. The literal shipped filler above has no
# digit at all, so it fails here even before the structure checks. Stage 2
# (specificity_hits below) replaces the loose numeric arm — see
# SPECIFICITY_STAGE for how the two are staged.
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
# LEGACY (stage-1) numeric grounding: any 2+ digit number cleared it, which is
# what a bare year exploited (see SPECIFICITY_STAGE). Kept only for the disarmed
# stage so behaviour does not change until the stage-2 backlog is drained.
NUM2_RE = re.compile(r"\d[\d,.]*\d")
VERSION_RE = re.compile(r"\b\d+\.\d+(?:\.\d+)*\b")

# --- Specificity stage 2 (decision e732e816ab3e: 2026-10-21 audit Issue 4 +
# Rec 7). The 2026-10-18 thin-analysis gate (decision 7925e9ba91b6, PR #154)
# shipped MIN_LEN + grounding, but its numeric arm accepts ANY 2+ digit number,
# so analysis/bronze-sandcastle-apt-uses-legitimate-windows-apps-for-encrypted.md
# (508 bytes) cleared it on "August 2025 through August 2026" alone. Stage 2
# requires ONE of:
#
#   - a CVE id;
#   - an ATT&CK technique id (T1566, T1566.001);
#   - a version token (2.3.1, 152.0.7977.82);
#   - an IOC: a defanged or live domain, an IPv4 address, a 32-64 hex hash;
#   - a named tool/malware/actor designation that appears in BOTH the analysis
#     AND the event's own text (the story's event titles/snippets), so a writer
#     cannot invent a name to satisfy the gate;
#
# plus the pre-existing subject-naming alternative for non-CVE research pieces
# (a research/policy analysis can never contain any of the above).
#
# STAGED, per the decision: stage "warn" reports the new rule per analysis and
# counts the shipped analyses that would newly fail, WITHOUT quarantining — a
# straight flip would quarantine the backlog and re-queue it against a prompt
# that does not yet ask for the extra specificity, burning agent runs. Flip with
# PROSE_LINT_SPECIFICITY_STAGE=hard once the backlog is re-analysed.
ATTACK_RE = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
# 32 hex = MD5, 40 = SHA-1, 64 = SHA-256. A bare 32-char hex run is still a
# distinctive observable (a GUID without dashes), never prose filler.
HASH_RE = re.compile(r"\b[0-9a-fA-F]{32,64}\b")
# TLD allowlist, not `[a-z]{2,63}`: prose is full of file names (cmd.exe,
# claude.json) whose "TLD" is an extension — ioc.py's FILE_EXT_TLDS problem.
IOC_TLDS = (
    "com", "net", "org", "io", "co", "ru", "cn", "top", "xyz", "info",
    "biz", "me", "dev", "app", "cloud", "site", "online", "su", "ir", "kp",
    "hk", "tw", "jp", "kr", "uk", "de", "fr", "nl", "pl", "br", "in", "au",
    "ca", "us", "eu", "cc", "ws", "tv", "sh", "link", "click", "live",
    "shop", "store", "tech", "world", "space", "website", "network",
    "hosting", "support", "pro", "name", "mobi", "asia", "gov", "edu", "mil",
    "int", "icu", "buzz", "sbs", "cyou", "rest", "cam", "bar", "cyber",
)
DOMAIN_RE = re.compile(
    r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:"
    + "|".join(sorted(IOC_TLDS, key=len, reverse=True)) + r")\b", re.I)
# Defanged indicators are the house style ("americanprgoress[.]top"), so the
# IOC probe normalises them back before matching.
DEFANG_RE = re.compile(
    r"\[\s*\.\s*\]|\(\s*\.\s*\)|\{\s*\.\s*\}"
    r"|\[\s*dot\s*\]|\(\s*dot\s*\)", re.IGNORECASE)

# Acronyms/brands that appear in nearly every analysis: naming one is not
# specificity, and letting them ground would gut the rule. Deliberately short
# and high-precision, like SLOP.
GENERIC_DESIGNATIONS = {
    "cisa", "nist", "mitre", "nsa", "fbi", "kev", "cve", "cves", "cvss",
    "epss", "ttp", "ttps", "ioc", "iocs", "api", "apis", "http", "https",
    "tls", "dns", "ssh", "rdp", "vpn", "sql", "xss", "rce", "csrf", "ssrf",
    "dll", "dlls", "exe", "pdf", "url", "urls", "apt", "apts", "lolbin",
    "lolbins", "os", "oses", "windows", "linux", "android", "macos", "ios",
    "chrome", "firefox", "edge", "safari", "google", "microsoft", "apple",
    "amazon", "azure", "aws", "gcp", "github", "openai", "anthropic",
    "claude", "cloudflare", "adobe", "cisco", "fortinet", "ivanti",
    "vmware", "citrix", "sap", "oracle", "kubernetes", "docker", "npm",
    "pypi", "patchstack", "wordpress", "united", "states", "europe", "asia",
    "africa", "america", "china", "russia", "iran", "north", "korea",
}


# Which arm quarantines. "warn" = stage 1 (report only, legacy numeric
# grounding still decides). "hard" = stage 2 (specificity decides).
SPECIFICITY_STAGE_ENV = "PROSE_LINT_SPECIFICITY_STAGE"
SPECIFICITY_STAGE = (os.environ.get(SPECIFICITY_STAGE_ENV) or "warn").strip().lower()

# Digests always link their coverage (prompts/daily-digest.md: "Every story
# appears in prose, linked once as [name](stories/<slug>/)").
DIGEST_LINK_RE = re.compile(r"\]\(stories/")

# Grounding alternative for non-CVE stories (2026-09-25): a research
# disclosure with no CVE id, a policy/landscape piece, an incident note —
# none can ever contain a CVE/version token, so the numeric grounding rule
# was structurally unpassable for them (the kubernetes/GCP research story
# was re-analyzed and re-quarantined 10+ times before this existed). An
# analysis that NAMES THE STORY'S SUBJECT is grounded: ≥2 capitalized
# title tokens (≥4 chars, not function words) appearing in the text.
# Generic filler ("Analyst note based on event content") still fails — it
# never names the subject.
TITLE_STOPWORDS = {
    "the", "this", "that", "these", "those", "their", "a", "an", "and",
    "or", "of", "in", "on", "for", "to", "with", "without", "from", "at",
    "by", "as", "is", "are", "be", "was", "were", "after", "before",
    "amid", "among", "into", "onto", "over", "under", "per", "via", "new",
    "how", "why", "what", "when", "where", "who", "all", "more", "most",
    "than", "then", "some", "still", "says", "said", "report", "reports",
    "warning", "warnings", "issue", "issues", "update", "updates", "take",
    "takes", "taken", "puts", "put", "gets", "get", "goes", "gone",
}

# A story that fails the analysis gate this many times is flagged for drop
# review instead of being requeued forever (the kubernetes/GCP story burned
# an agent run every hour for 10+ hours on a structurally unpassable
# analysis). Remove .rejects/<id>.capped to reset.
MAX_ANALYSIS_QUARANTINES = 3


def _banned_hits(text):
    """Banned-string violations shared by analyses and digests. Curly
    apostrophes normalize to straight ones first — "it's" slop written with
    U+2019 is still slop."""
    out = []
    low = text.lower().replace("\u2019", "'")
    if EM_DASH in text:
        out.append("em dash (U+2014) present (banned by the prompts)")
    for p in SLOP:
        if p in low:
            out.append(f"AI-slop phrase {p!r}")
    return out


def _subject_tokens(title):
    """Capitalized ≥4-char title tokens that aren't function words."""
    out = []
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9.-]{3,}", title or ""):
        if tok[0].isupper() and tok.lower() not in TITLE_STOPWORDS:
            out.append(tok)
    return out


def _names_subject(text, title):
    low = text.lower()
    toks = _subject_tokens(title)
    if not toks:
        # No nameable subject (all-lowercase/stopword title): nothing to
        # name, so the fallback can never fire — CVE/numeric grounding only.
        return False
    matched = 0
    for tok in toks:
        if re.search(r"\b" + re.escape(tok) + r"\b", low, re.IGNORECASE):
            matched += 1
    # ≥2 distinct tokens: one common word ("controller", "network") must
    # not ground an analysis of a different story. A single-token subject
    # (2026-10-04: "France tax office ..." yields only ["France"]) names
    # everything it can with one hit, so the bar is min(2, len(tokens)).
    return matched >= min(2, len(toks))


def _has_ioc(text):
    """True when the prose carries a real observable: domain, IPv4, hash.
    Defanged forms ([.]/(.)) are the house style and normalise first."""
    norm = DEFANG_RE.sub(".", text or "")
    return bool(IPV4_RE.search(norm) or HASH_RE.search(norm)
                or DOMAIN_RE.search(norm))


def _designations(source_text):
    """Tool/malware/actor DESIGNATIONS in the event's own text.

    A designation is a name-like token, not any capitalized word: an acronym
    (CLEANGULP, UTA0565), an acronym+word compound (COFFLoader), or a
    letter/digit compound. Plain capitalized words (Sandboxie, Windows) are
    excluded deliberately — naming a technology is not naming tooling, and
    the bronze-sandcastle stub must stay a negative."""
    out = set()
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9_.-]{3,}", source_text or ""):
        t = tok.strip("._-")
        if len(t) < 4 or t.lower() in TITLE_STOPWORDS \
                or t.upper() in GENERIC_DESIGNATIONS \
                or t.lower() in GENERIC_DESIGNATIONS:
            continue
        if re.fullmatch(r"[A-Z0-9][A-Z0-9_-]{3,}", t) \
                or re.search(r"[A-Z]{2,}[a-z]{2,}|[a-z]{2,}[A-Z]{2,}", t) \
                or re.search(r"[A-Za-z]{2,}\d{2,}|\d{2,}[A-Za-z]{2,}", t):
            out.add(t)
    return out


def _names_designation(text, subject_title, source_text):
    """The analysis names a tool/malware/actor that the EVENT text names.
    Title tokens are skipped: naming the story's subject is the separate
    subject-naming arm below, so the two arms stay distinct."""
    toks = _designations(source_text)
    if not toks:
        return False
    titled = {t.lower() for t in _subject_tokens(subject_title)}
    low = text.lower()
    for t in toks:
        if t.lower() in titled:
            continue
        if re.search(r"\b" + re.escape(t.lower()) + r"\b", low):
            return True
    return False


def specificity_hits(text, subject_title=None, source_text=None):
    """STAGE-2 specificity (decision e732e816ab3e): [] when grounded.

    Grounded means at least one CVE id, ATT&CK technique id, version token,
    IOC, or event-sourced tool/malware/actor designation — or, for non-CVE
    research pieces, the story subject named as before. A bare year or any
    2-digit number no longer clears it. Returns human-readable violations
    (never raises); the caller decides WARN (stage "warn") vs quarantine
    (stage "hard")."""
    text = text or ""
    if CVE_RE.search(text) or ATTACK_RE.search(text) or VERSION_RE.search(text):
        return []
    if _has_ioc(text):
        return []
    if _names_designation(text, subject_title, source_text):
        return []
    if subject_title and _names_subject(text, subject_title):
        return []
    return ["no specificity: needs a CVE id, an ATT&CK technique id, a "
            "version token, an IOC (domain/IP/hash), a named tool/malware/"
            "actor drawn from the event text, or the story subject by name "
            "(a bare year or any 2-digit number no longer grounds)"]


def specificity_backlog(analysis_dir, stories=None):
    """Store-wide stage-2 dry run: ids of shipped analyses that would newly
    fail (decision e732e816ab3e's "report the count, do not quarantine yet").
    stories maps id -> mapping with title/source_text (the card fields);
    unknown ids are probed title-less, which is the conservative direction."""
    stories = stories or {}
    out = []
    for f in sorted(glob.glob(os.path.join(analysis_dir, "*.md"))):
        sid = os.path.splitext(os.path.basename(f))[0]
        st = stories.get(sid) or {}
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        if specificity_hits(text, subject_title=st.get("title") or "",
                            source_text=st.get("source_text")):
            out.append(sid)
    return out


# The one arm of the bookkeeping family that is HARD (2026-10-26 audit
# Issue 8 + Rec 4, the residual of applied card e8f2664e00bd / PR #150).
# `the event (reference|references|referenced|referencing)` narrates the
# ingest object in reader-facing prose, and the WARN-only treatment left the
# class routine: the audit counted 17 of them in a single lint run and the
# files shipped anyway. The shape is fixed and mechanical (say what was
# reported, not that the ingest object references it), so it quarantines and
# requeues like the other hard prose errors. Precision: the regex is the
# identical construction the WARN used, including its case-insensitivity —
# no code-span stripping, so backticking the phrase cannot buy an exemption
# from a rule about sentences. The WIDE family stays WARN (see the module
# docstring) so the 100-file flood is still avoided.
EVENT_REFERENCE_RE = re.compile(
    r"\bthe event (?:reference|references|referenced|referencing)\b",
    re.IGNORECASE)


def event_reference_hits(text):
    """HARD violation: `the event references …` bookkeeping in analysis prose.

    2026-10-26 audit Issue 8 + Rec 4: the narrow construction (not the whole
    bookkeeping family) quarantines — see EVENT_REFERENCE_RE. Returns one
    message per occurrence naming the matched phrase, so the log says which
    sentence to rewrite (name the report instead: "BleepingComputer reported
    …", "the offseq radar entry notes …")."""
    out = []
    for m in EVENT_REFERENCE_RE.finditer(text or ""):
        out.append(f"internal triage bookkeeping {m.group(0)!r} (published "
                   f"prose names the story and its reporting, never the "
                   f"ingest/triage state; rewrite the sentence to name the "
                   f"report itself)")
    return out


def triage_bookkeeping_hits(text):
    """DISTINCT WARN: internal triage bookkeeping in published analysis
    prose, one message per occurrence (2026-10-17 audit Issue 2 / Rec 4b).

    Unlike raw_html_hits this is deliberately NOT fed into lint_analysis:
    the phrasing is prose-quality, not a factual contradiction, and the
    family is broad enough that a hard rule would quarantine 100+ live
    cards and requeue them against a prompt that does not ban the wording
    (see TRIAGE_BOOKKEEPING + the module docstring). quarantine_analysis
    logs these as WARN and keeps the file; the audit/desk acts on them.
    Curly apostrophes normalize to straight ones first, mirroring
    _banned_hits.

    One construction is NOT WARN — `the event references/reference/…` — and
    deliberately lives in event_reference_hits (HARD, 2026-10-26 audit
    Issue 8 + Rec 4), never in this tuple."""
    low = (text or "").replace("\u2019", "'")
    out = []
    for pat in TRIAGE_BOOKKEEPING:
        for m in re.finditer(pat, low, re.IGNORECASE):
            out.append(f"internal triage bookkeeping {m.group(0)!r} "
                       f"(published prose narrates the story, not the "
                       f"ingest/triage state)")
    return out


def malformed_compound_hits(text):
    """HARD violation: a dropped-hyphen / dropped-word compound in prose.

    2026-10-26 audit Issue 4: "makes this a patch immediately item for any
    estate running AOS-8" shipped in the published digest — a malformed
    compound ("patch-immediately item") that no rule could see, because
    banned strings and grounding checks say nothing about word order. See
    MALFORMED_COMPOUND_RE for the exact shape and its precision notes.

    Returns one message per occurrence naming the matched phrase, so the fix
    is obvious in the log (hyphenate the compound or rewrite the phrase: "an
    immediate patch"). The hint quotes the canonical defective/legal pair
    instead of interpolating the matched head, because "an immediate items"
    (or any fabricated article + plural) reads as nonsense in the log. Code
    spans and fenced blocks are stripped first, so a quoted example stays
    legal.
    """
    stripped = re.sub(r"```.*?```", "", text or "", flags=re.S)
    stripped = re.sub(r"`[^`\n]+`", "", stripped)
    out = []
    for m in MALFORMED_COMPOUND_RE.finditer(stripped):
        adv = m.group(1)
        if adv in LY_ADJECTIVES:
            continue
        out.append(f"malformed compound {m.group(0)!r} (adverb {adv!r} sits "
                   f"in the attributive slot: hyphenate the compound or move "
                   f"the adverb in front of the noun, e.g. 'a patch "
                   f"immediately item' -> 'an immediate patch')")
    return out


def raw_html_hits(text):
    """Literal HTML in agent prose that breaks the rendered site.

    2026-10-07: a desk backfill event described an XSS payload with a
    literal `<img src=x onerror=...>` tag; markdown passes inline HTML
    through, the story page rendered src="x", and the fail-closed link
    lint red-ed every deploy for 12h. Payloads/markup belong in code
    spans — code spans and fenced blocks are stripped before matching, so
    documented payloads are safe. Only tags that actually break output are
    flagged: href/src attributes (dangling-link FAIL) and active elements
    (script/style/iframe/object/embed/form/link/meta/base). Bare
    placeholders (`<ip>`, `<id>`) and tag-name mentions stay allowed.
    Returns the offending tag strings.
    """
    stripped = re.sub(r"```.*?```", "", text or "", flags=re.S)
    stripped = re.sub(r"`[^`\n]+`", "", stripped)
    out = []
    for m in re.finditer(r"<[a-zA-Z][^<>]*>", stripped):
        tag = m.group(0)
        if re.search(r"\s(?:href|src)\s*=", tag, re.IGNORECASE):
            out.append(tag[:80])
        elif re.match(r"<(script|style|iframe|object|embed|form|link|meta|base)\b",
                       tag, re.IGNORECASE):
            out.append(tag[:80])
    return out


def internal_id_hits(text):
    """Bare internal event/channel ids in agent prose that breaks the rendered
    site.

    2026-10-25 audit Issue 1 + Rec 1: published analyses printed the
    pipeline's own identifiers (`masto:117498992322565382`, `mf:164959`,
    `rd:…`, …) — the front page hero analysis led with one. A reader cannot
    resolve them and they narrate ingest state instead of the story, so this
    is a HARD violation (see INTERNAL_ID_RE). Code spans and fenced blocks
    are stripped before matching, so an id carried inside a genuine payload
    stays legal. Returns the offending tokens.
    """
    stripped = re.sub(r"```.*?```", "", text or "", flags=re.S)
    stripped = re.sub(r"`[^`\n]+`", "", stripped)
    return [m.group(0) for m in INTERNAL_ID_RE.finditer(stripped)]


def lint_analysis(text, story=None, subject_title=None, source_text=None):
    """HARD violations for one analysis (plain markdown) — each of these
    quarantines. story, when given, only names the file in the messages.
    subject_title, when given, enables the subject-grounding alternative
    (see TITLE_STOPWORDS note): a non-CVE story's analysis is grounded when
    it names the story's subject. source_text is the event text the analysis
    was written from (event titles/snippets) — it enables the stage-2
    tool/malware/actor arm. Empty list = passes the gate. Paragraph-count
    drift is soft: see soft_paras().

    Which grounding rule decides depends on SPECIFICITY_STAGE: "warn" (the
    shipped default) keeps the legacy numeric arm so nothing new is
    quarantined, "hard" applies specificity_hits (see its docstring)."""
    out = _banned_hits(text)
    for tag in raw_html_hits(text):
        out.append(f"raw HTML {tag} (payloads/markup belong in code spans)")
    for ev_id in internal_id_hits(text):
        out.append(f"internal event id {ev_id!r} (published prose names the "
                   f"story, never the ingest object; drop the "
                   f"parenthetical)")
    out.extend(malformed_compound_hits(text))
    out.extend(event_reference_hits(text))
    if any(l.lstrip().startswith("#") for l in text.splitlines()):
        out.append("markdown heading line (prompts ban headings)")
    if not MIN_LEN <= len(text) <= MAX_LEN:
        out.append(f"length {len(text)} chars (need {MIN_LEN}..{MAX_LEN})")
    if SPECIFICITY_STAGE == "hard":
        out.extend(specificity_hits(text, subject_title=subject_title,
                                    source_text=source_text))
    else:
        grounded = bool(CVE_RE.search(text) or NUM2_RE.search(text)
                        or VERSION_RE.search(text))
        if not grounded and subject_title:
            grounded = _names_subject(text, subject_title)
        if not grounded:
            out.append("no grounding: no CVE id, no 2+ digit number, no "
                       "version token, and the story subject is never named")
    if story:
        out = [f"{story}: {m}" for m in out]
    return out


def soft_paras(text):
    """SOFT violations: paragraph-count drift from the prompts' 2-4 promise.
    Reported as WARNs, never quarantines. Only an OVER-LONG body is reported
    (2026-10-18 decision 7925e9ba91b6): the under-minimum arm was pure log
    flood (1-paragraph notes are the house style — see the PARAGRAPH COUNT
    IS SOFT note above), so routine short analyses no longer WARN. A real
    prose-lint error still fails hard through lint_analysis."""
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    if len(paras) <= MAX_PARAS:
        return []
    return [f"{len(paras)} paragraph(s) (prompts promise "
            f"{MIN_PARAS}-{MAX_PARAS} short plain paragraphs)"]


def depth_violations(text, score):
    """HARD depth floor for significant stories (2026-10-31 audit Issue 4).

    Score-blind length floors let a 406-char write-up ship for a 30-source
    score-6.0 zero-day. A story at/above SIGNIFICANT_SCORE needs THREE
    paragraphs and SIGNIFICANT_MIN_LEN chars; below the bar the analysis is
    quarantined and re-analyzed, so the gate tracks editorial weight instead
    of treating every story as the same size. Non-significant stories are
    untouched (the house style is dense short notes)."""
    try:
        score = float(score or 0)
    except (TypeError, ValueError):
        score = 0.0
    if score < SIGNIFICANT_SCORE:
        return []
    out = []
    if len(text) < SIGNIFICANT_MIN_LEN:
        out.append(f"length {len(text)} chars (score {score:.1f} needs "
                   f">= {SIGNIFICANT_MIN_LEN} for a significant story)")
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    if len(paras) < SIGNIFICANT_MIN_PARAS:
        out.append(f"{len(paras)} paragraph(s) (score {score:.1f} needs "
                   f">= {SIGNIFICANT_MIN_PARAS} for a significant story)")
    return out


def lint_digest(text):
    """Violations for one daily digest (plain markdown). Banned strings plus
    the coverage-link invariant — no length/paragraph bounds (long-form is
    legal here) — and the malformed-compound rule (2026-10-26 audit Issue 4:
    "makes this a patch immediately item" shipped because nothing in this
    gate looked at word order)."""
    out = _banned_hits(text)
    out.extend(malformed_compound_hits(text))
    if not DIGEST_LINK_RE.search(text):
        out.append("no stories/ link (digests always link their coverage)")
    return out


def quarantine_analysis(stories_dir, analysis_dir, story, now=None, log=print):
    """Lint one story's analysis file; on violations quarantine + requeue.

    story is the story dict (or any mapping with "id") — only story["id"] is
    read; the json is re-read fresh from disk for the write-back so a stale
    card can never clobber newer fields. The CALLER owns the live-card gate:
    never call this for a story without a card (orphan/frozen files stay).

    Returns the violation list (empty = clean, or no analysis file — nothing
    to lint). A distinct WARN line is logged for internal triage bookkeeping
    (triage_bookkeeping_hits) whether or not the file is later quarantined —
    that rule never affects the return value. On violations: the file is moved
    (os.replace, never deleted) to <analysis_dir>/.rejects/<id>-<UTC
    timestamp>.md and the story json's
    "analysis" key is cleared (stale updated_at marker gone with it), which
    re-queues the story via merge.emit_needs (queues on a missing analysis
    file). Writes the json back only when the key existed — no churn on
    marker-less stories.
    """
    sid = story["id"]
    ap = os.path.join(analysis_dir, sid + ".md")
    if not os.path.exists(ap):
        return []
    with open(ap, encoding="utf-8", errors="replace") as f:
        text = f.read()
    subject_title = (story.get("title") or "") if isinstance(story, dict) else None
    source_text = story.get("source_text") if isinstance(story, dict) else None
    violations = lint_analysis(text, story=story,
                               subject_title=subject_title,
                               source_text=source_text)
    if SPECIFICITY_STAGE != "hard":
        # Stage-1 rollout (decision e732e816ab3e): the stage-2 rule is a WARN
        # that names the files which would newly fail — no quarantine until
        # the backlog is re-analysed and the stage flips to "hard".
        spec = specificity_hits(text, subject_title=subject_title,
                                source_text=source_text)
        if spec:
            log(f"WARN analysis/{sid}.md: specificity (kept, "
                f"stage={SPECIFICITY_STAGE}): {'; '.join(spec)}")
    violations = violations + depth_violations(
        text, story.get("score") if isinstance(story, dict) else None)
    soft = soft_paras(text)
    triage = triage_bookkeeping_hits(text)
    if triage:
        # Distinct WARN (2026-10-17 audit Issue 2 / Rec 4b): kept, never a
        # hard violation — see TRIAGE_BOOKKEEPING (the `the event references`
        # arm is the one exception: it is HARD via event_reference_hits, so
        # it never reaches here). Logged before the quarantine branch so a
        # bookkeeping-leaking analysis that ALSO hard-fails still records it
        # for the desk.
        log(f"WARN analysis/{sid}.md: triage-bookkeeping (kept): "
            f"{'; '.join(triage)}")
    if not violations:
        if soft:
            log(f"WARN analysis/{sid}.md: soft (kept): {'; '.join(soft)}")
        return []
    ts = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%S")
    rejects = os.path.join(analysis_dir, ".rejects")
    os.makedirs(rejects, exist_ok=True)
    prior = len(glob.glob(os.path.join(rejects, sid + "-*.md")))
    name = f"{sid}-{ts}.md"
    os.replace(ap, os.path.join(rejects, name))
    if prior + 1 >= MAX_ANALYSIS_QUARANTINES:
        # Retry cap: flag for drop review instead of requeuing forever
        # (2026-09-25: one story burned an agent run every hour for 10+
        # hours on a structurally unpassable analysis). merge.emit_needs
        # skips capped stories; remove the marker to reset.
        cap_marker = os.path.join(rejects, sid + ".capped")
        open(cap_marker, "w").close()
        log(f"CAPPED analysis/{sid}.md: failed the gate {prior + 1} times — "
            f"flagged for drop review, will not re-analyze "
            f"(remove .rejects/{sid}.capped to reset)")
    sp = os.path.join(stories_dir, sid + ".json")
    try:
        with open(sp, encoding="utf-8") as f:
            st = json.load(f)
    except (OSError, ValueError):
        st = None
    if st is not None and isinstance(st, dict) \
            and st.pop("analysis", None) is not None:
        with open(sp, "w", encoding="utf-8") as f:
            json.dump(st, f, indent=1)
    log(f"WARN analysis/{sid}.md: quarantined to .rejects/{name} "
        f"({'; '.join(violations)})")
    return violations
