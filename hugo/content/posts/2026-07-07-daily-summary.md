---
title: "Januscape VM Escape 🔴, DHS HSIN Breach 🏛️, UNK_MassTraction Roundcube Chain 📧, EtherRAT Teams Calls 📞"
date: 2026-07-07
tags: ["kvm", "vm-escape", "januscape", "dhs-hsin", "breach", "roundcube", "proofpoint", "etherrat", "phishing", "beyondtrust", "cisa-kev"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "16-year-old Linux KVM flaw (CVE-2026-53359) enables VM escape on Intel and AMD hosts. DHS confirms HSIN breach undetected for six weeks during World Cup 2026 security prep. Chinese espionage cluster UNK_MassTraction exploits Roundcube chain against US/Canadian universities."
---
# Daily Threat Intelligence Digest — July 7, 2026

*12 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking. Two significant gaps identified via community cross-reference (DHS HSIN breach, Januscape KVM escape).*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] CVE-2026-53359 "Januscape" — 16-Year-Old Linux KVM Flaw Enables VM Escape on Intel and AMD Systems**

A use-after-free vulnerability in Linux's KVM hypervisor — dormant for 16 years — has been disclosed and patched. Tracked as CVE-2026-53359 and dubbed "Januscape," the flaw sits in the shadow MMU code shared across both Intel and AMD architectures, making it the first publicly known KVM exploit triggerable on both CPU families.

Discovered by researcher Hyunwoo Kim (@v4bel) and demonstrated in Google's kvmCTF bug bounty program (up to $250,000), the vulnerability allows an attacker with root on a guest VM to corrupt the host kernel's shadow page state, leading to full host compromise. In a public cloud scenario, a single malicious guest could panic the host kernel (denial of service against all other tenants) or execute arbitrary code with host root privileges to take over the physical machine and all VMs on it.

On RHEL-based distributions, the flaw can also be exploited by unprivileged local users for privilege escalation to root. Exploitation requires root on the guest (typically default on cloud VMs); if root is unavailable, it can be chained with a privilege escalation bug like Dirty Frag.

