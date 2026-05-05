---
title: "🔴 Copy Fail Exploited, 🏛️ AiTM Phishing 35K Users, 📦 PyTorch Backdoored, 🌐 Apache RCE, 💰 Everest Hits TSYS"
date: 2026-05-05
tags: ["CVE-2026-31431","Copy Fail","CVE-2026-22679","Weaver","AiTM","phishing","PyTorch Lightning","supply chain","CVE-2026-23918","Apache","CVE-2026-0073","Android","Everest","TSYS","DigiCert","Amazon SES","Edge","CVE-2026-23863","WhatsApp","ransomware","ShaiWorm"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA confirms active exploitation of the Copy Fail Linux kernel vulnerability as it enters the KEV catalog. A sophisticated Microsoft-documented AiTM phishing campaign targeted 35,000 users across 13,000 organizations, while the PyTorch Lightning supply chain attack deployed the ShaiWorm credential stealer to millions of developers. Organizations should immediately patch Copy Fail, Apache HTTP Server, and Android devices, and rotate credentials if PyTorch Lightning 2.6.3 was used."
---
# Tia N. List — Daily Threat Intelligence Digest
### May 5, 2026

**72 articles ingested from Miniflux Cyber feeds across the past 24 hours.**

*Previous 5 days reporting summary:* Yesterday's digest covered cPanel CVE-2026-41940 reaching 40,000+ compromised servers with CISA KEV listing, Instructure breach confirmed at 275M records by ShinyHunters, DigiCert Defender false positive, Microsoft Teams phishing at 72% success rate, FEMITBOT Telegram Mini App fraud platform, FreeBSD DHCP RCE, MOVEit Automation auth bypass, and SAP npm supply chain self-replication. Earlier this week: cPanel "Sorry" ransomware, ConsentFix v3 OAuth automation, Everest ransomware targeting Symcor, cPanelSniper PoC, Copy Fail KEV listing, Cordial/Snarky Spider AiTM, AccountDumpling Facebook phishing, MacSync stealer, SHADOW-EARTH-053 ShadowPad, and the Trellix source code breach.


## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Copy Fail (CVE-2026-31431) — CISA adds to KEV with active in-the-wild exploitation as researchers warn of AI-generated PoC noise**

CISA has confirmed that threat actors are actively exploiting the Copy Fail Linux kernel privilege escalation vulnerability in the wild, adding CVE-2026-31431 to its Known Exploited Vulnerabilities catalog with a two-week remediation deadline for federal agencies (May 15). The announcement comes just one day after Theori researchers disclosed the flaw alongside a proof-of-concept exploit. CyberScoop reports the discovery has exposed tensions in vulnerability disclosure practices: Theori's AI-powered platform (Xint) found the bug, and the company leaned heavily on AI-generated content for its public disclosure, drawing criticism from other researchers who described the blog post as "AI slop" that obscured the legitimate technical severity. VulnCheck's Caitlin Condon noted that hundreds of copycat PoC exploits have surfaced since disclosure, most of which are "AI-generated artifacts that do nothing but add banners or different colors to the CLI." The underlying vulnerability remains severe — any local user can gain root on any Linux kernel built since 2017, and it serves as a container escape primitive. Mitigation remains: disable the `algif_aead` module. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-says-copy-fail-flaw-now-exploited-to-root-linux-systems/); [CyberScoop](https://cyberscoop.com/copy-fail-linux-vulnerability-artificial-intelligence/)]

**[NEW] Weaver E-cology critical RCE (CVE-2026-22679) actively exploited since March via exposed debug API endpoint**

A critical unauthenticated remote code execution vulnerability in Weaver E-cology, a widely-used Chinese enterprise office automation platform, has been actively exploited in the wild since mid-March — just five days after the vendor released a patch and two weeks before public disclosure. Tracked as CVE-2026-22679, the flaw stems from an exposed debug API endpoint in E-cology 10.0 that passes user-supplied parameters directly to backend RPC functionality without authentication or input validation, effectively creating a remote command execution interface. Vega threat intelligence researchers documented a multi-phase attack campaign: threat actors first validated RCE via ping commands to callback servers, then attempted PowerShell payload downloads (blocked by endpoint defenses) and a target-aware MSI installer (which failed to execute). They subsequently pivoted to fileless obfuscated PowerShell for remote script retrieval. Despite having RCE access, the attackers never established persistent sessions on targeted hosts. The vendor's fix (build 20260312) removes the debug endpoint entirely — no workarounds exist, making patching the only mitigation. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/weaver-e-cology-critical-bug-exploited-in-attacks-since-march/)]


## 🎯 Threat Actor Activity & Campaigns

**[NEW] Microsoft documents large-scale "code of conduct" phishing campaign — 35,000 users across 13,000 organizations hit with multi-stage AiTM attack**

Microsoft Defender Research has disclosed a sophisticated adversary-in-the-middle phishing campaign that targeted over 35,000 users across more than 13,000 organizations in 26 countries between April 14-16, with 92% of targets in the United States. The campaign used code-of-conduct-themed lures — emails with subject lines like "Internal case log issued under conduct policy" — that created urgency through accusations and time-bound action prompts. The multi-stage attack chain included PDF attachments directing victims through a series of intermediate pages (Cloudflare CAPTCHA, "encrypted materials" staging page, platform-aware redirect) before delivering them to an AiTM proxy that captured authentication tokens during a Microsoft sign-in flow, bypassing non-phishing-resistant MFA entirely. Healthcare (19%), financial services (18%), and professional services (11%) were the most targeted sectors. Microsoft recommends enabling phishing-resistant MFA (FIDO keys), network protection with SmartScreen, and Zero-hour auto purge. Full IOCs including sender domains and PDF hashes are available in the Microsoft advisory. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/04/breaking-the-code-multi-stage-code-of-conduct-phishing-campaign-leads-to-aitm-token-compromise/)]

