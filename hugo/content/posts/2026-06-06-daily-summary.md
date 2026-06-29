---
title: "UNC3753 vishing, UniFi OS CVSS 10.0🔴, SolarWinds KEV, STX RAT supply chain, OP-512 web shells"
date: 2026-06-06
tags: ["UNC3753","CVE-2026-28318","CVE-2026-34908","CVE-2026-34909","CVE-2026-34910","STX RAT","OP-512","UniFi","SolarWinds","Trend Micro","Claude Code","DBIR 2026","supply chain","vishing","Luna Moth","OP-512","Polyfill"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "UNC3753 targets US law firms with vishing and physical office intrusions in single-day extortion blitz; Ubiquiti UniFi OS critical chain (CVSS 10.0 × 3) enables unauthenticated root RCE with persistent JWT forgery; CISA adds SolarWinds Serv-U CVE-2026-28318 to KEV with active exploitation confirmed; STX RAT supply chain campaign expands to 11 packages targeting crypto traders and 100M+ X-VPN users; China-linked OP-512 deploys custom IIS web shell framework."
---

# Daily Threat Intelligence Digest — June 6, 2026

*42 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] UNC3753 (Luna Moth) Targets US Law Firms with Vishing + Physical Office Intrusions — FBI Corroborates, Single-Day Attack-to-Exfiltration Cycle**

Mandiant's Google Threat Intelligence Group (GTIG) disclosed an active, financially motivated campaign by threat cluster **UNC3753** (aka Luna Moth, Chatty Spider, Silent Ransom Group) targeting dozens of US-based legal, professional, and financial services organizations. The campaign combines voice phishing, commercial RMM tools, and — in a significant tactical escalation — **physical office intrusions** corroborated by an FBI Cyber FLASH Alert. [[Cyberpress](https://cyberpress.org/unc3753-targets-us-law-firms/)]

**Attack flow:** The chain begins with benign invoice-themed emails carrying no malicious payloads — simply priming targets for a follow-up call. Threat actors then call employees (details harvested from corporate websites), impersonating internal IT helpdesk or security teams. Victims are guided to install legitimate RMM tools (AnyDesk, Bomgar, Zoho Assist, SuperOps) via Privnote self-destructing links. Once inside, attackers pivot from BYOD endpoints through corporate VDI using Windows 365 and Citrix clients.

**Extortion velocity:** In multiple confirmed incidents, the full sequence from initial contact to data theft and extortion completed within a **single business day**. Staging and exfiltration began in under an hour in some cases. Attackers target iManage document repositories for W-2s, W-9s, SSNs, client agreements, and audit records. Exfiltration uses Google Drive (observed: 1.7 GB), WinSCP (additional 14.4 GB in one case), and Rclone. Extortion emails arrive within 30 minutes of exit, giving organizations **three days** to negotiate or face data publication on the LEAKEDDATA site at `business-data-leaks[.]com`.

**Physical escalation:** Individuals posing as IT technicians have physically entered corporate offices attempting to exfiltrate data via USB storage media — a convergence of digital and physical threat vectors rarely seen in extortion campaigns.

**IOCs:** C2 IPs include 192.236.147.131, 192.236.147.138, 193.141.60.212, 64.94.84.97. Phishing domains follow the pattern `<org>-itdesk[.]com`.

**Mitigation:** Enforce application control (WDAC) to block unauthorized RMM binaries; disable USB read/write via GPO/MDM; enable MFA on iManage, SharePoint, and VDI entry points; monitor SSH port 22 for high-volume WinSCP/Rclone transfers from internal VDIs.

---

**[NEW] UniFi OS Critical Chain — Three CVSS 10.0 Vulnerabilities Enable Unauthenticated Root RCE on Network Management Appliances**

