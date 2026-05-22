---
title: "🐧 Copy Fail KEV, ⚡ Megalodon 5.5K Repos, 🔴 Google Chromium Leak, 🏭 Foxconn 8TB, 🕸️ First VPN Takedown"
date: 2026-05-22
tags: ["Copy Fail","CVE-2026-31431","Megalodon","supply-chain","Chromium","Foxconn","Nitrogen","Kimwolf","First VPN","Trend Micro","art-template","Drupal","Cisco","Apache OFBiz","Microsoft Edge","DBIR"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA adds Copy Fail (CVE-2026-31431) Linux LPE to KEV with active exploitation confirmed. Megalodon campaign compromises 5,500+ GitHub repos in 6 hours. Google accidentally exposes unfixed Chromium Service Worker flaw enabling silent JS RCE. Foxconn ransomware leaks 8TB of NVIDIA/Apple IP. First VPN takedown seizes 33 servers across 27 countries. Prioritize Linux kernel patching, audit GitHub Actions workflows, and restrict OAuth device-code flows."
---

# Daily Threat Intelligence Digest — May 22, 2026

*89 articles ingested from Miniflux Cyber feeds. External cross-referencing via TLDR InfoSec (May 20 — gap detection: Copy Fail, Edge passwords), Reddit r/cybersecurity (fresh content), and tl;dr sec #329 (May 21 — AI honeypots, GitHub Action canaries, MDASH).*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Copy Fail (CVE-2026-31431) — CISA Adds to KEV with Active Exploitation Confirmed; 732-Byte PoC Roots Any Linux Since 2017**

CISA has added the "Copy Fail" Linux kernel privilege escalation vulnerability to its Known Exploited Vulnerabilities (KEV) catalog, confirming active in-the-wild exploitation. Tracked as CVE-2026-31431 (CVSS 7.8), the flaw resides in the Linux kernel's `algif_aead` module — a cryptographic algorithm interface. Theori researchers disclosed it alongside a "100% reliable" 732-byte Python exploit that works unmodified across every major Linux distribution shipping kernels built since 2017, including Ubuntu 24.04 LTS, Amazon Linux 2023, RHEL 10.1, and SUSE 16. The exploit writes 4 controlled bytes into the page cache of any readable file (e.g., `/usr/bin/su`) without modifying the on-disk binary, making it invisible to file-integrity monitoring. It is deterministic (no race condition), cross-container, and leaves no forensic trace on disk. Microsoft, Palo Alto Unit 42, and CERT-EU have all issued urgent advisories. The upstream fix was committed April 1, but distribution patches remain pending across several vendors. Interim mitigation: `echo "install algif_aead /bin/false" > /etc/modprobe.d/disable-algif.conf && rmmod algif_aead`. CISA orders federal agencies to patch by June 4 under BOD 22-01. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-says-copy-fail-flaw-now-exploited-to-root-linux-systems/); [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/01/cve-2026-31431-copy-fail-vulnerability-enables-linux-root-privilege-escalation/); [CERT-EU](https://cert.europa.eu/publications/security-advisories/2026-005/pdf); [r/cybersecurity](https://old.reddit.com/r/cybersecurity/) (641↑)]

**[NEW] Megalodon Automated Campaign Compromises 5,500+ GitHub Repositories in 6 Hours — CI/CD Secrets and Cloud Credentials Harvested**

An automated supply chain attack dubbed "Megalodon" pushed 5,718 malicious commits to 5,561 repositories in a single six-hour window on May 18, 2026. Discovered by SafeDep's Malysis engine, the campaign weaponized GitHub Actions workflows using throwaway accounts with randomized 8-character usernames. Two payload variants were deployed: a mass variant (SysDiag) that injected a `.github/workflows/ci.yml` file auto-triggered on every push/pull request, and a targeted variant (Optimize-Build) using `workflow_dispatch` triggers that remain dormant until explicitly fired via the GitHub API — leaving zero failed builds, no CI red flags, and no visible workflow runs. The payload exfiltrates environment variables, 27 credential file paths, cloud metadata (AWS IMDSv2, GCP, Azure), OIDC tokens for identity impersonation, and source code. In one confirmed case, the npm package `@tiledesk/tiledesk-server` versions 2.18.6–2.18.12 carried the backdoor into production without any application code changes. [[Cyber Security News](https://cyberpress.org/megalodon-malware-compromised/); [GBHackers](https://gbhackers.com/megalodon-malware-rapidly-infects-over-5500-github-repositories/)]

**[NEW] Google Accidentally Exposes Unfixed Chromium Service Worker Flaw — Silent JS RCE on All Chromium Browsers**

Google accidentally leaked details of an unfixed Chromium vulnerability that allows Service Workers to keep JavaScript running in the background even after the browser window is closed, enabling remote code execution. Discovered by researcher Lyra Rebane and reported in December 2022, the bug was marked fixed in the issue tracker but never actually patched — Google's automated system publicly exposed the details on May 20 when access restrictions were lifted after the issue was closed for 14 weeks. Rebane confirmed the exploit still works on Chrome Dev 150 and Edge 148, and noted that the latest Edge version no longer shows a download popup when triggered, making the exploit completely silent. Potential abuse scenarios include DDoS botnets, traffic proxying, and arbitrary redirects — all from a single webpage visit. All Chromium-based browsers are affected (Chrome, Edge, Brave, Opera, Vivaldi, Arc). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/google-accidentally-exposed-details-of-unfixed-chromium-flaw/); [Ars Technica](https://arstechnica.com/) via BleepingComputer]

**[NEW] Foxconn Ransomware Attack — Nitrogen Gang Steals 8TB of Data Including NVIDIA/Apple IP**

Foxconn, one of the world's largest electronics manufacturers and key supplier to NVIDIA and Apple, suffered a ransomware attack at the hands of the Nitrogen group. The attackers exfiltrated approximately 8TB of data including over 10 million files containing confidential documents, engineering drawings, and client information. Nitrogen — a double-extortion ransomware group with ties to the ALPHV/BlackCat ecosystem — leaked verified screenshots of the stolen data on the dark web. Foxconn confirmed the attack briefly affected some North American facilities but stated operations have been restored. The stolen intellectual property poses risks for counterfeit production, AI model training, and state-sponsored espionage given Foxconn's defense industry supply chain involvement. [[Malware.News](https://malware.news/t/was-foxconn-hit-by-a-cyberattack/107224#post_1); [Panda Security Mediacenter](https://www.pandasecurity.com/mediacenter/) via Malware.News]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Kimwolf Botmaster "Dort" Arrested in Canada — 2M-Device DDoS Botnet Takedown**

Canadian authorities arrested 23-year-old Jacob Butler (online alias "Dort") in Ottawa on Wednesday, charging him with operating the KimWolf DDoS botnet that infected nearly two million IoT devices worldwide. Unsealed court documents reveal KimWolf operated as a DDoS-for-hire service launching attacks reaching nearly 30 Tbps — the largest publicly disclosed DDoS attack at its peak — and was used in over 25,000 attacks targeting computers worldwide, including DoD Information Network IP addresses. The botnet enslaved everything from digital photo frames to Android TV boxes. Separately, the Central District of California unsealed seizure warrants targeting 45 DDoS-for-hire platforms, disrupting multiple botnet services including one that collaborated with KimWolf. Butler faces up to 10 years in prison and awaits extradition to the U.S. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/us-and-canada-arrest-and-charge-suspected-kimwolf-botnet-admin/); [Krebs on Security](https://krebsonsecurity.com/2026/05/alleged-kimwolf-botmaster-dort-arrested-charged-in-u-s-and-canada/); [CyberScoop](https://cyberscoop.com/kimwolf-botnet-alleged-administrator-jacob-butler-arrested-canada/)]

**[NEW] Chinese Espionage Group Calypso Targets Telcos Across Asia-Pacific with Showboat/JFMBackdoor Malware**

A Chinese cyber-espionage campaign attributed to the Calypso/Red Lamassu group has been targeting telecommunications providers with two newly documented malware families — the Linux-based Showboat (aka kworker) and Windows-based JFMBackdoor — active since at least mid-2022. Researchers at Lumen's Black Lotus Labs and PwC Threat Intelligence detail Showboat as a modular post-exploitation framework acting as a SOCKS5 proxy and port-forwarding pivot point, enabling lateral movement across internal networks. It can conceal processes via code retrieved from Pastebin and online forums used as "dead drops." JFMBackdoor is a full-featured Windows espionage implant supporting reverse shell, file management, TCP proxying, registry manipulation, screenshot capture, and self-removal. Infrastructure analysis suggests shared tooling across multiple China-aligned groups operating decentralized clusters targeting distinct victim sets across Asia Pacific and the Middle East. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/chinese-hackers-target-telcos-with-new-linux-windows-malware/); [Lumen Black Lotus Labs](https://blog.lumen.com/) via BleepingComputer]

**[UPDATE] First VPN Takedown — European Authorities Seize 33 Servers Across 27 Countries, Arrest Administrator**

The coordinated international takedown of "First VPN" — a bulletproof VPN service deeply embedded in the ransomware ecosystem — involved French and Dutch authorities, Eurojust, and Europol seizing over 33 servers across 27 countries on May 19–20. Operation Saffron (Bitdefender's codename) also included a suspect interview in Ukraine. Critically, investigators obtained live traffic data from users who believed their activities were anonymous, yielding 83 intelligence packages covering 506 identified users — signaling a wave of follow-up prosecutions. The service appeared in nearly every major Europol cybercrime investigation. [[CyberScoop](https://cyberscoop.com/europol-take-down-first-vpn-cybercrime/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/police-seize-first-vpn-service-used-in-ransomware-data-theft-attacks/); [Malware.News](https://malware.news/t/operation-saffron-bitdefender-joins-first-vpn-takedown/107205#post_1)]

**[UPDATE] npm Resets All 2FA-Bypass Tokens — Emergency Response to Ongoing TeamPCP Supply Chain Campaign**

npm has invalidated all granular write-access tokens that bypass two-factor authentication in a platform-wide credential reset announced May 19, aimed at disrupting the ongoing Mini Shai-Hulud/TeamPCP campaign. Maintainers must generate new tokens and update CI environments. The emergency action follows the automated burst of 639 malicious package versions across 323 npm packages on May 18. The TeamPCP campaign has now claimed TanStack, Mistral AI, Guardrails AI, LiteLLM, @antv, Nx Console, Checkmarx, Trivy, and Microsoft DurableTask — making it the most prolific software supply chain campaign in recent memory. [[Cyber Security News](https://cyberpress.org/npm-resets-risky-tokens/); [GBHackers](https://gbhackers.com/mini-shai-hulud-attack-prompts-npm/); [Tenable Blog](https://www.tenable.com/blog/mini-shai-hulud-frequently-asked-questions)]

**[NEW] INJ3CTOR3's FreePBX JOMANGY Campaign — Six-Layer Self-Healing Persistence on VoIP Infrastructure**

Cyble Research & Intelligence Labs (CRIL) documented a campaign from INJ3CTOR3 deploying the previously unknown JOMANGY PHP webshell family against FreePBX VoIP infrastructure. The campaign exhibits a six-layer persistence architecture designed to self-heal within minutes from any single surviving channel — including recurring cron polling (every 1–3 minutes), shell profile stagers, and aggressive competitor eviction (scrubbing 50+ rival webshell signatures, blocking 11 rival C2 IPs). An inventory of 3,080 C2 IP addresses was observed, with ~39% on Alibaba Cloud infrastructure. The primary candidates for initial access are CVE-2025-64328 (post-auth command injection) and CVE-2025-57819 (pre-auth SQL injection). [[Cyber Security News](https://cyberpress.org/freepbx-hit-with-persistence/); [Malware.News](https://malware.news/t/jomangy-inj3ctor3-s-self-healing-freepbx-toll-fraud-campaign/107201#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] art-template npm Package Hijacked — iOS Safari Exploit Framework Delivered via Watering-Hole Supply Chain**

The widely used `art-template` npm package (transferred by original maintainer aui to an unknown actor) has been weaponized to deliver a Coruna-style iOS Safari exploit framework. Malicious versions 4.13.3, 4.13.5, and 4.13.6 load a heavily obfuscated JavaScript implant (`49554fde7424c31c.js`) that exclusively targets Safari/WebKit on iOS 11.0–17.2 and partially macOS Safari, hard-rejecting Chrome, Firefox, Edge, Android, and iOS 17.3+. The implant performs five anti-bot layers, probes WebKit memory layout for version-specific JIT exploitation, and fetches payload modules from SHA-256-addressed remote paths gated by a secret session key. Indicators: C2 at `l1ewsu3yjkqeroy[.]xyz`, loader at `utaq[.]cfww[.]shop`. [[Cyber Security News](https://cyberpress.org/art-template-package-compromised/); [Socket Research](https://socket.dev/) via Cyber Security News]

**[NEW] CISA Adds Trend Micro Apex One CVE-2026-34926 to KEV — Pre-Auth Directory Traversal Enables Agent-Level Code Injection**

CISA added CVE-2026-34926 (CVSS 6.7) to its KEV catalog, confirming active exploitation in enterprise environments. The directory traversal flaw (CWE-23) in Apex One on-premise allows a pre-authenticated attacker to modify a key table on the server and inject malicious code pushed to every managed endpoint — weaponizing the defender's own security infrastructure for lateral movement. Trend Micro's IR team discovered and reported the flaw. Fixed builds: CP 18012 (existing SP1) or Build 17079 (new installs). Earlier Build 17079 was temporarily withdrawn due to an unrelated issue but remains protective. [[CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog); [Cyber Security News](https://cyberpress.org/exploited-trend-micro-apex/); [GBHackers](https://gbhackers.com/cisa-warns-trend-micro-apex-one-vulnerability/)]

**[NEW] Cisco Secure Workload CVE-2026-20223 (CVSS 10.0) — Max Severity, No Workarounds**

Cisco patched a maximum-severity authentication bypass in Secure Workload's internal REST APIs that allows unauthenticated attackers to gain Site Admin privileges, granting sensitive data access and configuration changes across tenant boundaries. No workarounds exist. Fixed in versions 3.10.8.3 and 4.0.3.17. Separately, Cisco's Catalyst SD-WAN CVE-2026-20182 (also CVSS 10.0, disclosed earlier via Rapid7) remains under active exploitation — CISA added it to KEV on May 14. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisco-max-severity-secure-workload-flaw-gives-hackers-site-admin-privileges/); [SecurityWeek](https://www.securityweek.com/cisco-patches-critical-vulnerability-in-secure-workload/); [TLDR InfoSec](https://tldr.tech/infosec/2026-05-20)]

**[NEW] EU-Wide CRA (Cyber Resilience Act) Implementation Begins — New Security Requirements for Connected Products**

The EU Cyber Resilience Act is moving toward implementation, establishing mandatory cybersecurity requirements for products with digital elements sold in the EU market — covering hardware, software, and SaaS. The regulation requires manufacturers to provide security updates for the expected product lifetime, report actively exploited vulnerabilities to ENISA within 24 hours, and prohibit default passwords and known exploitable vulnerabilities. Products must carry CE marking with supporting cybersecurity documentation. Non-compliance carries fines up to €15M or 2.5% of global turnover. [[Malware.News](https://malware.news/t/cyber-resilience-act-cra-le-grand-basculement-industriel-de-la-cybersecurite-europeenne/107208#post_1)]

**[NEW] Drupal CVE-2026-9082 — Critical SQL Injection in PostgreSQL Configurations, PoC Published Same Day**

Drupal published a highly critical SQL injection vulnerability (CVE-2026-9082, rated 20/25 on Drupal's own scale) affecting sites running PostgreSQL. An unauthenticated attacker can exploit unsanitized PHP array keys reaching SQL placeholder construction in the PostgreSQL EntityQuery condition handler. A detection PoC was published the same day and the patch diff circulated within hours on social media. AI-assisted exploit development tools dramatically shorten the weaponization window. Drupal released fixes across all supported branches (11.x, 10.x) plus exceptional releases for EOL 11.1.x and 10.4.x. Sites on MySQL, MariaDB, or SQLite are not affected. [[Tenable Blog](https://www.tenable.com/blog/cve-2026-9082-highly-critical-sql-injection-vulnerability-in-drupal-core-sa-core-2026-004); [Drupal Security Advisory SA-CORE-2026-004](https://www.drupal.org/sa-core-2026-004)]

**[NEW] Apache HTTP Server 2.4.67 Fixes 11 Vulnerabilities Including HTTP/2 Double-Free RCE (CVE-2026-23918)**

Apache released version 2.4.67 addressing 11 security vulnerabilities. The most notable is CVE-2026-23918 (CVSS 8.8) — a double-free vulnerability in the HTTP/2 module allowing potential RCE triggered by early stream reset. Other fixes include CVE-2026-29168 (mod_md unrestricted OCSP response resource exhaustion), CVE-2026-28780 (heap buffer overflow in mod_proxy_ajp), and CVE-2026-24072 (mod_rewrite privilege escalation via ap_expr for .htaccess authors). [[Apache CHANGES_2.4.67](https://dlcdn.apache.org/httpd/CHANGES_2.4.67); [OpenCVE](https://app.opencve.io/cve/CVE-2026-23918)]

---

## 🛡️ Defense & Detection

**[NEW] Verizon DBIR 2026: Vulnerability Exploitation Overtakes Credential Theft as Top Breach Vector; Network Asset Attacks Up 3×**

The 2026 Verizon DBIR — analyzing 31,000+ incidents and 22,000+ confirmed breaches — reveals a fundamental shift: exploitation of vulnerabilities has overtaken credential abuse as the leading known initial access vector. Network asset breaches (VPNs, firewalls, routers) surged from 1.5% to 5% — a 3× increase — matching user-device targeting frequency. JPMorganChase CISO Pat Opet noted at RSAC 2026: "The very devices that are supposed to be our frontline defense are becoming our greatest weakness." The remediation gap is widening: only 26% of KEV vulnerabilities were fully remediated (down from 38%), median fix time rose to 43 days, and vulnerability instances grew from 68.7M (2022) to 527M (2025). [[Eclypsium](https://eclypsium.com/) via Malware.News; [Rapid7](https://www.rapid7.com/blog/post/tr-q1-2026-threat-landscape-report-geopolitics-ransomware)]

**[NEW] Microsoft Edge Will Stop Loading Saved Passwords in Cleartext Memory After Researcher Disclosure**

Security researcher Tom Jøran Sønstebyseter Rønning disclosed that Microsoft Edge decrypts ALL saved passwords into process memory at startup — regardless of whether the user visits the associated sites — where they remain in cleartext, accessible to any admin on a shared system via VDI/Citrix/terminal server. Unlike Chrome's App-Bound Encryption, Edge offered no such protection. Microsoft initially dismissed the finding as "an expected feature" but reversed course following public pressure, announcing that Edge build 148+ will no longer load passwords into memory on startup. [[DarkReading](https://www.darkreading.com/cyber-risk/microsoft-edge-passwords-enterprise-risk); [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-edge-to-stop-loading-cleartext-passwords-in-memory-on-startup/); [Microsoft Edge VR Blog](https://microsoftedge.github.io/edgevr/posts/Saved-passwords-in-Edge-memory-what-were-changing-and-why/)]

**[NEW] Kali365 PhaaS — FBI IC3 Warning: AI-Powered Phishing Kit Targets Microsoft 365 OAuth Tokens**

The FBI's IC3 issued an official warning about Kali365, a PhaaS kit first observed in April 2026 targeting Microsoft 365 OAuth tokens. Distributed via Telegram, Kali365 uses AI-generated phishing lures, automated campaign templates, and real-time tracking, exploiting the OAuth device-code flow to bypass MFA entirely. The FBI urges organizations to restrict the OAuth device code flow via Conditional Access policies. [[Cyber Security News](https://cyberpress.org/fbi-kali365-attacks-microsoft-365-users/); [GBHackers](https://gbhackers.com/fbi-warns-kali365-phaas-platform-targets-microsoft-365/)]

---

## ⚡ Quick Hits

- **Apache OFBiz CVE-2026-45434 (CVSS 9.8)** — Auth bypass via `requirePasswordChange` chains to `ProgramExport` for unauthenticated RCE. Ships with 10+ demo accounts using default password `ofbiz`. Fixed in 24.09.06. [[Cyber Security News](https://cyberpress.org/apache-ofbiz-flaw-exploited/)]
- **Splunk Patches CVE-2026-20238/39/40** — Low-privileged DoS, session cookie leakage, RBAC bypass. [[GBHackers](https://gbhackers.com/splunk-patches-multiple-vulnerabilities-enabling-dos-attacks/)]
- **npm Supply Chain via Hugging Face (DPRK-Linked)** — `terminal-logger-utils` uses Hugging Face for second-stage malware. Keylogging, clipboard polling, Telegram session theft. [[Cyber Security News](https://cyberpress.org/hugging-face-hosts-malware/)]
- **macOS Kernel Exploit via Mythos AI on Apple M5** — Researchers used Anthropic's Mythos AI to find a kernel memory corruption exploit on M5. [[Schneier on Security](https://www.schneier.com/blog/archives/2026/05/macos-kernel-memory-corruption-exploit.html)]
- **Trump Postpones AI Security Executive Order** — Citing competitiveness concerns, Trump delayed an EO requiring 90-day testing for frontier AI models. [[CyberScoop](https://cyberscoop.com/trump-postpones-executive-order-focused-on-ai-security/)]
- **Shadowbyt3$ Claims Starbucks Data Breach** — $500K demand; alleges access via exposed S3 bucket `starbucks-prod` since April 1. [[Malware.News](https://malware.news/t/shadowbyt3-targets-starbucks-company/107220#post_1)]
- **Hackers Hide Malware in Nested macOS-Style Folders** — Spear-phishing campaign uses ZIPs mimicking Chinese university notices to evade scanners. [[GBHackers](https://gbhackers.com/nested-macos-style-folders/)]
- **DeepLoad Malware — ClickFix Delivery** — Tricking users into executing PowerShell commands that deploy a password stealer. [[Malware.News](https://malware.news/t/deepload-malware-explained-clickfix-delivery-and-password-stealing/107223#post_1)]
- **Operation Dragon Whistle** — VS Code and Discord webhooks abused to target Pakistani government agencies. [[Cyber Security News](https://cyberpress.org/dragon-whistle-targets-university/)]
