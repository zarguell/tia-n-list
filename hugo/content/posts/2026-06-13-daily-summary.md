---
title: "$1.9B Outsider Takedown, 400+ Arch Packages Compromised, ShinyHunters Hits American Tower & MSG, Handala Claims Cal Water, Conti Guilty Plea, phpBB Decade-Old Auth Bypass"
date: 2026-06-13
tags: ["China","Supply Chain","ShinyHunters","Handala","Conti","AUR","phpBB","Anthropic","AI Export Controls","DragonForce","Ransomware","Arch Linux","Critical Infrastructure"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "FBI takes down $1.9B China-based phishing platform Outsider; 400+ Arch Linux packages compromised with eBPF rootkit; ShinyHunters expands to American Tower (5.2M records with cell tower access codes) and MSG (26M records); Handala claims California water utility breach with destructive toolkit deployed; Conti operator pleads guilty; phpBB patches 10-year-old auth bypass."
---
# Daily Threat Intelligence Digest — June 13, 2026

*46 articles ingested from Miniflux Cyber feeds. External cross-referencing via Reddit skipped — Saturday light-volume handling. Prior digests: June 8–12, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] FBI, Google, and Lumen Shut Down "Outsider" — China-Based AI-Powered Phishing Empire Responsible for $1.9 Billion in Losses**

