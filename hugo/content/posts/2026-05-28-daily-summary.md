---
title: "🔴 FortiClient zero-day exploited ⚠️ Apache httpd pre-auth RCE 🎯 ClearFake blockchain C2 🇨🇮 CISA LiteSpeed KEV 🛡️ Notepad++ RCE ⚡ Roundcube SQLi"
date: 2026-05-28
tags: ["FortiClient","CVE-2026-35616","Apache","CVE-2026-23918","ClearFake","LiteSpeed","CVE-2026-48172","Notepad++","Roundcube","BadHost","CVE-2026-48710","EKZ","Silent Ransom","Kali365","Glassworm","SpaceBears"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "FortiClient EMS zero-day exploited to deliver EKZ infostealer via fake patches; Apache httpd pre-auth RCE PoC published (CVSS 8.8); CISA adds LiteSpeed cPanel to KEV with May 29 deadline. Also: ClearFake adopts immutable blockchain C2, Notepad++ emergency patch, and Roundcube pre-auth SQLi."
---

# Daily Threat Intelligence Digest — May 28, 2026

*82 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] FortiClient EMS Zero-Day (CVE-2026-35616) Exploited to Deliver EKZ Infostealer via Fake Patches — Unauthenticated RCE Across Managed Fleets**

Arctic Wolf Labs has observed active exploitation of a critical improper access control vulnerability in **FortiClient Endpoint Management Server (EMS)**, tracked as CVE-2026-35616, allowing unauthenticated attackers to bypass API authentication and issue privileged administrative requests — effectively turning the management server into a remote code execution platform for every managed endpoint.

Attackers send specially crafted HTTP requests to exposed EMS instances (port 8013). Despite missing valid certificates or credentials, the server processes them as legitimate administrative actions — producing a consistent EMS log entry: *"Certificate not found in request header"* followed within seconds by a fabricated Fortinet fabric device identity. Threat actors then modify Remote Access Profile configurations and endpoint policies, inserting a malicious script that executes automatically via FortiClient's `on_connect` VPN tunnel behavior.

Within seconds of an endpoint establishing an IPsec tunnel, `fortitray.exe` launches a `.cmd` script executing base64‑encoded PowerShell that downloads **FortiEndpoint_Patch.exe** from `83.138.53[.]110` — a previously unreported infostealer Arctic Wolf named **EKZ**. The malware harvests Chromium and Firefox browser credentials (passwords, cookies, autofill data including credit cards) by leveraging Chromium's `IElevator::DecryptData` interface and dynamically loading Firefox NSS libraries. Collected data is stored in a local SQLite database and exfiltrated via HTTP POST.

