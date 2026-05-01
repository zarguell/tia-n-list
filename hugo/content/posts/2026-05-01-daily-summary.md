---
title: "🚨 cPanel Zero-Day Active Exploitation, 🪵 Copy Fail Linux Root, 🔗 Mini Shai-Hulud Supply Chain"
date: 2026-05-01
tags: ["cPanel","CVE-2026-41940","Linux","CVE-2026-31431","supply-chain","TeamPCP","Shai-Hulud","SAP","APT","Gemini-CLI","Wireshark","Exim","SonicWall","Scattered-Spider","Deep#Door","Unit42","AI-malware","BlackCat","ransomware","FBI"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA has added the cPanel authentication bypass (CVE-2026-41940) to its KEV list as active exploitation and a public PoC accelerate the threat to ~1.5M exposed instances. A new Linux kernel flaw (Copy Fail, CVE-2026-31431) grants reliable root access on every distro since 2017. The TeamPCP supply chain campaign has expanded to SAP npm packages with 1,800 confirmed victims."
---

# Tia N. List — Daily Threat Intelligence Digest
### May 1, 2026

**122 articles ingested from 27 feeds across the past 24 hours.**

*Previous 5 days reporting summary:* Yesterday's digest covered the breaking disclosure of cPanel CVE-2026-41940, SonicWall emergency firewall patches, the EnOcean SmartServer building automation flaws, and the Copy Fail Linux kernel vulnerability (then in embargo). Earlier this week, the Shai-Hulud self-replicating worm was reported targeting Bitwarden and other npm packages.

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] cPanel Authentication Bypass Now on CISA KEV — PoC Published, Exploitation Since February**

CISA added CVE-2026-41940 to its Known Exploited Vulnerabilities catalog on April 30, as a public proof-of-concept exploit from watchTowr confirms the flaw is trivially exploitable. The vulnerability is a CRLF injection in cPanel's login session handling that allows attackers to bypass password authentication entirely by injecting line breaks into the Authorization header. Successful exploitation grants full control over the cPanel host, its configurations, databases, and all hosted websites. watchTowr also released a Detection Artifact Generator to verify whether instances remain vulnerable. KnownHost, a major hosting provider, confirmed exploitation attempts as early as February 23, 2026 — nearly two months before cPanel released patches on April 28. Namecheap temporarily blocked cPanel ports 2083 and 2087 ahead of the fix. Rapid7's Shodan scans show approximately 1.5 million cPanel instances exposed online. Patched versions span seven release branches (11.110.0 through 11.136.0) plus WP Squared 11.136.1. Organizations that cannot patch immediately should block external access to ports 2083, 2087, 2095, and 2096, and run cPanel's detection script to check for indicators of compromise. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/critical-cpanel-and-whm-bug-exploited-as-a-zero-day-poc-now-available/); [CyberScoop](https://cyberscoop.com/cpanel-authentication-bypass-vulnerability-cve-2026-41940-exploited/)]

**[UPDATE] Copy Fail Linux Kernel Flaw (CVE-2026-31431) — Public PoC Gives Reliable Root on Every Distro Since 2017**

The Copy Fail vulnerability we flagged yesterday as breaking embargo has now been publicly disclosed with a proof-of-concept exploit. The 732-byte Python script reliably achieves root on every major Linux distribution shipped since 2017 by exploiting a logic bug in the `authencesn` cryptographic template. By combining the AF_ALG socket interface with the `splice()` system call, an unprivileged local attacker can perform a 4-byte controlled write into the page cache of any readable file — including setuid-root binaries. Theori, which discovered the flaw using its AI-driven Xint Code platform, confirmed the exploit works on Ubuntu 24.04 LTS, Amazon Linux 2023, RHEL 10.1, and SUSE 16. The fix was applied upstream on April 1 by reverting the "in-place" crypto optimization introduced in kernel 4.14 (2017). The researchers characterize it as more practical than Dirty Pipe: "One script, every distro, no offsets." Multi-tenant Linux hosts, Kubernetes/container clusters, CI runners, and cloud SaaS platforms running user code should prioritize patching immediately. As an interim mitigation, disable the `algif_aead` module: `echo "install algif_aead /bin/false" > /etc/modprobe.d/disable-algif.conf`. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-linux-copy-fail-flaw-gives-hackers-root-on-major-distros/)]

