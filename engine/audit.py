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
from datetime import datetime, timedelta, timezone

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
# live in audit_checks.py (pinned by test_audit.py).
import audit_checks as jc  # noqa: E402

_all_stories = jc.load_all_stories(DATA)
_ok, _detail, _ghosts = jc.dedup_invariants(_all_stories)
check("dedup_invariants", _ok, _detail)
_tel_problems, _tel_info = jc.triage_telemetry("/home/ubuntu/repos/cronman/logs/cronman",
                                               os.path.join(DATA, "triage"), NOW)
check("triage_drift", not _tel_problems, "; ".join(_tel_problems) or _tel_info)
_worst_h, _qa_detail = jc.queue_age(DATA, _all_stories, NOW)
check("analysis_queue_age", _worst_h is None or _worst_h <= 48, _qa_detail)
_lang_hits = jc.language_scan(DATA)
check("language_scan", not _lang_hits, "; ".join(_lang_hits[:4]) or "no non-Latin script bleed")

EXTRA = {
    "duplicate_suspects": jc.duplicate_suspects(_all_stories, NOW),
    "digest_overrides": jc.digest_overrides(DATA),
    "samples": jc.sampling_targets(DATA),
    "trends": jc.store_trends(DATA, _all_stories, NOW),
    "ghost_stories": _ghosts,
}

print(json.dumps({"date": TODAY, "checks": checks, **EXTRA}, indent=1))
