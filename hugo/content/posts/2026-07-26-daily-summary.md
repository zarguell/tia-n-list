---
title: "🎯 Steam ClickFix Drops XMRig, 🔧 SourTrade In-Browser Malware, 🎭 ShinyHunters Sextortion, ⚠️ FastJson CVE-2026-16723 Active RCE, ⚠️ Certighost AD CS PoC Public"
date: 2026-07-26
tags: ["ClickFix","XMRig","Cryptominer","Malvertising","SourTrade","ShinyHunters","Sextortion","FastJson","CVE-2026-16723","Active Exploitation","AD CS","Certighost","CVE-2026-54121","Threat Intelligence"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Steam forums abused for ClickFix cryptomining, SourTrade malvertising builds malware in browser memory, ShinyHunters data fuels sextortion campaign, FastJson CVE-2026-16723 actively exploited with no patch available, and Certighost AD CS domain takeover PoC goes public."
---

# Daily Threat Intelligence Digest — July 26, 2026

3 articles ingested and analyzed from curated cyber intelligence feeds. Prior-digest continuity tracked across Jul 22–25. Gap detection via web search surfaced FastJson CVE-2026-16723 (active exploitation, no patch) and Certighost CVE-2026-54121 (AD CS PoC public) as unindexed critical stories.

---

## 🎯 Threat Actor Activity & Campaigns

### Steam Forum ClickFix Attacks Infect Gamers with XMRig Cryptominers

Threat actors are abusing **Steam discussion forums** in a ClickFix social engineering campaign that tricks gamers into installing XMRig cryptominers. Attackers create random Steam accounts and reply to user posts about game crashes, lost inventory items, and technical issues, posing as helpful community members.

Victims are instructed to open **PowerShell as administrator** and run a command that claims to fix the problem. In reality, the command silently downloads and executes an XMRig miner. Because the victim manually launches the command, the attack bypasses security protections that would otherwise auto-block malicious code execution.

The PowerShell script masquerades as a Windows optimization utility named "msf util" — a fake tool name designed to sound legitimate. While ClickFix attacks require user interaction, they are effective because they present as a genuine solution to a real problem the user is experiencing.

**Action:** Educate users that legitimate technical support never involves copy-pasting PowerShell commands from forum posts. Monitor for anomalous PowerShell execution from gaming-related processes.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/steam-forum-clickfix-attacks-infect-gamers-with-xmrig-cryptominers/)

---

### SourTrade Malvertising Campaign Builds Malware Directly in Browser Memory

A large-scale malvertising campaign tracked as **SourTrade** is using fake **Solana, Luno, and TradingView** webpages with malicious JavaScript that assembles malware directly in the browser's memory, completely in-memory with no files written to disk. The operation, documented by ad security platform **Confiant**, has been active since **late 2024** and targets users across **25 languages in 12 countries**, primarily in Asia Pacific and Latin America.

The attack chain is technically sophisticated:
- The landing page registers a **Service Worker** that acts as a download manager
- A **SharedWorker** is set up as an assembly engine that incrementally builds the malware from components received in subsequent stages
- The page requests a `/config` response with session-unique seed and size parameters
- A sophisticated **filtering system** ensures only genuine targets (retail traders and crypto investors) reach the malicious pages — researchers, scanners, and security bots are redirected to blank pages

By rotating seed and size parameters per session, each malware payload is unique, making signature-based detection ineffective. The browser itself becomes "a local assembly pipeline" for the malware.

**Hunting hypothesis:** Monitor for Service Worker registrations from financial/trading domains, especially those with suspicious origin or unusual `/config` endpoint requests. Investigate SharedWorker activity from browser contexts that should not require parallel processing.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/malicious-sites-use-javascript-to-build-malware-in-browser-memory/) · Confiant

---

### ShinyHunters Data Leaks Fuel $2,000 Sextortion Email Campaign

Threat actors are weaponizing email addresses exposed in data breaches previously leaked by the **ShinyHunters** extortion group to send sextortion emails demanding **$2,000 in Bitcoin**. BleepingComputer confirmed that leaked data from breaches including **Amtrak, Hallmark, Substack, Betterment, CarGurus, ADT, Panera Bread, and McGraw Hill** is being used in this campaign.

The emails claim to come from ShinyHunters and threaten that the recipient's device was compromised, their camera accessed, and browsing history on adult websites recorded. However, the messages appear to be sent by **third parties who downloaded ShinyHunters' leaked data** rather than by the extortion group itself. ShinyHunters denied any involvement in the sextortion campaign when contacted.

While the use of a real leaked email address makes these threats appear credible, there is **no evidence** that the senders actually compromised recipients' devices, installed malware, or accessed their cameras. This campaign illustrates the cascading harm of data breaches — data leaked by one group is repurposed by multiple downstream actors.

**Action:** Organizations whose data appeared in ShinyHunters-related breaches should notify affected users of this specific sextortion risk. Users receiving such emails should not pay and report to local law enforcement. There is no evidence of actual device compromise — the threats are based solely on exposed email addresses.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/shinyhunters-data-leaks-fuel-2-000-sextortion-email-scam/)

---

## ⚠️ Vulnerabilities & Patches

### [GAP] FastJson CVE-2026-16723: Critical RCE Actively Exploited — No Patch Available

