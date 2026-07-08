---
title: "Gitea Authentication Bypass 🔴, CISA Adds ColdFusion to KEV 🔴, Cavern Manticore Iran C2 🎯, Accenture Confirms 35 GB Breach 🎯, Ubiquiti 7 Critical Patches ⚠️"
date: 2026-07-08
tags: ["gitea", "authentication-bypass", "cisa-kev", "coldfusion", "cavern-manticore", "iran", "mois", "accenture", "breach", "uat-7810", "longleash", "ubiquiti", "unifi", "tenda", "backdoor", "cordyceps", "github-actions", "vidar", "xmrig", "factory-v3", "cisa", "mythos", "logging"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Gitea Docker instances actively exploited via authentication bypass flaw (CVE-2026-20896, CVSS 9.8). CISA adds ColdFusion RCE to KEV, orders federal patching by July 11. Iran MOIS-linked Cavern Manticore deploys modular C2 framework against Israeli IT providers. Accenture confirms 35 GB source code theft. UAT-7810 expands ORB network with LONGLEASH malware. Ubiquiti patches seven critical UniFi OS flaws."
---
# Daily Threat Intelligence Digest — July 8, 2026

*24 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] CVE-2026-20896: Gitea Docker Images Under Active Exploitation — Authentication Bypass via Single HTTP Header**

Sysdig researchers are tracking active exploitation of CVE-2026-20896 (CVSS 9.8), a critical authentication bypass in Gitea's official Docker images (versions ≤1.26.2). The flaw stems from the Docker image shipping with `REVERSE_PROXY_TRUSTED_PROXIES = *` as the default, meaning any source IP is treated as trusted. If reverse-proxy authentication is enabled, anyone who can reach the Gitea HTTP port can send a crafted `X-WEBAUTH-USER` header and impersonate any user — including administrators — with no password or token required.

Sysdig caught the first in-the-wild hit just 13 days after disclosure: a VPN-exit scanner that grabbed access. Approximately 6,200 Gitea instances are exposed to the internet per Shodan. Successful exploitation grants access to private repositories, API keys, database credentials, deploy tokens, and CI/CD configurations committed to the instance. Gitea 1.26.3 and 1.26.4 fix the issue by making reverse-proxy authentication opt-in. Standard (non-Docker) Gitea installations use a secure default and are unaffected.

