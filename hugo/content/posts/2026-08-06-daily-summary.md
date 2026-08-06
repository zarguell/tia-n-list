---
title: "🔴 TeamCity RCE Under Active Attack, 🎯 Snowflake Hacker Pleads Guilty, ⚠️ Cisco CVSS 10.0 FMC Flaw, 🎯 TeamPCP Traced to 2020, 🎯 COLDCARD Scam Wave, 📋 OT Tax Push"
date: 2026-08-06
tags: ["threat-intelligence","cisa-kev","jetbrains-teamcity","teampcp","snowflake","cisco","clickfix","phishing","ransomware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "JetBrains TeamCity CVE-2026-63077 added to CISA KEV under active exploitation; Snowflake extortionist Connor Moucka pleads guilty; Cisco patches a CVSS 10.0 FMC auth bypass; Oligo traces TeamPCP back to 2020; Proofpoint documents COLDCARD-themed ScreenConnect phishing."
---

# Daily Threat Intelligence Digest — August 6, 2026

25 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking. External CVE monitoring surfaced the August 5 CISA KEV addition — JetBrains TeamCity (CVE-2026-63077), now under confirmed active exploitation — before it reached the feeds.

---

## 🔴 Critical Threats & Active Exploitation

### [UPDATE] JetBrains TeamCity CVE-2026-63077 Now Under Active Exploitation — CISA Adds to KEV, Federal Deadline August 8

*Initial disclosure covered Jul 31 (no exploitation known at that time). New today: CISA added CVE-2026-63077 to the KEV catalog on August 5, and threat actors have begun exploiting the flaw.*

CISA has formally confirmed active exploitation of **CVE-2026-63077** (CVSS 9.8), the critical **deserialization of untrusted data (CWE-502)** flaw in **JetBrains TeamCity On-Premises** that gives unauthenticated attackers **remote code execution via the agent polling protocol** — bypassing authentication and running arbitrary OS commands with the privileges of the TeamCity server process. Roughly a week after JetBrains' disclosure (which reported no exploitation), CISA added it to the Known Exploited Vulnerabilities catalog on **August 5** with a **BOD 26-04 remediation deadline of August 8** for federal agencies. SecurityWeek reports hackers have started exploiting the flaw; no public details of the attacks exist yet.

- **Affected:** all TeamCity On-Premises versions. Patched in **2025.11.7** and **2026.1.3**; a security patch plugin is available for versions 2017.1+.
- **Why it matters:** TeamCity is a CI/CD server — a compromised build pipeline means source code theft, stored credentials, and malicious code injected into software releases. This is the second actively exploited build-platform flaw in a month (after N-able N-central), and the third critical KEV entry this week.
- **Action:** Upgrade or install the patch plugin immediately; treat any unpatched, internet-reachable TeamCity instance as compromised and audit for unauthorized agents, build-config changes, and credential access. No public exploit details means the window to patch ahead of weaponization is open now.

**Sources:** [SecurityWeek](https://www.securityweek.com/hackers-start-exploiting-recent-jetbrains-teamcity-vulnerability/) · [The Hacker News](https://thehackernews.com/2026/08/cisa-flags-teamcity-cve-2026-63077-rce.html) · [JetBrains advisory](https://blog.jetbrains.com/teamcity/2026/07/cve-2026-63077/) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### [UPDATE] KEV Patch Clock Ticking: N-central Deadline Is Today, Langflow and Tomcat Due Tomorrow

*Aug 4 KEV batch fully covered yesterday. New today: BleepingComputer confirms the wave, and the BOD 26-04 deadlines are now imminent — one is due today.*

The three KEV additions from the **August 4 batch** — **CVE-2026-9198** (IBM Langflow, CVSS 9.8, unauthenticated code injection/RCE on default deployments), **CVE-2026-34486** (Apache Tomcat EncryptInterceptor bypass), and **CVE-2026-18556** (N-able N-central auth bypass) — carry **BOD 26-04 due dates of August 7**. The companion N-central bypass **CVE-2026-18577** is due **today, August 6**. For federal agencies these are hard deadlines; for everyone else they mark the exploitation-confirmed floor. N-able's on-prem hotfix **2026.3.1.7** remains the only unaffected build; Langflow deployments should be treated as compromised if they were internet-exposed pre-patch.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-warns-of-hackers-exploiting-langflow-n-central-apache-tomcat-flaws/) · [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] Snowflake Extortion Mastermind Connor Moucka Pleads Guilty — Faces Up to 32 Years

**Connor Riley Moucka** (aka Alexander Moucka, "Waifu"), the 26-year-old Canadian at the center of the 2024 **Snowflake mass-compromise spree**, pleaded guilty to his role in breaching **at least 165 organizations' cloud accounts** and stealing data on **hundreds of millions of individuals** for extortion. Per the Justice Department, Moucka — arrested October 30, 2024 — **earned $495,000** extorting victims, selling stolen data, and in one case re-extorting a victim using data of a government official. He faces up to **32 years in prison**; co-defendant **John Erin Binns** (charged in connection with the same campaign) remains part of the case. Between February and October 2024, the pair stole credentials from Snowflake customer environments — many lacking MFA — and demanded ransoms from companies including Ticketmaster, AT&T, and Santander. One of the largest cyber-extortion cases of 2024 now moves to sentencing.

**Action:** This conviction is a reminder that the Snowflake credential-harvesting playbook (stolen employee credentials + no MFA on customer portals) is now a documented, prosecuted pattern — enforce MFA on all SaaS admin portals and audit for legacy credentials.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/canadian-pleads-guilty-to-snowflake-cloud-data-theft-attacks/) · [CyberScoop](https://cyberscoop.com/connor-moucka-guilty-snowflake-attack-spree/)

### [UPDATE] TeamPCP's Roots Go Back to 2020 — Oligo Links the ChainDrop Actor to TA-NATALSTATUS and IronErn

*ChainDrop npm worm covered in depth Aug 5. New today: Oligo Security research pushes TeamPCP's operational history back years and names prior aliases.*

The actor behind the year's biggest open-source supply-chain campaigns — including this week's **ChainDrop** worm (1,300+ packages, 2B monthly downloads) and the earlier Shai-Hulud waves — **has been active since at least 2020**, per Oligo Security. Oligo tied TeamPCP to activity tracked under **TA-NATALSTATUS and IronErn**, spanning 2020 to late 2025, via shared IPs, domains, a file server, and C2 infrastructure. The links emerged from the **ShadowRay 2.0** investigation: the late-2025 campaign that produced the **first self-propagating botnet running on hijacked AI infrastructure**. Oligo highlights the campaign's defining trait — **AI-accelerated payload evolution**, with malicious code adapting to target environments "at a speed we're not used to seeing," and notes TeamPCP publishes from an official GitHub account "not even trying to hide their identity." The finding implies TeamPCP was likely behind additional unattributed attacks.

**Action:** Treat TeamPCP as a standing supply-chain threat with years of infrastructure — block known domains, enforce dependency provenance checks, and monitor for AI-infrastructure botnet patterns (ShadowRay-class Ray/ML-framework exposure).

**Source:** [CyberScoop](https://cyberscoop.com/teampcp-long-active-history-2020-oligo-security/) · Oligo Security

### [UPDATE] COLDCARD Fear-Baiting Phishing Pushes ScreenConnect RAT — Fake "Security Audit" Scam Documented by Proofpoint

*COLDCARD RNG flaw and $88.6M Bitcoin theft covered Aug 3. New today: a phishing campaign weaponizes the incident's fear factor to install remote access software.*

Proofpoint has documented a phishing campaign exploiting the disclosed COLDCARD wallet vulnerability and suspected **$88.6M Bitcoin theft** to trick users into installing **ConnectWise ScreenConnect**. Emails spoofing COLDCARD (from `compliance@coldcardteamnews.com`, subject "Hardware audit now available") claim a coordinated security audit across all hardware revisions and direct victims to **coldcardcompliance.com**, a convincing COLDCARD clone with a live "Customer Service" chat staffed (per Proofpoint) by real operators who pressure hesitant victims through the install. The "Start Hardware Audit" button downloads **Coldcard_Diagnostic_Tool.bat** — a 25.7MB batch file that requests UAC elevation, decodes embedded payloads via certutil, installs a **ScreenConnect MSI**, and connects to the attacker's C2 at **activeretirementrelocation[.]com**, granting full remote access (data theft, crypto theft, potential ransomware deployment).

**Action:** No legitimate COLDCARD audit tool exists — ignore any email or site asking you to "verify" your device, and never run downloaded diagnostic tools for wallet security. Block the domain and C2; treat any victim device as fully compromised.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/coldcard-security-audit-phishing-attack-installs-remote-access-tool/) · Proofpoint

### [NEW] khunt Post-Exploitation Toolkit Lives Inside an Oracle Database — Huntress Documents Rare DB-Resident Attack

Huntress uncovered an attacker running the **khunt post-exploitation toolkit from inside an Oracle database** — a technique "rarely documented in the wild." The intrusion began with **SQL injection** through an unvalidated autocomplete search endpoint in a public-facing Java application running on Apache Tomcat (traffic traced to `178.162.151[.]229`). The attackers exploited Oracle's embedded JVM via `CREATE JAVA SOURCE` to **compile and store the toolkit as a database schema object**, executing it through SQL with no files on disk:

- **KhuntCmd** — launches `cmd.exe`, confirmed **SYSTEM-level** command execution via `whoami`
- **KhuntHash** — dumps Oracle's internal user table (usernames/password data)
- **KhuntFS/KhuntFS2** — file browsing, reading, search
- **KhuntT / KhuntUnzip** — install check and file extraction

The operators used KhuntCmd to copy the **SAM, SECURITY, and SYSTEM registry hives** (for offline credential recovery) and enumerate services. Huntress could not confirm exfiltration but assesses the hives were likely stolen for credential dumping.

**Action:** Database accounts used by public-facing applications must not have privileges to create Java sources or run administrative procedures; sanitize all application input. Hunt for `CREATE JAVA SOURCE`, `java_source` objects, and PL/SQL wrappers executing OS commands in Oracle DBs.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-run-khunt-post-exploitation-toolkit-from-oracle-database/) · Huntress

### [NEW] macOS ClickFix Campaign Adds a Server-Side Fingerprinting Gate — 250+ Domains Deliver AMOS Only to "Qualified" Macs

Microsoft Threat Intelligence documented a macOS **ClickFix campaign distributing infostealers (MacSync and Atomic Stealer/AMOS)** through a mass-produced family of algorithmically named domains — **250+ confirmed front-end domains** following a `file<word><word>` pattern (`filecopperbasket[.]sbs`, `filevelvettractor[.]sbs`, `apricotfilepoint[.]com`, etc.). The notable evolution: the operation **cloaked its lures behind a server-side browser-fingerprinting gate** (a Traffic Distribution System). Earlier, the malicious command sat in the served HTML; now a ~2.5KB profiling script collects browser/WebGL GPU/timezone/console signals and the server returns the "Download for macOS" lure **only to visitors matching a genuine macOS environment** — crawlers, sandboxes, and Windows browsers get blank pages or benign decoy sites. The chain ends with curl-piped-to-Terminal execution of AMOS, harvesting credentials, wallets, and keychains. Microsoft flags **macOS 26.4's paste-block warning** as a direct mitigation for this delivery class.

**Action:** Alert on Terminal sessions spawning curl/base64/osascript after web browsing; block the `file<word><word>` domain pattern and `/curl/<id>` staging paths; remind users no legitimate download requires pasting commands into Terminal.

**Source:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/08/05/macos-clickfix-campaign-learned-hide/)

