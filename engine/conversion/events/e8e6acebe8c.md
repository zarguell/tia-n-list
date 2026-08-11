Microsoft has shipped the largest Patch Tuesday release in history: **622 vulnerabilities** across its product suite, shattering June's previous record of 198. The release includes 56 Critical and 510 Important vulnerabilities. Two vulnerabilities were exploited in the wild:

- **CVE-2026-56155** (CVSS 7.8) — Active Directory Federation Services elevation of privilege. An authorized attacker can elevate to administrator privileges. Credited to Microsoft DART, indicating discovery during active incident response. Microsoft has not disclosed exploitation details.

- **CVE-2026-56164** (CVSS 5.3) — Microsoft SharePoint Server elevation of privilege. Missing authentication for a critical function allows unauthorized privilege escalation over the network. AMSI integration can mitigate. Credited to Mandiant Incident Response and Google Cloud FLARE team.

The release also includes a **publicly disclosed vulnerability**: **CVE-2026-50661** (CVSS 6.1) — Windows BitLocker security feature bypass. Likely patches the "GreatXML" BitLocker bypass disclosed by Nightmare Eclipse in June, which requires physical access.

**Additional critical items** from the massive release:

- **CVE-2026-55944** (CVSS 9.8, Exploitation More Likely) — Microsoft Dynamics NAV/Business Central RCE via untrusted data deserialization. No authentication or user interaction required.

- **Multiple DHCP Server RCEs** (CVSS 8.8–9.8) — Five critical DHCP vulnerabilities, three assessed Exploitation More Likely.

- **20 Windows Kernel EoP** vulnerabilities, six assessed Exploitation More Likely.

- **Nightmare Eclipse "LegacyHive"** — A new PoC for mounting another user's NT user hive has emerged from the same researcher.

**Rapid7 SharePoint Research (CVE-2026-55040):** Rapid7 Labs disclosed a critical (CVSS 9.1) JWT token authentication bypass in Microsoft SharePoint, discovered during a zero-day research project for Pwn2Own Berlin. An unauthenticated attacker who knows a target user's AD SID or UPN can bypass authentication and assume that user's identity — including site administrators. Rapid7 has chained this with a separate RCE vulnerability for **unauthenticated remote code execution**. The RCE component will be patched in the August Patch Tuesday cycle; patching CVE-2026-55040 now breaks the full chain. Full technical details will be published within 30 days.

**Lifecycle note:** SharePoint Server 2016 and 2019 reached end of extended support today (July 14, 2026). No ESU is available — only SharePoint Subscription Edition remains supported.

**Action:** Prioritize AD FS patching (CVE-2026-56155) and SharePoint updates (CVE-2026-56164, CVE-2026-55040). The Rapid7 SharePoint auth bypass + pending RCE chain makes unpatched SharePoint servers an urgent target.

---
