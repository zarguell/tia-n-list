#!/usr/bin/env python3
"""Contract suite for engine/repair_bragjack_split.py (2026-11-06 audit Rec 6,
owner decision 44e6933152d1).

Pins the bounded split of the BragJack over-merge:

  1. `--dry-run` (the default) writes nothing.
  2. `--apply` keeps the BragJack events on the story (retitled to the
     cybersecuritynews.com claim) and re-owns each unrelated author-series
     event — KREMLIN, Chosen Brick/Telegram-C2, WaterPlum, Rapuncel,
     AI-agent retail card theft — to its own story, with an id derived from
     that event's title and no dev.to scaffolding / hashtag tail in it.
  3. No story file is deleted, every event keeps exactly one owner, and the
     derived fields of every touched story match its own events.
  4. A second `--apply` is a no-op ("nothing to split").
  5. A redirect shell or a story with no BragJack claim is refused, not
     guessed at.

Run: python3 engine/test_repair_bragjack_split.py   (exit 0 = pass)
"""
import glob
import hashlib
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repair_bragjack_split as rb  # noqa: E402

failures = []


def snapshot(dirpath):
    """{filename: content sha1} — compares "nothing was written" without
    dumping whole story records into the log."""
    out = {}
    for p in sorted(glob.glob(os.path.join(dirpath, "*.json"))):
        out[os.path.basename(p)] = hashlib.sha1(
            open(p, "rb").read()).hexdigest()
    return out


