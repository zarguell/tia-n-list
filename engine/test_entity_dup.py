#!/usr/bin/env python3
"""Entity dup probe + score-0 sweep contract suite (2026-10-20 owner decision
eda9f1100d5d, audit Issue 3 / Recs 2 & 3).

The title-jaccard probe (duplicate_suspects, floor 0.5) cannot see reworded
headlines: the live residual pairs OpenCode / AOMEI / Ahold Delhaize /
NightmareStresser are real duplicates it missed, and the score-0.0 backlog
(Trezor / BambooToken / NightmareStresser) was never merged because the human
2-merge/day budget always went to visible pairs. This suite pins:

  1. entity_dup_suspects catches a reworded pair (OpenCode-like fixture:
     jaccard ~0.17, same victim entity, distinctive tokens via the entity set,
     first_seen 3d apart) that duplicate_suspects does NOT surface.
  2. distinct incidents sharing boilerplate are not paired.
  3. disjoint CVE sets (both sides carrying CVEs) are exonerated.
  4. sweep_score0_merges drains a Trezor-like trio meeting every predicate
     (score 0, jaccard >= 0.5, no analysis, no digest ref): losers keep their
     json with merged_into + 0 events, winner absorbs events + derived fields.
  5. the sweep refuses analysis-file / digest-referenced / score>0 /
     distinct-CVE pairs.
  6. a second run immediately after merges is a no-op (idempotent).
  7. the per-invocation cap holds.

Run: /home/zach/.local/venvs/tia-engine/bin/python engine/test_entity_dup.py
     (from the repo/worktree root; exit 0 = pass)
"""
import glob
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import merge  # noqa: E402
import audit_checks as jc  # noqa: E402

NOW = datetime(2026, 10, 25, 12, 0, tzinfo=timezone.utc)
failures = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


def story(sid, title, first_seen, last_seen=None, cves=None, score=0.0,
          n_events=1, merged_into=None):
    return {"id": sid, "title": title, "cves": list(cves or []),
            "score": score, "first_seen": first_seen,
            "last_seen": last_seen or first_seen,
            "sources": ["example.com"], "n_sources": 1,
            "events": [{"event_id": f"{sid}-e{i}", "label": "original"}
                       for i in range(n_events)],
            **({"merged_into": merged_into} if merged_into else {})}


def pair_keys(pairs):
    return {frozenset((p["a"], p["b"])) for p in pairs}


# ── 1. the probe catches a reworded pair the title probe cannot see ──────
print("1. entity probe: reworded OpenCode-like pair")

REWORD = {
    "opencode-hack": story(
        "opencode-hack",
        "OpenCode hack exposes API keys amid AI distillation attacks",
        "2026-10-19T15:57:09Z", last_seen="2026-10-24T10:00:00Z", n_events=2),
    "opencode-guidance": story(
        "opencode-guidance",
        "Opencode API Key Breach Response Guidance",
        "2026-10-22T09:45:06Z", last_seen="2026-10-23T10:00:00Z", n_events=1),
}
title_probe = jc.duplicate_suspects(REWORD, NOW)
check("title probe (floor 0.5) misses the reworded pair", title_probe, [])
entity = merge.entity_dup_suspects(REWORD, NOW)
check("entity probe surfaces exactly the pair", len(entity), 1)
p = entity[0]
check("pair members (pool is id-sorted)", (p["a"], p["b"]),
      ("opencode-guidance", "opencode-hack"))
check("shared entity includes opencode", "opencode" in p["shared_entities"], True)
check("distinctive bar met via the entity set (api < 4 chars)",
      p["shared_tokens"] + len(p["shared_entities"]) >= 2, True)
check("first_seen gap days", p["first_seen_gap_days"], 2)
check("title probe already-surfaced pairs can be excluded",
      merge.entity_dup_suspects(REWORD, NOW,
                                exclude=pair_keys(title_probe + entity)), [])
check("merged-away shell never surfaces",
      merge.entity_dup_suspects(
          {"opencode-hack": REWORD["opencode-hack"],
           "opencode-guidance": story("opencode-guidance", "Opencode API Key "
                                      "Breach Response Guidance",
                                      "2026-10-22T09:45:06Z",
                                      merged_into="opencode-hack")}, NOW), [])
check("outside the 10-day first_seen window never surfaces",
      merge.entity_dup_suspects(
          {"opencode-hack": REWORD["opencode-hack"],
           "opencode-guidance": story("opencode-guidance",
                                      "Opencode API Key Breach Response Guidance",
                                      "2026-11-05T09:45:06Z")}, NOW), [])

