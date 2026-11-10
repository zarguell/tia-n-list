#!/usr/bin/env python3
"""Pages artifact staging contract suite.

`engine/stage_pages.py` exists because the deploy artifact used to be the whole
repo root (114k files, 87k of them raw events under engine/data/events/ that no
page references), which is what made the Pages sync blow past deploy-pages'
timeout. The contract:

  1. staging copies ONLY the published surface — source trees (engine/,
     kevrichment/), the runtime state/ dir and caches never ship;
  2. every PUBLISHED_* entry missing from the source is a hard error (a silent
     skip would publish a site missing a whole section);
  3. every relative href/src/fetch target in the staged HTML resolves inside
     the staged tree — a new output dir that is not staged fails the build
     instead of shipping dead links;
  4. href/src inside <script> blocks are NOT references (the generated pages
     carry JS template strings like href="' + pageHref(p) + '");
  5. PUBLISHED_* covers every generated root path in .gitignore, so a new
     generated path cannot be forgotten here silently.

Run: python3 engine/test_stage_pages.py   (exit 0 = pass)
Wired into CI (site-deploy.yml).
"""
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stage_pages  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(name, got, expect, detail=""):
    ok = got == expect
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got!r} want {expect!r} {detail}")
    return ok


def write(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def fake_site(root):
    """A minimal repo root shaped like the real one after `ssg.py`."""
    write(os.path.join(root, ".gitignore"),
          "__pycache__/\n"
          "# generated static site (built by CI)\n"
          "/index.html\n/style.css\n/404.html\n/deploy.json\n"
          "/robots.txt\n/stories.json\n/stories-index.json\n/sitemap.xml\n"
          "/stories/\n/daily/\n/feeds/\n/posts/\n/cti/\n/methodology/\n"
          "/about/\n/kev/\n/megapatch/\n"
          "# source-only\n"
          "/engine/data/digest-candidates.json\n"
          "engine/tests/node_modules/\n")
    write(os.path.join(root, "index.html"),
          '<html><head><base href="https://example.test/"></head>'
          '<body><a href="stories/">s</a><a href="style.css">c</a>'
          '<a href="daily/2026-01-01/">d</a>'
          '<a href="https://example.com/ext">x</a>'
          "<script>var t = '<a href=\"' + pageHref(p) + '\">';"
          "fetch('stories-index.json');</script></body></html>")
    for name in ("404.html", "style.css", "robots.txt", "sitemap.xml",
                 "stories.json", "stories-index.json", "deploy.json"):
        write(os.path.join(root, name), "x")
    write(os.path.join(root, "stories", "index.html"), "<html>all</html>")
    write(os.path.join(root, "stories", "a-story", "index.html"), "<html>s</html>")
    write(os.path.join(root, "daily", "2026-01-01", "index.html"), "<html>d</html>")
    write(os.path.join(root, "feeds", "feed-all.xml"), "<rss/>")
    write(os.path.join(root, "cti", "rule.sigma"), "title: r")
    write(os.path.join(root, "methodology", "index.html"), "<html>m</html>")
    write(os.path.join(root, "about", "index.html"), "<html>a</html>")
    write(os.path.join(root, "kev", "kev-index.json"), "{}")
    write(os.path.join(root, "megapatch", "index.html"), "<html>mp</html>")
    write(os.path.join(root, "posts", "2026-01-01-daily-summary", "index.html"),
          "<html>p</html>")
    # source + runtime trees that must never be staged
    write(os.path.join(root, "engine", "ssg.py"), "# source")
    write(os.path.join(root, "engine", "data", "events", "rss:a.json"), "{}")
    write(os.path.join(root, "engine", "data", "events", "rss:a.md"), "body")
    write(os.path.join(root, "kevrichment", "data", "index.json"), "{}")
    write(os.path.join(root, "state", "deploys", "pending.json"), "[]")
    write(os.path.join(root, "stories", "__pycache__", "junk.pyc"), "x")


def staged_paths(dest):
    out = set()
    for dp, _, fns in os.walk(dest):
        for fn in fns:
            out.add(os.path.relpath(os.path.join(dp, fn), dest).replace(os.sep, "/"))
    return out


def main():
    ok = True
    tmp = tempfile.mkdtemp(prefix="stage-pages-")
    try:
        src = os.path.join(tmp, "repo")
        dest = os.path.join(tmp, "site")
        fake_site(src)

        print("gitignore -> generated root paths")
        ok &= check("root-anchored one-segment paths only",
                    sorted(stage_pages.generated_root_paths(src)),
                    sorted(list(stage_pages.PUBLISHED_FILES)
                           + [d + "/" for d in stage_pages.PUBLISHED_DIRS]))

        print("published surface vs .gitignore")
        ok &= check("fake site matches", stage_pages.check_published_matches_gitignore(src), [])
        write(os.path.join(src, ".gitignore"), "/index.html\n/reports/\n")
        errs = stage_pages.check_published_matches_gitignore(src)
        ok &= check("new generated dir flagged",
                    any("reports/" in e and "not staged" in e for e in errs), True,
                    detail=str(errs[:1]))
        fake_site(src)  # restore

        print("staging copies the published surface only")
        files, size = stage_pages.stage(src, dest)
        got = staged_paths(dest)
        ok &= check("source tree excluded",
                    sorted(p for p in got if p.startswith(("engine/", "kevrichment/",
                                                           "state/"))), [])
        ok &= check("caches excluded",
                    sorted(p for p in got if "__pycache__" in p), [])
        ok &= check("root files staged",
                    sorted(p for p in got if "/" not in p),
                    sorted(stage_pages.PUBLISHED_FILES))
        ok &= check("content staged",
                    all(p in got for p in ("stories/index.html", "cti/rule.sigma",
                                           "kev/kev-index.json",
                                           "posts/2026-01-01-daily-summary/index.html")),
                    True)
        ok &= check("file count reported", files, len(got))
        ok &= check("size reported positive", size > 0, True)
        ok &= check("restaging is idempotent", stage_pages.stage(src, dest)[0], files)

        print("reference verification")
        checked, verrs = stage_pages.verify(dest)
        ok &= check("clean tree verifies", verrs, [])
        ok &= check("script-block href/src ignored",
                    any("pageHref" in e for e in verrs), False)
        ok &= check("refs were checked", checked > 0, True)
        # a referenced-but-unstaged asset must fail the build
        os.remove(os.path.join(dest, "daily", "2026-01-01", "index.html"))
        _, verrs = stage_pages.verify(dest)
        ok &= check("missing referenced page flagged",
                    [e.split(" (")[0] for e in verrs], ["unresolvable reference 'daily/2026-01-01/'"])
        os.remove(os.path.join(dest, "stories-index.json"))
        _, verrs = stage_pages.verify(dest)
        ok &= check("missing fetch() target flagged",
                    any("stories-index.json" in e for e in verrs), True)

        print("missing generated input is a hard error")
        os.remove(os.path.join(src, "cti", "rule.sigma"))
        shutil.rmtree(os.path.join(src, "cti"))
        try:
            stage_pages.stage(src, dest)
            ok &= check("missing cti/ raises", "no error", "SystemExit")
        except SystemExit as e:
            ok &= check("missing cti/ raises", "cti/" in str(e), True)

        print("real repo: PUBLISHED covers the generated site block")
        ok &= check("real .gitignore matches PUBLISHED",
                    stage_pages.check_published_matches_gitignore(REPO), [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