**Patched in mainline Linux on June 19 (commit 81ccda30b4e8).** Cloud providers and Linux distribution maintainers should have patched; enterprises should verify their kernel versions are at or past the fix commit. [[SecurityWeek](https://www.securityweek.com/linux-kernel-vulnerability-allows-vm-escape-on-intel-and-amd-systems/); [The Hacker News](https://thehackernews.com/2026/07/16-year-old-linux-kvm-flaw-lets-guest.html); [GitHub](https://github.com/V4bel/Januscape)]

**Recommended action:** Verify all KVM hosts are running kernel ≥6.12.x with the June 19 patch. Audit cloud VM fleets. If unpatched, restrict untrusted guest workloads and enable nested virtualization protections.

---

**[NEW] DHS Confirms Breach of Homeland Security Information Network (HSIN) — Undetected for ~6 Weeks, World Cup 2026 Security Docs Exposed**

The Department of Homeland Security has confirmed that hackers breached the Homeland Security Information Network (HSIN) and an associated Microsoft SharePoint system between late May and early June 2026. The intrusion went undetected for approximately five to six weeks before DHS's Office of Intelligence and Analysis identified the compromise and launched a forensic investigation.

HSIN is the federal government's primary sensitive-but-unclassified (SBU) intelligence-sharing platform, serving seven tiers of partners (federal, state, local, tribal, territorial, international, and private sector). The platform stores threat profiles on persons of interest, interagency security planning documents for major national events, incident response protocols, and PII collected during law enforcement and national security operations.

**Critical timing:** The breach window coincides with peak pre-tournament security preparation for the 2026 FIFA World Cup (games continue through July 19). HSIN is the primary coordination platform for World Cup security across 16 host cities, including venue-specific threat assessments, counterterrorism coordination protocols, and watch lists. If attackers exfiltrated World Cup planning documents, the intelligence could reveal law enforcement response timelines, surveillance targets, and venue security gaps.

The attackers compromised two systems in parallel — HSIN's network servers and a SharePoint instance — suggesting a targeted intrusion from a privileged foothold. The precise initial access vector has not been disclosed. DHS states classified networks were unaffected. Investigators have not confirmed whether data was exfiltrated.

**This is HSIN's second security incident;** a 2023 contractor misconfiguration exposed SBU data to unauthorized users. The escalation from accidental exposure to targeted compromise signals adversaries now view HSIN as a high-value collection target. [[TechRepublic](https://www.techrepublic.com/article/news-dhs-hsin-breach-2026/); [Nextgov/FCW](https://www.nextgov.com/cybersecurity/2026/06/hackers-breached-dhs-information-sharing-network-people-familiar-say/414534/); [Decryption Digest](https://www.decryptiondigest.com/blog/dhs-hsin-breach-federal-security-intel-sharepoint-2026); [BleepingComputer](https://www.bleepingcomputer.com/news/security/dhs-confirms-hackers-breached-hsin-info-sharing-platform/)]

**Recommended action:** All partner organizations with HSIN access should (1) treat their data as potentially compromised, (2) review shared World Cup security materials for operational sensitivity, (3) initiate credential rotation for any accounts with HSIN/SharePoint access, and (4) brief security leadership on potential downstream impacts.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] UNK_MassTraction: Suspected Chinese Espionage Group Exploits Roundcube Chain to Breach US and Canadian Universities**

Proofpoint threat researchers published analysis of an ongoing espionage campaign targeting physics and engineering departments at US and Canadian universities. The threat cluster, tracked as UNK_MassTraction, exploited a two-CVE chain in the Roundcube open-source email client:

- **CVE-2024-42009** — Remote code execution via XSS in Roundcube (requires victim to open a crafted email)
- **CVE-2025-49113** — Post-authentication RCE to gain persistent foothold on the mailserver

Proofpoint identified fewer than 10 confirmed university victims but estimates "a few dozen" may be impacted, noting "there is a high likelihood that many victims have not been made aware of this activity yet." The campaign, first observed in May 2026, targets administrators and professors with national security links or research in astrophysics and particle physics. Attackers deployed webshells and backdoors for persistent access and data exfiltration. The campaign is ongoing. [[CyberScoop](https://cyberscoop.com/china-espionage-attacks-us-canada-universities-proofpoint/); [Proofpoint](https://www.proofpoint.com/us/blog/threat-insight/one-email-closer-edge-unkmasstraction-physics-exploitation)]

**Recommended action:** Verify Roundcube versions against CVE-2024-42009 and CVE-2025-49113 patches. Monitor for anomalous webshell activity on university mailservers. Alert institutional security teams at physics/engineering research departments.

---

**[NEW] Fake IT Support Calls on Microsoft Teams Deliver EtherRAT Malware**

Palo Alto Networks' Unit 42 documented a social engineering campaign in which threat actors abuse Microsoft Teams voice calls to deploy the EtherRAT malware for initial access to corporate networks. The kill chain:

1. **Phishing email** with "Employee Survey" lure and malicious PDF attachment
2. **Microsoft Teams voice call** from an external account impersonating IT support (account: `helpdesk@Progressive936.onmicrosoft[.]com`)
3. **Remote control granted** through Teams' built-in screen sharing
4. **Legitimate RMM tools installed** (HopToDesk, AnyDesc) to maintain persistent access
5. **EtherRAT malware loaded** via malicious MSI installer (`v7.msi`) from `camorreado[.]click`, deploying a Node.js-based loader

The attack exploits a gap in most security awareness training: users are trained not to install software from unknown sources but are less prepared to refuse help from someone who has already called and established rapport. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-it-support-calls-on-microsoft-teams-push-etherrat-malware/); [Unit 42 GitHub](https://github.com/PaloAltoNetworks/Unit42-timely-threat-intel/blob/main/2026-06-28-Fake-IT-support-abuses-Teams-to-deliver-EtherRAT.txt)]

**Recommended action:** Configure Microsoft Teams external access policies to restrict cross-tenant communications. Educate staff that IT support will never request remote control via unsolicited voice calls. Block MSI downloads from untrusted domains.

---

**[NEW] Phishing Campaign Impersonates 30+ Brands in Fake Job Interviews to Steal Google Accounts**

A large-scale phishing campaign impersonating more than 30 well-known brands — including Adobe, Netflix, Coca-Cola, OpenAI, American Airlines, Louis Vuitton, and FIFA — is targeting marketing professionals with fake job interviews to steal Google account credentials. The operation:

- Abuses the legitimate cloud-based **PeopleForce** HR platform and a domain associated with **Salesforce Marketing Cloud** for initial delivery
- Uses **nested redirects** through multiple legitimate services before reaching the malicious landing page
- Employs the **names and pictures of real recruiters** at impersonated companies
- Uses at least **34 domains** impersonating brands across airlines, apparel, staffing, hospitality, and entertainment sectors

Researcher Will Thomas (Team Cymru) identified and analyzed the campaign. The targeting of marketing professionals is a deliberate choice — these roles often have access to corporate social media accounts and advertising platforms, making credential theft particularly valuable for follow-on brand impersonation attacks. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/phishing-poses-as-big-brand-job-interview-to-steal-google-accounts/)]

**Recommended action:** Warn marketing and HR departments about the campaign. Advise candidates to verify interview invitations through official company career portals rather than email links. Monitor for Google account takeovers in marketing teams.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] BeyondTrust Warns of Critical Authentication Bypass Flaws in Remote Access Software**

BeyondTrust urged customers to patch two critical vulnerabilities in its Remote Support (RS) and Privileged Remote Access (PRA) software:

