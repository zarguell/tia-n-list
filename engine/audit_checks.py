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
from datetime import datetime, timedelta, timezone

from merge import (title_jaccard, distinct_series_codes,
                   distinct_advisory_ids, title_discriminators)

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


def roundup_family(title):
    """'microsoft' | 'ics' | 'other' if title is a DEDICATED vendor Patch
    Tuesday / numbered-Windows-flaws roundup, else None.

    A dedicated roundup names the vendor/month up front. Two false positives
    the naive substring test produced: a multi-topic weekly digest mentions
    Patch Tuesday as the last item in a comma list ("WeChat worm, hacking AI
    agents, biggest Microsoft Patch Tuesday"), and an exploit-kit writeup can
    contain "V8 flaws" (the old digit-plus-flaws pattern read the "8" as a
    count).
    """
    t = (title or "").lower()
    pt = t.find("patch tuesday")
    if pt >= 0:
        if "," in t[:pt]:          # Patch Tuesday is a trailing list item
            return None
    elif not ("windows" in t
              and re.search(r"\b\d[\d,]*\s*(cves?|vulnerabilit\w+|flaws?)", t)):
        return None
    if any(x in t for x in ("ics", "siemens", "schneider", "phoenix contact")):
        return "ics"
    if "microsoft" in t:
        return "microsoft"
    # "other" bucket: only a DEDICATED roundup, not a story that merely
    # mentions Windows CVEs. Two 2026-09-22 audit false positives: a legacy
    # exploitation story ("CVE-2011-3402, CVE-2013-3918" reads as a count
    # via the digit-comma prefix) and vendor advisories without a month
    # reference ("Chipmaker Patch Tuesday: Nvidia, AMD, Arm..."). Require
    # a month reference or a patches/fixes verb — tested against the title
    # with the literal "patch tuesday" removed so the noun use can't
    # satisfy the verb half of the gate.
    stripped = t.replace("patch tuesday", " ")
    if (re.search(r"\b(january|february|march|april|may|june|july|"
                   r"august|september|october|november|december)\b", stripped)
            or re.search(r"\b(patch(?:es|ed|ing)?|fix(?:es|ed|ing)?)\b",
                          stripped)):
        return "other"
    return None


def dedup_invariants(stories):
    """Mechanically-detectable failure classes from the 2026-08-24 triage
    drift: events referenced by >1 active story, merged_into cycles, dangling
    redirects (merged_into to a missing story), events stranded inside
    redirect shells, and true same-slug-base duplicates (shared event or
    similar titles; distinct advisory codes — in the title or the slug —
    exonerate). Returns (ok, detail, ghost_count)."""
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

    # dangling redirects: a shell whose merged_into chain never reaches a live
    # story (a `-2` twin was dropped while the pointer stuck around). The
    # cycle case is reported separately; cycles are skipped here.
    orphans = []
    for sid, s in stories.items():
        if not s.get("merged_into"):
            continue
        seen, cur = set(), sid
        while stories.get(cur, {}).get("merged_into") and cur not in seen:
            seen.add(cur)
            cur = stories[cur]["merged_into"]
        if cur in seen:
            continue                      # cycle, already reported above
        if cur not in stories:
            orphans.append(f"{sid} -> {s['merged_into']}")

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
                              and not distinct_series_codes(ta, tb)
                              and not distinct_advisory_ids(a, b)):
                    dups.append(f"{a} + {b}")

    ghosts = sum(1 for s in stories.values() if not s.get("merged_into") and not s.get("events"))
    problems = ([("multi-ref", x) for x in multi] +
                [("cycle", x) for x in cycles] +
                [("orphan-redirect", x) for x in orphans] +
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
                       (r"no keep/drop decisions recognized", "no decisions recognized"),
                       (r"keep -> unknown story", "keep->unknown-story WARNs "
                        "(LLM-invented story ids; fragmented clusters possible)")):
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


