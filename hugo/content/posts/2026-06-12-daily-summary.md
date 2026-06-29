---
title: "🚨 Ivanti CVE-2026-10520 KEV, 🔴 Oracle PeopleSoft ShinyHunters, 💰 AudiA6 Dismantled, 🪟 GreatXML BitLocker Bypass, 🤖 LangGraph RCE Chain, 🇰🇷 Coupang $409M Fine"
date: 2026-06-12
tags: ["Ivanti","CVE-2026-10520","CISA KEV","BOD 26-04","Oracle PeopleSoft","CVE-2026-35273","ShinyHunters","AudiA6","crypto laundering","GreatXML","BitLocker bypass","Nightmare Eclipse","LangGraph","CVE-2025-67644","CVE-2026-28277","Coupang","data breach fine","AuditA6 takedown","Tchap","OnyxC2","OnionDrop","CVE-2026-0257","criminal AI","UNC1151","Subjugation","Maine breach portal"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA adds Ivanti Sentry CVE-2026-10520 to KEV under first BOD 26-04 3-day deadline; Oracle releases PeopleSoft mitigations as Mandiant confirms ShinyHunters targeting 100+ orgs; AudiA6 crypto laundering service dismantled in 11-country operation; GreatXML becomes 8th Nightmare Eclipse zero-day targeting BitLocker; LangGraph checkpointer RCE chain disclosed; Coupang hit with record $409M fine in South Korea. Patch Ivanti Sentry immediately, apply Oracle PeopleSoft mitigations, audit OIDC trust policies."
---

# Daily Threat Intelligence Digest — June 12, 2026

*60 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Ivanti Sentry CVE-2026-10520 (CVSS 10.0) — CISA KEV, First Vulnerability Subject to BOD 26-04's 3-Day Deadline, Most Exposed Instances Likely Compromised**

CISA added the actively exploited Ivanti Sentry OS command injection to its KEV catalog on Thursday and ordered federal agencies to patch within three days under the newly issued BOD 26-04 — making CVE-2026-10520 the **first vulnerability** subject to the new risk-based directive. Shadowserver reports "a large amount of exploitation attempts based on the public PoC" and warns that systems not already patched are "most likely compromised." Only ~50 Sentry admin portals remain detectable; many more are likely blocklisted from public scanning. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-gives-feds-3-days-to-patch-ivanti-flaw-exploited-in-attacks/); [Shadowserver](https://twitter.com/Shadowserver/status/1543123456)]

**Prior context (June 10–11):** Ivanti patched CVE-2026-10520 alongside an auth bypass (CVE-2026-10523, CVSS 9.9) on Tuesday. Attackers began backdooring exposed instances within 24 hours. The combined exploit chain gives unauthenticated root RCE + admin account creation. Ivanti still has not updated its advisory to acknowledge active exploitation.

---

**[UPDATE] Oracle PeopleSoft CVE-2026-35273 (CVSS 9.8) — Mitigations Released, Mandiant/GTIG Confirm ShinyHunters Targeting 100+ Organizations, Primarily Higher Education**

Oracle published an out-of-band security alert for a critical unauthenticated RCE in PeopleSoft PeopleTools (versions 8.61, 8.62) — the same zero-day exploited by ShinyHunters (UNC6240) since late May. Mandiant and Google Threat Intelligence Group confirmed the exploitation window spans May 27 through June 9, 2026, and have notified over 100 organizations, 68% of which are in US higher education. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/oracle-mitigates-peoplesoft-zero-day-exploited-in-data-theft-attacks/); [SecurityWeek](https://www.securityweek.com/google-confirms-exploitation-of-oracle-peoplesoft-zero-day-by-shinyhunters/); [Mandiant/GTIG via HelpNetSecurity](https://www.helpnetsecurity.com/2026/06/11/oracle-peoplesoft-under-attack-cve-2026-35273/)]

**New technical details from Mandiant:**
- **Entry vector:** Exploitation of `/PSEMHUB/` endpoints
- **Staging:** MeshCentral v1.1.59 agents on IPs 142.11.200[.]186–190, masquerading as Azure services via domain `azurenetfiles[.]net`
- **Lateral movement:** Custom bash script (`[victim]_fanout.sh`) using stolen/hardcoded credentials
- **Exfiltration:** Data compressed with `zstd`, sent via SSH to 176.120.22[.]24 (ShinyHunters DLS)
- **Extortion:** `README-IF-YOU-SEE-THIS-YOUVE-BEEN-HACKED.TXT` dropped in WebLogic directories

**Action:** Oracle has released **mitigations only** (patch pending). Disable PSEMHUB service or block external access to `/PSEMHUB/*` and `/PSIGW/HttpListeningConnector`. Perform forensic review of PeopleSoft/WebLogic directories for webshells, unauthorized XML files, and the IOCs above. **University IT teams should treat this as emergency priority.**

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] AudiA6 Crypto Laundering Service Dismantled — $380 Million Ransomware Pipeline Cut in 11-Country Operation**

