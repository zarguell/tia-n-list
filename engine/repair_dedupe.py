#!/usr/bin/env python3
"""One-time deterministic dedup repair for the story store.

Repairs damage left by the triage schema drift (Aug 17-24, 2026), when keeps
were misparsed as "create NEW story" and events were double-referenced:

  1. Same-slug-base active stories (foo / foo-2 / foo-3) whose titles match
     (jaccard >= 0.4) or that share an event -> merged into one canonical
     story (most events, then most sources, then earliest first_seen).
  2. Active stories sharing an event with similar titles (jaccard >= 0.30)
     -> merged the same way (e.g. two outlets' story on one incident).
  3. Remaining events referenced by several active stories -> kept in the
     story whose title is most similar to the event's, stripped elsewhere
     (an event belongs to exactly one story).

Emptied shells keep their json with "merged_into" so old URLs redirect.
Scores and the needs-analysis queue are rebuilt afterwards (same as
triage apply). Run with --dry-run to preview.

Usage: python3 repair_dedupe.py [--dry-run]
"""
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

from merge import GENERIC, DATE_STOP, _norm_tokens, _series_codes
from store import load_events

ENGINE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ENGINE, "data")
STORIES = os.path.join(DATA, "stories")
EVENTS = os.path.join(DATA, "events")
ANALYSIS = os.path.join(DATA, "analysis")
NEEDS = os.path.join(DATA, "needs-analysis.json")
HOT_THRESHOLD = 3.3


def load_stories():
    out = {}
    for f in glob.glob(os.path.join(STORIES, "*.json")):
        s = json.load(open(f))
        out[s["id"]] = s
    return out


# Title-verb filler that inflates similarity between unrelated headlines
# ("X Lets Attackers Gain..." vs "Y Lets Hackers Gain..."). Not story signal.
FILLER = {"lets", "let", "gain", "gains", "using", "use", "used", "new", "via",
          "could", "can", "from", "into", "your", "you", "their", "its", "how",
          "why", "what", "before", "after", "amid", "warns", "warn"}


def disc(title):
    return _norm_tokens(title) - GENERIC - DATE_STOP - FILLER


def jac(a, b):
    A = disc(a or "")
    B = disc(b or "")
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def distinct_codes(a, b):
    """Both titles carry advisory/vuln series codes (AV26-815, CVE-2026-19598)
    and none are shared -> different advisories, never merge (same rule as
    merge.py's clustering)."""
    ca, cb = _series_codes(a or ""), _series_codes(b or "")
    return bool(ca and cb and not (ca & cb))


def canon(group):
    return sorted(group, key=lambda s: (-len(s["events"]),
                                        -len(s.get("sources", [])),
                                        s.get("first_seen", ""),
                                        s["id"]))[0]


def merge_story(stories, frm, into, log):
    if frm == into or stories[frm].get("merged_into"):
        return
    tgt = stories[into]
    for ref in stories[frm].get("events", []):
        if any(r["event_id"] == ref["event_id"] for r in tgt["events"]):
            continue
        tgt["events"].append(ref)
    tgt["sources"] = list(dict.fromkeys(tgt.get("sources", []) + stories[frm].get("sources", [])))
    tgt["n_sources"] = len(tgt["sources"])
    tgt["cves"] = sorted(set(tgt.get("cves", [])) | set(stories[frm].get("cves", [])))
    tgt["first_seen"] = min(tgt.get("first_seen", "9999"), stories[frm].get("first_seen", "9999"))
    tgt["last_seen"] = max(tgt.get("last_seen", ""), stories[frm].get("last_seen", ""))
    stories[frm]["merged_into"] = into
    stories[frm]["events"] = []
    stories[frm]["n_sources"] = 0
    log.append(f"merge {frm} -> {into}")


def strip_double_refs(stories, events, log):
    for _ in range(5):                      # to fixpoint
        changed = False
        owners = {}
        for sid, s in stories.items():
            if s.get("merged_into"):
                continue
            for r in s.get("events", []):
                owners.setdefault(r["event_id"], set()).add(sid)
        for eid, sids in owners.items():
            if len(sids) < 2:
                continue
            ev = events.get(eid)
            ev_title = ev.get("title", "") if ev else ""
            ranked = sorted(sids, key=lambda sid: (-jac(stories[sid].get("title", ""), ev_title),
                                                   -len(stories[sid]["events"]), sid))
            keeper = ranked[0]
            for sid in ranked[1:]:
                stories[sid]["events"] = [r for r in stories[sid]["events"] if r["event_id"] != eid]
                changed = True
                if not stories[sid]["events"] and not stories[sid].get("merged_into"):
                    stories[sid]["merged_into"] = keeper
                    log.append(f"shell {sid} -> {keeper}")
        if not changed:
            break


