---
title: Chrome zero-day exploits 🔥, Windows RasMan flaw 🛡️, PayPal subscription scam 💳, Cross-platform ransomware 💣, EDR process sideloading 🎯
date: 2025-12-15
tags: ["zero-day exploitation","privilege escalation","email security bypass","ransomware","threat actors","edr evasion","financial fraud","iot vulnerabilities","windows security","browser security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Attackers are actively exploiting a Chrome zero-day vulnerability while also leveraging an unpatched Windows RasMan flaw and sophisticated PayPal subscription scams that bypass email security filters. Storm-0249 is advancing EDR evasion techniques through process sideloading, and the new VolkLocker ransomware variant demonstrates alarming cross-platform capabilities that significantly expand potential victim pools.
---

# Daily Threat Intel Digest - 2025-12-15

Good morning. Here's what you need to know today. We're looking at a critical unpatched Windows flaw, a new Chrome zero-day under active attack, and a clever PayPal scam that bypasses email security entirely. Let's get to it.

## 🔴 Critical Threats & Active Exploitation

**[NEW] CISA alerts on actively exploited Google Chromium zero-day flaw**
CISA has issued an urgent alert for a critical zero-day vulnerability, CVE-2025-14174, affecting the Chromium engine used by Google Chrome and other browsers. The out-of-bounds memory access flaw is being actively exploited in the wild, allowing attackers to execute code simply by having a user visit a malicious webpage. This poses an immediate risk to millions of users; applying browser updates is critical [[GBHackers](https://gbhackers.com/cisa-alerts-on-google-chromium-zero-day-flaw/)].

**[NEW] Unpatched Windows RasMan flaw allows arbitrary code execution**
Security researchers have disclosed a critical, unpatched vulnerability in the Windows Remote Access Connection Manager (RasMan) service that enables local attackers to elevate privileges and execute arbitrary code with SYSTEM-level permissions. Discovered during analysis of a separate patched vulnerability (CVE-2025-59230), this flaw represents a significant privilege escalation risk on all supported Windows versions, as Microsoft has not yet released a fix [[GBHackers](https://gbhackers.com/windows-remote-access-connection-manager-flaw/)].

**[NEW] PayPal subscriptions abused to send fake purchase emails**
A sophisticated email scam is abusing PayPal's legitimate "Subscriptions" feature to send authentic emails that bypass SPF, DKIM, and DMARC filters. Scammers create a paused subscription and manipulate the "Customer Service URL" field to include fake purchase confirmations for expensive items and a fraudulent support number. Because the emails originate from `service@paypal.com`, they appear legitimate and are designed to trick recipients into calling the scammers, leading to financial fraud or malware installation [[BleepingComputer](https://www.bleepingcomputer.com/news/security/beware-paypal-subscriptions-abused-to-send-fake-purchase-emails/)].

**[NEW] CISA adds actively exploited Sierra router flaw to KEV catalog**
CISA has added CVE-2018-4063, a critical file upload vulnerability in Sierra Wireless AirLink ALEOS routers, to its Known Exploited Vulnerabilities (KEV) catalog. The flaw, which allows unrestricted file upload of dangerous types, is now seeing active exploitation in the wild. This puts a wide range of operational and IoT networks at risk, especially those using aging or unmanaged infrastructure [[GBHackers](https://gbhackers.com/cisa-adds-actively-exploited-sierra-router-flaw/)].

**[NEW] Microsoft: December security updates cause Message Queuing failures**
Microsoft has confirmed that its December 2025 Patch Tuesday updates are breaking Message Queuing (MSMQ) functionality on Windows 10 22H2, Server 2019, and Server 2016. The updates introduce a security model change that modifies NTFS permissions on the MSMQ storage folder, causing applications to fail with "insufficient resources" errors. This impacts critical enterprise applications and IIS websites, forcing admins into a difficult choice between rolling back security patches or facing service disruption [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-december-security-updates-cause-message-queuing-failures/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Storm-0249 now uses EDR process sideloading to conceal malicious activity**
The initial access broker Storm-0249, previously reported for EDR process abuse, has escalated its tactics. The group is now sideloading malicious DLLs into legitimate EDR processes to execute malicious activity under the guise of routine security operations. This technique allows them to bypass detection and maintain persistence on targeted networks, representing a significant challenge for organizations relying solely on process-level EDR telemetry [[GBHackers](https://gbhackers.com/storm-0249-edr/)].

**[NEW] New VolkLocker ransomware variant targets both Linux and Windows systems**
The pro-Russia hacktivist group CyberVolk has re-emerged with VolkLocker 2.x, a new ransomware-as-a-service (RaaS) platform. This variant is notable for its cross-platform capabilities, targeting both Linux and Windows systems, and its use of Telegram-based automation for managing operations and victim communications. This marks a technical evolution for the group and expands its potential victim pool significantly [[GBHackers](https://gbhackers.com/volklocker-ransomware/)].