---
title: "🛡️ RoguePlanet patch in progress, 🎯 Joomla/LiteSpeed exploited, 🐍 Arista no-patch tunnel bug, 📱 Rokarolla Android malware, 💣 ShinyHunters Kodak breach, 🔥 Oracle 245 patches"
date: 2026-06-17
tags: ["rogueplanet","cve-2026-50656","joomla","litespeed","arista","rokarolla","shinyhunters","kodak","oracle","android-malware","dragonforce","ghosttree","chrome","firefox","novo-nordisk","cal-water","handala","jetbrains","cisa-kev"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Microsoft works on RoguePlanet Defender patch (CVE-2026-50656); Joomla, LiteSpeed flaws exploited and added to CISA KEV; Arista EOS tunnel bug (CVE-2026-7473) has no fix and evades scanners; Rokarolla Android trojan targets 217 banking apps; ShinyHunters claims Kodak breach with 2.2M records; Oracle ships 245 patches in second monthly CSPU. Iran-linked Handala group breaches Cal Water. Two extortion groups separately hit Novo Nordisk for $50M and $25M — neither paid."
---

# Daily Threat Intelligence Digest — June 17, 2026

*56 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] RoguePlanet (CVE-2026-50656) — Microsoft Assigns CVE, Working on Defender Patch One Week After Public Disclosure**

Microsoft has confirmed it is working on a security patch for the **RoguePlanet** Microsoft Defender race condition zero-day, now tracked as **CVE-2026-50656**, one week after researcher Nightmare Eclipse publicly released an exploit granting SYSTEM privileges on fully patched Windows 10 and Windows 11. Microsoft's advisory acknowledges the vulnerability in the Microsoft Malware Protection Engine but does not credit the researcher — part of an ongoing dispute over Microsoft's bug bounty practices. The exploit triggers a race condition in Defender's internal processing to spawn a SYSTEM-level command prompt regardless of whether real-time protection is enabled. Nightmare Eclipse previously leaked BlueHammer, RedSun, GreenPlasma, MiniPlasma, YellowKey, and UnDefend exploits, with Microsoft fixing GreenPlasma, MiniPlasma, and YellowKey in the June Patch Tuesday. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-working-on-defender-patch-for-rogueplanet-zero-day/)]

**Hunting hypothesis:** Monitor for unexpected `cmd.exe` or `powershell.exe` child processes spawned from `MsMpEng.exe` — the Defender engine process should never launch interactive shells.

---

**[NEW] Joomla (CVE-2026-48907) and LiteSpeed (CVE-2026-54420) Vulnerabilities Exploited in Attacks — CISA Adds to KEV**

Threat actors are actively exploiting two vulnerabilities in web hosting environments, both added to CISA's KEV catalog this week. **CVE-2026-48907** affects the Joomla Content Editor (JCE) Pro versions before 2.9.99.5 — an improper access issue allowing unauthenticated attackers to upload arbitrary files and execute PHP code. Joomla warned that exploit code is public, attacks are automated, and even sites without public registration are not safe. **CVE-2026-54420** affects LiteSpeed's cPanel user-end plugin before version 2.4.8 — a UNIX symlink following vulnerability allowing FTP or web shell users to escalate privileges to **root** on shared hosting servers running CloudLinux/CageFS, exploited in the wild since May. CISA ordered federal agencies to patch the Joomla flaw by June 19 and the LiteSpeed flaw by June 18 per BOD 26-04. [[SecurityWeek](https://www.securityweek.com/joomla-litespeed-vulnerabilities-exploited-in-attacks/)]

---

**[NEW] Arista EOS Tunnel Bug (CVE-2026-7473) — No Patch Coming, Vulnerability Scanners Will Miss It**

An actively exploited vulnerability in Arista EOS switches (CVE-2026-7473) allows attackers to bypass network segmentation by sending traffic in an unconfigured tunnel protocol to a decapsulation IP address — the switch unwraps and forwards it regardless of protocol. **There is no software fix planned.** Arista says changing decapsulation behavior would break existing deployments. The vulnerability lives entirely in configuration, not a version string, meaning version-based vulnerability scanners will either miss it or generate overwhelming false positives. Arista flagged in-the-wild exploitation on **May 5**, but the CVE did not appear in public databases for weeks and only landed on CISA's KEV on **June 9** — a five-week visibility gap. Admins must inventory tunnel endpoints via `show ip decap-group`, apply upstream ACLs restricting tunnel protocols, and validate using configuration auditing, not version checking. [[Malware.News/Eclypsium](https://malware.news/t/no-patch-coming-the-arista-eos-tunnel-bug-your-scanner-will-miss/107943#post_1)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Rokarolla Android Banking Trojan Targets 217 Banking and Crypto Apps**

Zimperium discovered **Rokarolla**, a new Android banking trojan distributed via malicious websites posing as Google Chrome or TikTok download pages. The malware uses 137 commands for near-complete device takeover, including fake login overlays targeting 217 financial applications, keylogging, SMS interception, contact harvesting, call blocking (to prevent fraud alerts), and continuous screenshot capture. During installation, Rokarolla impersonates Google Play Protect to trick users into granting Accessibility service permissions, then hides its icon and disables Google Play Protect. Not found on Google Play — distributed exclusively through sideloaded APKs. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-rokarolla-android-malware-targets-217-banking-crypto-apps/)]

