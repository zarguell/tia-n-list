#!/usr/bin/env python3
"""Judgment-layer audit checks (2026-08-24).

The triage-drift incident (Aug 17-24, 2026) was invisible to the output checks
— site up, queues draining — because the JUDGMENT layer had no invariants.
These functions audit the judgment: store dedup invariants, triage drift
telemetry, non-Latin script scan, digest override log, near-duplicate
suspects, adversarial sampling targets, and creation-vs-consolidation trends.

Pure functions (data_dir/now passed in) so test_audit.py can pin them;
audit.py imports and wires them into its report.
"""
import glob
import json
import os
import re
from datetime import timedelta

from merge import title_jaccard, distinct_series_codes, title_discriminators

CJK_RE = re.compile(r"[\u0400-\u04FF\u4E00-\u9FFF\u3040-\u30FF\uAC00-\uD7AF\u0600-\u06FF]")


def load_all_stories(data_dir):
    out = {}
    for f in glob.glob(os.path.join(data_dir, "stories", "*.json")):
        try:
            s = json.load(open(f))
            out[s["id"]] = s
        except Exception:
            pass
    return out


def dedup_invariants(stories):
    """Mechanically-detectable failure classes from the 2026-08-24 triage
    drift: events referenced by >1 active story, merged_into cycles, events
    stranded inside redirect shells, and true same-slug-base duplicates
    (shared event or similar titles; distinct advisory codes exonerate).
    Returns (ok, detail, ghost_count)."""
    owners = {}
    for sid, s in stories.items():
        for r in s.get("events", []):
            owners.setdefault(r["event_id"], set()).add(sid)
    multi = sorted(f"{e}: {','.join(sorted(sids))}"
                   for e, sids in owners.items() if len(sids) > 1)

    cycles = []
    for sid in stories:
        seen, cur = set(), sid
        while stories.get(cur, {}).get("merged_into"):
            if cur in seen:
                cycles.append(sid)
                break
            seen.add(cur)
            cur = stories[cur]["merged_into"]

    in_shell = sum(len(s.get("events", [])) for s in stories.values() if s.get("merged_into"))

    by_base = {}
    for sid, s in stories.items():
        if not s.get("merged_into") and s.get("events"):
            by_base.setdefault(re.sub(r"-\d+$", "", sid), []).append(sid)
    dups = []
    for base, group in by_base.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                ta, tb = stories[a].get("title", ""), stories[b].get("title", "")
                shares = bool({r["event_id"] for r in stories[a]["events"]} &
                              {r["event_id"] for r in stories[b]["events"]})
                if shares or (title_jaccard(ta, tb) >= 0.4
                              and not distinct_series_codes(ta, tb)):
                    dups.append(f"{a} + {b}")

    ghosts = sum(1 for s in stories.values() if not s.get("merged_into") and not s.get("events"))
    problems = ([("multi-ref", x) for x in multi] +
                [("cycle", x) for x in cycles] +
                [("in-shell", str(in_shell))] * (1 if in_shell else 0) +
                [("same-base", x) for x in dups])
    detail = "; ".join(f"{k}: {v}" for k, v in problems[:8]) or \
        f"clean ({ghosts} eventless ghosts, informational)"
    return not problems, detail, ghosts


def duplicate_suspects(stories, now, max_out=10, max_age_days=45, min_jaccard=0.5):
    """Near-duplicate ACTIVE story pairs the mechanical merge likely missed
    (different outlets, few shared tokens): title jaccard >= min_jaccard with
    >= 2 shared discriminators, distinct advisory codes exonerated, actor-only
    matches (1 shared token) excluded. Recent stories only. Output is for the
    LLM to adjudicate (merge via a triage decisions file), never automatic."""
    cutoff = (now - timedelta(days=max_age_days)).strftime("%Y-%m-%dT%H:%M:%S")
    pool = [s for s in stories.values()
            if not s.get("merged_into") and s.get("events")
            and s.get("last_seen", "") >= cutoff]
    out = []
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            a, b = pool[i], pool[j]
            ta, tb = a.get("title", ""), b.get("title", "")
            shared = title_discriminators(ta) & title_discriminators(tb)
            j_ = title_jaccard(ta, tb)
            if j_ < min_jaccard or len(shared) < 2 or distinct_series_codes(ta, tb):
                continue
            out.append({"a": a["id"], "b": b["id"], "jaccard": round(j_, 2),
                        "title_a": ta[:70], "title_b": tb[:70]})
    out.sort(key=lambda x: -x["jaccard"])
    return out[:max_out]


def language_scan(data_dir, max_files=800):
    """Non-Latin script bleed (CJK/Cyrillic/Arabic) in published English
    prose — the 2026-08-23 'Chinese characters in an analysis' catch, made
    deterministic instead of luck-of-the-sample. Accented Latin and emoji are
    not flagged."""
    hits = []
    for pat in ("analysis/*.md", "digests/*.md"):
        for f in glob.glob(os.path.join(data_dir, pat))[:max_files]:
            try:
                text = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            m = CJK_RE.search(text)
            if m:
                ctx = text[max(0, m.start() - 20):m.end() + 20].replace("\n", " ")
                hits.append(f"{os.path.relpath(f, data_dir)}: …{ctx}…")
    return hits


def digest_overrides(data_dir):
    """Aggregate the digest agent's editorial deviations (promote/demote/
    wildcard) across all digests — the feedback loop for tuning score.py."""
    out = []
    for f in glob.glob(os.path.join(data_dir, "digests", "*.json")):
        d = os.path.splitext(os.path.basename(f))[0]
        try:
            for o in json.load(open(f)).get("overrides", []):
                out.append({"digest": d, **o})
        except Exception:
            pass
    out.sort(key=lambda o: o["digest"], reverse=True)
    return out


