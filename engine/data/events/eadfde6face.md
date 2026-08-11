*Previously covered July 8. New: SecurityWeek coverage provides additional detail on the Leash malware family evolution and SOHO router compromise scale.*

Cisco Talos's continued analysis of the China-linked APT cluster UAT-7810 (LapDogs campaign) documents the evolution from SHORTLEASH to an expanded toolkit: LONGLEASH (upgraded reverse shell with HTTP/DNS/SOCKS/TCP/ICMP/UDP proxying and TLS/PKI), DOGLEASH (lightweight Linux backdoor via web shells), and JARLEASH (Java-based FTP/SFTP/Netcat tool). The campaign has compromised over 1,000 SOHO routers to build an Operational Relay Box (ORB) network used as proxy infrastructure by other China-aligned APTs. The group exploits known n-day vulnerabilities in Ruckus and ASUS routers.

**Recommended action:** Patch all internet-facing Ruckus and ASUS routers against CVE-2020-22653, CVE-2020-22658, CVE-2023-25717, and CVE-2025-2492. Monitor for anomalous proxy connections from edge network devices.

---
