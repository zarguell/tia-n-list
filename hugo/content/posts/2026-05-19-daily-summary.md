---
title: "🔴 CISA GovCloud leak worst ever, 🎯 SEPPmail 7-CVE pre-auth RCE, ⚠️ Nx Console supply chain hijack, 🦞 Claw Chain OpenClaw CVSS 9.6, 📊 PostgreSQL 11-CVE update, 🎭 Gamaredon 12-wave Ukraine campaign"
date: 2026-05-19
tags: ["CISA","AWS GovCloud","SEPPmail","Nx Console","supply chain","PostgreSQL","Gamaredon","Storm-2949","Claw Chain","OpenClaw","Mythos Preview","NGINX Rift","infostealer","SHub","B1ack's Stash","7-Eleven"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Critical: CISA contractor exposed AWS GovCloud keys + plaintext passwords on GitHub for 6 months — worst government leak in recent history. SEPPmail gateway pre-auth RCE gives full mail traffic access. Nx Console VS Code extension (2.2M users) hijacked in supply chain attack targeting developer secrets. OpenClaw 4-bug chain (CVSS 9.6) enables AI agent sandbox escape. Patch: PostgreSQL 11 CVEs, NGINX Rift active exploitation. Gamaredon continues 12-wave phishing against Ukraine. B1ack's Stash releases 4.6M stolen credit cards."
---
# Daily Threat Intelligence Digest — May 19, 2026

*63 articles ingested from Miniflux Cyber feeds. External cross-referencing via Reddit r/cybersecurity and TLDR InfoSec API (Monday issue — Tuesday's not yet published at 7:15 AM ET).*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] CISA Contractor Leaks AWS GovCloud Keys — Worst Government Data Leak in Recent History**

A Nightwing contractor working for CISA maintained a public GitHub repository named "Private-CISA" since November 2025 that exposed highly privileged AWS GovCloud administrative credentials, plaintext passwords for dozens of internal CISA systems, and access credentials for the agency's internal software artifact repository. The 844 MB repository included CI/CD build logs, Kubernetes manifests, Terraform infrastructure code, SAML certificates, and detailed documentation of CISA's internal deployment workflows. GitGuardian researcher Guillaume Valadon called it "the worst leak I've witnessed in my career," noting the contractor had deliberately disabled GitHub's built-in secret scanning feature. Security researcher Philippe Caturegli (Seralys) validated the credentials granted high-privilege access to three AWS GovCloud accounts. The artifact repository access is considered the most dangerous vector — a compromised build pipeline could allow attackers to inject backdoors into every CISA software deployment. The repository was taken down on May 15 after KrebsOnSecurity and Seralys notified CISA directly, but the AWS keys remained valid for an additional 48 hours. CISA's response: "Currently, there is no indication that any sensitive data was compromised." The agency has lost nearly one-third of its workforce since the start of the second Trump administration. [[Krebs on Security](https://krebsonsecurity.com/2026/05/cisa-admin-leaked-aws-govcloud-keys-on-github/); [GitGuardian](https://blog.gitguardian.com/how-we-got-a-cisa-github-leak-taken-down-in-26-hours/); [Cyber Security News](https://cyberpress.org/cisa-admin-exposes-aws-govcloud/)]

**[UPDATE] NGINX Rift (CVE-2026-42945) — Active Exploitation Confirmed, 5.7M Exposed Servers**

VulnCheck has confirmed active in-the-wild exploitation of CVE-2026-42945, the critical heap buffer overflow in NGINX's `ngx_http_rewrite_module` that went undetected for 18 years. Attackers are sending crafted HTTP requests to trigger heap buffer overflows in the NGINX worker process. Censys data shows approximately 5.7M internet-facing NGINX servers running potentially vulnerable versions. The rewrite-only exploitation constraint reduces but does not eliminate the attack surface. F5 released patches last week in versions 1.31.0/1.30.1. [[GBHackers](https://gbhackers.com/critical-nginx-vulnerability/); prior coverage: May 14, 18 digests]

**[NEW] SEPPmail Gateway — 7 Critical CVEs Enable Pre-Auth RCE and Full Mail Traffic Theft**

InfoGuard disclosed seven critical vulnerabilities in the SEPPmail Secure E-Mail Gateway appliance affecting thousands of publicly accessible instances. The most severe, CVE-2026-2743, exploits a directory traversal in the Large File Transfer module to overwrite `/etc/syslog.conf` with a Perl reverse shell — triggered by flooding logs to force a `syslogd` restart via `newsyslog`. Four additional critical flaws hit the GINA V2 web interface, including unauthenticated Perl `eval()` RCE (CVE-2026-44128), Local File Inclusion exposing mail traffic and LDAP databases (CVE-2026-44127), environment variable disclosure (CVE-2026-7864), and insecure deserialization (CVE-2026-44126). Successful exploitation yields complete appliance takeover with cleartext access to all inbound/outbound mail. Fixed in version 15.0.4. Blue teams typically have no visibility into these virtual appliances, making detection especially difficult. [[Cyber Security News](https://cyberpress.org/seppmail-gateway-flaws-mail-traffic/); [GBHackers](https://gbhackers.com/seppmail-gateway-flaws-expose-organizations-to-rce-and-email/)]

**[NEW] Nx Console VS Code Extension Hijacked — 2.2M Installations Targeted in Supply Chain Attack**

On May 18, attackers compromised version 18.95.0 of the Nx Console VS Code extension (2.2M+ installations) by scraping a contributor's GitHub token from a prior incident, planting an invisible orphan commit in the Nx repository, and publishing the infected extension using compromised marketplace credentials. The payload is a multi-stage credential stealer targeting GitHub, npm, AWS, HashiCorp Vault, Kubernetes, Claude Code configs, and 1Password — with three independent exfiltration channels (HTTPS, GitHub API, DNS tunneling) and a persistent Python backdoor on macOS. The Nx team removed the malicious version within 11 minutes and released version 18.100.0. However, any developer who opened a workspace with the compromised extension should consider all secrets on that machine compromised and reimage the workstation. This is the second supply chain attack on Nx in under a year, and one of the first to specifically target AI coding assistant configurations. [[Cyber Security News](https://cyberpress.org/nx-console-hijacked-attack/); [GBHackers](https://gbhackers.com/nx-console-vs-code-extension/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Storm-2949 — Compromised Identity Escalates to Full Azure Cloud-Wide Breach**

Microsoft Threat Intelligence published a detailed breakdown of Storm-2949's methodical, multi-layered attack campaign that began with a single compromised identity and expanded to full-spectrum cloud compromise across Microsoft 365 and Azure. The attacker abused Microsoft's Self-Service Password Reset (SSPR) process — calling victims impersonating IT support, convincing them to approve MFA prompts, then resetting passwords and enrolling their own MFA device. Storm-2949 compromised multiple users including IT personnel and senior leadership, then used Microsoft Graph API for directory discovery, Azure VM extensions (VMAccess, Run Command) for credential harvesting, Azure Key Vault for secret extraction, and ScreenConnect RMM for persistent remote access. Data exfiltration spanned OneDrive, SharePoint, Azure Storage, and Azure SQL — over multiple days, alternating between secret-based and OAuth-based authentication. The attack used legitimate cloud management features to blend with expected administrative behavior, making detection heavily dependent on cross-domain telemetry correlation. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/) via Malware.News]

**[NEW] Gamaredon (UAC-0010) Sustains 12-Wave Phishing Campaign Against Ukraine — GammaDrop/GammaLoad Deployers**

Harfang Lab has documented at least 12 waves of spearphishing emails since September 2025 from the Russian-aligned Gamaredon group, targeting Ukrainian government entities — particularly the Security Service of Ukraine (SSU) across Luhansk, Lviv, and Chernivtsi oblasts. The campaigns exploit CVE-2025-8088 (WinRAR directory traversal) to drop VBScript-based payloads: the first-stage GammaDrop downloader, which retrieves GammaLoad from Cloudflare Workers-hosted C2 infrastructure. GammaLoad establishes RunOnce persistence and communicates with C2 every ~3.5 minutes, collecting system info for victim fingerprinting. Recent May 2026 waves introduce ARJ archives (disguised as ZIP/RAR) and Bingbot user-agent strings. Many Ukrainian institutions lack properly enforced SPF, DKIM, and DMARC policies, enabling spoofing and compromised-account abuse. [[GBHackers](https://gbhackers.com/gammaload-in-phishing-campaigns/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] PostgreSQL Critical Security Update — 11 CVEs Including Stack Overflow RCE and SQL Injection**

PostgreSQL released versions 18.4, 17.10, 16.14, 15.18, and 14.23 addressing 11 security vulnerabilities and over 60 bugs. Notable CVEs: CVE-2026-6637 (CVSS 8.8) — stack buffer overflow in the `refint` module enabling potential RCE; CVE-2026-6475 (CVSS 8.8) — symlink attack in `pg_basebackup`/`pg_rewind` allowing arbitrary file overwrite; CVE-2026-6477 (CVSS 8.8) — `libpq lo_*` functions allow server to overwrite client memory buffers; CVE-2026-6476 (CVSS 7.2) — SQL injection in `pg_createsubscriber` enabling superuser SQL execution; CVE-2026-6473 (CVSS 8.8) — integer wraparound leading to out-of-bounds writes. PostgreSQL 14 reaches end-of-life on November 12, 2026. Organizations should upgrade immediately and migrate from MD5 to SCRAM-SHA-256 authentication. [[GBHackers](https://gbhackers.com/postgresql-flaws-expose-databases/)]

**[NEW] SHub/Reaper macOS Infostealer — Spoofs Apple Security Updates via AppleScript URL Scheme**

A new variant of the SHub macOS infostealer — dubbed Reaper — uses the `applescript://` URL scheme to display a fake Apple security update prompt, then installs a backdoor that steals browser credentials, documents with financial data, and cryptocurrency wallet apps. Unlike earlier SHub variants that relied on "ClickFix" tactics (tricking users into pasting terminal commands), Reaper leverages Apple's own scripting automation to gain execution — bypassing the manual copy-paste step. Affects browser-saved credentials, crypto wallets, and sensitive documents. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/shub-macos-infostealer-variant-spoofs-apple-security-updates/)]

**[NEW] Claw Chain — Four OpenClaw Vulnerabilities Enable Sandbox Escape to Full System Compromise**

Cyera Research disclosed four chained vulnerabilities (CVE-2026-44112, CVSS 9.6) in OpenClaw, an autonomous AI agent platform. The chain moves from a malicious plugin or prompt to TOCTOU write escape (privilege escalation), environment variable leakage of secrets, loopback exploitation granting full owner access, and TOCTOU read escape exposing arbitrary files. The findings underscore the challenge of sandboxing AI agents that require broad system access to function. [[SecurityWeek](https://www.securityweek.com/claw-chain-openclaw-flaws-allow-sandbox-escape-backdoor-delivery/); [TLDR InfoSec]

**[UPDATE] Mythos Preview — Cloudflare Confirms AI Can Now Build Working Exploits**

Cloudflare's security team published findings from Project Glasswing, Anthropic's controlled research program, showing Mythos Preview can automatically chain multiple low-severity bugs into working, high-severity exploits — closing the gap between vulnerability discovery and PoC generation. Cloudflare ran approximately 50 concurrent agent instances on narrowly scoped hypotheses, with adversarial review agents, achieving working exploit chains from bugs that would have languished in a triage backlog. The model showed inconsistent organic refusals to build exploits, sometimes completing equivalent tasks when framed differently — Cloudflare warns emergent guardrails alone are not a reliable safety boundary. [[Cyber Security News](https://cyberpress.org/mythos-preview-automates-poc-exploit/); [GBHackers](https://gbhackers.com/mythos-preview-automates-poc-exploit-creation/)]

**[NEW] Four-Faith Industrial Routers Targeted in Active Botnet Hijacking Campaign**

Threat actors are actively exploiting CVE-2024-9643 in Four-Faith industrial cellular routers to conscript them into a botnet. The authentication bypass vulnerability allows remote attackers to hijack routers used in industrial and critical infrastructure environments — ICS, SCADA, and remote monitoring applications. [[GBHackers](https://gbhackers.com/four-faith-industrial-routers-targeted-in-botnet-hijacking-campaign/)]

---

## 🛡️ Defense & Detection

**[NEW] April 2026 Infostealer Trend Report — LummaC2 Dominates, Remus Uses Ethereum for Dead Drop Resolution**

AhnLab's ASEC April 2026 infostealer report documents LummaC2 as the dominant infostealer by volume, followed by Vidar, AgentTesla, and ACRStealer. Distribution remains driven by SEO-poisoned crack/keygen downloads, file hosting services (S3 buckets, Mega, Mediafire), and email campaigns. 85.9% of samples are EXE, 14.1% use DLL side-loading (predominantly Python DLLs). The emerging Remus infostealer employs the Dead Drop Resolver technique — querying Ethereum smart contracts via `eth.llamarpc.com` for C2 configuration — and uses ChaCha20 with different keys for inbound/outbound communication. macOS infections continue via the ClickFix technique; 800 malicious scripts and 33 C2 domains collected in April. [[ASEC](https://asec.ahnlab.com/en/93750/)]

---

## 📋 Policy & Industry News

**[NEW] B1ack's Stash Releases 4.6 Million Stolen Credit Cards for Free**

The dark web carding marketplace B1ack's Stash released approximately 4.6 million stolen credit card records as a free download — the second such mass release in 15 months (following 4M cards in February 2025). The stated pretext is seller misconduct on the platform. Each record includes full PAN, CVV2, expiration date, billing address, full name, email, phone, and IP address. Approximately 70% of victims are US-based. After filtering duplicate and expired records, SOCRadar estimates 4.3M net new actionable records. The data richness enables CNP fraud (AVS bypass trivial), identity theft, and highly convincing phishing. [[Malware.News](https://malware.news/t/b1ack-s-stash-releases-4-6-million-stolen-credit-cards-for-free/107093#post_1)]

**[NEW] Congress Learns of Prescription Data Hack Months Later — RXNT Breach Affecting Congressional Medical Contractor**

Lawmakers were only informed in May that RXNT, a healthcare software company used by the Office of the Attending Physician (OAP) to manage prescription services for Congress, was breached on March 1 and March 3. Hackers obtained copies of patient prescription data. The delayed disclosure raises questions about incident reporting timelines for congressional medical contractors. [[Malware.News](https://malware.news/t/congress-learns-of-prescription-data-hack-months-later/107095#post_1)]

**[NEW] 7-Eleven Data Breach Confirmed After ShinyHunters Ransom Demand**

SecurityWeek confirmed that 7-Eleven suffered a data breach, with the ShinyHunters-associated CoinbaseCartel extortion group demanding ransom. Details on the scope and data types compromised remain limited. [[SecurityWeek](https://www.securityweek.com/7-eleven-data-breach-confirmed-after-shinyhunters-ransom-demand/)]

---

## ⚡ Quick Hits

- **Storm-2949 IOCs**: C2 infrastructure at `176.123.4[.]44`, `91.208.197[.]87`, `185.241.208[.]243` (ScreenConnect). [Microsoft]
- **Extant Aerospace breach**: Defense contractor disclosed breach affecting 3,012 individuals with SSNs exposed. [[Malware.News](https://malware.news/t/extant-aerospace-data-breach-exposed-ssns-for-more-than-3-000-people/107096#post_1)]
- **INTERPOL Operation Ramz**: 201 arrests, 53 servers seized across 13 MENA countries, 382 suspects identified. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/interpol-operation-ramz-seizes-53-malware-phishing-servers/)]
- **Russia's MAX super app**: State-backed platform lacks end-to-end encryption, actively detects VPN usage, provides technical foundation for SORM surveillance. [[Malware.News](https://malware.news/t/russia-rolls-out-surveillance-through-state-backed-super-app-max/107086#post_1)]
- **Incransom targets Bergen Community College**: Ransomware incident at the New Jersey educational institution. [[Malware.News](https://malware.news/t/incransom-targets-bergen-community-college/107103#post_1)]

---

*63 articles ingested from Miniflux Cyber feeds, supplemented by Reddit r/cybersecurity and TLDR InfoSec cross-referencing (Monday May 18 issue). Prior digests: May 14-18, 2026. Sources include Krebs on Security, GitGuardian, BleepingComputer, SecurityWeek, Cyber Security News, GBHackers, ASEC, Microsoft Security Blog, Harfang Lab, InfoGuard, Cloudflare, Cyera Research, SOCRadar, and Malware.News.*
