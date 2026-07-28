---
title: "🔴 FastJson RCE Active Exploitation, 🔴 Arista/Fortinet CISA KEV Adds, 🎯 Dysphoria Botnet 200K Devices, 🎯 EY Breach Claimed by ShinyHunters, ⚠️ Certighost AD CS PoC, 📋 Wyden Urges Legacy VPN Purge"
date: 2026-07-28
tags: ["fastjson","cve-2026-16723","rce","zero-day","arista","velocloud","fortinet","cisa-kev","dysphoria","botnet","shinyhunters","ernst-young","certighost","ad-cs","active-directory","ransomware","clop","open-secure-ai-alliance","nvidia","microsoft-project-perception","origin-energy","data-breach"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "FastJson RCE zero-day actively exploited against US firms with no patch available; CISA adds Arista VeloCloud (CVSS 10.0) and Fortinet FortiOS to KEV; Dysphoria DDoS botnet reaches 200K devices using blockchain C2; ShinyHunters claims Ernst & Young breach with July 31 deadline; Certighost AD CS PoC exploit enables domain takeover; Nvidia launches Open Secure AI Alliance with 40+ partners."
---
# Daily Threat Intelligence Digest — July 28, 2026

28 articles ingested from cyber feeds (BleepingComputer, SecurityWeek, CyberScoop, Qualys, Microsoft). Gap detection via CISA KEV alert identified Fortinet FortiOS CVE-2025-68686 addition. Prior-digest continuity cross-referenced against Jul 23–27 — multiple stories are updates with new information. FastJson CVE-2026-16723 and Certighost CVE-2026-54121 (first reported as gaps Jul 26) now carrying detailed reporting.

---

## 🔴 Critical Threats & Active Exploitation

### [UPDATE] FastJson CVE-2026-16723: Active RCE Exploitation Continues — No Patch Available

*Previously identified as a gap on Jul 26. New today: BleepingComputer and SecurityWeek carry confirmed targeting details from Imperva and ThreatBook.*

Hackers are actively exploiting **CVE-2026-16723** (CVSS 9.0), an unauthenticated remote code execution vulnerability in Alibaba's **FastJson** Java library affecting versions 1.2.68 through 1.2.83. The flaw works under FastJson's default configuration — no AutoType enablement required, no classpath gadget required.

**New details confirmed by Imperva and ThreatBook:**
- Attacks target **Financial Services, Healthcare, Computing, Retail, and Business** sectors
- Focused primarily on **US-based organizations**, with some attacks in Singapore and Canada
- Roughly **30% of observed attacks originate from Ruby and Go tools**; the rest from browser impersonators
- Exploitation achieved via crafted JSON `@type` values to trigger resource lookups that bypass AutoType restrictions
- **No patched FastJson 1.x release exists** — Alibaba published an advisory on July 21 but has not shipped a fix for the 1.x branch
- **Only mitigation**: migrate to FastJson 2.x or enable SafeMode

Organizations running FastJson 1.x behind internet-facing Spring Boot services have no straightforward patch to apply. Any exposed service processing untrusted JSON should be treated as high-priority remediation.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-target-us-firms-in-fastjson-rce-zero-day-attacks/) · [SecurityWeek](https://www.securityweek.com/unpatched-fastjson-vulnerability-exploited-in-attacks/) · Imperva · ThreatBook

### CISA Adds Two Exploited Vulnerabilities to KEV — Arista VeloCloud (CVSS 10.0) and Fortinet FortiOS

**CISA added two CVEs to its Known Exploited Vulnerabilities (KEV) catalog on July 27:**

**CVE-2026-16812 — Arista VeloCloud Orchestrator OS Command Injection (CVSS 10.0)**
- Unauthenticated remote attacker can execute OS commands on VCO with no login required
- Patched by Arista in versions 5.2.3.14, 6.1.3.4, 6.4.2.4, 7.0.0.1
- VCO is designed to be internet-exposed; no configuration can prevent this
- Attackers only need network access to the VCO web interface — no credentials required
- Arista published attacker IP addresses in its advisory

**CVE-2025-68686 — Fortinet FortiOS Information Disclosure (CVSS 5.3)**
- Patch bypass vulnerability — restores a symlink persistence trick used after an earlier breach
- Affects FortiOS 7.6.0–7.6.1, 7.4.0–7.4.6, and all 7.2, 7.0, and 6.4 releases
- Patched in FortiOS 7.6.2 and 7.4.7
- Enables an attacker to maintain read access to sensitive files despite a prior fix

The pairing is notable: one (Arista) grants full system takeover; the other (Fortinet) quietly preserves access for already-compromised systems.

**Action:** Apply patches immediately. For Arista VCO, no workaround is available — patch or isolate. For FortiOS, migrate older trains to supported builds. Hunt for signs of prior compromise on both.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/arista-patches-velocloud-orchestrator-zero-day-exploited-in-attacks/) · [SecurityWeek](https://www.securityweek.com/critical-arista-velocloud-orchestrator-vulnerability-exploited-as-zero-day/) · [CISA](https://www.cisa.gov/news-events/alerts/2026/07/27/cisa-adds-two-known-exploited-vulnerabilities-catalog) · [SecurityOnline](https://securityonline.info/cisa-kev-arista-velocloud-fortios/)

### [UPDATE] MCBS Data Breach Official Count: 1,261,464 Individuals — PEAR Ransomware Claims Responsibility

*Previously covered Jul 27 (1.2M, PEAR ransomware claim). New today: BleepingComputer reports the official HHs disclosure with confirmed count and specific covered entities named.*

Atlanta-based Medical Computer Business Services (MCBS) has officially disclosed that the September 2025 network breach impacted **1,261,464 individuals** in a filing with the U.S. Department of Health and Human Services. The PEAR ransomware group previously took credit for the attack, claiming 3 TB of stolen data.

Exposed data varies per individual and includes: full name, SSN, DOB, address, health plan beneficiary numbers, health insurance policy numbers, medical history, treatment information, and diagnosis data.

Seven "covered entities" whose patient data was routed through MCBS were named in the notification. MCBS processes patient records for healthcare providers as a billing and practice-management intermediary.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/data-breach-at-medical-billing-firm-mcbs-affects-126-million-people/)

