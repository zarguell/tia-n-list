---
title: "ColdFusion RCE Exploited ⚡ PolinRider Supply Chain 🎯 Armored Likho APT 🛡️ Veil#Drop Stealer ⚠️ Bad Epoll PoC 🔐 AI Crypto Injection"
date: 2026-07-06
tags: ["CVE-2026-48282","ColdFusion","PolinRider","North Korea","supply chain","Armored Likho","APT","Veil#Drop","PureLog","infostealer","CVE-2026-46242","Bad Epoll","Linux kernel","prompt injection","AI agents","cryptocurrency","US Army","defacement"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "ColdFusion CVE-2026-48282 exploited within 2 hours of disclosure — patch immediately. PolinRider campaign compromises 100+ open source packages. Armored Likho APT targets government and energy sectors. Veil#Drop framework abuses Blogspot for PureLog stealer delivery. Bad Epoll PoC exploit released. AI agents tricked into crypto payments via SEO poisoning and hidden prompts."
---

# Daily Threat Intelligence Digest — July 6, 2026

*14 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Adobe ColdFusion CVE-2026-48282 Exploited Within Two Hours of Disclosure — Shadowserver Tracks ~800 Exposed Instances, CCCS Warns of Ongoing Attacks**

KEVIntel confirmed that threat actors began exploiting CVE-2026-48282, a maximum-severity unauthenticated remote code execution vulnerability in Adobe ColdFusion (CVSS 10.0), **within two hours** of Adobe's public disclosure on Tuesday. The flaw affects ColdFusion versions 2025.9, 2023.20, and earlier, requiring no user interaction for exploitation.

The Canadian Center for Cyber Security (CCCS) has urged defenders to secure systems against ongoing attacks. Shadowserver now tracks approximately 800 Adobe ColdFusion instances exposed online, though the split between honeypots and exploitable systems is unknown. Adobe had tagged the vulnerability Priority 1 — indicating high risk of targeted exploitation — and urged administrators to patch within 72 hours. KEVIntel founder Ryan Dewhurst observed the exploitation through the firm's global honeypot network.

*Previously covered July 1 at disclosure. New today: confirmed active exploitation within 2 hours of patch release, ~800 exposed instances, CCCS warning issued.* [[BleepingComputer](https://www.bleepingcomputer.com/news/security/max-severity-adobe-coldfusion-flaw-now-exploited-in-attacks/)]

**Recommended action:** Patch ColdFusion instances immediately. If patching is delayed, restrict network access to ColdFusion management interfaces and monitor for anomalous HTTP requests to ColdFusion endpoints.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] PolinRider: North Korean Hackers Compromise 100+ Open Source Packages in Broad Supply Chain Campaign**

North Korean state-sponsored hackers are targeting open source developers in a supply chain campaign tracked as PolinRider, active since December 2025. Socket reports that the campaign has compromised **108 unique packages** producing **162 malicious release artifacts** across NPM, Packagist, Go modules, and Chrome extensions.

Attackers compromise maintainer accounts to tamper with legitimate repositories, then push infected packages. They also rewrite Git history to make malicious changes appear older. The compromised repositories contain obfuscated JavaScript loaders that connect to blockchain and public RPC infrastructure to retrieve encrypted payloads — delivering the DEV#POPPER remote access trojan (RAT) and the OmniStealer information stealer.

The campaign recently expanded to Packagist, where multiple packages under the `sevenspan` namespace were compromised, with malicious loaders hidden in configuration files that were missed during cleanup. This is associated with the broader Contagious Interview operation, which overlaps with DeceptiveDevelopment, Operation Dream Job, and ClickFake Interview campaigns.

Socket warns that "teams that installed any affected package or extension version should treat the installation environment as potentially compromised" — because the malware targets developer environments, remediation should be performed from a clean machine. [[SecurityWeek](https://www.securityweek.com/north-korean-hackers-target-open-source-developers-in-supply-chain-attacks/)]

**Recommended action:** Audit environments for any packages from compromised namespaces (sevenspan on Packagist). Scan developer workstations for DEV#POPPER or OmniStealer indicators. Rotate all credentials from potentially compromised build machines.

---

**[NEW] Armored Likho APT Targeting Government and Electric Power Entities in Three Countries**

Kaspersky has identified a new advanced persistent threat actor tracked as **Armored Likho** conducting financially motivated attacks and cyber-espionage operations against government and electric power organizations in **Russia, Brazil, and Kazakhstan**.

The actor's arsenal includes modular remote access trojans and information stealers — chief among them **BusySnake Stealer**, a Python-based infostealer that packs multiple evasion techniques, dynamically decrypting bytecode only when a function is called and re-encrypting it immediately after. The malware can capture screenshots, exfiltrate keystroke logs, decrypt stored passwords from Chromium and Firefox browsers, extract cookies, scrape OTP keys, harvest Telegram sessions and credentials, find cryptocurrency wallets, and establish reverse SSH tunnels for persistent interactive access.

Initial access is achieved through spear-phishing emails containing archives with executables or LNK files that display decoy documents while malware installs in the background. The group previously used Go2Tunnel for remote access tunneling but has since integrated that capability directly into BusySnake Stealer. Armored Likho's operations appear to overlap with the previously documented **Eagle Werewolf** group, which used the structurally similar AquilaRAT. [[SecurityWeek](https://www.securityweek.com/armored-likho-apt-targeting-government-electric-power-entities/)]

**Recommended action:** Monitor for spear-phishing emails targeting government and energy sector employees, particularly those containing LNK files or executables with decoy documents. Deploy Python runtime monitoring in critical environments.

---

**[NEW] Veil#Drop: Multi-Stage Fileless Malware Framework Abuses Google Blogspot to Deliver PureLog Stealer**

Securonix has uncovered a sophisticated malware delivery framework dubbed **Veil#Drop** that chains together compromised websites, Google's Blogspot infrastructure, PowerShell download cradles, and fileless execution techniques to deploy the **PureLog Stealer**.

The infection chain begins with a JavaScript file posing as a document that launches PowerShell code bypassing execution policies. The PowerShell retrieves payloads from attacker-controlled Blogspot pages. A second-stage loader contains XOR-encoded .NET assemblies stored as large embedded data blobs that are reconstructed and decrypted at runtime — preventing static analysis and bypassing signature-based detection.

PureLog Stealer harvests credentials, cookies, autofill data, session tokens, and browsing histories from Chrome, Edge, Firefox, Brave, Opera, and Chromium-based browsers — plus cryptocurrency wallets, messaging apps, email clients, FTP clients, cloud storage tools, and password managers. Securonix notes that "in enterprise environments, information stealers are frequently the first stage of larger intrusion campaigns" — stolen credentials can later enable ransomware, data theft, BEC attacks, or long-term espionage. [[SecurityWeek](https://www.securityweek.com/blogspot-hosted-payloads-delivered-in-veildrop-attacks/); [The Hacker News](https://thehackernews.com/2026/07/veildrop-malware-chain-uses-blogger.html)]

**Recommended action:** Monitor for PowerShell execution originating from JavaScript or document files. Block untrusted Blogspot domains in proxy policies. Review endpoint detection rules for XOR-encoded .NET assembly loading patterns.

---

## ⚠️ Vulnerabilities & Patches

**[UPDATE] Public PoC Exploit Released for Linux 'Bad Epoll' (CVE-2026-46242) — Root Access on Servers and Android**

A proof-of-concept exploit has been publicly released for **CVE-2026-46242**, the Linux kernel race condition and use-after-free vulnerability in the epoll event notification subsystem. The flaw enables unprivileged local users to escalate to root privileges on Linux desktops, servers, and Android devices.

*Previously covered July 5 at disclosure. New today: public PoC exploit available in the wild. The race condition was patched in recent kernel updates but required two attempts to fully fix.* [[SecurityWeek](https://www.securityweek.com/proof-of-concept-exploit-released-for-linux-bad-epoll-root-access-vulnerability/); [Threat Modeling](https://threat-modeling.com/cve-2026-46242-bad-epoll-linux-kernel-root-privesc-android/)]

**Recommended action:** Apply latest kernel updates immediately. Verify Android security patch levels. On systems where patching is delayed, restrict unprivileged user namespaces.

---

**[NEW] SEO Poisoning + Hidden Prompts Trick AI Agents Into Making Cryptocurrency Payments**

Zscaler ThreatLabz has documented two active campaigns using **indirect prompt injection** embedded in malicious websites to exploit autonomous AI agents into making cryptocurrency payments and trusting fraudulent platforms.

In the first campaign, attackers used SEO poisoning to rank for searches related to the Python library `requests-secure-v2`. The fraudulent website contains hidden prompts instructing AI agents to make a payment as part of an API key acquisition flow — including a hidden `<div>` tag and schema markup directing the agent to initiate a cryptocurrency transfer. The attackers maintain 10 GitHub repositories linking to multiple similar websites.

In the second campaign, a typosquatting operation imitates the decentralized finance platform **DeBank**, with hidden prompts telling AI agents the impersonating site is the legitimate domain. Zscaler tested 26 LLMs against these attacks: **four models** (Llama 3.3 70B, Llama 3.2 90B Vision, Gemini 3 Flash, Gemini 2.5 Pro) made actual payments, and **two models** (Claude Sonnet 4.5, GPT-5.4) miscategorized the fraudulent site as legitimate.

"As AI agents become a more common interface to the web, the content itself is going to become a larger attack surface," Zscaler notes. [[SecurityWeek](https://www.securityweek.com/prompt-injection-attacks-trick-ai-agents-into-making-crypto-payments/)]

**Recommended action:** Organizations deploying AI agents with web-browsing or payment capabilities should implement strict allowlists for financial transactions, validate cryptocurrency addresses against known legitimate sources, and monitor for unexpected outbound payment initiation from AI agent workflows.

---

## 📋 Policy & Industry News

**[NEW] US Army Websites Defaced With Pro-Kurdish Messages — 404 Hijacking Campaign Targets Legacy Third-Party Hosting**

Multiple US Army subdomains — **oil.army.mil** (Open Innovation Lab) and **ai2c.army.mil** (Artificial Intelligence Integration Center) — were defaced in a 404 hijacking campaign displaying messages denigrating President Donald Trump and US Ambassador to Türkiye Tom Barrack, calling to "FREE KURDISTAN," with a sign-off reading "Kurdish sr was here."

The websites run on WordPress and Microsoft cloud infrastructure, hosted on a legacy third-party platform not connected to the Army's enterprise network. The Army confirmed incident response is ongoing and the affected pages have been secured. Kurdish hacktivists have a long history of defacing government websites. [[CyberScoop](https://cyberscoop.com/us-army-websites-defaced-404-hijacking-kurdistan/)]

---

## ⚡ Quick Hits

- **[NEW] France to Stop Certifying Non-Quantum-Safe Encryption** — France is accelerating its post-quantum cryptography transition, announcing it will no longer certify encryption algorithms that are not quantum-safe. The move signals growing regulatory pressure on cryptographic modernization timelines. [[Schneier on Security](https://www.schneier.com/blog/archives/2026/07/france-to-stop-certifying-non-quantum-safe-encryption.html)]

- **[NEW] Vietnam Arrests 7 Suspects Behind HiAnime Anime Piracy Service** — Vietnamese authorities arrested seven individuals behind HiAnime, the largest anime piracy streaming service before its June shutdown. The group generated ~$12.85 million in illegal advertising revenue across 100+ websites hosting 26,000+ pirated anime titles. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/vietnam-arrests-suspects-behind-hianime-anime-piracy-service/)]

- **[NEW] 2-Click Remote Code Execution in Meccha Chameleon via Steam Workshop Maps** — A severe vulnerability in the Steam game Meccha Chameleon allows attackers to achieve remote code execution on every player in a game lobby through malicious Steam Workshop maps. The flaw has since been patched. This represents a novel attack vector — using game mod distribution platforms for malware delivery. [[Khael Kugler](https://khaelkugler.com/blogs/meccha_chameleon.html)]
