---
title: FortiCloud SSO bypass 🔓, Chinese APT Cisco zero-day 🎯, OAuth phishing attacks 📧, Sinobi ransomware extortion 💰, UEFI firmware flaws ⚙️
date: 2025-12-20
tags: ["authentication bypass","zero-day exploitation","apt groups","oauth phishing","ransomware","firmware vulnerabilities","network appliances","email security","deepfake","device authentication"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical authentication bypass vulnerabilities in FortiCloud SSO devices and a Cisco zero-day exploited by Chinese APT groups put thousands of organizations at risk of complete network compromise. OAuth phishing attacks against Microsoft 365, Sinobi ransomware double extortion campaigns, and UEFI firmware vulnerabilities affecting major motherboards demonstrate the diverse attack surface requiring immediate attention.
---

# Daily Threat Intel Digest - December 20, 2025

## 🔴 Critical Threats & Active Exploitation

**[NEW] 25,000+ FortiCloud SSO Devices Exposed to Critical Bypass Flaws**  
Over 25,000 internet-facing Fortinet devices with FortiCloud SSO enabled are vulnerable to critical authentication bypass vulnerabilities (CVE-2025-59718 and CVE-2025-59719). CVE-2025-59718 is already in CISA's Known Exploited Vulnerabilities Catalog, indicating active exploitation. Attackers can bypass authentication to gain unauthorized access, putting organizations at risk of complete network compromise. The Shadowserver Foundation is actively notifying affected entities, and immediate patching is required [[CyberPress](https://cyberpress.org/forticloud-sso-exposure-leaves-25000-devices-vulnerable/); [GBHackers](https://gbhackers.com/25000-forticloud-sso-enabled-systems-vulnerable/)].

**[UPDATE] Cisco Email Gateway Zero-Day Exploited by Chinese APT**  
The newly identified CVE-2025-20393 (CVSS 10.0) is being actively exploited in attacks targeting Cisco Secure Email Gateway appliances with Spam Quarantine enabled. China-nexus threat actor UAT-9685 leverages this flaw to execute arbitrary commands with root privileges, establishing persistent backdoors. This continues a trend of APT groups targeting network appliances for espionage [[Arctic Wolf](https://arcticwolf.com/resources/blog/cve-2025-20393/); [Eclypsium](https://eclypsium.com/news/cisco-secure-email-gateway-under-siege-cve-2025-20393-cvss-10-exploited-in-the-wild-by-chinese-apt/)].

**[UPDATE] Gladinet Triofox Zero-Day Allows SYSTEM-Level RCE**  
Critical vulnerability CVE-2025-12480 in Gladinet's Triofox platform enables unauthenticated remote code execution through a complex 20-step exploit chain. Threat group UNC6485 leveraged local host header injection to access admin setup pages, then abused built-in antivirus features to execute malicious scripts. Affected organizations should patch immediately and investigate for signs of compromise, as exploitation leaves minimal forensic artifacts [[CyberPress](https://cyberpress.org/gladinet-triofox-0-day-vulnerability/); [VulnCheck](https://www.vulncheck.com/blog/triofox-exploit-cve-2025-12480/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Sinobi Ransomware Claims Double Extortion Attacks**  
The newly observed Sinobi ransomware group has claimed attacks on Italian refrigeration leader Fhiaba S.r.l. and Canadian biblical storytelling organization NBS Canada. The group threatens to publish stolen data unless negotiations begin, marking its emergence as an active extortion-focused operation. Unlike typical ransomware, Sinobi focuses on data theft rather than encryption [[DeXpose](https://www.dexpose.io/sinobi-ransomware-targets-italian-refrigeration-leader-fhiaba-s-r-l/); [DeXpose](https://www.dexpose.io/sinobi-ransomware-targets-nbs-canada/)].

**[NEW] FBI: Deepfake Impersonation of U.S. Officials Dating to 2023**  
An ongoing campaign uses AI voice cloning and encrypted messaging apps to impersonate senior U.S. government officials, targeting individuals including officials' family members. Attackers use credential harvesting requests and contact list access to enable further targeting. The FBI's revised timeline reveals activity began under the previous administration, with campaigns leveraging Signal and WhatsApp to lend credibility [[CyberScoop](https://cyberscoop.com/fbi-says-ongoing-deepfake-impersonation-of-us-officials-dates-back-to-2023/); [IC3](https://www.ic3.gov/PSA/2025/PSA251219)].

**[NEW] Wave of OAuth Device Code Phishing Targets Microsoft 365**  
Multiple threat groups, including financially motivated TA2723 and suspected Russia-aligned UNK_AcademicFlare, are exploiting OAuth device code authorization flows to bypass MFA. Attackers trick victims into entering device codes on legitimate Microsoft login pages, granting attackers persistent account access. Campaigns use phishing kits like SquarePhish and Graphish, with significant volume increases since September [[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-365-accounts-targeted-in-wave-of-oauth-phishing-attacks/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] UEFI Flaw Enables Pre-Boot DMA Attacks on Major Motherboards**  
A critical UEFI firmware vulnerability (CVE-2025-11901, CVE-2025-14302/14303/14304) affects ASUS, Gigabyte, MSI, and ASRock motherboards, allowing DMA attacks before IOMMU protection initializes. Malicious PCIe devices can read/write system memory during boot, bypassing OS security. Riot Games' Vanguard anti-cheat blocks vulnerable systems from launching Valorant. Firmware updates are required [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-uefi-flaw-enables-pre-boot-attacks-on-motherboards-from-gigabyte-msi-asus-asrock/); [CERT/CC](https://www.kb.cert.org/vuls/id/382314)].

**[NEW] HPE UOCAM Vulnerabilities Require Urgent Patching**  
HPE addressed multiple undisclosed vulnerabilities in Unified OSS Console Assurance Monitoring (UOCAM) versions prior to 3.1.19. While exploit details are limited, centralized server management tools are high-value targets for attackers seeking persistence. Organizations should review HPESBNW04989 and apply updates promptly [[Malware.news](https://malware.news/t/hpe-security-advisory-av25-853/102744#post_1)].