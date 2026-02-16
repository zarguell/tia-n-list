---
title: BeyondTrust RCE exploitation 🚨, Chrome zero-day attacks 🌐, ClickFix social engineering 🎭, Rhysida ransomware delivery 💀, AI configuration theft 🤖
date: 2026-02-16
tags: ["rce exploitation","zero-day","social engineering","infostealer","ransomware","domain takeover","industrial control systems","apt activity","ai security","fileless malware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical vulnerabilities in BeyondTrust and Google Chrome are being actively exploited in the wild, enabling full domain takeovers and arbitrary code execution through malicious web pages. Sophisticated campaigns like ClickFix and OysterLoader demonstrate evolving social engineering tactics while threat actors increasingly target AI configurations and industrial control systems for maximum impact.
---

# Daily Threat Intel Digest - 2026-02-16

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] BeyondTrust RCE exploited for full domain takeover**  
Attackers are actively exploiting CVE-2026-1731 in self-hosted BeyondTrust Remote Support and Privileged Remote Access, deploying SimpleHelp RMM tools to create domain administrator accounts. Arctic Wolf's latest threat intelligence shows attackers using renamed executables in ProgramData, executing commands like `net user REDACTED_USERNAME REDACTED_PASSWORD /add /domain` followed by enterprise admin group additions. Cloud instances were auto-patched February 2, but self-hosted deployments (RS ≤25.3.1, PRA ≤24.3.4) remain vulnerable to this domain-level takeover [[Arctic Wolf](https://cyberpress.org/beyondtrust-flaw/)].  

**[NEW] Google Chrome zero-day under active exploitation**  
Google confirmed CVE-2026-2441 (CVSS 8.8), a use-after-free flaw in CSS, is being actively exploited. This is the first Chrome zero-day of 2026, discovered and reported by researcher Shaheen Fazim on February 11. The vulnerability allows arbitrary code execution via malicious web pages, prompting emergency patches to versions 145.0.7632.75/76 (Windows/Mac) and 144.0.7559.75 (Linux). Users should update immediately as exploits require only web page visits [[Google Releases](https://cyberpress.org/google-chrome-zero-day-flaw/)].  

**[NEW] Critical FileZen flaw enables OS command execution**  
Authenticated attackers are exploiting CVE-2026-25108 (CVSS 8.8/8.7) in Soliton Systems' FileZen file transfer solution, targeting versions V-5.0.0-V-5.0.10 and V-4.2.1-V-4.2.8. The OS command injection flaw, active in the wild since mid-February, exploits antivirus scanning processes to execute arbitrary commands. Japan's JVN advisory urges immediate upgrades to V-5.0.11, as exploitation requires only valid credentials [[JVN Advisory](https://cyberpress.org/filezen-file-transfer-flaw/)].  

## 🎯 Threat Actor Activity & Campaigns

**[NEW] ClickFix campaign delivers StealC via fake CAPTCHA**  
A novel social engineering wave uses fake Cloudflare CAPTCHA prompts to trick users into running PowerShell commands, deploying StealC infostealer. Attackers compromise legitimate websites (e.g., restaurant sites) to inject scripts prompting victims to press Win+R and paste malicious commands. The fileless chain uses reflective shellcode loading into svchost.exe, stealing browser data, crypto wallets, and system details. Key IOCs include payload IPs (94.154.35.115) and SHA-256 hashes [[LevelBlue](https://cyberpress.org/clickfix-targets-windows-users/)].  

**[NEW] XWorm RAT distributed via legacy Office vulnerability**  
A cyber-espionage campaign leverages CVE-2018-0802 (Microsoft Equation Editor RCE) to deliver XWorm RAT v7.2. Phishing emails with malicious Excel add-ins trigger shellcode that downloads HTA files, leading to process hollowing in Msbuild.exe. The RAT enables data theft, DDoS attacks, and ransomware deployment via 50+ plugins. Despite being an 8-year-old flaw, unpatched Office components remain prime targets [[Fortinet](https://cyberpress.org/phishing-spreads-xworm-rat/)].  

**[NEW] OysterLoader fuels Rhysida ransomware attacks**  
A sophisticated multi-stage loader called OysterLoader (aka Broomstick/CleanUp) is delivering Rhysida ransomware via fake software sites impersonating tools like PuTTY and Google Authenticator. Written in C++, it uses API flooding, LZMA compression, and steganography to evade detection. The loader establishes persistence through scheduled tasks every 13 minutes and communicates with C2 via encrypted HTTP. Researchers link it to Wizard Spider associates [[Sekoia](https://cyberpress.org/oysterloader-fuels-rhysida-attacks/)].  

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical ZLAN ICS flaws enable device takeover**  
CISA advisory ICSA-26-041-02 details CVE-2026-25084 and CVE-2026-24789 (both CVSS 9.8) in ZLAN5143D serial-to-Ethernet servers. The flaws allow unauthenticated attackers to bypass controls or reset passwords, threatening OT environments in manufacturing. Firmware 1.600 is affected; mitigations include network isolation, VPNs for remote access, and immediate patching [[CISA Advisory](https://cyberpress.org/zlan-ics-flaws/)].  

**[NEW] AI-powered phishing surge in 2025**  
Security reports highlight a sharp increase in AI-driven attacks personalizing phishing lures and QR code "quishing." Attackers use algorithms to craft CEO impersonation emails and dynamic phishing sites, while QR codes redirect to fraudulent pages. Defenders should implement behavioral analytics and user awareness training to counter these scalable threats [[Securelist](https://cyberpress.org/ai-phishing-attacks-surge/)].  

## 🛡️ Defense & Detection

**[NEW] Hudson Rock exposes AI configuration theft**  
A real-world infostealer infection exfiltrated OpenClaw AI workspace files, including `openclaw.json` (with gateway tokens) and `device.json` (containing private keys). This marks a shift from credential theft to targeting AI agent identities. Defenders should monitor for file-grabbing routines targeting `.openclaw` directories and memory-only injection techniques [[Hudson Rock](https://malware.news/t/hudson-rock-identifies-real-world-infostealer-infection-targeting-openclaw-configurations/104138#post_1)].  

**[NEW] Kimsuky continues Korean-language targeting**  
North Korea's Kimsuky group is distributing IPSInvoice.chm, a malicious Windows Help file disguised as a penalty notice. The malware, analyzed by Wezard4u,延续了该组织针对韩语用户的传统。Defenders should block CHM execution from untrusted sources [[Wezard4u](https://malware.news/t/kimsuky-ipsinvoice-chm/104136#post_1)].