---

## 🎯 Threat Actor Activity & Campaigns

### Dysphoria DDoS Botnet Reaches 200,000 Devices with Blockchain-Based C2

A botnet called **Dysphoria** has compromised approximately 200,000 devices globally and is being used for DDoS attacks and traffic relay operations, according to **QiAnXin XLab** researchers.

Key technical details:
- Evolved from **JackSkid** and **FBot** malware families
- Uses **Ethereum ENS** and **Solana SNS** domains for covert C2 resolution
- C2 addresses hidden inside **fake IPv6 strings**, recovered via custom byte-transformation algorithm
- First spotted March 25, 2026; has undergone multiple rapid variant updates
- Functional separation between DDoS variants and relay variants
- Use of blockchain infrastructure makes takedown significantly harder than traditional DNS-based botnets

**Hunting hypothesis:** Monitor for unusual ENS/SNS DNS queries from endpoints that should not be resolving blockchain domains. Investigate devices with anomalous outbound traffic on non-standard ports.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-dysphoria-ddos-botnet-spreads-to-200k-devices-worldwide/) · QiAnXin XLab

### ShinyHunters Claims Ernst & Young Data Breach, Sets July 31 Extortion Deadline

The **ShinyHunters** extortion gang has claimed responsibility for the recently disclosed **Ernst & Young** data breach, stating it obtained credentials via a supply-chain attack against a third-party support ticket system used by EY's IT personnel.

