---
title: "🔴 Chrome 151 fixes 6 critical memory flaws, 🎯 UNC6671 vishing gang hits hedge funds, ⚠️ Zero-privilege RCE in AI coding agents, ⚠️ TONTOU bypasses Spectre v2 mitigations, 🛡️ Cloudflare ships workerd sandbox fixes, 📋 Senate probes transnational scam coordination"
date: 2026-08-07
tags: ["Chrome","AI security","vulnerabilities","supply chain","critical infrastructure","phishing","data breach","ransomware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Chrome 151 addresses six critical memory-safety flaws; new research shows zero-privilege RCE in Anthropic, Google, and OpenAI coding agents and a Spectre v2 bypass leaking Linux password hashes; the UNC6671 vishing group expands hedge-fund extortion while the ChainDrop npm worm routes C2 through an Ethereum contract."
---

# Daily Threat Intelligence Digest — August 7, 2026

*91 articles ingested and analyzed from curated cyber intelligence feeds.*

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] Chrome 151 Patches 41 Flaws — Six Critical Memory-Safety Bugs in WebGL, Skia, and ANGLE

Google shipped Chrome 151.0.7922.108/.109 for Windows and macOS (151.0.7922.108 on Linux) on August 6, fixing 41 vulnerabilities including six critical use-after-free and out-of-bounds-write issues in WebGL (CVE-2026-19137, CVE-2026-19170), Aura, Skia, ANGLE, and Views. The release also resolves 35 high-severity flaws spanning V8, GPU, Media, Payments, and Web Authentication — many reachable from crafted web content as renderer footholds. Some bug reports stay restricted while the update propagates; deploy immediately, especially on endpoints that touch untrusted sites or run GPU-accelerated web apps.

