---
title: "🔴 Clop Windchill RCE, 🎯 Laundry Bear Zimbra Espionage, ⚠️ AgentForger ChatGPT Flaw, 🛡️ Nuclear Malware Benchmark, 📋 FedRAMP 20× Transition"
date: 2026-07-24
tags: ["threat-intelligence","daily-digest","clop","ransomware","laundry-bear","zimbra","openai","chatgpt","agentforger","sentinelone","fast16","fedramp","microsoft-passkey","dolphin-x","sectopat","uac-0099","notepad++","origin-energy","rubio-visa-restrictions"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Clop ransomware exploits CVE-2026-12569 targeting PTC Windchill/FlexPLM; international advisory on Laundry Bear Zimbra zero-click espionage; AgentForger ChatGPT Workspace Agent CSRF disclosed; SentinelOne Fast16 nuclear-sabotage malware benchmark shows only GPT-5.6 Sol completes all stages; FedRAMP 20× transition shifts to continuous machine-readable evidence."
---

# Daily Threat Intelligence Digest — July 24, 2026

31 articles ingested and analyzed from curated cyber intelligence feeds. Prior-digest continuity tracked across Check Point, RefluXFS, SharePoint, OpenAI/Hugging Face, and Chick-fil-A stories — all already covered in previous days. Gap detection via web search surfaced one new policy story (Microsoft passkey mandate). Three sets of multi-source stories merged (Zimbra/Laundry Bear ×3, Origin breach ×2).

---

## 🔴 Critical Threats & Active Exploitation

### Clop Ransomware Exploits CVE-2026-12569 (CVSS 9.3) to Target Windchill, FlexPLM

The **Clop/Cl0p** ransomware gang is actively exploiting **CVE-2026-12569**, a critical improper input validation vulnerability (CVSS 9.3) in **PTC Windchill** and **FlexPLM** enterprise systems, in a data-theft extortion campaign documented by ReliaQuest and Ransom-ISAC.

Key details:
- Exploitation enables **unauthenticated remote code execution**
- Clop operators deploy **JSP webshells** to exfiltrate sensitive product data
- Extortion emails sent from `support@cryptohox.com` (multiple variants)
- Targets **Internet-exposed Windchill and FlexPLM instances**
- Attribution to Cl0p based on tradecraft overlap with prior enterprise-targeting campaigns
- CVE-2026-12569 already on **CISA KEV** since June 25

**Action:** Immediately identify and patch all Internet-exposed PTC Windchill and FlexPLM instances. Hunt for JSP webshells under `/Windchill/login/`. Block email domains associated with extortion outreach.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/clop-ransomware-targets-windchill-flexplm-in-data-theft-attacks/) · [Ransom-ISAC](https://ransom-isac.org/blog/clop-windchill-flexplm-exploitation/)

---

### [UPDATE] Laundry Bear (Void Blizzard) Zimbra Zero-Click Espionage — Joint International Advisory

*New today: Joint advisory from CISA/FBI/13+ countries; Unit 42 publishes CL-STA-1114 campaign details; three separate reporting sources merged below.*

The Russian state-sponsored group tracked as **Laundry Bear / Void Blizzard / CL-STA-1114** has been conducting a persistent cyberespionage campaign since **July 2025** exploiting **CVE-2025-66376**, a zero-click vulnerability in **Zimbra Collaboration Suite** that was patched November 2025 — five months after attacks began.

The exploit requires only a **view** (no click) and steals:
- Previous **90 days of email archives**
- **Account passwords** and **2FA tokens**
- **Search history** and **organization email directories**
- **Newly created passwords**

Targeted sectors include **government, defense, education, energy, law enforcement, media, finance, transportation, and technology** across **NATO member states, Ukraine, CIS countries, and Africa**. The advisory notes a pattern of Ukrainian targeting first as a "testbench" before broader global deployment.

**Action:** Patch Zimbra Collaboration Suite to the latest version. Review Unit 42 and CISA advisory IOCs. Hunt for exploitation dating back to July 2025 — treat any unpatched ZCS instance as potentially compromised.

**Sources:** [CyberScoop](https://cyberscoop.com/russian-laundry-bear-zimbra-exploit/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/russian-hackers-exploit-zimbra-zero-click-flaw-for-email-theft/) · [Unit 42](https://unit42.paloaltonetworks.com/russian-webmail-espionage/) · [CISA Advisory](https://media.defense.gov/2026/Jul/22/2003965244/-1/-1/1/CSA_RUSSIA_PHISHING_TARGET_ZIMBRA.PDF)

---

## 🎯 Threat Actor Activity & Campaigns

### FakeAgent Campaign: Fake Claude App via Bing Ads Delivers SectopRAT

A **malvertising campaign** on Bing search is pushing a fake Claude desktop app installer hosted on a **legitimate Claude.ai domain** to deliver the **SectopRAT** remote access trojan. Dubbed **FakeAgent**, the campaign compromised **at least 29 organizations** between July 21–22.

Attack flow:
1. Malicious **Claude Artifact** hosted on claude.ai (downloaded **7,100 times** before Anthropic removed it)
2. Directs victims to fake installer page serving `ClaudeDesktop.exe`
3. The executable is a legitimate JetBrains Chromium component that **DLL-side-loads** `libcef.dll` (SectopRAT)
4. Persistence via `DockerDesktop.exe` installing a scheduled task
5. Anti-analysis: **VMProtect packing**, shellcode injection, string obfuscation

This follows earlier patterns of Claude Artifact abuse used to push macOS malware via ClickFix lures earlier this year.

**Action:** Block untrusted Claude Artifact URLs. Hunt for IOCs provided by Huntress. Restrict DLL sideloading paths in enterprise environments.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-claude-app-promoted-by-bing-ads-pushes-sectoprat-malware/)

---

### Dolphin X RAT — AI-Powered Victim Profiling and Ranking

A new **Dolphin X** remote access trojan is being advertised on cybercrime forums by a vendor using the alias "Kontraktnik." Analyzed by Varonis Threat Labs, it boasts **329 features** across ten categories, targeting **300+ applications** for credential harvesting.

Standout feature: an **"AI Profiler"** that scores infected users based on application usage and assigns risk levels, helping attackers identify which victims to prioritize for follow-on exploitation. The operator panel processes application usage, risk scores, and generates daily summaries.

**Hunting hypothesis:** Monitor for beaconing traffic associated with Dolphin X C2. Watch for credential theft targeting 300+ application categories (browsers, crypto wallets, email clients, VPNs, enterprise apps).

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-dolphin-x-malware-uses-ai-to-rank-high-value-targets/) · [Varonis](https://www.varonis.com/blog/dolphin-x-stealer)

---

### UAC-0099 Abuses Notepad++ Plugins for Sandworm Initial Access

Ukraine's **CERT-UA** has uncovered attacks by threat cluster **UAC-0099** (previously linked to providing initial access for **Sandworm/APT44**) distributing a ZIP archive containing the legitimate Notepad++ application with a malicious **LunchPoke** DLL disguised as a plugin.

Attack chain:
1. VBS script disguised as a PDF document
2. Retrieves `Evernote.zip` containing Notepad++ 8.8.3, malicious `NppExport.dll`, password-protected `updater.rar`, and legitimate WinRAR
3. Launches Notepad++ which loads the malicious DLL via standard plugin mechanism
4. DLL establishes persistence and deploys further payloads

No vulnerability or supply-chain compromise is exploited — the attack relies on social engineering to deliver the trojanized archive.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-abuse-notepad-plus-plus-plugins-to-stealthily-install-malware/)

