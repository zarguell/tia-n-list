---
title: RESURGE malware attacks 🔐, Chrome extension crypto theft 💰, ransomware surge 💣, SQL Server hardening 🛡️, macOS persistence 🍎
date: 2026-03-01
tags: ["malware","ransomware","phishing","vulnerability exploitation","crypto theft","persistence techniques","sql server security","macos security","initial access","data breach"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: RESURGE malware exploits critical Ivanti vulnerabilities while compromised Chrome extensions steal cryptocurrency wallets through ClickFix attacks. Ransomware gangs expand attacks across healthcare and construction sectors as security teams must address SQL Server hardening and macOS persistence techniques to reduce breach risks.
---

# Daily Threat Intel Digest - 2026-03-01

## 🔴 Critical Threats & Active Exploitation

**[NEW] RESURGE Malware Exploits Ivanti Connect Secure CVE-2025-0282**  
Attackers are actively exploiting a critical Ivanti Connect Secure vulnerability (CVE-2025-0282) to deploy RESURGE, a sophisticated Linux backdoor that operates with complete passive C2. Unlike conventional implants, RESURGE injects itself into Ivanti's web server process and activates only upon receiving specially crafted TLS traffic, generating no detectable outbound traffic during dormancy. This makes network-based detection extremely challenging. Organizations using unpatched Ivanti appliances face immediate risk of persistent, stealthy compromise [[Picus Security](https://www.picussecurity.com/resource/resurge-malware-exploits-ivanti-connect-secure-cve-2025-0282-vulnerability)].

**[NEW] QuickLens Chrome Extension Hijacked for ClickFix Attacks and Crypto Theft**  
A compromised Chrome extension ("QuickLens - Search Screen with Google Lens") with 7,000 users is actively deploying ClickFix attacks and stealing cryptocurrency wallets. After changing ownership in February 2026, the extension stripped CSP headers and contacted a C2 server to deliver malicious scripts that displayed fake Google Update prompts. Victims tricked into running commands received info-stealers targeting MetaMask, Phantom, and 9 other wallets. Google has disabled the extension, but users must revoke stored credentials and transfer crypto assets [[BleepingComputer](https://www.bleepingcomputer.com/news/security/quicklens-chrome-extension-steals-crypto-shows-clickfix-attack/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Ransomware Surge Targets Healthcare, Construction, and Critical Infrastructure**  
Multiple ransomware gangs expanded operations on February 28, 2026, with Nightspire attacking U.S. healthcare provider Hicare and tech firm PriceTable; DragonForce compromising construction firm Aegis Project Controls (threatening to leak 214GB of military/biosecurity facility data); Qilin hitting hospitality and manufacturing targets; and MyData striking Greece's sole appliance producer PYRAMIS. These attacks highlight ransomware's continued focus on sectors with high operational disruption value [[DeXpose](https://www.dexpose.io/nightspire-ransomware-attack-hicare-hicare/); [DeXpose](https://www.dexpose.io/dragonforce-ransomware-attack-on-aegis-project-controls/); [DeXpose](https://www.dexpose.io/qilin-strikes-north-andover-country-club-in-ransomware-attack/); [DeXpose](https://www.dexpose.io/mydata-ransomware-attack-on-pyramis-metallourgia-s-a/)].

**[UPDATE] Phishing Campaign Distributes Teramind Spyware via Fake Zoom/Google Meet**  
Threat actors are leveraging fake Microsoft Store-style pages for Zoom and Google Meet to distribute Teramind, a legitimate enterprise monitoring tool abused for surveillance. The malicious MSI installer uses stealth deployment, disables detection in Add/Remove Programs, and creates persistent services. A single installer file can be reused for thousands of attacks by renaming it with embedded campaign codes. C2 communication occurs via rt.teramind.co [[Malwarebytes](https://www.malwarebytes.com/blog/threat-intel/2026/02/fake-zoom-and-google-meet-scams-install-teramind-a-technical-deep-dive); [CyberPress](https://cyberpress.org/phishing-attacks-impersonate-zoom-and-google-meet/); [GBHackers](https://gbhackers.com/fake-zoom-and-google-meet-phishing-campaigns/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Ivanti Connect Secure CVE-2025-0282 Under Active Exploitation**  
The RESURGE malware campaign confirms in-the-wild exploitation of CVE-2025-0282, a critical vulnerability in Ivanti Connect Secure VPN appliances. Attackers gain initial access through this flaw before deploying the stealthy backdoor. Ivanti customers must apply vendor patches immediately and assume compromise if unpatched [[Picus Security](https://www.picussecurity.com/resource/resurge-malware-exploits-ivanti-connect-secure-cve-2025-0282-vulnerability)].

**[NEW] SQL Server Hardening Guide Addresses Critical Attack Paths**  
Security researchers released a comprehensive CIS-aligned hardening guide for Microsoft SQL Server 2019/2022, emphasizing disabling high-risk features like xp_cmdshell, CLR integration, and Ad Hoc Distributed Queries to prevent RCE and privilege escalation. The guide details specific configurations to block common attack vectors used in ransomware deployments [[SOCFortress](https://socfortress.medium.com/microsoft-sql-server-2019-2022-secure-deployment-hardening-guide-cis-benchmarks-70bf7ecb6700)].

## 🛡️ Defense & Detection

**[NEW] macOS AutoLaunchedApplicationDictionary Persistence Technique Documented**  
Security researchers detailed a stealth macOS persistence method using the AutoLaunchedApplicationDictionary within com.apple.loginwindow preferences. This "living-off-the-land" technique—used by APTs like Windshift and Kimsuky—avoids LaunchAgents detection by adding entries to user Login Items via legitimate APIs. Defenders should monitor changes to this domain using `defaults read com.apple.loginwindow AutoLaunchedApplicationDictionary` [[cocomelonc](https://cocomelonc.github.io/macos/2026/02/28/mac-malware-persistence-4.html)].

**[NEW] SQL Server Hardening Checklist Reduces Breach Surface**  
The new CIS benchmark provides an actionable checklist including: dedicated SQL hosts, encrypted connections, disabled xp_cmdshell/CLR, restricted sysadmin roles, and mandatory auditing. High-availability environments require synchronized patching across replicas to prevent version mismatches that break security controls [[SOCFortress](https://socfortress.medium.com/microsoft-sql-server-2019-2022-secure-deployment-hardening-guide-cis-benchmarks-70bf7ecb6700)].

## 📋 Policy & Industry News

**[NEW] Connecticut Senate Bill Mandates Breach Forensics**  
Connecticut introduced SB 117, requiring entities experiencing "massive breaches" (≥100,000 residents) to conduct mandatory forensic examinations. The bill raises response costs but aims to improve incident investigation quality for large-scale events [[DataBreaches.net](https://databreaches.net/2026/02/28/connecticut-senate-bill-raises-the-stakes-on-data-breach-response/)].

**[NEW] Operational Security Failure Costs Tax Agency $4.8M**  
South Korea's National Tax Service accidentally exposed the recovery phrase for a seized crypto wallet in press photos, leading to the immediate theft of $4.8M in assets. The incident highlights critical risks of photographing or digitizing seed phrases, which provide full wallet access without additional safeguards [[BleepingComputer](https://www.bleepingcomputer.com/news/security/48m-in-crypto-stolen-after-korean-tax-agency-exposes-wallet-seed/)].