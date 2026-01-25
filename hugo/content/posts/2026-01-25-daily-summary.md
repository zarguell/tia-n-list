---
title: Sandworm DynoWiper attacks ⚡, Qilin ransomware expansion 💰, Konni AI malware 🤖, Teams surveillance concerns 👁️
date: 2026-01-25
tags: ["apt activity","ransomware","data wiper","ai-generated malware","energy sector","blockchain targeting","privacy concerns","critical infrastructure","russian state actors","north korean actors"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Russian state-sponsored Sandworm deployed destructive DynoWiper malware against Poland's energy infrastructure, continuing their decade-long pattern of critical infrastructure attacks targeting power plants and renewable energy systems. Qilin ransomware expanded their double-extortion campaign to legal and construction sectors while North Korean Konni group pioneered AI-generated malware attacks on blockchain developers, and Microsoft Teams introduced controversial location-sharing capabilities raising workplace surveillance concerns.
---

# Daily Threat Intel Digest - 2026-01-25

## 🔴 Critical Threats & Active Exploitation

**[NEW] Microsoft emergency OOB update fixes Outlook freeze bug after Patch Tuesday**  
Microsoft released out-of-band updates for Windows 10, 11, and Server to address Outlook freezing issues triggered by January Patch Tuesday updates. The bug prevented Outlook from opening when PST files were stored on cloud storage (OneDrive/Dropbox), causing unresponsiveness and sent email failures. Primarily affecting enterprise deployments using classic Outlook, the updates (KB5078127, KB5078132, etc.) are available via Windows Update or Microsoft Catalog. Unaffected systems can wait for next month's scheduled updates. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-releases-emergency-oob-update-to-fix-outlook-freezes/)]

**[NEW] Sandworm targets Polish energy grid with new DynoWiper malware**  
Russian state-sponsored Sandworm (APT44) attempted to deploy a destructive data-wiper called DynoWiper (SHA-1: 4EC3C90846AF6B79EE1A5188EEFA3FD21F6D4CF6) against Poland's energy infrastructure in late December 2025. The attack targeted two combined heat/power plants and renewable energy management systems but was successfully blocked. This continues Sandworm's decade-long pattern of disruptive attacks against critical infrastructure, following previous wiper campaigns against Ukraine's energy sector in 2015 and 2025. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/sandworm-hackers-linked-to-failed-wiper-attack-on-polands-energy-systems/)]

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Qilin ransomware escalates attacks across legal, construction sectors**  
Expanding their ongoing campaign, Qilin ransomware claimed three new victims on January 24: German law firm HARTE-BAVENDAMM, US construction company D & D Building, and equipment supplier Shiffler Equipment Sales. The group continues double-extortion tactics, threatening to leak stolen data unless negotiations begin. This multi-sector targeting demonstrates Qilin's aggressive expansion beyond previous attacks on energy and automotive sectors noted in January 22-23 reporting. [[DeXpose via Malware.News](https://malware.news/t/qilin-ransomware-strikes-german-law-firm-harte-bavendamm/103572#post_1); [Malware.News](https://malware.news/t/qilin-ransomware-targets-d-d-building/103571#post_1); [Malware.News](https://malware.news/t/qilin-ransomware-targets-shiffler-equipment-sales/103570#post_1)]

**[NEW] North Korean Konni group uses AI-generated malware against blockchain engineers**  
Konni (Opal Sleet/TA406) deployed novel AI-generated PowerShell backdoors in phishing attacks targeting blockchain developers in Asia-Pacific. The attack chain uses Discord-hosted links delivering ZIP archives with malicious LNK files that execute obfuscated PowerShell malware. Researchers attribute the code to AI development due to structured documentation, modular design, and LLM-style comments like "# <-- your permanent project UUID". The malware performs anti-analysis checks before C2 communication, enabling theft of API credentials and cryptocurrency assets. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/konni-hackers-target-blockchain-engineers-with-ai-built-malware/)]

## 📋 Policy & Industry News

**[NEW] Microsoft Teams location sharing feature sparks surveillance concerns**  
Microsoft confirmed an upcoming Teams update that will automatically detect employee work locations via Wi-Fi network connections and share this data with employers. Documented in Microsoft 365 Roadmap (MC1081568), the feature aims to optimize hybrid work policies but raises significant privacy implications regarding workplace monitoring. [[GBHackers](https://gbhackers.com/microsoft-teams-to-begin-sharing-employee-location/)]