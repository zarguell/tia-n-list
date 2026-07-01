---
title: 🔴 Azure CLI Password Spray, Adobe 7 Critical Patches, 🎯 CitrixBleed Returns, Quebec Water Hack, 🛡️ Phantom Squatting
date: 2026-07-01
tags: ["Azure CLI","password spray","Adobe ColdFusion","CVE-2026-48276","Citrix NetScaler","CVE-2026-8451","CitrixBleed","BlueHammer","CVE-2026-33825","Oracle EBS","Quebec water plant","OT security","Phantom Squatting","AI security","BioShocking","PyPI supply chain","Operation Navy Ghost","Aflac","data breach","quantum-safe","PQC","CISA KEV","ANCHOR-CI","DHS"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Active password spray campaign targeting Azure CLI bypasses MFA via deprecated OAuth ROPC flow; Adobe patches 7 max-severity ColdFusion and Campaign flaws (Priority 1); Citrix NetScaler memory disclosure (CVE-2026-8451) shares root cause with CitrixBleed; Russian NoName group hacked Quebec water treatment plant OT; Unit 42 reveals 250K phantom squatting domains weaponized by adversaries; Aflac Japan breach impacts 4.38M."
---

# Daily Threat Intelligence Digest — July 1, 2026

*31 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking. One critical OT incident gap identified via community cross-reference.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Massive Password Spray Campaign Targeting Azure CLI — 81 Million Login Attempts, ROPC Flow Bypasses MFA**

Huntress observed over **81 million password spray login attempts** between June 12–21 targeting Microsoft 365 environments through the Azure CLI, resulting in **78 compromised accounts across 64 organizations**. Attackers relied on the deprecated **OAuth ROPC (Resource Owner Password Credentials)** flow, which mints tokens without interactive MFA prompts — effectively bypassing MFA configurations not explicitly scoped to cover OAuth flows. [[SecurityWeek](https://www.securityweek.com/massive-password-spray-campaign-targeting-azure-cli/)]

The attacks originated primarily from **AS32167 (LSHIY LLC)**, a Hong Kong/China/New York-based hosting provider. Huntress reports that credential spray volume has increased **155× across its customer base** in the past six months. Eight of the impacted organizations had **no MFA policy at all**. Huntress reported the abuse to LSHIY and received no response. The IPv6 ranges associated with LSHIY-linked ASNs have prior reports of originating from China.

**Recommended action:** Audit OAuth ROPC flow usage in your tenant — it is deprecated in OAuth 2.1. Ensure Conditional Access policies explicitly cover OAuth authentication flows, not just browser-based sign-ins. Review Sign-In logs for ROPC-based authentications from AS32167.

---

**[UPDATE] BlueHammer (CVE-2026-33825) — CISA Confirms Ransomware Gangs Now Exploiting Microsoft Defender LPE**

CISA has updated the Known Exploited Vulnerabilities catalog to confirm that ransomware operators are actively exploiting CVE-2026-33825 (BlueHammer), a privilege escalation flaw in Microsoft Defender that enables local attackers to reach SYSTEM by accessing the Security Account Manager (SAM) database. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-windows-bluehammer-flaw-now-exploited-by-ransomware-gangs/); [SecurityWeek](https://www.securityweek.com/bluehammer-vulnerability-exploited-in-ransomware-attacks/)]

*Previously covered June 30. New today: CISA explicitly calls out ransomware gangs in KEV update. Huntress confirmed hands-on-keyboard exploitation days after the April 2026 Patch Tuesday fix.*

**Recommended action:** Confirm April 2026 Patch Tuesday was applied across all Windows endpoints. BlueHammer is a post-authentication LPE typically chained after initial access — treat any unpatched system as a lateral movement vector.

---

**[UPDATE] Oracle E-Business Suite (CVE-2026-46817) — Active Exploitation Underway**

Threat intelligence firm Defused has confirmed active exploitation of CVE-2026-46817, a critical unauthenticated vulnerability (CVSS 9.8) in the Oracle EBS File Transmission component of Oracle Payments. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-oracle-e-business-suite-flaw-now-exploited-in-attacks/); [SecurityWeek](https://www.securityweek.com/exploitation-of-recent-oracle-e-business-suite-vulnerability-begins/)]

*Previously covered June 30. New today: Defused confirms exploitation in the wild. Shadowserver tracks 450+ exposed EBS instances, nearly 200 in the US.*

**Recommended action:** Apply Oracle May 2026 Critical Patch Update immediately. Remove EBS instances from direct internet exposure where possible.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Russian NoName Group Hacked Quebec Water Treatment Plant — OT Access to Pumps and Chlorine Dosing**

Canada's Communications Security Establishment (CSE) revealed that the pro-Russian hacktivist group **NoName** gained unauthorized access to a Quebec municipality's water treatment plant operational technology systems, giving the ability to manipulate **control pumps and chlorine dosing levels**. [[Yahoo News Canada](https://ca.news.yahoo.com/russian-group-hacked-quebec-water-080005964.html); [The Epoch Times](https://www.theepochtimes.com/world/russia-backed-hackers-gained-access-to-quebec-towns-water-treatment-systems-cyber-agency-6055340)]

The intrusion targeted a small Quebec town's OT environment, marking an escalation in NoName's operational focus from DDoS attacks to direct manipulation of industrial control systems. While CSE did not disclose whether the attackers actually altered chemical dosing, the access achieved — pump and chlorine controls — represents a public safety risk if leveraged offensively. NoName is a Russian state-backed cybercriminal group frequently conducting operations against NATO member states.

**Recommended action:** Water and wastewater utilities should review remote access to OT systems, segment IT/OT networks, and verify that HMI and SCADA access requires multi-factor authentication. Consider CISA's ICS advisory framework for water sector cyber hygiene.

---

**[NEW] Operation Navy Ghost — Trojanized PyPI Packages Target Telegram Bot Developers**

A campaign active since November 2025 has published at least **eight trojanized Pyrogram forks** on PyPI, collectively downloaded over 25,000 times, that backdoor Telegram bot servers. Discovered by Checkmarx, the packages hide a `secret.py` backdoor in the helpers module that registers hidden Telegram command handlers — enabling arbitrary Python code execution and shell commands on the infected server. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/malicious-pypi-packages-give-hackers-control-of-telegram-bot-servers/)]

The backdoor activates only on Telegram bot accounts (typically production servers), giving attackers file read access, credential dumping, chat access, database downloads, and persistent backdoor installation. A hardcoded OWNERS list with Telegram IDs ensures exclusive attacker control. Affected packages include `VLifeGram` (4,150 downloads), `pyrogram-styled` (15,370 downloads), and six others.

**Recommended action:** Check `pip list` or `requirements.txt` for any of the named packages. Rotate all credentials on affected servers and revoke Telegram bot tokens immediately.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Adobe Patches Seven Max-Severity ColdFusion and Campaign Flaws**

Adobe released emergency patches for **seven maximum-severity vulnerabilities** in ColdFusion (six CVEs: CVE-2026-48276, -48277, -48281, -48282, -48316) and Campaign Classic (CVE-2026-48286). All seven are rated **Priority 1** — indicating high risk of targeted exploitation — and can be exploited in low-complexity attacks requiring **no user interaction**. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/adobe-patches-seven-max-severity-coldfusion-campaign-flaws/)]

ColdFusion flaws (affecting versions 2025.9, 2023.20 and earlier) enable unauthenticated **remote code execution**. Campaign Classic flaw affects on-premises instances only (v7.4.3 build 9396 and earlier). Adobe stated it is not aware of active exploitation but tagged all as Priority 1. Concurrently, Adobe CSO Aanchal Gupta announced Adobe will move to **twice-monthly security bulletins** starting July 14.

**Recommended action:** Patch ColdFusion and Campaign Classic instances within 72 hours per Adobe's Priority 1 guidance. Note Adobe's shift to bi-monthly Patch Tuesday schedule.

---

**[NEW] Citrix NetScaler Memory Disclosure Flaw (CVE-2026-8451) — Shares Root Cause with CitrixBleed**

Citrix disclosed **six vulnerabilities** in NetScaler ADC and NetScaler Gateway appliances (CVSS 6.9–8.8), including a high-severity memory disclosure flaw discovered by watchTowr that shares a **root cause with the 2023 CitrixBleed** vulnerability — out-of-bounds memory reads triggered by malformed SAML requests. [[CyberScoop](https://cyberscoop.com/citrix-netscaler-flaw-cve-2026-8451-citrixbleed/); [watchTowr](https://labs.watchtowr.com/citrixbleed-to-infinity-and-beyond-citrix-netscaler-pre-auth-memory-overread-cve-2026-8451/)]

CVE-2026-8451 affects NetScaler appliances configured as SAML identity providers for single sign-on. The bulletin also includes: two memory overflow DoS conditions, an unauthenticated arbitrary file read vulnerability (management interface exposed), a TCP timestamp memory overread, and an HTTP/2 DoS requiring manual configuration. NetScaler has amassed **20+ KEV entries** in three years. No active exploitation confirmed at disclosure time.

**Recommended action:** Patch to latest NetScaler builds. For the HTTP/2 DoS, manually configure the timeout parameter per Citrix guidance even after patching.

---

## 🛡️ Defense & Detection

**[NEW] Phantom Squatting — AI-Hallucinated Domains Weaponized as Supply Chain Attack Vector**

Unit 42 published comprehensive research on **phantom squatting**: LLMs consistently hallucinate web domains for legitimate brands, and adversaries are **pre-registering these nonexistent domains** to intercept AI-generated traffic. Their multi-agent discovery framework analyzed 913 global brands across 685,339 prompts, generating 2.1 million URLs — of which **13,229 were confirmed malicious** and **250,000 hallucinated domains remain unregistered** and available for adversarial registration. [[Unit 42](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/)]

Four real-world detection cases demonstrate proactive detection lead times of **23–51 days** before adversary registration. A standout case — the **Montana Empire phishing kit** — featured an attacker who used an AI coding assistant to build the phishing infrastructure targeting a phantom domain the pipeline had flagged 23 days earlier, demonstrating the complete closed loop from AI-assisted development to AI-hallucinated delivery.

**Key finding:** Phantom domains exploit a **zero-reputation bypass** — at registration, they carry no blocklist history, reputation score, or threat intelligence signal. Traditional URL defenses are structurally blind to them until sufficient malicious telemetry accumulates.

---

**[NEW] BioShocking — Prompt Injection Attack Fools AI Browsers Into Ignoring Safety Guardrails**

LayerX researchers devised a prompt injection attack dubbed **BioShocking** that tricks AI-powered browsers into treating sensitive real-world actions as part of a fictional game scenario, causing them to bypass safety guardrails. Tested against **six agentic browser products** (ChatGPT Atlas, Comet, Fellou, Genspark, Sigma Browser, Claude Chrome plugin), **all six were compromised** — only OpenAI has implemented an effective fix. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-bioshocking-attack-manipulates-ai-browser-into-data-theft/)]

The PoC presents a BioShock-themed puzzle where wrong answers are rewarded, teaching the AI agent that normal rules do not apply. In the final step, the agent is instructed to visit a GitHub repo and exfiltrate credentials — all six agents complied.

---

**[NEW] Microsoft Accelerates Quantum-Safe Roadmap — Critical Products to PQC by 2029**

Microsoft announced it is accelerating its post-quantum cryptography timeline, now targeting **2029 for critical products and services** to transition to quantum-resistant encryption — earlier than previously planned. The company cited advances in quantum research that have "shifted the risk horizon" for cryptographically relevant quantum computers. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-accelerates-quantum-safe-roadmap-as-risks-grow/); [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/06/30/microsoft-advances-quantum-safe-security-as-the-risk-timeline-shifts/)]

