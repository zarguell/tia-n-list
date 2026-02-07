---
title: SolarWinds exploitation 🔴, Firebase phishing 📧, AI infostealers 🤖, Russian hacktivists 🇷🇺, industrial flaws 🏭
date: 2026-02-07
tags: ["solarwinds exploitation","phishing","ai infostealers","malware distribution","hacktivist threats","industrial vulnerabilities","social engineering","credential theft","domain compromise"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: SolarWinds Web Help Desk instances are being actively exploited to achieve full domain compromise while malicious VS Code extensions target AI developer tools for cognitive context theft. Russian hacktivists are threatening Nordic entities with DDoS attacks as cybercriminals leverage Firebase to bypass email filters and social engineering tactics that combine fake emails with live support calls.
---

# Daily Threat Intel Digest - 2026-02-07

## 🔴 Critical Threats & Active Exploitation

**[NEW] SolarWinds Web Help Desk exploited for full domain compromise**  
Microsoft observed active exploitation of internet-exposed SolarWinds Web Help Desk (WHD) instances enabling unauthenticated remote code execution. Attackers leverage PowerShell and BITS to deploy Zoho ManageEngine RMM tools, establish reverse SSH/RDP persistence, and escalate to DCSync attacks against domain controllers. While the exact CVE used is unconfirmed, vulnerabilities include CVE-2025-40551 (deserialization), CVE-2025-40536 (security bypass), and CVE-2025-26399. Organizations using WHD must patch immediately, isolate exposed instances, and rotate credentials [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/02/06/active-exploitation-solarwinds-web-help-desk/)].  

