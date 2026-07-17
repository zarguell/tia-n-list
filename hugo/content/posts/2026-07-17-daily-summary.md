---
title: "🥤 Coca-Cola Ransomware, 🇯🇵 Nichirei Cold Chain Hit, 🔴 SharePoint KEV Cluster Grows, 🍎 ClickLock macOS Stealer, 🕷️ Scattered Spider Sentenced"
date: 2026-07-17
tags: ["ransomware","CVE","SharePoint","Fortinet","macOS","Scattered Spider","KEV","supply-chain","CISA","infostealer"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Coca-Cola Fairlife ransomware halts U.S. dairy production; Nichirei cyberattack disrupts Japan's cold-chain logistics including KFC; CISA adds SharePoint RCE zero-day and two Fortinet flaws to KEV with July 19 deadline; ClickLock macOS stealer uses novel process-killing social engineering; Scattered Spider members sentenced to 5.5 years for TfL hack."
---

# Daily Threat Intelligence Digest — July 17, 2026

35 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] Coca-Cola Fairlife — Ransomware Attack Halts U.S. Dairy Production Nationwide

Coca-Cola has disclosed a ransomware attack against its Fairlife dairy subsidiary that has temporarily suspended all Fairlife production across the United States. In an SEC Form 8-K filing, Coca-Cola confirmed unauthorized access to Fairlife's production-related systems and activated incident response and business continuity protocols. Canadian production remains unaffected. The company has notified law enforcement but has not disclosed whether data was stolen, whether extortion demands were received, or which ransomware group is responsible. No group has claimed responsibility at this time.

Fairlife produces ultra-filtered milk products, Core Power protein shakes, and nutrition drinks sold nationwide. The attack on a major food production and cold-chain supply chain represents a significant escalation in ransomware targeting of consumer goods infrastructure.

