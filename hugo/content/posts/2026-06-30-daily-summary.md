---
title: "🪟🔨 BlueHammer Ransomware, 🛡️ SimpleHelp Djinn Stealer, 💼 Oracle EBS 0-Day, 🏢 Nissan PeopleSoft Update, 📱 Supreme Court Geofence Ruling"
date: 2026-06-30
tags: ["CVE-2026-33825","BlueHammer","SimpleHelp","Djinn Stealer","CVE-2026-48558","Oracle EBS","CVE-2026-46817","ShinyHunters","PeopleSoft","Bumblebee","Akira","Daktronics","Chatrie","geofence","AI AGENT Act"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA flags BlueHammer as ransomware-exploited; SimpleHelp CVE exploited to deploy Djinn Stealer targeting AI dev credentials; Oracle E-Business Suite CVE-2026-46817 exploited in the wild; Nissan confirms PeopleSoft breach impacting hundreds of companies; Supreme Court rules geofence warrants are 4th Amendment searches; Microsoft details Perplexity AI impersonation extension intercepting browser queries."
---
# Daily Threat Intelligence Digest — June 30, 2026

*30 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Windows BlueHammer (CVE-2026-33825) — CISA Confirms Ransomware Gangs Now Exploiting Microsoft Defender LPE**

CISA has updated the Known Exploited Vulnerabilities catalog to flag **CVE-2026-33825 (BlueHammer)** as actively exploited by ransomware gangs. The high-severity privilege escalation flaw in Microsoft Defender was already in KEV since April following zero-day exploitation, but CISA's Monday update specifically calls out ransomware operators. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-windows-bluehammer-flaw-now-exploited-by-ransomware-gangs/)]

The vulnerability, leaked by researcher "Nightmare Eclipse" in April alongside PoC exploit code in protest of MSRC disclosure practices, allows a local attacker to reach SYSTEM privileges by gaining access to the Security Account Manager (SAM) database. Microsoft patched it in April 2026 Patch Tuesday, but Huntress Labs confirmed hands-on-keyboard exploitation days later.

**Recommended action:** Confirm April 2026 Patch Tuesday was applied across all Windows endpoints.

---

**[NEW] Critical SimpleHelp Vulnerability (CVE-2026-48558) Exploited to Deploy Djinn Stealer — New Cross-Platform Malware Targeting AI Developer Credentials**

Attackers are actively exploiting **CVE-2026-48558**, a critical authentication bypass in the SimpleHelp RMM platform (used by MSPs and IT departments), to deploy **TaskWeaver** (a JS-based malware loader) and **Djinn Stealer**, a previously undocumented cross-platform stealer targeting Windows, macOS, and Linux. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-exploit-critical-simplehelp-flaw-deploy-new-djinn-infostealer-taskweaver-malware/); [SecurityWeek](https://www.securityweek.com/critical-simplehelp-vulnerability-exploited-for-malware-delivery/)]

Djinn Stealer targets: MCP config for AI coding assistants (Claude, Gemini, Codex, Cline, OpenCode), cloud/infra credentials (AWS, GCP, Azure, Docker, Terraform, Vault), Git/package manager tokens, and cryptocurrency wallets. Data is AES-256-GCM encrypted before exfiltration. ~1,000 vulnerable SimpleHelp servers were internet-exposed at disclosure.

**Recommended action:** Update SimpleHelp immediately. Invalidate all technician sessions. Rotate exposed credentials.

---

**[NEW] Oracle E-Business Suite Critical Flaw (CVE-2026-46817) Now Exploited — CVSS 9.8 Unauthenticated HTTP Takeover**

Defused confirmed active exploitation of **CVE-2026-46817**, a critical unauthenticated vulnerability in Oracle EBS File Transmission (Oracle Payments), over the weekend. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-oracle-e-business-suite-flaw-now-exploited-in-attacks/)]

CVSS 9.8, no public PoC. Oracle patched in May 2026 CPU. Shadowserver tracks 450+ exposed EBS instances globally, ~200 in the US. This is separate from the PeopleSoft ShinyHunters campaign.

---

**[UPDATE] ShinyHunters PeopleSoft Campaign — Nissan Confirms Employee Data Breach; NAIC Disputes Scope of Data Theft**

