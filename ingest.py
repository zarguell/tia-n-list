"""
Ingest CISA KEV catalog, CISA Vulnrichment (SSVC), and NVD API data.
"""

import json
import os
import re
import time
from datetime import datetime

import requests

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
VULNRICHMENT_RAW = "https://raw.githubusercontent.com/cisagov/vulnrichment/develop"
VULNRICHMENT_API = "https://api.github.com/repos/cisagov/vulnrichment/contents"
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

USER_AGENT = "kevrichment/1.0 (+https://github.com/zarguell/kevrichment)"


def _headers():
    return {"User-Agent": USER_AGENT}


# ---------------------------------------------------------------------------
# CISA KEV
# ---------------------------------------------------------------------------

def get_kev_source_date(kev_data):
    """Extract the catalog source date from KEV metadata."""
    return kev_data.get("catalogVersion", "").split("T")[0] if kev_data.get("catalogVersion") else ""


def fetch_kev():
    """Fetch the full CISA KEV catalog. Returns the parsed JSON dict."""
    resp = requests.get(KEV_URL, headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_latest_kev_entries(kev_data, count=5):
    """Return the N most recently added KEV entries (sorted by dateAdded descending)."""
    entries = kev_data.get("vulnerabilities", [])
    entries_sorted = sorted(entries, key=lambda e: e.get("dateAdded", ""), reverse=True)
    return entries_sorted[:count]


# ---------------------------------------------------------------------------
# CISA Vulnrichment (SSVC)
# ---------------------------------------------------------------------------

def _vulnrichment_path(cve_id):
    """Compute the vulnrichment file path on GitHub for a CVE ID.

    Directory structure: ``{year}/{thousands_group}xxx/CVE-YYYY-XXXX.json``

    Examples:
        CVE-2024-1709  ->  2024/1xxx/CVE-2024-1709.json
        CVE-2025-12345 ->  2025/12xxx/CVE-2025-12345.json
    """
    parts = cve_id.split("-")
    if len(parts) != 3:
        return None
    year = parts[1]
    seq = parts[2].lstrip("0")
    if not seq:
        seq = "0"
    seq_num = int(seq)
    prefix = str(seq_num // 1000)
    return f"{year}/{prefix}xxx/{cve_id}.json"


def fetch_vulnrichment(cve_id):
    """Fetch Vulnrichment SSVC data for a specific CVE.

    Returns dict with keys ``automatable``, ``technical_impact``, ``exploitation``
    (each ``"yes" | "no" | "unknown"``) or an empty dict if unavailable.
    """
    path = _vulnrichment_path(cve_id)
    if not path:
        return {}

    raw_url = f"{VULNRICHMENT_RAW}/{path}"
    try:
        resp = requests.get(raw_url, headers=_headers(), timeout=15)
        if resp.status_code == 404:
            return {}
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"    [WARN] Vulnrichment fetch failed for {cve_id}: {e}")
        return {}

    # The SSVC data lives in the CISA-ADP container under "metrics" as
    # {"other": {"type": "ssvc", "content": {"options": [{"Automatable": "yes"}, ...]}}}
    adp_list = data.get("containers", {}).get("adp", [])

    ssvc_options = {}
    for adp in adp_list:
        title = adp.get("title", "")
        if "CISA" not in title and "ADP" not in title and "Vulnrichment" not in title:
            continue
        for metric in adp.get("metrics", []):
            other = metric.get("other", {})
            if other.get("type") != "ssvc":
                continue
            for opt in other.get("content", {}).get("options", []):
                for k, v in opt.items():
                    if k.lower() in ("automatable", "technical impact", "technical_impact", "exploitation"):
                        ssvc_options[k.lower().replace(" ", "_")] = str(v).lower()

    if not ssvc_options:
        return {}

    return {
        "automatable": ssvc_options.get("automatable", "unknown"),
        "technical_impact": ssvc_options.get("technical_impact", "unknown"),
        "exploitation": ssvc_options.get("exploitation", "unknown"),
    }


# ---------------------------------------------------------------------------
# NVD API
# ---------------------------------------------------------------------------

def fetch_nvd(cve_id, api_key=None):
    """Fetch NVD CVE record.

    Parameters
    ----------
    api_key : str or None
        NVD API 2.0 key.  Without one the rate limit is 5 req/30s;
        with a key it is 50 req/30s.  Falls back to the ``NVD_API_KEY``
        environment variable if not provided.
    """
    if api_key is None:
        api_key = os.environ.get("NVD_API_KEY")
    url = f"{NVD_API}?cveId={cve_id}"
    headers = _headers()
    if api_key:
        headers["apiKey"] = api_key
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"    [WARN] NVD fetch failed for {cve_id}: {e}")
        return {}


