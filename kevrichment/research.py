"""
Agentic research workflow per CVE.

Two modes:
  **Agent mode** – receives ``web_search`` / ``web_extract`` callables from the
  agent context for rich multi-source web research.

  **Standalone mode** – falls back to the GitHub API, NVD data analysis, and
  direct advisory-URL construction.  No search-engine API key required.
"""

from heuristics import (
    assess_complexity,
    check_default_enablement,
    extract_component,
    extract_delivery_mechanism,
    generate_hunting_hypothesis,
    generate_summary,
    guess_vendor_advisory_url,
    synthesize_preconditions,
)

# ---------------------------------------------------------------------------
# Research engine
# ---------------------------------------------------------------------------

class ResearchEngine:
    """Per-CVE research engine.

    Parameters
    ----------
    web_search : callable or None
        ``web_search(query, limit=5) -> dict``  (agent tool).
        When ``None`` the engine operates in standalone mode.
    web_extract : callable or None
        ``web_extract(urls) -> dict``  (agent tool).
    """

    def __init__(self, web_search=None, web_extract=None):
        self._web_search = web_search
        self._web_extract = web_extract
        self._agent_mode = web_search is not None

    # ------------------------------------------------------------------ Main

    def research(self, cve_id, vendor_project, product, cve_description,
                 nvd_data=None, vulnrichment_data=None):
        """Run the full research workflow for one CVE.

        Returns
        -------
        dict
            ``kevrichment_research`` block ready to insert into the CVE record.
        """
        searches = 0
        sources = []

        result = {
            "vulnerable_component": "",
            "vulnerable_component_enabled_by_default": "unknown",
            "preconditions_for_exploit": "",
            "public_poc_exists": "unknown",
            "public_poc_urls": [],
            "vendor_advisory_url": "",
            "exploit_complexity_notes": "",
            "kevrichment_summary": "",
            "delivery_mechanism": None,
        }

        # -- 1.  Identify the specific vulnerable component -----------------
        component = extract_component(
            cve_description, product, vendor_project, nvd_data=nvd_data
        )
        result["vulnerable_component"] = component

        # -- 2.  Search for public PoC on GitHub ---------------------------
        from ingest import search_github_poc
        gh_results = search_github_poc(cve_id)
        searches += 1
        sources.append(f"github (search:{cve_id})")

        poc_urls = [r["url"] for r in gh_results]
        if poc_urls:
            result["public_poc_exists"] = "yes"
            result["public_poc_urls"] = poc_urls
        else:
            result["public_poc_exists"] = "no"

        # -- 3.  Agent-assisted enrichment ---------------------------------
        if self._agent_mode:
            self._agent_research(cve_id, vendor_project, product, component,
                                 result, sources)
            searches += 3  # three web_search calls inside

        # -- 4.  Vendor advisory -------------------------------------------
        if not result.get("vendor_advisory_url"):
            fallback_url = guess_vendor_advisory_url(cve_id, vendor_project)
            if fallback_url:
                result["vendor_advisory_url"] = fallback_url
                sources.append(fallback_url)

        # -- 5.  Preconditions & complexity ---------------------------------
        result["preconditions_for_exploit"] = synthesize_preconditions(
            cve_description, component, product, nvd_data
        )
        result["exploit_complexity_notes"] = assess_complexity(
            nvd_data, result["public_poc_exists"]
        )

        # -- 6.  Default enablement ----------------------------------------
        result["vulnerable_component_enabled_by_default"] = \
            check_default_enablement(cve_description, component, product)

        # -- 7.  Summary ---------------------------------------------------
        result["kevrichment_summary"] = generate_summary(
            result, vendor_project, product
        )

        # -- 7b. Delivery mechanism (for transparency) ---------------------
        result["delivery_mechanism"] = extract_delivery_mechanism(
            cve_description
        )

        # -- 8.  Hunting hypothesis -----------------------------------------
        # Extract CWE and CVSS data from NVD for compositional hypothesis
        cwe_ids = []
        cvss_av = None
        cvss_ac = None
        cvss_pr = None
        cvss_ui = None
        if nvd_data:
            vulns = nvd_data.get("vulnerabilities") or []
            if vulns:
                cve_item = vulns[0].get("cve", {})
                for w in cve_item.get("weaknesses", []):
                    for d in w.get("description", []):
                        val = d.get("value", "")
                        if val.startswith("CWE-"):
                            cwe_ids.append(val)
                metrics = cve_item.get("metrics", {})
                cvss = (metrics.get("cvssMetricV31") or metrics.get("cvssMetricV30") or [{}])[0]
                cd = cvss.get("cvssData", {})
                cvss_av = cd.get("attackVector")
                cvss_ac = cd.get("attackComplexity")
                cvss_pr = cd.get("privilegesRequired")
                cvss_ui = cd.get("userInteraction")
        result["hunting_hypothesis"] = generate_hunting_hypothesis(
            cve_id, vendor_project, product, cve_description,
            cwe_ids, cvss_av, cvss_ac, cvss_pr, cvss_ui, result
        )

        return result

    # ------------------------------------------------------------------
    #  Agent-mode helpers
    # ------------------------------------------------------------------

    def _agent_research(self, cve_id, vendor, product, component, result, sources):
        """Perform web searches via agent tools."""
        try:
            # Component research
            q1 = f"{vendor} {product} {cve_id} vulnerable component {component}"
            r1 = self._web_search(q1, limit=3)
            if r1 and "data" in r1:
                for item in r1["data"].get("web", []):
                    url = item.get("url", "")
                    if url:
                        sources.append(url)

            # Default-enablement research
            if component:
                q2 = f"{vendor} {product} {component} {'enabled by default' if len(component) > 3 else 'default configuration'}"
                r2 = self._web_search(q2, limit=3)
                if r2 and "data" in r2:
                    for item in r2["data"].get("web", []):
                        sources.append(item.get("url", ""))

            # Vendor advisory search
            q3 = f"{vendor} {cve_id} security advisory patch"
            r3 = self._web_search(q3, limit=3)
            if r3 and "data" in r3:
                for item in r3["data"].get("web", []):
                    url = item.get("url", "")
                    if url:
                        sources.append(url)
                        if not result["vendor_advisory_url"]:
                            low = url.lower()
                            if any(kw in low for kw in ("advisory", "security", "patch", "cve")):
                                result["vendor_advisory_url"] = url

            # Try to pull advisory content
            if result["vendor_advisory_url"] and self._web_extract:
                try:
                    self._web_extract([result["vendor_advisory_url"]])
                except Exception as e:
                    print(f"    [WARN] web_extract failed: {e}")

        except Exception as e:
            print(f"    [WARN] Agent research failed: {e}")


# Convenience alias for backwards compat
def research_cve(cve_id, vendor_project, product, cve_description,
                 nvd_data=None, vulnrichment_data=None,
                 web_search=None, web_extract=None):
    """One-shot research for a single CVE (creates a temporary engine)."""
    engine = ResearchEngine(web_search=web_search, web_extract=web_extract)
    return engine.research(cve_id, vendor_project, product, cve_description,
                           nvd_data, vulnrichment_data)
