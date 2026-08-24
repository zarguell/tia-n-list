#!/usr/bin/env python3
"""Tia N. List — daily auditor: deterministic health/quality checks.

Emits JSON: {date, checks: {name: {ok, detail}}}. The LLM pass
(prompt-audit.txt) reads this, adds qualitative sampling of digest/analyses/
CTI records, and writes the human report to data/audits/<date>.md.

Every check is best-effort and never crashes the run — a failed check is a
data point, not a fatal error. Checks cover: the other automations' run
status (via the automation service API), digest/hourly/CTI freshness, queue
drain, store invariants, detection validity, live site, snapshot pin.
"""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENGINE)
DATA = os.path.join(ENGINE, "data")
NOW = datetime.now(timezone.utc)
TODAY = NOW.strftime("%Y-%m-%d")

# the automations this site depends on (ids as registered in the service)
AUTOMATIONS = {
    "hourly": "9ae955b1-cbc7-4fbf-a60e-c4bb619beacf",
    "digest": "c2d673b5-6646-4f08-9360-ef0fc53f1455",
    "cti": "58c9d1b0-29cb-4f36-920c-8537106b488f",
    "safety_net": "584193a5-99d8-4c01-8773-41e2570de689",
}
BASE_URL = "https://zarguell.github.io/tia-n-list"

checks = {}


def check(name, ok, detail):
    checks[name] = {"ok": bool(ok), "detail": str(detail)}


def sh(cmd, timeout=25, cwd=None):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd).stdout
    except Exception as e:
        return f"ERR {e}"


# 1. digest published today
dp = os.path.join(DATA, "digests", TODAY + ".md")
if os.path.exists(dp):
    size = os.path.getsize(dp)
    check("digest_published", size > 600, f"exists, {size}B")
else:
    check("digest_published", False, f"missing {TODAY}.md")

# 2. hourly engine fresh: newest event + last commit
newest = ""
for f in glob.glob(os.path.join(DATA, "events", "*.json")):
    try:
        d = (json.load(open(f)).get("published_at") or "")[:19]
        if d > newest:
            newest = d
    except Exception:
        pass
