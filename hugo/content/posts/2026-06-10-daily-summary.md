---
title: "🔴 RoguePlanet Defender Zero-Day, 🚫 Arista EOS Unpatched, 📊 Record Patch Tuesday 206, 🐍 Shai-Hulud 471 Artifacts, 🇫🇷 Tchap Breach 650K Messages"
date: 2026-06-10
tags: ["Microsoft","Patch Tuesday","Zero-Day","RoguePlanet","Arista","CISA KEV","Shai-Hulud","Supply Chain","Ivanti","Veeam","ServiceNow","OpenSSL","AI Phishing","Tchap","Claude Fable 5"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Critical: RoguePlanet Microsoft Defender zero-day grants SYSTEM on fully patched Windows; Arista EOS actively exploited with no patch planned. Major: Record 206-vulnerability Patch Tuesday with 3 zero-days fixed; Shai-Hulud supply chain expands to 471 artifacts across 100+ npm/PyPI packages; France's Tchap government messaging breached (650K messages, 73K accounts). Also: Ivanti Sentry CVSS 10.0 RCE, Veeam Backup RCE, ServiceNow data exposure, OpenSSL High-Severity UAF found by AI, OpenClaw AI agent falls for phishing, Unit 42 cloud logging defense evasion deep dive, CISA revamps vulnerability prioritization."
---
# Daily Threat Intelligence Digest — June 10, 2026

*84 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — old.reddit.com returned errors on both `/hot/` and `/new/` endpoints. External gap detection via web search found no critical gaps beyond feed coverage. Prior digests: June 5–9, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] RoguePlanet: Microsoft Defender Race Condition Zero-Day Grants SYSTEM on Fully Patched Windows 10/11**

