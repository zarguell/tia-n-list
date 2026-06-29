---
title: "Windows Kernel LPE DigiCert CA Compromise KnowledgeDeliver Zero-Day WhatsApp Zero-Click Charter Breach Fragnesia Linux LPE"
date: 2026-05-27
tags: ["CVE-2026-40369", "DigiCert", "CVE-2026-5426", "WhatsApp", "Charter", "ShinyHunters", "Fragnesia", "Seedworm", "Nimbus Manticore", "NIST", "Mythos", "SharePoint RCE", "CERT-In", "Linux LPE", "zero-click"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Critical: Windows kernel LPE bypasses all browser sandboxes (CVE-2026-40369, public PoC), DigiCert CA compromised via support chat — stolen EV certs signed Zhong Stealer malware (60 certs revoked), KnowledgeDeliver zero-day exploited for Cobalt Strike via hardcoded machine keys, zero-click WhatsApp takeover chain on iOS 16 targeting 200+ victims. Gaps from Reddit: DigiCert, Fragnesia Linux LPE regression (CVE-2026-46300), NIST/NVD halts universal CVE enrichment (29K CVEs abandoned). Priority actions: apply May 2026 Patch Tuesday, audit ASP.NET machine keys, review NVD blind spots, deploy endpoint coverage on support systems."
---
# Daily Threat Intelligence Digest — May 27, 2026

*77 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] CVE-2026-40369 — Windows Kernel LPE: 100% Reliable SYSTEM from Any Sandbox — Ori Nimron Drops Full Exploit After Pwn2Own Rejection**

A critical vulnerability in the Windows kernel (`ExpGetProcessInformation` via `NtQuerySystemInformation` info class 253) allows any unprivileged process — including a sandboxed Chrome, Edge, or Firefox renderer — to escalate deterministically to `NT AUTHORITY\SYSTEM`. Researcher **Ori Nimron** built a working exploit intended for Pwn2Own Berlin 2026 but was turned away due to venue capacity; he publicly dropped the full exploit chain, including a Chrome sandbox emulator PoC on GitHub.

The bug has two compounding failures that bypass kernel protections: when `Length=0` is passed to the syscall, `ProbeForWrite` becomes a complete no-op (its entire body is conditioned on `if (Length)`), so any pointer including raw kernel-mode addresses passes through. Simultaneously, class 253 dispatches via a `goto` statement that intentionally skips the pointer sanitization step used correctly by neighboring classes 5 and 252. The result is a direct, arbitrary increment of kernel memory at attacker-supplied addresses — incrementing three DWORDs (process count, thread count, handle count) per running process.

Critically, Windows lacks SMAP (Supervisor Mode Access Prevention), relying entirely on `__try/__except` software guards — meaning corrupted kernel pointers freely dereference attacker-controlled user-mode pages without crashing. The published five-stage exploit chains a prefetch side-channel for `ntoskrnl` base leak, class 253 primitive for registry array corruption, arbitrary kernel read via fake `UNICODE_STRING`, privilege enablement via `token+0x42` byte increment, and `CreateRemoteThread` into `winlogon.exe` for SYSTEM shell.