---

**[NEW] Kodak Confirms Breach — ShinyHunters Claims 2.2 Million Records, Sets June 18 Leak Deadline**

Kodak confirmed that an unauthorized third party gained temporary access to company data and is working with external cybersecurity experts and law enforcement. The **ShinyHunters** extortion group claimed responsibility, alleging theft of **2.2 million records** containing customer PII and internal corporate data, and set a **June 18** leak deadline. The incident comes amid ShinyHunters' ongoing campaigns against Salesforce customers (1.5 billion records claimed), Snowflake victims, and the recently disclosed Oracle PeopleSoft zero-day campaign against 100+ organizations including the University of Nottingham. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/kodak-confirms-data-breach-claimed-by-shinyhunters-extortion-gang/)]

---

**[NEW] GhostTree Attack Abuses Recursive Windows Junctions to Hide Malware**

Researchers detailed the **GhostTree** attack technique, which abuses recursive NTFS junctions — file system features any user can create without admin privileges — to hide malware. NTFS junctions and symbolic links let one directory transparently point to another. In GhostTree, attackers create nested junction chains that make directory traversal loop infinitely, causing security tools to hang or skip the hidden content. The technique enables stealthy malware persistence that evades traditional file system scanning. Since any user can create junctions, no privilege escalation is needed. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ghosttree-attack-abused-recursive-windows-junctions-to-hide-malware/)]

---

**[UPDATE] DragonForce Ransomware — Sustained UK Campaign Hits 7 Companies in May**

DragonForce ransomware affiliates claimed **seven UK-based organizations** in May 2026, posting them on the group's Tor data leak site — including **Practicus** (executive search), **WSM** (tax advisory), **Helix International** (MSP serving Fortune 500 clients across healthcare/finance), and **Cult Wines** (luxury retail/finance). DragonForce affiliates are opportunistic, exploiting edge devices (Ivanti Connect Secure, Fortinet FortiOS, SonicWall SSL-VPN) and abusing BYOVD tactics to bypass EDR. The group made headlines in June 2025 when Scattered Spider-linked affiliates hit UK retailers M&S, Co-op, and Harrods. *Previously covered June 16: DragonForce using Microsoft Teams TURN relays for stealth C2.* [[Malware.News/UK Cybercrime Journal](https://malware.news/t/uk-cybercrime-journal-sustained-dragonforce-campaign/107951#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Oracle's Second Monthly CSPU Delivers 245 Patches — 120+ Critical, 100 Remotely Exploitable Without Auth**

Oracle released its June 2026 Critical Security Patch Update, the second since transitioning to monthly patch cycles. The update covers 245 vulnerabilities across Communications, EBS, Enterprise Manager, Fusion Middleware, MySQL, PeopleSoft, and other product families. Roughly **120 flaws** are rated critical, and **100 can be exploited remotely without authentication**. Fusion Middleware received the heaviest patch load with 100+ fixes. Oracle warned it "continues to periodically receive reports of attempts to maliciously exploit vulnerabilities for which patches already exist," referencing the ShinyHunters group's exploitation of CVE-2026-35273 (PeopleSoft) against 100+ organizations. [[SecurityWeek](https://www.securityweek.com/oracles-second-monthly-security-updates-deliver-245-patches/)]

---

**[NEW] Chrome 149 and Firefox 152 Patch 70+ Vulnerabilities Including Critical Memory Safety Bugs**

Google released Chrome 149 (Windows/Mac: 149.0.7827.155/.156, Linux: 149.0.7827.155) fixing **33 security defects** — 7 critical-severity (six use-after-free issues exploitable for RCE and potential sandbox escape) and 26 high-severity flaws. Mozilla released Firefox 152 addressing **40 vulnerabilities**, including 13 high-severity issues spanning use-after-free, privilege escalation, sandbox escape, JIT miscompilation, and memory safety bugs that could enable arbitrary code execution. No in-the-wild exploitation reported for either browser. [[SecurityWeek](https://www.securityweek.com/chrome-and-firefox-updated-to-patch-critical-high-severity-vulnerabilities/)]

---

**[NEW] Malicious JetBrains Marketplace Plugins Steal AI API Keys from Developers**

Aikido Security discovered **15 malicious plugins** on the JetBrains Marketplace designed to steal AI API keys from developers. The plugins masquerade as AI coding assistants, code-review tools, and Git utilities powered by OpenAI, DeepSeek, and SiliconFlow. Developers who installed these plugins may have had their API credentials for AI services exfiltrated — a supply-chain attack vector targeting the developer toolchain directly. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/malicious-jetbrains-marketplace-plugins-steal-ai-api-keys-from-developers/)]

