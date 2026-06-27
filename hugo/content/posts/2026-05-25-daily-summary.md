---
title: "Copy Fail LPE CISA KEV, TrapDoor Cross-Ecosystem Supply Chain, Ghost CMS ClickFix, nginx-poolslip PoC, SonicWall Scanning Surge, Underminr CDN Abuse"
date: 2026-05-25
tags: ["CVE-2026-31431", "Copy Fail", "Linux", "supply chain", "TrapDoor", "Ghost CMS", "CVE-2026-26980", "ClickFix", "nginx", "CVE-2026-9256", "poolslip", "SonicWall", "Underminr", "CDN", "Storm-2949", "Azure", "Void Dokkaebi", "InvisibleFerret", "CypherLoc", "Chinese PhaaS", "Kazuar", "Turla"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Copy Fail Linux LPE added to CISA KEV with active exploitation confirmed; TrapDoor cross-ecosystem supply chain campaign hits npm, PyPI, Crates targeting crypto/AI devs; Ghost CMS SQL injection exploited in large-scale ClickFix campaign compromising 700+ domains; nginx-poolslip PoC demonstrates full remote ASLR bypass; SonicWall scanning surge signals imminent vulnerability disclosure; Underminr CDN abuse technique affects 88M+ domains."
---

# Daily Threat Intelligence Digest — May 25, 2026

*36 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[GAP] Copy Fail (CVE-2026-31431) — 100% Reliable Linux LPE Now Added to CISA KEV — Active Exploitation Confirmed**

A deterministic local privilege escalation vulnerability in the Linux kernel's AF_ALG cryptographic interface (algif_aead module) has been added to CISA's Known Exploited Vulnerabilities catalog, confirming active in-the-wild exploitation. Tracked as CVE-2026-31431 and dubbed "Copy Fail," the flaw allows any unprivileged local user to gain root access by writing four controlled bytes to the page cache of any readable file — no race condition, no memory offset guessing, no compilation required.

The 732-byte Python PoC works unmodified across every major Linux distribution shipped since 2017 (kernel 4.14+): Ubuntu 24.04 LTS, Amazon Linux 2023, RHEL 10.1, and SUSE 16 were all demonstrated rooting in a single attempt. The bug originates from a 2017 in-place optimization to algif_aead.c that chained page-cache pages into the writable destination scatterlist; during AEAD decryption, `authencesn` writes 4 bytes past the buffer into the file page cache before failing the authentication check. Because the corruption affects *cached* file pages (not the on-disk copy), it can tamper with setuid-root binaries without altering disk forensics — a reboot clears the evidence.

CISA added the flaw to KEV on May 1 with a May 15 federal remediation deadline. Patches are available in kernels 6.18.22+, 6.19.12+, and 7.0+. For systems that cannot immediately patch: `rmmod algif_aead` and block the module via modprobe config. Rotate all SSH host keys on affected systems as a precaution. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-says-copy-fail-flaw-now-exploited-to-root-linux-systems/); [Palo Alto Unit 42](https://origin-unit42.paloaltonetworks.com/cve-2026-31431-copy-fail/); [Tenable](https://www.tenable.com/blog/copy-fail-cve-2026-31431-frequently-asked-questions-about-linux-kernel-privilege-escalation); [r/cybersecurity](https://www.reddit.com/r/cybersecurity/) — 641↑]

**[NEW] TrapDoor Supply Chain Campaign — 34 Malicious Packages Across npm, PyPI, and Crates.io Target Crypto/AI Developers**

A coordinated supply chain attack first surfaced on May 22 is actively compromising developers across three major package ecosystems. Dubbed "TrapDoor" by Socket Security researchers, the campaign spans 21 npm packages, 7 PyPI packages, and 6 Crates.io packages masquerading as developer utilities, wallet checkers, security auditors, and build helpers — all designed to blend into normal development workflows in crypto, DeFi, Solana, and AI tooling.

Each ecosystem is exploited through its native execution model: npm packages trigger a 1,149-line credential harvester via `postinstall` hooks; PyPI packages auto-execute a remote JavaScript payload on import using `node -e` from the attacker's GitHub Pages domain; Crates.io packages abuse `build.rs` during Rust compilation to XOR-encrypt and exfiltrate local keystores. All 384+ malicious versions and artifacts anchor to the GitHub account `ddjidd564`, which hosts an `AUDIT-Matrix.md` describing the operation as a "Universal AI Agent Extraction Framework."

The most sophisticated technique involves poisoning AI coding assistant configurations: hidden zero-width Unicode characters instruct Cursor and Claude Code to execute "security scans" that silently exfiltrate developer secrets. The attackers also opened malicious PRs against `langchain-ai/langchain`, `langflow-ai/langflow`, `run-llama/llama_index`, and `OpenHands/OpenHands` — each PR attempted to inject attacker-controlled `.cursorrules` or `CLAUDE.md` under innocuous commit messages. [[Cyber Security News](https://cyberpress.org/supply-chain-attack-compromises-34-packages/); [GBHackers](https://gbhackers.com/hackers-compromise-34-npm-pypi-and-crates-packages/)]

**[NEW] Ghost CMS SQL Injection Exploited in Large-Scale ClickFix Campaign — 700+ Domains Including Harvard, Oxford, DuckDuckGo Compromised**

A critical SQL injection vulnerability (CVE-2026-26980) in Ghost CMS is being actively exploited in a large-scale campaign impacting over 700 domains discovered by XLab at Qianxin. The flaw, patched on February 19 in Ghost 6.19.1 but still unpatched on thousands of sites, allows unauthenticated attackers to steal admin API keys and inject malicious JavaScript into published articles.

The attack chain exploits the SQLi to exfiltrate admin API keys, then uses elevated rights to inject a JavaScript loader that fingerprints visitors. Qualifying targets are served a fake Cloudflare prompt via iframe, instructing them to paste a PowerShell command — the ClickFix lure — which drops DLL loaders, JavaScript droppers, or an Electron-based malware sample named `UtilifySetup.exe`. Compromised targets include Harvard University, Oxford University, Auburn University, and DuckDuckGo. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ghost-cms-sql-injection-flaw-exploited-in-large-scale-clickfix-campaign/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Storm-2949 Attack Chain Fully Documented — Azure RBAC Abuse, Key Vault Secrets Exfiltrated in Minutes**

Microsoft Threat Intelligence has published a detailed breakdown of a Storm-2949 campaign targeting Microsoft 365 and Azure environments, moving beyond the earlier SSPR abuse angle covered in the May 20 digest. The attack begins with highly targeted social engineering — impersonating IT support to trick victims into approving fraudulent MFA prompts via Self-Service Password Reset (SSPR). Once authenticated, attackers register their own devices with Microsoft Authenticator for persistent access.

Using custom Python scripts and Microsoft Graph API, the attackers enumerated users, roles, and applications before pivoting to Azure Key Vault. In just **four minutes**, they manipulated access configurations using their privileged "Owner" RBAC role and extracted dozens of critical secrets including database connection strings and identity credentials. The assault expanded across the cloud ecosystem: Azure SQL firewall rules were modified, Azure Storage network configurations opened to attacker-controlled IPs, and SAS tokens used to siphon data directly to attacker devices. Backdoor local admin accounts were created via Azure VM extensions (Run Command, VMAccess), and ScreenConnect was installed for persistent remote access. Known attacker IPs: 176.123.4.44, 91.208.197.87, 185.241.208.243. [[Cyber Security News](https://cyberpress.org/hackers-abuse-azure-rbac/); [GBHackers](https://gbhackers.com/hackers-exploit-azure-rbac/)]

**[NEW] Void Dokkaebi Evolves — InvisibleFerret Malware Now Compiled as Native Binaries via Cython, Chrome Downgraded to Manifest V2**

North Korea-aligned threat actors tracked as Void Dokkaebi (Famous Chollima) are evolving their developer-targeting operations. Trend Micro's TrendAI Research documented a shift in InvisibleFerret delivery: instead of readable Python scripts, the payload is now compiled into `.pyd` files (Windows) and `.so` shared libraries (macOS) using Cython — rendering signature-based detection on plain-text Python malware largely ineffective.

The infection chain begins with fake job interviews at AI and cryptocurrency firms, tricking developers into downloading malicious repositories. A companion Python execution script (`.mod` file) loads the compiled binary with encoded C2 IP addresses passed as command-line arguments. Alongside InvisibleFerret, the BeaverTail JavaScript module handles initial access and data theft — using shuffled Base64 arrays, junk byte insertion, and 4-byte XOR keys to hide C2 infrastructure. A specialized Chrome module downgrades the browser on macOS to a version supporting Manifest V2 extensions, bypassing Google's security enforcement to reach crypto wallet extensions. Brave Browser is also targeted due to its continued Manifest V2 support. [[Cyber Security News](https://cyberpress.org/invisibleferret-uses-compiled-extensions/)]

---

## ⚠️ Vulnerabilities & Patches

**[UPDATE] nginx-poolslip (CVE-2026-9256) — PoC Released with Full Remote ASLR Bypass — CVSS 9.2**

A fully weaponized proof-of-concept has been published for CVE-2026-9256, the heap buffer overflow in NGINX's `ngx_http_rewrite_module` previously flagged by the Canadian Cyber Centre (AV26-501, covered in May 23 digest). The vulnerability, now actively demonstrated against a hardened Linux server running NGINX 1.31.0, goes beyond a conventional DoS: researchers published a multi-stage exploit that performs remote heap probing (~300 crafted HTTP requests), Heap Feng Shui to force predictable memory layout, precise ASLR bypass by leaking active memory offsets, and ultimately interactive root-level shell access.

The flaw (CVSS v4.0: 9.2) is triggered when a `rewrite` directive uses regex patterns with overlapping PCRE capture groups (e.g., `^/((.*))$` paired with `$1$2` in a redirect). Critically, the archived `kubernetes/ingress-nginx` running NGINX 1.27.1 is **permanently vulnerable** to both CVE-2026-9256 and the earlier CVE-2026-42945 (Rift) — it will never receive upstream fixes. Immediate mitigation: replace unnamed PCRE captures with named captures (`(?<name>...)`). [[Cyber Security News](https://cyberpress.org/nginx-poolslip-flaw/); [GBHackers](https://gbhackers.com/nginx-poolslip-flaw-exposes-servers/)]

**[NEW] SonicWall Scanning Surge — 597K Sessions in a Single Day, Same Actor Pattern as Pre-Disclosure Reconnaissance**

GreyNoise has documented a dramatic surge in reconnaissance activity targeting SonicWall SonicOS management interfaces between May 9–18, peaking at approximately **597,000 sessions** on May 12 — 46 times the typical daily baseline and the largest single-day total in 90 days. The scanning infrastructure is operationally identical to the actor that conducted pre-disclosure reconnaissance ahead of CVE-2026-0400 in February 2026: same Chrome 119 on Linux user-agent (94.5% of Q1 traffic, ~99% now), traffic originating from Netherlands (~56%) and Ukraine (~44%), and concentrated through a single ASN (AS211736).

Given the established pre-disclosure scanning pattern (37, 25, and 10 days lead time before CVE-2026-0400), this activity strongly suggests a new SonicOS vulnerability disclosure is imminent. Defenders should immediately restrict SonicOS management interfaces to trusted IP ranges, enforce MFA on every SSL VPN account, audit administrative accounts created since May 1, and block AS211736 traffic at the network edge. [[Cyber Security News](https://cyberpress.org/actively-scan-sonicwall-firewalls/)]

---

## 🛡️ Defense & Detection

**[NEW] Underminr: Shared CDN Infrastructure Abuse Enables Domain Reputation Bypass — 88M Domains at Risk**

Researchers at ADAMnetworks and Rescana have documented a novel technique dubbed "Underminr" that exploits an inherent architectural weakness in shared CDN infrastructure. Rather than a software vulnerability, Underminr abuses the multi-tenant design of CDN platforms — Cloudflare, Akamai, AWS CloudFront, and Fastly — where millions of domains share edge infrastructure.

Attackers register their own domains on the same CDN platforms used by high-reputation services, then manipulate HTTP Host headers or SNI during TLS handshakes to make malicious traffic appear destined for trusted domains. Unlike traditional domain fronting (which relies on Host/SNI mismatch), Underminr leverages native CDN multiplexing behavior, making detection significantly harder. Over 88 million domains may be exposed to this risk. Observed exploitation includes phishing payload delivery, C2 channel establishment, and HTTP/2 multiplexing to interleave malicious and benign traffic. Mitigations require moving beyond domain reputation filtering to deep packet inspection for SNI/Host header consistency validation and behavioral analytics on encrypted traffic patterns. [[GBHackers](https://gbhackers.com/hackers-exploit-shared-cdns/)]

**[NEW] CypherLoc Scareware Campaign — 2.8M Attacks This Year Using Encrypted Browser-Based Payloads**

Barracuda Networks has documented a massive ongoing campaign using the CypherLoc scareware kit — approximately 2.8 million attacks tracked since the beginning of 2026. The campaign represents a significant evolution in scareware: instead of frozen-screen scams or traditional malware installers, CypherLoc operates entirely as a browser-resident framework using AES-encrypted JavaScript payloads gated by URL fragments as decryption keys.

The attack chain begins with phishing emails directing victims to a harmless-looking landing page that decrypts and executes an encrypted payload only when specific URL fragment conditions are met. The technique includes HMAC integrity checks, Base64 decoding, and automatic URL fragment removal from browser history via `history.replaceState()`. Victims are presented with spoofed login forms and fraudulent technical support phone numbers — calling connects them to human operators posing as Microsoft support who complete the financial scam. This encrypted, fragment-gated execution model makes traditional URL-based blocklisting ineffective. [[Cyber Security News](https://cyberpress.org/cypherloc-fuels-support-scams/); [GBHackers](https://gbhackers.com/hackers-use-cypherloc-kit/)]

---

## 📋 Policy & Industry News

**[NEW] Google Threat Intelligence Reports Chinese-Language PhaaS Ecosystem Matures — RCS/iMessage Delivery, Digital Wallet Tokenization, AI Page Generators**

Google Threat Intelligence Group (GTIG) published a comprehensive analysis of a dozen mature PhaaS offerings operating in the Chinese-language underground. Unlike Russian-speaking counterparts, these services operate openly with less operational security — posting luxury lifestyle photos on Telegram — and focus almost exclusively on non-Chinese targets. Key technical developments include: RCS and iMessage delivery (end-to-end encryption prevents carrier-side inspection), real-time OTP interception via live admin panels that let attackers interact with victims during login, exploitation of digital wallet provisioning to tokenize stolen cards for contactless payments, and AI-powered page generators using Puppeteer to clone legitimate site HTML/CSS/JS on demand.

The YY Lai Yu (YY来鱼) platform, first advertised in August 2024, exemplifies the shift: over 400 phishing templates supporting 119 countries with deep localization for Japan (Amazon, Apple, PayPay, Nintendo, JR Rail, and 15+ other Japanese brands). The platform uses human verification anti-bot screens that defeat automated security vendor analysis. Organizations should prioritize FIDO2/WebAuthn deployment — hardware security keys are the only effective countermeasure against real-time OTP interception. [[Malware.News via Google Cloud Blog](https://malware.news/t/2-phaas-2-furious-the-evolution-of-chinese-language-phishing-services/107284); [Google Cloud Blog](https://cloud.google.com/blog/topics/threat-intelligence/chinese-language-phishing-services/)]

---

## ⚡ Quick Hits

- **Kazuar Goes Modular** — Secret Blizzard (Turla/FSB Center 16) has evolved the Kazuar backdoor into a modular spyware framework with Kernel/Bridge/Worker architecture, ~150 configuration options, leadership election, and IPC-based internal communication. One infected system communicates externally at a time, dramatically reducing network noise. [[GBHackers](https://gbhackers.com/kazuar-malware-becomes-modular-spyware/)]
- **France #1 for Violent Crypto Holder Attacks** — A new report finds ~70% of documented "wrench attacks" against cryptocurrency holders occur in France, shifting the threat model from digital compromise to physical coercion. [[Malware.News](https://malware.news/t/france-sees-more-violent-attacks-on-crypto-holders-than-any-other-country/107279)]
- **Unmasking Lawxsz** — Multi-vector OSINT investigation attributes the Valkyrie and Prysmax stealers to Lucas Sa██bria, an Argentinian malware developer operating across BreachForums, Telegram, GitHub, and TikTok. Identity confirmed via breach data, phone number OSINT, and platform cross-referencing. [[Malware.News](https://malware.news/t/unmasking-lawxsz-attributing-the-developer-behind-valkyrie-and-prysmax-stealers/107280)]
- **Telegram Mule-as-a-Service** — KELA research documents organized MaaS operations using deepfake KYC bypass, AI-generated synthetic identities, and Telegram channels selling verified bank/fintech accounts. Latin America emerging as primary hotspot via Brazil's PIX network. [[Cyber Security News](https://cyberpress.org/telegram-markets-verified-accounts/)]
- **Wireshark 4.6.6 Released** — Latest stable release includes bug fixes and protocol updates. [[Malware.News](https://malware.news/t/wireshark-4-6-6-released-sun-may-24th/107281)]

---

*36 articles ingested from Miniflux Cyber feeds, supplemented by Reddit r/cybersecurity cross-referencing (fresh content detected — Copy Fail gap identified). Prior digests: May 20–24, 2026. Sources include BleepingComputer, Palo Alto Unit 42, Tenable, CISA KEV, Trend Micro, Microsoft Threat Intelligence, Socket Security, XLab/Qianxin, GreyNoise, ADAMnetworks, Rescana, Barracuda Networks, Google Threat Intelligence Group, GBHackers, Cyber Security News, Malware.News, KELA, and DataBreaches.net.*