Microsoft patched CVE-2026-40369 (CVSS 7.8) in the **May 2026 Patch Tuesday** — this update is urgent for any Windows 11 24H2/25H2 or Windows Server 2025 deployment. [[Cyber Security News](https://cyberpress.org/windows-kernel-flaw/)]

---

**[GAP] DigiCert CA Compromise — Social Engineering via Support Chat Steals EV Code-Signing Certificates to Sign Zhong Stealer Malware — 60 Certificates Revoked**

One of the most consequential attacks on public-key infrastructure this year unfolded at DigiCert in early April. A threat actor posed as a customer via the support chat channel, delivering a malicious `.scr` file disguised as a screenshot inside a ZIP archive. After four failed delivery attempts (blocked by CrowdStrike sensors), a **fifth attempt compromised ENDPOINT1 on April 2**. A second analyst endpoint was compromised on April 4 and went **undetected for nearly two weeks** — it lacked a CrowdStrike sensor entirely.

Attackers used the compromised support endpoints to access DigiCert's internal customer portal, exploiting a proxy feature that lets support staff view accounts from the customer's perspective. This allowed them to **extract initialization codes for approved but pending EV Code Signing certificate orders** — along with the hardware token PIN and software needed to retrieve the certificates and their key material.

**27 certificates were stolen and used to sign Zhong Stealer malware** (associated with Chinese GoldenEyeDog / APT-Q-27), enabling it to bypass Windows SmartScreen and other trust-based defenses. DigiCert revoked 60 certificates total (27 confirmed stolen, 33 precautionary) across **13 countries**, affecting customers including Shuttle, Lenovo, Palit, Tencent (TikTok), and security firm DigiFors. Root cause: missing endpoint coverage on a critical support machine, inadequate risk analysis for certificate initialization code access, and a Salesforce customer portal that blindly forwarded malicious attachments to support staff. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/digicert-says-it-was-breached-via-malicious-screensaver-file/); [Mozilla Bugzilla](https://bugzilla.mozilla.org/show_bug.cgi?id=2033170)]

---

**[NEW] CVE-2026-5426 — KnowledgeDeliver Zero-Day Exploited for Godzilla Web Shell via Hardcoded Machine Key Across All Deployments**

Mandiant responded to an attack where hackers exploited a critical **pre-authentication deserialization vulnerability** (CVE-2026-5426) in the KnowledgeDeliver learning management system to deploy the **Godzilla (BlueBeam) in-memory .NET web shell**. The root cause: identical hardcoded ASP.NET machine keys shared across **all customer deployments** in a standardized `web.config` file for installations before February 24, 2026.

The machine key enabled ViewState deserialization attacks — attackers signed malicious ViewState payloads for OS-level RCE without authentication. On compromised servers, malicious JavaScript prompted users to download a fake "security authentication plugin" that deployed a **Cobalt Strike beacon**. The payload was encrypted with a key tied to the compromised organization's name, confirming intentional targeting.

This follows an alarming pattern: identical ViewState deserialization attacks using hardcoded/stolen machine keys compromised **85 SharePoint servers** (July 2025), Gladinet CentreStack (March 2025), and Sitecore servers for WeepSteel reconnaissance tool deployment. Organizations running any ASP.NET application should immediately audit for hardcoded or shared machine keys. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/knowledgedeliver-flaw-exploited-as-a-zero-day-to-install-web-shells/)]

---

**[NEW] Zero-Click WhatsApp Account Takeover (CVE-2025-43300 + CVE-2025-55177) — Active Campaign Targeting iOS 16 Devices**

A forensically confirmed zero-click campaign is actively hijacking WhatsApp accounts on iPhones running iOS 16. Italian digital forensics firm **Forenser** identified the pattern after multiple iPhone users reported their WhatsApp accounts sending fraudulent wire-transfer requests. Every affected user shared the same profile: an iPhone running **iOS 16** (iPhone 8 through 14), with **no suspicious entries in the Linked Devices section** — the attacker's session was never registered as a traditional linked device.

The two-vulnerability chain: **CVE-2025-43300** — an out-of-bounds write in Apple's ImageIO framework via crafted DNG image (patched August 2025, but iOS 16 devices never received the fix), and **CVE-2025-55177** — a WhatsApp authorization bypass in linked-device synchronization messages (below WhatsApp for iOS 2.25.21.73). Chained together, attackers exfiltrate cryptographic handshake material to instantiate a new WhatsApp client invisibly bound to the victim's account.

WhatsApp confirmed **approximately 200 targeted victims over three months**, describing it as a "highly selective and advanced operation." Apple has not issued a dedicated iOS 16 patch. **Urgent action:** devices stuck on iOS 16 should be replaced; enable Two-Step Verification and Lockdown Mode for high-risk users (journalists, executives, security professionals). If a contact receives a suspicious money request, they must not reply in the same chat — the attacker's session may intercept the reply. [[Cyber Security News](https://cyberpress.org/0-click-whatsapp-attack/); [GBHackers](https://gbhackers.com/new-zero-click-whatsapp-account-takeover-attack-targets-ios-16-users/)]

