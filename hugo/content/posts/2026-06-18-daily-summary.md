---
title: "🔴 FortiBleed 73k+ creds, 📦 Mastra supply chain, 🐘 Dropping Elephant RAT, 🇧🇷 SmartRAT ClickFix, 🐧 Showboat malware, 🔑 Kodak deadline"
date: 2026-06-18
tags: ["fortibleed","fortinet","supply-chain","mastra","npm","dropping-elephant","smartrat","clickfix","showboat","shinyhunters","kodak","ransomware","cve-2026-39808","cve-2026-54420","bod-26-04","kimsuky","iran"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "FortiBleed exposes 73,000+ Fortinet VPN credentials across 194 countries — verify your domain. Mastra AI framework npm supply chain attack backdoors 141 packages via easy-day-js. Dropping Elephant evolves in-memory RAT with AMSI bypass. AI-generated ClickFix campaign delivers SmartRAT banking malware targeting Brazil. Showboat Linux framework targets Middle East telcos since 2022. Kodak confirms breach as ShinyHunters June 18 deadline arrives. CISA LiteSpeed cPanel BOD 26-04 deadline today."
---
# Daily Threat Intelligence Digest — June 18, 2026

*78 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] FortiBleed — 73,000+ Fortinet VPN Credentials Exposed Across 194 Countries, Verified as Authentic**

