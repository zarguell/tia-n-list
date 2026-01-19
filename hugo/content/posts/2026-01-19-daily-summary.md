---
title: Database leaks affecting millions 💾, HPE OneView RCE exploited 🚨, Kerberos DNS attacks 🔄, Chrome extension hijacks 🌐
date: 2026-01-19
tags: ["data breaches","remote code execution","kerberos attacks","browser extensions","ransomware","supply chain","adversary-in-the-middle","session hijacking","critical infrastructure","threat actors"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Multiple database leaks expose over 10 million records across recruitment, veterinary, payment, and engineering platforms while a critical HPE OneView RCE vulnerability is actively exploited by the RondoDox botnet for unauthenticated remote code execution. Attackers are also leveraging Kerberos relay attacks via DNS CNAME manipulation to bypass authentication and deploying Chrome extensions that hijack HR/ERP systems through session token theft.
---

# Daily Threat Intel Digest - 2026-01-19

## 🔴 Critical Threats & Active Exploitation

**[NEW] Multiple database leaks expose 10M+ records across global platforms**  
Threat actors claim to have breached databases of Vietnam-based recruitment platform JobsGO (2.3M records with CVs/PII), veterinary platform MyVete (5.57M records/30GB), Senegalese payment service PIXPAY (API keys/JWT tokens), and French engineering firm Groupe Fondasol (888 employee records with access tokens). MyVete faces a $100K ransom demand by Jan 30. These datasets enable targeted phishing, credential abuse, and social engineering campaigns across healthcare, financial, and engineering sectors [[SOCRadar via Malware.News](https://malware.news/t/multiple-database-leak-claims-involve-jobsgo-myvete-pixpay-and-fondasol/103382#post_1)].

**[NEW] Critical HPE OneView RCE (CVE-2025-37164) actively exploited**  
The RondoDox botnet is exploiting this CVSS 10.0 flaw (affects v5.20-10.20) for unauthenticated remote code execution. CISA added it to KEV. Organizations must patch immediately as HPE OneView manages infrastructure globally [[Check Point Research via Malware.News](https://malware.news/t/19th-january-threat-intelligence-report/103381#post_1)].

**[NEW] Kerberos relay attack via DNS CNAMEs bypasses authentication**  
CVE-2026-20929 allows attackers to force victims to request Kerberos tickets for malicious systems, enabling lateral movement even with NTLM disabled. Attackers exploit CNAME manipulation through network MITM positions. Mitigation requires enforcing SMB signing, Channel Binding Tokens for HTTP/S, and LDAP signing [[CyberPress via GBHackers](https://gbhackers.com/new-kerberos-relay-technique-exploits-dns-cnames-to-bypass-existing-defenses/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Five Chrome extensions hijack HR/ERP systems**  
A coordinated campaign deployed five extensions (2.3K+ installs) stealing session tokens from Workday, NetSuite, and SAP SuccessFactors. Attackers block security controls to enable account takeovers via session hijacking. Organizations should audit browser extensions and monitor for anomalous session activity [[GBHackers](https://gbhackers.com/five-chrome-extensions/)].

**[NEW] Remcos RAT targets South Korean users**  
Distributed via fake VeraCrypt installers and illegal gambling sites, the RAT employs evasion techniques to persist on systems. AhnLab warns of broader regional targeting as attackers leverage social engineering to deploy credential theft malware [[AhnLab via Malware.News](https://malware.news/t/remcos-rat-being-distributed-to-korean-users/103378#post_1)].

**[NEW] Operation Poseidon abuses Google Ads redirection**  
Spear-phishing campaigns exploit Google Ads redirection mechanisms to deliver malware to high-value targets. Technical details indicate evasion of traditional email security filters, necessitating URL inspection and ad-tracker monitoring [[Genians via Malware.News](https://malware.news/t/operation-poseidon-spear-phishing-attacks-abusing-google-ads-redirection-mechanisms/103368#post_1)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Modular DS WordPress flaw under active exploitation**  
CVE-2026-23550 (CVSS 10.0) allows unauthenticated admin takeover via exposed routes. Exploitation began Jan 13; upgrade to v2.5.2 immediately. Attackers leverage this to deploy web shells and ransomware [[Check Point Research via Malware.News](https://malware.news/t/19th-january-threat-intelligence-report/103381#post_1)].

**[NEW] ServiceNow "BodySnatcher" flaw enables user impersonation**  
CVE-2025-12420 in Virtual Agent API lets attackers impersonate any user using only an email address, bypassing MFA/SSO. Unauthenticated attackers could execute privileged AI workflows or create admin accounts. Patching is critical for organizations using ServiceNow [[GBHackers](https://gbhackers.com/new-bodysnatcher-flaw/)].

## 🛡️ Defense & Detection

**[NEW] Mandiant releases NTLMv1 rainbow tables**  
Publicly available tables now enable <12-hour cracking of Net-NTLMv1 hashes on <$600 hardware. Attackers can escalate to DCSync for full AD compromise. Organizations must disable NTLMv1 via GPO and monitor Event ID 4624 for "LM"/"NTLMv1" usage [[CyberPress](https://cyberpress.org/mandiant-releases-rainbow-tables-enabling-ntlmv1/)].

**[NEW] Kubernetes worker node hardening guide released**  
Part V of CIS-aligned guidance covers kubelet authentication, X.509 certs, and OS hardening to prevent node-to-cluster compromise. Key steps: disable anonymous access, enforce webhook authorization, and limit filesystem permissions [[SOCFortress](https://socfortress.medium.com/secure-kubernetes-deployment-guide-self-managed-part-v-3b2b26468ff5?source=rss-36613248f635------2)].

## 📋 Policy & Industry News

**[NEW] CIRO breach impacts 750K Canadian investors**  
The Investment Regulatory Organization confirmed a 2025 breach exposed names, SINs, income data, and account numbers. Though credentials weren't stolen, affected individuals receive 2-year credit monitoring. The 9,000-hour investigation found no evidence of dark web data publication [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ciro-data-breach-last-year-exposed-info-on-750-000-canadian-investors/)].

**[NEW] Japanese nuclear regulator loses phone in China**  
A Nuclear Regulation Authority employee lost a work phone containing sensitive contact info during a China trip in Nov 2025. The incident underscores geopolitical espionage risks and data loss protocols for critical infrastructure personnel [[DataBreaches.Net](https://malware.news/t/japanese-nuclear-regulator-employee-loses-phone-containing-sensitive-info-in-china/103372#post_1)].

## ⚡ Quick Hits

- OpenAI spotted testing "Sonata" and "Salute" features for ChatGPT, potentially expanding audio/ML capabilities [[BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/openai-hostname-hints-at-a-new-chatgpt-feature-codenamed-sonata/)]  
- Microsoft released OOB updates fixing Remote Desktop credential failures and Windows 11 23H2 shutdown bugs [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-releases-oob-windows-updates-to-fix-shutdown-cloud-pc-bugs/)]  
- WhisperPair Bluetooth flaw still impacts millions of devices lacking firmware patches for Fast Pair vulnerabilities [[Panda Security](https://malware.news/t/can-hackers-eavesdrop-and-track-people-via-bluetooth-audio-devices/103379#post_1)]