### Ransom Cartel Creator Maksim Silnikau Sentenced to 16 Years

**Maksim Silnikau**, the 40-year-old Belarusian creator and administrator of the **Ransom Cartel** ransomware operation, was sentenced to **16 years in prison** for attacks on at least 18 companies worldwide. The DOJ says Silnikau (aliases "J.P. Morgan," "xxx," "lansky") built the operation in May 2021, recruited affiliates on underground forums, supplied stolen credentials and encryptors, and ran an affiliate portal handling negotiations and revenue shares. Ransom Cartel — which launched publicly in December 2021 and shares code lineage with **REvil** (likely built by a former member without full source access) — attempted to extort at least **$5.2M**, with confirmed losses over **$6.7M** across 18 victims, including a medical-technology startup disrupted for two months. Silnikau was arrested in Spain in July 2023, **fled while awaiting extradition**, and was recaptured crossing from Poland into Belarus before consenting to extradition.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/ransom-cartel-ransomware-creator-sentenced-to-16-years-in-prison/) · DOJ

---

## ⚠️ Vulnerabilities & Patches

### Cisco Ships Two Dozen Fixes — CVSS 10.0 FMC Auth Bypass, 9.9 SD-WAN Trio, IOS XE Command Injection

Cisco's Wednesday advisory batch covers roughly two dozen vulnerabilities, headlined by critical flaws with no known in-the-wild exploitation:

