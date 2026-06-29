---
title: "🔴 Atomic Arch 1,500+ AUR, FortiSandbox Exploited, 🎯 UNC6508 REDCap, DragonForce Teams C2, ⚠️ Vertex AI RCE, Cisco SD-WAN ZD"
date: 2026-06-16
tags: ["Atomic Arch", "FortiSandbox", "UNC6508", "REDCap", "DragonForce", "Backdoor.Turn", "Cisco SD-WAN", "Vertex AI", "CVE-2026-54420", "SimpleHelp", "SearchLeak", "OptinMonster", "The Quarry", "ShinyHunters", "Earth Lusca", "SprySOCKS"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Atomic Arch supply-chain attack expands to 1,500+ AUR packages; FortiSandbox critical flaws now actively exploited; CISA adds LiteSpeed cPanel plugin to KEV under new BOD 26-04; DragonForce abuses Microsoft Teams TURN relays for stealth C2; Google exposes UNC6508 Chinese espionage in medical networks since 2023; Unit 42 discloses Vertex AI SDK bucket squatting RCE; Cisco patches fifth SD-WAN Manager zero-day."
---

# Daily Threat Intelligence Digest — June 16, 2026

*72 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Atomic Arch Supply Chain Attack Expands to 1,500+ AUR Packages — Arch Linux Suspends Registrations**

The Atomic Arch supply chain campaign against the Arch User Repository has ballooned from 400+ compromised packages (covered June 13) to **over 1,500 malicious packages** published by June 11. Arch Linux has **suspended new AUR account registrations** for cleanup and is actively tracking down malicious commits. Attackers targeted orphaned packages with legitimate history and modified PKGBUILDs to pull malicious npm packages (`atomic-lockfile`, `js-digest`) during installation, then expanded to Bun-based install paths. The payload includes a **Rust-based infostealer** (browser cookies, SSH keys, API tokens, Slack/Discord/Teams credentials) and an **eBPF rootkit** for kernel-level stealth. Systems where packages were installed with elevated privileges should be treated as fully compromised — rebuild from clean media. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/over-400-arch-linux-packages-compromised-to-push-rootkit-infostealer/); [SecurityWeek](https://www.securityweek.com/atomic-arch-supply-chain-attack-hits-1500-aur-packages/); [Truesec/Sonatype](https://www.truesec.com/hub/blog/supply-chain-attack-compromising-arch-linux-aur-packages-infostealer-rootkit)]

---

**[NEW] Fortinet FortiSandbox Critical Flaws (CVE-2026-39813, CVE-2026-39808, CVE-2026-25089) Now Actively Exploited**

Defused reported active exploitation of three critical pre-auth RCE vulnerabilities in Fortinet's FortiSandbox threat detection platform starting June 15. Patched April 14, the flaws enable **unauthenticated command injection** with no user interaction — attackers can escalate privileges and execute arbitrary code remotely. Defused notes CVE-2026-39813 (no prior recorded exploitation), CVE-2026-39808, and CVE-2026-25089 (listed as "vibecoded, likely faulty exploit"). CISA tracks **26 Fortinet vulnerabilities** as exploited in attacks, 13 abused by ransomware gangs. Admins must upgrade affected deployments immediately. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/critical-fortinet-fortisandbox-flaws-now-exploited-in-attacks/)]

---

**[NEW] CISA Adds LiteSpeed cPanel Plugin Flaw to KEV — First CVE Under BOD 26-04 Three-Day Deadline**

CISA added **CVE-2026-54420** (the LiteSpeed cPanel user-end plugin symlink-following vulnerability) to its Known Exploited Vulnerabilities catalog, ordering federal agencies to patch within **three days** under the new BOD 26-04 risk-based directive — making it the **first vulnerability subject to the new expedited timeline**. The flaw allows attackers with FTP or web shell access to escalate privileges to **root on shared hosting servers running CloudLinux/CageFS**. CISA also previously warned agencies about related CVE-2026-48172. A detection command is available to check logs for exploitation attempts. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-warns-of-another-actively-exploited-cpanel-plugin-flaw/)]

---

**[NEW] DragonForce Ransomware Abuses Microsoft Teams TURN Relays for Stealth C2 — Backdoor.Turn Malware**

