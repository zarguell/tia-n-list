---
title: "🕵️ Mastra AI Attributed to North Korea, 🦠 Prinz Eugen Ransomware, ⚙️ Sinobi Technical Deep Dive, 📋 ENISA SBOM Report"
date: 2026-06-21
tags: ["Supply Chain Attack","North Korea","Sapphire Sleet","BlueNoroff","Ransomware","Prinz Eugen","Sinobi","Lynx","SBOM","ENISA","CRA"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Microsoft attributes Mastra npm supply chain attack to North Korean Sapphire Sleet targeting 166 crypto wallets. Prinz Eugen ransomware prioritizes recent files with no ransom note. Sinobi technical analysis reveals DeviceIoControl shadow copy destruction. ENISA SBOM adoption report highlights operationalization gap ahead of CRA enforcement."
---

# Daily Threat Intelligence Digest — June 21, 2026

*7 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Mastra AI Supply Chain Attack Attributed to North Korean Sapphire Sleet — Cross-Platform Stealer Targets 166 Crypto Wallets**

Microsoft has formally attributed the June 17 Mastra npm supply chain compromise to **Sapphire Sleet (BlueNoroff)**, a North Korean state-sponsored threat actor specializing in cryptocurrency theft. [[Microsoft](https://www.bleepingcomputer.com/news/security/microsoft-links-mastra-ai-supply-chain-attack-to-north-korean-hackers/)] The attack, initially reported when 141 @mastra packages were backdoored with the typosquatted `easy-day-js` dependency, is now understood to have deployed a **cross-platform information stealer** targeting Windows, Linux, and macOS developer environments.

The second-stage payload collected host info, browser histories, installed applications, and checked for **166 cryptocurrency wallet browser extensions** including MetaMask, Phantom, Coinbase Wallet, Binance Wallet, and TronLink. Microsoft's investigation identified follow-on activity including a PowerShell backdoor previously tied to Sapphire Sleet, Microsoft Defender exclusion additions, and a malicious Windows service granting SYSTEM privileges. [[Sonatype](https://www.sonatype.com/blog/easy-day-js-targets-mastra-dependency-attacks-grow)] The group was also responsible for the April 2026 Axios npm supply chain attack. [[Aikido](https://www.aikido.dev/blog/over-140-popular-mastra-npm-packages-hit-by-supply-chain-attack)]

The consistency of C2 infrastructure, persistence mechanisms, and targeting profile confirms this as an ongoing North Korean crypto-theft campaign rather than a one-off supply chain incident.

---

**[NEW] Prinz Eugen Ransomware Prioritizes Recent Files, Operates Without Ransom Note**

Malwarebytes' Threatdown team has identified a new hands-on-keyboard ransomware operation named **Prinz Eugen** with several unusual characteristics. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-prinz-eugen-ransomware-prioritizes-recent-files-for-encryption/)] Unlike most extortion operations, Prinz Eugen does not operate as RaaS and leaves **no ransom note** on encrypted systems — ransom communications happen entirely out-of-band via email, phone, or dark-web victim portals.

Key findings from the investigation:
- **Initial access**: Stolen RDP credentials, followed by manual payload deployment (`servertool.exe`)
- **RMM abuse**: RemotePC tool used for persistence via backdoor admin account
- **Encryption**: Go-based binary using **ChaCha20-Poly1305** with Argon2id/SHA-256/HKDF-SHA256 key derivation; processes files in 1 MB chunks with SHA-256 integrity verification
- **Targeting prioritization**: Most recently modified files encrypted first; when timestamps tie, alphabetical order — designed to maximize pressure on victims by hitting business-critical data in active use
- **Anti-forensics**: Encryption key overwritten with zeroes, garbage collection forced, then self-deletes from disk

At least **5 victims** identified by researchers, with only 3 currently listed on the leak site. In one incident (Standard Bank), the attacker demanded 1 BTC and was refused.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Sinobi Ransomware (Lynx Rebrand) Technical Deep Dive Reveals Novel Shadow Copy Destruction via DeviceIoControl**

Picus Security published a detailed technical analysis of **Sinobi ransomware**, first observed July 2025 and assessed as a rebrand of Lynx ransomware (active since 2024). [[Picus Security](https://www.picussecurity.com/resource/blog/how-sinobi-ransomware-encrypts-files-and-destroys-backups)] While the strain is not new, the analysis documents several noteworthy implementation details relevant to detection engineering:

- **Initial access**: Affiliates authenticated via **SonicWall SSL VPN** using credentials stolen from an MSP, then pivoted over RDP — the compromised account held domain admin privileges
- **Shadow copy destruction**: Uses `DeviceIoControl` with IOCTL code `0x53C028` (IOCTL_VOLSNAP_SET_MAX_DIFF_AREA_SIZE) with a zero-size buffer, silently discarding all Volume Shadow Copies — avoids the noisy `vssadmin delete shadows` command that EDR tools universally flag
- **Restart Manager API abuse**: Terminates processes holding file handles via legitimate Windows Restart Manager, sparing Explorer and critical processes to keep the desktop responsive for the ransom note
- **Encryption**: Curve-25519 ECDH + AES-128-CTR with per-file keys; partial encryption modes (5%, 15%, 25%) configurable
- **ACL takeover**: Grants Everyone SID GENERIC_ALL rights when write permissions denied; enables `SeTakeOwnershipPrivilege` as fallback

The SonicWall SSL VPN initial access vector mirrors patterns seen in Akira, BlackCat, and other ransomware operations, reinforcing the need for MFA enforcement on VPN appliances and MSP credential hygiene.

---

## 📋 Policy & Industry News

**[NEW] ENISA SBOM Adoption Report — From Best Practice to Regulatory Imperative Under CRA**

ENISA's 2026 "SBOM Adoption State of Play" report concludes that generating Software Bills of Materials is no longer the challenge — **operationalizing them** is the gating problem. [[SOCFortress (ENISA Report Part II)](https://socfortress.medium.com/enisa-sbom-adoption-in-2026-from-security-best-practice-to-regulatory-imperative-part-ii-c36fa696e7ee)] As the EU Cyber Resilience Act moves toward enforcement in December 2027, manufacturers placing digital products on the European market will be required to maintain SBOMs throughout the product lifecycle. The report identifies a widening gap between SBOM generation tooling and the workflows needed to consume SBOM data for active risk reduction — a gap that vulnerability assessment platforms, MSSPs, and enterprise development teams will need to close.

---

## ⚡ Quick Hits

- **Global Schools Group Injunctions Fail to Stop Data Leak** — Global Schools Group obtained court injunctions prohibiting the publication of sensitive student/parent data acquired by threat actor FulcrumSec, but the orders had no practical effect on the leak. [[DataBreaches.net](https://databreaches.net/2026/06/20/global-schools-group-obtained-two-court-injunctions-that-didnt-seem-to-change-much-and-might-backfire/)]
- **AI Vulnerability Discovery Pushing 2026 CVEs Toward 66,000** — FIRST now projects the year will land near 66,000 CVEs, well above initial projections, driven in large part by AI-assisted vulnerability discovery tooling. [[Help Net Security](https://www.helpnetsecurity.com/2026/06/21/week-in-review-74k-fortinet-firewall-credentials-stolen-splunk-enterprise-rce-under-active-attack/)]
