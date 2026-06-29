---
title: "💀 cPanel Sorry ransomware mass-exploitation, 🔑 ConsentFix v3 automated Azure OAuth abuse, 🏔️ Everest hits Canadian financial processor Symcor"
date: 2026-05-03
tags: ["cPanel","CVE-2026-41940","ransomware","OAuth","Azure","phishing","Everest","insider-threat"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "The cPanel CVE-2026-41940 authentication bypass has escalated to mass ransomware deployment as the Sorry encryptor actively breaches hundreds of websites, while ConsentFix v3 introduces fully automated OAuth abuse targeting Azure tenants using Pipedream webhooks. Organizations must immediately verify cPanel patching and audit OAuth consent grants."
---
# Tia N. List — Daily Threat Intelligence Digest
### May 3, 2026

**11 articles ingested from Miniflux Cyber feeds across the past 24 hours.**

*Previous 5 days reporting summary:* Yesterday's digest covered cPanel CVE-2026-41940 PoC release (cPanelSniper) with 44,000 compromised IPs scanning, Copy Fail (CVE-2026-31431) added to CISA KEV with Microsoft warning of imminent exploitation, Cordial Spider and Snarky Spider weaponizing AiTM phishing, AccountDumpling Facebook phishing compromising 30,000+ accounts via Google AppSheet, MacSync stealer distributed through 200+ fake Google Ads, Instructure Canvas LMS breach, Five Eyes agentic AI guidance, and former ransomware negotiators sentenced. Earlier this week: SHADOW-EARTH-053 deploying ShadowPad, ConsentFix OAuth phishing, Deep#Door Python backdoor, Unit 42 malicious AI extensions, Hugging Face/ClawHub malware distribution, GitHub Actions supply-chain attack, ProFTPD SQL injection, Qinglong cryptomining exploitation, and SonicWall firewall vulnerabilities.

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] cPanel CVE-2026-41940 escalates to mass ransomware deployment — "Sorry" encryptor breaches hundreds of websites**

The cPanel authentication bypass first disclosed on April 28 has crossed from reconnaissance and exploitation into active ransomware deployment. Attackers are now deploying a Go-based Linux encryptor called "Sorry" ransomware that appends the `.sorry` extension to encrypted files, using ChaCha20 for symmetric encryption with RSA-2048 key protection — making decryption impossible without the attacker's private key. Hundreds of compromised sites are already indexed in Google search results, with victims sharing samples on security forums. Shadowserver's count of 44,000+ compromised IPs (reported yesterday) underscores the massive attack surface being harvested. The ransomware leaves a standardized `README.md` note in each directory with a fixed Tox contact ID, indicating a single campaign operator rather than opportunistic exploitation by multiple groups. All cPanel/WHM users must immediately run `/usr/local/cpanel/scripts/upcp` to install the emergency patch — automatic update channels do not deliver it. Organizations should also audit session directories for indicators of compromise, rotate all credentials, and verify that restored backups predate the February zero-day exploitation window. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/critrical-cpanel-flaw-mass-exploited-in-sorry-ransomware-attacks/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] ConsentFix v3 introduces fully automated Azure OAuth abuse — Pipedream webhooks eliminate manual token theft**

A new variant of the ConsentFix OAuth phishing technique, circulating on hacker forums, automates what was previously a manual social engineering attack into a scalable pipeline targeting Microsoft Azure tenants. The v3 attack chain begins by validating target tenant IDs, then harvesting employee details to craft personalized phishing lures hosted on Cloudflare Pages. The critical innovation is the use of Pipedream (a free serverless integration platform) as a three-in-one automation layer: webhook endpoint to receive the victim's OAuth authorization code, immediate token exchange engine via Microsoft's API, and real-time token collector. Phishing emails embed malicious links inside PDFs hosted on DocSend to bypass spam filters. Captured tokens are then imported into Specter Portal for interactive access to the victim's Microsoft environment — email, files, and any services the token permits. The attack exploits the architectural trust placed in first-party Microsoft apps through the Family of Client IDs (FOCI) mechanism, which shares permissions across Microsoft applications. Push Security researchers confirmed the technique works but note that real-world impact depends on tenant configuration and permissions. Mitigations include token binding to trusted devices, behavioral detection rules, and app-level authentication restrictions. Organizations relying on Microsoft SaaS should audit OAuth consent grants, particularly for first-party apps, and implement conditional access policies that can revoke tokens when risk signals change. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/consentfix-v3-attacks-target-azure-with-automated-oauth-abuse/)]

## ⚠️ Vulnerabilities & Patches

**[NEW] Everest ransomware claims attack on Symcor — major Canadian financial services processor**

The Everest ransomware group has claimed responsibility for a cyberattack against Symcor, one of Canada's largest business process outsourcing companies. Symcor processes financial transactions for major Canadian banks including check clearing, payment processing, and statement rendering — making it a high-value target with potential systemic impact on the Canadian financial sector. The group has threatened to publish the full leak unless Symcor initiates negotiations. Given Symcor's role processing data for multiple financial institutions, a successful breach could expose sensitive customer financial data across the banking sector. This claim has not yet been confirmed by Symcor. [[Malware.News/DeXpose](https://malware.news/t/everest-ransomware-group-strikes-canadian-firm-symcor/106628#post_1)]

## 📋 Policy & Industry News

**[NEW] Maryland pharmacist indicted for unauthorized computer access at University of Maryland Medical Center**

Matthew Bathula, 41, of Clarksville, Maryland, faces federal charges including two counts of unauthorized access to a protected computer and one count of aggravated identity theft stemming from unauthorized access while employed as a pharmacist at the University of Maryland Medical Center. The case highlights the persistent risk of insider threats in healthcare environments, where employees with legitimate system access can exploit their privileges to access sensitive patient data. Healthcare remains the most frequently targeted sector for insider breaches due to the high value of medical records and the broad access granted to clinical staff. [[Malware.News/DataBreaches](https://malware.news/t/maryland-pharmacist-indicted-on-unauthorized-computer-access-related-to-u-maryland-medical-center/106620#post_1)]

## ⚡ Quick Hits

- **Six additional ransomware claims reported** — A wave of ransomware group claims surfaced from DeXpose monitoring: cmdorganization targeted Zampell Ltd (U.S. refractory services) and JG Stewart Construction (Canada), Blackwater hit Grupo EBD (Brazil), AiLock attacked Site Design Group Ltd (U.S. landscape architecture), and Pear Group struck Beyond Measure & Associates (U.S. church design). All follow the standard claim-and-threaten-to-leak pattern with no confirmed data releases at time of reporting. [[Malware.News/DeXpose](https://malware.news/t/cmdorganization-ransomware-attack-on-zampell-ltd/106627#post_1)]

- **Research: "Stressing LLMs" explores binary obfuscation techniques targeting AI-based reverse engineering** — Security researcher Alexander Hanel published a methodology for generating deliberately complex binaries with thousands of interdependent XOR functions and inflated DWARF debug metadata (function names exceeding 7,000 characters) designed to stress-test LLM-based malware analysis pipelines. The techniques explore whether tokenization inflation and computational complexity can degrade static analysis accuracy or exceed context window limits. While theoretical rather than an active threat, the research highlights emerging adversarial considerations as LLMs become embedded in security tooling. [[Malware.News](https://malware.news/t/stressing-llms-triage-stage/106622#post_1)]
