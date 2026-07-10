---
title: "GigaWiper destructive backdoor, HalluSquatting agentic botnets, CISA KEV additions, Helix vishing group, KDDI 12M breach"
date: 2026-07-10
tags: ["gigawiper","hallusquatting","cisa-kev","helix","forg365","ghostlock","tenda-backdoor","blackcat","shinyhunters","supply-chain","interpol"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "23 articles ingested. Microsoft details GigaWiper destructive backdoor amalgamating Crucio and FlockWiper. CISA adds 4 actively exploited flaws including Langflow CVSS 10.0 to KEV. HalluSquatting technique weaponizes AI hallucinations for botnet delivery. New Helix vishing group targets SharePoint. KDDI breach impacts 12 million. GhostLock 15-year-old Linux kernel flaw disclosed with PoC. Tenda router hardcoded backdoor remains unpatched."
---

# Daily Threat Intelligence Digest — 2026-07-10

23 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] GigaWiper: Destructive Backdoor Stitches Together Crucio Ransomware, FlockWiper Into Single Golang Implant

Microsoft Threat Intelligence published a deep-dive analysis of **GigaWiper**, a sophisticated Golang-based backdoor observed actively since October 2025 that consolidates three independent malware families into a single modular implant. The backdoor communicates via RabbitMQ (C2) and Redis (status updates), persists through scheduled tasks, and provides **20 distinct commands** including disk-level wiping, fake ransomware encryption (keys generated and discarded — no decryption possible), BSOD triggering via boot-file deletion, screen recording, and VNC-style remote control.

**Key architectural finding:** GigaWiper is not a purpose-built tool but an amalgamation. Command 1 embeds a standalone physical-disk wiper (overwrites raw disk, removes partition metadata). Command 3 reimplements **Crucio ransomware** (CISA-advisory-documented, Dec 2023) — encrypts files with random keys that are never saved, renames them `.candy`, drops a wallpaper image. Command 12 reimplements **FlockWiper**, a C-based wiper recoded in Golang with multi-pass secure wiping. PDB paths and function names reference a "GRAT" framework, suggesting an unrecovered parent tooling ecosystem.

C2 infrastructure observed at `185.182.193[.]21` and `212.8.248[.]104`. Microsoft has released Defender detections and IOCs.

**Hunting hypothesis:** Look for scheduled tasks named "OneDrive Update" running every minute, RabbitMQ/Redis traffic from non-standard ports, and `DeviceIoControl` with `IOCTL_DISK_CREATE_DISK` calls — these are the implant's fingerprint for partition-table destruction.

