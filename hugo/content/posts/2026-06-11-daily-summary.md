---
title: "Ivanti Sentry exploited, Exchange zero-day patched, ShinyHunters hits 100+ orgs, Miasma source leaked, JDY expands, BOD 26-04, Langflow exploited"
date: 2026-06-11
tags: ["ivanti","exchange","shinyhunters","miasma","jdy","cisa","langflow","updraftplus","thegentlemen","peoplesoft","bod-26-04"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Ivanti Sentry CVE-2026-10520 exploited within hours of patch. Exchange Server zero-day CVE-2026-42897 actively exploited. ShinyHunters hits 100+ PeopleSoft orgs including Nottingham University (454K affected). Miasma worm source code open-sourced with destructive dead-man switch. CISA BOD 26-04 mandates 3-day patch cadence. Langflow CVE-2026-5027 exploited in attacks on 7K exposed instances. Apply patches urgently for Ivanti, Exchange, Langflow, and UpdraftPlus."
---

# Daily Threat Intelligence Digest — June 11, 2026

*79 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit detected no critical gaps beyond feed coverage. tl;dr sec skipped — Thursday, latest issue not yet live. Prior digests: June 6–10, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Ivanti Sentry CVE-2026-10520 (CVSS 10.0) — Patched Tuesday, Exploited Wednesday, Most Exposed Instances Already Backdoored**

Just one day after Ivanti released patches for a maximum-severity OS command injection in Sentry secure mobile gateways, the Shadowserver Foundation reported that attackers had already backdoored virtually every reachable exposed instance. CVE-2026-10520 allows unauthenticated remote code execution as root via a crafted request. Shadowserver identified 19 vulnerable instances in its scans, with at least 2 confirmed backdoored, and noted "if you have not patched now you are most likely compromised" — Ivanti's own advisory still states "no evidence of exploitation at time of disclosure" as of this writing. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/max-severity-ivanti-sentry-vulnerability-now-exploited-in-attacks/); [Malware.News](https://malware.news/t/ivanti-sentry-s-cve-2026-10520-enables-root-rce/107736#post_1)]

**Prior context (June 10):** Ivanti patched CVE-2026-10520 on Tuesday alongside an auth bypass (CVE-2026-10523, CVSS 9.9). CISA has flagged 34 Ivanti CVEs as actively exploited. Every exposed Sentry instance should be treated as compromised — rebuild from known-good firmware.

---

**[NEW] Microsoft Patches Actively Exploited Exchange Server Zero-Day (CVE-2026-42897) — XSS in Outlook Web Access, CISA KEV Since May 15**

Microsoft shipped emergency security updates for Exchange Server 2016, 2019, and Subscription Edition (SE) to fix CVE-2026-42897, a high-severity spoofing/XSS vulnerability in Outlook Web Access that was actively exploited before a patch existed. An unauthenticated attacker can execute arbitrary JavaScript in the victim's browser context by sending a specially crafted email — no user interaction beyond opening the message in OWA. CISA added the flaw to its KEV catalog on May 15, giving federal agencies two weeks to patch. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-patches-exchange-server-zero-day-exploited-in-attacks/); [SecurityWeek](https://www.securityweek.com/microsoft-patches-exploited-exchange-server-vulnerability/)]

Microsoft had deployed an automatic temporary mitigation via the Exchange Emergency Mitigation Service (EEMS) in mid-May. The June 2026 security updates provide a permanent fix. Twenty Exchange Server CVEs have been added to CISA's KEV catalog over the past five years, with ransomware gangs exploiting 14 of them.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] ShinyHunters PeopleSoft Data Theft Campaign Hits 100+ Organizations — Nottingham University Breach Confirmed, 454,600 Students Exposed**

ShinyHunters is conducting a widespread data theft campaign targeting Oracle PeopleSoft instances, claiming 300 compromised instances across more than 100 organizations worldwide. The threat actor told BleepingComputer they are using a "gadget chain" of old and zero-day vulnerabilities. Researcher "Michael R" found exposed infrastructure including MeshCentral agents, credential spray scripts, and ransom note deployment tooling. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/oracle-peoplesoft-servers-hacked-in-shinyhunters-data-theft-attacks/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/nottingham-university-data-breach-affects-over-450-000-students/)]

