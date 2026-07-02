---
title: "🦂 Scattered Spider Extradition, 🔴 FortiBleed-Lynx Link, 🏛️ DHS HSIN Breach, 🍫 ChocoPoC Malware, 🍎 Apple Email Leak"
date: 2026-07-02
tags: ["scattered-spider","fortibleed","lynx-ransomware","dhs-hsin","chocopoc","shinyhunters","oracle-ebs","apple-privacy","cisa-kev","sharepoint"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Scattered Spider member extradited; FortiBleed credential theft linked to INC/Lynx ransomware; DHS HSIN info-sharing platform breached; ChocoPoC malware targets researchers; Apple Hide My Email vulnerability unfixed; CISA adds SharePoint RCE to KEV; 950+ Oracle EBS instances exposed."
---
# Daily Threat Intelligence Digest — July 2, 2026

*18 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Alleged Scattered Spider Member Extradited to United States — 19-Year-Old Linked to $100M+ Ransomware Operation**

A dual US-Estonian citizen, 19-year-old Peter Stokes, has been extradited from Finland to the United States to face charges for his membership in the Scattered Spider hacking collective. Stokes was arrested on April 10 at Helsinki Airport while attempting to board a flight to Japan. Court documents allege his involvement in at least four Scattered Spider breaches dating back to March 2023 — when he was 16 years old — including a hack of an online communication platform and a May 2025 breach of a multibillion-dollar luxury retailer where attackers called the IT helpdesk posing as employees to reset credentials and gain administrator access. The retailer refused an $8 million ransom demand but incurred over $2 million in remediation costs.

Scattered Spider (also tracked as 0ktapus, Octo Tempest, UNC3944) has been linked to over 100 network intrusions resulting in more than $100 million in ransom payments and counts Caesars, MGM Resorts, Riot Games, DoorDash, Reddit, and Twilio among its victims. Stokes faces charges of fraud, conspiracy, and computer intrusion and remains in custody after appearing in federal court in Chicago. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/alleged-scattered-spider-hacker-extradited-to-the-united-states/)]

---

**[NEW] FortiBleed Credential-Theft Campaign Linked to INC and Lynx Ransomware — Over 430,000 FortiGate Devices Targeted**

SOCRadar's follow-up investigation into the FortiBleed campaign has established direct links between the massive credential-theft operation and the INC and Lynx ransomware-as-a-service operations. Researchers identified a Windows server within the FortiBleed infrastructure showing browser sessions actively accessing both ransomware groups' negotiation panels — direct evidence that the same individuals operated across the credential-theft and ransomware extortion platforms.

The campaign was substantially larger than previously understood: approximately **430,000 FortiGate firewalls** were targeted, custom "FortiGate Sniffer" tools were deployed on roughly **19,000 devices** to intercept VPN credentials and authentication data directly from network traffic, and over **500 operational servers** were identified. After notifying affected organizations, the active compromised device count has fallen to approximately 11,000. SOCRadar believes the attackers exploited a previously undisclosed Nextcloud zero-day to expand access after initial compromise. The investigation identified persistent backdoor accounts using the username "adminin" on compromised systems and assesses the operation consists of roughly 20 members with defined roles. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fortibleed-credential-theft-campaign-linked-to-lynx-ransomware/)]

---

**[NEW] DHS Confirms HSIN Information-Sharing Platform Breached — Unknown Threat Actor During World Cup Security Period**

The Department of Homeland Security confirmed that the Homeland Security Information Network (HSIN), a sensitive information-sharing platform used by federal, state, local, and private-sector partners, was compromised by an unknown threat actor. The intrusion occurred between late May and early June, targeting HSIN servers and a SharePoint system used for collaboration. The DHS Office of Intelligence and Analysis has conducted a damage assessment but has not attributed the attack or determined whether documents were exfiltrated. DHS emphasized that classified systems were not affected and that the system remains operational. As the United States is currently overseeing security for the FIFA World Cup, HSIN's role in interagency coordination, incident management, and security planning for planned events raises the stakes on understanding the scope of the attacker's access. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/dhs-confirms-hackers-breached-hsin-info-sharing-platform/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] ChocoPoC Malware Targets Security Researchers via Trojanized PoC Exploits on GitHub**

