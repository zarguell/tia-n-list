---
title: "🔴 Check Point SmartConsole Zero-Day KEV, 🎯 Iranian ICS Attacks Target Siemens/Schneider, ⚠️ RefluXFS Linux LPE, 🛡️ Supply Chain Worm Wave Hits npm/PyPI, 📋 Suno 55M Breach"
date: 2026-07-23
tags: ["check-point","cve-2026-16232","ics-security","iran","linux-kernel","supply-chain","npm","pypi","data-breach","sharepoint","ai-security","langflow","ransomware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA adds Check Point SmartConsole zero-day to KEV with July 25 deadline; US warns Iranian hackers now targeting Siemens, Schneider, and Rockwell ICS PLCs; RefluXFS Linux kernel LPE in XFS (CVE-2026-64600) gives root even with SELinux; GitGuardian documents four more npm/PyPI supply chain attacks including IronWorm with eBPF rootkit; Suno (55.3M) and Paidwork (23.3M) data breaches exposed via HIBP."
---

# Daily Threat Intelligence Digest — July 23, 2026

28 articles ingested and analyzed from curated cyber intelligence feeds. One duplicate pair (Check Point zero-day) merged. Prior-digest continuity tracked across SharePoint, Langflow, supply-chain worms. Gap detection: no unindexed critical stories found.

---

## 🔴 Critical Threats & Active Exploitation

### CVE-2026-16232 — Check Point SmartConsole Zero-Day Actively Exploited; CISA Adds to KEV

Check Point Software has addressed an actively exploited zero-day authentication bypass vulnerability in its **SmartConsole** GUI admin panel, tracked as **CVE-2026-16232**. The flaw allows unauthenticated attackers to obtain an application login token that can be used to authenticate with **administrator privileges**, enabling full security policy and configuration changes.

Key details:
- Affects **Security Management Server** and **Multi-Domain Security Management (MDS)** products
- Exploitation requires no Trusted Client restrictions and internet exposure of the Management Server IP
- Check Point confirms exploitation of "a very small number of customers"
- **CISA added CVE-2026-16232 to KEV** on July 22, setting a **July 25** federal remediation deadline
- This is the third Check Point CVE added to KEV this year (after CVE-2026-50751 in May, CVE-2024-24919 in 2024)
- Also patched: **CVE-2026-62144** (critical auth bypass/priv esc) and **CVE-2026-62145** (high-severity local privilege escalation)
- All three discovered internally by Check Point; CVE-2026-16232 was already exploited as zero-day before discovery

The **Qilin ransomware group** was recently observed targeting Check Point appliances, though attribution of this specific exploitation is unconfirmed.

**Action:** Apply patches immediately. Restrict Management Server IP access. Enable Trusted Client restrictions. Review IOCs provided by Check Point. Federal agencies: remediate by July 25.

**Sources:** [SecurityWeek](https://www.securityweek.com/new-check-point-zero-day-vulnerability-exploited-in-the-wild/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/check-point-patches-smartconsole-zero-day-exploited-in-attacks/) · [Check Point Advisory](https://support.checkpoint.com/results/sk/sk185169/)

---

### [UPDATE] CVE-2026-50522 — Fourth SharePoint Vulnerability Exploited Within a Month; Machine Key Theft Ongoing

*Previously covered July 22 (CVE-2026-50522 with watchTowr machine-key theft confirmation). New: SecurityWeek frames this as the fourth SharePoint vulnerability exploited this month — now part of a sustained exploitation cluster.*

The active exploitation of **CVE-2026-50522** — a critical deserialization RCE in on-premise Microsoft SharePoint Server — continues to generate incident response activity. SecurityWeek now counts this as the **fourth SharePoint vulnerability exploited in the past month's wave of attacks**, alongside CVE-2026-58644, CVE-2026-56164, and CVE-2026-45659.

Defused honeypots observed exploitation attempts beginning around July 17 targeting what appeared to be a zero-day, later confirmed as CVE-2026-50522. After public PoC was released, watchTowr confirmed attackers are **stealing machine keys** to retain long-term access beyond the patch window.

Microsoft has not yet updated its advisory to reflect active exploitation. CVE-2026-50522 is not yet on CISA KEV (as of July 22), unlike CVE-2026-58644 which was added July 16.

**Action:** Patch immediately (July 14 Patch Tuesday update). Rotate machine keys on any internet-exposed SharePoint server. Hunt for unauthorized authentication tokens.

**Sources:** [SecurityWeek](https://www.securityweek.com/fourth-sharepoint-vulnerability-exploited-in-past-months-wave-of-attacks/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/critical-sharepoint-rce-flaw-exploited-to-steal-machine-keys/)

---

### [UPDATE] CISA Orders Urgent Action on Langflow RCE (CVE-2026-0770) — 220+ Exploitation Attempts

*Previously covered July 22 (CISA KEV addition for CVE-2026-0770). New: Detailed exploitation telemetry — 220+ attempts from 64 unique IPs, weaponized payloads executing as root.*

CISA has ordered federal agencies to prioritize patching **CVE-2026-0770**, a critical unauthenticated RCE in the **Langflow** visual framework for building AI agents. The flaw allows arbitrary code execution as **root** via improper handling of the `exec_globals` parameter to the validate endpoint (Trend Micro ZDI).

New telemetry from KEVIntel:
- **First in-the-wild exploitation observed June 27**
- **220+ exploitation attempts** recorded from **64 unique source IP addresses** before CISA KEV inclusion
- Malicious activity goes **beyond vulnerability scanning** with actual weaponized payloads

Langflow is the first AI agent framework added to CISA KEV. Patches were available from the vendor but many self-hosted instances remain vulnerable.

**Action:** Federal agencies: patch by CISA deadline. Non-federal: identify and patch all Langflow instances immediately. Hunt for exploitation artifacts dating back to late June.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-orders-feds-to-patch-actively-exploited-langflow-rce-flaw/) · [KEVIntel](https://blog.kevintel.com/cve-2026-0770-exploited-in-the-wild-langflow-rce-added-to-cisa-kev/)

---

## 🎯 Threat Actor Activity & Campaigns

### US Government Warns: Iranian Hackers Now Targeting Siemens, Schneider Electric, and Rockwell ICS Devices

The US government has updated its April advisory on Iran-linked attacks against critical infrastructure, revealing that Iranian APT groups have expanded targeting to include **Siemens S7-1200**, **Schneider Electric Modicon M340 (BMX P34)**, and **Rockwell Automation CompactLogix/Micro850** programmable logic controllers (PLCs).

Key findings from the updated advisory (published July 22):
- Hackers used vendor configuration software (**Rockwell Studio 5000**, **Schneider EcoStruxure Control Expert**, **Siemens TIA Portal**) to download malicious project files to PLCs
- Attackers **extracted and exfiltrated PLC project files**, then **modified and deleted logic**
- PLC modifications **disabled critical shutdown and alarm logic**, allowing systems to enter unsafe conditions without operator notification
- Some attacks used **malicious ladder logic** that overrode safe operating parameters
- Connections made via leased third-party-hosted infrastructure to ports 44818, 2222, 102, 502, and 22

The advisory names groups **CyberAv3ngers** (previously linked to many ICS attacks) and **Handala** (which hit Stryker in 2025 and claimed access to California Water Service last month) as active in these campaigns.

Updated IOCs and detection guidance are available in the advisory.

**Action:** Review internet-exposed PLCs. Audit for unauthorized configuration software access. Verify safety shutdown/alarm logic integrity on Siemens, Schneider, and Rockwell PLCs. Restrict access to ports 44818, 2222, 102, 502, 22 from untrusted networks.

**Sources:** [SecurityWeek](https://www.securityweek.com/us-warns-of-iranian-hackers-targeting-siemens-schneider-and-rockwell-ics-devices/)

---

### Sandworm_Mode: Self-Propagating Worm Targets AI Development Toolchains

CrowdStrike published a report on **Sandworm_Mode**, a self-propagating worm targeting AI coding assistants and software development environments. First discovered by Socket in February, the malware is now spreading more broadly with increasing capabilities:

- Steals **credentials, API keys, and secrets** for nine major LLM providers
- Targets **CI/CD pipelines**, cloud providers, and automated build/test/publish systems
- Self-propagates through code repositories with minimal detection
- Part of the broader **Shai-Hulud** family of supply-chain worms (alongside Miasma, IronWorm, Mini Shai-Hulud)

CrowdStrike's Adam Meyers characterized this as "the new hotness right now" — reflecting the accelerating trend of adversaries targeting AI supply chains.

**Hunting hypothesis:** Audit CI/CD pipelines for unauthorized credential access. Monitor for unusual API key usage against LLM providers. Review repository logs for anomalous code push behavior from automated accounts.

**Sources:** [CyberScoop](https://cyberscoop.com/sandworm-mode-malware-ai-supply-chain-crowdstrike/) · [CrowdStrike](https://www.crowdstrike.com/en-us/blog/denying-the-worm-sandworm-mode-and-ai-toolchain-supply-chain-attacks/)

---

### White House Accuses Moonshot AI of Illicitly Distilling Anthropic's Fable Model

White House Office of Science and Technology Policy Director **Michael Kratsios** publicly accused Beijing-based **Moonshot AI** of distilling Anthropic's recently released **Fable** model to create its **Kimi K3** product.

Kratsios stated that Moonshot AI developed "a sophisticated internal platform to conduct large scale distillation against U.S. models" using multiple access methods to avoid detection. The company allegedly used **GB300 servers** acquired through Thailand to train its models.

Moonshot AI's K3 is promoted as a 2.8 trillion parameter open model with near-frontier performance at lower token costs — a profile that Kratsios argues is indicative of illicit distillation rather than independent research.

Kratsios distinguished between legitimate small-model distillation (which "plays a vital role") and "large-scale, covert industrial distillation aimed at stealing proprietary U.S. technology."

**Sources:** [CyberScoop](https://cyberscoop.com/white-house-accuses-moonshot-ai-anthropic-model-distillation/)

---

## ⚠️ Vulnerabilities & Patches

### RefluXFS (CVE-2026-64600) — Linux Kernel LPE via XFS Race Condition

Qualys Threat Research Unit, in collaboration with Anthropic (using Claude Mythos Preview during manual audit workflow), discovered **CVE-2026-64600** — a race condition in the Linux kernel's XFS filesystem copy-on-write path. An unprivileged local user can exploit this flaw to **overwrite any readable file on an XFS volume at the block layer**, achieving host root privileges — even on systems running **SELinux in Enforcing mode**.

Key details:
- Affects any Linux distribution with XFS root filesystem and **reflink enabled** (default on RHEL, Oracle Linux, Amazon Linux, Fedora)
- Exploitation is **highly reliable** and leaves **no kernel log output**
- Attackers with a local account can escalate to full root
- Patches available in latest kernel updates

**Action:** Apply Linux kernel updates immediately. For systems where patching is delayed, consider disabling XFS reflink support (evaluating performance impact).

**Sources:** [Qualys](https://blog.qualys.com/vulnerabilities-threat-research/2026/07/22/refluxfs-a-linux-kernel-local-privilege-escalation-to-root-in-xfs-cve-2026-64600)

---

### CVE-2026-48294 (HermeticReader) — Adobe Acrobat Chrome Extension with 329M Installs Enabled Silent WhatsApp Data Theft

Guardio researchers disclosed **CVE-2026-48294** (dubbed **HermeticReader**), a UXSS-class cross-origin data disclosure vulnerability in the **Adobe Acrobat Chrome extension** (329 million installs). The attack chain:

1. A victim visits a malicious webpage
2. The page abuses the extension's internal messaging system — lacking security checks — to activate the **Hermes** integration engine (dormant unless a feature flag is enabled)
3. Once activated, Hermes bridges to **WhatsApp Web** with a predictable Tab ID
4. The attacker silently scrapes private **chats, contacts, and account details** in plain text

No WhatsApp vulnerability, malware, or credential theft is required. Adobe patched the flaw in June after Guardio's disclosure. Despite the massive install base and severe impact, no active exploitation has been publicly confirmed.

**Action:** The Adobe Acrobat Chrome extension auto-updates. Verify your browser has the latest version. Consider disabling the extension if WhatsApp integration is not actively used.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/adobe-chrome-extension-flaw-let-sites-access-private-whatsapp-chats/) · [SecurityWeek](https://www.securityweek.com/flaw-in-adobe-extension-with-300m-installs-enabled-whatsapp-data-theft/) · [Guardio](https://guard.io/labs/hermeticreader---the-vulnerability-that-turned-adobe-300m-install-extension-into-a-full-whatsapp-takeover)

---

### Oracle July 2026 CPU: 1,449 Security Updates, 1,235 CVEs — Largest Quarter

Oracle released its third quarterly Critical Patch Update for 2026 with **1,449 security updates** addressing **1,235 unique CVEs**. Key statistics:
- **86%** (1,235) are for non-Oracle CVEs (open-source components in Oracle products)
- **Oracle E-Business Suite**: 410 patches (28% of total) — highest
- **Oracle Fusion Middleware**: 355 patches
- **Oracle Communications**: 168 patches, 122 remotely exploitable without auth
- **Oracle GoldenGate**: 27 new updates (max CVSS 9.1)
- **Oracle Database Server**: 15 new updates (max CVSS 9.9)

**Action:** Prioritize E-Business Suite and Communications product patches. Note that the vast majority are third-party component CVEs — these affect customers even if they don't directly use Oracle applications.

**Sources:** [Qualys](https://blog.qualys.com/vulnerabilities-threat-research/2026/07/22/oracle-critical-patch-update-july-2026-security-update-review) · [SecurityWeek](https://www.securityweek.com/oracle-patches-over-1400-vulnerabilities-with-quarterly-security-updates/)

---

### InfraTrust Pulse: New Framework for Prioritizing Infrastructure Vulnerabilities

Eclypsium launched **InfraTrust**, a knowledge base and monthly **InfraTrust Pulse** report designed to help organizations prioritize infrastructure, firmware, networking, and edge device vulnerabilities based on **exploitability, exposure, and real-world risk** rather than CVSS scores alone.

The inaugural July 2026 report tracks **61 advisories from 14 vendors**, including:
- **6 critical advisories**
- **26 remotely exploitable, unauthenticated vulnerabilities**
- Several flaws listed in CISA KEV

The report focuses on the growing threat of Russian and Chinese state-sponsored actors targeting network edge devices (routers, VPNs, firewalls).

**Action:** Incorporate exposure-based prioritization into vulnerability management. Review InfraTrust Pulse for infrastructure-specific patch guidance.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-infratrust-report-reveals-infrastructure-flaws-admins-should-patch-first/)

---

## 🛡️ Defense & Detection

### [UPDATE] Four More Supply Chain Attacks Hit npm and PyPI (June–July 14)

*Previously covered July 17-22 (Miasma worm, Shai-Hulud, Mini Shai-Hulud). New: GitGuardian documents four additional attacks — IronWorm, Hades on PyPI, CI token theft, two typosquat campaigns.*

Between early June and July 14, 2026, four more supply chain attacks hit the npm and PyPI ecosystems:

1. **Miasma worm spread continues**: Reached the Vapi server SDK and additional packages before researchers closed the gap. Credential harvesting with self-spreading logic.
2. **IronWorm** (JFrog): Rust-built infostealer planted in **36 npm packages** using an **eBPF kernel rootkit** for stealth. Spread via stolen npm credentials to publish trojanized versions of victims' packages. Stopped before reaching widely-used packages.
3. **Hades** on PyPI: A matching PyPI variant of the Miasma/Shai-Hulud worm, carrying identical credential harvesting and self-spreading logic ("Hades — The End for the Damned").
4. **CI token theft campaign**: Attackers backdoored packages with **millions of weekly downloads** by stealing CI/CD tokens.

The attacks share a single objective: "land where the credentials live and leave with them."

**Action:** Audit CI/CD token exposure. Rotate npm/PyPI publish tokens. Verify package integrity checksums before deployment. Monitor for unexpected package updates in your dependency tree.

**Sources:** [GitGuardian](https://blog.gitguardian.com/shai-hulud-npm-pypi-supply-chain-attacks/)

---

### Study: AI-Generated (Vibe-Coded) Apps Contain Riddled Security Flaws — 434 Exploitable Issues Found

Xint.io (Theori's AI-driven pentest platform) analyzed AI-generated applications and found **434 exploitable security issues** across three test applications. Key findings:

**Most common flaws:**
1. **Rate limiting / DOS** — 93 flaws (most common). Missing controls lead to runaway server costs or trivial service takedown.
2. **Authorization/IDOR** — 88 flaws. Users accessing data beyond permissions scope.
3. **Access boundary / traversal / SSRF** — 54 flaws.

**Critical-severity flaws (23 found):**
- **Hardcoded secrets** most common at 11 findings
- **Debug-mode RCE** — 6 findings

**Positive trend:** Injection flaws (SQLi, XSS) barely showed up, suggesting AI models have genuinely improved in foundational security code generation. However, **fine-grained authorization breaks as apps grow** — IDOR went from 11% in small apps to 28% in a larger brownfield app.

**Action:** Do not skip security review for AI-generated code. Specifically audit for hardcoded secrets, rate limiting, and authorization boundaries. Use automated scanning tools targeting AI-specific weakness patterns.

**Sources:** [SecurityWeek](https://www.securityweek.com/vibe-coded-apps-riddled-with-exploitable-security-flaws/) · [Xint.io](https://xint.io/)

---

### GAO: 7 of 10 Federal Cyber Reporting Rules Are Duplicative

The Government Accountability Office (GAO) found that **80 out of 117 federal cybersecurity reporting rules** (68%) duplicate requirements across 37 agencies. The report, requested by House Homeland Security Chairman Garbarino and Sen. Peters, examined rules requiring private-sector written reports of incidents, plans, and reviews to federal agencies.

Harmonization efforts that began under the Biden administration and continued under Trump have had limited success. The finding underscores the compliance burden on organizations subject to multiple sector-specific cyber regulations.

**Sources:** [CyberScoop](https://cyberscoop.com/gao-report-duplicate-cybersecurity-regulations-harmonization/) · [GAO Report](https://www.gao.gov/assets/gao-26-108606.pdf)

---

## 📋 Breaches & Industry News

### Suno (55.3M) and Paidwork (23.3M) Data Breaches Expose Tens of Millions

Have I Been Pwned (HIBP) confirmed two large data breaches affecting **tens of millions of accounts**:

**Suno** (AI music generator): Breached November 2025. **55.3M unique email addresses** leaked, along with phone numbers, names, physical addresses, and partial payment card data (type, expiration, last 4 digits) for tens of thousands of Stripe payment records. The breach also exposed source code revealing Suno was scraping music from Deezer, YouTube, and Genius.

**Paidwork** (gig-work platform): Allegedly breached March 2026. **23.3M unique email addresses** leaked in an 11 GB database containing names, password hashes, addresses, DOBs, phone numbers, bank account numbers, and financial transaction records. Paidwork disputes the breach, stating "no confirmed evidence" of compromise.

**Action:** Users of either platform should change passwords and monitor financial accounts. Organizations: check employee credential exposure in these datasets.

**Sources:** [SecurityWeek](https://www.securityweek.com/suno-paidwork-data-breaches-affect-tens-of-millions-of-accounts/)

---

### South Korea Discloses Data Breach Affecting 6,000+ Diplomats and Foreign Ministry Staff

South Korea disclosed that an **unknown threat actor** breached the National Diplomatic Academy's online education system between **April 2025 and February 2026** — a **10-month** undetected access period. The breach impacts at least **6,000 individuals**, including **350 current government attachés** dispatched to overseas missions.

Exposed data: IDs, names, email addresses, and encrypted passwords. The ministry claims no unique identification numbers, mobile phone numbers, photographs, or home addresses were compromised. The education platform was established in 2022 for COVID-19-era remote training.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/south-korea-discloses-data-breach-impacting-diplomats-worldwide/)

---

### Stadler Rail Rejects $12.3M Everest Ransomware Demand; Upbound Group Reports $13M Fraud

**Stadler Rail** (Swiss train manufacturer, 18,000 employees, $4.9B revenue) disclosed that the **Everest ransomware gang** demanded 10M Swiss francs ($12.3M) after breaching a data exchange platform shared with one of its suppliers. The company stated it "will not pay any ransom under any circumstances" and filed a criminal complaint. The breach was limited to technical information from the supplier; Stadler's own IT and production operations were unaffected.

**Upbound Group** (fintech, formerly Rent-A-Center) disclosed via SEC filing that threat actors who stole customer data from its systems leveraged it to commit **$13M in fraudulent lease-to-own agreements** through its **Acima** segment. The attackers used stolen data to obtain goods from third-party retailers, leaving Acima to absorb the losses. The company implemented enhanced authentication and fraud-detection measures.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/swiss-rail-giant-stadler-rejects-123m-ransom-demand-after-cyberattack/) · [BleepingComputer](https://www.bleepingcomputer.com/news/security/upbound-says-hack-caused-13-million-in-fraudulent-acima-leases/)

---

## ⚡ Quick Hits

- **Palo Alto Networks to acquire Embrace** — Palo Alto Networks announced plans to acquire Embrace, an observability platform provider, expanding its security operations capabilities. (SecurityWeek)
- **Qilin ransomware hits Spanish wastewater utility** — ASEC reports Qilin ransomware attack on a Spanish public wastewater management organization. (ASEC/AhnLab)
- **RansomHouse hits Japanese frozen food/logistics firm** — RansomHouse ransomware attacked Nichirei, a Japanese frozen food and logistics company. (ASEC/AhnLab)
- **South Korean autonomous robot manufacturer source code leaked** — Source code belonging to a South Korean autonomous robot manufacturer was posted on a cybercrime forum. (ASEC/AhnLab)
- **Endpoint security firm Glow launches with $180M at $1.2B valuation** — One of the largest cybersecurity startup launches of 2026. (SecurityWeek)
- **Meta hires Assaf Keren as CISO** — Former CSO/CISO at Qualtrics and PayPal joins Meta as its new Chief Information Security Officer. (SecurityWeek)
- **AJ Shipley appointed CPO at CrowdStrike** — AJ Shipley named Chief Product Officer at CrowdStrike. (SecurityWeek)

---

*Digest generated July 23, 2026. 28 feed articles reviewed, 2 prior digests cross-referenced for continuity, gap detection via web search.*