**[NEW] Everest ransomware claims attack on TSYS — second major financial sector target in three days**

The Everest ransomware group has claimed responsibility for a cyberattack against TSYS (Total System Services), one of the largest payment processing companies in the United States. The group has threatened to publish stolen data unless TSYS initiates negotiations through their leak site channels. TSYS processes payment cards for thousands of financial institutions and is a critical node in the U.S. payment infrastructure. This claim follows Everest's May 3 attack claim against Canadian financial processor Symcor, suggesting a deliberate targeting pattern against financial services firms. TSYS has not yet confirmed the breach. [[Malware.News/DeXpose](https://malware.news/t/everest-ransomware-hits-payment-giant-tsys/106662#post_1)]

**[NEW] Amazon SES abuse surge — automated credential theft and authenticated phishing at scale**

Threat actors are systematically exploiting exposed AWS IAM access keys to hijack Amazon Simple Email Service for large-scale phishing campaigns that bypass all email authentication checks. Kaspersky reports an uptick in attacks where bots built on the open-source TruffleHog utility automatically scan GitHub repositories, .env files, Docker images, and S3 buckets for exposed AWS credentials. After validating key permissions and email sending limits, attackers distribute convincing phishing emails — including fabricated DocuSign notifications and full BEC email thread impersonations — that pass SPF, DKIM, and DMARC validation because they originate from legitimate Amazon infrastructure. Blocking the delivery IPs is impractical as it would disrupt all SES traffic. Organizations should audit AWS IAM permissions for least-privilege access, rotate keys regularly, enable MFA, and apply IP-based restrictions to SES. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/amazon-ses-increasingly-abused-in-phishing-to-evade-detection/); [Cyber Security News](https://cyberpress.org/attackers-abuse-amazon-ses/)]


## ⚠️ Vulnerabilities & Patches

**[NEW] PyTorch Lightning backdoored on PyPI — "ShaiWorm" credential stealer deployed via version 2.6.3**

A supply chain attack on the PyTorch Lightning package (11 million+ monthly downloads) has been disclosed after version 2.6.3 published to PyPI included a hidden execution chain that silently downloads the Bun JavaScript runtime and executes an 11.4 MB obfuscated payload ("router_runtime.js") on import. Microsoft Defender detects the payload as "ShaiWorm" — a credential stealer targeting .env files, API keys, GitHub tokens, browser data (Chrome, Firefox, Brave), and cloud service credentials (AWS, Azure, GCP). The malware naming and attack pattern closely mirror the Mini Shai-Hulud SAP npm supply chain attack from April 29, suggesting a possible shared operator or toolkit. Microsoft reports the attack affected "a small number of devices" and was "contained to a narrow set of environments." The package has been reverted to the safe version 2.6.1 on PyPI. Anyone who ran `import lightning` with version 2.6.3 must immediately rotate all secrets and credentials. The compromise vector for the build/release pipeline remains under investigation. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/backdoored-pytorch-lightning-package-drops-credential-stealer/)]

**[NEW] Apache HTTP Server critical double-free RCE (CVE-2026-23918) — patch to 2.4.67 immediately**

The Apache Software Foundation has released version 2.4.67 to address a critical double-free memory corruption vulnerability in the HTTP/2 implementation of Apache HTTP Server 2.4.66. CVE-2026-23918 is triggered by a specially crafted "early reset" HTTP/2 frame that causes the server to free the same memory block twice, potentially enabling remote code execution. At minimum, exploitation causes denial-of-service via crash. The vulnerability was responsibly disclosed on December 10, 2025, but the patch took five months to reach public release. Given Apache's massive global deployment footprint, organizations should upgrade immediately or temporarily disable HTTP/2 as a mitigation. [[Cyber Security News](https://cyberpress.org/critical-apache-http-server-vulnerability-2/)]

**[NEW] Android zero-click RCE (CVE-2026-0073) grants remote shell access via adbd**

