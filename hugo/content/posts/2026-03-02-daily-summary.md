---
title: AWS data center attacks 🔥, LockBit 5.0 expansion 💣, APT37 Zoho abuse 🎯, Agent Tesla evasion 🕵️, AI agent hijacking 🤖
date: 2026-03-02
tags: ["ransomware","apt activity","physical security","cloud infrastructure","process injection","blockchain c2","ssrf vulnerabilities","ai security","data exfiltration","threat actors"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Physical attacks on AWS Middle East data centers and LockBit 5.0's global expansion highlight the convergence of physical and cyber threats across critical infrastructure sectors. APT37's abuse of legitimate cloud services, Agent Tesla's advanced evasion techniques, and emerging AI agent hijacking vulnerabilities demonstrate how threat actors are evolving tradecraft across multiple attack vectors.
---

# Daily Threat Intel Digest - March 2, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] AWS Middle East outage disrupts global services after physical data center attack**  
A severe infrastructure failure struck AWS ME-CENTRAL-1 (UAE) and ME-SOUTH-1 (Bahrain) regions after external objects struck a UAE data center, igniting a fire that forced power shutdowns. This disrupted 38 services in ME-CENTRAL-1 and 46 in ME-SOUTH-1, including EC2, RDS, and Lambda. The incident underscores physical infrastructure risks to cloud operations, requiring multi-AZ redundancy and failover testing. AWS restored services by March 2 after rerouting traffic [[Cyberpress](https://cyberpress.org/amazon-web-services-power-outage/); [GBHackers](https://gbhackers.com/middle-east-aws-outage/)].

**[UPDATE] Fake Zoom/Teramind campaign infects 1,437 users in 12 days**  
Attackers leveraging fake Zoom meeting pages have deployed legitimate Teramind surveillance software to 1,437 Windows users by March 1. The campaign uses forced "update" prompts on fake waiting rooms, installing Teramind in stealth mode to exfiltrate credentials and monitor activity. This rapid expansion highlights the growing abuse of legitimate tools for surveillance, requiring user education on update verification [[Cyberpress](https://cyberpress.org/fake-zoom-update-malware/); [Malwarebytes](https://www.malwarebytes.com/blog/scams/2026/02/fake-zoom-meeting-update-silently-installs-surveillance-software)].

**[NEW] LockBit 5.0 claims victims in Brazil, India, and China**  
LockBit 5.0 added three high-profile targets to its leak site on March 1: Brazil's Brassuco Alimentos (food industry), India's OMAX Autos (automotive), and China's Yaomazi Food. The group threatens data leaks unless negotiations begin, emphasizing ransomware's continued global expansion across critical sectors. Victims should conduct compromise assessments and validate offline backups [[DeXpose Brassuco](https://www.dexpose.io/lockbit-5-0-targets-brazilian-food-industry-leader-brassuco-alimentos/); [DeXpose OMAX](https://www.dexpose.io/lockbit-5-0-targets-omax-autos-limited-in-india/); [DeXpose Yaomazi](https://www.dexpose.io/lockbit-5-0-targets-chinese-food-giant-yaomazi-food-co-ltd/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] APT37 evolves Ruby Jumper toolkit with Zoho WorkDrive abuse**  
North Korean APT37 enhanced its air-gapped breach toolkit "Ruby Jumper" by leveraging Zoho WorkDrive for command-and-control – a first for the group. The campaign installs a full Ruby runtime to deploy payloads like THUMBSBD (USB-based C2) and FOOTWINE (Android surveillance), targeting government entities. Organizations must monitor Ruby installations in ProgramData and USB-based lateral movement [[Cyberpress](https://cyberpress.org/apt37-air-gap-breach-campaign/)].

**[NEW] Agent Tesla campaign uses process hollowing to evade defenses**  
A new phishing-driven Agent Tesla campaign employs process hollowing via `Aspnet_compiler.exe` to bypass security tools. The multi-stage attack uses encrypted PowerShell downloads from catbox.moe and AES decryption in-memory, exfiltrating data via SMTP to `mail.taikei-rmc-co.biz`. Defenders should block `Aspnet_compiler.exe` abuse and monitor for JScript attachments [[Cyberpress](https://cyberpress.org/agent-tesla-evades-detection/)].

**[NEW] OCRFix botnet combines ClickFix phishing and blockchain C2**  
A new botnet campaign abuses fake Tesseract OCR sites to deliver ClickFix-style PowerShell commands. It uses EtherHiding on BNB Smart Chain to conceal C2 infrastructure, rotating commands via blockchain transactions. This highlights emerging convergence of social engineering and crypto-based obfuscation [[GBHackers](https://gbhackers.com/ocrfix-botnet-uses-clickfix/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Angular SSR flaw (CVE-2026-27739) enables critical SSRF attacks**  
A severe SSRF vulnerability in Angular SSR packages (CVSS 4.0) allows attackers to manipulate Host/X-Forwarded headers to trigger unauthorized server-side requests. Affects `@angular/ssr` v19–21 and `@nguniversal` ≤16.2.0. Patch immediately or switch to absolute URLs [[Cyberpress](https://cyberpress.org/angular-ssr-flaw/); [GBHackers](https://gbhackers.com/angular-ssr-flaw/)].

**[NEW] OpenClaw "ClawJacked" flaw allows 0-click AI agent hijacking**  
OpenClaw's WebSocket gateway exposes a 0-click vulnerability enabling malicious sites to brute-force localhost passwords and hijack AI agents. Attackers can exfiltrate data or execute commands via trusted processes. Patch to v2026.2.26 and implement rate limiting [[Cyberpress](https://cyberpress.org/openclaw-zero-click-flaw-lets-attackers-take-over-developer-ai-agents-via-malicious-sites/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/clawjacked-attack-let-malicious-websites-hijack-openclaw-to-steal-data/)].

**[NEW] SonicWall firewalls scanned en masse for SSL VPN targets**  
Attackers launched 84,000+ scanning sessions from 4,000+ IPs against SonicWall firewalls, focusing on SSL VPN enumeration via SonicOS REST API. This pre-attack mapping indicates imminent credential theft or vulnerability exploitation. Administrators should restrict API access and monitor for abnormal scanning [[GBHackers](https://gbhackers.com/sonicwall-firewall-attack/)].

## 📋 Policy & Industry News

**[UPDATE] Project Compass arrests 30 in crackdown on "The Com" cybercrime network**  
International law enforcement operation Project Compass arrested 30 suspects and identified 179 tied to "The Com" – a decentralized collective blending ransomware, extremism, and sextortion. Subgroups like 764 recruit youth for violent acts. This disrupts TVN operations but requires ongoing vigilance for crypto-linked ransomware and grooming keywords [[Cyberpress](https://cyberpress.org/project-compass-operation-cracks-down/); [GBHackers](https://gbhackers.com/project-compass-operation-cracks-down/)].

**[NEW] Samsung halts Texas data collection without explicit consent**  
Samsung settled with Texas over unlawful smart TV data collection via Automated Content Recognition (ACR). The company must obtain express consent for ACR data and update privacy disclosures, setting a precedent for IoT privacy enforcement [[BleepingComputer](https://www.bleepingcomputer.com/news/security/samsung-tvs-to-stop-collecting-texans-data-without-express-consent/)].