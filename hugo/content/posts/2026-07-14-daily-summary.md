---
title: "Daily Threat Intel Digest - 2026-07-14"
date: 2026-07-14T06:00:00Z
tags: ["threat-intel", "rabbitmq", "jscrambler", "supply-chain", "fsb", "turla", "sanctions", "malware", "apt", "lumma-stealer", "crashstealer", "nihon-kotsu", "lidl", "cmmc", "entra-id"]
categories: ["Threat Intelligence"]
author: "Tia N. List"
summary: "RabbitMQ critical OAuth secret disclosure (CVE-2026-57219), Jscrambler npm supply chain compromise with infostealer, EU/UK joint sanctions on FSB/Turla and GRU, Nihon Kotsu taxi operator cyberattack, CrashStealer macOS infostealer, and ASEC's June APT trend report covering 20 state-sponsored groups."
---

# Daily Threat Intelligence Digest — July 14, 2026

20 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] Nihon Kotsu — Japan's Largest Taxi Operator Shuts Down After Cyberattack

Japan's largest taxi operator, **Nihon Kotsu**, disclosed a malware infection that forced the company to shut down internal systems over the weekend, including its taxi dispatch system which remains offline. The company has ~$1 billion in annual revenue, employs 18,228 people, and operates 8,558 taxis. Car hire booking, web reservations, telephone dispatch, and the "labor taxi" service for expectant mothers are all suspended across Tokyo, Yokohama, and Saitama.

Nihon Kotsu confirmed "unauthorized external access (malware infection)" and has engaged external cybersecurity experts. No ransomware group has claimed responsibility yet, and no data leak has been confirmed — but the company acknowledged it is investigating that possibility. Customers have been warned not to open suspicious attachments or click links claiming to come from the company.

**Action:** Monitor for ransomware claims on dark web leak sites. Organizations with supply chain exposure to Japanese transportation/logistics should verify Nihon Kotsu-related service continuity.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/japans-largest-taxi-operator-shuts-systems-after-cyberattack/)

---

### [NEW] Jscrambler npm Supply Chain Compromise — Infostealer in 4 Package Releases

Jscrambler disclosed that an attacker compromised its npm publishing credentials and pushed malicious versions of the `jscrambler` package spanning releases 8.14, 8.16, 8.17, and 8.20. The malicious package included an infostealer executing during the `preinstall` hook, downloaded 1,479 times during the two-hour window before the compromise was detected and the safe version 8.22 was published.

The infostealer used **ChaCha20-Poly1305 per-string obfuscation** and targeted:
- Source code, developer credentials (Git, SSH, environment variables, CI/CD tokens)
- Cloud credentials (AWS, Azure, GCP, Kubernetes secrets)
- AI tool configurations (Claude, Cursor, Windsurf, VS Code, Zed)
- Cryptocurrency wallets (MetaMask, Phantom, Coinbase, Exodus, Trust Wallet)
- Browser data and messaging apps (Slack, Discord, Telegram)

