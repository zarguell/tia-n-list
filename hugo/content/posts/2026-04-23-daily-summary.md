---
title: Microsoft Defender zero-days exploited 🛡️, triple supply chain attacks 🔗, DPRK fake IT workers 👤, AI-assisted malware 🤖
date: 2026-04-23
tags: ["zero-day exploitation","supply chain attacks","privilege escalation","north korea apt","credential theft","ai security","patch management","developer security","threat actors","software vulnerabilities"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Actively exploited Microsoft Defender zero-days and a coordinated triple supply chain attack targeting npm, PyPI, and Docker Hub underscore the shrinking window between vulnerability disclosure and weaponization. North Korean threat actors are advancing operations through fake IT worker infiltration schemes and AI-assisted malware campaigns, while critical ASP.NET Core and LMDeploy vulnerabilities demand immediate patching and key rotation to prevent privilege escalation and token forgery.
---
# Daily Threat Intel Digest - April 23, 2026

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] BlueHammer/RedSun Microsoft Defender Zero-Days - CISA Adds to KEV Catalog After Hands-On-Keyboard Attacks Confirmed**

CISA has added CVE-2026-33825 (BlueHammer) to its Known Exploited Vulnerabilities catalog, giving federal agencies until May 7th to patch after Huntress Labs confirmed attackers are actively exploiting the Microsoft Defender privilege escalation flaw in real-world intrusions. The vulnerability allows low-privileged local users to gain SYSTEM permissions, and Huntress observed evidence of "hands-on-keyboard threat actor activity" tied to compromised FortiGate SSL VPN access with infrastructure geolocated to Russia. This follows last week's disclosure that disgruntled researcher "Chaotic Eclipse" leaked proof-of-concept code for three zero-days (BlueHammer, RedSun, and UnDefend) after Microsoft's handling of the disclosure process. Organizations running Windows systems with Microsoft Defender should assume potential exploitation and prioritize patching within the two-week window [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-orders-feds-to-patch-microsoft-defender-flaw-exploited-in-zero-day-attacks/); [Huntress Labs analysis](https://www.bleepingcomputer.com/news/security/recently-leaked-windows-zero-days-now-exploited-in-attacks/)].

**[NEW] Triple Supply Chain Attack Hits npm, PyPI, and Docker Hub in 48-Hour Window**

Three coordinated supply chain attacks struck the developer ecosystem between April 21-23, all designed to steal credentials from CI/CD pipelines and developer environments. TeamPCP compromised Checkmarx KICS Docker Hub images and VS Code extensions with credential-harvesting payloads, while a separate campaign dubbed CanisterSprawl deployed a self-propagating npm worm that recursively compromised packages across ecosystems. A third attack targeted the Xinference PyPI package with a credential stealer. All three campaigns shared the same objective: exfiltrating API keys, cloud credentials, SSH keys, and registry tokens. Organizations using affected packages should check for pinning to compromised versions and rotate any credentials that may have been exposed [[GitGuardian](https://blog.gitguardian.com/three-supply-chain-campaigns-hit-npm-pypi-and-docker-hub-in-48-hours/); [Checkmarx Security Update](https://checkmarx.com/blog/checkmarx-security-update-april-22/); [Socket.dev analysis](https://socket.dev/blog/checkmarx-supply-chain-compromise)].

**[NEW] LMDeploy SSRF Exploited Within 12 Hours of Disclosure**

Attackers exploited a critical Server-Side Request Forgery vulnerability (CVE-2026-33626, CVSS 7.5) in LMDeploy just 12 hours and 31 minutes after the public advisory was published—no proof-of-concept code required. The flaw affects LMDeploy's vision-language module and enables attackers to make arbitrary requests from vulnerable servers. The rapid weaponization demonstrates the collapsing window between disclosure and exploitation and validates the need for pre-patch compensating controls [[GBHackers](https://gbhackers.com/attackers-exploit-lmdeploy-flaw/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical ASP.NET Core Privilege Escalation - CVE-2026-40372 (CVSS 9.1)**

Microsoft released out-of-band emergency patches for CVE-2026-40372, a high-impact ASP.NET Core privilege escalation vulnerability that could allow unauthenticated attackers to forge authentication material and obtain SYSTEM privileges on affected systems. The flaw affects Microsoft.AspNetCore.DataProtection versions 10.0.0 through 10.0.6, specifically on Linux, macOS, and other non-Windows operating systems. Critically, authentication cookies and other signed artifacts issued during the vulnerable period may remain valid **even after patching** unless organizations rotate their Data Protection key ring. Organizations running non-Windows ASP.NET Core deployments should update to version 10.0.7 and schedule immediate key rotation to invalidate any potentially forged tokens [[SOC Prime](https://socprime.com/blog/cve-2026-40372-detection/); [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/new-microsoft-defender-redsun-zero-day-poc-grants-system-privileges/)].

**[NEW] Apple iOS Notification Privacy Flaw - CVE-2026-28950**

Apple released iOS 26.4.2 and iPadOS 26.4.2 emergency updates fixing a notification storage flaw that retained deleted notification content in internal device logs, enabling forensic recovery of private communications. The vulnerability came to light after the FBI successfully extracted deleted Signal messages from a defendant's iPhone through the notification database during a criminal investigation. While the issue affects all app notifications, secure messaging apps like Signal that display message previews in notifications are particularly impacted. Signal users can mitigate exposure by setting Notification content to "Name Only" or "No Name or Content" in the app's settings [[Apple Security Advisory](https://support.apple.com/en-us/127002); [404 Media via Schneier](https://www.schneier.com/blog/archives/2026/04/fbi-extracts-deleted-signal-messages-from-iphone-notification-database.html); [Malwarebytes](https://www.malwarebytes.com/blog/news/2026/04/apple-fixes-ios-bug-that-kept-deleted-notifications-including-chat-previews)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] North Korean Fake IT Worker Infrastructure Exposed**

Research triggered by cryptocurrency investigator ZachXBT uncovered infrastructure and tactics behind North Korean IT worker infiltration schemes, where actors use fake personas to gain employment at global organizations for revenue generation and sanctions evasion. The investigation identified the domain luckyguys[.]site as part of the broader campaign, adding to growing evidence of DPRK's systematic use of fraudulent remote work to access funds and intelligence within target organizations [[GBHackers](https://gbhackers.com/north-korean-fake-it-workers/)].

**[NEW] Lazarus Deploys AI-Assisted Malware Through Backdoored Coding Tests**

North Korea's Lazarus Group is using AI-assisted malware and backdoored coding challenges to steal millions in cryptocurrency from Web3 developers. The group, designated HexagonalRodent by Expel, likely evolved from fraudulent IT worker operations before pivoting to malware-driven theft campaigns. In three months, the operation exfiltrated data from developer environments through malicious coding assessments distributed to job seekers in the crypto space [[GBHackers](https://gbhackers.com/lazarus-lures-developers/)].

**[NEW] Chinese-Language Guarantee Marketplaces Enable Cross-Border Fraud Operations**

A detailed analysis of Dabai Guarantee, a Chinese-language Telegram-based marketplace, reveals how criminal syndicates coordinate large-scale financial fraud operations targeting Japan, South Korea, and other countries. The platform functions as a one-stop shop for money laundering, compromised accounts, SIM cards, and "sweeping teams" that conduct ghost-tapping attacks against retail payment systems. Analysis of Public Group 301 shows organized campaigns purchasing cosmetics and tobacco products through card fraud for resale in secondary markets, demonstrating how traditional money laundering has migrated to decentralized Telegram infrastructure [[Recorded Future](https://www.recordedfuture.com/research/evolution-of-the-chinese-language)].

## 🛡️ Defense & Detection

**[NEW] AI Security Testing Validates Autonomous Attack Capabilities**

Unit 42 research demonstrates that multi-agent AI systems can autonomously chain vulnerabilities to attack cloud environments with minimal human oversight. While the research was conducted in controlled conditions without active defenders, the UK's AI Security Institute independently verified that current frontier models complete expert-level cybersecurity tasks 73% of the time—tasks that were impossible for AI before April 2025. The findings underscore that competency thresholds for sophisticated security work have dropped dramatically, making existing exploit chains faster and cheaper to develop while demanding that defenders adopt agent-based detection and response capabilities to match machine-speed threats [[Unit 42](https://unit42.paloaltonetworks.com/autonomous-ai-cloud-attacks/); [Truesec analysis](https://www.truesec.com/hub/blog/mythos-what-it-actually-means-and-what-it-does-not)].

**[NEW] Roblox Settlement Forces Platform-Wide Age Verification and Chat Restrictions**

Roblox agreed to $35+ million in settlements across multiple US states (Alabama, Nevada, West Virginia) and will implement mandatory age verification for all users starting May 1st. Adults and users under 16 will be prohibited from chatting unless on a "trusted friend" list, and all communications involving minors must remain unencrypted for potential law enforcement access. The settlements address allegations that the platform failed to protect children from predators and misrepresented its safety controls. Starting in June, the platform will split into three tiers with graduated chat restrictions based on age verification [[Malwarebytes](https://www.malwarebytes.com/blog/news/2026/04/roblox-clamps-down-on-chats-and-age-checks-as-legal-pressure-builds)].