Law enforcement from 11 countries, coordinated by Europol and Eurojust, dismantled "AudiA6" — an industrial-scale cryptocurrency laundering service that acted as a central money laundering hub for ransomware groups between 2022 and 2025. The service was linked to 15+ international ransomware investigations and laundered over $380 million via thousands of fraudulent exchange accounts opened with stolen identities, charging 3–10% commission with ~1-hour turnaround. [[BleepingComputer](https://www.bleepingcomputer.com/news/legal/authorities-dismantle-audia6-ransomware-crypto-laundering-service/); [Malware.News](https://malware.news/t/ransomware-gangs-cut-off-from-eur-336-million-audia6-crypto-laundering-pipeline/107787#post_1); [Europol](https://www.europol.europa.eu/media-press/newsroom/news/audia6-cryptocurrency-laundering-service-dismantled)]

**Takedown results:** 2 administrators arrested in Georgia (Ruslan Tkachuk, 37, Ukrainian; Alexander Ledenev, 25, Russian), 25 domains seized, 80 vehicles/properties seized, ~$900K in cryptocurrency frozen, 6,000 KYC money mule records recovered. Both suspects are also administrators of the Dark2Web underground forum. The US DoJ unsealed charges, with sentences up to 20 years.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] GreatXML: Eighth Nightmare Eclipse Zero-Day — Turns Defender Offline Scan Into BitLocker Backdoor, No Patch Available**

Just one day after publishing RoguePlanet, the researcher operating as MSNightmare/Nightmare Eclipse (now "Chaotic Eclipse") released **GreatXML** — a BitLocker bypass that exploits the Windows Recovery Environment state left behind after Microsoft Defender Offline Scan runs on a system. The exploit uses a planted `unattend.xml` plus a modified `Recovery` directory at the root of the recovery partition. Any subsequent reboot into WinRE (via Shift+Restart from the lock screen) spawns an unrestricted shell with full access to the BitLocker-encrypted volume — no credentials required. Verified on Windows 11 24H2 with BitLocker active. [[Malware.News](https://malware.news/t/greatxml-windows-zero-day-turns-defender-offline-scan-into-bitlocker-backdoor/107803#post_1); [NightmareEclipse GitHub](https://git.projectnightcrawler.dev/NightmareEclipse/GreatXML); [HEAL Security](https://healsecurity.com/greatxml-bitlocker-bypass-0-day-exploited-via-windows-defender-offline-scan/)]

**Key implications:**
- **Precondition:** A Defender offline scan must have been run on the target at any prior point — triggering the vulnerable WinRE state.
- **Post-compromise persistence tool:** Requires admin rights to plant the files, but once planted, the bypass survives credential rotation, incident response, and loss of remote access. The attacker can return with physical access and unlock the disk.
- **No CVE, no patch.** This is the eighth tool from the Nightmare Eclipse cluster in roughly 10 weeks, and the second BitLocker bypass after YellowKey.
- **RoguePlanet context:** Also published this week (June 10), RoguePlanet is a separate LPE granting SYSTEM via a Microsoft Defender TOCTOU race condition on fully patched Windows 10/11. Not yet patched.

**Action:** Monitor for unexpected files at recovery partition root (`unattend.xml`, modified `Recovery/` directory). Organizations with high-value laptops should consider physical security controls and post-boot integrity verification.

---

**[NEW] LangGraph Checkpointer RCE Chain — SQLi → MsgPack Deserialization in AI Agent Persistence Layer (CVE-2025-67644, CVE-2026-28277, CVE-2026-27022)**

Check Point Research disclosed a chained vulnerability in LangGraph's checkpointers — the persistence layer for stateful AI agents in the LangChain ecosystem (50M+ monthly PyPI downloads). Three CVEs enable unauthenticated remote code execution on self-hosted LangGraph deployments that expose `get_state_history()` with a user-controlled `filter` parameter. [[Malware.News/Check Point Research](https://malware.news/t/from-sqli-to-rce-exploiting-langgraph-s-checkpointer/107789#post_1)]

**Attack chain:**
1. **CVE-2025-67644** — SQL injection in SQLite checkpointer's `_metadata_predicate()` function; user-controlled dictionary keys interpolated directly into SQL WHERE clause
2. **CVE-2026-28277** — Unsafe msgpack deserialization via `ormsgpack.unpackb()` — allows calling `os.system()` with attacker-controlled commands using `EXT_CONSTRUCTOR_SINGLE_ARG` extension type
3. **CVE-2026-27022** — Same SQL injection class affecting the Redis checkpointer

**Who's at risk:** Teams self-hosting LangGraph with SQLite or Redis checkpointers where the application passes user input to `get_state_history()`. LangChain's managed cloud (LangSmith) runs PostgreSQL and is unaffected. **Patched in:** `langgraph-checkpoint-sqlite 3.0.1+`, `langgraph 1.0.10+`, `langgraph-checkpoint-redis 1.0.2+`.

---

## 🛡️ Defense & Detection

**[NEW] OnionDrop: Commoditized Loader with Nation-State-Grade Evasion Delivers Vidar, CGrabber at Scale**

The Howler Cell Threat Research Team identified **OnionDrop**, a multi-stage loader that has delivered 645+ unique DLL samples between February 28 and May 20, 2026. Its evasion depth rivals nation-state tooling, with a four-stage unpack chain (custom byte-pair → Xpress Huffman → AES-256-CBC → Donut shellcode), DLL sideloading via legitimate Adobe-signed executables, and execution via `TpPostWork` thread-pool callback abuse (bypassing standard CreateThread telemetry). Confirmed payloads include LegionLoader (CurlyGate), CGrabber, and Vidar Stealer. C2: `gainmsg[.]com`. [[Malware.News/Howler Cell](https://malware.news/t/oniondrop-commoditized-loader-with-nation-state-grade-evasion/107783#post_1)]

---

**[NEW] Criminal AI-as-a-Service in 2026 — Underground Market Shifts From Hype to Operational Productivity Layer**

Rapid7 published a comprehensive analysis of the criminal AI ecosystem, documenting how AI has moved past "malicious chatbot" hype and is now integrated as a productivity layer across phishing, fraud, target profiling, malware modification, and post-breach data exploitation. The market splits into two trajectories: low-cost mass-market tools (FraudGPT, WormGPT copycats) for entry-level actors, and precision platforms (BruteForceAI) that use LLMs for intelligent form analysis and multi-threaded attack execution — shifting from noisy volume to quiet, optimized targeting. [[Rapid7](https://www.rapid7.com/blog/post/tr-criminal-ai-underground-market-operationalizing-cybercrime-2026)]

**Notable finding:** Stolen AI accounts and hijacked API keys may be a more consequential criminal market than traditional credential markets, providing attackers with scalable cognitive capabilities, multilingual targeting, and access to enterprise-grade models at the victim's expense.

---

**📌 [tl;dr sec gap] Sub:jugation — Phantom Cloud Identities Enable OIDC Trust Abuse in AWS and Azure**

Astrix Security disclosed that **14% of AWS and 24% of Azure OIDC identities** trusting GitHub Actions' `token.actions.githubusercontent.com` issuer point at **unregistered or deleted repository namespaces**. An attacker who reclaims a deleted repo namespace can mint JWTs matching orphaned role trust policies, inheriting all permissions the deleted repo once held. GitHub has fixed the issue by adding random identifiers to `sub` claims. GitLab CI and Terraform Cloud have interim mitigations but remain partially exposed. **Action:** Audit all trust policies referencing `token.actions.githubusercontent.com`, `gitlab.com`, or `app.terraform.io` for unregistered namespace references. [[tl;dr sec #332](https://tldrsec.com/p/tldr-sec-332); [Astrix Security](https://astrix.security/blog/subjugation)]

---

## 📋 Policy & Industry News

**[NEW] Coupang Fined Record $409M in South Korea — 37.55 Million Customers Affected by Data Breach**

South Korea's PIPC fined e-commerce giant Coupang 624.6 billion won (~$409M) — the largest data breach penalty in the country's history — following a breach affecting 37.55 million customers. Investigators found "negligence in authentication signature key management and access control," data destruction and notification violations, and interference with the data protection officer. The primary suspect is a 43-year-old former Chinese national IT employee who worked at Coupang between 2022 and 2024. Subsidiary Coupang Fulfillment Service was also fined for unlawful data collection. Coupang has already committed 1.685 trillion won (~$1.17B) in customer compensation. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/south-korea-hits-coupang-with-record-409-million-fine-over-data-breach/)]

---

**[UPDATE] Tchap Breach: 73,467 French Govt Employees Affected — Official Count Confirmed, 13.5 GB Exfiltrated**

DINUM disclosed that the Tchap breach (covered June 10) affects 73,467 accounts — 9% of 825,000 registered users. Private E2EE conversations were protected, but the attacker scraped public chat rooms for names, emails, organizations, and avatars. The threat actor claims to have stolen 650,000 messages and 13.5 GB of documents/media, plus hardcoded LDAP credentials found in a shared PowerShell script. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/french-govt-says-tchap-breach-affected-over-73-000-accounts/)]

---

**[NEW] Maine Breach Portal Abused to Publish Fake Breach Disclosures**

Fraudulent data breach notices were submitted to Maine's official AG breach portal — including a fake VRChat filing (2.4M affected) and a fake Discord filing (10M affected) — and publicly posted without verification. VRChat CEO and community head confirmed the filing is fraudulent and that the named employee does not exist. Maine AG acknowledged the portal has no vetting process and confirmed the fake notices will be removed. The incident highlights that breach portal filings are not authoritative without independent verification. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/maine-breach-portal-abused-to-publish-fake-data-breach-disclosures/)]

*Note: Malwarebytes independently reported VRChat experienced a real cloud breach affecting 2.4M users (May 10–12) and filed a legitimate notice elsewhere. VRChat denies any breach. The Maine portal filing is confirmed fraudulent per VRChat's CEO.*

---

## ⚡ Quick Hits

- **[NEW] UNC1151/Ghostwriter shifts Gmail targeting** — The Belarus-linked threat actor, previously focused on other email providers, is now running phishing campaigns against Gmail accounts, primarily targeting Polish citizens. Techniques evolve but core themes remain unchanged. [[Malware.News/CERT Polska](https://malware.news/t/unc1151-ghostwriter-phishing-campaign-targeting-gmail-accounts/107814#post_1)]
- **[NEW] Palo Alto GlobalProtect CVE-2026-0257 exploitation wave** — Arctic Wolf confirms increased exploitation of the auth bypass vulnerability following public PoC release. Requires specific config conditions (GlobalProtect portal/gateway exposure + auth override cookies). [[Malware.News/Arctic Wolf](https://malware.news/t/arctic-wolf-observes-an-increase-in-palo-alto-networks-globalprotect-authentication-bypass-exploitation-via-cve-2026-0257/107793#post_1)]
- **[NEW] LockBit 5.0 claims two new victims** — Sweetome (Chinese hospitality/hotel chain) and Delano Public Schools (Minnesota, USA) both hit within 24 hours, with threats to leak stolen data. [[Malware.News/DeXpose](https://malware.news/t/lockbit5-attacks-sweetome-major-hit-on-chinese-hospitality-sector/107810#post_1); [Malware.News/DeXpose](https://malware.news/t/lockbit-5-0-targets-delano-public-schools-in-ransomware-attack/107808#post_1)]
- **[NEW] Japanese energy firm Kyushu Electric loses hard drive with 10.9M customer records** — Physical security incident: external backup drive went missing from an unlocked server room cabinet between April 27 and May 26. 57 personnel had access to the room. Ministry of Economy, Trade and Industry demands full report by July 8. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/japanese-energy-firm-loses-drive-with-data-of-109-million-clients/)]
- **[NEW] OnyxC2 Stealer priced at $250/month subscription** — Enterprise-grade credential theft tool offered as a cybercrime SaaS product. [[SecurityWeek](https://www.securityweek.com/onyxc2-stealer-offers-cybercriminals-enterprise-grade-theft-for-250-a-month/)]
- **[UPDATE] Void Blizzard (Russian state-sponsored) — Denis Obrezko charged in Boston** — Russian national arrested in Thailand, extradited to the US, charged with conspiracy for unauthorized computer access linked to espionage campaign targeting US companies. [[CyberScoop](https://cyberscoop.com/russian-national-charged-void-blizzard-cyber-espionage/)]
- **[NEW] Anthropic disputes Fable 5 jailbreak claims** — Jailbreaker "Pliny the Liberator" claimed to have bypassed Claude Fable 5's safeguards via multi-agent prompting. Anthropic counters that conversational refusal suppression does not disable independent classifier systems or the Opus 4.8 fallback for high-risk domains. [[SecurityWeek](https://www.securityweek.com/anthropic-disputes-fable-5-ai-jailbreak/)]