Ubiquiti patched three critical vulnerabilities in UniFi OS Server that chain together to deliver **unauthenticated remote code execution with root privileges**. Bishop Fox confirmed the full exploit chain end-to-end on version 5.0.6 — a single crafted HTTP request yields a root shell, no credentials, no user interaction. [[Cyberpress](https://cyberpress.org/critical-unifi-os-flaws/)]

**The chain:**

1. **CVE-2026-34908 / CVE-2026-34909 (CVSS 10.0 each)** — Authentication gateway bypass via URI normalization mismatch. Nginx reads the raw `$request_uri` for auth decisions but passes the normalized `$uri` (where `%2f` decodes to `/`) to upstream backends. Attackers craft a request whose raw form starts with the auth-exempt `/api/auth/validate-sso/` prefix passing the gate, while its normalized form hits authenticated proxy routes.

2. **CVE-2026-34910 (CVSS 10.0)** — Command injection in the package-update service. The handler shells out the attacker-controlled package name via `fmt.Sprintf` into `sh -c`. No validation on the package name means shell metacharacters are interpreted directly. The `ucs-update` account holds passwordless sudo rights over `dpkg`, `chmod`, `systemctl`, and `uos` — enabling installation of a crafted `.deb` whose post-install script runs as root.

**Worse than a single patch:** Root on a UniFi OS Server means full management-plane compromise: the JWT signing key can be read and forged admin sessions minted offline. Bishop Fox confirmed that a forged owner-scope JWT token authenticated successfully against both vulnerable 5.0.6 and **fully patched 5.0.8** consoles. Any signing key stolen before patching continues to generate valid admin sessions indefinitely. In deployments with UniFi Access and UniFi Protect, the same position unlocks physical doors, clones NFC/face credentials, views live camera feeds, and deletes recorded surveillance footage.

**Action:** Patch to UniFi OS Server 5.0.8 or hardware-equivalent fixed version. Restrict TCP 11443 to a dedicated management VLAN. **Treat any instance exposed before patching as fully compromised** — rotate JWT signing key (`/data/unifi-core/config/jwt.yaml`), TLS keys, cloud tokens, and database credentials. Rebuild from known-good image. Biometric and NFC data cannot be rotated — treat as permanently disclosed.

---

**[NEW] CISA Adds SolarWinds Serv-U CVE-2026-28318 to KEV — Unauthenticated DoS, 12,000+ Servers Exposed**

CISA added **CVE-2026-28318** (uncontrolled resource consumption) to its Known Exploited Vulnerabilities catalog on June 5, confirming active exploitation targeting SolarWinds Serv-U file transfer servers. An unauthenticated attacker can crash servers by sending a crafted HTTP POST with `Content-Encoding: deflate` header — no credentials required. [[Cyberpress](https://cyberpress.org/exploited-solarwinds-serv-u-vulnerability/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-hackers-now-exploit-solarwinds-serv-u-flaw-to-crash-servers/)]

SolarWinds released Serv-U 15.5.4 Hotfix 1 on Thursday. Shodan tracks 12,000+ exposed Serv-U servers; Shadowserver finds ~3,100 (fewer false positives). Administrators who upgraded to 15.5.4 but skipped the hotfix remain vulnerable — a critical gap that patch inventory tools may miss. Federal agencies must remediate by June 19 under BOD 22-01.

**Context:** This is the 11th SolarWinds product vulnerability added to CISA's KEV catalog. The Clop ransomware gang previously exploited Serv-U RCE (CVE-2021-35211) in 2021; Chinese state-sponsored DEV-0322 also weaponized it in zero-day attacks. Block POST requests with `content-encoding` headers at the WAF as a compensating control.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] STX RAT Supply Chain Campaign Expands — 11 Trojanized Packages Including X-VPN (100M+ Users), Actor Operating Bitbucket Repository**

Cyderes' Howler Cell Threat Research Team expanded their documented STX RAT supply chain campaign from the initial CPUID HWMonitor discovery to **11 confirmed trojanized packages** spanning crypto trading platforms (Binance, MEXC, Bybit, Exodus, MetaTrader 5), Steam (lure using renamed MT5 installer), and crucially **X-VPN** (100M+ reported users). [[Malware.News/Cyderes](https://malware.news/t/inside-an-active-stx-rat-supply-chain-campaign/107614#post_1)]

All packages use an identical **CRYPTBASE.dll sideloading** technique into a multi-stage in-memory unpack chain delivering STX RAT — a reflective-loading infostealer with remote access, credential theft, and system reconnaissance capabilities. The actor, operating under alias **Leda Elacoate** (`pufferfish11@firemail[.]cc`), maintained a Bitbucket repository (`amos-trading/dist-internal`) over approximately one month, systematically expanding from crypto-focused lures to VPN software.

**Campaign evolution:** Initial packages (January 26–February 2, 2026) used C2 subdomain `helloworld[.]supp0v3[.]com`. After the initial HWMonitor disclosure, the actor rotated C2 to `welcome[.]supp0v3[.]com` rather than going dark. The X-VPN configuration contained a placeholder `referrer: changeme` value — indicating a builder-based workflow where parameters are injected prior to distribution. X-VPN shipped a fix in version 77.5.2 on May 28 (ten days from disclosure) with stricter DLL loading, startup hash verification, and hardened directory permissions.

**Defense:** Block `supp0v3[.]com` and all subdomains. Alert on CRYPTBASE.dll loading from any path other than `C:\Windows\System32\` or `SysWOW64\`. Hunts for processes loading CRYPTBASE.dll from non-standard paths followed by outbound HTTPS connections.

---

**[NEW] OP-512 — China-Linked Cluster Deploys Custom ASPX/ASHX Web Shell Framework Against IIS Servers**

ReliaQuest identified a previously undocumented China-linked espionage cluster, tracked as **OP-512**, deploying a purpose-built web shell framework targeting Internet Information Services (IIS) servers. The compromised server ran Windows Server 2016 with end-of-life .NET Framework 4.0 — EDR telemetry had flagged anomalous DNS queries 75 days before the main intrusion. [[Cyberpress](https://cyberpress.org/china-linked-aspx-ashx-web-shells/)]

**Tradecraft highlights:**
- **Self-reporting web shell:** An `.aspx` file manager encodes its own URL into hex-segmented DNS queries on access — fire-and-forget deployment that automatically reports its location to operator infrastructure
- **Dual-channel crypto:** Two `.ashx` command handlers, each with a **unique RSA public key** (separate private keys required per implant). Command pipeline: Base64 → RC4 decrypt → RSA signature verification → execution
- **Timestomping:** All three shells scan surrounding files, calculate a median last-modified timestamp, and backdate themselves — a web shell dropped in 2026 reads forensically as if placed in 2022
- **In-memory privilege escalation:** Loaded Potato Suite (BadPotato, SweetPotato, EfsPotato) via reflective .NET assembly loading — nothing written to disk

OP-512 is at least the **fourth China-linked cluster** targeting IIS servers in under a year, joining CL-STA-0048, GhostRedirector, and DragonRank. Base64-encoded `whoami` commands matched character-for-character with ReliaQuest's documented Flax Typhoon ArcGIS compromise, suggesting shared playbooks across the ecosystem.

**Detection:** Signature-based detection is ineffective by design. Focus on outbound DNS from `w3wp.exe` with long hex-segmented subdomains; reflective .NET assembly loading in IIS worker processes; and new DLL generation in ASP.NET temporary compilation directories outside deployment windows.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Trend Micro Deep Security Agent Flaw — Unprivileged Local Process Creates Repeatable Protection Gap, No Patch After 4 Months**

A researcher (Matheuzsecurity) disclosed a design flaw in Trend Micro Deep Security Agent for Linux allowing an unprivileged local process to force the agent's kernel modules to unload and reload — creating a **repeatable ~1.3-second protection gap** during which blocked content lands on disk undetected. [[Cyberpress](https://cyberpress.org/deep-security-agent-reload-flaw/); [GBHackers](https://gbhackers.com/trend-micro-deep-security-agent-flaw/)]

The attack exploits an "event storm" — sustained bursts of filesystem and process activity causing the agent's `ds_am.init` process to execute `rmmod bmhook` followed by `rmmod tmhook` (confirmed via bpftrace). Both modules reload automatically, but the window between unload and full livepatch re-patching is ~19.6 seconds total, with behavior monitoring (`bmhook`) fully absent for measurable periods. The modules repeated the unload-and-reload cycle across multiple consecutive runs — the condition is attacker-triggerable and repeatable on demand.

Reported to Trend Micro on **February 6, 2026**. After four months with no CVE assignment or confirmed fix timeline, the researcher published findings on June 3. No patch available. Classified under CWE-693 (Protection Mechanism Failure). Local-only scope limits severity, but the bypass is exploitable without root, kernel module loading rights, or direct `rmmod` calls.

---

## 🛡️ Defense & Detection

**[NEW] Microsoft Threat Intelligence: Claude Code GitHub Action's Read Tool Exposes CI/CD Secrets via Prompt Injection — Patched in v2.1.128**

Microsoft Threat Intelligence discovered that Anthropic's Claude Code GitHub Action could expose CI/CD workflow secrets when AI agents process untrusted GitHub content. While the Bash tool was sandboxed via Bubblewrap with environment scrubbing enabled for non-write-user-triggered workflows, the **Read tool was not subject to the same isolation** — it operated as direct in-process calls, bypassing the sandbox entirely and accessing `/proc/self/environ` to read `ANTHROPIC_API_KEY` and other credentials. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/)]

**Bypass chain:** The researchers embedded a prompt injection in an issue body framing credential access as a "compliance review" and instructed the model to strip the first 7 characters of any discovered API key (`sk-ant-...` → laundered to `...`). This defeated both Claude's safety filters (no visible API key prefix to trigger refusal) and GitHub's secret scanner (no known credential pattern remaining in stdout). The laundered key could then be exfiltrated via WebFetch, Bash, GitHub MCP to issue comments, or workflow logs.

Anthropic mitigated in **Claude Code v2.1.128** (May 5) by blocking access to sensitive `/proc/` files in the Read tool.

**Broader rule:** Microsoft recommends the "Agents Rule of Two" — an AI-powered workflow should never hold all three capabilities simultaneously: (1) processing untrusted input, (2) access to secrets, and (3) ability to change state or communicate externally. [[Microsoft](https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/)]

---

**[NEW] Verizon 2026 DBIR: Attacks Are Living in the Browser — Shadow AI Up 4×, Credential Abuse Invisible to Traditional Tools**

Keep Aware's analysis of the Verizon 2026 DBIR reveals structural shifts in the attack landscape that traditional network and endpoint tools are missing. The data shows 67% of users access AI services on corporate devices through personal accounts, 45% of employees are regular AI users, and Shadow AI is now the 3rd most common non-malicious insider action in DLP datasets — a **fourfold increase**. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/what-2026-dbir-confirms-attacks-are-living-in-the-browser/)]

**Key findings:** 39% of breaches involved credential abuse; 63% of Microsoft-themed phishing sites were not flagged by any VirusTotal vendor at the time of employee exposure; 100% of credential theft attempts passed through non-browser security controls (proxy, DNS filter, EDR) unblocked; 13% of unique browser extensions were high or critical risk; 93% of poor-reputation extensions were labeled as "productivity" tools by marketplace categories. ClickFix social engineering accounted for 2.7% of browser-detected attacks — a small share but a growing technique worth tracking.

**Takeaway:** The browser is no longer just an application — it is the primary work environment. Security programs relying exclusively on network, endpoint, and identity telemetry have blind spots where attackers have learned to operate.

---

## 📋 Policy & Industry News

**[NEW] Polyfill.io Service Reactivates — HTTP 401 Auth Prompts Appear on Toshiba, Muji, Samsung Smart TV Websites**

The legacy `polyfill[.]io` domain — purchased by a Chinese entity in 2024 — became active again starting late May 2026, serving HTTP 401 authentication requests to browsers visiting pages on Toshiba, Muji, Zojirushi, FiNC Technologies, Ishiyaku Publishers, and Hobonichi websites. Samsung Smart TVs also displayed the rogue login prompt on June 1. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/suspicious-polyfill-login-prompts-pop-up-on-toshiba-muji-websites/)]

No confirmed credential theft has been linked to this resurgence, but the incident highlights how dormant supply chain remnants from the 2024 Polyfill compromise (which impacted 100K+ websites) continue to pose risk. Websites that removed the service at the time but failed to clean all pages are surfacing malicious prompts years later when the domain rotates ownership or infrastructure.

---

## ⚡ Quick Hits

- **Qualys joins Anthropic's Project Glasswing and OpenAI's Trusted Access for Cyber programs** — Qualys becomes the latest major security vendor to join the frontier AI safety initiatives, following the June 3 announcement of Glasswing's expansion to 150 organizations. [[Qualys](https://blog.qualys.com/product-tech/2026/06/05/advancing-cybersecurity-in-the-age-of-frontier-ai-qualys-steps-into-project-glasswing)]
- **Metasploit adds Apache ActiveMQ RCE (CVE-2026-34197) and Gogs Rebase RCE** — New exploit modules for Apache ActiveMQ via Jolokia `addNetworkConnector()` and Gogs pull request rebase argument injection. CVE-2026-34197 requires authentication. [[Rapid7](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-05-06-2026)]
- **AI Worm prototype carries its own LLM** — Bruce Schneier highlights a researcher prototype of an AI-powered internet worm that carries and runs its own LLM on compromised computers — the closest implementation yet to John Brunner's 1975 novel conception of a worm. [[Schneier on Security](https://www.schneier.com/blog/archives/2026/06/ai-worm.html)]
- **Shadowserver identifies 1,061 exposed ATG systems, 909 in US** — Building on the June 3 CISA/FBI/NSA advisory, Shadowserver's scanning on port 10001/tcp found 1,061 accessible automatic tank gauge systems after filtering honeypots. Iranian-linked intrusions confirmed at multiple US gas stations. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/over-900-us-gas-station-tank-gauge-systems-exposed-to-attacks/)]
- **SecurityWeek roundup: Anthropic AI threat mapping, Palantir CTO eyed for CISA, Let's Encrypt post-quantum timeline** — Anthropic published a year-long ATT&CK-aligned analysis of AI-enabled operations; the Trump administration considers Palantir CTO Shyam Sankar or IBM's Tom Parker for CISA director; Let's Encrypt targets late 2026 for Merkle Tree Certificate staging (post-quantum TLS). Dragos acquired xIoT security firm Phosphorus. [[SecurityWeek](https://www.securityweek.com/in-other-news-anthropic-maps-ai-threats-unpatched-comodo-flaw-palantir-chief-eyed-for-cisa/)]
