---
title: "🔴 SonicWall SMA Zero-Days Exploited, 🔴 Record 622 Microsoft CVEs, 🔴 Claude for Chrome Unpatched, 🎯 GitHub BoryptGrab Campaign, 🎯 Russian Bulletproof Hosting Charged"
date: 2026-07-15
tags: ["SonicWall","CVE-2026-15409","CVE-2026-15410","Microsoft Patch Tuesday","CVE-2026-56155","CVE-2026-56164","SharePoint","Rapid7","CVE-2026-55040","Claude","Anthropic","Browser Security","Infostealer","GitHub","Phishing","MFA","Bulletproof Hosting","Ransomware","CISA KEV","ShareFile"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "SonicWall SMA1000 zero-days exploited with CVSS 10.0, CISA KEV deadline July 17. Microsoft ships record 622 Patch Tuesday CVEs with two in-wild zero-days and Rapid7's critical SharePoint auth bypass. Claude for Chrome flaw persists unpatched after 8 versions. 292 fake GitHub repos distribute BoryptGrab infostealer. U.S. charges Russian bulletproof hosting operators."
---

# Daily Threat Intelligence Digest — July 15, 2026

37 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] SonicWall SMA1000 — Two Zero-Day Flaws Under Active Exploitation, CVSS 10.0, Added to CISA KEV

SonicWall has confirmed that two vulnerabilities in its SMA1000 secure remote access appliances are being actively exploited as zero-days and has issued an urgent patch advisory. **CVE-2026-15409** (CVSS 10.0) is a critical server-side request forgery (SSRF) vulnerability in the SMA1000 Appliance Work Place interface that allows a **remote, unauthenticated attacker** to force the appliance to make requests to unintended locations. **CVE-2026-15410** (CVSS 7.2) is a post-authentication code injection flaw in the Management Console enabling OS command execution as an administrator.

SonicWall investigated multiple incidents confirming active exploitation. CISA has added both to KEV with a **July 17, 2026** federal remediation deadline under BOD 26-04. Affected models: SMA 6210, 7210, and 8200v. No workarounds exist — patching to hotfix versions 12.4.3-03453 or 12.5.0-02835 is the only remediation. SonicWall provides IOCs including anomalous log entries at `/__api__/login`, `/__api__/logout`, and `/wsproxy` endpoints. If compromised, re-image or redeploy appliances, rotate all credentials, and reset TOTP tokens.

**Hunting hypothesis:** An unauthenticated attacker sends a crafted SSRF payload to the SMA1000 Work Place interface (`/__api__/login` or `/wsproxy`), forcing the appliance to proxy requests to internal infrastructure, then chains with CVE-2026-15410 via a compromised admin session to execute arbitrary OS commands on the appliance — establishing persistent VPN tunnel access into the victim network.

