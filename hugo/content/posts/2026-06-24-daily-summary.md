---
title: "🔴 Cisco CUCM exploited, 🎯 Klue/LastPass widens, 🤖 Mythos cracks classified systems, 🏭 Tata breached, 🎥 FFmpeg PixelSmash RCE"
date: 2026-06-24
tags: ["Cisco CVE-2026-20230", "Klue supply chain", "LastPass", "Anthropic Mythos", "Tata Electronics", "FortiBleed", "Lazarus", "FFmpeg PixelSmash", "Samsung KNOX", "macOS Gaslight", "Edgecution", "OpenClaw", "Huione Group", "WorldLeaks", "AMOS", "Miasma", "Scattered Spider", "CISA KEV"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Cisco Unified CM CVE-2026-20230 exploited in attacks (SSRF→root, recon payloads); Klue supply chain widens — LastPass and BeyondTrust confirm Salesforce data theft; Anthropic's Mythos model finds vulnerabilities in classified US government systems under Project Glasswing; Tata Electronics confirms cyberattack as WorldLeaks leaks Apple iPhone manufacturing data; FFmpeg PixelSmash (CVE-2026-8461, CVSS 8.8) enables RCE via crafted media files across all platforms; Samsung KNOX eight-year-old UAF (CVE-2026-20971) affects Galaxy S9–S25; Arctic Wolf reverse-engineers FortiBleed credential pipeline; Lazarus deploys memory-only malware against financial sector; macOS.Gaslight Rust backdoor weaponizes prompt injection against analysts; Zscaler details Edgecution browser-extension malware; Unit 42 finds persistent malicious skills on OpenClaw marketplace; DOJ seizes Huione Group infrastructure; Five Eyes warns of AI-powered cyberattacks."
---

# Daily Threat Intelligence Digest — June 24, 2026

*56 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — `reddit_gap_check.py` unavailable (chronic failure threshold exceeded, 25+ consecutive days per prior digests). External gap detection via web search found no critical gaps beyond feed coverage. Prior digests: June 19–23, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Cisco Unified CM CVE-2026-20230 Actively Exploited — SSRF Vulnerability Grants Root Access on Voice Servers**

Threat actors are actively exploiting CVE-2026-20230, a high-severity SSRF vulnerability (CVSS 8.6) in Cisco Unified Communications Manager (Unified CM) and Unified CM Session Management Edition, with exploitation observed over the weekend. The flaw, patched by Cisco on June 3, allows unauthenticated remote attackers to abuse the WebDialer component's handling of user-supplied URLs to write arbitrary files to the OS via `file://` URIs — ultimately achieving root privileges. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisco-unified-cm-sme-flaw-cve-2026-20230-now-exploited-in-attacks/); [SecurityWeek](https://www.securityweek.com/hackers-exploiting-cisco-unified-cm-vulnerability/)]

Threat intelligence firm Defused confirmed attacks originating from a single IP address using properly constructed `file://` payloads. The observed PoC appears designed for reconnaissance — writing a test file (`/tmp/cve-2026-20230-test.txt`) to vulnerable devices — but now that SSD Secure has published a full technical write-up and PoC exploit, broader weaponized exploitation is expected. CISA has **not yet** added this CVE to KEV.

**Hunting hypothesis:** Monitor for HTTP requests to Unified CM WebDialer endpoints containing `file://` URI schemes from unexpected IPs. Check for unexpected files written to `/tmp/` on CUCM appliances.

**Recommended action:** Patch immediately if running affected Unified CM versions. This is internet-facing voice infrastructure — treat as crown-jewel priority.

---

**[UPDATE] Klue Supply Chain Breach Widens — LastPass Confirms Salesforce Data Theft, BeyondTrust Discloses Impact**

The Icarus extortion group's June 12 compromise of Klue's OAuth integrations continues to ripple through the security vendor ecosystem. **LastPass** confirmed attackers accessed customer names, phone numbers, email addresses, physical addresses, and support case data from its Salesforce environment using stolen OAuth tokens — but emphasized that customer vaults, products, and infrastructure remain secure. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/lastpass-confirms-data-breach-in-klue-supply-chain-attack/)]

