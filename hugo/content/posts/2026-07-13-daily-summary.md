---
title: "Joomla Zero-Day RCE, ShareFile Emergency Shutdown, RedHook ADB Abuse"
date: 2026-07-13
tags: ["joomla","cisa-kev","sharefile","progress-software","android-malware","redhook","wireless-adb","secrets-scanning","cisa","zero-day","rce"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Two CVSS 10 Joomla extension flaws exploited as zero-days and added to CISA KEV; Progress Software forces emergency ShareFile Storage Zone Controller shutdown over credible threat; RedHook Android malware gains shell access via novel Wireless ADB abuse."
---

# Daily Threat Intelligence Digest — July 13, 2026

8 articles ingested and analyzed from curated cyber intelligence feeds.

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] Two CVSS 10 Joomla Extensions Under Active Zero-Day Exploitation, Added to CISA KEV

Two Joomla extensions — **Balbooa Forms** (CVE-2026-56291) and **iCagenda** (CVE-2026-48939) — both carry CVSS 10.0 scores for unauthenticated arbitrary file upload vulnerabilities enabling remote code execution. Both were exploited as zero-days before patches were available, and CISA added them to the Known Exploited Vulnerabilities catalog on July 10 with a 3-day remediation deadline under BOD 26-04.

- **Balbooa Forms** (CVE-2026-56291): Affects versions ≤2.4.0. Exploits the frontend attachment upload endpoint to upload PHP webshells. Patched in v2.4.1 (July 9), but threat actors exploited it in the wild prior to the patch.
- **iCagenda** (CVE-2026-48939): Affects file attachment feature. Developer JoomliC observed in-the-wild exploitation on June 15. Patched in v4.0.8 and v3.9.15 (June 15–16).

**Action:** Audit any Joomla deployments for these extensions immediately. If present, update to patched versions now — both flaws require no authentication to exploit.

[SkyBox / SecurityWeek](https://www.securityweek.com/organizations-warned-of-exploited-joomla-extension-vulnerabilities/) · [The Hacker News](https://thehackernews.com/2026/07/icagenda-and-balbooa-forms-joomla-flaws.html)

### [NEW] Progress Software Forces ShareFile Storage Zone Controller Shutdown Over Credible Threat

Progress Software has disabled ShareFile account access via Storage Zone Controllers and is urging all customers to **manually shut down the servers hosting their Storage Zone Controllers** while the company investigates a "credible external security threat." Progress claims no unauthorized access to customer data has been confirmed at this time.

Users speculate the threat may relate to two vulnerabilities patched in March — **CVE-2026-2699** (CVSS 9.8) and **CVE-2026-2701** (CVSS 9.1) — which can be chained to achieve unauthenticated RCE via configuration changes and malicious file uploads.

**Action:** If your organization runs ShareFile Storage Zone Controllers, follow Progress's guidance and shut them down immediately. Review network logs for signs of exploitation targeting the March 2026 flaws.

[SecurityWeek](https://www.securityweek.com/progress-prompts-sharefile-storage-zone-controller-shutdown-amid-security-concerns/)

---

## ⚠️ Vulnerabilities & Patches

*(No additional CVE items beyond the critical section today.)*

---

## 🛡️ Defense & Detection

### [NEW] RedHook Android Malware Evolves: Wireless ADB Abuse Enables No-Root Shell Access

A new variant of the **RedHook** Android RAT (analyzed by Group-IB) introduces a novel privilege escalation technique: it abuses Android's Wireless Debugging (Wireless ADB) mechanism to gain shell-level (UID 2000) privileges without requiring a rooted device or a computer connection.

**Attack chain:** The malware tricks the victim into granting Accessibility permissions → automatically enables Developer Options and Wireless Debugging → retrieves the pairing code from screen → connects to the local ADB daemon via loopback (127.0.0.1) → deploys a Shizuku-based framework to execute privileged commands, install/uninstall apps, capture screens, and steal credentials.

The malware supports 53 server-issued commands, uses multiple persistence mechanisms (WakeLocks, mutual service restarts, watchdog alarms), and is distributed via social engineering impersonating government agencies and financial institutions.

**Detection heuristic:** Monitor Android devices for unexpected Wireless ADB activation (Settings → Developer Options → Wireless Debugging enabled without user intent) and Accessibility service connections to unknown packages. Shell process spawning from apps without ADB authorization is a strong signal.

[BleepingComputer / Group-IB](https://www.bleepingcomputer.com/news/security/redhook-android-malware-now-uses-wireless-adb-for-shell-access/)

### [NEW] CISA Publishes Post-Mortem of Its Own GitHub Leak — Six Lessons for Every Security Team

CISA published a formal lessons-learned document following the May 2026 incident where 844 MB of sensitive data was found in a public GitHub repository (reported by GitGuardian, taken down in 26 hours). GitGuardian's researcher distilled six actionable takeaways:

1. **Take external vulnerability reports seriously** — CISA's initial notification path was convoluted (CERT/CC, personal contacts, journalist), costing response time.
2. **Scan repositories continuously** — The exposed repo sat public for six months; continuous monitoring caught it.
3. **Build a dedicated secrets-leak playbook** — CISA had no GitHub/cloud incident playbook and lost time building one during the incident.
4. **Simplify reporting channels** — The researcher filed through multiple channels before reaching the right team.
5. **Consolidate development environments** — Unmanaged tooling (personal GitHub accounts, contractor laptops, ad hoc scripts) created the blind spot.
6. **Test credential rotation readiness** — Key rotation took longer than expected due to system complexity.

**Key takeaway:** This is the first known instance of a national cybersecurity agency publicly advocating for secrets scanning and transparency. The postmortem itself is the most valuable artifact — most organizations bury these incidents.

[GitGuardian Blog](https://blog.gitguardian.com/cisa-github-leak-incident-response-lessons/)
