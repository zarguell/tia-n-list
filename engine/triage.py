#!/usr/bin/env python3
"""Tia N. List — LLM triage gate for the hourly pipeline.

The deterministic merge is a fast path, but it cannot judge relevance or do
semantic grouping (Patch Tuesday roundups from different outlets failed to
merge because their titles share no tokens). The LLM triage pass adds the
judgment layer AT INGEST TIME:

  collect          -> writes data/triage/context-<date>.json: NEW events
                      (never triaged, not excluded) + candidate stories, so the
                      LLM can decide keep/drop and correct clustering.
  apply <decisions> -> applies the LLM decisions (keep/drop/merge) to the
                      store, rescoring + re-emitting needs-analysis.

Decision format (data/triage/decisions-<date>.json):
  {"decisions": [
     {"event_id": "mf:159824", "action": "keep", "story": "<existing-slug>|NEW",
      "story_title": "only when NEW", "reason": "optional",
      "exploitation": {"CVE-2026-59310": {"status": "exploited|suspected",
                                          "evidence": "1-2 sentence quote"}}},
     {"event_id": "mf:159825", "action": "drop", "reason": "press release, no substance"}],
   "merges": [{"from": "<slug>", "into": "<slug>"}]}

  ``exploitation`` is OPTIONAL, only for events that name CVEs. Statuses:
  exploited — the event reports OBSERVED in-the-wild exploitation (implants,
  victim counts, campaigns, CISA KEV confirmation); suspected — public exploit
  code/PoC or likely-but-unconfirmed exploitation. Attribute only the CVEs you
  can actually tie to the claim (a bulletin's blanket "actively exploited"
  does NOT flag all 200 CVEs). Omit the field entirely when the event makes no
  exploitation claim. apply() persists it to the event json with
  source="triage" (the deterministic backfill uses source="backfill").

Merged-away stories keep their json with "merged_into" and empty events so old
URLs and digest links resolve (ssg renders them as redirects); they are
excluded from cards/feeds/home.
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
EVENTS = os.path.join(DATA, "events")
STORIES = os.path.join(DATA, "stories")
TRIAGE = os.path.join(DATA, "triage")
STATE = os.path.join(TRIAGE, "state.json")
RUN_TAG = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M")

SCHEMA_HINT = (
    'Write decisions as JSON with EXACTLY this shape:\n'
    '{\n'
    '  "decisions": [\n'
    '    {"event_id": "<id>", "action": "keep", "story": "<existing candidate story id>", "reason": "..."},\n'
    '    {"event_id": "<id>", "action": "keep", "story": "NEW", "story_title": "<clean title>", "reason": "..."},\n'
    '    {"event_id": "<id>", "action": "drop", "reason": "..."}\n'
    '  ],\n'
    '  "merges": [{"from": "<fragment story id>", "into": "<canonical story id>"}]\n'
    '}\n'
    'STRICT KEY NAMES: the array key is "decisions" (never "events"); the story\n'
    'key is "story" (never "story_id"); "story" holds a candidate_stories id\n'
    'verbatim or the literal string "NEW". Optional per-event field\n'
    '"exploitation": {"CVE-...": {"status": "exploited|suspected", "evidence": "1-2 sentences"}}.'
)
NEEDS = os.path.join(DATA, "needs-analysis.json")
ANALYSIS = os.path.join(DATA, "analysis")
HOT_THRESHOLD = 3.3      # 0-10 scale (was 2.0 on 0-6); same analysis-queue bar as merge.py

# Keys the SSG "Why this score" template renders from score_breakdown. A story
# missing any of these raises a jinja UndefinedError that aborts the whole site
# build and blocks the hourly publish, so we backfill defensively below.
_SB_KEYS = ("base", "breadth", "authority", "severity", "velocity",
            "pickup", "recency", "reddit", "kev", "n_sources")
_SB_DEFAULTS = {k: (1.0 if k == "recency" else (False if k == "kev"
                else (0 if k == "n_sources" else 0.0)))
                for k in _SB_KEYS}

NOW = datetime.now(timezone.utc)
TODAY = NOW.strftime("%Y-%m-%d")


def _load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"processed": []}


def _save_state(st):
    os.makedirs(TRIAGE, exist_ok=True)
    json.dump(st, open(STATE, "w"), indent=1)


def _load_stories():
    out = {}
    for f in glob.glob(os.path.join(STORIES, "*.json")):
        s = json.load(open(f))
        out[s["id"]] = s
    return out


def _slugify(title, taken):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:64].rstrip("-")
    if not slug:
        slug = "story"
    n = 2
    base = slug
    while slug in taken:
        slug = f"{base}-{n}"
        n += 1
    return slug


def collect():
    from store import load_events
    events = load_events()
    state = _load_state()
    processed = set(state["processed"])
    new = [e for eid, e in events.items()
           if eid not in processed and not e.get("excluded")]
    new.sort(key=lambda e: e.get("published_at", ""), reverse=True)

    # Only the recent window needs LLM judgment — events older than 48h were
    # already clustered by the deterministic merge (acceptable for history).
    # Mark everything outside the window processed so it never resurfaces.
    cutoff = (NOW - timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%SZ")
    recent, older = [], []
    for e in new:
        (recent if (e.get("published_at", "") >= cutoff) else older).append(e)
    recent = recent[:30]                       # cap the per-run LLM batch (30-min window)
    for e in older:
        processed.add(e["id"])
    _save_state({"processed": sorted(processed)})

    stories = _load_stories()
    cutoff3 = (NOW - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    cands = [s for s in stories.values()
             if not s.get("merged_into")
             and (s.get("last_seen", "") >= cutoff3 or s.get("score", 0) >= HOT_THRESHOLD)]
    cands.sort(key=lambda s: s.get("last_seen", ""), reverse=True)
    cands = cands[:40]

    # Duplicate suspects: active stories whose slug base collides with another
    # active story (the -2/-3 suffix pattern) or that share an event with one.
    # Surfaced regardless of age so stranded duplicates can still be merged.
    by_base, ev_owners = {}, {}
    for s in stories.values():
        if s.get("merged_into"):
            continue
        by_base.setdefault(re.sub(r"-\d+$", "", s["id"]), []).append(s["id"])
        for r in s.get("events", []):
            ev_owners.setdefault(r["event_id"], set()).add(s["id"])
    suspect_ids = set()
    for base, group in by_base.items():
        if len(group) > 1:
            suspect_ids.update(group)
    for owners in ev_owners.values():
        if len(owners) > 1:
            suspect_ids.update(owners)
    cands += [stories[sid] for sid in sorted(suspect_ids)
              if sid not in {c["id"] for c in cands}][:20]

    def _event_title(refs):
        for r in refs or []:
            ev = events.get(r.get("event_id"))
            if ev:
                return ev.get("title", "")
        return ""

    os.makedirs(TRIAGE, exist_ok=True)
    ctx = {
        "date": TODAY,
        "decisions_path": f"engine/data/triage/decisions-{RUN_TAG}.json",
        "instructions": (
            "For every new event decide: (1) keep or drop — keep only stories worth "
            "covering (real security events, vulnerabilities, attacks, breaches, "
            "advisories with substance); drop press releases, vendor marketing, "
            "generic explainers, and anything duplicating an existing story. "
            "(2) If keep, assign the event to the RIGHT story: an existing candidate "
            "story id if it belongs there (this FIXES mechanical clustering — e.g. "
            "different outlets' Patch Tuesday roundups are ONE story), or NEW with a "
            "clean story_title. (3) merges: list candidate stories that are really "
            "the same story (from = fragment, into = the most complete one). "
            "(4) For every kept event that names CVEs, optionally assess exploitation: "
            "exploited = the event reports OBSERVED in-the-wild exploitation (implants, "
            "victim counts, campaigns, CISA KEV confirmation); suspected = public exploit "
            "code/PoC or likely-but-unconfirmed. Attribute ONLY the CVEs you can tie to "
            "the claim — a bulletin's blanket 'actively exploited' does NOT flag all its "
            "CVEs. Omit the exploitation field when the event makes no claim.\n\n"
            + SCHEMA_HINT),
        "new_events": [{
            "id": e["id"], "title": e.get("title", ""),
            "source": e.get("source", ""), "published_at": e.get("published_at", ""),
            "cves": e.get("cves", []),
            "snippet": (e.get("content_md") or "")[:220].replace("\n", " "),
        } for e in recent],
        "candidate_stories": [{
            "id": s["id"], "title": s.get("title", ""),
            "n_events": len(s.get("events", [])), "last_seen": s.get("last_seen", ""),
            "first_event_title": _event_title(s.get("events")),
        } for s in cands],
    }
    path = os.path.join(TRIAGE, f"context-{RUN_TAG}.json")
    json.dump(ctx, open(path, "w"), indent=1)
    print(f"triage: {len(recent)} new events (48h window, capped), {len(cands)} candidate stories -> {path}")
    print(f"triage: write decisions to {ctx['decisions_path']}")


def _read_event(eid):
    p = os.path.join(EVENTS, eid + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


def _normalize_decisions(dec):
    """Tolerant front end for LLM-written decision files. The documented
    schema is {"decisions": [...], "merges": [...]}, but models drift (seen in
    the wild: top-level "events", "keep"/"drop" lists, "story_id" instead of
    "story", exploitation values as bare strings). Accept the variants, count
    what cannot be salvaged so apply() can report it loudly instead of
    silently discarding the run's judgment."""
    out, ignored = [], 0
    raw = dec.get("decisions")
    if not isinstance(raw, list):
        raw = dec.get("events")
    if not isinstance(raw, list):
        raw = ([dict(d, action="keep") for d in dec.get("keep", []) if isinstance(d, dict)] +
               [dict(d, action="drop") for d in dec.get("drop", []) if isinstance(d, dict)])
    for d in raw if isinstance(raw, list) else []:
        if not isinstance(d, dict):
            ignored += 1
            continue
        eid = d.get("event_id") or d.get("id")
        action = d.get("action")
        if action not in ("keep", "drop"):
            if d.get("story") or d.get("story_id") or d.get("story_title"):
                action = "keep"
            elif str(d.get("drop", "")).lower() in ("true", "1"):
                action = "drop"
            else:
                ignored += 1
                continue
        if not eid:
            ignored += 1
            continue
        norm = {"event_id": eid, "action": action,
                "story": d.get("story") or d.get("story_id"),
                "story_title": d.get("story_title"), "reason": d.get("reason") or d.get("rationale")}
        ex = {}
        if isinstance(d.get("exploitation"), dict):
            for cve, v in d["exploitation"].items():
                if isinstance(v, str):
                    v = {"status": v}
                if isinstance(v, dict):
                    ex[cve] = v
        norm["exploitation"] = ex
        out.append(norm)
    merges = dec.get("merges", []) if isinstance(dec.get("merges", []), list) else []
    return out, merges, ignored


