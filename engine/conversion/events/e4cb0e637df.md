Oracle published an out-of-band security alert for a critical unauthenticated RCE in PeopleSoft PeopleTools (versions 8.61, 8.62) — the same zero-day exploited by ShinyHunters (UNC6240) since late May. Mandiant and Google Threat Intelligence Group confirmed the exploitation window spans May 27 through June 9, 2026, and have notified over 100 organizations, 68% of which are in US higher education.

**New technical details from Mandiant:**

- **Entry vector:** Exploitation of `/PSEMHUB/` endpoints

- **Staging:** MeshCentral v1.1.59 agents on IPs 142.11.200[.]186–190, masquerading as Azure services via domain `azurenetfiles[.]net`

- **Lateral movement:** Custom bash script (`[victim]_fanout.sh`) using stolen/hardcoded credentials

- **Exfiltration:** Data compressed with `zstd`, sent via SSH to 176.120.22[.]24 (ShinyHunters DLS)

- **Extortion:** `README-IF-YOU-SEE-THIS-YOUVE-BEEN-HACKED.TXT` dropped in WebLogic directories

**Action:** Oracle has released **mitigations only** (patch pending). Disable PSEMHUB service or block external access to `/PSEMHUB/*` and `/PSIGW/HttpListeningConnector`. Perform forensic review of PeopleSoft/WebLogic directories for webshells, unauthorized XML files, and the IOCs above. **University IT teams should treat this as emergency priority.**

---