**Sources:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/09/gigawiper-anatomy-of-a-destructive-backdoor-assembled-from-multiple-malware/) | [SecurityWeek](https://www.securityweek.com/gigawiper-combines-multiple-malware-for-system-level-sabotage/)

---

### [NEW] CISA Adds 4 Actively Exploited Flaws to KEV — Adobe, Joomla, Langflow, SharePoint

CISA added four vulnerabilities to its Known Exploited Vulnerabilities catalog on July 7–8, confirming active exploitation in the wild:

- **CVE-2026-48282** (CVSS 10.0) — Path traversal in Langflow, enabling unauthenticated RCE
- **CVE-2026-48908** — JoomShaper SP Page Builder unrestricted file upload
- **CVE-2026-55255** — Langflow authorization bypass
- **CVE-2026-45659** — SharePoint Server RCE

Federal agencies are required to patch by July 4–11 under BOD 22-01 deadlines. Langflow CVSS 10.0 is notable for its trivial exploitation potential against exposed instances.

**Sources:** [CISA](https://www.cisa.gov/news-events/alerts/2026/07/07/cisa-adds-three-known-exploited-vulnerabilities-catalog) | [The Hacker News](https://thehackernews.com/2026/07/cisa-adds-4-actively-exploited-adobe.html)

---

## 🛡️ Defense & Detection

### [NEW] 'HalluSquatting' — Turning AI Hallucinations Into Agentic Botnet Delivery

Researchers from Tel Aviv University, Technion, and Intuit detailed **HalluSquatting**, a novel attack technique that weaponizes LLM hallucination tendencies. Attackers pre-register fake repository/package names that AI assistants commonly hallucinate when asked to fetch resources. Hallucination rates reached 85% for repo-cloning prompts and 100% for skill installations across foundation models.

Affected tools include Cursor, Windsurf, GitHub Copilot, Cline, Gemini CLI, and OpenClaw. When a user asks the AI to clone a hallucinated repo, it pulls the attacker-controlled resource and executes commands via the built-in terminal, enabling malware deployment or botnet node recruitment. The technique is notably independent of direct prompt injection — no attacker-to-user communication channel required.

**Defense note:** Agentic botnets represent a new infection vector that bypasses traditional network firewalls. Validation of AI tool outputs before execution is the primary mitigation; researchers withheld exploit details from the public paper.

**Source:** [SecurityWeek](https://www.securityweek.com/hallusquatting-turns-ai-hallucinations-into-botnet-delivery-mechanism/)

---

### [NEW] Operation Muck and Load — 222 GitHub Lure Repositories Deliver Malware

Socket Research identified **Operation Muck and Load**, a campaign involving 222 lure repositories across 190 GitHub accounts. A malicious Go module posing as a DNS scanning tool loads PowerShell code that fetches encrypted payloads from public dead drops (Pastebin, Rlim, YouTube, Instagram, Telegram, Google Docs, GitCode). The final payload chain delivers AsyncRAT, Quasar RAT, Remcos-style RAT, Vidar infostealer, spyware, and XMRig cryptominers.

Since January 2026, the actor published 1,200+ versions (700 malicious) using GitHub Actions workflows. The module hides PowerShell execution with excessive horizontal whitespace and bypasses script-execution policies.

**Source:** [SecurityWeek](https://www.securityweek.com/network-of-200-github-repositories-used-for-malware-infection/)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] Helix Vishing Group Emerges — SharePoint Data Theft, Links to ShinyHunters

ReliaQuest identified a new data-extortion group called **Helix** targeting SharePoint environments via voice phishing, device-code phishing, and MFA abuse. The group calls employees impersonating managers (caller ID spoofing), tricks targets into device-code authentication, registers a new MFA authenticator for persistence, then bulk-exfiltrates SharePoint data from IP `179.43.185[.]230` using `python-requests/2.28.1`.

ReliaQuest found infrastructure overlaps with the now-defunct **BlackFile** group (same AS51852) and tactical overlaps with **ShinyHunters** (vishing playbook, NICENIC registrar use). Helix emerged shortly after BlackFile ceased operations in April, suggesting operator migration. High-impact mitigation: disable device-code authentication where possible.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-helix-vishing-group-emerges-in-sharepoint-data-theft-attacks/)

---

### [NEW] Forg365 — AI-Powered Phishing-as-a-Service Targets Microsoft 365

ZeroBEC researchers detailed **Forg365**, a mature PhaaS platform combining adversary-in-the-middle (AiTM) phishing, device-code phishing, and AI-assisted lure generation. The platform includes a browser extension (ForgCookie, compatible with Chrome/Edge/Brave) that maintains persistent Microsoft SSO access by automatically refreshing session cookies via silent OAuth flows.

Notable: the platform integrates AI email generation directly into the admin dashboard, uses Amazon SES for delivery and Cloudflare Pages for landing pages, and includes anti-analysis features (AES-encrypted redirectors, bot detection, debugger traps, sandbox checks). Organizations should monitor Entra logs for device-code authentication events and unexpected OAuth grants.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-forg365-phishing-platform-uses-ai-to-target-microsoft-365-accounts/)

---

### [UPDATE] Former DigitalMint Negotiator Sentenced — 70 Months for BlackCat Collusion

Angelo Martino, 41, a former DigitalMint ransomware negotiator, was sentenced to 70 months in prison for sharing victim negotiating positions and insurance limits with BlackCat (ALPHV) affiliates while employed to negotiate ransoms. Martino extracted $75.3 million from five victims including a $26.8M ransom from a nonprofit and $25.7M from a financial services firm. Co-conspirators Kevin Martin and Ryan Goldberg were sentenced to 4 years each in May. The FBI seized $10M in assets including a bayfront home, a fishing boat, and cryptocurrency wallets.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/us-ransomware-negotiator-gets-4-years-in-prison-for-blackcat-attacks/) | [CyberScoop](https://cyberscoop.com/digitalmint-ransomware-negotiator-angelo-martino-sentenced/)

---

### [NEW] 764 Splinter Group Leader Sentenced to 40 Years

Alexis Aldair Chavez, 19, who led the 8884 offshoot of the violent extremist collective 764, was sentenced to 40 years in federal prison for sexual exploitation of children, racketeering, and CSAM offenses. Chavez coerced victims into self-harm, animal torture, and suicide attempts via social media platforms, messaging apps, and gaming services.

**Source:** [CyberScoop](https://cyberscoop.com/764-splinter-group-leader-sentenced-alexis-chavez/)

---

## ⚠️ Vulnerabilities & Patches

### [NEW] GhostLock (CVE-2026-43499) — 15-Year-Old Linux Kernel Use-After-Free With PoC

Nebula Security published exploit code for **GhostLock**, a use-after-free vulnerability in the Linux kernel present since kernel 2.6.39 (2011) across all major distributions. The flaw exists in a task-priority cleanup helper function — when a deadlock triggers a rollback, memory is freed while a dangling pointer remains in another task, enabling local privilege escalation to root. Patched in April 2026. Nebula demonstrated container escape via Google's kernelCTF program and received a $92,337 bounty.

**Sources:** [SecurityWeek](https://www.securityweek.com/15-year-old-linux-vulnerability-ghostlock-earns-researchers-92k-from-google/) | [Nebula Security](https://nebusec.ai/research/ionstack-part-2/)

---

### [NEW] Unpatched Backdoor in Tenda Router Firmware (CVE-2026-11405)

CERT/CC disclosed a hardcoded authentication backdoor in Tenda router firmware affecting models FH1201, W15E, AC10, AC5, and AC6. The `/bin/httpd` login function contains a fallback code path that performs plaintext `strcmp()` against a hidden configuration variable (`sys.rzadmin.password`) if MD5-based authentication fails, granting role=2 (root-equivalent) admin access. Tenda was notified on May 19, 2026 but has not issued a patch or response. No user-facing mitigation exists beyond disabling remote management — the backdoor is baked into the binary.

**Source:** [SOCFortress](https://socfortress.medium.com/unpatched-backdoor-in-tenda-router-firmware-cve-2026-11405-b2dace8ef73b)

---

### [NEW] Palo Alto Networks Patches 13 Vulnerabilities

PAN released security updates addressing 13 vulnerabilities across its product line. No critical CVEs or active-exploitation indicators were disclosed in the advisory.

**Source:** [SecurityWeek](https://www.securityweek.com/palo-alto-networks-patches-13-vulnerabilities/)

---

## 📋 Policy & Industry

### [NEW] Interpol Operation First Light Nets 5,800 Arrests Across 97 Countries

Interpol's anti-fraud crackdown **Operation First Light** identified 142,000 victims, arrested 5,800 alleged cybercriminals, and seized $293M. The operation targeted social-engineering scams including BEC, sextortion, romance scams, and investment fraud. Authorities analyzed 152,800 cybercrime cases, solved nearly 24,000, and blocked 31,000+ bank accounts.

**Source:** [CyberScoop](https://cyberscoop.com/interpol-cybercrime-crackdown-operation-first-light/)

---

### [NEW] KDDI Data Breach Impacts 12 Million — Zero-Day in ISP Email System

Japanese telecom KDDI confirmed a June 17 breach affecting 12.2 million email addresses and 7.6 million passwords across five ISP subsidiaries (STNet, JCOM, Chubu Telecommunications, NIFTY, BIGLOBE). Attackers exploited a zero-day vulnerability in a third-party email system component. KDDI ejected the attackers, is forcing password resets, and is working with the vendor on a patch. KDDI's mobile and fixed-line services on separate infrastructure were unaffected.

**Source:** [SecurityWeek](https://www.securityweek.com/12-million-impacted-by-data-breach-at-japanese-telco-kddi/)

---

### [NEW] Microsoft Expects More Windows Security Updates From AI-Discovered Flaws

Microsoft announced that its **MDASH** (multi-model agentic scanning harness) AI system is finding vulnerabilities at an accelerated pace, and customers should expect higher volumes of Patch Tuesday updates. Microsoft also updated its Secure Development Lifecycle (SDL) to account for AI-enabled attack techniques. Separately, Reuters reported CISA is using Anthropic's Fable AI model to scan government software for vulnerabilities.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-expects-more-windows-security-updates-from-ai-discovered-flaws/)

---

## ⚡ Quick Hits

- **OpenMandriva sabotage:** A contributor with admin privileges deleted GitHub repositories and pushed empty packages obsoleting Gnome/Cosmic desktop environments after a dispute. The project is restoring data and conducting a full audit. [BleepingComputer](https://www.bleepingcomputer.com/news/security/openmandriva-linux-says-contributor-tried-to-sabotage-the-project/)
- **Injective SDK supply-chain attack:** Compromised GitHub account published malicious `@injectivelabs/sdk-ts` v1.20.21 on npm, stealing cryptocurrency wallet private keys and seed phrases. 310 downloads before deprecation; 87 dependent packages with 112K cumulative downloads. [BleepingComputer](https://www.bleepingcomputer.com/news/security/injective-sdk-on-npm-infected-with-cryptocurrency-wallet-stealer/)
- **CSIRT Gadgets forecast — TeamPCP/Vect context:** "The package was not the prize." The real risk from poisoned CI/CD tooling is credential harvesting (GitHub PATs, cloud keys, K8s secrets) that persists long after the malicious package is removed. [CSIRT Gadgets](https://csirtgadgets.com/commits/2026/7/9/forecast-the-package-was-not-the-prize)
- **UK government agentic AI defense plan:** UK rolls out national AI defense strategy alongside industry pledges for responsible AI security development. [SecurityWeek](https://www.securityweek.com/uk-government-rolls-out-agentic-ai-defense-plan-alongside-industry-pledge/)
