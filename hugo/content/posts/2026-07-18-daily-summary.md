---
title: "🔴 CVE-2026-63030 wp2shell WordPress RCE, 🔴 Abbott Labs ShinyHunters Breach, ⚠️ HollowByte OpenSSL DoS, 🎯 TKMS Naval Defense Ransomware, 🛡️ AI Agent RCE via WhatsApp"
date: 2026-07-18
tags: ["CVE-2026-63030","WordPress","SharePoint","CVE-2026-58644","ShinyHunters","Ransomware","OpenSSL","Metasploit","AI-Security","Threat-Intelligence"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Critical pre-auth RCE in WordPress Core (wp2shell) dominates alongside SharePoint RCE detection signatures. ShinyHunters breaches Abbott Labs via Entra SSO vishing, The Gentlemen claim 1TB+ from naval defense firm TKMS, and a silent OpenSSL DoS fix highlights sub-CVE hardening gaps."
---

# Daily Threat Intelligence Digest — July 18, 2026

15 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] CVE-2026-63030 (wp2shell) — Critical Pre-Auth WordPress Core RCE

A critical unauthenticated remote code execution vulnerability in WordPress Core, dubbed **wp2shell**, was disclosed via GitHub Security Advisory on July 17. CVE-2026-63030 (CVSS 7.5) exploits the WordPress REST API batch endpoint, allowing an unauthenticated attacker to execute arbitrary code on default WordPress installations without requiring additional plugins. The vulnerability affects WordPress 6.9.0–6.9.4 and 7.0.0–7.0.1; fixes are available in 6.9.5 and 7.0.2.

Rapid7 notes that the vulnerable code path is reachable when a persistent object cache is not in use — the default for many WordPress deployments. WordPress maintainers are forcing updates for affected installations with automatic updates enabled. No public exploitation has been confirmed at time of publication, but Rapid7 assesses that a public PoC is highly likely given the open-source nature of WordPress and the accessibility of AI-assisted code analysis.

**Action:** Update WordPress immediately. Verify all internet-facing WordPress sites have been upgraded to 6.9.5, 7.0.2, or later. With WordPress powering ~43% of all websites, the attack surface is massive.

[Rapid7](https://www.rapid7.com/blog/post/etr-cve-2026-63030-wp2shell-a-critical-remote-code-execution-vulnerability-in-wordpress-core) · [GitHub Advisory](https://github.com/WordPress/wordpress-develop/security/advisories)

---

### [UPDATE] CVE-2026-58644 SharePoint RCE — Rapid7 Publishes ETR with Detection Signatures

*Previously covered July 15-17 (SharePoint exploitation cluster). New: Rapid7 ETR publishes specific AMSI/Defender detection signatures and exploitation details for the deserialization RCE.*

Rapid7 has published its Emergent Threat Response for CVE-2026-58644 (CVSS 9.8), confirming the vulnerability results from deserialization of untrusted data (CWE-502) in on-premises Microsoft SharePoint Server. Microsoft has confirmed active exploitation, and CISA added the vulnerability to KEV on July 16 with a July 19 federal deadline.

Rapid7 documents three specific Microsoft Defender and AMSI detection signatures organizations should enable: **Exploit:Script/SuspSignoutReqBody.A** (request body scanning, blocks exploitation in Subscription Edition), **Exploit:Script/ToolPaneAuthBypass.A** and **Exploit:Script/ToolPaneAuthBypass** (request header scanning, applicable to 2016/2019/Subscription Edition). Microsoft recommends enabling AMSI integration for every SharePoint web application and initiating incident response if exploitation artifacts are detected.

**Action:** Federal remediation deadline is tomorrow (July 19). Enable AMSI Full Mode, apply the three detection signatures, and scan for exploitation artifacts. This is the fifth CVE in the active SharePoint exploitation cluster.

[Rapid7 ETR](https://www.rapid7.com/blog/post/etr-cve-2026-58644-microsoft-sharepoint-server-unauthenticated-remote-code-execution-vulnerability-exploited-in-the-wild) · [CISA Alert](https://www.cisa.gov/news-events/alerts/2026/07/16/cisa-adds-three-known-exploited-vulnerabilities-catalog)

---

### [NEW] Abbott Laboratories — ShinyHunters Claims Access After Vishing Attack on Entra SSO

Abbott Laboratories is investigating two separate cybersecurity incidents. The primary incident involves unauthorized access to legacy Exact Sciences systems in its Cancer Diagnostics business, confirmed after the **ShinyHunters** extortion gang added Abbott to its data leak site with an initial July 18 deadline (subsequently extended to July 21). ShinyHunters claims to have gained access through a vishing attack targeting multiple Abbott employees in mid-June, compromising a Microsoft Entra SSO account to reach connected SaaS applications.

The group claims exfiltration of data from Microsoft Entra, ServiceNow, SharePoint, Databricks, and Coupa — allegedly including 30+ million rows of customer PII (names, emails, phone numbers, SSNs), 22 million client notes with doctor-patient conversations, and 20 million medical orders.

A second, separate incident involves threat actor **ShadowByt3$** claiming access to Abbott's LabCentral customer portal via compromised customer credentials. Abbott states this portal houses only publicly available technical documents.

ShinyHunters has been increasingly targeting medtech companies, with prior victims including Medtronic, OneMedical, iRhythm, AdaptHealth, and Stryker.

**Action:** Monitor for data publication on ShinyHunters leak site. Organizations using SaaS platforms connected to Entra SSO should verify vishing resilience and review conditional access policies for SSO accounts.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/abbott-laboratories-probes-two-cyber-incidents-amid-extortion-claims/)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] The Gentlemen Ransomware Claims Thyssenkrupp Marine Systems Breach — 1TB+ Allegedly Exfiltrated