**Confirmed victim: University of Nottingham** — 454,600 current and former students affected, including names, addresses, phone numbers, ethnicities, passport numbers, disabilities, and fee payment data. The university confirmed the breach and reported it to the UK ICO. Have I Been Pwned added the data. [[SecurityWeek](https://www.securityweek.com/university-of-nottingham-confirms-breach-after-hackers-leak-data/)]

**IOCs:** 142.11.200[.]186–190, 108.174.202[.]99, 176.120.22[.]24. The threat actor's MeshCentral staging servers and .bash_history files revealed SSH brute-force scripts targeting PeopleSoft admin accounts. Organizations running PeopleSoft should audit logs for connections from these IPs immediately.

---

**[UPDATE] JDY Botnet Expands to 1,500+ Bots — Volt Typhoon-Linked Recon Network Targets US Military Infrastructure**

Black Lotus Labs by Lumen documented significant expansion of the JDY botnet, a China-linked distributed scanning and fingerprinting network tied to Volt Typhoon. JDY has grown from 650 bots (January 2024) to over 1,500 compromised SOHO and IoT devices, with a "clear focus" on US military and associated networks. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/china-linked-jdy-botnet-expands-targeting-of-us-military-networks/)]

**Capabilities:** TCP/UDP/ICMP scanning, TLS certificate harvesting, service fingerprinting via downloadable rule sets, and raw SYN scanning (source port 19000) when root privileges are available. The botnet is controlled via hidden Tor services and the open-source Platypus framework. Compromised devices include Cisco, Araknis, Ubiquiti, DrayTek, and Hikvision hardware across MIPS/MIPSEL architectures. The operators rapidly operationalize reconnaissance output against newly disclosed vulnerabilities — observed targeting CVE-2026-35616 (FortiClient EMS) shortly after disclosure.

---

**[UPDATE] Miasma Worm Source Code Open-Sourced on GitHub — Dead Man Switch Destroys Victims' Files on Token Revocation, 5-Stage Build Pipeline Evades Signatures**

The Miasma credential-stealing framework was deliberately open-sourced on GitHub via numerous compromised developer accounts, each hosting a repo named "Miasma-Open-Source-Release." SafeDep's analysis reveals new details about the worm that previously hit 73 Microsoft repositories (covered June 8). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/the-miasma-worm-source-code-briefly-leaked-on-github/)]

**New details:**
- **Dead man switch:** Installed on Linux (systemd user service) and macOS (LaunchAgent) — monitors stolen GitHub token validity every 60 seconds. If revoked, executes `rm -rf ~/; rm -rf ~/Documents`, recursively deleting home directories. Active for up to 72 hours.
- **5-stage build pipeline:** Per-file AES-256-GCM encryption of embedded assets, randomized string obfuscation, JavaScript obfuscation, and a self-extracting loader with three layers of encryption. Each build produces a unique sample — signature-based detection is ineffective.
- **No C2 infrastructure required:** Operates entirely through GitHub as its command channel.
- **AI coding tool targeting:** Poisons configurations for Claude, Gemini, Cursor, Copilot, Kiro, and Cline.

The open-sourcing follows the same pattern as Shai-Hulud's leak, which led to Miasma's creation and a surge in supply-chain attacks. The SDK-ification of worm frameworks is accelerating the democratization of supply-chain compromise.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Langflow CVE-2026-5027 Exploited — Path Traversal in AI Dev Platform, 7,000 Exposed Instances, Unauthenticated Exploitation Confirmed**

Attackers are actively exploiting CVE-2026-5027 (high-severity), a path traversal vulnerability in Langflow's file upload endpoint (`POST /api/v2/files`). The filename parameter is unsanitized, allowing `../` sequences to write arbitrary files. Langflow enables unauthenticated auto-login by default — a single request yields a valid session token, no credentials required. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/path-traversal-flaw-in-ai-dev-platform-langflow-exploited-in-attacks/)]

Discovered by Tenable (reported January 2026, publicly disclosed March 27 after no vendor response). Fixed in langflow-base 0.8.3 and Langflow 1.9.0. VulnCheck honeypots confirmed active exploitation dropping test files. Censys scans identified ~7,000 publicly exposed instances (historical, 12-month window). Recommended version: 1.10.0. Previous Langflow flaws (CVE-2026-0770, CVE-2026-21445, CVE-2026-33017) have also been exploited, including by MuddyWater (Iranian APT).

---

**[UPDATE] CISA BOD 26-04: Federal Agencies Must Patch Critical Vulns in 3 Days — "Patch Smarter, Not Harder" Directive Official**

CISA's binding operational directive BOD 26-04 is now official, requiring federal agencies to prioritize vulnerabilities based on four criteria: public exposure, automatable exploitation, system takeover potential, and active exploitation evidence. Vulnerabilities meeting all four criteria must be patched within **3 days** with mandatory forensic triage. [[CyberScoop](https://cyberscoop.com/cisa-vulnerability-remediation-directive-bod-26-04/); [Malware.News](https://malware.news/t/cisa-directive-revamps-how-agencies-prioritize-vulnerable-systems/107761#post_1)]