def ingest_noise(data_dir, now, *, raw_glob=None, window_days=2,
                 min_decisions=30, drop_rate=0.8, share=0.35, share_drop=0.6,
                 stub_rate=0.5, min_kept=10, flood_days=7,
                 flood_min=50, flood_share=0.5):
    """Ingest-noise audit (2026-09-16): a single Mastodon tag-spam account
    flooded ~65% of hourly triage volume for a week before anyone noticed —
    site up, queues draining, so the output checks were blind. These are the
    per-source ingest invariants that would have flagged it day one.

    Detectors, over triage decisions windows (decisions-<ts>.json, hourly):
      1. junk source — source with >= min_decisions decisions whose drop
         rate >= drop_rate (gamefan's consumer links: 94% dropped).
      2. tag-spam author — author (joined via the collector's raw toot
         signal, raw_glob) holding >= share of attributed decisions at a
         drop rate >= share_drop: crowds the 30-event/hour triage cap and
         delays real articles (gamefan: 45% share, 94% dropped).
      3. kept-stub source — kept events whose .md is < 200c: the agent
         writes "grounded" analyses from nothing (securityweek: 62% stubs
         kept at 81%).
      4. flood entrant — source that minted >= flood_min events in the last
         flood_days AND >= flood_share of its lifetime presence in that
         window — a brand-new firehose even when triage keeps it
         (thehackerwire: ~26/day, 94% KEPT — detectors 1-2 are blind to it).

    Returns (problems, info): problems = human-readable findings (audit
    FAILs when non-empty); info = per-source/per-author tables for the
    report's EXTRA payload. Pure: data_dir/now/raw_glob passed in.
    """
    events = {}
    for f in glob.glob(os.path.join(data_dir, "events", "*.json")):
        try:
            ev = json.load(open(f))
        except Exception:
            continue
        eid = ev.get("id") or os.path.splitext(os.path.basename(f))[0]
        try:
            md_len = os.path.getsize(os.path.join(data_dir, "events", eid + ".md"))
        except OSError:
            md_len = 0
        events[eid] = (ev.get("source") or "?", ev.get("published_at") or "", md_len)

    author_of = {}
    if raw_glob:
        for f in glob.glob(raw_glob):
            try:
                lines = open(f, errors="replace")
            except OSError:
                continue
            with lines:
                for line in lines:
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    if r.get("id"):
                        author_of[str(r["id"])] = (r.get("author") or "?").lower()

    cutoff = (now - timedelta(days=window_days)).strftime("%Y-%m-%dT%H")
    per_source = {}   # src -> [decisions, drops, kept_stub_md]
    per_author = {}   # author -> [decisions, drops]
    attributed = 0
    for f in glob.glob(os.path.join(data_dir, "triage", "decisions-*.json")):
        ts = os.path.basename(f)[10:-5]
        try:
            if datetime.strptime(ts, "%Y-%m-%dT%H%M").replace(tzinfo=timezone.utc) \
                    < now - timedelta(days=window_days):
                continue
        except ValueError:
            continue  # decisions-frag2.json and other non-hourly files
        try:
            dec = json.load(open(f)).get("decisions", [])
        except Exception:
            continue
        for d in dec:
            eid = d.get("event_id") or ""
            src = events.get(eid, ("?", "", 0))[0]
            action = d.get("action")
            ps = per_source.setdefault(src, [0, 0, 0])
            ps[0] += 1
            if action == "drop":
                ps[1] += 1
            elif events.get(eid, ("", "", 0))[2] < 200:
                ps[2] += 1
            raw_id = eid.split(":", 1)[1] if ":" in eid else None
            author = author_of.get(raw_id)
            if author:
                pa = per_author.setdefault(author, [0, 0])
                pa[0] += 1
                attributed += 1
                if action == "drop":
                    pa[1] += 1

    lifetime, recent = {}, {}
    flood_cutoff = (now - timedelta(days=flood_days)).strftime("%Y-%m-%d")
    for src, pub, _md in events.values():
        lifetime[src] = lifetime.get(src, 0) + 1
        if pub[:10] >= flood_cutoff:
            recent[src] = recent.get(src, 0) + 1

    problems = []
    for src, (n, drops, stubs) in per_source.items():
        if n >= min_decisions and drops / n >= drop_rate:
            problems.append(f"junk source {src}: {100 * drops // n}% dropped "
                            f"({drops}/{n} decisions, {window_days}d)")
        kept = n - drops
        if kept >= min_kept and stubs / kept >= stub_rate:
            problems.append(f"kept-stub source {src}: {100 * stubs // kept}% of "
                            f"{kept} kept events have <200c content")
    for src, rec in recent.items():  # flood: decision-independent
        life = lifetime.get(src, 0)
        if rec >= flood_min and life and rec / life >= flood_share:
            problems.append(f"flood entrant {src}: {rec} events in {flood_days}d "
                            f"= {100 * rec // life}% of lifetime {life}")
    for author, (n, drops) in per_author.items():
        if (n >= min_decisions and attributed
                and n / attributed >= share and drops / n >= share_drop):
            problems.append(f"tag-spam author {author}: {n} decisions "
                            f"({100 * n // attributed}% of attributed window), "
                            f"{100 * drops // n}% dropped")

    def table(stats, has_stub):
        rows = sorted(stats.items(), key=lambda kv: -kv[1][0])[:12]
        out = []
        for key, (n, drops, stubs) in rows:
            row = {"name": key, "decisions": n,
                   "dropped_pct": round(100 * drops / n) if n else 0}
            if has_stub:
                kept = n - drops
                row["kept_stub_pct"] = round(100 * stubs / kept) if kept else 0
            row["events_7d"] = recent.get(key, 0)
            row["lifetime"] = lifetime.get(key, 0)
            out.append(row)
        return out

    info = {
        "window_days": window_days,
        "attributed_decisions": attributed,
        "sources": table(per_source, True),
        "authors": [{"name": a, "decisions": n,
                     "dropped_pct": round(100 * d / n) if n else 0}
                    for a, (n, d) in sorted(per_author.items(),
                                            key=lambda kv: -kv[1][0])[:12]],
    }
    return problems, info