if newest:
    try:
        dt = datetime.fromisoformat(newest.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age_h = (NOW - dt).total_seconds() / 3600
        check("hourly_fresh", age_h <= 26, f"newest event {newest} ({age_h:.0f}h old)")
    except Exception as e:
        check("hourly_fresh", False, f"parse {newest}: {e}")
else:
    check("hourly_fresh", False, "no events on disk")

last = sh(["git", "log", "-1", "--format=%cI"], cwd=ROOT, timeout=10).strip()
if last and not last.startswith("ERR"):
    try:
        age_h = (NOW - datetime.fromisoformat(last)).total_seconds() / 3600
        check("last_commit", age_h <= 26, f"{last[:16]} ({age_h:.0f}h old)")
    except Exception:
        check("last_commit", False, f"unparsable {last}")
else:
    check("last_commit", False, "git log unavailable")


def qlen(path, key=None):
    try:
        d = json.load(open(path))
        return len(d.get(key, d)) if isinstance(d, dict) else len(d)
    except Exception:
        return -1


needs = qlen(os.path.join(DATA, "needs-analysis.json"), "events")
ctiq = qlen(os.path.join(DATA, "cti-queue.json"))
iocc = qlen(os.path.join(DATA, "iocs-candidates.json"), "candidates")
check("analysis_queue", needs >= 0, f"{needs} pending")
check("cti_queue", ctiq >= 0, f"{ctiq} uncovered cases")
check("ioc_candidates", iocc >= 0, f"{iocc} new candidates")

# 3. store invariants: event refs resolve, cti story_ids exist
story_ids = set()
for f in glob.glob(os.path.join(DATA, "stories", "*.json")):
    try:
        story_ids.add(json.load(open(f))["id"])
    except Exception:
        pass
bad_refs = 0
for f in glob.glob(os.path.join(DATA, "stories", "*.json")):
    try:
        s = json.load(open(f))
        for r in s.get("events", []):
            if not os.path.exists(os.path.join(DATA, "events", r["event_id"] + ".json")):
                bad_refs += 1
    except Exception:
        pass
bad_cti = 0
for f in glob.glob(os.path.join(DATA, "cti", "*.json")):
    try:
        if json.load(open(f)).get("story_id") not in story_ids:
            bad_cti += 1
    except Exception:
        bad_cti += 1
check("store_invariants", bad_refs == 0 and bad_cti == 0,
      f"{bad_refs} bad event refs, {bad_cti} cti story_id mismatches")

# 4. detection validity (sigma check CLI + yara-x compile)
sigma_bad = 0
if shutil.which("sigma"):
    for f in glob.glob(os.path.join(DATA, "cti", "*.sigma")):
        r = subprocess.run(["sigma", "check", f], capture_output=True, text=True, timeout=25)
        if r.returncode != 0:
            sigma_bad += 1
else:
    sigma_bad = -1
check("sigma_valid", sigma_bad == 0, "sigma-cli missing" if sigma_bad == -1 else f"{sigma_bad} failing rules")

yara_bad = 0
try:
    import yara_x
    for f in glob.glob(os.path.join(DATA, "cti", "*.yara")):
        try:
            yara_x.compile(open(f).read())
        except Exception:
            yara_bad += 1
except Exception:
    yara_bad = -1
check("yara_valid", yara_bad == 0, "yara-x missing" if yara_bad == -1 else f"{yara_bad} failing rules")

# 5. the other automations' run status (last 24h, via the service API)
key = os.environ.get("OPENHANDS_AUTOMATION_API_KEY", "")
run_status = {}
for name, aid in AUTOMATIONS.items():
    if not key:
        run_status[name] = "no-api-key"
        continue
    out = sh(["curl", "-s", "--max-time", "15", "-H", f"Authorization: Bearer {key}",
              f"http://localhost:8000/api/automation/v1/{aid}/runs"])
    try:
        runs = json.loads(out).get("runs", [])
        settled = [x for x in runs if x.get("status") in ("COMPLETED", "FAILED")]
        run_status[name] = f"{settled[0]['status']} {str(settled[0].get('created_at'))[:16]}" if settled else "no-settled-run"
    except Exception:
        run_status[name] = "unreadable"
core_failed = [n for n in ("hourly", "digest", "cti") if run_status.get(n, "").startswith("FAILED")]
check("automation_runs", not core_failed, "; ".join(f"{k}: {v}" for k, v in run_status.items()))

# 6. live site + snapshot pin (digest URL = latest EXISTING digest, so the
# check is timing-robust — the auditor runs after the digest, but this
# tolerates a missed day and still flags total staleness)
digest_dates = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob(os.path.join(DATA, "digests", "*.md"))]
latest_digest = max(digest_dates) if digest_dates else TODAY
pages = ["/", "/stories/", "/cti/", "/cti/iocs/", "/cti/snapshots/latest.json", f"/daily/{latest_digest}/"]
bad_pages = []
for p in pages:
    code = sh(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "20", BASE_URL + p]).strip()
    if code != "200":
        bad_pages.append(f"{p}={code}")
check("live_site", not bad_pages, ", ".join(bad_pages) or f"{len(pages)}/{len(pages)} pages 200")

pin_ok = False
pin_detail = "err"
try:
    d = json.loads(sh(["curl", "-s", "--max-time", "20", BASE_URL + "/cti/snapshots/latest.json"]))["date"]
    man = json.loads(sh(["curl", "-s", "--max-time", "20", f"{BASE_URL}/cti/snapshots/{d}/manifest.json"]))
    bundle = sh(["curl", "-s", "--max-time", "20", f"{BASE_URL}/cti/snapshots/{d}/stix-bundle.json"])
    h = hashlib.sha256(bundle.encode()).hexdigest()
    pin_ok = h == man["files"]["stix-bundle.json"]["sha256"]
    pin_detail = f"{d} sha256 {'match' if pin_ok else 'MISMATCH'}"
except Exception as e:
    pin_detail = f"err {e}"
check("snapshot_pin", pin_ok, pin_detail)

# 7. coverage state
n_records = len(glob.glob(os.path.join(DATA, "cti", "*.json")))
n_sigma = len(glob.glob(os.path.join(DATA, "cti", "*.sigma")))
n_yara = len(glob.glob(os.path.join(DATA, "cti", "*.yara")))
covered = set()
for f in glob.glob(os.path.join(DATA, "cti", "*.json")):
    try:
        for t in json.load(open(f)).get("attack", []):
            covered.add(t["id"])
    except Exception:
        pass
check("coverage", True,
      f"{n_records} records, {len(covered)} techniques, {n_sigma} sigma, {n_yara} yara")