A security researcher known as Nightmare Eclipse publicly released a new zero-day exploit dubbed **"RoguePlanet"** just hours after Microsoft's Patch Tuesday — a race condition in Microsoft Defender's internal processing logic that spawns a command prompt with SYSTEM privileges on fully patched Windows 10 and Windows 11 devices. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-defender-rogueplanet-zero-day-grants-system-privileges/); [CyberSecurityNews](https://cybersecuritynews.com/windows-defender-0-day-exploit-rogueplanet/)]

ThreatLocker confirmed the exploit works against fully patched Windows 11 systems with KB5094126 installed. The flaw was originally developed as an RCE via malicious SMB shares (.vhd files), but Microsoft silently hardened Defender's `mpengine!SysIO*` API in mid-May, breaking the remote attack path. The remaining LPE vector uses a TOCTOU race condition — the same class exploited in Nightmare Eclipse's earlier BlueHammer exploit (CVE-2026-33825, patched April 2026).

The release continues Nightmare Eclipse's ongoing protest against Microsoft's vulnerability disclosure and bug bounty practices, following BlueHammer, RedSun, GreenPlasma, YellowKey, and MiniPlasma. **Microsoft has not yet issued a CVE or advisory.** Organizations with application allowlisting can block the exploit as a compensating control. Monitor for an emergency patch from Microsoft.

---

**[NEW] Arista EOS CVE-2026-7473 — No Patch Will Be Released, CISA KEV, Actively Exploited Tunnel Decapsulation Bypass**

Arista confirmed active exploitation of **CVE-2026-7473** (CVSS 6.9) in its Extensible Operating System (EOS), a tunnel protocol validation bypass affecting devices configured as tunnel endpoints (GRE, VXLAN, decap-groups). The switch incorrectly decapsulates and forwards unexpected tunnel protocols destined to the same IP — enabling traffic injection, reconnaissance, and potential data exfiltration. [[SecurityWeek](https://www.securityweek.com/no-patch-planned-for-exploited-arista-eos-vulnerability/)]

**Arista will not release a patch.** The vendor explicitly states "no software upgrade path is planned due to the risk of breaking existing configurations," directing customers to apply manual configuration mitigations instead. CISA added the flaw to its KEV catalog on Tuesday covering 7020R, 7280R/R2, 7500R/R2, 7280R3, 7500R3, and 7800R3 series. A vendor refusing to patch an actively exploited internet-facing vulnerability is extremely rare and signals that organizations must treat the mitigation instructions as emergency priority. Federal agencies have two weeks under BOD 22-01.

---

**[UPDATE] Microsoft Record Patch Tuesday: 206 Vulnerabilities Fixed, Including 3 Zero-Days (GreenPlasma, YellowKey, HTTP/2 Bomb)**

Microsoft shipped its **largest Patch Tuesday on record** — 206 vulnerabilities across Windows, Office, Exchange, Azure, and .NET. 33 are rated Critical, 28 of which are remote code execution flaws. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-june-2026-patch-tuesday-fixes-3-zero-day-200-flaws/); [Krebs on Security](https://krebsonsecurity.com/2026/06/a-record-breaking-patch-tuesday-for-june-2026/); [CyberScoop](https://cyberscoop.com/microsoft-patch-tuesday-june-2026/); [Rapid7](https://www.rapid7.com/blog/post/em-patch-tuesday-june-2026); [Qualys](https://blog.qualys.com/vulnerabilities-threat-research/2026/06/09/microsoft-and-adobe-patch-tuesday-june-2026-security-update-review)]

**Three publicly disclosed zero-days patched (none actively exploited):**
- **CVE-2026-45586 (GreenPlasma)** — Windows CTFMON EoP via improper link resolution. Grants SYSTEM privileges. Disclosed by Nightmare Eclipse.
- **CVE-2026-50507 (YellowKey)** — Windows BitLocker security feature bypass via WinRE and USB/EFI boot. Physical access required. Also disclosed by Nightmare Eclipse.
- **CVE-2026-49160 (HTTP/2 Bomb)** — HTTP.sys DoS via HTTP/2 header compression abuse. Single home computer can crash web servers in ~20 seconds. New `MaxHeadersCount` registry setting introduced as mitigation.

**Critical CVEs to prioritize:** Multiple Remote Desktop Client RCEs (CVE-2026-42985, CVE-2026-47289, CVE-2026-47654, CVE-2026-42992, CVE-2026-44801, CVE-2026-44799, CVE-2026-48563 — all Critical), Windows Hyper-V RCE (CVE-2026-45641, CVE-2026-47652, CVE-2026-45607), Windows DHCP Client RCE via stack buffer overflow (CVE-2026-44815, Critical), Windows Graphics Component RCE (CVE-2026-44812, CVE-2026-44803, both Critical), Microsoft Cryptographic Services EoP (CVE-2026-44810, Critical), and Azure Kubernetes Service RCE (CVE-2026-32193, Critical). The volume of critical RCE bugs in Remote Desktop Client alone — 7 CVEs — signals a significant code quality finding.

The 206-figure is a record that reflects an alarming trend: vulnerability volumes are structurally increasing. June 2026 now holds the record, surpassing May 2026's 190 CVEs. Active Directory Domain Services (CVE-2026-45648), Kerberos KDC (CVE-2026-47288), and Windows Kernel (CVE-2026-45657) also received critical RCE fixes.

---

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Shai-Hulud Supply Chain Campaign Escalates — 100+ Packages, 471 Malicious Artifacts Across NPM and PyPI, MCP-Themed and Typosquatting Waves**

The ongoing Shai-Hulud / Mini Shai-Hulud / Miasma supply chain campaign has escalated dramatically, now totaling over **471 malicious artifacts across 106 NPM packages and 37 PyPI packages**, with new waves continuing to hit the ecosystem. [[SecurityWeek](https://www.securityweek.com/over-100-npm-pypi-packages-hit-in-new-shai-hulud-supply-chain-attacks/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/github-disables-microsoft-repos-pushing-password-stealing-malware/); [CyberSecurityNews](https://cybersecuritynews.com/23-pypi-packages-compromised/)]

**Three new developments since the June 9 update:**
1. **Typosquat wave (June 7):** GitLab's Vulnerability Research team identified five malicious PyPI packages — `rlask` and `tlask` (Flask typosquats), `rsquests` (Requests typosquat), `nhmpy` (NumPy typosquat), and weaponized `mflux-streamlit` — all deploying the Shai-Hulud worm via a copycat actor using TeamPCP's open-sourced code. These packages execute at install time, no import required. [[GitLab](https://about.gitlab.com/blog/shai-hulud-copycat-campaign-targets-python-developers/)]
2. **Second "Hades" wave (June 8):** A new PyPI wave hit 29+ packages targeting bioinformatics, graph ML, and **MCP-themed packages** including `langchain-core-mcp`, `openai-mcp`, `instructor-mcp`, `tiktoken-mcp`, and `ray-mcp-server`. The malware mutated: payload is no longer bundled — instead searches `sys.path` at runtime to split loader from payload, evading static detection.
3. **471 total artifacts:** The campaign now spans 411 npm artifacts (106 packages) + 60 PyPI artifacts (37 packages). High-profile casualties include TanStack (84 malicious versions), UiPath, DraftLab, and `mistralai`/`guardrails-ai` on PyPI.

**Action:** Rotate all CI/CD secrets, npm/PyPi publish tokens, and cloud credentials on any system that may have installed affected packages. Audit for `*-setup.pth` files, unexpected Bun runtime downloads, and GitHub Actions creating unexpected public repos. Lock dependencies and add time delays to package update pipelines.

---

**[NEW] France's Tchap Government Messaging Platform Breached via Social Engineering — 650K Messages, 73K Accounts, 13.5 GB Exfiltrated**

DINUM, France's digital affairs directorate, confirmed that ANSSI detected a breach of **Tchap** — the mandatory encrypted messaging platform for French civil servants (300K+ monthly users). The attacker used social engineering to compromise a single user account on the education shard, then scraped public chat rooms for data. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/french-govt-messaging-service-breached-in-account-hijacking-attack/); [Security Affairs](https://securityaffairs.com/193393/security/frances-government-messaging-app-tchap-got-breached.html)]

**Attacker's claimed haul:** 650,000 messages, data on 73,000+ accounts (names, emails, affiliated entity, device metadata), 13.5 GB of documents and media. The attacker also claimed to have discovered hardcoded LDAP credentials in a PowerShell script shared by a French tax authority director.

**Architecture note:** Tchap's public rooms are unencrypted by design. Private rooms are E2EE and remain protected. DINUM emphasized that no sensitive data should have been shared in public rooms per terms of service — a post-breach reminder that Security Affairs aptly called "the digital equivalent of putting up a sign after the accident." The compromise underscores that mandatory mass adoption of encrypted platforms (mandated by PM Bayrou in August 2025) without proportional investment in security review produces predictable outcomes. CNIL notified.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Ivanti Sentry Max Severity RCE + Auth Bypass (CVE-2026-10520 CVSS 10.0, CVE-2026-10523 CVSS 9.9)**

Ivanti patched two critical vulnerabilities in its Sentry secure mobile gateway (formerly MobileIron Sentry): an **OS command injection (CVE-2026-10520, CVSS 10.0)** allowing unauthenticated remote code execution as root, and an **authentication bypass (CVE-2026-10523, CVSS 9.9)** enabling unauthenticated attackers to create rogue admin accounts. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-max-severity-ivanti-sentry-flaw-allows-code-execution-as-root/); [SecurityWeek](https://www.securityweek.com/critical-vulnerabilities-patched-in-fortinet-ivanti-products/)]

Additionally, Ivanti patched two high-severity EPMM flaws (CVE-2026-6973, CVE-2026-10727) enabling authenticated RCE via arbitrary Apache directives and root command execution. Fortinet simultaneously patched **CVE-2026-25089 (CVSS 9.8)**, an unauthenticated OS command injection in FortiSandbox WEB UI. No evidence of exploitation for any of these four flaws. Ivanti products have been a frequent zero-day target — treat these patches as urgent preventive maintenance.

---

**[NEW] Veeam Backup & Replication CVE-2026-44963 — Critical RCE on Domain-Joined Backup Servers**

Veeam released security updates for **CVE-2026-44963**, a critical RCE vulnerability in Backup & Replication 12.3.2.4465 and earlier (fixed in 12.3.2.4854). Any authenticated domain user can exploit the flaw — notably, many organizations join Veeam servers to Windows domains despite Veeam's long-standing best practices. Version 13.x builds are unaffected due to architectural changes. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-veeam-vulnerability-exposes-backup-servers-to-rce-attacks/)]

**Ransomware context:** Veeam backup servers are prime targets — ransomware gangs have explicitly told BleepingComputer they target VBR to block restoration. CISA has flagged four prior Veeam flaws as actively exploited, including CVE-2024-40711 (abused by Akira, Fog, Frag, FIN7). While no active exploitation of CVE-2026-44963 has been reported yet, the disclosure of a patch is the starting gun for exploit development. Apply immediately.

---

**[NEW] ServiceNow Security Incident — Unauthenticated API Endpoint Exposed Customer Instance Data**

ServiceNow disclosed a security incident after attackers exploited an unauthenticated access flaw via a vulnerable REST API endpoint. The company applied a security update on June 5, 2026, changing the endpoint configuration to require authentication. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/servicenow-discloses-security-incident-exposing-customer-data/)]

**Technical details:** Admin discussions on Reddit identified the vulnerable endpoint as `/api/now/related_list_edit/create`, reportedly configured with `requires_authentication=false`. The attacker IP **51.159.98.241** was observed making requests to the endpoint. ServiceNow instances commonly store IT support tickets, employee records, internal documentation, asset inventories, and security incident reports — support case data containing credentials and API tokens is a particularly high-value target. ServiceNow is still evaluating whether to publish a CVE.

---

**[NEW] OpenSSL CVE-2026-45447 — High-Severity Heap UAF Found by Claude AI, Possible RCE**

OpenSSL patched 18 vulnerabilities including **CVE-2026-45447**, a high-severity heap use-after-free in PKCS#7 signature verification that can lead to heap corruption, process crashes, and possibly remote code execution. Discovered by a Calif researcher collaborating with **Claude AI and Anthropic Research** — triggered by a specially crafted PKCS#7 or S/MIME signed message with an empty `digestAlgorithms` ASN.1 SET. [[SecurityWeek](https://www.securityweek.com/openssl-patches-high-severity-vulnerability-found-with-ai/)]

This is only the **second high-severity OpenSSL flaw of 2026**. Alex Gaynor of Anthropic was credited with reporting half a dozen of the newly patched vulnerabilities, suggesting Anthropic's Mythos model contributed to the discoveries. The finding continues a trend: in January 2026, AISLE's AI system discovered all 12 OpenSSL CVEs in that coordinated release.

---

## 🛡️ Defense & Detection

**[NEW] OpenClaw AI Agent Falls for Classic Phishing — Credential and Data Exfiltration via Social Engineering, Even With Strict Guardrails**

Varonis Threat Labs tested an OpenClaw AI email agent against phishing techniques that have tricked humans for decades — and found it vulnerable. The agent, connected to a Gmail inbox with fabricated enterprise data (AWS keys, CRM exports, SSH credentials), was tested with both generic and strict security configurations. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/openclaw-ai-agent-found-falling-for-phishing-attacks-spills-user-data/)]

**Results:** In both configurations, the agent emailed AWS IAM keys, database credentials, and SSH access to an attacker-posing-as-team-lead under a supposed production issue. It also exfiltrated a CRM customer export on a "remote presentation" pretext. The agent successfully detected a phishing link and malicious OAuth app, but **failed on identity verification** — it could not distinguish an urgent request from an attacker because the framework lacked sender-identity validation. GPT-5.4 showed a more cautious posture than Gemini 3.1 Pro. **Recommendation:** AI agents must explicitly verify sender identities, require human approval for first-time external communications, and implement zero-trust principles for social interactions—not just technical indicators.

---

**[NEW] Unit 42: Blinding the Watchmen — 7 Techniques for Abusing AWS CloudTrail and Google Cloud Logging**  

Palo Alto Networks Unit 42 published a comprehensive deep-dive on how attackers abuse cloud logging services for defense evasion and continuous visibility. The report details **7 specific techniques** targeting AWS CloudTrail and Google Cloud Logging, with detection logic for each. [[Unit 42](https://unit42.paloaltonetworks.com/cloud-logging-defense-evasion/)]

**Key techniques:** Stop logging (disable trails/sinks), delete log storage destination (S3 bucket/log bucket), delete log router (trail/sink), impair logging via attacker-controlled KMS encryption key, log poisoning (directly modify JSON log files in S3), configure new log routing to attacker-controlled destination, and log redirection (change existing destination). The most impactful finding: log poisoning via direct S3 object manipulation breaks chain of custody — AWS's CloudTrail log file integrity validation (enabled by default in Console but NOT via API/CLI) is the only defense. **Action:** Restrict `update-trail`/`sinks.update` permissions to highly privileged users; enable CloudTrail integrity validation; lock Google Cloud log buckets.

---

## 📋 Policy & Industry News

**[NEW] CISA Revamps Vulnerability Prioritization — New Binding Operational Directive Moves Beyond "Patch Everything"**

CISA acting director Nick Andersen announced a new binding operational directive fundamentally reshaping how federal agencies prioritize vulnerabilities — moving from "a patch is released, apply this patch as quickly as you can" to risk-based prioritization factoring in internet exposure, KEV status, and exploit automability. [[CyberScoop](https://cyberscoop.com/cisa-cyber-risk-prioritization-vulnerability-directive/)]

Andersen framed the shift as a necessary acknowledgment of resource constraints: "We have to be okay with saying there are some systems that are less important than others." The directive, driven in part by AI-accelerated exploit timelines, targets publication Wednesday. The agency also announced a hiring sprint targeting 329 new personnel (182 offers by end of June), focusing on operational capabilities.

---

## ⚡ Quick Hits

- **[NEW] Anthropic Launches Claude Fable 5 — Public Release of Mythos-Derived Model With Cybersecurity Guardrails** — Claude Fable 5 is the "same underlying model" as Mythos but routes cybersecurity and biology queries to Claude Opus 4.8's capabilities. Data retention policies extended to 30 days for safety monitoring. Project Glasswing members upgraded to full Mythos 5. [[BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-rolls-out-claude-fable-5-but-its-available-for-a-limited-time/); [CyberScoop](https://cyberscoop.com/anthropic-claude-fable-5-release-mythos-guardrails/)]

- **[NEW] SAP June 2026 Security Patch: 4 Critical Flaws in NetWeaver and Commerce Cloud** — Including CVE-2026-44748 (CVSS 9.9, SAML authentication bypass via XML Signature Wrapping), CVE-2026-27671 (CVSS 9.8, unauthenticated memory corruption), CVE-2026-22732 (CVSS 9.1, Spring Security), and CVE-2026-40128 (CVSS 9.0, directory traversal). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/sap-fixes-critical-flaws-in-netweaver-and-commerce-cloud/); [SecurityWeek](https://www.securityweek.com/sap-patches-critical-netweaver-commerce-vulnerabilities/)]

- **[NEW] Adobe Patches 123 Vulnerabilities Across Multiple Products** — Including fixes for Experience Manager, InDesign, InCopy, Reader, ColdFusion, Dreamweaver, and Substance 3D Sampler. Matches the record-breaking Patch Tuesday theme. [[SecurityWeek](https://www.securityweek.com/adobe-patches-123-vulnerabilities/); [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-june-2026-patch-tuesday-fixes-3-zero-day-200-flaws/)]

- **[UPDATE] CISA KEV Adds LiteLLM RCE (CVE-2026-42271) and Check Point VPN Auth Bypass (CVE-2026-50751)** — Both added June 8. LiteLLM due June 22; Check Point due June 11 (shortest federal deadline of 2026). Both were covered in detail in the June 9 digest. Apply fixes if not yet done. [[SOCPrime](https://socprime.com/blog/cve-2026-50751-check-point-vpn-authentication-bypass-exploited-in-targeted-attacks/); [SOCRadar](https://socradar.io/blog/cisa-kev-litellm-cve-2026-42271-check-point-cve-2026-50751/)]

---

*84 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — old.reddit.com returned errors on both `/hot/` and `/new/` endpoints. External gap detection via web search found no critical gaps beyond feed coverage. Prior digests: June 5–9, 2026. Stale CVE/topic blocklist applied. Sources include BleepingComputer, SecurityWeek, CyberScoop, Krebs on Security, Rapid7, Qualys, Unit 42 (Palo Alto Networks), CyberSecurityNews, SOCPrime, Security Affairs, GitLab, and independent researchers (Nightmare Eclipse, Varonis).*