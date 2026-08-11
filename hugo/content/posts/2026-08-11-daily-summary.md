---
title: "🔴 Gunra Ransomware Joint Advisory, 🎯 DeadLock Rust Encryptor Deep-Dive, 🎯 Abyssos RAT Emerges, ⚠️ Pass-the-Passkey MFA Bypass, 🛡️ Ghostjacking Turns Logs Into Attack Vectors, 📋 OpenAI Ships GPT-5.6-Cyber"
date: 2026-08-11
tags: ["ransomware","critical infrastructure","MFA","supply chain","AI security","vulnerabilities"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "US and South Korean agencies issued a joint advisory on Gunra ransomware exploiting Fortinet VPN flaws, while Microsoft and Zscaler dissected DeadLock and Abyssos; researchers broke passkey MFA assumptions, mapped a LiteLLM supply-chain blast radius, and showed poisoned logs can hijack AI agents."
---

# Daily Threat Intelligence Digest — August 11, 2026

*103 articles ingested and analyzed from curated cyber intelligence feeds.* External research confirmed the SonicWall SMA1000 flaw pair exploited as zero-days remains flagged in CISA's KEV catalog for ransomware-campaign use.

---

## 🔴 Critical Threats & Active Exploitation

### [UPDATE] Joint US–South Korea Advisory: Gunra Ransomware Exploits Fortinet VPNs to Bypass MFA and Steal Cloud Data

CISA and South Korean agencies issued a joint #StopRansomware advisory on the Gunra ransomware-as-a-service operation, which is exploiting vulnerable Fortinet VPN appliances, weak remote-access controls, and exposed RDP infrastructure to enter enterprise networks — chaining FortiOS authentication bypasses CVE-2024-55591 and CVE-2025-24472 to create persistent superuser accounts and bypass MFA. Built on leaked Conti source code and first seen in April 2025, Gunra has hit government, healthcare, finance, manufacturing, transportation, utilities, education, media, and retail across Africa, the Americas, Asia-Pacific, Europe, and the Middle East. The group recruits ethical hackers and penetration testers and reportedly benefits from tools tied to North Korean government-linked hackers; affiliates exfiltrate documents and data before encryption, then threaten publication on a Tor-hosted leak site. Windows and Linux variants encrypt files with ChaCha20 and RSA-4096, appending the .ENCRT extension. Patch exposed VPNs immediately, enforce phishing-resistant MFA, and segment edge infrastructure.

**Sources:** [Cyber Security News](https://cyberpress.org/gunra-ransomware-bypasses-vpn-mfa/) · [CyberScoop](https://cyberscoop.com/us-south-korea-gunra-ransomware-warning/) · [Malware News (CISA advisory)](https://malware.news/t/cisa-advisory-stopransomware-gunra-ransomware/124662) · [Malware News (ChaCha20 analysis)](https://malware.news/t/gunra-ransomware-multithreaded-chacha20-encryption-explained/124675)

### [UPDATE] SonicWall SMA1000 Zero-Days Now Confirmed in Ransomware-Campaign Use

CISA has confirmed ransomware gangs are exploiting the two SonicWall SMA1000 vulnerabilities disclosed July 14 — CVE-2026-15409, a maximum-severity (CVSS 10.0) unauthenticated server-side request forgery in the Appliance Workplace interface, and CVE-2026-15410, a CVSS 7.2 code-injection flaw in the Management Console — both added to the KEV catalog and flagged as used in ransomware campaigns. The SSRF turns an internet-facing VPN gateway into a proxy for internal services; chained, the pair escalates from unauthenticated internet access to root-level appliance compromise. PSIRT observed pre-disclosure exploitation beginning June 22 by a cluster tracked as UTA0533, and subsequent reporting links substantial activity to the INC ransomware operation. Organizations on affected SMA 6210/7210/8200v firmware must upgrade to 12.4.3-03453 or 12.5.0-02835 and treat previously exposed, unpatched appliances as compromised — re-image, rotate credentials, and reset TOTP tokens.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-sonicwall-sma1000-flaws-now-exploited-by-ransomware-gangs/) · [Cyber Security News](https://cyberpress.org/cisa-sonicwall-sma1000-ssrf-zero-day-attacks/)

### [UPDATE] Water Campaign Expands: New Jersey and Alabama Utilities Join the Target List

Two New Jersey water systems — Cape May and Woodbine — were targeted in cyberattacks on July 27, and Alabama utilities have now reported similar activity, expanding the multi-state campaign beyond the states already disclosed. The FBI says water and wastewater utilities in at least seven states have reported incidents since July 27, with some activity degrading water operations; reporting attributes the campaign to Iranian hackers targeting internet-exposed programmable logic controllers, including Rockwell Automation devices. The New Jersey systems appear to have suffered only phone-system disruption, but the campaign's steady geographic spread argues for treating every internet-facing ICS controller as an active beachhead.

**Sources:** [SecurityWeek](https://www.securityweek.com/new-jersey-alabama-join-states-targeted-in-water-cyberattacks/) · [FBI alert](https://www.fbi.gov/investigate/cyber/alerts/2026/malicious-cyber-actors-targeting-water-and-wastewater-sector-internet--facing-programmable-logic-controllers-causing-operational-disruptions)

### [UPDATE] CERT Polska Confirms Siemens PLC Sabotage at Polish CHP Plant via Private APN

A follow-up report from CERT Polska confirms hackers used a dedicated mobile gateway and a private Access Point Name (APN) — misconfigured to allow arbitrary devices on the network to communicate — to pivot from a wind farm into the OT network of a Polish combined heat-and-power plant, where they sabotaged Siemens programmable logic controllers and shut down a steam turbine and the process-water treatment system. The December 29, 2025 intrusion hit a facility supplying heat to roughly 50,000 residents and briefly interrupted cogeneration. CERT Polska warns the APN misconfiguration pattern is common in Poland and elsewhere and has published hardening recommendations for private APN deployments.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-breached-a-small-polish-energy-plant-via-private-apn-last-year/) · [GBHackers](https://gbhackers.com/siemens-plc-network/) · [Cyber Security News](https://cyberpress.org/apn-hackers-halt-turbine/)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] DeadLock Ransomware: Rust Encryptor With Decentralized Recovery Infrastructure

Microsoft Threat Intelligence detailed DeadLock, an emerging financially motivated operation first seen in July 2025 that has already listed more than 80 organizations on its leak site — more than half in Europe — across IT, mining, manufacturing, transportation, logistics, hospitality, and consumer goods. Its recovery ecosystem combines the Session messaging network with blockchain-backed services, making communication, leak-hosting, and negotiation infrastructure resilient to takedown. The Rust-based encryptor's pre-encryption routine disables Windows Defender, deletes backups, and clears event logs; it also geofences against Russian, Ukrainian, Belarusian, and several CIS languages plus Iran, Syria, Oman, and Yemen, deleting itself in those locales. DeadLock is linked to affiliates of the Lynx and INC ransomware ecosystems.

**Sources:** [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/08/10/deadlock-ransomware-breaking-down-a-rust-based-encryptor-with-decentralized-recovery-infrastructure/) · [GBHackers](https://gbhackers.com/deadlock-ransomware-attack/) · [Cyber Security News](https://cyberpress.org/deadlock-steals-encrypts-extorts/)

### [NEW] Abyssos: New Modular C++ RAT Combines Hidden VNC, Browser Hijacking, and Credential Theft

Zscaler ThreatLabz documented Abyssos, a C++ remote-access trojan first observed in late June 2026 and still under active development, that functions as a full post-compromise framework rather than a single-purpose stealer. Its most concerning feature is a hidden VNC capability — HVNC_START opens a remote virtual desktop and HVNC_INPUT lets operators simulate keyboard and mouse activity, launching Chrome, Edge, Firefox, and other applications inside an isolated session to sidestep desktop monitoring. Abyssos also steals browser sessions and credentials, exfiltrates files, logs keystrokes, and downloads additional modules from its C2, giving operators an interactive foothold for hands-on intrusion activity.

**Sources:** [Cyber Security News](https://cyberpress.org/abyssos-rat-takes-control/) · [GBHackers](https://gbhackers.com/abyssos-rat-hijacks-browser-sessions/)

### [NEW] Aeternum Botnet Runs Entire C2 Stack on the Polygon Blockchain

Unit 42 analyzed Aeternum, a C++ botnet loader that shifts command-and-control entirely to the public Polygon blockchain, with operators writing encrypted and plaintext instructions directly into smart contracts that infected devices query via public RPC endpoints. The design eliminates centralized servers and domains, making infrastructure takedown impractical — an evolution of the EtherHiding-style blockchain C2 pattern. Aeternum also uses VM detection and antivirus scanning checks to evade analysis.

**Source:** [Unit 42](https://unit42.paloaltonetworks.com/aeternum-blockchain-c2-analysis/)

### [NEW] ErrTraffic MaaS Stores Malware Delivery Infrastructure in Polygon Smart Contracts

WatchGuard Threat Lab documented ErrTraffic, a malware-as-a-service operation that hides its delivery infrastructure inside Polygon blockchain smart contracts rather than embedding C2 addresses in injected website code, letting operators rotate infrastructure without touching the compromised sites hosting the initial lure. The chain combines ClickFix social engineering with blockchain-based EtherHiding and dynamic payload delivery, pushing Vidar, Okobot, LegionLoader, OnionDrop-related payloads, and BabaDedaLoader, plus DLL side-loading variants. Detection and takedown become significantly harder when the delivery layer lives on-chain.

**Source:** [Cyber Security News](https://cyberpress.org/errtraffic-conceals-infrastructure-on-polygon/)

### [NEW] Play Ransomware Masquerades as PsExec With Custom PSexesvc.exe Service

Play ransomware is deploying a custom service binary named PSexesvc.exe that mimics Microsoft Sysinternals PsExec, hiding in plain sight as routine Windows administration during lateral movement and payload execution. The binary has been observed alongside tools and a ransom note staged in C:\Users\Public\Music\, an unremarkable-looking path during investigations. Play also uses genuine PsExec and WMI for lateral movement, so defenders must treat the T1036 masquerading pattern — not just the binary name — as the detection signal.

**Source:** [GBHackers](https://gbhackers.com/play-ransomware-minics-psexec/)

### [UPDATE] Storm-1175 Deploys StormEncryptor Ransomware as Third Strain — China-Based Former Medusa Affiliate

Microsoft Threat Intelligence attributes the new StormEncryptor ransomware family to Storm-1175, a financially motivated actor believed to be China-based whose recent attacks were likely preceded by exploitation of CVE-2026-18577, the N-able N-central authentication bypass added to CISA's KEV catalog this month. The deployment marks the actor's third ransomware strain in recent months, following Medusa and prior tooling, with a history of exploiting zero-days and n-days in GoAnywhere MFT, SmarterTools SmarterMail, Microsoft Exchange, Ivanti Connect Secure, and JetBrains TeamCity. Organizations running N-central should treat the appliance as compromised if unpatched and hunt for StormEncryptor artifacts.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-stormencryptor-ransomware-used-by-former-medusa-affiliate/)

### [NEW] Six npm Packages Fetch Payloads via Ethereum Transactions — DPRK-Linked Technique

Sonatype Research Labs identified six npm packages delivering the same malicious payload — three hijacked legitimate packages and three new malicious ones — that use the "NullReceiver" technique to retrieve infrastructure from Ethereum transactions. The activity shares the same Ethereum wallet address flagged by OpenSourceMalware in the DPRK-linked Contagious Interview campaign, extending blockchain-based delivery into the North Korean IT-worker social-engineering playbook. Review dependency trees for the flagged packages and audit for Ethereum transaction-based payload resolution.

**Source:** [Malware News](https://malware.news/t/six-npm-packages-use-ethereum-transactions-to-retrieve-malicious-payloads/124654)

---

## ⚠️ Vulnerabilities & Patches

### [NEW] "Pass-the-Passkey" Attack Family Breaks Phishing-Resistant MFA Without Touching Private Keys

SpecterOps disclosed more than 20 Pass-the-Passkey techniques that undermine WebAuthn passkey protections across Windows 11, Microsoft Entra ID, browsers, password managers, and enterprise authentication workflows — without breaking FIDO2 cryptography or extracting private keys from hardware security keys. Instead, the attacks exploit the ecosystem around passkeys: endpoint logging gaps, weak server-side assertion validation, and authentication-prompt and application-interface weaknesses. The most serious chain combines a Windows event logging flaw with insufficient WebAuthn assertion validation to impersonate privileged enterprise users. The research challenges the assumption that passkeys are inherently replay- and session-abuse-proof.

**Sources:** [Cyber Security News](https://cyberpress.org/pass-the-passkey-attack/) · [GBHackers](https://gbhackers.com/pass-the-passkey-attack-exploits-windows-and-entra-id/)

### [NEW] Cisco ClamAV Memory Corruption Bugs Let Remote Attackers Crash Secure Endpoint Scanning

Cisco disclosed multiple ClamAV memory-corruption vulnerabilities — CVE-2026-20337, CVE-2026-20338, CVE-2026-20339, and CVE-2026-20345 — that let unauthenticated remote attackers terminate the ClamAV scanning process on affected Secure Endpoint Connector installations (advisory cisco-sa-clamav-WuuvVd26). Windows connectors carry a High impact rating and CVSS 7.5 because the scanning process runs in a privileged context; Linux and macOS connectors received Medium ratings. SecurityWeek notes public proof-of-concept code is available, so patch the connector fleet promptly.

**Sources:** [Cyber Security News](https://cyberpress.org/clamav-memory-corruption-bugs/) · [SecurityWeek](https://www.securityweek.com/cisco-warns-of-high-severity-clamav-vulnerabilities-with-public-poc/)

### [NEW] Red Hat ACM Flaw Lets Namespace Editors Escalate to Full Kubernetes Cluster-Admin

CVE-2026-10090 (CVSS 9.9) is a critical privilege-escalation vulnerability in Red Hat Advanced Cluster Management for Kubernetes, rooted in the Application Subscription controller (multicluster-operators-subscription), that lets a user with limited namespace-level editing permissions obtain full cluster-admin access across the cluster. The flaw, made public August 5, breaks a core Kubernetes authorization boundary — the separation between namespace-scoped and cluster-scoped permissions. Patch ACM immediately and audit for unexpected cluster-admin grants.

**Sources:** [Cyber Security News](https://cyberpress.org/red-hat-acm-flaw-namespace-editors-escalate/) · [GBHackers](https://gbhackers.com/red-hat-kubernetes-flaw/)

### [NEW] LiteLLM Supply-Chain Breach Blast Radius: 2,500+ Organizations and 434,000 CI/CD Pipelines

CloudSEK's analysis of the LiteLLM AI supply-chain compromise — orchestrated by Team PCP in March 2026 by pushing a malicious package to the popular LLM gateway — reconstructs exposure across more than 2,500 organizations and roughly 434,000 CI/CD pipelines worldwide. The short-lived malicious package created standing risks to cloud credentials, source-code repositories, Kubernetes environments, package registries, and AI services downstream of build and deploy chains. Organizations using LiteLLM or its dependents should rotate cloud credentials, audit pipeline secrets, and review Kubernetes access as if the dependency chain was compromised.

**Sources:** [Malware News](https://malware.news/t/2-500-companies-and-434-000-ci-cd-pipelines-exposed-in-the-largest-ai-supply-chain-breach-of-2026/124673) · [Cyber Security News](https://cyberpress.org/litellm-breach-threatens-cloud/)

---

## 🛡️ Defense & Detection

### [NEW] GitHub Expands Dependabot Malware Alerts to Eight Package Ecosystems

GitHub extended Dependabot's malware-detection capability beyond npm to PyPI, Maven, RubyGems, NuGet, Go, crates.io, and PHP Composer, ingesting OpenSSF's shared malicious-packages repository as a new threat-intelligence source. The expansion closes a gap for polyglot environments where malicious Python, Java, Ruby, .NET, Go, Rust, and PHP dependencies previously went unalerted. Enable the alerts across repos and treat the OpenSSF-sourced indicators as a standing dependency-hygiene feed.

**Sources:** [Cyber Security News](https://cyberpress.org/github-expands-dependabot-malware-alerts/) · [GBHackers](https://gbhackers.com/github-expands-dependabot-malware-alerts/)

### [NEW] "Ghostjacking": Poisoned Logs Turn Enterprise AI Agents Into Attack Tools

Researchers at Tenet presented Ghostjacking at DEF CON, demonstrating how adversaries can plant malicious instructions as plain text inside logs and alerts generated by Cloudflare, Datadog, and Sentry monitoring platforms — content that AI agents read and execute word for word. A blocked request's error log, rendered into an agent's context, becomes a live instruction to take harmful actions, turning trusted observability data into an attack surface. Treat logs and alerts as untrusted input to agentic tooling, and validate agent actions against the data they were built to read.

**Sources:** [SecurityWeek](https://www.securityweek.com/ghostjacking-attack-uses-poisoned-logs-to-turn-ai-agents-bad/) · [CryptoBriefing](https://cryptobriefing.com/ghostjacking-attack-poisoned-logs-ai-agents/)

### [NEW] Claude Code Makes Auto Mode Default — Classifier Blocks 89% of Dangerous Commands

Anthropic is flipping Claude Code's default permission setting to Auto Mode starting August 14 for Pro, Max, and Team plans, replacing manual approval prompts with an automated classifier that blocks 89% of dangerous commands and prompt-injection attacks. The change responds to "permission fatigue": users approve 97% of permission prompts, a rate the company calls reflexive clicking rather than scrutiny. The classifier reduces — but does not eliminate — the risk of agentic code execution, so keep least-privilege tooling, sandboxed environments, and review gates around agent workloads.

**Sources:** [Cyber Security News](https://cyberpress.org/claude-code-makes-auto-mode-default/) · [GBHackers](https://gbhackers.com/claude-code-auto-mode-blocks-attacks/)

---

## 📋 Policy & Industry News

### [NEW] OpenAI Expands Daybreak With GPT-5.6-Cyber for Vetted Defenders

OpenAI announced the expansion of its Daybreak cybersecurity program with two tiers and a purpose-trained model: Daybreak Blue offers approved defenders general-purpose frontier models (GPT-5.6 Sol) for vulnerability discovery, secure code review, malware analysis, and incident response, while Daybreak Red unlocks GPT-5.6-Cyber for authorized vulnerability research, exploit validation, and security testing. Access is restricted to select companies — Accenture, IBM, Capgemini, Cognizant, EY, KPMG, PwC, NCC Group, SpecterOps — and security vendors including Palo Alto Networks, CrowdStrike, Cisco, Sophos, Akamai, Fortinet, and Cloudflare. OpenAI says the model will not be available to general users, citing abuse risk.

**Sources:** [GBHackers](https://gbhackers.com/openai-launches-gpt-5-6-cyber-to-find-zero-day-vulnerabilities/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/openai-releases-chatgpt-56-cyber-but-its-only-for-approved-users/) · [CyberScoop](https://cyberscoop.com/openai-daybreak-expansion-specialized-cyber-services/)

### [NEW] Mozilla Rotates Firefox and Thunderbird GPG Signing Key After Exposure

Mozilla issued a new GPG signing subkey for Firefox and Thunderbird artifacts after an unencrypted copy of the previous key was inadvertently committed to a private GitHub repository. The key signed Linux tarballs, RPM packages, and checksum files; the exposure of the private copy meant anyone with access could have forged signed release artifacts. Mozilla has rotated and revoked the affected subkey — verify artifact signatures against the new key and audit recent downloads from mirrors.

**Sources:** [SecurityWeek](https://www.securityweek.com/mozilla-issues-new-firefox-gpg-key-following-exposure/) · [Mozilla Security Blog](https://blog.mozilla.org/security/2026/08/10/updated-gpg-key-for-signing-firefox-and-thunderbird-releases/)

### [NEW] NATO and AI Startup AISLE Join CVE Numbering Authorities Under ENISA Root

The NATO Cyber Security Centre and AISLE, a San Francisco– and Prague-based AI vulnerability-research startup, joined the CVE program as numbering authorities under the ENISA Root, bringing the total to 20 authorities. The move gives NATO's cyber defense arm and AI-assisted vulnerability discovery a direct role in assigning the identifiers the industry uses to track flaws. Expect faster CVE assignment for NATO-identified vulnerabilities and AI-discovered software defects.

**Source:** [CyberScoop](https://cyberscoop.com/nato-aisle-enisa-cve-vulnerability-tracking/)

### [NEW] UK Man Tied to "The Com" Sentenced for Blackmail and Sextortion Against 117 Victims

Justin Swaddle, a 20-year-old from Leeds tied to the loosely organized online criminal network "The Com," was sentenced to two years in prison after pleading guilty to child sexual abuse offenses and blackmail affecting 117 victims across multiple countries. The National Crime Agency investigated Swaddle from January 2024 after his October 2023 arrest on charges of possessing, making, and distributing indecent images; he must now register as a sex offender. The sentence underscores the ongoing law-enforcement crackdown on the network's victimization of children and teenagers.

**Sources:** [CyberScoop](https://cyberscoop.com/uk-justin-swaddle-the-com-sentenced/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/member-of-the-com-sent-to-prison-for-blackmail-sextortion/)

### [NEW] Valve Notifies Steam Hardware Customers of Breach at Shipping Partner CEVA Logistics

Valve is notifying Steam hardware customers in Europe that attackers who breached its shipping partner CEVA Logistics between July 29 and August 1 accessed information needed to ship hardware orders. CEVA — a CMA CGM subsidiary operating 1,000 warehouses — is one of the world's largest logistics providers, and the stolen data centers on shipping details for Steam hardware purchases. Customers should be alert to shipping-themed phishing that leverages the stolen order data.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/valve-notifies-steam-hardware-customers-of-a-data-breach/)

---

## ⚡ Quick Hits

- **LexisNexis takes services offline after suspicious activity** — Diligence, Metabase API, and Newsdesk were disconnected after unusual activity on servers hosted by an unnamed third-party vendor; the company is rebuilding affected systems in a new environment with help from a forensic firm. ([BleepingComputer](https://www.bleepingcomputer.com/news/security/lexisnexis-shuts-down-services-after-suspicious-activity-on-servers/))

- **Android banking droppers surge as operators change packaging** — Kaspersky Q2 telemetry shows blocking down overall but banking payloads increasingly wrapped in loader apps and detected as Trojan-Droppers, shifting threat-category rankings while distribution tactics evolve to evade app-store controls. ([GBHackers](https://gbhackers.com/android-banking-droppers/))

- **The Gentlemen claims attack on AnMed Health** — the ransomware group listed the US healthcare provider on August 10, threatening to leak sensitive data unless AnMed engages in negotiations; organizations in the sector should watch for credential-based initial access. ([Malware News](https://malware.news/t/the-gentlemen-ransomware-attack-on-anmed-health-system/124670))

- **Advisory wave:** Plesk Obsidian blind SQL injection (CVE-2026-64636, prior to 18.0.80.1), Roundcube Webmail security updates 1.6.18 and 1.7.3, HashiCorp Consul (prior to 2.0.3), Magnolia CMS stored XSS (CVE-2026-18478), plus Qualcomm, Cisco Secure Endpoint, Dell, and IBM bulletins — apply the Canadian Cyber Centre's AV26-788 through AV26-795 batch this week. ([Malware News](https://malware.news/t/webpros-security-advisory-av26-790/124642))

- **Lumma Stealer or variant observed in the wild** — Malware Traffic Analysis posted a fresh 2026-08-10 infection analysis of the Lumma stealer family; review the IoCs if your org touches the flagged delivery chains. ([Malware News](https://malware.news/t/2026-08-10-lumma-stealer-or-variant/124671))

- **Anthropic adds invisible watermarks and C2PA metadata to Claude content** — EU-released Claude models from August 2 include machine-readable content marking, with global rollout planned, following Anthropic's signing of the EU AI Act Article 50(2) transparency code. ([Cyber Security News](https://cyberpress.org/anthropic-adds-invisible-watermarks-c2pa-metadata/))
