---
title: Ivanti EPMM critical flaw 🔴, SonicWall admin takeover ⚠️, Bitcoin Depot breach 💰, Claude Code leak weaponized 💻, UNC6783 extortion
date: 2026-04-09
tags: ["code injection","sql injection","apt activity","active exploitation","remote code execution","infostealer","financial sector","enterprise security","authentication bypass","threat actor"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical vulnerabilities in Ivanti EPMM and SonicWall SMA1000 appliances are being actively exploited, with threat actors achieving full administrative control through SQL injection and code injection techniques that bypass authentication mechanisms. The rapid weaponization of the Claude Code leak within 24 hours underscores the speed at which exposed development tools become attack vectors, distributing infostealers like Vidar alongside RATs, while emerging threat actors such as UNC6783 target enterprise support infrastructure for extortion purposes.
---


# Daily Threat Intel Digest - April 9, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] CISA orders emergency Ivanti EPMM patch as exploitation escalates**

CISA has given federal agencies until April 11 to patch CVE-2026-1340, a critical code injection flaw in Ivanti Endpoint Manager Mobile (EPMM) that has been exploited since January. The vulnerability enables unauthenticated remote code execution on internet-exposed appliances, and Shadowserver is tracking approximately 950 vulnerable IPs still online—predominantly in Europe (569) and North America (206). The agency added this vulnerability to its Known Exploited Vulnerabilities catalog and warned that the flaw represents "a frequent attack vector for malicious cyber actors." Organizations outside the federal mandate should prioritize patching immediately given active exploitation in the wild. [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-orders-feds-to-patch-exploited-ivanti-epmm-flaw-by-sunday/); [GBHackers](https://gbhackers.com/cisa-issues-warning-on-critical-ivanti-epmm-flaw/)

**[NEW] Critical SonicWall SMA1000 vulnerabilities enable full admin takeover**

SonicWall has disclosed four vulnerabilities in SMA1000 appliances with no temporary workarounds available. The most severe (CVE-2026-4112, CVSS 7.2) allows SQL injection enabling privilege escalation from read-only admin to full primary administrator control. Two additional flaws (CVE-2026-4114, CVE-2026-4116) bypass TOTP-based MFA in the Appliance Management Console, Connect Tunnel, and Workplace environments. An authentication bypass flaw (CVE-2026-4113) enables credential guessing through observable server response differences. Patched versions 12.4.3-03387 and 12.5.0-02624 are now available, and administrators should upgrade immediately as these vulnerabilities affect only SMA1000 series hardware and virtual appliances. [CyberPress](https://cyberpress.org/multiple-sonicwall-vulnerabilities/); [GBHackers](https://gbhackers.com/multiple-sonicwall-flaws-enable-sql-injection/)

**[NEW] Palo Alto Cortex XSOAR Teams integration flaw allows unauthenticated data access**

A critical vulnerability (CVE-2026-0234, CVSS 9.2) in Cortex XSOAR and Cortex XSIAM's Microsoft Teams integration allows unauthenticated attackers to access and modify sensitive data without credentials. The flaw stems from improper cryptographic signature verification (CWE-347), enabling attackers to impersonate trusted sources and bypass authentication entirely. Versions 1.5.0 through 1.5.51 are vulnerable; patch to version 1.5.52 or later. Since these platforms centralize security operations and incident response workflows, exploitation could disrupt threat detection, hide malicious activity, or expose confidential intelligence. [CyberPress](https://cyberpress.org/palo-alto-cortex-xsoar-flaw/); [GBHackers](https://gbhackers.com/palo-alto-cortex-xsoar-flaw-in-microsoft-teams-integration/)

**[NEW] Bitcoin Depot breach: $3.6M stolen from crypto ATM giant**

Attackers stole approximately 50.9 Bitcoin ($3.665 million) from Bitcoin Depot's corporate wallets after breaching IT systems on March 23. The threat actors harvested credentials to digital asset settlement accounts and moved funds before access was blocked. The company operates over 25,000 Bitcoin ATMs and BDCheckout locations worldwide. While the incident appears contained to corporate environments and did not affect customer platforms, the company acknowledged potential reputational harm and regulatory costs, noting that cyber insurance coverage may not fully offset losses. This follows a separate 2024 breach exposing data from nearly 27,000 users. [BleepingComputer](https://www.bleepingcomputer.com/news/security/crypto-atm-giant-bitcoin-depot-says-hackers-stole-36-million-from-its-wallets/)

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Silver Fox drops ValleyRAT via fake Telegram Chinese language pack**

The Chinese-linked Silver Fox threat group is distributing the ValleyRAT backdoor through a malicious installer disguised as a Telegram Chinese language pack. The attack uses zpaqfranz compression—an uncommon format designed to evade security scanners—and includes logic to detect and evade Chinese antivirus software by dropping legitimate ByteDance programs alongside malicious payloads. Once installed, the malware deploys a vulnerable Wincor Nixdorf driver to gain kernel-level access and disable remaining defenses. The campaign targets Windows systems with a six-step infection chain, and defenders should block the identified Hong Kong-based C2 infrastructure and monitor for unusual zpaqfranz execution. [CyberPress](https://cyberpress.org/fake-telegram-drops-valleyrat/); [GBHackers](https://gbhackers.com/silver-fox-campaign/)

**[NEW] UNC6783 targets Zendesk support tickets for extortion**

Google Threat Intelligence Group has attributed a campaign of BPO compromises to the newly tracked UNC6783 actor, which may be linked to the Raccoon persona. The group social engineers helpdesk staff at business process outsourcing providers, directing victims to spoofed Okta login pages matching the pattern `[.]zendesk-support<##>[.]com`. A key capability is a phishing kit that steals clipboard contents to bypass MFA and register attacker-controlled devices with target organizations. After exfiltrating sensitive support ticket data, UNC6783 extorts victims via ProtonMail. Google is tracking dozens of targeted corporate entities, and defenders should deploy FIDO2 security keys, monitor live chat for abuse, and audit MFA device enrollments. [BleepingComputer](https://www.bleepingcomputer.com/news/security/google-new-unc6783-hackers-steal-corporate-zendesk-support-tickets/)

**[NEW] DragonBreath APT deploys RoningLoader with advanced evasion**

The espionage group DragonBreath (APT-Q-27) is using the RoningLoader malware in a campaign combining DLL side-loading and code injection to bypass traditional security defenses. Active since at least 2022, the group has steadily evolved its capabilities, with recent campaigns documented by QianXin and Sophos. The new loader enables the threat actor to establish persistent footholds in target environments while evading detection through living-off-the-land techniques. [GBHackers](https://gbhackers.com/roningloader-campaign/)

**[UPDATE] Claude Code leak weaponized—Vidar and GhostSocks distributed via GitHub**

The March 31 accidental exposure of Anthropic's Claude Code source material has been fully weaponized. Within 24 hours, threat actors created fake GitHub repositories distributing a Rust-compiled dropper that conducts extensive anti-analysis checks, targets high-performance gaming PCs for potential cryptomining, disables Windows Defender, and delivers Vidar infostealer alongside the GhostSocks RAT. Vidar aggressively harvests browser credentials, session tokens, cryptocurrency wallets, and system data. Organizations should enforce strict software installation policies, restrict developers to officially verified channels, and deploy endpoint detection capable of identifying Rust-compiled malware and behavioral anomalies. [CyberPress](https://cyberpress.org/claude-leak-fuels-malware/)

## ⚠️ Vulnerabilities & Patches

**[NEW] GitLab patches critical DoS and code injection vulnerabilities**

GitLab has released versions 18.10.3, 18.9.5, and 18.8.9 addressing 12 vulnerabilities across Community and Enterprise editions. The most critical (CVE-2026-5173, CVSS 8.5) exposes a method in WebSocket connections allowing authenticated attackers to invoke unintended server-side methods. Two high-severity DoS flaws affect the Terraform state lock API (CVE-2026-1092) and GraphQL API (CVE-2025-12664). Additional issues include code injection via Code Quality reports (CVE-2026-1516), XSS in customizable analytics (CVE-2026-4332), and information disclosure through CSV exports (CVE-2026-2104). GitLab.com and GitLab Dedicated users are protected; self-managed instances require immediate patching. [CyberPress](https://cyberpress.org/gitlab-fixes-critical-bugs/); [GBHackers](https://gbhackers.com/gitlab-addresses-multiple-vulnerabilities/)

**[NEW] Chrome 147 patches critical code execution vulnerabilities**

Google has released Chrome version 147 for Windows, Mac, and Linux, patching multiple vulnerabilities that could allow arbitrary code execution and full system compromise. All users should update immediately to the stable channel release. [GBHackers](https://gbhackers.com/critical-chrome-flaws/)

**[NEW] Apache ActiveMQ vulnerability disclosed**

Apache has published security advisory AV26-330 addressing CVE-2026-34197 affecting ActiveMQ Broker versions prior to 5.19.4 and 6.2.3. Organizations running affected versions should review the advisory and apply necessary updates. [Malware News](https://malware.news/t/apache-activemq-security-advisory-av26-330/105874#post_1)

## 🛡️ Defense & Detection

**[NEW] Meta Business Manager notifications abused for phishing**

Attackers are exploiting legitimate Meta Business Manager partner request notifications to bypass email security filters. By manipulating account display names with phishing content and embedding malicious links, threat actors send emails from authentic Meta infrastructure (facebookmail.com), easily passing spam filters. Victims are redirected to fake Facebook Help pages designed to harvest credentials. Defenders should block identified domains (aisupportpage[.]online, helpforpage[.]online, pagereport[.]online, pagereview[.]online, pagesactnow[.]help, pageshub[.]click), train users to verify login pages directly via browser, and implement hardware security keys for 2FA. [CyberPress](https://cyberpress.org/meta-notifications-abused/); [GBHackers](https://gbhackers.com/meta-business-alerts/)

**[NEW] macOS Atomic Stealer distributed via Script Editor ClickFix variant**

A new campaign targeting macOS users employs a ClickFix technique using Script Editor instead of Terminal to deliver Atomic Stealer (AMOS). Victims visit fake Apple-themed sites offering disk cleanup instructions, which trigger applescript:// URLs to launch Script Editor with pre-filled executable code. The malware downloads a base64+gzip-encoded payload, extracts the AMOS binary, and harvests Keychain data, cryptocurrency wallets, browser credentials, autofill data, and credit cards. macOS 26.4 added Terminal protections against ClickFix but Script Editor remains exploitable. Users should treat Script Editor prompts as high-risk and rely only on official Apple documentation for troubleshooting. [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-macos-stealer-campaign-uses-script-editor-in-clickfix-attack/)

## 📋 Policy & Industry News

**[NEW] Microsoft Partner Center account suspensions block WireGuard, VeraCrypt updates**

Microsoft has suspended developer accounts for maintainers of widely-used open source projects including WireGuard, VeraCrypt, MemTest86, and Windscribe without prior notification. Affected developers report inability to publish Windows driver updates and security patches, with no human contact available through standard support channels. Microsoft VP Scott Hanselman attributed the suspensions to failure to complete mandatory account verification for the Windows Hardware Program, though developers stated they received no warning emails. Following media coverage, Microsoft indicated the issue would be addressed. The situation raises concerns about critical security update availability if similar automated suspensions affect other projects. [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-suspends-dev-accounts-for-high-profile-open-source-projects/)

**[NEW] Anthropic Glasswing initiative signals AI vulnerability discovery at scale**

Anthropic announced Project Glasswing, providing partners including AWS, Apple, Cisco, Google, and Microsoft access to the unreleased Claude Mythos Preview model. The company claims the model has already discovered thousands of high-severity vulnerabilities across major operating systems and browsers. The initiative aims to accelerate defensive security use of AI capabilities, with Anthropic briefing senior U.S. government officials on both offensive and defensive applications. Intelligence community observers have raised concerns about the dual-use implications and potential for such capabilities to flow to adversaries, with Senator Mark Warner calling on industry to "correspondingly accelerate and reprioritize patching." [Malware News](https://malware.news/t/anthropic-s-glasswing-initiative-raises-questions-for-us-cyber-operations/105877#post_1)

**[NEW] AWS AgentCore "Agent God Mode" enables broad IAM privilege escalation**

Unit 42 researchers have documented "Agent God Mode" vulnerabilities in Amazon Bedrock's AgentCore that grant agents broad IAM permissions, enabling privilege escalation and data exfiltration. Organizations using AWS Bedrock agents should review the research and apply recommended controls to limit IAM scope. [Unit 42](https://unit42.paloaltonetworks.com/exploit-of-aws-agentcore-iam-god-mode/)

## ⚡ Quick Hits

- **Eurail breach**: Approximately 300,000 people impacted by a data breach at the European rail ticketing service. [SecurityWeek](https://www.securityweek.com/300000-people-impacted-by-eurail-data-breach/)
- **China supercomputer theft unverified**: Reports of a 10-petabyte data theft from China's Tianjin National Supercomputing Center lack independent confirmation; treat with skepticism pending verification. [GBHackers](https://gbhackers.com/chinas-tianjin-supercomputer-data-theft/)
- **Linux Foundation Slack impersonation**: Social engineering campaign targeting open source developers via Slack impersonating Linux Foundation leadership. [GBHackers](https://gbhackers.com/linux-foundation-leader/)