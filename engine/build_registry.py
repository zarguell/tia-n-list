#!/usr/bin/env python3
"""Convert 30 days of legacy Tia daily digests into the Storyline hybrid store.

Deterministic pass 1 of the conversion (no LLM): parse entries, cluster them
GLOBALLY across all days (CVE-bridge + title-token similarity) so multi-week
stories merge into one story by construction, and emit a staged store under
conversion/ mirroring engine/data's layout. Subagents author the per-day
analyses afterwards; nothing here creates or merges stories.

Outputs (staging, for review before swap):
  conversion/events/<id>.md + <id>.json   one event per digest entry
  conversion/stories/<slug>.json          clustered stories (original/update labels)
  conversion/manifest.json                day -> assigned story slugs (for digests)

Usage: python3 build_registry.py [--days 30]
"""
import glob
import json
import os
import re
import sys
import hashlib
from datetime import datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
DIGESTS_SRC = "/home/coder/workspace/tia-n-list-pipeline/daily-digests"
OUT = os.path.join(ENGINE, "conversion")

CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
SRC_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TRAILING_LINKS = re.compile(r"(\[[^\]]+\]\([^)]+\)\s*[;·]?\s*)+[\]·;]?$")
MARKER_RE = re.compile(r"^\s*\[?(UPDATE|NEW|SPONSORED|ANALYSIS|EXCLUSIVE|FIX|GUIDE|GAP)\s*[:\]]?\s*", re.I)
EMOJI_RE = re.compile(r"^[^\w#\[]{0,10}[\U0001F000-\U0001FAFF\u2600-\u27BF\U0001F300-\U0001F5FF]+\s*")
STOP = set("""the a an and or of in on at to for with via new update says report week year months
after before over under by from as its it is are was were has have been this that these those
which who whom whose more most some any all also over amid into against among between""".split())

CYBER_STOP = set("""security threat malware ransomware vulnerability vulnerabilities zero day zero-day
exploit exploits exploited exploitation attacker attackers attack attacks campaign campaigns breach
breaches data leak leaks exposed critical actively disclosed disclosure patched patch patches fixed
fix fixes advisory warns warning targeted target targets victims victim organizations organization
company companies users user researchers researcher flaw flaws bug bugs issue issues tool tools
group groups operation operations activity active cve cvss kev adds added confirmed confirms first
latest official hackers hacking cyber cyberattack cyberattacks hackers hacking intelligence intel
report reports reporting analysis analyzes analyst analysts update updates warning warnings alert
alerts flagged flags marks marking ongoing large-scale large scale new-old massive major minor high
medium low severe details detail deep-dive deep dive look takes takes-on takes-on takes-on threat
actors actor group groups nationwide global regional industrial government gov state federal agencies
agency researchers research reveal reveals exposing exposed hits hit strike strikes strikes-on
targeting targeting-again again resurfaces returns return back again still now today week weeks month
months year years day days hour hours minute minutes""".split())

def domain_of(url):
    m = re.match(r"https?://(?:www\.)?([^/:]+)", url or "")
    return m.group(1).lower() if m else ""


def slugify(title, max_len=64):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:max_len].rstrip("-")


