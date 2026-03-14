---
title: Veeam RCE flaw 🔴, GlassWorm supply chain 🪱, LockBit 5.0 spree 💣, Handala wiper tactics 📱
date: 2026-03-14
tags: ["rce vulnerability","supply chain attack","ransomware","wiper malware","phishing","threat actors","backup software","ide security","mdm abuse","data breach"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: A critical RCE vulnerability in Veeam Backup & Replication enables full server compromise, while the GlassWorm supply chain campaign infects developer environments through malicious VS Code extensions. LockBit 5.0 continues attacking organizations across multiple sectors and the Iran-linked Handala Group is weaponizing Microsoft Intune to deploy wiper malware on mobile devices.
---
# Daily Threat Intel Digest - 2026-03-14

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical RCE flaw in Veeam Backup & Replication allows full server compromise**
Veeam released patches for a critical vulnerability (CVE-2026-21669, CVSS 9.9) that allows an authenticated attacker with domain user access to execute arbitrary code on the Backup Server. Because backup servers often hold privileged credentials and have high-trust access to production environments, this flaw poses a severe risk of lateral movement and data destruction. Organizations must upgrade to the latest build immediately, as the complexity of the exploit chain is low once valid credentials are obtained [[Arctic Wolf](https://arcticwolf.com/resources/blog/multiple-authenticated-high-and-critical-vulnerabilities-veeam-backup-replication/)].

**[NEW] Windows 11 update breaks C: drive access on Samsung devices**
A widespread issue is affecting Samsung Galaxy Book 4 and other consumer devices running Windows 11 versions 24H2 and 25H2, where users receive "Access denied" errors when trying to access the C: drive or launch applications. The problem appears linked to the February 2026 security updates interacting poorly with the Samsung Share application. Microsoft is investigating, but users are advised to avoid a circulating workaround that involves changing C: drive ownership to "Everyone," as this severely weakens OS security controls [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-windows-11-users-cant-access-c-drive-on-some-samsung-pcs/)].

**[NEW] GlassWorm malware campaign targets VS Code developers via transitive dependencies**
A new supply chain attack dubbed "GlassWorm" has infected at least 72 malicious Open VSX extensions by hiding malware in transitive dependencies rather than the initial package release. By allowing a seemingly safe package to pull in a compromised extension after trust is established, attackers are sneaking malicious code into developer environments targeting Windows, macOS, and Linux systems. This stealthy method highlights the risks of dependency trees in integrated development environments (IDEs) [[GBHackers](https://gbhackers.com/glassworm-spreads-via-72-malicious-open-vsx-extensions/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Handala Group expands wiper tactics via Microsoft Intune**
Following the disruptive wiper attack on Stryker reported yesterday, new analysis reveals the Iran-linked Handala Group weaponized Microsoft Intune management services to deploy wiper malware. The attack specifically targeted employees' phones, including personal devices enrolled in the MDM, effectively rendering them inoperable. This indicates a shift from simple data wiping to weaponizing MDM infrastructure itself, suggesting similar tactics may be used against other organizations in the healthcare or defense sectors [[Nextgov/FCW](https://www.nextgov.com/cybersecurity/2026/03/stryker-hack-could-set-stage-more-pro-iran-cyber-sabotage/412115/); [Arctic Wolf](https://arcticwolf.com/resources/blog/stryker-systems-disrupted-cyber-attack-handala-group-claims-responsibility/)].

**[NEW] LockBit 5.0 claims 10+ new victims across global sectors**
LockBit 5.0 has posted a significant number of new victims in the last 24 hours, targeting a diverse range of industries including municipal government (Town of Orange, VA), education (Webster Public Schools), healthcare (CognitiveHealth Technologies, Elmwood Healthcare), and manufacturing (PKM Steel Service, Thai Hua Rubber, HB-Technik). The spree indicates the operation is fully active despite recent law enforcement disruptions, with data leaks threatened for non-compliance [[DeXpose](https://www.dexpose.io/lockbit-5-0-strikes-town-of-orange-virginia/); [DeXpose](https://www.dexpose.io/lockbit-5-0-targets-webster-public-schools/); [DeXpose](https://www.dexpose.io/lockbit-5-0-targets-cognitivehealth-technologies-in-ransomware-attack/)].

**[NEW] Phishing campaign abuses Google Cloud Storage for trusted redirects**
A large-scale phishing operation is leveraging `storage.googleapis.com` URLs to act as trusted redirectors, sending victims to various scam domains hosted on the `.autos` TLD. The campaign themes range from fake Netflix rewards and Dell laptop giveaways to "cloud storage full" alerts and fake job offers. By using legitimate Google infrastructure as the initial hop, attackers bypass many email filters and security blocklists [[Malware Analysis](https://malwr-analysis.com/2026/03/14/ongoing-phishing-campaign-abusing-google-cloud-storage-to-redirect-users-to-multiple-scam-pages/)].

**[NEW] Fake Malwarebytes calendar invites target victims with tech support scams**
A new scam campaign is distributing fake calendar invites impersonating Malwarebytes renewal notices, demanding payment for hundreds of dollars of services. The invites do not contain links but urge victims to call a fraudulent "billing support" number, where operators attempt to steal payment details or convince users to install remote access software. Red flags include unnatural phrasing like "4yrold" and inconsistent formatting in the event descriptions [[Malwarebytes](https://www.malwarebytes.com/blog/threat-intel/2026/03/fake-malwarebytes-renewal-notices-in-your-calendar)].

## 🛡️ Defense & Detection

**[NEW] FBI seeks victims of Steam-based malware drainers**
The FBI Seattle Division is investigating a cluster of malicious games on Steam that distributed information stealers and cryptocurrency drainers between May 2024 and January 2026. Titles such as *BlockBlasters*, *Chemia*, and *PirateFi* were used to harvest credentials and drain wallets. Security teams should query endpoints for installations of these specific titles and check user browsers for unauthorized browser extensions or crypto wallet activity [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-seeks-victims-of-steam-games-used-to-spread-malware/)].

## ⚡ Quick Hits

- **Retail Breach:** Loblaw Companies disclosed a data breach exposing customer names, emails, and phone numbers, though financial data was not accessed [[Cyberpress](https://cyberpress.org/loblaw-data-breach/)].
- **ICS Advisory:** ABB released security advisory AV26-236 addressing vulnerabilities in the embedded webserver of AWIN GW100 and GW120 gateways [[Canadian Centre for Cyber Security](https://cyber.gc.ca/en/alerts-advisories/control-systems-abb-security-advisory-av26-236)].
- **Employee Data Leak:** Starbucks confirmed a data breach impacting employee information, though specific details on the scope were limited in available reports [[SecurityWeek](https://www.securityweek.com/starbucks-data-breach-impacts-employees/)].