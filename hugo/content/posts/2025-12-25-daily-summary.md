---
title: FortiGate 2FA bypass 🔐, MongoDB RCE flaw 💥, Typosquatting malware 🎯, Bank credential theft 💰, Evasive Panda APT 🐼
date: 2025-12-25
tags: ["fortigate vulnerability","mongodb rce","typosquatting","cosmali loader","bank theft","evasive panda","apt activity","phishing","vulnerability management","two-factor bypass"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical infrastructure faces immediate risks as attackers exploit a FortiGate 2FA bypass vulnerability and MongoDB RCE flaw while distributing malware through typosquatting domains targeting software piracy tools. Financial institutions suffer significant losses from sophisticated credential theft operations, and Chinese APT group Evasive Panda continues refining DNS poisoning tactics to deliver stealthy implants across multiple regions.
---

# Daily Threat Intel Digest - 2025-12-25

## 🔴 Critical Threats & Active Exploitation

**[NEW] FortiGate 2FA bypass exploited via case sensitivity trick**  
Attackers are actively exploiting a 3-year-old Fortinet FortiGate vulnerability (CVE-2020-12812) to bypass two-factor authentication by manipulating username case sensitivity. The flaw allows unauthorized access to administrative interfaces, SSL VPNs, and IPsec VPNs when attackers use alternate capitalization (e.g., "Jsmith" instead of "jsmith"), triggering fallback authentication without 2FA enforcement. All organizations using FortiOS versions prior to 6.0.10, 6.2.4, or 6.4.1 with LDAP configurations are vulnerable and should apply immediate mitigations including disabling username case sensitivity or removing secondary LDAP groups [[Cyberpress](https://cyberpress.org/hackers-abuse-3-year-old-fortigate-flaw/)].

**[NEW] MongoDB RCE flaw demands emergency patching**  
A critical remote code execution vulnerability (CVE-2025-14847) in MongoDB exposes hundreds of thousands of databases to unauthenticated attacks through improper length parameter handling in zlib compression. Exploitation allows attackers to execute arbitrary code and potentially gain full system control without credentials. The flaw impacts MongoDB 8.2.0-8.2.3, 8.0.0-8.0.16, 7.0.0-7.0.26, 6.0.0-6.0.26, 5.0.0-5.0.31, 4.4.0-4.4.29, and all v4.2/4.0/3.6 server versions. Emergency patches are available in versions 8.2.3+, 8.0.17+, 7.0.28+, 6.0.27+, 5.0.32+, and 4.4.30+ [[BleepingComputer](https://www.bleepingcomputer.com/news/security/mongodb-warns-admins-to-patch-severe-rce-flaw-immediately/); [Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/mongodb-security-advisory-av25-862)].

**[NEW] Typosquatting MAS domain spreads Cosmali Loader**  
Attackers registered the look-alike domain "get.activate[.]win" (missing "d" from legitimate "get.activated.win") to distribute PowerShell malware through Microsoft Activation Scripts (MAS). Victims who mistyped the command received the Cosmali Loader, which deploys XWorm RAT and cryptominers while warning victims through hijacked control panels. The campaign demonstrates continued abuse of software piracy tools for malware distribution, with impact spanning Windows systems globally [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-mas-windows-activation-domain-used-to-spread-powershell-malware/)].

**[NEW] FBI seizes $28M bank credential theft operation**  
U.S. authorities disrupted a phishing infrastructure stealing bank credentials through fraudulent search ads, seizing the 'web3adspanels.org' domain containing thousands of stolen login records. The scheme caused confirmed losses of $14.6M from 19+ victims, with attempted damages reaching $28M. Attackers used Google/Bing ads impersonating legitimate banking portals to harvest credentials, demonstrating the ongoing effectiveness of search engine poisoning for financial fraud [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-seizes-domain-storing-bank-credentials-stolen-from-us-victims/)].

## 🎯 Threat Actor Activity & Campaigns  

**[UPDATE] Evasive Panda refines DNS poisoning tactics**  
The China-linked APT group Evasive Panda (StormBamboo) expanded its stealthy campaign (Nov 2022-Nov 2024) using DNS poisoning and fake software updaters to deliver MgBot implants. New research reveals the group distributed malicious updaters impersonating SohuVA, iQIYI Video, and Tencent QQ through manipulated domains like "p2p.hd.sohu.com[.]cn". Attackers employed multi-stage loaders with PJW API hashing, hybrid DPAPI/RC5 encryption, and version-specific payloads for Windows/MacOS targeting across China, India, and Türkiye [[Cyberpress](https://cyberpress.org/evasive-panda-adversary/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] MongoDB releases emergency patches for RCE**  
MongoDB addressed CVE-2025-14847 (CVSS:9.8) in its December 24 advisory, urging immediate upgrades for all supported versions. The vulnerability allows unauthenticated RCE through uninitialized heap memory exposure in zlib compression. Administrators unable to patch immediately should disable zlib compression via networkMessageCompressors settings as temporary mitigation [[JIRA advisory](https://jira.mongodb.org/browse/SERVER-115508); [Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/mongodb-security-advisory-av25-862)].

## 🛡️ Defense & Detection

**[NEW] Microsoft Teams adds external user blocking**  
Microsoft will roll out Defender for Office 365 integration in January 2026, allowing admins to block external users/domains via the Tenant Allow/Block List. The feature targets increasing Teams abuse by ransomware groups like Black Basta and Matanbuchus operators, supporting up to 4,000 blocked domains and 200 email addresses. Organizations must enable "Block specific users" and "Allow security team management" in Teams admin center pre-deployment [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-teams-to-let-admins-block-external-users-via-defender-portal/)].

## 📋 Policy & Industry News

**[NEW] CISA loses ransomware warning program lead**  
David Stern, architect of CISA's Pre-Ransomware Notification Initiative (PRNI), resigned after being denied a requested reassignment, potentially disrupting the agency's ability to provide early ransomware attack warnings. The departure raises concerns about reduced proactive threat intelligence sharing during critical infrastructure attacks [[DataBreaches.Net](https://databreaches.net/2025/12/24/cisa-loses-key-employee-behind-early-ransomware-warnings/)].

**[NEW] Industry opposes HIPAA security rule overhaul**  
Healthcare organizations are pushing back against HHS-proposed HIPAA Security Rule updates, arguing the requirements would impose excessive compliance burdens. The opposition centers on mandatory encryption, penetration testing, and incident response timelines that providers claim lack cost-benefit justification [[DataBreaches.Net](https://databreaches.net/2025/12/24/industry-continues-to-push-back-on-hipaa-security-rule-overhaul/)].