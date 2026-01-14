---
title: Microsoft zero-days 🔴, FortiOS RCE exploitation 🚨, CastleLoader gov attacks 🏛️, university ransomware breaches 🎓, Magecart payment theft 💳
date: 2026-01-14
tags: ["zero-day vulnerabilities","remote code execution","malware campaigns","ransomware","government sector","education sector","payment theft","credential harvesting","patch management","supply chain attacks"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical Microsoft and FortiOS zero-day vulnerabilities enable memory extraction and unauthenticated RCE, creating immediate risks for enterprise networks and requiring emergency patching before credential rotation. Government entities, universities, and e-commerce platforms face targeted campaigns from CastleLoader malware, ransomware gangs, and Magecart skimmers that steal sensitive data through sophisticated evasion and social engineering techniques.
---

# Daily Threat Intel Digest - 2026-01-14

## 🔴 Critical Threats & Active Exploitation

**[NEW] Microsoft Desktop Window Manager Zero-Day Exploited in Wild**  
CVE-2026-20805 allows authenticated local attackers to extract sensitive system memory data without user interaction, potentially compromising credentials and encryption keys [[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-desktop-window-manager-zero-day-vulnerability/); [GBHackers](https://gbhackers.com/microsoft-desktop-window-manager-zero-day/)]. Microsoft confirmed active exploitation and released patches January 13, 2026. The vulnerability affects all Windows versions where Desktop Window Manager runs, making workstations handling confidential data immediate targets. Organizations should prioritize patching before credential rotation.

**[NEW] FortiOS Remote Code Execution Vulnerability Exploitable Without Authentication**  
CVE-2025-25249 (CVSS 7.4) stems from a heap-based buffer overflow in the cw_acd daemon, enabling unauthenticated remote attackers to execute arbitrary code on FortiOS and FortiSwitchManager systems [[CyberPress](https://cyberpress.org/fortios-and-fortiswitchmanager-vulnerabilities/); [GBHackers](https://gbhackers.com/fortios-and-fortiswitchmanager-flaw/)]. Affected versions span FortiOS 6.4.0–7.6.3 and FortiSwitchManager 7.0–7.2. Organizations must upgrade to patched versions immediately or block CAPWAP-CONTROL traffic (UDP 5246-5249) as temporary mitigation.

**[NEW] Monroe University Confirms 320,000 Victims in December 2024 Ransomware Attack**  
Attackers maintained access to university networks for two weeks, stealing personal, financial, and health data including Social Security numbers and medical records [[BleepingComputer](https://www.bleepingcomputer.com/news/security/monroe-university-says-2024-data-breach-affects-320-000-people/)]. The breach notification began January 2, 2026, with credit monitoring offered. This adds to a trend of U.S. university breaches, following similar incidents at University of Hawaii and Baker University, highlighting educational institutions as persistent ransomware targets.

## 🎯 Threat Actor Activity & Campaigns

**[NEW] CastleLoader Malware Targets U.S. Government Entities**  
Sophisticated loader has impacted 469 devices across government agencies and critical infrastructure using multi-stage evasion via Inno Setup installers and AutoIt scripts [[CyberPress](https://cyberpress.org/castleloader-malware-targets-us-government/); [GBHackers](https://gbhackers.com/castleloader-malware/)]. Delivered through ClickFix social engineering, it performs process hollowing into legitimate processes like jsc.exe, deploying file-less malware to bypass signature detection. C2 server at 94.159.113.32 confirmed, with mutex and user agent IOCs available. Organizations should implement EDR solutions monitoring memory injections.

**[NEW] Ukraine Defense Personnel Targeted in Charity-Themed PluggyApe Campaign**  
Void Blizzard (UAC-0190) uses fake charity websites with Ukrainian language messages and compromised phone numbers to deliver PluggyApe.V2 backdoor via .docx.pif files [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ukraines-army-targeted-in-new-charity-themed-malware-campaign/); [CyberPress](https://cyberpress.org/charity-lure-cyber-attacks-ukrainian-defense/)]. The malware uses WebSockets/MQTT for C2 and retrieves infrastructure from Pastebin/Rentry.co. Mobile devices are prime targets due to poor monitoring. Military personnel should verify charities through official channels and report suspicious files to csoc@post.mil.gov.ua.

**[NEW] VVS Stealer Harvests Discord Credentials and Browser Data**  
Python-based malware sold via Telegram since April 2025 exfiltrates Discord tokens, Nitro subscriptions, payment details, and data from 19 browsers using AES-128-CTR obfuscation [[CyberPress](https://cyberpress.org/vvs-stealer-discord-credential-token-theft/); [GBHackers](https://gbhackers.com/vvs-stealer/)]. Persists via startup folders and injects JavaScript into Discord's Electron app to hijack sessions. Data exfiltrated to Discord webhooks. Organizations should restrict PyInstaller execution and monitor for anomalous Discord API traffic.

## ⚠️ Vulnerabilities & Patches

**[NEW] Microsoft Patch Tuesday Addresses 114 Vulnerabilities Including 3 Zero-Days**  
January 2026 release patches critical RCE flaws in LSASS (CVE-2026-20854) and Office (CVE-2026-20944/20955), alongside zero-days CVE-2026-20805 (Desktop Window Manager) and CVE-2026-21265 (Windows Digital Media) [[CyberPress](https://cyberpress.org/microsoft-fixes-114-vulnerabilities/); [GBHackers](https://gbhackers.com/microsoft-january-2026-patch-tuesday/); [CyberScoop](https://cyberscoop.com/microsoft-patch-tuesday-january-2026/)]. 57 elevation-of-privilege bugs dominate, with SMB servers and Windows kernel drivers requiring immediate attention. WSUS servers (CVE-2026-20856) and Office endpoints should be prioritized due to network-based exploitation and phishing risks.

**[NEW] Node.js Releases Emergency Patches for 8 High-Severity Vulnerabilities**  
All active release lines (20.x, 22.x, 24.x, 25.x) updated to fix memory leaks, permission bypasses, and DoS flaws including CVE-2025-55131 (uninitialized memory exposure) and CVE-2025-55130 (symlink sandbox escape) [[CyberPress](https://cyberpress.org/node-js-security-release-patches-7-vulnerabilities-across-all-release-lines/); [GBHackers](https://gbhackers.com/node-js-security-release-fixes-7-vulnerabilities/)]. Enterprises using Node.js for untrusted code execution must upgrade immediately to prevent multi-tenant environment compromises.

## 🛡️ Defense & Detection

**[NEW] Game-Theoretic AI Framework Automates Cyber Attack/Defense Strategy**  
Generative Cut-the-Rope (G-CTR) converts penetration testing logs into attack graphs 245x faster than manual analysis, increasing exploit success rates by 142% in cyber-range tests [[CyberPress](https://cyberpress.org/game-theoretic-ai-cyber-attack-defense-strategies/); [GBHackers](https://gbhackers.com/ai-driven-game/)]. The system computes Nash equilibrium strategies for optimal attack paths and defensive controls with <5ms overhead. While promising for automated defense, organizations should monitor for adversaries weaponizing similar frameworks.

**[NEW] Magecart Campaign Steals Payment Data via Fake Stripe Forms**  
Campaign active since 2022 injects skimmer JavaScript into WooCommerce sites, creating fake Stripe payment forms to steal credit card data from major networks [[CyberPress](https://cyberpress.org/magecart-attack-credit-card-data-checkout-pages/); [GBHackers](https://gbhackers.com/magecart-campaign-2/)]. Obfuscated with XOR encryption (key: "777") and evades admin detection. E-commerce sites must enforce Content Security Policies and regularly audit checkout pages for unauthorized iframes.

## 📋 Policy & Industry News

**[NEW] Trump Renominates Sean Plankey to Lead CISA**  
Plankey's stalled 2025 nomination resubmitted to Senate after serving as senior adviser to DHS Secretary [[CyberScoop](https://cyberscoop.com/sean-plankey-re-nominated-to-lead-cisa/)]. Confirmation hurdles remain due to Sen. Rick Scott's hold over Coast Guard contract disputes. Leadership continuity at CISA remains critical amid escalating cyber threats to critical infrastructure.