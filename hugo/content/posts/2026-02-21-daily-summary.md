---
title: BeyondTrust RCE exploitation 🔴, Healthcare ransomware attacks 🏥, Starkiller phishing service 🎣, French banking breach 💰, AD persistence techniques 🔍
date: 2026-02-21
tags: ["ransomware","rce exploitation","healthcare sector","phishing-as-a-service","banking sector","active directory","supply chain","vpn security","data breach","mfa bypass"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical RCE vulnerabilities in BeyondTrust and supply chain breaches in Pulse Secure are enabling widespread ransomware deployment against healthcare and high-tech targets, while the Starkiller phishing platform democratizes MFA-bypass attacks for low-skill attackers. French banking infrastructure suffered a massive credential-based breach affecting 1.2 million accounts, and attackers are weaponizing Active Directory dynamic objects for stealthy persistence that evades traditional forensic detection.
---

# Daily Threat Intel Digest - 2026-02-21

## 🔴 Critical Threats & Active Exploitation

**[NEW] BeyondTrust Remote Support RCE actively exploited in ransomware campaigns**  
Attackers are leveraging CVE-2026-1731, a pre-authentication remote code execution flaw in BeyondTrust Remote Support (≤25.3.1) and Privileged Remote Access (≤24.3.4), to deploy ransomware. CISA confirmed active exploitation and added the flaw to its KEV catalog, urging immediate patches. The vulnerability enables OS command injection via crafted requests, allowing unauthenticated attackers to gain full system control. Healthcare and critical infrastructure organizations are prime targets due to widespread use of BeyondTrust for remote access. Mitigate by upgrading to Remote Support 25.3.2+ or PRA 25.1.1+ and restricting internet exposure of management interfaces [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-beyondtrust-rce-flaw-now-exploited-in-ransomware-attacks/); [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)].

