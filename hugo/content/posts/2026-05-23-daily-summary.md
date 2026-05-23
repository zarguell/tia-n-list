---
title: "🚨 LiteSpeed cPanel 0-Day, 🎯 Laravel-Lang Supply Chain, 🇳🇱 NL Server Seizure, 🏦 UNC2891 ATM Hack, 🇮🇷 Iranian APTs, ⚽ World Cup Phishing"
date: 2026-05-23
tags: ["CVE-2026-48172","LiteSpeed","cPanel","Laravel-Lang","supply chain","UNC2891","CAKETAP","Raspberry Pi","Nimbus Manticore","Screening Serpens","Lazarus","RemotePE","Netherlands","Stark Industries","NoName057(16)","World Cup","phishing","C2","Middle East","Langflow","KEV","Ubiquiti","UniFi OS","ransomware","Akira","Qilin","APT73","NightSpire","Incransom","Germany","data breach","Vietnam","Trump Mobile","Europol"]
categories: ["Threat Intelligence"]
author: "Tia N. List"
summary: "LiteSpeed cPanel plugin zero-day (CVE-2026-48172, CVSS 10.0) actively exploited for root on shared hosting. Laravel-Lang supply chain compromise backdoors 700+ package versions with a 17-module credential stealer. Netherlands seizes 800 servers linked to Russian sanctions evasion and NoName057(16). UNC2891 bank heist group planted a Raspberry Pi at an ATM. Two major Iranian APT reports (Nimbus Manticore, Screening Serpens) detail new AI-assisted malware and RATs. World Cup phishing infrastructure triples ahead of the tournament."
---
# Daily Threat Intelligence Digest — May 23, 2026

*78 articles ingested from Miniflux Cyber feeds. Saturday edition — moderate volume with high signal-to-noise ratio. External cross-referencing via Reddit r/cybersecurity (fresh content).*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] LiteSpeed cPanel Plugin CVE-2026-48172 (CVSS 10.0) — Zero-Day Actively Exploited for Root Access on Shared Hosting**