**[NEW] Mini Shai-Hulud Supply Chain Attack Hits SAP, Lightning, and Intercom — 1,800 Victims Confirmed**

The TeamPCP-linked supply chain campaign has expanded dramatically, compromising four SAP Cloud Application Programming Model (CAP) npm packages with 2.2 million combined monthly downloads: `@cap-js/db-service`, `@cap-js/sqlite`, `@cap-js/postgres`, and `mbt`. The malicious versions were live for 2–4 hours before being unpublished. The campaign, dubbed "Mini Shai-Hulud" via a hardcoded marker string, delivers a Bun-based credential stealer that harvests GitHub tokens, npm credentials, cloud secrets (AWS, Azure, GCP), Kubernetes tokens, and browser passwords. Stolen data is encrypted and exfiltrated via public GitHub repositories — over 1,200 victim repos have been identified so far. The malware also targets AI coding agents, injecting persistence hooks into `.claude/settings.json` and `.vscode/tasks.json`. A peer-to-peer dead-drop mechanism allows infected machines without usable credentials to borrow tokens from other compromised hosts. OX Security and Wiz have both confirmed TeamPCP attribution through a shared RSA public key. The campaign also compromised Salesforce Lightning SDK and Intercom's `intercom-client` npm package, with approximately 1,800 organizations confirmed affected. Organizations using SAP CAP, MTA build pipelines, or any of the affected packages should rotate all exposed credentials, check for public GitHub repos containing the string "A Mini Shai-Hulud has Appeared," and treat any affected machines as fully compromised. [[OX Security](https://www.ox.security/blog/shai-hulud-sap-supply-chain-attack-npm/); [Wiz](https://www.wiz.io/blog/mini-shai-hulud-supply-chain-sap-npm); [SecurityWeek](https://www.securityweek.com/sap-npm-packages-targeted-in-supply-chain-attack/); [Phoenix Security](https://phoenix.security/mini-shai-hulud-sap-cap-mbt-npm-supply-chain-bun-credential-stealer/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] China-Backed SHADOW-EARTH-053 Deploys ShadowPad in Multi-Stage Espionage Campaign**

