---
title: "FortiBleed IAB Identified, Gravity SMTP 17M+ Blocks, ShinyHunters Hits IC Security, CryptoBandits Tor Backdoor, Thailand Healthcare Campaign"
date: 2026-06-20
tags: ["fortibleed","fortinet","cve-2026-4020","gravity-smtp","wordpress","shinyhunters","icarus","klue","cryptobandits","thailand","healthcare","ransomware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "FortiBleed IAB identified on Exploit forum; Gravity SMTP CVE actively exploited at scale (17M+ blocks); ShinyHunters demands payment from IC Security (2.7M records); CryptoBandits Tor-backed clipper detailed; Thailand healthcare campaign analyzed. Patch Gravity SMTP and rotate email API keys."
---

# Daily Threat Intelligence Digest — June 20, 2026

*34 articles ingested and analyzed. Gaps identified via web search.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] FortiBleed — Unit 42 Publishes Independent Analysis, Initial Access Broker Identified on Russian-Language Forum**

Unit 42 published its own threat brief on the FortiBleed credential theft campaign, confirming the threat actors are using a curated password list built from prior breaches and successful vulnerability exploits for internet-wide password spraying against Fortinet, Sophos, and MSSQL services. An **initial access broker (IAB)** on the Russian-language Exploit[.]in forum has claimed responsibility, referencing an unspecified CVE and offering harvested credentials for sale as of June 16. Unit 42 has not validated the IAB's claims but observed the same campaign infrastructure targeting Palo Alto Networks customer telemetry as collateral.

Recorded Future's Insikt Group independently identified malicious infrastructure (IP 85.11.187.8) linked to the campaign, recovering artifacts consistent with a full credential-harvesting and follow-on intrusion workflow: sniffer logs (`fg_capture.log`), Hashcat/Hashtopolis cracking orchestration files, Active Directory enumeration scripts (`ad_enum.py`, `ad_full_audit.py`), password-spraying tooling, SMB/DFS collection scripts, and log-clearing markers. The FortiBleed dataset now covers 73,932 firewall URLs across 194 countries. [[Unit 42](https://unit42.paloaltonetworks.com/large-scale-credential-attacks/); [Malware.News / Recorded Future](https://malware.news/t/fortibleed-campaign-exposing-credentials-for-73-932-fortigate-systems/108081#post_1)]

**Context:** *Previously covered June 18 (initial disclosure), June 19 (CISA formal warning). New today: Unit 42 independent analysis, IAB attribution to Exploit[.]in forum, Insikt Group infrastructure artifacts.*

**Hunting hypothesis:** Monitor for successful admin logins on FortiGate/Sophos edge devices within minutes of high-volume password-failure events — the IAB's workflow sprays first, then accesses immediately upon successful auth.

---

**[NEW] Gravity SMTP Plugin (CVE-2026-4020) — Unauthenticated Info Disclosure Exploited at Scale, 17M+ Wordfence Blocks**

Threat actors are actively exploiting CVE-2026-4020, a medium-severity (CVSS 5.3) unauthenticated information disclosure vulnerability in the **Gravity SMTP WordPress plugin** (100,000+ active installs). The flaw stems from an exposed REST API endpoint (`/wp-json/gravitysmtp/v1/tests/mock-data`) whose `permission_callback` always returns `true`, allowing any unauthenticated visitor to extract a comprehensive JSON system report containing:

- API keys, secrets, and OAuth tokens for configured email integrations (Amazon SES, Google, Mailjet, Resend, Zoho)
- WordPress configuration details (installed plugins, themes, software versions)
- Database configuration (server version, table names)
- PHP environment information

Wordfence has blocked **over 17 million exploit attempts** against protected customers, with a spike of 4 million on June 7 alone. Successful exploitation allows attackers to impersonate the victim organization via email services and perform reconnaissance for follow-on attacks. All plugin versions 2.1.4 and older are affected; patched in version 2.1.5 (released March 17). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-exploit-info-disclosure-bug-in-gravity-smtp-wordpress-plugin/)]

