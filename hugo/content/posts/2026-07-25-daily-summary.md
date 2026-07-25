---
title: "🎯 Hermes Agent Weaponized in Bangkok, 🎯 Hotel Wi-Fi DNS Hijacks M365, 🎯 Botnets Hit 60M IPs, ⚠️ Rockwell Arena Flaws Patched, 📋 CIRCIA Pushback, 📋 Europol Com Crackdown"
date: 2026-07-25
tags: ["Hermes AI agent","Thai Finance Ministry","DNS hijacking","APT28","botnets","TrickBot","Rockwell Arena","CIRCIA","Europol","Slopsquatting","cyber threat intelligence"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "First documented case of an open-source AI agent weaponized against a government ministry, APT28-linked hotel Wi-Fi DNS hijack campaign, botnet ecosystem surpasses 60M IPs, Rockwell patches Arena Simulation flaws, industry pushes back on CIRCIA reporting rules, and Europol flags 4,340 URLs in 'The Com' crackdown."
---

# Daily Threat Intelligence Digest — July 25, 2026

19 articles ingested and analyzed from curated cyber intelligence feeds. Prior-digest continuity tracked across Jul 22–24. Gap detection via web search (r/cybersecurity, CISA KEV) surfaced no unindexed critical stories. Cross-reference confirmed Chick-fil-A as UPDATE from Jul 22.

---

## 🎯 Threat Actor Activity & Campaigns

### Hermes AI Agent Used to Automate Post-Exploitation in Thai Finance Ministry Attack

A threat actor deployed the **open-source Hermes AI agent** in unattended **"YOLO" mode** to automate post-exploitation activity during an alleged breach of **Thailand's Ministry of Finance**. The activity was uncovered by **Hunt.io** and researcher **Bob Diachenko** after discovering three exposed web directories on a Hong Kong-hosted server containing **585 files (~470 MB)** of exploit code, web shells, HTTP tunneling tools, custom scripts, stolen credentials, compiled payloads, and Hermes AI agent logs.

Recovered files referenced Ministry of Finance systems by name, hostname, and internal IP address. Scripts targeted the ministry's **Hadoop infrastructure, Apache Ambari, and GlassFish** servers. The Ministry of Finance has not confirmed the breach, and some artifacts only indicate targeting rather than successful compromise.

**Significance:** This is the first publicly documented case of an open-source AI agent operating in fully unattended mode being used in a real-world attack chain. The YOLO mode setting gives the AI unrestricted decision-making authority over post-exploitation actions, raising urgent questions about how defenders should model AI-enabled threat actors. Defenders should assume AI-assisted intrusion automation will become more common — hunt for anomalous tool execution sequences that lack the pauses and latencies of human interaction.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hermes-ai-agent-used-to-automate-attack-on-thai-finance-ministry/) · Hunt.io

---

### Hackers Hijack Hotel Wi-Fi DNS to Steal Microsoft 365 Accounts

A campaign active since **June 2026** is compromising **Wi-Fi gateways at hotels and conference centers** to redirect users to fake Microsoft 365 login pages. **ReliaQuest** identified compromised gateways across multiple U.S. cities, India, and Saudi Arabia, affecting organizations in financial services, professional services, legal, health care, energy, and retail.

Attack chain:
- Initial access likely through weakly protected management interfaces (SSH, SNMP, web admin dashboards) or unpatched vulnerabilities on Wi-Fi appliances
- Attacker changes DNS settings to redirect traffic to phishing pages capturing M365 credentials
- Since devices serve corporate events, hijacking accounts gives access to **sensitive business information and communications**

ReliaQuest assesses the activity is similar to the **FrostArmada** router-based campaigns attributed to **APT28 (Fancy Bear / Forest Blizzard)**. The campaign is non-sector-specific, targeting traveling employees wherever they connect.

**Action:** Enforce MFA resistant to real-time proxy attacks (FIDO2/WebAuthn) for all corporate M365 accounts. Advise traveling employees to avoid using hotel Wi-Fi for work authentication without a corporate VPN. Auditors should review hotel and conference center Wi-Fi provider security postures for event security planning.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-hijack-hotel-wi-fi-dns-to-steal-microsoft-365-accounts/)

---

### Botnet Ecosystem Surpasses 60 Million IPs as Residential Proxy Networks Proliferate

**Lumen Technologies' Black Lotus Labs** published a report Friday documenting the accelerating growth of **residential proxy-based botnets**. Key findings:

