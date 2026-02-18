---
title: Dell RecoverPoint zero-day 🏢, Chromium attacks 🌐, OpenSSL AI flaws 🔍, Atlassian spam 📧, Phobos arrest ⚖️
date: 2026-02-18
tags: ["zero-day exploitation","china apt","browser vulnerabilities","ssl/tls security","ransomware","saas abuse","malware distribution","privilege escalation","threat actors","law enforcement"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Chinese state actors exploit a critical Dell RecoverPoint zero-day to deploy BRICKSTORM and GRIMBOLT malware while attackers actively target Chromium browsers and multiple OpenSSL vulnerabilities emerge from AI discovery. SaaS platforms face abuse through Atlassian Cloud spam campaigns delivering financial scams, and law enforcement disrupts ransomware operations with the arrest of a Phobos affiliate affecting critical infrastructure targets.
---

# Daily Threat Intel Digest - 2026-02-18

## 🔴 Critical Threats & Active Exploitation

**[NEW] Dell RecoverPoint zero-day enables China-nexus espionage campaign**  
Attackers have exploited a critical hardcoded-credential vulnerability (CVE-2026-22769, CVSS 10.0) in Dell RecoverPoint for Virtual Machines since mid-2024 to deploy BRICKSTORM and GRIMBOLT malware, creating "Ghost NICs" on VMware ESXi servers for stealthy lateral movement. UNC6201 leverages the Tomcat Manager's default admin credentials to deploy WAR file web shells, achieving root-level persistence on unpatched appliances prior to v6.0.3.1 HF1. Dell's advisory urges immediate patching as Chinese state actors maintain footholds in less than a dozen known victim networks [[SOC Prime](https://socprime.com/blog/cve-2026-22769-vulnerability/); [CyberScoop](https://cyberscoop.com/china-brickstorm-grimbolt-dell-zero-day/)].

**[NEW] CISA warns of actively exploited Chromium zero-day**  
A Use-After-Free flaw in Chromium's CSS component (CVE-2026-2441, CVSS 8.8) is under active attack, enabling RCE via malicious HTML pages. Google patched it in Chrome 122.0.6261.94 and Edge equivalents, but CISA's KEV addition signals ongoing campaigns targeting browsers beyond Chrome through shared engine vulnerabilities. Users must update immediately as exploitation requires no user interaction beyond page viewing [[Cyberpress](https://cyberpress.org/cisa-chromium-zero-day/)].

**[NEW] Windows ActiveX RCE flaw added to KEV after 18 years**  
CISA added the decades-old CVE-2008-0015 (Windows Video ActiveX Control RCE) to its Known Exploited Vulnerabilities catalog, confirming active attacks via malicious webpages. While primarily impacting legacy systems, unpatched modern environments with ActiveX enabled face arbitrary code execution risks. Federal agencies must patch by March 10, 2026 [[Cyberpress](https://cyberpress.org/cisa-adds-actively-exploited-windows-activex-rce-flaw-to-kev-catalog/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Atlassian Cloud abused in large-scale spam campaigns**  
Cybercriminals exploited Jira Cloud's trusted domain reputation to deliver localized financial scams targeting investors and government entities from December 2025-January 2026. Attackers used free trial instances on AWS IP 13.227.180.4 to bypass SPF/DKIM via Jira Automation rules, avoiding bulk-user invites while delivering malicious links through go.sparkpostmail1.com. Industries with Jira deployments received tailored lures in six languages [[Cyberpress](https://cyberpress.org/atlassian-cloud-powers-spam-scams/)].

**[NEW] ClickFix campaign delivers Matanbuchus 3.0 and AstarionRAT**  
Attackers used ClickFix social engineering to distribute Matanbuchus 3.0 loader via fake MSI downloads, ultimately deploying the new AstarionRAT. The campaign achieves domain controller compromise within 40 minutes using PsExec and rogue "DefaultService" accounts. AstarionRAT employs RSA-encrypted C2 disguised as app telemetry to www.ndibstersoft.com, with Matanbuchus priced at $10K-$15K/month as premium MaaS [[Huntress via Cyberpress](https://cyberpress.org/matanbuchus-3-0-deploys-astarionrat/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] AI discovers 12 OpenSSL zero-days, including 9.8-severity flaw**  
AI systems found twelve OpenSSL zero-days across 2025-2026 releases, ten receiving CVE-2025 IDs and two CVE-2026 IDs. Notably, CVE-2025-15467 (CVSS 9.8) allows remote code execution without valid keys via CMS message parsing. Three vulnerabilities persisted since 1998-2000, predating OpenSSL itself. Five patches were AI-proposed and merged upstream [[Schneier on Security](https://www.schneier.com/blog/archives/2026/02/ai-found-twelve-new-vulnerabilities-in-openssl.html)].

**[NEW] Critical Windows Admin Center privilege escalation patched**  
CVE-2026-26119 (CVSS 8.8) enables authenticated attackers to escalate privileges and execute arbitrary code on managed servers through improper authentication mechanisms. Microsoft's February 17, 2026 patch addresses the flaw, which requires immediate action as exploitation requires low complexity and grants high-impact access to sensitive systems [[Cyberpress](https://cyberpress.org/critical-privilege-escalation-flaw/)].

## 🛡️ Defense & Detection

**[NEW] DigitStealer infrastructure patterns expose macOS infostealer**  
The JXA-based DigitStealer targeting Apple M2 devices exhibits predictable C2 patterns: Njalla nameservers, Tucows-registered domains, and homogeneous nginx/OpenSSH stacks on Abstract Ltd ASN. Defenders can hunt for cryptographic challenge responses in JSON polling and correlate with WHOIS data for early detection. The malware avoids public MaaS panels, suggesting a tightly controlled operation [[Cyberpress](https://cyberpress.org/digitstealer-exposes-macos-vulnerabilities/)].

## 📋 Policy & Industry News

**[NEW] Palo Alto Networks acquires Koi Security for agentic endpoint protection**  
Palo Alto will integrate Koi's AI agent security tech into Prisma AIRS and Cortex XDR to address "agentic endpoints" where AI agents access sensitive data evading traditional EDR. The move responds to rising attacks via authentication bypasses, API RCE, and identity spoofing in AI toolchains [[Cyberpress](https://cyberpress.org/palo-alto-networks-to-acquire-koi-security-to-advance-agentic-endpoint-protection/)].

**[NEW] Polish authorities arrest Phobos ransomware affiliate**  
A 47-year-old alleged Phobos affiliate was arrested in Małopolskie, Poland, facing up to five years for ransomware attacks affecting hospitals, schools, and defense contractors. The operation, part of Europol's "Phobos Aetor" initiative, seized devices and encrypted communication tools tied to the group's 1,000+ global victims [[CyberScoop](https://cyberscoop.com/phobos-ransomware-affiliate-arrested-poland/)].