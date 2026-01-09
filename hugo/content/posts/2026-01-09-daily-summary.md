---
title: Undertow RCE exploitation 🔴, AI infrastructure campaigns 🤖, Chinese APT telco breaches 🏢, Ghost Tap Android malware 📱
date: 2026-01-09
tags: ["rce attacks","ai infrastructure","apt activity","telecommunications","mobile malware","oauth attacks","session hijacking","unauthenticated attacks","financial fraud","authentication bypass"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical RCE vulnerabilities in Undertow HTTP servers enable unauthenticated attackers to perform session hijacking attacks while coordinated campaigns target AI infrastructure deployments with SSRF exploits and LLM reconnaissance. Chinese APT group UAT-7290 continues breaching telecommunications companies through edge device exploits as "Ghost Tap" Android malware facilitates unauthorized NFC transactions and OAuth attacks bypass Microsoft Entra authentication protections.
---

# Daily Threat Intel Digest - January 9, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical RCE in Undertow HTTP Server enables session hijacking**  
Attackers are actively exploiting CVE-2025-12543 (CVSS 9.6) in Undertow HTTP servers, a core component powering millions of Java applications on WildFly and JBoss EAP platforms. The flaw stems from improper validation of HTTP Host headers, enabling unauthenticated attackers to perform cache poisoning, network reconnaissance, and session hijacking attacks. Red Hat has released emergency patches (RHSA-2026:0386/RHSA-2026:0383) and states no workarounds exist, making immediate patching critical for production environments. [[Cyber Press](https://cyberpress.org/undertow-http-server-vulnerability/)]

**[NEW] SmarterMail pre-auth RCE exploited via PoC**  
SmarterTools SmarterMail servers face unauthenticated RCE attacks through CVE-2025-52691 (CVSS 10.0), allowing attackers to bypass authentication via path traversal in file uploads. Attackers can write arbitrary files to web-accessible directories by manipulating the `guid` parameter in multipart requests, enabling web shell deployment. Despite fixes released in October 2025, public disclosure in December created a 3-month exposure window. Organizations running vulnerable builds (≤9406) must upgrade to build 9413 immediately. [[Cyber Press](https://cyberpress.org/smartertools-smartermail-vulnerability/); [WatchTowr Labs](https://labs.watchtowr.com/do-smart-people-ever-say-theyre-smart-smartertools-smartermail-pre-auth-rce-cve-2025-52691/)]

**[UPDATE] AI infrastructure attacks intensify with 91K+ sessions**  
GreyNoise intelligence confirms coordinated campaigns targeting AI deployments have surged to 91,000+ sessions since October 2025. Two distinct operations identified: 1) SSRF attacks exploiting Ollama and Twilio integrations (1,688 sessions/48h peak), and 2) LLM endpoint reconnaissance campaigns (80,469 sessions across 73+ APIs). Attackers use benign queries like "How many states in the US?" to fingerprint OpenAI, Claude, and Gemini models without triggering alerts. Implement strict egress filtering and DNS blocking for OAST callback domains. [[GreyNoise](https://www.greynoise.io/blog/threat-actors-actively-targeting-llms)]

**[UPDATE] Ni8mare RCE spreads in n8n automation servers**  
Self-hosted n8n workflow automation platforms face critical CVE-2026-21858 (CVSS 10.0) enabling unauthenticated RCE through webhook endpoint exploitation. Attackers manipulate content-type parsing to access sensitive files (credentials, encryption keys), then forge admin sessions for command execution. All versions prior to 1.121.0 are vulnerable; patch immediately and rotate all stored secrets due to potential compromise. [[SOCFortress](https://socfortress.medium.com/n8n-cve-2026-21858-ni8mare-a656405fccce)]

## ⚠️ Vulnerabilities & Patches

**[NEW] Cisco switches globally hit by DNS client reboot loops**  
A firmware bug in Cisco's DNS client is causing widespread reboot loops across CBS250/350, Catalyst C1200, and SG550X series switches. Devices crash when attempting to resolve DNS queries (e.g., "www.cisco.com"), logging fatal "SRCADDRFAIL" errors. Administrators report cycles every few minutes, disrupting network operations. Temporary mitigations include disabling DNS resolution or blocking outbound internet access from management interfaces until patches release. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisco-switches-hit-by-reboot-loops-due-to-dns-client-bug/)]

**[NEW] jsPDF vulnerability exposes secrets via generated PDFs**  
A critical flaw in the jsPDF JavaScript library allows attackers to steal sensitive data when users generate PDFs on malicious websites. The vulnerability enables data exfiltration through manipulated PDF content, potentially accessing local files or browser sessions. Developers using jsPDF versions prior to the January 8 patch must update immediately. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/critical-jspdf-flaw-lets-hackers-steal-secrets-via-generated-pdfs/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Chinese APT UAT-7290 breaches Southeast European telcos**  
Cisco Talos attributes telco intrusions to UAT-7290, a China-nexus actor active since 2022, now expanding beyond South Asia. The group leverages Linux malware (RushDrop, SilentRaid, Bulbature) and one-day exploits on edge devices to deploy operational relay boxes (ORBs). They establish persistence through credential theft and port forwarding, facilitating lateral movement for other China-aligned actors. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-china-linked-hackers-breach-telcos-using-edge-device-exploits/)]

**[NEW] "Ghost Tap" Android malware drains bank accounts via NFC**  
Chinese threat actors weaponize NFC-enabled Android malware to execute unauthorized tap-to-pay transactions. Group-IB confirms $355,000 in fraudulent losses from a single operation targeting banking apps. The malware hijacks NFC payment protocols, enabling remote fund transfers without victim interaction. [[GBHackers](https://gbhackers.com/new-ghost-tap-attack/)]

## 🛡️ Defense & Detection

**[NEW] Microsoft mandates MFA for 365 Admin Center**  
Microsoft will block password-only access to Microsoft 365 admin centers starting February 9, 2026, affecting portal.office.com/adminportal, admin.cloud.microsoft, and admin.microsoft.com. The policy counters credential-stuffing attacks targeting high-privilege accounts. Organizations must enable MFA for all admins via Microsoft Authenticator, SMS, or hardware tokens to prevent lockouts. [[Cyber Press](https://cyberpress.org/microsoft-enforces-mandatory-mfa-for-microsoft-365-admin-center-logins/)]

**[NEW] New OAuth attack bypasses Entra authentication**  
The "ConsentFix" (AuthCodeFix) attack exploits Microsoft Entra's OAuth 2.0 flow to steal authorization codes from Azure CLI/PowerShell logins. Attackers redirect users to malicious URIs, capture authorization codes from error pages, and redeem them for privileged tokens within 10 minutes. Defenders should enforce Token Protection and monitor for non-interactive sign-ins after user logins. [[Cyber Press](https://cyberpress.org/new-oauth-based-attack/); [GlückKanja](https://www.glueckkanja.com/de/posts/2025-12-31-vulnerability-consentfix)]

## 📋 Policy & Industry News

**[NEW] Trump withdraws US from international cyber organizations**  
The administration exited the Global Forum on Cyber Expertise, Online Freedom Coalition, and European Centre of Excellence for Countering Hybrid Threats, citing "mismanagement" and "contrary interests." Critics warn the move creates leadership vacuums exploitable by adversaries. [[CyberScoop](https://cyberscoop.com/trump-pulls-us-out-of-international-cyber-orgs/)]

**[NEW] UK launches £210M cyber action plan**  
The UK government established a central Government Cyber Unit to coordinate risk management across departments, backed by a Software Security Ambassador Program (Cisco, Palo Alto Networks, NCC Group). The plan enforces supply chain security through the Cyber Security and Resilience Bill. [[Cyber Press](https://cyberpress.org/uk-strengthen-defenses-across-government-departments/)]

**[NEW] CISA retires 10 emergency cyber directives**  
CISA closed its largest batch of Emergency Directives (2019-2024), including SolarWinds mitigation and Microsoft Exchange protections, as required actions shift to Binding Operational Directive 22-01's Known Exploited Vulnerabilities catalog. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-retires-10-emergency-cyber-orders-in-rare-bulk-closure/)]

## ⚡ Quick Hits

- **ChatGPT Health launches** with isolated data processing and physician-developed safety frameworks [[Cyber Press](https://cyberpress.org/chatgpt-health-a-dedicated-space/)]  
- **CrowdStrike acquires SGNL** for $740M to enhance just-in-time identity access controls [[CyberScoop](https://cyberscoop.com/crowdstrike-sngl-deal-740-million/)]  
- **Texas court blocks Samsung TV data collection** (later vacated) over ACR surveillance concerns [[BleepingComputer](https://www.bleepingcomputer.com/news/security/texas-court-blocks-samsung-from-collecting-smart-tv-viewing-data-then-vacates-order/)]