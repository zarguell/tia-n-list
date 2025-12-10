---
title: Windows Zero-Day escalation 🔴, North Korean blockchain malware 🇰🇵, PowerShell security bypass ⚡, EDR process abuse 🛡️, fake Teams supply chain 🎯
date: 2025-12-10
tags: ["zero-day","privilege escalation","north korean apt","blockchain malware","react2shell","powershell bypass","edr abuse","ransomware","initial access brokers","supply chain attacks"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Windows Zero-Day CVE-2025-62221 enables active SYSTEM privilege escalation across all supported versions while North Korean Lazarus groups exploit React2Shell to deploy blockchain-powered EtherRAT malware with five persistence mechanisms. PowerShell Mark-of-the-Web bypasses and Storm-0249's EDR process abuse demonstrate how attackers are subverting trusted security tools, alongside Silver Fox's sophisticated supply chain impersonation using fake Microsoft Teams installers.
---

# Daily Threat Intel Digest - 2025-12-10

## 🔴 Critical Threats

**Actively Exploited Windows Zero-Day Elevates to SYSTEM**  
Microsoft patched CVE-2025-62221, a Windows Cloud Files Mini Filter Driver vulnerability already exploited in the wild. Attackers combine this use-after-free flaw with other code execution bugs to gain SYSTEM privileges on all supported Windows versions. The driver is used by cloud services like OneDrive and remains present even without those apps installed. CISA added this to its KEV catalog with a Dec 30 patch deadline.  
*So What?* This is an active exploitation pathway to full system compromise – prioritize patching immediately, especially on enterprise endpoints where cloud storage integrations exist. [Microsoft December 2025 Patch Tuesday Fixes 56 Vulnerabilities Fixed and 3 Zero-days](https://www.bleepingcomputer.com/news/microsoft/microsoft-december-2025-patch-tuesday-fixes-3-zero-days-57-flaws/)  

**North Korean Hackers Deploy Blockchain-Powered Malware via React2Shell**  
Lazarus-affiliated groups exploited the critical React2Shell flaw (CVE-2025-55182) to deploy EtherRAT, a Linux implant using Ethereum smart contracts for C2. The malware establishes five persistence mechanisms and self-updates to evade detection. Over 30 organizations were compromised within days of public disclosure.  
*So What?* Blockchain C2 complicates takedowns while React2Shell's widespread use in cloud environments creates mass exploitation risk – patch React/Next.js now and monitor for Ethereum RPC anomalies. [North Korean hackers exploit React2Shell flaw in EtherRAT malware attacks](https://www.bleepingcomputer.com/news/security/north-korean-hackers-exploit-react2shell-flaw-in-etherrat-malware-attacks/)  

## ⚠️ Vulnerabilities & Exploits

**PowerShell Bypasses Mark-of-the-Web Protections**  
CVE-2025-54100 allows attackers to execute malicious scripts via Invoke-WebRequest by exploiting code execution before file writes, circumventing MotW security controls. Microsoft now forces user confirmation prompts in PowerShell 5.1 and recommends -UseBasicParsing.  
*So What?* Default PowerShell behavior changed overnight – update automation scripts to avoid hangs and prevent potential script-based compromises. [Windows PowerShell now warns when running Invoke-WebRequest scripts](https://www.bleepingcomputer.com/news/security/microsoft-windows-powershell-now-warns-when-running-invoke-webrequest-scripts/)  

**Ivanti EPM Vulnerable to Unauthenticated XSS**  
CVE-2025-10573 (CVSS 9.6) lets attackers poison administrator dashboards by joining fake endpoints, enabling session hijacking via stored JavaScript. Hundreds of internet-exposed instances exist despite vendor warnings.  
*So What?* Critical enterprise management tool exposure – patch immediately and restrict internet access to EPM consoles. [Ivanti warns of critical Endpoint Manager code execution flaw](https://www.bleepingcomputer.com/news/security/ivanti-warns-of-critical-endpoint-manager-code-execution-flaw/)  

**GitHub Copilot for JetBrains Vulnerable to Command Injection**  
CVE-2025-64671 lets attackers execute arbitrary code through cross-prompt injection in AI coding assistants, part of the broader "IDEsaster" class affecting multiple AI development tools.  
*So What?* AI code assistants introduce new attack surfaces – update Copilot plugins and review auto-approve terminal settings. [Microsoft December 2025 Patch Tuesday Fixes 56 Vulnerabilities Fixed and 3 Zero-days](https://www.bleepingcomputer.com/news/microsoft/microsoft-december-2025-patch-tuesday-fixes-3-zero-days-57-flaws/)  

## 👤 Threat Actor Activity

**Storm-0249 Abuses EDR Processes for Stealthy Persistence**  
This ransomware IAB side-loads malicious DLLs into legitimate SentinelOne EDR processes after initial access via ClickFix social engineering. Attackers then abuse trusted EDR components for C2 and data collection.  
*So What?* EDR tools become blind spots when compromised – monitor for unsigned DLL loads in security processes and restrict curl/PowerShell execution. [Ransomware IAB abuses EDR for stealthy malware execution](https://www.bleepingcomputer.com/news/security/ransomware-iab-abuses-edr-for-stealthy-malware-execution/)  

**Silver Fox Pushes Fake Teams Installer via SEO Poisoning**  
China-linked APT leverages Cyrillic/Russian false flags and SEO manipulation to distribute ValleyRAT-laced Microsoft Teams installers targeting Chinese-speaking employees.  
*So What?* Sophisticated supply chain impersonation bypasses language-based defenses – validate all software installers through official channels. [Threat Actors Poison SEO to Spread Fake Microsoft Teams Installer](https://gbhackers.com/fake-microsoft-teams-2/)  

## 🛡️ Security Tools & Defenses

**Android GPUs Hardened Against Exploitation**  
Google and Arm restricted deprecated/debug GPU IOCTLs via SELinux policies, blocking access to non-production interfaces on 45% of Android devices. This reduces kernel attack surface without breaking legitimate apps.  
*So What?* Proactive attack surface reduction that protects billions of devices – adopt similar hardware-level filtering in embedded systems. [Further Hardening Android GPUs](http://security.googleblog.com/2025/12/further-hardening-android-gpus.html)  

**Insurance Coverage Now Includes Deepfake Reputational Harm**  
Coalition expanded cyber policies to cover deepfake-enabled fraud and reputation attacks, providing forensic analysis and legal takedown services. Claims remain rare but growing in sophistication.  
*So What?* Financial protection emerging for AI-powered social engineering attacks – assess coverage gaps in your cyber policies. [Organizations can now buy cyber insurance that covers deepfakes](https://cyberscoop.com/url-coalition-cybersecurity-insurance-coverage-deepfakes-reputational-harm/)  

## 📰 Industry Developments

**UK Sanctions Russian and Chinese Information Warfare Firms**  
The UK imposed sanctions against entities tied to state-sponsored disinformation campaigns, reflecting escalating geopolitical cyber tensions.  
*So What?* Signals increased regulatory pressure on information operations – review supply chain relationships with sanctioned entities. [UK Sanctions Russian and Chinese Firms Suspected of Being ‘Malign Actors’ in Information Warfare](https://www.securityweek.com/uk-sanctions-russian-and-chinese-firms-suspected-of-being-malign-actors-in-information-warfare/)  

**Spanish Teen Arrested for Stealing 64M Personal Records**  
A 19-year-old was detained for breaching nine companies and selling data including IBAN codes and DNI numbers on hacker forums.  
*So What?* Youth cybercrime scaling dramatically – strengthen identity monitoring and data minimization practices. [Spain arrests teen who stole 64 million personal data records](https://www.bleepingcomputer.com/news/security/spain-arrests-teen-who-stole-64-million-personal-data-records/)