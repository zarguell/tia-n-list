---
title: Juniper router RCE 🔥, Steaelite RAT extortion 💰, Google API data leaks 🔐, SeaFlower crypto backdoor 🪙, Infostealer SSO attacks 🔓
date: 2026-02-27
tags: ["router vulnerabilities","rat malware","api security","web3 threats","credential theft","ransomware","endpoint security","jail escape","supply chain","brute force"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical Juniper PTX router vulnerabilities and emerging Steaelite RAT campaigns pose significant infrastructure risks, while exposed Google API keys silently leak sensitive Gemini AI data to attackers. SeaFlower backdoors targeting Web3 wallets and infostealer-driven SSO brute-force attacks demonstrate escalating threats to cryptocurrency assets and corporate identity systems.
---

# Daily Threat Intel Digest - 2026-02-27

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical Juniper PTX RCE Enables Full Router Takeover**  
A critical vulnerability (CVE-2026-21902, CVSS 9.8) in Juniper PTX Series routers running Junos OS Evolved allows unauthenticated attackers to execute code as root via exposed On-Box Anomaly Detection services [[Juniper advisory](https://cyberpress.org/juniper-ptx-routers-at-risk/); [[GBHackers](https://gbhackers.com/juniper-networks-ptx-vulnerability/)]. Attackers can sniff traffic, pivot deeper into networks, and maintain persistence. Immediate patching to 25.4R1-S1-EVO/25.4R2-EVO or disabling the service (`request pfe anomalies disable`) is critical as core network gear requires tight protection against such bypasses.

**[NEW] Critical Trend Micro Apex One Flows Allow Remote Code Execution**  
Eight vulnerabilities in Trend Micro Apex One endpoint protection platform include two critical unauthenticated RCE flaws enabling malicious code uploads [[GBHackers](https://gbhackers.com/critical-trend-micro-apex-one-vulnerabilities/)]. A Critical Patch (Solution ID KA-0022458) was released Feb 24 for Apex One 2019 on-premises (Windows) and cloud versions. Organizations running unpatched instances face full system compromise as attackers bypass endpoint defenses.

**[NEW] Steaelite RAT Powers Double-Extortion Attacks**  
A new RAT, Steaelite, integrates ransomware deployment, credential theft, and file exfiltration into a single browser-based dashboard, streamlining double-extortion campaigns [[CyberPress](https://cyberpress.org/steaelite-rat-drives-extortion/)]. Features include real-time surveillance, clipboard hijacking for crypto theft, and upcoming Android ransomware modules. Enterprises face heightened risk as data theft occurs pre-encryption, rendering traditional ransomware defenses insufficient.

**[NEW] Google API Keys Expose Gemini Data Without Warning**  
Legacy Google API keys—previously deemed harmless for client-side use—silently gained access to Gemini AI endpoints after Generative Language API enablement [[Truffle Security](https://cyberpress.org/google-api-key-misconfigurations-lead-to-silent-data-exposure-via-gemini/); [[BleepingComputer](https://www.bleepingcomputer.com/news/security/previously-harmless-google-api-keys-now-expose-gemini-ai-data/)]. Attackers exploit exposed keys to access private data and rack up AI usage bills. Truffle Security found 2,800+ live keys from major firms. Rotate keys, audit Gemini API usage, and enforce scoping to prevent silent data leakage.

## 🎯 Threat Actor Activity & Campaigns

**[NEW] SeaFlower Backdoor Targets Web3 Wallets**  
A sophisticated campaign, SeaFlower, injects backdoors into legitimate Web3 wallet apps (MetaMask, Coinbase Wallet) to exfiltrate seed phrases via cloned websites promoted through search engines [[CyberPress](https://cyberpress.org/seaflower-targets-web3-wallets/)]. Chinese-language artifacts suggest a Chinese-speaking actor. Users downloading wallets from unofficial sources face total wallet compromise; restrict downloads to official app stores and validate domains.

**[NEW] Infostealers Drive Corporate SSO Brute-Force Attacks**  
Infostealer-extracted credentials fuel credential-stuffing attacks against corporate SSO gateways, particularly F5 BIG-IP devices [[GBHackers](https://gbhackers.com/massive-brute-force-attacks/)]. Defused Cyber’s analysis of 70 compromised credentials confirmed 71% originated from infostealer logs. Enforce MFA, monitor for anomalous login patterns, and rotate credentials linked to known infostealer breaches.

## ⚠️ Vulnerabilities & Patches

**[NEW] FreeBSD Jail Escape Vulnerability**  
CVE-2025-15576 allows attackers to escape FreeBSD jail environments (v14.3, 13.5) and gain full host filesystem access [[GBHackers](https://gbhackers.com/freebsd-vulnerabilities/)]. Update to patched versions immediately as jails rely on strict isolation, and this flaw enables lateral movement from compromised containers.

**[NEW] Malicious Go Crypto Module Deploys Rekoobe Backdoor**  
A backdoored Go cryptography module on pkg.go.dev harvests passwords and installs the Rekoobe Linux backdoor in developer/CI environments [[GBHackers](https://gbhackers.com/malicious-go-crypto-module/)]. The package mimics trusted libraries to hijack password prompts. Audit Go dependencies via `go list -m -u all` and avoid third-party crypto packages lacking reputable maintainers.

## 🛡️ Defense & Detection

**[NEW] Microsoft Defender Adds URL Click Alerts for Teams**  
Microsoft Defender for Office 365 now extends URL click alerts to Microsoft Teams, surfacing risky link activity with full message context in the Defender portal [[CyberPress](https://cyberpress.org/microsoft-defender-enhances-security/); [[GBHackers](https://gbhackers.com/microsoft-defender-enhances-security-with-url-click-alerts/)]. Enabled by default for MDO Plan 2/M365 E5, this closes a visibility gap against phishing in collaborative platforms. Update SOC playbooks to incorporate Teams alerts and hunt via KQL: `AlertEvidence | where ServiceSource == "Microsoft Defender for Office 365" | where Title has "Teams"`.