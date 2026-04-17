---
title: Microsoft Defender zero-days exploited 🔐, AI infrastructure vulnerability 🤖, water treatment malware 💧, ransomware rebranding 💣
date: 2026-04-17
tags: ["zero-day exploitation","privilege escalation","ai security","critical infrastructure","ransomware","ot security","supply chain","remote monitoring tools","threat actors"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Active exploitation of unpatched Microsoft Defender zero-days grants SYSTEM privileges while a critical flaw in Model Context Protocol enables arbitrary command execution across AI infrastructure. ZionSiphon malware targets Israeli water treatment facilities for chlorine sabotage, and former BlackBasta affiliates deploy Payouts King ransomware with sophisticated evasion techniques.
---
# Daily Threat Intel Digest - April 17, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] Two unpatched Microsoft Defender zero-days under active exploitation**

Threat actors are exploiting three Windows zero-day vulnerabilities discovered by disgruntled researcher "Chaotic Eclipse," with two remaining unpatched and granting SYSTEM privileges on fully updated systems. The RedSun exploit abuses Windows Defender's cloud file handling to overwrite system files and achieve privilege escalation, while UnDefend allows standard users to block antivirus definition updates—both work on Windows 10, Windows 11, and Server 2019+ even after April Patch Tuesday. BlueHammer (CVE-2026-33825) was patched this month but has been exploited in the wild since April 10, with Huntress Labs confirming hands-on-keyboard activity combining all three techniques on compromised VPN accounts [[BleepingComputer](https://www.bleepingcomputer.com/news/security/recently-leaked-windows-zero-days-now-exploited-in-attacks/); [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/new-microsoft-defender-redsun-zero-day-poc-grants-system-privileges/)].

**[NEW] Critical RCE flaw in Model Context Protocol threatens AI infrastructure**

A systemic vulnerability in Anthropic's Model Context Protocol—now the industry standard for AI agent communication—enables arbitrary command execution through MCP adapters. OX Security researchers discovered the architectural flaw allows attackers to seize complete control of affected MCP implementations, gaining direct access to the underlying systems hosting AI workloads. The vulnerability threatens the expanding ecosystem of AI agent deployments that rely on MCP for tool integration and inter-agent communication [[GBHackers](https://gbhackers.com/critical-flowise-flaw-enables-remote-command-execution/)].

**[NEW] ZionSiphon malware targets Israeli water treatment with chlorine sabotage**

A new OT-focused malware strain specifically designed to sabotage Israeli water treatment and desalination plants can manipulate hydraulic pressures and raise chlorine levels to dangerous amounts. ZionSiphon checks for Israeli IP ranges and scans for water treatment software before activating its payload, which appends malicious configuration changes to maximize chlorine dosage and flow. While the current sample contains a flawed XOR verification that triggers self-destruction instead of execution, Darktrace warns the malware represents a concerning evolution in critical infrastructure targeting—with USB propagation designed to cross air-gapped environments [[BleepingComputer](https://www.bleepingcomputer.com/news/security/zionsiphon-malware-designed-to-sabotage-water-treatment-systems/); [GBHackers](https://gbhackers.com/zionsiphon-malware/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Payouts King ransomware emerges from BlackBasta alumni**

A technically sophisticated ransomware operation dubbed "Payouts King" is being deployed by former BlackBasta affiliates, combining the group's social engineering playbook with hardened obfuscation and encryption routines. The operation focuses on high-value data theft and selective encryption while leveraging strong cryptography and extensive EDR evasion techniques to stay ahead of security tools. The emergence signals continued fragmentation and rebranding among established ransomware ecosystems [[GBHackers](https://gbhackers.com/payouts-king-emerges/)].

**[NEW] Cybercriminals weaponize RMM tools for physical cargo theft**

Organized crime groups are infecting freight brokers and trucking carriers with remote monitoring software to hijack commercial shipments, turning network access into physical theft at scale. Since August 2025, attackers have compromised load boards, hijacked email threads, and deployed legitimate RMM tools like ScreenConnect, SimpleHelp, and LogMeIn Resolve to steal cargo ranging from electronics to energy drinks. The campaigns exploit trust in digital logistics infrastructure, with stolen credentials enabling attackers to post fraudulent freight listings and redirect shipments before selling goods online or shipping them overseas [[GBHackers](https://gbhackers.com/cargo-hackers-hit-trucking/); [CyberPress](https://cyberpress.org/cargo-theft-cyberattack-wave/)].

## ⚠️ Vulnerabilities & Patches

**[UPDATE] Marimo exploitation expands to Hugging Face supply chain**

Attackers exploiting CVE-2026-39987 in the marimo Python notebook platform are now deploying an NKAbuse backdoor variant hosted on Hugging Face Spaces, transforming AI/ML developer environments into infection vectors. The campaign chains pre-authentication RCE with credential theft and lateral movement to PostgreSQL and Redis databases, using a blockchain-based C2 channel designed to evade monitoring. Organizations running marimo notebooks or allowing access to Hugging Face Spaces should treat these environments as high-risk attack surfaces [[GBHackers](https://gbhackers.com/weaponized-cve-2026-39987/)].

**[NEW] April Microsoft patches trigger domain controller reboot loops**

Windows domain controllers are entering restart loops due to LSASS crashes after installing the April 2026 security update (KB5082063), potentially rendering domains unavailable for authentication services. The issue specifically affects environments using Privileged Access Management on non-Global Catalog domain controllers, with Microsoft confirming the problem impacts Windows Server 2016 through 2025. No fix is currently available—administrators must contact Microsoft Support for mitigation measures if already deployed [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-warns-of-reboot-loops-affecting-some-domain-controllers/)].

## 📋 Policy & Industry News

**[NEW] Operation PowerOFF dismantles DDoS infrastructure, warns 75,000 users**

International law enforcement has seized 53 DDoS-for-hire domains and issued warnings to over 75,000 individuals using booter services across 21 countries. The coordinated action resulted in four arrests and 25 search warrants, with authorities now deploying awareness campaigns including search engine ads targeting young people seeking DDoS tools. The operation builds on previous phases that dismantled infrastructure and seized databases containing over 3 million criminal accounts [[BleepingComputer](https://www.bleepingcomputer.com/news/security/operation-poweroff-identifies-75k-ddos-users-takes-down-53-domains/); [SecurityWeek](https://www.securityweek.com/53-ddos-domains-taken-down-by-law-enforcement/)].

**[NEW] EU age verification app bypassed in under two minutes**

The European Union's newly launched age verification application contains critical design flaws allowing attackers to hijack user identity credentials by manipulating locally stored configuration files. Security consultant Paul Moore demonstrated that deleting specific encryption values and restarting the app triggers a PIN reset flow that grants access to the original user's identity vault, with additional flaws allowing rate-limiting bypass and biometric authentication disable—contradicting EU officials' claims of robust privacy standards [[CyberPress](https://cyberpress.org/eus-new-age-verification-app/); [GBHackers](https://gbhackers.com/eu-age-verification-app-breached/)].

**[NEW] US nationals sentenced for North Korean IT worker infiltration scheme**

Two New Jersey men received prison sentences of nine years and 92 months respectively for facilitating North Korea's long-running operation to plant IT workers inside US businesses, generating over $5 million for the regime. The conspiracy placed operatives at more than 100 US companies including Fortune 500 firms, with participants stealing sensitive defense contractor files related to US military technology. The case highlights the dual-use risk of DPRK IT workers who can operationalize their access for espionage when tasked [[CyberScoop](https://cyberscoop.com/us-nationals-sentenced-facilitate-north-korea-tech-worker-scheme/)].