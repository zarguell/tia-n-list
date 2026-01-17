---
title: Meta XSS flaws 🕸️, Black Basta leader 👤, Qilin attacks utilities ⚡, UAT-8837 zero-day 🛠️, access broker case ⚖️
date: 2026-01-17
tags: ["xss vulnerabilities","ransomware","apt activity","zero-day exploits","energy sector","threat actors","access brokers","account takeover","china nexus"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical XSS vulnerabilities in Meta's Conversion API enable zero-click Facebook account hijacking across millions of third-party deployments, while ransomware groups like Black Basta and Qilin continue targeting critical infrastructure and major organizations globally. China-linked actor UAT-8837 is actively exploiting Sitecore zero-days for initial access to North American infrastructure, highlighting the ongoing risks from sophisticated state-sponsored threats and access brokers facilitating cybercrime.
---

# Daily Threat Intel Digest - 2026-01-17

## 🔴 Critical Threats & Active Exploitation

**[NEW] Meta Conversion API XSS flaws enable zero-click Facebook account hijacking**  
Two critical cross-site scripting vulnerabilities in Meta's Conversions API Gateway allow attackers to hijack Facebook accounts without user interaction, affecting both Meta's infrastructure and potentially 100 million third-party deployments. The flaws stem from improper origin validation in the client-side `capig-events.js` script and unsafe string concatenation in the gateway backend, enabling arbitrary JavaScript execution in trusted contexts across facebook.com, meta.com, and countless third-party sites that load the vulnerable script [[Cyberpress](https://cyberpress.org/exploiting-xss-in-meta-conversion-api/); [GBHackers](https://gbhackers.com/critical-xss-vulnerabilities-in-meta-conversion-api-enable-zero-click-account-takeover/)]. Researchers identified CSP bypass techniques on Meta's help pages and note the open-source gateway's widespread deployment exponentially expands the attack surface.

**[UPDATE] Windows 11 January update breaks shutdowns on Secure Launch systems**  
Microsoft's January 13 security update (KB5073455) is causing Windows 11 Enterprise and IoT devices with Secure Launch enabled to restart instead of shutting down or hibernating. The bug affects version 23H2 systems, forcing users to execute `shutdown /s /t 0` via Command Prompt to power down devices [[Cyberpress](https://cyberpress.org/windows-11-users-report-shutdown-failures/); [GBHackers](https://gbhackers.com/windows-11-january-update-sparks-widespread-shutdown-complaints/)]. Microsoft acknowledged the issue on January 15 with no permanent fix available yet, leaving organizations reliant on hibernation for power preservation particularly vulnerable.

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Black Basta ransomware leader identified as Interpol issues Red Notice**  
Law enforcement in Ukraine and Germany have identified Oleg Evgenievich Nefedov, a 35-year-old Russian national, as the leader of the Black Basta ransomware gang. Nefedov, known by aliases including "tramp" and "Washingt0n," was previously linked to the now-defunct Conti ransomware operation [[BleepingComputer](https://www.bleepingcomputer.com/news/security/black-basta-boss-makes-it-onto-interpols-red-notice-list/)]. The gang has claimed responsibility for at least 600 ransomware incidents targeting major organizations including Rheinmetall, Hyundai Europe, Ascension healthcare, and Capita, with police raids in Ukraine seizing digital storage and cryptocurrency assets from two additional suspects.

**[NEW] Qilin ransomware claims attack on Texas State Utilities**  
The Qilin ransomware group announced the January 15 compromise of Texas State Utilities (texasstateutilities.com), a critical U.S. energy sector entity. The operators have threatened to leak stolen data unless their demands are met, continuing ransomware groups' aggressive targeting of essential infrastructure [[Malware News](https://malware.news/t/qilin-ransomware-attack-on-texas-state-utilities/103358#post_1)]. The incident highlights the ongoing risk to energy providers from financially motivated attacks seeking extortion through data theft threats.

**[NEW] China-linked UAT-8837 exploits Sitecore zero-day for initial access**  
A China-nexus threat actor tracked as UAT-8837 is actively exploiting the CVE-2025-53690 ViewState deserialization zero-day in Sitecore products to breach critical infrastructure organizations in North America. The actor leverages the flaw alongside compromised credentials and known vulnerabilities for initial access, then uses open-source tools like GoTokenTheft, Certipy, and SharpHound for credential harvesting and Active Directory reconnaissance [[BleepingComputer](https://www.bleepingcomputer.com/news/security/china-linked-hackers-exploited-sitecore-zero-day-for-initial-access/)]. Cisco Talos assesses medium confidence of Chinese state affiliation based on TTP overlaps with known threat actors.

## ⚠️ Vulnerabilities & Patches

**[NEW] Wireshark 4.6.3 addresses 4 vulnerabilities in network analysis tool**  
The Wireshark project released version 4.6.3 fixing four security vulnerabilities alongside nine bug fixes in the widely used network protocol analyzer [[Malware News](https://malware.news/t/wireshark-4-6-3-released-sat-jan-17th/103359#post_1)]. Organizations using Wireshark for network forensics and monitoring should prioritize this update to mitigate potential security risks during packet analysis operations.

**[UPDATE] Palo Alto Networks GlobalProtect DoS flaw patched**  
Palo Alto Networks has addressed CVE-2026-0227, a high-severity denial-of-service vulnerability affecting GlobalProtect Gateway and Portal in PAN-OS 10.1 and later. Unauthenticated attackers could exploit the improper exception handling flaw to disrupt firewall services and potentially force devices into maintenance mode through repeated attacks [[SOC Prime](https://socprime.com/blog/cve-2026-0227-vulnerability/)]. While no active exploitation was reported at disclosure, the availability of proof-of-concept exploit code and exposure of nearly 6,000 firewalls necessitate immediate patching.

## 🛡️ Defense & Detection

**[NEW] Researchers hijack StealC malware infrastructure via XSS vulnerability**  
CyberArk researchers exploited a cross-site scripting flaw in StealC's administrative panel to observe attacker sessions, steal cookies, and collect hardware fingerprints from infostealer operators. The technique revealed one operator using an Apple M3 system with Eastern European time settings, accessed via Ukraine's TRK Cable TV ISP [[BleepingComputer](https://www.bleepingcomputer.com/news/security/stealc-hackers-hacked-as-researchers-hijack-malware-control-pictures/)]. Researchers disclosed the vulnerability to disrupt the growing StealC malware-as-a-service ecosystem, which has seen increased adoption following Lumma Stealer operational issues.

## 📋 Policy & Industry News

**[NEW] Jordanian access broker pleads guilty after selling FBI network access**  
Feras Khalil Ahmad Albashiti, a 40-year-old Jordanian national operating as "r1z," pleaded guilty to trafficking unauthorized access credentials after selling an undercover FBI agent access to 50 company networks in May 2023. Albashiti exploited vulnerabilities in commercial firewall products and sold EDR-killing malware, with investigators linking his operations to a $50 million ransomware attack against a U.S. manufacturer [[CyberScoop](https://cyberscoop.com/jordanian-national-access-broker-pleads-guilty/); [Malware News](https://malware.news/t/jordanian-man-admits-selling-unauthorized-access-to-computer-networks-of-50-companies/103351#post_1)]. Scheduled for sentencing in May, he faces up to 10 years in prison.

**[NEW] Lawmaker probes NSF program allowing Chinese institution access to US supercomputers**  
Rep. John Moolenaar, chair of the House China Select Committee, has urged the NSF to revoke Chinese institutions' access to the Advanced Cyberinfrastructure Coordination Ecosystem (ACCESS) program after discovering sanctioned entities like the National University of Defense Technology could leverage U.S. supercomputing resources [[Malware News](https://malware.news/t/lawmaker-worries-nsf-program-loophole-enables-chinese-institutions-to-access-us-backed-computing-resources/103349#post_1)]. The loophole potentially allows Chinese entities to conduct advanced AI and materials research without obtaining export-controlled GPUs, raising national security concerns about technology transfer risks.