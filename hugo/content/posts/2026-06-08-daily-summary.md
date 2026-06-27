---
title: "🇲 Miasma Hits 73 MS GitHub Repos, 🛡️ C0XMO Botnet Targets DD-WRT, 🔒 OpenAI ChatGPT Lockdown Mode, 🕵️‍♂️ SRG Fast-Flux Exposed, 🧱 VerdantBamboo pfSense BRICKSTORM, 📱 Instagram AI Hack Confirmed"
date: 2026-06-08
tags: ["Miasma","Microsoft","GitHub","supply chain","C0XMO","botnet","DD-WRT","OpenAI","ChatGPT","Silent Ransom Group","UNC3753","VerdantBamboo","BRICKSTORM","pfSense","Kimsuky","Instagram","Meta"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Miasma worm hits 73 Microsoft GitHub repositories in the most aggressive supply chain attack on AI coding agents to date — planted config files execute credential harvesters when developers open repos in Claude Code, Cursor, or VS Code. Plus: C0XMO botnet exploits DD-WRT buffer overflow with multi-arch support, OpenAI rolls out ChatGPT Lockdown Mode blocking prompt injection exfiltration, Silent Ransom Group fast-flux infrastructure exposed across multiple continents, VerdantBamboo BRICKSTORM variant deployed on MSP pfSense firewalls, and Meta confirms 20,225 Instagram accounts hacked via AI support tool abuse."
---
# Daily Threat Intelligence Digest — June 8, 2026

*15 articles ingested and analyzed. One critical gap.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Miasma Worm Hits 73 Microsoft GitHub Repositories — Supply Chain Attack Targets AI Coding Agents via Claude Code, Cursor, VS Code Hooks, Azure CI/CD Permanently Broken**

On June 5, GitHub disabled 73 repositories across four Microsoft organizations (Azure, microsoft, Azure-Samples, MicrosoftDocs) in a 105-second automated sweep after a malicious commit was pushed to `Azure/durabletask` using a previously compromised contributor account — the same account used in the May 19 PyPI attack on the same project. [[Computing.co.uk](https://www.computing.co.uk/news/2026/security/microsoft-s-github-repositories-taken-offline-amid-miasma-supply-chain-attack); [StepSecurity](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents); [OpenSourceMalware](https://opensourcemalware.com/blog/miasma-reaches-azure); [The Next Web](https://thenextweb.com/news/miasma-worm-microsoft-github-supply-chain); [The Hacker News](https://thehackernews.com/2026/06/miasma-worm-hits-73-microsoft-github.html)]

**How it works:** The attacker backdated the commit to 2020-03-09 and used `[skip ci]` to evade CI detection. The commit planted zero source code changes but added five files — four configuration files and one 4.6 MB obfuscated JavaScript credential harvester (`setup.js`). Each config file targets a different execution trigger:

- **Claude Code & Gemini CLI:** A `SessionStart` hook in `.claude/settings.json` executes `node .github/setup.js` automatically when an AI session opens in the repo directory — no explicit invocation required.
- **Cursor AI:** A `.cursor/rules/setup.mdc` file with `alwaysApply: true` tells the agent to run the payload as a "project setup requirement."
- **VS Code:** A `.vscode/tasks.json` entry with `"runOn": "folderOpen"` triggers execution when the folder is opened in VS Code — no AI agent needed.
- **npm:** A `preinstall` script in `package.json` fires during `npm install`.

**The payload:** Once triggered, the Bun-based worm harvests credentials for AWS, Azure, GCP, Kubernetes, npm, and GitHub, then uses those stolen tokens to propagate itself into any repository the victim can write to — spreading autonomously across the ecosystem. The credential harvester also targets AI coding tool configurations (Claude Code, Cursor, VS Code settings).

**Impact:** `Azure/functions-action@v1` — the official GitHub Action for deploying Azure Functions — was among the disabled repos, breaking CI/CD pipelines globally. Microsoft characterized the incident as an "internal management issue." Organizations relying on the action were forced to migrate to Azure CLI, Azure DevOps Pipelines, or Zip Deploy. Affected projects include `durabletask` (.NET, Go, JS, Java, MSSQL implementations), `azure-functions-host`, `azure-webjobs-sdk`, language workers across 7 stacks, `azure-search-openai-demo`, and `windows-driver-docs`.

**Campaign context:** Miasma is a rebrand of Mini Shai-Hulud, whose source code was open-sourced by the TeamPCP threat group in May 2026. This is the same worm that compromised 32 `@redhat-cloud-services` npm packages on June 1. Unlike earlier Shai-Hulud strains (which targeted AWS/GitHub credentials), this variant added dedicated Azure and GCP credential collectors and shifted from "execute on package install" to "execute on folder open" — bypassing traditional supply chain defenses focused on package registry hooks.

**Action:** Organizations should (1) audit GitHub repositories for unexpected `.claude/`, `.cursor/`, `.vscode/` configuration files or `setup.js` payloads, (2) block `SessionStart` hooks for Claude Code/Gemini CLI in shared repos, (3) search for unexplained public repos described as "Miasma: The Spreading Blight," and (4) consider this a watershed moment for supply chain security — the attack surface for AI coding agents now includes every repository a developer opens.

---

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Silent Ransom Group (UNC3753) Fast-Flux Infrastructure Exposed — Residential Proxy Networks Span Multiple Continents**

Resecurity published an analysis of Silent Ransom Group's infrastructure, revealing that their data leak site (`business-data-leaks[.]com`) and related C2 infrastructure rely on DNS fast-flux techniques using residential IP addresses across Latin America, Eastern Europe, Central Asia, the Middle East, and Asia. [[DataBreaches.net via Malware.News](https://malware.news/t/silent-ransom-group-srg-uncovering-dns-fast-flux-infrastructure/107631#post_1); [BleepingComputer](https://www.bleepingcomputer.com/news/security/silent-ransom-group-targets-law-firms-with-fake-it-support-calls/)]

**Technical detail:** The constant IP rotation makes takedown attempts and IP-blocking countermeasures far less effective. The same infrastructure has been linked to additional cybercrime-related services and domains beyond SRG's leak platform. This infrastructure finding complements the Mandiant/UNC3753 law firm targeting report covered on June 6 — the group's operational security includes layered infrastructure resilience alongside its vishing and physical intrusion tactics.

**Prior context:** SRG uses callback phishing (BazarCall-style) impersonating IT helpdesk, deploying RMM tools via Privnote self-destructing links, and exfiltrating via WinSCP/Rclone. Extortion emails arrive within 30 minutes of exit, with a 3-day negotiation deadline and escalation to direct calls to clients and regulators.

**[UPDATE] VerdantBamboo BRICKSTORM Campaign — pfSense FreeBSD Variant Deployed on MSP Firewalls, 18-Month Access Maintained**

Volexity's ongoing investigation into the VerdantBamboo (WARP PANDA / UNC5221) campaign has uncovered a pfSense firewall compromise at a managed service provider, deploying a FreeBSD-compatible variant of the BRICKSTORM backdoor. [[Cyberpress](https://cyberpress.org/verdantbamboo-breaches-pfsense-firewall/)]

**New detail:** The attackers deployed a BSD-compatible BRICKSTORM implant named `blocklist` under `/usr/local/libexec/ipsec/` on the MSP's pfSense firewall, and modified `/etc/rc.d/cron` for persistence. They enabled web SSL VPN access to reconnect to the internal network, then pivoted to deploy the PLENET/GRIMBOLT backdoor on a Synology NAS. Two additional malware families were identified: AGENTPSD (basic Python reverse shell) and PLENET (.NET Native AOT backdoor for Linux). The victim organization's network edge appliances — lacking EDR coverage — provided persistent beachheads that survived initial remediation attempts.

**Prior context (covered June 5):** The campaign achieved 18+ months of persistent access through network edge appliances (Egnyte Storage Sync VM, pfSense, Synology NAS). C2 consistently uses Cloudflare IP addresses with distinct TLS certificates.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] C0XMO Botnet Exploits Six-Year-Old DD-WRT Buffer Overflow — Gafgyt Variant with Multi-Arch Support, Actively Kills Rival Malware**

Fortinet discovered C0XMO, a new Gafgyt/IoT botnet variant actively spreading via CVE-2021-27137 (CVSS 9.8), a buffer overflow in DD-WRT router firmware requiring no authentication for arbitrary code execution. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/c0xmo-botnet-spreads-via-dd-wrt-router-flaw-kills-rival-malware/)]

