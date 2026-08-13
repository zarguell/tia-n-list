#!/usr/bin/env python3
"""Tia N. List — NVD publish-date cache for CVEs in the story store.

The "first disclose" anchor of the per-CVE timeline is the NVD ``published``
timestamp (the CNA/CVE disclosure date). On-KEV CVEs already carry
``cve_published`` in the kevrichment index; this script fills the gap for every
CVE in the story store (candidates included) into a small committed cache:

    engine/data/nvd-published.json   {"CVE-YYYY-NNNN": "YYYY-MM-DD", ...}

Deterministic, idempotent, resumable: cached CVEs are skipped, failed fetches
are retried on the next run. NVD_API_KEY is honored (50 req/30s with key,
5 req/30s without — the delay is set accordingly).
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
CACHE = os.path.join(ENGINE, "data", "nvd-published.json")
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


def fetch_published(cve_id, api_key):
    url = f"{NVD_API}?cveId={cve_id}"
    req = urllib.request.Request(url)
    if api_key:
        req.add_header("apiKey", api_key)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    for v in data.get("vulnerabilities", []):
        cve = v.get("cve", {})
        if cve.get("id") == cve_id and cve.get("published"):
            return cve["published"][:10]
    return None


def main():
    api_key = os.environ.get("NVD_API_KEY")
    delay = 0.8 if api_key else 7.0
    cves = story_cves()
    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE))
    todo = [c for c in cves if c not in cache]
    print(f"nvd-published: {len(cves)} store CVEs, {len(cache)} cached, "
          f"{len(todo)} to fetch (delay {delay}s)", flush=True)
    ok = fail = 0
    for i, c in enumerate(todo):
        try:
            d = fetch_published(c, api_key)
        except Exception as e:  # noqa: BLE001 — network/parse failure: retry next run
            print(f"  [WARN] {c}: {e}", flush=True)
            fail += 1
            time.sleep(delay)
            continue
        if d:
            cache[c] = d
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
    print(f"nvd-published: done — {ok} added, {fail} failed, "
          f"{len(cache)}/{len(cves)} total")


if __name__ == "__main__":
    sys.exit(main())
