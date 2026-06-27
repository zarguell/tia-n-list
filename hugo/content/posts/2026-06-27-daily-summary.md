---
title: "🚨 Cisco KEV Deadline, Splunk RCE, Russian Signal Hack, Jaguar Land Rover Attribution, Polymarket $3M Attack"
date: 2026-06-27
tags: ["CISA KEV","Cisco","Splunk","RCE","Signal","Russian Intelligence","Jaguar Land Rover","Ransomware","Polymarket","Supply Chain","OpenAI","Phishing","Amazon Q","Metasploit","LiteLLM","ATF","Secret Service","Chrome","Facial Recognition"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA adds Cisco CVE-2026-20230 and PTC Windchill CVE-2026-12569 to KEV with urgent Sunday patching deadline. Splunk Enterprise CVE-2026-20253 (CVSS 9.8) exploited in the wild — unauthenticated RCE via PostgreSQL sidecar. FBI warns Russian intelligence phishing campaign now steals Signal Backup Recovery Keys for full message history access. Russian hackers attributed to $2.5B Jaguar Land Rover ransomware disaster. Polymarket loses $3M in supply-chain attack. Amazon Q Developer vuln (CVSS 8.5) exposes cloud credentials via malicious repositories. Recommended actions: patch Cisco Unified CM, Splunk Enterprise, and LiteLLM immediately; rotate Signal recovery keys; update Amazon Q VS Code extension."
---

# Daily Threat Intelligence Digest — June 27, 2026

*54 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Cisco CVE-2026-20230 — CISA Adds SSRF to KEV With Sunday Patching Deadline for Federal Agencies**

CISA has added CVE-2026-20230, a server-side request forgery vulnerability in Cisco Unified Communications Manager, to its Known Exploited Vulnerabilities catalog, giving federal agencies until Sunday, June 28 to remediate under BOD 26-04. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-sets-urgent-deadline-to-fix-cisco-flaw-exploited-in-attacks/)]

Cisco patched the flaw on June 3 (critical severity, unauthenticated, remote exploitation via crafted HTTP requests) and initially reported no active exploitation. Last week, Defused observed exploitation attempts writing arbitrary files to affected endpoints. The KEV addition confirms CISA now assesses active, ongoing exploitation. CISA also simultaneously added **CVE-2026-12569**, a critical RCE in PTC Windchill and FlexPLM (product lifecycle management systems), to KEV with the same Sunday deadline.

**Context:** *Previously covered June 24 (active exploitation observed, PoC published). New today: CISA KEV addition, formal federal remediation deadline, and simultaneous PTC Windchill KEV addition.*

**Recommended action:** Patch Cisco Unified CM immediately — voice infrastructure is internet-facing. Federal agencies bound by BOD 26-04 must remediate by EOD June 28.

---

**[NEW] Splunk Enterprise CVE-2026-20253 — Critical Unauthenticated RCE (CVSS 9.8) via PostgreSQL Sidecar, KEV Confirmed, Active Exploitation in the Wild**