# 8. story fragmentation: one story split into several (the Patch Tuesday
# class). Signal: the same "patch tuesday"-family month group having more than
# one LIVE story. (CVE-overlap is NOT used — bulletin roundups list many CVEs,
# so shared CVEs produce false positives; this detector is deliberately
# precise, and the LLM quality sample catches anything subtler.)
import re as _re
month_group = {}
for f in glob.glob(os.path.join(DATA, "stories", "*.json")):
    try:
        s = json.load(open(f))
    except Exception:
        continue
    if s.get("merged_into"):
        continue
    t = (s.get("title") or "").lower()
    # roundup class: the monthly vendor batch. Literal "patch tuesday", OR a
    # numbered Windows-flaws roundup ("Microsoft Patches 398 Windows Flaws..."
    # is the same story and lacks "patch tuesday" — this is why the August
    # fragment was missed). The NUMBER requirement keeps meta-stories out
    # ("Expects More Security Updates From AI-Discovered Flaws" is not a
    # roundup even though it mentions windows flaws).
    is_roundup = ("patch tuesday" in t) or (
        "windows" in t
        and _re.search(r"\d+\s*(cves?|vulnerabilit\w+|flaws?)", t)
    )
    if not is_roundup:
        continue
    if any(x in t for x in ("ics", "siemens", "schneider", "phoenix contact")):
        fam = "ics"
    elif "microsoft" in t:
        fam = "microsoft"
    else:
        fam = "other"      # e.g. "Chipmaker Patch Tuesday: Intel, AMD..." — NOT Microsoft
    # month from the first event's publish date (title may omit it)
    refs = s.get("events", [])
    month = "?"
    if refs:
        try:
            ev = json.load(open(os.path.join(DATA, "events", refs[0]["event_id"] + ".json")))
            month = (ev.get("published_at") or "")[:7]
        except Exception:
            pass
    key = f"{fam}/{month}"
    month_group.setdefault(key, []).append(s["id"])
fragments = []
for key, sids in sorted(month_group.items()):
    if len(sids) > 1:
        fragments.append(f"{key} patch-tuesday: {len(sids)} live stories ({', '.join(s[:36] for s in sids)})")
check("fragmentation", not fragments, "; ".join(fragments[:8]) or "no duplicate-story fragments")

# ── 9-15. judgment-layer audit (2026-08-24): the triage-drift incident was
# invisible to output checks (site up, queues draining) because the judgment
# layer had no invariants. These sections audit the JUDGMENT: store dedup
# invariants, triage drift telemetry, adversarial sampling targets, digest
# override log, near-duplicate suspects, and creation trends. Pure functions
# so test_audit.py can pin them.
from merge import title_jaccard, distinct_series_codes  # noqa: E402


def load_all_stories():
    out = {}
    for f in glob.glob(os.path.join(DATA, "stories", "*.json")):
        try:
            s = json.load(open(f))
            out[s["id"]] = s
        except Exception:
            pass
    return out


def dedup_invariants(stories):
    """The mechanically-detectable failure classes from the 2026-08-24 triage
    drift: events referenced by >1 active story, merged_into cycles, events
    stranded inside redirect shells, and true same-slug-base duplicates
    (shared event or similar titles; distinct advisory codes exonerate)."""
    owners = {}
    for sid, s in stories.items():
        for r in s.get("events", []):
            owners.setdefault(r["event_id"], set()).add(sid)
    multi = sorted(f"{e}: {','.join(sorted(sids))}"
                   for e, sids in owners.items() if len(sids) > 1)

    cycles = []
    for sid in stories:
        seen, cur = set(), sid
        while stories.get(cur, {}).get("merged_into"):
            if cur in seen:
                cycles.append(sid)
                break
            seen.add(cur)
            cur = stories[cur]["merged_into"]

    in_shell = sum(len(s.get("events", [])) for s in stories.values() if s.get("merged_into"))

    by_base = {}
    for sid, s in stories.items():
        if not s.get("merged_into") and s.get("events"):
            by_base.setdefault(_re.sub(r"-\d+$", "", sid), []).append(sid)
    dups = []
    for base, group in by_base.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                ta, tb = stories[a].get("title", ""), stories[b].get("title", "")
                shares = bool({r["event_id"] for r in stories[a]["events"]} &
                              {r["event_id"] for r in stories[b]["events"]})
                if shares or (title_jaccard(ta, tb) >= 0.4
                              and not distinct_series_codes(ta, tb)):
                    dups.append(f"{a} + {b}")

    ghosts = sum(1 for s in stories.values() if not s.get("merged_into") and not s.get("events"))
    problems = ([("multi-ref", x) for x in multi] +
                [("cycle", x) for x in cycles] +
                [("in-shell", str(in_shell))] * (1 if in_shell else 0) +
                [("same-base", x) for x in dups])
    detail = "; ".join(f"{k}: {v}" for k, v in problems[:8]) or \
        f"clean ({ghosts} eventless ghosts, informational)"
    return not problems, detail, ghosts