**Nissan Americas** filed CA AG breach notifications: SSNs, banking info, payroll, tax documents, beneficiary data exposed. Oracle says "hundreds of companies" impacted. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/nissan-discloses-employee-data-breach-linked-to-oracle-zero-day-attacks/)]

**NAIC** disputes ShinyHunters' 3.1TB claim, stating stolen data is mostly public reports and configs — not critical regulatory platforms. ShinyHunters admitted prior claims were "AI-hallucinated" but maintains a validated 105,000-file inventory. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/naic-says-public-data-stolen-in-shinyhunters-peoplesoft-breach/)]

*Previously covered June 27, 29. New: Nissan filing with specifics; NAIC formal response; ShinyHunters admits exaggeration.*

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] From Bing Search to Ransomware in 44 Hours — DFIR Report Details Bumblebee + AdaptixC2 → Akira Intrusion Chain**

Full incident report: SEO poisoning via Bing for "ManageEngine OpManager" → Bumblebee via trojanized MSI → AdaptixC2 C2 → NTDS.dit + Veeam credential theft → 77GB exfiltrated via FileZilla to Ukraine → Akira ransomware. [[The DFIR Report](https://thedfirreport.com/2026/06/29/from-bing-search-to-ransomware-bumblebee-and-adaptixc2-deliver-akira-3/)]

Key TTPs: Two-tier delivery infra (Hostinger AS47583, "LLC Vector" code cert), reverse SSH tunnels through Cloudflare, RustDesk for persistence, partial file encryption (-n=15), Swisscom parallel intrusion with WMIC service termination.

**Detection:** Monitor Bing/lookalike download domains. Event 5145 credential store scanning. DGA queries from non-browser processes. FileZilla installs via RDP clipboard.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Daktronics Controller Flaws — Highway Signs and Billboards Remotely Hackable**

CISA advisory on three vulns in Daktronics VFC-DMP-5000/8000 controllers: unauthenticated path traversal, default admin credentials, authenticated arbitrary file upload. Root-level access achievable. Internet-exposed controllers allow message tampering on highway signs/billboards. Patches released. [[SecurityWeek](https://www.securityweek.com/new-controller-flaws-expose-highway-signs-and-billboards-to-remote-hacking/)]

---

## 🛡️ Defense & Detection

**[NEW] Perplexity AI Impersonation — Chromium Extension Intercepts Every Browser Query**

Microsoft Threat Intelligence identified "Search for perplexity ai" (ID flkebkiofojicogddingbdmcmkpbplcd) — a malicious extension routing all Omnibox queries and real-time keystrokes through perplexity-ai[.]online before redirecting to legitimate search engines. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/06/29/chromium-extension-uses-airelated-branding-redirect-browser-search/)]

Ships server.js + nginx.conf proving intentional query logging. Uses MV3 declarativeNetRequest for invisible two-hop redirect. Modular rules for Bing/Google redirection (currently disabled). Taken down after MS disclosure.

---

## 📋 Policy & Industry News

**[NEW] Supreme Court Rules Geofence Warrants Are 4th Amendment Searches — Chatrie v. United States**

6-3 ruling: collecting phone location data via geofence warrants requires a warrant. Justice Kagan: "A new technology should not transform what individuals had reasonably thought they could withhold from the Government." [[CyberScoop](https://cyberscoop.com/supreme-court-geofence-warrant-ruling-phone-privacy-chatrie/)]

---

**[NEW] Warner AI AGENT Act — Draft Bill for FTC-Vetted AI Agent Providers**

Sen. Warner's draft bill would create FTC-certified AI agent provider list, require human-identity linking, and mandate user permission controls. Applies to platforms with 50M+ monthly users. [[CyberScoop](https://cyberscoop.com/ai-agent-act-senate-draft-bill-mark-warner/)]

---

## ⚡ Quick Hits

- **US Seizes 400 FIFA World Cup Illegal Streaming Domains** — DOJ ICHIP operation targeting servers in Peru/Bulgaria. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/us-seizes-hundreds-of-fifa-world-cup-illegal-streaming-domains/)]

- **Progress Kemp LoadMaster Pre-Auth RCE (CVE-2026-8037) PoC Published** — watchTowr full analysis of uninitialized heap vulnerability enabling pre-auth RCE in Kemp LoadMaster load balancers (GA v7.2.63.1 and older). Patches available since June 4. Verify patching. [[watchTowr](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/)]