Timeline:
- **March 28 – April 12:** Attacker accessed the third-party IT service management platform
- **April 23:** EY detects unusual activity
- **July 2026:** EY discloses breach; support tickets containing client tax information were stolen
- **July 27:** ShinyHunters adds EY to its leak site, threatens data release if EY does not contact them by **July 31, 2026**

EY has not disclosed the name of the compromised support system, the specific data types exposed, or how many individuals are affected. This is the latest in a series of high-profile ShinyHunters-related breaches, following the sextortion campaign documented Jul 26 that used ShinyHunters' previously leaked data.

**Action:** Organizations that use EY for tax services should prepare for potential downstream phishing or fraud targeting employees whose data may have been exposed in the support tickets.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/ernst-and-young-data-breach-claimed-by-shinyhunters-extortion-gang/)

### [UPDATE] Coca-Cola Confirms Data Theft in Fairlife Ransomware Attack

*Previously reported Jul 16 (ransomware attack disclosed to SEC). New today: Coca-Cola now confirms data was stolen during the attack.*

Coca-Cola has confirmed that hackers stole data from its dairy subsidiary **Fairlife** during a ransomware attack earlier this month. The **Anubis ransomware gang** claimed responsibility and threatened to leak 1 TB of files. Most US production has resumed, though some systems remain non-operational.

