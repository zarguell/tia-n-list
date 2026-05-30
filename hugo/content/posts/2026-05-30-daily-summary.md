---
title: "🔥 PAN-OS auth bypass CISA KEV, 🇳🇱 17M botnet disrupted, 🦠 DriveSurge ClickFix, 💻 JINX-0164 macOS malware, 🧵 npm dependency confusion campaign"
date: 2026-05-30
tags: ["cve-2026-0257","pan-os","palo-alto","botnet","drivesurge","clickfix","jinx-0164","macos-malware","operation-dragon-weave","npm","supply-chain","23andme","data-breach","azure","linkedin","signal","almerys"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA adds PAN-OS GlobalProtect auth bypass (CVE-2026-0257) to KEV with active exploitation across two waves; Dutch authorities disrupt 17M-device Asocks botnet; DriveSurge ClickFix campaign targets thousands of sites; JINX-0164 uses LinkedIn lures for custom macOS malware against crypto devs; Operation Dragon Weave espionage campaign uses Azure Blob C2; 33 malicious npm packages in single-operator dependency confusion campaign."
---

# Daily Threat Intelligence Digest — May 30, 2026

*51 articles ingested from Miniflux Cyber feeds. Saturday edition — focused on genuinely new developments. Prior digests: May 25–29, 2026. Cross-referencing via Reddit r/cybersecurity detected no critical gaps beyond already-observed stories. Stale items omitted: Gogs zero-day, Charter/Carnival breaches, SideCopy, GREYVIBE, The Gentlemen ransomware (all covered May 29).*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] PAN-OS CVE-2026-0257 CISA KEV — GlobalProtect Authentication Bypass Actively Exploited, Rapid7 Confirms Two Attack Waves**

CISA added CVE-2026-0257 to its Known Exploited Vulnerabilities catalog on May 29, confirming active in-the-wild exploitation of an authentication bypass in Palo Alto Networks PAN-OS and Prisma Access. The flaw allows a remote unauthenticated attacker to forge authentication override cookies and establish unauthorized VPN connections through the GlobalProtect gateway — critical for any organization running internet-facing GlobalProtect appliances.

Rapid7 MDR documented two distinct exploitation waves. The first, on May 17, originated from **Vultr** hosting (IP: 104.207.144.154, machine name: `GP-CLIENT`, spoofed MAC: `aa:bb:cc:dd:ee:ff`) targeting local admin accounts via cookie authentication. The second wave on May 21 originated from **Dromatics Systems** (IPs: 146.19.216.119/120/125, machine name: `DESKTOP-GP01`) using SAML authentication profiles — with some victims receiving full VPN IP assignments granting internal network access. The consistent spoofed MAC across both waves strongly suggests a single threat actor.

**The vulnerability mechanics:** The GlobalProtect service (`/usr/local/bin/gpsvc`) decrypts authentication override cookies using the certificate's private key but performs **zero signature verification** on the decrypted content. When the certificate used for cookie encryption is shared with another feature (e.g., the HTTPS service), an attacker can retrieve the public key from the TLS certificate, forge valid cookies with arbitrary usernames, and bypass authentication entirely. The auth override feature is not enabled by default, but once enabled with certificate reuse, exploitation is trivial.

