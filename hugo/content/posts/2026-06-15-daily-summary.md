---
title: "📡 Outsider Takedown Details, 🇪🇺 ShinyHunters Council of Europe, 🔓 Lapsus$ GitHub Claim, 🇰🇵 APT37 NarwhalRAT, 🦠 Ransomware Surge, 🏥 Novo Nordisk Breach"
date: 2026-06-15
tags: ["outsider-enterprise", "operation-ghost-hook", "shinyhunters", "lapsus", "apt37", "narwhalrat", "dragonforce", "qilin", "ransomware", "novo-nordisk", "bwh-hotels", "kimsuky", "data-breach", "phishing-as-a-service", "maine-ag", "threat-intelligence"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "FBI publishes operational details on Outsider Enterprise takedown — 3.8M credit cards recovered. ShinyHunters claims Council of Europe breach (297GB, June 16 deadline). Lapsus$ claims GitHub Internal breach. APT37 deploys NarwhalRAT with pCloud dead-drop C2. Ransomware surge: DragonForce, Qilin, Nightspire, Nova hit 12+ victims over the weekend. Novo Nordisk reports data breach."
---

# Daily Threat Intelligence Digest — June 15, 2026

*27 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — `reddit_gap_check.py` unavailable (scrapling module, consistent failures across prior digests June 9–14). Web search credits exhausted — no external gap detection performed. Prior digests: June 10–14, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Operation Ghost Hook — FBI Publishes Operational Details on Outsider Enterprise Takedown, 3.8 Million Credit Cards Recovered**

The FBI, Google, and Lumen Technologies released additional operational details on the dismantling of **Outsider Enterprise**, the China-based phishing-as-a-service platform taken down as part of **Operation Riptide** (covered June 13). The operation recovered **3.8 million stolen credit card records** and seized multiple admin servers, a Shopify storefront (~$100K in USDT seized), and a Telegram bot containing customer information. Google confirmed **2.5 million SMS messages** were sent in a two-week period from Outsider infrastructure, with Android users flagging 55,000 as fraudulent. Google has filed a civil lawsuit targeting the operation's infrastructure and is coordinating with AT&T, T-Mobile, and Verizon to block fraudulent SMS. The company is advocating for seven bipartisan anti-scam bills including the **Stop SCAMS Act**, which would require the FBI to lead a coordinated national anti-scam strategy. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-disrupts-massive-ai-powered-phishing-service-using-a-million-urls/)]

---

**[NEW] ShinyHunters Claims Theft of 297GB of Council of Europe Data — June 16 Leak Deadline**

The ShinyHunters cybercrime group has claimed responsibility for a breach of the **Council of Europe**, threatening to publish 297 GB of allegedly stolen data unless demands are met by **June 16**. The claim has not been independently confirmed. This extends ShinyHunters' accelerating campaign — following the Oracle PeopleSoft zero-day exploitation (CVE-2026-35273, 100+ victim organizations, covered June 10–12), American Tower Corporation (5.2M records including cell tower gate codes, covered June 13), and Madison Square Garden (26M records, covered June 13). The Council of Europe claim suggests the group's operational tempo is increasing, not slowing, following the June 13 leak of American Tower and MSG data. [[DataBreaches.net via Malware.News](https://malware.news/t/shinyhunters-claims-theft-of-297gb-of-council-of-europe-data-claims-unconfirmed-as-yet/107847#post_1)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Lapsus$ Claims Breach of GitHub Internal — Threatens to Leak Source Code Unless Buyer Found**

The notorious extortion group **Lapsus$** claimed on June 13 to have breached **GitHub Internal (github.com)**, the core infrastructure of the Microsoft-owned development platform. The group stated: *"Everything for the main platform is there. No ransom, we do not care about extorting Github. If no buyer is found, we leak for free."* No independent confirmation from GitHub has been published as of this writing. If confirmed, this would represent one of the most significant source code breaches in recent years — GitHub hosts the source code for millions of projects and its internal tooling could provide attackers with intel on how the platform vets for malware (critical given the ongoing Shai-Hulud/Miasma supply chain campaign). [[DeXpose/Malware.News](https://malware.news/t/lapsus-strikes-github-internal-in-latest-cybersecurity-breach/107864#post_1)]

---

**[NEW] APT37 (North Korea) Deploys NarwhalRAT via Microsoft-Themed Phishing, Uses pCloud as Dead-Drop C2**

A new analysis documents **APT37** (ScarCruft, Group 123, Reaper) deploying a new remote access trojan called **NarwhalRAT** through spear-phishing emails disguised as Microsoft account team communications and cybersecurity advisories. Initial access leverages malicious **LNK files** that trigger installation of a compiled Python-based RAT with comprehensive info-stealing capabilities: keylogging, screen capture, USB data exfiltration, and remote command execution. The C2 architecture uses a **dual structure** — a Korean-based relay server paired with the **pCloud API** as a dead-drop resolver, making infrastructure takedown harder than traditional C2 domains. EDR policies should be reviewed for detection of LNK → PowerShell → Python chained execution patterns. [[Malware.News](https://malware.news/t/analysis-of-apt37-narwhalrat-leveraging-ms-themed-phishing-and-dead-drop-c2/107848#post_1)]

---

**[UPDATE] Ransomware Activity Surge — DragonForce (3 UAE/Hotel Targets), Qilin (4 Victims), Nightspire, Nova, WorldLeaks, Pear**

Several ransomware groups posted new victims over the weekend:

- **DragonForce** claimed three new victims — **Corniche Hotel Abu Dhabi** (UAE luxury hotel), **Durrat Resort Management** (Bahrain), and **INK** — following their June 12 wave of Al Shafar GRC, Al Ishrak Contracting, and Cheoy Lee Shipyards (covered June 13). The UAE/hotel-sector targeting pattern continues.
- **Qilin** posted four victims on June 12–14: **DISTINET MURCIA SL** (Spain, business services), **TagleRock Technologies**, **AltaVista Strategic Partners**, and **Wright Constable & Skeen**.
- **Nightspire** hit **Pattono S.r.l** (Italian technology company).
- **Nova Ransomware** targeted **Balai Besar POM di Bandung** (Indonesian food/drug regulatory body, `.go.id` domain) — a notable government-sector target in Southeast Asia.
- **WorldLeaks** claimed **Centra Sota Cooperative** (US agricultural cooperative).
- **Pear Ransomware** hit **K & E Distributing** (Canada).

All claims are via victim-shaming leak sites and threat actor statements on cybercrime forums. [[Malware.News](https://malware.news/t/dragonforce-targets-corniche-hotel-abu-dhabi-in-ransomware-attack/107862#post_1); [Malware.News](https://malware.news/t/qilin-strikes-spanish-business-service-provider-distinet-murcia-sl/107861#post_1)]

---

## 📋 Policy & Industry News

**[UPDATE] Maine Disables Data Breach Portal Following Fake VRChat/Discord Filings**

The Maine Attorney General's Office has **temporarily disabled public access** to its official breach notification database following the June 12 disclosure of fake VRChat and Discord breach filings on the portal (covered June 13). Companies may still submit disclosures through alternative channels, but public inspection now requires a direct request to the AG's office. The incident exposed a gap in the portal's submission verification process — essentially no validation beyond a web form. [[SecurityWeek](https://www.securityweek.com/maine-disables-data-breach-portal-due-to-fake-submissions/)]

---

**[NEW] Novo Nordisk Reports Data Breach, Warns Clinical Trial Patients**

Danish pharmaceutical giant **Novo Nordisk** disclosed a security incident, advising clinical trial patients to "remain vigilant" for potential misuse of their personal information. The breach adds Novo Nordisk to the growing list of biopharma companies targeted for intellectual property and patient data. The company has not disclosed the scope or method as of this writing. [[DataBreaches.net via Malware.News](https://malware.news/t/novo-nordisk-reports-data-breach-tells-clinical-trial-patients-to-remain-vigilant/107850#post_1)]

---

**[NEW] UK Hotel Chain (BWH Hotels / Best Western) Confirms 6-Month Data Breach Affecting Guest Reservations**

**BWH Hotels**, the parent company of WorldHotels and Best Western Hotels & Resorts, confirmed that personal information of guests with reservations at one of its properties was compromised over a six-month period. UK hotel guests have been warned to watch for convincing fraudulent messages. The breach underscores persistent targeting of the hospitality sector, where reservation systems hold PII (names, addresses, payment data, travel dates) lucrative for phishing campaigns. [[DataBreaches.net via Malware.News](https://malware.news/t/uk-hotel-guests-issued-urgent-check-alert-as-personal-details-stolen-from-major-chain/107849#post_1)]

---

## ⚡ Quick Hits

- **Kimsuky (North Korea) deploys new LNK malware** — Korean-language analysis documents Kimsuky's latest campaign using a malicious `.lnk` file titled "Wave Energy Theory May 2026 Revised Edition.lnk," targeting energy/economic analysis researchers. [[Malware.News](https://malware.news/t/kimsuky-2026-5-lnk/107851#post_1)]
- **Evil MSI Background: BASE64 Statistical Analysis** — SANS ISC diary provides a statistical analysis methodology for detecting Base64-obfuscated content in MSI installer files. Useful for analysts encountering MSI-based malware distribution. [[SANS ISC](https://isc.sans.edu/diary/30674)]
- **Local LLM complexity attacks on reverse engineering** — A practitioner's lab notebook tests 10 local LLMs (gemma4:31b, qwen3.6:35b) on a synthetic binary RE benchmark with increasing XOR-round complexity. gemma4:31b emerges as the strongest local baseline, solving up to 4-round fixtures. Most failures cluster around C integer width rules and cast timing — not missing the algorithm entirely. [[Malware.News](https://malware.news/t/stressing-llms-local-model-complexity-attacks-progress/107866#post_1)]
- **Smart glasses detection research** — As AR glasses with recording capabilities become more common, researchers examine technical challenges of detecting recording through smart eyewear — a growing privacy concern for security-conscious organizations. [[Malware.News](https://malware.news/t/smart-glasses-can-record-you-and-detecting-them-isn-t-so-simple/107852#post_1)]

---

*27 articles ingested from Miniflux Cyber feeds. External cross-referencing via Reddit skipped — `reddit_gap_check.py` unavailable. Web search credits exhausted — no external gap detection performed. Prior digests: June 10–14, 2026. Stale CVE/topic blocklist applied. Sources include BleepingComputer, SecurityWeek, DataBreaches.net, Malware.News, SANS ISC, and independent researchers.*