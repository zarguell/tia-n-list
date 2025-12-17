---
title: Gladinet/Triofox RCE exploitation 🚨, parked domains malware 🌐, ClickFix DarkGate delivery 💀, Cellik Android RAT 📱, BlindEagle Colombia targeting 🎯
date: 2025-12-17
tags: ["remote code execution","cloud storage vulnerabilities","parked domains","malware distribution","darkgate","android rat","apt activity","social engineering","government sector","mobile threats"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical vulnerabilities in Gladinet CentreStack and Triofox cloud storage platforms are being actively exploited through hardcoded keys, while parked domains have evolved into a primary malware distribution channel with over 90% malicious content. Sophisticated campaigns including ClickFix social engineering, Cellik Android RAT automation, and BlindEagle's targeting of Colombian government agencies demonstrate multi-vector threats across cloud infrastructure, web infrastructure, and mobile platforms requiring immediate defensive prioritization.
---

# Daily Threat Intel Digest - December 17, 2025

## 🔴 Critical Threats & Active Exploitation

**[NEW] CISA Warns of Actively Exploited Hardcoded Keys in Gladinet CentreStack/Triofox**  
Attackers are exploiting hardcoded cryptographic keys in Gladinet CentreStack and Triofox cloud storage platforms to achieve remote code execution without authentication. The vulnerability (CVE-2025-14611) allows Local File Inclusion attacks, enabling data theft and full system compromise. CISA added this to its KEV catalog with a federal remediation deadline of January 5, 2026, but warns all organizations to patch immediately due to active exploitation [[CyberPress](https://cyberpress.org/cisa-warns-triofox-vulnerabilities/); [GBHackers](https://gbhackers.com/cisa-alerts-on-actively-exploited-gladinet-centrestack-and-triofox-flaws/)]. Over 80,000 organizations use these platforms for secure file sharing.

**[NEW] Critical RCE in NVIDIA Isaac Lab Exploited in the Wild**  
A deserialization flaw (CVE-2025-32210) in NVIDIA’s Isaac Lab robotics simulation framework enables unauthenticated remote code execution with CVSS 9.0 severity. Attackers can hijack systems running vulnerable versions (<v2.3.0) across all platforms, potentially stealing sensitive AI research data or deploying ransomware. NVIDIA confirmed active exploitation and urged immediate patching, though attacker origins remain unclear [[CyberPress](https://cyberpress.org/nvidia-isaac-lab-vulnerability/); [GBHackers](https://gbhackers.com/nvidia-isaac-lab-flaw-enables-remote-code-execution/)].

**[NEW] Parked Domains Become Primary Malware Distribution Channel**  
New Infoblox research reveals over 90% of visits to parked domains now lead to malware, scams, or phishing—a dramatic shift from <5% maliciousness a decade ago. Attackers leverage "direct search" advertising models and cloaking to redirect real users (not scanners) through multi-layered traffic distribution systems delivering Tedy malware, credential theft, and scams. Major brands like Netflix, Gmail, and Scotiabank are typosquatted, while one actor controls 80,000+ domains using "double fast flux" DNS to resist takedowns [[CyberPress](https://cyberpress.org/parked-domains-malware-scams/); [GBHackers](https://gbhackers.com/malware-and-phishing/)].

**[UPDATE] Chrome Emergency Update Patches Actively Exploited RCE Flaws**  
Google released Chrome 143.0.7499.146/.147 to address two high-severity vulnerabilities: CVE-2025-14765 (use-after-free in WebGPU) and CVE-2025-14766 (out-of-bounds read/write in V8). Both enable remote code execution, with the first flaw awarded a $10,000 bounty. While disclosure details are restricted pending patch adoption, Google’s urgent rollout signals active exploitation risk—continuing the trend of zero-day Chrome attacks flagged in prior reporting [[CyberPress](https://cyberpress.org/chrome-security-update-patches-vulnerabilities/); [GBHackers](https://gbhackers.com/chrome-security-update-fixes-flaws/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] "ClickFix" Social Engineers Deliver DarkGate via Fake Browser Alerts**  
A new campaign tricks users into executing malicious PowerShell commands by spoofing "Word Online extension not installed" errors. Victims copy/paste obfuscated PowerShell commands from pop-ups into Windows Run dialogs, deploying DarkGate malware through HTA files and AutoIt scripts. Attackers use clipboard manipulation and multi-stage payloads to evade detection, leveraging MITRE TTPs like T1059.001 (PowerShell) and T1027 (Obfuscation) [[CyberPress](https://cyberpress.org/clickfix-darkgate-infection/); [GBHackers](https://gbhackers.com/darkgate-malware/)].

**[NEW] BlindEagle Targets Colombian Government with Caminho Downloader**  
BlindEagle (APT-C-36) compromised a Colombian Ministry of Commerce email account to launch spear-phishing campaigns delivering DCRAT RAT via the Caminho downloader. The attack chain uses fraudulent judicial portals, nested JavaScript/PowerShell scripts, and steganography to hide payloads in PNG files. DCRAT employs AES-256 encryption and certificate-based C2 authentication, while Caminho’s Portuguese code hints at Brazilian cybercrime origins [[CyberPress](https://cyberpress.org/blindeagle-campaign/); [Zscaler Research](https://www.zscaler.com/blogs/security-research/blindeagle-targets-colombian-government-agency-caminho-and-dcrat)].

**[NEW] Cellik Android RAT Automates Play Store App Infection**  
A new MaaS offering called Cellik enables attackers to inject spyware into legitimate Google Play apps via a one-click APK builder. For $150/month, it provides live screen streaming, notification interception, hidden browser activity, and credential overlay theft. The malware claims to bypass Play Protect and has already been observed in trojanized apps, escalating risks for Android users sideloading APKs [[CyberPress](https://cyberpress.org/one-click-android-malware-tool/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/cellik-android-malware-builds-malicious-versions-from-google-play-apps/)].