Microsoft's Quantum Safe Program priorities: (1) upgrading network cryptography to TLS 1.3 for post-quantum key exchange, (2) building crypto-agility to swap algorithms without redesigning applications, (3) modernizing cryptographic trust chains for code signing, certificates, and updates. The PQC targets are integrated into Microsoft's Secure Future Initiative.

---

## 📋 Policy & Industry News

**[NEW] DHS Unveils ANCHOR-CI to Replace Disbanded Critical Infrastructure Cybersecurity Council**

The Department of Homeland Security launched the **Alliance of National Councils for Homeland Operational Resilience – Critical Infrastructure (ANCHOR-CI)** to replace CIPAC, the federal-private sector information sharing body that was disbanded under former DHS Secretary Kristi Noem. The new council will be **managed by CISA** and exempt from FACA public transparency requirements. [[CyberScoop](https://cyberscoop.com/dhs-anchor-ci-cybersecurity-information-sharing/)]

The restoration addresses a year-long gap during which critical infrastructure owners and operators lost access to federal threat intelligence coordination. New Secretary Markwayne Mullin has been sympathetic to industry concerns. CISA Director will have expanded authority over council membership — a change from CIPAC where the private sector self-governed representation.

---

**[NEW] Aflac Japan Data Breach Exposes 4.38 Million Customers**

Aflac Life Insurance Japan disclosed that attackers accessed its policyholder portal repeatedly between **June 15 and June 25**, exfiltrating personal information of **4.38 million customers** — including names, addresses, phone numbers, dates of birth, and insurance account data. Premium transfer account information for approximately 230,000 people was also compromised. [[SecurityWeek](https://www.securityweek.com/aflac-japan-data-breach-impacts-4-38-million/)]

The incident is confined to Aflac Japan systems and does not affect Aflac's US business. At least five services remain disrupted. No credit card data was exposed. Investigation is ongoing with third-party forensic support.

---

## ⚡ Quick Hits

- **[UPDATE] Anthropic Restores Claude Fable 5 Access** — The Commerce Department has lifted export controls on Claude Fable 5, with access restoration beginning Wednesday. Mythos 5 remains restricted to select companies. This follows the broader administration framework on frontier AI model access reported June 29. [[BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-to-restore-claude-fable-access-on-wednesday/)]

- **[NEW] Google Patches 382 Chrome Vulnerabilities** — Google released a massive cumulative security update for Chrome, addressing 382 vulnerabilities across the browser. No zero-day exploitation has been confirmed at this time. [[SecurityWeek](https://www.securityweek.com/google-patches-382-chrome-vulnerabilities/)]

- **[NEW] Adobe Transitions to Bi-Monthly Security Bulletins** — Starting July 14, Adobe will publish security updates on the **second and fourth Tuesday** of each month, doubling the cadence to accelerate patch delivery. Out-of-band response remains in effect for zero-days. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/adobe-patches-seven-max-severity-coldfusion-campaign-flaws/)]

- **[UPDATE] Fake Perplexity Chrome Extension — Taken Down After Microsoft Disclosure** — The malicious "Search for perplexity ai" extension intercepted browser queries and logged keystroke-level search suggestions. It has been removed from Chrome Web Store. Remainder: audit browser extension inventories for AI-themed impersonation tools. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-perplexity-extension-on-chrome-web-store-tracked-searches/)]
