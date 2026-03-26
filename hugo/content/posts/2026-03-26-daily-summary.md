---
title: Cisco Firewall RCE 🔥, PolyShell Magento attacks 🛒, Coruna iOS exploit kit 📱, energy sector ransomware ⚡, Torg Grabber infostealer 💰
date: 2026-03-26
tags: ["rce vulnerabilities","magento exploitation","ios exploit kit","ransomware","infostealer","energy sector","supply chain attacks","cryptocurrency","phishing","remote access"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical remote code execution vulnerabilities in Cisco firewalls and Magento stores are being actively exploited by attackers using advanced techniques including WebRTC skimmers to steal payment data. Sophisticated threat campaigns are simultaneously targeting the energy sector with ransomware, compromising iOS devices through the Coruna exploit kit, and deploying the Torg Grabber infostealer against cryptocurrency environments, creating a multi-front security challenge requiring urgent patching and enhanced supply chain monitoring.
---
# Daily Threat Intel Digest - 2026-03-26

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Cisco Secure Firewall flaw (CVE-2026-20131) under active attack**
Attackers are actively exploiting a critical deserialization flaw in Cisco Secure Firewall Management Center (FMC) that allows unauthenticated, remote code execution with root privileges. Tracked as CVE-2026-20131 with a CVSS score of 10.0, the vulnerability resides in the web-based management interface and requires no user interaction. Cisco confirmed exploitation in the wild began in March 2026, meaning internet-exposed FMC interfaces are at immediate risk of full system compromise. While SaaS-based management has been auto-patched, on-premises administrators must upgrade immediately as no workarounds exist [[Cisco advisory via CyberPress](https://cyberpress.org/cisco-secure-firewall-flaw/); [GBHackers](https://gbhackers.com/cisco-secure-firewall-vulnerability-3/)].

**[NEW] PolyShell campaign exploits over 56% of vulnerable Magento stores**
A massive exploitation campaign targeting the "PolyShell" vulnerability in Adobe Commerce and Magento Open Source has successfully compromised 56.7% of vulnerable stores within days of public disclosure. Attackers are leveraging a flaw in the REST API to achieve unauthenticated RCE or stored XSS, and in some instances, delivering a novel "WebRTC Skimmer." This skimmer uses DTLS-encrypted UDP protocols to bypass standard Content Security Policy (CSP) controls and exfiltrate payment card data, highlighting a sophisticated evolution in e-commerce skimming tactics [[Sansec via BleepingComputer](https://www.bleepingcomputer.com/news/security/polyshell-attacks-target-56-percent-of-all-vulnerable-magento-stores/)].

**[NEW] Synology DSM vulnerability enables unauthenticated RCE**
Synology issued an urgent security update (Synology-SA-26:03) for DiskStation Manager (DSM) to patch a critical vulnerability that allows unauthenticated remote attackers to execute arbitrary commands. While specific technical details were sparse in the release, the vendor explicitly warned of ongoing security events requiring immediate patching to protect NAS devices from takeover [[GBHackers](https://gbhackers.com/synology-diskstation-manager-vulnerability/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Coruna exploit kit linked to Operation Triangulation**
Researchers have analyzed the "Coruna" exploit kit, confirming it is a direct evolution of the framework used in Operation Triangulation. The kit contains updated exploits for iOS vulnerabilities CVE-2023-32434 and CVE-2023-38606, previously used as zero-days. Unlike the limited scope of Triangulation, Coruna is now being used in broader campaigns, including watering-hole attacks in Ukraine and financially motivated attacks in China. The modular design supports exploits for iOS versions up to 17.2, posing a significant risk to unpatched devices [[Kaspersky via Malware.news](https://malware.news/t/coruna-the-framework-used-in-operation-triangulation/105415#post_1)].

**[NEW] Energy sector faces relentless ransomwave in 2025**
A new report details 187 confirmed ransomware attacks against the global energy sector in 2025, with RansomHub, Akira, and Play accounting for nearly half of all incidents. Initial access brokers are increasingly specializing in energy infrastructure, advertising admin-level access to power plants and water treatment facilities. Geopolitical hacktivists, such as Sector 16, have also escalated from DDoS to demonstrating operational technology (OT) access, claiming the ability to manipulate physical controls at US and European facilities [[Cyble via Malware.news](https://malware.news/t/the-energy-sector-s-ransomware-nightmare-why-critical-infrastructure-can-t-catch-a-break/105414#post_1)].

**[NEW] Torg Grabber infostealer bypasses Chrome App-Bound Encryption**
A new information-stealing malware, "Torg Grabber," has been identified targeting 728 distinct cryptocurrency wallet extensions alongside password managers and 2FA tools. Active since late 2025, the malware employs a "ClickFix" technique for initial access and has evolved to bypass Chrome's App-Bound Encryption (ABE) protection. Its operators register new C2 infrastructure weekly, and the malware is capable of executing shellcode and stealing files, posing a severe threat to crypto-heavy environments [[Gen Digital via BleepingComputer](https://www.bleepingcomputer.com/news/security/new-torg-grabber-infostealer-malware-targets-728-crypto-wallets/)].

**[UPDATE] Malicious npm packages target crypto developers**
Following prior reports of crypto-focused npm attacks, new details have emerged on a campaign using packages like `raydium-bs58` and `ethersproject-wallet` to steal private keys. Published by user "galedonovan," these typosquatted libraries hook into Base58 decode and Wallet constructor functions, exfiltrating keys directly to a Telegram bot. Security teams should audit for these specific packages, as the attack relies on obfuscated code that allows the malicious function to execute normally while leaking credentials [[Socket via CyberPress](https://cyberpress.org/telegram-attack-targets-crypto-developers/)].

**[UPDATE] TeamPCP Trivy supply chain attack**
Microsoft has released new detection and defense guidance for the supply chain attack targeting Aqua Security's Trivy vulnerability scanner (CVE-2026-33634). The TeamPCP threat actor leveraged incomplete remediation to inject credential-stealing malware into official releases. This update provides specific hunting rules and indicators of compromise (IoCs) to help organizations determine if their CI/CD pipelines were affected by the compromised tool [[GBHackers](https://gbhackers.com/microsoft-to-detect-defend-against-trivy-supply-chain-attack/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Node.js fixes multiple DoS and crash vulnerabilities**
Node.js released version 20.20.2 "Iron," addressing seven security flaws including a high-severity issue (CVE-2026-21637) in TLS handling that allows remote process crashes via uncaught exceptions. Additional patches cover a V8 HashDoS vulnerability (CVE-2026-21717), HTTP/2 memory leaks (CVE-2026-21714), and timing side-channels in HMAC verification. Organizations running public-facing Node.js services should upgrade immediately to prevent service disruptions [[CyberPress](https://cyberpress.org/node-js-fixes-multiple-vulnerabilities/); [GBHackers](https://gbhackers.com/node-js-releases-urgent-patches-for-multiple-vulnerabilities/)].

**[NEW] Apple patches 85 vulnerabilities across platforms**
Apple released security updates for macOS, iOS, iPadOS, watchOS, tvOS, and visionOS, addressing 85 distinct vulnerabilities. While none are currently being exploited in the wild, the update covers a wide range of components. Users are advised to update to the latest versions to ensure coverage against potential future exploitation [[SANS ISC via Malware.news](https://malware.news/t/apple-patches-almost-everything-again-march-2026-edition-wed-mar-25th/105402#post_1)].

**[NEW] ISC BIND patches multiple DNS vulnerabilities**
ISC released security advisories for BIND 9, fixing vulnerabilities including CVE-2026-1519 (excessive NSEC3 iterations causing high CPU), CVE-2026-3104 (memory leak), and CVE-2026-3119 (TKEY record causing termination). Administrators of DNS servers running versions 9.11 through 9.21 should review the matrices and apply patches to prevent DoS or potential ACL bypasses [[Canadian Centre for Cyber Security via Malware.news](https://malware.news/t/isc-bind-security-advisory-av26-280/105396#post_1)].

**[UPDATE] Cisco releases bundled security advisories (AV26-281)**
Cisco published its semiannual bundled security advisories, covering vulnerabilities in IOS, IOS XE, ASA, and FTD software across Catalyst switches and wireless controllers. Administrators should review the bundle to identify updates relevant to their specific devices, as some vulnerabilities may allow unauthorized access or DoS conditions [[Cisco via Malware.news](https://malware.news/t/cisco-security-advisory-av26-281/105398#post_1)].

**[UPDATE] Cheap IP-KVMs riddled with firmware flaws**
Expanding on previous reports of IP-KVM risks, Eclypsium researchers detailed vulnerabilities in low-cost devices from JetKVM, GL.iNet, Sipeed, and Anjeet. Critical findings include lack of firmware signing (allowing malicious updates), default credentials, and open API endpoints (e.g., Wi-Fi configuration on Sipeed). JetKVM was the only vendor to implement cryptographic signing during the disclosure window, highlighting a security gap in the broader consumer hardware market [[Eclypsium via Malware.news](https://malware.news/t/bts-70-how-cheap-kvms-could-be-your-networks-weak-link/105399#post_1)].

## 🛡️ Defense & Detection

**[NEW] Google accelerates post-quantum encryption timeline to 2029**
Google announced it is moving its internal migration to quantum-resistant encryption up to 2029, six years ahead of the U.S. federal government's 2035 mandate. Citing rapid advancements in quantum computing hardware, Google urges other organizations to accelerate their transition to NIST-vetted algorithms to mitigate "harvest now, decrypt later" threats [[CyberScoop](https://cyberscoop.com/google-moves-post-quantum-encryption-timeline-to-2029/)].

**[NEW] LeakBase forum admin arrested in Russia**
Russian law enforcement apprehended the alleged administrator of LeakBase, a prominent cybercrime forum for stolen data, in Taganrog. This arrest represents a significant disruption to the underground economy for credentials and database leaks, potentially drying up a key resource for infostealers and initial access brokers [[GBHackers](https://gbhackers.com/leakbase-forum-admin-arrested/)].

**[NEW] Phishers abuse Bubble AI no-code platform for evasion**
Threat actors are abusing the legitimate "Bubble" no-code platform to host phishing pages, specifically targeting Microsoft account credentials. By hosting on `*.bubble.io`, attackers bypass email reputation filters, while the platform's complex JavaScript bundles and Shadow DOM structures hinder static analysis detection tools [[Kaspersky via BleepingComputer](https://www.bleepingcomputer.com/news/security/bubble-ai-app-builder-abused-to-steal-microsoft-account-credentials/)].

## 📋 Policy & Industry News

**[NEW] Alleged RedLine infostealer developer extradited to US**
Armenian national Hambardzum Minasyan has been extradited to the U.S. to face charges for his alleged role in developing and administering the RedLine infostealer. The charges include conspiracy to commit access device fraud and money laundering, following Operation Magnus which disrupted the RedLine and Meta stealers in 2024 [[CyberScoop](https://cyberscoop.com/alleged-redline-infostealer-conspirator-extradited-to-us/)].

**[NEW] European officials emphasize private sector role in takedowns**
At RSAC, European cybercrime officials from the Netherlands, UK, and Germany highlighted the critical role of private sector partners in operations like the LockBit takedown. They noted that industry involvement is now standard for identifying infrastructure and amplifying disruption narratives to prevent other criminals from filling the void [[Nextgov/FCW via Malware.news](https://malware.news/t/european-officials-highlight-private-sector-help-in-major-cybercrime-takedowns/105404#post_1)].