def check(name, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {want!r}")
    if not ok:
        failures.append(name)


STORY = "1-basic-information-original-title-bragjack-technical-overview-h"

# (event id, source, title, url) — the live story's six events plus the
# AI-agent retail piece the published prose narrated (an author-series repost
# that belongs to no BragJack claim either).
EVENTS = [
    ("masto:1", "dev.to",
     "1. Basic Information Original Title: BragJack [Technical Overview]: "
     "How We Hijacked Top 5... # security # threatintel # software # coding",
     "https://dev.to/anoymask/bragjack-prompt-forcing-1d67"),
    ("masto:2", "dev.to",
     "1. Basic Information Original Title: The extension you never "
     "installed: KREMLIN forges... # security # threatintel # software # dev",
     "https://dev.to/anoymask/kremlin-forging-chromium-integrity-oli"),
    ("masto:3", "dev.to",
     "1. Overview Original Title: Iranian cyber targeting of dissidents, "
     "activists and... # security # threatintel # software # developme",
     "https://dev.to/anoymask/chosen-brick-iranian-windows-34ng"),
    ("masto:4", "dev.to",
     "1. Basic Information Original Title: North Korean \"WaterPlum,\" "
     "commonly referred to as... # security # threatintel # software # dev",
     "https://dev.to/anoymask/waterplum-north-korean-campaign-4528"),
    ("masto:5", "dev.to",
     "1. Basic Information Original Title: Threat Intel | One Kit, Forty "
     "Companies: How a... # security # threatintel # software # develo",
     "https://dev.to/anoymask/rapuncel-fake-github-repositories-1nl8"),
    ("masto:6", "dev.to",
     "1. Basic Information Original Title: Autonomous AI agents breach "
     "online retailers in chained attacks... # security # threatintel # dev",
     "https://dev.to/anoymask/ai-agents-retailer-card-theft-9xk2"),
    ("masto:7", "cybersecuritynews.com",
     "BragJack attack lets malicious extensions hijack AI agents in five "
     "major browsers - new prompt-forcing technique",
     "https://cybersecuritynews.com/bragjack-ai-agent-hijacking/"),
]
STORY_TITLE = EVENTS[-1][2]


def build_store(root, events=EVENTS, story_title="A rolling dev.to author "
                                                 "series (BragJack)"):
    sdir = os.path.join(root, "stories")
    edir = os.path.join(root, "events")
    os.makedirs(sdir)
    os.makedirs(edir)
    refs = []
    for i, (eid, src, title, url) in enumerate(events):
        json.dump({"id": eid, "title": title, "kind":
                   "original" if i == 0 else "update", "source": src,
                   "url": url, "published_at": f"2026-09-1{i % 10}T00:00:0{i}Z",
                   "cves": [], "lang": "en",
                   "content_md": title + "\n\nvia Mastodon " + url,
                   "excluded": False},
                  open(os.path.join(edir, eid + ".json"), "w"))
        with open(os.path.join(edir, eid + ".md"), "w") as fh:
            fh.write("x" * 800)
        refs.append({"event_id": eid, "label": "original" if i == 0 else "update"})
    json.dump({"id": STORY, "title": story_title,
               "first_seen": "2026-09-10T00:00:00Z",
               "last_seen": "2026-09-19T00:00:00Z",
               "sources": ["dev.to", "cybersecuritynews.com"], "n_sources": 2,
               "cves": [], "score": 0.0,
               "reddit_signal": {"posts": 0, "best_score": 0},
               "events": refs},
              open(os.path.join(sdir, STORY + ".json"), "w"))
    return sdir, edir


tmp = tempfile.mkdtemp()
try:
    # ── 1. dry run writes nothing ──────────────────────────────────────────
    root = os.path.join(tmp, "dry")
    sdir, edir = build_store(root)
    before = snapshot(sdir)
    rc = rb.main(["--stories-dir", sdir, "--events-dir", edir])
    check("dry run exits 0", rc, 0)
    check("dry run writes no story files", snapshot(sdir), before)
    check("dry run writes no event files",
          sorted(os.path.basename(p) for p in glob.glob(os.path.join(edir, "*.json"))),
          sorted(f"{e[0]}.json" for e in EVENTS))

    # ── 2. apply splits the series ─────────────────────────────────────────
    root = os.path.join(tmp, "apply")
    sdir, edir = build_store(root)
    rc = rb.main(["--stories-dir", sdir, "--events-dir", edir, "--apply"])
    check("apply exits 0", rc, 0)
    stories = {json.load(open(p))["id"]: json.load(open(p))
               for p in glob.glob(os.path.join(sdir, "*.json"))}
    check("original story is never deleted", STORY in stories, True)
    orig = stories[STORY]
    check("original keeps only the BragJack events",
          sorted(r["event_id"] for r in orig["events"]), ["masto:1", "masto:7"])
    check("original is retitled to the BragJack claim", orig["title"], STORY_TITLE)
    check("five components became five stories", len(stories) - 1, 5)

    new_ids = sorted(sid for sid in stories if sid != STORY)
    check("no dev.to scaffolding in a new id",
          [i for i in new_ids if "basic-information" in i or i.startswith("1-")
           or "original-title" in i or "overview" in i], [])
    check("no hashtag tail in a new id",
          [i for i in new_ids if i.endswith("-security-threatintel")], [])
    check("one new story per component (KREMLIN/Chosen Brick/"
          "WaterPlum/Rapuncel/AI-retailer)",
          [i for i in new_ids
           if any(k in i for k in ("kremlin", "iranian-cyber", "waterplum",
                                   "one-kit-forty", "online-retailers"))],
          new_ids)
    check("each new story holds exactly one event",
          sorted(len(stories[i]["events"]) for i in new_ids), [1] * 5)
    check("new stories carry the event's cleaned claim as title",
          all(stories[i]["title"] and "Original Title" not in stories[i]["title"]
              and "#" not in stories[i]["title"] for i in new_ids), True)

    owners = {}
    for sid, s in stories.items():
        for r in s["events"]:
            owners.setdefault(r["event_id"], []).append(sid)
    check("every event has exactly one owner",
          {e: o for e, o in owners.items() if len(o) > 1}, {})
    check("all events still owned", len(owners), len(EVENTS))
    check("derived fields match each touched story's own events",
          [(s["n_sources"], len(s["sources"]))
           for s in stories.values() if s["n_sources"] != len(s["sources"])], [])
    check("moved events are re-kinded to original",
          sorted(json.load(open(os.path.join(edir, e + ".json")))["kind"]
                 for e in ("masto:2", "masto:6")), ["original", "original"])
    moved_rec = json.load(open(os.path.join(edir, "masto:2.json")))
    check("event records keep every collector-written key (content_md, cves, "
          "lang) — only kind changes",
          (sorted(moved_rec), moved_rec.get("lang"),
           bool(moved_rec.get("content_md"))),
          (["content_md", "cves", "excluded", "id", "kind", "lang",
            "published_at", "source", "title", "url"], "en", True))

    # ── 3. idempotent ──────────────────────────────────────────────────────
    after_first = snapshot(sdir)
    rc = rb.main(["--stories-dir", sdir, "--events-dir", edir, "--apply"])
    check("second apply exits 0 (nothing to split)", rc, 0)
    check("second apply writes nothing", snapshot(sdir), after_first)

    # ── 4. refusal paths ───────────────────────────────────────────────────
    root = os.path.join(tmp, "shell")
    sdir, edir = build_store(root)
    p = os.path.join(sdir, STORY + ".json")
    s = json.load(open(p))
    s["merged_into"] = "somewhere-else"
    json.dump(s, open(p, "w"))
    check("redirect shell is refused", rb.main(["--stories-dir", sdir,
                                                "--events-dir", edir, "--apply"]), 2)

    root = os.path.join(tmp, "missing")
    sdir, edir = build_store(root)
    os.remove(os.path.join(sdir, STORY + ".json"))
    check("missing target is refused",
          rb.main(["--stories-dir", sdir, "--events-dir", edir]), 2)

    # no BragJack claim left to retain -> refuse rather than mint an empty story
    root = os.path.join(tmp, "noclaim")
    sdir, edir = build_store(root)
    p = os.path.join(sdir, STORY + ".json")
    s = json.load(open(p))
    s["events"] = [r for r in s["events"] if r["event_id"] not in ("masto:1", "masto:7")]
    json.dump(s, open(p, "w"))
    check("no retained BragJack claim is refused",
          rb.main(["--stories-dir", sdir, "--events-dir", edir, "--apply"]), 2)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
if failures:
    print(f"FAIL: {len(failures)} checks failed: {failures}")
    sys.exit(1)
print("PASS: repair_bragjack_split contracts hold")
