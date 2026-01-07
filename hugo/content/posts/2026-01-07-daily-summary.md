---
title: TridentLocker ransomware 🚨, Chrome extension data theft 📱, China energy attacks ⚡, Router RCE flaws 🌐, Post-quantum crypto 🛡️
date: 2026-01-07
tags: ["ransomware","china apt","browser extensions","data exfiltration","critical infrastructure","router vulnerabilities","post-quantum cryptography","energy sector","supply chain","malware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: TridentLocker ransomware compromised federal contractor data while malicious Chrome extensions exfiltrated AI conversations from nearly a million users. Chinese state actors dramatically increased attacks on Taiwan's energy infrastructure as critical router vulnerabilities and post-quantum migration deadlines present immediate security challenges.
---

# Daily Threat Intel Digest - 2026-01-07

## 🔴 Critical Threats & Active Exploitation

**[NEW] Sedgwick Government Solutions breach exposes federal agency data**  
TridentLocker ransomware group compromised Sedgwick's federal contractor subsidiary, stealing 3.39 GB of sensitive data from clients including DHS, CISA, USCIS, CBP, and ICE. The attack exploited an isolated file transfer system, with network segmentation preventing wider impact, but stolen data may include claims processing information for government agencies. TridentLocker's emerging RaaS operation has claimed 12 victims since November 2025, targeting critical infrastructure contractors across North America and Europe [[Cyberpress](https://cyberpress.org/sedgwick-tridentlocker-ransomware-attack/); [GBHackers](https://gbhackers.com/sedgwick-acknowledges-data-breach/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/sedgwick-confirms-breach-at-government-contractor-subsidiary/)].

**[NEW] Malicious Chrome extensions steal 900,000 users' AI chats**  
Two data-stealing browser extensions impersonating AITOPIA ("Chat GPT for Chrome with GPT-5" and "AI Sidebar with Deepseek") exfiltrated ChatGPT/DeepSeek conversations from 900,000+ users via deepaichats[.]com C2. The malware harvested complete chat transcripts (including proprietary code and corporate strategies) every 30 minutes, exploiting excessive browser permissions. Despite researcher disclosure in December 2025, both extensions remained active on Chrome Web Store, with one holding Google's "Featured" badge [[Cyberpress](https://cyberpress.org/malicious-chrome-extension-exposed-for-stealing-chatgpt-and-deepseek-chats-from-900000-users/); [GBHackers](https://gbhackers.com/malicious-chrome-extension-leaks-chatgpt-and-deepseek-chats-of-900000-users/)].

**[NEW] China-linked attacks on Taiwan's energy sector surge 1000%**  
Taiwan's National Security Bureau reported Chinese state actors (BlackTech, Flax Typhoon, Mustang Panda, APT41, UNC3886) increased attacks on energy infrastructure tenfold in 2025. Attackers targeted petroleum/electricity/natural gas systems, injecting malware during software upgrades and exploiting hardware/software flaws. Spikes coincided with political events, with 54% more attacks on emergency services/hospitals overall. Industrial control system compromises enable operational intelligence theft [[BleepingComputer](https://www.bleepingcomputer.com/news/security/taiwan-says-chinas-attacks-on-its-energy-sector-increased-tenfold/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical D-Link DSL router flaw actively exploited**  
CVE-2026-0625 (unauthenticated command injection via dnscfg.cgi) affects end-of-life DSL-526B, DSL-2640B, DSL-2740R, and DSL-2780B models. Active exploitation observed through honeypots allows RCE without authentication. D-Link urges immediate device replacement as firmware updates are unavailable – these 2020 EoL devices remain common in consumer/SMB environments [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-d-link-flaw-in-legacy-dsl-routers-actively-exploited-in-attacks/)].

**[NEW] Google patches high-severity WebView bypass**  
CVE-2026-0628 enables attackers to circumvent security policies in Chrome's WebView component, potentially allowing malicious content delivery in embedded browser contexts. Fixed in Chrome 143.0.7499.192/.193; enterprises using WebView-reliant applications should prioritize updates [[GBHackers](https://gbhackers.com/google-warns-of-high-risk-webview-vulnerability/)].

**[NEW] Veeam Backup flaw enables root-level RCE**  
Critical vulnerability in Veeam Backup & Replication v13.0.1.180 and earlier permits attackers to execute arbitrary code with root privileges. Though technical details are sparse, Veeam's urgent advisory indicates widespread impact on backup infrastructure – a high-value target for ransomware operators [[GBHackers](https://gbhackers.com/veeam-backup-vulnerability-exposes-systems/)].

## 🛡️ Defense & Detection

**[NEW] Interactive analysis overcomes static phishing detection gaps**  
Sophisticated phishing campaigns (QR codes, CAPTCHA-protected redirect chains, OAuth abuse) evade traditional email filters. Controlled detonation environments like ANY.RUN enable analysts to solve CAPTCHAs, follow redirects, and submit test credentials to confirm credential harvesting in minutes. This approach captures multi-stage TTPs missed by sandbox-only detection [[Cyberpress](https://cyberpress.org/every-soc-analysts-essential-guide-to-fast-phishing-detection-in-2026/)].

**[NEW] Agentic AI closes identity risk remediation loop**  
Qualys' Agent Grant correlates signals from AD/Entra/Okta to compute quantifiable Identity TruRisk scores, then automates remediation (disabling accounts, enforcing MFA, reducing entitlements) with policy guardrails. Validated risk reduction replaces motion metrics like password rotation rates, addressing identity’s role in 74% of breaches [[Qualys Blog](https://blog.qualys.com/product-tech/2026/01/06/agent-grant-agentic-ai-identity-security)].

## 📋 Policy & Industry News

**[NEW] Australia mandates post-quantum crypto migration by 2030**  
ASD’s Cryptographic Bill of Materials (CBOM) framework requires phasing out RSA/DH/ECDH/ECDSA by end-2030, adopting ML-DSA-87/ML-KEM-1024. Hybrid schemes are discouraged. The LATICE framework (Locate-Assess-Triage-Implement-Communicate) prioritizes long-lived data/infrastructure. Immediate steps: inventory crypto dependencies and demand PQC readiness from vendors [[SOCFortress](https://socfortress.medium.com/planning-for-post-quantum-cryptography-from-policy-mandate-to-practical-action-the-australian-cefb22ff7d0b)].

**[NEW] FCC imposes $10K fines for false robocall database reports**  
New Robocall Mitigation Database rules require annual recertification and 2-factor authentication for submissions. Violations include $10K penalties for false/inaccurate filings and $1K for untimely updates. The policy combats spoofing after voice-cloning attacks exploited verification gaps [[CyberScoop](https://cyberscoop.com/fcc-finalizes-new-penalties-for-robocall-violators/)].