**[NEW] Ransomware forces University of Mississippi Medical Center to shut down 35 clinics**  
A ransomware attack at the University of Mississippi Medical Center (UMMC) took information systems offline, forcing the closure of all 35 statewide clinics and cancellation of non-urgent appointments. The incident highlights escalating risks to healthcare delivery, where encryption of EHRs and scheduling systems disrupts patient care. UMMC has not disclosed the ransomware strain or data theft status. Defenders should isolate clinical networks, enforce offline backups, and monitor for incremental ransomware variants targeting healthcare [[Cyberwarzone via Malware.news](https://malware.news/t/ummc-ransomware-attack-forces-closure-of-35-mississippi-clinics/104298#post_1)].

**[NEW] Pulse Secure network breached via backdoor embedded in VPN software**  
Pulse Secure (Ivanti) suffered a supply-chain breach after attackers implanted a backdoor in its VPN code, affecting 119 customer organizations. The intrusion underscores recurring Ivanti VPN vulnerabilities exploited by state-aligned groups. Compromised VPN appliances provide attackers with persistent network access and lateral movement capabilities. Ivanti customers should audit VPN logs for anomalous authentication, apply emergency patches, and rotate all credentials stored in VPN sessions [[Cyberwarzone via Malware.news](https://malware.news/t/pulse-secure-network-hacked-via-backdoor-embedded-in-its-vpn-software/104299#post_1)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Starkiller phishing-as-a-service proxies real login pages to bypass MFA**  
A new phishing-as-a-service platform named Starkiller enables attackers to relay victims through legitimate login pages, capturing credentials and session tokens in real time. The service uses reverse proxies and URL masking (e.g., `login.microsoft.com@[malicious-site]`) to evade traditional detection. It logs keystrokes, steals MFA tokens, and provides campaign analytics, significantly lowering the barrier for low-skill attackers. Organizations should train users to inspect full URLs, deploy anti-phishing tools that detect proxy behaviors, and monitor for session hijacking [[Krebs on Security](https://krebsonsecurity.com/2026/02/starkiller-phishing-service-proxies-real-login-pages-mfa/); [Abnormal AI analysis](https://abnormal.ai/blog/starkiller-phishing-kit)].

**[NEW] Japanese tech giant Advantest confirms ransomware attack**  
Advantest, a $120B market-cap semiconductor testing equipment leader, detected a ransomware intrusion on February 15 that may have exposed customer and employee data. The incident disrupted corporate networks and required third-party incident response. While no ransomware group has claimed responsibility, the attack reflects escalating targeting of high-tech supply chains by financially motivated actors. Defenders should加强网络分段 and prioritize firmware integrity monitoring for industrial equipment suppliers [[BleepingComputer](https://www.bleepingcomputer.com/news/security/japanese-tech-giant-advantest-hit-by-ransomware-attack/)].

**[NEW] French banking registry breach exposes 1.2 million accounts via compromised credentials**  
Attackers accessed France’s national bank account registry (FICOBA) using credentials stolen from a civil servant, exposing data on 1.2 million accounts including IBANs, identities, and addresses. The breach disrupted the registry’s operations and prompted fraud warnings. Organizations should enforce phishing-resistant MFA for administrative accounts and audit logging for sensitive financial databases [[BleepingComputer](https://www.bleepingcomputer.com/news/security/data-breach-at-french-bank-registry-impacts-12-million-accounts/); [DataBreaches.Net](https://databreaches.net/2026/02/20/a-single-compromised-account-gave-hackers-access-to-1-2-million-french-banking-accounts/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Roundcube CVE-2025-49113 added to CISA KEV amid active exploitation**  
CISA added CVE-2025-49113, a critical vulnerability in Roundcube Webmail versions prior to 1.5.10/1.6.11, to its Known Exploited Vulnerabilities catalog. The flaw (details undisclosed) is actively exploited in the wild. Administrators should update to patched versions immediately and restrict webmail access to trusted networks [[Canadian Centre for Cyber Security](https://cyber.gc.ca/en/alerts-advisories/roundcube-security-advisory-av25-309)].

**[NEW] Windows Notepad Markdown RCE (CVE-2026-20841) PoC released**  
A high-severity RCE vulnerability in modern Windows Notepad (versions ≤11.2508) allows command injection via malicious Markdown links when users Ctrl+click them. PoC exploits are publicly available, enabling arbitrary code execution. Microsoft patched the issue in build 11.2510+. Defenders should enforce Microsoft Store updates and block execution of `.md` files from untrusted sources [[Cyber Press](https://cyberpress.org/poc-released-for-windows-notepad-vulnerability-enabling-malicious-command-execution/)].

**[NEW] PayPal data breach exposed PII for 6 months due to software error**  
A coding error in PayPal’s Working Capital loan app exposed names, SSNs, and other PII of business customers from July to December 2025. PayPal reversed the code after discovery and offered credit monitoring. The breach underscores risks of insecure data handling in fintech platforms. Users should enable account alerts and monitor credit reports for identity theft [[BleepingComputer](https://www.bleepingcomputer.com/news/security/paypal-discloses-data-breach-exposing-users-personal-information/); [DataBreaches.Net](https://databreaches.net/2026/02/20/a-single-compromised-account-gave-hackers-access-to-1-2-million-french-banking-accounts/)].

## 🛡️ Defense & Detection

**[NEW] Active Directory dynamic objects abused for stealthy persistence**  
Attackers are weaponizing AD dynamic objects, which self-delete after a TTL, to bypass quotas, pollute ACLs, and erase forensic evidence. Techniques include creating ephemeral machine accounts to bypass MAQ, corrupting AdminSDHolder with orphan SIDs, and exploiting hybrid sync gaps in Entra ID. Defenders should monitor for creation of objects with `entryTTL` or `msDS-Entry-Time-To-Die` attributes and enforce real-time alerting on anomalous ACL changes [[Tenable Blog](https://www.tenable.com/blog/active-directory-dynamic-objects-stealthy-threat)].

**[NEW] Anthropic launches Claude Code Security for AI-driven vulnerability scanning**  
Anthropic introduced Claude Code Security, an embedded scanning tool for codebases that identifies vulnerabilities and suggests patches. Early testing shows effectiveness in finding high-severity flaws, but researchers note it may miss complex threats requiring human analysis. The tool represents a shift toward AI-augmented security reviews but requires validation to avoid false negatives. Security teams should integrate it as a supplement, not replacement, for manual code reviews [[CyberScoop](https://cyberscoop.com/anthropic-claude-code-security-automated-security-review/)].

## 📋 Policy & Industry News

**[NEW] Google blocks 1.75 million malicious apps from Play Store in 2025**  
Google prevented 1.75M policy-violating apps from reaching Android users, down from 2.36M in 2024, citing improved AI-driven detection. Over 80,000 developer accounts were banned. Enhanced protections include expanded fraud coverage and in-call scam defenses. Defenders should enable Play Protect and prioritize scanning of sideloaded apps [[Cyber Press](https://cyberpress.org/google-blocks-1-75-million-malicious-app/); [GBHackers](https://gbhackers.com/1-75-million-malicious-apps-blocked/)].

**[NEW] Winter Olympics 2026 spur hacktivist campaigns targeting defense industry**  
Hacktivist groups are coordinating attacks on defense contractors and Olympics sponsors via DDoS and data leaks, exploiting heightened event visibility. Google Threat Intelligence notes overlap with state-aligned actors targeting supply chains. Organizations tied to the Games should increase monitoring of public-facing assets and prepare for brand-impacting disruptions [[Rapid7 Blog](https://www.rapid7.com/blog/post/it-hacktivism-winter-olympics-2026)].