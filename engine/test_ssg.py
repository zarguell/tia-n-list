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

        def story(sid, sources=("example.com",), cves=()):
            st = {"id": sid, "title": sid.replace("-", " "), "sources": list(sources),
                  "cves": list(cves), "score": 6.0, "last_seen": "2026-08-14T12:00:00Z",
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

        # 5. chip rows trimmed for the grid: 2 outlets + "+N more"; KEV CVEs
        # first, 2 shown + "+N more"; the KEV badge reflects the FULL kev set
        import kev as kev_mod
        kev_dir = os.path.join(tmp, "kev")
        os.makedirs(kev_dir)
        with open(os.path.join(kev_dir, "index.json"), "w") as f:
            json.dump({"cves": [{"cve_id": "CVE-2026-68820"}]}, f)
        saved_kev_dir = kev_mod.KEV_DIR
        kev_mod.KEV_DIR = kev_dir
        try:
            story("chip-trim",
                  sources=("tenable.com", "securityweek.com", "malware.news",
                           "bleepingcomputer.com", "krebsonsecurity.com"),
                  cves=("CVE-2026-55040", "CVE-2026-68820",
                        "CVE-2026-70329", "CVE-2026-63520"))
            events["e-chip-trim"] = ev("e-chip-trim", text="Event body.")
            c = card("chip-trim", events)
            ok &= check("sources capped at 2", c["card_sources"],
                        ["tenable.com", "securityweek.com"])
            ok &= check("sources_more count", c["sources_more"], 3)
            ok &= check("KEV CVE first in card_cves", c["card_cves"],
                        ["CVE-2026-68820", "CVE-2026-55040"])
            ok &= check("cves_more count", c["cves_more"], 2)
            ok &= check("KEV badge uses full kev set", c["kev_cves"],
                        ["CVE-2026-68820"])
            # edge: exactly 2 sources / 1 CVE -> no more-chips
            story("chip-edge", sources=("a.com", "b.com"),
                  cves=("CVE-2026-00001",))
            events["e-chip-edge"] = ev("e-chip-edge", text="Event body.")
            c = card("chip-edge", events)
            ok &= check("2 sources no more-chip",
                        (c["card_sources"], c["sources_more"]),
                        (["a.com", "b.com"], 0))
            ok &= check("1 cve no more-chip",
                        (c["card_cves"], c["cves_more"]),
                        (["CVE-2026-00001"], 0))
        finally:
            kev_mod.KEV_DIR = saved_kev_dir

        # 6. quiet-state honesty (2026-08-15): <2 hot -> banner on the home
        # page, count-accurate for 0 and 1; >=2 hot -> no banner
        def render_index(quiet, total_hot):
            return ssg.render("index.html", active="index", og_url=ssg.site_url(""),
                              hero=None, cards=[], quiet=quiet,
                              hot_threshold=5.0, total_hot=total_hot)

        html_quiet0 = render_index(True, 0)
        ok &= check("quiet banner renders at 0 hot", "quiet-banner" in html_quiet0, True)
        ok &= check("0-hot banner says 'No stories cleared'",
                    "No stories cleared" in html_quiet0, True)
        ok &= check("0-hot banner links to all stories", "Browse all stories" in html_quiet0, True)
        html_quiet1 = render_index(True, 1)
        ok &= check("1-hot banner says 'Only 1 story'",
                    "Only 1 story cleared" in html_quiet1, True)
        html_hot = render_index(False, 6)
        ok &= check("no banner at 6 hot", "quiet-banner" not in html_hot, True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

        # markdown cross-refs (2026-10-07: missing-story links red-den
        # deploys — now caught at VPS lint time instead of on Actions)
        rd = tempfile.mkdtemp(prefix="tia-refs-")
        try:
            open(os.path.join(rd, "a.md"), "w").write(
                "[x](stories/real-story/) and [y](daily/2026-10-07/) ok\n"
                "but [z](stories/no-such-story/) breaks and "
                "`[c](stories/also-missing/)` is code.\n")
            errs = ssg.lint_md_refs({"real-story"}, {"2026-10-07"},
                                    [os.path.join(rd, "a.md")])
            ok &= check("missing story flagged, code span ignored",
                        errs, ["a.md: stories/no-such-story/ has no story"])
            open(os.path.join(rd, "b.md"), "w").write("[y](daily/1999-01-01/)\n")
            errs = ssg.lint_md_refs({"real-story"}, {"2026-10-07"},
                                    [os.path.join(rd, "b.md")])
            ok &= check("missing digest flagged",
                        errs, ["b.md: daily/1999-01-01/ has no digest"])
        finally:
            shutil.rmtree(rd, ignore_errors=True)

        # deploy stamp (2026-10-07: the async watcher verifies against
        # the live stamp, not the Actions API)
        import subprocess as _sp
        info = ssg.deploy_info()
        head = _sp.run(["git", "rev-parse", "HEAD"], capture_output=True,
                       text=True).stdout.strip()
        ok &= check("deploy stamp names HEAD without GITHUB_SHA",
                    info["sha"], head)
        ok &= check("deploy stamp has built_at", "built_at" in info, True)
        os.environ["GITHUB_SHA"] = "abc123"
        try:
            ok &= check("GITHUB_SHA wins on Actions",
                        ssg.deploy_info()["sha"], "abc123")
        finally:
            del os.environ["GITHUB_SHA"]

        # ---- 2026-11-13 UI pass: digest status badges + CTI per-case intel ----
        badges = ssg.digest_markers_html(
            "<p>[NEW] a</p><p>[UPDATE] b</p><p>[REVISIT] c</p>")
        ok &= check("digest [NEW] renders as a badge",
                    'class="dg-badge dg-new"' in badges, True)
        ok &= check("digest [UPDATE] renders as a badge",
                    'class="dg-badge dg-update"' in badges, True)
        ok &= check("digest [REVISIT] renders as a badge",
                    'class="dg-badge dg-revisit"' in badges, True)
        ok &= check("digest badge rendering is idempotent",
                    ssg.digest_markers_html(badges), badges)
        ok &= check("non-status bracket words stay text",
                    ssg.digest_markers_html("[ASOS] stays text"), "[ASOS] stays text")
        ok &= check("empty digest html is untouched", ssg.digest_markers_html(""), "")

        import cti as cti_mod
        orig_tech = cti_mod.load_techniques
        cti_mod.load_techniques = lambda: {
            "T1595": {"id": "T1595", "name": "Active Scanning",
                      "tactic": "reconnaissance", "tactic_name": "Reconnaissance"}}
        try:
            intel = {
                "case-rich": {"sigma": True, "splunk": True, "kql": False,
                              "yara": False, "iocs": 3},
                "case-yara": {"sigma": False, "splunk": False, "kql": False,
                              "yara": True, "iocs": 0},
                "case-empty": {"sigma": False, "splunk": False, "kql": False,
                               "yara": False, "iocs": 0},
            }
            recs = {sid: {"title": sid, "attack": [{"id": "T1595"}]}
                    for sid in intel}
            mx = cti_mod.build_matrix(recs, {}, lambda sid: intel[sid])
            covered = cti_mod.all_covered(mx)
        finally:
            cti_mod.load_techniques = orig_tech
        tech = [x for tac in mx for x in tac["techniques"] if x["id"] == "T1595"][0]
        ok &= check("CTI row keeps every case", len(tech["cases"]), 3)
        ok &= check("CTI cases with intel sort first",
                    tech["cases"][0]["story_id"], "case-rich")
        ok &= check("CTI intel travels with the case",
                    tech["cases"][0]["intel"]["iocs"], 3)
        ok &= check("CTI detection = sigma/yara only",
                    [c["detection"] for c in tech["cases"]], [True, True, False])
        ok &= check("CTI technique detection count", covered[0]["n_detections"], 2)

        # ---- 2026-11-13: the published source list (/feeds/sources/) ----
        feeds = ssg.load_source_feeds()
        ok &= check("OPML loads every checked-in feed", len(feeds), 53)
        ok &= check("source rows are https and titled",
                    all(f["feed"].startswith("https://") and f["title"]
                        and f["host"] for f in feeds), True)
        ok &= check("source hosts are unique",
                    len({f["host"] for f in feeds}), len(feeds))
        ok &= check("sources sorted by title",
                    [f["title"].lower() for f in feeds],
                    sorted(f["title"].lower() for f in feeds))
        # activity joins on the source host; unknown hosts are ignored
        now = ssg.datetime.now(ssg.timezone.utc)
        evs = {
            "a": {"source": feeds[0]["host"], "published_at":
                  (now - ssg.timedelta(days=2)).isoformat()},
            "b": {"source": "www." + feeds[0]["host"], "published_at":
                  (now - ssg.timedelta(days=40)).isoformat()},
            "c": {"source": "not-in-the-opml.example", "published_at":
                  now.isoformat()},
        }
        act = ssg.source_activity(evs, feeds, days=30)
        ok &= check("activity counts the 30-day window only",
                    act[feeds[0]["host"]]["n"], 1)
        ok &= check("activity keeps the newest sighting",
                    act[feeds[0]["host"]]["latest"].strftime("%Y-%m-%d"),
                    (now - ssg.timedelta(days=2)).strftime("%Y-%m-%d"))
        ok &= check("activity ignores non-OPML sources",
                    "not-in-the-opml.example" in act, False)

        page = ssg.env.get_template("feeds-sources.html").render(
            active="feeds", feeds=[
                {"title": "Example", "site": "https://example.com/",
                 "feed": "https://example.com/feed", "host": "example.com",
                 "latest": "2026-11-01", "last_30d": 7}],
            src_count=1, active_count=1, total_30d=7,
            og_url="https://example.com/feeds/sources/")
        ok &= check("sources page lists the feed", "example.com" in page, True)
        ok &= check("sources page links the OPML download",
                    'href="feeds/sources.opml"' in page, True)
        ok &= check("sources page renders the stats", ">7<" in page, True)
        ok &= check("sources page external links are noopener",
                    'rel="noopener noreferrer"' in page, True)

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