Rapid7 released a public Python PoC script that iterates through the certificate chain and tests each public key. Affected: PAN-OS 10.2.x–12.1.x and Prisma Access. Patches available; 8 of 10 impacted Rapid7 MDR customers experienced authentication probes rather than full VPN establishment. [[Rapid7](https://www.rapid7.com/blog/post/etr-rapid7-observed-exploitation-of-pan-os-globalprotect-authentication-bypass-vulnerability-cve-2026-0257); [Cyber Security News](https://cyberpress.org/pan-os-globalprotect-authentication-bypass/); [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)]

---

**[NEW] Dutch Authorities Disrupt 17-Million-Device Botnet — Seize 200+ Servers Tied to Asocks Proxy Service**

Dutch police and the National Cyber Security Centre (NCSC) took down a massive botnet comprising at least **17 million infected devices**, seizing over 200 servers at a Dutch hosting provider. The botnet is linked to **Asocks**, a proxy service advertising 7 million IPs across 150 locations and 100,000 clients, with subscriptions ranging from $5–$15/month. The infrastructure enabled DDoS attacks, traffic proxying, and cryptocurrency mining. While Asocks markets itself as a legitimate proxy service, the NCSC confirmed the device owners were not knowing participants. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/dutch-govt-disrupts-malware-botnet-with-17-million-infected-devices/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] DriveSurge — New Threat Actor Using ClickFix and Fake Update Drive-By Attacks Across Thousands of Compromised Sites**

A newly tracked threat actor dubbed "DriveSurge" is operating a large-scale drive-by campaign leveraging ClickFix and fake browser/software update lures across thousands of compromised websites. The actor fingerprinted victims for platform-specific payload delivery (Windows, macOS, Linux) with anti-analysis checks, cache-based deduplication to avoid repeated-execution monitoring, and a deliberate two-phase attack architecture — reconnaissance now, exploitation later. This represents the operationalization of ClickFix at scale, consistent with the rising trend observed by Red Canary in May 2026 intelligence insights. [[Malware.News](https://malware.news/t/meet-drivesurge-a-new-threat-actor-using-clickfix-and-fake-update-drive-by-attacks-in-thousands-of-compromised-sites/107440#post_1)]

---

**[NEW] JINX-0164 — Financially Motivated Group Uses LinkedIn Lures and Custom macOS Malware to Target Cryptocurrency Developers**

Wiz Research documented a threat actor tracked as JINX-0164, active since mid-2025, targeting cryptocurrency organizations via sophisticated LinkedIn social engineering. Fake recruiter/business partner profiles direct targets to impersonation sites (Microsoft Teams, Apple driver portals) that deploy **AUDIOFIX** — a macOS infostealer/RAT compatible with both Intel and Apple Silicon, masquerading as the `coreaudiod` system process via launchctl. AUDIOFIX harvests macOS Keychain credentials, browser passwords, SSH keys, cloud tokens (AWS, Azure, GCP), and cryptocurrency wallets, while hijacking active Slack, Discord, and Telegram sessions.

The group's novel CI/CD abuse: stolen GitHub tokens are used to inject malicious code into internal repositories via stealthy Git techniques (altered commit metadata, direct pushes to main branches). In April 2026, JINX-0164 compromised npm package **@velora-dex/sdk v4.9.1** to deploy **MINIRAT**, a lightweight Go backdoor. All C2 shares the domain `datahub.ink`, and the group uses VPNs (Mullvad, Astrill, ExpressVPN) for operational security. While tactics partially overlap with North Korean patterns, researchers found no direct infrastructure overlap, assessing JINX-0164 as a distinct, financially motivated actor. [[GBHackers](https://gbhackers.com/jinx-0164-uses-linkedin-lures/); Wiz Research]

---

**[NEW] Operation Dragon Weave — China-Linked Espionage Campaign Targets Czech Republic and Taiwan Using Azure Blob Storage as Dead-Drop C2**

Seqrite Labs uncovered a targeted spear-phishing campaign against officials and citizens in the Czech Republic and Taiwan, attributed with moderate confidence to a China-based threat actor. The campaign uses **region-specific lures**: a Czech Social Security Administration (ČSSZ) appointment notice and a Traditional Chinese project application review form (計畫申請審查結果通知單). Dual delivery paths — a LNK file triggering a VBS → PowerShell → XOR-decrypted chain, and a Rust-based executable dropper — both converge on DLL sideloading via `UnityPlayer.dll` to execute a Rust loader (**RUSTCLOAK**), which decrypts and runs **AZUREVEIL**, an Adaptix C2 agent with 36 post-exploitation commands and in-memory BOF execution capability.

**Notable C2 tradecraft:** The malware communicates via Microsoft Azure Blob Storage with a SAS token valid from March 2026 through March 2027, blending C2 traffic with legitimate cloud traffic. This dead-drop resolver technique makes the C2 channel resilient to infrastructure takedown — similar to the ClearFake blockchain-based C2 reported May 28, but using enterprise cloud storage instead of smart contracts. [[Malware.News via Seqrite Labs](https://malware.news/t/operation-dragon-weave-uncovering-a-china-linked-campaign-targeting-czech-republic-and-taiwan-using-azure-cloud-c2/107419#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] 33 Malicious npm Packages in Dependency Confusion Campaign — Single Operator, Three Accounts, Nine Scopes, C2 Active on oob.moika.tech**

Microsoft Threat Intelligence published a deep-dive analysis of 33 malicious npm packages published under three accounts (`mr.4nd3r50n`, `ce-rwb`, `t-in-one`) across nine organizational scopes targeting enterprise developer environments. The packages impersonate internal services (SVP BaaS, SberPay payment widget, Capibar Chat UI kit, credential/auth modules) using inflated version numbers (100.100.100) to win dependency resolution over real internal packages.

The execution chain: `npm install` triggers a `postinstall` hook running heavily obfuscated JavaScript that downloads platform-specific payloads from `https://oob.moika[.]tech/payload/<platform>`. Currently in **reconnaissance-only mode** (flag `RECON_ONLY=1`) — collecting environment variables, hostnames, and installed packages — but the architecture supports a server-side toggle to full exploitation (credential theft, data exfiltration, backdooring).

**Single-operator attribution:** All three accounts share the identical hardcoded HTTP header `X-Secret: l95HdDaz3kQx1Zsg3WxH6HvKANf51RY1`, same C2 server, identical package template generator, and temporally correlated publishing bursts (12-minute gap between mr.4nd3r50n and ce-rwb batches on May 28). The `mr.4nd3r50n` account started as a legitimate bug bounty researcher (April 2024) probing npm dependency confusion, then pivoted to malicious publishing ~2 years later. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/29/33-malicious-npm-packages-abuse-dependency-confusion-profile-developer-environments/); [Malware.News](https://malware.news/t/malicious-npm-packages-abuse-dependency-confusion-to-profile-developer-environments/107441#post_1)]

---

## 📋 Policy & Industry News

**[NEW] California AG Sues 23andMe Over 2023 Breach — Violations of Genetic Privacy Act, CCPA, and False Advertising Law**

California Attorney General Rob Bonta filed a lawsuit against 23andMe (now Chrome Holding Co.) over the October 2023 credential-stuffing breach that exposed sensitive genetic and health data of **nearly 7 million customers**, including 855,541 Californians. The suit alleges the company failed to implement reasonable safeguards against credential-stuffing, missed multiple opportunities to detect the intrusion, and made misleading public statements — claiming high security standards before the incident and blaming customers for password reuse afterward. Violations span the California Genetic Information Privacy Act, the California Reasonable Data Security Law, the CCPA, and False Advertising Law. Penalties of $1,000–$7,500 per violation are sought via injunction. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/california-ag-sues-23andme-over-2023-breach-exposing-health-data/)]

---

## ⚡ Quick Hits

- **LLMShare Campaign — ChatGPT Share Links Abused for Malware Delivery:** Push Security discovered threat actors using Google ads to direct ChatGPT-searching users to legitimate `chatgpt.com` shared pages displaying fake OpenAI outage notices. Victims are redirected to `openew[.]app` to download trojanized desktop applications (Windows, macOS). The same operators also abused Claude Artifacts for ClickFix-style lures. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/chatgpt-share-links-abused-to-host-fake-outage-pages-to-deliver-malware/)]

- **Canadian Cyber Centre Issues Alert on GitHub Internal Breach — 3,800 Repos Exfiltrated via Nx Console Supply Chain Attack:** The Canadian Centre for Cyber Security (AL26-013) confirmed the May 18 compromise of GitHub's internal systems through malicious Nx Console VS Code extension v18.95.0, exfiltrating ~3,800 internal repositories. Recommended: audit CI/CD logs for anomalous cloning post-May 18, rotate credentials exposed on developer machines between May 11–20, and enforce IDE extension allowlists. [[Malware.News via Canadian Cyber Centre](https://malware.news/t/al26-013-security-incident-impacting-github-internal-repositories/107430#post_1)]

- **Signal Users Targeted in Backup-Stealing Phishing Campaign:** Attackers are sending SMS messages impersonating Signal Support, instructing victims to navigate to Settings → Backups and paste their 64-character recovery key into the chat. Obtaining this key enables decryption of full message archives. The campaign appears targeted at journalists, activists, and dissidents — Signal will never request your recovery key by message. [[Malware.News via Malwarebytes](https://malware.news/t/signal-users-targeted-in-backup-stealing-phishing-attacks/107422#post_1)]

- **French Health Payments Processor Breach Exposes National ID Data:** Almerys, a French healthcare payments middleman, suffered a breach of its third-party payment authorization portal, potentially exposing *numéro de sécurité sociale* (French SSN equivalent) and other PII — fueling identity theft and fraud concerns. The company processes "third-party payment" (tiers payant) transactions so patients don't pay upfront. [[Malware.News via DataBreaches.net](https://malware.news/t/french-health-payments-breach-exposed-id-data-fuels-fraud-fears/107420#post_1)]

---

*51 articles ingested from Miniflux Cyber feeds. 7 articles selectively read for this digest. Saturday edition — focused on genuinely new stories. Stale topics omitted per prior digest analysis (May 25–29): Gogs zero-day, Charter/Carnival breaches, SideCopy XenoRAT, GREYVIBE AI campaigns, The Gentlemen ransomware, Samba CVE-2026-4480, OpenVPN macOS vuln, nginx-poolslip PoC — all covered in recent prior digests. Sources include BleepingComputer, Rapid7, Microsoft Security Blog, Wiz Research, Seqrite Labs, Malware.News, GBHackers, Cyber Security News, Canadian Centre for Cyber Security, Malwarebytes, DataBreaches.net.*