Security researcher Bob Diachenko discovered an exposed server containing what appears to be a database of Fortinet/FortiGate VPN credentials for **73,932 firewall URLs** across 194 countries — approximately 50% of all internet-facing FortiGate devices globally. Hudson Rock independently confirmed the dataset covers **21,632 unique domains** including Chevron, Samsung, Foxconn, Comcast, AT&T, Mercedes-Benz, Toyota, Siemens, Accenture, and government agencies. Kevin Beaumont independently verified multiple credentials as authentic and confirmed the data appears recent, distinct from the 2025 Belsen Group leak. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fortibleed-leak-exposes-fortinet-vpn-credentials-for-73-000-devices/); [DoublePulsar](https://doublepulsar.com/fortibleed-75k-fortinet-firewalls-have-admin-passwords-cracked-60299faa65f8)]

The attackers — assessed as a Russian-speaking multi-operator group — allegedly conducted **~1.16 billion credential attempts against 320,777 FortiGate targets** plus 2.1 billion against 163,650 Microsoft SQL Server systems, using a 45-GPU Hashtopolis cluster. They intercepted SSL VPN authentication hashes from exported Fortinet configs, cracked them, and used recovered credentials for lateral movement into Active Directory environments. Multiple orgs across Japan, Taiwan, Vietnam, Iraq, and Turkey were fully compromised, including a Turkish NATO defense contractor from which classified documents were allegedly stolen. Fortinet's statement characterizes the data as re-shared from previous incidents and brute-force campaigns, not linked to a new vulnerability. Hudson Rock has published a free domain lookup tool. [[Hudson Rock](https://www.hudsonrock.com/blog/fortibleed-75000-fortinet-firewalls-compromised-global-enterprises-exposed-claim-your-ethical-disclosure)]

**Recommended actions:** Immediately rotate VPN admin credentials, enforce MFA on all FortiGate admin accounts, review gateway logs for suspicious auth patterns, and **do not expose the FortiGate management interface to the internet** — a majority of affected devices had their management interface publicly accessible.

---

**[UPDATE] FortiSandbox Zero-Days (CVE-2026-39808, CVE-2026-39813, CVE-2026-25089) — Active Exploitation Continues, 13 Sources Across 9 Countries**

Attackers continue active exploitation of three critical pre-auth vulnerabilities in Fortinet's FortiSandbox platform (patched April 14, June 9). Defused observed **49 exploitation events from 13 distinct IPs** originating from China, South Korea, Taiwan, India, Singapore, Germany, Netherlands, Canada, and Bulgaria over six days. Multiple independent operators, not a single campaign — exploits function together for pre-auth RCE, privilege escalation, and arbitrary command execution. The sandbox is a high-value target as it ingests from and connects to other Fortinet devices across the security architecture. CISA has not yet added these to KEV despite flagging 26 other Fortinet flaws since 2021. *Previously covered June 16.* [[CyberScoop](https://cyberscoop.com/fortinet-fortisandbox-vulnerabilities-exploits/)]

---

**[NEW] Mastra AI Framework npm Supply Chain Attack — easy-day-js Backdoors 140+ Packages, Postinstall Drops RAT Payload**

Attackers compromised the **@mastra npm organization** and silently added **easy-day-js** (a typosquatted copy of the legitimate `dayjs` date library) as a dependency across **141 packages** in an 88-minute window on June 17. Mastra is a popular open-source AI agent framework — `@mastra/core` has 918K weekly npm downloads. The malicious `postinstall` hook executes automatically during `npm install` without the application needing to import the package, downloading and running a second-stage RAT from attacker-controlled infrastructure. [[Sonatype](https://www.sonatype.com/blog/easy-day-js-targets-mastra-dependency-attacks-grow); [Aikido](https://www.aikido.dev/blog/over-140-popular-mastra-npm-packages-hit-by-supply-chain-attack)]

This continues the pattern established by the Axios compromise and Atomic Arch campaign: trusted packages used as delivery vehicles for malicious dependencies. **Any host where the affected packages were installed should be treated as compromised** — credentials rotated, lockfiles regenerated from known-good versions, and developer workstations, CI runners, and build agents investigated for persistence mechanisms. [[StepSecurity](https://www.stepsecurity.io/blog/mastra-npm-packages-compromised-using-easy-day-js)]

---

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Kodak Confirms Breach as ShinyHunters' June 18 Leak Deadline Arrives**

Kodak confirmed to BleepingComputer that an unauthorized third party accessed company data after the **ShinyHunters** extortion group claimed **2.2 million records** (customer PII and corporate data) and threatened to leak by **June 18** unless paid. The company is working with law enforcement and external incident responders. This continues ShinyHunters' accelerating campaign: following the Oracle PeopleSoft zero-day campaign (100+ orgs), American Tower (5.2M records with cell tower gate codes), Madison Square Garden (26M records), and the Council of Europe (297 GB claimed). As of publishing, the Kodak data has not appeared on public leak sites — the deadline is today. [[SecurityWeek](https://www.securityweek.com/kodak-admits-data-breach-after-shinyhunters-hack-claims/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/kodak-confirms-data-breach-claimed-by-shinyhunters-extortion-gang/); [Malwarebytes](https://www.malwarebytes.com/blog/news/2026/06/kodak-confirms-breach-as-shinyhunters-leak-threat-reaches-deadline)]

---

**[NEW] Dropping Elephant Deploys Heavily Reworked In-Memory RAT — Rapid7 Details AMSI-Bypassing Donut Shellcode Chain**

Rapid7 documented an evolved **Dropping Elephant** (PRC-linked APT) campaign using a China energy-sector contract lure (GRES-3 pump project) to deliver a significantly reworked RAT through a multi-stage attack chain: malicious LNK → PowerShell downloader → DLL side-loading via legitimate **Fondue.exe** → AES-decrypted Donut shellcode → in-memory RAT. The final implant patches **AMSI, WLDP, and ETW** in-process before execution, uses control-flow flattening and Salsa20-encrypted C2 fields, and supports directory listing, file download/execute, screen capture, and shell execution. Despite heavy re-engineering, code-level comparison with 2025 samples confirms shared lineage. Defenders should hunt for Fondue.exe loading APPWIZ.cpl from `C:\Users\Public\` or a scheduled task named `GoogleErrorReport` running every minute. [[Rapid7](https://www.rapid7.com/blog/post/tr-malware-tracking-dropping-elephant-tradecraft-china-themed-loader-chain)]

---

**[NEW] Showboat Malware: Linux Post-Exploitation Framework Targeting Middle East Telecoms Since 2022 — Zero AV Detection Until April 2026**

Lumen's Black Lotus Labs disclosed **Showboat**, a modular Linux x86-64 post-exploitation framework active since mid-2022, used exclusively against Middle East telecommunications companies. The malware achieved **zero detection across 65 AV engines** and remained fully undetected until April 2026. It is attributed with moderate-to-high confidence to PRC-backed threat actors. Showboat uses XOR encryption with hardcoded keys, disguises beacon data inside PNG image fields to evade network detection, and supports standard RAT capabilities including file transfers, directory manipulation, and long-term persistence. [[Malware.News/Picus](https://malware.news/t/showboat-malware-targeting-middle-east-telecom-firms-since-2022/107962#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] AI-Generated ClickFix Campaign Delivers SmartRAT Banking Malware — Zscaler Details 30+ C2 Commands, QR Code Swap Attacks**

Zscaler ThreatLabz analyzed a **ClickFix** campaign generated with AI website builders, impersonating a Brazilian bank (cartaobb[.]com) to deliver **SmartRAT** (aka Banana RAT), a PowerShell-based banking trojan. The infection chain: fake CAPTCHA → copy-to-clipboard PowerShell command → full-screen fake BSOD that traps the victim → multi-stage PowerShell dropper → AES-encrypted RAT. SmartRAT supports 30+ C2 commands including keylogging, screen capture, fake bank-branded overlays for 8 major Brazilian banks, **QR code interception/swap** (replaces legitimate banking QR codes with attacker-controlled ones), credential harvesting, file exfiltration, and complete remote control. The C2 panel had severe client-only authentication — any user could access it by setting `localStorage` values. Notably, AI tools generated both the phishing page and the C2 panel; the C2 panel's AI provenance is visible in verbose emoticon-laced comments and insecure deployment. [[Zscaler/Malware.News](https://malware.news/t/clickfix-campaign-generated-via-ai-delivers-smartrat/107984#post_1)]

---

**[NEW] Crypto Clipper Uses Tor, Worm-Like USB Propagation, and EVAL-Based RCE — Microsoft Security Blog Analysis**

Microsoft Threat Intelligence published an analysis of a **crypto clipper** active since February 2026 that uses a bundled Tor proxy for C2 routing, worm propagation via USB .lnk shortcuts, and clipboard monitoring for cryptocurrency seed phrases/private keys. Uniquely, the C2 can return an `EVAL` command that executes arbitrary JScript code at runtime (remote code execution). The malware uses dual-component architecture (worm + stealer), PyArmor-obfuscated Python installer, and Tor SOCKS5 proxy at localhost:9050. **Hunting signals:** WScript spawning curl, localhost:9050 activity, clipboard surveillance patterns, and .lnk propagation on removable media. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/)] via [[Malware.News](https://malware.news/t/crypto-clipper-uses-tor-and-worm-like-propagation-for-persistence-and-control/108000#post_1)]

---

## 🛡️ Defense & Detection

**[NEW] RMM Abuse Surge — Red Canary's Detection Guide for 8 Remote Monitoring Tools Abused by Threat Actors**

Red Canary documents the accelerating abuse of legitimate **remote monitoring and management (RMM)** tools — **ScreenConnect, NetSupport Manager, SimpleHelp, PDQ Connect, iDrive RemotePC, Syncro, Atera, ITarian, and QuickAssist** — by ransomware groups and financially motivated attackers. Key findings: adversaries often use one free-trial RMM to deploy a second, more permanent RMM; multiple RMMs on a single host are common (observed: 4 concurrent tools); attackers use cracked license keys, renamed binaries in non-standard paths, and MSIExec side-loading to evade EDR. The core detection shift: from "is this binary malicious?" to "is this RMM behavior authorized?" [[Red Canary](https://redcanary.com/blog/security-operations/rmm-detection/)]

---

**[NEW] Attackers Actively Exploiting Gravity SMTP Plugin Vulnerability in WordPress Ecosystems**

Wordfence reported active exploitation of a sensitive information exposure vulnerability in the **Gravity SMTP** WordPress plugin. Attackers are exploiting the flaw to read email configuration data, potentially exposing SMTP credentials and email traffic. This adds to the growing targeting of WordPress plugin ecosystems, following the recent OptinMonster CDN supply-chain attack (1.2M sites, covered June 16). [[Wordfence via Malware.News](https://malware.news/t/attackers-actively-exploiting-sensitive-information-exposure-vulnerability-in-gravity-smtp-plugin/107980#post_1)]

---

## 📋 Policy & Industry News

**[NEW] GitHub Dismissed Security Reports on Design Flaws Now Exploited by Shai-Hulud Supply-Chain Worm**

Deep Specter Research submitted two formal vulnerability reports to GitHub's HackerOne disclosure channel identifying design flaws in the GitHub platform that they say are enabling variants of the **Shai-Hulud/Miasma** supply-chain worm. GitHub closed both reports without action. The researchers now say those same flaws are being actively exploited to compromise packages and developer accounts globally. This echoes a pattern where platform-level vulnerabilities in code hosting and CI/CD infrastructure are enabling the next generation of software supply chain attacks faster than the industry patches for them. [[DataBreaches.net via Malware.News](https://malware.news/t/github-dismissed-security-reports-on-flaws-now-exploited-by-supply-chain-worm-researchers-say/107958#post_1)]

---

**[NEW] CISA LiteSpeed cPanel Patch Deadline Today — BOD 26-04 First Three-Day Deadline**

Today, **June 18**, is the compliance deadline for federal agencies under CISA's new BOD 26-04 directive to patch **CVE-2026-54420** (LiteSpeed cPanel plugin, root escalation on shared hosting). This was the first vulnerability subject to the expedited three-day remediation timeline — a significant shift from traditional 7/14/30-day windows. *Previously covered June 16.* [[CISA/SecurityWeek](https://www.securityweek.com/joomla-litespeed-vulnerabilities-exploited-in-attacks/)]

---

## ⚡ Quick Hits

- **CISA now has full Mythos Preview access** — Multiple sources report CISA has been granted full preview access to Anthropic's Mythos model following the June 13 export control directive. This suggests government-access terms are being negotiated alongside the public model recall. [[Malware.News](https://malware.news/t/cisa-now-has-full-mythos-preview-access-people-familiar-say/107997#post_1)]
- **US officials warn Iran cyber threat persists despite preliminary nuclear deal** — US intelligence assesses Iran-linked groups continue targeting critical infrastructure and US allies, regardless of diplomatic progress. [[Malware.News](https://malware.news/t/us-officials-see-iran-cyber-threat-persisting-despite-preliminary-deal/107973#post_1)]
- **Roblox developers losing entire games to session token theft** — Attackers pose as recruiters on Discord, persuade developers to run Python infostealer packages ("robase"), then steal authenticated Roblox sessions, group accounts, games, and in-platform currency. Recovery has required media pressure. [[Malwarebytes/Malware.News](https://malware.news/t/roblox-developers-are-losing-entire-games-to-malware-attacks/107993#post_1)]
- **SailPoint to acquire Entro (~$200M), 1Password acquires Apono (~$250-300M)** — Two major identity security M&A deals announced: SailPoint adds Entro's non-human identity security capabilities; 1Password adds Apono's just-in-time privileged access management. [[SecurityWeek](https://www.securityweek.com/sailpoint-to-acquire-entro-in-reported-200-million-deal/); [SecurityWeek](https://www.securityweek.com/1password-acquires-apono-in-reported-250m-300m-deal/)]
- **Rockwell Automation patches vulnerabilities in ICS controllers and software** — Multiple patches released for ControlLogix and other industrial control products. Details behind SecurityWeek paywall. [[SecurityWeek](https://www.securityweek.com/rockwell-automation-patches-vulnerabilities-in-ics-controllers-and-software/)]
- **Kimsuky LNK malware targets energy/economic analysts** — Korean-language analysis continues documenting Kimsuky's persistent LNK-based phishing campaigns targeting South Korean energy and economic analysis researchers. [[Malware.News](https://malware.news/t/kimsuky-260506-pdf-lnk/107974#post_1)]
