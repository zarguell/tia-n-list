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
# high-precision.
TRIAGE_BOOKKEEPING = (
    # "The event references …", "the event reference to …"
    r"\bthe event (?:reference|references|referenced|referencing)\b",
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

# Specificity (the filler-killer): a grounded analysis names a CVE, a
# multi-digit number or a version. The literal shipped filler above has no
# digit at all, so it fails here even before the structure checks.
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
NUM2_RE = re.compile(r"\d[\d,.]*\d")
VERSION_RE = re.compile(r"\b\d+\.\d+\b")

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
    _banned_hits."""
    low = (text or "").replace("\u2019", "'")
    out = []
    for pat in TRIAGE_BOOKKEEPING:
        for m in re.finditer(pat, low, re.IGNORECASE):
            out.append(f"internal triage bookkeeping {m.group(0)!r} "
                       f"(published prose narrates the story, not the "
                       f"ingest/triage state)")
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


def lint_analysis(text, story=None, subject_title=None):
    """HARD violations for one analysis (plain markdown) — each of these
    quarantines. story, when given, only names the file in the messages.
    subject_title, when given, enables the subject-grounding alternative
    (see TITLE_STOPWORDS note): a non-CVE story's analysis is grounded when
    it names the story's subject. Empty list = passes the gate.
    Paragraph-count drift is soft: see soft_paras()."""
    out = _banned_hits(text)
    for tag in raw_html_hits(text):
        out.append(f"raw HTML {tag} (payloads/markup belong in code spans)")
    if any(l.lstrip().startswith("#") for l in text.splitlines()):
        out.append("markdown heading line (prompts ban headings)")
    if not MIN_LEN <= len(text) <= MAX_LEN:
        out.append(f"length {len(text)} chars (need {MIN_LEN}..{MAX_LEN})")
    grounded = bool(CVE_RE.search(text) or NUM2_RE.search(text) or VERSION_RE.search(text))
    if not grounded and subject_title:
        grounded = _names_subject(text, subject_title)
    if not grounded:
        out.append("no grounding: no CVE id, no 2+ digit number, no version "
                   "token, and the story subject is never named")
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
    """Violations for one daily digest (plain markdown). Banned strings only
    plus the coverage-link invariant — no length/paragraph bounds (long-form
    is legal here)."""
    out = _banned_hits(text)
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
    violations = lint_analysis(text, story=story,
                               subject_title=(story.get("title") or "")
                               if isinstance(story, dict) else None)
    violations = violations + depth_violations(
        text, story.get("score") if isinstance(story, dict) else None)
    soft = soft_paras(text)
    triage = triage_bookkeeping_hits(text)
    if triage:
        # Distinct WARN (2026-10-17 audit Issue 2 / Rec 4b): kept, never a
        # hard violation — see TRIAGE_BOOKKEEPING. Logged before the
        # quarantine branch so a bookkeeping-leaking analysis that ALSO
        # hard-fails still records it for the desk.
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
