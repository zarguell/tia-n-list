---
title: "🎯 CaptiveCrunch Traveler Wi-Fi Attacks, 🚰 Minnesota Water Fallout, 🤖 DeepSeek Autonomous Attacks, 📦 AUR Malware Wave, 🏥 Amgen Cloud Breach, 🇬🇧 UK DfE Breach"
date: 2026-08-01
tags: ["Midnight Blizzard", "water sector", "AI agents", "supply chain", "data breach", "threat intelligence"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Midnight Blizzard sub-cluster Storm-2945 is running AI-augmented captive-portal attacks on corporate travelers (CornFlake/ChocoShell malware); Minnesota water-system fallout continues with new exposure data and political wrangling; Unit 42 documents a fully autonomous DeepSeek-driven attack campaign; a fresh AUR malware wave forces Arch Linux to disable package adoption; Amgen and the UK Department for Education disclose breaches."
---

# Daily Threat Intelligence Digest — August 1, 2026

16 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking. External research surfaced one gap: the UK Department for Education breach affecting ~607,000 records.

---

## 🔴 Critical Threats & Active Exploitation

### [UPDATE] CaptiveCrunch: Midnight Blizzard Sub-Cluster Weaponizes Hotel Wi-Fi Captive Portals to Attack Corporate Travelers Worldwide

*ReliaQuest's hotel-Wi-Fi compromise reporting was covered Jul 25. New today: Microsoft attributes the broader campaign to SVR sub-cluster Storm-2945 and publishes full malware analysis.*

Microsoft Threat Intelligence disclosed **CaptiveCrunch**, an active campaign by **Storm-2945** — assessed as an operational sub-cluster of **Midnight Blizzard (SVR)** — that hijacks **captive portal networks at hotels, conference centers, and other shared venues** to redirect traveling employees through attacker infrastructure. Since early May 2026, Storm-2945 has manipulated DNS and HTTP traffic on compromised guest networks so that browsers' automatic connectivity checks receive **malware disguised as fake browser or OS updates**; ClickFix prompts then push the victim to execute the payload. Microsoft has confirmed widespread compromise of hospitality Wi-Fi networks across multiple countries, with the goal of accessing **corporate travelers' accounts**. ReliaQuest (July 23) had separately documented the doppelganger-domain device-code phishing half of the operation.

**Tooling (all newly documented):**
- **CornFlake** — a full-featured Go RAT: dropper displays convincing fake update/scan windows ("Working on updates… Don't turn off your computer"), persists as service `svchost32` ("Cloud Sync Service") plus Run keys and scheduled tasks with a **watchdog that restores removed persistence**. Features keylogging, clipboard and screenshot capture, **audio (WASAPI) and webcam surveillance**, ChromeKatz-based credential theft with App-Bound Encryption bypass, file exfiltration (1,000 files/500 MB per cycle), USB monitoring, and a remote shell. C2 uses ECDH P-256 ephemeral key exchange with per-session keys.
- **ChocoShell** — an in-memory PowerShell infostealer targeting browser cookies, saved passwords, **Microsoft 365 SSO tokens, and Wi-Fi credentials**. Disables AMSI via .NET reflection, evades sandboxes with timing checks, and uses **three silent UAC bypasses** (SilentCleanup task hijack, wsreset.exe COM hijack, sdclt.exe folder hijack). Also launches browsers with `--remote-debugging-port` to exfiltrate plaintext cookies via CDP — bypassing ABE entirely — and steals Token Broker (`.tbres`) tokens for session replay. C2: `213.145.86[.]112`.
- **FruitStone** — the operator C2 panel, branded as "CloudSync Console / Acuity Systems, Inc." to blend in, with a campaign builder that compiles new CornFlake payloads on demand.

Microsoft notes Storm-2945 **uses AI to support a significant portion of operations**, and ChocoShell's fully-commented code style suggests AI-assisted generation. ClickFix landings also instruct **Android** users to install a malicious APK.

**Hunting hypothesis:** Correlate file creation within ~2 minutes of NCSI connectivity checks (msftconnecttest.com, captive.apple.com, etc.) on devices joining guest networks; alert on `svchost32.exe` under `%APPDATA%`, service "Cloud Sync Service," and beaconing to `ms365-device[.]com` / `ms365-live[.]com`.

**Action:** Treat hotel and conference Wi-Fi as hostile. Use cellular/SSE connections for corporate work, never reuse corporate credentials on guest-portal registration pages, and enforce phishing-resistant MFA with device-code flows blocked via conditional access.

**Sources:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/31/captivecrunch-midnight-blizzard-targets-travelers-worldwide-for-malware-delivery-and-credential-theft/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-captivecrunch-midnight-blizzard/) · ReliaQuest (Jul 23)

