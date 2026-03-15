---
title: AppsFlyer SDK crypto-stealer 💎, LockBit ransomware attacks 🔒, Windows RRAS RCE patches 🛡️, Docker security guide 🐳
date: 2026-03-15
tags: ["supply chain attack","crypto-stealer","ransomware","lockbit","critical infrastructure","rce vulnerability","container security","docker","hotpatch","windows security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Attackers compromised the AppsFlyer Web SDK to inject cryptocurrency-stealing JavaScript that swaps wallet addresses during Bitcoin, Ethereum, and Solana transactions while preserving normal functionality. Ransomware operations including LockBit 5.0 and Akira continue targeting critical infrastructure in energy, healthcare, and food sectors while Microsoft issued out-of-band hotpatches for Windows RRAS remote code execution flaws and CIS released Docker hardening guidance.
---
# Daily Threat Intel Digest - 2026-03-15

## 🔴 Critical Threats & Active Campaigns

**[NEW] AppsFlyer Web SDK hijacked in supply chain crypto-stealer attack**
Attackers compromised the AppsFlyer Web SDK to inject obfuscated JavaScript that steals cryptocurrency by swapping wallet addresses during transactions. The malicious code, delivered via the official domain `websdk.appsflyer.com`, targets major cryptocurrencies including Bitcoin, Ethereum, and Solana, preserving normal SDK functionality while siphoning funds to attacker-controlled wallets. This supply chain breach impacts a vast user base, as AppsFlyer analytics are integrated into over 100,000 mobile and web applications used by 15,000 businesses globally [[BleepingComputer](https://www.bleepingcomputer.com/news/security/appsflyer-web-sdk-used-to-spread-crypto-stealer-javascript-code/)].

**[UPDATE] Ransomware surge targets Energy, Healthcare, and Food sectors**
Following yesterday's reported spree, LockBit 5.0 has claimed responsibility for attacks on PT Energi Mega Persada, a major Indonesian oil and gas company, and Praxis Oberhof, a Swiss dental clinic. Simultaneously, the Akira ransomware group targeted Mh Soluciones, a Spanish outsourcing firm, threatening to leak 85GB of corporate data including employee passports and government contracts. Additionally, the AiLock group has claimed an attack on Raw Seafoods, Inc., a U.S. seafood supplier. This wave of activity underscores the relentless targeting of critical infrastructure and services by diverse ransomware operations [[DeXpose/Malware News](https://malware.news/t/lockbit5-targets-indonesian-energy-firm-pt-energi-mega-persada/104923#post_1); [DeXpose/Malware News](https://malware.news/t/lockbit-5-0-strikes-swiss-dental-clinic-praxis-oberhof/104922#post_1); [DeXpose/Malware News](https://malware.news/t/akira-ransomware-strikes-mh-soluciones-in-spain/104921#post_1); [DeXpose/Malware News](https://malware.news/t/ailock-ransomware-attack-on-raw-seafoods-inc/104920#post_1)].

## 🛡️ Vulnerabilities, Patches & Hardening

**[NEW] Microsoft releases OOB hotpatch for critical Windows RRAS RCE flaws**
Microsoft has issued an out-of-band update, KB5084597, to address three critical remote code execution vulnerabilities (CVE-2026-25172, CVE-2026-25173, CVE-2026-26111) in the Windows Routing and Remote Access Service (RRAS). These flaws allow an authenticated domain attacker to execute code on a target machine by tricking a user into connecting to a malicious server via the RRAS management tool. While the vulnerabilities were patched on March 10, this specific hotpatch is crucial for Enterprise clients utilizing "hotpatch" updates, as it applies fixes in-memory without requiring a system reboot—a critical capability for mission-critical infrastructure [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-releases-windows-11-oob-hotpatch-to-fix-rras-rce-flaw/)].

**[NEW] CIS-aligned technical guide released for securing Docker CE**
A comprehensive security standard for Docker Community Edition has been published to mitigate high-risk attack vectors such as container escape, privilege escalation, and root compromise via exposed APIs. The guide establishes a mandatory production baseline covering host hardening, daemon configuration, image supply chain security, and runtime isolation. Key controls include enabling user namespace remapping (`userns-remap`), disabling inter-container communication (ICC) on the default bridge, and enforcing non-root container execution to limit the blast radius of potential breaches [[SOCFortress](https://socfortress.medium.com/secure-deployment-of-docker-ce-cis-aligned-technical-guide-6213b15d9a05?source=rss-36613248f635------2)].