# ── 2. distinct incidents sharing boilerplate are not paired ─────────────
print("2. entity probe: boilerplate-sharing distinct incidents")
BOILER = {
    "frappe-lms": story(
        "frappe-lms",
        "Frappe LMS remote code execution flaw exploited in attacks",
        "2026-10-20T00:00:00Z"),
    "ibm-mq": story(
        "ibm-mq",
        "IBM MQ remote code execution flaw exploited in attacks",
        "2026-10-21T00:00:00Z"),
    "canvas-auth": story(
        "canvas-auth",
        "Researchers detail Canvas LMS authentication bypass",
        "2026-10-20T00:00:00Z"),
    "ibm-auth": story(
        "ibm-auth",
        "Analysts chart IBM MQ authentication bypass",
        "2026-10-21T00:00:00Z"),
}
check("distinct incidents sharing boilerplate not surfaced",
      merge.entity_dup_suspects(BOILER, NOW), [])

# ── 3. disjoint CVE sets (both sides carrying) are exonerated ────────────
print("3. entity probe: distinct CVE sets exonerated")
CVE_FIX = {
    "cve-side-a": story("cve-side-a",
                        "AcmeVPN gateway flaw lets attackers hijack sessions",
                        "2026-10-20T00:00:00Z", cves=["CVE-2026-0001"]),
    "cve-side-b": story("cve-side-b",
                        "AcmeVPN client flaw lets attackers hijack sessions",
                        "2026-10-22T00:00:00Z", cves=["CVE-2026-0002"]),
    "cve-side-c": story("cve-side-c",
                        "AcmeVPN client flaw lets attackers hijack sessions",
                        "2026-10-22T00:00:00Z", cves=[]),
}
check("disjoint CVE sets (both sides carry) exonerated",
      [p for p in merge.entity_dup_suspects(CVE_FIX, NOW)
       if frozenset((p["a"], p["b"])) == frozenset(("cve-side-a",
                                                    "cve-side-b"))], [])
check("one-side-empty CVE pair still surfaces",
      len([p for p in merge.entity_dup_suspects(CVE_FIX, NOW)
           if frozenset((p["a"], p["b"])) == frozenset(("cve-side-a",
                                                        "cve-side-c"))]), 1)

# ── 4-7. the score-0 sweep ───────────────────────────────────────────────
def sweep_env(titles_scores=None, extra_files=None, cves=None):
    """Temp data dir with stories/ digests/ analysis/; returns (paths, stories,
    events). titles_scores: {sid: (title, score, n_events)}."""
    root = tempfile.mkdtemp(prefix="tia-sweep-test-")
    for d in ("stories", "digests", "analysis"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    titles_scores = titles_scores or {}
    stories, events = {}, {}
    for sid, (title, score, n_events) in titles_scores.items():
        s = story(sid, title, "2026-09-11T07:55:15Z", cves=(cves or {}).get(sid),
                  score=score, n_events=n_events)
        stories[sid] = s
        json.dump(s, open(os.path.join(root, "stories", sid + ".json"), "w"),
                  indent=1)
        for i in range(n_events):
            eid = f"{sid}-e{i}"
            events[eid] = {"id": eid, "title": title,
                           "url": f"https://{sid}.example.com/{i}",
                           "published_at": f"2026-09-1{i}T07:55:15Z",
                           "cves": list((cves or {}).get(sid) or []),
                           "content_md": ""}
    for path, content in (extra_files or {}).items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)
    return root, stories, events


TRIO = {
    "trezor-a": ("Trezor: 347,000 users targeted in phishing attacks after "
                 "Brevo breach", 0.0, 3),
    "trezor-b": ("Trezor 347K users targeted in phishing after Brevo data "
                 "breach", 0.0, 1),
    "trezor-c": ("Trezor Phishing Campaign Affects 347,000 Users After "
                 "Brevo Hack", 0.0, 1),
}

print("4. sweep drains a Trezor-like trio meeting every predicate")
root, stories, events = sweep_env(TRIO)
cands = merge.score0_sweep_candidates(stories, analysis_dir=os.path.join(root, "analysis"),
                                      digest_dir=os.path.join(root, "digests"), now=NOW)
check("candidates found", len(cands), 2)
log = merge.sweep_score0_merges(stories, events, stories_dir=os.path.join(root, "stories"),
                                analysis_dir=os.path.join(root, "analysis"),
                                digest_dir=os.path.join(root, "digests"),
                                reddit_posts=[], now=NOW)