The confirmation shifts this incident from a production disruption to a confirmed data breach with extortion risk.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/coca-cola-confirms-data-theft-in-fairlife-ransomware-attack/) · [SecurityWeek](https://www.securityweek.com/coca-cola-confirms-data-breach-after-fairlife-ransomware-attack/)

### [UPDATE] Cl0p Ransomware Windchill/FlexPLM Campaign — New Details from ReliaQuest, Ransom-ISAC

*Previously covered Jul 24 (Clop exploiting CVE-2026-12569). New today: ReliaQuest and Ransom-ISAC publish detailed campaign analysis with new IoCs.*

A **Cl0p ransomware affiliate** continues exploiting **CVE-2026-12569** (CVSS 9.3) in PTC Windchill and FlexPLM enterprise PLM systems. New campaign intelligence:

- Attack chain: pre-authentication information disclosure in FlexPLM WSDL endpoint chained with server-side flaw in Windchill login servlet to achieve RCE and deploy JSP webshells
- **Campaign active since July 20**, targeting **aerospace, automotive, manufacturing, and retail/apparel** sectors
- Attackers enumerate filesystems, stage data, and exfiltrate for extortion
- Extortion emails sent with subject line **"Windchill PDMLink module serious data leak"** to hundreds of users per victim
- As of July 22, Cl0p has not yet listed victims on its dark web leak site

**Action:** Patch CVE-2026-12569 immediately. Hunt for JSP webshells under `/Windchill/login/`. Block extortion email domains. CISA added this CVE to KEV on June 25 — any internet-exposed, unpatched instance should be treated as potentially compromised.

**Source:** [SecurityWeek](https://www.securityweek.com/ptc-windchill-vulnerability-exploited-in-ransomware-campaign/) · ReliaQuest · Ransom-ISAC

---

## ⚠️ Vulnerabilities & Patches

### [UPDATE] Certighost CVE-2026-54121: Public PoC Enables Low-Privilege AD CS Domain Takeover

*Previously identified as a gap on Jul 26. New today: BleepingComputer reports exploit release with full technical detail.*

A proof-of-concept exploit for **Certighost** (CVE-2026-54121) has been publicly released. The vulnerability in **Active Directory Certificate Services** allows any authenticated domain user — with no admin rights — to impersonate a **Domain Controller** and extract the **krbtgt secret**, enabling full Active Directory domain compromise.

Key details:
- Discovered by researchers **H0j3n** and **Aniq Fakhrul**, reported to Microsoft May 14, 2026
- Patched in **July 14, 2026 Patch Tuesday** (2 weeks ago)
- Attacker manipulates machine account attributes to obtain a certificate allowing authentication as that machine via PKINIT
- Targeting a Domain Controller account enables privileged AD operations

**Action:** If not already patched, apply the July 14 Microsoft update immediately. After patching, audit AD CS for signs of abuse — look for unexpected certificate requests from non-DC machines, anomalous Kerberos TGT requests, and unauthorized certificate templates. Given the patch is 2 weeks old and PoC code is now public, expect scanning activity.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-certighost-poc-exploit-lets-attackers-hijack-windows-domains/)

### MedusaHVNC Malware Sold as MaaS Uses Hidden Windows Desktops for Stealth

Security researchers at **BlackFog** have analyzed **MedusaHVNC**, a remote access trojan sold as malware-as-a-service (MaaS) via its own website and Telegram channel. The malware uses Windows' legitimate hidden desktop capability to operate completely invisibly to the user.

Infection chain (5 stages):
1. **wscript.exe** executes a JScript launcher (7.5-second delay)
2. Drops files to `%TEMP%\Nx2981Okkr2\` including encrypted payload and `.bat` in Startup folder for persistence
3. **AutoIT** decrypts payload and starts **charmap.exe** (Windows Character Map — LOLBIN)
4. Two-layer decryption: 16-byte repeating XOR on 1M+ bytes, then **ChaCha20** with 32-byte key
5. Final payload communicates with hardcoded C2: **51.89.204.28:4444**

The operator can launch Chrome, Edge, or Firefox within a hidden desktop, invisible to the victim. Uses legitimate Windows functions (BitBlt, SendInput, SetWindowsHookExW, clipboard APIs) for screen capture and interaction.

**Detection:** Since the hidden desktop is a legitimate Windows feature, detection relies on identifying unexpected data exfiltration rather than behavioral monitoring of the desktop itself.

**Source:** [SecurityWeek](https://www.securityweek.com/medusahvnc-malware-uses-hidden-windows-desktops-to-evade-detection/) · BlackFog

### Qualys: Sub-10-Minute Cloud Takeovers — Exposed IAM Keys Accelerate Attacks

Qualys Threat Research published a detailed analysis of two real-world cloud attacks that reached meaningful impact in less than 10 minutes:

**Attack 1 — Crypto Mining:** Compromised AWS credentials enabled deployment of crypto mining infrastructure across EC2 and ECS within **ten minutes** of initial access.

**Attack 2 — AI Model Abuse:** Exposed AWS access key in a publicly accessible S3 bucket enabled privilege escalation across **19 AWS principals**, unauthorized use of **Amazon Bedrock models**, and broader cloud resource abuse in **under eight minutes**.

Key takeaway: The interval between initial access and operational impact is shrinking dramatically. Attackers treat cloud environments as connected systems, using existing permissions and relationships to expand reach. AI is compressing the gap between discovery, decision-making, and execution.

**Source:** [Qualys](https://blog.qualys.com/product-tech/2026/07/27/the-sub-10-minute-cloud-takeover-how-exposed-iam-keys-misconfiguration-and-ai-are-rewriting-the-rules-of-cloud-breaches/)

---

## 🛡️ Defense & Detection

### Nvidia + 40 Tech Giants Launch Open Secure AI Alliance

Nvidia and a coalition of over 40 technology, cybersecurity, and enterprise software companies announced the **Open Secure AI Alliance**, an initiative to develop and share open source tools, models, and techniques for securing AI systems and agents. Inaugural partners include Adobe, Cisco, Cloudflare, CrowdStrike, Databricks, Dell, Elastic, HPE, Hugging Face, IBM, LangChain, Microsoft, Nous Research, Palantir, Palo Alto Networks, Red Hat, Salesforce, ServiceNow, Snowflake, and others.

Key contributions:
- **Nvidia:** NOOA — open source project for tracing, testing, and auditing agent behavior
- **HPE:** SPIFFE/SPIRE zero-trust identity framework for AI agents
- **Hugging Face:** Donating Safetensors model weight storage format to PyTorch Foundation
- **IBM/Red Hat:** Lightwell project for automated vulnerability remediation at scale
- **Microsoft:** MDASH — multi-model agentic scanning harness for software bug discovery
- **SpaceXAI:** Open-sourcing Grok Build terminal-based AI coding agent; plans to eventually open-source Grok model weights

The alliance argues that open models and security tooling are defensive assets. Nvidia specifically cited the recent OpenAI/Hugging Face incident: when closed AI tools blocked forensic work, Hugging Face used open-weight GLM 5.2 to review 17,000+ actions and contain the breach.

**Source:** [SecurityWeek](https://www.securityweek.com/nvidia-and-tech-giants-launch-ai-security-alliance/)

### Microsoft Launches Project Perception with MAI-Cyber-1-Flash Model

Microsoft unveiled **Project Perception**, an AI-powered security platform centered on a new agentic model called **MAI-Cyber-1-Flash**, which runs inside Microsoft's **MDASH** security tool. The platform brings together signals, context, models, and specialized agents into "a continuously learning system of defense" that can "reason, prioritize and act at machine speed while keeping humans firmly in control."

The announcement positions Microsoft alongside OpenAI and Anthropic in the increasingly competitive AI cybersecurity market. Microsoft's argument is that its existing in-house capabilities — including its threat intelligence from the Digital Crimes Unit, Defender suite, and Entra ID telemetry — give Project Perception an edge over rivals.

Separately, Microsoft announced **EXTRA (External Red Team Alliance)**, a formalized global extension of its AI Red Team. The initiative provides unrestricted gifts to **18 universities on six continents** to advance AI safety and security research, covering security operations, misuse scenarios, multilingual harms, alignment failures, and domain-specific abuse patterns.

**Sources:** [CyberScoop](https://cyberscoop.com/microsoft-ai-cybersecurity-project-perception/) · [Microsoft](https://blogs.microsoft.com/blog/2026/07/27/rethinking-security-for-the-age-of-ai/) · [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/27/enhancing-ai-security-through-global-ai-red-teaming/)

### Google Adopts New Threat Actor Naming System — Drops APT Conventions

Google announced a new naming system for threat actors it tracks, moving away from APT-number conventions to **cryptonym-based naming**. The system abandons numeric designations in favor of descriptive codenames, similar to the approach taken by Microsoft and other vendors.

SecurityWeek notes the change means "security teams now have one more naming system to keep straight," as Google joins Microsoft, CrowdStrike, Mandiant, and others in maintaining independent naming taxonomies. Google previously used APT designations (e.g., APT29, Sandworm) aligned with the wider industry convention.

The fragmentation of naming systems continues to be a challenge for threat intelligence sharing, though Google argues its new system better describes actor behavior and targeting rather than arbitrary numbers.

**Sources:** [CyberScoop](https://cyberscoop.com/google-threat-actor-naming-system/) · [SecurityWeek](https://www.securityweek.com/google-adopts-new-threat-actor-naming-system/)

---

## 📋 Policy & Industry News

### Sen. Wyden Urges Federal Purge of Legacy Public-Facing VPNs

Sen. **Ron Wyden** (D-Ore.) sent a letter to the Office of Management and Budget, CISA, and NIST calling for a coordinated campaign to eliminate legacy, insecure public-facing VPNs across the federal government.

Wyden's letter cites a string of high-profile VPN-related attacks affecting federal agencies: the **ArcaneDoor** attacks on Cisco firewalls, **FortiBleed** credential exposures across Fortinet gateways, and vulnerabilities exploited in **Ivanti** and **Check Point** VPN appliances.

"Modern remote-access solutions eliminate this vulnerability entirely," Wyden wrote, calling on agency leaders to "require the adoption of modern, secure remote-access technology" using zero-trust principles.

**Significance:** This represents the most direct congressional pressure yet on federal agencies to accelerate zero-trust remote access adoption. Organizations contracting with the federal government should anticipate similar requirements flowing down.

**Source:** [CyberScoop](https://cyberscoop.com/wyden-calls-for-federal-legacy-vpn-purge-zero-trust/)

### Origin Energy Data Breach Affects 900,000 Australians

**Origin Energy**, one of Australia's largest electricity and gas retailers with 4.8 million customers, confirmed a data breach affecting **900,000 current and former customers**. Exposed data includes names, DOBs, phone numbers, addresses, account information, and partial payment card or bank account numbers.

The company began investigating a "potential security threat" in early July. New information on **July 22** confirmed the intrusion. An individual claiming to be the attacker told a news outlet that **2 million customer records** were obtained and, later, that an agreement had been reached with Origin for no data release. Origin has not confirmed any agreement and stated the matter is under criminal investigation.

Origin warned customers that even if data is not released, other threat actors could leverage the incident for scams.

**Source:** [SecurityWeek](https://www.securityweek.com/origin-energy-data-breach-affects-900000-australians/)

### Apple Sued Over Fake App Store Crypto Wallet — $1.8M in Bitcoin Stolen

Three individuals are suing Apple for approximately **$1.8 million in Bitcoin** stolen after downloading and using a fraudulent **Sparrow Wallet** application from the official App Store. The complaint, filed July 24 in California, alleges Apple failed to adequately review App Store applications while promoting the marketplace as a safe and trusted source.

The legitimate Sparrow Wallet is a desktop-only application (Windows, macOS, Linux) — no iOS version exists. Scammers have repeatedly published impersonating apps in the App Store, the real Sparrow Wallet developer states.

Three victims lost a total of approximately **$1.8M** between May 2024 and July 2025. The lawsuit argues Apple's review process is insufficient to prevent obvious impersonation attacks.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/apple/apple-sued-over-fake-app-store-crypto-wallet-app-stealing-18m-in-bitcoin/)

---

## Gap Detection

| Source | Story | Status | Action |
|--------|-------|--------|--------|
| CISA KEV alert (Jul 27) | **CVE-2025-68686 Fortinet FortiOS** — added to KEV as patch bypass vulnerability | ✅ Incorporated into Critical Threats section |
| | **CVE-2026-16812 Arista VeloCloud** — added to KEV (CVSS 10.0) | ✅ Already covered from feed articles, KEV addition noted |
| r/cybersecurity hot | Trending stories (career discussions, Lavender/AI warfare opinion, Skynet Day reflections) — no critical unindexed security stories | No action — Skynet Day/OpenAI HF incident already covered in prior digests; others non-security |
| General web scan | No significant unindexed stories identified outside CISA KEV addition | No action |

---

## Stories Excluded from Today's Digest

- **SourTrade malvertising** (SOCFortress Medium) — same story already covered via BleepingComputer in Jul 26 digest; no new information
- **GitHub/PyPI supply chain policies** (SecurityWeek) — same story already covered in Jul 27 digest
- **Shadow AI agents** (BleepingComputer) — sponsored content from Nudge Security; no independent threat intelligence
- **"Skynet Day" retrospective** (SecurityWeek/AP) — opinion feature about OpenAI/Hugging Face incident already covered in Jul 22–23 digests
- **PTC Windchill** (SecurityWeek) — covered as UPDATE above with new ReliaQuest/Ransom-ISAC details; standalone SW article used for sourcing
- **Trump mail-in voting** (CyberScoop) — not cybersecurity
- **Qualys AWS Lambda scanning** (Qualys) — vendor product announcement, not threat intelligence
- **Microsoft "Rethinking security" blog** — duplicative of Project Perception announcement already covered

---

*Digest generated July 28, 2026. 28 feed articles reviewed, 5 prior digests cross-referenced for continuity, CISA KEV alert monitored for additions. Stories excluded as already covered in prior digests or non-security: SourTrade (Jul 26), GitHub/PyPI policies (Jul 27), Shadow AI agents (sponsored), Skynet Day/OpenAI HF reflection (Jul 22–23), Trump voting politics.*
