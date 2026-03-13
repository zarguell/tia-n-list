---
title: CrackArmor Linux flaws 🔴, Chrome zero-days, Handala wiper, PlugX APT, supply chain 📦
date: 2026-03-13
tags: ["linux vulnerabilities","zero-day exploits","apt activity","wiper malware","supply chain attack","privilege escalation","iran threat actors","china-nexus apt","browser security","container security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: CrackArmor vulnerabilities expose millions of Linux systems to root privilege escalation while Chrome zero-days enable active remote code execution attacks. Iran-linked Handala expands destructive wiper campaigns against financial targets and a China-nexus actor employs PlugX malware in regional supply chain compromises.
---
# Daily Threat Intel Digest - March 13, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] CrackArmor: Critical AppArmor flaws enable Linux root takeover**
Researchers at Qualys have disclosed "CrackArmor," a set of nine vulnerabilities in the AppArmor Linux Security Module that allow unprivileged local users to escalate privileges to root and break container isolation. Tracked as a confused deputy vulnerability, these flaws affect over 12.6 million Linux systems running distributions where AppArmor is enabled by default, including Ubuntu, Debian, and SUSE. Attackers can manipulate AppArmor profiles via pseudo-files to trigger denial-of-service conditions or execute arbitrary code within the kernel, effectively collapsing the security boundary for containers and cloud environments. Immediate kernel patching is required as the flaw has existed since 2017 [[GBHackers](https://gbhackers.com/critical-crackarmor-vulnerabilities-expose-12-6-million-linux-servers/); [Qualys Blog](https://blog.qualys.com/vulnerabilities-threat-research/2026/03/12/crackarmor-critical-apparmor-flaws-enable-local-privilege-escalation-to-root)].

**[UPDATE] Chrome zero-day exploitation - Skia and V8 flaws confirmed**
Google has released an emergency security update for Chrome (version 146.0.7680.75/76) to address two zero-day vulnerabilities actively exploited in the wild, expanding on the critical browser threat reported yesterday. The flaws are identified as CVE-2026-3909, an out-of-bounds write in the Skia graphics engine, and CVE-2026-3910, an inappropriate implementation in the V8 JavaScript engine. Both vulnerabilities allow for remote code execution. While specific technical details and threat actors remain restricted to allow user adoption, the confirmed active exploitation necessitates immediate patching for all Windows, macOS, and Linux users [[Cyberpress](https://cyberpress.org/two-new-google-chrome-zero-day-vulnerabilities/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/google-fixes-two-new-chrome-zero-days-exploited-in-attacks/); [SecurityWeek](https://www.securityweek.com/chrome-146-update-patches-two-exploited-zero-days/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Handala expands wiper campaign to Verifone**
Following yesterday's report on the destructive wiper attack against Stryker, the Iran-linked Handala group (Void Manticore) has claimed a new intrusion targeting payment processor Verifone on March 11. The group alleges they stole transaction and financial data and caused widespread disruptions. Handala, attributed to Iran's Ministry of Intelligence and Security (MOIS), is increasingly targeting Western critical infrastructure and financial entities using custom wiper malware (BiBi, Hatef, Hamsa). Organizations, especially those with ties to the defense industrial base or payment processing, should heighten monitoring for wiper TTPs and unusual account activity [[SOCRadar](https://malware.news/t/dark-web-profile-handala-hack/104882#post_1); [GBHackers](https://gbhackers.com/iran-linked-handala/)].

**[UPDATE] China-nexus APT uses PlugX in Persian Gulf targeting**
ThreatLabz has observed a China-nexus threat actor, likely linked to Mustang Panda, targeting countries in the Persian Gulf region with a PlugX backdoor variant. This campaign updates yesterday's reporting on APT activity by providing specific technical details: actors are using an Arabic-language document lure depicting Iranian missile strikes on a US base in Bahrain as a social engineering hook. The attack chain employs a Windows shortcut (LNK) to download a malicious CHM file, which then delivers a heavily obfuscated PlugX payload using Control Flow Flattening (CFF) and Mixed Boolean Arithmetic (MBA) [[Zscaler](https://www.zscaler.com/blogs/security-research/china-nexus-threat-actor-targets-persian-gulf-region-plugx)].

**[NEW] OphimCMS supply chain compromise trojanizes jQuery**
Security researchers have identified six malicious packages on the Packagist repository targeting the OphimCMS content management system. The packages (`theme-dy`, `theme-mtyy`, etc.) ship trojanized JavaScript within bundled jQuery libraries rather than the PHP codebase, making detection difficult. The malicious code redirects users to gambling sites, exfiltrates URLs to `userstat.net`, and downloads second-stage scripts from infrastructure linked to the sanctioned FUNNULL technology group. This campaign highlights the risk of supply chain compromise in the PHP ecosystem [[Cyberpress](https://cyberpress.org/packagist-themes-ship-malware/); [GBHackers](https://gbhackers.com/jquery-campaign/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] MediaTek hardware flaw exposes Android PINs to physical attacks**
A critical hardware vulnerability in the MediaTek Dimensity 7300 chipset allows attackers with physical access to extract Android lock screen PINs and decrypt storage in under a minute using Electromagnetic Fault Injection (EMFI). Because the flaw resides in the Boot ROM (EL3 privilege level), it cannot be fully patched via software; vendors can only implement mitigations. This affects millions of Android devices from brands including Realme, Motorola, Oppo, and Nothing. The vulnerability specifically endangers cryptocurrency wallets stored on these devices, as seed phrases can be extracted during the boot process [[Cyberpress](https://cyberpress.org/critical-mediatek-flaw/); [GBHackers](https://gbhackers.com/898-new-critical-mediatek-vulnerability/)].

**[NEW] OpenSSH GSSAPI flaw crashes processes on Linux distros**
A newly discovered vulnerability in OpenSSH (CVE-2026-3497) allows unauthenticated attackers to crash SSH child processes on Linux distributions using the GSSAPI Key Exchange patch, such as Ubuntu and Debian. The flaw stems from an error-handling logic error that calls `sshpkt_disconnect()` instead of `ssh_packet_disconnect()`, leading to the processing of an uninitialized stack variable and subsequent memory corruption. While primarily a denial-of-service vector, it also violates privilege boundaries by leaking heap memory to the root monitor process. Administrators should disable `GSSAPIKeyExchange` if immediate patching is not possible [[Cyberpress](https://cyberpress.org/new-openssh-flaw-in-gssapi-authentication/); [GBHackers](https://gbhackers.com/openssh-gssapi-flaw-can-be-exploited/)].

## 📋 Policy & Industry News

**[NEW] Slack AI auto-enables features, violating change control norms**
Slack has activated AI features for numerous organizations without explicit administrator consent, overriding previously disabled settings. Unlike the July 2025 rollout, which provided advance notice, this March 2026 activation bypassed standard change management processes, potentially violating ISO 42001 controls for AI management systems. Security teams should audit their Slack configurations immediately, document "Auto-enabling of AI features" as a risk, and monitor for unintended data exposure [[Stackaware Blog](https://blog.stackaware.com/p/slack-ai-auto-enable-iso-42001-change-control)].

**[NEW] FBI queries of Americans’ data under FISA 702 rose 35% in 2025**
The FBI conducted 7,413 searches of U.S. person data under Section 702 of the Foreign Intelligence Surveillance Act in November 2025, up from 5,518 in December 2024. The increase comes as the authority nears its April expiration, with the Trump administration pushing for a clean reauthorization. While the "hit rate" for useful information dropped from 38% to 28%, the surge in queries underscores the tension between national surveillance capabilities and civil liberties concerns [[Nextgov/FCW](https://www.nextgov.com/cybersecurity/2026/03/fbi-queries-americans-data-under-fisa-702-rose-35-2025/412103/)].

## ⚡ Quick Hits

- **Starbucks data breach:** Threat actors accessed 889 employee accounts on Starbucks Partner Central via credential harvesting, exposing SSNs and financial details [[BleepingComputer](https://www.bleepingcomputer.com/news/security/starbucks-discloses-data-breach-affecting-hundreds-of-employees/)].
- **Loblaw breach:** Canadian retail giant Loblaw disclosed a breach exposing customer names, phone numbers, and emails, though financial data remains uncompromised [[BleepingComputer](https://www.bleepingcomputer.com/news/security/canadian-retail-giant-loblaw-notifies-customers-of-data-breach/)].
- **England Hockey ransomware:** The AiLock ransomware gang claims to have stolen 129GB of data from England Hockey, including membership and medical information [[BleepingComputer](https://www.bleepingcomputer.com/news/security/england-hockey-investigating-ransomware-data-breach/)].