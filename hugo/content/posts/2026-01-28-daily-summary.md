---
title: WinRAR exploitation 🚨, Fortinet SSO bypass 🔓, AI malware targeting India 🎯, Node.js sandbox escape 💻, ChatGPT extension theft 📱
date: 2026-01-28
tags: ["apt activity","zero-day exploits","ai-powered attacks","government targeting","supply chain attacks","cloud security","malware campaigns","nation-state threats","authentication bypass","session hijacking"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Nation-state actors and cybercriminal groups are actively exploiting critical vulnerabilities in WinRAR and Fortinet SSO implementations to achieve persistent access and administrative control across enterprise environments. AI-generated malware campaigns targeting Indian government entities and widespread session token theft from malicious ChatGPT extensions highlight the growing sophistication of attackers leveraging emerging technologies while Node.js sandbox escape vulnerabilities threaten application security across countless projects.
---

# Daily Threat Intel Digest - January 28, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] WinRAR CVE-2025-8088 exploited by multiple nation-state and cybercrime groups**  
Attackers are actively exploiting a six-month-old WinRAR path traversal vulnerability to achieve persistent access on Windows systems through malicious archive files. Both Russian-linked groups (UNC4895/RomCom, APT44/FROZENBARENTS, TEMP.Armageddon/CARPATHIAN, Turla/SUMMIT) and China-based actors have deployed this flaw since July 2025, with financial criminals distributing commodity RATs and banking trojans. The exploit uses Alternate Data Streams to write LNK/HTA/BAT files to the Startup folder, requiring no user interaction after archive opening [[Google Threat Intel](https://cloud.google.com/blog/topics/threat-intelligence/exploiting-critical-winrar-vulnerability)]; [BleepingComputer](https://www.bleepingcomputer.com/news/security/winrar-path-traversal-flaw-still-exploited-by-numerous-hackers); [CyberScoop](https://www.cyberscoop.com/winrar-defect-active-exploits-google-threat-intel). Update to WinRAR 7.13+ is critical; Google provides IOC collections for hunting.

**[NEW] Critical Fortinet FortiCloud SSO authentication bypass (CVE-2026-24858) under active attack**  
Attackers are exploiting a new critical vulnerability in Fortinet's SSO implementation to gain administrative access to FortiOS, FortiManager, and FortiAnalyzer devices. The vulnerability allows attackers with any FortiCloud account to authenticate to other customers' devices when SSO is enabled, bypassing previous patches for CVE-2025-59718. Fortinet has disabled FortiCloud SSO access from vulnerable firmware versions while patches are developed, and confirmed exploitation via malicious accounts `cloud-noc@mail.io` and `cloud-init@mail.io` [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fortinet-blocks-exploited-forticloud-sso-zero-day-until-patch-is-ready); [Fortinet Advisory](https://fortiguard.fortinet.com/psirt/FG-IR-26-060). Organizations should review logs for these indicators and consider disabling SSO until patches arrive.

**[NEW] OpenSSL vulnerabilities enable potential remote code execution**  
OpenSSL released patches for multiple vulnerabilities, with CVE-2025-15467 (High severity) enabling stack buffer overflow RCE in CMS parsing with AEAD ciphers, and CVE-2025-11187 (Moderate) allowing PKCS#12 parameter validation bypass. These affect OpenSSL versions 3.0-3.6 and require immediate upgrading to 3.0.19, 3.3.6, 3.4.4, 3.5.5, or 3.6.1 respectively [[OpenSSL Advisory](https://openssl-library.org/news/vulnerabilities/index.html); [CyberPress](https://cyberpress.org/openssl-vulnerabilities-remote-execute-malicious-code); [Canadian Centre Cyber Security](https://cyber.gc.ca/en/alerts-advisories/openssl-security-advisory-av26-058). While FIPS modules remain largely unaffected, organizations should prioritize updates on systems processing CMS or PKCS#12 files.

## 🎯 Threat Actor Activity & Campaigns

**[NEW] SHEETCREEP/FIREPOWER/MAILCREEP campaign targets Indian government with AI-generated malware**  
A sophisticated campaign is targeting Indian government entities using three custom backdoors leveraging legitimate cloud services for C2: SHEETCREEP (C# using Google Sheets), FIREPOWER (PowerShell via Firebase), and MAILCREEP (Golang via Microsoft Graph). ThreatLabz identified high-confidence indicators of generative AI use in malware development, including emojis in error handling and verbose commenting patterns [[Zscaler ThreatLabz](https://www.zscaler.com/blogs/security-research/apt-attacks-target-indian-government-using-sheetcreep-firepower-and)]. The campaign uses PDF lures with geographic filtering, employs typos suggesting hands-on-keyboard operation, and shares TTPs with Pakistan-linked APT36 while introducing new evasion techniques.

**[NEW] Vietnam-based PureRAT actor uses AI to build phishing tools**  
A Vietnam-based cybercrime actor appears to be leveraging generative AI to create scripts for phishing campaigns, marking a continuation of AI-powered attack tooling that lowers technical barriers for financially motivated attackers [[Malware-News](https://malware.news/t/purerat-attacker-now-using-ai-to-build-toolset/103637#post_1)]. While specific payloads aren't detailed, this represents the growing trend of AI accelerating phishing kit development and campaign operationalization.

**[UPDATE] 31 additional defendants charged in massive ATM jackpotting operation**  
US authorities have charged 31 more defendants linked to the Tren de Aragua gang's ATM jackpotting scheme, bringing total defendants to 87 across recent months. The group uses Ploutus malware installed via physical access to force ATMs to dispense cash, with stolen funds laundered through predetermined arrangements [[BleepingComputer](https://www.bleepingcomputer.com/news/security/us-charges-31-more-suspects-linked-to-atm-malware-attacks)]. This demonstrates ongoing financial infrastructure attacks despite previous indictments.

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical vm2 Node.js sandbox escape (CVE-2026-22709)**  
A critical vulnerability in the popular vm2 Node.js sandbox library allows escaping the secure context to execute arbitrary code on the host system. The flaw arises from improper sanitization of Promise callbacks in version 3.10.0, with a partial fix in 3.10.1 and complete fix in 3.10.2 [[BleepingComputer](https://www.bleepingcomputer.com/news/security/critical-sandbox-escape-flaw-discovered-in-popular-vm2-nodejs-library); [GitHub Advisory](https://github.com/patriksimek/vm2/security/advisories/GHSA-99p7-6v5w-7xg8). With over 200,000 GitHub projects and 1M weekly downloads, immediate patching is crucial for systems executing untrusted JavaScript.

**[NEW] 16 malicious ChatGPT extensions steal session tokens**  
A coordinated campaign deployed 16 malicious Chrome extensions disguised as ChatGPT enhancers that hijack session tokens from authenticated ChatGPT sessions. The extensions inject content scripts into chatgpt.com to intercept authorization headers, granting attackers full account access including conversation histories and connected services like Google Drive [[LayerX via CyberPress](https://cyberpress.org/16-malicious-chatgpt-extensions-exposed); [Malwarebytes](https://www.malwarebytes.com/blog/threat-intel/2026/01/watch-out-for-att-rewards-phishing-text-that-wants-your-personal-details)). With 900 installations and all variants still live in stores, enterprises should implement extension allowlists and monitor for these specific IDs.

## 🛡️ Defense & Detection

**[NEW] WhatsApp launches Strict Account Settings against spyware**  
WhatsApp introduced a lockdown-style feature allowing high-risk users (journalists, activists) to restrict attachments/media from non-contacts and limit advanced functionality. The optional setting provides protection against sophisticated spyware attacks like Pegasus, similar to Apple's Lockdown Mode and Google's Advanced Protection [[CyberScoop](https://www.cyberscoop.com/whatsapp-strict-account-settings-lockdown-style-spyware-protection/); [WhatsApp Blog](https://blog.whatsapp.com/whatsapps-latest-privacy-protection-strict-account-settings). This represents platform-level acknowledgment of targeted threats against civil society.

**[NEW] Android 16 enhances theft protection with stronger authentication safeguards**  
Google expanded Android's theft protection including: granular Failed Authentication Lock controls, Identity Check expansion to all Biometric Prompt apps, increased lockout times for screen lock guessing (excluding identical attempts), and default-on Theft Detection Lock and Remote Lock in Brazil [[Google Blog](http://security.googleblog.com/2026/01/android-theft-protection-feature-updates.html)]. These features make devices harder targets for snatch-and-run theft and improve account recovery options.

**[NEW] AWS WorkMail abuse enables phishing infrastructure bypassing SES controls**  
Attackers are abusing compromised AWS credentials to create WorkMail organizations for phishing campaigns, bypassing SES sandbox restrictions. The attack chain involves creating WorkMail organizations, verifying domains, and using SMTP access to send high-volume emails without CloudTrail logging [[Rapid7](https://www.rapid7.com/blog/post/dr-threat-actors-aws-workmail-phishing-campaigns)]. Defenders should monitor for WorkMail API calls (CreateOrganization, CreateUser) and consider SCP restrictions blocking WorkMail if unused.

**[NEW] Nike investigating potential breach after World Leaks extortion claim**  
Nike is investigating a potential cybersecurity incident after the World Leaks extortion group (believed to be Hunters International rebrand) claimed 1.4TB theft and posted files online [[BleepingComputer](https://www.bleepingcomputer.com/news/security/nike-investigates-data-breach-after-extortion-gang-leaks-files)]. The group previously targeted high-profile organizations including US Marshals Service and Tata Technologies. Organizations should prepare for extortion negotiations while conducting forensic analysis.

## 📋 Policy & Industry News

**[NEW] Memory Integrity Enforcement (MIE) provides hardware-enforced memory safety on iPhone 17**  
Apple's Memory Integrity Enforcement (MIE) combines Enhanced MTE (EMTE), secure type-aware allocators, and tag confidentiality enforcement to prevent buffer overflows, use-after-free, and type confusion at hardware level with near-zero performance overhead [[8kSec](https://8ksec.io/mie-deep-dive-kernel/)]. The implementation includes SPTM hypervisor protection and synchronous tag checking, addressing weaknesses in standard ARM MTE like the TikTag attack. This represents a fundamental shift toward hardware-based vulnerability mitigation.

**[NEW] Data Privacy Day 2026 emphasizes "Privacy-First" enterprise advantages**  
The January 28 Data Privacy Day highlights how privacy has shifted from compliance checkbox to competitive advantage, with 81% of B2B buyers listing "Data Sovereignty" as top-three requirement [[Seqrite](https://www.seqrite.com/blog/data-privacy-day-2026-why-the-privacy-first-enterprise-is-winning-the-trust-race/)]. Organizations are implementing Privacy-Enhancing Technologies (PETs) and synthetic data for AI training while minimizing data hoarding to reduce "Privacy Debt."

**[NEW] Microsoft announces 2026 Security Excellence Awards winners**  
Microsoft recognized partners for AI-powered security innovations including Avertium (Security Trailblazer), BlueVoyant (Data Security), Tata Consultancy Services (Secure Access), Anna Bordioug of Protiviti (Security Changemaker), and Illumio (Software Development) [[Microsoft Blog](https://www.microsoft.com/en-us/security/blog/2026/01/27/microsoft-announces-the-2026-security-excellence-awards-winners/)]. The awards highlight industry collaboration in advancing Zero Trust and AI-integrated defenses.