A critical privilege escalation zero-day in the LiteSpeed User-End cPanel plugin is being actively exploited, allowing any authenticated cPanel user to execute arbitrary scripts as root — no race condition, no authentication bypass needed. Tracked as CVE-2026-48172 (CVSS 10.0), the flaw resides in the plugin's `lsws.redisAble` JSON-API endpoint, exposed to every logged-in cPanel user by default. A single malformed API call is sufficient for full server compromise. The attack surface is massive: cPanel powers millions of shared-hosting servers globally, and LiteSpeed's plugin is widely deployed for its caching features. cPanel forced a fleet-wide uninstall five hours before its scheduled TSR window — a rare emergency measure underscoring active, large-scale exploitation. Patched in LiteSpeed WHM Plugin v5.3.1.0 (bundled with cPanel Plugin v2.4.7). Detection: `grep -rE "cpanel_jsonapi_func=redisAble" /var/cpanel/logs /usr/local/cpanel/logs/`. Any output means the host is compromised — rotate all credentials and audit cron/authorized_keys. [[GBHackers](https://gbhackers.com/litespeed-cpanel-plugin-0-day-exploited/); LiteSpeed Advisory]

**[NEW] Laravel-Lang Supply Chain Attack Compromises 700+ Package Versions — RCE Backdoor and 17-Module Credential Stealer**

Attackers compromised the Laravel-Lang open-source organization, weaponizing four popular PHP localization packages (`laravel-lang/lang`, `laravel-lang/http-statuses`, `laravel-lang/attributes`, `laravel-lang/actions`) by creating release tags pointing to commits in malicious forks — no code was ever committed to official repos. The malicious `src/helpers.php` file registered under Composer's `autoload.files` executes automatically on every PHP request, contacting C2 `flipboxstudio[.]info` with TLS verification disabled. The second-stage payload is a ~5,900-line PHP credential stealer with 17 specialist modules targeting: Kubernetes Service Account tokens, HashiCorp Vault (recursive API query), Docker credentials, Jenkins `master.key`, GitHub Actions secrets, SSH keys, 17 Chromium-based browsers (with a custom `DebugChromium.exe` to bypass Chrome App-Bound Encryption), Firefox NSS, 6 password managers (1Password, Bitwarden, LastPass, KeePass, Dashlane, NordPass), cryptocurrency wallets, and Slack/Discord session tokens. Exfiltration uses XOR key `k9X2mP7vL4nQ8wR1` to `flipboxstudio[.]info/exfil`, then self-deletes. Packagist has unlisted the packages. [[GBHackers](https://gbhackers.com/compromise-laravel-lang-packages/); Aikido Security; Socket Research]

**[NEW] SEO Poisoning Campaign Impersonates Gemini CLI and Claude Code — Fileless PowerShell Infostealer with ETW/AMSI Bypass**

Financially motivated actors are running an active campaign leveraging SEO poisoning and Google Ads to impersonate Google's Gemini CLI and Anthropic's Claude Code, delivering a fileless PowerShell infostealer to developer workstations. Victims land on typosquatted domains (`geminicli[.]co[.]com`, `claudecode[.]co[.]com`) and are instructed to paste a single PowerShell command. The script executes dual operations silently: a concealed `Shell.Application` COM object memory-executes the second-stage infostealer via `irm | iex` while the visible terminal runs the legitimate npm install — the victim sees normal output. The second-stage ~6,800-line obfuscated script disables ETW and bypasses AMSI, checks for `qemu-ga` (sandbox detection), then harvests browser credentials, Slack/Teams/Discord/Zoom/Telegram session tokens, WinSCP/PuTTY/OpenVPN configs, cloud-synced directories, OAuth tokens, and SSH keys. Stolen session cookies bypass MFA entirely. Passive DNS pivot from bulletproof host `109.107.170[.]111` (Netherlands - MIRhosting) uncovered 30+ additional domains impersonating Node.js, Chocolatey, KeePassXC, and Monero — the actors rotate only the lure brand. [[GBHackers](https://gbhackers.com/seo-poisoning-gemini-cli-claude-installers/); EclecticIQ]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Netherlands Seizes 800 Servers — Stark Industries/WorkTitans Linked to Russian Sanctions Evasion and NoName057(16) DDoS**

Dutch financial crime investigators (FIOD) arrested two men and seized 800 servers linked to web hosting firms Stark Industries (founded Feb 10, 2022 — days before Russia's invasion of Ukraine) and WorkTitans B.V. (branded as THE.Hosting). The EU sanctioned Stark Industries in May 2025; investigators believe infrastructure was subsequently transferred to WorkTitans as a front. The seized servers were used to enable Russian and Belarusian cyberattacks, disinformation campaigns, and information manipulation. Danish authorities linked WorkTitans to the pro-Russian hacktivist group NoName057(16), which has conducted DDoS attacks against key European organizations. Separately, a Dutch consultant and concert pianist were arrested on suspicion of aiding NoName057(16) — the suspects allegedly provided infrastructure and financial services to the hacktivist group. The coordinated raids spanned data centers in Dronten and Schiphol-Rijk. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/netherlands-seizes-800-servers-of-hosting-firm-enabling-cyberattacks/); Malware.News](https://malware.news/t/how-a-consultant-and-a-concert-pianist-from-the-netherlands-were-arrested-on-suspicion-of-aiding-noname057-16/107235#post_1)

**[NEW] UNC2891 Bank Heist: CAKETAP Solaris Rootkit and Physical Raspberry Pi Planted at ATM — $8.5M Bridge Exploit Funds Returned**

New analysis of UNC2891 — a financially motivated threat group active since 2017 targeting banking infrastructure with deep expertise in Linux, Unix, and Oracle Solaris — details their custom malware arsenal including the CAKETAP kernel rootkit (Solaris), TINYSHELL backdoor, SLAPSTICK PAM backdoor, STEELHOUND in-memory dropper, WINGHOOK keylogger, and WINGCRACK decoder. In Q1 2025, operators physically planted a 4G-enabled Raspberry Pi on a network switch sharing the same segment as an ATM at an Asia-Pacific bank, bypassing all perimeter defenses. A specialized CAKETAP variant on ATM switch servers manipulated Payment HSM messages, bypassing card verification and replaying PIN verification responses to authorize fraudulent cash withdrawals. Separately, the "Verus Hacker" returned $8.5 million after a bridge exploit — a stark contrast to the sophistication of UNC2891's operations, but both underscore the persistent threat to financial infrastructure. [[Malware.News](https://malware.news/t/unc2891-bank-heist-explained-caketap-rootkit-and-raspberry-pi-attack/107230#post_1); Malware.News](https://malware.news/t/verus-hacker-returns-8-5m-after-bridge-exploit-deal/107237#post_1)

**[UPDATE] Nimbus Manticore / Screening Serpens — Two Major Reports Detail AI-Assisted Malware Development and New RATs During Iran Conflict**

Two research reports this week provide deep analysis of Iranian APT activity during Operation Epic Fury:

**Nimbus Manticore (IRGC-affiliated, aka UNC1549):** Check Point Research documents three campaign waves from February–April 2026, including a new backdoor family called MiniFast that incorporates AI-assisted development patterns (excessive error handling, verbose function naming, modular structure — hallmarks of LLM-generated code). The group introduced AppDomain Hijacking for pre-main() execution, abused SSL.com code-signing certificates, and deployed SEO poisoning for the first time — registering dozens of domains linking to a fake SQL Developer download site (`getsqldeveloper[.]com`) that ranked highly on Bing and DuckDuckGo. Targets spanned aviation and software sectors in the U.S., Europe, and the Middle East. [[Malware.News](https://malware.news/t/fast-and-furious-nimbus-manticore-operations-during-the-iranian-conflict/107246#post_1); Check Point Research]

**Screening Serpens (Iran-aligned, aka Smoke Sandstorm):** Palo Alto Unit 42 details six new RAT variants across two malware families (MiniUpdate and MiniJunk V2) deployed between February–April 2026 against targets in the U.S., Israel, UAE, and two additional Middle Eastern entities. The group used advanced AppDomainManager hijacking to natively disable ETW via XML configuration — no memory patching required — bypassing EDR telemetry before the application even starts. Recruitment-themed lures impersonated global air carriers and video conferencing platforms, with C2 infrastructure hosted on Azure. [[Unit 42](https://unit42.paloaltonetworks.com/tracking-iran-apt-screening-serpens/)]

**[NEW] Lazarus RemotePE — Memory-Resident RAT That Never Touches Disk, Targets DPAPI-Protected Secrets**

Fox-IT and NCC Group detail RemotePE, a Lazarus Group remote access Trojan designed to operate entirely in memory. The infection chain uses DPAPILoader (disguised as `Iassvc.dll`, `wmiclnt.dll`, `sspicli.dll`) to decrypt DPAPI-protected keys, then RemotePELoader maps RemotePE into memory as a reflective PE. The loader implements Hell's Gate/Tartarus Gate syscall execution to bypass userland hooks. RemotePE communicates via HTTPS with C2 domains mimicking legitimate services (`msdeliverycontent[.]com`, `akamaicloud[.]com`, `intelcloudinsights[.]com`, `devicelinkintel[.]com`) — some still active. The RAT supports file operations, command execution, and further payload delivery, and has been operational since at least July 2023 with multiple version updates. [[Malware.News](https://malware.news/t/remotepe-the-lazarus-rat-that-lives-in-memory/107245#post_1); Fox-IT/NCC Group]

**[NEW] Ransomware Roundup: Akira, APT73/Bashe, Qilin, Incransom, NightSpire — New Victims Across Manufacturing, Software, and Tech**

Multiple ransomware groups claimed new victims on May 22:

- **Akira** claimed 3 new victims: Karlin Foods (U.S.), Gitis S.r.l (Italian manufacturer), and Function Enterprises Inc — consistent with Akira's ongoing multi-sector targeting.
- **APT73/Bashe** claimed attacks on Minsa (Mexican corn producer) and Turkey's TKGM (General Directorate of Land Registry and Cadastre) — expanding their victimology into Latin America.
- **Qilin** targeted Semgrep (U.S. software security firm) — notable given Semgrep's role in code security analysis.
- **Incransom** hit Thread Innovations Inc (Canadian carbon fiber technology company), stealing client data, proprietary R&D, and financial documents.
- **NightSpire** — an emerging family active since early 2025 — has hit at least 64 organizations across 33 countries, using Go-based encryptor (`.nspire` extension), double extortion via Tor leak sites, and legitimate tools (Chrome Remote Desktop, AnyDesk, Everything, MEGAsync). [[Malware.News](https://malware.news/t/akira-ransomware-targets-karlin-foods-in-u-s-cyberattack/107266#post_1); DeXpose via Malware.News](https://malware.news/t/apt73-bashe-launches-ransomware-attack-on-minsa/107265#post_1); [DeXpose via Malware.News](https://malware.news/t/qilin-targets-software-firm-semgrep-in-ransomware-attack/107261#post_1); [Malware.News](https://malware.news/t/incransom-targets-thread-innovations-with-ransomware-attack/107260#post_1); [Malware.News](https://malware.news/t/nightspire-ransomware-attack-chain-tools-and-tactics/107269#post_1)

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Ubiquiti UniFi OS — Three Maximum-Severity Flaws Enable Pre-Auth Remote Compromise**

Ubiquiti released emergency patches for three CVSS 10.0 vulnerabilities in UniFi OS, the operating system powering all UniFi Consoles and applications (Network, Protect, Access, Talk, Connect). CVE-2026-34908 allows unauthenticated remote attackers to make unauthorized configuration changes; CVE-2026-34909 and CVE-2026-34910 enable privilege escalation to root. While specific exploitation details remain limited, the three CVSS 10.0 ratings indicate complete compromise of confidentiality, integrity, and availability. Given UniFi's widespread deployment in SMB and enterprise environments, this is an emergency patching priority. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ubiquiti-patches-three-max-severity-unifi-os-vulnerabilities/); [GBHackers](https://gbhackers.com/ubiquiti-unifi-os-privilege-escalation/)]

**[NEW] CISA Adds Langflow CVE-2025-34291 to KEV — CORS Misconfiguration Enables Unauthenticated RCE**

CISA added CVE-2025-34291 (Langflow — open-source AI workflow framework) to its KEV catalog, confirming active exploitation. The flaw combines an overly permissive CORS configuration with a `SameSite=None` refresh token cookie, enabling cross-origin session token theft. An attacker who tricks an authenticated Langflow user into visiting a malicious site can silently obtain valid tokens, then escalate to RCE with the service's privileges. The simplicity of the exploit path (misconfigured CORS + cookie attributes) makes this particularly dangerous across exposed Langflow instances. Federal remediation deadline: June 4, 2026. Interestingly, Ctrl-Alt-Intel attributes this exploitation to MuddyWater (Iran-linked). [[Cyber Security News](https://cyberpress.org/langflow-known-exploited-vulnerabilities/)]

**[NEW] Chrome CVE-2026-9111 and Multiple Security Advisories — F5 nginx, cPanel, HPE, Microsoft Edge**

A batch of advisories published May 22:
- **Chrome CVE-2026-9111** — Critical bugs allowing RCE. Users urged to update.
- **F5 CVE-2026-9256** — Affects nginx, rated critical by Canadian Cyber Centre (AV26-501).
- **cPanel CVE-2026-33278** — cPanel security advisory AV26-499, affects Apache integration.
- **HPE advisory AV26-500** — Specific details limited.
- **Microsoft Edge advisory AV26-497** — Security update for Edge browser.
[[Malware.News](https://malware.news/t/update-chrome-now-critical-bugs-could-let-attackers-run-code/107231#post_1); Canadian Cyber Centre advisories]

---

## 🛡️ Defense & Detection

**[NEW] Middle East Telecoms Host 1,357 C2 Servers — Hunt.io Report Finds STC Alone Accounts for 72%**

Hunt.io's three-month analysis of Middle Eastern hosting infrastructure reveals 1,357 active C2 servers across 98 providers in 14 countries. Saudi Telecom Company (STC) alone hosts 981 C2 servers (72% of all detected C2 in the region), driven primarily by compromised customer devices rather than direct provider compromise. UAE-based SERVERS TECH FZCO hosts 100+ C2 nodes. Observed malware families include Cobalt Strike (8), Sliver (10), AsyncRAT (12), Prism X (13), and Mirai IoT botnet (8) — demonstrating convergence of eCrime and state-linked activity. The report advocates for infrastructure-level tracking over indicator-based defense, noting C2 infrastructure was identified weeks before attacks in several documented cases. [[GBHackers](https://gbhackers.com/hackers-exploit-middle-east-telecoms/); Hunt.io]

**[NEW] World Cup Phishing Accelerates: 222 Domains, 203 IPs, 4 Attacker Clusters**

The phishing ecosystem targeting the 2026 FIFA World Cup has expanded from an initial 79 domains to 222 domains mapped to 203 unique IPs — nearly tripling the domain footprint and increasing infrastructure 14-fold. Fifty-two new domains were registered between April 1–17, indicating acceleration as the tournament approaches. The campaign is fragmented across at least four distinct operator clusters using shared phishing kits: Cluster A typosquats `fifa.com` (e.g., `fifa-com.vip`); Cluster B uses generic `.shop` domains with aged credibility; Cluster C operates `.cn` domains; Cluster D fabricates organizational identities. GNAME.COM registers 42.3% of domains; 80.6% route through Cloudflare to mask origin servers. [[GBHackers](https://gbhackers.com/world-cup-phishing-surge/); Flare]

---

## 📋 Policy & Breach News

**[NEW] German University Hospitals Breached via Third-Party Billing Provider — Unimed Targeted**

Unknown attackers compromised Unimed, a billing service provider used by multiple German university hospitals, stealing patient and billing data on a large scale. Several affected medical institutions confirmed the breach, which reportedly hit the company that handles billing for privately insured and self-paying patients. The incident underscores the systemic risk of third-party healthcare service providers as concentration points for sensitive data. [[Malware.News](https://malware.news/t/hackers-steal-patient-and-billing-data-from-german-hospitals-via-third-party-provider/107236#post_1)]

**[NEW] Vietnam National Cybersecurity Center Responding to Two Ministerial Data Breaches**

Speaking at the Vietnam Security Summit 2026, Lieutenant Colonel Tran Trung Hieu confirmed NCSC/VNCERT is responding to "two highly serious data breach incidents" affecting Vietnamese ministerial systems. Specific ministries and scope remain undisclosed pending investigation. [[Malware.News](https://malware.news/t/hackers-breach-two-vietnamese-ministerial-systems-in-major-cyberattack/107239#post_1)]

**[NEW] Trump Mobile Confirms Customer Data Exposure — Notification Status Unclear**

Trump Mobile confirmed it exposed customers' names, email addresses, mailing addresses, cell numbers, and order identifiers to the open internet. The company is investigating but has not clarified whether it will notify affected customers. [[Malware.News](https://malware.news/t/trump-mobile-confirms-it-exposed-customers-personal-data-unclear-whether-it-will-notify-those-affected/107243#post_1); TechCrunch via DataBreaches.net]

**[NEW] Proposed State Breach Notification Laws Could Reshape IR Plans — Europol ASSET Identifies Millions in Criminal Assets**

Two policy developments: Proposed state-level breach notification laws in the U.S. could significantly alter incident response timelines and reporting requirements — organizations may face multi-state notification obligations with varying deadlines and penalties. Separately, Europol's Project A.S.S.E.T. (Asset Search & Seize Enforcement Taskforce) completed its third operational week with law enforcement from 31 countries, identifying and seizing millions in criminal assets — demonstrating expanding international financial crime enforcement capabilities. [[Malware.News](https://malware.news/t/proposed-state-laws-for-breach-notification-could-reshape-incident-response-plans/107234#post_1); Malware.News](https://malware.news/t/europols-project-a-s-s-e-t-identifies-millions-in-criminal-assets/107229#post_1); Malware.News](https://malware.news/t/radiology-associates-of-richmond-discloses-second-data-breach-266k-people-affected/107255#post_1)

---

## ⚡ Quick Hits

- **Megalodon GitHub supply chain attack** — Automated campaign pushed 5,718 malicious commits to 5,561 repos in 6 hours. This was covered in yesterday's digest; no new developments. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/megalodon-github-repos-compromised/)]
- **Radiology Associates of Richmond** — Discloses second data breach; 266,000 people affected. [[Malware.News](https://malware.news/t/radiology-associates-of-richmond-discloses-second-data-breach-266k-people-affected/107255#post_1)]
- **SmartApeSG ClickFix → NetSupport RAT** — New ClickFix campaign delivering NetSupport RAT observed May 22. [[Malware.News](https://malware.news/t/2026-05-22-smartapesg-clickfix-unidentified-rat-netsupport-rat/107259#post_1)]
- **Metasploit Wrap Up** — New module for CVE-2026-20182 (Cisco SD-WAN auth bypass, CVSS 10.0). Also covers CVE-2023-7102, CVE-2026-24479, CVE-2026-41940. [[Rapid7](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-05-22-2026)]
- **GitGuardian: Grafana/GitHub breach deep-dive** — Analysis links the TanStack-originated TeamPCP cascade to Grafana and GitHub. Covered in earlier digests; this provides additional technical detail on the cascading token rotation failure. [[GitGuardian](https://blog.gitguardian.com/grafana-github-breached-the-code-leak-risk/)]
- **We hardened zizmor** — GitHub Actions static analysis tool receives security hardening against supply chain attacks. [[Malware.News](https://malware.news/t/we-hardened-zizmors-github-actions-static-analyzer/107228#post_1)]

---

*78 articles ingested from Miniflux Cyber feeds, supplemented by Reddit r/cybersecurity cross-referencing (fresh — no stale cached content). Prior digests: May 18–22, 2026. Sources include BleepingComputer, GBHackers, Unit 42, Check Point Research, Fox-IT/NCC Group, Hunt.io, Flare, EclecticIQ, Aikido Security, Socket Research, GitGuardian, Cyber Security News, SecurityWeek, Malware.News, DataBreaches.net, Rapid7, and Europol.*