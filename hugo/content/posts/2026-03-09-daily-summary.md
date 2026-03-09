---
title: Hikvision exploit 🔓, Apple zero-days 🍎, China-linked APT 🇨🇳, AI app phishing 🤖, prompt injection attacks 💉
date: 2026-03-09
tags: ["iot vulnerabilities","zero-day exploits","apt activity","mobile security","ai security","phishing","prompt injection","surveillance security","identity management","critical infrastructure"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: China-linked UAT-9244 compromises South American telecoms while attackers actively exploit critical Hikvision surveillance flaws and Apple zero-days across multiple platforms. Fraudulent AI applications deliver Facebook phishing campaigns and prompt injection attacks weaponize AI systems against enterprises, undermining security assumptions in automated workflows.
---

# Daily Threat Intel Digest - 2026-03-09

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical Hikvision CVE-2017-7921 actively exploited after CISA KEV addition**  
Attackers are actively exploiting a 2017 authentication bypass vulnerability in Hikvision surveillance cameras and NVRs, enabling full device compromise and lateral network movement. CISA added the flaw to its Known Exploited Vulnerabilities catalog on March 5, 2026, mandating federal agency patches by March 26 and urging private sector action. Successful exploitation grants attackers live video access, recording downloads, and configuration manipulation—potentially compromising both physical and digital security [[Cyberpress](https://cyberpress.org/multiple-hikvision-product-vulnerabilities/); [GBHackers](https://gbhackers.com/hikvision-multiple-product-vulnerability/)].  

**[NEW] Apple platforms hit by trio of actively exploited zero-days**  
CISA confirmed active exploitation of three Apple vulnerabilities across iOS, iPadOS, macOS, and Safari: CVE-2023-43000 (Use-After-Free via malicious web content), CVE-2021-30952 (integer overflow for arbitrary code execution), and CVE-2023-41974 (UAF in malicious apps enabling kernel privileges). Federal agencies must patch by March 26, 2026, as these flaws facilitate device compromise without user interaction in some cases [[Cyberpress](https://cyberpress.org/hackers-exploit-macos-and-ios-vulnerabilities/); [GBHackers](https://gbhackers.com/cisa-alerts-users-vulnerabilities-impacting-macos-and-ios/)].  

**[NEW] Critical ExifTool CVE-2026-3102 enables macOS RCE via malicious images**  
Attackers can execute arbitrary code on macOS systems by embedding shell commands in image metadata processed by vulnerable ExifTool versions using the `-n` flag. Kaspersky’s GReAT warns that automated workflows in forensics and journalism silently process such files, allowing stealthy payload delivery. Users should verify ExifTool integrations and update immediately, as the vulnerability undermines macOS security assumptions [[Cyberpress](https://cyberpress.org/exiftool-vulnerability/); [GBHackers](https://gbhackers.com/critical-exiftool-vulnerability/)].  

**[NEW] Nginx UI flaw (CVE-2026-27944) exposes full system backups**  
Unauthenticated attackers can download and decrypt complete Nginx UI system backups containing user credentials, session tokens, and SSL private keys due to a critical flaw with CVSS 9.8. The vulnerability exposes highly sensitive data, enabling full system compromise if exploited [[GBHackers](https://gbhackers.com/nginx-ui-vulnerabilities/)].  

## 🎯 Threat Actor Activity & Campaigns  

**[NEW] China-linked UAT-9244 targets South American telecoms with novel malware**  
Cisco Talos attributes UAT-9244 to China-aligned Famous Sparrow, detailing its deployment of three malware families: TernDoor (Windows backdoor via DLL side-loading), PeerTime (Linux P2P backdoor using BitTorrent C2), and BruteEntry (Go-based scanner for brute-forcing external services). The campaign leverages compromised telecom infrastructure as operational relay boxes for broader attacks, evidenced by Simplified Chinese debug strings [[Cyberpress](https://cyberpress.org/china-targets-telecoms-again/)].  

**[NEW] Fraudulent AI apps deliver Facebook phishing on iOS**  
Attackers distribute fake ChatGPT and Gemini-branded iOS apps via the App Store to harvest Facebook credentials from business users. The phishing scheme targets advertisers and marketers, promising ad management tools but instead delivering credential-stealing interfaces. Malicious apps identified include "GeminiAI Advertising" (ID: 6759005662) and "Ads GPT" (ID: 6759514534), exploiting trusted app store distribution [[Cyberpress](https://cyberpress.org/fake-ai-apps-phish/)].  

## ⚠️ Vulnerabilities & Patches  

**[NEW] ZITADEL identity platform vulnerable to 1-click XSS (CVE-2026-29191)**  
A critical Cross-Site Scripting flaw in ZITADEL’s `/saml-post` endpoint enables unauthenticated attackers to execute malicious JavaScript via crafted links. The vulnerability, rated Critical severity, could allow full system takeover by compromising identity and access management workflows [[GBHackers](https://gbhackers.com/1-click-zitadel-vulnerability/)].  

**[UPDATE] Indirect prompt injection attacks weaponize AI agents against enterprises**  
Real-world attacks now exploit indirect prompt injection (IDPI) to manipulate AI-based systems, including a December 2025 incident where attackers bypassed an ad review AI to approve scam military glasses advertisements. Obfuscation techniques (CSS hiding, dynamic JavaScript) enable silent malicious instruction execution, requiring defenders to adopt advanced prompt-intent analysis tools like Prisma AIRS [[Cyberpress](https://cyberpress.org/hackers-exploit-ai-injection/)].  

## 📋 Policy & Industry News  

**[NEW] EU court adviser mandates immediate phishing refunds from banks**  
Advocate General Athanasios Rantos ruled that banks must refund unauthorized transaction victims immediately unless fraud is suspected, citing the EU Payment Services Directive (PSD2). Banks can later seek recovery if customer negligence is proven, shifting liability burdens and impacting incident response practices [[BleepingComputer](https://www.bleepingcomputer.com/news/legal/eu-court-adviser-says-banks-must-immediately-refund-phishing-victims/)].  

**[NEW] Trump administration releases high-level cybercrime strategy**  
The White House unveiled a national cybersecurity strategy emphasizing offensive tactics against attackers, AI integration, and critical infrastructure protection. The framework lacks implementation details but signals increased federal focus on disrupting cybercrime ecosystems [[Security Boulevard](https://securityboulevard.com/2026/03/trump-administration-lays-out-a-high-level-strategy-to-combat-cybercrime/)].