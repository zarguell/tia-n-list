---
title: "🚨 Cisco SD-WAN Zero-Day, 🛡️ Comodo ComoDoS, 🎯 VerdantBamboo BRICKSTORM, ⚠️ Triple npm Onslaught, 🔴 DentaQuest 2.6M Breach"
date: 2026-06-05
tags: ["Cisco","SD-WAN","zero-day","Comodo","ComoDoS","VerdantBamboo","BRICKSTORM","npm","supply-chain","IronWorm","Miasma","DentaQuest","data-breach","VECT","ransomware","Microsoft Edge","Hola Browser","MCP","Five Eyes","Gemini","Zapocalypse"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Cisco's 7th SD-WAN zero-day in 2026 (CVE-2026-20245) actively exploited with no patch available. Comodo ComoDoS zero-day goes unpatched — Marcus Hutchins discovers remote IPv6 crash. VerdantBamboo APT shows 18-month dwell time via network appliances. Triple npm supply chain onslaught (IronWorm, Phantom Gyp/Miasma, Shai-Hulud wave) hits 100+ packages. DentaQuest breach exposes 2.6M accounts. Key actions: patch adjacent Cisco SD-WAN CVEs, audit network appliance access, rotate npm tokens, and monitor for WSL2 payload staging blind spots."
---

# Daily Threat Intelligence Digest — June 5, 2026

*91 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit r/cybersecurity skipped — both `/hot/` and `/new/` returned errors (old.reddit.com inaccessible). tl;dr sec #331 (published ~June 4) checked — identified no material gaps; Zapocalypse chain (Token Security) patched in March, covered here as defense insight. Prior digests: June 1–4, 2026. Stale CVE/topic blocklist applied: CVE-2022-0492 (cgroup container escape, covered June 4), Dashlane vault breach (covered June 2), TA4922/Atlas RAT (covered June 4), Stock Exchange espionage (covered June 4), UN WFP breach (covered June 3), Mirasvit Magento RCE (covered June 2).*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Cisco Catalyst SD-WAN Manager CVE-2026-20245 — 7th SD-WAN Zero-Day of 2026, Actively Exploited, No Patch Available**

Cisco disclosed a high-severity privilege escalation vulnerability (CVSS 7.8) in its Catalyst SD-WAN Manager (formerly vManage) that is being actively exploited in the wild, with observed cases resulting in unauthorized configuration changes pushed to edge devices. Tracked as **CVE-2026-20245**, the flaw allows authenticated attackers with `netadmin` privileges to upload a crafted file and execute arbitrary commands as root. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-cisco-sd-wan-flaw-exploited-in-zero-day-attacks-to-gain-root/); [SecurityWeek](https://www.securityweek.com/cisco-warns-of-7th-sd-wan-zero-day-exploited-in-2026/); [GBHackers](https://gbhackers.com/cisco-sd-wan-security-flaw/)]

**Attack chain context:** The most likely path chains CVE-2026-20182 (CVSS 10.0) or CVE-2026-20127 (CVSS 10.0) — both authentication bypasses in the SD-WAN Controller exploited by threat actor **UAT-8616** (Cisco Talos) since at least 2023 — to obtain the `netadmin` privileges required, then deploys CVE-2026-20245 to escalate to root. This marks the seventh SD-WAN vulnerability exploited in 2026 alone, indicating a sustained, methodical campaign against Cisco SD-WAN infrastructure.

**Indicators of compromise:** Check `/var/log/scripts.log` for entries referencing `/usr/bin/vconfd_script_upload_tenant_list.sh` with suspicious `-cli path` arguments. Also audit SD-WAN Controller authentication logs for `"Accepted publickey for vmanage-admin"` from unknown IPs.

**Action:** No patch or workaround exists. Organizations should (1) immediately patch CVE-2026-20182 and CVE-2026-20127 (patches available since mid-May) to break the attack chain, (2) audit and restrict `netadmin` accounts, (3) collect admin-tech files before any upgrades, and (4) treat internet-exposed SD-WAN Manager instances as priority incidents — patching alone won't remediate already-compromised systems.

---

**[NEW] Comodo Internet Security 0-Day (ComoDoS) — Remote IPv6 Packet Crashes Windows, Vendor Unresponsive for Months**

A critical zero-day vulnerability discovered by **Marcus Hutchins** (MalwareTech) in Comodo Internet Security's firewall driver `Inspect.sys` allows remote attackers to crash a target Windows system with a **single IPv6 packet**, bypassing all firewall rules. Dubbed **ComoDoS**, the flaw is an integer underflow in the IPv6 extension header parser that wraps `payload_length` to ~18 quintillion bytes, causing immediate system crash at DISPATCH_LEVEL. [[Cyberpress](https://cyberpress.org/comodo-internet-security-0-day/); [GBHackers](https://gbhackers.com/comodo-internet-security-0-day-flaw/)]

**Key technical details:**
- The crash is triggerable regardless of firewall rules or open/closed ports — the IPv6 parsing occurs *before* enforcement
- A reachable OOB-write primitive via `memcpy` with a 4 GB copy size exists but is too large to survive under realistic network conditions, making RCE unlikely with this bug alone
- Hutchins submitted a full root-cause analysis, patch recommendations, and PoC to Comodo — **received no acknowledgment** despite two follow-ups
- This follows ZDI's nearly two-year failed attempt to get Comodo to patch a separate vulnerability (ZDI-24-953)
- Full PoC published on GitHub via Scapy: `IPv6 + IPv6ExtHdrDestOpt + TCP`

**Verdict:** RCE is unlikely from this specific bug, but the crash (DoS) is trivial to trigger remotely. Organizations using Comodo Internet Security should monitor for a vendor response and consider alternative endpoint protection if none materializes.

---

**[NEW] Microsoft Edge Patches Three Pwn2Own Vulnerabilities — CVE-2026-45495 Enables Remote Code Execution**

Microsoft patched three Edge browser vulnerabilities discovered at the Pwn2Own competition by researcher **Orange Tsai** (DEVCORE Research Team), disclosed June 4. [[Cyberpress](https://cyberpress.org/microsoft-edge-vulnerability/); [GBHackers](https://gbhackers.com/microsoft-edge-vulnerability/)]

| CVE | Score | Type | Impact |
|-----|-------|------|--------|
| CVE-2026-45492 | 4.3 | Origin Validation Error | Chained to RCE in current user context |
| CVE-2026-45494 | 5.0 | UXSS | Script execution across any target domain |
| CVE-2026-45495 | **7.5** | **Directory Traversal → RCE** | Full RCE via feedback log file path handling |

CVE-2026-45495 is the most severe — a directory traversal in Edge's feedback log handling that, combined with the other flaws, enables full arbitrary code execution. Patches available via MSRC. **Action:** Update Edge via `edge://settings/help` immediately on all managed endpoints.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] VerdantBamboo (Chinese APT) Uses BRICKSTORM Malware — 18-Month Dwell Time via Network Appliance Exploitation**

Volexity documented a long-running campaign by **VerdantBamboo** (aka WARP PANDA / UNC5221) that compromised network edge appliances to infiltrate enterprise networks and access Microsoft 365 environments. Discovered during an incident response engagement in September 2025, the operation achieved at least **18 months of persistent access**. [[Cyberpress](https://cyberpress.org/verdantbamboo-targets-network-appliances/); [GBHackers](https://gbhackers.com/chinese-apt-verdantbamboo/)]

**Tradecraft highlights:**
- Initial compromise of an **Egnyte Storage Sync VM** used as proxy to blend traffic and bypass Conditional Access policies
- Compromised the victim's **MSP via pfSense firewall** — established a beachhead that persisted even after primary remediation
- Deployed **BRICKSTORM** malware in Linux and FreeBSD variants, with separate C2 domains for fallback implants (opsec: if primary is blocked, secondary backdoors remain hidden)
- Exploited a sudo misconfiguration on Egnyte for local privilege escalation; used obfuscated BRICKSTORM variant for FreeBSD/pfSense
- When Egnyte was isolated, pivoted to **Synology NAS** using stolen admin credentials (no MFA) and deployed **PLENET** backdoor
- C2 infrastructure consistently used **Cloudflare IP addresses** with distinct TLS certificates

**Recommendation:** Audit network edge appliances (Egnyte, pfSense, Synology NAS) for unauthorized SSH, cron entries, or unexpected outbound connections. Enforce MFA on all administrative accounts — including MSP-managed devices.

---

**[NEW] Triple npm Supply Chain Onslaught — IronWorm, Phantom Gyp (Miasma), and Shai-Hulud Wave Hit Developer Ecosystems in 48 Hours**

Three coordinated or coincident supply-chain campaigns struck npm within hours of each other, collectively compromising **100+ packages** across maintainer accounts with overlapping TTPs indicating an escalating automated attack infrastructure against the software supply chain.

**1. IronWorm (36 packages)** — Rust-based infostealer hiding behind an eBPF kernel rootkit, communicating over Tor. Targets 86 environment variables (OpenAI, AWS, Anthropic, npm credentials) and 20 credential files. Self-propagates via stolen npm Trusted Publishing tokens. Uses GitHub Actions build artifacts as dead-drop exfiltration to avoid C2 infrastructure entirely. Started from compromised account `asteroiddao`. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-ironworm-malware-hits-36-packages-in-npm-supply-chain-attack/); [Cyberpress](https://cyberpress.org/ironworm-targets-developer-secrets/)]

**2. Phantom Gyp / Miasma (57 packages, 286+ versions)** — A new variant of the Miasma worm exploited npm's `binding.gyp` build configuration file to execute code during `npm install` without triggering conventional lifecycle script monitoring. Dubbed **"Phantom Gyp"**, the 157-byte payload weaponizes `node-gyp rebuild` command substitution. The malware deploys the **Bun runtime** to evade Node.js detection, accesses GitHub Actions runner memory to recover masked secrets, and poisons AI coding environments (Claude Code, Cursor, VS Code configs). C2 uses GitHub account `liuende501` (236 repos) as dead-drop storage with beacon keyword `thebeautifulmarchoftime`. [[GBHackers](https://gbhackers.com/dozens-of-npm-packages-via-binding-gyp/); [Cyberpress](https://cyberpress.org/binding-gyp-targets-npm-maintainers/)]

**3. Shai-Hulud Miasma Wave** — Continuing the Red Hat compromise from earlier this week, hundreds of npm packages hit by the Shai-Hulud worm's automated propagation engine. [[Malware.News](https://malware.news/t/new-shai-hulud-miasma-wave-hits-hundreds-of-npm-packages/107591#post_1)]

**Action:** Developers should audit `binding.gyp` files in dependencies, rotate all npm tokens, enable 2FA, and check for GitHub commit authors named `claude` with impossible timestamps (13 years ago) — a tell for IronWorm compromise. Monitor for unexpected `node-gyp rebuild` invocations during install.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] DentaQuest Data Breach — 2.6 Million Accounts Exposed, ShinyHunters Leaks Data**

The dental benefits administrator DentaQuest confirmed a breach that exposed sensitive data of **2.6 million accounts** after the ShinyHunters extortion group leaked 234 GB of stolen data. Compromised information includes email addresses, full names, phone numbers, government-issued IDs, health insurance information, and dates of birth. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/dentaquest-data-breach-exposed-info-of-26-million-accounts/)]

The breach came to light when ShinyHunters listed DentaQuest on its data leak site in May. DentaQuest serves 35 million customers across 50 states. ~66% of the exposed records were already present in HIBP from prior breaches. **Action:** Impacted individuals face elevated risk of targeted phishing and social engineering using health insurance and PII data.

---

**[NEW] VECT 2.0 Ransomware — Implementation Bugs Corrupt Files Beyond Attacker's Own Recovery**

Morphisec analysis reveals that VECT 2.0 ransomware's Windows implementation contains critical coding errors that often permanently corrupt files, making decryption impossible even for the attacker. [[GBHackers](https://gbhackers.com/vect-2-0-ransomware-breaks-files/); [Cyberpress](https://cyberpress.org/vect-2-0-corrupts-files/)]

**Key failures:** (1) Nonce-loss bug — for files >128 KB, encrypts four 32 KB blocks with different nonces but writes only the final nonce; (2) Buffer-size mismatch — files between 32-128 KB may be renamed without encryption or partially damaged; (3) Race conditions from shared buffers across concurrent encryption threads produce inconsistent file states. **Impact:** Victims who pay the ransom may still lose data permanently — the attacker's own decryptor cannot handle the chaotic file states left behind. **Action:** Prioritize blocking VECT execution early in the attack chain; do not assume decryption is possible.

---

**[NEW] Hola Browser Supply Chain Compromise — Cryptominer Delivered to Windows Users**

The Windows version of Hola Browser was compromised in a supply chain attack that delivered a Monero cryptocurrency miner (`me.exe`, later renamed `HolaMonitorService.exe`) to ~0.1% of users. Discovered during AppEsteem certification testing by Sophos and Sygnia. The miner adds a Windows Defender exclusion rule and creates an auto-starting service activated when the system is idle. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hola-browser-for-windows-compromised-to-deliver-cryptominer/)]

