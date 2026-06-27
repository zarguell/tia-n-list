---
title: "🔴 NGINX Exploitation Active, 🪟 Windows MiniPlasma Zero-Day, 🏢 Grafana Breach Confirmed, 🐧 DirtyDecrypt PoC, 🤖 Claude Code RCE, 🍎 Apple M5 Kernel Exploit"
date: 2026-05-18
tags: ["NGINX","Windows","Grafana","Linux","Claude Code","Apple M5","ransomware","supply chain","DirtyDecrypt","Tycoon2FA","Pwn2Own","Fast16","MiniPlasma","JDownloader","PHP","npm"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Critical: NGINX Rift exploitation confirmed over the weekend with 5.7M exposed servers; Windows MiniPlasma zero-day PoC grants SYSTEM on fully patched Windows 11; DirtyDecrypt PoC adds fourth Dirty Frag-class Linux LPE. Major incidents: Grafana Labs breach via stolen GitHub token (Coinbase Cartel); Tycoon2FA returns with OAuth device-code phishing. Patch priorities: Claude Code RCE (v2.1.118), NGINX rewrite patches, and PHP image-processing memory bugs."
---

# Daily Threat Intelligence Digest — May 18, 2026

*36 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] NGINX Rift (CVE-2026-42945) — Active exploitation confirmed over the weekend, 5.7M exposed servers**

VulnCheck has confirmed active in-the-wild exploitation of CVE-2026-42945 ("NGINX Rift"), the critical heap buffer overflow in NGINX's `ngx_http_rewrite_module` that went undetected for 18 years. Public PoC code was published last week by Depthfirst; over the weekend, VulnCheck detected attacks hitting its canary systems. Censys data shows approximately 5.7M internet-exposed NGINX servers running potentially vulnerable versions, though the exploitable subset requires specific `rewrite` configurations. The heap overflow can achieve RCE when ASLR is disabled, and the public PoC reportedly includes an ASLR bypass mechanism. F5 released patches last week — any deployment using `rewrite` or `set` directives should treat this as an emergency patching priority. [[SecurityWeek](https://www.securityweek.com/exploitation-of-critical-nginx-vulnerability-begins/)]

**[NEW] Windows MiniPlasma zero-day gives SYSTEM on fully patched Windows 11 — PoC released**

Researcher "Chaotic Eclipse" has published a proof-of-concept exploit for a Windows privilege escalation zero-day dubbed MiniPlasma that grants SYSTEM privileges on fully patched Windows 11 systems. The flaw targets the `cldflt.sys` Cloud Filter driver — specifically a routine originally reported by Google Project Zero's James Forshaw in September 2020 (CVE-2020-17103, marked fixed in December 2020). The researcher claims Microsoft never actually patched the issue or the patch was silently rolled back. BleepingComputer confirmed the exploit works on a fully patched Windows 11 system running the latest May 2026 Patch Tuesday updates. This is the latest in Chaotic Eclipse's disclosure spree following BlueHammer, RedSun, YellowKey (BitLocker bypass), and GreenPlasma — several of which were exploited in the wild within days of publication. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/new-windows-miniplasma-zero-day-exploit-gives-system-access-poc-released/)]

**[UPDATE] DirtyDecrypt (CVE-2026-31635) — PoC released for fourth Dirty Frag-class Linux LPE**

A proof-of-concept exploit has been released for DirtyDecrypt (also known as DirtyCBC), a local privilege escalation vulnerability in the Linux kernel's `rxgk` module that allows attackers to gain root access. The flaw belongs to the same page-cache corruption class as Dirty Frag, Fragnesia (both covered in prior digests), and Copy Fail (CISA KEV, May 15 deadline). Exploitation requires `CONFIG_RXGK` enabled, limiting the attack surface to Fedora, Arch Linux, and openSUSE Tumbleweed. CVE-2026-31635 was patched in the mainline kernel on April 25. The same mitigation used for Dirty Frag (module blacklist for `esp4`, `esp6`, `rxrpc`) also protects against DirtyDecrypt, at the cost of breaking IPsec VPNs and AFS. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/exploit-available-for-new-dirtydecrypt-linux-root-escalation-flaw/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Grafana Labs breached via compromised GitHub token — Coinbase Cartel claims source code theft**