**Hunting hypothesis:** An unauthenticated remote attacker sends `X-WEBAUTH-USER: admin` to any internet-facing Gitea Docker instance with reverse-proxy auth enabled, gaining full repository access without credentials. [[SecurityWeek](https://www.securityweek.com/critical-gitea-flaw-under-active-exploitation-researchers-warn/); [SecurityAffairs](https://securityaffairs.com/194902/hacking/critical-gitea-docker-bug-under-active-exploitation-exposes-repositories-and-secrets.html); [GitHub Advisory](https://github.com/go-gitea/gitea/security/advisories/GHSA-f75j-4cw6-rmx4)]

**Recommended action:** Update all Gitea Docker deployments to ≥1.26.3 immediately. Audit for reverse-proxy authentication configurations. Restrict Gitea HTTP ports to trusted networks.

---

**[UPDATE] CVE-2026-48282: Adobe ColdFusion — CISA Adds to KEV, Orders Federal Patching by Friday**

*Previously covered July 6. New today: CISA has added CVE-2026-48282 to its Known Exploited Vulnerabilities catalog and ordered FCEB agencies to patch by July 11 under BOD 26-04.*

CISA's KEV addition confirms what was already evident: the maximum-severity (CVSS 10.0) unauthenticated RCE in Adobe ColdFusion is being actively exploited. Attackers began scanning within two hours of Adobe's disclosure on June 30. CISA's action under BOD 26-04 — the new binding directive that prioritizes patching based on exploitation evidence, automation potential, and internet exposure — signals the agency's urgency. The Canadian Centre for Cyber Security (CCCS) also issued its own advisory. Shadowserver tracks nearly 800 internet-exposed ColdFusion instances, though many may be honeypots. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-orders-feds-to-patch-max-severity-coldfusion-flaw-by-friday/); [The Hacker News](https://thehackernews.com/2026/07/cisa-adds-4-actively-exploited-adobe.html)]

**Recommended action:** Patch ColdFusion to the latest version immediately. FCEB agencies: comply with the July 11 BOD 26-04 deadline. Restrict internet access to ColdFusion administrative interfaces.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Cavern Manticore: Iran MOIS Deploys Modular "Cavern" C2 Framework Against Israeli IT Providers**

Check Point Research has disclosed a new Iran-linked APT cluster, Cavern Manticore, affiliated with Iran's Ministry of Intelligence and Security (MOIS), deploying a previously undocumented modular C2 framework called Cavern (aka Cav3rn). The group shares tactical overlap with MuddyWater and Lyceum (assessed as a subgroup of OilRig).

The attack chain exploits SysAid's software update feature for DLL side-loading, deploying a trojanized `uxtheme.dll` containing the Cavern Agent. The agent then fetches five post-exploitation DLL modules over HTTPS/WebSocket from `hospitalinstallation[.]com`:

- **mhm.dll** — File operations, recursive search, archive handling, bidirectional transfer
- **db.dll** — SQL database enumeration, query, export, manipulation
- **ode.dll** — Active Directory reconnaissance, user/group enumeration, LDAP brute-force
- **n-ten.dll** — Network reconnaissance, port scanning, SMB brute-force
- **n-sws.dll** — SOCKS5 proxy and WebSocket tunneling

Notably, Cavern Manticore chains trusted IT provider relationships — compromising an initial IT services company, pivoting to a second-hop provider, then reaching the intended target. The actor abuses RMM tools and browser-based remote desktop (leveraging features like remote printing to exfiltrate data when clipboard and file-transfer controls are blocked). The framework uses three .NET compilation formats (.NET Framework, Mixed-Mode C++/CLI, and Native AOT) as an anti-analysis measure, with per-module AppDomain isolation for anti-forensics.

**Hunting hypothesis:** An attacker exploits a SysAid software update mechanism to side-load a trojanized DLL, then uses the Cavern C2 framework to pivot through IT service providers into target networks via compromised RMM tools. [[The Hacker News](https://thehackernews.com/2026/07/iran-linked-hackers-use-new-cavern-c2.html); [Check Point Research](https://research.checkpoint.com/2026/cavern-manticore-exposing-iran-linked-modular-c2-framework/)]

**Recommended action:** Hunt for SysAid DLL side-loading indicators. Audit RMM tool access logs for lateral movement between customer environments. Monitor for C2 domain `hospitalinstallation[.]com` and related IoCs.

---

**[NEW] Accenture Confirms Data Breach — 35 GB of Source Code Reportedly Stolen**

Accenture has confirmed a security breach after threat actor "888" claimed to have stolen approximately 35 GB of source code and related data from the company's Azure DevOps repositories. The threat actor reportedly exfiltrated RSA keys, SSH keys, Azure personal access tokens (PATs), Azure Storage access keys, and configuration files. Accenture stated it "remediated the source" of the breach and that there is "no impact to operations and service delivery" — but did not disclose the attack vector, scope, or whether customer data was affected.

The same threat actor previously attempted to sell Accenture employee data following a third-party breach in 2024. Accenture also suffered a LockBit ransomware attack in 2021. The reuse of the "888" moniker suggests a persistent interest in the organization. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/accenture-confirms-breach-after-hacker-offers-stolen-data-for-sale/)]

**Recommended action:** Accenture customers and partners should review shared access credentials, PATs, and storage keys. Monitor for exposed Accenture source code or configuration data on underground forums.

---

**[NEW] UAT-7810 Expands ORB Network with LONGLEASH Malware — Compromises Unpatched Ruckus and ASUS Routers**

Cisco Talos researchers have documented the ongoing expansion of a Chinese APT cluster (UAT-7810) that is building an Operational Relay Box (ORB) network by compromising internet-facing networking devices, primarily unpatched Ruckus routers. The ORB network serves as proxy infrastructure for other China-aligned APTs, including UAT-5918, allowing threat actors to route traffic through legitimate local infrastructure to evade detection.

New malware discovered in the campaign includes:

- **LONGLEASH** — Upgraded successor to SHORTLEASH, adding reverse shell, HTTP/DNS/SOCKS/TCP/ICMP/UDP proxying, SMTP client/server, TLS/PKI support, self-removal on tamper detection, and intermediate C2 forwarding
- **DOGLEASH** — Lightweight Linux backdoor deployed via web shells, supporting shell execution, file access, and in-memory code execution
- **JARLEASH** — Java-based administrative tool with FTP/SFTP/Netcat server functionality
- **LEASHTEST** — MIPS IoT device capability testing utility

The group exploits known n-day vulnerabilities: CVE-2020-22653, CVE-2020-22658, and CVE-2023-25717 (Ruckus routers) and CVE-2025-2492 (ASUS AiCloud routers). Organizations deploying Ruckus or ASUS networking equipment on the internet perimeter should verify patch status immediately. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/chinese-hackers-develop-longleash-malware-to-expand-orb-network/)]

