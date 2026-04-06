---
title: FortiClient EMS RCE exploited 🔴, Dgraph CVSS 10.0 flaw unpatched 💀, North Korean APTs (UNC1069, Kimsuky) deploy RATs 🏴, supply chain attacks target developers 🔗
date: 2026-04-06
tags: ["fortinet vulnerability","rce exploitation","database security","apt activity","north korea","supply chain attack","ransomware","malicious packages","rat malware","social engineering"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical vulnerabilities in FortiClient EMS and Dgraph database are being actively exploited, with over 2,000 servers exposed and a CVSS 10.0 flaw lacking patches, creating urgent risks for organizations unable to remediate immediately. North Korean threat actors UNC1069 and Kimsuky are conducting sophisticated campaigns using fake Microsoft Teams domains, malicious LNK files, and Python backdoors, while supply chain compromises targeting developer ecosystems through WordPress breaches and malicious npm packages continue to expand the attack surface.
---


# Daily Threat Intel Digest - 2026-04-06

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical FortiClient EMS Flaw Under Active Exploitation — 2,000+ Servers Exposed**

Fortinet has released an emergency patch for a critical vulnerability (CVE-2026-35616) in FortiClient Enterprise Management Server that allows unauthenticated remote code execution. The flaw, discovered by security firm Defused and confirmed exploited as a zero-day, affects versions 7.4.5 and 7.4.6. Shadowserver Foundation's internet scanning reveals over 2,000 exposed FortiClient EMS instances globally, with the majority located in the United States and Germany. Attackers can achieve full system compromise with a single crafted HTTP request, potentially allowing them to push malware to thousands of managed endpoints, disable security software, or deploy ransomware through the server's trusted communication channels. A separate FortiClient EMS flaw (CVE-2026-21643), also discovered by Defused and reported last week, remains actively exploited. Organizations must apply hotfixes immediately or upgrade to version 7.4.7 when available. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-fortinet-forticlient-ems-flaw-cve-2026-35616-exploited-in-attacks/)] [[CyberPress](https://cyberpress.org/over-2000-forticlient-ems-servers-exposed-as-rce-attacks-surge/)] [[GBHackers](https://gbhackers.com/2000-forticlient-ems-instances-exposed-online/)]

---

**[NEW] Dgraph Database Vulnerability Exposes Servers to Complete Takeover — No Patch Available**

A critical flaw (CVE-2026-34976, CVSS 10.0) in the open-source Dgraph database allows unauthenticated attackers to bypass all authentication mechanisms. The vulnerability stems from the `restoreTenant` command being inadvertently excluded from the security middleware's protection list, enabling remote access to administrative functions without credentials. Attackers can overwrite databases, read sensitive server files, conduct SSRF attacks against internal services, and steal credentials including Kubernetes tokens. No official patch exists at this time. Organizations should restrict access to admin endpoints, enforce strict firewall rules, and monitor for unauthorized restore attempts. [[CyberPress](https://cyberpress.org/dgraph-flaw/)] [[GBHackers](https://gbhackers.com/critical-dgraph-database-flaw/)]

---

**[NEW] React2Shell Exploitation Harvests 766+ Hosts' Credentials via NEXUS Listener**

Attackers are conducting large-scale automated credential theft after exploiting CVE-2025-55182 (React2Shell) in vulnerable Next.js applications. Cisco Talos attributes the campaign to threat cluster UAT-10608, which has compromised at least 766 hosts within a 24-hour period using a framework called NEXUS Listener. The operation automatically extracts database credentials, AWS/GCP/Azure tokens, SSH private keys, API keys, Kubernetes tokens, and environment secrets. Stolen data is exfiltrated in chunks to a C2 server over port 8080. Defenders should apply React2Shell patches, rotate all credentials immediately, enforce AWS IMDSv2, and enable secret scanning to limit exposure. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-exploit-react2shell-in-automated-credential-theft-campaign/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] North Korean UNC1069 Deploys Fake Microsoft Teams Domains for RAT Delivery**

DPRK-linked threat group UNC1069 is conducting sophisticated social engineering attacks using counterfeit Microsoft Teams domains to deliver Remote Access Trojans. The campaign, identified by Security Alliance (SEAL) researchers, involves newly registered malicious domains like onlivemeet[.]com that impersonate Microsoft Teams. Attackers revive old conversations from compromised Telegram and LinkedIn accounts, send partnership proposals via fake Slack groups, and use legitimate platforms like Calendly to establish credibility before delivering meeting links. Victims are redirected to fake Teams interfaces prompting them to download what appears to be a "TeamsFx SDK update," which actually installs malware. The group primarily targets professionals in technology, finance, and consulting sectors. [[CyberPress](https://cyberpress.org/exploit-fake-microsoft-teams/)] [[GBHackers](https://gbhackers.com/threat-actors-weaponize-fake-microsoft-teams/)]

---

**[NEW] Kimsuky Evolves LNK-Based Infection Chain with Multi-Stage Python Backdoor**

North Korean state-sponsored group Kimsuky has significantly upgraded its attack methodology, now using complex multi-stage infection chains involving malicious LNK files to deliver Python backdoors. According to AhnLab Security Intelligence Center (ASEC), the group has moved away from simple direct infections to sophisticated multi-step processes that use decoy documents disguised as resumes or backup guides, batch scripts, and XML-scheduled tasks to evade detection. Two malware variants have been identified: a simple downloader that self-deletes after 180 seconds, and a more dangerous interactive backdoor that sends a "HAPPY" beacon to C2 servers and can execute shell commands, upload/download files, and securely delete evidence by overwriting files with random data. Attribution to Kimsuky is confirmed through reused decoy documents, "sch.db" XML scheduling files, and consistent naming conventions with previous campaigns. [[CyberPress](https://cyberpress.org/kimsuky-lnks-drop-backdoor/)]

---

**[NEW] Germany Doxes "UNKN" — Identity Revealed for Alleged GandCrab and REvil Leader**

German Federal Criminal Police (BKA) have publicly identified 31-year-old Russian Daniil Maksimovich Shchukin as "UNKN" (a.k.a. UNKNOWN), the alleged leader of the GandCrab and REvil ransomware operations. Shchukin and accomplice Anatoly Sergeevitsch Kravchuk (43) reportedly extorted nearly €2 million across two dozen cyberattacks in Germany between 2019 and 2021, causing over €35 million in total economic damage. Shchukin previously appeared in a 2023 U.S. Justice Department filing seeking seizure of cryptocurrency accounts containing over $317,000 in ransomware proceeds. GandCrab, which pioneered double-extortion tactics, announced its shutdown in May 2019 after extorting over $2 billion from victims. REvil later emerged as its spiritual successor, known for high-profile attacks including the Kaseya incident. Shchukin is believed to reside in Krasnodar, Russia. [[KrebsOnSecurity](https://krebsonsecurity.com/2026/04/germany-doxes-unkn-head-of-ru-ransomware-gangs-revil-gandcrab/)] [[Malware.news](https://malware.news/t/germany-doxes-unkn-head-of-ru-ransomware-gangs-revil-gandcrab/105751#post_1)]

---

**[NEW] ILSpy WordPress Site Compromised to Distribute Fake Browser Extensions**

The official WordPress website for ILSpy, a popular open-source .NET decompiler, was breached to redirect visitors to a malicious domain distributing fake browser extensions. Cybersecurity group vx-underground confirmed the compromise after video evidence showed the ILSpy download link redirecting users to an attacker-controlled site prompting installation of a malicious extension. The site remains offline (returning 502 Bad Gateway), indicating administrators took it offline for investigation. Developers who recently visited the site or installed unexpected extensions should immediately remove them, reset all passwords, and perform full system scans. This attack highlights the growing targeting of developer ecosystems as an entry point for supply chain intrusions. [[CyberPress](https://cyberpress.org/breach-ilspy-wordpress/)] [[GBHackers](https://gbhackers.com/hackers-breach-ilspy-wordpress-domain/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Tax Season Phishing Campaigns Surge — RMM Tools, Credential Theft, and BEC**

Security researchers have tracked over 100 email campaigns using tax themes to spread malware, steal credentials, and commit financial fraud in early 2026. A major trend involves delivery of legitimate Remote Monitoring and Management (RMM) software such as N-Able, Datto, RemotePC, and Zoho Assist—allowing attackers to establish persistent access while evading detection. One campaign impersonated the U.S. IRS, using a fake "Transcript Viewer" button that downloads N-able RMM. Threat actor TA2730 targets investment and financial institutions across Canada, Switzerland, Singapore, and Australia using spoofed W-8BEN tax forms, directing victims to convincing credential harvesting pages impersonating Swissquote and Questrade. Business Email Compromise (BEC) attacks also surged, with spoofed executive emails requesting employee W-2 records containing names, addresses, and Social Security numbers. [[CyberPress](https://cyberpress.org/tax-scams-drain-victim-funds/)]

---

**[NEW] QR Code Phishing Campaign Impersonates State Courts for Payment Fraud**

Scammers are circulating fake "Notice of Default" traffic violation text messages impersonating state courts across multiple U.S. states, including New York, California, North Carolina, Illinois, Virginia, Texas, Connecticut, and New Jersey. The campaign, which differs from previous toll and parking scams by using embedded QR codes, directs recipients to phishing sites that impersonate state DMVs after solving a captcha. The fake sites request a $6.99 payment along with personal and credit card information. Stolen data enables financial fraud, identity theft, and follow-on phishing. State agencies have repeatedly stated they do not request payments via text messages. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/traffic-violation-scams-switch-to-qr-codes-in-new-phishing-texts/)]

---

## 🛡️ Defense & Detection

**[NEW] 36 Malicious npm Packages Target Strapi CMS with Redis RCE and Persistent C2 Malware**

A sophisticated supply-chain attack has been identified involving 36 malicious npm packages masquerading as Strapi content management system plugins. The packages, published using multiple fake developer accounts (umarbek1233, kekylf12, tikeqemif26, umar_bektembiev1), were designed to target cryptocurrency-related infrastructure and deployed at least eight different malware variants. Attackers exploited Redis configuration commands to achieve RCE, write cron jobs and web shells, and escape Docker containers by writing files outside container boundaries. The malware harvested sensitive files including .env configurations, private keys, and wallet data, while maintaining persistent C2 communication for real-time command execution. Security researchers from Safedep recommend verifying npm packages before installation and monitoring build environments for unusual behavior. [[CyberPress](https://cyberpress.org/rogue-npm-packages-deliver-malware/)] [[GBHackers](https://gbhackers.com/36-malicious-strapi-npm/)]

---

**[NEW] ResokerRAT Abuses Telegram Bot API for Stealthy C2 Communication**

A newly identified Windows RAT called ResokerRAT uses Telegram's Bot API as its command-and-control channel, enabling it to blend with legitimate encrypted traffic and evade traditional network defenses. When executed, the malware establishes a mutex ("Global\\ResokerSystemMutex"), checks for debugger attachments, and polls its Telegram bot for commands. Commands include "/startup" for persistence via Windows Run registry keys, "/screenshot" for capturing screen images via PowerShell, "/download" for fetching additional payloads, and registry modifications to disable Task Manager and User Account Control prompts. The use of a widely trusted messaging platform makes C2 traffic difficult to distinguish from normal user activity. [[CyberPress](https://cyberpress.org/resokerrat-hijacks-windows-via-telegram/)] [[GBHackers](https://gbhackers.com/resokerrat-hijacks-telegram-api/)]

---

**[NEW] Google DeepMind Warns of "AI Agent Traps" — Malicious Web Content Hijacks Autonomous AI**

Google DeepMind researchers have identified a novel attack technique dubbed "AI Agent Traps" that exploits how autonomous AI agents perceive, interpret, and act on web content. As AI agents evolve beyond chatbots to actively browse the web and execute tasks, threat actors can craft adversarial web pages containing hidden instructions tailored for machine interpretation. Six trap types were identified: content injection (hidden malicious instructions in metadata), semantic manipulation (distorting agent reasoning), cognitive state poisoning (tainting learned behavior over time), behavioral control (hijacking operational logic), systemic traps (cascading failures in multi-agent environments), and human-in-the-loop manipulation (influencing human decisions through manipulated outputs). The research, led by scientist Matija Franklin, warns that existing security tools designed for human users cannot detect these machine-targeted threats. [[CyberPress](https://cyberpress.org/hijack-ai-agents-via-malicious-web-content/)] [[GBHackers](https://gbhackers.com/google-deepmind-flags-new-threat/)]

---

## ⚡ Quick Hits

- **[NEW]** Traffic violation phishing scams have evolved to include QR codes, CAPTCHA challenges, and impersonation of state court systems across multiple U.S. states.
- **[NEW]** German authorities have identified Daniil Shchukin as "UNKN," the alleged leader behind GandCrab and REvil ransomware operations, linked to €35M in damages across Germany.
- **[NEW]** Poisoned npm packages continue targeting developers, with 36 malicious Strapi plugins delivering Redis RCE and persistent C2 malware to cryptocurrency-related infrastructure.