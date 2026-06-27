---
title: "🇰🇷 Klue OAuth victims grow, 🤖 AryStinger botnet D-Link, ⚡ FortiBleed GPU cracking, 🎯 Kimsuky LNK campaign, 📦 Steganographic Remcos RAT"
date: 2026-06-22
tags: ["klue","icarus","arystinger","fortibleed","kimsuky","remcos","botnet","supply-chain","apt","brazil","sbom","enisa"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Klue OAuth breach expands to 9+ cybersecurity victims with Icarus leak deadline today. AryStinger botnet compromises 4,000+ D-Link routers. New FortiBleed analysis reveals $350/day GPU cluster cracking 75K+ Fortinet passwords. Kimsuky, Remcos steganographic campaigns, and Brazil Civil Defense attack round out the threat landscape."
---
# Daily Threat Intelligence Digest — June 22, 2026

*14 articles ingested and analyzed. Gaps identified via web search.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Klue OAuth Breach — 9+ Cybersecurity Firms Disclose Impact, Icarus Sets Data Leak Deadline for Today**

The supply chain breach of market intelligence platform Klue continues to widen, with **nine organizations** now publicly acknowledging data theft from their Salesforce instances following the June 11–12 compromise of Klue's OAuth integrations. Cybersecurity firms **HackerOne, Huntress, Jamf, OneTrust, Recorded Future, Snyk, and Tanium** — plus **Insurity** and **Sprout Social** — have confirmed that attackers used compromised legacy credentials at Klue to steal OAuth tokens and query their Salesforce CRMs for business contact data. [[SecurityWeek](https://www.securityweek.com/more-cybersecurity-firms-disclose-impact-from-klue-hack/); [Malware.News/Databreaches](https://malware.news/t/klue-oauth-breach-victim-list-grows-as-icarus-hackers-claim-attack/108097#post_1)]

Klue CEO Jason Smith confirmed CrowdStrike and law enforcement involvement. Salesforce has disabled the Klue integration platform-wide, and **Gong** also disabled its Klue integration, warning that licensed user data (names, business titles, emails) was accessed — though Gong clarified no call recordings or transcripts were compromised.

The **Icarus** extortion group has set **June 22** as the data leak deadline on its Tor leak site, threatening to publish the stolen Salesforce data unless Klue and affected organizations negotiate. This story has been tracked since June 19 — today's delta is the expanded victim list and the active leak deadline.

**Hunting hypothesis:** Revoke and rotate any OAuth tokens issued to Klue or similar third-party Salesforce integrations. Audit Salesforce API access logs for unexpected `/services/data/` queries from IPs 138.226.246.94, 212.86.125.24, 213.111.148.90, 94.154.32.160.

---

**[NEW] AryStinger Botnet Compromises 4,000+ D-Link Routers for Global Proxy Network**

Qianxin XLab has identified **AryStinger**, a previously undocumented malware botnet that has infected over **4,000 outdated D-Link routers** — primarily DIR-850L and DIR-818LW models — converting them into remotely controlled proxy nodes for malicious traffic. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/arystinger-botnet-infected-thousands-of-d-link-routers-worldwide/)]

The malware exploits three known CVEs (CVE-2013-3307, CVE-2016-5681, CVE-2025-11837) affecting end-of-life hardware with no available patches. Infected devices operate as "executors" that receive distributed scanning, proxying, tunneling, and command execution tasks from an attacker-controlled server — splitting massive footprinting operations into parallel chunks across thousands of compromised routers. Additionally, AryStinger can tamper with DNS settings to hijack browsing and quietly monitor all inbound/outbound traffic.

Nearly half of all infections (48.5%) are in **South Korea**, followed by China (31.8%), Sweden (6.4%), Malaysia (3.5%), and Singapore (2.5%). XLab also identified a **Go-based NAS variant** with additional capabilities (IP/DNS scanning, internal network recon via open-source pentesting tools, and support for Shell, Go, Java, and Python source code execution). The NAS variant currently has limited reach but represents a significant capability upgrade. No attribution to any known threat actor cluster.

**Recommended action:** Replace end-of-life D-Link DIR-850L and DIR-818LW routers immediately. If replacement is not possible, disable remote management and apply strict ACLs.

---

**[UPDATE] FortiBleed — Attackers Rented 36-GPU AI Cluster for $350/Day to Crack 75,000+ Fortinet Firewall Passwords at Nation-State Speed**

New analysis from InfoStealers reveals the operational mechanics behind the FortiBleed credential theft campaign with striking detail: the attackers bypassed Fortinet's encryption by renting a **36-GPU cluster on Vast.ai** — a decentralized cloud compute marketplace built for the GenAI industry — at **$14.40/hour (~$350/day)** . [[Malware.News/InfoStealers](https://malware.news/t/nation-state-level-compute-power-from-the-ai-rush-enabled-the-massive-fortibleed-campaign/108096#post_1)]

The cluster, managed entirely through a Telegram bot, achieved:
- **720 billion hashes/second** against legacy Fortinet salted SHA-256 hashes
- **180–360 million hashes/second** against newer PBKDF2-based hashes (designed to resist GPU cracking)

Beyond raw compute, the operators used **AI-assisted coding tools (Cursor)** to write the Telegram bots and management scripts, and **agentic penetration testing frameworks** to automate Active Directory enumeration after cracking credentials. This creates a fully AI-integrated intrusion pipeline: AI-written management code → rented AI GPUs → AI-driven post-exploitation. Initial access broker **SantaAd** was identified selling bulk Fortinet access on Russian-language forums, confirming the IAB-to-ransomware affiliate pipeline these credentials feed into.

