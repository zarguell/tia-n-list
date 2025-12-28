---
title: Rainbow Six Siege breach 🎮, WIRED subscriber leak 📰, EDR-Freeze technique 🛡️, MongoBleed exploitation 💾
date: 2025-12-28
tags: ["gaming security","data breach","media publishing","edr evasion","mongodb vulnerabilities","healthcare compliance","threat actors","access control","regulatory enforcement"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Ubisoft's Rainbow Six Siege infrastructure was compromised enabling god-mode privileges and massive credit distribution, while Condé Nast faces a 40M-record subscriber leak threat following WIRED's 2.3M-record breach exposing personal data. The EDR-Freeze technique demonstrates how Windows Error Reporting can be weaponized to blind security tools, alongside increased regulatory enforcement as healthcare entities face significant fines for data protection failures.
---

# Daily Threat Intel Digest - 2025-12-28

## 🔴 Critical Threats & Active Exploitation

**[NEW] Rainbow Six Siege breach grants hackers god-mode privileges**  
Attackers compromised Ubisoft's internal systems for Rainbow Six Siege, enabling them to ban/unban players, manipulate moderation feeds, and distribute approximately 2 billion R6 Credits ($13.33M value) to accounts worldwide. The breach also unlocked all cosmetic items, including developer-only skins. Ubisoft shut down servers and announced transaction rollbacks since 11:00 AM UTC, but hasn't disclosed the root cause. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/massive-rainbow-six-siege-breach-gives-players-billions-of-credits/)]

**[NEW] WIRED subscriber database leaked with 40M-record Condé Nast threat**  
A confirmed 2.3M-record WIRED subscriber database containing names, addresses, and phone numbers was leaked Christmas Day after unheeded vulnerability reports starting in November. Threat actor "Lovely" threatens to release an additional 40M records affecting Condé Nast publications like Vogue and The New Yorker. The breach exploited IDOR vulnerabilities and broken access controls, with Hudson Rock validating authenticity via infostealer logs. Physical addresses exposed enable doxing/swatting risks. [[InfoStealers](https://www.infostealers.com/article/wired-database-leaked-40-million-record-threat-looms-for-conde-nast/)]

**[UPDATE] MongoBleed linked to rumored Ubisoft infrastructure breach**  
Unverified claims suggest Ubisoft's broader infrastructure was breached via MongoBleed (CVE-2025-14847), a MongoDB memory-leak vulnerability disclosed in previous reporting. Threat actors allegedly pivoted from exposed MongoDB instances to steal internal source code from the 1990s-present and exfiltrate user data for extortion. While Ubisoft confirmed only the Rainbow Six Siege abuse, the MongoBleed connection—actively exploited in recent campaigns—significantly expands risk scope if validated. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/massive-rainbow-six-siege-breach-gives-players-billions-of-credits/)]

## 🛡️ Defense & Detection

**[NEW] EDR-Freeze technique suspends security tools via WerFaultSecure abuse**  
Researchers detailed EDR-Freeze, a proof-of-concept that suspends EDR/AV processes (e.g., MsMpEng.exe) by weaponizing Windows Error Reporting. The attack triggers WerFaultSecure.exe to dump EDR memory, then suspends both the dump process and EDR threads indefinitely—creating a race condition that blinds defenses without malware execution. Detection relies on spotting unusual WerFaultSecure command lines with /pid, /tid, and /cancel arguments targeting security processes. [[Detect FYI](https://detect.fyi/forensic-insights-into-an-edr-freeze-attack-e559b0e50a91)]

## 📋 Policy & Industry News

**[NEW] OrthopedicsNY fined $500K for patient data protection failures**  
New York Attorney General Letitia James penalized Orthopedics NY LLP $500,000 for inadequate system safeguards that exposed patient information. The fine underscores regulatory enforcement trends for healthcare entities failing to implement reasonable security controls, with HIPAA violations increasingly triggering state-level actions. [[DataBreaches.net](https://databreaches.net/2025/12/27/orthopedicsny-fined-500k-by-nys-for-patient-data-breach/)]