A new campaign delivers a Python-based remote access trojan named ChocoPoC through weaponized proof-of-concept exploit repositories on GitHub, specifically targeting cybersecurity researchers and penetration testers. Rather than embedding malware directly in the exploit code, attackers added malicious PyPI packages — "frint" and "skytext" — as dependencies. During installation, "skytext" decrypts embedded Python code that downloads the final payload from a Mapbox dataset. The ChocoPoC RAT can execute arbitrary shell commands, steal browser passwords, cookies, autofill data, collect shell history and network configuration, and enumerate running processes.

Sekoia identified at least seven malicious repositories hosting exploits for FortiWeb (CVE-2025-64446), React2Shell (CVE-2025-55182), MongoBleed (CVE-2025-14847), PAN-OS (CVE-2026-0257), Ivanti Sentry (CVE-2026-10520), Check Point VPN (CVE-2026-50751), and Joomla SP Page Builder (CVE-2026-48908). The "skytext" package was downloaded 2,400 times, predominantly on Linux systems, with downloads surging following each high-profile vulnerability disclosure. Researchers assess with high confidence that the attacker primarily used compromised accounts to publish malicious packages and PoCs. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-chocopoc-malware-targets-researchers-via-trojanized-poc-exploits/)]

---

**[NEW] Medtronic Notifies 9 Million Customers of ShinyHunters Data Breach**

Healthcare device manufacturer Medtronic is notifying affected customers that its corporate IT systems were breached between April 13–19, exposing personal data including names, contact information, dates of birth, Social Security numbers, and health-related information of up to nine million individuals. The data extortion group ShinyHunters claimed the attack and listed Medtronic on its dark web extortion portal on April 18. The listing was later removed, and Medtronic has confirmed the stolen data was not publicly exposed. This incident is separate from the Oracle PeopleSoft exploitation wave — ShinyHunters targeted Medtronic's corporate IT systems directly. Medtronic operates in 150 countries with $33.5 billion in annual revenue and emphasized that medical devices remain safe to use. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/medtronic-notifies-customers-impacted-by-shinyhunters-data-breach/)]

---

**[NEW] Kubota Discloses Month-Long Network Intrusion — Employee PII, Payroll Data, and SSNs Exposed**

Kubota North America Corporation disclosed that an unknown threat actor maintained access to its network systems for over a month — from March 16 to April 20 — accessing files containing employee personal information including names, Social Security numbers (for employees and dependents), dates of birth, taxpayer IDs, driver's license numbers, direct deposit bank account information, corporate payment card data, and benefits enrollment information. Kubota began sending personalized notifications on June 30 and is offering Kroll identity protection services. No ransomware group has claimed responsibility, and the company reported no operational disruption. Kubota is a Japanese industrial manufacturer operating in 120 countries with 52,000 employees and $20 billion in annual revenue. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/kubota-says-hackers-had-month-long-access-to-network-systems/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Apple 'Hide My Email' Vulnerability Exposes Users' Real Email Addresses — Unfixed for Over a Year**