**Indicator:** Requests to `GET /wp-json/gravitysmtp/v1/tests/mock-data?page=gravitysmtp-settings` in web server access logs.

**Recommended action:** Update to Gravity SMTP ≥ 2.1.5 immediately. Rotate any email service API keys and OAuth tokens that may have been exposed.

---

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Klue OAuth Breach — Victim List Grows, Huntress Confirms Data Theft, Salesforce Disables Integration**

Klue CEO Jason Smith publicly confirmed the June 12 security incident, attributing the breach to a **compromised legacy credential associated with an integration service** that allowed attackers to steal OAuth tokens used to connect Klue Battlecards to customer Salesforce environments. CrowdStrike has been engaged for incident response. The "Icarus" extortion group (active since April 2026) used automated Python scripts to query Salesforce REST APIs — conducting slow reconnaissance mapping valuable objects before rapid data exfiltration. **Huntress confirmed** they were among the victims, with stolen data including CRM contacts, sales communications, price quotes, and competitive intelligence reports. Salesforce has disabled the Klue Battlecards integration platform-wide. Known attacker IPs: 138.226.246.94, 212.86.125.24, 213.111.148.90, 94.154.32.160. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/klue-oauth-breach-victim-list-grows-as-icarus-hackers-claim-attack/); [Malware.News](https://malware.news/t/icarus-ransomware-group-compromises-canadian-firm-klue-com/108088#post_1)]

**Context:** *Previously covered June 19 (initial disclosure). New today: Klue CEO statement confirming compromised legacy credential, Huntress confirmed as victim, Salesforce platform-wide disable.*

**Hunting hypothesis:** Review Salesforce API logs for SOQL queries from unexpected IPs hitting `/services/data/v59.0/sobjects` followed by bursts on `/services/data/v59.0/query`. Revoke and rotate OAuth tokens for any Klue or similar third-party Salesforce integrations.

---

**[NEW] ShinyHunters Claims IC Security Breach — 2.7M Records Threatened for Leak by June 22**

The ShinyHunters extortion group claimed responsibility for a cyberattack against **IC Security (icsecurity.com)**, a U.S.-based cybersecurity firm, with a threat to leak **2.7 million compromised records** unless demands are met by June 22, 2026. The group published a "FINAL WARNING" on June 19 demanding payment. IC Security provides physical security systems (access control, surveillance) and cybersecurity services — the compromise of a cybersecurity vendor's own systems raises supply chain concerns for its client base. The attackers claim to have exfiltrated "over 2.7 million records and other internal corporate data." [[DeXpose via Malware.News](https://malware.news/t/shinyhunters-compromise-ic-security-in-major-ransomware-attack/108090#post_1); [DeXpose](https://www.dexpose.io/shinyhunters-compromise-ic-security-in-major-ransomware-attack/)]

---

## 🛡️ Defense & Detection

**[NEW] CryptoBandits — Microsoft Details Tor-Backed Cryptocurrency Clipper with Backdoor Capabilities**

Microsoft disclosed **CryptoBandits**, a Windows-based cryptocurrency clipper active since February 2026 that establishes a lightweight backdoor blending data exfiltration and remote code execution capabilities. The malware deploys a **bundled Tor client** on infected systems, routing all C2 communication through a local SOCKS5 proxy (`localhost:9050`) to reduce DNS visibility and hide its command-and-control location. Distributed via malicious shortcut (.lnk) payloads, CryptoBandits deploys two components: a **worm for USB propagation** and a **clipper/stealer** that:

- Extracts seed phrases and private keys from cryptocurrency wallets
- Replaces clipboard cryptocurrency addresses with attacker-controlled addresses
- Polls C&C every 500ms for instructions via WScript and ActiveXObject
- Multi-layered obfuscation (Python installer + JavaScript payloads all decrypted at runtime)
- Evades Microsoft Defender by excluding specific file paths

Microsoft notes this demonstrates "how lightweight, script-based stealers can deliver outsized impact when paired with anonymized communications and runtime tasking." [[SecurityWeek](https://www.securityweek.com/cryptobandits-malware-doubles-as-a-backdoor-abuses-tor/)]

**Detection:** Monitor for local SOCKS proxy usage (localhost:9050), WScript spawning processes with network connections, and scheduled tasks launching obfuscated JavaScript.

---

**[NEW] Thailand Healthcare Sector Targeted via RAR-Backed Multi-Stage Infection Chain**

Seqrite's Threat Research Unit documented an active malware campaign targeting **Thailand's healthcare ecosystem**, including Ministry of Health personnel, hospital administration, and clinical departments. Active since at least April 7, 2026, the campaign uses healthcare-themed spear-phishing lures (medical equipment approvals, patient admission requests, CT scan results) delivered through malicious RAR archives. The infection chain follows a consistent pattern:

**RAR → Obfuscated BAT → Rouki-Obfuscated Payload Loader → Startup Persistence (WindowSecuryt.bat) → Python Infostealer (sim.py) → Telegram Exfiltration**

Key technical details: GitHub-hosted payload delivery (masqueraded as `.png` files), PowerShell-based decoding routines, auto-cleanup of temporary artifacts, and a Python-based information stealer that exfiltrates data via Telegram. The targeting specificity — tailored lure filenames for radiology, procurement, and clinical staff — suggests either prior reconnaissance of healthcare organizations or sector-informed targeting from knowledge of operational workflows. All observed samples were uploaded from Thailand IPs, suggesting in-country staging infrastructure. [[Malware.News / Seqrite](https://malware.news/t/threat-actors-weaponizing-rar-archives-to-target-thailand-s-healthcare-sector/108073#post_1)]

**IOCs:** GitHub repos `ud-7-te/ud-vtn`, `d7-te/vtn`; persistence path `%STARTUP%\WindowSecuryt.bat`; C2 staging via raw.githubusercontent.com.

---

## ⚡ Quick Hits

- **Handala Threat Group profile** — Iranian-linked hacktivist group (pro-Palestinian agenda) with multi-stage wiper attacks against Israeli and US targets. Notable: launched "RedWanted" doxing site in March 2026; claimed wiper attack on Stryker medical devices and breach of FBI Director Kash Patel's personal email. [[Malware.News](https://malware.news/t/handala-threat-group-tactics-targets-and-attack-timeline/108092#post_1)]
- **Bombay High Court blocks FulcrumSec data leak** — Indian court issued an injunction preventing publication of stolen data from FulcrumSec, a security firm. Rare example of judicial intervention as a data leak prevention measure. [[Malware.News](https://malware.news/t/bombay-high-court-blocks-fulcrumsec-data-leak/108078#post_1)]
- **Mitsubishi Electric security advisory (AV26-616)** — ICS advisory for Mitsubishi Electric control system products. Specifics not detailed in feed. [[Malware.News](https://malware.news/t/control-systems-mitsubishi-electric-security-advisory-av26-616/108086#post_1)]
- **Aurora ransomware claims ALS Global breach** — Global testing/inspection company (ASX:ALQ, 20,500+ employees, 65+ countries) listed on Aurora's leak site. No statement from ALS Global yet. [[Malware.News](https://malware.news/t/aurora-ransomware-strikes-als-global/108091#post_1)]
- **SecurityWeek In Other News roundup** — Apple patched Beats Studio Buds eavesdropping flaw (CVE-2025-20701), DOT closed Delta CrowdStrike probe, and AWS Continuum developments. [[SecurityWeek](https://www.securityweek.com/in-other-news-apple-patches-beats-eavesdropping-flaw-dot-closes-delta-crowdstrike-probe-aws-continuum/)]
- **SocGholish cleanup continues** — Law enforcement cleaned 14,971 compromised WordPress sites and seized 106 servers in Operation Endgame. [[Malware.News](https://malware.news/t/nearly-15-000-infected-websites-cleaned-in-socgholish-crackdown/108084#post_1)]
