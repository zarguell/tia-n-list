---
title: "🇷🇺 Turla STOCKSTAY backdoor, ⚙️ PTC Windchill exploited, 🌏 CL-STA-1062 APT report, 🔵 Bluekit BitM phishing, 🇵🇱 SIM-swap bust, 🏭 Akira victims"
date: 2026-06-26
tags: ["turla","stockstay","ptc-windchill","cve-2026-12569","lantronix","cve-2025-67038","cl-sta-1062","tinyrct","miasma","supply-chain","bluekit","phishing","shopify","sim-swapping","cellebrite","akira-ransomware","mcp","windows-10-esu","draftkings"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Turla's STOCKSTAY .NET backdoor analyzed by Google Threat Intelligence. CISA adds PTC Windchill CVE-2026-12569 to KEV. CL-STA-1062 APT targets SE Asian energy. Bluekit phishing kit adds browser-in-the-middle. Poland arrests SIM-swapping gang. Akira claims two US victims."
---

# Daily Threat Intelligence Digest — June 26, 2026

*56 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — `reddit_gap_check.py` unavailable (chronic failure threshold exceeded, 25+ consecutive days per prior digests). External gap detection via web search found no critical gaps beyond feed coverage. Prior digests: June 21–25, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Turla's STOCKSTAY Backdoor — Google Exposes Russian FSB-Aligned APT's .NET Espionage Implant Targeting Ukrainian Military**

Google Threat Intelligence Group has published a comprehensive analysis of STOCKSTAY, a multi-component .NET backdoor attributed with high confidence to the Russia-linked threat actor **Turla** (FSB Center 16), revealing an espionage platform in active development since at least December 2022. [[SecurityWeek](https://www.securityweek.com/russian-apt-deploys-stockstay-backdoor-against-ukrainian-targets/); [Google Cloud Blog](https://cloud.google.com/blog/topics/threat-intelligence/stockstay-turla-intelligence-gathering)]

STOCKSTAY consists of three core components communicating via WM_COPYDATA IPC: **STOCKBROKER** (proxy-aware WebSocket tunneler using websocket-sharp), **STOCKMARKET** (orchestrator with encrypted on-disk config disguised as cryptocurrency market data), and **STOCKTRADER** (backdoor supporting file ops, registry manipulation, command execution, screen capture, and system survey via WMI). The implant generates a unique 4096-bit RSA key pair per infection and encrypts all C2 traffic over secure WebSocket connections.

GTIG has documented a detailed operational timeline: earliest samples from September 2023 (Germany), deployment alongside KAZUAR during a Mandiant IR in January 2024 (Ukraine, via compromised domain controller), MSI-based delivery targeting Italian foreign policy entities (February 2024), drone-themed phishing with WinRAR CVE-2025-8088 (November 2025, Ukraine), and continued targeting into 2025–2026. Delivery vectors include malicious RDP files, compromised Ukrainian government WordPress sites, and phishing emails from compromised academic accounts.

**Key overlaps with KAZUAR:** The K1MORPHER string obfuscation (based on the Squirrel3 PRNG) now appears in both malware families. Environmental keying (hostname or domain hash required for config decryption) is used in both ecosystems. GTIG assesses with moderate confidence that STOCKSTAY and KAZUAR share developer(s).

**Hunting hypothesis:** Monitor for WebSocket connections to Render/Glitch/Heroku-hosted endpoints under `/ws` path from .NET processes, registry Run keys pointing to `%LOCALAPPDATA%\Programs\SMN\`, and scheduled tasks named `GoogleUpdaterTask*`. C2 infrastructure observed: `wss://wool-basalt-clock.glitch.me/ws`, `wss://weatherdataai.theworkpc.com/ws`, `wss://canal1zac1a.onrender.com/ws`, `wss://driverx86-adobe.onrender.com/ws`.

---

**[NEW] First-Ever Exploitation of PTC Windchill Vulnerability (CVE-2026-12569) — CISA Adds to KEV, Manufacturing PLM Systems in Crosshairs**

CISA has added CVE-2026-12569 to its Known Exploited Vulnerabilities catalog after confirming active exploitation of a critical remote code execution vulnerability in **PTC Windchill PDMlink and FlexPLM** — product lifecycle management software used extensively in manufacturing and retail supply chains. [[SecurityWeek](https://www.securityweek.com/first-ever-exploitation-of-ptc-windchill-vulnerability-discovered-in-the-wild/); [CISA](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)]

The flaw is an improper input validation vulnerability allowing an unauthenticated, remote attacker to execute arbitrary code by sending a malicious request. This is the first known in-the-wild exploitation of a Windchill vulnerability. PTC has released patches. Attacker naming convention observed: webshells use 16 lowercase hex characters — security teams should hunt for POST requests to `/Windchill/login/[0-9a-f]{16}.jsp`.

**Recommended action:** Patch PTC Windchill and FlexPLM immediately. Monitor for anomalous POST requests to Windchill login endpoints with hex-named JSP files.

---

**[UPDATE] Lantronix EDS5000 (CVE-2025-67038) — Exploitation Confirmed After OT Threat Warning, Attackers Reverse-Engineered the Patch**

Researchers at Forescout confirmed that exploitation of CVE-2025-67038, the critical unauthenticated OS command injection (CVSS 9.8) in **Lantronix EDS5000 serial-to-ethernet converters**, was detected in a honeypot on April 5 — after Lantronix released a patch but **before** Forescout published its BRIDGE:BREAK technical analysis. [[SecurityWeek](https://www.securityweek.com/lantronix-serial-to-ip-converter-flaw-exploited-in-attacks-after-ot-threat-warning/); [Forescout](https://www.forescout.com/blog/analyzing-active-exploitation-of-lantronix-and-openwrt-luci/)]

This timing strongly suggests the attackers reverse-engineered the patch to develop an exploit, a tactic known as patch-gapping. The vulnerability allows unauthenticated command injection at root level by concatenating the supplied username directly into a shell command. CISA added this vulnerability to KEV on June 23. Patched in firmware 2.2.0.0R1.

**Context:** *Previously covered June 23–25 (CISA KEV addition). New today: Confirmed exploitation in the wild confirmed by Forescout honeypot data, patch-gapping vector identified.*

**Recommended action:** Verify Lantronix EDS5000 firmware is updated to 2.2.0.0R1. For OT environments unable to patch immediately, isolate these devices from internet-facing networks.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] CL-STA-1062: Chinese-Speaking APT Targets Southeast Asian Governments and Critical Energy Infrastructure with TinyRCT Backdoor**

Unit 42 published a detailed report on **CL-STA-1062** (aka UAT-7237), a Chinese-speaking threat actor active since at least March 2022, targeting government entities and state-owned energy enterprises across Southeast Asia. [[Unit 42](https://unit42.paloaltonetworks.com/cl-sta-1062-tinyrct-backdoor/)]

The actor's toolkit blends open-source components (SoftEther VPN, Mimikatz, JuicyPotato, VNT, yuze, fscan) with a custom .NET backdoor tracked as **TinyRCT** — a lightweight RAT with arbitrary command execution, file enumeration/exfiltration, screen capture, and a self-destruct mechanism. TinyRCT performs environment validation (checks it runs from `%LOCALAPPDATA%`), generates a unique GUID victim profile, and communicates via AES-128-CBC encrypted HTTP with a 10-second beacon interval.

Infection chain: malicious `chrome_setup.zip` containing a legitimate signed `chrome_setup.exe` + malicious `chrome_setup.exe.config` + malicious DLL uses AppDomainManager Injection. The loader checks for `%USERPROFILE%\Downloads`, then retrieves TinyRCT from staging server, saves as `PerfWatson2.exe` (masquerading as Visual Studio telemetry), and creates `GoogleUpdaterTaskSystem*` scheduled task for persistence.

Unit 42 observed compromise of **at least 10 distinct organizations** between October–December 2025, with APT-level operational security: configuration backups before modification, use of compromised infrastructure within target countries, and tunneling tools disguised as VMware executables or XDR agents.

**IOCs:** C2 at `139.180.134[.]221`, `202.182.102[.]5`, `45.76.210[.]43`, `45.32.113[.]172`.

---

**[UPDATE] Miasma Returns: Leo Platform npm Compromise — 23 Malicious Packages, binding.gyp Execution Bypasses Metadata Scanners**

The Shai-Hulud Miasma supply chain campaign has struck again: the czirker npm maintainer account was compromised on June 25, publishing 23 malicious package versions targeting the **RStreams** and **Leo Platform** ecosystems. [[Malware.News/Sonatype](https://malware.news/t/miasma-returns-leo-platform-compromise-in-npm/108229#post_1)]

This wave continues the Miasma playbook Sonatype previously documented — avoiding obvious `preinstall`/`postinstall` scripts in favor of **`binding.gyp`** execution via `node-gyp` during package installation. A package can look clean in metadata and still execute malicious code before the application ever imports it. Targets include GitHub tokens, npm publishing tokens, cloud credentials, CI/CD secrets, SSH keys, and AI coding assistant configuration files.

**Context:** *Previously covered June 18–24 (initial Miasma campaign, Shai-Hulud worm, Mini Shai-Hulud, binding.gyp evasion, AI persistence files). New today: Leo Platform and RStreams ecosystem compromise, 23 additional malicious packages, czirker maintainer account takeover.*

**Recommended action:** Review lockfiles and SBOMs for Leo Platform and RStreams package versions published June 25. Treat affected systems as potentially compromised — rotate credentials only after persistence removal.

---

## 🛡️ Defense & Detection

**[NEW] Bluekit Phishing Kit Adopts Browser-in-the-Middle — 70+ New Hostnames, rrweb DOM Streaming for Real-Time Credential Theft**

The Bluekit phishing-as-a-service platform has evolved significantly, adding browser-in-the-middle (BitM) capabilities that use the open-source `rrweb` JavaScript library to serialize DOM changes and stream them over WebSocket to the attacker's browser session. Netcraft reports 70+ new hostnames identified over the past week. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/bluekit-phishing-kit-adopts-browser-in-the-middle-for-login-theft/)]

Unlike adversary-in-the-middle setups, BitM gives the victim a legitimate login page loaded in the attacker's browser — authentication completes in the attacker's session, granting an active session token. Anti-analysis features: randomized CSS filters (defeats screenshot detection), >1MB frequently changing obfuscated JS bundles, custom CAPTCHA mimicking Cloudflare, browser fingerprinting (RAM, CPU, screen resolution, headless detection), and WebRTC IP mismatch detection.

Bluekit previously offered AI-assisted phishing email drafting via multi-LLM support (Llama, GPT-4.1, Claude, Gemini, DeepSeek) and 40+ templates targeting Outlook, Gmail, iCloud, GitHub, and Ledger. The live monitoring system (5-second update interval) still allows operators to track victims in real time.

**Detection signals:** CSS filter manipulation on top-level HTML elements with randomized values, WebSocket connections sending binary/encrypted data on login pages, and keyboard input/mouse click delays on login forms exceeding normal latency.

---

**[NEW] Shop App Abused for Callback Phishing — Fake Receipts in Legitimate Order-Tracking Platform**

Threat actors are exploiting **Shop**, Shopify's widely used order-tracking app (50M+ Google Play downloads, 7M Apple ratings), by injecting fake purchase receipts into users' order histories impersonating Norton, McAfee, Apple, and PayPal. Each fake receipt contains a phone number that rings a scammer rather than a legitimate support desk. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/order-tracking-app-shop-abused-to-push-callback-phishing-attacks/)]

Victims are social-engineered into disclosing account credentials, payment card details, and OTPs, or tricked into installing remote access software. Gen Digital researchers note this is more effective than email-based callback phishing because Shop is a trusted platform. No evidence that Shop, Shopify, or impersonated brands were compromised.

**Mitigation:** Users seeing unexpected receipts should verify charges directly with their bank, not call listed numbers.

---

## 📋 Policy & Industry News

**[NEW] FCC Overhauls Emergency Alert System and Undersea Cable Cybersecurity Rules**

The Federal Communications Commission approved new rules overhauling cybersecurity protections for the nation's **Emergency Alert System (EAS)** and **Wireless Emergency Alerts (WEA)**, and issued the first comprehensive update to submarine cable security regulations in decades. [[CyberScoop](https://cyberscoop.com/fcc-undersea-cable-regulations-national-security/)]

The EAS/WEA rules mandate basic cyber hygiene: strong passwords, timely vendor patches, and firewalls for system operators. A new **authentication ID** system will verify alerts before submission to prevent unauthorized or duplicate alerts. The submarine cable rule creates a streamlined licensing path for providers that can self-certify to "high security standards" while imposing new licensing requirements on submarine line terminal equipment operators.

---

**[NEW] Poland Busts SIM-Swapping Gang — Four Arrested, Millions in Crypto Stolen via Telecom Partner Breach**

The Polish Cybercrime Bureau (CBZC), with FBI and HSI support, arrested four members of an organized cybercrime group that breached telecommunications partners and hijacked email accounts to execute SIM-swapping attacks, stealing millions in cryptocurrency. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/poland-busts-sim-swapping-gang-tied-to-millions-in-crypto-theft/)]

Blockchain investigator ZachXBT identified one suspect as **Wojtek Kulisz**, alias "Merry." Maximum penalty: 25 years in prison.

---

**[NEW] Russia Used Cellebrite to Break Into Human Rights Activist's Phone Despite Contract Cancellation — Citizen Lab**

Citizen Lab's investigation found that Russian authorities used **Cellebrite's UFED** phone-cracking technology to access the device of imprisoned human rights activist Andrey Pivovarov around June 2021 — after Cellebrite had canceled its contract with Russia. [[CyberScoop](https://cyberscoop.com/russia-cellebrite-activist-phone-hacking/)]

The historic architecture (offline mode, legacy hardware continued functioning after updates ceased) made it difficult to cut off problematic customers. Information from the phone may have been used to surveil fellow dissident Anastasiya Burakova.

---

**[NEW] Microsoft Quietly Extends Free Windows 10 ESU to October 2027**

Microsoft has extended the free Windows 10 Extended Security Updates (ESU) program for consumers by an additional year, with coverage now available through **October 12, 2027** — a quiet update with no formal announcement. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-quietly-extends-free-windows-10-esu-support-to-october-2027/)]

Users already enrolled will automatically remain covered. The extension applies to personal devices only.

---

## ⚡ Quick Hits

- **[UPDATE] DraftKings Credential Stuffing — Third Defendant Sentenced** — Nathan Austad ("Snoopy"), 21, of Minnesota, sentenced to 18 months in federal prison for the November 2022 credential stuffing attack compromising ~60,000 DraftKings accounts. $1.3M restitution, $463K forfeiture. Third of three defendants now sentenced. [[CyberScoop](https://cyberscoop.com/draftkings-hack-sentencing-nathan-austad-snoopy/)]

- **[NEW] Akira Ransomware Claims Two US Manufacturing Victims** — Padget Technologies (robotics/automation) and JMS Southeast (temperature measurement/control) added to Akira's leak site on June 25. Employee PII, NDAs, and customer data threatened. [[Malware.News/DeXpose](https://malware.news/t/akira-ransomware-targets-padget-technologies/108234#post_1); [Malware.News/DeXpose](https://malware.news/t/akira-ransomware-attack-targets-jms-southeast/108233#post_1)]

- **[NEW] Enterprise-Ready MCP Specification Shifts Security to Developers** — Major overhaul of the Model Context Protocol moves critical security responsibilities from the protocol to developers and platform operators. [[SecurityWeek](https://www.securityweek.com/new-enterprise-ready-mcp-specification-brings-new-security-challenges/)]

---

*56 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — `reddit_gap_check.py` unavailable (chronic failure threshold exceeded, 25+ consecutive days). Prior digests: June 21–25, 2026. Stale CVE/topic blocklist applied. Sources include SecurityWeek, Google Cloud Blog, Unit 42, BleepingComputer, CyberScoop, CISA, Forescout, Netcraft, Gen Digital, Citizen Lab, Malware.News/Sonatype, and DeXpose.*