**[NEW] Phishing campaign abuses Google Firebase to bypass email filters**  
Cybercriminals are leveraging free Firebase developer accounts to send phishing emails from trusted `firebaseapp.com` subdomains, bypassing traditional spam filters. The campaign uses fear/urgency tactics (e.g., fraudulent account alerts) and high-value lures (e.g., fake giveaways) to steal credentials. IOCs include sender addresses like `noreply@pr01-1f199.firebaseapp.com` and redirect chains via `rebrand.ly`. Security teams should monitor unauthorized Firebase subdomain traffic and educate users on social engineering [[Cyberpress](https://cyberpress.org/cybercriminals-use-firebase-distribute-phishing-emails/); [GBHackers](https://gbhackers.com/hackers-exploit-free-firebase-accounts/)].  

**[NEW] AI agent infostealer exfiltrates "cognitive context" from developers**  
A malicious VS Code extension impersonating "Moltbot" is delivering ScreenConnect relays and infostealers targeting AI developer tools. RedLine, Lumma, and Vidar malware families now scrape AI agent "memory" directories to steal proprietary prompts, API keys, and session logs—enabling "Cognitive Context Theft" and lateral movement. The campaign highlights risks in agentic AI workflows lacking sandboxing. Organizations should audit AI tool configurations and block unauthorized extensions [[InfoStealers](https://www.infostealers.com/article/ai-agents-most-downloaded-skill-is-discovered-to-be-an-infostealer/)].  

**[NEW] RenEngine Loader infects 400k+ victims via cracked games**  
A multi-stage malware campaign uses modified Ren’Py game launchers (e.g., cracked Far Cry, FIFA installers) to deliver HijackLoader and execute encrypted payloads. Since April 2025, the campaign has infected 5,000+ daily victims globally, with India, the U.S., and Brazil most affected. The chain includes AV evasion, UAC bypass, and credential theft via DLL sideloading. Defenders should block piracy sites and monitor for Ren’Py processes with unusual network activity [[Cyberpress](https://cyberpress.org/renengine-loader-evades-security/)].  

**[NEW] Apple Pay phishing combines fake emails with live support calls**  
Attackers send Apple-branded emails warning of fraudulent transactions, instructing users to call "support" numbers. Live agents then harvest 2FA codes and payment details by claiming to "secure" accounts. Victims report sophisticated emails with case IDs and fake receipts. Apple never requests 2FA codes via phone—users should verify senders and avoid unsolicited calls [[Malwarebytes](https://www.malwarebytes.com/blog/news/2026/02/apple-pay-phish-uses-fake-support-calls-to-steal-payment-details)].  

## 🎯 Threat Actor Activity & Campaigns  

**[NEW] Russian Legion hacktivists threaten Denmark in "Operation Ragnarök"**  
The state-funded Russian Legion alliance (including ShadowClawZ 404, Russian Partisan) issued a 72-hour deadline to Denmark, demanding aid withdrawal or threatening "digital wasteland" attacks. Though assessed as limited to DDoS/web defacements, the group offers financial incentives to recruits, echoing NoName057(16) tactics. Nordic entities should prepare for DDoS disruptions and monitor CCTV vulnerabilities [[Truesec](https://www.truesec.com/hub/blog/russian-hacktivist-group-russian-legion-initiate-opdenmark)].  

**[UPDATE] DKnife AitM framework expands to hijack app updates**  
China-linked DKnife operators (active since 2019) are using DNS hijacking and deep packet inspection to replace Android/Windows app updates with malware like ShadowPad and DarkNimbus. New findings show Simplified Chinese in configs and targeting of WeChat data, though regional spread includes the Philippines and UAE. Infrastructure remains active as of Jan 2026. Defenders should enforce TLS for updates and inspect DNS anomalies [[Cyberpress](https://cyberpress.org/china-apt-hijacks-linux-devices/)].  

## ⚠️ Vulnerabilities & Patches  

**Teness fixes multiple flaws in Nessus 10.10.x and 10.11.x**  
Teness released Nessus 10.10.2 and 10.11.2 to address undisclosed vulnerabilities in versions 10.10.1/earlier and 10.11.0–10.11.1. Users should update immediately to prevent potential exploitation [[Canadian Centre for Cyber Security](https://cyber.gc.ca/en/alerts-advisories/tenable-security-advisory-av26-095)].  

**Moxa patches critical flaws in industrial computers**  
Moxa fixed CVE-2026-0714 and CVE-2026-0715 affecting UC/V Series devices running OS images prior to MIL v3.4.1 (UC), MIL3 (V), or MIL2 (V2406C). These RCE flaws could allow unauthenticated attackers to compromise industrial systems—prioritize patching for exposed devices [[Canadian Centre for Cyber Security](https://cyber.gc.ca/en/alerts-advisories/control-systems-moxa-security-advisory-av26-094)].  

**Microsoft Edge patches security flaws in stable channel**  
Microsoft updated Edge Stable Channel to v144.0.3719.115 to address vulnerabilities in prior versions. Enterprises should deploy updates via standard mechanisms [[Canadian Centre for Cyber Security](https://cyber.gc.ca/en/alerts-advisories/microsoft-edge-security-advisory-av26-093)].  

## 🛡️ Defense & Detection  

**Guide released for secure syslog-ng deployment**  
SOCFortress published a CIS-inspired hardening guide for syslog-ng, covering TLS enforcement, log integrity, and flow control. It includes an audit script for 35 controls (e.g., disabling plaintext listeners, quota enforcement) to reduce NSM data loss and tampering risks [[SOCFortress](https://socfortress.medium.com/secure-syslog-ng-deployment-and-hardening-guide-dc5c998d1b68)].  

**Cisco shares reference architecture for event SOCs**  
Cisco launched a Event SOCs website and operations guide detailing hardening practices for large-scale cyber events. Recommendations include network segmentation, real-time monitoring, and incident response playbooks tailored for high-visibility environments [[Feedpress](https://feedpress.me/link/23535/17271550/event-soc-guide)].  

## 📋 Policy & Industry News  

**OpenAI launches "Trusted Access" for cybersecurity with safeguards**  
OpenAI debuted GPT-5.3-Codex via a verified framework for autonomous vulnerability hunting, patching, and threat modeling. Access requires KYC (individuals), enterprise audits, or invite-only researcher roles, with $10M in API grants for defensive teams. Guardrails block malware creation/data exfiltration via refusal training and real-time monitoring [[Cyberpress](https://cyberpress.org/openai-unveils-trusted-access-for-cybersecurity-with-enhanced-security-capabilities/)].  

**DHS IG audits biometric data practices at ICE and OBIM**  
The DHS Inspector General initiated a probe into ICE and the Office of Biometric Identity Management (OBIM) focusing on facial recognition, PII collection, and third-party data broker use. Senators Warner and Kaine raised concerns over civil liberties violations in immigration enforcement [[CyberScoop](https://www.cyberscoop.com/dhs-ig-audit-ice-obim-biometric-data-privacy-facial-recognition/)].