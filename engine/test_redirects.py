#!/usr/bin/env python3
"""Merged-story redirect map contract suite.

Background: a merged-away story keeps its URL working. That used to cost one
rendered stub page per merge (3,085 files, ~780/month of growth, 44% of every
published story page on 2026-11-27); it is now one key in redirects.json plus
href canonicalization at write() time. The properties that make that swap safe:

  1. chains resolve (a -> b -> c) so a two-hop merge still lands on the story
     that is actually published;
  2. cycles and dangling targets are DROPPED, never resolved into a redirect
     loop or a redirect to a 404;
  3. a canonical id that this build does not render (frozen, missing) is
     dropped too — the map only promises destinations that exist;
  4. every in-page href naming a merged id is rewritten to the canonical id,
     relative and same-site absolute alike, fragment preserved;
  5. the map itself is the 404 resolver's only input, so its target shape is
     validated (same-origin "stories/<id>/" only — no open redirect).

Run: python3 engine/test_redirects.py   (exit 0 = pass)
Wired into CI (site-deploy.yml) and run_engine.sh.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import redirects as redir  # noqa: E402

BASE = "https://example.test/site"


def story(sid, merged_into=None):
    return {"id": sid, "merged_into": merged_into} if merged_into else {"id": sid}


def check(name, got, expect, detail=""):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {expect!r} {detail}")
    return ok


def check_resolve():
    ok = True
    stories = {"a": story("a"), "b": story("b", "a"), "c": story("c", "b")}
    ok &= check("direct merge resolves", redir.resolve("b", stories), "a")
    ok &= check("two-hop chain resolves to the live story", redir.resolve("c", stories), "a")
    ok &= check("a live story resolves to itself", redir.resolve("a", stories), "a")

    cyc = {"x": story("x", "y"), "y": story("y", "x")}
    ok &= check("cycle resolves to None (never a loop)", redir.resolve("x", cyc), None)

    dangling = {"d": story("d", "gone")}
    ok &= check("dangling target resolves to None", redir.resolve("d", dangling), None)
    return ok


def check_build_map():
    ok = True
    stories = {
        "live": story("live"),
        "m1": story("m1", "live"),
        "m2": story("m2", "m1"),
        "cyc1": story("cyc1", "cyc2"),
        "cyc2": story("cyc2", "cyc1"),
        "dangle": story("dangle", "missing"),
        "to-frozen": story("to-frozen", "frozen"),
        "frozen": story("frozen"),
    }
    m = redir.build_map(stories, renderable={"live"})
    ok &= check("merged id maps to its canonical", m.get("m1"), "live")
    ok &= check("chains collapse to the published id", m.get("m2"), "live")
    ok &= check("cycles are dropped", "cyc1" in m or "cyc2" in m, False)
    ok &= check("dangling targets are dropped", "dangle" in m, False)
    ok &= check("non-rendered canonicals are dropped (fail safe)",
                "to-frozen" in m, False)
    ok &= check("live stories are not map keys", "live" in m, False)
    ok &= check("default renderable = every non-merged id",
                redir.build_map({"live": story("live"), "m": story("m", "live")}),
                {"m": "live"})
    return ok


def check_published_map():
    return check("published map is ids only (resolver builds the path)",
                 redir.published_map({"m1": "live", "a1": "z9"}),
                 {"a1": "z9", "m1": "live"})


def check_canon_hrefs():
    ok = True
    m = {"m1": "live"}
    ok &= check("relative merged href rewritten",
                redir.canon_hrefs('<a href="stories/m1/">x</a>', m, BASE),
                '<a href="stories/live/">x</a>')
    ok &= check("same-site absolute href rewritten",
                redir.canon_hrefs(f'<a href="{BASE}/stories/m1/">x</a>', m, BASE),
                f'<a href="{BASE}/stories/live/">x</a>')
    ok &= check("fragment preserved",
                redir.canon_hrefs('<a href="stories/m1/#detections">x</a>', m, BASE),
                '<a href="stories/live/#detections">x</a>')
    ok &= check("canonical href left byte-identical",
                redir.canon_hrefs('<a href="stories/live/">x</a>', m, BASE),
                '<a href="stories/live/">x</a>')
    ok &= check("unmapped merged-adjacent href untouched",
                redir.canon_hrefs('<a href="stories/other/">x</a>', m, BASE),
                '<a href="stories/other/">x</a>')
    ok &= check("other-site absolute URL untouched",
                redir.canon_hrefs('<a href="https://evil.test/stories/m1/">x</a>', m, BASE),
                '<a href="https://evil.test/stories/m1/">x</a>')
    ok &= check("non-story href untouched",
                redir.canon_hrefs('<a href="daily/2026-01-01/">x</a>', m, BASE),
                '<a href="daily/2026-01-01/">x</a>')
    ok &= check("empty map is a no-op",
                redir.canon_hrefs('<a href="stories/m1/">x</a>', {}, BASE),
                '<a href="stories/m1/">x</a>')
    return ok


def check_target_shape():
    ok = True
    ok &= check("valid same-origin story path", redir.valid_target("stories/live/"), True)
    ok &= check("absolute URL rejected", redir.valid_target("https://evil.test/x"), False)
    ok &= check("protocol-relative rejected", redir.valid_target("//evil.test/x"), False)
    ok &= check("missing trailing slash rejected", redir.valid_target("stories/live"), False)
    ok &= check("empty target rejected", redir.valid_target(""), False)
    return ok


def main():
    ok = check_resolve()
    ok &= check_build_map()
    ok &= check_published_map()
    ok &= check_canon_hrefs()
    ok &= check_target_shape()
    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