def redirect_target(stories, sid):
    """Follow merged_into to the live canonical story; cycle-safe."""
    seen = set()
    while sid in stories and stories[sid].get("merged_into") and sid not in seen:
        seen.add(sid)
        sid = stories[sid]["merged_into"]
    return sid if sid in stories and not stories[sid].get("merged_into") else None


def break_cycles(stories, log):
    """Historic mutual merges left A->B->A pointer cycles. In each cycle the
    member with the fewest events (then lexicographic id) becomes the shell
    pointing at the cycle's other live member."""
    visited = set()
    for sid in stories:
        if sid in visited:
            continue
        chain, cur = [], sid
        while cur in stories and stories[cur].get("merged_into") and cur not in chain:
            chain.append(cur)
            cur = stories[cur]["merged_into"]
        visited.update(chain)
        if cur not in chain or cur not in stories or not stories[cur].get("merged_into"):
            continue                          # no cycle reachable from sid
        cyc = chain[chain.index(cur):] + [cur]
        members = sorted(set(cyc), key=lambda x: (len(stories[x].get("events", [])), x))
        shell, keep = members[0], members[1]
        stories[shell]["merged_into"] = keep
        stories[keep]["merged_into"] = None   # keep becomes the live canonical
        visited.update(members)
        log.append(f"cycle broken: {shell} -> {keep} (live)")


def main():
    dry = "--dry-run" in sys.argv
    stories = load_stories()
    events = load_events()
    log = []

    # 0a. merged_into pointer cycles first: redirects must terminate
    break_cycles(stories, log)

    # 0b. shells that still hold events (a mechanical merge once deposited
    # into a merged-away story): move them to the redirect target
    for s in stories.values():
        tgt = redirect_target(stories, s.get("merged_into")) if s.get("merged_into") else None
        if not tgt or not s.get("events"):
            continue
        moved_n = 0
        for ref in s["events"]:
            if not any(r["event_id"] == ref["event_id"] for r in stories[tgt]["events"]):
                stories[tgt]["events"].append(ref)
                moved_n += 1
        s["events"] = []
        s["n_sources"] = 0
        log.append(f"shell {s['id']} -> {tgt} (recovered {moved_n} event refs)")

    # 1. same-slug-base duplicate groups
    by_base = {}
    for s in stories.values():
        if not s.get("merged_into") and s.get("events"):
            by_base.setdefault(re.sub(r"-\d+$", "", s["id"]), []).append(s)
    for base, group in by_base.items():
        if len(group) < 2:
            continue
        ids = [s["id"] for s in group]
        c = canon(group)
        for s in group:
            shares = bool({r["event_id"] for r in s["events"]} &
                          {r["event_id"] for r in c["events"]})
            same_advisory = distinct_codes(s["title"], c["title"])
            if s is not c and not same_advisory and (jac(s["title"], c["title"]) >= 0.4 or shares):
                merge_story(stories, s["id"], c["id"], log)

    # 2. shared-event + similar-title pairs
    for _ in range(5):
        owners = {}
        for sid, s in stories.items():
            if s.get("merged_into"):
                continue
            for r in s.get("events", []):
                owners.setdefault(r["event_id"], set()).add(sid)
        pairs = set()
        for sids in owners.values():
            if len(sids) > 1:
                sids = sorted(sids)
                for i in range(len(sids)):
                    for j in range(i + 1, len(sids)):
                        pairs.add((sids[i], sids[j]))
        changed = False
        for a, b in pairs:
            if stories[a].get("merged_into") or stories[b].get("merged_into"):
                continue
            ta, tb = stories[a]["title"], stories[b]["title"]
            # >= 2 shared discriminators (not filler verbs) + similarity floor:
            # a shared roundup event alone is NOT evidence of same story
            if len(disc(ta) & disc(tb)) >= 2 and jac(ta, tb) >= 0.30 \
                    and not distinct_codes(ta, tb):
                c = canon([stories[a], stories[b]])
                other = b if c["id"] == a else a
                merge_story(stories, other, c["id"], log)
                changed = True
        if not changed:
            break

    # 3. remaining double-referenced events -> single owner
    strip_double_refs(stories, events, log)

    print(f"repair: {len(log)} actions")
    for line in log:
        print(" ", line)
    if dry:
        print("dry-run: nothing written")
        return

    import score as score_mod
    reddit_posts = json.load(open(os.path.join(DATA, "reddit.json"))) \
        if os.path.exists(os.path.join(DATA, "reddit.json")) else []
    queue = []
    for s in stories.values():
        json.dump(s, open(os.path.join(STORIES, s["id"] + ".json"), "w"), indent=1)
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
            if newest and newest > marker:
                queue.append(s["id"])
    json.dump({"updated_at": datetime.now(timezone.utc).isoformat(), "stories": queue},
              open(NEEDS, "w"), indent=1)
    print(f"repair: rescored, needs-analysis {len(queue)}")


if __name__ == "__main__":
    main()
