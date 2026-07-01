#!/usr/bin/env python3
"""
Batch agentic research for kevrichment.
Reads 10 CVEs without Hermes analysis, runs web research, updates files.
"""
import json
import re
import time
import sys
from hermes_tools import web_search, write_file, terminal

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
from research import ResearchEngine

CVES_DIR = BASE / "data" / "cves"

def find_cves_needing_analysis(count=10):
    """Find CVE IDs without Hermes research."""
    result = terminal(f"""cd {BASE} && python3 -c "
import json, glob
files = sorted(glob.glob('data/cves/*.json'))
needing = []
for f in files:
    d = json.load(open(f))
    r = d.get('kevrichment_research', {{}})
    if r.get('preconditions_source') != 'hermes':
        needing.append(d['cve_id'])
        if len(needing) >= {count}:
            break
print('\\\\n'.join(needing))
" """)
    ids = [line.strip() for line in result.get("output", "").strip().split("\n") if line.strip()]
    return ids

def read_cve(cve_id):
    """Read existing CVE JSON file via Python (avoids stdout truncation)."""
    path = f"{CVES_DIR}/{cve_id}.json"
    result = terminal(f"python3 -c \"import json; print(json.dumps(json.load(open('{path}'))))\"")
    return json.loads(result["output"])

def write_cve(cve_id, record):
    """Write updated CVE JSON file."""
    path = f"{CVES_DIR}/{cve_id}.json"
    write_file(path, json.dumps(record, indent=2))
    return path

def search_vendor_advisory(cve_id, vendor, product):
    """Web search for vendor advisory URL."""
    query = f"{vendor} {cve_id} security advisory patch"
    try:
        r = web_search(query, limit=3)
        if r and "data" in r:
            for item in r["data"].get("web", []):
                url = item.get("url", "")
                if url:
                    low = url.lower()
                    if any(kw in low for kw in ("advisory", "security", "patch", "cve", vendor.lower()[:5])):
                        return url, [url]
    except Exception as e:
        print(f"  [WARN] Advisory search failed: {e}")
    return "", []

def search_component_info(cve_id, vendor, product, component):
    """Web search for vulnerable component details."""
    query = f"{vendor} {product} {component} security vulnerability"
    urls = []
    try:
        r = web_search(query, limit=3)
        if r and "data" in r:
            for item in r["data"].get("web", []):
                u = item.get("url", "")
                if u:
                    urls.append(u)
    except Exception as e:
        print(f"  [WARN] Component search failed: {e}")
    return urls

def search_default_enablement(cve_id, vendor, product, component):
    """Web search for default enablement info."""
    if len(component) < 3:
        return []
    query = f"\"{component}\" \"enabled by default\" {product}"
    urls = []
    try:
        r = web_search(query, limit=3)
        if r and "data" in r:
            for item in r["data"].get("web", []):
                u = item.get("url", "")
                if u:
                    urls.append(u)
    except Exception as e:
        print(f"  [WARN] Default enablement search failed: {e}")
    return urls

def extract_poc_from_search(cve_id):
    """Search for public PoC/exploit code."""
    query = f"{cve_id} exploit PoC github"
    poc_urls = []
    try:
        r = web_search(query, limit=5)
        if r and "data" in r:
            for item in r["data"].get("web", []):
                url = item.get("url", "")
                if url and ("github.com" in url or "exploit-db.com" in url or "poc" in url.lower()):
                    poc_urls.append(url)
    except Exception as e:
        print(f"  [WARN] PoC search failed: {e}")
    return poc_urls

def extract_component_from_advisory(cve_id, vendor, product, description):
    """Try harder to extract the vulnerable component using web search."""
    if not description:
        return product
    
    # First try the existing deterministic extraction from NVD description
    patterns = [
        r'in the ([A-Z][a-zA-Z0-9_ -]{1,45}?)(?: component| module| feature| function)\b',
        r'in ([A-Z][a-zA-Z0-9_ -]{1,45}?)(?: component| module| feature| function)',
        r'(?:a |the )?vulnerability in (?:the )?([A-Z][a-zA-Z0-9_ /-]{1,45}?)(?:\s+(?:allows|could|that|may|can|is|are|was|permit|\w+ly\b)|\s*$)',
        r'the affected ([A-Z][a-zA-Z0-9_ -]{1,40})(?: is| are| component)',
    ]
    for pat in patterns:
        m = re.search(pat, description, re.IGNORECASE)
        if m:
            found = m.group(1).strip().rstrip(".")
            if 3 < len(found) < 200:
                return found
    return product