def duplicate_suspects(stories, max_out=10, max_age_days=45):
    """Near-duplicate ACTIVE story pairs the mechanical merge likely missed
    (different outlets, no shared tokens): title jaccard >= 0.5 with >= 2
    shared discriminators, distinct advisory codes exonerated. Output is for
    the LLM to adjudicate (merge via a triage decisions file), never an
    automatic merge."""
    cutoff = (NOW - timedelta(days=max_age_days)).strftime("%Y-%m-%dT%H:%M:%S")
    pool = [s for s in stories.values()
            if not s.get("merged_into") and s.get("events")
            and s.get("last_seen", "") >= cutoff]
    out = []
    for i in range(len(pool)):
        for j in range(i + 1, len(pool)):
            a, b = pool[i], pool[j]
            j_ = title_jaccard(a.get("title", ""), b.get("title", ""))
            if j_ < 0.5 or distinct_series_codes(a.get("title", ""), b.get("title", "")):
                continue
            out.append({"a": a["id"], "b": b["id"], "jaccard": round(j_, 2),
                        "title_a": a.get("title", "")[:70], "title_b": b.get("title", "")[:70]})
    out.sort(key=lambda x: -x["jaccard"])
    return out[:max_out]


CJK_RE = _re.compile(r"[\u0400-\u04FF\u4E00-\u9FFF\u3040-\u30FF\uAC00-\uD7AF\u0600-\u06FF]")