Splunk disclosed CVE-2026-20253 on June 10 — a critical unauthenticated RCE in Splunk Enterprise (CVSS 9.8) stemming from missing authentication on a PostgreSQL sidecar service recovery endpoint proxied through Splunk Web. [[Malware.News/Zscaler ThreatLabz](https://malware.news/t/critical-unauthenticated-remote-code-execution-in-splunk-enterprise-cve-2026-20253/108248#post_1)]

watchTowr Labs published a PoC and technical deep-dive on June 12. Splunk updated its advisory on June 18 to warn of **active exploitation in the wild**, and CISA added the CVE to KEV the same day. The attack chain progresses from path traversal for arbitrary file creation → connection string injection to attacker-controlled PostgreSQL → credential theft via `.pgpass` file → arbitrary file write → **remote code execution as the Splunk service account**.

**Impact is severe:** Splunk Enterprise is the security telemetry backbone for most organizations. An attacker with code execution can tamper with logs, suppress alerts, harvest credentials from indexed data, establish persistence, and pivot to internal systems. Affected versions: Splunk Enterprise 10.2.x (prior to 10.2.4) and 10.0.x (prior to 10.0.7). Splunk Cloud Platform is not affected (does not use the PostgreSQL sidecar).

**Hunting hypothesis:** Monitor for HTTP POST requests to `/en-US/splunkd/__raw/v1/postgres/recovery/backup` with empty or spoofed `Authorization: Basic` headers from unexpected IPs.

**Recommended action:** Upgrade Splunk Enterprise to fixed versions immediately. As a temporary workaround, disable the PostgreSQL sidecar (`[postgres] disabled = true` in `server.conf`) — this breaks Edge Processor and SPL2 pipelines but preserves core search and dashboard functionality. Remove Splunk Web from direct internet exposure.

---

**[NEW] FBI/CISA: Russian Intelligence Phishing Campaign Evolves to Steal Signal Backup Recovery Keys — Historical Messages at Risk**

The FBI and CISA have updated their joint advisory on a Russian intelligence-linked phishing campaign (UNC5792, UNC4221) targeting Signal users, warning that attackers have evolved beyond account hijacking to stealing **Signal Backup Recovery Keys**, enabling access to victims' full message history. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-russian-hackers-now-target-signal-backup-recovery-keys/)]

The campaign, attributed to Russian Intelligence Services (RIS) including FSB Border Guards, continues to target high-value individuals: current and former US/international government officials, military personnel, journalists, and Ukraine-based personnel. The two-phase attack: (1) phishing messages posing as Signal support trick victims into enabling Signal Secure Backups and generating a recovery key, (2) a follow-up message claiming a "sync issue" prompts victims to copy and paste the key into the conversation. Once obtained, attackers can restore the backup to their own devices and read **all historical messages and group conversations**.

**Critical detail:** Creating a new Signal account with the same phone number **does not invalidate** a stolen recovery key. Users must manually generate a new recovery key in Signal's backup settings. Even then, backups already downloaded remain accessible to attackers.

**Mitigation:** Never share your Signal Backup Recovery Key with anyone. Legitimate Signal support communicates only through official channels and never requests verification codes or recovery keys within the app.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Russian Hackers Attributed to $2.5 Billion Jaguar Land Rover Ransomware Attack — UK Economy Hit at 1950s Production Levels**

Investigators have attributed the ransomware attack on Jaguar Land Rover to Russian hackers, with the Cyber Monitoring Centre estimating the economic impact at **£1.9 billion (~$2.5 billion)**, rippling through more than **5,000 businesses** and dragging car production to levels not seen since 1952. The Bank of England flagged the damage in its economic outlook. [[Malware.News/DataBreaches](https://databreaches.net/2026/06/26/russian-hackers-behind-the-2-5-billion-jaguar-land-rover-cyberattack-investigators-say/)]

The attack's staggering scale — a single ransomware incident affecting a national GDP metric — underscores the systemic risk concentrated in automotive supply chains, where a single manufacturing disruption cascades through thousands of suppliers and dealers.

---

**[NEW] Polymarket Loses $3 Million in Supply-Chain Attack — Customers to Be Fully Reimbursed**

Polymarket, the $9 billion cryptocurrency prediction market, suffered a supply-chain attack after hackers compromised a third-party frontend vendor and injected malicious JavaScript into the platform's official website. The attack tricked users into approving fraudulent transactions, resulting in approximately **$3 million in losses** (~1,893 ETH) from fewer than 15 affected accounts. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/polymarket-customers-lose-3-million-in-supply-chain-attack/)]

Polymarket confirmed its own servers and backend infrastructure were not impacted. Blockchain security firm PeckShield tracked the stolen funds as they were bridged from Polygon to Ethereum. The company has committed to fully reimbursing affected customers.

---

**[NEW] 'Poisoned Tenant' Campaign — Attackers Create Fake OpenAI Organizations to Infiltrate Cybersecurity Firms**

Push Security has identified a novel social engineering campaign dubbed **"Poisoned Tenant"** where threat actors create OpenAI/ChatGPT tenants impersonating legitimate companies and invite employees to join them. The invitations come from OpenAI's legitimate notification address (`noreply@tm.openai.com`), pass email authentication checks, and appear identical to normal ChatGPT workspace invitations. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cybersecurity-firms-targeted-by-fraudulent-openai-organization-invites/)]

The attackers research individual employees, name the organization after the target company, and attach a payment method for legitimacy. Push Security believes the goal is to convince employees to use the fake ChatGPT workspace as if it were a legitimate corporate AI platform — capturing sensitive information submitted in prompts: source code, internal documents, security research, and strategic plans. The campaign currently targets cybersecurity and technology companies.

---

**[NEW] Iranian-Turkish National Arrested in Montenegro for $3.4 Billion Hacking Campaign**

A 39-year-old Iranian-Turkish dual national wanted by the United States for mass hacking attacks causing **$3.4 billion** in damages was arrested in Montenegro. The suspect is sought by the U.S. District Court in New York on multiple hacking-related charges. [[Malware.News/DataBreaches](https://databreaches.net/2026/06/26/iranian-turkish-national-sought-by-us-on-hacking-charges-arrested-in-montenegro/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Amazon Q Developer Flaw (CVE-2026-12957, CVSS 8.5) — Poisoned Repositories Can Steal Cloud Credentials via VS Code Extension**

Wiz Research disclosed two high-severity vulnerabilities in Amazon's AI-powered coding assistant, Amazon Q Developer for VS Code. **CVE-2026-12957** (CVSS 8.5) allows arbitrary code execution and cloud credential theft simply by having a developer open a malicious repository — auto-execution, shell spawning, and environment inheritance combine to expose active AWS session credentials without any visible warning. A second issue, **CVE-2026-12958**, involves symlink handling. AWS has patched both. [[SecurityWeek](https://www.securityweek.com/amazon-q-flaw-enabled-cloud-credential-theft-via-malicious-repositories/); [Wiz Research](https://cryptobriefing.com/amazon-q-developer-credential-theft-flaw/)]

**Recommended action:** Update the Amazon Q Developer VS Code extension to the latest patched version. Treat any unsolicited repository as potentially hostile.

---

**[NEW] Weekly Metasploit Update: Modules for LiteLLM SQLi (CVE-2026-42208, CVSS 9.3), Next.js Auth Bypass, Audiobookshelf, and Dalfox RCE**

This week's Metasploit Framework release adds four new modules targeting vulnerabilities across the AI tooling and web application landscape: [[Rapid7](https://www.rapid7.com/blog/post/pt-weekly-metasploit-update-modules-for-audiobookshelf-litellm-next-js-dalfox-and-more)]

- **LiteLLM Proxy Pre-Auth SQL Injection** (CVE-2026-42208, CVSS 9.3) — on the CISA KEV list. Affects the widely used AI proxy gateway. Pre-authentication, no credentials required.
- **Next.js Middleware Authorization Bypass** (CVE-2025-29927, CVSS 9.1) — affects self-hosted Next.js applications.
- **Audiobookshelf Unauthenticated API Auth Bypass** (CVE-2025-25205) — affects self-hosted audiobook/podcast server versions 2.17.0–2.19.0.
- **Dalfox Deserialization RCE** (CVE-2026-45087) — unauthenticated RCE in Dalfox Server ≤ 2.12.0.

**Recommended action:** Prioritize LiteLLM patching given the CVSS 9.3 score and CISA KEV listing. The Metasploit module availability lowers the exploitation barrier significantly.

---

## 🛡️ Defense & Detection

**[NEW] Malware Steals Chrome Session Cookies via Native Messaging Abuse — MFA Bypass Achieved Through Legitimate Browser Feature**

Researchers at Malwarebytes detailed an active campaign where phishing emails deliver a `.pfd.js` attachment (disguised as a PDF) that deploys a malicious Chrome extension. The extension abuses **Chrome Native Messaging** — a legitimate feature for extension-to-OS communication — to bridge the browser sandbox to the host operating system, executing PowerShell commands and stealing authenticated session cookies. [[Malwarebytes](https://www.malwarebytes.com/blog/news/2026/06/malware-steals-chrome-session-cookies-to-take-over-your-accounts)]

The stolen session cookies enable **MFA bypass**: attackers can access accounts the victim is already logged into without needing passwords or 2FA codes. The extension is installed via Chrome policy settings, making it appear as an administrator-managed deployment. The malware operates as a Windows backdoor with remote command-and-control capabilities.

**IOCs:** Extension ID `gghagmhimhgfeajfdmjkgmmehbokmglg` (masquerading as "Cloud vn105rkj64"), C2 at `ext2[.]info`.

---

## 📋 Policy & Industry News

**[NEW] ATF Cancels Controversial Ad-Tech Geolocation Contract Following Congressional Scrutiny**

The Bureau of Alcohol, Tobacco, Firearms and Explosives canceled its contract with **Penlink's Webloc** — a commercial ad-surveillance tool that purchased location data from the advertising ecosystem to track Americans without a warrant. The cancellation came a month after ATF Director Robert Cekada acknowledged under congressional questioning that the agency had purchased licenses for the tool and conducted **340+ searches**, including **222 tied to active case numbers**. [[CyberScoop](https://cyberscoop.com/atf-cancels-penlink-ad-surveillance-contract/)]

In one instance, the tool was used to get location data for devices associated with a defense contractor at the same time as a suspected arson incident — but the prosecutor and judge expressed "serious discomfort" with warrantless ad-tech surveillance, and ATF ultimately opted for a court-ordered cell tower data request instead. Sen. Ron Wyden called the cancellation "a victory for Americans' constitutional rights" and renewed his push for the Government Surveillance Reform Act.

---

**[NEW] Secret Service Phone Security Lapses Exposed by DHS Inspector General — Personal Devices Used Routinely for Official Business**

A DHS Inspector General report found that Secret Service employees routinely relied on **personal, unsecured phones** for official business — including during domestic and overseas protective assignments — because government-issued devices lacked messaging apps needed to communicate with law enforcement and foreign partners. [[Malware.News/Nextgov](https://malware.news/t/secret-service-phone-security-lapses-put-us-officials-at-risk-watchdog-says/108247#post_1)]

Key findings: 15,000+ calls between personal devices during protective events; 24,000+ text messages between personal and government devices; one employee's phone was never wiped over 8 years and 20 international trips (policy requires wiping within 24 hours of return); government devices lacked mobile threat defense software required by DHS policy. The report specifically connects the phone security gaps to the **July 13, 2024 Butler assassination attempt** — a Secret Service employee used a personal device to receive a photo of the would-be assassin because the government phone couldn't reliably send images.

---

## ⚡ Quick Hits

- **[NEW] Google Chrome Security Update (AV26-634)** — Google released Chrome 149.0.7827.200/201 for Windows/Mac and 149.0.7827.200 for Linux, addressing vulnerabilities in the Stable Channel. [[Canadian Centre for Cyber Security](https://malware.news/t/google-chrome-security-advisory-av26-634/108239#post_1)]

- **[NEW] Meta Testing Facial Recognition for Police and Military** — Meta is prototyping facial recognition features with a Pentagon supplier, according to reporting flagged by Bruce Schneier. ICE has separately expressed interest in deploying FR-equipped eyeglasses for real-time identification. [[Schneier on Security](https://www.schneier.com/blog/archives/2026/06/meta-is-testing-facial-recognition-for-police-and-military.html)]

- **[NEW] Linux Foundation Launches Akrites Open Source Security Project** — The Linux Foundation unveiled Akrites, a new open source security initiative providing tools and channels for reporting, patching, and disclosing open source software vulnerabilities. [[SecurityWeek](https://www.securityweek.com/linux-foundation-unveils-new-open-source-security-project-akrites/)]

- **[NEW] First Circuit Affirms Dismissal of Data Breach Class Action** — The First Circuit upheld dismissal of a putative class action against Bayamón Medical Center, holding that the plaintiff failed to plausibly allege her injuries were traceable to the healthcare provider's 2019 ransomware attack — a significant precedent for Article III standing in data breach litigation. [[DataBreaches.net](https://databreaches.net/2026/06/26/first-circuit-affirms-dismissal-of-data-breach-class-action-for-lack-of-traceable-injury/)]
