---
title: Critical infrastructure exposure ⚠️, supply chain compromises 🔗, AiTM payroll fraud 💰, mobile espionage campaigns 📱
date: 2026-04-11
tags: ["critical infrastructure","apt activity","supply chain security","ransomware","edr killers","financial fraud","mobile spyware","zero-day exploitation","industrial control systems"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Iranian state-sponsored threat actors are actively exploiting nearly 4,000 exposed Rockwell PLCs across U.S. critical infrastructure, demonstrating the severe risk of operational technology exposure and the escalating geopolitical dimensions of ICS attacks. Meanwhile, supply chain compromises affecting CPUID's software distribution, widespread GitHub/GitLab abuse for malware delivery, and commercial EDR killers are enabling ransomware operators to disable endpoint defenses before encryption, while AiTM session hijacking campaigns target payroll systems and ProSpy spyware campaigns pivot to targeting journalists and civil society members across the Middle East.
---


# Daily Threat Intel Digest - 2026-04-11

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Iranian APTs Targeting US Critical Infrastructure — CISA Confirms Operational Disruptions, ~3,900 Rockwell PLCs Exposed**

Federal agencies have confirmed that Iranian state-backed threat actors are actively exploiting Rockwell Automation/Allen-Bradley programmable logic controllers (PLCs) across U.S. critical infrastructure, resulting in documented operational disruptions and financial losses. The joint advisory from CISA, FBI, and NSA reveals that actors have extracted device project files and manipulated HMI and SCADA displays. Censys Internet scanning identified 5,219 internet-exposed EtherNet/IP hosts globally, with 74.6% (3,891 hosts) located in the United States—predominantly on cellular carrier networks serving field-deployed industrial equipment. The targeting aligns with escalating geopolitical tensions, including the recent U.S.-Israel operations against Iranian assets and ongoing Strait of Hormuz disputes. CISA advises organizations to immediately audit PLC exposure, enforce MFA for OT network access, and review logs for suspicious traffic on industrial control ports. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/nearly-4-000-us-industrial-devices-exposed-to-iranian-cyberattacks/)] [[CyberPress](https://cyberpress.org/ransomware-groups-increasingly-turn-to-edr-killers/)] [[Malware.news](https://malware.news/t/iranian-apt-target-us-critical-infrastructure/105933#post_1)]

---

**[NEW] Adobe Reader Zero-Day Enables Silent RCE via Malicious PDFs**

A sophisticated zero-day vulnerability in Adobe Acrobat Reader allows remote code execution with zero user interaction—simply opening a malicious PDF is sufficient. Tracked by EXPMON researcher Haifei Li, the exploit has been active since November 28, 2025, targeting builds 2023.006.20320 and 26.00121367. The attack chain exploits /OpenAction triggers to automatically execute embedded JavaScript, which uses util.readFileIntoStream to fingerprint the victim's operating system by reading ntdll.dll and exfiltrates system data through RSS.addFeed API calls disguised as "Adobe Synchronizer" traffic. Russian-language lures referencing oil and gas industry events suggest state-aligned espionage motivations. The malware uses heavy obfuscation with base64-encoded payloads in PDF objects, and the attacker's C2 infrastructure includes 169.40.2.68:45191 and 188.214.34.20:34123. Defenders should monitor for HTTP/HTTPS traffic containing "Adobe Synchronizer" in the User-Agent header and deploy behavioral monitoring to detect privileged API abuse, as traditional signature-based AV exhibits low detection rates on VirusTotal. [[SocFortress Medium](https://socfortress.medium.com/the-pdf-you-just-opened-could-be-watching-you-inside-the-adobe-reader-zero-day-e2bd6897816b)]

---

**[NEW] CPUID Supply Chain Compromise Distributes Advanced Trojanized Loader via HWMonitor**

Attackers compromised CPUID's secondary API for approximately six hours between April 9–10, redirecting downloads for CPU-Z and HWMonitor to serve trojanized installers containing an advanced multi-stage loader. The malicious payload is flagged by 20+ antivirus engines and exhibits sophisticated TTPs: it's deeply trojanized, operates almost entirely in-memory, uses file masquerading, and proxies NTDLL functionality from a .NET assembly to evade EDR detection. Users downloading from the official portal received a trojanized HWiNFO variant wrapped in a suspicious Russian-language Inno Setup installer. vxunderground analysis confirms the same threat group previously targeted FileZilla FTP users last month, indicating a pattern of focusing on widely-used developer utilities. CPUID has since secured the breach and reports original binaries were not modified; however, any users who downloaded tools during the six-hour window should treat their systems as potentially compromised and conduct forensic analysis. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/supply-chain-attack-at-cpuid-pushes-malware-with-cpu-z-hwmonitor/)]

---

**[UPDATE] WordPress Ninja Forms Plugin RCE Under Active Exploitation — Patch Available**

A critical arbitrary file upload vulnerability in the Ninja Forms "File Upload" extension (CVE-2026-07409) is being actively exploited, with a public proof-of-concept now available. The flaw affects versions up to and including 3.3.26 and allows unauthenticated attackers to achieve remote code execution by uploading webshells. Truesec researchers confirm exploitation in the wild, and organizations should immediately update to version 3.3.27 or later. Sites unable to patch should deploy WAF rules to block malicious upload patterns and audit their environments for unauthorized files matching common webshell signatures. [[Truesec](https://www.truesec.com/hub/blog/critical-vulnerability-in-ninja-forms-file-upload-wordpress-plugin-cve-2026-07409)] [[Malware.news](https://malware.news/t/critical-vulnerability-in-ninja-forms-file-upload-wordpress-plugin-cve-2026-07409/105932#post_1)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Storm-2755 Conducts AiTM Payroll Hijacking Targeting Canadian Organizations**

Microsoft has tracked a threat actor, Storm-2755, using adversary-in-the-middle (AiTM) session hijacking to redirect employee payroll deposits to attacker-controlled accounts. By intercepting live Microsoft 365 sessions, the group bypasses MFA and blends fraudulent transactions into normal user activity. The campaign specifically targets Canadian organizations, representing a new financial fraud vector that complements traditional business email compromise. Security teams should audit Microsoft 365 sign-in logs for anomalous authentication patterns, enforce phishing-resistant MFA (FIDO2/hardware keys) for payroll administrators, and implement conditional access policies requiring device compliance for financial system access. [[GBHackers](https://gbhackers.com/storm-2755-uses-aitm/)]

---

**[NEW] Fake Claude Sites Distributing PlugX RAT via DLL Sideloading**

Malwarebytes researchers identified a convincing fake Claude website serving a trojanized "Claude-Pro-windows-x64.zip" installer that deploys PlugX malware, a remote access trojan with espionage capabilities dating to 2008. The attack chain uses DLL sideloading (MITRE T1574.002): a VBScript dropper launches a legitimately signed G DATA antivirus updater (NOVUpdate.exe) which loads a malicious avk.dll from its directory. The malware establishes C2 to 8.217.190.58 on port 443 within seconds of execution and persists via the Windows Startup folder. Attribution is complicated—PlugX has Chinese state-linked associations, but source code circulation in underground forums has broadened the operator pool. The campaign exploits Claude's surge to 290 million monthly visits, demonstrating how popular AI tools become attractive social engineering lures. Users should only download Claude from claude.com/download and scan their systems for NOVUpdate.exe, avk.dll, or the misspelled "Cluade" directory. [[Malwarebytes](https://www.malwarebytes.com/blog/scams/2026/04/fake-claude-site-installs-malware-that-gives-attackers-access-to-your-computer)]

---

**[NEW] ProSpy Spyware Campaign Targets Middle Eastern Journalists via Fake Messaging Apps**

Security researchers from Access Now and Lookout have documented ProSpy, a mobile espionage campaign targeting journalists, politicians, and civil society members across the Middle East. The operation uses fake profiles on LinkedIn and social engineering via fake Apple Support calls to trick victims into installing trojanized secure messaging applications. The attackers exploit Signal's QR code linking feature to secretly gain access to encrypted message archives. Attribution to BITTER APT (South Asia-based) was established through shared infrastructure with the "Dracarys" 2022 Android spyware campaign and identical task-handling code patterns. The targeting of civil society represents a significant operational pivot for BITTER, which traditionally focuses on government and energy sectors, suggesting a "hack-for-hire" engagement by an unknown third party. [[CyberPress](https://cyberpress.org/prospy-targets-messaging-users/)]

---

## ⚠️ Vulnerabilities & Patches

**[UPDATE] GitHub Copilot CamoLeak — Patch Now Available, Organizations Should Audit AI Tool Access**

The "CamoLeak" vulnerability (CVE-2025-59145, CVSS 9.6) in GitHub Copilot Chat has been patched after public disclosure revealed attackers could exfiltrate API keys and private source code via prompt injection. The technique exploited hidden markdown instructions in pull requests that Copilot would process, causing it to search accessible repositories for secrets and encode findings into image URLs routed through GitHub's trusted Camo proxy. This allowed data exfiltration while bypassing Content Security Policies. GitHub patched the flaw by disabling image rendering inside Copilot Chat in October 2025, but organizations using Copilot should audit integration permissions, restrict AI access to sensitive repositories, and monitor for unusual outbound connections from developer workstations. [[CyberPress](https://cyberpress.org/exploit-github-copilot-vulnerability/)] [[GBHackers](https://gbhackers.com/hackers-exploit-github-copilot-flaw/)]

---

**[NEW] HPE Aruba Private 5G Platform Open Redirect Enables Credential Theft**

CVE-2026-23818 in HPE Aruba Networking Private 5G Core On-Prem allows attackers to craft phishing URLs that redirect authenticated users to fake login pages during the authentication workflow. Exploitation requires social engineering—a target must click a malicious link—after which the open redirect silently routes them to an attacker-controlled server mimicking the legitimate GUI. The victim re-enters credentials, which are captured, before seamless redirection back to the real login page. HPE has released patches, and organizations should immediately update affected systems while implementing web security controls to detect suspicious redirects and monitoring authentication flows for anomalous patterns. [[CyberPress](https://cyberpress.org/hpe-aruba-private-5g-platform-vulnerability/)]

---

**[NEW] ClickFix Campaign Evolves to Target macOS via Script Editor**

The prolific ClickFix social engineering campaign, responsible for over half of all malware loader activity in 2025, has pivoted from Terminal-based infection to abusing macOS Script Editor. Instead of instructing victims to paste commands, the updated technique displays a "Reclaim Disk Space" lure that opens a pre-filled AppleScript via the applescript:// URL scheme. The script executes `curl -kSsfL | zsh` to download and run Atomic Stealer (AMOS), a macOS infostealer targeting browser credentials and cryptocurrency wallets. The technique relies on Script Editor appearing as a trusted "Apple-prepared" tool, increasing victim compliance. macOS Tahoe (26.4+) includes protections against these script-based attacks, but older systems remain vulnerable. Users should never execute scripts from untrusted webpages and should verify any technical instructions through official support channels before proceeding. [[Malwarebytes](https://www.malwarebytes.com/blog/news/2026/04/clickfix-finds-new-way-to-infect-macs)]

---

**[NEW] GitHub and GitLab Infrastructure Abused for Malware Delivery — 30+ Families Observed**

Cofense research reveals extensive abuse of GitHub and GitLab platforms for malware distribution, leveraging the trust these platforms command to bypass secure email gateways. GitHub-hosted campaigns favor raw githubusercontent.com URLs for silent background payload downloads, with Remcos RAT accounting for 21% of observed volume. GitLab abuse peaks at 64% of campaigns focused exclusively on malware delivery, including Byakugan, Async RAT, and DcRAT. Sophisticated actors now combine malware delivery with credential phishing in hybrid attacks—delivering infostealers followed by fake document pop-ups prompting victims to enter corporate credentials. GitLab additionally employs device fingerprinting: Windows victims receive remote administration tool payloads while Mac/Android users encounter credential phishing portals. Platform moderation delays enable weeks of active campaigns before malicious repositories are purged. [[CyberPress](https://cyberpress.org/github-gitlab-fuel-attacks/)]

---

## 🛡️ Defense & Detection

**[NEW] Google Deploys Memory-Safe Rust DNS Parser in Pixel Baseband Firmware**

Google's Pixel team has successfully integrated a memory-safe Rust-based DNS parser into the Pixel 10 modem firmware, representing a milestone in hardening cellular baseband against memory corruption vulnerabilities. The project uses the Hickory DNS crate with custom no_std support, replacing complex C/C++ DNS parsing code with a Rust implementation that eliminates entire vulnerability classes. The 371KB addition enables parsing of DNS responses in the trusted computing base while reducing attack surface. This follows Project Zero's remote code execution achievement against Pixel modems via internet-packet-based attacks, demonstrating the ongoing arms race between modem complexity and security hardening. The work establishes infrastructure for broader Rust adoption in embedded cellular environments. [[Google Security Blog](http://security.googleblog.com/2026/04/bringing-rust-to-pixel-baseband.html)]

---

**[NEW] Chrome 147 Security Update Addresses Multiple Vulnerabilities**

Google has released Chrome 147.0.7727.55/56 for Windows and Mac (147.0.7727.55 for Linux) addressing multiple security vulnerabilities. The Canadian Centre for Cyber Security issued advisory AV26-337 urging immediate updates, particularly for organizations running Chrome in enterprise environments where browser compromises often lead to credential theft and network pivots. IT administrators should verify deployment of version 147 across managed endpoints. [[Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/google-chrome-security-advisory-av26-337)] [[Malware.news](https://malware.news/t/google-chrome-security-advisory-av26-337/105931#post_1)]

---

**[NEW] ESET Research Documents EDR Killer Ecosystem — 90 Tools, 35 Vulnerable Drivers**

ESET Research has published comprehensive analysis of the EDR killer landscape, documenting nearly 90 distinct tools actively deployed by ransomware operations to disable endpoint detection before encryption. While BYOVD (Bring Your Own Vulnerable Driver) remains dominant with 54 tools exploiting 35 vulnerable drivers, researchers identified a growing class of driverless EDR killers—EDRSilencer and EDR-Freeze—which block network communications or freeze processes without kernel interaction. Commercial "EDR killer as a service" offerings including DemoKiller, AbyssKiller, and CardSpaceKiller are actively sold to affiliates of Qilin, Medusa, and Akira ransomware groups. ESET emphasizes that driver-centric threat attribution is unreliable, as independent affiliates rather than core operators typically select and deploy these tools. Defenders should deploy application control to block known vulnerable drivers and unauthorized anti-rootkit utilities like GMER and PC Hunter. [[CyberPress](https://cyberpress.org/ransomware-groups-increasingly-turn-to-edr-killers/)]