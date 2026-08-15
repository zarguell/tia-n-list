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
import bleach

ENGINE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENGINE)                       # repo root = Pages root
TMPL_DIR = os.path.join(ENGINE, "templates")
EVENTS_DIR = os.path.join(ENGINE, "data", "events")
STORIES_DIR = os.path.join(ENGINE, "data", "stories")
DIGESTS_DIR = os.path.join(ENGINE, "data", "digests")
CTI_DIR = os.path.join(ENGINE, "data", "cti")
ANALYSIS_DIR = os.path.join(ENGINE, "data", "analysis")

# bleach allowlist for article/analysis/digest bodies (the ONLY |safe renders).
# Tags/attrs/protocols here are the complete set that survives sanitize().
ALLOWED_TAGS = ["p", "br", "a", "strong", "em", "b", "i", "u", "s", "code", "pre",
                "blockquote", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6",
                "hr", "table", "thead", "tbody", "tr", "th", "td", "span", "div",
                "sup", "sub", "img", "figure", "figcaption"]
ALLOWED_ATTRS = {
    "a": ["href", "title"],
    "td": ["colspan", "rowspan"],
    "th": ["colspan", "rowspan"],
    "img": ["src", "alt", "title"],
    "code": ["class"],
    "pre": ["class"],
}
ALLOWED_PROTOCOLS = {"http", "https", "mailto"}
LOCAL_TZ = ZoneInfo("America/New_York")          # pipeline convention; digest runs 11:15 UTC = 07:15 EDT
DIGEST_RUN_UTC = "11:15:00Z"                      # stable pubDate anchor for the daily feed
BASE_URL = "https://zarguell.github.io/tia-n-list"


def site_url(path):
    """Join a base-relative path (e.g. 'stories/x/' or '/daily/') to the site URL."""
    return BASE_URL + "/" + path.lstrip("/")
HOT_THRESHOLD = 5.0      # display "hot" = the heat() h2 band; merge.py keeps its own 3.3 analysis-queue gate
DIGEST_TOP_N = 10      # not a hard limit — how many stories the digest page lists

def pl(n, word):
    """'1 day' / '3 days' for template gap strings; None -> empty."""
    if n is None:
        return ""
    try:
        n = int(n)
    except (TypeError, ValueError):
        return f"{n} {word}s"
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


