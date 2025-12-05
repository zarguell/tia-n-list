---
title: React2Shell critical RCE 🔴, BRICKSTORM China malware 🇨🇳, Predator zero-click spyware 📱, SMS phishing evolution 🎣, critical infrastructure targeting ⚡
date: 2025-12-05
tags: ["rce vulnerabilities","apt activity","china threat actors","mobile spyware","phishing campaigns","critical infrastructure","web exploitation","vpn security","zero-click attacks"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: React2Shell enables unauthenticated RCE in React/Next.js applications while China-linked BRICKSTORM malware maintains sophisticated persistence in critical infrastructure environments. Predator spyware evolves with zero-click ad-based infections as SMS phishing campaigns pivot to rewards and tax scams targeting mobile users.
---

# Daily Threat Intel Digest - December 5, 2025

## 🔴 Critical Threats
**React2Shell (CVE-2025-55182) Enables Unauthenticated RCE**  
A critical vulnerability in React Server Components' "Flight" protocol allows remote code execution without authentication in React and Next.js applications. With a CVSS 10.0 rating, exploitation is trivial in default configurations. Meta has patched affected packages (19.0.1+, 19.1.2+, 19.2.1+), but Wiz reports 39% of cloud environments run vulnerable versions. Public PoC exists, and broad exploitation is imminent. So What? DevOps teams using React/Next.js must patch immediately outside standard cycles - this is the worst-case RCE scenario for web frameworks. [Critical React, Next.js flaw lets hackers execute code on servers](https://www.bleepingcomputer.com/news/security/critical-react2shell-flaw-in-react-nextjs-lets-hackers-run-javascript-code/)  

**China-Linked BRICKSTORM Malware Embeds in Critical Infrastructure**  
CISA/NSA warn of sustained BRICKSTORM operations targeting VMware vSphere and Windows systems since 2022. The Golang-based malware uses layered encryption, self-reinstalls when disrupted, and maintains average 393-day persistence. Attackers steal Active Directory data, cryptographic keys, and pivot via stolen credentials. CrowdStrike attributes this to "Warp Panda" (UNC5221). So What? Critical infrastructure orgs should hunt for YARA/Sigma rules, segment networks, and audit VMware tools immediately - this represents China's most sophisticated cloud espionage campaign to date. [CISA warns of Chinese "BrickStorm" malware attacks on VMware servers](https://www.bleepingcomputer.com/news/security/cisa-warns-of-chinese-brickstorm-malware-attacks-on-vmware-servers/)  

## ⚠️ Vulnerabilities & Exploits
**ArrayOS AG VPN Vulnerability Exploited for Webshell Deployment**  
Hackers are actively exploiting a command injection flaw in Array Networks AG Series VPN devices (pre-9.4.5.9) to plant webshells and create rogue users. Despite a May fix, the flaw lacks a CVE identifier. JPCERT reports attacks since August from 194.233.100[.]138, primarily targeting Japan. Over 1,800 exposed instances exist globally. So What? Organizations using Array VPNs must upgrade to 9.4.5.9+ or disable DesktopDirect immediately - this is classic edge-device neglect enabling persistent access. [Hackers are exploiting ArrayOS AG VPN flaw to plant webshells](https://www.bleepingcomputer.com/news/security/hackers-are-exploiting-arrayos-ag-vpn-flaw-to-plant-webshells/)  

**7-Zip RCE (CVE-2025-11001) Actively Exploited in Healthcare/Finance**  
A symbolic link vulnerability in 7-Zip versions pre-25.0.0 allows arbitrary file write and code execution during archive extraction. NHS England confirmed active exploitation in November. The CVSS 7.0 flaw enables ransomware deployment or data theft via crafted ZIPs. So What? Patch 7-Zip to v25+ immediately - this proves that even "benign" utilities become high-value targets when unpatched. Automated patching is strongly recommended. [Active Exploitation of 7-Zip RCE Vulnerability Shows Why Manual Patching is No Longer an Option](https://blog.qualys.com/product-tech/2025/12/04/active-exploitation-of-7-zip-rce-vulnerability-shows-why-manual-patching-is-no-longer-an-option)  

**Foxit PDF Reader Weaponized in ValleyRAT Campaigns**  
Threat actors are exploiting Foxit PDF Reader via DLL sideloading in job-se phishing campaigns. The attacks deliver ValleyRAT, enabling full system control and data theft. Social engineering lures target employment platforms. So What? PDF readers remain underrated attack surfaces - block Foxit updates from untrusted sources and scrutinize document-handling policies. [Threat Actors Exploit Foxit PDF Reader to Seize System Access and Steal Data](https://gbhackers.com/foxit-pdf-reader/)  

## 👤 Threat Actor Activity
**Predator Spyware Adds "Aladdin" Zero-Click Ad-Based Infection**  
Intellexa's Predator spyware now uses malicious ads ("Aladdin") to infect targets zero-click via mobile ad networks. The technique forces weaponized ads onto devices via IP targeting, exploiting vulnerabilities in Samsung Exynos basebands among other vectors. Google links Intellexa to 15 zero-day exploits since 2021. So What? High-risk individuals should enable Lockdown Mode (iOS) or Advanced Protection (Android) - this represents an evolution of commercial spyware bypassing user interaction. [Predator spyware uses new infection vector for zero-click attacks](https://www.bleepingcomputer.com/news/security/predator-spyware-uses-new-infection-vector-for-zero-click-attacks/)  

**China-Based SMS Phishing Pivots to Rewards/Tax Scams**  
Phishing groups behind package delivery scams now spoof T-Mobile/AT&T rewards programs and tax authorities to harvest payment data and mobile wallet enrollment codes. Thousands of domains registered in days, with sites only loading on mobile. Fake e-commerce stores also deployed. So What? User education on mobile-based phishing is critical - these attacks bypass traditional email filters and exploit holiday shopping urgency. [SMS Phishers Pivot to Points, Taxes, Fake Retailers](https://krebsonsecurity.com/2025/12/sms-phishers-pivot-to-points-taxes-fake-retailers/)  

## 🛡️ Security Tools & Defenses
**UK NCSC Launches Proactive Notifications for Vulnerable Devices**  
The NCSC's new service scans UK-facing systems to notify orgs of exposed vulnerabilities. Delivered via Netcraft, it complements the Early Warning service by identifying risks pre-compromise. Emails originate from netcraft.com with no attachments/payments. So What? UK organizations should enroll immediately - this passive vulnerability mapping reduces blind spots in edge device management. [NCSC's ‘Proactive Notifications’ warns orgs of flaws in exposed devices](https://www.bleepingcomputer.com/news/security/ncscs-proactive-notifications-warns-orgs-of-flaws-in-exposed-devices/)  

**Microsoft Emphasizes Cyber Hygiene Fundamentals in New Guidance**  
Microsoft's Deputy CISO outlines four priorities: hygiene (asset inventories, segmentation), modern standards (phishing-resistant MFA, DNSSEC), fingerprinting, and collaboration. It deprecates EWS dependencies and pushes DMARC enforcement. So What? This grounds orgs in proven defenses amid AI hype - especially critical for resource-constrained teams. [Cybersecurity strategies to prioritize now](https://www.microsoft.com/en-us/security/blog/2025/12/04/cybersecurity-strategies-to-prioritize-now/)  

## 📰 Industry Developments
**Sean Plankey's CISA Director Nomination Withdrawn Amid Holds**  
Plankey's nomination stalled after Sens. Scott (R-FL) and Wyden (D-OR) placed holds over unrelated contract disputes and a delayed telecom security report. Acting leadership continues indefinitely. So What? CISA lacks Senate-confirmed leadership during a critical period for implementing the national cyber strategy - this hampers agency authority. [Sean Plankey nomination to lead CISA appears to be over after Thursday vote](https://cyberscoop.com/sean-plankey-cisa-nomination-stalled-senate-holds/)  

**Trump Administration's 5-Page Cyber Strategy Targets January Release**  
The draft strategy focuses on six pillars: cyber offense, regulatory alignment, workforce, procurement, critical infrastructure, and emerging tech. Notably shorter than Biden's 35-page version, it emphasizes "shaping adversary behavior" and includes AI/quantum sections. So What? The streamlined approach suggests faster policy shifts but less prescriptive guidance - orgs should prepare for deterrence-focused regulations. [Five-page draft Trump administration cyber strategy targeted for January release](https://cyberscoop.com/trump-national-cybersecurity-strategy-2025-release/)