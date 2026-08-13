#!/usr/bin/env python3
"""Tia N. List — NVD info cache for CVEs in the story store.

Per-CVE NVD data used by the KEV-tracking pages:
    engine/data/nvd-info.json   {"CVE-YYYY-NNNN": {"published": "YYYY-MM-DD",
                                                   "description": "<en text>"}, ...}

- ``published`` is the "first disclose" anchor of the per-CVE timeline.
- ``description`` is the NVD English description — the vulnerability-name
  source for candidate rows (never article headlines).

Deterministic, idempotent, resumable: cached entries with both fields are
skipped, failed fetches are retried on the next run. NVD_API_KEY is honored
(50 req/30s with key, 5 req/30s without — the delay is set accordingly).
"""
import glob
import json
import os
import re
import sys
import time
import urllib.request

ENGINE = os.path.dirname(os.path.abspath(__file__))
STORIES = os.path.join(ENGINE, "data", "stories")
CACHE = os.path.join(ENGINE, "data", "nvd-info.json")
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,7}$")


def story_cves():
    cves = set()
    for p in glob.glob(os.path.join(STORIES, "*.json")):
        s = json.load(open(p))
        if s.get("merged_into"):
            continue
        for c in s.get("cves") or []:
            if CVE_RE.match(c):
                cves.add(c)
    return sorted(cves)


def fetch_info(cve_id, api_key):
    """Rich NVD block for one CVE, or None. Fields:
    published, last_modified, description, cvss {score,severity,vector},
    ssvc {exploitation,automatable,technical_impact}, cwes, references."""
    url = f"{NVD_API}?cveId={cve_id}"
    req = urllib.request.Request(url)
    if api_key:
        req.add_header("apiKey", api_key)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    for v in data.get("vulnerabilities", []):
        cve = v.get("cve", {})
        if cve.get("id") != cve_id:
            continue
        published = (cve.get("published") or "")[:10] or None
        last_modified = (cve.get("lastModified") or "")[:10] or None
        description = None
        for d in cve.get("descriptions", []):
            if d.get("lang") == "en":
                description = re.sub(r"\s+", " ", d.get("value", "")).strip()
                break
        cvss = {}
        for m in (cve.get("metrics") or {}).get("cvssMetricV31", []):
            d = m.get("cvssData") or {}
            cvss = {"score": d.get("baseScore"),
                    "severity": d.get("baseSeverity", ""),
                    "vector": d.get("vectorString", "")}
            break
        ssvc = {}
        for m in (cve.get("metrics") or {}).get("ssvcV203", []):
            opts = {o: v2 for o in ((m.get("ssvcData") or {}).get("options") or [])
                    for o, v2 in o.items()}
            ssvc = {"exploitation": opts.get("exploitation", ""),
                    "automatable": opts.get("automatable", ""),
                    "technical_impact": opts.get("technicalImpact", "")}
            break
        cwes = sorted({(w.get("description") or [{}])[0].get("value", "")
                       for w in cve.get("weaknesses", [])} - {""})
        references = [r.get("url", "") for r in cve.get("references", [])
                      if r.get("url", "").startswith("http")]
        return {"published": published, "last_modified": last_modified,
                "description": description or "",
                "cvss": cvss, "ssvc": ssvc, "cwes": cwes,
                "references": references}
    return None


def main():
    api_key = os.environ.get("NVD_API_KEY")
    delay = 0.8 if api_key else 7.0
    cves = story_cves()
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE))
    todo = [c for c in cves if c not in cache or not cache[c].get("ssvc")]
    print(f"nvd-info: {len(cves)} store CVEs, {len(cache)} cached, "
          f"{len(todo)} to fetch (delay {delay}s)", flush=True)
    ok = fail = 0
    for i, c in enumerate(todo):
        try:
            info = fetch_info(c, api_key)
        except Exception as e:  # noqa: BLE001 — network failure: retry next run
            print(f"  [WARN] {c}: {e}", flush=True)
            fail += 1
            time.sleep(delay)
            continue
        if info and info.get("published"):
            cache[c] = info
            ok += 1
            if ok % 25 == 0:
                json.dump(cache, open(CACHE + ".tmp", "w"), indent=1)
        else:
            fail += 1
        if i < len(todo) - 1:
            time.sleep(delay)
    json.dump(cache, open(CACHE, "w"), indent=1, sort_keys=True)
    if os.path.exists(CACHE + ".tmp"):
        os.remove(CACHE + ".tmp")
    with_desc = sum(1 for v in cache.values() if v.get("description"))
    with_ssvc = sum(1 for v in cache.values() if v.get("ssvc"))
    print(f"nvd-info: done — {ok} added, {fail} failed, "
          f"{len(cache)}/{len(cves)} total, {with_desc} with descriptions, "
          f"{with_ssvc} with SSVC")


if __name__ == "__main__":
    sys.exit(main())
