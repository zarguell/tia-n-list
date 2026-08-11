*Previously covered Jul 29 (initial disclosure). New today: CISA added to KEV with a 3-day remediation deadline, Hotfix now available across all affected release trains.*

**CVE-2026-20316** — a high-severity (CVSS 5.3, rated High by Cisco) static credential vulnerability in Cisco Secure Firewall Management Center — has been **added to CISA's Known Exploited Vulnerabilities (KEV) catalog** as of July 29. Federal agencies have until **August 1, 2026** to remediate under BOD 26-04.

**Key details:**

- Static credentials for a low-privilege account are hardcoded into FMC software affecting releases 7.0, 7.2, 7.4, 7.6, 7.7, and 10.0

- **No workarounds available** — patch or isolate

- The low-privilege access can be chained with other FMC vulnerabilities (not yet identified by Cisco) to escalate privileges

- CISA's KEV entry confirms this is being actively used in attacks

- Attack surface reduced when FMC management interface is not internet-exposed, but CISA's KEV inclusion signals widespread scanning/pre-positioning

- Reported by Jimi Sebree of Horizon3.ai

**Cisco FMC attack chain implications:** This follows the Jul 27 addition of **Arista VeloCloud CVE-2026-16812** (CVSS 10) to KEV — two major network management appliances have had exploited zero-days added to CISA's catalog within one week.

**Action:** Install hotfixes available from Cisco for each affected release train. Audit `/var/log/messages` for signs of prior exploitation.