---

## ⚠️ Vulnerabilities & Patches

### AgentForger — ChatGPT Workspace Agent CSRF Lets Attackers Forge an AI Insider

Zenity Labs disclosed **AgentForger**, a critical vulnerability in OpenAI's **ChatGPT Workspace Agents** that allows an attacker to create an invisible, fully autonomous agent inside an organization with a single successful phish.

The attack:
1. Victim (already logged into ChatGPT with authorized connectors like Gmail/Outlook) clicks a weaponized URL
2. URL contains parameters naming the **Chief of Staff** agent template + a malicious `initial_assistant_prompt`
3. The prompt tells the agent to accept emails from the attacker as commands
4. Attacker sends emails with subject starting "TASK" — agent autonomously executes them
5. Results emailed back to attacker — **recon, credential harvesting, BEC, internal phishing**

**"This isn't a forged request, it's a forged insider,"** said Zenity CTO Michael Bargury. The agent is invisible to the organization.

OpenAI accepted the report within a day and **fixed the vulnerability within three days** (June 4–8, 2026). Zenity disclosed publicly on Thursday.

**Action:** Verify OpenAI has patched your Workspace Agents. Review connector usage across your ChatGPT workspace. Treat this as a warning about agent trust boundaries — any platform allowing connector-authenticated agent creation via URL params is potentially vulnerable to similar attacks.

