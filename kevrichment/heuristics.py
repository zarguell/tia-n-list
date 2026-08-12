"""Heuristic analysis functions for CVE research enrichment.

Extracted from ResearchEngine — these are pure functions that analyze NVD
descriptions, synthesize preconditions, and generate hunting hypotheses.
They don't use instance state and are independently testable.
"""

import re


def extract_component(description, product, vendor, nvd_data=None):
    """Extract the specific vulnerable component from the description.

    Multi-strategy extraction with CPE fallback. Returns the most specific
    deployment-recognizable component name, falling back to *product* when
    nothing better is found.
    """
    if not description:
        return product

    candidates = []  # (component, weight) — higher weight = more specific

    # ── Strategy 1: named thing with type keyword ────────────────────
    # "in the [NAME] function/module/component/control/dll/library/…"
    patterns_keyword = [
        # (pattern, weight_bonus)
        (r'(?:in|within)\s+the\s+'
         r'([A-Z][A-Za-z0-9_:\-.()/]{1,70}?)'
         r'\s+(?:function|class|method|subroutine|api)\b',
         2),   # very specific (function-level) — low weight
        # Lowercase-starting function names: "in the string_vformat function"
        (r'(?:in|within)\s+the\s+'
         r'([a-z][A-Za-z0-9_]{2,60})'
         r'\s+function\b',
         2),   # function-level (lowercase) — same weight
        (r'(?:in|within)\s+the\s+'
         r'([A-Z][A-Za-z0-9_:\-()/ ]{1,70}?)'
         r'\s+(?:control|driver|service|server|object|handler|plugin|addon|filter)\b',
         6),   # deployment-recognizable component
        (r'(?:in|within)\s+the\s+'
         r'([A-Z][A-Za-z0-9_:\-()/ ]{1,70}?)'
         r'\s+(?:dll|library)\b',
         4),   # generic library/dll — lower weight to avoid overmatching
        # "in the X component" — without requiring "of" after it
        (r'(?:in|within)\s+the\s+'
         r'([A-Z][A-Za-z0-9_:\-()/ ]{1,70}?)'
         r'\s+component\b',
         4),   # component mention
        (r'(?:in|within)\s+the\s+'
         r'([A-Z][A-Za-z0-9_:\-()/ ]{1,70}?)'
         r'\s+(?:component|module|feature|engine)\s+of\b',
         5),   # "component of" — more specific
    ]
    for pat, weight in patterns_keyword:
        for m in re.finditer(pat, description):
            # Don't use IGNORECASE — require literal [A-Z] for component name
            raw = m.group(1).strip().rstrip(".")
            found = raw.rstrip("()")
            if 3 < len(found) < 200 and found.lower() != product.lower():
                # Reject candidates with unmatched parentheses (check raw before rstrip)
                if raw.count("(") != raw.count(")"):
                    continue
                candidates.append((found, weight))

    # ── Strategy 2: vulnerability-type keyword patterns ──────────────
    # "Stack-based buffer overflow in [the] [NAME] allows|could|…"
    vuln_heads = [
        r'(?:buffer\s+overflow|heap\s+overflow|stack\s+overflow)',
        r'(?:use-after-free|type\s+confusion|out-of-bounds\s+(?:read|write))',
        r'(?:integer\s+overflow|memory\s+corruption|race\s+condition)',
        r'(?:privilege\s+escalation|remote\s+code\s+execution)',
        r'(?:improper\s+(?:input\s+)?validation|missing\s+authentication)',
        r'(?:cross-site\s+scripting|SQL\s+injection|path\s+traversal)',
        r'(?:vulnerability|weakness|flaw|defect)',
    ]
    for head in vuln_heads:
        pat = (
            head + r'\s+in\s+(?:the\s+)?'
            # Greedy quantifier — avoids :: matching the terminator
            r'([A-Z][A-Za-z0-9_:\-.()/]{1,70})'
            r'(?:\s+(?:function|component|module|allows|could|that|may|can|is|are|was|permit|in|'
            r'exists|triggers|results|leads|gives|grants|allowing|causing|leading|'
            r'\w+ly\b)|[.,;)\]]|$)'
        )
        for m in re.finditer(pat, description):
            # Case-sensitive: require literal [A-Z] for component name start
            raw = m.group(1).strip().rstrip(".")
            found = raw.rstrip("()")
            if 3 < len(found) < 200 and found.lower() != product.lower():
                if raw.count("(") != raw.count(")"):
                    continue
                candidates.append((found, 5))

    # ── Strategy 3: "as used in the [COMPONENT]" ────────────────────
    # Describes the deployment context: "as used in the X control"
    m = re.search(
        r'as used in (?:the |an |a )?'
        r'([A-Z][A-Za-z0-9_:\-.()/ ]{1,70}?)'
        r'(?:\s+(?:control|dll|library|module|component|object|in|for|[.,;:]|$))',
        description
    )
    if m:
        raw = m.group(1).strip().rstrip(".")
        found = raw.rstrip("()")
        if 3 < len(found) < 200 and found.lower() != product.lower():
            if raw.count("(") != raw.count(")"):
                pass
            else:
                candidates.append((found, 5))

    # ── Strategy 4: "on affected [COMPONENT]" / "affected [COMPONENT]" ─
    for m in re.finditer(
        r'(?:the |on )?affected\s+'
        r'([A-Z][A-Za-z0-9_:\-.()/ ]{1,50}?)'
        r'(?:\s+(?:component|module|function|is|are|allows|was|[.,;:]|$))',
        description
    ):
        raw = m.group(1).strip().rstrip(".")
        found = raw.rstrip("()")
        if 3 < len(found) < 200 and found.lower() != product.lower():
            if raw.count("(") != raw.count(")"):
                continue
            candidates.append((found, 4))

    # ── Strategy 5: CPE fallback ────────────────────────────────────
    if nvd_data:
        from_software = set()
        vulns = nvd_data.get("vulnerabilities") or []
        if vulns:
            for cfg in vulns[0].get("cve", {}).get("configurations", []):
                for node in cfg.get("nodes", []):
                    for cpe_match in node.get("cpeMatch", []):
                        criteria = cpe_match.get("criteria", "")
                        if cpe_match.get("vulnerable", False):
                            parts = criteria.split(":")
                            if len(parts) >= 6:
                                cpe_vendor = parts[3]
                                cpe_product = parts[4]
                                cpe_part = parts[2]
                                # Only "a" (application) parts — skip OS/hardware
                                if cpe_part == "a" and cpe_vendor.lower() != vendor.lower():
                                    name = cpe_product.replace("_", " ").title()
                                    if 3 < len(name) < 200 and name.lower() != product.lower():
                                        from_software.add(name)
        if from_software:
            for name in from_software:
                candidates.append((name, 3))

    # ── Select the best candidate ───────────────────────────────────
    if not candidates:
        return product

    # Deduplicate by name, keep highest weight
    best = {}
    for name, weight in candidates:
        if name not in best or weight > best[name]:
            best[name] = weight

    # Sort by weight desc, length desc (prefer longer = more specific)
    ranked = sorted(best.items(), key=lambda x: (-x[1], -len(x[0])))
    return ranked[0][0]