def _recompute_derived(story):
    """Derived fields must reflect ONLY the events a story currently holds.
    Absorb unions last_seen/cves/sources in, but strips (drop/reassign/merge)
    never rolled them back — a stripped event left its timestamp and CVEs
    behind, resurrecting dead stories in the hot scores (2026-08-24 metabase
    incident: 12-day-old story scored hot on a roundup's last_seen)."""
    last, cves, sources = "", set(), []
    for r in story.get("events", []):
        e = _read_event(r["event_id"])
        if not e:
            continue
        last = max(last, e.get("published_at", "") or "")
        cves |= set(e.get("cves") or [])
        d = _domain(e.get("url"))
        if d and d not in sources:
            sources.append(d)
    if story["events"]:
        story["last_seen"] = last or story.get("last_seen", "")
        story["cves"] = sorted(cves)
        story["sources"] = sources
    story["n_sources"] = len(story.get("sources", []))


def _strip_event_refs(stories, eid, keep_sid):
    """An event lives in exactly ONE story: drop stale references the
    mechanical merge left in other stories. Returns slugs emptied by the
    strip so callers can redirect them."""
    emptied = []
    for sid, s in stories.items():
        if sid == keep_sid or s.get("merged_into"):
            continue
        if any(r["event_id"] == eid for r in s.get("events", [])):
            s["events"] = [r for r in s["events"] if r["event_id"] != eid]
            _recompute_derived(s)          # roll back last_seen/cves/sources too
            if not s["events"]:
                emptied.append(sid)
    return emptied


