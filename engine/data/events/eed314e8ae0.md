CISA has updated the Known Exploited Vulnerabilities catalog to flag **CVE-2026-33825 (BlueHammer)** as actively exploited by ransomware gangs. The high-severity privilege escalation flaw in Microsoft Defender was already in KEV since April 2022 following zero-day exploitation, but CISA's Monday update specifically calls out ransomware operators.

The vulnerability, leaked by researcher "Nightmare Eclipse" in April alongside PoC exploit code in protest of MSRC disclosure practices, allows a local attacker to reach SYSTEM privileges by gaining access to the Security Account Manager (SAM) database. Microsoft patched it in April 2026 Patch Tuesday, but Huntress Labs confirmed hands-on-keyboard exploitation days later. CISA has now flagged eight Microsoft Defender vulnerabilities exploited in attacks, with two of those also abused by ransomware gangs.

**Recommended action:** Confirm April 2026 Patch Tuesday was applied across all Windows endpoints. This is a post-authentication LPE — ransomware operators are likely chaining it after initial access to escalate to domain-wide compromise.

---
