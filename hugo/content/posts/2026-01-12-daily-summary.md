---
title: EDRStartupHinder bypass 🔧, Nissan data breach 🚗, InputPlumber keystroke injection ⌨️, Penguin pig-butchering 🐧, WordPress auth bypass 💻
date: 2026-01-12
tags: ["edr bypass","automotive sector","keystroke injection","pig butchering","wordpress","data breach","endpoint security","financial fraud","linux vulnerabilities","authentication bypass"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Attackers are deploying the EDRStartupHinder tool to bypass Windows endpoint protections while Nissan suffers a massive 900GB data breach and InputPlumber vulnerabilities expose Linux systems to keystroke injection attacks. The emergence of Penguin's pig-butchering-as-a-service ecosystem and widespread WordPress plugin authentication bypass exploits highlight the growing sophistication of criminal operations targeting both enterprises and individuals.
---

# Daily Threat Intel Digest - 2026-01-12

## 🔴 Critical Threats & Active Exploitation

**[NEW] EDRStartupHinder Tool Disables Security Software on Windows 11 25H2**  
Attackers can now prevent antivirus and EDR solutions from launching during Windows startup by exploiting the Windows Bindlink API and Protected Process Light (PPL) mechanisms. The proof-of-concept tool redirects critical system DLLs before security services initialize, causing PPL-protected processes to terminate due to invalid signatures. Successfully demonstrated against Microsoft Defender and multiple commercial EDR products, this technique requires reconnaissance of target systems but represents a fundamental bypass of endpoint protections. Organizations should monitor for bindlink.dll usage, unauthorized service creation, and registry modifications to service group orders [[researcher analysis](https://www.zerosalarium.com/2026/01/edrstartuphinder-edr-startup-process-blocker.html); [technical breakdown](https://cyberpress.org/edrstartuphinder-disables/)].

**[NEW] Nissan Motor Suffers 900GB Data Breach Claimed by Everest Group**  
Japanese automaker Nissan Motor Co. reportedly had approximately 900GB of sensitive data exfiltrated by the Everest hacking group, potentially exposing intellectual property, supply chain details, and employee information. While the breach remains under investigation, the scale suggests sophisticated access to Nissan's internal systems, likely posing risks to vehicle R&D data and manufacturing operations. The claim follows recent increases in automotive sector targeting by financially motivated groups [[threat intelligence report](https://gbhackers.com/nissan-motor-breach/)].

**[UPDATE] Instagram Clarifies "Data Breach" as API Abuse**  
Meta confirms a password reset email bug allowed mass scraping requests but denies a breach after 17 million user records surfaced on hacking forums. While no passwords were exposed, the leaked data (names, emails, phone numbers, addresses) enables targeted phishing and SIM swapping attacks. Despite initial claims of API exploitation, Meta states the issue stems from account recovery abuse and has been patched. Users remain vulnerable to social engineering using the leaked PII, though no immediate password changes are required unless suspicious activity is detected [[BleepingComputer](https://www.bleepingcomputer.com/news/security/instagram-denies-breach-amid-claims-of-17-million-account-data-leak/); [Meta statement](https://www.bleepingcomputer.com/news/security/instagram-denies-breach-amid-claims-of-17-million-account-data-leak/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] InputPlumber Flaws Enable Keystroke Injection in SteamOS/Linux**  
Critical vulnerabilities in Valve's SteamOS-integrated InputPlumber utility (CVE-2025-66005/CVE-2025-14338) allow local attackers to inject keystrokes into active sessions, leak sensitive files, and cause denial-of-service via inadequate D-Bus authorization. The CreateTargetDevice method specifically enables creation of virtual keyboards for code execution under logged-in users. Patches are available in InputPlumber v0.69.0 and SteamOS 3.7.20, though some API risks remain unresolved. Gaming environments and Linux systems using InputPlumber for input device management are at immediate risk [[SUSE advisory](https://security.opensuse.org/2026/01/09/inputplumber-lack-of-dbus-auth.html); [technical analysis](https://cyberpress.org/inputplumber-vulnerability/)].

**[NEW] Atarim WordPress Plugin Auth Bypass Exploited in the Wild**  
Public PoC exploit code released for CVE-2025-60188 exposes 2.5M WordPress sites to unauthorized admin access. The vulnerability stems from HMAC secret key exposure via REST API endpoints, allowing attackers to forge signatures and access user data, license keys, and system configurations. Plugin versions before the latest patch are vulnerable, with immediate updates critical due to trivial exploitability requiring only site ID enumeration [[PoC details](https://cyberpress.org/poc-exploit-released-for-atarim-plugin-authentication-bypass-vulnerability/)].

**[NEW] Critical Buffer Overflow in zlib untgz Utility**  
Version 1.3.1.2 of zlib contains an unbounded strcpy() flaw in the TGZfname() function, enabling memory corruption via crafted archive names. The overflow occurs pre-validation during argument processing, affecting any system using the untgz utility for archive extraction. Denial-of-service is certain, with potential code execution dependent on memory layout. Input validation or alternative extraction tools are recommended pending patches [[technical analysis](https://cyberpress.org/critical-zlib-vulnerability/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] "Penguin" Operation Industrializes Pig-Butchering Scams**  
A new Pig Butchering-as-a-Service (PBaaS) ecosystem centered on "Penguin" and "UWORK" platforms enables low-cost, large-scale romance and investment fraud. The operation sells complete scam kits including stolen PII, pre-registered SIMs, social media accounts, and CRM platforms for under $2,500. Notably, UWORK provides fake trading sites integrated with MetaTrader and mobile app distribution systems, dramatically lowering barriers for transnational crime groups. Indicators include uworkcrm[.]com and lion-forex[.]com domains [[PBaaS analysis](https://cyberpress.org/penguin-operation-sells-pig-butchering/)].

**[NEW] Carding Market Infrastructure Mapped by Team Cymru**  
Research identified 28 unique IPs and 85 domains hosting illicit credit card markets, primarily hosted by offshore providers like Privex. The analysis revealed TLD preferences (.su, .cc, .ru) and operational patterns distinguishing transactional platforms from discussion forums. This intelligence enables proactive takedowns and disruption of financial fraud infrastructure, though the supply chain remains resilient through jurisdictional shielding [[infrastructure research](https://cyberpress.org/carding-markets-28-ips-85-domains/)].

## 📋 Policy & Industry News

**[NEW] California Bans Data Broker Reselling Health Data**  
The California Privacy Protection Agency blocked Datamasters from selling health data after enforcement of the Delete Act revealed unregistered brokerage activities. The firm sold lists targeting Alzheimer's patients, drug addicts, and demographics ("Senior Lists," "Hispanic Lists") without compliance, resulting in fines and deletion orders. This action signals aggressive enforcement against data brokers exploiting sensitive health information [[enforcement order](http://cppa.ca.gov/pdf/datamasters_order_signed.pdf); [agency statement](https://www.bleepingcomputer.com/news/legal/california-bans-data-broker-reselling-health-data-of-millions/)].

**[NEW] Analysis: US Adopts "Gray Zone" Cyber Tactics in Venezuela**  
Recent operations against Venezuela's oil sector suggest a strategic shift toward sustained cyber-enabled economic pressure below conflict thresholds. Tactics involve persistent access and intermittent disruption rather than catastrophic attacks, mirroring Russian hybrid warfare models. This integration of cyber tools with sanctions and diplomatic pressure indicates growing state adoption of gray zone campaigns for geopolitical leverage [[strategic analysis](https://cyberscoop.com/gray-zone-cyber-operations-state-power-below-threshold-conflict-op-ed/)].