BeyondTrust also disclosed impact, joining a victim list that now includes HackerOne, Huntress, Jamf, OneTrust, Recorded Future, Snyk, Tanium, Insurity, and Sprout Social. LastPass warned of increased phishing risk using sender domains `baccarat.com[.]au`, `robinskitchen.com[.]au`, and `house[.]com[.]au`. The Icarus group's data leak deadline for negotiations passed June 22 with no published dump reported as of this writing, but affected organizations continue rotating OAuth tokens and auditing Salesforce API logs.

**Context:** *Previously tracked June 19–23 (initial disclosure, Klue CEO statement, Huntress confirmed, Salesforce platform-wide disable, Icarus extortion). New today: LastPass and BeyondTrust confirm impact, specific phishing sender domains identified.*

---

**[NEW] Anthropic's Mythos Model Found Vulnerabilities in Classified US Government Systems During Project Glasswing Test**

Anthropic's Mythos AI model identified vulnerabilities in classified US government computer systems within hours during a testing exercise conducted with US intelligence agencies, a senior US official told the Associated Press. The testing was conducted under **Project Glasswing**, an Anthropic initiative aimed at securing critical software from the "severe" fallout the Mythos model could pose to public safety and national security. [[SecurityWeek/AP](https://www.securityweek.com/anthropics-mythos-model-found-vulnerabilities-in-classified-us-government-systems-official-says/)]

The disclosure confirms Sen. Mark Warner's June 11 statement that "this tool broke into almost all of our classified systems, not in weeks but in hours," attributed to NSA/Cyber Command chief Gen. Joshua Rudd. The development comes amid growing tensions between Anthropic and the Trump administration: the White House recently restricted foreign national access to Mythos 5 and Fable 5, prompting Anthropic to disable the models for all customers. More than 100 cybersecurity executives — from Adobe, Nvidia, and others — urged the administration to ease restrictions, arguing Mythos is "quite good" at finding flaws but "not uniquely good," and that removing the best cyber defense capabilities helps adversaries more than it hurts.

---

**[NEW] Tata Electronics Cyberattack — WorldLeaks Leaks Apple iPhone Manufacturing Data**

Tata Electronics, a key Apple iPhone manufacturer and one of India's largest tech manufacturing companies, confirmed a cyberattack that impacted parts of its IT infrastructure "a few weeks ago." The WorldLeaks extortion group — a rebrand of the former Hunters International ransomware operation — leaked data allegedly stolen from Tata, including directories and documents containing Apple product manufacturing data: internal component schematics, PCB designs, material specifications, and SDK files. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/tata-electronics-confirms-cyberattack-as-hackers-leak-data/)]

WorldLeaks operates purely as a data extortion group (no encryptor), previously claiming victims including Dell (July 2025) and Nike (January 2026). Tata says operations were unaffected. Apple has not commented on whether proprietary data was exposed. For a company producing iPhone components, the leaked schematics and specs represent significant intellectual property theft — though the actual threat to supply chain integrity depends on whether manufacturing process data was also exfiltrated.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Lazarus Targets Financial Sector with Three-Stage Memory-Only Malware Toolset**