- **CVE-2026-20079 (CVSS 10.0)** — Secure Firewall Management Center (FMC) **authentication bypass** letting remote unauthenticated attackers execute scripts and gain **root** via crafted HTTP requests.
- **CVE-2026-20303 / 20304 / 20310 (CVSS 9.9 each)** — Catalyst SD-WAN: improper input validation, improper access control, and improper link resolution before file access.
- **CVE-2026-20272 (CVSS 9.8)** — IOS XE **command injection**; **CVE-2026-20267 (CVSS 9.0)** — IOS XE improper access control.
- **CVE-2026-20200 (CVSS 8.8)** — Integrated Management Controller (IMC): remote command execution with **public PoC code available**; affects UCS C-Series M7/M8 rack servers in standalone mode.

**Action:** Priority order: FMC auth bypass (unauthenticated, root) and the IMC flaw with public PoC; then SD-WAN/IOS XE. No exploitation reported yet — patch while the window is quiet.

**Source:** [SecurityWeek](https://www.securityweek.com/cisco-patches-critical-sd-wan-ios-xe-fmc-vulnerabilities/)

### The $50,000 Bixby Exploit Chain: Samsung Members → Samsung Account → Bixby "Capsules" → System-Level RCE

Researchers **Dimitrios Valsamaras (Microsoft)** and **Ken Gannon (Mobile Hacking Lab)** detailed at Black Hat a four-step chain — demonstrated at **Pwn2Own Ireland (October 2025)** for $50,000 against a Galaxy S25 — that achieves **system-level remote compromise** of Samsung phones:

1. **CVE-2025-21079** — a malicious link forces preinstalled **Samsung Members** to connect to an attacker website
2. **CVE-2025-58486** — forces **Samsung Account** to an attacker-controlled site
3. **CVE-2025-58487** — an XSS in Samsung Account opens **Bixby** via a special "side entrance" permission
4. The attacker then abuses **Capsules** — hidden background mini-servers Bixby normally exclusively controls — to exfiltrate data and reach **system** privileges, the highest level on a stock device, enabling RCE.

Samsung patched the apps in **November–December 2025**; the chain works on **older devices that haven't received the patches** and requires all targeted apps installed (preinstalled on flagship and most mid-range models).

**Action:** Ensure Samsung Members/Samsung Account apps are updated on all fleet and personal Galaxy devices; older or budget models are the residual risk.

**Source:** [SecurityWeek](https://www.securityweek.com/how-a-50000-exploit-chain-turned-bixby-against-samsung-phones/)

### Borrowing Windows Hello Keys: Researcher Shows PRT and Passkey Abuse Without a PIN — Detection Guidance Included

Researcher **Dirk-jan Mollema** (of ROADtools fame) published a deep dive on **Windows Hello for Business (WHFB) key abuse** — a consequence of the design Microsoft "left as-is." From a compromised low-privilege user session, an attacker can use the user's **TPM-backed WHFB key without PIN or biometrics** (via the Passport KSP / NCrypt interface, which works from cached data):

- **PRT theft:** sign a locally generated JWT with the WHFB key → request a **Primary Refresh Token (valid 90 days, renewable)** — no admin rights required.
- **Passkey/FIDO2 abuse:** the WHFB key can be used as a **WebAuthn passkey** (via a minimal implementation written with Claude's help and shipped in ROADtools) — satisfying **Conditional Access policies requiring phishing-resistant authentication** and letting the attacker authenticate from anywhere within 5 minutes of capturing an assertion.
- **Persistence:** tokens obtained without a device-ID claim can **register a new (fake) device**, then upgrade to a PRT — and because WHFB use counts as fresh MFA, the attacker can register additional backdoor authentication material.

**Hunting hypothesis / detection:** WHFB sign-ins with no device identity are the tell — `SigninLogs | where AuthenticationDetails has "Windows Hello for Business" | where DeviceDetail.deviceId == ""` — plus generic monitoring for unexpected new Windows device registrations.

**Action:** The technique requires prior session compromise, so endpoint hygiene remains the primary control; add the deviceless-WHFB-sign-in query to Entra ID monitoring and treat unexpected device registrations as a persistence red flag.

**Source:** [dirkjanm.io](https://dirkjanm.io/borrowing-windows-hello-keys/)

---

## 📋 Policy & Industry News

### Senate Intel Chairman Pushes Treasury to Use the Tax Code to Modernize OT

Senate Intelligence Committee Chairman **Tom Cotton (R-Ark.)** wrote to Treasury Secretary Scott Bessent urging the department to "make better use of existing incentives in the tax code" to spur investment in **operational technology** — the hardware and software underpinning U.S. critical infrastructure, which Cotton calls underfunded, outdated, and increasingly vulnerable to cyberattack. The letter lands amid the multi-state water-sector campaign (covered through Aug 5) and CISA's repeated warnings about internet-exposed PLCs.

**Source:** [CyberScoop/FedScoop](https://fedscoop.com/treasury-tax-code-ot-cyberattacks-tom-cotton-letter/)

### Brown Health Medical Group-MA Breach Hits 311,760 — Historic File Server Exposed SSNs, Financial Data

**Lifespan Physician Group of Massachusetts** (doing business as Brown Health Medical Group-MA) is notifying **311,760 individuals** — 290,357 of them Massachusetts residents — that their personal, medical, and financial information was stolen in a breach. The incident occurred in **December 2025** at its Hawthorn location and involved a **historic file server**; the EHR system was not affected, but the attackers accessed files containing **names, contact info, DOBs, Social Security numbers, driver's license and government ID numbers, medical/disability records, financial account information, and card numbers**, plus personnel records including payroll. The organization determined the exposure on June 22, 2026, has notified HHS, and is offering two years of identity protection. No threat actor has claimed responsibility.

**Source:** [SecurityWeek](https://www.securityweek.com/311000-impacted-by-brown-health-medical-group-ma-data-breach/)

---

## ⚡ Quick Hits

- **Google Blogger locks hundreds of blogs in malware false positive** — since August 4, legitimate blogs have been locked (some deleted) under the "Malware and Similar Malicious Content" policy; affected admins are flooding Google's support forum. ([BleepingComputer](https://www.bleepingcomputer.com/news/google/google-blogger-locks-hundreds-of-blogs-in-malware-false-positive/))
- **GitGuardian: 40 million fake commits flooded public GitHub** — commit volume exploded from ~8M/day in June to ~40M/day by July 31; 70%+ of public events are now spam commits (web-flow accounts, random names) pointing to an illegal Chinese **online lottery operation** ("Rúyì cǎi") via layered redirect chains on Hong Kong-hosted infrastructure — a reminder that platform-level automation is now trivially cheap. ([GitGuardian](https://blog.gitguardian.com/40-million-fake-push-when-spam-commits-took-over-the-public-github/))
- **ASEC dark-web roundup (Week 1, August)** — a South Korean automotive parts manufacturer's internal server access and database, and a Turkish HR consulting firm's data, offered for sale on underground markets. ([ASEC/AhnLab](https://asec.ahnlab.com/en/94844/))

---

## Gap Detection

| Source | Story | Status | Action |
|--------|-------|--------|--------|
| CISA KEV | **CVE-2026-63077 (JetBrains TeamCity) added Aug 5** — unauthenticated RCE under active exploitation, due Aug 8 | ✅ New KEV entry | Added to Critical Threats as [UPDATE] |
| CISA KEV | Aug 4 batch (Langflow CVE-2026-9198, Tomcat CVE-2026-34486, N-central CVE-2026-18556) — due dates Aug 6–7 now imminent | Already covered Aug 5 | Deadline update folded into Critical |
| Community sources | No new unindexed critical stories beyond the KEV additions | No action | |

---

*Digest generated August 6, 2026. 25 feed articles reviewed; prior digests Aug 1–5 cross-referenced for continuity; CISA KEV catalog monitored (catalog version 2026.08.05; one new addition: TeamCity CVE-2026-63077). Excluded as prior-digest repeats, vendor marketing, or non-threat-intel: Pass-ta-key re-report (covered Aug 4), SOCFortress Shai-Hulud analysis (ChainDrop covered Aug 5), Black Hat vendor-announcements roundup, sponsored Push Security explainer, Microsoft CNAPP leadership post, Tenable/Palo Alto product posts, SecurityWeek opinion columns.*
