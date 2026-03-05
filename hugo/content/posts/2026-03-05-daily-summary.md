---
title: Cisco Firewall auth bypass 🔴, Tycoon 2FA takedown 🚨, Silver Dragon Google Drive C2 🐉, Phobos Ransomware disruption 💰, LeakBase forum seizure ⚖️
date: 2026-03-05
tags: ["authentication bypass","phishing-as-a-service","apt activity","ransomware","cybercrime forum","file-based c2","mfa bypass","credential theft","vulnerability management","law enforcement"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical Cisco firewall vulnerabilities allowing unauthenticated root access demand immediate patching while global authorities successfully disrupted the Tycoon 2FA phishing platform that compromised 96,000 victims through MFA bypass techniques. State-sponsored Silver Dragon APT continues evading detection using Google Drive for stealth command-and-control, while law enforcement actions against Phobos ransomware operators and the LeakBase cybercrime forum demonstrate coordinated efforts to dismantle criminal infrastructure protecting critical sectors worldwide.
---

# Daily Threat Intel Digest - 2026-03-05

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical Cisco Firewall Flaw Under Active Exploitation**  
Cisco has patched a critical authentication bypass vulnerability in its Secure Firewall Management Center (FMC) software (CVE-2026-20079, CVSS 10.0) that allows unauthenticated attackers to gain root access via crafted HTTP requests. The flaw stems from improper boot process initialization, enabling remote code execution without credentials. Cisco confirms no public exploits yet, but the pre-auth nature and trivial exploit path make this an immediate patch priority for all on-premises deployments. Cloud-based FMC instances are unaffected. Upgrade to patched releases immediately using Cisco's Software Checker tool [[Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2); [Cyberpress](https://cyberpress.org/cisco-secure-firewall-management-vulnerability/)].  

**[NEW] Global Coalition Dismantles Tycoon 2FA Phishing Operation**  
Microsoft, Europol, and international partners have seized the Tycoon 2FA Phishing-as-a-Service platform, which bypassed MFA for 96,000+ victims worldwide since 2023. The adversary-in-the-middle (AiTM) operation hijacked live sessions to compromise Microsoft 365 and Google accounts, driving 62% of phishing blocked by Microsoft at its peak. Authorities seized 330 domains and servers, disrupting attacks that targeted healthcare, education, and government sectors. Primary operator Saad Fridi (Pakistan-attributed) ran the service like a business with RaccoonO365 connections. Organizations should adopt phishing-resistant MFA (FIDO2) and monitor for AiTM reverse proxy indicators [[Microsoft](https://blogs.microsoft.com/on-the-issues/2026/03/04/how-a-global-coalition-disrupted-tycoon/); [Cyberpress](https://cyberpress.org/tycoon-2fa-phishing/)].  

**[UPDATE] Silver Dragon APT Leverages Google Drive for Stealth C2**  
APT-linked Silver Dragon (aligned with APT41) has deployed GearDoor, a new backdoor using Google Drive for command-and-control communications to evade network monitoring. Active since mid-2024 across Europe and Southeast Asia, the group uses file extensions (.png, .cab, .rar) within unique Google Drive folders to receive encrypted commands and exfiltrate data. This file-based C2 method bypasses traditional protocol inspection, requiring defenders to monitor for abnormal Google Drive API usage and file transfer patterns. The campaign also uses BamboLoader with advanced obfuscation [[Check Point](https://research.checkpoint.com/2026/silver-dragon-targets-organizations-in-southeast-asia-and-europe/); [Cyberpress](https://cyberpress.org/silver-dragon-apt-uses-google-drive/)].  

## 🎯 Threat Actor Activity & Campaigns  

**[NEW] SloppyLemming APT Targets Critical Infrastructure in South Asia**  
India-linked SloppyLemming (aka Outrider Tiger) has intensified espionage against Pakistan and Bangladesh's nuclear regulators, energy utilities, and banks using BurrowShell and Rust-based RATs. The group expanded infrastructure to 112 Cloudflare Workers domains for payload delivery (up from 13 in Sept 2024), impersonating entities like Pakistan's nuclear authority and Dhaka Electric Supply. Infection chains start with weaponized PDFs that trigger ClickOnce applications leading to Cobalt Strike. The campaign highlights Cloudflare's abuse for C2 and demands network segmentation for critical infrastructure [[Arctic Wolf](https://arcticwolf.com/resources/blog/sloppylemming-deploys-burrowshell-and-rust-based-rat-to-target-pakistan-and-bangladesh/); [Cyberpress](https://cyberpress.org/sloppylemming-targets-southeast-asia/)].  

**[UPDATE] Phobos Ransomware Admin Pleads Guilty, $39M Scheme Disrupted**  
Russian national Evgenii Ptitsyn admitted to wire fraud for administering the Phobos ransomware-as-a-service operation, which extorted over $39 million from 1,000+ victims. Ptitsyn sold access to affiliates for $300 per deployment and took cuts of ransoms since 2020. His plea follows Operation Aether arrests and infrastructure seizures in Poland/Italy. Organizations should monitor for Phobos TTPs (RDP brute force, data exfil before encryption) and implement network access controls [[BleepingComputer](https://www.bleepingcomputer.com/news/security/phobos-ransomware-admin-pleads-guilty-to-wire-fraud-conspiracy/); [Talos analysis](https://blog.talosintelligence.com/understanding-the-phobos-affiliate-structure/)].  

**[NEW] "Operation Leak" Seizes LeakBase Cybercrime Forum**  
The FBI and international law enforcement seized LeakBase, a major cybercriminal forum trafficking stolen databases and credentials since BreachForums' takedown. Authorities seized domains (leakbase.ws/.la) and preserved user data/IP logs, enabling attribution. The forum facilitated over 400 imminent ransomware attacks before its shutdown. Organizations should query breach databases for credentials and enforce MFA, as leak data may circulate [[Cyberpress](https://cyberpress.org/operation-leak-shuts-down-leakbase-cybercrime/); [GBHackers](https://gbhackers.com/operation-leak-authorities-dismantle-leakbase-forum/)].  

## ⚠️ Vulnerabilities & Patches  

**[NEW] Cisco Catalyst SD-WAN Flaws Enable Root Access**  
Cisco patched multiple critical vulnerabilities in Catalyst SD-WAN Manager, including CVE-2026-20129 (CVSS 9.8), allowing unauthenticated API bypass for netadmin privileges. Two bugs (CVE-2026-20122, CVE-2026-20128) are under active exploitation. Affected devices face complete compromise if unpatched, enabling ransomware deployment. Upgrade immediately to v20.9.8.2/20.12.6.1/20.15.4.2/20.18.2.1 and block internet access to management interfaces [[Cisco advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-authbp-qwCX8D4v); [Cyberpress](https://cyberpress.org/critical-cisco-catalyst-sd-wan-vulnerabilities-allow-attackers-to-gain-root-access/)].  

**[NEW] Google Chrome Patches 10 Vulnerabilities**  
Google released an emergency Chrome update fixing 10 flaws (3 critical, 7 high) on March 3. While no in-the-wild exploits are confirmed, the patches resolve memory corruption risks enabling RCE. Users should update to Chrome 122.0.6261.128+ [[GBHackers](https://gbhackers.com/google-rolls-out-emergency-chrome-update/)].  

## 🛡️ Defense & Detection  

**[NEW] Study Reveals 2,622 Valid Certificates Exposed in Code Repositories**  
A GitGuardian/Google study found 2,622 valid TLS certificates exposed via leaked private keys on GitHub/DockerHub, affecting 900+ Fortune 500 firms. Only 24 were revoked despite disclosure efforts, highlighting systemic PKI management failures. 22% of certs differed from online versions, indicating post-leak reissues without revocation. Organizations should enforce certificate cryptoperiods, automate key rotation (e.g., Let's Encrypt), and scan repos for private keys [[GitGuardian](https://blog.gitguardian.com/certificates-exposed-a-google-gitguardian-study/)].  

**[NEW] Malicious Laravel Packages Distribute PHP RAT**  
Threat actor nhattuanbl uploaded three malicious PHP packages to Packagist deploying a persistent RAT that contacts C2 at helper.leuleu.net:2096. The obfuscated payload steals database/API credentials and enables remote commands. Affected packages: `nhattuanbl/lara-helper`, `nhattuanbl/simple-queue`, and `nhattuanbl/lara-swagger` (dependency). Organizations should audit Laravel dependencies, rotate secrets, and block outbound C2 traffic [[Socket research](https://socket.dev/blog/malicious-packagist-packages-disguised-as-laravel-utilities); [Cyberpress](https://cyberpress.org/malicious-laravel-packages-deploy-rat/)].  

## 📋 Policy & Industry News  

**[NEW] Law Enforcement Seizes LeakBase Forum in Global Operation**  
The FBI dismantled LeakBase via "Operation Leak," seizing domains and user data/IP logs to disrupt cybercrime data markets. The forum, active since BreachForums' takedown, hosted stolen credentials and corporate data. Authorities urge cooperation via FBI-SU-Leakbase@fbi.gov. This follows trends in targeting cybercrime infrastructure like Qakbot [[Cyberpress](https://cyberpress.org/operation-leak-shuts-down-leakbase-cybercrime/)].  

**[NEW] Reclaim Security Raises $26M for Automated Remediation**  
Reclaim Security secured $26M in funding to preemptively patch vulnerabilities before exploitation, citing machine-speed attacks using tools like Claude Code. The platform aims to reduce the 27-day average remediation gap through continuous exposure management. The investment reflects growing demand for automated patch orchestration [[GBHackers](https://gbhackers.com/reclaim-security-raises-26m-to-eliminate-the-27-day-remediation-gap/)].  

## ⚡ Quick Hits  

- **Safari Back-Button Hijacked in Malvertising:** D-Shortiez campaign exploits WebKit history manipulation to trap users in redirect loops, targeting iOS/Safari with 300M+ impressions since Aug 2025 [[Cyberpress](https://cyberpress.org/d-shortiez-hijacks-webkit-back-button/)].  
- **RedAlert Espionage Targets Israeli Civilians:** Trojanized Rocket Alert app harvests geolocation and personal data amid Israel-Iran conflict [[GBHackers](https://gbhackers.com/redalert-mobile-espionage/)].  
- **ClickFix Campaign Hits Web3 Experts:** Fake LinkedIn VCs push malware via fake CAPTCHA flows targeting crypto/Web3 professionals [[GBHackers](https://gbhackers.com/fake-linkedin-vcs/)].