def clean_title(title):
    t = EMOJI_RE.sub("", title)
    t = MARKER_RE.sub("", t)
    t = re.sub(r"\*\*", "", t)
    t = re.sub(r"\s*\[(web search|tl;dr sec|r/cybersecurity|gap)[^\]]*\]\s*$", "", t, flags=re.I)
    t = re.sub(r"\s*See\s+\S+\s+section above\.?\s*", " ", t)
    t = re.sub(r"\s*\[\[[^\]]*\]\([^)]*\)\]\s*$", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


QUALITY = {"reuters.com": 1.15, "apnews.com": 1.1, "bbc.com": 1.1,
           "bloomberg.com": 1.1, "securityweek.com": 1.0, "thehackernews.com": 1.0,
           "bleepingcomputer.com": 1.0, "krebsonsecurity.com": 1.05, "wired.com": 1.0,
           "arstechnica.com": 1.0, "theregister.com": 0.9, "darkreading.com": 0.9,
           "cyberscoop.com": 0.9, "recordedfuture.com": 0.9, "thedfirreport.com": 1.0,
           "gbhackers.com": 0.8, "malware.news": 0.8}
DEFAULT_QUALITY = 0.75


def provisional_score(first_seen, last_seen, sources, cves):
    """Deterministic placeholder score scaled to the site's 0-6 display range
    (M1 will replace with real miniflux/reddit signals). Recency half-life 72h,
    breadth, outlet quality, CVE bonus."""
    last = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
    hours = (datetime.now(timezone.utc) - last).total_seconds() / 3600
    recency = 2.718 ** (-max(0, hours) / 72)
    breadth = 1 + 0.6 * (len(set(sources)) - 1)
    q = max((QUALITY.get(d, DEFAULT_QUALITY) for d in sources), default=DEFAULT_QUALITY)
    bonus = 1.0 if cves else 0.0
    return round(min(6.0, recency * breadth * q * 2 + bonus), 1)


def tokens(title):
    t = EMOJI_RE.sub("", title)
    t = MARKER_RE.sub("", t)
    t = re.sub(r"[^a-z0-9\s]", " ", t.lower())
    return {w for w in t.split() if len(w) >= 4 and w not in STOP and w not in CYBER_STOP}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def parse_digest(path):
    date = os.path.basename(path)[:10]
    lines = open(path, encoding="utf-8").read().splitlines()
    entries = []
    cur = None
    date_h3 = re.compile(r"^[A-Z][a-z]+ \d{1,2}, \d{4}$")
    for ln in lines:
        if ln.startswith("### "):
            if date_h3.match(ln[4:].strip()):
                continue                       # old-format date line, not an entry
            if cur:
                entries.append(cur)
            raw = ln[4:]
            marker = "update" if re.search(r"\[UPDATE\]", ln) else "new"
            cur = {"date": date, "title": "", "marker": marker, "body": [], "sources": []}
            title = EMOJI_RE.sub("", raw).strip()
            title = title.rstrip("*").strip()
            title = MARKER_RE.sub("", title).strip()
            cur["title"] = title
        elif ln.startswith("**[") and not ln.startswith("**[" + "Sources"):
            if cur:
                entries.append(cur)
            raw = ln[2:]
            marker = "update" if re.search(r"\[UPDATE\]", ln) else "new"
            cur = {"date": date, "title": "", "marker": marker, "body": [], "sources": []}
            title = EMOJI_RE.sub("", raw).strip()
            title = title.rstrip("*").strip()
            title = MARKER_RE.sub("", title).strip()
            cur["title"] = title
        elif ln.startswith("## ") or ln.startswith("# "):
            if cur:
                entries.append(cur)
                cur = None
        elif cur is not None:
            s = ln.strip()
            if "**Source" in s or s.startswith("*Source"):
                tail = re.split(r"\*+Sources?:", s, maxsplit=1)[-1]
                cur["sources"] = SRC_RE.findall(tail)
            elif re.match(r"^\[[^\]]+\]\([^)]+\)", s):
                cur["sources"] = SRC_RE.findall(s)
            elif s:
                wrap = re.search(r"\[\[", s)
                if wrap:
                    cur["sources"] = SRC_RE.findall(s[wrap.start():])
                    rest = s[:wrap.start()].rstrip()
                    if rest:
                        cur["body"].append(rest)
                else:
                    m = TRAILING_LINKS.search(s)
                    if m and m.group(0).count("(") >= 2:
                        cur["sources"] = SRC_RE.findall(m.group(0))
                        rest = s[:m.start()].rstrip(" ;·")
                        if rest:
                            cur["body"].append(rest)
                    else:
                        cur["body"].append(ln.strip())
    if cur:
        entries.append(cur)
    for e in entries:
        e["body"] = "\n\n".join(e["body"]).strip()
        e["cves"] = sorted({c.upper() for c in CVE_RE.findall(e["title"] + " " + e["body"])})
    return entries


class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def cluster(entries):
    uf = UF()
    ids = [e["id"] for e in entries]
    # CVE bridge uses TITLE CVEs only — body-mentioned CVEs (policy roundups
    # listing the day's flaws) are weak signals that bridge unrelated stories.
    cve_sets = {e["id"]: {c.upper() for c in CVE_RE.findall(e["title"])} for e in entries}
    # CVE bridge: merge only FOCUSED entries (<=2 CVEs each) with a large shared
    # fraction. Multi-CVE "roundup" entries (e.g. "CISA Adds 4 Flaws to KEV")
    # must not bridge unrelated stories — they join via title tokens only.
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if uf.find(a) == uf.find(b):
                continue
            ca, cb = cve_sets[a], cve_sets[b]
            if not ca or not cb or len(ca) > 2 or len(cb) > 2:
                continue
            shared = ca & cb
            if shared and len(shared) / min(len(ca), len(cb)) >= 0.5:
                uf.union(a, b)
    # token similarity pass (O(n^2) is fine at this scale). Only SPECIFIC tokens
    # (cyber stopwords filtered) count; no containment rule — it chain-merged
    # unrelated stories on generic tokens with the full backlog.
    tok = {e["id"]: tokens(e["title"]) for e in entries}
    for i in range(len(ids)):
        ta = tok[ids[i]]
        if len(ta) < 2:
            continue
        for j in range(i + 1, len(ids)):
            if uf.find(ids[i]) == uf.find(ids[j]):
                continue
            tb = tok[ids[j]]
            if len(tb) < 2:
                continue
            if jaccard(ta, tb) >= 0.5:
                uf.union(ids[i], ids[j])
    return uf


def frontmatter_field(text, key):
    m = re.search(rf"^{key}:\s*(.*)$", text, re.M)
    if not m:
        return ""
    v = m.group(1).strip()
    if v.startswith('"') and v.endswith('"'):
        v = v[1:-1].replace('\\"', '"')
    elif v.startswith("'") and v.endswith("'"):
        v = v[1:-1]
    return v


def emit_digest_metadata(dates):
    """Extract the legacy emoji headline + executive summary from the Hugo posts
    frontmatter into digests/<date>.json (hybrid store: md content + json metadata)."""
    posts = "/home/coder/workspace/tia-n-list/hugo/content/posts"
    out = 0
    for d in dates:
        path = os.path.join(posts, f"{d}-daily-summary.md")
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        meta = {"date": d, "headline": frontmatter_field(text, "title"),
                "summary": frontmatter_field(text, "summary")}
        if meta["headline"] or meta["summary"]:
            json.dump(meta, open(os.path.join(OUT, "digests", d + ".json"), "w"), indent=1)
            out += 1
    return out


def main():
    days = 30
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])
    files = sorted(glob.glob(os.path.join(DIGESTS_SRC, "*.md")))[-days:]
    print(f"parsing {len(files)} digests ({files[0][-10:] if files else '?'} .. {files[-1][-10:] if files else '?'})")

    entries = []
    for f in files:
        for e in parse_digest(f):
            e["id"] = "e" + hashlib.sha1(
                (e["sources"][0] if e["sources"] else e["date"] + e["title"]).encode()
            ).hexdigest()[:10]
            entries.append(e)

    # dedupe entries globally by id (same article URL re-covered on later days
    # is the same event; duplicates also chained bogus unions)
    seen_ids = set()
    entries_dedup = []
    for e in entries:
        if e["id"] in seen_ids:
            continue
        seen_ids.add(e["id"])
        entries_dedup.append(e)
    entries = entries_dedup
    print(f"entries: {len(entries)}")

    uf = cluster(entries)
    groups = {}
    for e in entries:
        groups.setdefault(uf.find(e["id"]), []).append(e)

    os.makedirs(os.path.join(OUT, "events"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "stories"), exist_ok=True)
    manifest = {"days": [os.path.basename(f)[:10] for f in files], "stories_per_day": {}}

    story_count = 0
    multi_day = 0
    used_event_ids = set()
    for root, group in groups.items():
        group.sort(key=lambda e: e["date"])
        story_count += 1
        first = group[0]
        title = clean_title(first["title"])
        slug = slugify(title)
        # disambiguate slug collisions
        if slug in manifest.setdefault("slugs", set()):
            slug = slug + "-" + str(story_count)
        manifest["slugs"].add(slug)
        sources = []
        for e in group:
            sources.extend(e["sources"])
        cves = sorted({c for e in group for c in e["cves"]})
        events_refs = []
        for idx, e in enumerate(group):
            kind = "original" if idx == 0 else "update"
            eid = e["id"]
            if eid in used_event_ids:      # same article cited in another story
                eid = eid + "-" + str(story_count)
            used_event_ids.add(eid)
            body = e["body"] or clean_title(e["title"])
            with open(os.path.join(OUT, "events", eid + ".md"), "w") as f:
                f.write(body + "\n")
            json.dump({"id": eid, "title": clean_title(e["title"]), "kind": kind,
                       "source": domain_of(e["sources"][0]) if e["sources"] else "",
                       "url": e["sources"][0] if e["sources"] else "",
                       "published_at": e["date"] + "T00:00:00Z",
                       "cves": e["cves"]}, open(os.path.join(OUT, "events", eid + ".json"), "w"), indent=1)
            events_refs.append({"event_id": eid, "label": kind})
            manifest["stories_per_day"].setdefault(e["date"], []).append(slug)
        if len({e["date"] for e in group}) > 1:
            multi_day += 1
        domains = list(dict.fromkeys(domain_of(s) for s in sources if s))
        score = provisional_score(group[0]["date"] + "T00:00:00Z",
                                  group[-1]["date"] + "T00:00:00Z", sources, cves)
        json.dump({"id": slug, "title": title,
                   "first_seen": group[0]["date"] + "T00:00:00Z",
                   "last_seen": group[-1]["date"] + "T00:00:00Z",
                   "sources": domains,
                   "n_sources": len(domains),
                   "cves": cves, "score": score,
                   "reddit_signal": {"posts": 0, "best_score": 0},
                   "events": events_refs},
                  open(os.path.join(OUT, "stories", slug + ".json"), "w"), indent=1)

    # drop the scratch slugs set from the manifest
    manifest.pop("slugs", None)
    # sort per-day lists by date then keep order
    for d in manifest["stories_per_day"]:
        manifest["stories_per_day"][d] = list(dict.fromkeys(manifest["stories_per_day"][d]))
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    meta_count = emit_digest_metadata([os.path.basename(f)[:10] for f in files])
    print(f"stories: {story_count} | multi-day: {multi_day} | days: {len(files)} | digest metadata: {meta_count}")
    print(f"staged at {OUT}")


if __name__ == "__main__":
    main()
