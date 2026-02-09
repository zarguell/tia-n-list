---
title: Fortinet zero-days 🚨, Qilin oil pipeline attack 🛢️, Git metadata exposure 📂, Black Basta BYOVD 💣, Signal espionage 📱
date: 2026-02-09
tags: ["zero-day vulnerabilities","ransomware","critical infrastructure","data exposure","state-sponsored actors","byovd technique","supply chain attack","phishing","endpoint security","espionage"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical zero-day vulnerabilities in Fortinet and BeyondTrust products enable unauthenticated remote code execution while Qilin ransomware compromises Romania's oil pipeline operator through stolen credentials. Black Basta advances defense evasion with Bring Your Own Vulnerable Driver techniques, 5+ million Git servers expose repository metadata, and state-sponsored actors leverage Signal for espionage against European officials.
---

# Daily Threat Intel Digest - February 9, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical SQL injection in Fortinet FortiClient EMS enables unauthenticated RCE**  
Attackers can exploit a newly disclosed SQL injection vulnerability (CVE-2026-21643) in Fortinet's FortiClient EMS to achieve remote code execution without authentication. The flaw carries a CVSS score of 9.1 and affects organizations using the endpoint management server for centralized client deployment and management. Successful exploitation allows attackers to execute arbitrary commands, potentially leading to full network compromise of managed endpoints [[GBHackers](https://gbhackers.com/critical-fortinet-forticlient-ems-vulnerability/)].

**[NEW] BeyondTrust remote access products hit by critical 0-day RCE**  
A zero-day vulnerability (CVE-2026-1731) with a CVSS score of 9.9 is actively impacting BeyondTrust's Remote Support and Privileged Remote Access solutions. The vulnerability permits unauthenticated remote code execution on self-hosted deployments, putting thousands of organizations at risk of immediate compromise. BeyondTrust has issued an urgent advisory but patches are not yet available for all affected configurations [[GBHackers](https://gbhackers.com/beyondtrust-remote-access-0-day-rce/)].

**[NEW] Romanian oil pipeline operator compromised in Qilin ransomware attack**  
Qilin ransomware group has successfully breached Romania's national oil pipeline operator Conpet, claiming theft of nearly 1TB of sensitive data including financial records and internal documents. The attack, which disrupted technology infrastructure but spared oil transport operations, originated from an infostealer infection on an IT administrator's personal computer weeks earlier. Attackers leveraged stolen VPN and WSUS credentials to achieve domain compromise [[InfoStealers](https://www.infostealers.com/article/romanias-oil-pipeline-operator-hacked-how-an-infostealer-infection-paved-the-way-for-qilins-ransomware-attack/); [DataBreaches.Net](https://databreaches.net/2026/02/08/romanias-oil-pipeline-operator-confirms-cyberattack-as-hackers-claim-data-theft/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Vortex Werewolf targets Russian entities with Tor-enabled backdoors**  
A threat cluster tracked as "Vortex Werewolf" (aka SkyCloak) is actively targeting Russian government and defense organizations with sophisticated backdoor capabilities. The campaign delivers Tor-enabled RDP, SMB, SFTP, and SSH backdoors through highly credible phishing links masquerading as legitimate Telegram file-sharing resources. The use of multiple Tor-based access methods complicates detection and remediation efforts for targeted organizations [[GBHackers](https://gbhackers.com/vortex-werewolf/)].

**[NEW] Black Basta ransomware incorporates BYOVD technique to evade defenses**  
Black Basta has adopted a Bring Your Own Vulnerable Driver (BYOVD) technique to disable security software before encryption. Unlike previous campaigns that used separate tools for defense evasion, the ransomware now bundles a vulnerable driver directly in the payload, allowing it to terminate antivirus processes without additional binaries. This evolution increases detection difficulty and represents a significant tactical advancement for the group [[GBHackers](https://gbhackers.com/black-basta-ransomware-2/)].

**[NEW] State-sponsored hackers target European officials via Signal**  
Suspected state-sponsored actors are conducting coordinated espionage campaigns against military officials, diplomats, politicians, and journalists across Europe using Signal and other messenger services. German security agencies (BfV and BSI) have issued warnings about these social engineering attacks, which leverage trusted platforms to establish initial footholds for intelligence gathering operations [[GBHackers](https://gbhackers.com/hackers-target-military-officials/); [Malware.news](https://malware.news/t/german-security-agencies-warn-of-state-sponsored-phishing-attacks-via-messenger-services/103940)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Over 5 million misconfigured Git web servers expose repository metadata**  
A massive security misconfiguration has exposed the .git repository metadata of nearly 5 million web servers worldwide. The暴露 allows attackers to download entire source code repositories, including credentials, API keys, and sensitive configuration files. Research indicates this widespread misconfiguration affects organizations across all sectors, creating an easily exploitable attack surface for data theft and system compromise [[GBHackers](https://gbhackers.com/over-5-million-misconfigured-git-web-servers-found-exposing/)].

**[NEW] New Telegram phishing scam hijacks platform authentication flow**  
Attackers have developed a sophisticated phishing operation that integrates directly with Telegram's official API infrastructure. By registering their own API credentials, attackers create malicious login flows that capture fully authorized user sessions without requiring password theft. This approach bypasses traditional phishing defenses and enables persistent access to user communications and contacts [[GBHackers](https://gbhackers.com/telegram-phishing-scam/)].

## 🛡️ Defense & Detection

**[NEW] Crypto Scanner tool identifies quantum-vulnerable cryptography in codebases**  
Quantum Shield Labs has released Crypto Scanner, a free open-source CLI tool that scans source code for algorithms vulnerable to quantum attacks. The tool supports 14 programming languages and config files, classifying risks by quantum threat level from critical (RSA, ECC) to low (AES-256, ML-KEM). With Q-Day projected around 2033, this tool helps organizations begin migration to post-quantum cryptography before "harvest now, decrypt later" attacks become practical [[Cyberpress](https://cyberpress.org/detect-quantum-vulnerable-cryptography/); [GBHackers](https://gbhackers.com/new-crypto-scanner-tool-helps-developers-identify-quantum-risks/)].

**[NEW] Windows Minifilter framework enables deep ransomware detection**  
A new proof-of-concept tool demonstrates how Windows Minifilters can intercept file system operations at the OS level to detect ransomware encryption before data loss occurs. Part of the "Sanctum" EDR strategy, this approach provides visibility into malicious file manipulation activities that traditional security tools might miss, offering organizations an additional layer of defense against modern ransomware [[GBHackers](https://gbhackers.com/detecting-ransomware-using-windows-minifilters/)].

## 📋 Policy & Industry News

**[NEW] FCC urges communications providers to implement ransomware defenses**  
The FCC has issued public notice DA 26-96 highlighting best practices for defending against ransomware attacks in the communications sector. The Bureau recommends implementing network segmentation, multi-factor authentication, regular data backups, and incident response plans to protect critical communications infrastructure from increasing ransomware threats [[Malware.news](https://malware.news/t/fcc-cybersecurity-alert-and-recommendations-to-commuunications-providers/103936)].

**[NEW] VirusTotal integration enhances AI marketplace security**  
OpenClaw has partnered with VirusTotal to implement multi-layer threat scanning for AI agent skills submitted to its ClawHub marketplace. The integration combines traditional file analysis with AI-powered code inspection using Google's Gemini LLM, flagging malicious skills that attempt data exfiltration or unauthorized command execution. Daily re-scanning of live skills helps address evolving threats in the rapidly expanding AI agent ecosystem [[Cyberpress](https://cyberpress.org/virustotal-integrates-with-openclaw-to-enhance/); [GBHackers](https://gbhackers.com/openclaw-virustotal-safeguard-ai-agent-skill-ecosystem/)].