**Recommended action:** Patch all internet-facing Ruckus and ASUS routers against the listed CVEs. Monitor for ORB-related network traffic patterns (anomalous proxy connections from edge devices). Block C2 infrastructure from Talos IoC lists.

---

**[NEW] Spain Arrests Alleged Cyber Army of Russia Reborn Member — NoName057(16) Links Confirmed**

Spain's National Police arrested a man in Palencia in March for his role as a logistics operative for pro-Russian hacktivist groups Cyber Army of Russia Reborn (CARR) and Z-Pentest. The arrest, disclosed publicly July 7, was the result of an FBI tip received in August 2025. The suspect facilitated a Ukrainian hacker's escape to Russia via Poland and Belarus, maintained contact via encrypted messaging apps, and participated in NoName057(16) operations that were claimed on pro-Russian geopolitics sites.

Police seized computers and cryptocurrency storage devices and froze wallets used to receive crime proceeds. NoName057(16) was established by presidential decree in 2018, and the U.S. government has offered rewards of up to $10 million for information on its members. This follows the December 2025 extradition and guilty plea of Victoria Dubranova, another CARR member. [[CyberScoop](https://cyberscoop.com/spain-arrests-alleged-cyber-army-of-russia-reborn-member/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/spain-arrests-suspected-member-of-pro-russian-hacktivist-groups/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Ubiquiti Patches Seven Critical UniFi OS Vulnerabilities — Max-Severity Command Injection in Connect App**

Ubiquiti has released patches for seven critical-severity vulnerabilities across UniFi OS, including CVE-2026-50746 — a maximum-severity command injection flaw in the UniFi Connect Application (≤3.4.16). An attacker with network access can exploit improper access controls to execute arbitrary commands on the host device. The Connect Application manages commercial building operations including smart LED lighting and EV chargers. Six additional critical flaws (CVE-2026-50747, CVE-2026-50748, CVE-2026-54400, CVE-2026-54402, CVE-2026-55115, CVE-2026-55116) affect UniFi Talk, Access, Protect, and UniFi OS Server across routers, gateways, NAS devices, and surveillance systems.

Censys tracks over 100,000 internet-exposed UniFi OS instances, nearly 50,000 in the U.S. In June, CISA warned of active exploitation of three other max-severity UniFi OS flaws patched one month prior. Ubiquiti has not disclosed whether any of the current seven are being exploited in the wild, but six require no user interaction. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ubiquiti-warns-of-new-max-severity-unifi-os-vulnerability/)]

**Recommended action:** Update UniFi Connect Application to ≥3.4.20 and apply all other UniFi OS patches. Audit internet-facing UniFi deployments.

---

**[NEW] CVE-2026-11405: Tenda Router Firmware Hidden Backdoor — No Patch Available**

CERT/CC has disclosed a hidden authentication backdoor (CVE-2026-11405) in multiple Tenda router firmware versions. The undocumented mechanism in the `login()` function of `/bin/httpd` checks an alternate password from `sys.rzadmin.password` if standard MD5 authentication fails. If the backdoor password matches, full administrative access is granted regardless of the username entered.

Affected devices include Tenda FH1201, W15E, AC10, AC5, and AC6 V2 routers. No patch is available because Tenda could not be reached by CERT/CC. Users should disable the remote web management panel and change the default LAN IP address to reduce scanner discovery. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hidden-backdoor-in-tenda-router-firmware-grants-admin-access/)]

**Recommended action:** Disable remote web management on all Tenda routers immediately. Block internet access to the management interface. Consider replacing Tenda devices if possible.

---

**[NEW] Cordyceps: Class of GitHub Actions CI/CD Weaknesses Exploitable Across 300+ Major Repositories**

Researchers at Novee Security disclosed "Cordyceps," a class of CI/CD supply chain vulnerability that exploits the interaction between `pull_request_target` and `workflow_run` triggers in GitHub Actions. The attack pattern — command injection, code injection via `actions/github-script`, and cross-workflow privilege escalation — exploits how multiple valid workflow files compose, not individual file vulnerabilities. This means every affected pipeline passed all SAST/DAST scans.