Four dependent Jscrambler packages were also deprecated and replaced. Any developer who installed versions 8.14–8.20 should **treat their environment as compromised** — rotate all secrets, audit CI/CD pipelines, and restore from safe backups.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-backdoor-jscrambler-npm-package-with-infostealer-malware/) · [Socket Research](https://socket.dev/)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] EU and UK Impose First Joint Cyber Sanctions — Target Turla/FSB Center 16, GRU, and Lumma Stealer Operators

The European Union and United Kingdom jointly sanctioned dozens of Russian individuals and entities on July 14 — the first coordinated EU-UK cyber sanctions package. The EU sanctioned nine individuals and four entities; the UK separately sanctioned 24 individuals and entities.

**Key targets:**
- **FSB Center 16 / Turla (Secret Blizzard):** The EU formally identified the FSB's 16th Center as controlling Turla and blamed it for cyberespionage campaigns against France, Germany, Poland, Cyprus, the Netherlands, Austria, Slovakia, Romania, and Finland dating back to 2010. The EU also attributed the **December 2025 attack on Poland's energy grid** (which could have cut power to 500,000 people using DynoWiper) to FSB Center 16/Berserk Bear.
- **GRU leadership:** The UK sanctioned senior GRU figures Vyacheslav Stafeyev, Ivan Senin, and Ivan Kasyanenko for directing hybrid cyber operations and recruiting hackers via Russian universities.
- **IMPULS company:** Sanctioned for recruiting university-based hackers.
- **Lumma Stealer operators:** UK sanctioned individuals linked to the infostealer operation affecting at least 2,100 UK victims over six months.
- **Rybar LLC:** Ten individuals sanctioned for anti-Ukraine disinformation and alleged election interference in Moldova and Armenia.

Germany and France summoned Russian ambassadors. Separately, 13 nations including the US issued a joint advisory on Russian FSB targeting of network infrastructure devices.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/eu-and-uk-hit-russia-with-first-joint-cyber-sanctions-package/) · [CyberScoop](https://cyberscoop.com/eu-uk-russian-cyberespionage-sanctions/)

---

### [UPDATE] FSB Center 16 Router Targeting Campaign — 13-Nation Joint Advisory Reiterates Threat

*Previously covered: July 10 (GRU/Berserk Bear attribution), July 11 (LapDogs campaign). New: 13 nations issue joint advisory with updated technical details on FSB Center 16's exploitation of vulnerable network devices against critical infrastructure.*

The NSA, FBI, and authorities from 12 countries (Canada, Australia, New Zealand, Czech Republic, Denmark, Estonia, Finland, France, Italy, Poland, Sweden, UK) issued a joint cybersecurity advisory on Russia's FSB Center 16 targeting network infrastructure. The hackers scan the internet for routers with default or weak passwords and exploit **Cisco Smart Install** and specific CVEs — including **CVE-2008-4128** (18 years old) and **CVE-2018-0171** — to compromise edge devices.

The advisory recommends disabling Cisco Smart Install, enforcing strong authentication, and monitoring for unusual credentials and logins via local accounts.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-warns-of-actively-exploited-rce-flaws-in-joomla-extensions/) · [CyberScoop](https://cyberscoop.com/russian-fsb-cisco-joint-cybersecurity-advisory/)

---

### [NEW] CrashStealer — macOS Infostealer Impersonates Apple Crash Reporter, Delivered via Signed Notarized Dropper

Jamf researchers have documented **CrashStealer**, a new macOS infostealer masquerading as Apple's CrashReporter. The binary uses Apple's icon, creates a LaunchAgent named `com.apple.crashreporter.helper`, and displays a fake macOS password prompt to harvest Keychain data. First tracked in May 2026 in development, the malware was observed in active attacks in early July.

The payload is delivered via a **signed and Apple-notarized installer** ("Werkbit Setup"), bypassing Gatekeeper without warnings. After credential harvest, CrashStealer targets 14 password managers, 80+ cryptocurrency wallet extensions, browser credentials, and user documents. Stolen data is encrypted with **AES-256-GCM** and exfiltrated via libcurl. The delivery site requires a meeting PIN, suggesting a targeted campaign.

[BleepingComputer / Jamf](https://www.bleepingcomputer.com/news/security/new-crashstealer-malware-poses-as-apple-crash-reporting-tool/)

---

## ⚠️ Vulnerabilities & Patches

### [NEW] CVE-2026-57219 and CVE-2026-57221 — RabbitMQ Flaws Enable Unauthenticated Broker Takeover and Tenant Data Exposure

Miggo Security discovered two access-control vulnerabilities in RabbitMQ, both present since version 3.13.0 (early 2024). **CVE-2026-57219** (CVSS 8.7) is the more severe: an obsolete management endpoint (`GET /api/auth`) returns the broker's confidential OAuth client secret to any unauthenticated requester. In deployments using OAuth with Entra ID, Auth0, Keycloak, or UAA, an attacker can exchange the leaked secret for an administrator token and gain full broker control.

**CVE-2026-57221** (CVSS 5.3) is an authorization bypass in passive queue/exchange declaration operations. Even zero-permission accounts can enumerate queues and exchanges and retrieve metadata in shared environments.

Both are fixed in versions **4.3.0, 4.2.6, 4.1.11, 4.0.20, and 3.13.15**. **Patching alone is insufficient for CVE-2026-57219** — organizations must rotate the OAuth client secret after upgrading.

**Hunting hypothesis:** An unauthenticated attacker discovers a RabbitMQ management interface on port 15672, sends a single GET request to `/api/auth` to retrieve the OAuth client secret, exchanges it with the identity provider for an admin token, and takes full control of the message broker.

[Miggo Security](https://www.miggo.io/post/full-broker-takeover-no-login-required-miggo-discovers-critical-rabbitmq-vulnerabilities-putting-application-data-at-risk) · [CSO Online](https://www.csoonline.com/article/4196093/rabbitmq-flaws-expose-oauth-secrets-risk-complete-takeover-of-the-broker.html) · [GitHub Advisory (CVE-2026-57219)](https://github.com/rabbitmq/rabbitmq-server/security/advisories/GHSA-pj24-8j6m-vq9q) · [GitHub Advisory (CVE-2026-57221)](https://github.com/rabbitmq/rabbitmq-server/security/advisories/GHSA-9q2j-2hq8-22r2)

---

## 🛡️ Defense & Detection

### [NEW] ASEC June 2026 APT Threat Trend Report — 20 Groups Incorporating AI, Cloud, and MaaS

AhnLab's ASEC published its June 2026 APT trend report tracking **20 state-sponsored groups**. Key cross-regional findings:

- **North Korea:** APT38 compromised the Mastra npm supply chain (140+ packages). Kimsuky shifted to LNK files and cloud C2. Lazarus distributed typosquatting packages via npm. UNK_DeadDrop exploited GitHub/GitLab and VS Code/Cursor for credential theft.
- **China:** Multiple groups expanded beyond government/defense targets to medical research and energy. FishMonger enhanced stealth. Mustang Panda exploited Zoho WorkDrive. UNC6508 compromised REDCap servers.
- **Russia:** APT28 evolved PixyNetLoader with PNG steganography. **GreyVibe utilized generative AI and LLMs throughout operations.** Turla deployed STOCKSTAY for long-term diplomatic surveillance.
- **Iran:** MuddyWater leveraged CastleRAT MaaS from the TAG-150 criminal ecosystem. Nimbus Manticore used .NET AppDomain hijacking with Azure infrastructure.

**Action:** Enhanced monitoring of outbound traffic from development environments and CI/CD pipelines is warranted given the proliferation of npm supply chain attacks and cloud-based C2.

[ASEC](https://asec.ahnlab.com/en/94441/)

---

## 📋 Policy & Industry

### [NEW] Microsoft Entra ID: Passkeys Become Default Authentication, SMS/Voice Retired February 2027

Microsoft announced that beginning **September 1, 2026**, Entra ID will make passkeys the default authentication method, auto-enabling users currently on SMS or voice MFA. On **February 1, 2027**, Microsoft-provided SMS and voice authentication will be retired entirely. Microsoft cited AI-powered phishing campaigns reaching **54% click-through rates** as the driver.

[BleepingComputer](https://www.microsoft.com/en-us/security/blog/2026/07/13/microsoft-entra-id-security-updates-passkeys-are-the-default-authentication-method-in-entra-id/)

---

### [NEW] Pentagon Suspends CMMC Phase 2 — Rethinking Contractor Cybersecurity Framework

The DoD has suspended CMMC Phase 2 rulemaking, creating uncertainty for thousands of contractors that have invested in compliance preparation.

[SecurityWeek](https://www.securityweek.com/pentagon-suspends-cmmc-phase-2-as-it-rethinks-contractor-cybersecurity-rules/)

---

### [NEW] Lidl Online Shop Breach — Customer Data Stolen via Service Provider Hack

German supermarket chain **Lidl** notified customers in Germany, Belgium, and the Netherlands that attackers stole personal information from a service provider's customer data file. Passwords, payment info, and addresses were not affected.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/lidl-discloses-online-shop-breach-after-service-provider-hack/)

---

### [NEW] UK Charges Five Linked to Russian Coms Caller ID Spoofing Platform

UK authorities charged five people in connection with **Russian Coms**, a major caller ID spoofing platform used to make over 1.8 million scam calls across 107 countries since 2020.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/uk-charges-suspects-linked-to-russian-coms-call-spoofing-platform/)
