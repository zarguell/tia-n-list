#!/usr/bin/env python3
"""Tia N. List — static site generator (M0: design preview).

Logic only: reads the hybrid store (data/events/<id>.md + <id>.json and
data/stories/<id>.json), builds a render context, and renders the Jinja2
templates in templates/ into the repository root (GitHub Pages serves the
root). No HTML/XML/CSS lives in this file — all markup is in templates/ so it
can be linted and reviewed independently.

Hybrid store:
  data/events/<event-id>.md      markdown content of the article
  data/events/<event-id>.json    metadata: title, kind, source, url, published_at, cves
  data/stories/<story-id>.json   story metadata + ordered event refs + labels

Outputs:
  index.html, style.css, 404.html, robots.txt, sitemap.xml, stories.json
  stories/<id>/index.html          per-story timeline pages
  daily/<date>/index.html          daily top-stories digest page
  feeds/index.html                 feeds index
  feeds/feed-all.xml               every article (every story event)
  feeds/feed-hot.xml               stories above the hot threshold
  feeds/feed-daily.xml             today's top stories (the digest)

Usage: python3 ssg.py   (run from engine/)
"""
import glob
import json
import os
import posixpath
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from zoneinfo import ZoneInfo

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown import markdown as md_to_html

ENGINE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENGINE)                       # repo root = Pages root
TMPL_DIR = os.path.join(ENGINE, "templates")
EVENTS_DIR = os.path.join(ENGINE, "data", "events")
STORIES_DIR = os.path.join(ENGINE, "data", "stories")
DIGESTS_DIR = os.path.join(ENGINE, "data", "digests")
LOCAL_TZ = ZoneInfo("America/New_York")          # pipeline convention; digest runs 11:15 UTC = 07:15 EDT
DIGEST_RUN_UTC = "11:15:00Z"                      # stable pubDate anchor for the daily feed
BASE_URL = "https://zarguell.github.io/tia-n-list"


def site_url(path):
    """Join a base-relative path (e.g. 'stories/x/' or '/daily/') to the site URL."""
    return BASE_URL + "/" + path.lstrip("/")
HOT_THRESHOLD = 2.0
DIGEST_TOP_N = 10      # not a hard limit — how many stories the digest page lists

env = Environment(
    loader=FileSystemLoader(TMPL_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)
env.globals["site_url"] = site_url

MD_STRIP = re.compile(r"(!\[[^\]]*\]\([^)]*\)|\[([^\]]*)\]\([^)]*\)|^#{1,6}\s*|^\s*[-*+]\s+|^\s*>\s+|[*_`~]+)", re.M)


# ---------- helpers (data shaping only, no markup) ----------

def parse_utc(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)


def reltime(iso):
    secs = (datetime.now(timezone.utc) - parse_utc(iso)).total_seconds()
    if secs < 3600:
        return f"{max(1, int(secs // 60))}m ago"
    if secs < 86400:
        return f"{int(secs // 3600)}h ago"
    return f"{int(secs // 86400)}d ago"


def rfc2822(iso):
    return format_datetime(parse_utc(iso))


def date_human(iso):
    dt = parse_utc(iso)
    day = dt.day
    suffix = "th" if 4 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return dt.strftime(f"%B {day}{suffix}, %Y")


def md_text(text, max_chars=None):
    text = MD_STRIP.sub(lambda m: m.group(2) or "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text if max_chars is None else text[:max_chars]


def display_domain(s):
    """Defensive: if a source slips in as a full URL, render only its domain."""
    m = re.match(r"https?://(?:www\.)?([^/:]+)", s or "")
    return m.group(1).lower() if m else s


def md_snippet(text, max_chars=600):
    return md_text(text, max_chars)


def sanitize(html_text):
    """Strip active-content tags, event handlers, and dangerous URL schemes.

    Covers the audit-verified bypasses: script/style/iframe/object/embed blocks
    (incl. whitespace before the end-tag '>' and self-closing forms),
    case-insensitive on* attributes in any position, and javascript:/vbscript:/data:
    hrefs quoted or unquoted in any attribute position.
    """
    html_text = re.sub(r"<(script|style|iframe|object|embed)\b[^>]*>.*?</\s*\1\s*>",
                       "", html_text, flags=re.S | re.I)
    html_text = re.sub(r"<(script|style|iframe|object|embed)\b[^>]*/\s*>",
                       "", html_text, flags=re.I)
    # void elements (embed) and unclosed active tags: drop the opening tag so any
    # trailing "content" is inert text, not an active context
    html_text = re.sub(r"<(script|style|iframe|object|embed)\b[^>]*>",
                       "", html_text, flags=re.I)
    html_text = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)",
                       "", html_text, flags=re.I)
    html_text = re.sub(r"(href\s*=\s*)([\"']?)(?:javascript|vbscript|data):[^\"'>\s]*",
                       r"\1\2#", html_text, flags=re.I)
    return html_text


