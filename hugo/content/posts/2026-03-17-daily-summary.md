---
title: Handala wiper attack 💀, Chrome 0-day exploitation 🌐, RondoDox botnet exploits 🤖, Teams phishing hijack 🎣, The Gentlemen ransomware 💰
date: 2026-03-17
tags: ["ransomware","apt activity","zero-day vulnerabilities","iot botnet","spear-phishing","data wiper","credential theft","cloud security","government sector","healthcare"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: The Iran-aligned Handala group executed a destructive attack on Stryker by abusing Microsoft Intune administrative privileges to wipe tens of thousands of devices, while actively exploited Chrome zero-day vulnerabilities require immediate patching to prevent drive-by attacks. Organizations face concurrent threats from the RondoDox botnet weaponizing 174 exploits against edge infrastructure, credential harvesting campaigns hijacking legitimate websites for Microsoft Teams phishing, and The Gentlemen ransomware targeting global victims including critical infrastructure.
---
# Daily Threat Intel Digest - 2026-03-17

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Stryker confirms Intune abuse in massive wiper attack**
Investigators revealed that the destructive cyberattack against medical technology giant Stryker was executed without malware by abusing legitimate administrative tools. Attackers gained Global Administrator privileges in Stryker's Microsoft Intune environment and used the platform's built-in remote wipe functionality to factory reset nearly 80,000 corporate devices simultaneously. The Iran-aligned Handala group claimed responsibility, stating they wiped over 200,000 systems and exfiltrated 50 TB of data, though investigators found no evidence of data theft. Stryker confirmed its medical devices and clinical systems, which are segregated from the corporate Microsoft environment, remain operational [[BleepingComputer](https://www.bleepingcomputer.com/news/security/stryker-attack-wiped-tens-of-thousands-of-devices-no-malware-needed/); [Cyberpress](https://cyberpress.org/stryker-confirms-massive-wiper-attack/)].

**[UPDATE] CISA flags actively exploited Chrome 0-days**
CISA has added two critical zero-day vulnerabilities in Google Chrome to its Known Exploited Vulnerabilities (KEV) catalog following confirmation of in-the-wild exploitation. CVE-2026-3909 is an out-of-bounds write flaw in the Skia graphics engine, while CVE-2026-3910 involves improper memory buffer restrictions in the V8 JavaScript engine. Both flaws allow attackers to achieve arbitrary code execution via a specially crafted HTML page. Federal agencies have until March 27, 2026, to apply patches, but all organizations are urged to update immediately due to the risk of drive-by download attacks [[Cyberpress](https://cyberpress.org/cisa-chrome-0-day-vulnerabilities/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] "CamelClone" espionage campaign targets government sectors**
A new cyberespionage campaign dubbed "CamelClone" is actively targeting defense, diplomatic, and energy entities in Algeria, Mongolia, Ukraine, and Kuwait. The threat actors use spear-phishing emails containing malicious ZIP archives with disguised LNK files to infect systems. Notably, the campaign lacks traditional C2 servers; instead, it uses the legitimate `rclone` tool to exfiltrate sensitive data directly to anonymous MEGA cloud storage accounts, blending malicious traffic with normal web activity [[Cyberpress](https://cyberpress.org/camelclone-hits-governments/)].

**[UPDATE] Handala group expands destructive operations beyond Stryker**
Following the attack on Stryker, new intelligence highlights the Iran-linked Handala group's (Void Manticore) evolving tactics, including the use of zero-trust networking tools like NetBird and RDP for lateral movement. Polish officials suspect Iranian actors are also responsible for a recent attack on the country's National Atomic Energy Agency, though attribution remains under investigation. Handala's destructive toolkit includes custom wipers and AI-assisted PowerShell scripts designed to maximize operational disruption [[Cyberpress](https://cyberpress.org/handala-wipers-hit-networks/); [Security Boulevard](https://securityboulevard.com/2026/03/poland-suspects-iranian-actors-are-behind-attack-on-its-nuclear-power-center/)].

**[NEW] RondoDox botnet weaponizes 174 exploits against network edge**
The RondoDox botnet has emerged as a significant threat to network infrastructure, leveraging an arsenal of 174 different exploits to compromise IoT and edge devices. Initially observed using a "shotgun approach" with numerous exploits, the botnet has streamlined its operations to focus on highly effective vulnerabilities like React2Shell (CVE-2025-55182), often exploiting flaws before official CVEs are published. The botnet targets a wide range of architectures including ARM, MIPS, and x86 to conduct DDoS attacks [[Cyberpress](https://cyberpress.org/rondodox-abuses-residential-ips/)].

**[UPDATE] Microsoft Teams phishing leverages hijacked websites**
The ongoing phishing campaign abusing Microsoft Teams—previously attributed to Storm-1811—relies on hijacking legitimate WordPress websites to host credential-harvesting pages. By embedding malicious phishing kits within trusted domains (e.g., `/wp-includes/` or `/config/` directories), attackers bypass traditional email filters and domain reputation checks. The campaign uses lures such as "missed voicemail" notifications and urgent document sharing alerts to steal credentials from corporate users [[Cyberpress](https://cyberpress.org/attackers-hijack-legitimate-websites-to-target-microsoft-teams-users/)].

**[NEW] "The Gentlemen" ransomware claims spree of global victims**
The ransomware group known as "The Gentlemen" has claimed responsibility for attacks on five organizations within a single day, including Canal Capital (Colombia), Chase Asia (Thailand), Kabelovna Kabex (Czech Republic), Corporación Colina (Chile), and Payap University (Thailand). The group is threatening to leak stolen data unless ransom demands are met. The targeting of Kabelovna Kabex, a manufacturer of cables for nuclear power plants, raises concerns about critical infrastructure targeting alongside the financial and education sectors [[DeXpose via Malware.News](https://malware.news/t/the-gentlemen-ransomware-attack-on-canal-capital/105009#post_1)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Palo Alto Cortex XDR BIOC rules susceptible to decryption**
Security researchers have disclosed a technique to decrypt the Behavioral Indicators of Compromise (BIOC) rules used by Palo Alto Cortex XDR agents. The analysis revealed that AES-256-CBC encryption used a static key structure, allowing researchers to decrypt rules and identify hardcoded global whitelist conditions (e.g., specific command-line strings) that could be abused for evasion. Palo Alto Networks addressed the issue in agent version 9.1 (released late Feb 2026) by modifying the key derivation process and removing exploitable whitelists [[Cyberpress](https://cyberpress.org/researchers-reveal-technique-to-decrypt-and-exploit-cortex-xdr-bioc-rules/)].

**[NEW] HPE warns of critical RCE in Telco Service Orchestrator**
HPE has released a security advisory (AV26-244) for a remote buffer overflow vulnerability affecting HPE Telco Service Orchestrator versions prior to v4.2.12. The flaw (HPESBNW05029) could allow remote attackers to execute arbitrary code, posing a severe risk to telecommunications service providers utilizing the orchestration platform [[Canadian Centre for Cyber Security](https://malware.news/t/hpe-security-advisory-av26-244/104998#post_1)].

## ⚡ Quick Hits

*   **Malicious NPM packages spread PylangGhost RAT:** A supply chain campaign is delivering the North Korean-linked PylangGhost RAT via malicious packages such as `math-service` and `react-refresh-update`, targeting developers on Windows, Linux, and macOS [[GBHackers](https://gbhackers.com/pylangghost-rat/)].
*   **Fake Telegram installer distributes malware:** A typosquatting campaign using domains like `telegrgam[.]com` is distributing a malicious installer that disables Windows Defender, drops payloads, and establishes C2 via `jiijua[.]com` [[K7 Labs via Malware.News](https://malware.news/t/fake-telegram-malware-campaign-analysis-of-a-multi-stage-loader-delivered-via-typosquatted-websites/105011#post_1)].
*   **Convicted scammer targets athletes from prison:** A Georgia man allegedly ran a social engineering scheme from federal prison, impersonating an adult film star to trick professional athletes into handing over iCloud credentials and MFA codes [[CyberScoop](https://cyberscoop.com/nba-nfl-athletes-social-engineering-scheme-apple-icloud-mfa/)].