**Action:** Patch immediately. Audit SonicWall SMA logs for the published IOCs. These appliances sit at the network perimeter and provide VPN access — compromise grants direct network entry.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/sonicwall-warns-of-sma1000-flaws-exploited-in-zero-day-attacks-patch-now/) · [The Hacker News](https://thehackernews.com/2026/07/two-sonicwall-sma-1000-zero-days.html)

---

### [NEW] Microsoft July 2026 Patch Tuesday — Record 622 CVEs, Two Exploited Zero-Days, Rapid7 SharePoint Auth Bypass

Microsoft has shipped the largest Patch Tuesday release in history: **622 vulnerabilities** across its product suite, shattering June's previous record of 198. The release includes 56 Critical and 510 Important vulnerabilities. Two vulnerabilities were exploited in the wild:

- **CVE-2026-56155** (CVSS 7.8) — Active Directory Federation Services elevation of privilege. An authorized attacker can elevate to administrator privileges. Credited to Microsoft DART, indicating discovery during active incident response. Microsoft has not disclosed exploitation details.
- **CVE-2026-56164** (CVSS 5.3) — Microsoft SharePoint Server elevation of privilege. Missing authentication for a critical function allows unauthorized privilege escalation over the network. AMSI integration can mitigate. Credited to Mandiant Incident Response and Google Cloud FLARE team.

The release also includes a **publicly disclosed vulnerability**: **CVE-2026-50661** (CVSS 6.1) — Windows BitLocker security feature bypass. Likely patches the "GreatXML" BitLocker bypass disclosed by Nightmare Eclipse in June, which requires physical access.

**Additional critical items** from the massive release:
- **CVE-2026-55944** (CVSS 9.8, Exploitation More Likely) — Microsoft Dynamics NAV/Business Central RCE via untrusted data deserialization. No authentication or user interaction required.
- **Multiple DHCP Server RCEs** (CVSS 8.8–9.8) — Five critical DHCP vulnerabilities, three assessed Exploitation More Likely.
- **20 Windows Kernel EoP** vulnerabilities, six assessed Exploitation More Likely.
- **Nightmare Eclipse "LegacyHive"** — A new PoC for mounting another user's NT user hive has emerged from the same researcher.

**Rapid7 SharePoint Research (CVE-2026-55040):** Rapid7 Labs disclosed a critical (CVSS 9.1) JWT token authentication bypass in Microsoft SharePoint, discovered during a zero-day research project for Pwn2Own Berlin. An unauthenticated attacker who knows a target user's AD SID or UPN can bypass authentication and assume that user's identity — including site administrators. Rapid7 has chained this with a separate RCE vulnerability for **unauthenticated remote code execution**. The RCE component will be patched in the August Patch Tuesday cycle; patching CVE-2026-55040 now breaks the full chain. Full technical details will be published within 30 days.

**Lifecycle note:** SharePoint Server 2016 and 2019 reached end of extended support today (July 14, 2026). No ESU is available — only SharePoint Subscription Edition remains supported.

**Action:** Prioritize AD FS patching (CVE-2026-56155) and SharePoint updates (CVE-2026-56164, CVE-2026-55040). The Rapid7 SharePoint auth bypass + pending RCE chain makes unpatched SharePoint servers an urgent target.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-july-2026-patch-tuesday-fixes-massive-570-flaws-3-zero-days/) · [Rapid7 Patch Tuesday](https://www.rapid7.com/blog/post/em-patch-tuesday-july-2026) · [Rapid7 CVE-2026-55040](https://www.rapid7.com/blog/post/ve-cve-2026-55040-microsoft-sharepoint-jwt-token-authentication-bypass-fixed) · [Tenable](https://www.tenable.com/blog/microsofts-july-2026-patch-tuesday-addresses-569-cves-cve-2026-56155-cve-2026-56164)

---

### [NEW] Claude for Chrome — Unpatched Flaw Lets Rogue Extensions Read Gmail, Calendar, and Docs

Manifold Security has disclosed that **Claude for Chrome v1.0.80** remains vulnerable to two flaws that allow any other browser extension with DOM access to claude.ai to trigger tasks that read the user's Gmail, latest Google Docs (including comments), and Calendar. The vulnerability persists eight versions after being reported to Anthropic on May 21, 2026.

The primary flaw: Claude for Chrome's content script listens for clicks on `#claude-onboarding-button`, reads the `data-task-id` attribute, and opens the side panel with the matching task. The handler **never checks `event.isTrusted`**, so any extension can dispatch a synthetic click. Nine fixed task IDs remain in the allowlist — three of which (`usecase-gmail`, `usecase-gdocs`, `usecase-calendar`) read user data. In the default "ask before acting" mode, an approval dialog still fires (CVSS 7.7). In "Act without asking" mode, the task executes silently (CVSS 9.6).

A secondary flaw: the side panel reads `skipPermissions` from its URL and boots into `skip_all_permission_checks` when set. While not remotely exploitable today, a future bug exposing this parameter could enable fully silent data reads.

Anthropic closed the reports as duplicates of the earlier ClaudeBleed issue but the code remains unchanged in v1.0.80 (byte-for-byte identical to v1.0.72). No CVE or advisory has been published.

**Action:** Disable "Act without asking" mode in Claude for Chrome. Audit browser extensions with claude.ai DOM access permissions. This is the third iteration of trust boundary issues in this extension.

[SecurityWeek](https://www.securityweek.com/unpatched-claude-for-chrome-flaw-lets-extensions-read-gmail-calendar/) · [The Hacker News](https://thehackernews.com/2026/07/claude-for-chrome-flaw-lets-other.html) · [Manifold Security](https://www.manifold.security/blog/claude-for-chrome-extension-bypass)

---

### [UPDATE] Progress ShareFile Storage Zone Controller — Zero-Day Path Traversal Confirmed, Patches Released

*Previously covered July 11 (emergency shutdown) and July 13 (initial disclosure). New: Progress confirms the vulnerability is a high-severity path traversal and releases patches.*

Progress Software has confirmed that a **high-severity path traversal vulnerability** affecting all ShareFile Storage Zone Controller versions 5.x and 6.x was behind last week's emergency shutdown. An authenticated administrative user can read arbitrary files accessible to the application's service account, write attacker-controlled content to arbitrary directories, and enumerate the server filesystem layout. A CVE has been reserved and will be published in two weeks.

Patches are available: **versions 5.12.5 and 6.0.2**. Progress states there is no indication of unauthorized access to any customer data and no active threat has been identified. Once patches are installed, Storage Zone Controllers can be brought back online.

**Action:** Install patches immediately on any Storage Zone Controllers that were shut down last week, then bring systems back online.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/progress-confirms-sharefile-zero-day-flaw-behind-storage-zone-shutdown/)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] 292 Fake GitHub Repositories Distribute BoryptGrab Infostealer via DLL Side-Loading

