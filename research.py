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

    def __init__(self, web_search=None, web_extract=None, llm_synthesis_fn=None):
        self._web_search = web_search
        self._web_extract = web_extract
        self._agent_mode = web_search is not None
        self._llm_synthesis_fn = llm_synthesis_fn

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
            "delivery_mechanism": None,
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

        # -- 7b. Delivery mechanism (for transparency) ---------------------
        result["delivery_mechanism"] = self._extract_delivery_mechanism(
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
        result["hunting_hypothesis"] = self._generate_hunting_hypothesis(
            cve_id, vendor_project, product, cve_description,
            cwe_ids, cvss_av, cvss_ac, cvss_pr, cvss_ui, result
        )

        # -- 9.  LLM synthesis overrides (if configured) --------------------
        if self._llm_synthesis_fn:
            cvss_vector = ""
            if nvd_data:
                vulns = nvd_data.get("vulnerabilities") or []
                if vulns:
                    metrics = vulns[0].get("cve", {}).get("metrics", {})
                    cvss_entry = (metrics.get("cvssMetricV31") or
                                  metrics.get("cvssMetricV30") or [{}])[0]
                    cvss_vector = (cvss_entry.get("cvssData", {})
                                   .get("vectorString", ""))

            llm_data = dict(result)  # shallow copy — safe for strings/lists
            llm_result = self._llm_synthesis_fn(
                cve_id=cve_id,
                vendor=vendor_project,
                product=product,
                description=cve_description,
                cwe_ids=cwe_ids,
                cvss_vector=cvss_vector,
                vulnrichment_data=vulnrichment_data,
                research_data=llm_data,
            )
            if llm_result:
                if llm_result.get("preconditions"):
                    result["preconditions_for_exploit"] = llm_result["preconditions"]
                    result["preconditions_source"] = "llm"
                if llm_result.get("hunting_hypothesis"):
                    result["hunting_hypothesis"] = llm_result["hunting_hypothesis"]
                    result["hunting_hypothesis_source"] = "llm"

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
        """Build a precondition summary that answers: what must be true in
        *your deployment* for this CVE to be exploitable?

        Uses CVSS vector + product class (not description keyword matching)
        to determine the realistic access model:
          - Browsers/email clients → user interaction is the gate
          - Network services/appliances → network reachability
          - CLI/local tools → authenticated shell access

        Returns a compact, deployment-actionable string.
        """
        if not description:
            return "Insufficient information to determine preconditions."

        product_low = product.lower()

        # ---- Determine product class ----
        # Browser / client-side app
        is_browser = any(b in product_low for b in (
            "chrome", "chromium", "firefox", "safari", "edge", "browser"
        ))
        is_document_viewer = any(d in product_low for d in (
            "pdf", "reader", "viewer", "document", "office", "word", "excel"
        ))
        is_email_client = any(e in product_low for e in (
            "mail", "outlook", "thunderbird", "email client"
        ))
        is_network_appliance = any(n in product_low for n in (
            "switch", "router", "gateway", "firewall", "vpn",
            "load balancer", "ips", "ids"
        ))

        # ---- Extract CVSS fields ----
        cvss_av = None
        cvss_pr = None
        cvss_ui = None
        if nvd_data:
            vulns = nvd_data.get("vulnerabilities") or []
            if vulns:
                metrics = vulns[0].get("cve", {}).get("metrics", {})
                cvss_entry = (metrics.get("cvssMetricV31") or
                              metrics.get("cvssMetricV30") or [{}])[0]
                cd = cvss_entry.get("cvssData", {})
                cvss_av = cd.get("attackVector")
                cvss_pr = cd.get("privilegesRequired")
                cvss_ui = cd.get("userInteraction")

        pre = []

        # ---- Build the primary precondition ----
        if is_browser or is_document_viewer or is_email_client:
            # Client-side: user interaction is the main gate
            if cvss_ui == "REQUIRED" or is_browser:
                pre.append(
                    "User must interact with malicious content "
                    "(click a link, visit a webpage, open an attachment)"
                )
            else:
                # Rare: browser vuln with UI:N (drive-by without interaction)
                pre.append(
                    "User must visit a compromised or malicious webpage "
                    "(no explicit interaction required beyond page load)"
                )
        elif is_network_appliance or cvss_av == "NETWORK":
            # Server / network service
            if cvss_pr == "NONE":
                pre.append(
                    "Network reachability to the affected interface or "
                    "service — no authentication barrier"
                )
            elif cvss_pr == "LOW":
                pre.append(
                    "Network reachability to the affected interface or "
                    "service — low-privileged credentials required"
                )
            else:
                pre.append(
                    "Network reachability to the affected interface or "
                    "service — administrative credentials required"
                )

            # Add user interaction note if relevant
            if cvss_ui == "REQUIRED":
                pre.append(
                    "User on the target system must perform an action "
                    "(click, confirm, visit a URL) for the exploit to succeed"
                )
        elif cvss_av == "ADJACENT_NETWORK":
            pre.append(
                "Adjacent network access to the vulnerable component "
                "(same broadcast domain, layer-2 adjacency)"
            )
        elif cvss_av == "LOCAL":
            pre.append("Local shell or interactive access to the target system")
        elif cvss_av == "PHYSICAL":
            pre.append("Physical access to the target device or console")
        else:
            # Fallback
            pre.append("Unknown attack vector — review vendor advisory")

        # ---- Deployment precondition ----
        if component and component != product:
            pre.append(
                f"Target must run {product} with the {component} "
                f"component accessible"
            )
        else:
            pre.append(
                f"Target must run a vulnerable version of {product}"
            )

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

    def _generate_hunting_hypothesis(self, cve_id, vendor, product, description,
                                      cwe_ids, cvss_av, cvss_ac, cvss_pr,
                                      cvss_ui, result):
        """Generate a hunting hypothesis by composing independent data dimensions.

        Builds a single actionable sentence from *structured data fields* that
        were extracted independently (CWE, CVSS, component name, delivery
        mechanism from description), not from hardcoded keyword→template maps.

        This ensures the hypothesis is genuinely *derived* from analysis for
        each CVE rather than pattern-matched from product/vendor names.

        Dimensions
        ----------
        1. Vulnerability class   — CWE ID → "memory corruption" / "injection" etc.
        2. Attack vector         — CVSS AV  → "network-based" / "local" etc.
        3. Auth requirement      — CVSS PR  → "unauthenticated" / "authenticated"
        4. User interaction      — CVSS UI  → "user interaction required" / "none"
        5. Delivery mechanism    — extracted from description text
        6. Vulnerable component  — extracted from description text
        """
        comp = result.get("vulnerable_component", product)

        # ---- 1. Vulnerability class from CWE IDs ----
        CWE_CLASS_MAP = {
            "CWE-20":   ("improper input validation", "bypass input validation"),
            "CWE-22":   ("path traversal", "traverse directories"),
            "CWE-78":   ("OS command injection", "inject OS commands"),
            "CWE-79":   ("cross-site scripting", "inject scripts"),
            "CWE-89":   ("SQL injection", "inject SQL queries"),
            "CWE-94":   ("code injection", "inject code"),
            "CWE-116":  ("improper output encoding", "bypass output encoding"),
            "CWE-119":  ("memory corruption", "trigger memory corruption"),
            "CWE-122":  ("heap-based buffer overflow", "trigger heap overflow"),
            "CWE-125":  ("out-of-bounds read", "trigger out-of-bounds reads"),
            "CWE-269":  ("privilege escalation", "escalate privileges"),
            "CWE-287":  ("improper authentication", "bypass authentication"),
            "CWE-306":  ("missing authentication", "access without authentication"),
            "CWE-352":  ("cross-site request forgery", "forge cross-site requests"),
            "CWE-362":  ("race condition", "exploit race conditions"),
            "CWE-416":  ("use-after-free", "trigger use-after-free"),
            "CWE-434":  ("unrestricted file upload", "upload arbitrary files"),
            "CWE-502":  ("deserialization of untrusted data", "trigger untrusted deserialization"),
            "CWE-787":  ("out-of-bounds write", "trigger out-of-bounds writes"),
            "CWE-798":  ("hardcoded credentials", "exploit hardcoded credentials"),
            "CWE-843":  ("type confusion", "trigger type confusion"),
            "CWE-862":  ("missing authorization", "access without authorization"),
            "CWE-863":  ("incorrect authorization", "bypass authorization"),
            "CWE-918":  ("server-side request forgery", "forge server-side requests"),
            "CWE-1023": ("incomplete comparison", "exploit incomplete comparison logic"),
        }

        vuln_class = "vulnerability"
        vuln_action = "exploit the vulnerability"
        for cwe_id in cwe_ids:
            if cwe_id in CWE_CLASS_MAP:
                vuln_class = CWE_CLASS_MAP[cwe_id][0]
                vuln_action = CWE_CLASS_MAP[cwe_id][1]
                break

        # ---- 2. Attack vector from CVSS ----
        av_desc = "remotely"
        if cvss_av == "NETWORK":
            av_desc = "over the network"
        elif cvss_av == "ADJACENT_NETWORK":
            av_desc = "from an adjacent network"
        elif cvss_av == "LOCAL":
            av_desc = "with local access"
        elif cvss_av == "PHYSICAL":
            av_desc = "with physical access"

        # ---- 3. Authentication from CVSS PR ----
        auth_desc = None
        if cvss_pr == "NONE":
            auth_desc = "no authentication required"
        elif cvss_pr == "LOW":
            auth_desc = "low-privileged access only"
        elif cvss_pr == "HIGH":
            auth_desc = "high-privileged access required"

        # ---- 4. User interaction ----
        ui_desc = None
        if cvss_ui == "REQUIRED":
            ui_desc = "user interaction"
        elif cvss_ui == "NONE":
            ui_desc = "no user interaction"

        # ---- 5. Delivery mechanism from result dict (extracted in research()) ----
        deliv = result.get("delivery_mechanism")

        # ---- 6. Compose the hypothesis sentence ----
        # Builds: "[Verb] for [attacker action that triggers vuln in component],
        #          [qualifiers]."
        # All tokens come from independently-extracted data fields (CWE, CVSS,
        # component, delivery pattern) — no product/vendor keyword templates.

        # Action clause — the core attacker behavior
        if deliv:
            # Delivery mechanism from description: "crafted HTML page" etc.
            # "designed to" avoids subject-verb agreement issues
            action = f"{deliv} designed to {vuln_action}"
        elif cvss_av == "NETWORK":
            if auth_desc == "no authentication required":
                action = f"unauthenticated network-based attempts to {vuln_action}"
            else:
                action = f"network-based attempts to {vuln_action}"
        elif cvss_av == "LOCAL":
            action = f"local attempts to {vuln_action}"
        elif cvss_av == "PHYSICAL":
            action = f"physically-proximate attempts to {vuln_action}"
        else:
            action = f"attempts to {vuln_action}"

        # Target component
        if comp != product:
            target = f"in the {comp} component of {product}"
        else:
            target = f"in {product}"

        # Assemble: "Monitor for [action] [target][qualifiers]."
        sentence = f"Monitor for {action} {target}"

        # Trailing qualifiers
        qualifiers = []
        if auth_desc and auth_desc != "no authentication required":
            qualifiers.append(auth_desc)
        if ui_desc == "user interaction":
            qualifiers.append("requiring user interaction")

        if qualifiers:
            sentence = f"{sentence} — {', '.join(q for q in qualifiers if q)}"

        sentence += "."

        return sentence

    @staticmethod
    def _extract_delivery_mechanism(description):
        """Extract the delivery/trigger mechanism from the description text.

        Uses structural patterns (prepositional phrases) rather than
        product-specific keyword matching, so the mechanism is genuinely
        *extracted* from each CVE's description rather than hardcoded.
        """
        if not description:
            return None

        desc = description.strip()

        # Pattern 1: "via [a|the] [something]" — most common delivery indicator
        # Handles "via a crafted HTML page." (period directly after)
        # Handles "via a crafted HTML page (something)" (paren after)
        m = re.search(
            r'(?:via|through)\s+(?:a\s+|an\s+|the\s+)?'
            r'(crafted\s+\w[\w\s-]{2,60}?)'
            r'(?:\s+(?:allows|could|that|which)|'
            r'\s*[\.;:,]|\s*[\)\]]|$)',
            desc, re.IGNORECASE | re.DOTALL
        )
        if m:
            mech = m.group(1).strip().rstrip(".,;")
            if 5 < len(mech) < 120:
                return mech

        # Pattern 2: "by [supplying|providing|sending|crafting|uploading|submitting|passing] [a|an|the] [something]"
        m = re.search(
            r'by\s+(?:supplying|providing|sending|crafting|uploading|submitting|passing)'
            r'\s+(?:a\s+|an\s+|the\s+)?'
            r'(\w[\w\s-]{3,80}?)'
            r'(?:\s+(?:to|that|which)|'
            r'\s*[\.;:,]|\s*[\)\]]|$)',
            desc, re.IGNORECASE | re.DOTALL
        )
        if m:
            mech = m.group(1).strip().rstrip(".,;")
            if 5 < len(mech) < 120:
                # Ensure proper article prefix
                if not any(mech.startswith(p) for p in ("a ", "an ", "the ", "a crafted", "an crafted")):
                    return f"a {mech}"
                return mech

        # Pattern 3: "an attacker could [verb] [something]"
        m = re.search(
            r'(?:an\s+)?attacker\s+could\s+'
            r'(?:send|submit|provide|craft|upload|inject)'
            r'\s+(?:a\s+|an\s+|the\s+|carefully\s+crafted\s+)?'
            r'(\w[\w\s-]{4,80}?)'
            r'(?:\s+(?:to|that|which)|'
            r'\s*[\.;:,]|\s*[\)\]]|$)',
            desc, re.IGNORECASE | re.DOTALL
        )
        if m:
            mech = m.group(1).strip().rstrip(".,;")
            if 5 < len(mech) < 120:
                return f"carefully crafted {mech}".strip()

        # Pattern 4: Bare "a crafted [something]" at start of a clause
        m = re.search(
            r'(?:a\s+|the\s+)crafted\s+(\w[\w\s-]{3,80}?)'
            r'(?:\s+(?:allows|could|that)|'
            r'\s*[\.;:,]|\s*[\)\]]|$)',
            desc, re.IGNORECASE | re.DOTALL
        )
        if m:
            mech = m.group(1).strip().rstrip(".,;")
            if 5 < len(mech) < 120:
                return f"crafted {mech}"

        # Pattern 5: HTTP endpoint reference — "POST /path" or "GET /path"
        m = re.search(
            r'(?:POST|GET|PUT|DELETE|PATCH)\s+/[a-zA-Z0-9_/-]{3,100}',
            desc, re.IGNORECASE
        )
        if m:
            return m.group(0) + " requests"

        return None


# Convenience alias for backwards compat
def research_cve(cve_id, vendor_project, product, cve_description,
                 nvd_data=None, vulnrichment_data=None,
                 web_search=None, web_extract=None):
    """One-shot research for a single CVE (creates a temporary engine)."""
    engine = ResearchEngine(web_search=web_search, web_extract=web_extract)
    return engine.research(cve_id, vendor_project, product, cve_description,
                           nvd_data, vulnrichment_data)