The directive is driven by AI-accelerated exploit timelines — per Verizon's 2026 DBIR, only 26% of KEV-listed vulns were fully remediated in 2025, down from 38% the year prior, with median resolution time rising to 43 days. CISA estimates that at one large agency, just 1% of vulns would fall into the 3-day window, while 60% could be deferred to the next upgrade cycle. Private sector adoption is encouraged but not mandated. This joins similar guidance from India and the UK. [[Qualys](https://blog.qualys.com/qualys-insights/2026/06/10/how-federal-agencies-can-activate-a-risk-operations-center-roc-to-meet-cisa-bod-26-04)]

---

**[NEW] UpdraftPlus CVE-2026-10795 — Critical Auth Bypass in 3M+ WordPress Installs, RCE via Failed RSA Decryption Collapse**

Wordfence disclosed a critical unauthenticated authentication bypass in UpdraftPlus (3M+ active installs) affecting all versions ≤ 1.26.4. The vulnerability (CVE-2026-10795, CVSS 8.1) affects sites previously connected to UpdraftCentral — when the RSA decryption of the RPC message key fails, `phpseclib` returns `false` which passes to `Rijndael::setKey()`, collapsing to a deterministic all-zero AES-128 key. An attacker can forge arbitrary RPC commands as the connected admin, including uploading and activating a malicious plugin for full PHP/OS command execution. [[Wordfence](https://www.wordfence.com/blog/2026/06/critical-unauthenticated-authentication-bypass-vulnerability-patched-in-updraftplus-wordpress-plugin/); [Malware.News](https://malware.news/t/critical-unauthenticated-authentication-bypass-vulnerability-patched-in-updraftplus-wordpress-plugin/107751#post_1)]

Patched in version 1.26.5 (released June 5). Wordfence Premium users received a firewall rule on June 3; free users get protection July 3.

---

## 🛡️ Defense & Detection

**[NEW] GitHub Announces npm v12 Security Changes — Code Execution During Install Requires Explicit Approval**

GitHub announced that npm v12 (expected next month) will fundamentally change how dependencies are installed: `preinstall`/`install`/`postinstall` scripts from dependencies will not run unless explicitly approved; Git repository dependencies and remote URL tarballs will no longer resolve automatically. Each of these behaviors has been abused in recent supply-chain attacks, including the Shai-Hulud campaign. npm 11.16.0+ shows warnings for workflows that will break under v12. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/github-announces-npm-security-changes-to-tackle-supply-chain-attacks/)]

---

**[NEW] Infostealers in 2026: 11.1 Million Infected Devices, 3.3 Billion Stolen Identities in Circulation — MaaS Subscriptions From $60/Month**

Flashpoint's analysis documents the infostealer ecosystem's transformation into an industrial-scale credential theft machine. 2025's top stealers (Lumma, Acreed, Rhadamanthys) were displaced in early 2026 — **Vidar surged from 4th to 73% of infected hosts** while Lumma collapsed to 1.1% market share. Stolen credentials provide attackers authorized access, bypassing most security defenses. The injection chain from stealer infection to ransomware deployment is often direct and short. [[SecurityWeek](https://www.securityweek.com/infostealers-turn-millions-of-devices-into-credential-theft-machines/)]

---

## 📋 Policy & Industry News

**[NEW] Warner Proposes Critical Infrastructure Cyber Overhaul as AI Threats Rise**