The FBI, Google, and Lumen Technologies took down **Outsider**, a massive China-based cybercrime platform that provided phishing kits and hosted infrastructure for cybercriminals since July 2023, in an operation dubbed **"Operation Ghost Hook."** Outsider operated as a phishing-as-a-service enterprise, offering kits to create fake login pages and SMS/PIN/email verification bypass — all for as low as **$88/week** — and provided step-by-step instructions for customers to use Gemini and other AI platforms to generate custom phishing code. [[CyberScoop](https://cyberscoop.com/outsider-cybercrime-network-takedown-china-fbi-google-lumen/)]

**Operation results:** FBI seized several core admin server domains, a Shopify storefront, and ~$100K from Outsider payment wallets. Authorities recovered **3.9 million stolen credit cards** traced to Outsider's phishing domains. Google is working with AT&T, T-Mobile, and Verizon to intercept spam messages, and filed a civil lawsuit to dismantle the network's infrastructure. The platform's operators remain unidentified, but per Google "the operation is supported by multiple cybercrime groups providing different roles with overlapping infrastructure." The takedown was part of the broader **Operation Riptide** campaign.

---

**[NEW] Over 400 Arch Linux AUR Packages Compromised — eBPF Rootkit and Infostealer Target Developer Workstations**

A coordinated supply-chain attack on the Arch User Repository has compromised **400+ packages** via spoofed maintainer accounts, distributing a malicious npm package called **`atomic-lockfile`** through tampered PKGBUILD scripts. The malware includes an ELF payload with **credential-stealing and optional eBPF rootkit capabilities** — the rootkit can hide processes, files, and network interfaces from the kernel. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/over-400-arch-linux-packages-compromised-to-push-rootkit-infostealer/); [Sonatype](https://www.sonatype.com/); [Whanos report](https://github.com/Whanos)]

**Targeted data:** GitHub credentials, SSH keys, HashiCorp Vault tokens, browser cookie databases, Slack/Discord/Teams/Telegram data, Docker/Podman credentials, VPN material, shell histories — replicating the credential-harvesting pattern seen in the Shai-Hulud/Miasma campaigns but at the Linux distribution level. Both IFIN (Independent Federated Intelligence Network) and Sonatype independently documented the campaign. AUR maintainers are working to identify and remove malicious commits and ban the accounts pushing them. **Action:** Review the affected packages list from IFIN/Whanos, run the detection script for atomic-lockfile, and consider reinstalling from scratch if a rootkit is found — standard malware removal may not be sufficient.

---

**[UPDATE] ShinyHunters Expands Beyond PeopleSoft — American Tower (5.2M Records Including Cell Tower Gate Codes) and Madison Square Garden (26M Records) Threatened With June 15 Leak**

The ShinyHunters data-theft extortion campaign, already linked to the Oracle PeopleSoft zero-day (CVE-2026-35273) affecting 100+ organizations (covered June 11–12), has claimed **two additional high-profile US victims** with a June 15 leak deadline:

- **American Tower Corporation:** 5.2 million records allegedly compromised, including **customer and landowner PII, GPS coordinates and plaintext physical access codes for cell tower compounds across the United States**, data linked to T-Mobile, Verizon, and the US Department of Homeland Security, plus thousands of internal corporate records. This represents a potential physical security threat to critical communications infrastructure. [[DeXpose/Malware.News](https://malware.news/t/shinyhunters-breach-american-tower-corporation/107836#post_1)]

- **Madison Square Garden Sports Corp.:** 26 million records allegedly compromised, including customer PII and internal corporate data. [[DeXpose/Malware.News](https://malware.news/t/shinyhunters-breach-madison-square-garden-sports-corp/107835#post_1)]

**ShinyHunters' operational tempo is accelerating.** The group exploited CVE-2026-35273 since May 27, notified 100+ orgs by June 9, and by June 12 had claimed two entirely new major victims outside the PeopleSoft campaign. The American Tower breach — with physical cell tower access codes — raises the stakes beyond data theft to **infrastructure access compromise**. Rotate all physical access codes at affected sites as an immediate precaution.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Handala (Iran-Linked) Claims California Water Service Breach — 5GB Data Dump, Destructive Toolkit Deployed**

The Iran-linked threat actor **Handala** (also tracked as Storm-0842, Void Manticore, Homeland Justice) claimed responsibility for hacking **California Water Service's Chico District**, dumping **5 GB of stolen data** including customer billing records, RTKBase GNSS platform credentials, and network enumeration data. [[SecurityWeek](https://www.securityweek.com/iranian-cyber-group-handala-claims-cal-water-hack/)]

**Attack chain per Dataminr:** Initial access likely via Cal Water's **RTKBase platform** (GNSS base station, ~783 continuous hours of operation), with lateral movement to the customer billing database. **Critical concern:** Handala's deployed toolkit includes custom wipers (`win.handala`, `Handala Wiper`, `Hamsa Wiper`) and MBR-overwriting capabilities. Dataminr assesses: *"Security teams should treat the current disclosure as a possible precursor to a destructive follow-on."* Cal Water has not publicly acknowledged the intrusion. Handala framed the attack as retaliation for US actions in Iran and claimed they had the ability to disrupt water access (though unconfirmed). This follows similar Handala targeting of US infrastructure (LA Metro, US troops in Bahrain).

---

**[UPDATE] Conti Ransomware Operator Pleads Guilty — Faces Up to 20 Years**

Oleksii Oleksiyovych Lytvynenko, 44, a Ukrainian national extradited from Ireland, pleaded guilty to conspiracy to commit wire fraud for his role in the **Conti ransomware operation** between 2021 and 2022. Lytvynenko admitted to possessing data stolen from eight US and four overseas victims, and to coding a "loader" malware component used in attacks. Conti targeted 1,000+ victims worldwide, collecting over $150 million in ransom payments before disbanding in 2022. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ukrainian-national-pleads-guilty-to-role-in-conti-ransomware-operation/); [CyberScoop](https://cyberscoop.com/conti-ransomware-member-ukrainian-lytvynenko-guilty/)]

---

**[UPDATE] DragonForce Ransomware Hits Three UAE Targets in Single Day**

DragonForce claimed responsibility for ransomware attacks on three UAE-based organizations: **Al Shafar GRC**, **Al Ishrak Contracting**, and **Cheoy Lee Shipyards**. All three were reported on June 12 with victim data posted to DragonForce's leak site. These are the latest in a sustained campaign against UAE and Middle Eastern targets. [[Malware.News](https://malware.news/t/dragonforce-compromises-al-shafar-grc-in-uae-ransomware-attack/107840#post_1); [Malware.News](https://malware.news/t/dragonforce-targets-al-ishrak-contracting-in-uae-ransomware-attack/107838#post_1); [Malware.News](https://malware.news/t/dragonforce-strikes-cheoy-lee-shipyards-in-ransomware-attack/107837#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] phpBB Patches 10-Year-Old Authentication Bypass — Single HTTP Request Grants Admin Access**

A decade-old authentication bypass vulnerability in **phpBB** (the open-source PHP forum software powering thousands of active forums) allows an attacker to log in as any user — including administrators — with a single HTTP request. Discovered by application security firm Aikido, the flaw affects all phpBB 3.x versions up to 3.3.16 and 4.0.0-a2. **Patched in version 3.3.17** (June 6); no fix yet for 4.x branch. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/phpbb-forum-fixes-auth-bypass-bug-lurking-for-a-decade/); [Aikido](https://www.aikido.dev/)]

Exploitation is trivial — phpBB member lists are public by default, making target selection straightforward. While direct RCE is prevented by a separate password check in the Admin Control Panel, full administrative access means an attacker can read all private messages, modify content, delete accounts, and deface the forum. Aikido has withheld technical details to give admins time to patch but notes that OAuth users may experience breakage due to a relocated redirect handler.

---

**[NEW] Winget DSC + Self-Referencing LNK Attack Bypasses SmartScreen and EDR**

Attackers are abusing **Windows Winget's Desired State Configuration** feature to execute arbitrary PowerShell code through `ConfigurationRemotingServer.exe` — a trusted system process that EDR tools rarely flag. The attack is combined with a self-referencing LNK shortcut that bypasses the manual confirmation prompt entirely, enabling silent, trusted-process-based code execution. [[Malware.News](https://malware.news/t/winget-dsc-and-self-referencing-lnk-file-attack-explained/107841#post_1)]

---

## 📋 Policy & Industry News

**[NEW] Anthropic Pulls Fable 5 and Mythos 5 Offline Following Trump Administration Export Control Directive**

Anthropic removed its latest AI models — **Claude Fable 5** (public release) and **Mythos 5** (restricted release) — from public access after receiving a directive from the Trump administration prohibiting access by foreign nationals. This is described as **the US government's most significant action to date restricting advanced AI model distribution.** [[SecurityWeek/AP](https://www.securityweek.com/anthropic-says-it-has-taken-its-latest-ai-models-offline-to-comply-with-new-export-controls/)]

Anthropic publicly pushed back, stating the directive arrived on a Friday afternoon without specifying the underlying national security concerns: *"We believe the government should have the ability to block unsafe deployments, as part of a statutory process that is transparent, fair, clear, and grounded in technical facts. This action does not adhere to those principles."* The directive was issued 10 days after President Trump signed an executive order creating a federal framework to vet advanced AI systems — which stated participation would be voluntary — while this action appears to leverage mandatory export control authorities.

---

**[UPDATE] Maine Disables Breach Notification Portal After Fraudulent Filings**

Following the June 12 disclosure of fake VRChat and Discord breach filings on Maine's official AG breach portal (covered yesterday), the Maine Attorney General's Office has **temporarily disabled public access** to the breach notification database while reviewing reporting procedures. Companies may still submit disclosures, but public access requires a direct request to the AG's office. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/maine-disables-data-breach-notification-portal-after-fake-disclosures/)]

---

## ⚡ Quick Hits

- **[NEW] Direwolf Ransomware hits Did Asia** — The automotive leader in Vietnam has been targeted in a ransomware attack, with stolen data reportedly posted on the Direwolf leak site. [[Malware.News](https://malware.news/t/direwolf-ransomware-strikes-automotive-leader-did-asia/107839#post_1)]
- **[NEW] Labcorp reaches $35M settlement** — Over the 2019 American Medical Collection Agency breach that exposed 10.2 million patients. The settlement resolves claims from the multi-year litigation over one of the largest healthcare data breaches in US history. [[DataBreaches.net via Malware.News](https://malware.news/t/labcorp-reaches-35m-settlement-over-american-medical-collection-agency-breach/107832#post_1)]
- **[NEW] Google Chrome stable update (CVE-2026-11645)** — Google shipped emergency Chrome updates (Windows 149.0.7827.114, Mac 149.0.7827.115, Linux 149.0.7827.114) for out-of-bounds read/write in V8, following the June 9 patch for the same CVE exploited in the wild. [[Malware.News/Canadian Cyber Centre](https://malware.news/t/google-chrome-security-advisory-av26-593/107824#post_1)]
- **[NEW] FreePBX advisories (AV26-596)** — Authenticated command injection in UCP interface and RCE via unsafe file inclusion in Superfecta module for FreePBX 16/17. Patches available. [[Malware.News/Canadian Cyber Centre](https://malware.news/t/freepbx-security-advisory-av26-596/107830#post_1)]
- **[NEW] Moxa ICS advisory (CVE-2026-9266)** — Missing cryptographic step vulnerability in multiple Moxa industrial computer series (UC-1200A, UC-2200A, UC-3400A, UC-4400A, UC-8200, V1200, V3200/V3400 series). Patches available. [[Malware.News/Canadian Cyber Centre](https://malware.news/t/control-systems-moxa-security-advisory-av26-594/107826#post_1)]

---

*46 articles ingested from Miniflux Cyber feeds. External cross-referencing via Reddit skipped — Saturday light-volume handling. Prior digests: June 8–12, 2026. Stale CVE/topic blocklist applied. Sources include BleepingComputer, CyberScoop, SecurityWeek, AP, Rapid7, Malware.News/DeXpose, Zscaler ThreatLabz, Unit 42 (Palo Alto Networks), Sonatype, IFIN/Whanos, Dataminr, DataBreaches.net, Aikido, and the Canadian Centre for Cyber Security.*
