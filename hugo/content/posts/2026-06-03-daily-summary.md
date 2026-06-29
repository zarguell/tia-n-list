---
title: "🔴 VS Code Zero-Day, 💣 HTTP/2 Bomb DoS, 📱 Microsoft Android Debug Flag, 🎯 HazyBeacon AWS C2, 🖼️ Kirki WordPress Exploit, 🏛️ Trump AI EO"
date: 2026-06-03
tags: ["VS Code","GitHub","OAuth","HTTP/2 Bomb","DoS","nginx","Apache","Microsoft","Android","CVE-2026-41100","HazyBeacon","AWS Lambda","PlugX","Mustang Panda","AZUREVEIL","Kirki","WordPress","CVE-2026-8206","KMW CCTV","CVE-2026-5386","AI ransomware","EDR evasion","Trump","AI executive order","Project Glasswing","Mythos","Anthropic","JS.MonoGlyphRAT","CISA","CVE-2026-48019","Laravel","NTLM","Windows Search","Instagram","Meta AI"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Critical: VS Code zero-day leaks GitHub OAuth tokens with no patch available; HTTP/2 Bomb AI-discovered DoS threatens 880K+ web servers; six Microsoft 365 Android apps shipped with debug flag exposing account tokens. Campaigns: HazyBeacon abuses AWS Lambda for C2; Mustang Panda deploys PlugX via fake browser updater; AZUREVEIL targets Czech/Taiwan officials. Patch CVE-2026-8206 (Kirki WordPress) actively exploited — update immediately."
---

# Daily Threat Intelligence Digest — June 3, 2026

*95 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] VS Code Zero-Day Leaks GitHub OAuth Tokens via Single Click — Public PoC Released, No Patch Available**

A critical vulnerability in Visual Studio Code's webview message-passing system allows attackers to steal **full-scope GitHub OAuth tokens** by tricking a victim into clicking a single link — granting read/write access to every repository the victim can access, including private ones. Security researcher **Ammar Askar** released a working proof-of-concept exploit on June 2, choosing full public disclosure after a prior negative experience with Microsoft's Security Response Center. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/vs-code-zero-day-lets-hackers-steal-github-tokens-in-one-click/); [Cyberpress](https://cyberpress.org/1-click-github-flaw/)]

**How it works:** `github.dev` (VS Code's browser-based editor) authenticates users by POSTing an OAuth token that is **not scoped to a single repository**. Malicious JavaScript embedded in a webview can simulate keypresses in the main editor to install an extension that exfiltrates the token and queries the GitHub API for every accessible repo. No fix exists — this is a true zero-day.

**Temporary mitigation:** Clear cookies and local site data for `github.dev` in browser settings. This forces a re-authentication dialog that includes an "Extension wants to sign in" warning. Organizations should block or monitor `github.dev` access via CASB/proxy policies until Microsoft issues a patch.

**Broader context:** This is the seventh publicly disclosed zero-day in Microsoft products in two months, following the "Nightmare Eclipse" disclosures of BlueHammer, RedSun, UnDefend, YellowKey, GreenPlasma, and MiniPlasma — with three confirmed actively exploited in the wild. The researcher's stated distrust of MSRC's disclosure process mirrors the pattern driving this disclosure wave. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/vs-code-zero-day-lets-hackers-steal-github-tokens-in-one-click/)]

---

**[NEW] HTTP/2 Bomb — AI-Discovered Chained DoS Exhausts 32 GB Server Memory in Under 60 Seconds**

A remote denial-of-service exploit dubbed **"HTTP/2 Bomb"** targets every major web server in their default configurations — nginx, Apache httpd, Microsoft IIS, Envoy, and Cloudflare Pingora — by chaining two decade-old techniques into a devastating amplification attack. Discovered autonomously by **OpenAI's Codex**, the exploit can render servers inaccessible from a standard residential internet connection. [[Cyberpress](https://cyberpress.org/http-2-bomb-dos-exploit/); [GBHackers](https://gbhackers.com/http-2-bomb-remote-dos-exploit/); [Malware.News](https://malware.news/t/codex-discovered-a-hidden-http-2-bomb/107526#post_1)]