def heat(score):
    if score >= 4.5:
        return "h3", "hottest", "heat-3"
    if score >= 3.0:
        return "h2", "hot", "heat-2"
    if score >= HOT_THRESHOLD:
        return "h1", "warm", "heat-1"
    return "none", "new", "gray-500"


# ---------- store loading ----------

def load_events():
    events = {}
    for path in sorted(glob.glob(os.path.join(EVENTS_DIR, "*.json"))):
        eid = os.path.splitext(os.path.basename(path))[0]
        meta = json.load(open(path))
        md_path = os.path.join(EVENTS_DIR, eid + ".md")
        md_text = open(md_path).read() if os.path.exists(md_path) else ""
        events[eid] = {
            **meta,
            "content_md": md_text,
            "html": sanitize(md_to_html(md_text, output_format="html5")),
        }
    return events


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _toks(s):
    return {w for w in re.findall(r"[a-z0-9]{3,}", s.lower())}


def delta_body(events):
    """The story's ORIGINAL event renders in full; every other event renders only
    the sentences not already covered (accumulated across the original + prior
    deltas). An event whose delta is empty renders as a bare mention."""
    order = [e for e in events if e["kind"] == "original"] + \
            [e for e in events if e["kind"] != "original"]
    acc = set()
    out = {}
    for pos, e in enumerate(order):
        body = e["content_md"]
        if pos == 0:
            delta = body
            acc.update(_toks(body))
        else:
            sents = []
            for sent in SENT_SPLIT.split(body):
                st = _toks(sent)
                if not st:
                    continue
                if len(st) < 5:
                    if not st <= acc:
                        sents.append(sent)
                    continue
                if len(st & acc) / len(st) < 0.7:
                    sents.append(sent)
                    acc.update(st)
            delta = " ".join(sents)
        is_mention = pos > 0 and len(delta.split()) < 10
        out[e["id"]] = {
            "body_html": sanitize(md_to_html(delta, output_format="html5")) if not is_mention else "",
            "is_mention": is_mention,
        }
    return out


def load_stories(events):
    cards = []
    max_score = 1
    for path in sorted(glob.glob(os.path.join(STORIES_DIR, "*.json"))):
        st = json.load(open(path))
        evs = [events[e["event_id"]] for e in st["events"] if e["event_id"] in events]
        max_score = max(max_score, st.get("score", 0))
    for path in sorted(glob.glob(os.path.join(STORIES_DIR, "*.json"))):
        st = json.load(open(path))
        evs = [events[e["event_id"]] for e in st["events"] if e["event_id"] in events]
        if not evs:
            continue
        evs_sorted = sorted(evs, key=lambda e: e["published_at"])
        deltas = delta_body(evs_sorted)
        original = next((e for e in evs_sorted if e["kind"] == "original"), evs_sorted[0])
        hc, hl, hv = heat(st.get("score", 0))
        src_domains = [display_domain(s) for s in st.get("sources", [])]
        src_domains = [display_domain(s) for s in st.get("sources", [])]
        cards.append({
            "id": st["id"],
            "title": st["title"],
            "url": f"stories/{st['id']}/",
            "snippet": md_snippet(original["content_md"]),
            "sources": src_domains,
            "cves": st.get("cves", []),
            "score": st.get("score", 0),
            "heat_class": hc,
            "heat_label": hl,
            "heat_var": hv,
            "heat_pct": min(100, int(st.get("score", 0) / max_score * 100)),
            "reddit": st.get("reddit_signal", {}).get("best_score") or None,
            "n_sources": st.get("n_sources", len(st.get("sources", []))),
            "first_seen": st.get("first_seen", evs_sorted[0]["published_at"]),
            "last_seen": st.get("last_seen", evs_sorted[-1]["published_at"]),
            "first_seen_human": reltime(st.get("first_seen", evs_sorted[0]["published_at"])),
            "last_seen_human": reltime(st.get("last_seen", evs_sorted[-1]["published_at"])),
            "events": [{
                "kind": e["kind"],
                "title": e.get("title", st["title"]),
                "source": display_domain(e["source"]),
                "url": e["url"],
                "published_human": reltime(e["published_at"]),
                "published_date": date_human(e["published_at"]),
                "published_at": e["published_at"],
                "pub_date": rfc2822(e["published_at"]),
                "snippet": md_snippet(e["content_md"], 400),
                "body_html": deltas[e["id"]]["body_html"],
                "is_mention": deltas[e["id"]]["is_mention"],
            } for e in sorted(evs_sorted,
                              key=lambda e: (e["kind"] != "original", e["published_at"]))],
        })
    return sorted(cards, key=lambda c: c["score"], reverse=True)