def _sole_holder(stories, eid):
    """The active story whose ONLY event is this one (the mechanical merge's
    fresh mint). Reusing it instead of creating a twin prevents -2 slug
    duplicates when the LLM says NEW for an event merge.py already placed."""
    for sid, s in stories.items():
        if s.get("merged_into"):
            continue
        evs = s.get("events", [])
        if len(evs) == 1 and evs[0]["event_id"] == eid:
            return sid
    return None


def _write_event(e):
    json.dump(e, open(os.path.join(EVENTS, e["id"] + ".json"), "w"), indent=1)


def _domain(url):
    m = re.match(r"https?://(?:www\.)?([^/:]+)", url or "")
    return m.group(1).lower() if m else ""


def _absorb(story, ev, label):
    """Merge an event into a story (dedupe, update aggregate fields)."""
    refs = [r["event_id"] for r in story["events"]]
    if ev["id"] in refs:
        return False
    story["events"].append({"event_id": ev["id"], "label": label})
    d = _domain(ev.get("url"))
    if d and d not in story["sources"]:
        story["sources"].append(d)
    story["n_sources"] = len(story["sources"])
    story["cves"] = sorted(set(story.get("cves", [])) | set(ev.get("cves", [])))
    story["first_seen"] = min(story.get("first_seen", ev.get("published_at", "")),
                              ev.get("published_at", ""))
    if ev.get("published_at", "") > story.get("last_seen", ""):
        story["last_seen"] = ev["published_at"]
    return True


