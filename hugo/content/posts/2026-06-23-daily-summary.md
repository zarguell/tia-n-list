---
title: "Xsolis Breach, PixelSmash RCE, FortigateSniffer, GPT-5.5-Cyber, PQC EO, Bucket Hijack"
date: 2026-06-23
tags: ["Xsolis","PixelSmash","CVE-2026-8461","FortiBleed","OpenAI Daybreak","GPT-5.5-Cyber","post-quantum cryptography","WhatsApp phishing","Scattered Spider","Unit 42","bucket hijacking","AutoJack","PQC","Aurora ransomware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "48 articles ingested. Critical: Xsolis healthcare breach affects 1.4M; FortiBleed campaign deploys custom FortigateSniffer on 430K+ firewalls; PixelSmash (CVE-2026-8461) RCE in FFmpeg-powered media apps; OpenAI launches GPT-5.5-Cyber Daybreak expansion; Unit 42 reveals universal cloud bucket hijacking. Recommended actions: patch FFmpeg to 8.1.2, rotate FortiGate credentials, review cloud storage bucket permissions, prepare for PQC migration deadlines."
---
# Daily Threat Intelligence Digest — June 23, 2026

*48 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — `reddit_gap_check.py` unavailable (chronic failure threshold exceeded, 24+ consecutive days per prior digests). External gap detection via web search identified one critical gap: OpenAI Daybreak expansion (GPT-5.5-Cyber) absent from Miniflux feed coverage. Prior digests: June 18–22, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Xsolis Data Breach Exposes 1.4M Healthcare Records — Phishing Attack Compromised PII/PHI**

Healthcare technology company Xsolis disclosed a data breach affecting **1,396,519 individuals** after attackers gained access to its systems via a targeted phishing campaign on January 20. The intruders exfiltrated files containing personal and protected health information — names, dates of birth, SSNs, health insurance data, and medical treatment records — received by Xsolis from its client hospitals and health systems. [[SecurityWeek](https://www.securityweek.com/xsolis-data-breach-affects-1-4-million-individuals/)]

The breach was added to the HHS data breach tracker on Monday. No ransomware group has claimed responsibility. Xsolis stated it is "not aware of any actual or attempted misuse" of the stolen data. The incident underscores that healthcare service providers remain prime targets — a single phishing foothold at a third-party vendor cascades into exposure for millions of patients across multiple provider organizations.

---

**[UPDATE] FortiBleed Campaign — Custom FortigateSniffer Harvests Auth Traffic From 430K+ Compromised Firewalls**

SOCRadar published new operational details on the large-scale FortiBleed credential theft campaign, revealing the attackers deployed a **Go-based tool called "FortigateSniffer"** on compromised FortiGate devices after gaining administrative access via credential stuffing and brute-force attacks. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fortibleed-campaign-used-custom-fortigate-sniffer-to-steal-credentials/)]

The tool abuses FortiOS's built-in `diagnose sniffer packet` command to monitor traffic for authentication protocols across **24 protocols** including RADIUS, NTLM, Kerberos, LDAP, SMB, RDP, and database services. Captured PCAP data is processed through a "PCAP Deep Analysis Toolkit" that extracts cleartext credentials, password hashes, and Kerberos tickets, then generates Hashcat-ready files for offline cracking on a distributed GPU cluster.

The campaign has been active since at least **February 2026**, targeting more than **430,000 FortiGate firewalls** worldwide. The operator functions as an initial access broker (IAB), selling harvested network access to ransomware affiliates.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] WhatsApp Phishing Campaign Abuses Compromised Accounts, Installs ManageEngine for Remote Access**

Kaspersky identified an ongoing malware campaign targeting WhatsApp users across **11 countries** — Brazil, India, Mexico, Singapore, the UK, Spain, Taiwan, Australia, Russia, Vietnam, and Malaysia — using compromised accounts to distribute malicious VBScript files disguised as business and financial documents. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/whatsapp-phishing-attack-uses-fake-business-docs-to-hack-pcs/)]

The infection chain: compromised WhatsApp account sends messages containing only an obfuscated VBScript file → victim opens the file → VBScript downloads two additional scripts that disable UAC via Registry modification → a ZIP archive containing **ManageEngine Endpoint Central** is silently installed and configured to connect to attacker-controlled management servers → full remote administration access. On WhatsApp Desktop, the VBScript executes directly via `wscript.exe`.

While not definitively attributed, researchers found Chinese-language indicators and infrastructure overlap with IPs previously tied to **ValleyRAT** and **Gh0st RAT** activity.

---

**[NEW] Scattered Spider Members Plead Guilty Over £39M Transport for London Cyber Attack**