**Architecture breadth:** The malware compiles for ARM, MIPS, PowerPC, SuperH, x86, x86_64, and other architectures — targeting DVRs, routers, video management platforms, and Android-based devices. Samples were found using exploits for each platform.

**Propagation:** C0XMO downloads a Python scanner that brute-forces Telnet/SSH credentials on ports 22, 23, 80, 443, 7547, 8080, 8443, 8888, and others. After access, it copies itself to hidden locations (`/tmp/.sys`, `/var/tmp/.sys`, `/dev/shm/.sys`) and creates cron jobs for 15-minute persistence.

**Aggressive ecosystem competition:** C0XMO actively scans running processes to identify competitor botnet clients (and red-team tools, dev tools), terminates them, deletes their binaries, and removes their persistence mechanisms. It supports 19 DDoS methods including UDP/TCP/SYN/ICMP floods, "ping of death," NTP/Memcached amplification, Discord voice UDP floods, and Valve-specific floods.

**Fortinet rating:** "A considerably more advanced architecture and feature set compared to earlier IoT botnets." C2 communication uses a custom multi-stage handshake with magic strings and shared secrets.

---

## 🛡️ Defense & Detection

**[NEW] OpenAI Rolls Out ChatGPT Account Security Controls — Lockdown Mode Blocks Prompt Injection Exfiltration**