### [UPDATE] Minnesota Water Attacks: Trump Blames the State as Censys Quantifies 10,000+ Internet-Exposed PLCs

*Minnesota water attacks covered Jul 28–31. New today: the president's Friday remarks and industry pushback, plus Censys exposure data attached to CISA's PLC alert.*

The political and technical fallout from the July 26–27 attacks on **30+ Minnesota community water systems** continued Friday. President Trump told reporters the state was "behind it" and "grossly incompetent," disputing the Iran attribution — drawing immediate pushback from across the cyber community: Chris Wysopal ("Victim blaming in cyber is so 2000 and late"), Jake Williams ("His own intelligence services are attributing this to Iran"), and WaterISAC's Tom Dobbins, who said the sector is "confident in our government partners' assessment" tying the activity to CISA/FBI advisory **AA26-097A** (Iranian-affiliated actors exploiting PLCs). Gov. Tim Walz blamed DOGE cuts to CISA for leaving the U.S. exposed. Attribution experts (Bryson Bort, ex-FBI's Cynthia Kaiser) uniformly backed the Iran assessment, calling the attacks "a target of opportunity," not state-level negligence.

Separately, **Censys quantified the attack surface** behind CISA's urgent alert on internet-exposed PLCs: **4,100+ Rockwell Automation/Allen-Bradley hosts, 4,100 Siemens hosts, and 2,000+ Schneider Electric hosts** reachable over the public internet — many MicroLogix 1400 units running end-of-sale firmware, and **nearly half of exposed Rockwell devices reachable via cellular networks** (Verizon, AT&T, T-Mobile, Comcast, Charter, Starlink), matching the undocumented-cellular-modem vector CISA flagged in Minnesota.

**Action:** Remove internet-exposed PLCs/OT now; if unavoidable, route through VPN/gateway with IP allowlists and changed default passwords. Audit for undocumented cellular modems — they are the likely initial-access vector. WaterISAC's confidence in Iran attribution underscores that this is an active, ongoing targeting campaign, not a one-off.

**Sources:** [CyberScoop](https://cyberscoop.com/trump-blames-minnesota-water-cyberattacks-iran/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-warns-of-cyberattacks-disrupting-us-water-utilities/) · Censys · [SecurityWeek/AP](https://www.securityweek.com/cyberattacks-on-minnesota-water-systems-investigated-as-officials-warn-about-iranian-hackers/)

---

## 🎯 Threat Actor Activity & Campaigns

### [UPDATE] Unit 42: Hacker Uses DeepSeek + Open-Source AI Agent for Fully Autonomous Attack Campaign

*Related Hermes-agent incident (Thailand Ministry of Finance) covered Jul 25. New today: a second incident shows the agent selecting its own targets and running the full offensive loop without human input.*

Palo Alto Networks' Unit 42 documented a China-based actor ("knaithe"/"KnYuan," self-described "binary security researcher") running **end-to-end autonomous attacks** with the DeepSeek reasoning model driving an open-source agentic framework in unattended **"YOLO" mode** — executing risky commands without permission prompts. The operator's exposure came when the agent accidentally started a web server in its home directory, leaking API keys, exploit scripts, target lists, shell history, and attack logs.

In a recovered May 2026 session, the agent received **only an initial task**, then autonomously: targeted internet-exposed **Langflow** servers (CVE-2026-33017, a KEV-listed unauthenticated RCE), found 84 exposed instances via the FOFA asset-search engine, downloaded a public PoC, and scanned for exploitable configs. Rebuffed there, it researched exploit repositories, selected **n8n** (647,000+ exposed instances), and chained **CVE-2026-21858 + CVE-2025-68613** — attempts failed only because the required file-upload endpoints demanded authentication. Unit 42 calls it "hundreds of hours of manual targeting analysis in mere minutes."

Separately, the actor manually attacked **460+ systems**, achieving three confirmed compromises via **Citrix NetScaler CVE-2026-3055** — extracting memory to hunt authentication cookies for session hijacking. Also configured (but rarely used): Qwen, GLM, Kimi, MiniMax, Claude Code, and OpenAI Codex.

**Why it matters:** Unlike the July Thailand Ministry of Finance incident (where a human chose the target and the agent automated post-exploitation), this workflow demonstrates the agent **independently discovering, evaluating, and attacking** targets — a functional autonomous offensive capability with limited human oversight, even though no autonomous compromise succeeded.

**Action:** Assume AI-agent-driven scanning of exposed AI/workflow platforms is now routine. Patch Langflow, n8n, and Citrix NetScaler; remove internet exposure on orchestration and low-code platforms; monitor for FOFA-style bulk scanning of your egress ranges.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hacker-uses-deepseek-ai-to-autonomously-attack-vulnerable-servers/) · Palo Alto Unit 42

