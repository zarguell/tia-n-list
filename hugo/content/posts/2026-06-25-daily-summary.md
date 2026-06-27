---
title: "🟠 Cisco SD‑WAN zero‑day exposed, Ubiquiti/Lantronix KEV, Amadey/StealC takedown, Mistic RAT, macOS EDR bypass, 25‑year‑old curl bug"
date: 2026-06-25
tags: ["Cisco","SD-WAN","CVE-2026-20245","Mandiant","CISA KEV","Ubiquiti","Lantronix","Operation Endgame","Amadey","StealC","Mistic RAT","Woodgnat","macOS","EDR bypass","curl","Chrome 149","CVE-2026-8932","CVE-2026-11645","GitLab","PyPI","supply chain","n8n","Jenkins"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Cisco SD-WAN zero-day (CVE-2026-20245) exploited since March with root access; CISA adds 4 max-severity Ubiquiti/Lantronix flaws to KEV under active exploitation; Operation Endgame simultaneously disrupts Amadey and StealC malware networks recovering 27M credentials; Woodgnat IAB deploys new Mistic RAT linking to 6 ransomware families; macOS non-admin EDR bypass demonstrated against CrowdStrike and Kandji; 25-year-old curl vulnerability patched in 8.21.0; Chrome 149 patches 18 severe vulns including actively exploited CVE-2026-11645."
---
# Daily Threat Intelligence Digest — June 25, 2026

*63 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Cisco SD-WAN Zero-Day (CVE-2026-20245) — Mandiant Reveals Root Access Achieved via Rogue Peer Connections, Active Since March**

Mandiant has published detailed forensics on how an unknown threat actor exploited CVE-2026-20245, a high-severity command injection flaw in Cisco Catalyst SD-WAN Manager (vManage), Controller (vSmart), and Validator (vBond), to create rogue root accounts on targeted devices at a communications service provider. This is the **seventh actively exploited SD-WAN zero-day this year** — a staggering count that underscores what Mandiant calls the "living off the edge" paradigm. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/mandiant-reveals-how-cisco-sd-wan-zero-day-attacks-gained-root-access/); [CyberScoop](https://cyberscoop.com/cisco-sd-wan-zero-day-exploit-communications-provider/); [SecurityWeek](https://www.securityweek.com/cisco-sd-wan-zero-day-exploited-months-before-patching/)]

The intrusion began with unauthorized SD-WAN peering connections observed as early as **March 2026**, possibly exploiting previously disclosed authentication bypass CVEs (CVE-2026-20127, CVE-2026-20182). After gaining access via the `vmanage-admin` account, the attacker changed the default admin password, extracted edge device and controller configurations, exploited CVE-2026-20245 through a crafted CSV file (`evil_tenant.csv`), and created a rogue account named **"troot"** with root-level privileges. Mandiant noted extensive anti-forensic measures: configuration file backups before modification, deletion of the malicious CSV payload, log clearing, and a validation script to confirm traces were removed. Cisco has released patches.

**Hunting hypothesis:** Monitor SD-WAN Manager devices for unauthorized peering connections, unexpected `vmanage-admin` password changes followed by restoration, and CSV upload operations to the tenant-upload CLI feature.

---

**[NEW] CISA Adds Ubiquiti and Lantronix Flaws to KEV — Max-Severity Exploitation Confirmed, BOD 26-04 Clock Starts**

CISA has added **four critical vulnerabilities** to its Known Exploited Vulnerabilities (KEV) catalog, all confirmed under active exploitation. The Ubiquiti flaws affect UniFi OS: CVE-2026-34908 (access control bypass), CVE-2026-34909 (directory/path traversal), and CVE-2026-34910 (improper input validation enabling RCE) — chainable for **full remote code execution with elevated privileges** as demonstrated by Bishop Fox, which also released a free detection script. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-warns-of-max-severity-ubiquiti-flaws-exploited-in-attacks/); [SecurityWeek](https://www.securityweek.com/critical-ubiquiti-vulnerabilities-in-attackers-crosshairs/)]

The fourth addition is CVE-2025-67038, a critical root-level command injection in **Lantronix EDS5000** serial-to-ethernet servers (firmware 2.1.0.0R3) where the supplied username is concatenated directly into a shell command without sanitization. Patched in firmware 2.2.0.0R1. Federal agencies have three days per BOD 26-04 to apply updates.

**Recommended action:** Update Ubiquiti UniFi OS to latest patched version. Check for Bishop Fox's detection script on GitHub. Patch Lantronix EDS5000 to 2.2.0.0R1. For all affected products, verify no unauthorized access or configuration changes occurred.

---

**[NEW] Operation Endgame Disrupts Amadey and StealC — Simultaneous Court-Ordered Takedown Takes Down 326 Servers, Recovers 27M Credentials**

Microsoft, Europol, and partners from five countries executed a novel dual-malware disruption targeting the shared infrastructure of **Amadey** botnet and **StealC** infostealer — both sold as malware-as-a-service and frequently used together in ransomware intrusion chains. For the first time, a court-authorized takedown under the **RICO Act** simultaneously targeted two cybercrime tools. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/amadey-stealc-malware-operations-disrupted-in-operation-endgame-action/); [CyberScoop](https://cyberscoop.com/microsoft-amadey-stealc-takedown/); [SecurityWeek](https://www.securityweek.com/microsoft-and-allies-smash-shared-infrastructure-of-amadey-and-stealc-malware/)]

Results: **326 servers and 142 domains** seized, blocked, or sinkholed. **€41 million (~$47M)** in cryptocurrency linked to criminal activity identified. **Approximately 27 million credentials** recovered from **over 385,000 compromised systems**. The operation also targeted **SocGholish (FakeUpdates)** infrastructure. Private partners included ESET, Proofpoint, IBM X-Force, Bitsight, and Spamhaus. Microsoft's Digital Crimes Unit used its AI Copilot to identify connections between the two malware families as part of a single criminal enterprise.

Between them, Amadey (active since 2018) and StealC (active since 2023) were linked to **140,000+ infected devices in the first two weeks of May alone**. StealC has been the infostealer behind recent ClickFix campaigns on TikTok. While infrastructure disruptions rarely stop operations permanently unless arrests are made, this is the most significant coordinated action against the infostealer-as-a-service ecosystem to date.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Woodgnat IAB Deploys 'Mistic' RAT — New Backdoor Provides Ransomware Affiliates With Network Access to Qilin, Akira, Black Basta, and Three Other Ransomware Groups**

Broadcom's Symantec and Carbon Black threat hunter team identified **Backdoor.Mistic**, a new remote access trojan deployed by the initial access broker tracked as **Woodgnat (KongTuke)**, active since at least May 2024. Since April 2026, Woodgnat has been deploying Mistic against organizations across education, insurance, IT, and professional services sectors. [[SecurityWeek](https://www.securityweek.com/new-mistic-rat-opens-door-to-several-ransomware-families/); [GBHackers](https://gbhackers.com/modelorat-and-mistic-backdoor/)]

Mistic is deployed as a DLL via **sideloading** and provides file download/upload, code execution, folder manipulation, and configurable check-in frequency. Additional tools observed in intrusions include Curl, Reg.exe, PowerShell, Certutil, and WMIC for recon and lateral movement. Woodgnat's initial access vector relies on compromised WordPress sites and **ClickFix/FileFix/CrashFix** social engineering — plus a newer Microsoft Teams IT-support lure. The targeting is opportunistic: "cast a wide net, then assess which organizations to sell access to." Previously, Woodgnat deployed ModeloRAT. Linked ransomware affiliates: **Qilin, Interlock, Rhysida, Akira, 8Base, and Black Basta.**

---

**[NEW] macOS EDR Bypass via Legitimate OS Behavior — Standard User Account Can Silently Unload CrowdStrike Falcon, Permanently Deactivate Kandji MDM**

XM Cyber demonstrated a macOS attack technique requiring only a **standard (non-admin) user account** to silently disable enterprise endpoint security tools by chaining legitimate macOS behaviors rather than exploiting software vulnerabilities. The attack chain exploits the persistence of the kernel's code-signing trust cache after a legitimately signed application executes, injecting malicious payloads into application Interface Builder (NIB) files to invoke privileged XPC methods. [[SecurityWeek](https://www.securityweek.com/macos-weaknesses-chained-to-silently-disable-endpoint-security-agents/)]

Successfully demonstrated against:
- **CrowdStrike Falcon Sensor** — fully unloaded from standard user account. CrowdStrike fixed the issue, paid a bounty, and added detection/prevention on all sensor versions.
- **Kandji MDM** — permanently deactivated via two-stage chain (CVE-2026-39118 assigned).
- **Third unnamed EDR vendor** — confirmed vulnerable, patch in progress.

Researcher Hillel Pinto will release **XPC Hunter**, an open-source tool automating XPC privilege escalation surface discovery, at Black Hat US 2026.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] 25-Year-Old Curl Vulnerability (CVE-2026-8932) — AI-Discovered Flaw Allows Connection Reuse After Certificate Change**

