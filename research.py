"""
Agentic research workflow per CVE.

Two modes:
  **Agent mode** – receives ``web_search`` / ``web_extract`` callables from the
  Hermes agent context for rich multi-source web research.

  **Standalone mode** – falls back to the GitHub API, NVD data analysis, and
  direct advisory-URL construction.  No search-engine API key required.
"""

import json
import re
import time
from datetime import datetime


# ---------------------------------------------------------------------------
# Research engine
# ---------------------------------------------------------------------------

class ResearchEngine:
    """Per-CVE research engine.

    Parameters
    ----------
    web_search : callable or None
        ``web_search(query, limit=5) -> dict``  (Hermes agent tool).
        When ``None`` the engine operates in standalone mode.
    web_extract : callable or None
        ``web_extract(urls) -> dict``  (Hermes agent tool).
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
        start = time.time()
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
        }

        # -- 1.  Identify the specific vulnerable component -----------------
        component = self._extract_component(
            cve_description, product, vendor_project
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
            fallback_url = self._guess_vendor_advisory_url(cve_id, vendor_project)
            if fallback_url:
                result["vendor_advisory_url"] = fallback_url
                sources.append(fallback_url)

        # -- 5.  Preconditions & complexity ---------------------------------
        result["preconditions_for_exploit"] = self._synthesize_preconditions(
            cve_description, component, product, nvd_data
        )
        result["exploit_complexity_notes"] = self._assess_complexity(
            nvd_data, result["public_poc_exists"]
        )

        # -- 6.  Default enablement ----------------------------------------
        result["vulnerable_component_enabled_by_default"] = \
            self._check_default_enablement(cve_description, component, product)

        # -- 7.  Summary ---------------------------------------------------
        result["kevrichment_summary"] = self._generate_summary(
            result, vendor_project, product
        )

        # -- 8.  Hunting hypothesis -----------------------------------------
        result["hunting_hypothesis"] = self._generate_hunting_hypothesis(
            cve_id, vendor_project, product, cve_description, result
        )

        return result

    # ------------------------------------------------------------------
    #  Agent-mode helpers
    # ------------------------------------------------------------------

    def _agent_research(self, cve_id, vendor, product, component, result, sources):
        """Perform web searches via Hermes agent tools."""
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
                except Exception:
                    pass

        except Exception as e:
            print(f"    [WARN] Agent research failed: {e}")

    # ------------------------------------------------------------------
    #  Static / fallback helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_component(description, product, vendor):
        """Extract the specific vulnerable component from the description."""
        if not description:
            return product

        desc_low = description.lower()
        patterns = [
            # Most specific first — suffix-anchored patterns
            r'in the ([A-Z][a-zA-Z0-9_ -]{1,45}?)(?: component| module| feature| function)\b',
            r'in ([A-Z][a-zA-Z0-9_ -]{1,45}?)(?: component| module| feature| function)',
            # "vulnerability in (the) X allows|could|that…" — verb-terminated
            r'(?:a |the )?vulnerability in (?:the )?([A-Z][a-zA-Z0-9_ /-]{1,45}?)(?:\s+(?:allows|could|that|may|can|is|are|was|permit|\w+ly\b)|\s*$)',
            # Bare "vulnerability in the X" — comma/period/verb terminated
            r'(?:a |the )?vulnerability in the ([A-Z][a-zA-Z0-9_ -]{1,50}?)(?:[,\.;:]|\s+(?:allows|could|that|may|can|is|are|was|permit|\w+ly\b)|\s*$)',

            # "on affected X" — CVSS scope note pattern
            r'(?:on |the )?affected ([A-Z][a-zA-Z0-9_ -]{1,40})(?: is| are| allows| was)',
            r'the affected ([A-Z][a-zA-Z0-9_ -]{1,40})(?: is| are| component)',
        ]
        for pat in patterns:
            m = re.search(pat, description, re.IGNORECASE)
            if m:
                found = m.group(1).strip().rstrip(".")
                if 3 < len(found) < 200:
                    return found
        return product

    @staticmethod
    def _guess_vendor_advisory_url(cve_id, vendor):
        """Return a likely advisory URL based on vendor conventions."""
        known = {
            "microsoft": f"https://msrc.microsoft.com/update-guide/vulnerability/{cve_id}",
            "apache": f"https://lists.apache.org/thread.html?cve={cve_id}",
            "cisco": f"https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory?cve={cve_id}",
            "adobe": f"https://helpx.adobe.com/security/products.html/{cve_id}",
            "google": f"https://chromereleases.googleblog.com/search?q={cve_id}",
            "apple": f"https://support.apple.com/en-us/{cve_id.replace('-', '').lower()}",
            "linux": f"https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id={cve_id}",
            "oracle": f"https://www.oracle.com/security-alerts/{cve_id.replace('-', '_').lower()}.html",
            "vmware": f"https://www.vmware.com/security/advisories.html?cve={cve_id}",
            "fortinet": f"https://www.fortiguard.com/psirt?cve={cve_id}",
        }
        vendor_low = vendor.lower().strip()
        for key, url in known.items():
            if key in vendor_low:
                return url
        # Fallback: NVD detail page
        return f"https://nvd.nist.gov/vuln/detail/{cve_id}"

    @staticmethod
    def _check_default_enablement(description, component, product):
        """Determine if vulnerable component is enabled by default."""
        if not description:
            return "unknown"
        dl = description.lower()

        if "default" in dl or "by default" in dl:
            for word in ("enabled", "enable", "present", "active", "installed", "default configuration"):
                if word in dl:
                    return "yes"
            for word in ("disabled", "disables", "not", "opt-in"):
                if word in dl:
                    return "no"

        return "unknown"

    @staticmethod
    def _synthesize_preconditions(description, component, product, nvd_data):
        """Build structured precondition summary from CVSS + description."""
        if not description:
            return "Insufficient information to determine preconditions."

        pre = []
        dl = description.lower()

        # Network / local
        if any(w in dl for w in ("network", "remote", "adjacent", "over http", "tcp", "http request")):
            pre.append("Network access to the vulnerable service")
        if any(w in dl for w in ("local", "authenticated", "physical")):
            pre.append("Local or authenticated access")

        # Auth
        if "unauthenticated" in dl or "no authentication" in dl:
            pre.append("No authentication required")
        elif "authenticated" in dl or "authentication" in dl:
            pre.append("Valid credentials required")

        # User interaction
        if any(w in dl for w in ("click", "user interaction", "phishing", "social engineering")):
            pre.append("User interaction required")

        # From CVSS
        if nvd_data:
            vulns = nvd_data.get("vulnerabilities") or []
            if vulns:
                metrics = vulns[0].get("cve", {}).get("metrics", {})
                cvss = (metrics.get("cvssMetricV31") or metrics.get("cvssMetricV30") or [{}])[0]
                cd = cvss.get("cvssData", {})
                av = cd.get("attackVector", "")
                ac = cd.get("attackComplexity", "")
                pr = cd.get("privilegesRequired", "")
                ui = cd.get("userInteraction", "")

                if av == "NETWORK":
                    pre.append("Network-based (CVSS: AV:N)")
                elif av == "ADJACENT_NETWORK":
                    pre.append("Adjacent network access required (CVSS: AV:A)")
                elif av == "LOCAL":
                    pre.append("Local access required (CVSS: AV:L)")
                if ac == "HIGH":
                    pre.append("Attack complexity is HIGH (CVSS: AC:H)")
                if pr == "NONE":
                    pre.append("No privileges required (CVSS: PR:N)")
                if ui == "NONE":
                    pre.append("No user interaction required (CVSS: UI:N)")

        # Deployment precondition
        if component and component != product:
            pre.append(f"Target must serve {product} with the {component} component accessible")
        else:
            pre.append(f"Target must be running a vulnerable version of {product}")

        return "; ".join(pre)

    @staticmethod
    def _assess_complexity(nvd_data, poc_exists):
        """Assess exploitation complexity."""
        notes = []
        if poc_exists == "yes":
            notes.append("Public PoC available — significantly lowers barrier to exploitation")

        if nvd_data:
            vulns = nvd_data.get("vulnerabilities") or []
            if vulns:
                metrics = vulns[0].get("cve", {}).get("metrics", {})
                cvss = (metrics.get("cvssMetricV31") or metrics.get("cvssMetricV30") or [{}])[0]
                cd = cvss.get("cvssData", {})
                ac = cd.get("attackComplexity", "")
                score = cd.get("baseScore", 0)

                if ac == "LOW":
                    notes.append("CVSS attack complexity: LOW")
                elif ac == "HIGH":
                    notes.append("CVSS attack complexity: HIGH")
                if score >= 9.0:
                    notes.append("CRITICAL severity (CVSS >= 9.0)")
                elif score >= 7.0:
                    notes.append("HIGH severity (CVSS 7.0–8.9)")

        if not notes:
            notes.append("Exploitation complexity data limited — review vendor advisory for details")

        return " | ".join(notes)

    @staticmethod
    def _generate_summary(result, vendor, product):
        """Concise research summary."""
        parts = []
        comp = result.get("vulnerable_component", "")
        label = f"{vendor} {product}"
        if comp and comp != product:
            label += f" ({comp})"
        parts.append(label)

        poc = result.get("public_poc_exists", "unknown")
        if poc == "yes":
            n = len(result.get("public_poc_urls", []))
            parts.append(f"Public PoC found ({n} {'repo' if n == 1 else 'repos'})")
        elif poc == "no":
            parts.append("No public PoC identified in this cycle")

        default = result.get("vulnerable_component_enabled_by_default", "unknown")
        if default == "yes":
            parts.append("Enabled by default — broad exposure")
        elif default == "no":
            parts.append("Not enabled by default — reduced exposure")

        if result.get("vendor_advisory_url"):
            parts.append("Vendor advisory located")

        return " | ".join(parts) if parts else "Research incomplete"

    @staticmethod
    def _generate_hunting_hypothesis(cve_id, vendor, product, description, result):
        """Generate a concise, actionable hunting hypothesis (one sentence).

        Describes the *specific attacker behavior or TTP to look for*,
        not a rehash of preconditions or CVSS scores.  Examples:
          "Monitor for phishing links serving crafted HTML pages that
           trigger type confusion in V8."
          "Hunt for malformed VXLAN/GRE packets targeting EOS
           decapsulation interfaces."
        """
        comp = result.get("vulnerable_component", product)
        desc = (description or "").lower()
        product_low = product.lower()
        vendor_low = vendor.lower()

        # -- Ordered from most to least specific pattern --------------------
        # Each check returns a hypothesis immediately on first match.

        # Browser memory corruption (Chrome, Edge, Firefox, Safari)
        if any(b in product_low for b in ("chrome", "chromium", "edge", "firefox", "safari")):
            if any(w in desc for w in ("out of bounds", "type confusion",
                                       "use after free", "use-after-free",
                                       "buffer overflow", "heap overflow",
                                       "memory corruption")):
                if "html" in desc or "page" in desc or "web" in desc:
                    return (
                        f"Monitor for phishing links or compromised websites "
                        f"serving crafted HTML pages that trigger memory "
                        f"corruption in the {comp} engine."
                    )
                return (
                    f"Look for untrusted content — web pages, email "
                    f"attachments, or network inputs — that trigger memory "
                    f"corruption in the {comp} component of {product}."
                )

        # Tunnel / decapsulation protocol vulns (Arista, Cisco, network gear)
        if any(w in desc for w in ("tunnel", "decapsulation", "decapsulate",
                                   "vxlan", "gre ", "geneve")):
            proto = "tunnel protocol"
            if "vxlan" in desc:
                proto = "VXLAN"
            elif "gre" in desc:
                proto = "GRE"
            elif "geneve" in desc:
                proto = "GENEVE"
            return (
                f"Hunt for malformed {proto} packets targeting "
                f"{product} decapsulation interfaces — the device does "
                f"not verify the tunnel protocol type before processing."
            )

        # API / endpoint exposure — specific HTTP endpoints
        m = re.search(r'(?:POST|GET|PUT|DELETE)\s+/[a-zA-Z0-9_/-]+', description or "")
        if m and any(w in desc for w in ("endpoint", "request body",
                                          "configuration", "supplied",
                                          "preview")):
            return (
                f"Monitor for {m.group()} requests with crafted body "
                f"content that exploit insufficient validation in "
                f"the {comp} component of {product}."
            )

        # Auth bypass (certificate, IKEv1, SSO, OAuth)
        if any(w in desc for w in ("bypass user authentication",
                                    "bypass authentication",
                                    "authentication bypass",
                                    "certificate validation",
                                    "improper authentication",
                                    "missing authentication",
                                    "unauthenticated")):
            if "ike" in desc or "vpn" in desc:
                return (
                    f"Look for IKEv1 VPN connection attempts with crafted "
                    f"certificates designed to bypass user authentication "
                    f"on {product} Remote Access gateways."
                )
            return (
                f"Monitor for unauthenticated access attempts to the {comp} "
                f"component of {product} — requests without valid session "
                f"or token headers."
            )

        # OS command injection (CWE-78 family)
        if any(w in desc for w in ("command injection", "os command",
                                    "execute arbitrary command",
                                    "arbitrary command",
                                    "spawned the supplied command",
                                    "command execution",
                                    "CWE-78")):
            return (
                f"Look for crafted input to the {comp} component of "
                f"{product} that injects OS commands — monitor process "
                f"trees for spawned shells or unexpected child processes."
            )

        # Crafted file upload
        if all(w in desc for w in ("crafted file", "upload", "cli")):
            return (
                f"Monitor for local users uploading crafted files via "
                f"the {product} CLI that bypass input validation to "
                f"execute arbitrary commands."
            )

        # Memory safety (general, non-browser)
        if any(w in desc for w in ("out of bounds", "out-of-bounds",
                                    "buffer overflow", "heap overflow",
                                    "buffer over-read", "over-read",
                                    "CWE-125", "CWE-787", "CWE-119",
                                    "CWE-122", "CWE-416")):
            return (
                f"Hunt for oversized or malformed input payloads sent to "
                f"the {comp} component of {product} that could trigger "
                f"memory corruption."
            )

        # SQL injection
        if any(w in desc for w in ("sql injection", "sqli",
                                    "CWE-89")):
            return (
                f"Monitor {product} logs for unexpected SQL query patterns "
                f"or error responses indicating injection attempts against "
                f"the {comp} interface."
            )

        # Path traversal
        if any(w in desc for w in ("path traversal", "directory traversal",
                                    "CWE-22")):
            return (
                f"Look for requests containing '../' or encoded traversal "
                f"sequences targeting the {comp} endpoint of {product}."
            )

        # Improper input validation (generic)
        if any(w in desc for w in ("insufficient validation",
                                    "improper validation",
                                    "CWE-20", "CWE-116")):
            return (
                f"Hunt for specially crafted requests to the {comp} "
                f"component of {product} that bypass input validation "
                f"and trigger unintended code paths."
            )

        # XSS
        if any(w in desc for w in ("xss", "cross-site", "cross site",
                                    "CWE-79")):
            return (
                f"Monitor for reflective or stored script injection "
                f"in the {comp} component of {product}, typically "
                f"delivered via phishing URLs."
            )

        # Deserialization
        if any(w in desc for w in ("deserialization", "untrusted data",
                                    "CWE-502")):
            return (
                f"Monitor {product} for untrusted deserialization "
                f"attempts — unexpected serialized objects submitted "
                f"to the {comp} component."
            )

        # Privilege escalation
        if any(w in desc for w in ("privilege escalation",
                                    "privilege elevation",
                                    "CWE-269")):
            return (
                f"Hunt for users or processes gaining privileges beyond "
                f"their authorized scope in the {comp} component — "
                f"watch for unusual admin-level API calls from "
                f"low-privileged sources."
            )

        # SSRF
        if any(w in desc for w in ("ssrf", "server-side request forgery",
                                    "CWE-918")):
            return (
                f"Monitor {product} for outbound connections to internal "
                f"or unexpected destinations originating from the {comp} "
                f"component — classic SSRF indicator."
            )

        # Race condition
        if any(w in desc for w in ("race condition", "time-of-check",
                                    "toctou", "CWE-362")):
            return (
                f"Look for concurrent requests to the {comp} component "
                f"of {product} that exploit timing windows — rapid "
                f"sequential writes to the same resource."
            )

        # -- Final fallback from preconditions -----------------------------
        pre = result.get("preconditions_for_exploit", "").lower()
        if "local" in pre and "auth" in pre:
            return (
                f"Monitor for authenticated local user activity involving "
                f"the {comp} component of {product} — watch for "
                f"unusual file modifications or process execution."
            )
        if "network" in pre and "auth" in pre:
            return (
                f"Monitor for authenticated network requests to the {comp} "
                f"component of {product} that exploit the vulnerable "
                f"operation."
            )
        if "network" in pre:
            return (
                f"Hunt for network-based exploitation attempts targeting "
                f"the {comp} component of {product}."
            )
        return (
            f"Look for exploitation activity against the {comp} "
            f"component of {product}."
        )


# Convenience alias for backwards compat
def research_cve(cve_id, vendor_project, product, cve_description,
                 nvd_data=None, vulnrichment_data=None,
                 web_search=None, web_extract=None):
    """One-shot research for a single CVE (creates a temporary engine)."""
    engine = ResearchEngine(web_search=web_search, web_extract=web_extract)
    return engine.research(cve_id, vendor_project, product, cve_description,
                           nvd_data, vulnrichment_data)
