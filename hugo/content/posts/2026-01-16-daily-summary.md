---
title: AWS supply chain hijack 🔐, ransomware campaigns 💣, Windows update bugs 🔄, zero-click exploits 📱
date: 2026-01-16
tags: ["supply chain attacks","ransomware","zero-click exploits","cloud security","wordpress vulnerabilities","windows updates","data breaches","malware evasion","authentication bypass","mobile security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: AWS CodeBuild supply chain attacks enabled repository hijacking and malicious code injection affecting millions of cloud environments. Ransomware gangs expand targeting of professional services while zero-click exploits threaten mobile device security through chained vulnerabilities.
---

# Daily Threat Intel Digest - January 16, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] AWS CodeBuild Supply Chain Hijacks GitHub Repositories**  
Attackers exploited a regex filtering misconfiguration in AWS CodeBuild to hijack critical repositories, including the AWS JavaScript SDK used in 66% of cloud environments. By leveraging GitHub's sequential ID assignment, researchers created bot accounts with substring IDs to bypass webhook filters, steal GitHub credentials, and gain admin control. The vulnerability allowed malicious code injection into SDK releases distributed to millions via the AWS Console. AWS has implemented PR approval gates and recommends immediate webhook regex hardening. [[Wiz Research](https://www.cyberpress.org/aws-console-supply-chain-attack-github-hijackingcyber/); [GBHackers](https://gbhackers.com/aws-console-supply-chain-attack-enables-github-repository-hijacking/)]

**[NEW] Windows Update Bug Triggers Restart Loop on Enterprise PCs**  
Microsoft confirmed KB5073455 prevents Windows 11 23H2 devices with System Guard Secure Launch from shutting down or hibernating, forcing restarts instead. The issue affects Enterprise and IoT editions only, with no current workaround for hibernation failures. Users must execute `shutdown /s /t 0` from Command Prompt to power down safely. This compounds January's Windows update troubles after Cloud PC access failures and security alert false positives. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-some-windows-pcs-fail-to-shut-down-after-january-update/)]

**[NEW] Critical WordPress Plugin Exploited for Admin Takeover**  
The Modular DS plugin (40k+ installations) suffers from CVE-2026-23550, allowing unauthenticated attackers to bypass authentication and gain admin privileges. Active exploitation began January 13 via flawed "direct request" mode handling and automatic admin login fallback. Version 2.5.2 patches the vulnerability, and users must regenerate WordPress salts post-update. Review access logs for suspicious requests and rogue admin accounts. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-exploit-modular-ds-wordpress-plugin-flaw-for-admin-access/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Ransomware Gangs Target Legal, Manufacturing, and Food Sectors**  
Qilin ransomware claimed attacks on Germany's Aero-Coating, Canada's Bergmanis Preyra Legal Services, and Singapore's Neo Group, threatening data leaks unless ransoms are paid. Concurrently, Akira targeted US insuretech firm Paylogix (stealing 185GB including employee SSNs) and McAloon & Friedman law firm (627GB of legal/client data). These campaigns highlight ransomware's expansion into professional services and supply chain extortion. [[DeXpose](https://www.dexpose.io/qilin-ransomware-breaches-aero-coating/); [DeXpose](https://www.dexpose.io/qilin-ransomware-attack-on-bergmanis-preyra-legal-services/); [DeXpose](https://www.dexpose.io/qilin-ransomware-attack-on-neo-group/); [DeXpose](https://www.dexpose.io/akira-targets-insuretech-leader-paylogix-in-major-ransomware-attack/); [DeXpose](https://www.dexpose.io/akira-ransomware-targets-mcaloon-friedman-law-firm/)]

**[NEW] ShinyHunters Extorts Grubhub with Salesforce/Zendesk Data**  
Attackers stole Salesforce (Feb 2025) and Zendesk data from Grubhub via credentials compromised in the Salesloft Drift OAuth token breach. The ShinyHunters group is demanding Bitcoin to prevent leaks. While Grubhub confirms unauthorized access, it denies financial data theft. Organizations affected by Salesloft must rotate all OAuth tokens immediately. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/grubhub-confirms-hackers-stole-data-in-recent-security-breach/)]

## ⚠️ Vulnerabilities & Patches

**[NEW] Azure AD Token Flaw Enables Tenant-Wide Windows Admin Center Breaches**  
CVE-2026-20965 allows attackers with local admin rights on a single machine to compromise any Windows Admin Center-managed system in the same Azure tenant. The flaw stems from improper Proof-of-Possession token validation in Azure AD SSO. Microsoft has not yet released patches. [[GBHackers](https://gbhackers.com/azure-identity-token-flaw-exposes-windows-admin-center/)]

**[NEW] Zero-Click Exploit Chain Targets Google Pixel 9**  
Google Project Zero disclosed CVE-2025-54957 (Dolby decoder) and CVE-2025-36934 (kernel driver) chained for zero-click code execution and privilege escalation on Pixel 9 devices. No user interaction is required. Google has issued patches via January updates. [[GBHackers](https://gbhackers.com/zero-click-exploit-chain-discovered-targeting-google-pixel-9-devices/)]

## 🛡️ Defense & Detection

**[NEW] Gootloader Malware Evades Analysis with 1,000-Part ZIP Archives**  
Gootloader now concatenates 500–1,000 ZIP archives with truncated End of Central Directory records and randomized metadata to crash analysis tools. Expel released a YARA rule to detect these malformed archives, which unpack successfully via Windows utilities but fail in 7-Zip/WinRAR. Defenders should block wscript.exe/cscript.exe execution on downloaded content. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/gootloader-now-uses-1-000-part-zip-archives-for-stealthy-delivery/)]

## 📋 Policy & Industry News

**[NEW] CISA's Own Software Tool Found Vulnerable to XSS**  
A basic XSS flaw in CISA's "Software Acquisition Guide" web tool, discovered by Jeff Williams, allowed JavaScript injection and potential website defacement. Fixed in December after initial rejection from bug bounty programs. CISA acknowledged process improvements post-disclosure. [[CyberScoop](https://cyberscoop.com/cisa-secure-software-buying-tool-had-a-simple-xss-vulnerability-of-its-own/)]

**[NEW] Microsoft Launches VSCode Copilot Studio Extension**  
The new VSCode extension enables developers to manage Copilot Studio agents locally, integrate with Git workflows, and deploy via CI/CD pipelines. Available after 13k+ downloads, it supports AI-assisted agent editing while addressing recent concerns about AI development supply chain security. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-copilot-studio-extension-for-vs-code-now-publicly-available/)]

---
*Tia N. List, Senior Threat Intelligence Analyst*  
*Sources: 28 articles analyzed; 9 items prioritized for operational impact.*