# ---------- feed contexts (RSS is an MVP requirement) ----------

def feed_all_items(cards):
    items = []
    for c in cards:
        for e in c["events"]:
            items.append({
                "title": e["title"],
                "link": e["url"],
                "pub_date": e["pub_date"],
                "iso": e["published_at"],
                "description": e["snippet"],
            })
    items.sort(key=lambda i: i["iso"], reverse=True)
    for it in items:
        del it["iso"]
    return items


def feed_hot_items(cards):
    return [{
        "title": c["title"],
        "link": site_url(c["url"]),
        "pub_date": rfc2822(c["last_seen"]),
        "description": c["snippet"],
    } for c in cards if c["score"] >= HOT_THRESHOLD]


def feed_daily_items(digest_dates, meta_by_date, limit=5):
    """Feed-daily = the latest digest PAGES, one item per day, newest first:
    title = the emoji headline, link = the digest page, description = summary."""
    items = []
    for d in reversed(digest_dates[-limit:]):
        meta = meta_by_date.get(d, {})
        items.append({
            "title": meta.get("headline") or f"Daily threat landscape — {d}",
            "link": site_url(f"daily/{d}/"),
            "pub_date": rfc2822(f"{d}T{DIGEST_RUN_UTC}"),
            "description": meta.get("summary") or "The day's top stories, once a day.",
        })
    return items


# ---------- render ----------

def render(template, **ctx):
    return env.get_template(template).render(**ctx)


LINT_HITS = []


def lint_links():
    """Every internal href/src in generated HTML must resolve (against the base,
    i.e. root-relative-without-slash) to an existing output file. Same-directory
    relative links like href=\"feed-daily.xml\" from /feeds/ resolve to the base
    root and are caught here."""
    bad = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "engine")]
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), ROOT)
            content = open(os.path.join(root, fn)).read()
            for m in re.finditer(r'(?:href|src)="([^"]+)"', content):
                url = m.group(1)
                if url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                    continue
                target = url.split("#")[0].split("?")[0]
                if target.startswith("/"):
                    bad.append((rel, url, "origin-absolute, not base-relative"))
                    continue
                resolved = target.rstrip("/") + "/index.html" if target.endswith("/") or target == "." or target == "" else target
                if target in ("", "."):
                    resolved = "index.html"
                if not os.path.exists(os.path.join(ROOT, resolved)):
                    bad.append((rel, url, f"resolves to {resolved!r}, which does not exist"))
    return bad


def lint_chips():
    """Chips must render domains, never full URLs."""
    bad = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "engine")]
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), ROOT)
            content = open(os.path.join(root, fn)).read()
            for m in re.finditer(r'<span class="chip[^"]*">([^<]*)</span>', content):
                if "://" in m.group(1).lower():
                    bad.append((rel, m.group(1)[:70]))
    return bad


