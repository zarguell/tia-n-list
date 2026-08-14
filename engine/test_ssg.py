#!/usr/bin/env python3
"""Story-card snippet contract suite — analysis-preferred card text.

The card snippet on / (hot) and /stories/ (all) used to be the FIRST ORIGINAL
EVENT's auto-extracted body. When the original article body is empty (sites
that strip content — e.g. the GeoServer zero-day story's original event is a
bare "\\n") the card rendered literally nothing, even though an analyst-written
analysis existed for the story. And when we DID write an analysis, it is a
better summary than any extracted body. Contract:

  1. analysis exists + non-empty  -> snippet comes from the analysis, never empty;
  2. analysis file empty/missing   -> fall back to the first original event body;
  3. analysis snippets are trimmed at a sentence boundary (no mid-sentence cut),
     capped at 600 chars like the event-derived snippets were;
  4. feed-hot and stories-index.json consume the same card snippet, so the
     fix covers hot page, all-stories page, and the hot feed.

Run: python3 engine/test_ssg.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ssg  # noqa: E402


def ev(eid, published="2026-08-14T10:00:00Z", kind="original", text="",
       source="example.com", url="https://example.com/a"):
    return {"id": eid, "content_md": text, "kind": kind, "title": f"Title {eid}",
            "source": source, "url": url, "published_at": published}


def check(name, got, expect, detail=""):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {expect!r} {detail}")
    return ok


def main():
    ok = True
    tmp = tempfile.mkdtemp(prefix="tia-ssg-")
    try:
        stories_dir = os.path.join(tmp, "stories")
        analysis_dir = os.path.join(tmp, "analysis")
        os.makedirs(stories_dir)
        os.makedirs(analysis_dir)
        ssg.STORIES_DIR = stories_dir
        ssg.ANALYSIS_DIR = analysis_dir

        def story(sid):
            st = {"id": sid, "title": sid.replace("-", " "), "sources": ["example.com"],
                  "cves": [], "score": 6.0, "last_seen": "2026-08-14T12:00:00Z",
                  "events": [{"event_id": f"e-{sid}"}]}
            with open(os.path.join(stories_dir, sid + ".json"), "w") as f:
                json.dump(st, f)

        def card(sid, events):
            return next(x for x in ssg.load_stories(events) if x["id"] == sid)

        # 1. analysis exists + original event body EMPTY -> snippet from analysis
        story("empty-original-with-analysis")
        with open(os.path.join(analysis_dir, "empty-original-with-analysis.md"), "w") as f:
            f.write("First sentence of the analyst summary. Second sentence with more detail.\n\n"
                    "Context paragraph on impact and watch-items.\n")
        events = {"e-empty-original-with-analysis": ev(
            "e-empty-original-with-analysis", text="\n")}
        c = card("empty-original-with-analysis", events)
        expect = ("First sentence of the analyst summary. Second sentence with more detail. "
                  "Context paragraph on impact and watch-items.")
        ok &= check("analysis preferred over empty original", c["snippet"], expect)
        ok &= check("analysis snippet non-empty", bool(c["snippet"]), True)

        # 2a. empty analysis file -> fall back to the first original event
        story("empty-analysis-file")
        open(os.path.join(analysis_dir, "empty-analysis-file.md"), "w").close()
        events["e-empty-analysis-file"] = ev("e-empty-analysis-file",
                                             text="Event body text for the card.")
        c = card("empty-analysis-file", events)
        ok &= check("empty analysis falls back to event", c["snippet"],
                    "Event body text for the card.")

        # 2b. no analysis file at all -> first original event body
        story("no-analysis")
        events["e-no-analysis"] = ev("e-no-analysis", text="Event body text for the card.")
        c = card("no-analysis", events)
        ok &= check("no analysis falls back to event", c["snippet"],
                    "Event body text for the card.")

        # 3. long analysis trimmed at a sentence boundary, capped at 600
        story("long-analysis")
        para = " ".join(f"Sentence {i} carries real words for the story summary."
                        for i in range(30))
        with open(os.path.join(analysis_dir, "long-analysis.md"), "w") as f:
            f.write(para + "\n")
        events["e-long-analysis"] = ev("e-long-analysis", text="\n")
        c = card("long-analysis", events)
        ok &= check("analysis snippet capped at 600", len(c["snippet"]) <= 600, True,
                    f"len={len(c['snippet'])}")
        ok &= check("analysis snippet ends at sentence boundary",
                    c["snippet"].endswith("summary."), True, f"tail={c['snippet'][-40:]!r}")

        # 4. feed-hot + all-stories consume the same card snippet (the hot page
        # and /stories/ card both render s.snippet; feed-hot uses c["snippet"],
        # the all-stories index trims it to 220 chars)
        hot = ssg.feed_hot_items([c])
        ok &= check("feed-hot carries the analysis snippet",
                    hot[0]["description"] == c["snippet"], True)
        ok &= check("all-stories index snippet is the analysis text",
                    c["snippet"][:220].startswith("Sentence 0"), True,
                    f"head={c['snippet'][:60]!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