def fetch_nvd_batch(cve_ids, delay=0.6, api_key=None):
    """Fetch NVD data for multiple CVEs with rate-limit spacing."""
    results = {}
    for i, cve_id in enumerate(cve_ids):
        if i > 0:
            time.sleep(delay)
        print(f"    NVD: {cve_id}")
        results[cve_id] = fetch_nvd(cve_id, api_key=api_key)
    return results


# ---------------------------------------------------------------------------
# GitHub PoC search
# ---------------------------------------------------------------------------

def search_github_poc(cve_id, max_results=5):
    """Search GitHub for public repos mentioning the CVE ID."""
    url = (
        f"https://api.github.com/search/repositories"
        f"?q={cve_id}+exploit&sort=stars&order=desc&per_page={max_results}"
    )
    try:
        resp = requests.get(url, headers=_headers(), timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return [
            {
                "url": item.get("html_url", ""),
                "name": item.get("full_name", ""),
                "stars": item.get("stargazers_count", 0),
                "description": (item.get("description") or "")[:200],
            }
            for item in data.get("items", [])
        ]
    except requests.RequestException as e:
        print(f"    [WARN] GitHub search failed for {cve_id}: {e}")
        return []


# ---------------------------------------------------------------------------
# Vulnrichment scan — non-KEV high-priority CVEs
# ---------------------------------------------------------------------------

def _extract_ssvc_from_dict(data):
    """Extract SSVC values from a vulnrichment JSON dict."""
    ssvc_options = {}
    for adp in data.get("containers", {}).get("adp", []):
        title = adp.get("title", "")
        if "CISA" not in title and "ADP" not in title and "Vulnrichment" not in title:
            continue
        for metric in adp.get("metrics", []):
            other = metric.get("other", {})
            if other.get("type") != "ssvc":
                continue
            for opt in other.get("content", {}).get("options", []):
                for k, v in opt.items():
                    key = k.lower().replace(" ", "_")
                    if key in ("automatable", "technical_impact", "technical impact", "exploitation"):
                        ssvc_options[key] = str(v).lower()
    return ssvc_options


def scan_vulnrichment_high_priority(kev_cve_ids, max_results=5, max_per_dir=25):
    """Scan vulnrichment for non-KEV CVEs with ``automatable=yes`` + ``technical_impact=total``.

    These are CVEs that would require **3-day remediation** under BOD 26-04
    if the vulnerable asset is publicly exposed — even though CISA hasn't
    added them to the KEV catalog (yet).
    """
    # Auto-detect latest year
    try:
        resp = requests.get(VULNRICHMENT_API, headers=_headers(), timeout=10)
        resp.raise_for_status()
        dirs = [d["name"] for d in resp.json()
                if d["type"] == "dir" and d["name"].isdigit()]
        years = sorted(dirs, reverse=True)[:2]
    except requests.RequestException:
        years = ["2026", "2025"]

    found = []

    for year in years:
        if len(found) >= max_results:
            break
        try:
            resp = requests.get(f"{VULNRICHMENT_API}/{year}", headers=_headers(), timeout=10)
            resp.raise_for_status()
            groups = sorted(
                [d["name"] for d in resp.json() if d["type"] == "dir"],
                reverse=True,
            )[:5]
        except requests.RequestException:
            continue

        for group in groups:
            if len(found) >= max_results:
                break
            try:
                resp = requests.get(f"{VULNRICHMENT_API}/{year}/{group}", headers=_headers(), timeout=10)
                resp.raise_for_status()
                files = sorted(
                    [f["name"] for f in resp.json()
                     if f["type"] == "file" and f["name"].startswith("CVE-")],
                    reverse=True,
                )
            except requests.RequestException:
                continue

            checked = 0
            for fname in files:
                if len(found) >= max_results or checked >= max_per_dir:
                    break
                cve_id = fname.replace(".json", "")
                if cve_id in kev_cve_ids:
                    continue

                raw_url = f"{VULNRICHMENT_RAW}/{year}/{group}/{fname}"
                try:
                    resp2 = requests.get(raw_url, headers=_headers(), timeout=10)
                    resp2.raise_for_status()
                except requests.RequestException:
                    continue

                ssvc = _extract_ssvc_from_dict(resp2.json())
                checked += 1

                if ssvc.get("automatable") == "yes" and ssvc.get("technical_impact") == "total":
                    found.append({"cve_id": cve_id, "ssvc": ssvc})
                    print(f"    [HIGH] {cve_id} — auto=yes impact=total (non-KEV)")

    return found