def lint_backlinks(cards):
    """Completeness: every story must have >=1 digest backlink, and every digest
    analysis link must resolve to an existing story."""
    errs = []
    story_ids = {c["id"] for c in cards}
    for c in cards:
        if not c.get("digests"):
            errs.append(f"story {c['id']}: zero digest backlinks")
    for d in os.listdir(DIGESTS_DIR):
        if not d.endswith(".md"):
            continue
        body = open(os.path.join(DIGESTS_DIR, d)).read()
        for s in re.findall(r"\]\(stories/([^/]+)/\)", body):
            if s not in story_ids:
                errs.append(f"digest {d}: link to unknown story {s}")
    return errs


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    if rel.endswith(".html"):
        for m in re.finditer(r'(?:href|src|action)="/', content):
            snippet = content[max(0, m.start() - 34):m.end() + 16].replace("\n", " ")
            LINT_HITS.append((rel, snippet))
            print(f"WARN {rel}: path-absolute internal URL (resolves against the origin,"
                  f" not the Pages base): …{snippet}…", file=sys.stderr)
    print(f"  {rel}")


def main():
    events = load_events()
    cards = load_stories(events)
    hot_cards = [c for c in cards if c["score"] >= HOT_THRESHOLD]
    home_cards = hot_cards if len(hot_cards) >= 2 else cards[:30]

    manifest = {}
    manifest_path = os.path.join(ENGINE, "data", "manifest.json")
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path))
    digest_dates = sorted(
        os.path.splitext(f)[0] for f in os.listdir(DIGESTS_DIR)
        if f.endswith(".md") and re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", f)
    )
    story_days = {}
    for d, slugs in manifest.get("stories_per_day", {}).items():
        for s in slugs:
            story_days.setdefault(s, []).append(d)
    # union: any digest whose ANALYSIS explicitly links a story also backlinks it
    for d in digest_dates:
        body = open(os.path.join(DIGESTS_DIR, d + ".md")).read()
        for s in re.findall(r"\]\(stories/([^/]+)/\)", body):
            story_days.setdefault(s, []).append(d)
    for c in cards:
        days = sorted({x for x in story_days.get(c["id"], [])}, reverse=True)
        c["digests"] = [{"date": x, "url": f"daily/{x}/"} for x in days]
        ap = os.path.join(ENGINE, "data", "analysis", c["id"] + ".md")
        if os.path.exists(ap):
            c["analysis_html"] = sanitize(md_to_html(open(ap).read(), output_format="html5"))
        else:
            c["analysis_html"] = ""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    rfc_now = format_datetime(datetime.now(timezone.utc))

    print(f"rendering {len(cards)} stories, {len(hot_cards)} hot, feeds...")

    write("index.html", render("index.html", active="index",
                               hero=home_cards[0] if home_cards else None,
                               cards=home_cards[1:]))
    write("404.html", render("404.html", active=None))
    write("feeds/index.html", render("feeds.html", active="feeds"))
    write("style.css", open(os.path.join(TMPL_DIR, "style.css")).read())
    write("robots.txt", open(os.path.join(TMPL_DIR, "robots.txt")).read())

    derived = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stories": [{
            "id": c["id"], "title": c["title"], "url": site_url(c["url"]),
            "score": c["score"], "sources": c["sources"], "cves": c["cves"],
            "reddit_signal": {"best_score": c["reddit"] or 0},
            "first_seen": c["first_seen"], "last_seen": c["last_seen"],
            "snippet": c["snippet"],
            "events": [{
                "kind": e["kind"], "title": e["title"], "source": e["source"],
                "url": e["url"], "published_at": e["published_at"],
            } for e in c["events"]],
        } for c in cards],
    }
    write("stories.json", json.dumps(derived, indent=1))

    for c in cards:
        write(f"stories/{c['id']}/index.html", render("story.html", active=None, story=c))
    years = sorted({c["first_seen"][:4] for c in cards}, reverse=True)
    months = [(i, __import__("calendar").month_name[i]) for i in range(1, 13)]
    write("stories/index.html", render("stories-all.html", active="all",
                                       cards=cards, total=len(cards),
                                       years=years, months=months))

    build_today = datetime.now(LOCAL_TZ).strftime("%Y-%m-%d")
    cards_by_id = {c["id"]: c for c in cards}

    def day_cards(date):
        """The stories the digest's narrative actually covered: the digest's explicit
        'stories' field (analyst-authored) if present, else the manifest stories with a
        backport event dated that day. Live engine events never inflate a digest's list."""
        meta = digest_meta.get(date, {})
        if meta.get("stories"):
            slugs = [s for s in meta["stories"] if s in cards_by_id]
        else:
            slugs = []
            for slug in manifest.get("stories_per_day", {}).get(date, []):
                sp = os.path.join(STORIES_DIR, slug + ".json")
                if not os.path.exists(sp):
                    continue
                stj = json.load(open(sp))
                if any(events.get(ref["event_id"]) and
                       ":" not in events[ref["event_id"]]["id"] and
                       events[ref["event_id"]]["published_at"][:10] == date
                       for ref in stj.get("events", [])):
                    slugs.append(slug)
        return sorted((cards_by_id[s] for s in slugs), key=lambda c: -c["score"])[:DIGEST_TOP_N]

    digest_meta = {}
    for d in digest_dates:
        mp = os.path.join(DIGESTS_DIR, d + ".json")
        if os.path.exists(mp):
            digest_meta[d] = json.load(open(mp))
    digests_meta = []
    for d in reversed(digest_dates):                      # newest first
        md_content = open(os.path.join(DIGESTS_DIR, d + ".md")).read()
        analysis_html = sanitize(md_to_html(md_content, output_format="html5"))
        meta = digest_meta.get(d, {})
        write(f"daily/{d}/index.html", render("daily.html", active="daily", digest={
            "date": d,
            "headline": meta.get("headline") or f"Daily threat landscape — {d}",
            "summary": meta.get("summary", ""),
            "analysis_html": analysis_html,
            "stories": [{
                "title": c["title"],
                "url": c["url"],
                "last_seen_human": c["last_seen_human"],
            } for c in day_cards(d)],
        }))
        digests_meta.append({"date": d, "url": f"daily/{d}/",
                             "headline": meta.get("headline") or f"Daily threat landscape — {d}",
                             "summary": meta.get("summary", "")})
    write("daily/index.html", render("daily-index.html", active="daily", digests=digests_meta))
    # old-scheme redirects: posts/YYYY-MM-DD-daily-summary/ -> daily/YYYY-MM-DD/
    # targets are ABSOLUTE (relative meta-refresh URLs resolve against the page
    # path, not the base, in some browsers — verified broken)
    for d in digest_dates:
        write(f"posts/{d}-daily-summary/index.html",
              render("redirect.html", target_abs=site_url(f"daily/{d}/")))
    digest_date = digest_dates[-1] if digest_dates else build_today

    write("sitemap.xml", render("sitemap.xml", stories=cards))

    # feeds — MVP: all / hot / daily
    all_items = feed_all_items(cards)
    feeds = [
        ("feeds/feed-all.xml", "Tia N. List — Every article",
         "Every article, newest first.", "/feeds/feed-all.xml",
         all_items, rfc_now),
        ("feeds/feed-hot.xml", "Tia N. List — Hot stories",
         f"Stories scoring {HOT_THRESHOLD}+ on the hot ranking.", "/feeds/feed-hot.xml",
         feed_hot_items(cards), rfc_now),
        ("feeds/feed-daily.xml", "Tia N. List — Daily digest",
         "The daily threat landscape, one item per day.", "/feeds/feed-daily.xml",
         feed_daily_items(digest_dates, digest_meta), rfc_now),
    ]
    for rel, title, desc, self_url, items, built in feeds:
        write(rel, render("feed.xml", feed={
            "title": title, "description": desc, "self": self_url,
            "last_build": built, "entries": items,
        }))

    print("done.")

    bad_links = lint_links()
    for rel, url, why in bad_links:
        print(f"LINK FAIL {rel}: href/src {url!r} {why}", file=sys.stderr)
    bad_chips = lint_chips()
    for rel, chip in bad_chips:
        print(f"CHIP FAIL {rel}: full URL in chip {chip!r} (must be a domain)", file=sys.stderr)
    backlink_errs = lint_backlinks(cards)
    for e in backlink_errs:
        print(f"BACKLINK FAIL {e}", file=sys.stderr)
    if LINT_HITS or bad_links or bad_chips or backlink_errs:
        print(f"LINT FAIL: {len(LINT_HITS)} path-absolute + {len(bad_links)} unresolvable"
              f" internal URL(s) + {len(bad_chips)} URL-in-chip + {len(backlink_errs)}"
              " backlink errors in generated HTML — fix before publishing.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