A newly tracked China-aligned intrusion set, SHADOW-EARTH-053, has been targeting government and critical infrastructure networks across Asia since at least December 2024, with one NATO member also in scope. Trend Micro reports the group exploits older Microsoft Exchange and IIS vulnerabilities, including the ProxyLogon chain, to gain initial access. After establishing a foothold, the attackers deploy GODZILLA web shells for persistence and stage ShadowPad — a backdoor widely associated with Chinese state espionage — through DLL sideloading of legitimate signed executables. The group employs a layered toolkit including IOX proxy, GOST, Wstunnel, WMIC, and custom loaders for lateral movement, credential theft, and mailbox collection targeting high-value users. The campaign demonstrates how China-aligned actors continue to exploit N-day vulnerabilities in legacy Exchange servers that many organizations have patched in theory but not in practice. Organizations with exposed Exchange/IIS servers should prioritize patching, implement virtual patching via IPS/WAF, and monitor for IIS spawning command shells or unusual outbound traffic from web servers. [[Cyber Security News](https://cyberpress.org/shadowpad-spy-campaign/)]

**[NEW] Cordial Spider and Snarky Spider — The Next Generation of Scattered Spider**

CrowdStrike has identified two financially-motivated threat groups affiliated with "The Com" that are actively running Scattered Spider-style voice phishing and social engineering attacks against U.S. organizations across academic, aviation, retail, hospitality, financial services, legal, and technology sectors since at least October 2025. Cordial Spider and Snarky Spider use vishing, smishing, and phishing to capture credentials, session keys, or tokens from identity platforms, then traverse SaaS environments for data theft and extortion. Typical demands are in the seven-figure range. Cordial Spider operates a data-leak site called BlackFile (currently offline). Snarky Spider has escalated to swatting victim employees. Both groups use residential proxy networks (Mullvad, Oxylabs, NetNut, 9Proxy) to evade IP-based detection. While less technically sophisticated than Scattered Spider, they are described by CrowdStrike as the "new generation" — applying the same playbook with lower barriers to entry. [[CyberScoop](https://cyberscoop.com/crowdstrike-cordial-spider-snarky-spider-extortion-attacks/)]

**[NEW] Deep#Door — Sophisticated Python-Based Backdoor Combines Stealing with Destructive Capabilities**

Securonix has detailed a new campaign deploying Deep#Door, a multi-layered Windows backdoor that begins with an obfuscated batch file embedding its own Python payload — eliminating the need for separate payload downloads. Before activation, the malware disables Microsoft Defender, PowerShell logging, firewall logging, AMSI, and ETW. It employs VM, sandbox, and debugger detection to evade analysis. Persistence is established via the Startup folder, registry Run keys, scheduled tasks, and WMI subscriptions, with a watchdog routine that recreates deleted artifacts. Once active, Deep#Door functions as a full RAT: keylogging, clipboard monitoring, screenshot capture, webcam/microphone access, and remote command execution. Its credential theft targets Chrome/Firefox passwords, SSH private keys, Windows Credential Manager, and cloud tokens for AWS, Azure, and Google Cloud. Uniquely, it also carries destructive capabilities including MBR overwriting and forced system crashes. C2 communication uses the bore[.]pub tunneling service with dynamic port generation and challenge-response authentication. [[SecurityWeek](https://www.securityweek.com/sophisticated-deepdoor-backdoor-enables-espionage-disruption/); [Cyber Security News](https://cyberpress.org/deepdoor-stealer-campaign-spills/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Google Gemini CLI Remote Code Execution — CVSS 10.0**

Novee Security disclosed a maximum-severity RCE vulnerability in Google Gemini CLI that allows unauthenticated external attackers to execute arbitrary commands on host systems via CI/CD pipelines. The flaw (patched in `@google/gemini-cli` 0.39.1/0.40.0-preview.3 and `google-github-actions/run-gemini-cli` 0.1.22) exploits how Gemini CLI handles workspace trust in headless environments — it automatically loads configuration files from the working directory without validation. An attacker who submits a malicious pull request with crafted configuration files can trigger code execution on the CI/CD runner before any sandbox protections apply. The attack operates at the infrastructure level, bypassing AI safety mechanisms entirely. Successful exploitation exposes repository source code, build artifacts, workflow secrets, cloud service tokens, and lateral movement paths into production systems. [[Cyber Security News](https://cyberpress.org/google-gemini-cli-flaw-execute-commands/)]

**[NEW] Wireshark 4.6.5 Patches 40+ Vulnerabilities Including Critical RCE**

The Wireshark Foundation released version 4.6.5 addressing more than 40 security vulnerabilities, with four critical RCE flaws: CVE-2026-5402 (TLS dissector heap overflow), CVE-2026-5403 (SBC audio codec), CVE-2026-5405 (RDP dissector), and CVE-2026-5656 (profile import feature). Attackers can exploit these via maliciously crafted network packets on monitored networks or booby-trapped PCAP files distributed to analysts. No active exploitation has been confirmed, but the public disclosure of technical details significantly raises weaponization risk. SOC teams, threat hunters, and anyone analyzing untrusted network captures should upgrade immediately and avoid opening externally-sourced PCAP files without validation. [[Cyber Security News](https://cyberpress.org/multiple-wireshark-flaws/)]

**[NEW] Exim Mail Server 4.99.2 Fixes Four Memory Corruption Flaws**

Exim version 4.99.2 addresses CVE-2026-40684 (malicious DNS PTR record crash, primarily affecting musl libc), CVE-2026-40685 (corrupted JSON in email headers causing heap corruption), CVE-2026-40686 (large UTF-8 characters triggering out-of-bounds reads), and CVE-2026-40687 (SPA authentication driver out-of-bounds memory operations). Primary risk is denial-of-service through crafted emails or manipulated DNS responses, though memory corruption and data leakage are also possible. Administrators of internet-facing Exim servers should upgrade immediately — older versions are no longer maintained. [[Cyber Security News](https://cyberpress.org/multiple-exim-mail-server-flaws-allow-crashes-via-malicious-dns-data/)]

**[UPDATE] SonicWall Firewall Emergency Patches — CVE-2026-0204 Access Control Bypass**

Following yesterday's alert, SonicWall has released firmware updates addressing three vulnerabilities across Gen 6, 7, and 8 firewalls. CVE-2026-0204 (high severity) allows attackers who can reach the management interface to bypass access controls and potentially modify firewall configurations or disable security protections. Two medium-severity flaws (CVE-2026-0205 path traversal, CVE-2026-0206 DoS) require authentication. As an interim mitigation, SonicWall recommends restricting management access to SSH only by disabling HTTP/HTTPS-based management and SSLVPN on all interfaces. No in-the-wild exploitation has been reported. [[SecurityWeek](https://www.securityweek.com/sonicwall-urges-immediate-patching-of-firewall-vulnerabilities/)]

---

## 🛡️ Defense & Detection

**[NEW] Unit 42 Exposes 18 Malicious AI Browser Extensions — RATs, Stealers, and Spyware**

Palo Alto Networks' Unit 42 identified 18 high-risk Chrome extensions masquerading as AI productivity tools, delivering a range of malware including remote access Trojans, infostealers, search hijackers, brand impersonators, and spyware. Notable findings include: an MCP-themed RAT ("Chrome MCP Server") with over 30 remote commands and persistent WebSocket C2; an email surveillance extension ("Supersonic AI") that exfiltrates Gmail content including OTPs in plaintext; a job application assistant ("Reverse Recruiting") that steals OpenAI, Gemini, and Claude API keys; and a Chinese translation extension that deploys remote proxy PAC scripts to route all user traffic through attacker infrastructure. Multiple extensions contained AI-generated code fingerprints, indicating threat actors are using LLMs to accelerate malware production. All 18 extensions were reported to Google and either removed or warned. Organizations should audit installed browser extensions against the published extension IDs and treat browser add-ons with the same vetting rigor as any third-party application. [[Unit 42](https://unit42.paloaltonetworks.com/high-risk-gen-ai-browser-extensions/)]

**[NEW] Hugging Face and ClawHub Abused for Malware Distribution**

Acronis reports that AI platform ecosystems are increasingly being poisoned for malware delivery. On ClawHub, approximately 600 malicious "skills" were discovered across 13 developer accounts, distributing trojans, cryptominers, and the Atomic macOS Stealer (AMOS) through indirect prompt injection. On Hugging Face, at least two campaigns have been identified hosting malicious files in repositories, delivering infostealers, trojans, and loaders targeting Windows, Linux, macOS, and Android. The trend represents a migration from traditional delivery vectors (malvertising) to supply chain poisoning of trusted AI platforms exploiting rapid ecosystem growth and inherent user trust. [[SecurityWeek](https://www.securityweek.com/hugging-face-clawhub-abused-for-malware-distribution/)]

**[NEW] Supply Chain Attack Targets GitHub Actions via Malicious Ruby Gems and Go Modules**

A campaign linked to a GitHub account named "BufferZoneCorp" has been distributing malicious Ruby gems (using trusted prefixes like "knot-") and Go modules designed to compromise developer machines and CI/CD pipelines. Malicious Ruby gems exploit the native extension build process to silently execute code during installation, scanning for SSH keys, AWS credentials, and GitHub CLI configurations. The Go component is more advanced: it manipulates CI workflow environment variables, disables checksum verification, inserts fake execution wrappers to intercept commands, and in some cases appends hardcoded SSH public keys to `authorized_keys` for persistent access. Organizations should audit dependencies for BufferZoneCorp-linked packages, rotate exposed credentials, and review CI/CD workflows for unauthorized changes. [[Cyber Security News](https://cyberpress.org/supply-chain-attack-targets-github/)]

---

## 📋 Policy & Industry News

**[NEW] Former Cybersecurity Professionals Sentenced to 4 Years for BlackCat Ransomware Attacks**

Ryan Goldberg (40, Georgia) and Kevin Martin (36, Texas) were each sentenced to four years in federal prison on April 30 for deploying ALPHV/BlackCat ransomware against multiple U.S. victims in 2023. Both men worked in the cybersecurity industry — Goldberg at incident response firm Sygnia and Martin as a ransomware negotiator at DigitalMint. They paid BlackCat administrators a 20% cut of ransom payments in exchange for access to the ransomware platform. The group extorted approximately $1.2 million in Bitcoin from at least one victim (a Florida medical company), with unsuccessful attempts against nine others. A third co-conspirator, Angelo Martino, who abused his position as a ransomware negotiator to share confidential victim information (including insurance policy limits) with BlackCat operators, pleaded guilty in April 2026 and faces sentencing in July. Goldberg attempted to flee abroad but was tracked through 10 countries by the FBI. [[DOJ](https://www.justice.gov/opa/pr/two-americans-who-attacked-multiple-us-victims-using-alphv-blackcat-ransomware-sentenced); [CyberScoop](https://cyberscoop.com/incident-responders-ryan-goldberg-kevin-martin-sentenced-ransomware/)]

**[NEW] FBI Warns of Cyber-Enabled Cargo Theft Surge — $725M in 2025 Losses**

The FBI issued a public service announcement warning the transportation and logistics industry of a sharp rise in cyber-enabled cargo theft. Estimated losses in the U.S. and Canada reached nearly $725 million in 2025, a 60% surge year-over-year, with confirmed incidents rising 18% and average value per theft growing 36% to $273,990. Threat actors infiltrate freight broker and carrier systems through spoofed emails and phishing, then post fraudulent listings on load boards, impersonate legitimate companies, and reroute high-value shipments to complicit drivers. The FBI urges companies to verify shipment requests through secondary channels, enforce MFA, and maintain detailed records of vehicles and drivers. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-links-cybercriminals-to-sharp-surge-in-cargo-theft-attacks/)]

---

## ⚡ Quick Hits

- **ASUSTOR ADM Root RCE (CVE-2026-6644)** — A proof-of-concept exploit has been published for a critical command injection vulnerability in ASUSTOR's PPTP VPN client. CVSS 9.4, grants root access. With default credentials (admin/admin) unchanged on many deployments, the ~19,000 internet-facing ASUSTOR NAS hosts are at immediate risk. Patch to ADM 5.1.3.RGO1. [[Cyber Security News](https://cyberpress.org/poc-released-asustor-adm-root-rce/)]

- **Backdoored WordPress Plugin** — A long-dormant backdoor in the Quick Page/Post Redirect Plugin (70,000+ installs) was discovered registering a remote update source at `anadnet.com` that could push arbitrary code with full plugin-author permissions. The backdoor was injected in October 2020 and remained active across versions 5.2.1–5.2.3. Administrators should immediately replace with an alternative redirect plugin. [[Cyber Security News](https://cyberpress.org/backdoored-wordpress-plugin-uses-remote-update/)]

- **Krebs Investigation: Anti-DDoS Firm Behind Brazilian ISP Attacks** — KrebsOnSecurity reports that Huge Networks, a Brazilian DDoS protection firm, was compromised and its infrastructure used to build a Mirai-based botnet from TP-Link Archer AX21 routers (CVE-2023-1389) that conducted sustained DDoS attacks against Brazilian ISPs. The CEO attributes the compromise to a January 2026 intrusion and claims a competitor is responsible. [[Krebs on Security](https://krebsonsecurity.com/2026/04/anti-ddos-firm-heaped-attacks-on-brazilian-isps/)]

- **Bluekit Phishing Kit with AI Assistant** — A new all-in-one phishing platform called Bluekit offers 40+ templates targeting major services (Gmail, Outlook, GitHub, iCloud, Ledger) and includes an AI assistant panel supporting Llama, GPT-4.1, Claude, Gemini, and DeepSeek for drafting phishing campaigns. Stolen data is exfiltrated via Telegram. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-bluekit-phishing-service-includes-an-ai-assistant-40-templates/)]