Google's May 2026 Android Security Bulletin includes CVE-2026-0073, a critical zero-click remote code execution vulnerability in the Android System component linked to the Android Debug Bridge daemon (adbd) through Project Mainline. The flaw allows attackers within proximity (same network or adjacent communication channels) to gain shell-level access without any user interaction, affecting Android versions 14, 15, 16, and 16 QPR2. While shell access does not provide full root, it exposes sensitive system functions and enables staging of further attacks. Devices running the 2026-05-01 security patch level or later are protected. Organizations managing Android fleets should prioritize patch deployment immediately. [[Cyber Security News](https://cyberpress.org/android-zero-click-vulnerability/)]

**[NEW] WhatsApp patches file spoofing (CVE-2026-23863) and arbitrary URL scheme (CVE-2026-23866) vulnerabilities**

Meta has patched two medium-severity WhatsApp vulnerabilities disclosed through its bug bounty program. CVE-2026-23863 affects WhatsApp for Windows and allows attackers to create documents with embedded NUL bytes that appear as harmless files to recipients but execute as programs when opened. CVE-2026-23866 affects WhatsApp for iOS and Android, exploiting incomplete validation of AI rich response messages for Instagram Reels to trigger processing of media from arbitrary URLs, including custom URL scheme handlers (`facetime:`, `tel:`, `itms-apps:`). While neither vulnerability has evidence of in-the-wild exploitation, the URL scheme flaw could enable phishing redirection. Users should update WhatsApp to the latest version. [[SecurityWeek](https://www.securityweek.com/whatsapp-discloses-file-spoofing-arbitrary-url-scheme-vulnerabilities/)]


## 🛡️ Defense & Detection

**[NEW] Microsoft Edge stores all saved passwords in cleartext memory at startup — by design**

Security researcher @L1v1ng0ffTh3L4N has disclosed that Microsoft Edge decrypts and loads every saved password into process memory as cleartext the moment the browser launches — unlike Chrome, which decrypts credentials on demand using App-Bound Encryption. This behavior creates a significant risk in shared computing environments: a proof-of-concept tool demonstrates that a compromised admin account on a terminal server can extract plaintext credentials from all users running Edge, including those with disconnected sessions. Microsoft has confirmed this is "by design," despite Edge requiring re-authentication to view passwords in its UI — creating a false sense of security. Organizations using terminal services or shared workstations should migrate to dedicated password managers that decrypt on demand. [[GBHackers](https://gbhackers.com/microsoft-edge-found-storing-saved-passwords/)]

**[UPDATE] DigiCert breach — full attack chain revealed: malicious screensaver bypassed CrowdStrike after five attempts**

New technical details have emerged on the DigiCert breach first reported yesterday. The April 2026 attack began with a social engineering campaign targeting DigiCert customer support via Salesforce chat, where an attacker posing as a customer sent a ZIP file containing a malicious .scr (screensaver) executable. DigiCert's defenses blocked four delivery attempts before a support analyst executed the fifth. Critically, a malfunctioning CrowdStrike Falcon sensor on the infected endpoint prevented detection during initial analysis, allowing the attacker to move laterally into internal support systems. The attacker accessed EV code signing certificate initialization codes through the support portal's proxy feature, ultimately obtaining 60 fraudulent certificates across four CAs under the names of Lenovo, Kingston, Shuttle, and Palit. At least 27 certificates were used to sign Zhong Stealer malware. DigiCert revoked all 60 certificates within 24 hours of identifying the breach on April 17 and has since removed initialization code visibility from support tools, suspended affected accounts, disabled Okta FastPass, and restricted file types in support chat. [[Cyber Security News](https://cyberpress.org/hackers-use-malicious-screensaver-file/); [SecurityWeek](https://www.securityweek.com/digicert-revokes-certificates-after-support-portal-hack/)]


## 📋 Policy & Industry News

**[NEW] Medicare portal database inadvertently exposed health providers' Social Security numbers**

The Centers for Medicare and Medicaid Services (CMS) created a provider directory database to help seniors look up which doctors accept Medicare, but the database inadvertently exposed the Social Security numbers of health care providers. The exposure was discovered by The Washington Post. This represents the second major government data exposure this month following the DigiCert-related certificate trust disruption, highlighting ongoing challenges in government data handling practices. [[Malware.News/DataBreaches](https://malware.news/t/medicare-portal-database-exposed-health-providers-social-security-numbers/106658#post_1)]

**[NEW] Latvian national sentenced to 102 months for role in Russian ransomware organization**

Deniss Zolotarjovs, 35, of Moscow, Russia, has been sentenced to 102 months (8.5 years) in federal prison for his participation in a major Russian ransomware organization that stole from and extorted over 54 companies. The organization was led by former leaders of the Conti ransomware group and also operated Karakurt, a data extortion group. This follows last week's sentencing of two American ransomware negotiators to four years each for conducting their own ALPHV/BlackCat attacks. [[Malware.News/DataBreaches](https://malware.news/t/latvian-national-involved-with-karakurt-and-other-ransomware-gangs-sentenced-for-his-role-in-ransomware-organization/106659#post_1)]

---

*72 articles ingested from Miniflux Cyber feeds. Prior digest: May 4, 2026. Sources include BleepingComputer, Microsoft Security Blog, SecurityWeek, CyberScoop, GBHackers, Cyber Security News, and Malware.News/DeXpose.*