Arctic Wolf has identified a campaign involving **292 fake GitHub repositories** impersonating legitimate security products, cryptocurrency tools, developer utilities, and macOS software to distribute a BoryptGrab infostealer variant. The campaign uses a single templated HTML/JS artifact across all impersonated brands, directing victims to download a ZIP archive containing a trojanized `libcurl.dll` side-loaded by a legitimate signed WinGUP updater executable.

The malware targets 19 web browsers, 32 cryptocurrency wallets, Telegram sessions, Discord tokens, Steam sessions, Windows Credential Manager, and Desktop/Documents files. Notably, this BoryptGrab variant **bypasses Chrome's App-Bound Encryption via direct code injection into the browser process** — a previously undocumented capability. Stolen data is exfiltrated to a Russia-based C2 server. GitHub has removed most repositories but several GitHub Pages redirectors remained active at time of reporting. No persistence is established — the malware collects everything in a single execution.

[BleepingComputer / Arctic Wolf](https://www.bleepingcomputer.com/news/security/nearly-300-github-repos-pose-as-legit-software-to-push-malware/)

---

### [NEW] Jalisco and OmegaLord Phishing Kits Target Microsoft 365, Evade MFA

ReliaQuest has analyzed two new phishing toolkits targeting Microsoft 365 accounts. **Jalisco** uses the device-code phishing method, generating fresh Microsoft OAuth device codes in real-time when a victim opens the phishing page — bypassing Microsoft's 15-minute device code validity window designed to fight this attack vector. Attackers register rogue devices under benign names like "Microsoft" or "Windows" and exfiltrate SharePoint/SaaS data within **six minutes** of compromise. OmegaLord uses a fake PDF reader login page to harvest email addresses, passwords, and phone numbers for MFA interception.

Both kits follow the pattern of device-code phishing kits (EvilTokens, Kali365, Tycoon2FA, Venom, Forg365) that continue to proliferate. ReliaQuest recommends reducing the Entra ID device-registration limit from the default of 50 to 1-2, blocking device-code authentication via Conditional Access, and restricting OAuth Device Authorization grants.

[BleepingComputer / ReliaQuest](https://www.bleepingcomputer.com/news/security/new-phishing-kits-target-microsoft-365-accounts-evade-mfa/)

---

### [NEW] U.S. Charges Russian Bulletproof Hosting Operators — $62M in Damages to Ransomware Victims

Federal prosecutors have unsealed charges against three Russian nationals for operating **Media Land** and **ML.Cloud** — bulletproof hosting services that provided infrastructure to ransomware gangs including LockBit, BlackSuit, and Play, causing over $62 million in damages. The services operated across China, Finland, the Netherlands, and the United States, facilitating malware delivery, C2 operations, phishing, and DDoS attacks against U.S. banks, schools, hospitals, and government entities. The State Department is offering a $10 million reward via Rewards for Justice. This follows the EU-UK sanctions package announced yesterday (covered in July 14 digest) that also targeted Media Land and ML.Cloud.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/us-charges-alleged-russian-bulletproof-hosting-service-operators/)

---

### [NEW] LastPass and Bitwarden Users Targeted with Fake Security Alert Phishing Campaign

LastPass is warning users about a phishing campaign using fake security policy update emails sent from `hello@lastpassnewsletter.com`, directing victims to a DocuSign-impersonating landing page at `lastpasscompliance[.]com`. The domain was flagged as malicious by Microsoft Defender and Cloudflare. Bitwarden users are receiving similar emails from `hello@bitwardennewsletter.com` redirecting to `bitwardencompliance[.]com`. This is the third phishing campaign targeting LastPass users in 2026. Users who entered credentials on these sites should immediately change master passwords from a trusted device.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/lastpass-bitwarden-users-targeted-with-fake-security-alerts/)

---

## ⚠️ Vulnerabilities & Patches

### [NEW] SAP July 2026 Security Updates — Critical Flaws in NetWeaver, AppRouter, Commerce Cloud

SAP has addressed 16 vulnerabilities including three critical-severity issues. **CVE-2026-44747** is a memory corruption vulnerability (out-of-bounds write) in NetWeaver Application Server ABAP enabling unauthorized data access, modification, or system unavailability for authenticated attackers. **CVE-2026-27690** is an HTTP Request Smuggling vulnerability in SAP AppRouter (Node.js-based BTP middleware) enabling unauthenticated access to user responses and DoS. **CVE-2026-44761** in SAP Commerce Cloud stems from default credentials allowing attackers to obtain valid access tokens and read/modify data via APIs. CISA has added 14 SAP vulnerabilities to KEV since 2021, including two abused by ransomware.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/sap-warns-of-critical-flaws-in-netweaver-and-commerce-cloud/)

