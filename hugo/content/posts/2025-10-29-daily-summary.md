---
title: Daily Threat Intelligence Briefing - October 29, 2025
date: 2025-10-29
tags: ["cybersecurity", "threat-intelligence", "daily-briefing"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Daily cybersecurity briefing covering 24 articles with 10 indicators of compromise
statistics:
  date: 2025-10-29
  total_articles: 24
  total_iocs: 10
  unique_sources: 6
  generation_method: template
sources: ["krebs-on-security", "infosecurity-magazine", "securityweek", "bleeping-computer", "erev0scom-personal-blog-page", "cyberscoop"]
---

Good morning, cybersecurity professionals!

Tia N. List here with your daily threat intelligence briefing. I've been monitoring the threat landscape across 6 different security sources, and there are 24 articles worth your attention today.

Let's dive into what you need to know...

---

# Daily Threat Intelligence Briefing
*Published: October 29, 2025 at 02:04 PM*

## Executive Summary

Today's threat landscape shows:
- **Vulnerability Exploitation**: 2 articles (8.3% of coverage)
- **Botnet / Ddos**: 1 articles (4.2% of coverage)
- **Supply Chain Malware / Credential Theft**: 1 articles (4.2% of coverage)

## High-Priority Threats

### 1. Aisuru Botnet Shifts from DDoS to Residential Proxies

**Source:** Krebs On Security
**Score:** 92/100
**Category:** Botnet / Ddos

**Summary:** The Aisuru botnet, originally known for record‑breaking DDoS attacks, has pivoted to renting out infected IoT devices as residential proxies. The botnet now supplies a large pool of IP addresses that enable data‑harvesting and AI training operations while evading detection.

**[Read more](https://krebsonsecurity.com/2025/10/aisuru-botnet-shifts-from-ddos-to-residential-proxies/)**

### 2. Npm Malware Uses Invisible Dependencies to Infect Dozens of Packages

**Source:** Infosecurity Magazine
**Score:** 90/100
**Category:** Supply Chain Malware / Credential Theft

**Summary:** Koi Security uncovered the PhantomRaven malware campaign that infects npm packages via Remote Dynamic Dependencies, stealing npm tokens, GitHub credentials, and CI/CD secrets. The campaign has infected 126 packages with over 86,000 downloads.

**[Read more](https://www.infosecurity-magazine.com/news/npm-malware-invisible-dependencies/)**

### 3. New Atroposia RAT Surfaces on Dark Web

**Source:** Infosecurity Magazine
**Score:** 90/100
**Category:** Malware/Rat

**Summary:** A new remote access trojan, Atroposia, has been discovered on the dark web. It offers encrypted command channels, credential and wallet theft, DNS hijacking, local vulnerability scanning, and hidden remote desktop takeover. The RAT is sold as a modular toolkit and can be combined with other malicious services such as SpamGPT and MatrixPDF.

**[Read more](https://www.infosecurity-magazine.com/news/new-atroposia-rat-surfaces-on-dark/)**

### 4. CISA Warns of Exploited DELMIA Factory Software Vulnerabilities

**Source:** Securityweek
**Score:** 90/100
**Category:** Software Vulnerability Exploitation

**Summary:** CISA warns that two high‑severity vulnerabilities (CVE‑2025‑6204 and CVE‑2025‑6205) in Dassault Systèmes’ DELMIA Apriso factory software have been actively exploited. Attackers chain a code‑injection flaw with a missing‑authorization bug to create privileged accounts and upload malicious executables to the web root, compromising manufacturing operations.

**[Read more](https://www.securityweek.com/cisa-warns-of-exploited-delmia-factory-software-vulnerabilities/)**

### 5. Qilin ransomware abuses WSL to run Linux encryptors in Windows

**Source:** Bleeping Computer
**Score:** 90/100
**Category:** Ransomware

**Summary:** The Qilin ransomware gang now runs Linux‑based encryptors inside Windows via Windows Subsystem for Linux (WSL) to evade detection. It also uses remote‑access tools, legitimate utilities, and signed vulnerable drivers (BYOVD) to disable security software before encrypting data.

**[Read more](https://www.bleepingcomputer.com/news/security/qilin-ransomware-abuses-wsl-to-run-linux-encryptors-in-windows/)**

## Indicators of Compromise (IOCs)

### Kb Number

- **KB5050094** (Confidence: high)
  - *Preview cumulative update causing the issue*
- **KB5067036** (Confidence: high)
  - *Fix update released to resolve the issue*

### Cve

- **CVE-2022-47945** (Confidence: medium)
- **CVE-2021-3129** (Confidence: medium)
- **CVE-2017-9841** (Confidence: medium)
- **CVE-2025-24893** (Confidence: medium)
- **CVE-2025-6205** (Confidence: medium)

### Error Code

- **0x800F081F** (Confidence: high)
  - *Windows update failure on Windows 11 24H2*

### File

- **eskle.sys** (Confidence: medium)

## All Tracked Articles

**Aisuru Botnet Shifts from DDoS to Residential Proxies**
- *Source:* Krebs On Security
- *Score:* 92/100 | *Category:* Botnet / Ddos
- *URL:* https://krebsonsecurity.com/2025/10/aisuru-botnet-shifts-from-ddos-to-residential-proxies/

**Npm Malware Uses Invisible Dependencies to Infect Dozens of Packages**
- *Source:* Infosecurity Magazine
- *Score:* 90/100 | *Category:* Supply Chain Malware / Credential Theft
- *URL:* https://www.infosecurity-magazine.com/news/npm-malware-invisible-dependencies/

**New Atroposia RAT Surfaces on Dark Web**
- *Source:* Infosecurity Magazine
- *Score:* 90/100 | *Category:* Malware/Rat
- *URL:* https://www.infosecurity-magazine.com/news/new-atroposia-rat-surfaces-on-dark/

**CISA Warns of Exploited DELMIA Factory Software Vulnerabilities**
- *Source:* Securityweek
- *Score:* 90/100 | *Category:* Software Vulnerability Exploitation
- *URL:* https://www.securityweek.com/cisa-warns-of-exploited-delmia-factory-software-vulnerabilities/

**Qilin ransomware abuses WSL to run Linux encryptors in Windows**
- *Source:* Bleeping Computer
- *Score:* 90/100 | *Category:* Ransomware
- *URL:* https://www.bleepingcomputer.com/news/security/qilin-ransomware-abuses-wsl-to-run-linux-encryptors-in-windows/

**PhantomRaven attack floods npm with credential-stealing packages**
- *Source:* Bleeping Computer
- *Score:* 85/100 | *Category:* Credential Theft / Supply Chain Attack
- *URL:* https://www.bleepingcomputer.com/news/security/phantomraven-attack-floods-npm-with-credential-stealing-packages/

**MITRE Unveils ATT&CK v18 With Updates to Detections, Mobile, ICS**
- *Source:* Securityweek
- *Score:* 85/100 | *Category:* Threat Intelligence
- *URL:* https://www.securityweek.com/mitre-unveils-attck-v18-with-updates-to-detections-mobile-ics/

**PHP Servers and IoT Devices Face Growing Cyber-Attack Risks**
- *Source:* Infosecurity Magazine
- *Score:* 85/100 | *Category:* Botnet/Infrastructure Exploitation
- *URL:* https://www.infosecurity-magazine.com/news/php-servers-and-iot-devices-cyber/

**XWiki Vulnerability Exploited in Cryptocurrency Mining Operation**
- *Source:* Securityweek
- *Score:* 85/100 | *Category:* Vulnerability Exploitation
- *URL:* https://www.securityweek.com/xwiki-vulnerability-exploited-in-cryptocurrency-mining-operation/

**Ad and PR Giant Dentsu Says Hackers Stole Merkle Data**
- *Source:* Securityweek
- *Score:* 85/100 | *Category:* Data Breach / Exfiltration
- *URL:* https://www.securityweek.com/ad-and-pr-giant-dentsu-says-hackers-stole-merkle-data/

## References

All source articles are available for detailed analysis:

- **Krebs on Security**: https://krebsonsecurity.com/feed/
- **Infosecurity Magazine**: https://www.infosecurity-magazine.com/rss/news/
- **SecurityWeek**: https://www.securityweek.com/rss.xml
- **Bleeping Computer**: https://www.bleepingcomputer.com/feed/
- **erev0s.com personal blog page**: https://erev0s.com/rss/
- **CyberScoop**: https://www.cyberscoop.com/feed/