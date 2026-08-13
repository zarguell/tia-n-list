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
NEEDS = os.path.join(DATA, "needs-analysis.json")
ANALYSIS = os.path.join(DATA, "analysis")
HOT_THRESHOLD = 2.0

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

    os.makedirs(TRIAGE, exist_ok=True)
    ctx = {
        "date": TODAY,
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
            "CVEs. Omit the exploitation field when the event makes no claim."),
        "new_events": [{
            "id": e["id"], "title": e.get("title", ""),
            "source": e.get("source", ""), "published_at": e.get("published_at", ""),
            "cves": e.get("cves", []),
            "snippet": (e.get("content_md") or "")[:220].replace("\n", " "),
        } for e in recent],
        "candidate_stories": [{
            "id": s["id"], "title": s.get("title", ""),
            "n_events": len(s.get("events", [])), "last_seen": s.get("last_seen", ""),
            "first_event_title": (next((x.get("title", "") for x in s.get("events", [])), "")),
        } for s in cands],
    }
    path = os.path.join(TRIAGE, f"context-{TODAY}.json")
    json.dump(ctx, open(path, "w"), indent=1)
    print(f"triage: {len(recent)} new events (48h window, capped), {len(cands)} candidate stories -> {path}")


def _read_event(eid):
    p = os.path.join(EVENTS, eid + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


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


def apply(decisions_path):
    if not os.path.exists(decisions_path):
        print(f"no decisions file: {decisions_path}")
        sys.exit(1)
    dec = json.load(open(decisions_path))
    state = _load_state()
    processed = set(state["processed"])
    stories = _load_stories()
    moved = drops = 0

    for d in dec.get("decisions", []):
        eid = d.get("event_id")
        if not eid:
            continue
        ev = _read_event(eid)
        processed.add(eid)
        if not ev:
            continue
        if d.get("action") == "drop":
            ev["excluded"] = True
            ev["exclude_reason"] = d.get("reason", "")
            _write_event(ev)
            # remove from any story that references it (shouldn't happen for new
            # events, but be safe)
            for s in stories.values():
                if any(r["event_id"] == eid for r in s.get("events", [])):
                    s["events"] = [r for r in s["events"] if r["event_id"] != eid]
                    json.dump(s, open(os.path.join(STORIES, s["id"] + ".json"), "w"), indent=1)
            drops += 1
            continue
        if d.get("action") != "keep":
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
        if not target or target == "NEW":
            title = d.get("story_title") or ev.get("title", "")
            slug = _slugify(title, set(stories))
            stories[slug] = {
                "id": slug, "title": re.sub(r"\s+", " ", title).strip(),
                "first_seen": ev.get("published_at", ""), "last_seen": ev.get("published_at", ""),
                "sources": [d for d in [_domain(ev.get("url"))] if d],
                "n_sources": 1 if ev.get("url") else 0,
                "cves": ev.get("cves", []), "score": 0.0,
                "reddit_signal": {"posts": 0, "best_score": 0},
                "events": [{"event_id": eid, "label": "original"}],
            }
            ev["kind"] = "original"
            _write_event(ev)
            moved += 1
        else:
            if target not in stories:
                print(f"  WARN: keep -> unknown story {target} for {eid}; creating")
                title = d.get("story_title") or ev.get("title", "")
                slug = _slugify(title, set(stories))
                stories[slug] = {
                    "id": slug, "title": re.sub(r"\s+", " ", title).strip(),
                    "first_seen": ev.get("published_at", ""), "last_seen": ev.get("published_at", ""),
                    "sources": [d for d in [_domain(ev.get("url"))] if d],
                    "n_sources": 1 if ev.get("url") else 0,
                    "cves": ev.get("cves", []), "score": 0.0,
                    "reddit_signal": {"posts": 0, "best_score": 0},
                    "events": [{"event_id": eid, "label": "original"}],
                }
                ev["kind"] = "original"
                _write_event(ev)
            else:
                changed = _absorb(stories[target], ev, "update")
                if changed:
                    ev["kind"] = "update"
                    _write_event(ev)
                    moved += 1

    # story merges: move all events from -> into, mark from as merged_into
    for m in dec.get("merges", []):
        frm, into = m.get("from"), m.get("into")
        if frm not in stories or into not in stories or frm == into:
            print(f"  WARN: bad merge {frm} -> {into}")
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
        except Exception as e:
            print(f"  WARN: score {s['id']}: {e}")
            sc = {"score": 0.0}
        s["score"] = sc["score"]
        s["score_breakdown"] = {k: v for k, v in sc.items() if k != "score"}
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
    print(f"triage applied: {moved} kept/moved, {drops} dropped, {len(dec.get('merges', []))} merges, needs-analysis {len(queue)}")


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
