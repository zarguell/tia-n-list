#!/usr/bin/env python3
"""Stage the published site for the GitHub Pages artifact.

`ssg.py` writes the site into the REPOSITORY ROOT (`ROOT` is literally
"repo root = Pages root"), so `upload-pages-artifact` used to publish the
whole workspace: 114k files / ~330 MB, 87k of them raw event records under
engine/data/events/ (273 MB) that no page references — and that store grows
~1k files/day, so the artifact grew forever. GitHub Pages' deploy sync is
not sized for that: every deploy re-uploads it, and when the Pages backend
is slow the sync runs past deploy-pages' 600 s timeout (2026-11-05/06: six
"Timeout reached, aborting!" failures at exactly 10 min plus one
"Deployment failed, try again later", all with a green build).

This script copies ONLY the published surface into a staging dir and then
verifies the staged tree:

  * every PUBLISHED entry exists in the source tree (ssg.py produced it);
  * every relative href/src/fetch target in the staged HTML resolves inside
    the staged tree (so a new output dir that is not staged fails the build
    loudly instead of shipping a site with dead links);
  * PUBLISHED covers every generated site path in .gitignore — that file is
    the maintained list of what the build writes into the root, so a new
    generated path cannot be forgotten here silently.

Usage:
  python3 engine/stage_pages.py <dest> [--src <repo root>]
"""
import argparse
import html
import os
import re
import shutil
import sys

# The published surface: root files + generated directories. Kept in sync with
# the generated-site block in .gitignore (checked below).
PUBLISHED_FILES = (
    "index.html",
    "404.html",
    "style.css",
    "robots.txt",
    "sitemap.xml",
    "stories.json",
    "stories-index.json",
    "deploy.json",
)
PUBLISHED_DIRS = (
    "stories",
    "daily",
    "feeds",
    "posts",
    "cti",
    "methodology",
    "about",
    "kev",
    "megapatch",
)
PUBLISHED = PUBLISHED_FILES + tuple(d + "/" for d in PUBLISHED_DIRS)

# Copy noise that can appear under an output dir (a local ssg.py run from the
# repo root leaves nothing there today, but caches are never site content).
COPY_IGNORE = ("__pycache__", ".pytest_cache", "node_modules")

_SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script>", re.S | re.I)
_STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.S | re.I)
_HREF_RE = re.compile(r'(?:href|src)="([^"]*)"', re.I)
_FETCH_RE = re.compile(r"""fetch\(\s*(['"])([^'"]+)\1""")
_SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "#")


def generated_root_paths(src):
    """Generated site paths from .gitignore (root-anchored, one segment).

    .gitignore lists exactly what the build writes into the repo root (the
    generated static site block). Anything deeper (/engine/data/...) is source
    data, not published surface."""
    out = []
    try:
        with open(os.path.join(src, ".gitignore"), encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line.startswith("/") or line.startswith("/engine/"):
                    continue
                name = line[1:]
                if not name or name.startswith("!"):
                    continue
                is_dir = name.endswith("/")
                name = name.rstrip("/")
                if not name or "/" in name:
                    continue
                out.append(name + "/" if is_dir else name)
    except OSError:
        return []
    return out


def check_published_matches_gitignore(src):
    """Fail when .gitignore names a generated root path PUBLISHED does not stage."""
    declared = {p for p in generated_root_paths(src)}
    staged = set(PUBLISHED)
    missing = sorted(declared - staged)
    extra = sorted(staged - declared)
    errs = []
    if missing:
        errs.append(
            "generated path(s) in .gitignore but not staged: "
            + ", ".join(missing)
            + " — add them to PUBLISHED_* in engine/stage_pages.py (otherwise "
            "the site ships without them)")
    if extra:
        errs.append(
            "staged path(s) not listed as generated in .gitignore: "
            + ", ".join(extra)
            + " — either the .gitignore generated-site block lost them or "
            "PUBLISHED_* is stale")
    return errs


def stage(src, dest):
    """Copy the published surface of `src` into `dest`; return (files, bytes)."""
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    for name in PUBLISHED_FILES:
        sp = os.path.join(src, name)
        if not os.path.isfile(sp):
            raise SystemExit(f"stage_pages: missing generated file {name} "
                             f"(did engine/ssg.py run?)")
        shutil.copy2(sp, os.path.join(dest, name))
    for name in PUBLISHED_DIRS:
        sp = os.path.join(src, name)
        if not os.path.isdir(sp):
            raise SystemExit(f"stage_pages: missing generated directory {name}/ "
                             f"(did engine/ssg.py run?)")
        shutil.copytree(sp, os.path.join(dest, name),
                        ignore=shutil.ignore_patterns(*COPY_IGNORE))
    files = size = 0
    for dp, _, fns in os.walk(dest):
        for fn in fns:
            files += 1
            try:
                size += os.path.getsize(os.path.join(dp, fn))
            except OSError:
                pass
    return files, size


def _refs(doc):
    """Same-origin targets referenced by a page: href/src outside <script>,
    plus fetch() targets (which live inside scripts)."""
    markup = _STYLE_RE.sub("", _SCRIPT_RE.sub("", doc))
    for m in _HREF_RE.finditer(markup):
        yield m.group(1)
    for m in _FETCH_RE.finditer(doc):
        yield m.group(2)


def verify(dest):
    """Every relative reference in the staged HTML must resolve in `dest`.

    Pages serve a directory URL as its index.html, and every page carries
    `<base href="https://.../">`, so refs resolve against the site root."""
    missing = {}
    checked = 0
    for dp, _, fns in os.walk(dest):
        for fn in fns:
            if not fn.endswith(".html"):
                continue
            with open(os.path.join(dp, fn), encoding="utf-8", errors="ignore") as f:
                doc = f.read()
            for url in _refs(doc):
                url = html.unescape(url).strip()
                if not url or "{{" in url or url.startswith(_SKIP_SCHEMES):
                    continue
                rel = url.split("#")[0].split("?")[0].lstrip("/")
                if not rel:
                    continue
                checked += 1
                target = os.path.normpath(os.path.join(dest, rel))
                if os.path.isdir(target):
                    target = os.path.join(target, "index.html")
                if not os.path.exists(target):
                    rel_page = os.path.relpath(os.path.join(dp, fn), dest)
                    missing.setdefault(url, []).append(rel_page)
    errs = [f"unresolvable reference {url!r} (first seen in {pages[0]}, "
            f"{len(pages)} page(s))" for url, pages in sorted(missing.items())]
    return checked, errs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dest", help="staging directory to (re)create")
    ap.add_argument("--src", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))),
        help="repo root holding the generated site (default: this repo)")
    args = ap.parse_args(argv)

    errs = check_published_matches_gitignore(args.src)
    if errs:
        for e in errs:
            print(f"STAGE FAIL {e}", file=sys.stderr)
        return 2
    files, size = stage(args.src, args.dest)
    checked, verrs = verify(args.dest)
    print(f"staged {files} files ({size / 1e6:.1f} MB), "
          f"{checked} internal references checked")
    if verrs:
        for e in verrs:
            print(f"STAGE FAIL {e}", file=sys.stderr)
        print("hint: CI builds from a clean clone; a local tree can hold pages "
              "from older builds (ssg.py never deletes) — rebuild before "
              "staging locally.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