Hola confirmed the compromise, stating the distribution pipeline has been rebuilt with code-signing verification and tighter access controls. No evidence of user data access was found.

---

## 🛡️ Defense & Detection

**[NEW] Malicious Browser Extensions Target AI Chatbot Conversations — Urban VPN and Others Intercept ChatGPT, Claude, Copilot Data**

GData analysts documented a campaign of malicious Chrome extensions that intercept and exfiltrate conversations from ChatGPT, Claude, Copilot, Gemini, DeepSeek, and other AI platforms. Extensions like **Urban VPN** and **Smart Sidebar: ChatGPT, Claude & DeepSeek** inject JavaScript to capture DOM-rendered chat content, encode it (Base64), and POST it to attacker-controlled endpoints — even when the VPN feature is not active. [[GBHackers](https://gbhackers.com/ai-chatbot-users-targeted/)]

**Defense:** Audit installed extensions, revoke host-wide permissions, deploy extension allowlists via group policy, and monitor for anomalous Base64-encoded outbound traffic following AI-site visits. AI service providers should implement CSP and message-level encryption.

---

**[NEW] Gemini Voice Assistant Hijacked via Fake Context Alignment — Indirect Prompt Injection Through Messaging Notifications**

SafeBreach researchers disclosed a vulnerability in Google's Gemini voice assistant that allowed attackers to hijack the AI via **indirect prompt injections** delivered through ordinary messaging notifications. The attack class, dubbed **Fake Context Alignment**, exploited WhatsApp, Slack, and SMS notifications to embed hidden commands in foreign languages with muted hyperlinks — silently injecting malicious instructions that Gemini processed but did not read aloud. [[SecurityWeek](https://www.securityweek.com/gemini-voice-assistant-hijacked-via-messaging-notifications/)]

**Impact demonstrated:** Smart home control via Google Home, unauthorized Zoom calls, deceptive messaging from trusted contacts, and persistent AI memory poisoning. Google patched the vulnerability in November 2025 with content classifier improvements. SafeBreach published the research now to raise awareness of notification-based prompt injection risks as AI assistants gain deeper device integration.

---

**[NEW] Five Eyes Joint Advisory — Chinese Military Intelligence Recruits Government Staff Via Fake Jobs on LinkedIn, Indeed, Upwork**

The FBI, MI5, ASIO, CSIS, and NZSIS issued a joint advisory detailing how Chinese military intelligence officers use fake job postings for "foreign policy analyst" and "defense analyst" roles to recruit individuals with security clearances or government access. The six-stage chain: fake job ad → resume vetting for access → fake interview → trial report on sensitive topics (Indo-Pacific defense, bilateral relations) → escalating demands → payment via PayPal, Zelle, Wise, or crypto (hundreds to thousands per report). [[SecurityWeek](https://www.securityweek.com/five-eyes-chinese-spies-target-government-military-staff-with-fake-job-opportunities/)]

**Key insight:** Even unclassified information fragments become strategically significant when aggregated. The advisory warns individuals in the defense ecosystem — including contractors, academics, and journalists — to watch for suspicious recruitment approaches.

---

**[NEW] MCP Servers: The New Unmanaged API — Palo Alto Networks Maps the AI Agent Attack Surface**

Palo Alto Networks published a comprehensive analysis of Model Context Protocol (MCP) server security, arguing that MCP servers are replicating the shadow API problem that took security teams a decade to solve — but at AI deployment speed. Key risks: (1) MCP servers run as processes with elevated, often over-provisioned credentials; (2) the MCP specification doesn't mandate client authentication at the transport layer; (3) prompt injection via tool results allows attackers to poison RAG pipelines; (4) lateral movement through chained tool calls can cross trust boundaries that individual API calls wouldn't trigger. [[Palo Alto Networks](https://www.paloaltonetworks.com/blog/cloud-security/mcp-servers-ai-attack-surface-security/)]

**Recommendation:** Build an MCP security program in three phases: discovery (inventory every server, map its credentials and resource access), policy (scoped service identities, no personal access tokens in production), and runtime detection (monitor for cross-boundary tool-call chains).

---

## 📋 Policy & Industry News

**[NEW] Zapocalypse — Five Known Anti-Patterns Chained into Full Zapier Account Takeover**

Token Security researchers disclosed how five individually known security weaknesses — a sandbox with `os.system`, orphaned STS credentials in `/proc/self/mem`, an IAM role named `allow_nothing_role` that permitted full ECR read, an NPM publish token with `bypass_2fa: true` leaked in Docker image history, and publish rights to a frontend package — composed across Zapier's infrastructure to enable platform-wide account takeover. Reported February 12, fully remediated by March 5, 2026. [[Token Security](https://www.token.security/blog/zapocalypse-the-attack-chain-that-could-have-hijacked-zapier); [tl;dr sec #331](https://tldrsec.com/p/tldr-sec-331)]

**Takeaway for defenders:** The vulnerability was the composition across teams that each secured their component in isolation. Lambda sandbox, ECR/IAM, CI token management, and NPM publishing — each owned by a different group, each reasonable in isolation, catastrophic in combination.

---

## ⚡ Quick Hits

- **New SHub Stealer "Reaper" variant for macOS** — Blended stealer with AMOS-style file grabbing, crypto wallet modification (Exodus, Atomic, Ledger Live), and hidden backdoor via fake WeChat/Miro download pages using Script Editor ClickFix. Aborts if keyboard language is set to Russian. [[GBHackers](https://gbhackers.com/new-shub-stealer-variant/)]
- **Credit card theft campaign abuses Stripe as storage backend** — Magecart skimmer operating since December 2025 loads malicious code from Google Tag Manager containers, exfiltrates stolen card data to Stripe customer records (fake `cus_*` objects). Sansec discovered a Firestore-based variant using `braintree-payment-app` project to blend in with payment traffic. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/credit-card-theft-campaign-abuses-stripe-to-host-stolen-payment-info/)]
- **Fake Ghidra, dnSpy, SpiderFoot sites spread SessionGate malware** — 100+ active impersonation domains route security researchers through TDS to infostealers (RemusStealer, AnimateClipper) and a new multi-stage loader framework. "Top Google result + official-looking website" is no longer a reliable safety signal. [[GBHackers](https://gbhackers.com/fake-ghidra-dnspy-spiderfoot-sites/)]
- **WSL2 payload staging creates Sysmon blind spot** — Daniel Koifman demonstrates that WSL2's Hyper-V network stack is invisible to Windows Sysmon (no Event ID 3), and file writes via `/mnt/c/` are attributed to `DllHost.exe` with no attacker process chain. Sigma rule provided for detection via `DllHost.exe` + dangerous extensions in user-writable directories. [[Malware.News](https://malware.news/t/the-interesting-case-of-wsl-for-payload-staging/107607#post_1)]
- **Let's Encrypt adopts Merkle Tree Certificates for post-quantum TLS** — Targeting staging by late 2026 and production rollout in 2027, following Google's MTC initiative earlier this year. [[Cyberpress](https://cyberpress.org/lets-encrypt-merkle-tree-certificates/)]
- **AI-powered autonomous worm demonstrated in lab** — Canadian researchers published a preprint showing an LLM-driven worm that autonomously compromised 73.8% of a 33-host heterogeneous network across 15 trials, achieving up to 7 generations of self-replication and exploiting post-training-cutoff vulnerabilities (April-May 2026) by ingesting advisory text at runtime. [[Cyberpress](https://cyberpress.org/ai-powered-worm-linux-windows/); [GBHackers](https://gbhackers.com/ai-powered-worm-leverages-stolen-compute-devices/)]

---

*91 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — old.reddit.com inaccessible. tl;dr sec #331 checked (Friday, highest-value window). Prior digests: June 1–4, 2026. Sources include BleepingComputer, SecurityWeek, GBHackers, Cyber Security News (Cyberpress), Malware.News (JFrog, Morphisec, SentinelOne, Volexity), Palo Alto Networks, SafeBreach, Token Security, GData, Marcus Hutchins (MalwareTech), and independent researchers.*
