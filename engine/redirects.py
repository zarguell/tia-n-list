#!/usr/bin/env python3
"""Merged-story redirect map — one key per merge instead of one page per merge.

A story merged away by the triage/repair gates has to keep its URL working:
digests, CTI cases, already-delivered RSS items and other people's links all
name it. Until 2026-11-27 that guarantee was a rendered 200 + meta-refresh
page per merged story — 3,085 files and ~780/month of growth, 44% of every
published story page (measured 2026-11-27: 3,085 of 6,997).

The map is the same guarantee at one key per merge:

  redirects.json   {"stories/<merged>/": "stories/<canonical>/", ...}
  404.html         resolves a 404 path through the map, same-origin only

Generated pages never rely on the resolver: `canon_hrefs()` rewrites any href
naming a merged id at write() time, so the site links the canonical URL
directly and the build's own link lint proves nothing dangles.

Fail-safe by construction: an id is mapped only when its merged_into chain
reaches a story this build actually renders. Cycles, dangling targets and
frozen canonicals are left OUT of the map (the audit already reports them)
rather than producing a redirect loop or a 404 that redirects to a 404.
"""
import re

# A path in the map, site-root-relative: "stories/<id>/"
_PATH_RE = re.compile(r"^stories/([a-z0-9-]+)/$")
_HREF_RE = re.compile(r'href="([^"]*)"')


def resolve(story_id, stories):
    """Follow merged_into to the canonical id; None on cycle or dangling."""
    seen = set()
    cur = story_id
    while True:
        if cur in seen:
            return None                  # cycle: never resolve to a loop
        seen.add(cur)
        nxt = (stories.get(cur) or {}).get("merged_into")
        if not nxt:
            return cur if cur in stories else None
        cur = nxt


def _canonical_for(story_id, story, stories, renderable):
    """The canonical id this shell should redirect to, or None to leave it out."""
    if not story.get("merged_into"):
        return None
    canon = resolve(story_id, stories)
    if canon in (None, story_id) or canon not in renderable:
        return None
    return canon


def build_map(stories, renderable=None):
    """merged id -> canonical id, chains resolved, unresolvable ids dropped.

    stories     {id: story dict}, merged shells included.
    renderable  ids this build renders (the cards). Defaults to every
                non-merged id. A canonical id that is not renderable has no
                page, so it is dropped rather than guessed at.
    """
    if renderable is None:
        renderable = {sid for sid, st in stories.items() if not st.get("merged_into")}
    return {sid: canon
            for sid, st in stories.items()
            for canon in [_canonical_for(sid, st, stories, renderable)]
            if canon}


def published_map(mapping):
    """The published shape: merged id -> canonical id (ids only, sorted).

    The resolver prefixes "stories/" itself, so full paths would add ~70 KB
    of redundant text to a file fetched on demand by the 404 page (measured
    for 3,003 merges on 2026-11-27: ids 390 KB, ids+paths 443 KB).
    `valid_target()` still checks the path the resolver builds.
    """
    return {m: mapping[m] for m in sorted(mapping)}


def canon_hrefs(html, mapping, base_url=""):
    """Rewrite hrefs that name a merged story id to the canonical id.

    Handles relative ("stories/<id>/") and same-site absolute
    ("<base_url>/stories/<id>/") links, keeps any #fragment, and leaves every
    other href byte-identical. Applied in ssg.write() so no generated page can
    link a URL that no longer exists.
    """
    if not mapping or "stories/" not in html:
        return html
    prefix = (base_url.rstrip("/") + "/") if base_url else ""

    def fix(m):
        url = m.group(1)
        absolute = bool(prefix) and url.startswith(prefix)
        path = url[len(prefix):] if absolute else url
        if not path.startswith("stories/"):
            return m.group(0)
        head, sep, frag = path.partition("#")
        parts = head.split("/")
        if len(parts) < 2 or parts[1] not in mapping:
            return m.group(0)
        parts[1] = mapping[parts[1]]
        new = "/".join(parts) + (sep + frag if sep else "")
        return 'href="%s"' % ((prefix + new) if absolute else new)

    return _HREF_RE.sub(fix, html)


def valid_target(path):
    """A redirect target the 404 resolver may follow (same-shape check).

    Mirrors the map's own key shape so a corrupted or attacker-influenced
    redirects.json can never turn the page into an open redirect.
    """
    return bool(_PATH_RE.match(path or ""))