def language_scan():
    """Non-Latin script bleed (CJK/Cyrillic/Arabic) in published English
    prose — the 2026-08-23 'Chinese in an analysis' catch, made deterministic
    instead of luck-of-the-sample."""
    hits = []
    for pat in ("analysis/*.md", "digests/*.md"):
        for f in glob.glob(os.path.join(DATA, pat))[:800]:
            try:
                text = open(f, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            m = CJK_RE.search(text)
            if m:
                ctx = text[max(0, m.start() - 20):m.end() + 20].replace("\n", " ")
                hits.append(f"{os.path.relpath(f, DATA)}: …{ctx}…")
    return hits


def digest_overrides():
    """Aggregate the digest agents' editorial deviations (promote/demote/
    wildcard) across all digests — the feedback loop for tuning score.py."""
    out = []
    for f in glob.glob(os.path.join(DATA, "digests", "*.json")):
        d = os.path.splitext(os.path.basename(f))[0]
        try:
            for o in json.load(open(f)).get("overrides", []):
                out.append({"digest": d, **o})
        except Exception:
            pass
    out.sort(key=lambda o: o["digest"], reverse=True)
    return out


def triage_telemetry(cronman_log_dir, triage_dir):
    """Drift detection for the hourly LLM gate: schema WARNs in the wrapper
    log, keep/drop balance from the last 24h of decision files, and silent
    drift (judgment runs but no decisions file written)."""
    problems, info = [], []
    log_text = ""
    for d in (TODAY, (NOW - timedelta(days=1)).strftime("%Y-%m-%d")):
        p = os.path.join(cronman_log_dir, d + ".log")
        if os.path.exists(p):
            try:
                log_text += open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                pass
    for pat, label in ((r"WARN: \d+ decision entries could not be parsed", "unparsed decision entries"),
                       (r"no keep/drop decisions recognized", "no decisions recognized")):
        n = len(_re.findall(pat, log_text))
        if n:
            problems.append(f"{label} x{n}")
    judgment_runs = len(_re.findall(r"TIA pi judgment", log_text))
    cap_hits = len(_re.findall(r"triage: 30 new events", log_text))
    cutoff = (NOW - timedelta(hours=24)).timestamp()
    keeps = drops = 0
    for f in glob.glob(os.path.join(triage_dir, "decisions-*.json")):
        if os.path.getmtime(f) < cutoff:
            continue
        try:
            dec = json.load(open(f)).get("decisions", [])
        except Exception:
            continue
        keeps += sum(1 for x in dec if x.get("action") == "keep")
        drops += sum(1 for x in dec if x.get("action") == "drop")
    if judgment_runs and not (keeps or drops):
        problems.append(f"{judgment_runs} judgment runs in 24h but 0 decisions (silent drift)")
    if keeps + drops >= 10:
        ratio = keeps / (keeps + drops)
        info.append(f"keep/drop {keeps}/{drops} ({ratio:.0%} keep)")
        if ratio > 0.95:
            problems.append(f"suspiciously permissive triage: {ratio:.0%} keep")
    else:
        info.append(f"keep/drop {keeps}/{drops} in 24h")
    if cap_hits:
        info.append(f"30-event batch cap hit x{cap_hits} (window falling behind)")
    return problems, "; ".join(info) or "no signal"


def queue_age():
    """Analysis-queue staleness: a story pending > 48h is stuck, not queued."""
    try:
        q = json.load(open(os.path.join(DATA, "needs-analysis.json")))
    except Exception:
        return None, "needs-analysis.json unreadable"
    slugs = q.get("stories", [])
    if not slugs:
        return 0, "empty"
    stories = load_all_stories()
    worst_h, worst = 0.0, ""
    events_by_id = {}
    for f in glob.glob(os.path.join(DATA, "events", "*.json")):
        eid = os.path.splitext(os.path.basename(f))[0]
        try:
            events_by_id[eid] = (json.load(open(f)).get("published_at") or "")[:19]
        except Exception:
            pass
    for slug in slugs:
        s = stories.get(slug)
        if not s:
            continue
        newest = max((events_by_id.get(r["event_id"], "") for r in s.get("events", [])),
                     default="")
        if not newest:
            continue
        try:
            dt = datetime.fromisoformat(newest.replace("Z", "+00:00"))
            h = (NOW - dt).total_seconds() / 3600
            if h > worst_h:
                worst_h, worst = h, slug
        except Exception:
            pass
    return worst_h, (f"{len(slugs)} queued, oldest pending {worst_h:.0f}h ({worst[:48]})"
                     if worst else f"{len(slugs)} queued")


def sampling_targets():
    """Adversarial sampling for the LLM pass: not just the newest files (which
    luck found the Chinese-text issue) — the OLDEST hot analysis (staleness)
    and the stories the latest digest actually linked (what readers saw)."""
    out = {}
    analyses = []
    for f in glob.glob(os.path.join(DATA, "analysis", "*.md")):
        analyses.append((os.path.getmtime(f), f))
    analyses.sort()
    if analyses:
        out["newest_analyses"] = [os.path.basename(f) for _, f in analyses[-3:]]
        out["oldest_analyses"] = [os.path.basename(f) for _, f in analyses[:3]]
    digests = sorted(os.path.splitext(os.path.basename(f))[0]
                     for f in glob.glob(os.path.join(DATA, "digests", "*.json")))
    if digests:
        try:
            d = json.load(open(os.path.join(DATA, "digests", digests[-1] + ".json")))
            out["latest_digest"] = digests[-1]
            out["digest_linked_stories"] = d.get("stories", [])[:20]
        except Exception:
            pass
    return out


def store_trends(stories, days=7):
    """Creation vs consolidation trend: events/day and new active stories/day.
    Rising stories/day on flat events/day = fragmentation trending up."""
    from collections import Counter as _Counter
    ev_per_day = _Counter()
    for f in glob.glob(os.path.join(DATA, "events", "*.json")):
        try:
            ev_per_day[(json.load(open(f)).get("published_at") or "")[:10]] += 1
        except Exception:
            pass
    st_per_day = _Counter()
    for s in stories.values():
        if not s.get("merged_into"):
            st_per_day[(s.get("first_seen") or "")[:10]] += 1
    horizon = [(NOW - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days - 1, -1, -1)]
    return {
        "per_day": [{"date": d,
                     "events": ev_per_day.get(d, 0),
                     "new_active_stories": st_per_day.get(d, 0)} for d in horizon],
        "totals": {"active_stories": sum(1 for s in stories.values() if not s.get("merged_into")),
                   "merged_shells": sum(1 for s in stories.values() if s.get("merged_into"))},
    }


from datetime import timedelta  # noqa: E402  (sections above use NOW/timedelta)

_all_stories = load_all_stories()
_ok, _detail, _ghosts = dedup_invariants(_all_stories)
check("dedup_invariants", _ok, _detail)
_tel_problems, _tel_info = triage_telemetry("/home/ubuntu/repos/cronman/logs/cronman",
                                           os.path.join(DATA, "triage"))
check("triage_drift", not _tel_problems, "; ".join(_tel_problems) or _tel_info)
_worst_h, _qa_detail = queue_age()
check("analysis_queue_age", _worst_h is None or _worst_h <= 48, _qa_detail)
_lang_hits = language_scan()
check("language_scan", not _lang_hits, "; ".join(_lang_hits[:4]) or "no non-Latin script bleed")

EXTRA = {
    "duplicate_suspects": duplicate_suspects(_all_stories),
    "digest_overrides": digest_overrides(),
    "samples": sampling_targets(),
    "trends": store_trends(_all_stories),
    "ghost_stories": _ghosts,
}

print(json.dumps({"date": TODAY, "checks": checks, **EXTRA}, indent=1))