**Amplification ratios:**
| Server | Amplification | Time to 32 GB |
|--------|--------------|---------------|
| Envoy 1.37.2 | ~5,700:1 | ~10 seconds |
| Apache httpd 2.4.67 | ~4,000:1 | ~18 seconds |
| nginx 1.29.7 | ~70:1 | ~45 seconds |
| IIS (Server 2025) | ~68:1 | ~64 GB in ~45s |

**What makes it different:** Classic HPACK bombs were mitigated by capping decoded header size. This exploit sidesteps that entirely by abusing RFC 9113's permission to split the `Cookie` header into one field per crumb — neither Apache nor Envoy was counting crumbs against the field limit. The attack then stalls server responses using zero-byte flow-control windows, pinning the allocated memory indefinitely.

**Mitigations:** nginx patches available in 1.29.8+ (`max_headers` directive). Apache httpd requires standalone `mod_http2 v2.0.41`. IIS, Envoy, and Pingora have **no patches available** — organizations must disable HTTP/2 or front with a proxy enforcing per-request header count caps. PoC scripts and Docker labs are publicly available. Shodan identifies **880,000+ exposed endpoints**. [[Cyberpress](https://cyberpress.org/http-2-bomb-dos-exploit/)]

---

**[NEW] Microsoft 365 Android Apps Left Debug Flag Enabled in Production — CVE-2026-41100/101/102 — Billions of Downloads Exposed**

Six Microsoft 365 Android apps — Word, PowerPoint, Excel, 365 Copilot, Loop, and OneNote — shipped with `set IsDebugMode(true)` in their production builds, disabling the security check that restricts FOCI (Family of Client IDs) account token sharing to trusted Microsoft apps only. Enclave Security discovered that any malicious app on the same device can silently steal Microsoft account access tokens with just 15 lines of code. [[SecurityWeek](https://www.securityweek.com/exclusive-how-one-line-of-code-put-billions-of-microsoft-android-app-downloads-at-risk/)]

**Attack vector:** A supply chain attack via trojanized app updates. An attacker updates a legitimate app (e.g., a game) with malicious code. Auto-update silently installs it, the malicious code requests account tokens from the debug-enabled Microsoft app, and receives them without authorization checks. The stolen FOCI tokens are **reusable and refreshable** over long periods. Impact: full read/write access to emails, files, documents, and calendar.

Microsoft patched the flaw on May 12 (Patch Tuesday) and via Google Play Store. **User action required:** Ensure all Microsoft Android apps are updated to the latest versions. Microsoft Teams was not affected.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] HazyBeacon (CL-STA-1020) — Espionage Campaign Abuses AWS Lambda Function URLs as Stealthy C2 Relays**

A newly documented cyber espionage operation tracked as **HazyBeacon** (CL-STA-1020) is targeting Southeast Asian government networks by weaponizing AWS Lambda Function URLs as command-and-control relays. Attackers use stolen IAM credentials to deploy Lambda functions with `AuthType: NONE` (unauthenticated public access), creating HTTPS relay points that mask malicious traffic as legitimate AWS communication. [[GBHackers](https://gbhackers.com/hazybeacon-campaign-abuses-aws/); [Qualys](https://blog.qualys.com/qualys-insights/2026/06/02/hazybeacon-aws-lambda-function-url-command-control-abuse)]

**Detection challenge:** Traffic appears as normal HTTPS to `*.on.aws` domains. The attacker's backend receives connections that appear to originate from AWS. Monitor for rapid, sequential `CreateFunction` + `AddPermission` API calls from a single identity. Enforce IAM least-privilege and implement Service Control Policies restricting Lambda Function URL exposure.

---

**[NEW] Mustang Panda (China-Nexus) Deploys PlugX RAT via Fake Browser Updater — DLL Sideloading Through Legitimate G DATA Binary**

Mustang Panda is using a multi-stage LNK–PowerShell loader disguised as a fake "Browser Updater" to sideload **PlugX** through a legitimate G DATA antivirus binary (`Avk.exe`). The infection chain: LNK → hidden PowerShell → archive extraction → fake update UI → HTTP download of MSI → DLL sideloading → PlugX C2 observed at `fruitbrat[.]com`. [[GBHackers](https://gbhackers.com/mustang-panda-uses-lnk/)]

---

**[NEW] AZUREVEIL — China-Linked Spearphishing Delivers Adaptix C2 via Azure Blob Storage Dead-Drop — Targets Czech Republic and Taiwan**

Seqrite Labs documented a targeted campaign using region-specific lures (Czech Social Security appointment notice, Taiwanese project review form). The infection chain delivers **AZUREVEIL**, a modified Adaptix C2 agent with 36 post-exploitation commands, via a RUSTCLOAK loader using Windows fibers for threadless execution. **C2:** Microsoft Azure Blob Storage with SAS token, dead-drop architecture — no direct server. [[Cyberpress](https://cyberpress.org/azureveil-spearphishing-delivers-c2/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Windows `search:` URI Handler Leaks NTLMv2 Hashes via Single Click — No CVE Assigned, Unpatched**

Huntress researchers identified that Windows' built-in `search:` URI handler passes user-supplied UNC paths to Explorer without validation, coercing outbound SMB authentication. A single crafted link forces the system to leak Net-NTLMv2 hashes. **No CVE assigned** — Microsoft classified it below the servicing threshold. **Mitigation:** Block outbound SMB (TCP 445/139) to untrusted networks. [[GBHackers](https://gbhackers.com/windows-search-uri-handler-vulnerability/)]

---

**[NEW] CVE-2026-8206 — Kirki WordPress Plugin Actively Exploited for Admin Account Takeover — 500K+ Sites**

Defiant (Wordfence) blocked **222+ exploitation attempts** in 24 hours targeting the Kirki plugin (500K+ active sites). The flaw: an unauthenticated REST API endpoint accepts attacker-supplied email addresses during password reset, sending the reset link to the attacker. Fixed in version 6.0.7 (May 18). ~40% of the userbase may still be vulnerable. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/critical-kirki-flaw-exploited-to-hijack-wordpress-admin-accounts/)]

---

**[NEW] CVE-2026-5386 (CVSS 9.1) — KMW CCTV Cameras — Unverified Password Change Enables Full Surveillance Feed Takeover**

CISA disclosed an OT-critical vulnerability in KMW CCTV cameras (KM-IP521, KM-IP421) used across government services, transportation, and manufacturing. Unauthenticated remote password reset grants full control of video feeds and device configurations. No active exploitation reported. [[GBHackers](https://gbhackers.com/critical-kmw-cctv-flaw/); [Cyberpress](https://cyberpress.org/critical-kmw-cctv-flaw/)]

---

**[NEW] CVE-2026-48019 — Laravel CRLF Injection Enables Mail Relay Abuse**

A CRLF injection vulnerability (GHSA-5vg9-5847-vvmq, June 1) in Laravel's email handling allows attackers to inject arbitrary SMTP headers via user-supplied email addresses. Potential for mail relay abuse, phishing, and email spoofing via compromised Laravel apps. [[Cyberpress](https://cyberpress.org/laravel-crlf-injection-flaw/); [GBHackers](https://gbhackers.com/laravel-crlf-injection-flaw/)]

---

## 🛡️ Defense & Detection

**[NEW] Google Launches "Fake Call Detection" for Android — AI Deepfake Call Protection Enabled by Default**

Google rolled out a new Android security feature that detects AI deepfake impersonation calls in real time via RCS cross-device signal verification. Available on Android 12+ starting with Pixel devices. The FTC reported $2.95 billion in impersonation scam losses in 2024 alone. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/google-adds-android-protection-against-ai-deepfake-scam-calls/)]

---

**[NEW] CISA/FBI/NSA Joint Advisory: Cyberattacks Targeting U.S. Automatic Tank Gauge (ATG) Systems**

A multi-agency advisory warns of active, ongoing attacks against internet-exposed ATG systems used across energy, chemical, food/agriculture, and transportation sectors. Attackers exploiting authentication bypass, default credentials, OS command injection, and SQL injection. **Action:** Remove ATG systems from internet exposure immediately. [[GBHackers](https://gbhackers.com/cisa-warns-of-cyberattacks/)]

---

**[NEW] JS.MonoGlyphRAT — New JavaScript Backdoor Via Fake Purchase Orders Hits U.S. Enterprises**

A previously unattributed JS-based RAT delivered via fake purchase order `.js` attachments targeting procurement/finance staff. Uses monoglyph obfuscation, AES-encrypted PowerShell stagers, and C2 on non-standard ports (34567). [[GBHackers](https://gbhackers.com/fake-purchase-orders-spread-js-monoglyphrat/)]

---

**[NEW] AI-Built Ransomware Toolkit Automates EDR Evasion — Sophos Documents Multi-Agent Development Pipeline**

Sophos documented a threat actor using Cursor and Claude Opus agents to automate EDR bypass research against CrowdStrike, Sophos, and Microsoft Defender — compressing the research-to-weaponization timeline from months to days. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ai-built-ransomware-toolkit-automates-edr-evasion-ad-discovery/)]

---

## 📋 Policy & Industry News

**[NEW] Trump Administration Releases Scaled-Back AI Executive Order — Voluntary 30-Day Preview Replaces Mandatory 90-Day Model Testing**

The White House issued a revised AI EO significantly weakening federal AI vetting: voluntary 30-day access (down from 90), explicitly not mandatory or a licensing regime. Treasury leads new interagency cybersecurity clearinghouse. [[CyberScoop](https://cyberscoop.com/donald-trump-white-house-ai-executive-order-scaled-back/)]

---

**[NEW] Anthropic's Project Glasswing Expands to 150 Organizations — 10,000+ High/Critical Vulns Found in 2 Months**

Claude Mythos Preview has discovered 10,000+ high/critical severity vulnerabilities since April, including 2,000 bugs in Cloudflare systems, 271 vulns in Firefox 150 (10x previous rate), with 90%+ validation rate on reviewed findings. Anthropic will not release Mythos-class models to the public. [[CyberScoop](https://cyberscoop.com/anthropic-project-glasswing-expansion-critical-infrastructure-claude-mythos/)]

---

## ⚡ Quick Hits

- **CVE-2026-8181 — Burst Statistics WordPress Plugin Actively Exploited:** Authentication bypass in privacy analytics plugin (300K+ installs) under active attack. [[Malware.News](https://malware.news/t/attackers-actively-exploiting-critical-vulnerability-in-burst-statistics-plugin/107520#post_1)]
- **Claude Code GitHub Actions Supply Chain Flaw (Patched, CVSS 7.8):** Permission bypass enabling GitHub App actors to trigger agent-mode workflows, exfiltrate OIDC tokens, and achieve repo write access. Patched in v1.0.94. [[Cyberpress](https://cyberpress.org/claude-code-github-actions-flaw/)]
- **MSRC Dismissed Azure Portal Dependency Confusion RCE as "Automated Security Tooling":** Researcher Fayad registered unclaimed `@FxInternal/NetDiagnostics` npm package, confirmed code execution on Microsoft infrastructure. GHSA-83×6-432q-hpcf rated 9.3 Critical. [[Cyberpress](https://cyberpress.org/microsoft-msrc-dismissed-dependency-confusion/)]
- **Kali365 PhaaS Operator Expands to Outlook, Okta, Xerox DocuShare:** Phishing-as-a-service kit abusing Microsoft OAuth 2.0 device auth flow targets additional platforms. [[Malware.News](https://malware.news/t/from-token-bingo-to-max-takeover-kali365-operator-expands-operation-across-microsoft-outlook-okta-xerox-docushare-and-other-services/107512#post_1)]
- **Iran's Handala Brand Expands to Physical Threats:** Insikt Group attributes "Handala Popular Resistance Front" to Iran's MOIS, soliciting physical attacks against U.S./Israeli targets for financial reward. [[Malware.News](https://malware.news/t/iran-expands-handala-brand-to-physical-threats/107514#post_1)]
- **WFP Data Breach: 600K Gaza Households Exposed:** UN World Food Programme cyberattack exposed personal information of ~600K Gaza households — potentially largest humanitarian beneficiary data breach. [[Malware.News](https://malware.news/t/data-of-600-000-gaza-households-exposed-in-world-food-programme-cyberattack/107519#post_1)]
- **WeedHack MaaS Infects 116K+ Minecraft Systems:** Infostealer campaign distributed via YouTube malvertising and SEO poisoning targeting Minecraft mods, offering free dashboard and $5/month premium tier. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/over-116-000-mincraft-systems-infected-in-weedhack-malware-campaign/)]