---

**[NEW] Charter Communications Confirms Data Breach — ShinyHunters Claims 40 Million Records via Vishing Attack on Entra ID**

U.S. telecommunications giant Charter Communications (Spectrum brand, tens of millions of customers) confirmed a data breach after ShinyHunters listed the company on its leak site. The extortion group claims to have stolen **40 million records** — customer names, email addresses, phone numbers, plan information, and CPNI data — via a **vishing (voice phishing) attack on April 1** that compromised an employee's Microsoft Entra account, then exported data from Salesforce.

Charter's official statement claims "no sensitive personal information or CPNI" was exfiltrated — directly contradicting the threat actor's claims. This follows the same ShinyHunters playbook used against **7-Eleven** (185K records, covered May 26) and **Instructure/Canvas** (275M+ records) — the "Salesforce Aura" campaign systematically targeting SaaS-connected SSO accounts via social engineering. Organizations should treat Entra SAW (privileged access workstation) deployment and vishing-specific user training as urgent operational priorities. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/charter-confirms-data-breach-after-shinyhunters-extortion-threat/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Seedworm (MuddyWater) Weaponizes Signed SentinelOne and Fortemedia Binaries in Global Espionage Campaign**

Iran-linked Seedworm (MuddyWater / Static Kitten, operating under MOIS) breached a **major South Korean electronics manufacturer** as part of a sprawling early-2026 campaign spanning government agencies, airports, financial services, and industrial manufacturers across four continents — signaling a broadened intelligence-gathering mandate beyond the Middle East.

The campaign demonstrates significantly matured tradecraft. Attackers deployed **DLL sideloading via validly signed third-party executables**: `fmapp.exe` (Fortemedia Audio Utilities) loaded a malicious `fmapp.dll`, and `sentinelmemoryscanner.exe` — a **signed SentinelOne security binary** — loaded `sentinelagentcore.dll`. Both deployed **ChromElevator**, a publicly available post-exploitation tool for extracting browser passwords, cookies, and payment data from Chromium-based browsers.