DragonForce ransomware deployed **Backdoor.Turn**, a custom **Go-based RAT** that hides command-and-control traffic inside **Microsoft Teams TURN relay infrastructure** — the first known in-the-wild malware to abuse this technique. Symantec documented the attack against a major U.S. services company: the malware obtains an anonymous Teams visitor token, uses a legitimate Microsoft TURN relay during connection setup, then connects to the attacker's C2. Defenders see traffic associated with Microsoft Teams infrastructure. The attack also employed **BYOVD techniques** with drivers from Huawei, Topaz Antifraud, and K7 Security to obtain kernel privileges and terminate security tools. Capabilities include command execution, LDAP/AD search, TLS certificate capture, and browser credential theft. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ransomware-gang-abuses-microsoft-teams-relays-to-hide-malicious-traffic/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Google Exposes UNC6508 — Chinese Espionage Group Operating Undetected Since 2023, Targeting Medical Research**

Google Threat Intelligence Group discovered **UNC6508**, a previously unknown China-linked espionage group that compromised **REDCap servers** at a North American medical research university in September 2023 and remained undetected through November 2025. The group deployed **InfiniteRed** custom malware (persistence module, credential harvester, HTTP cookie-based backdoor) to exfiltrate data. In a novel technique for Chinese threat actors, UNC6508 abused legitimate **content compliance rules** in enterprise productivity tools to automatically BCC sensitive emails (keywords targeting medical research, military tech, and AI) to an attacker-controlled Gmail account. [[CyberScoop](https://cyberscoop.com/google-unc6508-china-espionage-threat/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/chinese-hackers-breach-redcap-servers-steal-medical-research/)]

---

**[NEW] Earth Lusca Expands Arsenal — Windows SprySOCKS Variants Target Government Orgs in Four Countries**

ESET discovered Windows variants of the SprySOCKS Linux backdoor used by Chinese threat group **Earth Lusca** (aka FishMonger) in attacks on government organizations in Taiwan, Thailand, Pakistan, and Honduras between 2023–2024. Two variants exist: **WIN_DRV** with kernel drivers for rootkit-like capabilities (hide processes, files, registry keys, network connections) and **WIN_PLUS** (a barebones backdoor). Both support 30+ C2 commands, SOCKS proxy functionality, keylogging, and TCP traffic diversion to hide the backdoor's listening port. ESET also found indications of a UEFI bootkit component potentially exploiting CVE-2023-24932. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/windows-version-of-sprysocks-linux-malware-used-to-attack-govt-orgs/)]

---

**[NEW] The Quarry — PhaaS Operation Behind Hundreds of IRS and SSA Phishing Campaigns**

SOCRadar detailed **The Quarry**, a sophisticated Phishing-as-a-Service operation run by a developer known as "RockyBelling" who has sold phishing toolkits to nearly **200 affiliates** since April 2025. The operation uses **Adspect traffic cloaking**, legitimate **ConnectWise ScreenConnect RMM** as the final payload (not traditional malware), **Telegram-based C2** for real-time victim notifications, and a **VBS dropper with UAC bypass** released April 2026. Over 90% of victims are in the United States, with top sectors being SaaS, healthcare, media, and fintech. The PhaaS model includes phishing kits, self-hosted ScreenConnect panels (~$2,000 setup, $100/month), and post-exploitation scripts for browser history and W-2 document theft. [[SOCRadar](https://socradar.io/blog/the-quarry-phaas-irs-ssa-phishing/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Pickle in the Middle — Vertex AI SDK Bucket Squatting Enables Cross-Tenant RCE (CVE fixed in v1.148.0)**

Unit 42 disclosed a vulnerability in the **Google Cloud Vertex AI SDK for Python** (versions 1.139.0–1.140.0) allowing an attacker operating entirely from their own Google Cloud project to hijack a victim's model upload and achieve **cross-tenant RCE** with zero initial access. The root cause: a **deterministic default staging bucket name** (`{project}-vertex-staging-{region}`) combined with a **missing ownership check** — the SDK uploads to any existing bucket regardless of project ownership. An attacker creates the predicted bucket in their own project, sets up a Cloud Function to replace uploaded models within the ~2.5-second window before the service agent reads them, and deploys a malicious `joblib` payload with a crafted `__reduce__` method. The exfiltrated OAuth token (cloud-platform scope) from Google's tenant project can access other model deployments, BigQuery datasets, and Kubernetes infrastructure. Google fixed the issue in v1.148.0 (April 15). [[Unit 42](https://unit42.paloaltonetworks.com/hijacking-vertex-ai-model/)]

---

**[NEW] Cisco SD-WAN vManage Zero-Day (CVE-2026-20262) Patched After Active Exploitation**

Cisco patched **CVE-2026-20262**, a file upload validation flaw in Catalyst SD-WAN Manager (formerly SD-WAN vManage) exploited as a zero-day earlier this month. The vulnerability allows authenticated remote attackers to **create or overwrite any file on the OS** and escalate to **root privileges**. Index.jsp and .war file upload attempts to specific API endpoints are IOCs. This is the **fifth SD-WAN Manager zero-day** flagged by CISA — the platform is under sustained attack. [[BleepingComputer](https://www.bleepercomputer.com/news/security/cisco-fixes-sd-wan-vmanage-flaw-exploited-in-zero-day-attacks/)]

---

**[NEW] SimpleHelp CVE-2026-48558 — Critical Flaw Allows Unauthenticated Technician Account Creation**

A critical flaw in SimpleHelp remote management software (versions ≤5.5.15, 6.0 pre-release) allows unauthenticated attackers to **create privileged technician accounts** on servers using OIDC authentication. The vulnerability in identity assertion validation enables bypassing MFA and gaining remote access to managed endpoints, with script execution capabilities. ~14,000 SimpleHelp servers are internet-exposed, with ~7.2% using OIDC. Patched in versions 5.5.16 and 6.0RC2 (June 9). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/simplehelp-bug-lets-hackers-create-rogue-remote-support-accounts/)]

---

**[NEW] SearchLeak — Microsoft 365 Copilot Turned Into 1-Click Data Theft Tool (CVE-2026-42824)**

Varonis disclosed **SearchLeak**, a three-stage attack chain chaining **parameter-to-prompt injection**, an **HTML rendering race condition**, and a **Bing SSRF** to exfiltrate email content, calendar events, OneDrive/SharePoint documents with a single click on a crafted URL. Microsoft addressed the vulnerability (assigned CVE-2026-42824, critical severity) earlier this month. The attack demonstrates how legacy bug classes (SSRF, HTML injection) become more dangerous in AI contexts where prompt injection enables new attack surfaces. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-attack-turned-microsoft-365-copilot-into-1-click-data-theft-tool/)]

---

## 🛡️ Defense & Detection

**[NEW] OptinMonster CDN Supply-Chain Attack Compromises 1.2 Million WordPress Sites**

Awesome Motive's CDN was breached in a supply-chain attack affecting **OptinMonster (1.2M sites)**, TrustPulse, and PushEngage. Attackers exploited a known UpdraftPlus vulnerability to access a marketing server containing CDN credentials, then modified JS files served from the CDN to collect admin authentication tokens and create **rogue administrator accounts**. The backdoor plugin (disguised as "Content Delivery Helper" or "Database Optimizer") included a web shell and arbitrary PHP execution, granting full site control. The attack window was short (OptinMonster: 25 minutes; PushEngage: ~21 hours), but compromised sites remain backdoored unless manually cleaned. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/optinmonster-wordpress-plugin-hacked-in-cdn-supply-chain-attack/)]

---

**[NEW] Splunk Enterprise CVE-2026-20253 — Unauthenticated RCE (CVSS 9.8)**

Splunk disclosed a critical pre-authentication remote code execution vulnerability (CVE-2026-20253, CVSS 9.8) in Splunk Enterprise on June 10. The flaw allows unauthenticated attackers to achieve RCE on the platform that sits at the heart of many security operations centers. Given Splunk's central role in log ingestion and detection, successful exploitation gives attackers full access to sensitive security telemetry. [[Malware.News/Picus Security](https://www.picussecurity.com/resource/blog/splunk-cve-2026-20253-unauthenticated-remote-code-execution-vulnerability-explained)]

---

## 📋 Policy & Industry News

**[UPDATE] Council of Europe Confirms Investigation Into ShinyHunters Breach Claim — June 16 Leak Deadline**

The Council of Europe confirmed to BleepingComputer it is investigating claims by ShinyHunters (covered June 15) that the group stole **429,000+ documents** including payroll data, personnel files, and CVs spanning 2011–2026. The extortion group's **June 16 deadline** for leaking the data is today. The breach, if confirmed, would affect 46 European member states and 700M+ citizens — the highest-profile ShinyHunters victim yet, following American Tower (5.2M records), Madison Square Garden (26M records), and Oracle PeopleSoft campaign (100+ organizations). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/council-of-europe-investigates-shinyhunters-data-breach-claims/)]

---

**[NEW] Ransomware Attack Shuts Down Mackay Sugar Mills — The Gentlemen Group Claims Responsibility**

Australia's second-largest sugar producer, **Mackay Sugar**, was hit by a ransomware attack on June 10 that shut down two of its three cane-processing mills in Queensland. The **Gentlemen** ransomware group (aka Storm-2697, active since mid-2025) claimed responsibility on June 15. Operations have partially resumed with manual crushing at one mill, but key cane supply and logistics systems remain down. The Gentlemen group is notable for its worm-like lateral movement capabilities and has listed over 500 alleged victims. [[SecurityWeek](https://www.securityweek.com/ransomware-attack-shuts-down-mills-of-australias-second-largest-sugar-producer/)]

---

**[NEW] Tech Coalition "Athena" Launches to Protect OSS Vulnerabilities Ahead of Disclosure**

Over two dozen organizations (BNY, Chainguard, Cisco, Cloudflare, Docker, JPMorganChase, PwC, and others) formed **Athena**, a shared platform to find, triage, and fix OSS vulnerabilities **before public disclosure** — driven by the acceleration of AI-powered exploitation. Members pool findings and push non-patch mitigations across infrastructure and network layers ahead of disclosure. Patches are distributed through Chainguard Libraries. The coalition represents a significant shift toward **orchestrated pre-disclosure defense** in response to the sub-zero-day exploitation window. [[SecurityWeek](https://www.securityweek.com/tech-coalition-athena-targets-oss-vulnerabilities-ahead-of-disclosure/)]

---

## ⚡ Quick Hits

- **iRhythm discloses data breach**: Cardiac monitoring company filed with SEC after attackers exfiltrated patient health information from third-party business applications via social engineering. Ransom demand received June 9. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/irhythm-discloses-data-breach-says-hackers-stole-patient-info/)]
- **ShinyHunters claims Infinite Campus breach**: 137,000 school staff accounts exposed in Salesforce data theft — names, email addresses, employers, and support tickets confirmed by Have I Been Pwned analysis. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/infinite-campus-data-breach-affects-137-000-school-staff-accounts/)]
- **FulcrumSec leaks Novo Nordisk data after $25M demand goes unpaid**: Danish pharma giant's data from clinical trials published after ransom deadline passed. [[DataBreaches.net](https://databreaches.net/2026/06/15/scoop-fulcrumsec-leaks-novo-nordisk-data-after-25m-demand-goes-unpaid/)]
- **JLR ordered 30,000 staff to reset passwords in-person** after cyberattack compromised staff credentials, former CISO revealed at Infosecurity Europe. [[DataBreaches.net](https://databreaches.net/2026/06/15/jlr-ordered-30000-staff-to-reset-passwords-in-person-after-cyberattack/)]
- **Ukrainian man pleads guilty** in U.S. to Conti ransomware conspiracy charges. [[SecurityWeek](https://www.securityweek.com/ukrainian-man-pleads-guilty-in-us-to-conti-ransomware-charges/)]
- **DOJ seizes CFAKE.com and SOCFAKE.com** in first domain seizure under the TAKE IT DOWN Act for hosting nonconsensual AI-generated nude imagery. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/doj-seizes-cfake-socfake-deepfake-nude-sites-under-take-it-down-act/)]
- **FBI warns of courier-based crypto scams**: Fraudsters using couriers to physically collect cash from victims of pig butchering schemes. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-fraudsters-use-couriers-to-steal-money-in-crypto-scams/)]