def triage_telemetry(cronman_log_dir, triage_dir, now):
    """Drift detection for the hourly LLM gate: schema WARNs in the wrapper
    log, keep/drop balance from the last 24h of decision files, and silent
    drift (judgment ran but no decisions file written). Returns
    (problems, info)."""
    problems, info = [], []
    log_text = ""
    for d in (now.strftime("%Y-%m-%d"), (now - timedelta(days=1)).strftime("%Y-%m-%d")):
        p = os.path.join(cronman_log_dir, d + ".log")
        if os.path.exists(p):
            try:
                log_text += open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                pass
    for pat, label in ((r"WARN: \d+ decision entries could not be parsed", "unparsed decision entries"),
                       (r"no keep/drop decisions recognized", "no decisions recognized")):
        n = len(re.findall(pat, log_text))
        if n:
            problems.append(f"{label} x{n}")
    judgment_runs = len(re.findall(r"TIA pi judgment", log_text))
    cap_hits = len(re.findall(r"triage: 30 new events", log_text))
    cutoff = (now - timedelta(hours=24)).timestamp()
    keeps = drops = 0
    for f in glob.glob(os.path.join(triage_dir, "decisions-*.json")):
        if os.path.getmtime(f) < cutoff:
            continue
        try:
            dec = json.load(open(f)).get("decisions", [])
        except Exception:
            continue
        keeps += sum(1 for x in dec if x.get("action") == "keep")
        drops += sum(1 for x in dec if x.get("action") == "drop")
    if judgment_runs and not (keeps or drops):
        problems.append(f"{judgment_runs} judgment runs in 24h but 0 decisions (silent drift)")
    if keeps + drops >= 10:
        ratio = keeps / (keeps + drops)
        info.append(f"keep/drop {keeps}/{drops} ({ratio:.0%} keep)")
        if ratio > 0.95:
            problems.append(f"suspiciously permissive triage: {ratio:.0%} keep")
    else:
        info.append(f"keep/drop {keeps}/{drops} in 24h")
    if cap_hits:
        info.append(f"30-event batch cap hit x{cap_hits} (window falling behind)")
    return problems, "; ".join(info) or "no signal"


def queue_age(data_dir, stories, now):
    """Analysis-queue staleness: a story pending > 48h is stuck, not queued.
    Returns (worst_hours or None, detail)."""
    try:
        q = json.load(open(os.path.join(data_dir, "needs-analysis.json")))
    except Exception:
        return None, "needs-analysis.json unreadable"
    slugs = q.get("stories", [])
    if not slugs:
        return 0.0, "empty"
    events_by_id = {}
    for f in glob.glob(os.path.join(data_dir, "events", "*.json")):
        eid = os.path.splitext(os.path.basename(f))[0]
        try:
            events_by_id[eid] = (json.load(open(f)).get("published_at") or "")[:19]
        except Exception:
            pass
    worst_h, worst = 0.0, ""
    for slug in slugs:
        s = stories.get(slug)
        if not s:
            continue
        newest = max((events_by_id.get(r["event_id"], "") for r in s.get("events", [])),
                     default="")
        if not newest:
            continue
        try:
            from datetime import datetime, timezone
            dt = datetime.fromisoformat(newest.replace("Z", "+00:00"))
            h = (now - dt).total_seconds() / 3600
            if h > worst_h:
                worst_h, worst = h, slug
        except Exception:
            pass
    return worst_h, (f"{len(slugs)} queued, oldest pending {worst_h:.0f}h ({worst[:48]})"
                     if worst else f"{len(slugs)} queued")


def sampling_targets(data_dir):
    """Adversarial sampling for the LLM pass: not just the newest files (the
    2026-08-23 Chinese-text catch was luck) — also the OLDEST analyses
    (staleness) and the stories the latest digest actually linked (what
    readers saw)."""
    out = {}
    analyses = []
    for f in glob.glob(os.path.join(data_dir, "analysis", "*.md")):
        analyses.append((os.path.getmtime(f), f))
    analyses.sort()
    if analyses:
        out["newest_analyses"] = [os.path.basename(f) for _, f in analyses[-3:]]
        out["oldest_analyses"] = [os.path.basename(f) for _, f in analyses[:3]]
    digests = sorted(os.path.splitext(os.path.basename(f))[0]
                     for f in glob.glob(os.path.join(data_dir, "digests", "*.json")))
    if digests:
        try:
            d = json.load(open(os.path.join(data_dir, "digests", digests[-1] + ".json")))
            out["latest_digest"] = digests[-1]
            out["digest_linked_stories"] = d.get("stories", [])[:20]
        except Exception:
            pass
    return out


def store_trends(data_dir, stories, now, days=7):
    """Creation vs consolidation trend: events/day and new active stories/day.
    Rising stories/day on flat events/day = fragmentation trending up."""
    from collections import Counter
    ev_per_day = Counter()
    for f in glob.glob(os.path.join(data_dir, "events", "*.json")):
        try:
            ev_per_day[(json.load(open(f)).get("published_at") or "")[:10]] += 1
        except Exception:
            pass
    st_per_day = Counter()
    for s in stories.values():
        if not s.get("merged_into"):
            st_per_day[(s.get("first_seen") or "")[:10]] += 1
    horizon = [(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days - 1, -1, -1)]
    return {
        "per_day": [{"date": d,
                     "events": ev_per_day.get(d, 0),
                     "new_active_stories": st_per_day.get(d, 0)} for d in horizon],
        "totals": {"active_stories": sum(1 for s in stories.values() if not s.get("merged_into")),
                   "merged_shells": sum(1 for s in stories.values() if s.get("merged_into"))},
    }
