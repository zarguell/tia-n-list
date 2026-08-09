---
title: "🔴 Puerto Rico voting systems found critically insecure, 🚨 Suisun City emergency after 911 outage, ⚠️ LoadMaster joins CISA KEV, 🎯 Head Mare trojanizes TrueConf installers, 🎯 BdThemes feed poisoning creates rogue admins"
date: 2026-08-09
tags: ["election security","critical infrastructure","CISA KEV","supply chain","ransomware","malware","vulnerabilities"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Election infrastructure heads into the midterms with a dozen-plus critical vulnerabilities and no remediation planned, while malware took down Suisun City's 911 dispatch; CISA added Progress LoadMaster to its KEV after 792 exploit attempts, and Head Mare's trojanized TrueConf installers plus a BdThemes supply-chain poisoning extend the week's supply-chain threat picture."
---

# Daily Threat Intelligence Digest — August 9, 2026

*10 articles ingested and analyzed from curated cyber intelligence feeds.* External research surfaced a CISA KEV addition now under active exploitation: Progress Kemp LoadMaster CVE-2026-8037.

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] Puerto Rico Voting Systems Carry Critical Flaws — Federal Research Halted After Political Pushback

Mojave Research documented at least a dozen high- and critical-severity vulnerabilities in the Dominion voting systems used in Puerto Rico's 2024 elections — reused and hardcoded passwords, disabled firewalls, open ports, and broken cryptography, plus cellular modems opening pathways into supposedly isolated software — during an ODNI-commissioned review, but found no evidence the weaknesses were exploited or votes altered. The firm's federal work ended via stop-work order after Trump adviser Kurt Olsen pushed back on findings that did not support election-manipulation claims, the researchers said Friday at DEF CON's Voting Village. The roughly 100-page report remains unremediated: Liberty Vote, which acquired Dominion's election business, told researchers it plans no changes before November, and the team expects the same insecure configuration to be deployed in the midterms.

