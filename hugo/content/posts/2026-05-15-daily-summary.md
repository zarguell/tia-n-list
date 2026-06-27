---
title: "🔥 Cisco SD-WAN 6th Zero-Day, 📦 TeamPCP Supply Chain Wave, 🐧 Fragnesia Linux LPE, 🤖 Kazuar Turla Botnet, 🏭 Foxconn Nitrogen Ransomware"
date: 2026-05-15
tags: ["Cisco","SD-WAN","CVE-2026-20182","TeamPCP","supply-chain","Shai-Hulud","node-ipc","OpenAI","Linux","Fragnesia","CVE-2026-46300","Turla","Kazuar","Secret-Blizzard","Sandworm","FamousSparrow","Exim","CVE-2026-45185","Pwn2Own","Foxconn","Nitrogen","CloudZ-RAT","OrBit-rootkit","npm","RubyGems"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Cisco SD-WAN faces its 6th exploited zero-day of 2026 with CISA Emergency Directive. TeamPCP's supply chain campaign widens to include OpenAI and node-ipc. Fragnesia becomes the third Linux kernel LPE in two weeks. Microsoft reveals Turla's Kazuar evolving into a modular P2P botnet."
---

# Daily Threat Intelligence Digest — May 15, 2026

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Cisco SD-WAN Zero-Day CVE-2026-20182 — 6th Exploited Flaw in 2026, CISA Emergency Directive Issued**

Cisco disclosed CVE-2026-20182 (CVSS 10.0), a critical authentication bypass in Catalyst SD-WAN Controller and Manager confirmed under active zero-day exploitation. The flaw allows unauthenticated remote attackers to gain administrative privileges by exploiting a broken peering authentication mechanism, granting access to NETCONF and the ability to manipulate network configuration across the entire SD-WAN fabric. CISA added the CVE to its Known Exploited Vulnerabilities catalog with a **May 17 remediation deadline** and issued Emergency Directive 26-03 with hunt and hardening guidance.

The sophisticated threat actor tracked as **UAT-8616** has exploited Cisco SD-WAN vulnerabilities since at least 2023. Post-compromise activity includes SSH key injection, NETCONF configuration manipulation, malicious account creation, software version downgrades to expose CVE-2022-20775 for root escalation, and extensive log clearing. Beyond UAT-8616, Cisco Talos has identified **10 additional threat clusters** exploiting the CVE-2026-20133/20128/20122 chain since public PoC code was published in March 2026. Tools deployed range from webshells and red team frameworks to cryptocurrency miners and credential stealers targeting AWS credentials and JWT tokens. All five CVEs in this campaign are now in CISA's KEV catalog. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisco-warns-of-new-critical-sd-wan-flaw-exploited-in-zero-day-attacks/); [Tenable FAQ](https://www.tenable.com/blog/faq-about-the-continued-exploitation-of-cisco-sd-wan-vulnerabilities-uat-8616); [SecurityWeek](https://www.securityweek.com/cisco-patches-another-sd-wan-zero-day-the-sixth-exploited-in-2026/)]

**[UPDATE] TeamPCP Supply Chain Assault Widens — OpenAI Breach Confirmed, node-ipc Compromised, BreachForums Contest Launched**

TeamPCP's Mini Shai-Hulud supply chain campaign continues expanding. OpenAI confirmed two employees' devices were breached through compromised TanStack packages, forcing rotation of code-signing certificates across macOS, Windows, iOS, and Android. macOS users must update OpenAI desktop apps before June 12. TeamPCP is also advertising nearly 450 Mistral AI repositories for $25,000 on hacker forums. Separately, the node-ipc npm package (822K weekly downloads) was compromised through a hijacked dormant maintainer account, with versions 9.1.6, 9.2.3, and 12.0.1 packing credential-stealing malware that exfiltrates AWS, Azure, GCP, and SSH keys via covert DNS TXT queries.

TeamPCP and BreachForums have launched a **$1,000 gamified contest** rewarding participants for using the open-source Shai-Hulud tool to compromise open-source packages, with scoring based on download counts of trojanized packages. The contest spans npm, PyPI, GitHub Actions, Docker, and OpenVSX. Meanwhile, RubyGems.org suspended new account registrations after bot accounts pushed 500+ malicious packages in a parallel supply chain attack. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/openai-confirms-security-breach-in-tanstack-supply-chain-attack/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/teampcp-hackers-advertise-mistral-ai-code-repos-for-sale/); [CyberSecurityNews](https://cyberpress.org/822k-download-node-ipc-breach/); [CyberSecurityNews](https://cyberpress.org/teampcp-breachforums-supply-chain-attacks/); [SecurityWeek](https://www.securityweek.com/hundreds-of-malicious-packages-force-rubygems-to-suspend-registrations/) (TLDR InfoSec)]

**[UPDATE] Fragnesia CVE-2026-46300 — Third Linux Kernel LPE in Two Weeks, Patches Available**

Fragnesia, a local privilege escalation vulnerability in the Linux kernel's XFRM ESP-in-TCP subsystem, allows unprivileged local users to gain root by writing arbitrary bytes into page cache of read-only files. A public PoC confirmed working on Ubuntu modifies `/usr/bin/su` in the page cache without changing the on-disk binary. CVE-2026-46300 follows Dirty Frag and Copy Fail as the third high-severity LPE targeting the same subsystem in two weeks. Kernel patches were released May 13; AlmaLinux and Fedora are patched, while Ubuntu, Debian, RHEL, and openSUSE remain vulnerable. The module blacklist mitigation (`rmmod esp4 esp6 rxrpc`) that protects against Dirty Frag also protects against Fragnesia — organizations that applied only kernel patches without the blacklist are not protected. [[Tenable FAQ](https://www.tenable.com/blog/fragnesia-cve-2026-46300-faq-about-new-linux-kernel-xfrm-esp-in-tcp-priv-esc); [SOC Prime](https://socprime.com/blog/cve-2026-46300-fragnesia-linux-kernel-flaw/); [SecurityWeek](https://www.securityweek.com/new-linux-kernel-vulnerability-fragnesia-allows-root-privilege-escalation/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Kazuar — Secret Blizzard (Turla) Evolves Into Modular P2P Botnet**

Microsoft published a comprehensive analysis of Kazuar, a sophisticated malware family attributed to Russia's FSB Center 16 (Secret Blizzard / Turla / Venomous Bear). Originally identified as a traditional backdoor, Kazuar has evolved into a highly modular P2P botnet ecosystem with three distinct module types: Kernel (central coordinator), Bridge (external communications proxy), and Worker (data collection and task execution). A single elected Kernel leader communicates externally on behalf of all other nodes, drastically reducing observable network traffic. The malware features 150+ configurable options across 8 categories, supports HTTP, WebSocket, and Exchange Web Services C2 channels, and uses Google Protocol Buffers for inter-module messaging. Kazuar targets government and diplomatic organizations across Europe, Central Asia, and Ukraine for long-term intelligence collection. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/14/kazuar-anatomy-of-a-nation-state-botnet/)]

**[NEW] FrostyNeighbor (UNC1151) Deploys Cobalt Strike via Scheduled Tasks Persistence**

The Belarusian-aligned threat group FrostyNeighbor (also tracked as Ghostwriter and Storm-0257) is using a new attack chain that combines spear-phishing PDFs impersonating Ukrainian telecom Ukrtelecom with Windows scheduled tasks for stealthy persistence. The campaign, discovered in March 2026, delivers a JavaScript version of PicassoLoader through geographic IP filtering — only victims in Ukraine receive the malicious payload. Operators manually review victim telemetry before deploying Cobalt Strike beacons. The group has been active since 2016 and previously exploited CVE-2023-38831 (WinRAR) and Roundcube XSS flaws. [[CyberSecurityNews](https://cyberpress.org/scheduled-tasks-enable-persistence/)]

**[NEW] Sandworm Actively Pivoting from IT to Critical OT Targets**

Nozomi Networks telemetry from 10 industrial organizations across 7 countries (July 2025–January 2026) reveals Sandworm (APT44) is systematically expanding from IT networks into operational technology environments, targeting engineering workstations, HMIs, PLCs, and RTUs. Rather than developing new tools, Sandworm exploits known vulnerabilities including EternalBlue, DoublePulsar, and WannaCry — relying on unpatched systems. Compromised machines showed an average of 43 days of detectable warning signs before escalation. In one case, a single infected system attempted lateral movement against 405 internal machines. Unlike ransomware groups that retreat when discovered, Sandworm **intensifies operations** when detected. [[GBHackers](https://gbhackers.com/sandworm-shift-from-it-breaches/)]

**[NEW] FamousSparrow (Chinese APT) Exploits Exchange to Breach Energy Sector**

Bitdefender uncovered a multi-wave intrusion by Chinese state-aligned APT FamousSparrow (overlapping with Earth Estries and Salt Typhoon) against an Azerbaijani oil and gas company between December 2025 and February 2026. The attackers exploited ProxyNotShell against Microsoft Exchange, repeatedly returning to the same entry point even after partial cleanup. The group deployed Deed RAT through a DLL sideloading chain abusing LogMeIn Hamachi, and later attempted to install the Terndoor backdoor via a kernel-mode driver rootkit. C2 domains impersonated security vendors including `sentinelonepro[.]com`. The targeting of Azerbaijan's energy sector is strategically significant given Europe's increased reliance on Azerbaijani gas since Russia's Ukraine transit agreement ended. [[GBHackers](https://gbhackers.com/chinese-apt-exploits-microsoft-exchange/)]

**[UPDATE] KongTuke Shifts to Microsoft Teams for Corporate Breach Access**

Initial access broker KongTuke has added Microsoft Teams to its social engineering toolkit, achieving persistent network access in under five minutes. Attackers pose as IT help desk staff using Unicode whitespace tricks to impersonate legitimate display names, then convince victims to paste a PowerShell command delivering ModeloRAT. The RAT variant observed in this campaign features a resilient 5-server C2 pool with automatic failover, multiple independent access paths (primary RAT, reverse shell, TCP backdoor), and expanded persistence using SYSTEM-level scheduled tasks that survive standard cleanup and reboots. The campaign has been active since April 2026, rotating through five M365 tenants. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/kongtuke-hackers-now-use-microsoft-teams-for-corporate-breaches/)]

**[NEW] CloudZ RAT + Pheno Plugin Steals OTPs via Windows Phone Link Abuse**

Cisco Talos documented a novel technique where the CloudZ RAT's Pheno plugin hijacks Microsoft Phone Link's local SQLite database to intercept SMS messages and OTP codes **without deploying any malware on the phone itself**. Active since January 2026, the campaign enters through fake ScreenConnect updates, delivers a Rust dropper and .NET loader, then establishes persistence via a SYSTEM-level scheduled task using `regasm.exe` as a LOLBin. The .NET loader includes timing checks, virtual machine detection, and hardware enumeration to evade analysis. [[Cisco Talos](https://blog.talosintelligence.com/cloudz-pheno-infostealer/) (TLDR InfoSec)]

## ⚠️ Vulnerabilities & Patches

**[NEW] node-ipc npm Supply Chain Attack — 822K Weekly Downloads Compromised**

The node-ipc package (822K weekly downloads) was weaponized through a hijacked dormant npm maintainer account. Malicious versions 9.1.6, 9.2.3, and 12.0.1 embed credential-stealing malware directly in the CommonJS entry point, targeting AWS, Azure, GCP, SSH keys, Kubernetes configs, and .env files. Exfiltration uses covert DNS TXT queries to attacker-controlled domains mimicking Azure infrastructure, splitting data into small chunks to evade detection. The ESM import path remains clean. Organizations should audit recent installations and rotate all exposed credentials. [[CyberSecurityNews](https://cyberpress.org/822k-download-node-ipc-breach/)]

**[UPDATE] Exim Dead.Letter CVE-2026-45185 — Unauthenticated RCE, Detailed Exploitation Available**

New analysis confirms CVE-2026-45185 ("Dead.Letter"), a use-after-free in Exim versions 4.97–4.99.2 compiled with GnuTLS, can be reliably escalated from a one-byte heap write to full remote code execution. The flaw triggers when a malicious client sends a TLS `close_notify` during an active BDAT session, causing Exim to free a buffer while stale callback pointers remain active. Exploitation requires no authentication and no special configuration beyond the vulnerable GnuTLS + BDAT combination. OpenSSL-based builds are not affected. Exim 4.99.3 patches the issue. Researchers note LLM-assisted exploit generation is accelerating the disclosure-to-weaponization timeline. [[CyberSecurityNews](https://cyberpress.org/new-exim-vulnerability/)]

**[UPDATE] Langflow CVE-2026-33017 Exploited Within 20 Hours of CISA KEV Listing**

Sysdig's Threat Research Team documented an attacker exploiting the Langflow RCE vulnerability within 20 hours of its addition to the CISA KEV catalog. The operator built a custom "KeyHunter" tool that scrapes credentials from online code sandboxes (CodePen, JSFiddle, StackBlitz, CodeSandbox) using browser fingerprint mimicry to bypass bot detection. The campaign used NATS as a C2 channel and treated compromised VPS infrastructure as disposable, deploying on cost-effective ARM instances with minimal operational security. [[CyberSecurityNews](https://cyberpress.org/langflow-attacks-target-aws/)]

## 🛡️ Defense & Detection

**[NEW] OrBit Linux Rootkit — 4-Year Tracking Reveals Open-Source Origin, Multiple Operators**

An Intezer analysis tracking OrBit from 2022 through 2026 reveals the rootkit is a repackaged build of Medusa, an open-source LD_PRELOAD rootkit published on GitHub in December 2022. Two parallel lineages exist: a full-featured "Lineage A" and a lite "Lineage B" (retired after 2024). The codebase has been deployed by at least three unrelated operators: UNC3886 (state-sponsored espionage, Mandiant), BLOCKADE SPIDER (Embargo ransomware, CrowdStrike), and a 2025 campaign linked to RHOMBUS botnet infrastructure. A 2025 infector variant introduced the first C2 communication channel to the previously passive SSH-backdoor-only implant. Detection can leverage YARA rules targeting the Medusa build pipeline's XOR-obfuscated string table and the nested-ELF loader structure. [[Intezer via Malware.News](https://malware.news/t/orbit-re-turns-tracking-an-open-source-linux-rootkit-across-four-years-of-forks-and-deployments/106998#post_1)]

**[NEW] TencShell — Go-Based Implant with Browser Artifact Access and Screen Control**

Cato CTRL documented a new threat targeting a global manufacturing enterprise through a compromised third-party in India. TencShell is a customized Go-based implant derived from the open-source Rshell C2 framework, featuring remote screen streaming, mouse/keyboard simulation, Chrome and Edge session data manipulation, UAC bypass, SOCKS5 proxy capabilities, and inline binary execution. The first-stage dropper retrieves Donut shellcode disguised as a `.woff` web font file and establishes persistence via a Run key entry named "OneDriveHealthTask." Infrastructure patterns suggest Chinese threat actor affiliation, with C2 domains impersonating Tencent API services. [[CyberSecurityNews](https://cyberpress.org/malware-gains-browser-access/)]

## 📋 Policy & Industry News

**[UPDATE] Foxconn Cyberattack — Nitrogen Ransomware Confirmed, Factories Resuming**

Foxconn confirmed a cyberattack disrupted North American factories in Mexico, Wisconsin, Ohio, Texas, Virginia, and Indiana. Nitrogen ransomware claimed responsibility, alleging theft of 8TB spanning 11M+ files including confidential data from Apple, Intel, Google, Dell, and NVIDIA. Foxconn stated affected factories are resuming normal production as of May 13. Security researchers note Nitrogen's recent leak site claims lack working file listings and include mostly older images, raising questions about inflated data-theft claims. Nitrogen previously used ALPHV and Conti code to build custom tools targeting Windows and VMware environments. [[CyberScoop](https://cyberscoop.com/foxconn-cyberattack-disrupts-north-america-factories/)]

**[NEW] Pwn2Own Berlin 2026 Day 1 — $523,000 Awarded, 24 Zero-Days Exploited**

Day 1 of Pwn2Own Berlin 2026 at OffensiveCon saw researchers demonstrate 24 unique zero-days earning $523,000 in bounties. Highlights include Orange Tsai's $175,000 Edge sandbox escape chaining 4 logic bugs, three separate Windows 11 privilege escalations ($30,000 each), k3vg3n's LiteLLM exploit chain ($40,000), and successful attacks against OpenAI Codex ($40,000), NVIDIA Container Toolkit ($50,000), LM Studio ($40,000), and Chroma ($20,000). DEVCORE Research Team leads with $205,000. Day 2 targets include SharePoint, Exchange, Safari, Cursor, Anthropic Claude Code, and Firefox. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/windows-11-and-microsoft-edge-hacked-on-first-day-of-pwn2own-berlin-2026/)]

## ⚡ Quick Hits

- **Akamai acquires LayerX** for $205M to expand AI and browser security capabilities [[SecurityWeek](https://www.securityweek.com/akamai-to-acquire-ai-and-browser-security-firm-layerx-for-205-million/)]
- **Pentagon cyber official** calls advanced AI "revolutionary warfare" at Rubrik Federal Cyber Resilience Breakfast [[CyberScoop](https://cyberscoop.com/pentagon-cyber-ai-revolutionary-warfare-mythos/)]
- **First public macOS kernel memory corruption exploit** demonstrated on Apple M5 chips [[Malware.News](https://malware.news/t/first-public-macos-kernel-memory-corruption-exploit-on-apple-m5/107008#post_1)]
- **Dell SupportAssist v5.5.16.0** causing widespread BSOD loops on Dell and Alienware devices worldwide [[CyberSecurityNews](https://cyberpress.org/dell-support-windows-bsod-loop/)]
- **NIST NVD changes enrichment model** — will only prioritize CISA KEV and critical software as CVE submissions surge 263% since 2020 [[Reddit r/cybersecurity](https://www.nist.gov/news-events/news/2026/04/nist-updates-nvd-operations-address-record-cve-growth) (TLDR InfoSec, 472↑)]
- **Chrome 148** patches 79 security vulnerabilities, 14 rated critical [[BleepingComputer](https://www.bleepingcomputer.com/news/security/18-year-old-nginx-vulnerability-allows-dos-potential-rce/)]
- **Next.js flaw** CVE-2026-44578 leaks cloud credentials, API keys, and admin interfaces [[GBHackers](https://gbhackers.com/next-js-security-flaw-leaks-cloud-credentials/)]
- **West Pharmaceutical Services** confirms material cyberattack with data exfiltration and encryption, global operations disrupted [[TLDR InfoSec]]