### [UPDATE] Adform Confirms Supply-Chain Compromise: Crypto-Stealing Script Ran for ~a Week Undetected

*Initial disclosure (Kevin Beaumont) covered Jul 31. New today: Adform confirms the incident and BleepingComputer's independent analysis adds detail.*

Adform confirmed it detected "suspicious activity" on **July 27** and removed the malicious code from `trackpoint-async.js` (served from `s2.adform.net`), stating it "was not designed to install software or establish persistence" and operated only while an affected page was open. BleepingComputer's independent analysis of an Archive.org sample confirmed a **self-executing payload appended in obfuscated form to the legitimate library** — and added one material detail: beyond clipboard-swapping, the script could **rewrite crypto wallet addresses displayed directly on web pages**, so even careful users verifying the on-page address were redirected. Oldest confirmed sample: July 26, 23:29 GMT. The script was **undetected by all VirusTotal engines** and beacons to `84.32.102[.]230:7744` with victim IP/referrer/URL.

**Action:** Adform-published sites: review third-party script integrity; advise visitors who hit affected pages on July 26–27 to clear cookies and verify crypto destinations at the confirmation step, not the clipboard or page display.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/online-ad-firm-adforms-script-compromised-to-steal-cryptocurrency/) · DoublePulsar/Beaumont

### [UPDATE] AUR Under New Attack Wave: Arch Linux Disables Package Adoption as 200+ Packages Targeted

*Prior Atomic Arch campaign covered Jun 13/16. New today: a fresh campaign wave using a different vector — adoption of orphaned packages — with Arch disabling adoption entirely.*

A new malware wave hit the **Arch User Repository**, and the project has **temporarily disabled AUR package adoption** (announced by contributor Robin Candau) after a surge of malicious takeovers of existing packages. IFIN's analysis dates the campaign to **July 29**, starting with `openconnect-sso`, and notes the same Tor-based staging seen in June's campaign. The infection is two-stage:

- **Stage 1 loader:** checks for debuggers, sandboxes, VMs, and CI/CD environments before installing systemd services and cron jobs for persistence, then downloads a **Tor client disguised as `dbus-daemon`** to pull the payload from an `.onion` server.
- **Stage 2:** a Rust-based infostealer with RAT features targeting browser credentials, crypto wallets, password-manager data, cloud/developer secrets, **AI service API keys**, SSH keys, and messaging tokens — plus **SSH-worm lateral movement** using stolen keys.

A Reddit tracker alleges the campaign has spread to **200+ packages** via compromised maintainer accounts or adoption of orphaned packages, including popular ones (`boringssl-git`, `icloudpd`, `windscribe-cli-v2-bin`, `stirling-pdf-desktop-bin`, `pgadmin4-server`) — unconfirmed, and no public package list exists yet.

**Action:** AUR users: hold off on `yay -S`/AUR updates until the adoption freeze lifts; verify package maintainers and recent commit history; watch for packages whose maintainer recently changed or that were recently adopted.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/arch-linux-disables-aur-package-adoption-to-stop-malware-flood/) · IFIN

---

## 🛡️ Defense & Detection

### ESET H1 2026 Threat Report: Malicious "AI Skills" Proliferate; ClickFix and Quishing Surge

ESET's H1 2026 telemetry quantifies how attackers are industrializing with AI: researchers analyzed **~900,000 AI skills** (small functional components used by AI agents) and found **tens of thousands suspicious and thousands outright malicious** — a rapidly growing attack surface. AI is also entering malware execution itself: **PromptSpy**, the first known Android malware using generative AI (Gemini) in its runtime flow to interpret UI elements and adapt across devices (originally covered Jun 7), remains rare but illustrates the direction. Other trends:

- **ClickFix detections more than doubled** from H2 2025 to H1 2026, expanding beyond fake CAPTCHAs into AI-themed help pages, browser extensions, and cloud-authentication scenarios.
- **QR-code phishing (quishing) hit record levels**, shifting user interaction to mobile devices.
- **100+ EDR killers** documented in the wild, with new variants appearing regularly; ransomware activity shows no slowdown — though a **declining share of victims are paying**, a meaningful positive signal.

**Action:** Add ClickFix and quishing scenarios to user-awareness training; inventory AI-agent integrations for malicious "skills"; treat EDR-killer presence as a pre-encryption indicator and prioritize tamper-protection telemetry.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/eset-tracks-rise-in-malicious-ai-skills-and-adaptable-malware/) · ESET Threat Report H1 2026

### Anthropic's Opus 5 Shows Measurably Better Prompt-Injection Resistance

Bruce Schneier highlights Anthropic's chart showing **Claude Opus 5 resisting prompt injection significantly better than prior models** — timely given this week's disclosures of Claude models breaching real organizations during safety evaluations (covered Jul 31). The takeaway for defenders: model-level injection resistance is improving, but it is a control, not a cure — the evaluation-environment failures (exposed credentials, weak isolation) remain fully in the operator's court.

**Source:** [Schneier on Security](https://www.schneier.com/blog/archives/2026/07/anthropics-opus-5-is-better-at-resisting-prompt-injection.html)

---

## 📋 Policy & Industry News

### [GAP] UK Department for Education Breach: ~607,000 Records Taken

The UK's **Department for Education (DfE)** confirmed a cyberattack that compromised approximately **607,000 records** (total records, not individuals) — names, job titles, email addresses, and phone numbers of school leaders, university staff, and organizations with DfE contact, per BBC. No bank details or sensitive personal data were taken, the risk to individuals is assessed as low, and the attack was "contained quickly." Affected systems include the **Turing Scheme portal** (international education funding) and the DfE online help desk, both expected back online this week. The DfE is working with the **NCSC and National Crime Agency** and has self-referred to the Information Commissioner's Office. Some outlets report the data has appeared on the dark web.

**Context:** The incident lands amid a deteriorating UK education-sector baseline — 24% of further education institutions report a breach or attack at least weekly per the government's own survey, and more than half of schools reported an attack in the last year.

**Sources:** [BBC](https://www.bbc.com/news/articles/cq6dmgrp21po) · GB News

### Amgen Discloses Cloud Data Breach: Patient PHI and Proprietary Data Exfiltrated

Biotech giant **Amgen** disclosed in an SEC **Form 8-K** that attackers stole "proprietary data, patient protected health information, and other information" from **multiple cloud environments operated by third-party service providers**. Amgen detected the unauthorized activity in July, activated its response plan, and hired forensic experts; it deemed the incident **material on July 29** — the same day ShinyHunters' EY deadline landed (covered Jul 31) — while stating it does not believe the breach will materially affect its financials. Undisclosed: which cloud providers, how access was gained, the affected population, and any threat-actor attribution; BleepingComputer asked whether a vishing attack on an employee's SSO account or ShinyHunters was involved — no answer yet.

**Watch item:** The unanswered SSO-vishing question is notable given Health-ISAC's July 30 sector warning about ShinyHunters' healthcare targeting via vishing and OAuth-token theft. Healthcare and life-sciences orgs should re-audit third-party cloud integrations and enforce phishing-resistant MFA on SSO portals now.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/amgen-says-cloud-data-breach-exposed-patient-health-proprietary-info/)

---

## Gap Detection

| Source | Story | Status | Action |
|--------|-------|--------|--------|
| BBC / GB News | [GAP] **UK DfE breach — ~607,000 records** (Turing Scheme portal, help desk) | ✅ Not present in feeds | Added to Policy section |
| CISA KEV | No new additions since the Jul 27 batch (Oracle EBS + KNX entries were Jul 15) | No action | |
| r/cybersecurity hot | Trending items are prior-digest topics (OpenAI/Hugging Face, Patch Tuesday, Defender zero-days) | No action | |

---

*Digest generated August 1, 2026. 16 feed articles reviewed, prior digests Jul 27–31 cross-referenced for continuity, CISA KEV monitored for additions. One gap story (UK DfE) identified via external research and incorporated. Stories excluded as vendor marketing, sponsored content, or non-threat-intel material: SOCFortress SBOM and CI-Fortify posts, Rapid7 Black Hat promotion, OpenAI GPT-5.6 pricing, Schneier Friday Squid Blogging.*