merges = [l for l in log if l.startswith("merge ")]
check("exactly 2 merges for the trio", len(merges), 2)
check("loser b shell keeps json with merged_into",
      stories["trezor-b"]["merged_into"], "trezor-a")
check("loser c shell keeps json with merged_into",
      stories["trezor-c"]["merged_into"], "trezor-a")
check("loser events emptied (old URL redirects)",
      (stories["trezor-b"]["events"], stories["trezor-c"]["events"]), ([], []))
check("winner absorbed all events",
      len(stories["trezor-a"]["events"]), 5)
check("both merges logged with both slugs",
      all(("trezor-a" in l and l.split()[1] in ("trezor-b", "trezor-c"))
          for l in merges), True)
on_disk = json.load(open(os.path.join(root, "stories", "trezor-b.json")))
check("loser shell written to disk", on_disk.get("merged_into"), "trezor-a")
win_disk = json.load(open(os.path.join(root, "stories", "trezor-a.json")))
check("winner written with rescored breakdown",
      "score_breakdown" in win_disk and "score" in win_disk, True)
check("winner derived cves rolled up from events",
      win_disk["cves"], [])
check("winner derived last_seen is max event ts",
      win_disk["last_seen"] == max(e["published_at"] for e in events.values()), True)

print("5. sweep refusal predicates")


def merged_sides(log):
    return [l.split()[1] for l in log if l.startswith("merge ")]


# analysis file on one side: the PAIR with the analyzed story refuses; the
# remaining predicate-meeting pairs still merge (bounded, per-pair gates)
root2, st2, ev2 = sweep_env(TRIO, extra_files={"analysis/trezor-b.md": "# x"})
log2 = merge.sweep_score0_merges(st2, ev2, stories_dir=os.path.join(root2, "stories"),
                                 analysis_dir=os.path.join(root2, "analysis"),
                                 digest_dir=os.path.join(root2, "digests"),
                                 reddit_posts=[], now=NOW)
check("analysis file refuses that story",
      "trezor-b" in merged_sides(log2), False)
check("unanalyzed sibling still merges",
      "trezor-c" in merged_sides(log2), True)
root2b, st2b, ev2b = sweep_env(TRIO, extra_files={"analysis/trezor-a.md": "# x"})
log2b = merge.sweep_score0_merges(st2b, ev2b, stories_dir=os.path.join(root2b, "stories"),
                                  analysis_dir=os.path.join(root2b, "analysis"),
                                  digest_dir=os.path.join(root2b, "digests"),
                                  reddit_posts=[], now=NOW)
check("analysis file on the WINNER side refuses",
      [l for l in log2b if l.startswith("merge ")], [])
# digest reference: md slate link + json sidecar stories + overrides
root3, st3, ev3 = sweep_env(
    TRIO,
    extra_files={"digests/2026-10-20.md":
                 "body [link](stories/trezor-c/) more\n"})
log3 = merge.sweep_score0_merges(st3, ev3, stories_dir=os.path.join(root3, "stories"),
                                 analysis_dir=os.path.join(root3, "analysis"),
                                 digest_dir=os.path.join(root3, "digests"),
                                 reddit_posts=[], now=NOW)
check("digest md link refuses that story",
      "trezor-c" in merged_sides(log3), False)
check("unreferenced sibling still merges",
      "trezor-b" in merged_sides(log3), True)
root3b, st3b, ev3b = sweep_env(
    TRIO,
    extra_files={"digests/2026-10-21.json":
                 json.dumps({"date": "2026-10-21", "stories": ["trezor-c"],
                             "overrides": []})})
log3b = merge.sweep_score0_merges(st3b, ev3b, stories_dir=os.path.join(root3b, "stories"),
                                  analysis_dir=os.path.join(root3b, "analysis"),
                                  digest_dir=os.path.join(root3b, "digests"),
                                  reddit_posts=[], now=NOW)
check("digest json slate refuses that story",
      "trezor-c" in merged_sides(log3b), False)
root3c, st3c, ev3c = sweep_env(
    TRIO,
    extra_files={"digests/2026-10-21.json":
                 json.dumps({"date": "2026-10-21", "stories": [],
                             "overrides": [{"action": "demote",
                                            "slug": "trezor-c", "why": "x"}]})})
log3c = merge.sweep_score0_merges(st3c, ev3c, stories_dir=os.path.join(root3c, "stories"),
                                  analysis_dir=os.path.join(root3c, "analysis"),
                                  digest_dir=os.path.join(root3c, "digests"),
                                  reddit_posts=[], now=NOW)