AISLE's autonomous vulnerability detection platform identified the **oldest security issue ever reported in curl**, a bug dating back approximately 25 years. CVE-2026-8932 exists because libcurl could **reuse an existing connection even after client certificate or private key settings had changed**, potentially exposing credentials to the wrong endpoint. Fixed in curl release **8.21.0** (June 24, 2026). AISLE discovered 6 CVEs in curl total this year. [[SecurityWeek](https://www.securityweek.com/25-year-old-vulnerability-patched-in-curl/); [AISLE](https://aisle.com/blog/aisle-discovers-6-new-cves-in-curl-including-the-oldest-issue-ever-reported); [Daniel Stenberg](https://daniel.haxx.se/blog/2026/05/11/mythos-finds-a-curl-vulnerability/)]

The curl project noted this is the oldest vulnerability ever found in the tool, underscoring both the value of AI-assisted code auditing for legacy codebases and the difficulty of discovering subtle logical errors in decades-old network protocol implementations.

---

**[NEW] Chrome 149 Addresses 18 Severe Vulnerabilities — CVE-2026-11645 Actively Exploited, 10 Use-After-Free Bugs Fixed**

Google released Chrome 149 (versions 149.0.7827.102/.103) patching **18 security vulnerabilities**, including **10 use-after-free bugs** — several in the WebGL rendering engine — and **CVE-2026-11645**, an out-of-bounds read/write flaw in the V8 JavaScript engine **confirmed as actively exploited** in the wild. [[SecurityWeek](https://www.securityweek.com/chrome-149-update-resolves-18-severe-vulnerabilities/); [Rescana](https://www.rescana.com/post/active-exploitation-alert-google-chrome-149-critical-vulnerabilities-patched-amid-ongoing-cve-2026-11645-attacks)]

**Recommended action:** Update Chrome/Chromium browsers immediately. Enterprise admins should push via group policy. This is the second actively exploited Chrome zero-day this quarter.

---

## ⚡ Quick Hits

- **Another BreachForums Clone Shuts Down** — The `breached[.]hn` clone listed itself for sale at $3,000, dropped to $1,500, and shut down entirely, citing fears of the ShinyHunters extortion group. The BreachForums ecosystem continues to fragment under legal and internal pressure. [[DataBreaches.net](https://databreaches.net/2026/06/24/another-breachforums-clone-shuts-down-citing-fears-of-shinyhunters/)]

- **GitLab Ships Urgent Patches (19.1.1, 19.0.3, 18.11.6)** — Most severe: CVE-2026-10086, an XSS vulnerability in GitLab EE's Analytics dashboard allowing authenticated developers to execute arbitrary client-side code in other users' sessions. Also: CVE-2026-12053 (sensitive info disclosure via Duo Workflows). [[GitLab Docs](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-1-1-released/); [SecurityWeek](https://www.securityweek.com/gitlab-patches-code-execution-information-disclosure-vulnerabilities/)]

- **Leaked PyPI Tokens: 62 Still Valid, 125 Projects Exposed** — GitGuardian's Public Monitoring found 62 live PyPI API tokens on GitHub — despite GitHub's automated scanning — affecting 125 projects with ~25,000 monthly downloads. PyPI security team invalidated the tokens after coordinated disclosure. Critical reminder: scope PyPI tokens to single projects. [[GitGuardian](https://blog.gitguardian.com/hunting-leaked-pypi-tokens-62-live-125-packages-exposed/)]

- **Jenkins Advisory** — Multiple plugin vulnerabilities patched: XXE in Assembla Plugin, path traversal in External Workspace Manager, RCE via OWASP ZAP Plugin (builds executed on controller), and Script Security sandbox bypass. [[Canadian Centre for Cyber Security (AV26-629)](https://malware.news/t/jenkins-security-advisory-av26-629/108198#post_1)]

- **n8n Patches Multiple Flaws** — Versions prior to 2.28.1/2.27.4/1.123.61 affected by HTTP domain restriction bypass via AI Agents MCP Connector, prototype pollution via workflow credentials enabling user/project enumeration, cross-issuer token exchange binding flaws, and shared credential header leak via HTTP request pagination expression. Notable: the MCP Connector bypass highlights a new attack surface at the intersection of AI agent tooling and workflow automation. [[Canadian Centre for Cyber Security (AV26-628)](https://malware.news/t/n8n-security-advisory-av26-628/108196#post_1)]
