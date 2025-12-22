---
title: WatchGuard RCE exploited 🔴, Wonderland SMS malware 📱, darknet insider recruitment 🕵️, AI safety bypasses 🤖, OAuth phishing attacks 🔐
date: 2025-12-22
tags: ["rce vulnerability","sms interception","insider threats","darknet markets","ai safety","oauth attacks","mobile malware","ransomware","phishing","central asia"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Attackers are actively exploiting WatchGuard firewall vulnerabilities and deploying Wonderland SMS malware to intercept communications in Central Asia. Criminal groups are recruiting corporate insiders via darknet markets while bypassing AI safety mechanisms and OAuth protections to compromise critical systems.
---

# Daily Threat Intel Digest - 2025-12-22

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Critical WatchGuard RCE flaw exploited amid mass unpatched deployments**  
Attackers are actively exploiting CVE-2025-14733, a critical RCE vulnerability affecting WatchGuard Firebox firewalls configured for IKEv2 VPN. Successful exploitation enables unauthenticated remote code execution with low complexity and no user interaction. Over 117,000 devices remain exposed online, with Shadowserver tracking continued exposure despite patches released December 19. CISA has added this to its KEV catalog and ordered federal agencies to patch by December 26. Unpatched devices face immediate compromise risk, even if VPN configurations are later removed, due to persistent Branch Office VPN settings. Compromised appliances show indicators including unauthorized process execution and secret exfiltration [[BleepingComputer](https://www.bleepingcomputer.com/news/security/over-115-000-watchguard-firewalls-vulnerable-to-ongoing-rce-attacks/); [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog?search_api_fulltext=CVE-2025-14733)].  

**[NEW] Wonderland malware pioneers bidirectional SMS interception in Central Asia**  
A sophisticated Android malware campaign targeting Uzbekistan users leverages dropper families (MidnightDat, RoundRift) distributed via compromised Telegram accounts to deploy the Wonderland SMS stealer. This malware represents the first mass-spreading bidirectional SMS interceptor in the region, using WebSocket-based C2 to receive real-time commands for SMS interception, call forwarding, USSD execution, and notification suppression. By hijacking OTPs and suppressing security alerts, attackers enable account takeovers and financial fraud. The campaign uses encrypted payloads, dynamic C2 rotation, and strong obfuscation, generating over $2M for threat actors in 2025. Users outside official app stores remain at high risk [[Cyberpress](https://cyberpress.org/wonderland-malware/)].  

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Ukrainian Nefilim affiliate pleads guilty amid revenue-sharing revelations**  
Artem Stryzhak, a Ukrainian national, admitted to conducting Nefilim ransomware attacks against corporations exceeding $100M–$200M in annual revenue across the U.S., Europe, and Australia. Court documents reveal Stryzhak obtained ransomware code in 2021 for a 20% revenue share, using ZoomInfo to research targets and customizing malware per victim. The operation leveraged "Corporate Leaks" sites for double extortion. His sentencing is scheduled for May 2026, while co-conspirator Volodymyr Tymoshchuk remains at large with $11M in bounties. Tymoshchuk is also linked to LockerGoga and MegaCortex operations affecting hundreds of organizations [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ukrainian-hacker-admits-affiliate-role-in-nefilim-ransomware-gang/)].  

**[NEW] Darknet markets fuel insider recruitment at critical infrastructure firms**  
Cybercriminals are escalating recruitment of corporate insiders across banking, telecom, and tech sectors, offering $3,000–$15,000 for network access or data theft. Listings target employees at cryptocurrency exchanges (Coinbase, Binance), cloud providers, and financial institutions, with one ad requesting access to U.S. Federal Reserve systems. Telecom insiders receive up to $15,000 for SIM-swapping operations, while ransomware groups offer profit shares for internal sabotage. Attackers use emotional manipulation and crypto payments to bypass traditional defenses, necessitating behavioral monitoring and darknet surveillance [[Cyberpress](https://cyberpress.org/cybercriminal-insider-threats/)].  

## ⚠️ Vulnerabilities & Patches

**[NEW] "Lies-in-the-Loop" attacks subvert AI safety dialogs for RCE**  
A novel technique called Lies-in-the-Loop (LITL) exploits Human-in-the-Loop (HITL) confirmation dialogs in AI code assistants like Claude Code and Microsoft Copilot Chat. Attackers use prompt injection to manipulate dialog displays—padding text to hide malicious commands or rewriting metadata—to trick users into approving RCE payloads. This undermines a key OWASP LLM Top 10 mitigation (LLM01/LLM06). Anthropic classified the issue as "informative," while Microsoft acknowledged but did not fix the Copilot vulnerability. Defenses require strict command validation, Markdown sanitization, and user education [[Cyberpress](https://cyberpress.org/lies-in-the-loop-attacks/)].  

**[NEW] OAuth device-code phishing bypasses MFA in Microsoft 365**  
Widespread campaigns abuse OAuth 2.0 Device Authorization Grant flows to compromise M365 accounts. Threat actors including TA2723 (financially motivated) and UNK_AcademicFlare (Russia-aligned) use phishing emails/QR codes to redirect users to legitimate Microsoft device login pages. Victims enter device codes, inadvertently authorizing malicious applications that bypass MFA and steal data. Tools like SquarePhish2 and Graphish automate attacks using QR codes and Azure App Registrations. Blocking device-code flows via Conditional Access policies is critical [[Cyberpress](https://cyberpress.org/oauth-device-code-phishing-attacks/)].  

## 🛡️ Defense & Detection

**[NEW] Arkanix Stealer evolves with VMProtect, ChromElevator bypasses**  
The Arkanix credential-stealing malware, distributed via Discord, now includes a C++ "Premium" variant with expanded capabilities: AMSI/ETW bypasses, VMProtect obfuscation, and ChromElevator integration to defeat Chrome's App-Bound Encryption. It harvests data from 20+ browsers, cryptocurrency wallets, VPN clients, and Discord variants, exfiltrating to Cloudflare-shielded C2 servers at `arkanix[.]pw`. Origin IP 195.246.231.60 hosts the Python backend. Defenders should monitor for registry artifacts (`HKEY_LOCAL_MACHINE\HARDWARE\DEVICEMAP\Scsi`) and VM detection API calls [[Malware.News](https://malware.news/t/deep-dive-into-arkanix-stealer-and-its-infrastructure/102764#post_1)].  

## ⚡ Quick Hits
- **OAuth phishing exploits device-code flows** [[Proofpoint via Cyberpress](https://cyberpress.org/oauth-device-code-phishing-attacks/)]  
- **UK government probes cyber incident after media reports** [[SecurityWeek](https://www.securityweek.com/uk-government-acknowledges-it-is-investigating-cyber-incident-after-media-reports/)]  
- **StealC delivered via cracked software lures** [[Malware-Traffic-Analysis](https://malware.news/t/2025-12-22-stealc-from-files-impersonating-cracked-versions-of-popular-software/102760#post_1)]