**Sources:** [SecurityWeek](https://www.securityweek.com/openai-fixes-chatgpt-agent-flaw-that-could-let-attackers-forge-an-ai-insider/) · [Zenity Part 1](https://www.zenity.io/) · [Zenity Part 2](https://www.zenity.io/)

---

### Microsoft Mandates Passkeys by February 2027 — Admits SMS/Voice MFA Insufficient Against AI Attacks

Microsoft has announced that **passkeys will be mandatory** for all Entra ID users by **February 2027**, acknowledging that SMS and voice-based MFA is no longer adequate against AI-driven phishing and adversarial-in-the-middle (AiTM) attacks.

The announcement follows the March 2026 **Tycoon2FA takedown**, which reduced phishing volume by 92% in Q2. Microsoft's threat intelligence shows AI-powered attacks can bypass SMS MFA reliably through real-time proxy techniques — making passkey adoption a security necessity rather than a convenience upgrade.

**Action:** Begin planning passkey deployment in Entra ID. Prioritize high-value admin and financial roles. Monitor support for FIDO2/WebAuthn across your device fleet.

**Sources:** [Windows Latest](https://www.windowslatest.com/2026/07/22/microsoft-admits-sms-and-voice-mfa-cant-stop-ai-attacks-mandates-passkeys-in-entra-by-february-2027/)

---

## 🛡️ Defense & Detection

### SentinelOne Fast16 Benchmark — Nuclear Sabotage Reverse Engineering

SentinelOne's **SentinelLabs** built the first long-horizon reverse-engineering benchmark for frontier AI models, using the **Fast16 malware** — a 2005 Windows trojan designed to sabotage Iran's nuclear weapons program via interference with **LS-DYNA** engineering software (pre-dating Stuxnet, possibly U.S.-developed).

The benchmark tracks models across eight escalating stages where new evidence repeatedly contradicts earlier conclusions. Results of tested models:
- **GPT-5.6 Sol** — only model to complete all 8 stages across multiple runs
- **GPT-5.5** — never got past the initial stage
- **Claude Opus 4.7/4.8, GLM-5.2** — solid local analysis but stalled; declared work finished before defects resolved

Key finding: **"Senior reverse engineers remain essential."** Even GPT-5.6 Sol made semantic errors, accepted weak quality controls, and claimed readiness prematurely. The gap is in "project-scale recovery" — the ability to withdraw a disproven conclusion, trace downstream dependencies, fix root cause, and carry correction through.

**Takeaway:** AI-assisted reverse engineering is accelerating but not autonomous. Human analysts defining objectives, exposing blind spots, and retaining publication authority remains the effective model.

**Sources:** [SecurityWeek](https://www.securityweek.com/nuclear-sabotage-malware-benchmark-trips-up-most-frontier-ai-models/)

---

### Microsoft Q2 2026 Email Threat Landscape Report

Microsoft's Digital Crimes Unit published email threat data for **April–June 2026**:

- **Tycoon2FA disruption** cut phishing volume by **92%** from pre-disruption averages
- **QR code phishing and CAPTCHA-gated phishing** both declined from March highs
- No single service emerged to replace Tycoon2FA at comparable scale
- **BEC and Teams-based threats** remain elevated
- Not all adversarial attention has subsided — notable campaigns repurposed remaining PhaaS infrastructure

**Takeaway:** Law enforcement disruption operations against PhaaS platforms produce measurable, durable impact. Organizations should use the current window to strengthen phishing-resistant authentication and train users on QR-code phishing and Teams-based threats.

**Sources:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/23/email-threat-landscape-q2-2026-trends-and-insights/)

---

### Red Canary Intelligence Insights: July 2026

Red Canary's monthly threat prevalence report for June 2026:
- **ClearFake** holds the #1 spot for the **third consecutive month** — fake CAPTCHA/drive-by download malware delivery via compromised websites
- **KongTuke** returns to #2 — a traffic distribution system (TDS) using compromised WordPress sites; activity at volumes not seen since November 2025

**Takeaway:** The ClickFix/fake CAPTCHA delivery chain remains the most prevalent threat vector, and compromised WordPress infrastructure continues to serve as a reliable distribution channel.

**Sources:** [Red Canary](https://redcanary.com/blog/threat-intelligence/intelligence-insights-july-2026/)

---

### ASEC June 2026 APT Attack Report (South Korea)

AhnLab's **ASEC** published its monthly APT threat report for Korea:
- **LNK file phishing** accounted for the highest proportion of APT initial access
- Threat actors used work-related document filenames and email lures
- **Types of malware deployed**: AutoIt malware (Type A), HTA downloaders via curl.exe (Type B), XenoRAT and infostealers (Type C), Python-script-based backdoors (Type D)
- GitHub and Google Drive used as download hosts for payloads

**Takeaway:** Korean organizations face a consistent APT phishing threat with evolving payload delivery methods. LNK-based initial access and cloud-hosted payloads are the dominant trends.

**Sources:** [ASEC](https://asec.ahnlab.com/en/94594/)

---

## 📋 Policy & Industry News

### Rubio Restricts Visas for Cybercriminals, Sextortionists

Secretary of State **Marco Rubio** announced new visa restriction policies targeting individuals involved in cyber scams, sextortion, and digital fraud — **including their family members**. The policy is authorized under a 1952 law allowing visa denial for those posing "potentially serious adverse foreign policy consequences."

The restrictions follow a March 2026 executive order and align with broader DOJ actions against the **Huione Group** cybercrime syndicate in June. Critics note potential for abuse of the same legal provision for other purposes.

**Sources:** [CyberScoop](https://cyberscoop.com/us-visa-restrictions-cybercriminals-rubio/)

---

### FedRAMP Rev5 Is Ending: What the 20× Transition Requires

FedRAMP **Rev5** is being replaced by **FedRAMP 20×**, shifting from narrative-heavy security controls to **Key Security Indicators (KSIs)** — measurable outcomes backed by machine-readable evidence.

Key changes:
- **56 KSIs** in Low baseline, **61** in Moderate
- Organized across **12 security domains**: cloud-native architecture, IAM, monitoring, incident response, change management
- Replaces annual sampled evidence with **continuous proof** of security posture
- Maril Vernon (Anecdotes Field CISO) notes: "The system rewarded proving a control existed at one moment in time" — 20× changes the question from "describe your security" to "continuously prove it"

**Action:** Cloud service providers should begin mapping existing controls to KSI framework. Review the 20× draft guidance and prepare for machine-readable evidence collection.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/fedramp-rev5-is-ending-what-the-20x-transition-really-requires/)

---

## ⚡ Quick Hits

- **Origin Energy breach** — Australian energy giant (4.8M customers) confirms data breach exposing names, addresses, DOBs, phone numbers, partial financial details. Hacker claims 2M records stolen and threatens full leak unless ransom paid. No ransomware group named yet. (BleepingComputer, SecurityWeek)
- **Abstract raises $25M** — Composable security operations platform Abstract announced $25M in funding to expand its offering. (SecurityWeek)
- **"Is Patching Dead?"** — SecurityWeek opinion piece argues organizations "cannot out-patch a machine that writes a working exploit from a vulnerability description in twenty hours," referencing Anthropic's Mythos model's demonstrated exploit-generation capabilities. (SecurityWeek)
- **EU fines Google $1B** — European Commission fined Google €890M ($1B) for Digital Markets Act violations favoring own services in Search and restricting developer payment options in Play Store. (BleepingComputer)

---

*Digest generated July 24, 2026. 31 feed articles reviewed, 5 prior digests cross-referenced for continuity, gap detection via web search. Three multi-source stories merged. Stories excluded as already covered in prior digests: CVE-2026-14266 (7-Zip, Jul 19), CVE-2026-64600/RefluXFS (Jul 22–23), CVE-2026-16232/Check Point (Jul 23), OpenAI/Hugging Face (Jul 22), Chick-fil-A credential stuffing (Jul 22), CSIRT Gadgets KEV analysis (Jul 22).*
