---
title: MongoBleed exploitation 🔴, Spotify catalog breach 🎵, Mustang Panda rootkit 🐼, Copilot backdoor flaw 🤖, Trust Wallet theft 💰
date: 2025-12-30
tags: ["mongodb","data breach","apt activity","cryptocurrency","supply chain","ai security","vulnerability exploitation","kernel malware","web application security","financial impact"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: The critical MongoBleed vulnerability threatens over 74,000 exposed MongoDB servers while Spotify faces massive intellectual property theft from hacktivists who stole 86 million music files. Chinese APT Mustang Panda advances espionage capabilities with kernel-mode rootkits, Microsoft's Copilot Studio contains a design flaw enabling backdoor access, and Trust Wallet's supply chain compromise resulted in $7 million in cryptocurrency losses.
---

# Daily Threat Intel Digest - 2025-12-30

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] MongoBleed exploitation widens as PoC code drops**  
CISA added CVE-2025-14847 ("MongoBleed") to its Known Exploited Vulnerabilities catalog amid confirmed active exploitation. The critical MongoDB server vulnerability enables unauthenticated attackers to read uninitialized heap memory, potentially exposing credentials or encryption keys. Over 74,000 internet-exposed MongoDB instances remain vulnerable (95% of all exposed servers), with Shadowserver Foundation reporting widespread scanning following the December 26 release of proof-of-concept exploit code. Organizations must patch to versions 8.2.3, 8.0.17, 7.0.28, 6.0.27, 5.0.32, or 4.4.30, or disable zlib compression immediately [[CyberPress](https://cyberpress.org/cisa-warns-of-actively-exploited-mongodb-server-vulnerability-cve-2025-14847/); [GBHackers](https://gbhackers.com/70000-mongodb-servers-exposed/); [Tenable](https://www.tenable.com/blog/cve-2025-14847-mongobleed-mongodb-memory-leak-vulnerability-exploited-in-the-wild)].

**[UPDATE] Coupang breach: Hacker's MacBook recovered, $1.17B compensation announced**  
Investigators retrieved a MacBook Air discarded in a river by the former Coupang employee responsible for the breach affecting 33.7 million South Koreans. Forensic analysis linked the device to the perpetrator via iCloud records and revealed attack scripts on seized hard drives. Coupang confirmed stolen data was limited to approximately 3,000 customers and announced ₩50,000 ($35) vouchers for all affected users, totaling $1.17B in compensation. The incident, traced to a retained security key, prompted a formal government inquiry and potential regulatory fines [[CyberPress](https://cyberpress.org/dumped-macbook/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/coupang-to-split-117-billion-among-337-million-data-breach-victims/)].

**[NEW] Spotify faces massive music catalog leak by hacktivists**  
The "Anna's Archive" hacktivist group claims to have stolen approximately 86 million music files (300TB) from Spotify's catalog, representing 99.6% of tracks frequently streamed. The group plans to release the files publicly via torrents in early 2026 after already publishing metadata. Spotify confirmed no user personal data was compromised and patched the scraping vulnerability, but the exposed files could be exploited to train AI systems without artist consent. The scraping occurred over months via user accounts targeting tracks from 2007-2025 [[Malware News](https://malware.news/t/will-hackers-release-all-of-spotify-s-most-listened-music-files/102887#post_1)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Mustang Panda deploys kernel-mode rootkit in espionage attacks**  
Chinese APT Mustang Panda (HoneyMyte) has adopted a new kernel-mode rootkit to deliver and conceal ToneShell backdoor malware against government organizations in Myanmar and Thailand. The rootkit, signed with a stolen certificate, uses a mini-filter driver to block deletion/renaming operations, interfere with Microsoft Defender, and protect injected payloads by denying handle access. Kaspersky reports this is the first observed use of kernel-mode loading for ToneShell, enhancing stealth against security tools and enabling persistent espionage [[BleepingComputer](https://www.bleepingcomputer.com/news/security/chinese-state-hackers-use-rootkit-to-hide-toneshell-malware-activity/)].

**[UPDATE] Trust Wallet crypto theft impacts 2,596 users**  
Following the December 24 browser extension compromise, Trust Wallet confirmed attackers drained approximately $7 million from 2,596 wallet addresses. The malicious extension (v2.68) was published via a leaked Chrome Web Store API key, bypassing release checks. Trust Wallet is reimbursing verified victims while warning of phishing domains impersonating support. The incident highlights systemic risks in browser extension supply chains and underscores the need for strict API key management [[BleepingComputer](https://www.bleepingcomputer.com/news/security/trust-wallet-says-7-million-crypto-theft-attack-drained-2-596-wallets/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Microsoft Copilot Studio design flaw enables backdoor access**  
The "Connected Agents" feature in Copilot Studio is enabled by default with insufficient access controls and no native audit logging. Researchers demonstrated that attackers with tenant access can deploy rogue agents to invoke legitimate agents (e.g., email-sending capabilities) without detection, enabling phishing, misinformation, or spam campaigns. Microsoft has not assigned a CVE identifier. Organizations should disable the feature for sensitive operations and implement third-party monitoring [[CyberPress](https://cyberpress.org/hackers-exploit-copilot-studios-new-connected-agents-feature-to-gain-backdoor-access/)].

**[NEW] EmEditor supply chain breach distributes infostealer**  
Attackers compromised EmEditor's official website between December 19-22, 2025, serving malware-laced MSI installers with fraudulent digital signatures. The popular text editor's downloads were tampered with to distribute infostealer malware, though specific payload details were not disclosed. Users who downloaded installers during this window should scan systems and update to clean versions [[GBHackers](https://gbhackers.com/emeditor-website/)].

## 📋 Policy & Industry News

**[NEW] OWASP releases Agentic AI Top 10 amid rising real-world attacks**  
OWASP published its first security framework for autonomous AI agents, citing 2025 incidents like prompt-jacking in Claude Desktop (CVSS 8.9), malicious MCP servers, and Amazon Q supply chain poisoning. The framework addresses risks such as "Agent Goal Hijack" (ASI01) and "Tool Misuse" (ASI02), providing a taxonomy for defending agentic systems. Organizations deploying AI agents should inventory MCP servers/plugins and enforce least-privilege policies [[BleepingComputer](https://www.bleepingcomputer.com/news/security/the-real-world-attacks-behind-owasp-agentic-ai-top-10/)].

**[NEW] Lithuanian national arrested for KMSAuto malware campaign**  
A 29-year-old suspect was extradited from Georgia to South Korea for distributing clipper malware via KMSAuto Windows activators, infecting 2.8 million systems. The operation stole $1.2M in cryptocurrency by swapping wallet addresses in clipboards across 3,100 victims. The arrest highlights risks of using unlicensed software activators, which frequently deliver malware [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hacker-arrested-for-kmsauto-malware-campaign-with-28-million-downloads/)].