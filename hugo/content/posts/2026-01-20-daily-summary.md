---
title: AVEVA RCE flaws 🏭, WhisperPair Bluetooth attacks 📱, VoidLink AI malware 🤖, ransomware multi-sector targeting 💣, Discord C2 abuse 💬
date: 2026-01-20
tags: ["industrial control systems","bluetooth vulnerabilities","ai-generated malware","ransomware","healthcare","aviation","infostealer","malvertising","command and control","critical infrastructure"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical AVEVA vulnerabilities and WhisperPair attacks demonstrate widespread exploitation of industrial systems and consumer devices, while VoidLink marks the emergence of AI-generated malware frameworks that democratize sophisticated attacks. Ransomware gangs continue targeting healthcare and aviation sectors with double-extortion tactics, while threat actors increasingly abuse legitimate platforms like Discord for command and control operations.
---

# Daily Threat Intel Digest - 2026-01-20

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical AVEVA RCE Flaws Allow Unauthenticated SYSTEM-Level Compromise**  
Seven critical vulnerabilities in AVEVA Process Optimization enable unauthenticated remote code execution with SYSTEM privileges across all versions through 2024.1. The most severe flaw (CVE-2025-61937, CVSS 10.0) exploits the "taoimr" service's API without authentication, allowing complete compromise of industrial control systems. Three additional CVEs (all CVSS 9.3) enable code injection, SQL injection, and DLL hijacking, while high-severity flaws facilitate privilege escalation via project file manipulation. Industrial organizations must upgrade to version 2025+ immediately or implement strict network segmentation and access controls on ports 8888/8889 [[Cyberpress](https://cyberpress.org/critical-aveva-software-vulnerabilities/)].

**[NEW] WhisperPair Attack Hijacks Millions of Bluetooth Devices Without Consent**  
A critical implementation flaw in Google's Fast Pair technology (CVE-2025-36911, CVSS 9.8) allows attackers to forcibly pair vulnerable audio accessories within 14 meters in seconds. Attackers exploit failed manufacturer enforcement of pairing-mode checks to gain complete control, enabling audio playback, eavesdropping, and persistent tracking via Google's Find Hub network. Over 100 affected device models passed certification despite the flaw; patches are available but adoption varies. Users should disable Bluetooth when unused and monitor for unexpected pairing notifications [[Cyberpress](https://cyberpress.org/whisperpair-attack-hijacks-laptops-and-earbuds-via-forced-bluetooth-pairing/); [GBHackers](https://gbhackers.com/whisperpair-vulnerability-pair-devices/)].

**[NEW] VoidLink Malware Marks Dawn of AI-Generated Offensive Capabilities**  
Check Point Research documented the first advanced malware framework built almost entirely by AI under single-actor direction. VoidLink leverages "Spec Driven Development" to generate modular, cloud-native malware (eBPF/LKM rootkits) with production-grade quality in under a week—speed previously requiring teams. OPSEC failures exposed AI-generated planning artifacts and 88,000+ lines of code after just one week. This demonstrates how AI enables individual actors to develop sophisticated, evasive frameworks at scale, normalizing high-complexity attacks that previously required state-level resources [[Check Point](https://research.checkpoint.com/2026/voidlink-early-ai-generated-malware-framework/)].

**[UPDATE] Ransomware Surge Targets Healthcare, Aviation, and Critical Infrastructure**  
Qilin ransomware claimed Vietnam Airlines (national aviation impact) and Italian manufacturer Casadei, while Sinobi struck healthcare provider Avalon Hills. Incransom exfiltrated 1.4TB from TruStar Holdings including financial data. These follow recent patterns of multi-sector targeting with double-extortion. All groups leverage common initial access vectors (phishing, exploited vulnerabilities). Organizations must enforce network segmentation, immutable backups, and monitor for anomalous data exfiltration patterns [[DeXpose reports via Malware.News](https://malware.news/t/qilin-strikes-vietnam-airlines-in-major-ransomware-attack/103412)].

**[NEW] TamperedChef Malware Distributed via Malvertising Campaign**  
A sophisticated malvertising operation weaponized a trojanized AppSuite PDF Editor (promoted via Google Ads) to deliver the TamperedChef infostealer. Affecting 100+ organizations across 19 countries, the campaign used stolen code-signing certificates to bypass SmartScreen and deployed ModeloRAT for persistence. After a 56-day dormancy period, the malware steals browser credentials and establishes backdoors. Security teams should block associated domains (fullpdf[.]com, pdftraining[.]com) and hunt for suspicious scheduled tasks [[Cyberpress](https://cyberpress.org/google-ads-pdf-editor-tamperedchef-malware/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] TP-Link VIGI Cameras Vulnerable to Auth Bypass Attack**  
CVE-2026-0629 (CVSS 8.7) enables attackers on the LAN to reset admin passwords without verification via the password recovery feature. Improper validation of client-side state allows full device compromise, facilitating surveillance network disruption and lateral movement. 28 camera models are affected; patches are available (e.g., VIGI C455 fixed in v3.1.0 Build 250820). Organizations should prioritize updates for internet-exposed cameras or implement network segmentation [[Cyberpress](https://cyberpress.org/tp-link-vulnerability-allows/)].

**[NEW] WordPress Plugin Bug Enables Unauthenticated Admin Access**  
CVE-2025-14533 (CVSS 9.8) affects Advanced Custom Fields: Extended (≤v0.9.2.1, 100k+ installs). The plugin's 'insert_user' function lacks role restrictions, allowing unauthenticated users to grant themselves admin privileges via form submissions. This enables complete site compromise through malicious plugin uploads or content injection. Patched in v0.9.2.2; Wordfence users received virtual patches on Dec 11, 2025 [[Wordfence via Malware.News](https://malware.news/t/100-000-wordpress-sites-affected-by-privilege-escalation-vulnerability-in-advanced-custom-fields-extended-wordpress-plugin/103406)].

## 🛡️ Defense & Detection

**[NEW] Discord Infrastructure Abused for Data Theft Operations**  
Two unrelated campaigns demonstrate Discord's exploitation as C2:  
- SolyxImmortal: Python-based info stealer using dual webhooks for credential/browser data exfiltration and screenshots. Persists via registry run keys and avoids network detection [[Cyberpress](https://cyberpress.org/solyximmortal-python-malware-discord-data-theft/)].  
- Clipboard Hijacker: Targets cryptocurrency communities with Pro.exe, swapping wallet addresses during transactions via clipboard monitoring. No network activity relies on offline execution [[Cyberpress](https://cyberpress.org/discord-clipboard-hijacker-wallet-address-theft/)].  
Defenders should monitor for Discord webhook traffic and registry modifications in %APPDATA%.

**[NEW] Fake Ad Blocker Delivers ModeloRAT via Browser Crash Attack**  
The NexShield malicious Chrome/Edge extension (removed from stores) triggers browser DoS via infinite runtime port connections ("CrashFix"). After restart, it displays fake errors tricking users into running PowerShell commands that deploy ModeloRAT. Corporate targets receive custom payloads for reconnaissance and persistence. Huntress attributed this to the KongTuke actor evolving toward enterprise targeting [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-ad-blocker-extension-crashes-the-browser-for-clickfix-attacks/)]. Organizations should audit browser extensions and detect anomalous PowerShell execution chains.

## ⚡ Quick Hits

- **Google Gemini Calendar Bypass Fixed**: Prompt injection vulnerability (via hidden event descriptions) allowed private meeting data exfiltration. Patched after responsible disclosure [[Cyberpress](https://cyberpress.org/google-gemini-privacy-controls-bypassed/)].  
- **Cloudflare Zero-Day Resolved**: ACME challenge path flaw enabled WAF bypass (CVE-2025-36911). Fixed Oct 27, 2025; no malicious exploitation confirmed [[Cyberpress](https://cyberpress.org/cloudflare-zero-day-flaw/)].  
- **PDFSider Malware Emerges**: New backdoor using DLL sideloading in PDF24 Creator for ransomware attacks. Features encrypted C2 and anti-analysis techniques [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-pdfsider-windows-malware-deployed-on-fortune-100-firms-network/)].  
- **Malware Trends Report 2025**: Stealers and RATs tripled activity; Lumma and XWorm led families. Root certificate installation emerged as top TTP (385K detections) [[ANY.RUN](https://malware.news/t/malware-trends-overview-report-2025/103418)].