env = Environment(
    loader=FileSystemLoader(TMPL_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)
env.globals["site_url"] = site_url
env.globals["pl"] = pl

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
    """Parse-based HTML sanitizer (bleach / html5lib): allowlist tags,
    attributes and protocols; everything else is stripped with content kept.

    This replaced the regex sanitizer after the 2026-08-11 audit proved it
    bypassable in real browsers: <svg/onload=…> and <img … /onerror=…>
    (slash-prefixed handlers), entity-encoded schemes (jav&#x61;script:),
    and non-href active attributes (action, xlink:href) all survived regex
    filtering. bleach tokenizes per the HTML spec, decodes character
    references BEFORE protocol checks, and drops any attribute not in the
    allowlist — the bypass classes above cannot survive.
    """
    return bleach.clean(
        html_text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def heat(score, last_seen=None):
    # bands are fixed tiers on the 0-10 scale (warm >= 3.3, hot >= 5.0, hottest >= 7.5) —
    # independent of HOT_THRESHOLD, which gates hot_cards/feed-hot/home
    if score >= 7.5:
        return "h3", "hottest", "heat-3"
    if score >= 5.0:
        return "h2", "hot", "heat-2"
    if score >= 3.3:
        return "h1", "warm", "heat-1"
    if last_seen:
        dt = parse_utc(last_seen)
        age_days = (datetime.now(timezone.utc) - dt).total_seconds() / 86400
        if age_days <= 7:
            return "none", "new", "gray-500"
    return "", "", ""    # old and cold: no badge


# ---------- store loading ----------

def load_events():
    from store import load_events as _load
    global store_safe_url
    from store import safe_url as store_safe_url
    events = _load()
    for e in events.values():
        e["html"] = sanitize(md_to_html(e["content_md"], output_format="html5"))
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


def _card_snippet(st, original):
    """Story-card snippet, analysis-preferred.

    The card on / (hot) and /stories/ (all) used to show the FIRST ORIGINAL
    EVENT's auto-extracted body. Sites that strip article bodies (e.g. the
    GeoServer zero-day story's original event is a bare "\\n") rendered
    literally nothing even when an analyst-written analysis existed — and when
    we DID write an analysis it is a better summary than any extracted body.
    So: analysis file exists and has text -> snippet from it (trimmed at a
    sentence boundary, never mid-sentence); otherwise the old event fallback.
    """
    ap = os.path.join(ANALYSIS_DIR, st["id"] + ".md")
    if os.path.exists(ap):
        plain = md_text(open(ap).read())
        if plain:
            if len(plain) <= 600:
                return plain
            out = ""
            for sent in SENT_SPLIT.split(plain):
                if out and len(out) + len(sent) + 1 > 600:
                    break
                out = f"{out} {sent}".strip()
            return out or plain[:600]
    return md_snippet(original["content_md"])


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
        hc, hl, hv = heat(st.get("score", 0), st.get("last_seen"))
        src_domains = [display_domain(s) for s in st.get("sources", [])]
        src_domains = [display_domain(s) for s in st.get("sources", [])]
        cards.append({
            "id": st["id"],
            "title": st["title"],
            "url": f"stories/{st['id']}/",
            "snippet": _card_snippet(st, original),
            "sources": src_domains,
            "cves": st.get("cves", []),
            "score": st.get("score", 0),
            "heat_class": hc,
            "heat_label": hl,
            "heat_var": hv,
            "heat_pct": min(100, int(st.get("score", 0) / max_score * 100)),
            "reddit": st.get("reddit_signal", {}).get("best_score") or None,
            "score_breakdown": st.get("score_breakdown", {}),
            "n_sources": st.get("n_sources", len(st.get("sources", []))),
            "first_seen": st.get("first_seen", evs_sorted[0]["published_at"]),
            "last_seen": st.get("last_seen", evs_sorted[-1]["published_at"]),
            "first_seen_human": reltime(st.get("first_seen", evs_sorted[0]["published_at"])),
            "last_seen_human": reltime(st.get("last_seen", evs_sorted[-1]["published_at"])),
            "events": [{
                "kind": e["kind"],
                "event_id": e["id"],
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
    # kev cross-link join: which of a story's CVEs have a kevrichment record?
    # (story cves are CVE_RE-validated + upper-cased at ingestion, so the
    # normalized membership check is exact; template renders linked chips)
    import kev as kev_mod
    kev_ids = kev_mod.kev_id_set()
    for c in cards:
        c["kev_cves"] = [x for x in c["cves"] if kev_mod.gate_cve(x) in kev_ids]
        # card chip rows are trimmed for the grid: 2 outlets + "+N more";
        # KEV CVEs first, 2 shown + "+N more". Full lists stay on c["sources"]
        # / c["cves"] (story page + all-stories search keep everything).
        c["card_sources"] = c["sources"][:2]
        c["sources_more"] = max(0, len(c["sources"]) - 2)
        kev_first = [x for x in c["cves"] if x in c["kev_cves"]] + \
                    [x for x in c["cves"] if x not in c["kev_cves"]]
        c["card_cves"] = kev_first[:2]
        c["cves_more"] = max(0, len(c["cves"]) - 2)
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
        dirs[:] = [d for d in dirs if d not in (".git", "engine", "kevrichment")]
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), ROOT)
            content = open(os.path.join(root, fn)).read()
            # href/src attributes AND inline-script fetch() targets: both must
            # resolve (against the base) to an existing output file. fetch URLs
            # used to escape the href/src check (2026-08-13: the candidates
            # dashboard fetched 'kev-candidates-index.json', resolving to the
            # repo root -> live 404; the kev dashboard's 'kev/kev-index.json'
            # was the correct base-relative form).
            for m in re.finditer(
                    r'(?:href|src)="([^"]+)"|fetch\(([\'"])([^\'"]+)\2\)', content):
                url = m.group(1) or m.group(3)
                # JS-generated hrefs (string concatenation in inline scripts)
                # are built at runtime from location.pathname — not lintable
                if "'" in url or "+" in url:
                    continue
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
        dirs[:] = [d for d in dirs if d not in (".git", "engine", "kevrichment")]
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), ROOT)
            content = open(os.path.join(root, fn)).read()
            for m in re.finditer(r'<span class="chip[^"]*">([^<]*)</span>', content):
                if "://" in m.group(1).lower():
                    bad.append((rel, m.group(1)[:70]))
    return bad


def lint_kev_links(cards):
    """Scoped link lint for `--kev` mode: walks /kev/ only (a fresh clone has
    no other generated output). KeV-internal targets must resolve on disk;
    stories/<slug>/ must be a loaded card (data-level existence); base.html
    chrome + footer targets are exempt from existence (they exist only in the
    full build); scheme/format behavior mirrors lint_links (defense-in-depth
    behind kev.py's safe_url allowlist)."""
    card_ids = {c["id"] for c in cards}
    bad = []
    kev_root = os.path.join(ROOT, "kev")
    if not os.path.isdir(kev_root):
        return [("kev/", "(missing)", "kev section not built")]
    # base.html chrome + footer + head targets, not generated by --kev
    exempt = {"", ".", "./", "index.html",
              "stories/", "daily/", "feeds/", "cti/", "methodology/", "about/",
              "style.css", "404.html", "robots.txt", "stories-index.json",
              "feeds/feed-all.xml", "feeds/feed-hot.xml", "feeds/feed-daily.xml",
              "feeds/feed-kev.xml"}
    for root, dirs, files in os.walk(kev_root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in sorted(files):
            if not fn.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), ROOT)
            content = open(os.path.join(root, fn)).read()
            # href/src + inline-script fetch() targets (mirrors lint_links)
            for m in re.finditer(
                    r'(?:href|src)="([^"]+)"|fetch\(([\'"])([^\'"]+)\2\)', content):
                url = m.group(1) or m.group(3)
                if "'" in url or "+" in url:
                    continue
                if url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                    continue
                target = url.split("#")[0].split("?")[0]
                if target.startswith("/"):
                    bad.append((rel, url, "origin-absolute, not base-relative"))
                    continue
                if target in exempt:
                    continue
                sm = re.match(r"^stories/([^/]+)/?$", target)
                if sm:
                    if sm.group(1) not in card_ids:
                        bad.append((rel, url, f"mentions story {sm.group(1)!r}, not in the loaded cards"))
                    continue
                resolved = (target.rstrip("/") + "/index.html" if (target.endswith("/") or target in (".", ""))
                            else target)
                if target in ("", "."):
                    resolved = "index.html"
                if not os.path.exists(os.path.join(ROOT, resolved)):
                    bad.append((rel, url, f"resolves to {resolved!r}, which does not exist"))
    return bad


def lint_kev_chips():
    """Chip lint scoped to /kev/ (mirror of lint_chips)."""
    bad = []
    kev_root = os.path.join(ROOT, "kev")
    for root, dirs, files in os.walk(kev_root):
        dirs[:] = [d for d in dirs if d != ".git"]
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
    """Integrity: every digest narrative link and every explicit digest 'stories'
    entry must resolve to an existing story — INCLUDING merged-away stories
    (they render as redirect pages, so their URLs still work). (Stories with
    zero featured digests are legitimate — backlinks only exist for featured
    coverage.)"""
    errs = []
    story_ids = {c["id"] for c in cards}
    for p in sorted(glob.glob(os.path.join(STORIES_DIR, "*.json"))):
        st = json.load(open(p))
        if st.get("merged_into"):
            story_ids.add(st["id"])
    for d in os.listdir(DIGESTS_DIR):
        base = os.path.splitext(d)[0]
        if d.endswith(".md"):
            body = open(os.path.join(DIGESTS_DIR, d)).read()
            for s in re.findall(r"\]\(stories/([^/]+)/\)", body):
                if s not in story_ids:
                    errs.append(f"digest {d}: link to unknown story {s}")
        if d.endswith(".json"):
            meta = json.load(open(os.path.join(DIGESTS_DIR, d)))
            for s in meta.get("stories", []):
                if s not in story_ids:
                    errs.append(f"digest {base}: stories list references unknown story {s}")
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

    # --kev mode: self-contained kev-section build + scoped lints, used as the
    # kev automation's pre-push verify. A fresh clone has NO generated output
    # (all gitignored), so this writes the shared assets the kev pages
    # reference, loads the story cards for the Mentioned-in join (identical to
    # the full build), and runs the scoped fail-closed lints.
    if "--kev" in sys.argv:
        write("style.css", open(os.path.join(TMPL_DIR, "style.css")).read())
        write("404.html", render("404.html", active=None))
        write("robots.txt", open(os.path.join(TMPL_DIR, "robots.txt")).read())
        import kev as kev_mod
        kev_total = kev_mod.render_site(env, write, cards)
        print(f"kev section: {kev_total} CVEs")
        bad_links = lint_kev_links(cards)
        for rel, url, why in bad_links:
            print(f"KEV LINK FAIL {rel}: href/src {url!r} {why}", file=sys.stderr)
        bad_chips = lint_kev_chips()
        for rel, chip in bad_chips:
            print(f"KEV CHIP FAIL {rel}: full URL in chip {chip!r}", file=sys.stderr)
        if LINT_HITS or bad_links or bad_chips:
            print(f"KEV LINT FAIL: {len(LINT_HITS)} path-absolute + {len(bad_links)}"
                  f" kev link errors + {len(bad_chips)} chip errors - fix before publishing.",
                  file=sys.stderr)
            sys.exit(1)
        print("done (--kev).")
        return

    hot_cards = [c for c in cards if c["score"] >= HOT_THRESHOLD]

    manifest = {}
    manifest_path = os.path.join(ENGINE, "data", "manifest.json")
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path))
    digest_dates = sorted(
        os.path.splitext(f)[0] for f in os.listdir(DIGESTS_DIR)
        if f.endswith(".md") and re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", f)
    )
    story_days = {}
    # backlinks = FEATURED coverage only: a story is "covered in" a digest when the
    # digest's narrative links it OR its metadata lists it. The manifest day-assignment
    # (which the live engine extends with every ingested article) is NOT featured
    # coverage — it would backlink articles the digest never wrote about.
    for d in digest_dates:
        body = open(os.path.join(DIGESTS_DIR, d + ".md")).read()
        for s in re.findall(r"\]\(stories/([^/]+)/\)", body):
            story_days.setdefault(s, []).append(d)
        jp = os.path.join(DIGESTS_DIR, d + ".json")
        if os.path.exists(jp):
            meta = json.load(open(jp))
            for s in meta.get("stories", []):
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

    # home = hot only, capped at 30 (a wall of 97 near-identical cards was
    # visual noise; "All stories" is one click away); when fewer than 2
    # stories clear the hot bar (quiet weekend), fall back to the top-30 so
    # the page is never empty — the quiet banner explains the state
    home_cards = (hot_cards if len(hot_cards) >= 2 else cards)[:30]
    quiet = len(hot_cards) < 2
    print(f"rendering {len(cards)} stories, {len(hot_cards)} hot, {len(home_cards)} on home...")

    write("index.html", render("index.html", active="index", og_url=site_url(""),
                               hero=home_cards[0] if home_cards else None,
                               cards=home_cards[1:],
                               quiet=quiet,
                               hot_threshold=HOT_THRESHOLD,
                               total_hot=len(hot_cards)))
    write("404.html", render("404.html", active=None))
    write("feeds/index.html", render("feeds.html", active="feeds", og_url=site_url("feeds/")))
    write("methodology/index.html", render("methodology.html", active=None, og_url=site_url("methodology/")))
    write("about/index.html", render("about.html", active=None, og_url=site_url("about/")))

    # CTI & detection tier: matrix + case pages
    import cti as cti_mod
    import sigma as sigma_mod
    cti_records = cti_mod.load_records()
    cards_by_id_cti = {c["id"]: c for c in cards}
    has_detection = lambda sid: os.path.exists(os.path.join(CTI_DIR, sid + ".sigma")) or \
                                os.path.exists(os.path.join(CTI_DIR, sid + ".yara"))
    cti_matrix = cti_mod.build_matrix(cti_records, cards_by_id_cti, has_detection)
    cti_covered = cti_mod.all_covered(cti_matrix)
    write("cti/index.html", render("cti.html", active="cti", og_url=site_url("cti/"),
                                   matrix=cti_matrix, covered=cti_covered))
    # curated IOC set (built once, used by case sidecars, feeds and snapshots)
    import ioc as ioc_mod
    iocs = ioc_mod.build_index(cards, events)
    curated_path = os.path.join(ENGINE, "data", "iocs-curated.json")
    if os.path.exists(curated_path):
        curated = {c["value"]: c for c in json.load(open(curated_path))}
        kept = [i for i in iocs if i["value"] in curated]
        for i in kept:
            i["reason"] = curated[i["value"]]["reason"]
        iocs = kept
    for sid, r in cti_records.items():
        card = cards_by_id_cti.get(sid)
        texts = {}
        for suffix in (".sigma", ".splunk", ".kql", ".yara"):
            p = os.path.join(CTI_DIR, sid + suffix)
            texts[suffix.lstrip(".") + "_text"] = open(p).read() if os.path.exists(p) else ""
        rec_iocs = [i for i in iocs if sid in i["stories"]]
        write(f"cti/{sid}.ioc.json", json.dumps(rec_iocs, indent=1))
        tech_by_id = cti_mod.load_techniques()
        # Story link: only when the story actually renders (live card, or
        # merged-away -> redirect page). Orphaned stories (all events dropped
        # by triage, no merged_into) render no page - the link would 404.
        story_url = ""
        if sid in cards_by_id_cti:
            story_url = f"stories/{sid}/"
        else:
            sp = os.path.join(STORIES_DIR, sid + ".json")
            if os.path.exists(sp) and json.load(open(sp)).get("merged_into"):
                story_url = f"stories/{sid}/"
        r = {**r, "confidence": cti_mod.confidence(r, card),
             "updated_at": r.get("updated_at", r.get("_generated", today)),
             "references": [u for u in r.get("references", [])
                            if store_safe_url(u)],   # LLM-authored refs: http/https only
             "attack": [{**t, "tactic_name": tech_by_id.get(t["id"], {}).get("tactic_name", "")}
                        for t in r.get("attack", [])],
             "iocs": rec_iocs, "story_url": story_url, **texts}
        write(f"cti/{sid}/index.html", render("cti_case.html", active=None, rec=r,
                                      og_url=site_url(f"cti/{sid}/")))

    # Derive Splunk/KQL variants from the authored Sigma rules (deterministic —
    # never hand-written, so they cannot drift). Overwrites stale variants;
    # committed variants survive when sigma-cli is absent (e.g. CI fallback).
    for f in sorted(glob.glob(os.path.join(CTI_DIR, "*.sigma"))):
        slug = os.path.splitext(os.path.basename(f))[0]
        splunk, kql = sigma_mod.convert_variants(f)
        # raw rule + derived variants in the source store (committed)
        sigma_text = open(f).read()
        write(f"cti/{slug}.sigma", sigma_text)
        # Never overwrite a variant with 'None' when sigma-cli is absent or a
        # conversion fails — keep the existing committed/published variant.
        if splunk is not None:
            variant = f"# {slug} — Splunk SPL variant (derived from {slug}.sigma via sigma convert)\n{splunk}\n"
            with open(os.path.join(CTI_DIR, slug + ".splunk"), "w") as out:
                out.write(variant)
            write(f"cti/{slug}.splunk", variant)
        if kql is not None:
            variant = f"# {slug} — KQL variant (derived from {slug}.sigma via sigma convert)\n{kql}\n"
            with open(os.path.join(CTI_DIR, slug + ".kql"), "w") as out:
                out.write(variant)
            write(f"cti/{slug}.kql", variant)

    # author-authored YARA rules: publish raw for defenders
    for f in sorted(glob.glob(os.path.join(CTI_DIR, "*.yara"))):
        slug = os.path.splitext(os.path.basename(f))[0]
        write(f"cti/{slug}.yara", open(f).read())

    # IOC feeds (curated set -> JSON/CSV/TXT/STIX + readable page)
    corroborated = [i for i in iocs if i["confidence"] == "corroborated"]
    reported = [i for i in iocs if i["confidence"] != "corroborated"]
    write("cti/iocs/index.html", render("iocs.html", active="cti", og_url=site_url("cti/iocs/"),
                                        iocs=iocs, corroborated=corroborated,
                                        reported=reported, generated=today))
    write("cti/iocs/iocs.json", json.dumps(iocs, indent=1))
    write("cti/iocs/iocs.csv", ioc_mod.to_csv(iocs))
    write("cti/iocs/iocs.txt", ioc_mod.to_txt(iocs))
    write("cti/iocs/iocs-stix.json", ioc_mod.to_stix(iocs, BASE_URL + "/"))

    # Tier 4: immutable daily STIX snapshots + latest pointer + index page
    import snapshots as snap_mod
    snap_dir = os.path.join(ROOT, "cti", "snapshots", today)
    snap_mod.write_snapshot(iocs, cti_records, BASE_URL + "/", snap_dir, today)
    latest = {"date": today, "url": site_url("cti/snapshots/" + today + "/")}
    write("cti/snapshots/latest.json", json.dumps(latest, indent=1))
    snap_manifest = json.load(open(os.path.join(snap_dir, "manifest.json")))
    write("cti/snapshots/" + today + "/index.html",
          render("snapshot_day.html", active="cti", snap=snap_manifest,
                          og_url=site_url(f"cti/snapshots/{today}/")))
    snap_index = [{"date": d, "m": m}
                  for d, m in snap_mod.list_snapshots(os.path.join(ROOT, "cti", "snapshots"))]
    write("cti/snapshots/index.html", render("snapshots.html", active="cti", og_url=site_url("cti/snapshots/"),
                                             snapshots=snap_index,
                                             latest=snap_manifest))

    # KEV catalog section (/kev/) — kevrichment data rendered in the Tia design
    # system; story pages cross-link enriched CVEs via the kev_cves join
    import kev as kev_mod
    kev_total = kev_mod.render_site(env, write, cards)
    print(f"  kev section: {kev_total} CVEs")

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

    # compact index for the all-stories page (JS-windowed render): card fields
    # only, snippet trimmed, no events arrays — ~300KB vs 1.46MB of DOM nodes
    write("stories-index.json", json.dumps([{
        "id": c["id"], "title": c["title"], "url": c["url"],
        "score": c["score"], "first_seen": c["first_seen"], "last_seen": c["last_seen"],
        "heat_label": c.get("heat_label", ""), "heat_class": c.get("heat_class", ""),
        "reddit": c.get("reddit") or 0, "last_seen_human": c.get("last_seen_human", ""),
        "snippet": c["snippet"][:220], "sources": c["sources"], "cves": c["cves"],
        "kev_cves": c.get("kev_cves", []),
        "card_sources": c["card_sources"], "sources_more": c["sources_more"],
        "card_cves": c["card_cves"], "cves_more": c["cves_more"],
    } for c in cards]))

    for c in cards:
        write(f"stories/{c['id']}/index.html", render("story.html", active=None, story=c,
                                       og_url=site_url(f"stories/{c['id']}/")))

    # stories merged away by the LLM triage gate keep their URL working as a
    # redirect to the canonical story (digest links + old URLs must resolve)
    for path in sorted(glob.glob(os.path.join(STORIES_DIR, "*.json"))):
        st = json.load(open(path))
        if st.get("merged_into"):
            write(f"stories/{st['id']}/index.html",
                  render("redirect.html", target_abs=site_url(f"stories/{st['merged_into']}/")))
    years = sorted({c["first_seen"][:4] for c in cards}, reverse=True)
    months = [(i, __import__("calendar").month_name[i]) for i in range(1, 13)]
    write("stories/index.html", render("stories-all.html", active="all", og_url=site_url("stories/"),
                                       cards=sorted(cards, key=lambda c: c["last_seen"], reverse=True),
                                       total=len(cards),
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
        write(f"daily/{d}/index.html", render("daily.html", active="daily",
                                              og_url=site_url(f"daily/{d}/"), digest={
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
    write("daily/index.html", render("daily-index.html", active="daily", og_url=site_url("daily/"), digests=digests_meta))
    # old-scheme redirects: posts/YYYY-MM-DD-daily-summary/ -> daily/YYYY-MM-DD/
    # targets are ABSOLUTE (relative meta-refresh URLs resolve against the page
    # path, not the base, in some browsers — verified broken)
    for d in digest_dates:
        write(f"posts/{d}-daily-summary/index.html",
              render("redirect.html", target_abs=site_url(f"daily/{d}/")))
    digest_date = digest_dates[-1] if digest_dates else build_today

    write("sitemap.xml", render("sitemap.xml", stories=cards,
                                kev_entries=kev_mod.kev_sitemap_entries(kev_mod.load_index())))

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
        ("feeds/feed-kev.xml", "Tia N. List — KEV catalog",
         "New CISA KEV entries with kevrichment enrichment (90-day window).", "/feeds/feed-kev.xml",
         kev_mod.feed_items(kev_mod.load_index()), rfc_now),
        ("feeds/feed-kev-candidates.xml", "Tia N. List — KEV candidates",
         "Exploited CVEs Tia's reporting is tracking that CISA has not listed on the KEV catalog yet (the live candidate set).", "/feeds/feed-kev-candidates.xml",
         kev_mod.candidate_feed_items(), rfc_now),
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
    import cti as cti_mod
    cti_errs = cti_mod.validate_records(cti_mod.load_records())
    for e in cti_errs:
        print(f"CTI FAIL {e}", file=sys.stderr)
    import sigma as sigma_mod
    sigma_errs = []
    for f in sorted(glob.glob(os.path.join(CTI_DIR, "*.sigma"))):
        cli_errs, missing = sigma_mod.check_with_cli(f)
        if cli_errs is None and missing:
            # sigma-cli not installed — structural check only
            cli_errs = sigma_mod.validate_sigma(f)
        for e in cli_errs:
            sigma_errs.append(f"{os.path.basename(f)}: {e}")
    for f in sorted(glob.glob(os.path.join(CTI_DIR, "*.splunk"))):
        sigma_errs += [f"{os.path.basename(f)}: {e}" for e in sigma_mod.validate_variant(f, "splunk")]
    for f in sorted(glob.glob(os.path.join(CTI_DIR, "*.kql"))):
        sigma_errs += [f"{os.path.basename(f)}: {e}" for e in sigma_mod.validate_variant(f, "kql")]
    import yara as yara_mod
    yara_errs = []
    for f in sorted(glob.glob(os.path.join(CTI_DIR, "*.yara"))):
        yara_errs += yara_mod.validate_yara(f)
    for e in yara_errs:
        print(f"YARA FAIL {e}", file=sys.stderr)
    if LINT_HITS or bad_links or bad_chips or backlink_errs or cti_errs or sigma_errs or yara_errs:
        print(f"LINT FAIL: {len(LINT_HITS)} path-absolute + {len(bad_links)} unresolvable"
              f" internal URL(s) + {len(bad_chips)} URL-in-chip + {len(backlink_errs)}"
              f" backlink errors + {len(cti_errs)} CTI errors + {len(sigma_errs)}"
              f" Sigma errors + {len(yara_errs)} YARA errors — fix before publishing.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
