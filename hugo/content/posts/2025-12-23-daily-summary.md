---
title: Water infrastructure ransomware 💧, Clop data breaches 🏫, supply chain attacks 📦, living-off-the-land tools 🔧, critical RCEs ⚡
date: 2025-12-23
tags: ["ransomware","data breach","supply chain","living-off-the-land","critical infrastructure","education sector","vulnerabilities","initial access","legitimate tool abuse"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Water infrastructure and education sectors face escalating ransomware threats with attackers using legitimate tools like BitLocker and exploiting zero-days in Oracle E-Business Suite to compromise millions of records and disrupt essential services. Supply chain attacks continue through malicious packages targeting developers and security researchers while living-off-the-land techniques using legitimate monitoring tools evade detection, highlighting the critical need for immediate patching of actively exploited vulnerabilities in network infrastructure.
---

# Daily Threat Intel Digest - 2025-12-23

## 🔴 Critical Threats & Active Exploitation

**[NEW] Romanian water authority hit by ransomware disrupting 1,000 systems**  
Attackers used Windows BitLocker to encrypt systems at Romania's National Administration "Romanian Waters," impacting 10 of 11 regional offices. While operational technology remains unaffected, critical IT systems including GIS servers, databases, and DNS infrastructure were compromised. The attack vector remains unidentified, but the use of BitLocker as ransomware shows attackers repurposing legitimate encryption tools. Authorities are working to integrate water infrastructure into national cyber defense systems following this incident [[BleepingComputer](https://www.bleepingcomputer.com/news/security/romanian-water-authority-hit-by-ransomware-attack-over-weekend/); [Cyberpress](https://cyberpress.org/ransomware-1000-it-systems-affected/)]

**[NEW] University of Phoenix breach exposes 3.5 million records**  
The Clop ransomware gang exploited an Oracle E-Business Suite zero-day (CVE-2025-61882) to steal personal data including names, contact information, dates of birth, social security numbers, and banking details from 3,489,274 individuals. The breach was discovered on November 21 but occurred in August, demonstrating a three-month dwell time. The university is offering free identity protection services including credit monitoring and $1 million fraud reimbursement. This incident is part of Clop's broader campaign targeting Oracle EBS deployments across educational institutions [[BleepingComputer](https://www.bleepingcomputer.com/news/security/university-of-phoenix-data-breach-impacts-nearly-35-million-individuals/); [Cyberpress](https://cyberpress.org/university-of-phoenix-data-breach/)]

**[NEW] Malicious NPM package steals WhatsApp accounts and creates persistent backdoors**  
The "lotusbail" package, masquerading as a legitimate WhatsApp Web API library, has been downloaded over 56,000 times in six months. It captures authentication tokens, session keys, message histories, and contact lists while providing functional API capabilities. The package uses custom RSA encryption and four layers of obfuscation to exfiltrate data, and links attacker devices to victim accounts for persistent access even after removal. Developers must manually unlink all devices in WhatsApp to fully remediate the threat [[BleepingComputer](https://www.bleepingcomputer.com/news/security/malicious-npm-package-steals-whatsapp-accounts-and-messages/); [Cyberpress](https://cyberpress.org/malicious-npm-package/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Webrat malware disguised as exploits targets security researchers**  
Attackers are distributing Webrat backdoor through GitHub repositories posing as proof-of-concept exploits for high-CVSS vulnerabilities (CVE-2025-10294, CVE-2025-59295, CVE-2025-59230). The campaign uses AI-generated vulnerability reports and lures inexperienced security professionals with password-protected archives containing malicious executables. Webrat functions as a RAT with capabilities including cryptocurrency wallet theft, Discord/Steam account compromise, and surveillance through webcam and microphone. Researchers warn this tactic specifically targets those who bypass basic safety protocols by running exploits directly on host machines [[Malware.news](https://malware.news/t/from-cheats-to-exploits-webrat-spreading-via-github/102788#post_1)]

**[NEW] ClickFix attacks evolve with steganographic payload delivery**  
Huntress researchers identified new ClickFix campaigns using steganography to hide malicious shellcode within PNG images, evading traditional detection systems. The multi-stage infection chain delivers information stealers including LummaC2 and Rhadamanthys through PowerShell scripts and process injection into explorer.exe. Attackers employ fake Windows Update pages with realistic animations to increase victim compliance. Organizations should consider disabling the Windows Run dialog via Group Policy to block the initial infection vector [[Cyberpress](https://cyberpress.org/clickfix-attacks/)]

**[NEW] Nezha legitimate monitoring tool abused as stealthy RAT**  
Ontinue's Cyber Defense Center discovered attackers deploying Nezha, an open-source monitoring utility with 10,000 GitHub stars, as a post-exploitation tool. The legitimate agent runs with SYSTEM/root privileges and provides attackers with complete control while appearing as benign monitoring traffic. The abuse was discovered during incident investigation where a Bash script silently installed Nezha, connecting compromised endpoints to attacker-controlled infrastructure hosted on Alibaba Cloud. VirusTotal shows zero detections as the tool remains unmodified [[Cyberpress](https://cyberpress.org/nezha-monitoring-tool-attack/)]

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical RCE in WatchGuard Fireware OS under active exploitation**  
CISA has added CVE-2025-14733, an out-of-bounds write vulnerability in WatchGuard's IKEv2 VPN implementation (iked process), to the Known Exploited Vulnerabilities catalog. The flaw allows remote, unauthenticated attackers to execute arbitrary code on vulnerable Firebox appliances. Exploitation affects both Mobile User VPN and Branch Office VPN configurations with dynamic gateway peers enabled. Organizations must immediately update to patched versions: 2025.1.4, 12.11.6, 12.5.15, or 12.3.1_Update4 [[malware.news](https://malware.news/t/al25-020-vulnerability-impacting-watchguard-fireware-os-cve-2025-14733/102782)]

**[NEW] Windows Imaging Component RCE requires complex exploitation**  
CVE-2025-50165, a critical uninitialized function pointer vulnerability in WindowsCodecs.dll, affects JPG image compression routines during non-standard 12-bit/16-bit color processing. Successful exploitation requires both address leakage and heap control, making practical attacks unlikely against modern Windows systems. The vulnerability is triggered during image saving, thumbnail generation, or background re-encoding—not simply viewing images. Microsoft has patched the issue by properly initializing function pointers [[Cyberpress](https://cyberpress.org/windows-imaging-component-vulnerability/)]

**[NEW] CISA flags actively exploited DigiEver NVR authorization flaw**  
CVE-2023-52163, a missing authorization vulnerability in DigiEver DS-2105 Pro network video recorders, allows unauthenticated command injection through the time_tzsetup.cgi interface. With confirmed active exploitation, organizations must patch immediately or discontinue use of affected products. Federal agencies have until January 12, 2026, to apply mitigations under BOD 22-01. This vulnerability poses particular risk to organizations relying on surveillance and security monitoring infrastructure [[Cyberpress](https://cyberpress.org/cisa-flags-kev-catalog/)]

## 🛡️ Defense & Detection

**[NEW] New MacSync malware dropper bypasses macOS Gatekeeper**  
The latest MacSync infostealer variant uses a digitally signed and notarized Swift application to evade macOS Gatekeeper checks. The dropper, distributed as "zk-call-messenger-installer-3.9.2-lts.dmg," inflates the disk image to 25.5MB with decoy PDFs and performs connectivity checks to evade sandbox analysis. The malware steals iCloud keychain credentials, browser passwords, cryptocurrency wallet data, and files. Apple has revoked the fraudulent certificate following disclosure [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-macsync-malware-dropper-evades-macos-gatekeeper-checks/)]

**[NEW] Microsoft finally deprecates RC4 authentication**  
After 26 years, Microsoft is removing the last remaining RC4 encryption instances from Windows Server authentication. The outdated cipher's susceptibility to Kerberoasting attacks contributed to major breaches, including the Ascension healthcare incident that affected 5.6 million patients. The long-overdue deprecation eliminates a critical weakness that attackers have exploited for decades to compromise enterprise networks [[Schneier](https://www.schneier.com/blog/archives/2025/12/microsoft-is-finally-killing-rc4.html)]

## 📋 Policy & Industry News

**[NEW] NIST and MITRE launch $20M AI cybersecurity research effort**  
The partnership establishes two new research centers focused on AI applications in critical infrastructure protection. The AI Economic Security Center will specifically address threats against water, electricity, and other essential services, driving development of agentic AI solutions for defense. This initiative reflects growing concerns about AI-enabled threats against critical infrastructure and the need for specialized research to counter emerging attack vectors [[Cyberscoop](https://cyberscoop.com/nist-mitre-announce-20-million-dollar-research-effort-on-ai-cybersecurity/)]

**[UPDATE] Interpol-led operation decrypts 6 ransomware strains, arrests 574**  
Operation Sentinel, conducted between October 27 and November 27 across 19 countries, resulted in 574 arrests and $3 million recovered from business email compromise, extortion, and ransomware attacks. The action disrupted cybercrime cases connected to $21 million in losses, with notable successes including prevention of a $7.9 million BEC wire transfer and development of decryption tools recovering 30 TB of encrypted data in Ghana [[BleepingComputer](https://www.bleepingcomputer.com/news/security/interpol-led-action-decrypts-6-ransomware-strains-arrests-hundreds/)]