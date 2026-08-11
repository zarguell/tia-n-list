Threat actors are actively exploiting CVE-2026-20230, a high-severity SSRF vulnerability (CVSS 8.6) in Cisco Unified Communications Manager (Unified CM) and Unified CM Session Management Edition, with exploitation observed over the weekend. The flaw, patched by Cisco on June 3, allows unauthenticated remote attackers to abuse the WebDialer component's handling of user-supplied URLs to write arbitrary files to the OS via `file://` URIs — ultimately achieving root privileges.

Threat intelligence firm Defused confirmed attacks originating from a single IP address using properly constructed `file://` payloads. The observed PoC appears designed for reconnaissance — writing a test file (`/tmp/cve-2026-20230-test.txt`) to vulnerable devices — but now that SSD Secure has published a full technical write-up and PoC exploit, broader weaponized exploitation is expected. CISA has **not yet** added this CVE to KEV.

**Hunting hypothesis:** Monitor for HTTP requests to Unified CM WebDialer endpoints containing `file://` URI schemes from unexpected IPs. Check for unexpected files written to `/tmp/` on CUCM appliances.

**Recommended action:** Patch immediately if running affected Unified CM versions. This is internet-facing voice infrastructure — treat as crown-jewel priority.

---