def _new_story(stories, title, ev, eid):
    slug = _slugify(title, set(stories))
    stories[slug] = {
        "id": slug, "title": re.sub(r"\s+", " ", title).strip(),
        "first_seen": ev.get("published_at", ""), "last_seen": ev.get("published_at", ""),
        "sources": [dom for dom in [_domain(ev.get("url"))] if dom],
        "n_sources": 1 if ev.get("url") else 0,
        "cves": ev.get("cves", []), "score": 0.0,
        "reddit_signal": {"posts": 0, "best_score": 0},
        "events": [{"event_id": eid, "label": "original"}],
    }
    return slug


def apply(decisions_path):
    if not os.path.exists(decisions_path):
        print(f"no decisions file: {decisions_path}")
        sys.exit(1)
    dec = json.load(open(decisions_path))
    state = _load_state()
    processed = set(state["processed"])
    stories = _load_stories()
    decisions, merges, ignored = _normalize_decisions(dec)
    moved = drops = 0

    for d in decisions:
        eid = d["event_id"]
        ev = _read_event(eid)
        processed.add(eid)
        if not ev:
            continue
        if d["action"] == "drop":
            ev["excluded"] = True
            ev["exclude_reason"] = d.get("reason", "")
            _write_event(ev)
            # remove from any story that references it (shouldn't happen for new
            # events, but be safe)
            _strip_event_refs(stories, eid, None)
            drops += 1
            continue
        if d["action"] != "keep":
            continue
        ev["excluded"] = False
        # exploitation assessment (optional): per-CVE map, CVE_RE-gated,
        # statuses whitelisted, source stamped so the backfill never overrides
        ex = d.get("exploitation") or {}
        assessed = {}
        for c, f in ex.items():
            if not re.fullmatch(r"CVE-\d{4}-\d{4,7}", c):
                continue
            if f.get("status") not in ("exploited", "suspected"):
                continue
            assessed[c] = {"status": f["status"],
                           "evidence": str(f.get("evidence", ""))[:400],
                           "source": "triage"}
        if assessed:
            ev["exploitation"] = assessed
        elif "exploitation" in ev:
            del ev["exploitation"]
        target = d.get("story")
        # If the mechanical merge already minted a story whose ONLY event is
        # this one, reuse it instead of creating a -2 twin (retake it, with an
        # optional cleaner title from the decision).
        sole = _sole_holder(stories, eid)
        if (not target or target == "NEW") and sole:
            target = sole
            if d.get("story_title"):
                stories[sole]["title"] = re.sub(r"\s+", " ", d["story_title"]).strip()
        if not target or target == "NEW":
            target = _new_story(stories, d.get("story_title") or ev.get("title", ""), ev, eid)
            ev["kind"] = "original"
            moved += 1
        elif target not in stories:
            print(f"  WARN: keep -> unknown story {target} for {eid}; creating")
            target = _new_story(stories, d.get("story_title") or ev.get("title", ""), ev, eid)
            ev["kind"] = "original"
            moved += 1
        else:
            changed = _absorb(stories[target], ev, "update")
            if changed:
                ev["kind"] = "update"
                moved += 1
            # Always persist: exploitation assessments and the excluded
            # flag must survive even when the event was already placed in
            # the target story (e.g. by the mechanical merge).
        _write_event(ev)
        # An event lives in exactly ONE story: strip stale references the
        # mechanical merge left behind; emptied shells redirect to the story
        # that owns the event now.
        for sid in _strip_event_refs(stories, eid, target):
            stories[sid]["merged_into"] = target

    # story merges: move all events from -> into, mark from as merged_into
    for m in merges:
        frm, into = m.get("from"), m.get("into")
        if frm not in stories or into not in stories or frm == into:
            print(f"  WARN: bad merge {frm} -> {into}")
            continue
        if stories[frm].get("merged_into"):
            print(f"  skip merge {frm} -> {into}: {frm} already merged into "
                  f"{stories[frm]['merged_into']}")
            continue
        # the target may have been emptied into another story earlier this
        # run (shell with merged_into): follow the redirect chain so events
        # land on a live canonical story, never inside a redirect shell
        seen = {frm}
        while stories[into].get("merged_into"):
            nxt = stories[into]["merged_into"]
            if nxt in seen or nxt not in stories or nxt == into:
                break
            seen.add(into)
            into = nxt
        if into == frm or stories[into].get("merged_into"):
            print(f"  WARN: merge {m.get('from')} has no live target; skipping")
            continue
        for ref in list(stories[frm].get("events", [])):
            ev = _read_event(ref["event_id"])
            if ev:
                _absorb(stories[into], ev, "update")
                ev["kind"] = "update"
                _write_event(ev)
        stories[frm]["merged_into"] = into
        stories[frm]["events"] = []
        stories[frm]["n_sources"] = 0
        _recompute_derived(stories[into])   # merged events may extend derived fields
        print(f"  merged {frm} -> {into}")

    # persist stories
    for s in stories.values():
        json.dump(s, open(os.path.join(STORIES, s["id"] + ".json"), "w"), indent=1)

    # rescore + re-emit needs-analysis
    from store import load_events
    import score as score_mod
    events = load_events()
    reddit_posts = json.load(open(os.path.join(DATA, "reddit.json"))) if os.path.exists(os.path.join(DATA, "reddit.json")) else []
    queue = []
    for s in stories.values():
        if s.get("merged_into"):
            continue
        try:
            sc = score_mod.hot_score(s, events, reddit_posts)
            s["score"] = sc["score"]
            s["score_breakdown"] = {k: v for k, v in sc.items() if k != "score"}
        except Exception as e:
            # A scoring failure for ONE story must not wipe a valid breakdown
            # or write an empty one (that crashes the SSG render and blocks the
            # whole publish). Preserve the existing breakdown/score if present;
            # otherwise fall back to a minimal zero breakdown carrying every
            # template key.
            print(f"  WARN: score {s['id']}: {e}")
            s.setdefault("score_breakdown", dict(_SB_DEFAULTS))
            s.setdefault("score", 0.0)
        # Crash-safety: guarantee every template key exists, so a stale or
        # missing-key breakdown can never take down the build.
        sb = s.get("score_breakdown")
        if not isinstance(sb, dict):
            sb = {}
            s["score_breakdown"] = sb
        missing = [k for k in _SB_KEYS if k not in sb]
        if missing:
            print(f"  WARN: {s['id']} score_breakdown missing {missing}; backfilling")
            for k in missing:
                sb[k] = _SB_DEFAULTS[k]
        s.setdefault("score", 0.0)
        json.dump(s, open(os.path.join(STORIES, s["id"] + ".json"), "w"), indent=1)
        if s["score"] >= HOT_THRESHOLD:
            ap = os.path.join(ANALYSIS, s["id"] + ".md")
            marker = (s.get("analysis") or {}).get("updated_at", "")
            if not os.path.exists(ap):
                queue.append(s["id"])
                continue
            newest = max((events.get(r["event_id"], {}).get("published_at", "")
                          for r in s.get("events", [])), default="")
            if not marker:
                import time as _t
                marker = datetime.fromtimestamp(os.path.getmtime(ap), tz=timezone.utc).isoformat()
            if newest and newest > marker:
                queue.append(s["id"])
    json.dump({"updated_at": NOW.isoformat(), "stories": queue},
              open(NEEDS, "w"), indent=1)

    state["processed"] = sorted(processed)
    _save_state(state)
    print(f"triage applied: {moved} kept/moved, {drops} dropped, {len(merges)} merges, needs-analysis {len(queue)}")
    if ignored:
        print(f"  WARN: {ignored} decision entries could not be parsed from {decisions_path}")
    if not decisions:
        print("  WARN: no keep/drop decisions recognized — schema mismatch? "
              "Expected top-level 'decisions' array with event_id/action/story keys")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: triage.py collect | apply <decisions.json>")
        sys.exit(1)
    if sys.argv[1] == "collect":
        collect()
    elif sys.argv[1] == "apply":
        apply(sys.argv[2])
    else:
        print("usage: triage.py collect | apply <decisions.json>")
        sys.exit(1)
