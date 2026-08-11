CISA added **CVE-2026-28318** (uncontrolled resource consumption) to its Known Exploited Vulnerabilities catalog on June 5, confirming active exploitation targeting SolarWinds Serv-U file transfer servers. An unauthenticated attacker can crash servers by sending a crafted HTTP POST with `Content-Encoding: deflate` header — no credentials required.

SolarWinds released Serv-U 15.5.4 Hotfix 1 on Thursday. Shodan tracks 12,000+ exposed Serv-U servers; Shadowserver finds ~3,100 (fewer false positives). Administrators who upgraded to 15.5.4 but skipped the hotfix remain vulnerable — a critical gap that patch inventory tools may miss. Federal agencies must remediate by June 19 under BOD 22-01.

**Context:** This is the 11th SolarWinds product vulnerability added to CISA's KEV catalog. The Clop ransomware gang previously exploited Serv-U RCE (CVE-2021-35211) in 2021; Chinese state-sponsored DEV-0322 also weaponized it in zero-day attacks. Block POST requests with `content-encoding` headers at the WAF as a compensating control.

---
