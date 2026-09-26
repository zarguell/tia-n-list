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

# Structure contract: prompts/tia-hourly.md promises "2-4 short plain
# paragraphs", no headings. Length bounds keep auto-extracted stubs (too
# short) and prompt-dumped novellas (too long) out of the analyst voice.
# PARAGRAPH COUNT IS SOFT (soft_paras, WARN only, never quarantines): the
# real-store smoke showed 121 of 158 shipped analyses are dense single-
# paragraph notes — mostly grounded, house-style writing. Enforcing 2-4 as
# hard would quarantine 86% of the store for structure alone and flood the
# re-analysis queue; the hard floor that actually separates filler from
# analysis is MIN_LEN + grounding.
MIN_PARAS, MAX_PARAS = 2, 4
MIN_LEN, MAX_LEN = 200, 6000

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
    matched = 0
    for tok in _subject_tokens(title):
        if re.search(r"\b" + re.escape(tok) + r"\b", low, re.IGNORECASE):
            matched += 1
    # ≥2 distinct tokens: one common word ("controller", "network") must not
    # ground an analysis of a different story.
    return matched >= 2


def lint_analysis(text, story=None, subject_title=None):
    """HARD violations for one analysis (plain markdown) — each of these
    quarantines. story, when given, only names the file in the messages.
    subject_title, when given, enables the subject-grounding alternative
    (see TITLE_STOPWORDS note): a non-CVE story's analysis is grounded when
    it names the story's subject. Empty list = passes the gate.
    Paragraph-count drift is soft: see soft_paras()."""
    out = _banned_hits(text)
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
    Reported as WARNs, never quarantines (see the PARAGRAPH COUNT IS SOFT
    note above — 86% of the real store is dense single-paragraph notes)."""
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    if MIN_PARAS <= len(paras) <= MAX_PARAS:
        return []
    return [f"{len(paras)} paragraph(s) (prompts promise "
            f"{MIN_PARAS}-{MAX_PARAS} short plain paragraphs)"]


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
    to lint). On violations: the file is moved (os.replace, never deleted)
    to <analysis_dir>/.rejects/<id>-<UTC timestamp>.md and the story json's
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
    soft = soft_paras(text)
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