The campaign has now been linked to **theft from 86,000+ Fortinet devices** across 194 countries. Kevin Beaumont's analysis highlights the dark irony: the GenAI industry's GPU infrastructure has commoditized nation-state cryptographic attack capability.

**Context:** *Previously covered June 18–21 (initial disclosure, CISA warning, Unit 42 analysis, IAB attribution). New today: full operational mechanics of password cracking infrastructure at $350/day.*

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Kimsuky Deploys LNK-Based Malware Disguised as Personal Data Breach Verification**

North Korean APT group **Kimsuky** continues its social engineering campaigns with a new lure: malicious `.lnk` files disguised as a **personal data breach verification request** themed around customer status data (`2603vvip고객현황.lnk`). The campaign targets Korean enterprise employees through multi-email exchanges that build trust before delivering the payload. [[Malware.News](https://malware.news/t/kimsuky-2603vvip-lnk/108098#post_1)]

This follows Kimsuky's established pattern of using Korean-language corporate-themed lures with multi-stage infection chains. The use of a "data breach verification" pretext is a notable evolution — preying on growing awareness of data breach incidents to lower victim guard.

---

**[NEW] Multi-Stage Steganographic Campaign Delivers Remcos RAT and Diverse Payloads Across Global Targets**

K7 Labs identified an active phishing campaign using a **steganographic .NET loader chain** that delivers **Remcos RAT** as the final payload, with infrastructure also observed dropping Agent Tesla, MassLogger, Phantom Stealer, Dark Cloud, RedLine Stealer, Formbook, and XWorm — suggesting a loader-as-a-service model. [[Malware.News/K7 Labs](https://malware.news/t/a-multi-stage-steganographic-loader-campaign-deploying-diverse-payloads-globally/108101#post_1)]

The infection chain follows: phishing archive → `.com` .NET executable → embedded Bitmap resource (steganography) → Optimax.dll (first-stage loader, memory-only) → System Optimizer Ultimate.dll (second-stage loader) → Remcos RAT via process hollowing. Payload filenames referencing "GST," "NEFT," "RTGS," and "IMPS" (Indian financial systems) confirm **India as a primary targeting region**. The decoy application masquerades as a brick-building game and runs in the background to avoid suspicion. Remcos RAT implements UAC bypass via eventvwr.exe, webcam/audio recording, browser credential theft (Chrome, Firefox), and exfiltration to C2 at `62.102.148.212:37393`.

---

**[NEW] Brazil's Civil Defense Alert Network Suffers Cyberattack**

Brazil's Civil Defense agency reported that its **official emergency alert system** was targeted in a cyberattack on Saturday. The incident is under investigation by Brazilian authorities. While details remain limited, the compromise of a civil alert system carries unique physical safety risks — the same system used to warn populations of natural disasters, severe weather, and public safety emergencies. [[Malware.News/Databreaches](https://malware.news/t/brazil-s-civil-defense-suffers-a-cyberattack-on-its-official-alert-network/108100#post_1); [Databreaches.net](https://databreaches.net/2026/06/21/brazils-civil-defense-suffers-a-cyberattack-on-its-official-alert-network/)]

---

## 🛡️ Defense & Detection

**[UPDATE] ENISA SBOM Part III — Practical CRA Readiness Roadmap to December 2027 Deadline**

ENISA's third and final SBOM adoption report shifts from "why" to "how," publishing an **8-step maturity roadmap** for organizations to achieve Cyber Resilience Act readiness before the December 2027 enforcement deadline. [[SOCFortress](https://socfortress.medium.com/enisa-sbom-adoption-in-2026-from-security-best-practice-to-regulatory-imperative-part-iii-fee435e13fd7)]

The roadmap progresses from foundational SBOM generation to continuous monitoring, developer workflow integration, and extended third-party supply chain visibility — emphasizing that CRA compliance should be a by-product of operational security, not a separate project. Key insight: the gap is no longer in SBOM generation tooling but in **consuming SBOM data for active risk reduction** — a gap that vulnerability assessment platforms and MSSPs will need to fill.

---

**[Industry] BSides San Antonio 2026 — Runtime Secrets, Azure Managed Identity Attacks, and Compliance Outcomes**

GitGuardian's recap of BSides San Antonio 2026 surfaced several operationally relevant talks. Hemanth Gorijala demonstrated that **runtime credentials can leak from production web applications** even when SAST, secret scanning, and CI/CD checks all report clean — the secret appears after build-time injection, lazy chunks, and runtime state. Manuel Melendez (Microsoft) showed that **over-permissioned Azure Managed Identities** on serverless resources (Logic Apps, Function Apps, Automation Accounts) can be abused by attackers with low-level access to request identity tokens for lateral movement. Dustin Cloos made the case that **compliance should prove what you did, not what you could do** — authentication logs beat MFA screenshots. [[GitGuardian](https://blog.gitguardian.com/bsides-satx-2026/)]

---

## ⚡ Quick Hits

- **Texas Parks & Wildlife data breach** — A third-party license vendor compromise exposed **3 million individuals'** driver's license and passport numbers. No SSNs, financial data, or minors' data affected, per TPWD. [[SecurityWeek](https://www.securityweek.com/texas-parks-wildlife-data-breach-affects-3-million-individuals/)]
- **Novo Nordisk breach market analysis** — Despite two independent threat actors demanding $50M and $25M and stealing 1.3TB of pharma data including undisclosed drug programs, the company's stock price remained stable. The article attributes this to investor focus on Novo Nordisk's core GLP-1 drug pipeline rather than data-loss perception. [[Malware.News/Databreaches](https://malware.news/t/two-data-breaches-didn-t-sink-novo-nordisk-s-stock-why-not/108099#post_1)]