**Action:** Monitor for ransomware group claims. Organizations in food and beverage supply chains should verify business continuity plans for ransomware scenarios affecting production systems.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/coca-cola-says-fairlife-ransomware-attack-halts-us-dairy-production/) · [SecurityWeek](https://www.securityweek.com/coca-cola-suspends-us-fairlife-production-due-to-ransomware-attack/)

---

### [NEW] Nichirei Cyberattack Disrupts Japan's Largest Cold-Chain Logistics Network, Hits KFC Japan Supply

Japanese frozen food giant Nichirei — one of Japan's top frozen food producers and the country's largest cold-chain logistics operator — confirmed a cyberattack on July 13 that disrupted operations across its network of 80 global subsidiaries. Nichirei Logistics Group, which transports frozen and refrigerated food for approximately 5,000 customers across Japan, experienced system compromises that disrupted food deliveries nationwide. The attack affected logistics operations supporting KFC Japan, forcing temporary service disruptions. Nichirei says it is ready to gradually restore operations.

This is the second major Japanese logistics/transportation cyberattack in two weeks, following the Nihon Kotsu taxi operator shutdown (covered July 14 digest).

**Action:** Japanese supply chain partners should verify Nichirei service continuity and monitor for potential data exposure. The concentration of cold-chain logistics in single operators creates cascading supply chain risk.

[SecurityWeek](https://www.securityweek.com/cyberattack-disrupts-operations-of-japanese-frozen-food-giant-nichirei/) · [The Record](https://therecord.media/cyberattack-japan-nichirei-logistics-impacts-kfc) · [The Cyber Express](https://thecyberexpress.com/nichirei-cyberattack-disrupts-supply-chain/)

---

### [UPDATE] CISA Adds CVE-2026-58644 SharePoint RCE Zero-Day and Two Fortinet FortiSandbox Flaws to KEV

*Previously covered July 15-16 (SharePoint exploitation cluster). New: CISA adds CVE-2026-58644 to KEV with July 19 federal deadline; two additional Fortinet FortiSandbox flaws added to KEV.*

CISA has added **CVE-2026-58644** (CVSS 9.8) — a critical deserialization of untrusted data vulnerability in Microsoft SharePoint Server — to the Known Exploited Vulnerabilities catalog with a July 19 federal remediation deadline. Microsoft has confirmed the vulnerability was exploited as a zero-day prior to patches becoming available on July 14. An attacker authenticated as at least a Site Owner can achieve repeatable remote code execution with low attack complexity.

CISA also added two actively exploited Fortinet FortiSandbox vulnerabilities — **CVE-2026-25089** and **CVE-2026-39808** — to KEV with the same July 19 deadline. Both are critical command injection flaws allowing unauthenticated remote code execution. Fortinet patched CVE-2026-39808 on April 14 and CVE-2026-25089 on June 9, but threat intelligence firm Defused first observed exploitation on June 16.

This brings the total SharePoint exploitation cluster to five CVEs, with four now on KEV and all requiring the same urgent patching cycle.

**Action:** Federal agencies have a July 19 deadline for SharePoint, FortiSandbox, and SonicWall SMA1000 patches — an unusual concentration of simultaneous BOD 26-04 deadlines. Prioritize all three immediately.

[The Hacker News](https://thehackernews.com/2026/07/cisa-adds-exploited-sharepoint-rce-zero.html) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-warns-feds-to-patch-exploited-fortinet-fortisandbox-flaws-by-sunday/) · [CISA Alert](https://www.cisa.gov/news-events/alerts/2026/07/16/cisa-adds-three-known-exploited-vulnerabilities-catalog)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] ClickLock macOS Stealer — Process-Killing Social Engineering Forces Password Disclosure, 100+ Systems Infected

Group-IB has analyzed **ClickLock**, a new macOS information-stealing malware delivered via ClickFix lures that terminates all visible system processes to force users into entering their login password. The malware has infected at least 100 systems across 33 countries since May 2026 and remained undetected by all VirusTotal scanners at time of analysis.

ClickLock uses two coercion mechanisms: a fake macOS password dialog (running a 210ms termination loop for 83 hours until the user complies), and a separate mechanism requesting Keychain authorization for Chrome's Safe Storage key (running a 200ms loop for 35 days). Data harvested includes credentials from eight browsers, cryptocurrency wallets and extensions, password-manager data, shell histories, and system information — all exfiltrated via Telegram Bot API with retry logic and file splitting for large payloads. A modified GSocket backdoor provides persistent remote access through multiple persistence mechanisms.

**Action:** Detect via osascript launching password dialogs, repeated process termination, mass browser profile access, and outbound Telegram API connections. Users should force shutdown via power button and boot to Safe Mode if prompted for passwords while the system appears unresponsive.

[BleepingComputer / Group-IB](https://www.bleepingcomputer.com/news/security/new-clicklock-macos-malware-traps-users-into-revealing-login-password/) · [SecurityWeek](https://www.securityweek.com/clicklock-stealer-bypasses-macos-security-with-social-engineering-process-killing/)

---

### [NEW] OkoBot Framework — 20-Payload Modular Stealer Delivered via ClickFix and Fake GitHub Repos

Kaspersky has documented **OkoBot**, a malicious framework delivering more than 20 payloads focused on stealing cryptocurrency wallet seed phrases, credentials, and browser data. The framework reaches victims through ClickFix attacks and malicious GitHub repositories — one impersonating SQL Server Management Studio but dropping a trojanized Audacity installer. OkoBot evolved from the TookPS campaign (running since March 2025) with a completely redesigned infection chain.

Notable modules include: an injector that installs hidden malicious Chrome extensions (Rilide), **SeedHunter** (injects into Trezor Suite/Ledger Wallet to display fake seed recovery screens), **MC Keylogger** (clipboard monitoring, USB detection, screenshots every 5 minutes), and **OkoSpyware** (FFmpeg-based video recording of 100 monitored applications). Geoblocking of payload delivery excludes Russia/CIS. Majority of victims are in Brazil, Vietnam, Canada, Mexico, and Turkey.

**Action:** Audit GitHub repositories before cloning. Monitor for SeedHunter's fake recovery screen behavior in Trezor Suite and Ledger Live. OkoBot's modular architecture and ClickFix delivery vector indicate a maturing operation.

[BleepingComputer / Kaspersky](https://www.bleepingcomputer.com/news/security/new-okobot-framework-deploys-20-payloads-to-steal-data-crypto/)

---

### [NEW] Scattered Spider Members Sentenced to 5.5 Years for Transport for London Attack

Two leading members of the Scattered Spider cybercrime collective — Thalha Jubair (20) and Owen Flowers (18) — were sentenced to five years and six months in prison each for hacking Transport for London (TfL) in August 2024. The attack disrupted internal systems and online services affecting 8.4 million Londoners, including Dial-a-Ride, concessionary travel cards, digital payments, and contactless ticketing. 148 systems became inoperable and all 27,000 TfL employees had to reset passwords in person. TfL reported £29 million in losses; officials estimated the UK economy could have lost up to £56 billion had the transport network been fully shut down.

At the time of arrest, Flowers' devices contained evidence of ongoing intrusion attempts against U.S. healthcare companies Sutter Health and SSM Health Care Corporation. The U.S. DOJ has also charged Jubair for conspiracy relating to at least 120 network breaches with over $115 million extorted globally. NCA Deputy Director Paul Foster described Scattered Spider as "the most significant cybercrime threat to the UK in recent years."

[BleepingComputer](https://www.bleepingcomputer.com/news/security/scattered-spider-members-behind-transport-for-london-hack-get-five-years-in-prison/) · [SecurityWeek](https://www.securityweek.com/two-scattered-spider-hackers-sentenced-to-jail-in-uk/)

---

## ⚠️ Vulnerabilities & Patches

### [UPDATE] Microsoft SharePoint Exploitation — Fourth KEV Entry, Tenable Confirms Five-CVE Active Exploitation Cluster

*Previously covered July 14-16. New: CISA adds CVE-2026-58644 to KEV; Tenable publishes comprehensive FAQ confirming four actively exploited CVEs with a fifth (CVE-2026-58644) newly confirmed exploited; post-exploitation activity includes IIS machine key theft and malware deployment.*

Tenable's Research Special Operations team has published a comprehensive FAQ on the SharePoint exploitation cluster, confirming that attackers are chaining multiple vulnerabilities for unauthorized access, RCE, IIS machine key theft, and malware persistence. The five CVEs form a layered attack surface: CVE-2026-32201 (spoofing, CVSS 6.5) for initial access, CVE-2026-45659 (RCE, CVSS 8.8) for code execution, CVE-2026-56164 (EoP, CVSS 9.8 per NVD) for privilege escalation, CVE-2026-55040 (auth bypass, CVSS 9.1) as a chain enabler, and CVE-2026-58644 (RCE, CVSS 9.8) for authenticated code execution.

Microsoft and CISA have published AMSI and Defender Antivirus detection signatures for three of the actively exploited flaws. CISA recommends scanning for machine key harvesting artifacts before rotating IIS machine keys.

**Action:** This is now a four-CVE KEV cluster with active exploitation confirmed across all on-premises SharePoint versions. SharePoint 2016/2019 reached end of extended support on July 14 — no ESU available. Enable AMSI Full Mode, restrict internet exposure, and audit for the published detection signatures.

[Tenable FAQ](https://www.tenable.com/blog/cve-2026-32201-cve-2026-45659-cve-2026-56164-faq-sharepoint-server-exploitation) · [CISA Hardening Alert](https://www.cisa.gov/news-events/alerts/2026/07/14/cisa-urges-sharepoint-hardening-after-new-exploitations)

---

### [UPDATE] Claude for Chrome — Manifold Security Confirms Flaw Still Exploitable in v1.0.80

*Previously covered July 15 (initial disclosure via SecurityWeek). New: BleepingComputer publishes detailed technical analysis confirming the synthetic click vulnerability remains unpatched in the latest version.*

Manifold Security researcher Ax Sharma has published a detailed analysis confirming the Claude for Chrome vulnerability remains reproducible in v1.0.80 (released July 7). The extension accepts JavaScript-generated click events without verifying `Event.isTrusted`, allowing any malicious extension with DOM access to claude.ai to trigger nine predefined workflows — including reading Gmail, Google Docs comments, Google Calendar, and modifying Salesforce leads. In "Act without asking" mode, workflows execute silently. Anthropic acknowledged the report as a duplicate of a broader issue but the code remains unchanged.

**Action:** Disable "Act without asking" mode. Audit browser extensions with claude.ai DOM access. This is the third Claude for Chrome trust boundary issue.

[BleepingComputer / Manifold Security](https://www.bleepingcomputer.com/news/security/claude-chrome-extension-flaw-lets-malicious-extensions-trigger-ai-actions/)

---

## 🛡️ Defense & Detection

### [NEW] Unit 42 2026 Global Incident Response Report — AI as Attacker Force Multiplier, Not New Attack Class

Unit 42's 2026 Global Incident Response Report, drawing on hundreds of engagements, concludes that AI is acting as a force multiplier for attackers — compressing attack lifecycles from days to hours — but has not yet introduced fundamentally new attack vectors. Threat actors continue relying on credential theft, phishing, known vulnerability exploitation, and ransomware. However, initial signals of AI-enabled tradecraft are emerging: agentic ransomware managing multiple extortion stages, malware calling out to LLM/MCP servers for C2 instructions, and token jacking of cloud AI service credentials generating millions in unauthorized compute charges.

Key insight: organizations relying primarily on detect-and-respond models may struggle as AI enables faster attacks at greater scale, reinforcing the need for prevention-first controls.

[Unit 42](https://unit42.paloaltonetworks.com/ai-incident-response-report/)

---

## 📋 Policy & Industry News

### [UPDATE] Russian Bulletproof Hosting Operators — U.S. Indictment Unsealed Against Media Land and ML.Cloud

*Previously covered July 15 (initial charges). New: Federal indictment unsealed with full operational details — $62M in damages across 21 states and multiple countries.*

The 2024 indictment unsealed Tuesday charges three Russian nationals — Alexander Volosovik (43, owner of Media Land), Yulia Pankova (29, owner of ML.Cloud), and Kirill Zatolokin (34) — with conspiracy to commit computer fraud, wire fraud, and money laundering. The St. Petersburg-based operation provided infrastructure supporting malware delivery, C2 operations, phishing, DDoS, and ransomware attacks against critical infrastructure in 21 U.S. states plus Australia, EU, UAE, Canada, and UK. The State Department is offering a $10 million reward. The operation was investigated since 2019.

[CyberScoop](https://cyberscoop.com/russian-nationals-medialand-mlcloud-indicted-bulletproof-hosting/)

---

### [NEW] 23andMe to Pay $18 Million in Multi-State Genetics Data Breach Settlement

23andMe (now Chrome Holding Co.) has agreed to pay $18 million to settle claims from 43 attorneys general following the 2023 credential-stuffing attack that went unnoticed for five months and stole data from 6.9 million customers, including genetic ancestry information. The multistate investigation found 23andMe lacked basic safeguards — no password blocklisting, no MFA, inadequate rate limiting, no breach-detection monitoring, and failure to address unusual login activity. The company initially denied the breach, then blamed customers. This follows a separate $30M class-action settlement, a £2.31M UK ICO fine, and the company's Chapter 11 bankruptcy filing in March 2025.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/23andme-to-pay-18-million-in-new-genetics-data-breach-settlement/)

---

## ⚡ Quick Hits

- **Rapid7 sunsets public AttackerKB platform** — The standalone vulnerability intelligence site will retire on August 18. Technical write-ups will continue on the Rapid7 blog; community contributions and public API will be retired. [Rapid7](https://www.rapid7.com/blog/post/ve-sunsetting-public-attackerkb-platform)

- **U.S. charges two Chinese nationals for laundering $43M from investment fraud** — Zhuoying Chen (27) and Haojie Zhang (38) allegedly managed a Queens/Brooklyn network using 140 bank accounts across 45 shell companies to launder investment scam proceeds. [BleepingComputer](https://www.bleepingcomputer.com/news/security/us-charges-two-over-laundering-43-million-from-investment-fraud/)

- **Federal Rotational Cyber Workforce program effectively shuttered** — A GAO report found only 8 of 634 applicants participated across 13 agencies since 2022. OPM cited "budgetary constraints" and will not advertise positions in 2026. The program officially ends next summer. [CyberScoop](https://cyberscoop.com/opm-federal-rotational-cyber-workforce-program-gao/)

- **Windows 11 24H2 Home/Pro and Windows Server 2022 reach end of support in 90 days** — October 13, 2026 deadline for mainstream support. Windows 10 Enterprise LTSB 2016 also ends updates. Enterprise and Education editions continue until October 2027. [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/windows-11-24h2-home-and-pro-reach-end-of-support-in-90-days/) · [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/windows-server-2022-reach-end-of-mainstream-support-in-90-days/)