The cybercrime collective known as **The Gentlemen** has posted Thyssenkrupp Marine Systems (TKMS) and subsidiary Atlas Elektronik to its leak portal, claiming exfiltration of more than 1TB of data from the naval defense manufacturer. TKMS acknowledged a network compromise at an isolated North American unit but stated the environment was segmented from core corporate infrastructure and contained no classified military records.

A German textile manufacturer, **ZEGO Textilveredelungszentrum**, has filed for bankruptcy after a ransomware attack forced a six-week production shutdown — demonstrating real-world operational destruction from ransomware beyond data theft.

Additionally, a new ransomware variant named **Spirals** combining file encryption with data theft has been deployed against an IT services firm in Asia.

**Action:** Naval defense contractors should verify TKMS supply chain communications. The ZEGO bankruptcy is a concrete example of ransomware-driven business failure from extended downtime.

[DataMinr / The Gentlemen](https://www.dataminr.com/resources/intel-brief/gentlemen-ransomware-claims-tkms-atlas-elektronik-breach/) · [The Register](https://www.theregister.com/cyber-crime/2026/07/13/german-firm-files-for-insolvency-blames-cybercrims-who-shut-down-production-for-6-weeks/5270524)

---

### [UPDATE] Scattered Spider Sentencing — 66 Months for TfL Attack, US Extradition Sought

*Previously covered July 17. New: CyberScoop provides additional sentencing details and expert commentary on leniency.*

Thalha Jubair (20) and Owen Flowers (18) were sentenced to 66 months in the UK for the Transport for London attack — the largest cybercrime prosecution in UK history. Flowers was previously arrested in connection with the attack in September 2024 but released; both pleaded guilty as trials were set to begin. At the time of arrest, Flowers was actively hacking Sutter Health and SSM Health Care Corporation. Traced cryptocurrency linked to Jubair totaled $89.5 million; two financial services firms paid $25M and $36.2M in Bitcoin respectively.

Unit 221B's Allison Nixon called the sentence "remarkably lenient" given the duration of continuous reoffending, and expressed hope the US will extradite the pair to face additional charges.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/scattered-spider-members-behind-transport-for-london-hack-get-five-years-in-prison/) · [CyberScoop](https://cyberscoop.com/scattered-spider-leaders-sentenced-united-kingdom/)

---

## ⚠️ Vulnerabilities & Patches

### [NEW] HollowByte — OpenSSL DoS with 11-Byte Payload, Silently Fixed

Okta's security research team has disclosed **HollowByte**, a denial-of-service vulnerability in OpenSSL that allows an unauthenticated attacker to permanently bloat server memory with an 11-byte TLS handshake payload. The flaw exploits how OpenSSL pre-allocates memory based on the handshake header's declared size before receiving the payload — a 4-byte header can claim any size, causing the server to allocate memory that never arrives.

Because glibc does not immediately return freed small-to-medium allocations to the OS, repeated exploitation causes permanent heap fragmentation and Resident Set Size inflation. In testing, higher-spec servers lost up to 25% of available memory while attack bandwidth remained below alerting thresholds. The only recovery is process restart.

OpenSSL silently fixed the vulnerability as a "hardening fix" without assigning a CVE. Patches are available in OpenSSL 4.0.1 and backported to 3.6.3, 3.5.7, 3.4.6, and 3.0.21.

**Action:** Upgrade OpenSSL packages immediately. While this is a DoS (not RCE), the 11-byte payload and sub-alerting-threshold bandwidth make it trivially exploitable and difficult to detect. OpenSSL is embedded in NGINX, Apache, Node.js, Python, PHP, MySQL, and PostgreSQL.

[BleepingComputer / Okta](https://www.bleepingcomputer.com/news/security/hollowbyte-ddos-flaw-bloats-openssl-server-memory-with-11-byte-payload/)

---

### [NEW] Metasploit Adds HTTP-to-SMB Relay and RISC-V Payload Support

Metasploit Framework has added a new HTTP-to-SMB relay module allowing attackers to relay NTLM HTTP authentication requests to multiple SMB targets, establishing sessions for further exploitation. The release also adds comprehensive RISC-V payload support (32-bit and 64-bit staged and stageless shell payloads with XOR encoders) and a Linux Fetch Multi payload family that auto-detects target architecture during delivery — one payload and handler can now serve across mipsel, mips64, aarch64, and armv7l targets simultaneously.

[BleepingComputer / Rapid7](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-an-http-to-smb-relay-plus-payload-improvements)

---

## 📋 Policy & Industry News

### [NEW] Ernst & Young Discloses Data Breach — Third-Party Support System Compromised

Ernst & Young (EY), one of the Big Four professional services firms with $53.2B revenue and 406,000 employees, is notifying customers of a data breach caused by unauthorized access to a third-party support ticket system. An unauthorized party accessed the platform between March 28 and April 12, downloading multiple documents — some containing client tax information. EY detected anomalous activity on April 23 and engaged external cybersecurity experts.

EY is offering 24 months of identity monitoring through Experian to affected clients. No group has claimed responsibility, and EY reports no indication of targeted individuals or misuse of stolen data.

**Action:** Big Four audit firms handle sensitive financial data across 150+ countries. This breach, via a third-party support system, underscores supply chain risk in professional services — not just software supply chains.

[BleepingComputer](https://www.bleepingcomputer.com/news/security/ernst-and-young-discloses-data-breach-after-support-system-hack/)

---

### [NEW] Iranian Threat Actors Track U.S. Military Personnel via Commercial Ad Data

Foreign threat actors linked to Iran are leveraging advertising technology metadata and cellular roaming protocols to track the smartphones of U.S. military personnel. By exploiting location data and device identifiers embedded in commercial ad networks, adversaries can monitor the movements of service members — demonstrating how the commercial data broker ecosystem creates intelligence collection opportunities for hostile nation-states.

[Financial Times](https://www.ft.com/content/44351c74-03c8-45ab-823b-5805c0daca5f)

---

### [NEW] CISA and International Partners Publish CVD Program Blueprint

CISA and international partners have released a joint guide for establishing a Coordinated Vulnerability Disclosure (CVD) program. The publication provides step-by-step recommendations for handling external bug reports, establishing legal safe harbors, and collaborating with security researchers — a practical resource for organizations without existing CVD frameworks.

[CISA Guide](https://www.cisa.gov/sites/default/files/2026-07/joint-guide-establishing-a-cvd-program-to-work-with-security-researchers_508c.pdf)

---

## 🛡️ Defense & Detection

### [NEW] OpenClaw AI Agent RCE via WhatsApp — Arbitrary Code Execution Through AI Agent Architectural Flaw

A security researcher has demonstrated that an OpenClaw AI agent integrated with WhatsApp can be exploited for remote code execution on the host system. By sending a specially crafted message, the researcher bypassed validation checks and forced the AI agent to execute arbitrary system commands — highlighting a new attack surface emerging from AI agent integrations with communication platforms.

**Action:** AI agents integrated with messaging platforms (WhatsApp, Slack, Teams) execute commands on host infrastructure. Architectural flaws in these agents — not prompt injection — enable host-level RCE. Audit AI agent deployments for input validation and sandboxing boundaries.

[Medium / Researcher](https://medium.com/@chinmohannayak/i-sent-a-whatsapp-message-to-an-ai-agent-it-ran-my-code-on-the-host-adbbcbb0e0ad)

---

### [NEW] Carding Infrastructure Evolution — Residential Proxies No Longer Sufficient

Flare researchers analyzed 2,889 unique underground posts across 545 threads documenting how carders have shifted from treating residential proxies as a reliable anonymity bypass to requiring a full "identity simulation stack" combining proxies with antidetect browsers, device fingerprints, billing information, time zones, cookies, and transaction behavior. The market increasingly distinguishes "clean" residential IPs (those not previously used against financial services) from "dirty" pools, and carders now demand city/ZIP-code-level geographic precision matching stolen identity data.

**Action:** Defenders should treat residential IP addresses as context signals, not trust indicators. Focus on behavioral consistency across the entire session rather than any single attribute.

[BleepingComputer / Flare](https://www.bleepingcomputer.com/news/security/inside-the-search-for-clean-residential-proxies-for-carding/)
