---
title: "🚨 Splunk RCE exploited, 🛡️ SocGholish takedown, 🔑 Klue OAuth breach, 🐛 Squidbleed, 💰 Accenture $4.18B OT play, 🎯 Popa botnet"
date: 2026-06-19
tags: ["splunk","fortibleed","socgholish","evil-corp","klue","icarus","popa-botnet","teampcp","squidbleed","nginx","autojack","shapedplugin","accenture","dragos","ransomware","supply-chain","cisa-kev","ot-security","wordpress"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Splunk Enterprise CVE-2026-20253 exploited in attacks — CISA adds to KEV. Operation Endgame takedown of SocGholish botnet cleans 15K WordPress sites. Klue OAuth breach enables Icarus extortion group to steal Salesforce data. Squidbleed (CVE-2026-47729) leaks memory from 29-year-old Squid bug. Accenture enters OT security market with $4.18B Dragos/runZero/NetRise acquisition. Patch Splunk, Squid, and NGINX immediately."
---

# Daily Threat Intelligence Digest — June 19, 2026

*86 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — `reddit_gap_check.py` unavailable (chronic failure threshold exceeded, 20+ consecutive days). External gap detection via web search found no critical gaps beyond feed coverage. tl;dr sec skipped — latest issue from June 11 is 8 days stale. Exa web extract credits exhausted — browser-based extraction used for paywalled content. Prior digests: June 14–18, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Splunk Enterprise CVE-2026-20253 Exploited in Attacks Days After Disclosure — WatchTowr PoC Published, CISA Adds to KEV**

CISA added a critical Splunk Enterprise pre-auth RCE vulnerability (CVE-2026-20253) to its Known Exploited Vulnerabilities catalog on June 18, giving federal agencies three days to patch under BOD 26-04 — the **first Splunk CVE ever added to KEV**. Splunk PSIRT confirmed "limited exploitation" of the flaw, which allows unauthenticated attackers to create or truncate arbitrary files via a PostgreSQL sidecar service endpoint that lacks authentication controls. Two days after Splunk's June 10 advisory, researchers at WatchTowr demonstrated and published a full RCE exploit chain. The bug affects Splunk Enterprise versions 10.2 before 10.2.4 and 10.0 before 10.0.7. Given Splunk's central position in enterprise SOC operations (log ingestion, detection, alerting), successful exploitation provides attackers full access to security telemetry and lateral movement opportunities. [[SecurityWeek](https://www.securityweek.com/splunk-enterprise-vulnerability-exploited-in-attacks-days-after-disclosure/)]

**Recommended action:** Patch immediately if running affected versions. Prioritize as crown-jewel infrastructure — Splunk is both detection platform and attack target.

---

**[UPDATE] FortiBleed — CISA Formally Warns Fortinet Users After 74K Device Credentials Exposed, Most Devices Still Online**

CISA issued a formal warning urging Fortinet customers to secure devices after the "FortiBleed" leak of nearly 74,000 firewall and VPN credentials, confirmed as authentic by Kevin Beaumont and Hudson Rock. The agency called for terminating all SSL VPN and administrative sessions, resetting all passwords, enabling phishing-resistant MFA, and restricting management interfaces from public internet access. The exposed dataset spans 21,632 unique domains across 194 countries, including Samsung, Chevron, Comcast, AT&T, Toyota, and multiple government agencies — a majority of affected devices remain online. The Russian-speaking threat group allegedly conducted ~1.16 billion credential attempts against 320,000+ FortiGate targets. Hudson Rock has published a free domain lookup tool. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-warns-fortinet-users-to-secure-devices-after-fortibleed-leak/)]

**Context:** *Previously covered June 18 (initial disclosure, 73K+ credentials), June 16 (FortiSandbox exploitation). New today: CISA formal warning, confirmed authenticity by independent verification.*

---

**[NEW] SocGholish Botnet Takedown — Operation Endgame Cleans Nearly 15,000 WordPress Sites, 106 Servers Seized**

International law enforcement agencies (FBI, Dutch NHCTU, RCMP, BKA, Europol) cleaned SocGholish malware infections from 14,971 compromised WordPress websites and took down 106 servers and domains linked to the Evil Corp Russian cybercrime group, as part of Operation Endgame. SocGholish (also tracked as FakeUpdates, GhoLoader) has been active since 2017, hijacking legitimate websites to deliver fake browser update lures that deploy Dridex, Doppelpaymer, LockBit, RansomHub, and other ransomware payloads. The Dutch police called this "the beginning of further action against SocGholish." [[BleepingComputer](https://www.bleepingcomputer.com/news/security/law-enforcement-nukes-socgholish-malware-from-nearly-15-000-sites/); [CyberScoop](https://cyberscoop.com/socgholish-malware-botnet-takedown-evilcorp/); [SecurityWeek](https://www.securityweek.com/15000-wordpress-websites-cleaned-up-in-socgholish-botnet-takedown/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Klue OAuth Breach — 'Icarus' Extortion Group Steals Salesforce Data via Stolen OAuth Tokens, Huntress Among Victims**

The relatively new "Icarus" extortion group (active since April 2026) compromised Klue's backend systems, pushed a malicious code update that stole OAuth tokens from customer Salesforce integrations, then used automated Python scripts to query Salesforce REST APIs for data theft over 24 hours. Hallmarks: slow reconnaissance ("a thousand queries in 15-minute window" after mapping valuable objects), then rapid exfiltration. Huntress confirmed they were among the victims, with stolen data including CRM contacts, sales communications, price quotes, and competitive intelligence reports. Salesforce disabled the Klue Battlecards integration platform-wide. Known attacker IPs: 138.226.246.94, 212.86.125.24, 213.111.148.90, 94.154.32.160. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/klue-oauth-breach-linked-to-icarus-salesforce-data-theft-attacks/); [SecurityWeek](https://www.securityweek.com/cybersecurity-firms-impacted-by-klue-supply-chain-attack/)]

**Hunting hypothesis:** Review Salesforce API logs for SOQL queries from unexpected IPs hitting `/services/data/v59.0/sobjects` followed by bursts on `/services/data/v59.0/query`. Revoke and rotate OAuth tokens for any Klue or similar third-party Salesforce integrations.

---

**[NEW] Popa Botnet Traced to Publicly-Traded Israeli Firm Alarum Technologies — Krebs, Synthient, Lumen, Nokia Release Coordinated Research**

A coordinated disclosure by KrebsOnSecurity, Synthient, Qurium, Lumen's Black Lotus Labs, and Nokia Deepfield links the Android-based Popa botnet (1.5–2.5M distinct IPs/day, a plugin of the Vo1d malware targeting cheap streaming TV boxes) to **NetNut**, a residential proxy provider owned by publicly-traded **Alarum Technologies Ltd [NASDAQ: ALAR]**. Synthient's SDK analysis "proves without a shadow of a doubt that Popa actively continues to be used by NetNut as part of their proxy pool." Alarum denies operating the infrastructure, claiming the Popa SDK was sold years ago. Spur found that NetNut does not perform meaningful KYC — anyone can buy proxy access via resellers with "a burner email address and $5 in crypto." Separately, Infoblox found **65% of its customer base queries residential proxy domains**, with 90%+ of pharmaceutical and food & beverage customers affected. [[Krebs on Security](https://krebsonsecurity.com/2026/06/popa-botnet-linked-to-publicly-traded-israeli-firm/); [Malware.News](https://malware.news/t/popa-botnet-linked-to-publicly-traded-israeli-firm/108045#post_1)]

**Context:** 42% of LG webOS apps and 25% of Samsung Tizen smart TV apps contain proxy SDKs that turn users' TVs into residential proxy nodes — often without meaningful consent.

---

**[UPDATE] TeamPCP Supply Chain Spree — CyberScoop Deep-Dive Reveals 1,000+ Packages, 500M Weekly Downloads, Core Operator in South Africa**

CyberScoop's comprehensive investigation into TeamPCP's four-month rampage reveals: **1,000+ packages compromised** across npm and PyPI, affecting ~500M weekly downloads combined. Google Threat Intelligence Group traces the core operator to **South Africa** (residential/mobile IPs). Palo Alto Networks tracks "ResoluteXBF" as the lead handler, with two additional members ("diencracked," "Shinigami"). The group listed ~4,000 private code repositories for sale at $95,000. Victims include Bitwarden, LiteLLM, Checkmarx, SAP, TanStack, Mistral AI, Red Hat. TeamPCP is motivated more by notoriety than money — approximately $90K in extortion proceeds — but has fundamentally eroded trust in open-source registries. The group collaborated with Lapsus$, ShinyHunters, Vect, DragonForce. [[CyberScoop](https://cyberscoop.com/teampcp-breaks-open-source-software-trust-model/)]

---

**[NEW] Gentlemen Ransomware Maintains Suite of EDR Killers — ESET Details 8 GentleKiller Variants Targeting 48 Security Products**

ESET documented **GentleKiller**, a custom EDR-killing tool used by Gentlemen RaaS with at least eight variants, each using different vulnerable drivers (BYOVD technique) to achieve kernel-level privileges and disable defenses from 48 security vendors including Microsoft, CrowdStrike, SentinelOne, Palo Alto, and Sophos. The toolkit also incorporates HexKiller (Warlock gang), ThrottleBlood (MesudaLocker/DragonForce), and HavocKiller. Notably, Gentlemen selects targets based on FortiGate endpoint configuration — a targeting vector made significantly more dangerous by the FortiBleed credential leak. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/gentlemen-ransomware-uses-multiple-edr-killers-to-disable-defenses/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Squidbleed (CVE-2026-47729) — 29-Year-Old Heartbleed-Style Bug Leaks Memory from Every Squid Proxy Version**

Researcher Lam Jun Rong (Calif.io) discovered a heap buffer overread in Squid Proxy's FTP directory listing parser, affecting **every version in its default configuration** — a bug that survived 29 years, thousands of commits, and multiple rewrites. Discovered with AI assistance (Claude Mythos Preview analyzed the code and immediately spotted the null-terminator edge case in a `strchr` call). The vulnerability leaks internal memory — including other users' HTTP requests containing passwords and API keys — through crafted FTP directory listings. The fix is a one-line patch. Mitigation: disable FTP support in Squid (Chrome dropped FTP years ago; most orgs get zero legitimate FTP traffic). Patched in Squid v7.6 (June 8). CVE-2026-47729. [[Calif.io via Malware.News](https://malware.news/t/squidbleed-cve-2026-47729/108051#post_1)]

---

**[NEW] F5 Patches Two Critical NGINX Flaws — CVE-2026-42530 (HTTP/3) and CVE-2026-42055 (Proxy/gRPC) Enable Code Execution**

F5 released out-of-band security updates for multiple NGINX products addressing two critical unauthenticated flaws: **CVE-2026-42530** (ngx_http_v3_module, HTTP/3) and **CVE-2026-42055** (ngx_http_proxy_v2_module/ngx_http_grpc_module) — both enabling DoS or code execution on systems with non-default configurations and ASLR bypassable conditions. Also patches two high-severity NGINX Gateway Fabric flaws (CVE-2026-11311, CVE-2026-50107) allowing authenticated config injection. No in-the-wild exploitation reported, but F5 vulnerabilities have been repeatedly targeted by cybercrime and state groups. Mitigations available for those who can't patch immediately. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/f5-issues-out-of-band-patches-for-critical-nginx-vulnerabilities/)]

---

**[NEW] AutoJack — Microsoft Security Research Demonstrates RCE Chain Against AI Agent Framework AutoGen Studio**

Microsoft Defender Security Research disclosed **AutoJack**, a three-weakness exploit chain against AutoGen Studio (Microsoft Research's open-source multi-agent UI) that allows untrusted web content rendered by a browsing agent to reach a local MCP WebSocket and execute arbitrary commands on the host. The chain: (1) origin allowlist trusts localhost but the agent itself is localhost, (2) auth middleware explicitly opts out MCP WebSocket paths without implementing auth, (3) `StdioServerParams` from the URL is executed verbatim. Microsoft fixed the issue in the upstream main branch. The vulnerable MCP WebSocket surface was never included in a public PyPI release. **Broader lesson:** localhost is no longer a trust boundary when agents browse untrusted content and talk to privileged local services. [[Microsoft Security Blog via Malware.News](https://malware.news/t/autojack-how-a-single-page-can-rce-the-host-running-your-ai-agent/108062#post_1)]

---

## 🛡️ Defense & Detection

**[NEW] ShapedPlugin WordPress Supply Chain Attack — Build Pipeline Compromised, Paid Plugins Backdoored with Credential Theft Malware**

Wordfence disclosed that **three paid ShapedPlugin products** (Product Slider Pro, Real Testimonials Pro, Smart Post Show Pro) were compromised at the build pipeline level. Infected releases delivered a hidden fake plugin impersonating WooCommerce components that steals WordPress credentials, 2FA secrets, database credentials, SMTP creds, and WooCommerce order/payment data (past 3 months). The loader (LicenseLoader.php) activates when an admin accesses the dashboard, contacts C2 for a backdoor, then self-deletes. Free versions on WordPress.org were clean — attackers targeted the vendor's release infrastructure directly. Patches available in versions 3.5.4 (Product Slider Pro), 3.2.6 (Real Testimonials Pro), and 4.0.2 (Smart Post Show Pro). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/shapedplugin-update-flow-hacked-to-infect-wordpress-sites/)]

---

**[NEW] Red Canary Intelligence Insights: June 2026 — ClearFake Dominates, Kali365 PhaaS Debuts at #2, HijackLoader Returns**

Red Canary's June 2026 threat rankings: **ClearFake** (JavaScript drive-by download, ClickFix/fake CAPTCHA) retains #1 for the second month, appearing in 7 of the top 10 threats. **Kali365** (OAuth device code PhaaS platform targeting Microsoft 365) debuts at #2 — a subscription-based platform accessed via Telegram that automates token theft through Cloudflare workers hosting branded login pages. **TeamPCP** re-enters at #6 following the Mini Shai-Hulud campaign. **HijackLoader** (DLL sideloading payload delivery) makes its first top-10 appearance since September 2025. Red Canary recommends blocking device-code auth flow via Conditional Access as the primary defense against Kali365. [[Red Canary](https://redcanary.com/blog/threat-intelligence/intelligence-insights-june-2026/)]

---

## 📋 Policy & Industry News

**[NEW] Accenture's $4.18B OT Cybersecurity Pivot — Acquires Majority Stake in Dragos, All of runZero and NetRise**

Accenture announced the acquisition of a **majority stake in Dragos** ($3.25B), plus Austin-based **runZero** (attack-surface discovery) and **NetRise** (firmware/software supply chain visibility) — totaling $4.18B. The combined entity positions Accenture as a major OT cybersecurity software player, a market estimated at $27B in 2026 and projected to reach $59B by 2031. Dragos CEO Robert M. Lee will continue leading the combined operation. The deal signals a structural shift: OT security is no longer an IT add-on but a standalone market attracting enterprise-scale investment. [[CyberScoop](https://cyberscoop.com/accenture-industrial-cybersecurity-acquisition-dragos-netrise-runzero/); [SecurityWeek](https://www.securityweek.com/accenture-to-acquire-majority-stake-in-dragos-all-of-runzero-netrise-in-4-1-billion-ot-cybersecurity-push/)]

---

## ⚡ Quick Hits

- **Apple patches Beats Studio Buds Bluetooth eavesdropping flaw** — CVE-2025-20701 (and related CVE-2025-20700, CVE-2025-20702) allows attackers in Bluetooth range to hijack earbuds and spy on conversations or initiate calls without authentication. Firmware update 1B211 delivered automatically. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/apple-fixes-beats-studio-buds-flaw-that-let-hackers-spy-on-conversations/)]
- **Avada Builder (1M+ WordPress sites) critical file deletion vuln** — CVE-2026-8713 (CVSS 9.1) enables unauthenticated arbitrary file deletion via form builder privacy cleanup, leading to full site takeover. Patched in version 3.15.4. [[Wordfence via Malware.News](https://malware.news/t/critical-unauthenticated-arbitrary-file-deletion-vulnerability-patched-in-avada-builder-wordpress-plugin/108038#post_1)]
- **Texas government breach** — Hackers stole 3M driver's license numbers and passport records from a Texas state government department. One of the largest state government breaches this year. [[DataBreaches.net via Malware.News](https://malware.news/t/texas-government-data-breach-allowed-hackers-to-steal-3-million-driver-s-licenses-and-passports/108057#post_1)]
- **ShinyHunters claims Amazon-owned One Medical breach** — 8.8TB alleged data theft; group threatens publication unless negotiations begin by June 22. Unverified — no sample data released. [[DataBreaches.net via Malware.News](https://malware.news/t/amazon-owned-one-medical-faces-alleged-8-8tb-data-breach/108061#post_1)]
- **Nintendo confirms data theft via WebMD subsidiary** — Employee survey data stolen from TinyPulse third-party service by Shadowbyt3$ extortion group. Nintendo's systems not compromised. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/nintendo-confirms-data-stolen-in-webmd-subsidiary-cyberattack/)]
- **Prinz Eugen: new Go-based ransomware analyzed** — ThreatDown/Malwarebytes details a Go-based encryptor that prioritizes recently modified files, uses out-of-band extortion, and employs anti-forensic techniques. [[Malwarebytes via Malware.News](https://malware.news/t/prinz-eugen-ransomware-a-deep-dive-into-a-new-go-based-encryptor/108029#post_1)]
- **Incransom ransomware claims two new victims** — Neubrandenburger Wohnungsgesellschaft mbH (German housing association) and Horizon Family Medical Group (US healthcare). [[Malware.News](https://malware.news/t/incransom-targets-neubrandenburger-wohnungsgesellschaft-mbh-in-germany/108056#post_1)]
- **Cisco to acquire WideField Security** — Bolstering Splunk's "Agentic SOC" capabilities with SOAR/automation technology. Terms undisclosed. [[SecurityWeek](https://www.securityweek.com/cisco-to-acquire-widefield-security-to-boost-splunks-agentic-soc/)]
- **FIFA World Cup phishing infrastructure surge** — Silent Push identified 227 domains registered on opening day following Ghost Stadium (Chinese-speaking cybercriminal group) pattern: consistent favicons, naming convention (two/three-letter prefix + "26fifashop.site.top"). [[Silent Push via Malware.News](https://malware.news/t/fifa-world-cup-hunting-227-phishing-domains-with-the-silent-push-mcp-server/108037#post_1)]

---

*86 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — reddit_gap_check.py unavailable (chronic failure threshold exceeded, 20+ consecutive days). External gap detection via web search found no critical gaps beyond feed coverage. Prior digests: June 14–18, 2026. Stale CVE/topic blocklist applied. Sources include BleepingComputer, SecurityWeek, CyberScoop, Krebs on Security, Red Canary, Wordfence, ESET, Microsoft Security Blog, Calif.io, DataBreaches.net, Silent Push, and independent researchers.*