A critical remote code execution vulnerability in **Alibaba Fastjson** (the widely used Java JSON library) tracked as **CVE-2026-16723** (CVSS 9.0) is under active exploitation with **no patched Fastjson 1.x release available**. Security firms **Imperva** and **ThreatBook** report active attacks targeting financial services, healthcare, computing, and retail organizations primarily in the United States, Singapore, and Canada.

Key details:
- Affects **Fastjson 1.2.68 through 1.2.83** (version 1.2.83 is the latest 1.x release and remains vulnerable)
- Works under **stock default configuration** — AutoType does not need to be enabled, and no classpath gadget is required
- Exploitable in **Spring Boot fat-JAR** deployments via crafted JSON `@type` values
- Alibaba published a security advisory on **July 21** but has not released a patched 1.x artifact
- Full technical details and working **proof-of-concept exploit code** are now public
- **Qi'anxin** estimates millions of exposed instances

This flaw is particularly dangerous because it bypasses protections that defenders relied on after earlier Fastjson disclosures (AutoType disablement, gadget-free classpath). Organizations running Fastjson 1.x behind internet-facing Spring Boot services have no straightforward patch to apply.

**Mitigation (no patch available):** Enable SafeMode in Fastjson configuration. Review whether Fastjson 1.x can be replaced with a maintained fork or newer library version. Segment internet-facing Spring Boot services. Monitor for deserialization attack patterns in JSON payloads. Consider WAF rules to block anomalous `@type` values in JSON bodies where feasible.

**Action:** Immediately audit all Java services for Fastjson 1.x dependency. Prioritize services that are internet-facing or process untrusted JSON. If migration is not immediately feasible, implement compensating controls (WAF, network segmentation, input validation).

**Sources:** [The Hacker News](https://thehackernews.com/2026/07/fastjson-1x-rce-vulnerability-targeted.html) · [SecurityOnline](https://securityonline.info/fastjson-rce-cve-2026-16723/) · [Capstone TI](https://captechgroup.com/threat-intelligence-center/fastjson-1x-rce-vulnerability-exploited-in-active-6a518f) · [GitHub Advisory](https://github.com/advisories/ghsa-crf3-v9rr-v7hj)

---

### [GAP] Certighost CVE-2026-54121: Public PoC Enables Low-Privilege AD CS Domain Takeover

A public, fully working proof-of-concept exploit dubbed **"Certighost"** has been released for **CVE-2026-54121**, a critical **Active Directory Certificate Services (AD CS)** vulnerability that allows any authenticated domain user — with no admin rights — to impersonate a **Domain Controller** and extract the **krbtgt secret**, enabling full Active Directory domain compromise.

Key details:
- Any **low-privilege domain user** can forge a Domain Controller certificate
- Extracting krbtgt enables **Golden Ticket** attacks for persistent domain access
- Microsoft patched the flaw in **July 14, 2026 Patch Tuesday**
- Discovered by researchers @h0j3n and reported through ZDI
- Public exploit code is now available on GitHub

This is the latest in a series of AD CS-focused vulnerabilities following **Certipy**, **ESC1-ESC13**, and **Pass the Certificate** attacks. AD CS continues to be a high-value attack surface because certificate services run with elevated privileges and are often deployed without the hardening attention given to core AD infrastructure.

**Action:** If not already patched, apply the July 14 Microsoft security update immediately. After patching, audit AD CS for signs of abuse — look for unexpected certificate requests from non-DC machines, anomalous Kerberos TGT requests, and unauthorized certificate templates. Treat any unpatched domain controller as potentially compromised.

**Sources:** [CybersecurityNews](https://cybersecuritynews.com/certighost-active-directory-cs-flaw/) · [Dataminr](https://www.dataminr.com/resources/intel-brief/certighost-cve-2026-54121/) · [CIRT Advisory](https://cirt.gov.jm/advisory/certighost-ad-cs-vulnerability-cve-2026-54121-allows-low-privileged-users-compromise)

---

## Gap Detection

- **r/cybersecurity hot:** No unindexed critical stories found — Reddit's current top stories (RSAC/Black Hat comparisons, market discussion) are non-security or already in feed.
- **CISA KEV:** No new additions since July 22 (6 CVEs added Jul 21–22, thoroughly covered in prior digests).
- **General news scan:** Two substantive gaps identified above — FastJson CVE-2026-16723 (active exploitation, no patch) and Certighost CVE-2026-54121 (AD CS PoC public). Excluded from prior digest coverage: Secure Boot shim bypass (Ars Technica re-reporting of Jul 16 SecurityWeek story), Iranian PLC expansion (Jul 22-23), NadMesh botnet (Jul 17-20), Slopsquatting/HalluSquatting (Jul 25), Clop Windchill (Jul 24).

---

*Digest generated July 26, 2026. 3 feed articles reviewed, 4 prior digests cross-referenced for continuity, gap detection via web search and CISA KEV monitoring. Excluded as already covered in prior digests: Slopsquatting/HalluSquatting (Jul 25), Clop Windchill (Jul 24), FakeAgent/Bing Ads SectopRAT (Jul 24), Check Point CVE-2026-16232 (Jul 23), Laundry Bear/Zimbra (Jul 24), SharePoint exploitation cluster (Jul 22-23).*