---

### [NEW] VMware Patches 7 Severe Vulnerabilities in Avi Load Balancer

VMware has released security updates for Avi Load Balancer addressing seven vulnerabilities including authentication bypasses and remote code execution flaws. Details are limited at this time.

[SecurityWeek](https://www.securityweek.com/7-severe-vulnerabilities-patched-in-vmware-avi-load-balancer/)

---

### [NEW] Chrome 150 and Firefox 152 — Critical Vulnerabilities Patched

Google has released Chrome 150 and Mozilla has released Firefox 152, both patching critical vulnerabilities. Ensure browser updates are deployed across all endpoints.

[SecurityWeek](https://www.securityweek.com/critical-vulnerabilities-patched-with-fresh-chrome-150-firefox-152-updates/)

---

## 📋 Policy & Industry News

### [NEW] White House Unveils "Gold Eagle" — Federal AI Cyber Threat Clearinghouse

The Trump administration has launched **Gold Eagle**, a federal clearinghouse managed by the Treasury Department for sharing AI-discovered cybersecurity vulnerabilities between government and private sector. The clearinghouse uses Anthropic's Mythos model (among others) to scan systems for vulnerabilities, with a new platform called **VINTS** (Vulnerability Information and Coordination Environment) built with Carnegie Mellon's Software Engineering Institute for receiving third-party vulnerability reports. CISA, DHS, and DoD are contributing partners. The administration noted that AI-assisted vulnerability discovery represents a "step function change" in volume compared to manual scanning.

[CyberScoop](https://cyberscoop.com/trump-gold-eagle-ai-cyber-clearinghouse/)

---

### [NEW] Treasury Sanctions First VPN Service for Aiding Ransomware Gangs

OFAC has sanctioned **1VPNS (First VPN Services)** and its alleged administrator Dmytro Rashevskyi for providing anonymity services "deeply embedded in the cybercriminal ecosystem" to ransomware operators. 1VPNS appeared in virtually every Europol investigation in recent years before the administrator's arrest in a May sting. TRM Labs reported pricing ranging from $58 (Sinobi) to $723 (Anubis) for ransomware group subscriptions. Victims include U.S. municipalities, hospitals, and financial services companies.

[CyberScoop](https://cyberscoop.com/us-sanctions-first-vpn-ransomware/)

---

### [NEW] Spanish Police Dismantle €140M Cyber Fraud and Money Laundering Network

Spanish Police have dismantled a cybercrime organization generating €140 million from investment fraud and BEC attacks, arresting four suspects across Spain, Portugal, and Panama. The operation involved 800+ bank accounts, 120 business accounts, and 67 money mules, with €94 million confirmed laundered and €3 million frozen during raids.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/spanish-police-take-down-140-million-cyber-fraud-ring-arrest-four/)

---

## 🛡️ Defense & Detection

### [NEW] ASEC June 2026 Infostealer Trend Report — Cracks, SEO Poisoning, macOS Polygon C2

AhnLab's ASEC has published its June 2026 infostealer trend report. Key findings: Remus, ACRStealer, LummaC2, and Vidar remain the dominant families. Distribution relies heavily on SEO poisoning to rank cracked software downloads, with Mediafire and Mega as primary hosts. 84.5% of malware uses EXE files; 15.5% uses DLL side-loading (python37.dll, LcMgr.dll). macOS threats are evolving — one variant dynamically fetches C2 addresses from Polygon smart contracts and persists via LaunchAgent. Email-based distribution delivered AgentTesla disguised as a Japanese materials company and DarkCloud as an Indian electronics manufacturer.

[ASEC](https://asec.ahnlab.com/en/94486/)

---

## ⚡ Quick Hits

- **Microsoft Entra ID passkeys default September 1** — Previously covered July 14. SMS/voice authentication retires February 1, 2027. Organizations should audit users still on phishable methods and plan passkey rollout. [BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-entra-id-gets-passkeys-default-authentication-starting-september/)

- **ICS Patch Tuesday** — Siemens, Schneider Electric, and Rockwell Automation have released security updates for industrial control system products. [SecurityWeek](https://www.securityweek.com/ics-patch-tuesday-vulnerabilities-fixed-by-siemens-schneider-rockwell/)

- **Adobe patches critical ColdFusion flaws** — Adobe has released security updates addressing maximum-severity ColdFusion and Campaign vulnerabilities. [SecurityWeek](https://www.securityweek.com/adobe-patches-critical-coldfusion-vulnerabilities/)

- **Dell PCs experience shutdown issues after Windows updates** — Microsoft is blocking July Windows 11 updates on some Dell devices due to shutdowns and performance issues caused by Intel Innovation Platform Framework driver conflicts from the June preview update. [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-some-dell-devices-shut-down-after-windows-update/)