Grafana Labs confirmed a breach on May 16 after a threat actor used a stolen token to access its GitHub environment and download the company's entire private codebase. The breach followed a targeted multi-stage attack: the attacker forked a public Grafana repository, injected a malicious `curl` command into the forked code, and exploited a vulnerable `pull_request_target` GitHub Actions workflow to extract a privileged token. The actor then accessed four additional private repositories before deleting the fork. The cybercrime group Coinbase Cartel — assessed as an offshoot of ShinyHunters, Scattered Spider, and LAPSUS$ — claimed responsibility. Grafana refused the ransom demand, publicly disclosing the incident the same day the demand arrived. No customer data or personal information was accessed. [[SecurityWeek](https://www.securityweek.com/grafana-confirms-breach-after-hackers-claim-they-stole-data/); [Cyber Security News](https://cyberpress.org/grafana-breach-exposes-github-codebase/); [GBHackers](https://gbhackers.com/grafana-labs-confirms-security-incident-github-codebase-access/)]

**[UPDATE] Tycoon2FA PhaaS returns with OAuth device-code phishing — Trustifi click-tracking URLs weaponized**

Despite an international takedown operation in March 2026, the Tycoon2FA phishing kit has rebuilt on new infrastructure and now supports OAuth device-code phishing attacks. eSentire TRU documented a campaign using invoice-themed emails with Trustifi click-tracking URLs that redirect through a four-layer delivery chain (Trustifi → Cloudflare Workers → obfuscated JavaScript → fake Microsoft CAPTCHA page). Victims are tricked into entering a Microsoft OAuth device code at `microsoft.com/devicelogin`, granting the attacker persistent OAuth tokens. The kit's blocklist now contains 230 vendor names, with detection evasion for Selenium, Puppeteer, Playwright, Burp Suite, and AI crawlers. Device code phishing has surged 37× this year, supported by at least 10 distinct PhaaS platforms. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/tycoon2fa-hijacks-microsoft-365-accounts-via-device-code-phishing/)]

**[UPDATE] JDownloader website compromised — official installers delivered RAT between May 6-7**