Senate Intelligence Committee Vice Chairman Mark Warner introduced the Combat Emerging Threats to Critical Infrastructure Act, requiring CISA to update sector-specific cybersecurity plans for all 16 critical infrastructure sectors within one year, with biennial reassessments. Some sector plans have not been updated in over a decade. The bill explicitly accounts for AI-enabled hacking, deepfakes, and quantum computing threats to encryption in financial services. [[Malware.News/Nextgov](https://malware.news/t/warner-proposes-overhaul-of-critical-infrastructure-cyber-plans-as-ai-threats-rise/107728#post_1)]

---

**[NEW] Krebs on Security Identifies The Gentlements Ransomware Admin as 36-Year-Old Russian IT Marketing Executive**

Brian Krebs traced the administrator of The Gentlemen ransomware group (second most active gang by victim count in 2026) to **Alexander Andreevich Yapaev**, a 36-year-old from Izhevsk, Russia, who lists himself as head of B2B marketing at Uralenergo Udmurtia. Operating under aliases Hastalamuerte and Zeta88 across cybercrime forums since 2019, Yapaev offers affiliates a 90/10 revenue split — the industry's most generous — driving the gang's rapid growth (332 published victims since mid-2025). [[Krebs on Security](https://krebsonsecurity.com/2026/06/who-runs-the-ransomware-group-the-gentlemen/); [Malware.News](https://malware.news/t/who-runs-the-ransomware-group-the-gentlemen/107733#post_1)]

---

## ⚡ Quick Hits

- **[NEW] RoguePlanet Anatomy Published** — Full technical breakdown of Nightmare Eclipse's Microsoft Defender race-condition zero-day. Validated on fully patched Windows 10/11. Server SKUs also vulnerable but PoC not adapted. [[SecurityWeek](https://www.securityweek.com/new-windows-zero-day-exploit-rogueplanet-released/); [Malware.News](https://malware.news/t/rogueplanet-anatomy-of-the-nightmare-eclipse-microsoft-defender-zero-day/107772#post_1)]
- **[NEW] US Seizes 13 China-Linked Domains Targeting Security Clearance Holders** — FBI/DOJ takedown of fake consulting firms using AI-generated photos and stolen identities to recruit US officials and military personnel with classified access. [[Nextgov/FCW via Malware.News](https://malware.news/t/us-seizes-alleged-china-linked-sites-targeting-security-clearance-holders/107763#post_1)]
- **[NEW] 67 Million Thais Exposed in Massive Data Leak** — Parliament launches probe after a database containing personal data of 67M Thai citizens was compromised. Scope suggests government or telecom-sector origin. [[Malware.News](https://malware.news/t/67-million-thais-exposed-in-massive-data-leak-parliament-launches-probe/107766#post_1)]
- **[NEW] Suspected Russian Hacker Denis Obrezko Arrested, Charged in Boston** — 36-year-old arrested in Thailand, extradited to US, charged with facilitating cyberattacks by Russia-aligned group against US companies. [[DataBreaches.net via Malware.News](https://malware.news/t/suspected-russian-hacker-arrested-and-charged-in-the-united-states/107771#post_1)]
- **[NEW] Chelan County Enters Third Week of Malware Disruptions** — No recovery timeline issued following Memorial Day weekend incident affecting county systems. [[DataBreaches.net via Malware.News](https://malware.news/t/wa-chelan-county-enters-third-week-of-disruptions-with-no-recovery-timeline/107770#post_1)]
- **[NEW] FIFA World Cup 2026 Scams Already Active** — FBI PSA: 40+ fraudulent domains including typosquatted ticket sites and fake recruitment portals. Cyble confirmed many still operational. [[Cyble via Malware.News](https://malware.news/t/fifa-world-cup-2026-scams-are-already-active-fake-domains-phishing-sites-and-how-to-stay-safe/107725#post_1)]
- **[NEW] Critical HVAC/UPS Vulnerabilities Could Disrupt Data Centers** — Claroty discovered auth bypass + RCE in Vertiv UPS network cards and Trane Tracer SC+ HVAC controllers. Patched by both vendors. [[SecurityWeek](https://www.securityweek.com/critical-hvac-and-ups-vulnerabilities-could-let-hackers-disrupt-data-centers/)]
- **[NEW] Free Spotify Premium TikTok Scams Spread Vidar Infostealer** — ReversingLabs documents two campaigns using short-form videos to trick users into pasting PowerShell commands that deliver Vidar on Windows. [[Malwarebytes via Malware.News](https://malware.news/t/free-spotify-premium-hacks-on-social-media-are-spreading-infostealers/107746#post_1)]
- **[NEW] Microsoft Fixes BitLocker Recovery Bug on Windows Server 2025** — KB5094125 resolves a known issue causing servers to boot into BitLocker recovery after April 2026 security updates. IT admins can also use KIR as compensating control. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-fixes-bitlocker-recovery-bug-on-windows-server-2025/)]
- **[NEW] OpenAI Detects Chinese Influence Operation Using ChatGPT to Stoke Data Center, Tariff Debates** — Two clusters of China-linked activity creating AI-generated imagery and social media comments. Rated low-impact (1-2 on Bookings breakout scale) by OpenAI's threat intel team. [[CyberScoop](https://cyberscoop.com/openai-china-influence-campaign-chatgpt/)]

---

*79 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit detected no critical gaps beyond feed coverage. tl;dr sec skipped — Thursday, latest issue not yet live. Prior digests: June 6–10, 2026. Sources include BleepingComputer, SecurityWeek, CyberScoop, Krebs on Security, Wordfence, Malware.News, SafeDep, Black Lotus Labs (Lumen), Flashpoint, Qualys, Tenable, VulnCheck, Shadowserver, Claroty, DataBreaches.net, Nextgov/FCW, Cyble, Malwarebytes, ReversingLabs, and independent researchers.*