---

## 🛡️ Defense & Detection

**[NEW] Captured Honeypot Logs Reveal Hackers Using Claude and Codex AI in Real-World Intrusions**

OALABS Research published captured session logs from a compromised host turned honeypot, providing unprecedented visibility into how attackers are using **Claude** (Anthropic) and **Codex** (GitHub Copilot) during active intrusions. The logs show attackers leveraging AI coding agents to write exploit code, analyze stolen data, and automate lateral movement steps — representing one of the first documented publicly available datasets of real-time AI-assisted intrusion activity. [[Malware.News/OALABS](https://malware.news/t/captured-logs-reveal-hackers-using-claude-and-codex-to-breach-companies/107944#post_1)]

---

## 📋 Policy & Industry News

**[NEW] Iran-Linked Handala Hacktivists Claim Cal Water Breach — 5GB of Data Leaked**

The **Handala** group, an Iran-linked threat actor believed to be a front for Iranian government hacking operations, leaked **5 GB of files** allegedly stolen from California Water Service (Cal Water), one of the largest investor-owned water utilities in the US. The group claimed it could have disrupted the water supply but chose not to, framing the attack as retaliation for US actions against Iran. Dataminr analysis indicates the leaked data includes personal information from a customer billing database and internal RTKBase application. Cal Water confirmed it is investigating in collaboration with federal and state partners, stating preliminary findings show no operational disruptions to water/wastewater systems. [[SecurityWeek](https://www.securityweek.com/cal-water-investigating-iranian-hackers-claims/)]

---

**[UPDATE] Novo Nordisk Breach — Two Separate Extortion Groups, Demands of $50M and $25M, Neither Paid**

New details emerged about the Novo Nordisk hack: **two separate threat actors** breached the Danish pharmaceutical giant. FulcrumSec (demanding $25M) accessed Novo Nordisk's systems via a **GitHub access token** in March, cloning repositories and finding additional credentials, stealing 1.3TB of data including undisclosed drug programs, proprietary compound structures, the Dicerna RNAi pipeline, and private AI models. A separate, unnamed threat actor demanded **$50 million** — also unpaid. Both groups have threatened to leak the stolen data. The stolen clinical trial data was pseudonymized and cannot be directly linked to patients by name. [[SecurityWeek](https://www.securityweek.com/cybercrime-group-claims-novo-nordisk-hack/); [Malware.News](https://malware.news/t/one-threat-actor-demanded-50-million-from-novo-nordisk-another-one-demanded-25-million-neither-got-paid/107941#post_1)]

*Previously covered June 16: FulcrumSec leaks Novo Nordisk data after $25M demand goes unpaid.*

---

## ⚡ Quick Hits

- **SpaceBears ransomware claims ECOVACS**: The ransomware group claimed a cyberattack on Chinese robotics leader ECOVACS, threatening to leak ~2 TB of stolen data. [[Malware.News/DeXpose](https://malware.news/t/spacebears-ransomware-attack-targets-robotics-leader-ecovacs/107946#post_1)]
- **Payload ransomware targets SPORTON International**: Taiwan-based testing and certification services provider hit by Payload ransomware group, which threatens to release sensitive data. [[Malware.News/DeXpose](https://malware.news/t/payload-ransomware-targets-sporton-international-inc/107945#post_1)]
- **Steam Workshop abused to push malware via Wallpaper Engine**: Threat actors hide malware (backdoors, cryptominers, account stealers) in wallpaper packages on Steam Workshop. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/steam-workshop-abused-to-spread-malware-via-wallpaper-engine-app/)]
- **Free World Cup stream sites serving scams**: Fake streaming platforms for the 2026 World Cup are distributing malware and harvesting credentials — no legitimate free streams exist. [[Malware.News](https://malware.news/t/free-world-cup-stream-sites-are-serving-scams-not-football/107933#post_1)]
- **Bluekit Phishing-as-a-Service emerges**: A new PhaaS platform detected in the wild, offering phishing toolkits to affiliates. [[Malware.News](https://malware.news/t/bluekit-phishing-as-a-service-phaas/107942#post_1)]
- **iRhythm confirms data stolen in cyberattack**: Cardiac monitoring company filed with SEC after attackers used social engineering to access third-party business applications and stole patient health information, demanding a ransom on June 9. *Previously covered June 16.* [[SecurityWeek](https://www.securityweek.com/irhythm-confirms-data-stolen-in-hack/)]
- **Cardiac patients' medical data stolen and held to ransom**: A separate incident involving patient medical data exfiltration and ransom demands. [[Malware.News](https://malware.news/t/cardiac-patients-medical-data-stolen-and-held-to-ransom/107928#post_1)]
