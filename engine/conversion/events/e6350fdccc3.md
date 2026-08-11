CISA added **CVE-2026-50751** (CVSS 9.3) to its Known Exploited Vulnerabilities catalog on Monday, ordering Federal Civilian Executive Branch agencies to patch by June 11 under BOD 22-01. The authentication bypass in Check Point Remote Access VPN and Mobile Access deployments (IKEv1-only) has been exploited in zero-day attacks since May 7, with a surge in early June.

Check Point Research confirmed at least one breach has been linked to a **Qilin ransomware affiliate**, with post-compromise activity including ELF payload retrieval from attacker VPS infrastructure (providers: Kaupo Cloud HK, Shock Hosting, Vultr Holdings). The attacks have affected "a few dozen" organizations globally, with VPS regions matching target geography.

While investigating the flaw, Check Point discovered a second vulnerability — **CVE-2026-50752** (CVSS 7.4) — in the same IKEv1 code path enabling man-in-the-middle attacks against site-to-site VPN tunnels. No exploitation observed yet.

**IOCs:** Attacker IPs include 45.77.149.152, 209.182.225.136, 38.60.157.139, 162.33.177.101, 45.76.26.42, 144.208.127.155, 38.54.88.201, 38.54.107.167, 66.42.99.200. MD5 hashes: 52fda5c1b9704544f32ee98d9060e689, 51d39aa39478beeac94f2d12f682ecce.

**Mitigation:** Apply hotfixes immediately — four of the nine affected version branches (R80.20.X, R80.40, R81, R81.10) are End of Support and require migration. Compensating controls: disable legacy remote access client, force IKEv2 only, require machine certificate authentication, enable IPS signatures.

---