A vulnerability in Apple's "Hide My Email" feature allows almost anyone to discover the real email address behind a generated alias, completely defeating the privacy protection the service is designed to provide. Security researcher Alex Murphey reported the flaw to Apple in June 2025. Apple claimed to have fixed the issue in March 2026, but independent testing by 404 Media and multiple other outlets confirmed the vulnerability remains exploitable as of July 1. The exact technical details are being withheld to prevent trivial abuse. Hide My Email is widely used by privacy-conscious users across Apple's ecosystem to compartmentalize identities and prevent tracking. [[404 Media](https://www.404media.co/apple-hide-my-email-vulnerability-reveals-peoples-real-email-addresses/); [MacRumors](https://www.macrumors.com/2026/07/01/hide-my-email-vulnerability-exposes-real-addresses/); [9to5Mac](https://9to5mac.com/2026/07/01/apple-hide-my-email-bug-seemingly-allows-100-of-real-email-addresses-to-be-discovered/)]

---

**[UPDATE] CISA Adds Microsoft SharePoint RCE (CVE-2026-45659) to Known Exploited Vulnerabilities Catalog**

CISA added CVE-2026-45659, a high-severity remote code execution vulnerability in Microsoft SharePoint Server (CVSS 8.8), to its Known Exploited Vulnerabilities catalog, confirming active exploitation in the wild. The flaw arises from deserialization of untrusted data and enables authenticated attackers to achieve remote code execution on affected SharePoint servers. The vulnerability was originally disclosed and patched by Microsoft in May 2026. Any unpatched SharePoint Server instances should be treated as actively at risk. [[The Hacker News](https://thehackernews.com/2026/07/sharepoint-rce-cve-2026-45659-added-to.html); [CISA](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)]

---

**[UPDATE] Oracle EBS CVE-2026-46817 Attack Surface Expands — 950 Exposed Instances, Reconnaissance Phase Underway**

Shadowserver reports tracking approximately 950 Oracle E-Business Suite instances exposed online — more than half in the United States — as active exploitation of CVE-2026-46817 (CVSS 9.8) continues. Defused observed a single IP address exploiting the flaw across six honeypot instances during a two-hour window on Saturday, characterized as "reconnaissance and weaponization testing" rather than a targeted campaign. The vulnerability affects the File Transmission component of Oracle Payments and allows unauthenticated attackers with HTTP network access to take over vulnerable systems through low-complexity attacks. Oracle patched this flaw in its May 2026 Critical Patch Update. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/over-900-oracle-e-business-instances-exposed-to-ongoing-attacks/); [CyberScoop](https://cyberscoop.com/oracle-ebs-critical-vulnerability-exploited/)]

---

## ⚡ Quick Hits

- **[UPDATE] Citrix Patches NetScaler Vulnerabilities Including 'HTTP/2 Bomb' Attack** — Citrix disclosed NetScaler ADC and Gateway vulnerabilities including a new HTTP/2 attack vector requiring manual configuration to fully mitigate, alongside file read and denial-of-service flaws. [[SecurityWeek](https://www.securityweek.com/citrix-patches-netscaler-vulnerabilities-including-new-http-2-bomb-attack/)]

- **[UPDATE] Adobe Patches 11 ColdFusion Flaws — 6 Rated Maximum Severity** — Adobe released ColdFusion 2025 Update 10 and 2023 Update 21 addressing 11 vulnerabilities, 6 of which carry a CVSS score of 10/10 enabling arbitrary code execution through unrestricted file upload and path traversal. Campaign Classic CVE-2026-48286 (CVSS 10) also patched. No active exploitation reported but all tagged Priority 1. [[SecurityWeek](https://www.securityweek.com/adobe-patches-critical-coldfusion-campaign-classic-vulnerabilities/)]

- **[NEW] CVE-2026-55407: Anthropic's buffa Protobuf Library Contains 22x Memory Amplification Bug** — Endor Labs' AI SAST engine discovered a denial-of-service vulnerability in Anthropic's Rust-based protobuf decoder (buffa) that amplifies small untrusted protobuf payloads into large heap allocations, enabling process-crashing memory exhaustion. Patched in buffa/connectrpc 0.8.0. [[Endor Labs](https://www.endorlabs.com/learn/endor-labs-ai-sast-finds-zero-day-cve-2026-55407-buffa); [Cybersecurity News](https://cybersecuritynews.com/anthropics-buffa-rust-library-0-day-vulnerability-enables-dos-attack/)]

- **[NEW] Canada's CSE Conducted Offensive Cyber Operations Against Fentanyl Brokers, Ransomware Gangs, and Chinese Espionage** — A report reveals that Canada's Communications Security Establishment conducted cyber operations targeting fentanyl trafficking networks, ransomware groups, and Chinese state-sponsored cyber espionage, providing a rare public window into active CSE offensive cyber activity. [[The Globe and Mail](https://www.theglobeandmail.com/politics/article-canadas-electronic-spy-agency-conducted-cyberattacks-on-criminals)]
