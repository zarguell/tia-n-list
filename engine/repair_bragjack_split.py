#!/usr/bin/env python3
"""Bounded split repair for the BragJack over-merge (2026-11-06 audit Rec 6,
owner decision 44e6933152d1).

One story — `1-basic-information-original-title-bragjack-technical-overview-h`
— bundled a rolling author series: five unrelated dev.to campaigns (KREMLIN,
Chosen Brick/Telegram-C2, WaterPlum, Rapuncel and the AI-agent retail
card-theft piece) were attached to the BragJack prompt-forcing story, and the
published prose had to narrate all of them under a BragJack title because the
data said they were one incident. The detector half of the 10-19 fix landed
(aggregator_series_suspects / same_disclosure_suspects); this is the data half.

What it does, and only this:

  * keeps the story's BragJack events (any event whose title or URL says
    BragJack — the cybersecuritynews.com coverage and the dev.to technical
    overview) with the story, and re-titles the story to that claim;
  * re-owns every OTHER event in the story to its own new story, one per
    component, with a story id derived from that event's cleaned title
    (dev.to scaffolding, "Original Title:" prefixes and trailing hashtags
    stripped — the raw titles are collector artifacts, not claims);
  * rebuilds derived fields for the touched stories and rescores them.

Nothing is deleted. The original story stays live (it keeps the BragJack
events), so this case creates no redirect shell; the standing rule still holds
for every other outcome — an over-merge loser keeps its json with
`merged_into` and is never unlinked, because old URLs must keep resolving.

Bounds (deliberate): exactly one target story, `--dry-run` by default, writes
only the touched story files + the new story files, never touches event
records' content, never re-runs the whole store, idempotent (a second --apply
finds nothing to split).

Usage:
  python3 engine/repair_bragjack_split.py             # dry run, prints the plan
  python3 engine/repair_bragjack_split.py --apply     # write the split
  python3 engine/repair_bragjack_split.py --apply --stories-dir DIR --events-dir DIR
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_registry import domain_of                       # noqa: E402
from merge import build_slug, _display_title               # noqa: E402
from repair_dedupe import recompute_derived_fields         # noqa: E402
from score import backfill_score_breakdown, hot_score      # noqa: E402
from store import safe_url, write_json                     # noqa: E402

DATA = os.path.join(HERE, "data")
STORIES = os.path.join(DATA, "stories")
EVENTS = os.path.join(DATA, "events")

TARGET = "1-basic-information-original-title-bragjack-technical-overview-h"

BRAGJACK_RE = re.compile(r"\bbragjack\b", re.I)
# dev.to repost scaffolding the collector carries verbatim: "1. Basic
# Information", "1. Overview", "Original Title:", a truncated headline and the
# author's hashtag tail.
SCAFFOLD_RE = re.compile(
    r"^\s*(?:\d+\.\s*)?(?:basic information|overview|summary|key points|"
    r"introduction|technical overview)\b[\s:.\u2014-]*", re.I)
ORIGINAL_TITLE_RE = re.compile(r"^\s*original title\s*[:\u2014-]\s*", re.I)
HASHTAG_TAIL_RE = re.compile(r"(?:\s*#\s*[A-Za-z0-9_]+)+\s*$")
ELLIPSIS_TAIL_RE = re.compile(r"[\s.]*\u2026?\s*\.\.\.\s*$")


def clean_claim(title):
    """The claim a dev.to repost's title actually makes: scaffolding, the
    'Original Title:' marker, the author's hashtag tail and the collector's
    truncation ellipsis stripped. Used for the NEW story ids/titles (event
    titles stay as collected — the store's raw record is not rewritten)."""
    t = HASHTAG_TAIL_RE.sub("", title or "")
    prev = None
    while prev != t:                 # "1. Basic Information Original Title: X"
        prev = t
        t = ORIGINAL_TITLE_RE.sub("", t)
        t = SCAFFOLD_RE.sub("", t)
    t = ELLIPSIS_TAIL_RE.sub("", t)
    return re.sub(r"\s+", " ", t).strip(" -:|\u2014")


def is_bragjack(ev):
    return bool(BRAGJACK_RE.search(ev.get("title") or "")
                or BRAGJACK_RE.search(ev.get("url") or ""))


def load_story(stories_dir, story_id):
    with open(os.path.join(stories_dir, story_id + ".json")) as fh:
        return json.load(fh)


def load_event(events_dir, eid):
    """Event meta + .md sidecar content, mirroring store.load_events for ONE
    event (the repair is bounded; it never loads the whole store)."""
    with open(os.path.join(events_dir, eid + ".json")) as fh:
        ev = json.load(fh)
    md = os.path.join(events_dir, eid + ".md")
    ev["content_md"] = open(md).read() if os.path.exists(md) else ""
    ev["url"] = safe_url(ev.get("url") or "")
    return ev


def taken_ids(stories_dir):
    return {json.load(open(f))["id"]
            for f in glob.glob(os.path.join(stories_dir, "*.json"))}


def build_plan(stories_dir, events_dir, story_id=TARGET):
    """(story, keep_refs, moves) — moves = [(event_id, event, new_id, title)].
    Raises SystemExit-ready ValueError on an unusable target (missing story,
    redirect shell, unknown event) rather than guessing."""
    path = os.path.join(stories_dir, story_id + ".json")
    if not os.path.exists(path):
        raise ValueError(f"target story not found: {path}")
    story = load_story(stories_dir, story_id)
    if story.get("merged_into"):
        raise ValueError(f"target {story_id} is a redirect shell "
                         f"(merged_into={story['merged_into']}); restore it "
                         f"first, this repair only splits live stories")
    taken = taken_ids(stories_dir)
    keep, moves = [], []
    for ref in story.get("events", []):
        ev = load_event(events_dir, ref["event_id"])
        if is_bragjack(ev):
            keep.append(ref)
            continue
        claim = clean_claim(ev.get("title") or ref["event_id"])
        new_id = build_slug(claim or ref["event_id"], taken)
        taken.add(new_id)
        moves.append((ref["event_id"], ev, new_id, _display_title(claim)
                      or claim or ref["event_id"]))
    return story, keep, moves


def bragjack_title(pairs, story):
    """The BragJack claim the story is retitled to: the cybersecuritynews.com
    headline when that event is present (the note names it), else the first
    retained BragJack event's display title, else the current title.

    `pairs` = [(ref, event)] for the retained events."""
    events = [ev for _ref, ev in pairs]
    for ev in events:
        if "cybersecuritynews.com" in (ev.get("source") or ""):
            return _display_title(ev.get("title") or "")
    if events:
        return _display_title(events[0].get("title") or "")
    return story.get("title", "")


def apply_plan(stories_dir, events_dir, story, keep, moves, out=print):
    """Write the split. Returns the list of story ids written."""
    events = {}
    for ref in story.get("events", []):
        events[ref["event_id"]] = load_event(events_dir, ref["event_id"])

    # retained BragJack events keep their refs (and labels) verbatim: the
    # split only removes the events that never belonged to the claim.
    keep_pairs = [(ref, events[ref["event_id"]]) for ref in keep]
    story["events"] = list(keep)
    claim = bragjack_title(keep_pairs, story)
    if claim:
        story["title"] = claim

    created = {}
    for eid, ev, new_id, title in moves:
        ev["kind"] = "original"
        created[new_id] = {
            "id": new_id,
            "title": title,
            "first_seen": ev.get("published_at") or "",
            "last_seen": ev.get("published_at") or "",
            "sources": [domain_of(ev.get("url"))] if ev.get("url") else [],
            "n_sources": 1 if ev.get("url") else 0,
            "cves": list(ev.get("cves") or []),
            "score": 0.0,
            "reddit_signal": {"posts": 0, "best_score": 0},
            "events": [{"event_id": eid, "label": "original"}],
        }

    touched = {story["id"]: story, **created}
    recompute_derived_fields(touched, events)
    for sid, s in touched.items():
        sc = hot_score(s, events, _social_posts())
        s["score"] = sc["score"]
        s["score_breakdown"] = {k: v for k, v in sc.items() if k != "score"}
        backfill_score_breakdown(s)
        s.setdefault("score", 0.0)
        write_json(os.path.join(stories_dir, sid + ".json"), s)
        out(f"  wrote {sid}  score {s['score']}  events {len(s['events'])}")

    for eid, ev, _new_id, _title in moves:
        # rewrite ONLY the event's own file, kind flipped to "original" (its
        # new story's founding event): every other key the collector wrote
        # (content_md among them) is preserved verbatim — this repair never
        # rewrites event content.
        path = os.path.join(events_dir, eid + ".json")
        with open(path) as fh:
            raw = json.load(fh)
        raw["kind"] = "original"
        write_json(path, raw)

    return sorted(touched)


def _social_posts():
    from store import load_social_posts
    try:
        return load_social_posts()
    except Exception:
        return []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true",
                    help="write the split (default: dry run, nothing written)")
    ap.add_argument("--stories-dir", default=STORIES)
    ap.add_argument("--events-dir", default=EVENTS)
    ap.add_argument("--story", default=TARGET)
    args = ap.parse_args(argv)

    try:
        story, keep, moves = build_plan(args.stories_dir, args.events_dir,
                                        args.story)
    except ValueError as exc:
        print(f"refusing: {exc}")
        return 2

    print(f"story: {story['id']} ({len(story.get('events', []))} events)")
    print(f"retain as BragJack ({len(keep)}):")
    for ref in keep:
        print(f"  {ref['event_id']}  {ref['label']}")
    print(f"re-own to their own stories ({len(moves)}):")
    for eid, ev, new_id, title in moves:
        print(f"  {eid}  ->  {new_id}\n      {title}")
    if not moves:
        print("nothing to split (idempotent)")
        return 0
    if not keep:
        print("refusing: no BragJack event to retain — the target no longer "
              "holds the claim this repair is scoped to")
        return 2
    print(f"retitle: {bragjack_title([(r, load_event(args.events_dir, r['event_id'])) for r in keep], story)}")

    if not args.apply:
        print("dry-run: nothing written (pass --apply)")
        return 0
    print("applying:")
    apply_plan(args.stories_dir, args.events_dir, story, keep, moves)
    print(f"split done: {len(moves)} new stories, {len(keep)} events retained")
    return 0


if __name__ == "__main__":
    sys.exit(main())