def process_cve(cve_id):
    """Research a single CVE with Hermes agent tools."""
    print(f"\n  ── {cve_id} ──")
    record = read_cve(cve_id)
    research = record.get("kevrichment_research", {})
    meta = record.get("research_meta", {})
    
    vendor = record.get("kev_vendor_project", "")
    product = record.get("kev_product", "")
    description = record.get("nvd_description", "")
    
    all_sources = list(meta.get("sources_consulted", []))
    
    # 1. Try harder to extract component
    engine = ResearchEngine()
    component = engine._extract_component(description, product, vendor)
    if component and component != product:
        print(f"    Component: {component}")
    else:
        print(f"    Component: {product} (generic)")
    
    # 2. Search for vendor advisory URL
    current_url = research.get("vendor_advisory_url", "")
    if not current_url or "nvd.nist.gov" in current_url:
        advisory_url, adv_sources = search_vendor_advisory(cve_id, vendor, product)
        if advisory_url:
            research["vendor_advisory_url"] = advisory_url
            all_sources.extend(adv_sources)
            print(f"    Advisory: {advisory_url}")
        else:
            print(f"    Advisory: (no new)")
    else:
        print(f"    Advisory: {current_url[:60]}…")
    
    # 3. Search for PoC
    current_poc = research.get("public_poc_exists", "unknown")
    if current_poc != "yes":
        poc_urls = extract_poc_from_search(cve_id)
        if poc_urls:
            existing_pocs = set(research.get("public_poc_urls", []))
            for u in poc_urls:
                if u not in existing_pocs:
                    research.setdefault("public_poc_urls", []).append(u)
                    all_sources.append(u)
            research["public_poc_exists"] = "yes"
            print(f"    PoC found: {len(poc_urls)} new")
        else:
            print(f"    PoC: none")
    else:
        print(f"    PoC: already yes ({len(research.get('public_poc_urls', []))} urls)")
    
    # 4. Component info search (for sources)
    if component:
        comp_sources = search_component_info(cve_id, vendor, product, component)
        all_sources.extend(comp_sources)
    
    # 5. Default enablement search (if still unknown)
    default_status = research.get("vulnerable_component_enabled_by_default", "unknown")
    if default_status == "unknown":
        def_sources = search_default_enablement(cve_id, vendor, product, component)
        all_sources.extend(def_sources)
    
    # 6. Mark as hermes-analyzed
    research["preconditions_source"] = "hermes"
    research["hunting_hypothesis_source"] = "hermes"
    if component and component != product:
        research["vulnerable_component"] = component
    
    # 7. Update meta
    original_source_count = len(meta.get("sources_consulted", []))
    deduped = list(dict.fromkeys(all_sources))
    meta["sources_consulted"] = deduped
    meta["searches_performed"] = len(deduped) - original_source_count
    record["kevrichment_research"] = research
    record["research_meta"] = meta
    
    write_cve(cve_id, record)
    print(f"  ✓ Saved")
    return {
        "cve_id": cve_id,
        "advisory": research.get("vendor_advisory_url", ""),
        "advisory_changed": not current_url or "nvd.nist.gov" in current_url,
        "new_sources": len(deduped),
        "component_improved": component != product,
    }

def main():
    cve_ids = find_cves_needing_analysis(10)
    if not cve_ids:
        print("No CVEs need analysis — all have Hermes research.")
        return
    
    print(f"Found {len(cve_ids)} CVEs needing analysis:")
    for cid in cve_ids:
        print(f"  {cid}")
    
    results = []
    errors = []
    start = time.time()
    
    for cve_id in cve_ids:
        try:
            result = process_cve(cve_id)
            results.append(result)
        except Exception as e:
            errors.append(f"{cve_id}: {e}")
            import traceback
            traceback.print_exc()
    
    elapsed = time.time() - start
    
    # Summary
    advisories_found = sum(1 for r in results if r.get("advisory") and "nvd.nist.gov" not in r["advisory"])
    components_improved = sum(1 for r in results if r.get("component_improved"))
    
    print(f"\n╔══ Batch Summary ══╗")
    print(f"  Processed: {len(results)}/{len(cve_ids)}")
    print(f"  Errors:    {len(errors)}")
    print(f"  Wall time: {elapsed:.1f}s")
    print(f"  Vendor advisories resolved: {advisories_found}")
    print(f"  Components improved: {components_improved}")
    
    if errors:
        print(f"\n  Errors:")
        for e in errors:
            print(f"    ✗ {e}")
    
    # Note: commit separately with terminal tool — execute_code sandbox lacks git config
    print(f"\n  → git commit with: cd {BASE} && git add data/cves/ && git commit -m \"kevrichment: agent research batch\" && git push")

if __name__ == "__main__":
    main()