check("digest json override refuses that story",
      "trezor-c" in merged_sides(log3c), False)
# score > 0 on either side
root4, st4, ev4 = sweep_env(dict(TRIO, **{"trezor-b": (TRIO["trezor-b"][0], 0.4, 1)}))
log4 = merge.sweep_score0_merges(st4, ev4, stories_dir=os.path.join(root4, "stories"),
                                 analysis_dir=os.path.join(root4, "analysis"),
                                 digest_dir=os.path.join(root4, "digests"),
                                 reddit_posts=[], now=NOW)
check("score > 0 refuses that story", "trezor-b" in merged_sides(log4), False)
root4b, st4b, ev4b = sweep_env(dict(TRIO, **{"trezor-a": (TRIO["trezor-a"][0], 2.0, 3)}))
log4b = merge.sweep_score0_merges(st4b, ev4b, stories_dir=os.path.join(root4b, "stories"),
                                  analysis_dir=os.path.join(root4b, "analysis"),
                                  digest_dir=os.path.join(root4b, "digests"),
                                  reddit_posts=[], now=NOW)
check("score > 0 on the winner side refuses",
      [l for l in log4b if l.startswith("merge ")], [])
# distinct CVE sets
root5, st5, ev5 = sweep_env(
    dict(TRIO), cves={"trezor-a": ["CVE-2026-1111"], "trezor-b": ["CVE-2026-2222"]})
log5 = merge.sweep_score0_merges(st5, ev5, stories_dir=os.path.join(root5, "stories"),
                                 analysis_dir=os.path.join(root5, "analysis"),
                                 digest_dir=os.path.join(root5, "digests"),
                                 reddit_posts=[], now=NOW)
check("distinct CVE sets refuse", [l for l in log5 if l.startswith("merge ")], [])

print("6. sweep idempotence: immediate second run merges nothing")
win_path = os.path.join(root, "stories", "trezor-a.json")
before = open(win_path).read()
reloaded = {}
for f in glob.glob(os.path.join(root, "stories", "*.json")):
    s = json.load(open(f))
    reloaded[s["id"]] = s
log6 = merge.sweep_score0_merges(reloaded, events, stories_dir=os.path.join(root, "stories"),
                                 analysis_dir=os.path.join(root, "analysis"),
                                 digest_dir=os.path.join(root, "digests"),
                                 reddit_posts=[], now=NOW)
check("second run merges nothing", [l for l in log6 if l.startswith("merge ")], [])
after = open(win_path).read()
if before != after:
    import hashlib
    print(f"    DEBUG before sha {hashlib.md5(before.encode()).hexdigest()} "
          f"after sha {hashlib.md5(after.encode()).hexdigest()}")
    for off, (cb, ca) in enumerate(zip(before, after)):
        if cb != ca:
            print(f"    DEBUG first diff at offset {off}: "
                  f"{before[max(0, off-40):off+40]!r} vs {after[max(0, off-40):off+40]!r}")
            break
check("winner file untouched by second run", before, after)

print("7. sweep cap respected")
STAR = {"star-w": ("WhisperRat campaign hits embassies with phishing lure",
                   0.0, 5)}
for i in range(1, 5):
    STAR[f"star-l{i}"] = (f"WhisperRat campaign hits embassies with phishing "
                          f"lure variant {i}", 0.0, 1)
root7, st7, ev7 = sweep_env(STAR)
cands7 = merge.score0_sweep_candidates(st7, analysis_dir=os.path.join(root7, "analysis"),
                                       digest_dir=os.path.join(root7, "digests"), now=NOW)
check("star pool builds all pairwise candidates", len(cands7), 10)
log7 = merge.sweep_score0_merges(st7, ev7, stories_dir=os.path.join(root7, "stories"),
                                 analysis_dir=os.path.join(root7, "analysis"),
                                 digest_dir=os.path.join(root7, "digests"),
                                 reddit_posts=[], now=NOW, cap=2)
check("cap limits merges to 2", len([l for l in log7 if l.startswith("merge ")]), 2)
merged_cnt = sum(1 for s in st7.values() if s.get("merged_into"))
check("exactly 2 shells after capped run", merged_cnt, 2)

for d in (root, root2, root2b, root3, root3b, root3c, root4, root4b, root5,
          root7):
    shutil.rmtree(d, ignore_errors=True)

print()
if failures:
    print(f"FAIL: {len(failures)} checks failed: {failures}")
    sys.exit(1)
print("ALL PASS")