**Sources:** [GBHackers](https://gbhackers.com/google-chrome-151-update-fixes-41-security-vulnerabilities/) · [Cyber Security News](https://cyberpress.org/chrome-151-use-after-free-out-of-bounds-write/) · [SecurityWeek](https://www.securityweek.com/critical-vulnerabilities-patched-with-chrome-151-update/)

### [NEW] Zero-Privilege RCE in Anthropic, Google, and OpenAI Coding Agents — Malicious GitHub Issues Execute Code

Novee Security researcher Elad Meged demonstrated that an unauthenticated attacker can use a malicious GitHub issue to achieve RCE, credential theft, persistent agent hijacking, and supply-chain compromise in default configurations of Claude Code Action, Gemini CLI, and OpenAI Codex — patterns found in more than 100 public repositories, including the vendors' own. Anthropic's fixes culminated in CVE-2026-54316, Google rated its case CVSS 10.0 and made breaking trust-model changes to headless Gemini CLI execution, and OpenAI hardened Codex by isolating stages after an AGENTS.md poisoning path. The common flaw is the agent harness — permission logic, tool routing, sandbox controls, shared workspace — not the model; any automation that processes externally controlled text without strong isolation carries the same risk.

**Sources:** [Cyber Security News](https://cyberpress.org/critical-flaws-in-claude-code-gemini-cll-openai-codex/) · [GBHackers](https://gbhackers.com/critical-flaws-in-claude-code-gemini-cli-and-openai-codex/)

### [NEW] Claude Code Executes Malicious Pull-Request Commands via .mcp.json — Anthropic Calls It Working as Designed

A malicious .mcp.json added to a pull request can launch local commands on a developer's workstation when Claude Code opens an already-trusted repository — with no prompt injection, user interaction, or Claude account — because project-scoped MCP configuration is processed automatically at session start (researcher Kevin Breen). The process runs with the developer's privileges and can expose environment variables, source code, cloud credentials, SSH keys, and Claude config; Anthropic classified the behavior as working as designed under its folder-trust model. Treat .mcp.json, .claude/, and related agent configuration as executable code, review PR branches before agent tools open them, and isolate PR reviews in disposable VMs.

**Sources:** [Cyber Security News](https://cyberpress.org/claude-code-rce-flaw-pull-requests-execute-commands/) · [GBHackers](https://gbhackers.com/claude-code-rce-flaw/)

### [UPDATE] ChainDrop npm Worm Rotates C2 via Ethereum Contract, Mints Real Provenance for Poisoned Packages

Unit 42's deep-dive on the ChainDrop/Shai-Hulud worm adds major new detail: C2 domains are resolved from an Ethereum smart contract (0xE1f2395ee43e45A1556EC6438a88c31B83493103) and were silently rotated to awqhnjewqjkl.icu on August 4, with a GitHub commit-search fallback, and the worm scrapes GitHub Actions runner memory for OIDC tokens and ephemeral secrets. A repository-gated path targeting opensearch-js signs poisoned tarballs with genuine Sigstore/SLSA provenance — valid provenance no longer means a clean package — and 453 public exfiltration repositories were found across five accounts. With 400+ packages (keyv, flat-cache, cacheable-request, cache-manager) still compromised, enumerate every package your npm credentials can publish, rotate exposed credentials, and clear poisoned lockfiles and caches, which survive tag rollbacks.

**Sources:** [Unit 42](https://unit42.paloaltonetworks.com/chaindrop-npm-worm-analysis/) · [Cyber Security News](https://cyberpress.org/shai-hulud-npm-worm-returns/) · [Cyber Security News — ChainDrop](https://cyberpress.org/chaindrop-automates-npm-package-infections/)

### [UPDATE] Forescout: 4,407 Rockwell Controllers Still Exposed as Water Campaign Spreads — 22 in Attack-Hit Cities

A new Vedere Labs scan (August 5) finds 4,407 internet-facing Rockwell Automation/Allen-Bradley controllers on port 44818 (EtherNet/IP), 65% in the US, with MicroLogix 1400 accounting for half — including 22 hosts in cities hit by the multi-state campaign, 86% of them on a single mobile carrier network. Over 70% of US controllers sit behind cellular routers, matching the FBI/EPA advisory's description of the attack vector; exposure is down 47% from the March 2020 peak but remains a live risk, and 19 of the 22 hosts are susceptible to CVE-2017-16740 (Modbus TCP DoS). Block direct internet access to EtherNet/IP and Modbus TCP, move cellular gateways to private APNs or VPNs, and replace end-of-life MicroLogix 1100s.

**Sources:** [Cyber Security News](https://cyberpress.org/4407-internet-facing-industrial-controllers/) · [CyberScoop](https://cyberscoop.com/exposed-rockwell-controllers-water-system-attacks/) · [GBHackers](https://gbhackers.com/hackers-target-internet-exposed-rockwell-plcs/)

### [NEW] UNC6671 Vishing Gang Targets Hedge Funds — BlackFile Rebrands to Redact, Pink, Helix, Falcon

The BlackFile-linked extortion group UNC6671 has hit Point72, Millennium, Two Sigma, Citadel, and private-equity firms with helpdesk vishing that funnels employees into adversary-in-the-middle passkey/MFA phishing pages (passkeyhelpdesk.com, addssopasskey.com), then drains Microsoft 365 and Okta SSO dashboards and deletes security notifications from compromised inboxes. Google Threat Intelligence Group tracked over $10.6 million in Bitcoin to group wallets between January and May 2026, with demands up to $3M settling near $750K; Mandiant is assisting several dozen compromised organizations. Treat unsolicited "passkey/MFA enrollment" calls as hostile and hunt AiTM sign-ins from residential proxies.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hedge-fund-cyberattacks-tied-to-blackfile-linked-unc6671-extortion-group/) · [Cyber Security News](https://cyberpress.org/unc6671-vishing-hits-financials/) · [SecurityWeek](https://www.securityweek.com/vishing-extortion-group-unc6671-rebrands-after-making-millions/)

### [NEW] Swiss Government SharePoint Breach Compromises ~200 Accounts

Attackers exploited SharePoint vulnerabilities fixed in the July Patch Tuesday updates — either CVE-2026-56164 (actively exploited privilege escalation) or CVE-2026-50522 (critical RCE later used to steal machine keys) — to breach Switzerland's federal SharePoint platform, compromising login credentials for roughly 200 accounts before detection on July 28. The Federal Office for IT (BIT) blocked external access, patched, reset passwords, and is reinstalling servers; no data theft beyond credentials has been found and no group has claimed the attack. Patch SharePoint immediately and audit for machine-key theft, the persistence mechanism that kept attackers in post-patch.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/swiss-government-sharepoint-breach-compromised-200-accounts/)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] Patchwork APT Runs Fake-PDF Shortcut Chains and Android Spyware

Patchwork (Dropping Elephant) has refreshed its espionage tooling with .lnk shortcuts disguised as PDFs — a June 2026 China energy-sector contract lure — that use PowerShell to drop memory-resident RATs via the Donut loader while patching AMSI, Windows Lockdown Policy, and Event Tracing for Windows to evade detection. The group also deploys trojanized Android apps that steal messages, files, call records, keystrokes, audio, and images, plus DLL side-loading through Fondue.exe/APPWIZ.cpl and VLC/libvlc.dll chains with scheduled-task persistence (GoogleErrorReport). Targets span government, defense, energy, and research across Asia, Europe, Türkiye, and the US — review shortcut-based document lures and hunt the Donut/QueueUserAPC patterns.

**Source:** [Cyber Security News](https://cyberpress.org/patchwork-apt-expands-espionage/)

### [NEW] ClickFix Delivers macOS Crypto-Draining Infostealer — First Partial-Wallet Drainer Seen

Huntress dissected a Go-based macOS infostealer delivered via ClickFix that steals browser passwords, Apple Keychain data, and cached credentials, and can intercept cryptocurrency transactions before signing — uniquely able to divert only a percentage of a wallet (Bitcoin, Litecoin, Dogecoin, Monero, Ethereum, XRP) rather than emptying it. The chain uses a Bash profiler that fetches an architecture-matched Mach-O payload, strips the quarantine attribute to bypass Gatekeeper alerts, and phishes admin credentials via a fake osascript error; C2 runs on Aeza Group infrastructure, a US/UK-sanctioned Russian bulletproof hoster. Gatekeeper quarantine removal and fake password prompts are the tells — block the loader pattern and audit macOS endpoints for the trustd-directory masquerade.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/clickfix-attack-pushes-macos-infostealer-for-crypto-theft-attacks/)

### [NEW] "Payroll Pirates": Arctic Wolf Tracks AiTM BEC Campaign Against Finance Workflows

Arctic Wolf is tracking an active business-email-compromise campaign using adversary-in-the-middle phishing to compromise Microsoft 365 accounts, identify personnel involved in financial workflows, and collect related email. The operators route malicious sign-ins through residential proxies to masquerade as consumer traffic and keep compromised sessions alive with automated activity at roughly eight-hour intervals. Hunt for AiTM sign-ins from residential IP ranges and anomalous session refreshes on finance-adjacent accounts.

**Source:** [Arctic Wolf via Malware News](https://malware.news/t/payroll-pirates-strange-new-tides-in-business-email-compromise/124581)

---

## ⚠️ Vulnerabilities & Patches

### [NEW] TONTOU: New CPU Attack Bypasses Spectre v2 Mitigations, Leaks Linux Password Hashes

MIT CSAIL researchers demonstrated a Time-of-Neutralization-to-Time-of-Use (TONTOU) attack that re-poisons branch-predictor state after eIBRS (Intel) or Safe RET (AMD) neutralization but before use, via unprivileged timer-interrupt injection. On an AMD Zen 2 host with the latest mitigations, the exploit leaked arbitrary kernel memory including /etc/shadow at 5.47 bytes/s with 91.97% accuracy — locating the file in five of ten runs, about 18 minutes each. Intel systems are also affected with added complexity; AMD published an advisory linking the interrupt-injection issue to Linux's Safe RET implementation.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-tontou-cpu-attack-bypasses-spectre-v2-fixes-leaks-linux-password-hashes/)

### [NEW] SpecterOps: WSUS Can Become a "Backdoor Factory" — NTLM Relay to SUSDB Delivers Malicious Updates

New research shows attackers can coerce a WSUS server's machine account into NTLM-authenticating to an attacker-controlled relay, then relay into the SQL Server hosting SUSDB and chain stored procedures to create a malicious update, target specific computer groups, and deploy it through the organization's trusted patch channel. A second technique bypasses signature validation to deliver unsigned payloads via BITS using .txt/.esd extensions. Combined with July advisories CVE-2026-50444 (missing authentication) and CVE-2026-50328 (tampering/DoS), WSUS is a high-value target: enforce Extended Protection for Authentication on the database, restrict ports 8530/8531, and retire unused instances.

**Sources:** [Cyber Security News](https://cyberpress.org/wsus-flaw-enterprise-update-servers-malware-delivery-systems/) · [GBHackers](https://gbhackers.com/hackers-can-abuse-microsoft-wsus-servers/)

### [NEW] ZBT Routers Ship With ENDLESSDOORS Factory Backdoor — Root C2 Calls Out Every ~35 Seconds

At least 20 Zbtlink router models (sold under Zbtlink, Wiflyer, and white-label brands) contain a factory-embedded implant tracked as CVE-2026-66747 that runs as root at boot and maintains outbound cleartext connections to hardcoded C2 (zbtctl.epplink.net, online-string.com, plus IPs), executing commands via popen() including an interactive root shell. Because the device initiates the connection, firewalls and NAT do not block it; operators can steal traffic, alter settings, or pivot into connected networks. Identify devices by model number rather than printed branding and block the listed C2 indicators.

**Source:** [Cyber Security News](https://cyberpress.org/zbt-routers-hide-root-backdoor/)

### [NEW] Enterprise Java Pre-Auth RCE Chains: BadBonita and SSOnOf(a)biz

Black Hat 2026 research (Novee) detailed 12 flaws across four enterprise Java platforms, including two pre-authentication RCE chains: BadBonita abuses URL-parsing and servlet-dispatch discrepancies plus partial-match regex filters to reach Bonita BPM's internal /serverAPI/ XStream deserialization; SSOnOf(a)biz (CVE-2026-31986) forges SSO tokens using Apache OFBiz's hardcoded HMAC key, then reaches Groovy evaluation through a preference-gate bypass. Neither chain requires legitimate credentials on default configurations. Treat internal middleware endpoints as attacker-reachable, replace partial regex path matching, and rotate shipped signing keys.

**Sources:** [Cyber Security News](https://cyberpress.org/enterprise-java-bonita-bpm-apache-ofbiz/) · [GBHackers](https://gbhackers.com/enterprise-java-vulnerabilities/)

### [NEW] Microsoft and Apple Ship Fresh Updates — Three CVSS 10.0, Four 9.9, macOS Screen Sharing Bypass

Microsoft's August 6 batch fixes a dozen-plus flaws across Active Directory, Azure, Entra, SharePoint, and Teams, led by three CVSS 10.0 network-exploitable elevation-of-privilege issues: CVE-2026-63508 (missing authentication in Planetary Computer Pro), CVE-2026-56162 (improper authentication in Azure SQL Database), and CVE-2026-65667 (missing authorization in Teams), plus 9.9s including CVE-2026-50515 (Azure Service Bus RCE) and CVE-2026-50481 (Active Directory EoP). Apple patched CVE-2026-65400 (CVSS 7.5), an authentication bypass letting network attackers log into Screen Sharing without credentials, in macOS Tahoe 26.6.1, Sequoia 15.7.9, and Sonoma 14.8.9.

**Source:** [SecurityWeek](https://www.securityweek.com/microsoft-apple-release-fresh-security-updates/)

### [NEW] Windows Hello Keys Can Be "Borrowed" for Entra ID Token Theft and Rogue Device Registration

New research (Mollema) shows a low-privilege process in an authenticated Windows session can request signatures from the user's Windows Hello for Business key — without PIN, biometrics, or admin rights — by using cached authentication material via the Passport Key Storage Provider. The signing capability enables Primary Refresh Token requests and WebAuthn-style assertions that can register an attacker-controlled Entra device for persistent access; no TPM key extraction is involved. Monitor Entra sign-ins lacking device IDs, unexpected device registrations, and new passkey enrollments.

**Source:** [Cyber Security News](https://cyberpress.org/windows-hello-keys-bypass-pins-gain-entra-id/)

### [NEW] NatJack: NAT Table Manipulation Hijacks TCP and Tamper With DNS Across Vendors

New research describes NatJack, a family of NAT state-table manipulation techniques — crafted spoofed packets that rewrite mappings in real time — enabling TCP hijacking, UDP DNS redirection, NAT port disclosure, and denial of service against flows sharing a NAT device. All evaluated NAT implementations (routers, firewalls, hypervisors, Kubernetes/Docker bridges) are affected to some degree; Microsoft fixed its Windows NAT (CVE-2026-56181), Linux netfilter patched under CVE-2026-63913, and AWS hardened NAT Gateway and Network Load Balancer. Stop treating NAT as a security boundary and segment untrusted tenants from high-value workloads sharing the same device.

**Source:** [GBHackers](https://gbhackers.com/new-natjack-nat-attack/)

### [NEW] Check Point Breaks Cloudflare Code Mode — Five workerd Flaws Enable Sandbox Escape and Cross-Tenant Leak

Check Point Research found five memory-corruption bugs in workerd, the runtime behind Code Mode and Cloudflare Workers — two rated critical (node:zlib use-after-free, HTMLRewriter UAF), plus URLPattern out-of-bounds reads and a KV SQL authorizer bypass enabling arbitrary deserialization. Demonstrated exploits include a Code Mode sandbox escape to native host code starting from prompt injection, and a cross-tenant heap read leaking another Worker's secrets — the tcmalloc heap sits outside both V8's cage and memory-protection keys. Cloudflare fixed managed Workers in production and shipped workerd v1.20260619.1 for self-hosted deployments; no CVEs assigned yet.

**Source:** [Check Point Research via Malware News](https://malware.news/t/when-agentic-glue-melts-exploiting-cloudflare-code-mode-and-workers/124585)

---

## 📋 Policy & Industry News

### Senate Probes Federal Coordination Against Transnational Scam Centers

Senators from both parties pressed administration officials on whether 13 federal agencies and foreign allies coordinate enough against scam operations, with witnesses acknowledging an interagency action plan is still in review and that crackdowns often displace scammers (progress in Cambodia versus Burma and Laos). Sen. Ricketts floated a Joint Interagency Task Force-style multinational mechanism; Sen. Shaheen's bipartisan SCAM Act seeks a single federal lead. The hearing reflects scam centers' blend of cybercrime, human trafficking, money laundering, and cryptocurrency.

**Source:** [CyberScoop](https://cyberscoop.com/senate-hearing-transnational-scam-task-force/)

### ICE Is Buying Credit Card Records Through Data Brokers

Reporting highlighted by Bruce Schneier shows ICE is purchasing credit card application data from data brokers — information consumers provide when opening cards — expanding the agency's data-broker acquisition practices. The disclosure renews scrutiny of buying financial data that would require legal process if obtained directly from financial institutions.

**Source:** [Schneier on Security](https://www.schneier.com/blog/archives/2026/08/ice-is-buying-access-to-credit-card-records.html)

### Unlimited Technology Systems Breach Impacts 3.8 Million — SSNs and Medical Data Stolen

Healthcare revenue-cycle technology provider Unlimited Technology Systems is notifying 3,803,750 individuals that attackers stole personal, medical, and health insurance data — names, SSNs, diagnoses, dates of service, insurance policy numbers, and scanned IDs — from a commercial data center between October 5–10, 2025. The company reported the incident to HHS in late July (added to the breach portal August 6) and is offering two years of credit monitoring; no actor has claimed the breach and no misuse has been reported. Affected individuals should freeze credit and watch for medical-identity fraud.

**Source:** [SecurityWeek](https://www.securityweek.com/3-8-million-impacted-by-unlimited-technology-systems-data-breach/)

---

## ⚡ Quick Hits

- **Cloudflare launches open-source "Cloudflare OS"** — an AI-agent workspace with a security and governance layer (Gatekeepers) to control agents' access to internal data. ([Cyber Security News](https://cyberpress.org/cloudflare-launches-open-source-os/))
- **"Papyrus" mobile ad fraud** — novel-reading apps hide WebViewOut browser workers behind the reading UI, generating fake clicks, scrolling, and consent-dialog interaction on 800+ domains; C2-driven behavior changes without app updates. ([Cyber Security News](https://cyberpress.org/papyrus-test-mode-exposed/))
- **Cardiology Associates of Port Huron** — alleged June intrusion with patient data theft; the practice has not issued a public disclosure despite reporting. ([Malware News](https://malware.news/t/cardiology-associates-of-port-huron-remains-silent-although-they-were-allegedly-hacked-and-had-patient-data-stolen-in-june/124576))