Two individuals believed to be members of the **Scattered Spider** cybercrime group changed their pleas to guilty just before trial, in connection with the September 2024 cyberattack against Transport for London that caused months of operational disruption and cost £39 million. [[Malware.News/DataBreaches](https://databreaches.net/2026/06/22/two-men-believed-to-part-of-scattered-spiders-plead-guilty-over-39m-tfl-cyber-attack/)]

This marks one of the first significant legal outcomes against the loosely organized cybercrime collective known for SIM-swapping, social engineering, and ransomware affiliate work.

---

**[NEW] Aurora Ransomware Claims Two New Victims — Insurance Underwriter and Dutch Civil Engineering Firm**

The Aurora ransomware operation added **NationsBuilders Insurance Services** (US crane/rigging insurance MGU) and **NTP B.V. Civil Engineering Construction** (Netherlands) to its leak site on June 22. NBIS reported 2.7 million filetree entries across 24 shares. [[Malware.News/DeXpose](https://malware.news/t/aurora-ransomware-attack-on-nationsbuilders-insurance-services/108134#post_1); [Malware.News/DeXpose](https://malware.news/t/aurora-ransomware-targets-ntp-b-v-civil-engineering/108133#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] FFmpeg PixelSmash (CVE-2026-8461) — MagicYUV Heap Overflow Enables RCE in Jellyfin, Nextcloud, Kodi**

JFrog disclosed a heap out-of-bounds write in FFmpeg's MagicYUV decoder — dubbed **PixelSmash** — that enables remote code execution on Jellyfin media servers and denial-of-service conditions in Kodi, Emby, Nextcloud, PhotoPrism, and OBS Studio (CVSS 8.8). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ffmpeg-fixes-pixelsmash-flaw-in-widely-used-video-decoder/)]

JFrog demonstrated full RCE against Jellyfin 10.11.9: a crafted MagicYUV AVI file triggers ffprobe metadata extraction → OOB write → AVBuffer.free hijacked to system(). FFmpeg 8.1.2 patches the flaw.

---

**[NEW] Unit 42 Reveals Universal Bucket Hijacking — Silent Cloud Data Exfiltration Across AWS, Azure, GCP**

Unit 42 disclosed a bucket hijacking technique exploiting global uniqueness of storage bucket names — an attacker with `storage.buckets.delete` permission can delete a victim's bucket, recreate it under their account, and silently redirect active data streams. [[Unit 42](https://unit42.paloaltonetworks.com/cloud-bucket-hijacking-risks/)]

---

## 🛡️ Defense & Detection

**[NEW] OpenAI Expands Daybreak With GPT-5.5-Cyber — Codex Security Plugin and Patch the Planet Initiative**

OpenAI announced a major expansion of its Daybreak cybersecurity initiative, releasing GPT-5.5-Cyber to trusted defenders alongside Codex Security for automated vulnerability discovery and patch generation. [[The Hacker News](https://thehackernews.com/2026/06/openai-expands-daybreak-with-gpt-55.html); [OpenAI](https://openai.com/index/daybreak-securing-the-world/)] **[web search gap]**

OpenAI also launched **Patch the Planet** with Trail of Bits for high-impact open-source projects. Daybreak has already surfaced 8 Linux kernel info-leak PoCs + 24 LPE exploits, a 23-year-old OpenBSD use-after-free, 34 FreeBSD vulns, 6 dnsmasq CVEs, an HTTP/2 Bomb DoS, and multiple browser flaws.

This comes alongside a **Five Eyes intelligence warning** that frontier AI hacking models are "months away" from broad availability. [[CyberScoop](https://cyberscoop.com/five-eyes-alliance-say-advanced-ai-hacking-models-months-away/)]

---

## 📋 Policy & Industry News

**[NEW] Trump Signs Executive Order Accelerating Post-Quantum Cryptography Migration**

Executive Order 14409 requires federal agencies to transition high-value assets to PQC for key establishment by Dec 31, 2030 and digital signatures by Dec 31, 2031. [[SecurityWeek](https://www.securityweek.com/trump-signs-executive-order-accelerating-post-quantum-cryptography-migration/)]

---

## ⚡ Quick Hits

- **JaredFromSubway MEV bot hacked — $15M crypto theft** [[BleepingComputer](https://www.bleepingcomputer.com/news/security/jaredfromsubway-mev-bot-hacked-in-15-million-crypto-theft/)]
- **Cherry Health data breach notification** — April incident disclosed June 18 [[Malware.News/DataBreaches](https://databreaches.net/2026/06/22/cherry-health-provides-preliminary-notice-of-recent-data-breach/)]
- **Flare: "Search Your Target" credential market** — $20/query targeted credential extraction [[BleepingComputer/Flare](https://www.bleepingcomputer.com/news/security/a-glimpse-into-the-search-your-target-market-for-stolen-credentials/)]
- **Dirkjanm.io: Conditional Access bypass via resource exclusion** — Microsoft fix rolling out June 15 [[dirkjanm.io](https://dirkjanm.io/bypassing-conditional-access-with-resource-exclusion/)]
- **Microsoft DART Report #9: Two unrelated threat actors in one intrusion** [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/06/22/one-intrusion-two-cyberattackers-uncovering-parallel-threat-activity/)]
- **CVE-2024-40766: SonicWall — patch fixed the bug, not the config** [[SANS ISC](https://malware.news/t/cve-2024-40766-the-patch-fixed-the-bug-nobody-fixed-the-configuration-tue-jun-23rd/108136#post_1)]
