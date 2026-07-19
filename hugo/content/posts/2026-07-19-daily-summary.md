---
title: "🔴 wp2shell Active Exploitation, ⚠️ 7-Zip RCE Patch, 🎯 ACR Stealer Surge, 📋 CISA BOD 26-04 Deadline Today"
date: 2026-07-19
tags: ["wp2shell","wordpress","CVE-2026-63030","CVE-2026-60137","7-zip","ACR-Stealer","CISA","KEV","SharePoint","FortiSandbox","ClickFix","vulnerability","malware","threat-intelligence"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "wp2shell pre-auth WordPress RCE now has public exploits and confirmed in-the-wild exploitation; CISA BOD 26-04 deadlines for SharePoint and FortiSandbox arrive today; 7-Zip patches critical XZ decompression RCE; Microsoft details ACR Stealer surge via ClickFix delivery chains."
---

# Daily Threat Intelligence Digest — July 19, 2026

5 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking and gap detection.

---

## 🔴 Critical Threats & Active Exploitation

### [UPDATE] wp2shell — Public Exploits Released, In-the-Wild Exploitation Confirmed

*Previously covered July 18 (initial disclosure). New: Public PoC exploits published on GitHub; watchTowr confirms first signs of in-the-wild exploitation; WordPress forces automatic updates.*

The situation with the **wp2shell** pre-authentication RCE chain (CVE-2026-63030 + CVE-2026-60137) has escalated significantly. Multiple public proof-of-concept exploits have been published on GitHub, and security firm watchTowr reports it is "already seeing PoC exploits in circulation" and "beginning to see the first signs of in-the-wild exploitation." WordPress has enabled forced automatic security updates for all supported installations running affected versions (6.9.0–6.9.4, 7.0.0–7.0.1).

The full attack chain: CVE-2026-63030 (REST API batch-route confusion, introduced in WordPress 6.9) is chained with CVE-2026-60137 (SQL injection in `WP_Query`'s `author__not_in` parameter, affecting 6.8+) to achieve unauthenticated RCE on a default WordPress installation with no plugins. Some public PoCs extract password hashes via SQLi and crack an admin password to upload a malicious plugin; others claim pre-auth RCE without credentials.

**Mitigations for unpatched systems:** Block `/wp-json/batch/v1` and `?rest_route=/batch/v1` at WAF level, or install a plugin blocking anonymous REST API access. Cloudflare has deployed WAF rules across all plans (including free) for both CVEs. Searchlight Cyber's wp2shell.com offers a vulnerability checker.

**Action:** This is now an actively exploited, pre-auth RCE affecting ~500 million websites. Patch to WordPress 6.9.5 or 7.0.2 immediately. Verify all internet-facing WordPress installations are updated.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/wordpress-core-wp2shell-rce-flaws-get-public-exploits-patch-now/) · [Searchlight Cyber](https://slcyber.io/research-center/wp2shell-pre-authentication-rce-in-wordpress-core/) · [WordPress Release](https://wordpress.org/news/2026/07/wordpress-7-0-2-release/)

---

### [UPDATE] CISA BOD 26-04 Deadlines Arrive Today — SharePoint, FortiSandbox, SonicWall SMA1000

*Previously covered July 15-18 (SharePoint exploitation cluster, SonicWall SMA1000 zero-days, FortiSandbox KEV additions). New: Today is the federal remediation deadline.*

Today, **July 19, 2026**, is the CISA BOD 26-04 remediation deadline for all agencies across three concurrent KEV entries:

- **CVE-2026-58644** — Microsoft SharePoint Server unauthenticated RCE (CVSS 9.8, deserialization of untrusted data). Exploited as a zero-day before patch availability. Part of the five-CVE active SharePoint exploitation cluster.
- **CVE-2026-25089** and **CVE-2026-39808** — Fortinet FortiSandbox unauthenticated command injection RCE flaws. Exploitation observed June 16 by Defused; patches available since April and June respectively.

The July 17 deadline for SonicWall SMA1000 (CVE-2026-15409 CVSS 10.0, CVE-2026-15410 CVSS 7.2) has already passed.

**Action:** Federal agencies: confirm remediation completion and file BOD 26-04 attestations. Non-federal organizations: if you haven't patched these yet, treat today as the hard deadline. The SharePoint cluster is the most actively exploited of the bunch.

[CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [CISA SharePoint Alert](https://www.cisa.gov/news-events/alerts/2026/07/14/cisa-urges-sharepoint-hardening-after-new-exploitations)

---

## ⚠️ Vulnerabilities & Patches

### [NEW] 7-Zip 26.02 — RCE via Heap-Based Buffer Overflow in XZ Decompression

7-Zip version 26.02 patches a remote code execution vulnerability in its processing of XZ-compressed data. Disclosed by Lunbun researcher Landon Peng and documented by Zero Day Initiative (ZDI-26-444), specially crafted XZ data triggers a heap-based buffer overflow that can allow attackers to execute arbitrary code as the user. The patch adds output buffer boundary checks to prevent the decoder from writing beyond available space.

Exploitation requires user interaction — opening a malicious archive or visiting a page that triggers archive extraction. 7-Zip has no automatic update mechanism; users must manually download version 26.02 from 7-zip.org.

While no active exploitation has been reported at this time, 7-Zip archive vulnerabilities have been weaponized before — in early 2025, a separate 7-Zip flaw was exploited as a zero-day by Russian hackers, and a WinRAR vulnerability (CVE-2025-8088) was used in phishing attacks to deliver RomCom malware.

**Action:** Update to 7-Zip 26.02 manually — the lack of auto-update means vulnerable versions will persist on endpoints indefinitely without proactive IT intervention.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/update-now-7-zip-fixes-rce-flaw-exploitable-with-malicious-archives/) · [ZDI Advisory](https://www.zerodayinitiative.com/advisories/ZDI-26-444/)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] Microsoft Warns of ACR Stealer Surge — ClickFix + WebDAV/MSHTA Delivery Chains Targeting Enterprise

Microsoft has published a detailed threat report on a surge in **ACR Stealer** (MaaS, believed to be a rebranding of Amatera Stealer) attacks against its enterprise customers between late April and mid-June 2026. Two primary intrusion chains are documented:

**Chain 1 — ClickFix + WebDAV:** A ClickFix social-engineering lure executes a command to run a malicious DLL from a remote WebDAV share via rundll32.exe. Attackers use GUID-based directory structures and filenames mimicking legitimate resources. After C2 contact, a heavily obfuscated PowerShell script establishes persistence via scheduled tasks masked as software updates, clears PowerShell history, and injects the payload into a system process for in-memory execution. Some variants use blockchain services as dead-drop resolvers ("EtherHiding") for updated C2 addresses.

**Chain 2 — ClickFix + MSHTA:** ClickFix launches MSHTA to retrieve malicious content, executing an obfuscated PowerShell downloader that extracts an encrypted payload concealed in a steganographic JPEG image and runs it directly in memory.

Targeted data includes browser passwords, cookies, session tokens (Chrome/Edge via DPAPI decryption), PDFs, Microsoft 365 documents, files from Desktop/Downloads, and enterprise-synced OneDrive/SharePoint directories.

**Action:** Block ClickFix delivery vectors — restrict rundll32.exe, mshta.exe, and PowerShell from launching content from remote/user-writeable paths. Microsoft provides IOCs and detailed mitigations in its report.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-warns-of-surge-in-acr-stealer-attacks-on-customers/) · [Microsoft Report](https://www.microsoft.com/en-us/security/blog/2026/07/16/acr-stealer-two-observed-intrusion-chains-amid-increased-threat-activity/)