- **CVE-2026-40138** (Critical) — Improper authentication weakness in RS (≤25.3.2) and PRA (≤25.3.2); enables unauthenticated attackers to bypass access controls and access appliances including accounts with elevated privileges
- **CVE-2026-40139** (Critical) — Improper processing of RS authentication requests; enables unauthenticated remote attackers to gain unauthorized access
- **CVE-2026-40140** / **CVE-2026-40141** (High) — Denial-of-service / additional impacts

Both critical flaws require a specific authentication configuration to be enabled. BeyondTrust has released patches. No active exploitation has been reported, but remote access software is a high-value target for initial access brokers. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/beyondtrust-warns-of-critical-flaws-in-remote-access-software/)]

**Recommended action:** Upgrade BeyondTrust RS/PRA to versions later than 25.3.2 immediately. Audit authentication configurations.

---

**[NEW] Q2 2026 Vulnerability Trends Report — Critical CVEs Up 62.5%, CISA KEV Adds 27% More Listings**

ASEC (AhnLab) published its Q2 2026 Vulnerability Trends Report, revealing a sharp acceleration in high-severity vulnerabilities:

- **20,701 new CVEs** reported in Q2 2026 (comparable to Q1 volume)
- **2,317 Critical vulnerabilities** (CVSS ≥9.0), a **62.5% increase** from 1,426 in Q1 — accounting for 11.2% of all new CVEs
- **75 new vulnerabilities added to CISA KEV** (up 27% year-over-year from Q2 2025), with 52% classified as Critical
- **CWE-20 (Improper Input Validation)** and **CWE-306 (Missing Authentication)** were the most exploited weakness classes in KEV listings
- Attacks concentrated on external access points: firewalls, VPNs, enterprise management panels, and authentication portals
- Supply chain attacks targeting compromised official installation packages and npm packages continue to rise
- Generative AI tools are accelerating both vulnerability discovery and exploit development on both sides

The data confirms that the vulnerability landscape is not merely growing but becoming more severe, with adversaries zeroing in on perimeter and identity infrastructure. [[ASEC](https://asec.ahnlab.com/en/94360/)]

---

## 📋 Policy & Industry News

**[NEW] Google Sues Chinese Scammers Using Gemini AI to Automate Phishing Operations**

Google filed a lawsuit against "Outsider Enterprise," a Chinese cybercrime network operating via Telegram that offered phishing-as-a-service and used Google's Gemini AI to create scam website templates. The group reportedly offered nearly 300 scam templates imitating Google, YouTube, government agencies (including NY E-ZPass), and more. Google worked with AT&T, Verizon, and T-Mobile to block malicious text messages. Google notes its on-device AI scam detection in Google Messages blocks approximately 10 billion scam texts per month. Bruce Schneier, while supporting the effort, expressed skepticism about the lawsuit's deterrent effect. [[Schneier on Security](https://www.schneier.com/blog/archives/2026/07/google-is-suing-chinese-scammers-who-are-using-gemini.html); [ArsTechnica](https://arstechnica.com/google/2026/06/google-sues-chinese-cybercrime-network-that-used-gemini-to-automate-scams/)]

---

**[NEW] Keyfactor Scores $1 Billion+ Investment for AI and Post-Quantum Security**

Keyfactor announced a $1 billion+ investment round focused on AI-driven certificate lifecycle management and post-quantum cryptography readiness. The funding signals growing enterprise demand for PKI modernization as quantum-safe cryptographic standards approach regulatory deadlines. [[SecurityWeek](https://www.securityweek.com/keyfactor-scores-1-billion-investment-for-ai-post-quantum-security/)]

---

**[NEW] Microsoft to Enable Windows Settings Backup by Default for Organizations**

The Windows settings backup and restore tool (formerly "Windows Backup for Organizations") will be enabled by default on Microsoft Entra-joined and Entra hybrid-joined enterprise systems after upgrading to Windows 11 26H2. Organizations should review their backup policies before the change takes effect. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-to-enable-windows-backup-for-organizations-by-default/)]

---

**[NEW] Microsoft Testing Cloud Rebuild — Remote System Reinstall from the Cloud**

Microsoft has begun testing "Cloud Rebuild" in Windows 11 Insider Experimental builds, a feature that can remotely trigger a complete system reinstall from the cloud for devices that are inoperable or persistently problematic. The feature was first previewed at Ignite 2025. Enterprise security teams should evaluate the recovery implications. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-testing-new-cloud-rebuild-windows-11-recovery-feature/)]

---

*Cross-reference: No duplicate overlap with July 4–6 digests confirmed. CVE-2026-45659 (SharePoint RCE KEV), CVE-2026-46242 (Bad Epoll), JadePuffer AI agentic ransomware, and CVE-2026-43456 (19-year-old Linux bonding bug) were covered in prior editions and not re-reported.*