Attackers exploited an unpatched CMS vulnerability in the official JDownloader website to swap legitimate Windows and Linux installers with a Python-based remote access Trojan. The compromise affected the "Download Alternative Installer" (Windows) and primary Linux shell installer links between May 6-7. macOS, JAR, Flatpak, Winget, and Snap packages were unaffected. Legitimate JDownloader installers are signed with a valid digital certificate from "AppWork GmbH" — the weaponized versions lacked this signature. Users who downloaded installers during the window should verify digital signatures and run system scans. [[Cyber Security News](https://cyberpress.org/jdownloader-installers-deliver-malware/)] This was briefly noted in the May 16 Quick Hits with limited detail; this update provides full technical scope.

**[NEW] Termite ransomware claims Ramar Foods International — U.S. food manufacturer threatened**

On May 16, the Termite ransomware group claimed responsibility for an attack against Ramar Foods International, a U.S. Filipino frozen food manufacturer. The group has threatened to leak stolen data unless negotiations are initiated. The incident adds to the ongoing pattern of ransomware groups targeting the food manufacturing sector. [[Malware.News](https://malware.news/t/termite-ransomware-group-strikes-ramar-foods-international/107072#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Claude Code RCE via malicious deeplinks (CVE patched in v2.1.118)**

Security researcher Joernchen of 0day.click disclosed an RCE vulnerability in Anthropic's Claude Code AI coding assistant. The flaw originated in the `eagerParseCliFlag` function, which naively scanned the entire command-line array for any string starting with `--settings=` without considering flag/argument context. An attacker could embed a malicious `--settings=` payload inside a `claude-cli://` deeplink's `q` parameter, registering a `SessionStart` hook to execute arbitrary shell commands. A secondary issue bypassed the workspace trust dialog entirely when the deeplink's `repo` parameter matched a previously trusted repository. Patched in version 2.1.118. Users on earlier versions should update immediately. [[Cyber Security News](https://cyberpress.org/claude-code-rce-vulnerability/); [GBHackers](https://gbhackers.com/claude-code-vulnerability/)]

**[NEW] Apple M5 macOS kernel exploit built in 5 days using Mythos AI — MIE mitigation bypassed**

The Calif research team has built the first public macOS kernel memory-corruption exploit running on Apple M5 silicon, developed in just five days using a combination of human expertise and Anthropic's Mythos Preview AI model. The data-only LPE chains two kernel vulnerabilities to escalate from an unprivileged local account to root shell, bypassing Apple's new Memory Integrity Enforcement (MIE) — the hardware-assisted memory safety system built around ARM MTE. The original bugs were identified by AI (falling within known vulnerability classes), while human expertise guided the novel MIE bypass. The exploit targets macOS 26.4.1 on bare-metal M5 hardware. Calif has withheld the full technical report until Apple ships a patch. [[Cyber Security News](https://cyberpress.org/apple-m5-macos-kernel-exploit-built/); [GBHackers](https://gbhackers.com/apple-m5-macos-kernel-exploit-with-mythos-preview/)]

**[NEW] Malicious npm packages steal SSH keys, cloud credentials, and crypto wallets — Shai-Hulud source code enables copycat campaigns**

Four malicious npm packages were discovered in a typosquatting campaign targeting developers. The packages — `@deadcode09284814/axios-util`, `axois-utils`, `chalk-tempalte`, and `color-style-utils` — deploy varied payloads including an information stealer for AWS/GCP/Azure credentials and SSH keys, a GoLang-based "phantom bot" for DDoS attacks that persists after package removal, and cryptocurrency wallet theft. One package is a direct Shai-Hulud clone, underscoring how TeamPCP's open-sourcing of the worm code has lowered the barrier for supply chain attacks. Combined weekly downloads reached 2,678. Developers should audit recent npm installations and rotate exposed credentials. [[Cyber Security News](https://cyberpress.org/npm-packages-steal-credentials/); [GBHackers](https://gbhackers.com/malicious-npm-packages-2/)]

**[NEW] PawsRunner steganography loader deploys PureLogs infostealer via fake invoice phishing**

FortiGuard Labs documented a sophisticated phishing campaign using a steganography loader called PawsRunner to deploy the PureLogs infostealer. The attack chain: fake invoice email with TXZ archive → hidden JavaScript → fileless .NET loader → PawsRunner executable (notable for cat photo application icons) → downloads PNG image with encrypted payload hidden via steganography → PureLogs data harvesting. The infostealer targets credentials from 80+ browsers, password managers, cryptocurrency wallets, and digital authenticators. The combination of fileless execution, steganography, and rapid data extraction makes this a challenging threat to detect. [[Cyber Security News](https://cyberpress.org/pawsrunner-deploys-purelogs-infostealer/)]

---

## 🛡️ Defense & Detection

**[NEW] Fast16 malware sabotages nuclear test simulations — Stuxnet-class cyberweapon targeting scientific truth**

Symantec has published an analysis of Fast16, a rare cyber-espionage framework designed not to steal data but to corrupt nuclear weapons simulations. The malware uses a selective hook engine that activates only under specific conditions — notably when simulation material density exceeds 30 g/cm³ (the threshold associated with uranium under compression during nuclear implosion). Fast16 manipulates output values in LS-DYNA and AUTODYN physics engines through three tampering mechanisms: reducing calculated values to 10% of true output, gradually lowering stress tensor values to 1%, and scaling pressure outputs down by 8-42%. Up to ten different malware builds were identified, each tailored to specific software versions. Components date back to approximately 2005, potentially predating Stuxnet. The malware uses a kernel-level driver for injection, IFEO hijacking for persistence, and avoids systems with security tools. [[GBHackers](https://gbhackers.com/fast16-malware-sabotages/)]

**[NEW] Linux Torvalds warns AI bug report spam is "unmanageable" — new kernel documentation sets strict rules**

Linus Torvalds has publicly warned that a flood of low-value AI-generated bug reports is overwhelming the private Linux security mailing list. In his Linux 7.1-rc4 announcement, Torvalds stated the AI report volume has made the security list "almost entirely unmanageable," with maintainers spending time on duplicate forwarding and responses to already-fixed issues. Updated kernel documentation authored by Willy Tarreau now explicitly states: bugs found with AI tools "should be treated as public," and AI-assisted submissions must include verified reproducers, concrete impact analysis, and ideally a tested patch. Reports are directed to public bug trackers unless they clearly match strict security criteria. The guidance warns against AI-styled formatting and speculative worst-case claims. [[GBHackers](https://gbhackers.com/ai-bug-report-spam-is-disrupting-linux-security-discussions/)]

**[NEW] Crafted JPEGs trigger PHP memory safety bugs — heap disclosure and buffer overflow in core image functions**

PT Swarm researchers uncovered two memory safety issues in PHP's core `ext/standard` extension: CVE-2025-14177 (CVSS 6.3), a heap memory disclosure in `getimagesize()` when parsing JPEG APP segments with multi-chunk reads, and a heap buffer overflow in `iptcembed()` when handling non-standard files like pipes where `fstat()` reports size as zero. The `iptcembed()` overflow is the more severe of the two, potentially leading to code execution. Both issues have been patched in recent PHP releases. [[GBHackers](https://gbhackers.com/crafted-jpegs-trigger-php-memory/)]

---

## 📋 Policy & Industry News

**[UPDATE] Pwn2Own Berlin 2026 final tally — $1.3M awarded for 47 zero-days, DEVCORE wins with $505K**

The three-day Pwn2Own Berlin 2026 hacking contest at OffensiveCon concluded with researchers earning $1,298,250 for 47 unique zero-day vulnerabilities. DEVCORE Research Team won the competition with 50.5 Master of Pwn points and $505,000 in rewards, highlighted by Orange Tsai's $200,000 Microsoft Exchange RCE chain (3 bugs to SYSTEM) and $175,000 Microsoft Edge sandbox escape. Other significant wins: STARLabs SG ($242,500), IBM X-Force's Valentina Palmiotti ($70,000), and successful exploits against VMware ESXi, Windows 11, Red Hat Enterprise Linux, and multiple AI coding agents including Claude Code and Cursor. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-earn-1-298-250-for-47-zero-days-at-pwn2own-berlin-2026/); [SecurityWeek](https://www.securityweek.com/hackers-earn-1-3-million-at-pwn2own-berlin-2026/)]

**[NEW] Former CISA nominee Sean Plankey named US CEO of drone defense startup UFORCE**

Sean Plankey, former CISA director nominee who withdrew in April amid Senate confirmation difficulties, has been named U.S. CEO of UFORCE, a London-based defense technology company founded by Ukrainians that manufactures combat drones for air, land, and sea. The startup, valued at $1 billion, plans to deploy its first U.S.-made unmanned surface vessels this summer. CISA has remained without a permanent director for the entirety of the second Trump administration. [[CyberScoop](https://cyberscoop.com/former-cisa-nominee-sean-plankey-named-us-ceo-of-defense-startup/)]

---

## ⚡ Quick Hits

- **April 2026 APT trends** — AhnLab's ASEC report documents 15 APT groups active in April, with North Korea-linked groups focusing on developer supply chain attacks (UNC1069 Axios npm tampering, Lazarus fake interviews/ClickFix), China-linked groups targeting cloud infrastructure, and Russia's APT28 exploiting compromised SOHO routers for DNS hijacking. [[ASEC](https://asec.ahnlab.com/en/93744/)]
- **Kimsuky targets South Korea** — Analysis of a Kimsuky-created `.jse` malware sample targeting Cheongdo County in South Korea, involving malicious JavaScript files in a campaign tied to the North Korean APT group. [[Malware.News](https://malware.news/t/kimsuky-x-jse/107071#post_1)]
- **Windows 11 KB5089549 update failure** — Microsoft confirmed the May 2026 Patch Tuesday update fails to install on systems with 10MB or less free space on the EFI System Partition, causing error 0x800f0922. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-confirms-kb5089549-windows-11-security-update-install-issues/)]
- **FunnelKit exploitation still active** — Active campaigns continue targeting the Funnel Builder WordPress plugin (40K+ sites) with payment card skimmers, despite patches released in version 3.15.0.3. IoCs: `analytics-reports[.]com/wss/jquery-lib.js` → `wss://protect-wss[.]com/ws`. [[Cyber Security News](https://cyberpress.org/funnelkit-bug-exposes-stores/)]

---

*36 articles ingested from Miniflux Cyber feeds, supplemented by Reddit r/cybersecurity and TLDR InfoSec cross-referencing. Prior digests: May 13-17, 2026. Sources include SecurityWeek, BleepingComputer, Cyber Security News, GBHackers, CyberScoop, Malware.News, ASEC, eSentire, and FortiGuard Labs.*