**Source:** [Nextgov/FCW](https://www.nextgov.com/cybersecurity/2026/08/voting-machine-researchers-say-federal-work-abruptly-ended-after-trump-ally-pushed-back-their-findings/415300/)

### [NEW] Suisun City Declares Emergency as Cyberattack Downs 911 Dispatch

Malware infected Suisun City, California's IT systems at 5:45 a.m. Friday, taking down 911 routing, police and fire dispatch, and other critical city systems, prompting the council to unanimously declare a state of emergency Saturday. Officials shut down the entire network to contain the threat and preserve evidence for a federal investigation; emergency calls are being routed through the Solano County dispatch center and officials say there is no imminent public danger. The FBI, DHS, and California's OES are assisting, and officials have not said how the malware entered the city's systems or who is responsible.

**Sources:** [CBS Sacramento](https://www.cbsnews.com/sacramento/news/suisun-city-california-malware-emergency/) · [Malware News](https://malware.news/t/city-of-suisun-declares-local-emergency-after-cyberattack-downs-911-dispatch-system/124608)

### [NEW] Progress Kemp LoadMaster Joins CISA KEV — Unauthenticated Command Injection Under Attack

CISA added CVE-2026-8037 (CVSS 9.6) to its Known Exploited Vulnerabilities catalog on August 7, citing active exploitation of an unauthenticated command injection in Progress Kemp LoadMaster that lets attackers run arbitrary commands on the appliance without credentials — rooted in a flawed escape_quotes() function per watchTowr Labs. Telemetry logged 792 exploitation attempts over 41 days from 65 unique IPs across 18 countries, with eSentire documenting largely unsuccessful attacks as early as July. Federal agencies face an August 10 BOD 26-04 deadline; treat every internet-facing LoadMaster as a priority patch and audit for post-exploitation artifacts.

**Sources:** [The Hacker News](https://thehackernews.com/2026/08/progress-kemp-loadmaster-flaw-hits-cisa.html) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### [UPDATE] City of Coweta Refuses Ransom After System-Wide Attack

Coweta, Oklahoma will not pay the ransom demand behind the August 5 attack on its systems — the city manager, who dealt with a ransomware infection at a previous city that was reinfected weeks after payment, says paying only invites recurrence. The city continues recovery from backups while officials assess the full scope of the intrusion.

**Source:** [Malware News](https://malware.news/t/city-of-coweta-refuses-to-pay-ransom-after-system-wide-cyberattack/124604)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] Head Mare Trojanizes TrueConf Installers to Push PhantomCore Backdoors

Kaspersky documented Head Mare exploiting unpatched TrueConf Server instances — reaching the video-conferencing platform through the default-open TCP port 4307 and chaining two flaws (KLCERT-26-057/058) to escape the app sandbox and execute code as SYSTEM — then replacing the legitimate client installer with a trojanized, unsigned build carrying the PhantomCore backdoor. A second implant, PhantomGraph, runs through two DLLs commanded over OneDrive and has been observed dumping LSASS memory and opening reverse SSH tunnels. With fixes only in TrueConf Server 5.3.9/5.4.9/5.5.5, anyone who pulls a client from a compromised server — including employees of partner organizations joining meetings — is exposed; Kaspersky reports multiple active campaigns against Russian industry, government, and energy targets.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-breach-trueconf-to-trojanize-client-installers-with-backdoors/)

### [NEW] BdThemes Supply-Chain Poisoning Turns Plugin Feed Into Rogue-Admin Factory

Wordfence disclosed a supply-chain compromise of BdThemes WordPress plugins in which an actor with write access to the vendor's promotional-feed storage bucket swapped legitimate JSON for XSS payloads that fire inside every logged-in admin's browser on each wp-admin page load. The injected script exploits an unescaped attribute introduced in March and silently creates a rogue administrator with deterministic credentials (bd_ plus a hostname-derived base36 hash), beacons the result to C2, and sets a local flag to run once — with the C2 tying back to the same operators behind the Advanced Responsive Video Embedder and OptinMonster supply-chain attacks of the past two months. All affected plugins are temporarily closed in the WordPress directory pending investigation; sites running Element Pack, Prime Slider, or other BdThemes plugins should audit for unexpected admin accounts and outbound beaconing.

**Source:** [Wordfence via Malware News](https://malware.news/t/psa-supply-chain-compromise-in-bdthemes-ecosystem-via-poisoned-api-response/124607)

### [NEW] CERT Polska: Private APN Was the Unseen Vector in December's Poland Energy Attacks

A follow-up report on the December 29, 2025 destructive attacks on Poland's energy sector reveals a second combined heat-and-power plant — supplying heat to 50,000 residents — was also hit in parallel, with attackers shutting down a steam turbine and the water-treatment system and interrupting cogeneration. The three-month investigation surfaced a previously unobserved access path: an attacker-operated private APN into the OT network, the first real-world use of that vector, enabled by a misconfiguration that let any device on the APN communicate with the plant. CERT Polska warns the configuration is common in Poland and other countries and published recommendations for private APN-based deployments; the findings were presented at DEF CON.

**Source:** [CERT Polska](https://cert.pl/en/posts/2026/08/incident-follow-up-report-energy-sector-2025/)

### [NEW] Multi-Stage PowerShell Loader Distributes via Vercel-Hosted Payloads

Researchers dissected an unattributed multi-stage loader in which PowerShell served directly from 203.188.171.166 and dorenzaa.com pulls a ZIP from Vercel-hosted infrastructure, drops it under %LOCALAPPDATA%\jsDownload, and executes Grape.exe; additional Vercel artifacts include executables and heavily obfuscated loaders using hidden IEX, Base64, and XOR encoding, capped with a decoy "Verification complete!" message. Neither C2 host drew any VirusTotal vendor detections at analysis time, and the initial infection vector remains unknown — a reminder that loader chains hosted on legitimate CDNs can slip past reputation-based blocking.

**Source:** [Malware News](https://malware.news/t/investigating-a-multi-stage-powershell-loader/124606)