Multiple samples of trojanized installers were also recovered from the same server, indicating active tooling development. Organisations should immediately upgrade FortiClient EMS, restrict port 8013 to trusted IPs, and hunt for Tor‑sourced logins, anomalous EMS log entries, and outbound HTTP to 83.138.53[.]110. [[GBHackers](https://gbhackers.com/forticlient-code-execution-flaw/); [Malware.News](https://malware.news/t/forticlient-ems-exploited-via-cve-2026-35616-to-deliver-ekz-infostealer-disguised-as-a-fortinet-patch/107373#post_1)]

---

**[UPDATE] CISA Adds LiteSpeed cPanel Plugin CVE-2026-48172 (CVSS 10.0) to KEV — Active Exploitation Confirmed, May 29 Federal Deadline**

CISA has formally added CVE-2026-48172 to its Known Exploited Vulnerabilities catalog, confirming active in‑the‑wild exploitation. First reported as a zero‑day on May 23 (covered in prior digest), the flaw allows any authenticated cPanel user to execute arbitrary scripts as root via the `lsws.redisAble` JSON‑API endpoint — no race condition, no authentication bypass needed. CISA's Binding Operational Directive 22‑01 mandates remediation by **May 29, 2026** (tomorrow) for federal agencies. The attack surface remains massive: cPanel powers millions of shared‑hosting servers globally. Detection: `grep -rE "cpanel_jsonapi_func=redisAble" /var/cpanel/logs /usr/local/cpanel/logs/` — any output means the host is compromised. [[GBHackers](https://gbhackers.com/cisa-warns-litespeed-cpanel-plugin-vulnerability-is-being-exploited-in-attacks/); May 23 prior digest]

---

**[GAP] Apache HTTP Server CVE-2026-23918 — Pre-Auth Double-Free in mod_http2 Enables DoS and RCE (CVSS 8.8) — PoC Published**

A critical double‑free memory corruption vulnerability in Apache HTTP Server's mod_http2 module (CVE-2026-23918, CVSS 8.8) affects version **2.4.66** running multi‑threaded MPM (event/worker) configurations — the default for most deployments. The attack requires only **one TCP connection and two HTTP/2 frames**: a HEADERS frame immediately followed by RST_STREAM on the same stream before the multiplexer registers it. Two nghttp2 callbacks push the same pointer onto a cleanup array twice; when freed, the second free operates on already‑freed memory.

On all deployments, exploitation guarantees **denial of service** — crashing worker processes with zero authentication. On **Debian‑derived systems** (including Ubuntu, Kali, and the official Apache Docker image), where APR uses the mmap allocator, independent researchers at Striga.ai and ISEC.pl have confirmed a **working remote code execution chain**. The exploit leverages Apache's scoreboard — a shared‑memory region mapped at a fixed address even with ASLR enabled — as a stable container to place fake structs, then tricks the cleanup path into calling `system()` with attacker‑controlled arguments.

**No complete interim mitigation exists short of disabling HTTP/2** (`Protocols h2 h2c`). Upgrade to Apache 2.4.67 (released May 5, 2026) is the only fix. MPM prefork configurations are not affected. The PoC is available at [striga-ai/CVE-2026-23918](https://github.com/striga-ai/CVE-2026-23918). [[Apache Advisory](https://httpd.apache.org/security/vulnerabilities_24.html); [ProbablyPwned](https://www.probablypwned.com/article/apache-http2-cve-2026-23918-double-free-dos-rce); [Lyrie Research](https://lyrie.ai/research/research/cve-2026-23918-apache-http2-double-free-rce)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] ClearFake Adopts BSC Testnet Smart Contracts for Immutable C2 — First Blockchain‑Based Command Channel Immune to Takedown**

The ClearFake campaign has pioneered a novel command‑and‑control architecture by storing malicious payload instructions directly inside **BNB Smart Chain (BSC) testnet smart contracts**, replacing traditional C2 servers with immutable blockchain storage. Unlike conventional campaigns dependent on hosting providers or registrars, this approach embeds malicious JavaScript within a decentralized ledger replicated across thousands of nodes — data that cannot be altered, removed, or seized.

The attack chain begins with a compromised website injecting a base64‑encoded JavaScript loader that queries a BSC smart contract via standard JSON‑RPC `eth_call`, retrieving the next‑stage payload directly from on‑chain storage — bypassing all URL‑based detection. TrendAI Research identified **four smart contracts** linked to a single deployer wallet, active since at least May 2025 with continuous updates through May 2026. A fourth contract acts as an **execution tracker**, recording successful infections (identified by public IP) and preventing reinfection.

Victims passing anti‑analysis checks are served ClickFix overlays: Windows users see a fake Google reCAPTCHA, macOS users a terminal‑based lure. The campaign delivers **SectopRAT** (.NET RAT for browser session hijacking) and **ACRStealer** (C++ infostealer for browser credentials, crypto wallets, VPN configs) simultaneously. Payloads execute filelessly or via DLL sideloading on Windows; macOS uses `curl`‑based download chains.

This marks a significant shift: blockchain‑based C2 that cannot be sinkholed or disrupted. Defenders must now rely on behavioral detection and endpoint monitoring rather than infrastructure takedown. [[GBHackers](https://gbhackers.com/clearfake-abuses-bsc-testnet/); [Cyber Security News](https://cyberpress.org/clearfake-abuses-blockchain-c2/)]

---

**[UPDATE] Silent Ransom Group FBI PSA — In‑Person Data Theft at Law Firms Confirmed, 100+ Attacks Since 2022**

The FBI issued a formal public service announcement (May 27, 2026) detailing the **Silent Ransom Group (SRG)** — a Russia‑based extortion operation emerging from the Conti disbandment in 2022 — which has claimed 100+ attacks with a surge in recent months. The group's TTP is unique in the cybercrime ecosystem: they impersonate internal IT support via phone and phishing, and if remote access fails, **physically send associates to victims' locations** to attach storage devices directly to workstations.

Law firms are the primary target — 134 ransomware incidents against the legal sector in Q1 2026 alone (Halcyon), making it the fourth‑most targeted industry. SRG does not deploy encryption; instead, stolen sensitive legal data creates privilege and reputational leverage for extortion. Experts at Recorded Future and Flashpoint note the group likely uses unwitting gig‑economy workers for physical visits, similar to delivery‑service contractors. Mitigations: enforce FIDO2 hardware MFA, implement help‑desk caller verification, and conduct vishing‑specific user training. [[CyberScoop](https://cyberscoop.com/fbi-warning-silent-ransom-group-law-firms/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-warns-of-silent-ransom-group-in-person-data-theft-attacks/); prior coverage: May 27]

---

**[NEW] Pirates in the Crosshairs — 40M Monthly Pirate Site Visitors Infected with SilentCryptoMiner Since 2022**

A long‑running cybercrime campaign distributing cryptocurrency miners via pirate content websites has been infecting users of illegal movie, TV show, and book streaming/download sites. Researchers from an unnamed IR firm discovered the campaign in April 2026 and traced its origins to at least **2022**, affecting sites with a combined monthly traffic of **~40 million visits**.

The infection chain uses fake video player plugin update prompts: when a user attempts to play content, the site displays a message claiming the plugin is outdated. Clicking downloads a ZIP archive containing a legitimate executable and a malicious DLL. The DLL uses a ROP‑chain‑based stack overflow to decrypt its payload and reflectively load a modified fork of **SilentCryptoMiner**.

The malware deploys a sophisticated multi‑component architecture: a **RAT agent** (injected into `conhost.exe`) with four remote commands, a **watchdog** (in `explorer.exe`) ensuring miner persistence via integrity checking every 5 seconds, and both CPU (XMRig‑based) and GPU miners. The miners use **DNS tunneling** disguised as `microsoft.com` traffic for C2 communication and **MurmurHash64‑based domain generation** that rotates weekly. Anti‑analysis measures include VM detection, Windows Defender exclusion configuration, MSRT deletion via `ZwSetInformationFile`, and disabling hibernation for maximum runtime. [[Malware.News](https://malware.news/t/pirates-in-the-crosshairs-how-one-cybercrime-gang-has-been-infecting-book-movie-and-tv-show-fans-for-years/107385#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical Notepad++ Vulnerabilities (CVE-2026-48778, CVE-2026-48800) — config.xml and shortcuts.xml Enable Arbitrary Code Execution**

Notepad++ released emergency patch v8.9.6.1 on May 26, 2026, addressing three security flaws, two of which enable arbitrary code execution without elevated privileges. **CVE-2026-48778** exploits the `<GUIConfig name="commandLineInterpreter">` tag in `config.xml` — when a user triggers *File → Open Containing Folder → cmd*, Notepad++ passes this tag's value directly to `ShellExecute()` with zero allowlist validation. An attacker can substitute any executable (e.g., `calc.exe`) by writing to `%APPDATA%\Notepad++\config.xml`. **CVE-2026-48800** exploits the same pattern via `shortcuts.xml`.

Attack vectors include: direct config file write (same‑user privilege), malicious `.lnk` files using `-settingsDir=` to redirect to attacker‑controlled configuration, cloud sync path poisoning, and social engineering via malicious archives. Any user on version 8.9.6 or earlier is affected. [[Cyber Security News](https://cyberpress.org/notepad-vulnerability/)]

---

**[NEW] Roundcube Pre‑Auth SQL Injection — 8 Vulnerabilities Patched, Critical SQLi in virtuser_query Plugin**

Roundcube Webmail released security updates 1.6.16 and 1.7.1 on May 24, 2026, resolving **eight distinct vulnerabilities** including a critical **pre‑authentication SQL injection** in the `virtuser_query` plugin. The SQLi originates from a `preg_replace` backslash escape bypass, enabling arbitrary SQL commands without any login credentials. No valid credentials are required to trigger the flaw, dramatically widening the attack surface.

Additional patched vulnerabilities include: stored XSS in draft restore dialogs, CSS injection via SVG `<animate>` in the HTML sanitizer, SSRF bypass via crafted local address URLs, resource fetch bypass, remote image blocking bypass via CSS `var()`, pre‑auth arbitrary file deletion via Redis/Memcache session poisoning, and code injection through unsafe LDAP `autovalues` option evaluation. Multiple bugs can be chained into multi‑stage attack scenarios. All Roundcube installations running 1.6.x or 1.7.x should upgrade immediately. [[Cyber Security News](https://cyberpress.org/roundcube-flaw-inject-sql-queries/); [GBHackers](https://gbhackers.com/roundcube-webmail-vulnerability-execute-malicious-sql-queries/)]

---

**[NEW] BadHost (CVE-2026-48710) — Starlette Host Header Injection Bypasses Authentication, Affecting FastAPI, vLLM, and MCP AI Servers**

A critical vulnerability in **Starlette** (the Python ASGI framework powering FastAPI, vLLM, LiteLLM, and countless AI agent frameworks) allows complete authentication bypass using a single malformed HTTP Host header. Tracked as CVE-2026-48710 and discovered by X41 D‑Sec during an OSTIF‑sponsored audit, the flaw affects all Starlette versions from 0.8.3 to 1.0.1 — a framework with ~325 million weekly downloads.

Starlette reconstructs URLs using `{scheme}://{host_header}{path}` without validating the Host header against RFC 9112 §3.2. An attacker injecting path‑altering characters (`/`, `?`, `#`) into the Host header causes Starlette's routing engine and middleware to see different paths — enabling authentication bypass, SSRF, and in confirmed cases, remote code execution. Impacted ecosystems include **vLLM and LiteLLM inference servers**, **MCP (Model Context Protocol) servers** for AI agent orchestration, and any FastAPI application using path‑based middleware. Fixed in Starlette 1.0.1 (May 21, 2026). Mitigations: upgrade Starlette, replace `request.url.path` with `request.scope["path"]` in middleware, deploy nginx to reject malformed Host headers. [[Cyber Security News](https://cyberpress.org/badhost-exploit-exposes-sensitive-ai/); [GBHackers](https://gbhackers.com/badhost-vulnerability-exposes-sensitive-ai-agent-server/)]

---

## 🛡️ Defense & Detection

**[NEW] GPU Mining Malware Spreads via SEO Poisoning and AI Chatbot Recommendations — Microsoft Documents 6‑Persistence Campaign**

Microsoft researchers documented an ongoing cryptojacking campaign targeting systems with high‑performance GPUs through a coordinated SEO poisoning operation that has also manipulated **AI chatbot recommendations**. Victims searching for utility software (CrystalDiskInfo, HWMonitor, Display Driver Uninstaller, FurMark, K‑Lite Codec Pack, PDFgear) encounter malicious download pages boosted in search rankings. Some users reported being directed to attacker‑controlled domains within AI assistant responses.

The infection uses a legitimate executable + malicious DLL from `gleeze[.]com` subdomains. The DLL installs **ScreenConnect** for persistent remote access, then deploys `SimpleRunPE.exe` — a process hollowing tool targeting Microsoft‑signed binaries (InstallUtil.exe, RegAsm.exe, MSBuild.exe) — establishing **six persistence mechanisms** across Windows autostart locations. The malware excludes itself from Microsoft Defender, checks for VMs and 40 analysis‑tool processes, then deploys GPU miners (gminer, lolMiner, SRBMiner‑MULTI). Microsoft notes the monetization strategy is "engineered to maximize GPU mining yield per compromised device" rather than focusing on volume. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/gpu-mining-malware-spreads-via-seo-poisoning-ai-chatbots/)]

---

**[NEW] Kali365 PhaaS — FBI Warns of OAuth Token Theft Campaign Bypassing MFA via Device Code Flow**

The FBI has issued a public service announcement about **Kali365**, a phishing‑as‑a‑service platform that enables even low‑skilled attackers to hijack Microsoft 365 accounts by stealing OAuth access tokens — completely bypassing multi‑factor authentication. Victims receive phishing messages (document‑sharing notifications, Teams invites) containing a short device code and instructions to enter it at a legitimate Microsoft device sign‑in URL. Once the victim approves, the attacker's device receives valid OAuth tokens, maintaining persistent access to Outlook, OneDrive, Teams, and SharePoint without repeated logins.

This technique abuses Microsoft's **OAuth device authorization grant flow** — the victim never types a password into a fake page, making it exceptionally difficult to detect. Attackers with valid tokens can read password‑reset emails, exfiltrate files, and send phishing emails from the victim's account. Defenders should migrate to FIDO2/WebAuthn hardware keys as the only complete mitigation against token theft, implement conditional access policies restricting device‑code flows, and educate users to never enter a device code they did not initiate. [[Malware.News](https://malware.news/t/kali365-phishing-kit-bypasses-mfa-and-steals-microsoft-logins/107353#post_1)]

---

## 📋 Policy & Industry News

**[NEW] Unit 42: The Evolving Cyber Extortion Economy — Encryption‑Free Extortion Rising, TGR-CRI-1135 Partners with LAPSUS$ and Vect Ransomware**

Palo Alto Networks Unit 42 published a comprehensive analysis of the shifting cyber extortion landscape. Key findings: the percentage of extortion incidents using encryption dropped to **78% in 2025**, down from near‑90% levels (2021–2024), as threat actors increasingly rely on data theft alone. Average cost of data‑theft extortion: **$5.08 million** (over $10M for broader U.S. breaches). Regulation‑driven compliance deadlines (SEC 4‑day, GDPR 72‑hour) are being weaponized by attackers to force rapid negotiations before organisations can complete internal assessments.

Notable developments: **TGR-CRI-1135 (TeamPCP)** — the group behind the Shai‑Hulud open‑source supply chain compromise framework — is now partnering with **LAPSUS$ Group** for extortion operations and **Vect ransomware** operators. Unit 42 warns of an approximate **3‑5 month window** before frontier AI models are weaponized by threat actors to accelerate attacks, with AI‑assisted intrusions already showing time‑to‑exfiltration as low as **25 minutes**. Mid‑sized organisations accounted for 64% of data‑only extortion victims, with Construction witnessing a 44% YoY increase as a data‑only extortion hotspot. [[Unit 42](https://unit42.paloaltonetworks.com/cyber-extortion-economy/)]

---

**[NEW] Glassworm Botnet Disrupted — CrowdStrike, Google, and Shadowserver Simultaneously Takedown 4‑Layer C2 Infrastructure**

The **Glassworm botnet**, which has been targeting software developers since early 2025 to poison open‑source supply chains (VSCode extensions, npm, PyPI, 300+ GitHub repos), was disrupted in a coordinated operation by CrowdStrike, Google, and the Shadowserver Foundation. The operation simultaneously severed access to four distinct C2 channels designed for resilience: **Solana blockchain** transactions, **BitTorrent DHT** peer‑to‑peer network, **Google Calendar** API, and traditional VPS infrastructure.

The Russia‑linked threat group behind Glassworm infected Windows, macOS, and Linux systems with credential theft malware and the GlasswormRAT remote access tool. CrowdStrike's Adam Meyers: "This forces the adversary to rebuild, while exposing tradecraft." The takedown demonstrates how infrastructure disruption can be effective where judicial processes are unavailable. [[CyberScoop](https://cyberscoop.com/crowdstrike-glassworm-botnet-takedown/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/glassworm-botnet-disrupted-after-resilient-c2-infrastructure-takedown/); prior Quick Hits: May 27]

---

## ⚡ Quick Hits

- **SpaceBears Ransomware Targets Ridge Law Firm + Swiss Skincare** — The group claimed 1.6TB of sensitive legal data from a Bronx personal injury law firm (May 27) and separately hit Swiss skincare innovator Filabé. [[Malware.News](https://malware.news/t/spacebears-strikes-ridge-law-firm/107381#post_1); [Malware.News](https://malware.news/t/spacebears-ransomware-attack-targets-swiss-skincare-innovator-filabe/107380#post_1)]
- **AI‑Generated npm Malware Backfires — Threat Actor's Own GitHub Token Hardcoded in Script** — OX Security discovered `mouse5212-super-formatter`, an npm package using AI‑generated code to exfiltrate victim files to GitHub via the Contents API — but the attacker hardcoded their own GitHub personal access token in the script, exposing their identity. The account was created hours before the first malicious upload and conducted 7 test exfiltration runs before deletion. [[Cyber Security News](https://cyberpress.org/ai-npm-malware-backfires/)]
- **Motorola Smart Feed App Caught Hijacking Amazon App Launches for Affiliate Revenue** — A preinstalled system app on Motorola smartphones was intercepting Amazon app launches to inject affiliate referral codes without user consent, effectively skimming commissions. Disabled after public backlash. [[Cyber Security News](https://cyberpress.org/preinstalled-motorola-app-hijacks-amazon/)]
- **RVTools Masquerade — Signed Fake Installer Deploys Modular Python RAT** — A signed fake installer posing as the legitimate RVTools VMware administration utility delivered a modular Python remote access trojan. The signed binary evades initial trust checks. [[Malware.News](https://malware.news/t/rvtools-masquerade-how-a-signed-fake-installer-deploys-a-modular-python-rat/107384#post_1)]
- **UK Visa Portal Leaked Thousands of Passport Copies and Selfies — Still Unfixed** — A misconfigured UK government visa application portal exposed thousands of applicants' passport scans and biometric selfies to the open internet. The vulnerability remains unpatched. [[Malware.News](https://malware.news/t/uk-visa-portal-spilled-thousands-of-applicants-passports-and-selfies-online-and-hasn-t-fixed-the-leak/107357#post_1)]
- **Malware Seller "Venom" Extradited to France** — A known malware seller operating under the pseudonym "Venom" has been extradited to France to face charges. [[Malware.News](https://malware.news/t/malware-seller-known-as-venom-extradited-to-france/107355#post_1)]
- **Lithuania Investigates Theft of 600,000 State Registry Records** — A data breach at Lithuanian state registries compromised approximately 600,000 records. Investigation ongoing. [[Malware.News](https://malware.news/t/lithuania-investigates-theft-of-600-000-state-registry-records/107356#post_1)]
