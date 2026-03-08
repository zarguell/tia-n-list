---
title: UAT-10027 healthcare attacks 🏥, Velvet Tempest ClickFix 💣, AI-powered cyberattacks 🤖, GitHub supply chain breach 📦
date: 2026-03-08
tags: ["healthcare targeting","clickfix attacks","ai integration","supply chain attacks","ransomware","malware","cyber warfare","blockchain abuse","threat actors"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: UAT-10027 is compromising U.S. healthcare organizations with Dohdoor backdoor that uses DNS-over-HTTPS for stealthy C2 communications before deploying Cobalt Strike beacons. Velvet Tempest is employing sophisticated ClickFix attacks to deliver Termite ransomware while threat actors are increasingly integrating AI across all attack stages and GitHub repositories distribute BoryptGrab stealer through supply chain attacks.
---

# Daily Threat Intel Digest - 2026-03-08

## 🔴 Critical Threats & Active Exploitation

**[NEW] UAT-10027 Campaign Targets U.S. Healthcare with Dohdoor Backdoor**  
Undocumented threat group UAT-10027 is actively compromising U.S. healthcare and education organizations with Dohdoor malware, which uses DNS-over-HTTPS (DoH) for stealthy command-and-control before deploying Cobalt Strike beacons. The healthcare targeting is particularly concerning as it enables persistent access to sensitive patient data and critical medical infrastructure, with attackers leveraging DoH to blend in with legitimate encrypted traffic and bypass network inspection controls [[Cyberwarzone](https://cyberwarzone.com/2026/03/08/uat-10027-targets-u-s-healthcare-with-dohdoor-malware-using-doh-c2/)].

**[NEW] Velvet Tempest Deploys Termite Ransomware via ClickFix Attacks**  
Termite ransomware operations linked to Velvet Tempest (aka DEV-0504) are using sophisticated ClickFix attacks that trick victims into pasting obfuscated commands into Windows Run dialogs, triggering malware delivery through nested cmd.exe chains and finger.exe. The attackers then use legitimate Windows utilities to deploy CastleRAT backdoors and DonutLoader, ultimately staging for ransomware deployment. Velvet Tempest has an extensive history deploying major ransomware variants including Ryuk, REvil, Conti, BlackCat, and LockBit, making their evolution to ClickFix techniques a significant escalation in social engineering tactics [[MalBeacon via BleepingComputer](https://www.bleepingcomputer.com/news/security/termite-ransomware-breaches-linked-to-clickfix-castlerat-attacks/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Middle East Cyber Mobilization Accelerates to 9-Hour Fuse Following Kinetic Strikes**  
Following "Operation Epic Fury" on February 28, hacktivist groups mobilized cyber attacks within just 9 hours, dramatically compressing the reaction time from days to hours. The campaign is dominated by two groups - Keymous+ (35.5% of attacks) and DieNet (32.7%) - concentrating 53% of attacks on government institutions to induce civil paralysis. Notably, Russian-aligned NoName057(16) has joined the pro-Iranian alliance, creating cross-regional cyber warfare convergence that breaks down geographic defense silos [[SOC Fortress](https://socfortress.medium.com/the-9-hour-fuse-5-surprising-realities-of-the-middle-easts-new-digital-front-f6f99be9b39c?source=rss-36613248f635------2)].

**[UPDATE] Aeternum C2 Botnet Abuses Polygon Blockchain for Resilient Infrastructure**  
The Aeternum C2 botnet has refined its techniques for storing encrypted command-and-control instructions on the Polygon blockchain, making traditional takedown efforts significantly harder. This blockchain-based C2 approach represents a fundamental evolution in resilient malware infrastructure that can withstand infrastructure seizure attempts. The technique continues the trend first reported on March 3, now with enhanced blockchain integration that complicates disruption efforts [[Cyberwarzone](https://cyberwarzone.com/2026/03/08/aeternum-c2-botnet-abuses-polygon-blockchain-to-hide-malware-commands-and-evade-takedowns/)].

**[NEW] Microsoft Reports AI Integration Across All Attack Stages**  
Threat actors are systematically incorporating generative AI to accelerate attacks and lower technical barriers across reconnaissance, phishing, malware development, and post-compromise activities. North Korean groups Jasper Sleet and Coral Sleet are using AI to generate fraudulent identities for remote worker schemes, craft culturally appropriate phishing content, and rapidly provision malicious infrastructure. Microsoft has observed attackers using jailbreaking techniques to bypass AI safeguards when generating malicious code, signaling AI's normalization in attacker toolkits [[Microsoft](https://www.bleepingcomputer.com/news/security/microsoft-hackers-abusing-ai-at-every-stage-of-cyberattacks/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] GitHub Campaign Distributes BoryptGrab Stealer via 100+ Repositories**  
Over 100 GitHub repositories are actively distributing the BoryptGrab information stealer, representing a significant supply chain attack vector targeting developers and organizations relying on open-source code. The campaign abuses GitHub's infrastructure to deliver malware that can harvest credentials, financial data, and other sensitive information from compromised systems [[SecurityWeek](https://www.securityweek.com/over-100-github-repositories-distributing-boryptgrab-stealer/)].

## 🛡️ Defense & Detection

**[NEW] Adversary Consolidation Doubles Per-Host Attack Intensity**  
February 2026 telemetry reveals a 50% reduction in unique attacking hosts but near-doubling of per-host attack intensity (from 877 to 1,650 events/host), indicating adversaries are consolidating into more efficient, higher-quality compromised infrastructure. The shift shows increased targeting of VNC services (doubling to 60.1M events) alongside DNS reconnaissance surge (+150%), suggesting refined botnet management that bypasses traditional IP reputation controls [[Deception.Substack via HoneyDB](https://medium.com/@foospidy/adversary-consolidation-per-host-attack-intensity-doubles-in-february-2026-626c5cd9a163?source=rss-58df3dedf52b------2)].

**[NEW] OpenAI Launches Codex Security for Automated Vulnerability Detection**  
OpenAI's Codex Security agent (formerly Aardvark) provides context-aware vulnerability discovery with 84% reduction in noise and 90% fewer over-reported severities during beta testing. The system generates editable threat models, validates findings in sandboxed environments, and proposes automated patches. It has already discovered critical vulnerabilities in OpenSSH, GnuTLS, and other widely-used open-source projects, assigning 14 CVEs to date [[OpenAI via CyberPress](https://cyberpress.org/openai-rolls-out-codex-security/)].