- **~60 million victim IP addresses** observed globally; ~1 in 4 in the United States
- **10 distinct "super-sized" botnets** each controlling ~1 million active victims daily
- **IPIDEA** — one of the largest residential proxy networks — recovered to **nearly half-strength within hours** of its January takedown and has now surpassed its pre-disruption size at **~10 million IPs**
- The demand market for residential proxies fuels rapid rebuild capabilities — takedowns provide only temporary disruption

**Takeaway:** Residential proxy networks have become resilient infrastructure-as-a-service for cybercriminals. Traditional botnet takedowns provide diminishing returns as the commercial market for anonymized IP access hardens. Defenders should focus on behavioral detection of proxy-rotated traffic rather than IP-based blocklisting.

**Source:** [CyberScoop](https://cyberscoop.com/botnets-residential-proxy-networks-proliferate-lumen-black-lotus-labs/) · [Lumen Blog](https://www.lumen.com/blog/en-us/symbiotic-parasites-the-modern-proxy-ecosystem)

---

### TrickBot Reborn: DNS Tunneling Enables Stealth C2 Communication

**SOCFortress** published analysis of a revived **TrickBot** variant that uses **DNS tunneling** for command-and-control communication, allowing the malware to blend its traffic with legitimate DNS queries and bypass network security controls.

The technique encodes stolen data and commands within DNS query and response packets, making detection through traditional network monitoring difficult. DNS tunneling is a well-known evasion method, but its adoption by a mature malware family like TrickBot signals continued evolution of the botnet's capabilities.

**Hunting hypothesis:** Monitor for anomalous DNS query patterns — unusually long subdomains, high query volumes to the same domain, or TXT/ANY record queries from endpoints that do not typically perform DNS resolution at that volume.

**Source:** [SOCFortress (Medium)](https://socfortress.medium.com/trickbot-reborn-stealth-c2-communication-via-dns-tunneling-e049d1de673a)

---

## ⚠️ Vulnerabilities & Patches

### Rockwell Patches Four Code Execution Flaws in Arena Simulation Software

**Rockwell Automation** has patched four high-severity memory corruption vulnerabilities in its **Arena Simulation** software — **CVE-2026-8085, CVE-2026-8312, CVE-2026-8313, and CVE-2026-8314**. The flaws result from improper validation of user-supplied data, causing out-of-bounds writes that could allow arbitrary code execution in the context of the current process.

- Affects Arena versions up to **17.00.00**; patched in **17.00.01**
- Exploitation requires user interaction — target must open a malicious `.doe` or `.sim` file
- Arena is used by **top global supply chain companies, hospitals, and defense contractors** for discrete-event simulation
- Researcher **Michael Heinzl** discovered **17 distinct vulnerabilities** in total; Rockwell grouped them into four CVEs
- **No evidence of in-the-wild exploitation**

While Arena does not directly control physical processes, successful exploitation could allow an attacker to pivot from a compromised simulation workstation to more sensitive network segments depending on deployment architecture.

**Action:** Update to Arena 17.00.01. Review network segmentation for simulation workstations. Treat `.doe` and `.sim` files from untrusted sources similarly to Office documents with macros.

**Source:** [SecurityWeek](https://www.securityweek.com/rockwell-patches-code-execution-flaws-in-arena-simulation-software/)

---

### Slopsquatting, Phantom Domains, and HalluSquatting — Unified AI Coding Agent Attack Vector

**ActiveState's** Shane Warden synthesizes three independently named attacks into a single observation: **AI coding agents hallucinate package names, repositories, and domains that sound real but do not exist**, and attackers can predict and pre-register those names to deliver malware.

Key findings from researchers at **Tel Aviv University, Technion, and Intuit** (published July 8, 2026, led by Aya Spira / Ben Nassi):
- Multiple AI coding agents (Cursor, Windsurf, GitHub Copilot, Cline, Gemini CLI, OpenClaw) hallucinated **identical names up to 85% of the time** for repository requests
- For skill installs, hallucination consistency reached **100%**
- The attack requires no phishing, no stolen credentials, no human clicking a link — just an automated process given permission to fetch

The attacks converge on "**Slopsquatting**" (fake package names), "**Phantom Domains**" (fake domain names), and "**HalluSquatting**" (fake repos/skills). Warden notes the ultimate payoff in one observed case was botnet enrollment via a hallucinated package.

**Action:** Pin dependency versions and hashes in CI/CD. Implement approval gates for packages fetched by AI coding assistants. Treat AI-generated dependency names as unverified until resolved against package registries. Train developers that compiler/CI passing is insufficient validation for AI-suggested dependencies.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/slopsquatting-phantom-domains-and-hallusquatting-are-the-same-ai-attack/)

---

## 📋 Policy & Industry News

### Industry's Message on CIRCIA: "Please Ask Us Fewer Questions"

**CISA's** public town halls on implementing the **Cyber Incident Reporting for Critical Infrastructure Act (CIRCIA)** — the 2022 law requiring critical infrastructure owners to report major cyberattacks within 72 hours and ransomware payments within 24 hours — produced consistent industry messaging: reduce the rule's scope, fewer incident triggers, less required information.

CISA has missed two deadlines for finalizing the rule (October 2025 and May 2026). The administration now targets completion by late 2026. Industry groups continue to press for narrower definitions of "covered cyber incident" and reduced reporting obligations.

The transcripts, published last week, show the fundamental tension at the heart of CIRCIA: CISA wants comprehensive threat visibility to protect the broader ecosystem; industry wants to minimize regulatory burden and legal exposure from mandatory disclosure.

**Source:** [CyberScoop](https://cyberscoop.com/cisa-circia-cyber-incident-reporting-rule-feedback/)

---

### Europol Flags 4,340 URLs for Removal in 'The Com' Crackdown

**Europol** announced the results of "**Referral Action Days**" (June–July 2026) targeting online content from **The Com**, a loosely organized nihilistic violent extremist network. Investigators from **nine countries** (Belgium, Finland, Hungary, Ireland, Luxembourg, the Netherlands, Portugal, Spain, and Sweden) flagged 4,340 URLs for removal.

The operation, coordinated by Europol's EU Internet Referral Unit (EU IRU) and Spain's CITCO, targeted content including violent videos depicting self-harm, suicide, CSAM, animal cruelty, and "manhunt" street attacks. The Com's content uses coded language and emojis to convey messages encouraging self-harm and sexual exploitation of minors.

The operation ties into the European Commission's **ProtectEU** counterterrorism agenda and aims to disrupt the group's online ecosystem and generate new investigative leads.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/europol-flags-4-340-urls-for-removal-in-the-com-crackdown/) · Europol

---

### Microsoft Leads 25+ Tech Companies in Open Letter Supporting Open-Source AI

**Microsoft**, joined by more than two dozen tech companies, published an open letter urging policymakers to **support open-source AI systems and code**, arguing that an open ecosystem is a safer approach than restricting access or relying on a handful of closed proprietary models.

The letter draws parallels to the 1980s software industry, where large businesses opposed open-source software but ultimately lost to a model that now underpins the modern internet. "Our AI leadership will be judged not by one frontier AI model, but by whether the United States builds a strong, open ecosystem that diffuses into every sector."

Cybersecurity experts note the tension: while open AI access democratizes innovation, it also arms low-level criminals who previously lacked the resources to launch sophisticated attacks.

**Source:** [CyberScoop](https://cyberscoop.com/tech-leaders-open-source-ai-cybersecurity/) · Microsoft

---

### Also Notable

- **OnTrac data breach** — Parcel delivery company OnTrac notifies customers that attackers breached its corporate network between March 20–22, accessing files containing customer personal details. The company's language suggests a possible ransom payment to prevent data publication. ([BleepingComputer](https://www.bleepingcomputer.com/news/security/ontrac-notifies-customers-of-data-breach-after-network-hack/))

- **Man sentenced to 6 years for hacking 750 women's Snapchat accounts** — Illinois man Kyle Svara, 26, received 76 months in prison after pleading guilty to phishing Snapchat access codes from over 750 women between May 2020 and February 2021. He targeted more than 4,500 victims and also possessed CSAM. ([BleepingComputer](https://www.bleepingcomputer.com/news/security/man-gets-six-years-for-hacking-750-womens-snapchat-accounts/))

- **[UPDATE] Chick-fil-A confirms 13,000+ customers affected in credential stuffing attacks** — Previously reported Jul 22. New today: confirmed count of 13,000+ affected customers as disclosed in breach notification letters filed with attorney general offices. Attackers targeted Chick-fil-A One loyalty accounts between June 17–19 using credentials obtained from third-party sources. ([BleepingComputer](https://www.bleepingcomputer.com/news/security/chick-fil-a-data-breach-affects-more-than-13-000-customers/))

---

### Gap Detection

- **r/cybersecurity hot**: No stories missed — the Reddit hot page's top security story was the hotel Wi-Fi DNS hijack (already captured).
- **CISA KEV**: No new additions since July 22 (6 CVEs added Jul 21–22, already covered in prior digests).
- **General news scan**: No significant unindexed stories identified.

---

*Digest generated July 25, 2026. 19 feed articles reviewed, 3 prior digests cross-referenced for continuity, gap detection via web search. Excluded as already covered in prior digests: Dolphin X AI malware (Jul 23), OpenAI/Hugging Face industry reactions (Jul 22–24), check-point zero-day CVE-2026-16232 (Jul 23).*
