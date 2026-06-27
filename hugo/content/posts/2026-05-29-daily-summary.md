---
title: "🔴 Samba CVSS 10.0, Gogs 0-Day RCE, Charter & Carnival Breaches, GreyVibe AI Cyberespionage"
date: 2026-05-29
tags: ["Samba","CVE-2026-4480","Gogs","RCE","Charter Communications","Carnival Cruise","GreyVibe","MicrosoftSystem64","SideCopy","OpenVPN","Oracle CPU","Gentlemen Ransomware","insider trading","supply chain","npm"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Two critical RCV vulnerabilities lead: Samba CVE-2026-4480 (CVSS 10.0, unauthenticated RCE in printing subsystem) and Gogs 0-day (CVSS 9.4, unpatched with Metasploit module). Major breaches confirmed — Charter Communications (4.9M accounts) and Carnival Cruise (6M customers including SSNs). GreyVibe Russian hybrid threat group uses ChatGPT/Gemini for AI-powered cyberespionage across 5 campaign tracks. MicrosoftSystem64 npm supply chain malware abuses HuggingFace for stealthy exfiltration."
---
# Daily Threat Intelligence Digest — May 29, 2026

*79 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Samba CVE-2026-4480 (CVSS 10.0) — Unauthenticated RCE in Printing Subsystem Affects All Samba Versions — Patch Immediately**

A maximum-severity vulnerability in Samba's printing subsystem allows unauthenticated remote attackers to execute arbitrary commands on affected print servers. Tracked as **CVE-2026-4480** with a perfect CVSS 10.0 score, the flaw lives in how Samba processes the `%J` substitution character within its `print command` configuration setting — an attacker-controlled job description string is passed directly to the shell without sanitization, enabling remote code execution with zero authentication and zero user interaction.

**Scope and mitigations:** Not all deployments are vulnerable. Servers are only at risk when `print command` includes `%J`. Deployments using `printing = cups` or `printing = iprint` are **not** affected. Wrapping `%J` in single quotes (`'%J'`) reduces but does not eliminate risk. The Samba team has released patched versions 4.22.10, 4.23.8, and 4.24.3. Enterprise mixed-OS networks using Samba as a Windows-compatible print server should treat this as an emergency patching priority. The CVSS 3.1 vector (AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H) reflects a worst-case remote-code-execution scenario with full cross-confidentiality impact. [[Cyber Security News](https://cyberpress.org/critical-samba-vulnerability/); [GBHackers](https://gbhackers.com/samba-security-flaw/)]

---

**[NEW] Gogs Zero-Day (CVSS 9.4) — Unpatched Argument Injection Enables Authenticated RCE — Metasploit Module Published, No Fix Available**

A critical argument injection vulnerability (CWE-88) in Gogs, the popular self-hosted Git service, allows any authenticated user to achieve remote code execution on the underlying server. Discovered by Rapid7's Jonah Burgess and tracked without a CVE ID, the flaw resides in Gogs' "Rebase before merging" merge operation: the `Merge()` function passes the pull request's base branch name directly to `git rebase` without a `--` separator, allowing an attacker to inject the `--exec` flag and execute arbitrary shell commands via `sh -c`.

**Why this is dangerous:** Gogs ships with open registration enabled by default (`DISABLE_REGISTRATION = false`) and no repository creation limits (`MAX_CREATION_LIMIT = -1`) — an unauthenticated attacker can register an account, create a repo, enable rebase merging, and exploit the flaw without any interaction from other users. A Metasploit module automates the full chain in seconds against both Linux and Windows targets. Shodan reveals **1,141+ internet-facing instances**, with the true install base (including VPN/internal deployments at companies and universities) significantly larger.

**Impact:** Full server compromise, cross-tenant data breach (read every repository including private ones), credential database dump (password hashes, API tokens, SSH keys, 2FA secrets), lateral movement, and supply-chain attacks via repository code modification. Rapid7 reported the flaw to Gogs maintainers on March 17, 2026 — no patch has been released. **Mitigations:** Set `DISABLE_REGISTRATION = true`, set `MAX_CREATION_LIMIT = 0`, audit for branch names beginning with `--`, and review user API token lists. A Shodan search `http.title:"Gogs" http.title:"Sign In"` will find exposed instances. [[Rapid7](https://www.rapid7.com/blog/post/ve-authenticated-rce-via-argument-injection-gogs-unfixed); [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-gogs-zero-day-flaw-lets-hackers-get-remote-code-execution/); [Cyber Security News](https://cyberpress.org/gogs-0-day-execute-code-servers/)]

---

**[UPDATE] Charter Communications Breach Confirmed — ShinyHunters Leaked 4.9M Records, Have I Been Pwned Verifies Data**

The ShinyHunters extortion gang's breach of U.S. telecom giant Charter Communications (Spectrum brand), first reported on May 27, now has confirmed impact numbers. Have I Been Pwned analyzed the leaked data and verified **4.9 million unique accounts** exposed — names, email addresses, phone numbers, physical addresses, and a subset of approximately 85,000 records from an internal employee directory including job titles. Charter maintains that no sensitive personal information (PI) or customer proprietary network information (CPNI) was stolen, despite ShinyHunters' claims of 42 million records including CPNI data. The attackers breached Charter's Salesforce environment on April 1 via a **vishing attack** that compromised an employee's Microsoft Entra account. After Charter refused to pay the ransom, ShinyHunters leaked the data on their dark web site. This is the latest in ShinyHunters' "Salesforce Aura" campaign targeting SaaS-connected SSO accounts — 7-Eleven (185K records, May 26), Instructure/Canvas (275M+ reported), and hundreds of others. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/charter-communications-data-breach-affects-49-million-accounts/)]

---

**[NEW] Carnival Cruise Data Breach — 6 Million Customers Exposed, SSNs and Passport Numbers Among Stolen Data**

Carnival Corporation, the world's largest cruise operator, confirmed a breach affecting **5,995,277 individuals** in the United States after a threat actor compromised an employee account via social engineering on April 10, 2026. The intrusion was detected on April 14, and by April 22 investigators confirmed data exfiltration. Exposed data includes full names, dates of birth, email and physical addresses, phone numbers, government-issued ID numbers (driver's licenses and passport numbers), loyalty program details, and **Social Security numbers** for a subset of victims. Carnival began notifying affected customers on May 27, more than six weeks after the incident, offering 24-month credit monitoring. This is Carnival's third major security incident following ransomware attacks in 2020/2021 and a multi-state settlement in 2022, indicating systemic weaknesses in employee security awareness and identity verification. [[Cyber Security News](https://cyberpress.org/carnival-cruise-data-breach-exposed/); [GBHackers](https://gbhackers.com/carnival-cruise-breach-leaks-sensitive-customer-information/); [SecurityWeek](https://www.securityweek.com/carnival-data-breach-exposed-6-million-people/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] GreyVibe — Russian Hybrid Threat Group Uses ChatGPT, Gemini, and 5 Campaign Tracks for AI-Powered Cyberespionage**

WithSecure has uncovered a likely Russian-speaking threat group tracked as **GreyVibe**, active since at least August 2025, using AI-generated lures and custom malware to target military, government, civilian, and business entities — primarily Ukrainian or Ukraine-related organizations. The group operates five distinct campaign tracks:

- **PhantomMail:** Spear-phishing with malicious ZIP/RAR archives via Google Drive and 4sync, using decoy PDFs impersonating Ukrainian government/telecom/energy entities
- **PhantomClick:** Fake CAPTCHA/ClickFix pages disguised as Zoom and LAPAS sites, tricking victims into running self-infecting commands
- **PrincessClub:** Fake Ukrainian adult/dating websites delivering **FallSpy Android spyware** and **PhantomRelay/LegionRelay** PowerShell RATs, using fake female Telegram personas and WebRTC-based live audio/video capture
- **DroneLink:** Fake Ukrainian military charity websites themed around FPV drones/UAVs
- **Nebo:** Fake Russian military communications login pages targeting Ukrainian military personnel

WithSecure attributes the campaign's notable lure quality to extensive use of **ChatGPT, Ideogram AI, and Google Gemini** for generating realistic content, including LLM artifacts detectable in generated images. Custom obfuscators (LOOKVALPS, LOOKVALJS, DAYLIGHT, TEASOUP) and the LegionRelay PowerShell RAT were likely AI-assisted. The group exhibits a hybrid profile — state-aligned targeting with cybercriminal operational patterns (public scanning platform uploads, cryptocurrency miner deployment, ties to former TrickBot members). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/greyvibe-hackers-use-chatgpt-gemini-to-power-cyberattacks/); [SecurityWeek](https://www.securityweek.com/russia-linked-greyvibe-attackers-use-ai-to-supercharge-cyberattacks/)]

---

**[NEW] MicrosoftSystem64 — npm Supply Chain Attack Abuses HuggingFace for Stealthy Data Exfiltration Across 3 Platforms**

A sophisticated supply chain attack targeting the npm ecosystem, traced through the malicious package **js-logger-pack** (29 incremental versions since early April 2026), deploys a cross-platform malware loader dubbed **MicrosoftSystem64**. The final payload is an 81 MB Node.js Single Executable Application (SEA) that operates on Windows, macOS, and Linux — establishing a WebSocket C2 channel (195.201.194.107:8010) with 24 supported commands for full remote control.

**Novel exfiltration technique:** Instead of traditional C2 servers, the malware uploads stolen data to **HuggingFace datasets**, blending malicious traffic with legitimate ML model traffic. It also uses HuggingFace model repositories to distribute updates, checking every 24 hours. The malware harvests credentials from 15+ browser families, 80+ cryptocurrency wallet extensions, Telegram Desktop sessions, SSH keys, and runs a built-in keylogger + 60-second screenshot capture. **C2 remains operational** as of May 28, with the embedded HuggingFace API token still valid at discovery. Persistence is platform-specific (scheduled tasks on Windows, LaunchAgents on macOS, systemd/XDG on Linux). [[GBHackers](https://gbhackers.com/microsoftsystem64-malware/); Malware.News]

---

**[NEW] SideCopy Targets Afghanistan Ministry of Finance with XenoRAT; DragonForce and Incransom Continue Ransomware Wave**

**Operation XENOFISCAL:** Seqrite Labs documented a Pakistan-linked SideCopy APT campaign targeting the **Ministry of Finance, Afghanistan**, using a Pashto-language spear-phishing lure ("List of Employees Who Were Introduced to the Intellectual and Psychological Warfare Seminar"). The infection chain uses LNK → mshta.exe → obfuscated JavaScript → .NET deserialization → shellcode → **XenoRAT 1.8.7**, with delivery infrastructure hosted inside Afghanistan's sovereign IP blocks (AS58469, Afghan Ministry of Communication) and C2 on Bulgarian hosting (HZ Hosting, AS59711). The decoy document is a legitimate Afghan MoF provincial staff directory spanning all 34 provinces — suggesting prior intelligence-gathering. [[Malware.News via Seqrite Labs](https://www.seqrite.com/blog/10271-2/)]

**DragonForce** claimed a ransomware attack against **Profundo**, a Dutch research organization (May 27), while **Incransom** threatened to release 100GB of data stolen from **Lawants**, a Spanish law firm (May 28). These follow DragonForce's 7-victim wave reported on May 26 and continue the trend of ransomware groups targeting research organizations and legal practices. [[Malware.News](https://malware.news/t/dragonforce-targets-dutch-research-firm-profundo/107409#post_1); [Malware.News](https://malware.news/t/incransom-targets-spanish-law-firm-lawants/107408#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] OpenVPN Connect macOS CVE-2026-9560 (CVSS 9.4) — Critical Privilege Escalation in Privileged Helper Component, Patched in 3.8.2**

OpenVPN released an emergency update for its macOS client (version 3.8.2, build 6009, May 25) addressing a critical vulnerability in the **privileged helper component** that could allow attackers to inject arbitrary commands with elevated privileges. Discovered by researchers Ismael Esquilichi, Pablo Redondo, and Lê Đức Ninh, the flaw stems from improper input validation in the component responsible for executing operations requiring elevated permissions. No active exploitation has been confirmed, but the high CVSS 9.4 score and the widespread deployment of VPN clients in enterprise environments make patching urgent. Users should verify the SHA-256 checksum (`8d50036510859956d20d1f50e43171be53417431104c6befb1352ff5187c248a`) before installation. [[GBHackers](https://gbhackers.com/openvpn-connect-macos-vulnerability/); [Cyber Security News](https://cyberpress.org/openvpn-connect-macos-flaw/)]

---

**[NEW] Oracle May 2026 Critical Security Patch Update — 35 CVEs, 11 Critical Across 5 Product Families**

Oracle released its May 2026 Critical Security Patch Update (CSPU), part of the new monthly cycle between larger quarterly CPUs, addressing **35 unique CVEs** across 5 product families. Of these, **11 (31.4%) are rated critical** and **18 (51.4%) high severity**. Oracle E-Business Suite received the most patches (12, 34.3% of total), followed by Oracle REST Data Services (11 patches, 31.4%). Three of the E-Business Suite patches are remotely exploitable without authentication. Oracle Communications (8 patches) and Oracle Database Server (3 patches) round out the update. Organizations should prioritize the E-Business Suite and REST Data Services patches given volume and remote-exploit surface. [[Tenable](https://www.tenable.com/blog/oracle-may-2026-critical-security-patch-update-addresses-35-cves)]

---

**[NEW] The Gentlemen Ransomware — Microsoft Dissects Self-Propagating Go RaaS with 21 Lateral Movement Attempts Per Target**

Microsoft Threat Intelligence published a detailed technical analysis of **The Gentlemen ransomware**, a RaaS platform tracked as Storm-2697 that emerged mid-2025 and recently partnered with **BreachForums** to recruit affiliates. The encryptor is written in Go (obfuscated with Garble) and features **per-file Curve25519+XChaCha20 encryption** with partial-file encryption options (`--fast`, `--superfast`, `--ultrafast`).

Its most distinctive capability is the **self-propagation module**: when activated with `--spread`, the malware attempts **21 remote execution operations per target host** across PsExec, WMIC, scheduled tasks (user + SYSTEM), Windows services, PowerShell Remoting, and WMI — each targeting both an SMB share from the infected host and a locally staged copy. The ransomware drops its own copy of PsExec (or downloads from Microsoft Sysinternals), disables Microsoft Defender and Windows Firewall on remote targets, and attempts lateral movement across discovered hosts including workstations, servers, and domain controllers. Observed impact across education, transportation, healthcare, and financial sectors globally. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/28/the-gentlemen-ransomware-dissecting-a-self-propagating-go-encryptor/)]

---

## 📋 Policy & Industry News

**[NEW] Google Security Engineer Charged with $1.2M Polymarket Insider Trading Using Confidential Search Trends**

Michele Spagnuolo, a 36-year-old Italian Google security engineer based in Switzerland, was arrested and charged with wire fraud, money laundering, and violating the Commodity Exchange Act for allegedly using confidential Google Year in Search data to place winning bets on the Polymarket prediction marketplace. Operating under the username "AlphaRaccoon," Spagnuolo allegedly risked approximately **$2.75 million across 25 outcomes** the market treated as unlikely, netting over $1.2 million. He accessed Google's internal "Year in Search" tool — marked "Google Confidential" in red text — to gain advance knowledge of the most-searched people in 2025. He allegedly changed his Polymarket username to an alphanumeric wallet address after users on Discord and X speculated the account was a Google insider. If convicted, the charges carry a combined maximum of 50 years in prison. [[CyberScoop](https://cyberscoop.com/google-security-engineer-insider-trading-polymarket/)]

---

**[NEW] IBM and Red Hat Commit $5 Billion to Secure Open Source Supply Chains Under "Project Lightwell"**

IBM and Red Hat announced a **$5 billion commitment** to open source supply chain security under an initiative dubbed "Project Lightwell." The investment will focus on securing the software supply chain from development through deployment, addressing the escalating threat of supply chain attacks targeting open source ecosystems — a theme underscored this week by the 176-package npm campaign, the MicrosoftSystem64/HuggingFace campaign, and the ongoing TrapDoor cross-ecosystem operation reported on May 25. No specific technical details or timelines have been released. [[SecurityWeek](https://www.securityweek.com/ibm-and-red-hat-commit-5-billion-to-secure-open-source-supply-chains-under-project-lightwell/)]

---

## ⚡ Quick Hits

- **FortiClient EMS / EKZ Infostealer — Arctic Wolf Detection Guidance:** Arctic Wolf Labs published detailed detection guidance for identifying CVE-2026-35616 exploitation delivering the EKZ infostealer. Key IOC: `"Certificate not found in request header"` in EMS logs followed within seconds by `"Certificate user: fortinet-ca2 … successfully updated"`. Defenders should also monitor for Tor-sourced administrative logins and unexpected Remote Access Profile configuration changes. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-exploit-forticlient-ems-flaw-to-push-infostealer-malware/); May 28 prior digest]

- **176-Package npm Campaign — Version 99.99.99:** Sonatype uncovered 176 malicious npm packages published with identical version numbers (99.99.99), designed to bypass internal dependency pinning and trust policies. The campaign demonstrates continued targeting of the npm ecosystem at scale. [[Malware.News via Sonatype](https://malware.news/t/inside-a-176-package-npm-campaign-built-to-beat-your-internal-dependencies/107396#post_1)]

- **FBI Warns of 300+ Fake FIFA World Cup Phishing Sites — Chinese Threat Actor "Ghost Stadium" Identified:** The FBI issued a PSA warning of hundreds of fake FIFA 2026 World Cup domains. Group-IB attributed the largest operation (300+ phishing sites) to Chinese threat actor **Ghost Stadium**, targeting ticket fraud. Bitdefender observed malvertising campaigns spanning the UK, Portugal, Spain, US, Canada, Mexico, Brazil, Germany, and Australia, targeting fake merchandise, streaming services, and Panini sticker offers. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-warns-of-fake-fifa-websites-running-world-cup-fraud-schemes/)]

- **Gitea Vulnerability Exposed 30,000 Deployments:** A vulnerability in the Gitea self-hosted Git service (a Gogs fork) potentially exposed approximately 30,000 deployments to attacks. Details from SecurityWeek. [[SecurityWeek](https://www.securityweek.com/gitea-vulnerability-exposed-30000-deployments-to-attacks/)]
