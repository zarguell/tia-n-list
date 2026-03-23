---
title: IP-KVM BIOS attacks 🔴, VoidStealer Chrome bypass 🎭, supply chain breaches 💔, DarkSword iOS espionage 📱, Telegram C2 operations 📨
date: 2026-03-23
tags: ["ip-kvm vulnerabilities","infostealer","supply chain attack","ios exploits","apt activity","iranian threat actors","c2 infrastructure","docker compromise","data breach"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: IP-KVM BIOS-level attacks and VoidStealer's Chrome ABE bypass demonstrate how low-cost hardware and debugger-based techniques can bypass traditional endpoint security to gain system control or steal sensitive data. Supply chain breaches and compromised Docker images highlight third-party risks while Iranian threat actors leveraging Telegram for C2 and LAPSUS$ extortion attempts show evolving attack methods.
---
# Daily Threat Intel Digest - 2026-03-23

## 🔴 Critical Threats & Active Exploitation

**[NEW] $30 IP-KVM Vulnerabilities Expose Enterprises to BIOS-Level Attacks**
Low-cost IP-KVM (Keyboard, Video, Mouse) devices used for remote management are exposing enterprises to BIOS-level compromises due to nine critical vulnerabilities across vendors GL-iNet, Angeet, Sipeed, and JetKVM. Because these devices operate below the operating system, attackers exploiting flaws like the unauthenticated file upload in the Angeet ES3 KVM (CVE-2026-32297, CVSS 9.8) can bypass endpoint security, inject keystrokes, and deploy ransomware without detection. Internet-exposed IP-KVMs have surged from 404 to over 1,600 in less than a year, creating a growing blind spot where a single compromised $30 device grants attackers full control over every connected machine [[CyberPress](https://cyberpress.org/30-ip-kvm-vulnerabilities/); [GBHackers](https://gbhackers.com/30-ip-kvm-flaws-could-enable-bios/)].

**[NEW] VoidStealer Bypasses Chrome ABE Without Injection or Privileges**
A new variant of the VoidStealer malware (v2.0) has become the first infostealer in the wild to bypass Google Chrome's Application-Bound Encryption (ABE) without requiring code injection or SYSTEM-level privileges. The malware attaches as a debugger to the browser process, using hardware breakpoints to intercept the master encryption key during the brief moment it is loaded into memory in plaintext during startup. This technique allows attackers to extract passwords, cookies, and sensitive data even on systems protected by Chrome's strongest data safeguards, rendering many traditional endpoint defenses ineffective against this "debugger-based" extraction method [[CyberPress](https://cyberpress.org/voidstealer-evades-chrome-abe/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/voidstealer-malware-steals-chrome-master-key-via-debugger-trick/); [GBHackers](https://gbhackers.com/voidstealer-steals-chrome/)].

**[NEW] Crunchyroll Breach Exposes 100GB of User Data via Supply Chain**
Threat actors claim to have exfiltrated 100GB of user data from Crunchyroll, including IP addresses, emails, and credit card information, by compromising an employee workstation at Telus, a third-party business process outsourcing (BPO) provider. The breach highlights the risks of BPO partnerships, as attackers leveraged access to Telus's environment to pivot into Crunchyroll's customer support and ticketing infrastructure. Crunchyroll has reportedly not acknowledged the incident, leaving users vulnerable to targeted phishing and financial fraud as the stolen data is allegedly circulated for sale [[CyberPress](https://cyberpress.org/crunchyroll-breach-hackers-claim-100gb-of-user-data-stolen/); [GBHackers](https://gbhackers.com/crunchyroll-data-breach/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] CISA Orders Patching for Actively Exploited DarkSword iOS Flaws**
Following recent reports of the DarkSword iOS exploit chain being used in espionage campaigns, CISA has added three vulnerabilities (CVE-2025-31277, CVE-2025-43510, CVE-2025-43520) to the Known Exploited Vulnerabilities (KEV) catalog, mandating federal agencies patch by April 3. New intelligence links the exploit chain to Russian threat actors (UNC6353) and commercial surveillance vendors, utilizing malware families like "GhostBlade" and "GhostKnife" to steal data from iPhones. While the attack chain is sophisticated, it currently only affects iOS versions 18.4 through 18.7, and Apple has released patches in recent updates [[CyberPress](https://cyberpress.org/apple-flaws-darksword-ios-attack-chain/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-orders-feds-to-patch-darksword-ios-flaws-exploited-attacks/)].

**[UPDATE] TeamPCP Supply Chain Attack Expands to New Docker Images**
The ongoing TeamPCP supply chain campaign has escalated with the discovery of two new compromised Docker image tags (0.69.5 and 0.69.6) for the Trivy vulnerability scanner on Docker Hub. These unauthorized images, lacking corresponding GitHub releases, expand the attack surface of the campaign, which also includes the "CanisterWorm" malware hijacking npm publisher accounts. Security teams must verify image integrity, as these compromised components are designed to deploy persistent backdoors within development environments [[GBHackers](https://gbhackers.com/trivy-supply-chain/); [GBHackers](https://gbhackers.com/canisterworm-hijacks-npm/)].

**[UPDATE] Iranian Handala Group Weaponizes Telegram for C2 Operations**
The FBI has issued a flash alert warning that Iranian state-sponsored threat actors, specifically the Handala hacktivist group and Homeland Justice, are now using Telegram as command-and-control (C2) infrastructure in malware attacks targeting dissidents and journalists. This TTP shift follows the FBI's seizure of four domains used by the group and their destructive attack on Stryker, where they wiped 80,000 devices using Microsoft Intune. Defenders are advised to monitor for unusual traffic to Telegram endpoints and block access if not business-required [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-warns-of-handala-hackers-using-telegram-in-malware-attacks/)].

**[NEW] LAPSUS$ Resurfaces, Claims AstraZeneca Data Breach**
The LAPSUS$ hacking group has re-emerged, claiming to have breached AstraZeneca's internal systems and exfiltrated 3GB of sensitive data, including source code, Terraform configurations, and CI/CD pipeline secrets. Unlike their previous high-profile dumps, the group is adopting a "pay-to-access" extortion model, selling the data via encrypted links rather than publishing it publicly. If verified, the exposure of cryptographic keys and infrastructure-as-code could allow attackers to pivot into AstraZeneca's cloud environments and supply chain portals [[CyberPress](https://cyberpress.org/lapsus-breach-of-astrazenecas/); [GBHackers](https://gbhackers.com/astrazeneca-data-breach-allegedly-claimed-by-lapsus/)].

## ⚠️ Vulnerabilities & Patches

**[UPDATE] Oracle Releases Emergency Patch for Critical Identity Manager Flaw**
Oracle has released an out-of-band security patch for a critical vulnerability in Oracle Identity Manager, addressing a zero-day flaw that was previously reported as being actively exploited by ransomware groups. While specific CVE details were not immediately available in the provided summary, vendors strongly recommend applying this update immediately to prevent unauthorized access and privilege escalation within identity management systems [[SecurityWeek](https://www.securityweek.com/oracle-releases-emergency-patch-for-critical-identity-manager-vulnerability/)].

**[NEW] Critical QNAP QVR Pro Flaw Enables Remote System Takeover**
QNAP has released a security advisory (QSA-26-07) for a critical vulnerability in its QVR Pro video surveillance application that allows unauthenticated remote attackers to gain full system access. Given QNAP's history of being targeted by ransomware groups like DeadBolt, administrators should prioritize patching this flaw to prevent devices from being hijacked for data exfiltration or as a launchpad for further network attacks [[GBHackers](https://gbhackers.com/critical-qnap-qvr-pro-flaw/)].