Seedworm shifted from heavy PowerShell usage to **Node.js-based automation**, with `node.exe` observed as the grandparent process for hijacked binaries — indicating automated loader infrastructure rather than hands-on-keyboard operation. Credential theft targeted SAM/SECURITY/SYSTEM hives for NTLM hashes and specialized tools for Kerberos TGT extraction. Exfiltration used **sendit.sh**, a public file-transfer service, blending stolen data with normal consumer cloud traffic. [[Cyber Security News](https://cyberpress.org/seedworm-weaponizes-signed-binaries/)]

---

**[UPDATE] Nimbus Manticore (Charming Kitten / UNC1549) Expands Campaigns with AI-Assisted Backdoors, AppDomain Hijacking, and US Aviation Targeting**

Check Point Research documents three additional campaign waves from Nimbus Manticore, an IRGC-linked subgroup of Charming Kitten. The group continues to evolve aggressively: moving from DLL sideloading to **AppDomain Hijacking** (trojanized XML `.config` files loading malicious DLLs at .NET application launch), deploying **MiniFast** (a new 64-bit Windows PE DLL backdoor with AI-assisted development patterns), and running **SEO poisoning campaigns** — a fake Oracle SQL Developer download site (`getsqldeveloper[.]com`) that ranked high on Bing and DuckDuckGo for the "sql developer" query.

New campaigns specifically target **US domestic airlines** through fraudulent hiring portals — a notable geographic expansion beyond the group's traditional Middle East and European focus. Lures include trojanized Zoom installers and OnlyOffice-hosted ZIP archives deploying the updated MiniJunk backdoor. This was first reported in the May 23 digest; the current detail adds the aviation focus and SQL Developer SEO vector. [[SecurityWeek](https://www.securityweek.com/iranian-apt-targets-aviation-software-companies-with-updated-tools/); Check Point Research via Malware.News]

---

## ⚠️ Vulnerabilities & Patches

**[GAP] Fragnesia (CVE-2026-46300) — Dirty Frag Regression Creates New Universal Linux LPE with Public PoC — All Kernels Before May 13 Affected**

A second Linux kernel page-cache write primitive, discovered by **William Bowling (Zellic/V12)** and dubbed Fragnesia, landed within two weeks of Copy Fail (CVE-2026-31431). Critically, Fragnesia is not an independent bug — it is a **regression introduced by the Dirty Frag patch** (CVE-2026-43284). The fix for Dirty Frag changed how `skb_try_coalesce()` propagates `SKBFL_SHARED_FRAG`, and that change accidentally dropped the flag along the `espintcp` ULP-transition path.

The result: **192 bytes per trigger** of AES-GCM keystream XOR directly into the page cache of any user-readable file — no race condition required. The public PoC overwrites the first 192 bytes of `/usr/bin/su` in the page cache with a root-shell ELF stub. The on-disk binary is untouched (a reboot clears the modification). The exploit requires user+network namespace access (`CAP_NET_ADMIN` from `unshare`), making it slightly more constrained than Copy Fail — but effective on any distribution where `kernel.apparmor_restrict_unprivileged_userns` is not enforced.

All Linux kernels before the May 13, 2026 patch are affected. **Workaround:** `rmmod esp4 esp6` and block via modprobe config. No CISA KEV status yet, but the public PoC and trivial exploitation surface make this an urgent patching priority. [[V12 Security PoC](https://github.com/v12-security/pocs/blob/main/fragnesia/README.md); [TLCTC Analysis](https://www.tlctc.net/cve-2026-46300.html)]

---

**[NEW] CVE-2026-45659 — Microsoft SharePoint Server Deserialization RCE (CVSS 8.8) — Site Member-Level Access Only Required**

Microsoft patched a deserialization vulnerability (CWE-502) in SharePoint Server as part of the May 2026 Patch Tuesday (130+ vulnerabilities addressed). The flaw requires only **Site Member-level permissions** (no admin) and allows an authenticated attacker to trigger arbitrary .NET deserialization gadget chains, achieving code execution as the SharePoint application service account. Attack vector: Network (AV:N), Complexity: Low (AC:L), no user interaction required.

This follows CVE-2026-20963 (also SharePoint deserialization, re-scored to CVSS 9.8 after unauthenticated exploitation was confirmed, added to CISA KEV in March 2026). Given the pattern of SharePoint deserialization CVEs being re-evaluated upward, treat this update as critical for any on-premises SharePoint deployment. Patches: KB5002863 (SE), KB5002870 (2019), KB5002868 (2016). [[Cyber Security News](https://cyberpress.org/microsoft-sharepoint-flaw/)]

---

## 📋 Policy & Industry News

**[GAP] NIST/NVD Ends Universal CVE Enrichment — 29,000 CVEs Moved to "Not Scheduled" — Security Teams Face Expanding Blind Spots**

Effective April 15, 2026, NIST fundamentally changed its National Vulnerability Database (NVD) operations, moving from universal CVE enrichment to a **risk-based triage model**. Only three categories will receive NIST enrichment going forward: CVEs in the CISA KEV catalog, those affecting U.S. federal government software, and CVEs tied to Executive Order 14028 critical software. Approximately **29,000 backlogged CVEs** have been reclassified as "Not Scheduled" — meaning they receive **no CVSS scores, no CPE identifiers, no CWE mappings** from NIST, potentially indefinitely.

With 50,000–70,000 new CVE submissions expected in 2026 (a 263% increase from 2020), security teams that rely on NVD-derived metadata for vulnerability management face expanding blind spots. Vulnerability scanners that depend exclusively on NVD enrichment cannot match a CVE to a product if CPE data is missing — the alert that should trigger a remediation workflow may never fire. **Action:** teams should cross-reference their CVE alert backlog against the NVD API for "Awaiting Analysis" or "Not Scheduled" status, and integrate multiple authoritative feeds (vendor advisories, CISA, CNAs) rather than treating any single source as authoritative. [[NIST](https://www.nist.gov/news-events/news/2026/04/nist-updates-nvd-operations-address-record-cve-growth); [Dark Reading](https://www.darkreading.com/threat-intelligence/nist-cutbacks-nvd-handling-impacts-cyber-teams); [Cloud Security Alliance](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/04/CSA_research_note_NIST_NVD_enrichment_changes_enterprise_vuln_mgmt_20260418-csa-styled.pdf)]

---

**[NEW] Anthropic Mythos Finds 10,000+ High/Critical Vulnerabilities in First Month of Project Glasswing — Discovery No Longer the Bottleneck, Patching Is**

Anthropic released findings from **Project Glasswing**, its month-old initiative using the Mythos-class AI model to scan systemically important code at scale. Results: **10,000+ high- or critical-severity vulnerabilities** discovered across partner organizations. Cloudflare identified **2,000 bugs** (400 high/critical) with false-positive rates better than human testers. Mozilla found and fixed **271 vulnerabilities in Firefox 150** — 10× the rate of the previous model. The UK AI Security Institute found Mythos Preview was the first model to solve both of its cyber range simulations end-to-end.

Of 1,752 high- or critical-rated findings independently reviewed, **over 90% were confirmed valid** and **62% confirmed as high or critical**. The report's central finding: the bottleneck has shifted from **vulnerability discovery to human triage and patching capacity**. Anthropic has not released Mythos publicly due to misuse safeguards being inadequate. Meanwhile, the publicly available Claude Opus 4.7 has patched over 2,100 vulnerabilities in enterprise use in three weeks. [[CyberScoop](https://cyberscoop.com/anthropic-mythos-software-flaws-glasswing/)]

---

## ⚡ Quick Hits

- **GitHub Enterprise Server 3.20.3 patches critical SSRF (CVE-2026-9312) plus Dirty Frag kernel CVEs** — The critical SSRF in an upload endpoint allows pre-auth access to internal services. Manual GPG key rotation required before upgrade. Dirty Frag kernel fixes address the IPsec/RxRPC LPE surface that Fragnesia regressed from. [[Cyber Security News](https://cyberpress.org/github-enterprise-server-3-20-3-fixes/)]
- **Microsoft Defender auto-isolation now in preview** — Automatic Attack Disruption for Defender for Endpoint will automatically isolate compromised endpoints from the network in real time, blocking lateral movement before ransomware can spread. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-defender-can-now-automatically-isolate-hacked-endpoints/)]
- **CERT-In mandates 12-hour patch deadline for internet-facing vulnerabilities** — India's national cyber agency published a 38-page blueprint requiring organizations to patch known exploited vulnerabilities in exposed systems within 12 hours. Also mandates 6-hour incident reporting and a 60-day three-phase roadmap for AI-era defense transformation. [[GBHackers](https://gbhackers.com/cert-in-mandates-12-hour-patch/)]
- **Red Canary: ClearFake #1 threat for May, ACR Stealer debuts, GraphRunner device-code abuse surge** — ClearFake (JavaScript drive-by, fake CAPTCHA ClickFix) takes the top spot delivering ACR Stealer (Amatera) via fake Claude Code GitLab pages. GraphRunner abuse of OAuth device code flow for MFA bypass continues rising as the Kali365/EvilTokens PhaaS ecosystem commoditizes the technique. [[Red Canary](https://redcanary.com/blog/threat-intelligence/intelligence-insights-may-2026/)]
- **Glassworm developer-targeting botnet takedown** — CrowdStrike, Google, and Shadowserver simultaneously severed all four C2 channels (Solana blockchain, BitTorrent DHT, Google Calendar, traditional VPS). Over 300 GitHub repos poisoned; sinkhole at 164.92.88.210. [[Cyber Security News](https://cyberpress.org/glassworm-targets-developer-platforms/)]
- **CloudZ Malware abuses Microsoft Phone Link to intercept SMS/OTPs** — New "Pheno" plugin for CloudZ RAT reads SMS and OTPs from Windows Phone Link's local SQLite database — no phone compromise needed. Active since January 2026. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cloudz-malware-abuses-microsoft-phone-link-to-steal-sms-and-otps/)]
