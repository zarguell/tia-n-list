---
title: "Android 0‑day exploited, WebLogic CISA KEV, Instagram AI bot defacement, Dashlane vault theft, TrapDoor supply chain, PHANTOMPULSE blockchain RAT"
date: 2026-06-02
tags: ["android","oracle weblogic","instagram","meta ai","dashlane","supply chain","red hat npm","phantompulse","gamaredon","screening serpens","magento","voip","strongdm","wordpress","linux","cisa kev"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "97 articles ingested. Critical: Android Framework zero-day (CVE-2025-48595) actively exploited — patch Android 14–16 devices immediately. CISA adds Oracle WebLogic CVE-2024-21182 to KEV. Instagram Meta AI exploit escalates — Obama White House, Space Force accounts defaced. Dashlane confirms <20 encrypted vaults downloaded. Major supply chain attacks: TrapDoor (34 packages across npm/PyPI/Crates.io with AI context poisoning) and Red Hat npm Miasma (96 backdoored versions, 309 GitHub repos). PHANTOMPULSE RAT analysis reveals blockchain C2 on Ethereum/Base/Optimism and hardware breakpoint defense evasion. Gamaredon fileless campaign uses NTFS ADS and cloud dead-drops against Ukraine. Screening Serpens deploys 6 new RAT variants with AppDomainManager EDR bypass. HP Poly VoIP phones (CVE-2026-0826), Magento cache plugin (CVE-2026-45247), and StrongDM (CVE-2026-4387) all have critical patches available."
---
# Daily Threat Intelligence Digest — June 2, 2026

*97 articles ingested from Miniflux Cyber feeds. External cross-referencing via Reddit r/cybersecurity detected one secondary gap (CVE-2026-0073 Android ADB bypass — PoC published, patched in same June bulletin). tl;dr sec: skipped — Tuesday publication makes Thursday's issue 5 days stale. Prior digests: May 28–June 1, 2026.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Android Zero-Day (CVE-2025-48595) Actively Exploited — Google's June 2026 Bulletin Patches 30+ Framework CVEs**

Google confirmed active exploitation of CVE-2025-48595, a high-severity integer overflow in the Android Framework component, in its June 1 Android Security Bulletin. The flaw enables **local privilege escalation to SYSTEM level with zero user interaction** — no phishing, no malicious link, no app installation required. Google's bulletin language mirrors the December 2025 disclosure pattern for CVE-2025-48633 and CVE-2025-48572, which were added to CISA KEV within 24 hours.

**Scope:** Android 14, 15, 16, and 16-QPR2 — hundreds of millions of devices. The June bulletin patches 30+ Framework CVEs, 35+ System CVEs, plus Kernel and vendor components. Devices running the 2026-06-05 security patch level are protected. Source code patches will hit AOSP within 48 hours.

**ADB bypass (CVE-2026-0073, cross-reference gap):** Multiple PoCs published for a separate critical authentication bypass in the ADB daemon's TLS certificate verification — `EVP_PKEY_cmp()` type confusion returns `-1` (truthy in C) when an EC/Ed25519 certificate is presented against a stored RSA key, granting unauthorized shell access. Requires Developer Options + wireless debugging enabled with prior USB pairing. Patched in the same June bulletin. [[Cyberpress](https://cyberpress.org/android-0-day-vulnerability-exploited/); [GBHackers](https://gbhackers.com/android-zero-day-vulnerability-actively-exploited/); GitHub PoCs for CVE-2026-0073]

---

**[NEW] CISA Adds Oracle WebLogic CVE-2024-21182 to KEV — Unauthenticated T3/IIOP Exploitation Confirmed**

CISA added CVE-2024-21182 to its Known Exploited Vulnerabilities catalog on June 1, confirming active exploitation of this Oracle WebLogic Server flaw. The vulnerability allows **unauthenticated remote attackers to gain access via the T3 and IIOP protocols** — a classic attack surface for WebLogic that has historically been leveraged by ransomware operators. Federal agencies must remediate by **June 4, 2026** under BOD 22-01. While Oracle patched this in its July 2024 CPU, the KEV addition signals attackers are now scanning for and exploiting unpatched instances at scale. [[GBHackers](https://gbhackers.com/cisa-issues-alert-on-oracle-weblogic-server-flaw/)]

---

**[UPDATE] Instagram Meta AI Bot Exploit Escalates — Obama White House, Space Force Accounts Defaced with Pro-Iranian Content**

What began as premium-handle theft (reported June 1) escalated dramatically over the weekend. The Instagram accounts for the **Obama White House** and the **Chief Master Sergeant of the U.S. Space Force** were defaced with pro-Iranian images and messages after Telegram-distributed instructions showed attackers how to trick Meta's AI support bot into resetting passwords. The exploit required no malware, no phishing link — attackers used a VPN with a local IP, requested a password reset, and told the AI bot to add their email to the target account. Meta pushed an emergency patch over the weekend.

Accounts with **any form of MFA enabled** (including SMS codes) were not affected. The attack highlights the growing risk of AI-assisted support tools handling sensitive account recovery — as Lumen's Black Lotus Labs noted, AI chatbots are "equally eager to help and vulnerable to persuasion" as human support agents. [[Krebs on Security](https://krebsonsecurity.com/2026/06/hackers-used-metas-ai-support-bot-to-seize-instagram-accounts/); [GBHackers](https://gbhackers.com/metas-ai-bot-misused-by-hackers/)]

---

**[NEW] Dashlane Brute-Force Attack — <20 Encrypted Vaults Downloaded via 2FA Bypass**

Dashlane confirmed that attackers successfully brute-forced **numeric 2FA codes** to register unauthorized devices on fewer than 20 personal plan accounts, downloading encrypted vaults. The attack began May 31 and triggered automated account lockouts. Dashlane's Master Password encryption remains intact — the attacker would still need to phish the master password to decrypt vault contents. The incident underscores that numeric TOTP/SMS 2FA codes are susceptible to brute-force in automated attacks. Organizations and users should migrate to passkeys or hardware security keys where available. [[SecurityWeek](https://www.securityweek.com/dashlane-brute-force-attack-leads-to-limited-encrypted-vault-downloads/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/dashlane-password-manager-users-locked-out-by-brute-force-attacks/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] TrapDoor Cross-Ecosystem Supply Chain Campaign — 34 Packages Across npm, PyPI, and Crates.io, AI Context Poisoning Included**

A large-scale supply chain campaign dubbed **TrapDoor** deployed 34 malicious packages across 384 versions spanning npm, PyPI, and Crates.io ecosystems. Targets include cryptocurrency, DeFi, Solana, AI, and security sector developers. The campaign's most sophisticated innovation: **AI context poisoning** — the npm sample injects payloads into `.cursorrules` and `CLAUDE.md` files using zero-width character steganography, forcing AI coding assistants (Cursor, Claude Code) to execute malicious commands during future interactions. The Rust (Crates.io) sample activates at compile time via `build.rs` — the moment a victim opens the project in VS Code or JetBrains. The PyPI sample uses regex-based scanning for SSH keys, AWS credentials, and GitHub tokens with webhook exfiltration. [[Cyberpress](https://cyberpress.org/malicious-packages-steal-credentials/); [GBHackers](https://gbhackers.com/34-malicious-packages-steal-cloud-keys/)]

---

**[UPDATE] Red Hat npm Compromise — Miasma/Shai-Hulud Variant Hits 32 Packages, 309 GitHub Repos Infected**

An attacker compromised a Red Hat employee's GitHub account and pushed malicious commits via GitHub Actions OIDC trusted publishing, backdooring 32 packages under `@redhat-cloud-services` (96 versions, ~117K weekly downloads). The **Miasma** malware variant shares code with TeamPCP's Mini Shai-Hulud — stealing GitHub Actions secrets, AWS/GCP/Azure credentials, HashiCorp Vault tokens, Kubernetes SA tokens, npm/PyPI publishing tokens, SSH keys, and more. OX Security confirmed 309 compromised GitHub repositories. Red Hat stated no customer or production environments were impacted. All affected packages were removed from npm. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/red-hat-npm-packages-compromised-to-steal-developer-credentials/)]

---

**[NEW] PHANTOMPULSE RAT — Elastic Reveals North Korean RAT with Blockchain C2, Hardware Breakpoint Defense Evasion**

Elastic Security Labs published new technical analysis of **PHANTOMPULSE**, the final-stage RAT in the REF6598 intrusion set (delivered via malicious Obsidian plugins). Attribution: North Korean clusters including BlueNoroff. Key capabilities:

- **Blockchain C2:** Queries Ethereum, Base, and Optimism ledgers via Blockscout providers to find a wallet address, reads the latest transaction input, and decrypts the active C2 URL. **Defensive sinkhole opportunity** — the malware does not verify who sent the transaction, so defenders can submit a crafted transaction to redirect all implants to a controlled server.
- **Hardware breakpoint defense evasion:** Disables AMSI, Windows Lockdown Policy (WLDP), and Event Tracing for Windows (ETW) by setting hardware breakpoints on security function entries rather than patching memory — evading signature-based memory scanners.
- **"schuac" UAC bypass:** Abuses COM interfaces to spawn elevated processes without triggering user prompts.
- **AI-assisted development artifacts:** Binary contains structured step numbering (`[STEP 1] Staged mode`) and verbose debug strings consistent with LLM-generated code.
- **Three process injection techniques:** Module stomping, manual DLL mapping, and debug-driven execution (`DbgNexum`) for shellcode, DLL, and EXE payloads respectively.

Hunt for the unique `0x580c0x580c` hex signature in blockchain transaction data to identify active C2 infrastructure. [[GBHackers](https://gbhackers.com/phantompulse-rat-uses-uac/); [Cyberpress](https://cyberpress.org/phantompulse-rat-bypasses-uac/)]

---

**[NEW] Gamaredon APT Launches Fileless Campaign Against Ukraine — GammaWorm Uses NTFS ADS, Cloud Dead-Drop C2**

Sekoia.io published a reconstruction of an active Gamaredon (FSB-linked) campaign targeting Ukrainian government, military, and critical infrastructure. The infection chain is nearly entirely fileless:

- Initial access via weaponized XHTML using **CVE-2025-8088** (WinRAR path traversal, patched in 7.13) to extract a hidden HTA to Windows Startup
- **GammaPhish** stage delivers **GammaLoad** modular loader via Supabase cloud infrastructure with fake BBC authentication prefix
- **GammaWorm** (20,000+ lines obfuscated VBScript) stores modules in **NTFS Alternate Data Streams** — invisible to standard directory listings — and uses Telegram, Telegra.ph, Teletype.in, and Cloudflare Workers as dead-drop resolvers for C2
- **GammaSteel** PowerShell stealer encrypts 71 modules in Windows registry via DPAPI, exfiltrates to S3-compatible storage

Sekoio recommends full system wipe as remediation due to Gamaredon's rapid malware iteration and DDR-based persistence. [[Cyberpress](https://cyberpress.org/gamaredon-apt-hides-malware/)]

---

**[NEW] Iran's Screening Serpens Deploys 6 New RAT Variants with AppDomainManager EDR Bypass**

Unit 42 documented Screening Serpens (UNC1549 / Smoke Sandstorm) deploying six new RAT variants between mid-February and April 2026 — two families (MiniUpdate and MiniJunk V2) — across coordinated campaigns targeting the U.S., Israel, UAE, and Middle East entities. The technical evolution: **AppDomainManager hijacking** places a malicious .NET configuration file that substitutes a custom AppDomainManager implementation, disabling ETW and bypassing strong-name validation before the host application fully launches — making it invisible to EDR tools that rely on post-initialization telemetry. 19+ Azure-hosted C2 domains and OnlyOffice document-sharing platforms used for payload delivery. [[Cyberpress](https://cyberpress.org/iranian-appdomainmanager-evasion/); [GBHackers](https://gbhackers.com/iranian-hackers-hijack-appdomainmanager/)]

---

**[NEW] Chollima (DPRK) Abuses Packagist — Blockchain Dead-Drop Loader Targets PHP Developers**

Socket researchers discovered obfuscated JavaScript appended to `tailwind.js` in the dev branch of the legitimate Laravel package `roberts/leads`. The loader uses a **blockchain dead-drop design**: queries TRON account transactions for a pointer, falls back to Aptos, then retrieves encrypted content from a BNB Smart Chain transaction. Decrypts and executes first-stage payload in-process, with optional hidden Node.js child process for second-stage payloads. Infra and XOR patterns match prior DPRK-linked campaigns (DEV#POPPER, OmniStealer, BeaverTail). The malicious version was removed by Packagist's security team. [[Cyberpress](https://cyberpress.org/chollima-targets-php-developers/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] CVE-2026-0826 (CVSS 9.2) — HP Poly VVX/Trio VoIP Phones — Unauthenticated Stack Buffer Overflow, Metasploit Module Published**

Rapid7 disclosed a critical unauthenticated stack buffer overflow in HP Poly VVX (150/250/350/450) and Trio (8300/8500/8800) VoIP phones during SDP ICE candidate attribute parsing. A remote attacker can achieve **root-level RCE** requiring only one crafted SIP INVITE request. Requires ICE feature enabled (non-default). CVSS 4.0 score of 9.2. ASLR is broken on these devices — shared libraries load at fixed addresses across reboots. Patched firmware available: VVX UCS 6.4.8, Trio UCS 7.2.8/8.1.7. HP recommends disabling ICE where not required. [[Rapid7](https://www.rapid7.com/blog/post/ve-cve-2026-0826-critical-unauthenticated-stack-buffer-overflow-hp-poly-vvx-trio-voip-phones-fixed)]

---

**[NEW] CVE-2026-45247 (CVSS 9.8) — Mirasvit Magento Cache Plugin — Unauthenticated PHP Object Injection RCE**

A critical unauthenticated RCE in Mirasvit Full Page Cache Warmer — one of the most popular Magento/Adobe Commerce cache extensions — carries a CVSS 9.8 score. The `CacheWarmer` cookie value is passed directly to PHP's `unserialize()` with no authentication gate, enabling classic PHP Object Injection. Any internet-facing storefront page is an attack vector. Sansec estimates **6,000+ vulnerable stores** (likely far higher behind CDNs). Patched in version 1.11.12. Cookie pattern `CacheWarmer:(Tz|Qz|YT)` indicates exploitation attempts. [[Cyberpress](https://cyberpress.org/critical-magento-cache-plugin-flaw/); [GBHackers](https://gbhackers.com/magento-cache-plugin-vulnerability/)]

---

**[NEW] CVE-2026-4387 — StrongDM Windows Desktop — Plaintext Session Tokens Enable Full Infrastructure Hijack**

SpecterOps disclosed that StrongDM's Windows desktop application stored authentication material (JWT + asymmetric key pair) in plaintext at `C:\Users\<username>\.sdm\state.kv`, protected only by default NTFS permissions. Any local attacker can exfiltrate the file to an external host and **replay a fully authenticated session** — gaining access to all databases, servers, and cloud infrastructure the victim can reach. The attack worked across entirely different hosts. Patched in Desktop 23.74.0 and CLI 53.77.0 (March 17) using Windows DPAPI and macOS Keychain. If you haven't updated since March, your session tokens may still be recoverable. [[Cyberpress](https://cyberpress.org/critical-strongdm-vulnerability/); [GBHackers](https://gbhackers.com/critical-strongdm-flaw-exposes-users/)]

---

## 🛡️ Defense & Detection

**[NEW] WordPress Steam Profile C2 — 1,980 Sites Infected, Payloads Hidden in Invisible Unicode Characters**

GoDaddy security engineers documented a long-running campaign (since July 2025) infecting ~1,980 WordPress sites with malware that uses **Steam Community profile comments** as C2 infrastructure. The threat actor encodes payloads using six invisible Unicode characters (zero-width joiners, invisible separators) hidden inside benign-looking Steam comments. The decoder maps invisible characters to binary, reconstructing a URL to `hello-mywordl[.]info` that serves malicious JavaScript. A backdoor responds to `POST` requests containing a specific authentication cookie (`tEcaKKXEsb`). Defenders should check for outbound connections to Steam from WordPress servers and inspect `_transient_caption_` cache entries. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/wordpress-malware-campaign-hides-payloads-in-steam-profiles/)]

---

**[NEW] Fake BlueWallet on Macs — Clipboard-Hijacking Crypto Stealer Targets 80+ Wallets**

A fake `update-bluewallet[.]com` site delivers an AppleScript that downloads a multi-stage infostealer targeting 80+ cryptocurrency wallets, browser credentials, password managers (1Password, Bitwarden, Dashlane), Telegram/Discord sessions, SSH keys, and cloud configs. The malware **hooks the clipboard** and silently swaps Bitcoin/Ethereum/Solana addresses using regex matching + `pbcopy`. Exfiltrates data via Telegram Bot API in 49MB chunks. Persists via LaunchAgent. The entire infection depends on the victim pressing Run in Script Editor — macOS's notarization gate is bypassed because the user is manually executing the script. [[Malwarebytes](https://www.malwarebytes.com/blog/threat-intel/2026/06/fake-bluewallet-steals-passwords-accounts-and-crypto-from-macs) via Malware.News]

---

## 📋 Policy & Industry News

**[UPDATE] Iran-Linked Wiper Attacks Target US Transit, Israeli, Saudi, and Turkish Orgs — MOIS-Affiliated "Ababil of Minab"**

Gambit Security published a deep-dive on a destructive campaign attributed to Iran's Ministry of Intelligence and Security (MOIS), traced through a pro-Iranian persona "Ababil of Minab." Targets include LA Metro (data exfiltration + system wipe), plus organizations in Israel, Saudi Arabia, and Turkey. Attackers combine data theft with **layered destruction**: scripted VM/storage deletion, manual database removal, and backup metadata wiping — systematically breaking every recovery path. Gambit recovered bespoke exfiltration tooling and identified additional undisclosed victims. [[Cyberpress](https://cyberpress.org/iran-hackers-wipe-systems/)]

---

## ⚡ Quick Hits

- **Critical Plesk XPath Injection (CVE-2026-44962):** Low-privileged users can escalate to command execution via APS Application Catalog search. Patched in Plesk 18.0.76.2 / 18.0.75.1 (February 2026). Temporary mitigation: disable APS in `panel.ini`. [[GBHackers](https://gbhackers.com/critical-plesk-vulnerability/)]
- **TP-Link Archer Command Injection (CVE-2026-5509, CVSS 8.5):** Authenticated injection in Archer BE450 v1 and BE7200 v1 via web management interface. Not sold in U.S. (Japan market). Fix: firmware 1.3.0 Build 20260416. [[Cyberpress](https://cyberpress.org/tp-link-router-vulnerability/)]
- **SVG Phishing Wave:** SANS ISC reports a surge in malicious SVG attachment-based phishing emails — SVG's web-friendly vector format is being abused to deliver embedded malicious content. [[SANS ISC](https://malware.news/t/new-wave-of-phishing-emails-with-svg-files-tue-jun-2nd/107501#post_1)]
- **AsyncRAT/DCRat Surge:** ANY.RUN's weekly tracker shows AsyncRAT leading with 824 uploads (+293 WoW), with DCRat and other RAT families also spiking. [[Cyberpress](https://cyberpress.org/stealer-malware-asyncrat-dcrat/)]
- **Spain Arrests Government Data Leaker:** Spanish National Police arrested an individual for leaking sensitive data from INCIBE, the State Attorney General's Office, National Police, and Civil Guard — posing national security risks. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/spain-arrests-doxer-leaking-sensitive-data-of-govt-employees/)]
- **RedSun Windows Defender LPE (CVE-2026-41091):** Continued coverage of the Nightmare Eclipse zero-day exploiting Windows Defender's remediation workflow for local privilege escalation — part of the broader researcher-Microsoft disclosure dispute. [[Malware.News](https://malware.news/t/redsun-exploiting-windows-defenders-remediation-workflow-for-local-privilege-escalation/107483#post_1)]

---

*97 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit r/cybersecurity detected one secondary gap: CVE-2026-0073 Android ADB bypass (PoC published; patched in same June bulletin — included as sub-item in Android coverage). tl;dr sec: skipped — Tuesday run makes Thursday's issue 5+ days stale. Prior digests: May 28–June 1, 2026. Sources include BleepingComputer, GBHackers, Cyber Security News, SecurityWeek, Krebs on Security, Rapid7, Elastic Security Labs, Sekoia.io, Unit 42 (Palo Alto Networks), GoDaddy, SpecterOps, SANS ISC, Cisco Talos, Malwarebytes, Malware.News, and independent researchers.*