A newly identified Lazarus subgroup has been targeting financial institutions and cryptocurrency organizations with a sophisticated malware framework operating almost entirely in memory, according to researchers at Fox-IT (Cognyte). The three-component toolset — **DPAPILoader**, **RemotePELoader**, and **RemotePE** — uses Windows Data Protection API (DPAPI) for environmental keying that binds malware execution to a specific victim environment, making traditional hash-based detection ineffective. [[Cognyte/Malware.News](https://www.cognyte.com/blog/lazarus-targets-the-financial-sector-with-memory-only-malware-toolset/)]

The infection chain: DPAPILoader decrypts and launches the next stage using DPAPI → RemotePELoader retrieves the final payload from attacker-controlled infrastructure entirely in memory → RemotePE RAT provides command execution, file manipulation, process management, and data access. Environmental keying means each deployment generates a unique encrypted payload — a deliberate shift toward stealth-first tradecraft that reduces forensic visibility and enables long-term access.

**Recommended action:** Monitor for suspicious DPAPI function calls (`CryptProtectData`/`CryptUnprotectData`) from unusual processes. Deploy behavioral detection for memory-only execution patterns.

---

**[UPDATE] FortiBleed — Arctic Wolf Reverse-Engineers 'CyberStrike Harvester' Behind Global FortiGate Credential Factory**

Arctic Wolf published a technical reverse-engineering analysis of the credential pipeline driving the FortiBleed campaign, revealing how the operator — tracked as an initial access broker on Russian-language forums — built a systematic credential factory using credential stuffing, password spraying, configuration harvesting, offline GPU cracking, and post-authentication traffic capture. [[Arctic Wolf via Malware.News](https://malware.news/t/inside-fortibleed-reverse-engineering-the-cyberstrike-harvester-behind-a-global-fortigate-credential-factory/108166#post_1)]

The campaign does not depend on a single malware payload but on an integrated pipeline: harvested configurations inform targeted password lists, 36-GPU rented clusters crack legacy salted SHA-256 hashes at 720 billion/second, and the FortigateSniffer tool (covered June 23) captures auth traffic from compromised devices. The data feeds ransomware affiliates through an IAB marketplace. The campaign has now been tracked for over a week, with CISA, Unit 42, Recorded Future, Hudson Rock, and now Arctic Wolf all publishing independent analyses — making this one of the most comprehensively documented credential-theft operations of 2026.

**Context:** *Previously tracked June 18–23 (initial disclosure, CISA warning, Unit 42 analysis, IAB attribution, GPU cluster mechanics, FortigateSniffer). New today: Arctic Wolf independent reverse-engineering of the full credential pipeline.*

---

**[NEW] macOS.Gaslight — Rust Backdoor Weaponizes Prompt Injection Against the Analyst, Not the Sandbox**

SentinelLABS disclosed **macOS.Gaslight**, a Rust-based macOS implant that embeds a 3.5 KB cascade of 38 fabricated "system" messages designed to steer LLM-assisted triage pipelines into aborting or refusing analysis. The implant communicates over a Telegram Bot API polling loop with AES-GCM payloads over certificate-pinned TLS, and self-redacts its bot token at runtime to prevent credential recovery from crash logs. [[SentinelOne](https://www.sentinelone.com/labs/macos-gaslight-rust-backdoor-turns-prompt-injection-on-the-analyst-not-the-sandbox/)]

Key capabilities: interactive shell via Telegram C2, a Python-based stealer (fetches a standalone CPython 3.10.18 at runtime from astral-sh/python-build-standalone), credential harvesting (login.keychain-db, browser data from Chrome/Brave/Firefox/Safari), and persistence via a LaunchAgent masquerading as `com.apple.system.services.activity`. SentinelLABS assesses with high confidence that this implant belongs to a cluster of DPRK-aligned macOS activity (XProtect detects under rule `MACOS_BONZAI_COBUCH`).

The analyst-targeting injection is notable: 38 fake system messages about token expiry, OOM kills, disk exhaustion, and injection warnings — designed to poison LLM-assisted reverse engineering pipelines. Anyone building such tooling should treat sample contents as adversarial input.

---

**[NEW] Payouts King IAB Deploys 'Edgecution' Malware via Malicious Microsoft Edge Browser Extension**

Zscaler ThreatLabz documented an innovative malware delivery mechanism used by an initial access broker affiliated with Payouts King ransomware: a malicious Microsoft Edge browser extension called **Edgecution** that abuses the Chrome native messaging protocol to escape the browser sandbox. [[Zscaler](https://www.zscaler.com/threatlabz/edgecution-malicious-edge-extension-backdoor)]

The attack chain begins with social engineering via Microsoft Teams — the attacker impersonates IT staff and directs victims to a fake "Outlook Updates Management Console" website. Buttons on the page deliver either an AutoHotKey script, Windows batch script, or PowerShell script that deploys the Edgecution payload. The extension runs in a **headless Edge browser** (invisible to the user), beacons to C2 via websockets over `cloudfront.net` subdomains, and uses the native messaging host to invoke a Python backdoor that executes arbitrary code, accesses the filesystem, and collects system information. A scheduled task maintains persistence. The Python backdoor includes its own embedded Python 3.13.3 distribution.

**IOCs:** C2 servers at `wss://d3nh8sl98s2554.cloudfront[.]net/ws`, `wss://d2g6dl71gua1qa.cloudfront[.]net/ws`, `wss://d1jp293q9tvi92.cloudfront[.]net/ws`.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] FFmpeg PixelSmash (CVE-2026-8461, CVSS 8.8) — Heap Out-of-Bounds Write Enables RCE via Crafted Media Files**

JFrog disclosed **PixelSmash**, a heap out-of-bounds write vulnerability in FFmpeg's libavcodec library within the MagicYUV decoder. The flaw exists in slice handling — "caused by an inconsistency between how the frame allocator and the decoder compute chroma plane heights." A 50 KB AVI, MKV, or MOV file can deliver the exploit payload. [[SecurityWeek](https://www.securityweek.com/ffmpeg-pixelsmash-flaw-allows-rce-on-video-players-media-servers-nas-appliances/)]

The attack surface is immense: any application using FFmpeg for media processing — desktop video players, file manager thumbnail generators (GNOME, KDE, XFCE via ffmpegthumbnailer), self-hosted media servers (Jellyfin, Emby, Plex), cloud transcoding pipelines, NAS appliances, and smart TVs. JFrog confirmed successful exploitation against Kodi, mpv, Jellyfin, Nextcloud, Immich, PhotoPrism, and OBS Studio. On Nextcloud, the flaw can be triggered as a near-zero-click attack via the Movie preview provider — the attacker only needs the file visible in a folder listing.

JFrog achieved code execution by targeting FFmpeg's `AVBuffer` struct — placing a NUL-terminated shell command at a specific out-of-bounds offset. FFmpeg version 8.1.2 contains the fix.

**Recommended action:** Update FFmpeg to 8.1.2 on all platforms. For media server operators: disable automatic thumbnail generation until patching is complete.

---

**[NEW] Samsung KNOX Eight-Year-Old UAF (CVE-2026-20971, CVSS 7.8) — Affects Galaxy S9 Through S25**

LucidBit Labs disclosed a use-after-free vulnerability in Samsung's KNOX security framework that went undetected for eight years, affecting nearly all Samsung Galaxy devices from the S9 through S25 (Android 13–16). The flaw exists in the interaction between PROCA (process authenticator) and FIVE (kernel integrity subsystem) — a race condition where a thread can be suspended between reading a pointer and using it, enabling exploitation via a non-ELF file load trick. [[SecurityWeek](https://www.securityweek.com/eight-year-old-samsung-knox-flaw-exposed-millions-of-galaxy-devices-to-kernel-attacks/)]

Samsung fixed the issue in its January 2026 SMR update. While local-only in theory, attackers have numerous ways to establish remote footholds on always-on mobile devices — making this a realistic enterprise risk for organizations with unpatched Galaxy devices in the field.

---

**[NEW] OpenClaw Skill Marketplace — Unit 42 Finds Persistent Malicious Skills Bypassing VirusTotal and ClawScan**

Unit 42 published a follow-up analysis of the OpenClaw AI agent skill marketplace, identifying **five unblocked malicious skills** — including persistent AMOS infostealers, file-padding evasion (22 MB inflated README to exceed scanner thresholds), **runtime agentic affiliate injection** (skill redirected financial recommendations through operator-controlled affiliate links from known-malicious domain `laosji[.]net`), and an **agentic front-running scheme** that weaponized a botnet of AI agents to execute a pump-and-dump on Solana meme tokens. [[Unit 42](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)]

All five skills passed ClawHub's VirusTotal and ClawScan screening at the time of analysis. The marketplace has since integrated NVIDIA's analysis tooling, but the findings confirm that AI agent supply chains present a fundamentally novel threat model: malicious skills use semantic instruction hijacking rather than exploits, bypassing traditional malware detection entirely.

---

## 🛡️ Defense & Detection

**[NEW] macOS ClickFix Campaign Silently Mounts DMGs to Deploy Atomic macOS Stealer**

Palo Alto Networks Unit 42 discovered a new macOS ClickFix campaign that uses Terminal commands to silently download, mount, and launch AMOS infostealer from malicious DMG files — without displaying them in Finder. The attack begins with a fake CAPTCHA page instructing users to paste a command into Terminal: the command uses `curl -fsSL` to download a DMG from `svs-verificationdate[.]beer`, `hdiutil attach -nobrowse` to mount it invisibly, and `open` to launch the embedded `.app` bundle. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-macos-clickfix-attack-silently-mounts-dmgs-to-push-infostealer/)]

AMOS targets 8 Chromium-based browsers and 5 Firefox-derived browsers for credential theft, plus Exodus, Electrum, Atomic Wallet, Wasabi Wallet, and 10+ other cryptocurrency wallets. Notably, it replaces legitimate Ledger Live and Trezor Suite installations with malicious versions for crypto theft. C2 infrastructure: `svs-verificationdate[.]beer` and `196.251.107[.]171`.

**Rule of thumb:** No legitimate CAPTCHA asks you to open Terminal. Treat any such instruction as a malware delivery attempt.

---

**[NEW] Miasma Campaign Deep-Dive — Tenable Analyzes the Developer Credential Economy**

Tenable's Research Special Operations published a comprehensive analysis of the **Miasma** supply chain campaign, situating it within the broader "Developer Credential Economy" — an industrial underground market where stolen developer credentials (GitHub tokens, npm tokens, CI/CD secrets) are brokered and weaponized with measured dwell times. [[Tenable](https://www.tenable.com/blog/what-the-miasma-campaign-reveals-about-the-new-supply-chain-threat-model-and-the-underground)]

Key takeaways: Miasma is a self-propagating npm worm derived from Mini Shai-Hulud (open-sourced May 12). It compromised 89+ packages across three waves (June 1–5) targeting Red Hat, Vapi.ai, and Azure repositories — producing malicious packages with valid SLSA Build Level 3 provenance attestations. The root cause: a stolen developer credential sat in infostealer logs for **seven weeks** before weaponization. The third wave (June 5) introduced AI coding assistant persistence files targeting Claude Code, Cursor, Gemini CLI, and VS Code — the first observed campaign to systematically target the AI-assisted development workflow as a persistence surface.

---

## 📋 Policy & Industry News

**[NEW] DOJ Seizes Huione Group Cloud Infrastructure — Treasury Sanctions Prince Group Network**

The Justice Department seized a cloud computing account hosting backend infrastructure for **Huione Guarantee**, one of the world's most prolific criminal marketplaces, used for cyber scams, fraud, money laundering, and human trafficking. The Treasury Department simultaneously added **H-Pay Service** to existing Huione sanctions and designated nine individuals and 26 entities linked to the **Prince Group** — a Cambodian conglomerate previously tied to $15 billion in bitcoin seized by DOJ last October. [[CyberScoop](https://cyberscoop.com/doj-huione-group-cybercrime-seizure/)]

The seized infrastructure processed billions in fraud proceeds from Southeast Asian scam centers. Treasury's actions build on October 2025 sanctions that severed Huione Group from the US financial system.

---

## ⚡ Quick Hits

- **Scattered Spider hackers plead guilty** — Two members of the cybercrime group (Owen Flowers, 18, and Thalha Jubair, 20) changed their pleas to guilty on the first day of trial at Woolwich Crown Court, admitting to the September 2024 hack of Transport for London that cost £39 million. [[Krebs on Security](https://krebsonsecurity.com/2026/06/scattered-spider-hackers-plead-guilty-on-day-1-of-trial/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/scattered-spider-members-plead-guilty-to-hacking-transport-for-london/)]
- **Dify AI Platform data exposure flaws** — Data exposure vulnerabilities reported in the Dify AI platform, which powers over 1 million applications. [[SecurityWeek](https://www.securityweek.com/data-exposure-flaws-threaten-dify-ai-platform-powering-over-1-million-apps/)]
- **Five Eyes warns of AI-powered cyberattacks** — The intelligence alliance of the US, UK, Canada, Australia, and New Zealand warned that frontier AI models will supercharge offensive hacking capabilities, calling the timeline "months, not years." [[DataBreaches.net](https://databreaches.net/2026/06/23/the-timeline-is-months-not-years-five-eyes-warns-of-ai-powered-cyberattacks/)]
- **EvilTokens phishing kit** — ANY.RUN analyzed the EvilTokens kit, which hides Microsoft 365 device-code phishing behind AES-GCM-encrypted browser code, creating a blind spot for static URL analysis. Concentrated targeting of US and European organizations. [[ANY.RUN](https://any.run/cybersecurity-blog/eviltokens-ghost-code-phishing-analysis/)]
- **Dragos unveils AI for OT security** — Dragos announced new AI capabilities for industrial/OT security monitoring. [[SecurityWeek](https://www.securityweek.com/dragos-unveils-ai-for-ot-security/)]
