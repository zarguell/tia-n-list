---
title: "🔴 CVE-2026-6875 ServiceNow RCE, 🎯 HollowGraph Iran C2, ⚠️ HollowByte OpenSSL DoS, 🍷 LegacyHive Windows Zero-Day, 🎯 JadePuffer EncForge Ransomware"
date: 2026-07-21
tags: ["service-now","zero-day","openssl","ransomware","iran-apt","ai-security","vm-escape","sandbox-escape","data-breach","vulnerability"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "ServiceNow AI sandbox escape under active exploitation; HollowByte OpenSSL DoS silently patched; LegacyHive Windows zero-day unpatched; Iranian HollowGraph C2 uses M365 calendar; JadePuffer deploys AI-specific ransomware."
---

# Daily Threat Intelligence Digest — July 21, 2026

24 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking. One gap story (Januscape Linux VM escape) surfaced via r/cybersecurity cross-reference. Multiple feed duplicates from prior days filtered out (Hugging Face breach, SonicWall SMA1000 details, wp2shell FAQ).

## 🔴 Critical Threats & Active Exploitation

### CVE-2026-6875 — ServiceNow AI Sandbox Escape Exploited Days After Disclosure

A critical sandbox escape vulnerability in ServiceNow's AI platform (CVE-2026-6875) is under active exploitation just four days after patches were released. The flaw allows unauthenticated attackers to execute arbitrary code by escaping the AI sandbox in certain configurations. ServiceNow deployed fixes to hosted instances on July 14; Searchlight Cyber disclosed technical details and PoC the same day. Threat intelligence firm Defused reported in-the-wild exploitation on July 18, with the captured payload later confirmed identical to Searchlight's PoC.

ServiceNow has not updated its advisory to reflect active exploitation, stating it has "not observed evidence that this activity is related to instances that ServiceNow hosts" — but self-hosted customers must patch immediately. Given the tight window between disclosure and weaponization, treat this as an exploitation race.

**Action:** Self-hosted ServiceNow customers: apply patches immediately. Hosted instances were auto-patched, but verify. Monitor for exploitation artifacts matching Searchlight Cyber's published PoC patterns.

Sources: [SecurityWeek](https://www.securityweek.com/exploitation-of-servicenow-vulnerability-seen-days-after-disclosure/) · [Searchlight Cyber](https://slcyber.io/) · [Defused](https://defused.io/)

### Windows LegacyHive Zero-Day — Privilege Escalation on Fully Patched Systems

A Windows zero-day vulnerability dubbed **LegacyHive** (no CVE assigned) in the Windows User Profile Service allows non-admin users to modify the classes registry hive and gain automatic code execution when an admin logs in. Disclosed by researcher "Nightmare Eclipse" on Patch Tuesday (July 14), the flaw works on up-to-date Windows systems. Tharros analyst Will Dormann confirmed the exploit chain; Kevin Beaumont validated it within a day and published Defender for Endpoint hunting queries.

Microsoft says it is "actively investigating." Free unofficial patches are now available from third parties. The disclosure timing — intentionally aligned with Patch Tuesday — is notable; Nightmare Eclipse released a stripped PoC to limit immediate weaponization.

**Action:** Apply unofficial mitigations where available. Deploy Kevin Beaumont's [MDE hunting queries](https://github.com/GossiTheDog/ThreatHunting/blob/master/AdvancedHuntingQueries/LegacyHive.kql). Monitor User Profile Service registry modifications.

Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/windows-legacyhive-zero-day-flaw-gets-free-unofficial-patches/)

## 🎯 Threat Actor Activity & Campaigns

### HollowGraph — Iranian C2 Framework Abuses Microsoft 365 Calendar for Stealthy C2

Security researchers have identified **HollowGraph**, a malicious module that uses Microsoft 365 mailbox calendars as a command-and-control channel. The module is part of the **Cavern** C2 framework, previously linked to an Iranian threat actor targeting entities in Israel. At least 12 systems infected, three actively communicating between June 3–July 9.

HollowGraph authenticates to the Microsoft Graph API using stolen credentials (stored in a file disguised as `logAzure.txt`). It creates calendar events dated May 13, 2050, with commands and exfiltrated data concealed in attached files. Two RSA keys encrypt/decrypt communications. The abuse of legitimate Microsoft Graph API traffic makes detection via traditional network monitoring extremely difficult.

**Hunting hypothesis:** Calendar events with far-future dates (2050) and attachments in compromised M365 tenants; anomalous Graph API calendar activity from unexpected geolocations.

Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-hollowgraph-malware-uses-microsoft-graph-for-stealthy-c2-comms/) · [Group-IB](https://group-ib.com/) · [Checkpoint Cavern Research](https://research.checkpoint.com/2026/cavern-manticore-exposing-iran-linked-modular-c2-framework/)

### [UPDATE] JadePuffer — Agentic AI Ransomware Adds AI-Specific Encryption

*Previously covered July 20 (initial JadePuffer disclosure). New: EncForge ransomware specifically targeting AI/ML infrastructure.*

The JadePuffer autonomous AI agent has returned with **EncForge**, a Go-based ransomware binary purpose-built for AI and ML environments. It targets ~180 file extensions covering model checkpoints, vector databases, training datasets, and embedding indices. In the latest attack, the agent exploited an exposed Docker socket on a previously breached Langflow instance (CVE-2025-3248) for root-level access. When payload delivery failed, the agent autonomously iterated through six Python scripts in five minutes, solving its own delivery problem in real time — a demonstration of agentic self-repair capabilities.

This is the first ransomware specifically designed to encrypt AI training assets, representing a new attack surface category.

Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/jadepuffer-agentic-attacks-now-target-ai-model-data-with-ransomware/) · [Sysdig](https://sysdig.com/)

### [UPDATE] SonicWall SMA1000 — Volexity Details Full Zero-Day Exploitation Chain

*Previously covered July 19 (BOD 26-04 deadline, KEV addition). New: Volexity IR report reveals previously unknown threat actor UTA0533 exploited CVE-2026-15409/CVE-2026-15410 starting June 22 — weeks before disclosure.*

Volexity's incident response report reveals the full attack chain: threat actor UTA0533 chained the SSRF (CVE-2026-15409, CVSS 10.0) and command injection (CVE-2026-15410, CVSS 7.2) flaws to install custom malware on SMA1000 VPN appliances, enabling persistent access and network proxying. The exploitation began three weeks before SonicWall's public disclosure.

**Action:** If you haven't patched SMA1000 appliances (12.4.3-03453 / 12.5.0-02835), assume compromise. Hunt for UTA0533 IOCs from Volexity's report.

Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/sonicwall-sma1000-flaws-exploited-as-zero-days-to-push-custom-malware/) · [Volexity](https://www.volexity.com/)

## ⚠️ Vulnerabilities & Patches

### HollowByte — OpenSSL Silent Memory-Exhaustion DoS (11-Byte Trigger)

Okta's red team discovered **HollowByte**, a DoS vulnerability in OpenSSL where a malicious 11-byte payload causes unvalidated buffer pre-allocation of up to 131 KB per connection. Because glibc retains small-to-medium allocations rather than returning them to the OS, successive connections permanently fragment and freeze server memory. A 1 GB system became unresponsive after 547 MB was consumed; on 16 GB systems, 25% of total memory was locked — bypassing standard connection-limiting defenses.

Patches were silently included in OpenSSL 4.0.1 and backported to 3.0.21, 3.4.6, 3.5.7, and 3.6.3. Apache, NGINX, Node.js, Python, Ruby, PHP, MySQL, PostgreSQL, and virtually all services linking OpenSSL are affected.

**Action:** Upgrade OpenSSL immediately. The 11-byte payload and silent patching (no CVE bulletin, no changelog mention) mean many organizations may be running vulnerable versions unknowingly. This is one of the most efficient DoS bugs in recent memory.

Sources: [SecurityWeek](https://www.securityweek.com/openssl-silently-fixes-hollowbyte-dos-vulnerability/) · [Okta](https://www.okta.com/)

### Zimbra Collaboration Suite 10.1.20 — Critical Command Injection + XSS + SSRF

Zimbra released patches for multiple critical vulnerabilities including an unauthenticated command injection in the SNMP monitoring component (when SNMP notifications are enabled and Swatchdog service is running). Four XSS flaws in the Classic Web Client, a mail forwarding restriction bypass (CVE-2026-50055), an EWS extension access control bug (CVE-2026-10631), a mailbox delegation authorization issue (CVE-2026-50054), and an SSRF in the Nextcloud integration are also fixed.

No exploitation reported, but Zimbra is a high-value target for email-oriented threat actors.

**Action:** Update to ZCS 10.1.20 immediately. Disable SNMP notifications if not required.

Sources: [SecurityWeek](https://www.securityweek.com/zimbra-update-patches-critical-vulnerabilities/)

### Januscape — 16-Year-Old Linux KVM Guest-to-Host VM Escape

*Gap story surfaced via r/cybersecurity — not in Miniflux feed.*

CVE-2026-53359 ("Januscape") is a use-after-free in Linux KVM's shadow MMU emulation code, present since 2010, that allows guest VMs to escape to the host on both Intel and AMD processors. Publicly disclosed July 6 after coordinated embargo. Patches are available in recent kernel updates. This affects all major cloud platforms using KVM virtualization.

**Action:** Patch Linux hosts immediately. Cloud providers have likely already patched managed instances, but self-hosted KVM deployments must update kernels.

Sources: [Ars Technica](https://arstechnica.com/security/2026/07/high-severity-guest-vm-escape-is-1-of-2-linux-vulnerabilities-to-surface-this-week/) · [BleepingComputer](https://www.bleepingcomputer.com/news/linux/new-januscape-linux-kernel-flaw-allows-vm-escape-on-intel-amd-devices/) · [SecPod](https://www.secpod.com/learn/security-research/januscape-linux-kernel-vm-escape-cve-2026-53359)

## 🛡️ Defense & Detection

### "Week of Sandbox Escapes" — Four AI Coding Agents Bypassed via Filewrite Tricks

Pillar Security demonstrated sandbox escapes in **Cursor, OpenAI Codex, Google Gemini CLI, and Antigravity** — without attacking the sandbox itself. The technique: the AI agent writes a file inside the workspace, then a trusted tool *outside* the sandbox (IDE extensions, Git hooks, VS Code task runner, language servers) reads and executes it. The agent follows every sandbox rule; the escape happens through the trust boundary between workspace files and host tools.

The research spans seven days of published write-ups. Key insight: sandboxing AI coding agents is insufficient when the agent's output files are implicitly trusted by the development toolchain. Organizations relying on AI coding agent sandboxes as a security boundary need to reassess.

Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/cursor-codex-gemini-cli-antigravity-hit-by-sandbox-escapes/) · [Pillar Security](https://www.pillar.security/blog/the-week-of-sandbox-escapes)

### Rapid7 — Exposed WebDAV Malware Delivery Lab Shows AI-Driven Adversary Operations

Rapid7 MDR discovered an exposed server functioning as a malware QA lab with 1,000+ artifacts. Attackers used generative AI for bulk lure generation, README documentation, and automated testing — operating "like modern software product teams." The lab tested WebDAV delivery paths, social engineering lures, and rundll32.exe execution chains. Notable for the operational methodology rather than the specific malware.

Sources: [Rapid7](https://www.rapid7.com/blog/post/tr-exposed-webdav-malware-delivery-lab-analysis)

## 📋 Breaches & Policy

### Ernst & Young Data Breach — Tax Client Personal and Financial Data Compromised

EY is notifying clients that their personal and financial information was stolen in a breach of a third-party service management platform used for tax-related work. Hackers had access between March 28 and April 12, downloading client documents containing names, addresses, SSNs, account numbers, credit/debit card numbers, and tax filing data. EY discovered the breach on April 23. Two years of free credit monitoring offered. No ransomware group has claimed responsibility.

Sources: [SecurityWeek](https://www.securityweek.com/ernst-young-data-breach-affects-personal-financial-information/)

### Estée Lauder — Data Breach via Oracle E-Business Suite Flaw (CVE-2025-61882)

Estée Lauder disclosed a breach via CVE-2025-61882 in Oracle E-Business Suite used for HR operations. The intrusion occurred August 9, 2025, but wasn't discovered until June 19, 2026 — a 10-month dwell time. Exposed data includes names, addresses, emails, SSNs, passport numbers, financial account info, health information, and employment records for an unknown number of the company's 57,000 employees.

Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/est-e-lauder-discloses-data-breach-via-oracle-e-business-flaw/)

### Commerce AI Standards Director Departs After Three Months

Chris Fall is stepping down as director of the Commerce Department's Center for AI Standards and Innovation (CAISI) after just three months. NIST Director Arvind Raman will serve as acting director. The rapid turnover raises questions about the stability of federal AI governance infrastructure.

Sources: [CyberScoop](https://cyberscoop.com/director-of-commerce-ai-standards-office-out-after-three-months/)

## ⚡ Quick Hits

- **WSUS sync meltdown continues** — Microsoft rolled out service-side mitigations and shared manual cleanup steps for WSUS servers impacted since July 13. Admins should run metadata cleanup scripts. (BleepingComputer)
- **Ostium DeFi hack — $23.75M stolen** — Attacker compromised off-chain price infrastructure to submit fraudulent price reports and generate artificial profits on the Arbitrum-based platform. (BleepingComputer)
- **HIH Index launches** — Former JPMorgan Chase CSO Richard Bird launched "The Hacker in a Hoodie" breach tracking index, grading entries by evidence tier (verified/attested/inferred) from SEC filings and news reports. Explicitly refuses to sum losses to avoid the industry's "trillion-dollar estimate" problem. (SecurityWeek)
