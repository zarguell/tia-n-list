---
title: Notepad++ supply chain hijack 🔓, ShinyHunters vishing expansion 📞, MongoDB ransomware campaign 💰, Arsink Android RAT 📱, ClawDBot RCE flaw ⚡
date: 2026-02-02
tags: ["supply chain attack","apt activity","ransomware","mobile malware","vulnerability management","android security","database security","credential theft","phishing","extortion"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Chinese state actors compromised Notepad++ update infrastructure to distribute malicious installers, while ShinyHunters expanded operations with vishing and DDoS attacks against SSO credentials. The MongoDB ransomware campaign wipes unauthenticated databases demanding Bitcoin payments, Arsink RAT infects 45,000 Android devices through cloud abuse, and a critical ClawDBot vulnerability enables one-click RCE attacks requiring immediate patching.
---

# Daily Threat Intel Digest - 2026-02-02  

## 🔴 Critical Threats & Active Exploitation  

**[NEW] Notepad++ supply chain hijacked by Chinese state actors**  
Attackers compromised Notepad++'s update infrastructure for six months, selectively redirecting users to malicious installers after gaining access to the hosting provider in June 2025. The operation exploited insufficient cryptographic verification in older versions, with threat actors leveraging stolen credentials to maintain access until December 2025. Notepad++ responded by migrating to a hardened hosting environment, enforcing certificate/signature verification in WinGup v8.8.9, and mandating XMLDSig verification in v8.9.2. Users must update immediately due to the precision targeting and sophistication of this state-sponsored campaign [[Cyberpress](https://cyberpress.org/state-sponsored-hackers-hijack-notepad-update-servers-to-push-users-to-malicious-sites/); [SecurityWeek](https://www.securityweek.com/notepad-supply-chain-hack-conducted-by-china-via-hosting-provider/); [GBHackers](https://gbhackers.com/notepad-users-targeted/)].  

**[UPDATE] ShinyHunters expands operations with vishing, harassment, and DDoS**  
ShinyHunters now employs voice phishing (vishing) calls, fake SSO login sites, and new extortion tactics like victim harassment and DDoS attacks to steal SSO credentials and MFA codes. After compromising cloud apps (SharePoint, Salesforce, DocuSign), attackers use stealth techniques like enabling Google Workspace's "ToogleBox Recall" to delete MFA notification emails. Google added phishing domains to Chrome Safe Blogging and released detection rules for Okta and SharePoint abuse. Organizations should adopt FIDO2/passkeys over SMS-based MFA [[Cyberpress](https://cyberpress.org/google-flags-shinyhunters-expansion/); [GBHackers](https://gbhackers.com/shinyhunters-threat/)].  

**[NEW] Moltbook AI vulnerability exposes 1.5M users' credentials**  
An insecure database misconfiguration in the AI agent social network exposed emails, JWT tokens, and API keys via sequential ID enumeration. The flaw enables credential hijacking, lateral movement to integrated services (email/calendar), and prompt injection attacks. Bot registrations inflated user counts to 1.5M, with no patches confirmed. Users must revoke exposed API keys and sandbox agent executions [[Cyberpress](https://cyberpress.org/moltbook-ai-flaw-leaks/); [GBHackers](https://gbhackers.com/moltbook-ai-flaw-exposing-api-keys-and-login-credentials/)].  

**[NEW] MongoDB ransomware campaign compromises 45% of exposed instances**  
Attackers are wiping unauthenticated MongoDB databases and leaving extortion notes demanding ~0.005 BTC (~$500). Of 208,500 exposed MongoDB servers, 3,100 lack authentication and 45% of those were already compromised. Nearly half of all exposed instances run outdated versions vulnerable to denial-of-service flaws. Administrators should firewall instances, enable authentication, and update to patched versions [[BleepingComputer](https://www.bleepingcomputer.com/news/security/exposed-mongodb-instances-still-targeted-in-data-extortion-attacks/); [GBHackers](https://gbhackers.com/hackers-target-mongodb-instances/)].  

**[NEW] NationStates breach exposes MD5 hashes and user data**  
A vulnerability in the "Dispatch Search" feature allowed a player to achieve RCE, copying email addresses (including historical), MD5 password hashes, IPs, and UserAgent strings. The site remains offline for a full server rebuild, with data exposed for 1.6M users. No payment data was stolen, but partial telegram message exposure is suspected. Passwords were stored using obsolete MD5 hashing [[BleepingComputer](https://www.bleepingcomputer.com/news/security/nationstates-confirms-data-breach-shuts-down-game-site/)].  

## 🎯 Threat Actor Activity & Campaigns  

**[UPDATE] ShadowHS fileless Linux malware automates lateral spread**  
ShadowHS now uses RustScan for SSH discovery and "spirit" for brute-force logins, enabling rapid lateral movement. The malware fingerprints security tools (CrowdStrike, Cortex XDR) and kills rivals (Kinsing, Ebury) before exfiltrating data via rsync over GSocket tunnels to 62.171.153[.]47. IOCs include loader hashes (20c1819c2fb886375d9504b0e7e5debb87ec9d1a53073b1f3f36dd6a6ac3f427) and MITRE ATT&CK mappings like T1059.004 (Unix Shell) [[Cyberpress](https://cyberpress.org/shadowhs-spreads-across-linux/); [GBHackers](https://gbhackers.com/fileless-linux-malware/)].  

**[NEW] Arsink RAT targets 45,000 Android devices via cloud abuse**  
Distributed through fake "mod/pro" app versions, Arsink steals SMS, contacts, photos, and audio, using Google Drive (via Apps Script), Firebase, and Telegram for exfiltration. Remote capabilities include flashlight control, wallpaper changes, and storage wiping. Egypt leads with 13,000 infections, followed by Indonesia (7,000). Google Play Protect blocks known variants, but attackers rapidly rotate infrastructure [[Cyberpress](https://cyberpress.org/arsink-rat-targets-android/); [GBHackers](https://gbhackers.com/arsink-rat/)].  

**[NEW] Malicious Google Ads push Mac cleaner scams**  
Attackers hijacked Google Ads for "mac cleaner" searches, redirecting users to Apple-themed pages serving obfuscated Base64 payloads. Commands like `curl | bash` download and execute RCE scripts silently. Compromised advertiser accounts enable trust exploitation. macOS users should avoid Terminal commands from ads and verify sources [[Cyberpress](https://cyberpress.org/malicious-mac-cleaner-ads-scam/)].  

## 🛡️ Defense & Detection  

**[NEW] Windows 11 update blocks unauthorized system file access**  
KB5074105 introduces stricter access controls for sensitive system files, preventing privilege escalation by validating permissions at multiple layers. The update also enhances the servicing stack (KB5074104) and updates AI components. Organizations should prioritize testing and deployment [[Cyberpress](https://cyberpress.org/windows-11-unauthorized-system-file-access/); [GBHackers](https://gbhackers.com/windows-11-block-unauthorized-access-to-system-files/)].  

**[NEW] AutoPentestX automates Linux security testing**  
Open-source toolkit consolidates network enumeration, vulnerability identification, and reporting for Kali/Ubuntu environments. Features modular architecture and JSON-based configurations for customizable testing. Useful for streamlined ethical hacking workflows [[Cyberpress](https://cyberpress.org/autopentestx-new-automated-penetration-testing-toolkit-targets-linux-environments/); [GBHackers](https://gbhackers.com/autopentestx-automated-penetration-testing-toolkit/)].  

## 📋 Policy & Industry News  

**[NEW] Apple limits cellular location tracking**  
New "Limit Precise Location" setting in iOS 26.3 restricts carrier access to neighborhood-level location data instead of precise addresses. Supported on iPhone Air, 16e, and iPad Pro (M5) with select carriers (e.g., EE, T-Mobile). Emergency location data remains unaffected [[BleepingComputer](https://www.bleepingcomputer.com/news/apple/new-apple-privacy-feature-limits-location-tracking-on-iphones-ipads/)].  

**[NEW] Critical ClawDBot flaw enables 1-click RCE**  
Insufficient `gatewayUrl` validation in ClawDBot v2026.1.28 allows attackers to steal authentication tokens via malicious links, leading to operator-level gateway compromise. Patched in v2026.1.29 with mandatory URL confirmation. Organizations should update immediately and audit WebSocket logs [[Cyberpress](https://cyberpress.org/1-click-clawdbot-vulnerability/); [GBHackers](https://gbhackers.com/1-click-flaw-in-clawdbot/)].