Confirmed exploitable instances include Microsoft Azure Sentinel (persistent write access to security content shipped to thousands of organizations), Google's AI Agent Development Kit (project-level owner access on Google Cloud), and Apache Doris (credential theft). The entry cost is a free GitHub account — no org membership or elevated privileges required. AI-generated CI/CD configurations are widening the gap by reproducing insecure patterns at scale. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/the-github-actions-attack-pattern-your-ci-security-scanners-miss/)]

**Recommended action:** Prefer `pull_request` over `pull_request_target` for untrusted contributions. Pin third-party actions to commit SHAs. Default repository permissions to read-only. Gate privileged workflows behind manual approval for first-time contributors.

---

## 🛡️ Defense & Detection

**[NEW] Vidar Stealer + XMRig Campaign Uses Factory-v3 MaaS Platform with Multi-Layer Evasion**

Unit 42 documented a financially motivated campaign delivering Vidar stealer and XMRig cryptocurrency miner via malvertising for cracked software. The campaign's evasion stack is notable:

- **Factory-v3 MaaS builder** — Go-compiled loaders with per-build unique hashes (27 unique UUIDs across 43 samples), defeating hash-based detection
- **Rogue Authenticode certificates** — Fabricated JustWatch GmbH and BleacherReport certificates (not chained to trusted roots, but visually deceptive)
- **File-size inflation** — Null-byte padding to 491 MB to evade sandbox size limits (actual payload: 2.3 MB)
- **AMSI bypass** — In-memory patch of `AmsiScanBuffer` with XOR-obfuscated DLL/function names
- **DLL search-order hijacking** — Fake `MpClient.dll` exports Windows Defender API functions

The dual-monetization scheme sells stolen credentials and crypto wallets on criminal markets while mining Monero passively. C2 servers at `136.243.203[.]109` and related IPs. The same Factory-v3 builder infrastructure serves a concurrent Lumma stealer campaign. [[Unit 42](https://unit42.paloaltonetworks.com/vidar-stealer-xmrig-miner-campaign-analysis/)]

**Recommended action:** Block C2 IPs and `pool.supportxmr[.]com`. Hunt for persistence indicators (registry `SystemAgentService`, scheduled tasks, startup batch scripts). Monitor for `MpClient.dll` loading from non-standard paths.

---

## 📋 Policy & Industry News

**[NEW] CISA Deploying Anthropic's Mythos AI for Automated Vulnerability Scanning in Government Software**

SecurityWeek reports that CISA is using Anthropic's Mythos AI tool to scan U.S. government software for security flaws. This follows Anthropic's Mythos model identifying the "Bad Epoll" Linux kernel vulnerability that human reviewers initially missed. CISA's adoption signals growing institutional trust in AI-assisted vulnerability discovery for critical infrastructure software. [[SecurityWeek](https://www.securityweek.com/cisa-reportedly-using-anthropics-mythos-to-scan-government-software-for-flaws/)]

---

**[NEW] OMB M-26-14: New Federal Logging Directive Ties Maturity Progression to Asset Visibility**

OMB M-26-14 rescinds M-21-31 and replaces blanket data-retention mandates with a five-element logging maturity model (levels 0–4) that agencies must progress through on a strict timeline. The directive explicitly ties each maturity milestone to how well agencies know what's on their networks — making asset visibility the prerequisite for compliance. Agencies must begin progression after CISA publishes the Logging Reference Architecture. [[Tenable Blog](https://www.tenable.com/blog/omb-m-26-14-asset-visibility-logging-maturity-model-compliance)]

---

**[NEW] AI Executive Order Cybersecurity Clearinghouse Deadline Passes**

The 30-day deadline for establishing the AI cybersecurity clearinghouse — mandated by the AI-focused executive order signed in June — passed last week. The clearinghouse, to be coordinated by Treasury, NSA, and CISA, is intended to prioritize vulnerability scanning, discovery, and patching across critical infrastructure. CyberScoop examines the gap between the mandate's ambition and the operational readiness to execute it. [[CyberScoop](https://cyberscoop.com/ai-executive-order-cybersecurity-clearinghouse-vulnerability-patching-gap/)]

---

*Cross-reference: CVE-2026-48282 (ColdFusion), CVE-2026-53359 (Januscape), Januscape KVM escape, Cordyceps CI/CD, and Armored Likho APT were covered in prior editions and tracked for continuity. No duplicate re-reporting.*