OpenAI is rolling out three new account security controls for ChatGPT: [[SecurityWeek](https://www.securityweek.com/openai-rolling-out-chatgpt-account-security-controls/)]

**1. Lockdown Mode** — Designed for users handling highly sensitive data. Blocks outbound network requests that could exfiltrate data from prompt injection attacks. When enabled, disables live web browsing, image support, deep research, agent mode, canvas networking, and file downloads. Available at `Settings > Security > Advanced Security`. **Important caveat:** Does not prevent prompt injections from appearing in processed content — only blocks the exfiltration stage.

**2. Active Sessions** — A panel showing all currently signed-in sessions and devices, with one-click logout for unrecognized sessions. Works for all ChatGPT accounts except those using organizational SSO.

**3. Advanced Account Security** (previously announced for high-risk users) — Opt-in feature that disables password-based login entirely, requiring FIDO2 physical security keys or passkeys. Replaces email/SMS account recovery with backup passkeys and recovery keys. Shortens session validity.

**Bottom line:** Lockdown Mode is the first dedicated anti-prompt-injection control at the platform level for consumer AI — limited in scope (prevents exfiltration, not injection), but a meaningful hedge for enterprise ChatGPT users handling sensitive data.

---

## 📋 Policy & Industry News

**[NEW] Ex-IBM Threat Intel Executive Alleges IBM and AT&T Hid Nation-State Breaches from Government**

William Barlow, former IBM Vice President of Threat Intelligence, filed a lawsuit claiming IBM and AT&T lacked basic security controls and concealed nation-state hacking breaches from government authorities. The unsealed complaint alleges that the companies failed to maintain logs for AT&T-managed VPN connections into IBM cloud services, preventing detection of unauthorized access. [[DataBreaches.net via Malware.News](https://malware.news/t/ex-threat-intel-exec-accuses-ibm-and-att-of-hiding-hacks/107629#post_1)]

**Context:** Tiffany Wang originally reported the story on DataBreaches.net. The lawsuit raises fundamental questions about security monitoring at two of the largest providers of government and enterprise infrastructure services. If proven, the allegations suggest systemic failures in incident detection and mandatory breach reporting — with national security implications given IBM and AT&T's roles in federal IT systems.

---

## ⚡ Quick Hits

- **[UPDATE] Instagram Meta AI Hack — Official Disclosure Confirms 20,225 Accounts Compromised** — Meta filed a data breach letter with the Maine Attorney General confirming the HTS AI-powered support tool bug allowed attackers to redirect password reset links to their own email addresses. High-profile victims include the Obama White House, Sephora, and Space Force Chief Master Sergeant John Bentivegna. Accounts without 2FA were exclusively affected. HTS tool disabled pending full remediation. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/meta-ai-support-data-breach-affects-20-000-instagram-accounts/); [SecurityWeek](https://www.securityweek.com/meta-says-20000-instagram-accounts-hacked-via-ai-tool-abuse/)]

- **[NEW] Kimsuky Targets South Korean Unification Ministry with Malicious PDF LNK** — The North Korean APT group distributed a malicious LNK file disguised as a Middle East policy briefing document (`(대외보안)통일부_중동상황관련_정책간담회_기획안.pdf.lnk`) targeting South Korea's Ministry of Unification. Likely aims to establish persistent access to inter-Korean policy discussions and diplomatic communications. [[Malware.News](https://malware.news/t/kimsuky-pdf/107628#post_1)]