def guess_vendor_advisory_url(cve_id, vendor):
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


def check_default_enablement(description, component, product):
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


def synthesize_preconditions(description, component, product, nvd_data):
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


def assess_complexity(nvd_data, poc_exists):
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


def generate_summary(result, vendor, product):
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


def generate_hunting_hypothesis(cve_id, vendor, product, description,
                                 cwe_ids, cvss_av, cvss_ac, cvss_pr,
                                 cvss_ui, result):
    """Generate a hunting hypothesis by composing independent data dimensions.

    Builds a single actionable sentence from *structured data fields* that
    were extracted independently (CWE, CVSS, component name, delivery
    mechanism from description), not from hardcoded keyword->template maps.

    This ensures the hypothesis is genuinely *derived* from analysis for
    each CVE rather than pattern-matched from product/vendor names.

    Dimensions
    ----------
    1. Vulnerability class   — CWE ID -> "memory corruption" / "injection" etc.
    2. Attack vector         — CVSS AV  -> "network-based" / "local" etc.
    3. Auth requirement      — CVSS PR  -> "unauthenticated" / "authenticated"
    4. User interaction      — CVSS UI  -> "user interaction required" / "none"
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

    vuln_action = "exploit the vulnerability"
    for cwe_id in cwe_ids:
        if cwe_id in CWE_CLASS_MAP:
            vuln_action = CWE_CLASS_MAP[cwe_id][1]
            break

    # ---- 2. Attack vector from CVSS ----
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


def extract_delivery_mechanism(description):
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
