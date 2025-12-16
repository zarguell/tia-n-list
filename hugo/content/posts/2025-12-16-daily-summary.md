---
title: Apple WebKit zero-days 🍎, ShinyHunters extortion 💰, React2Shell exploitation ⚡, supply chain breaches 🔗, SantaStealer MaaS 🦠
date: 2025-12-16
tags: ["zero-day exploitation","webkit vulnerabilities","extortion campaigns","apt activity","supply chain attacks","automotive sector","malwares-as-a-service","privilege escalation","data breaches","credential theft"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Apple WebKit zero-days and React2Shell vulnerabilities enable widespread active exploitation, with Chinese APTs deploying backdoors while ShinyHunters conducts massive extortion campaigns against PornHub and SoundCloud. Supply chain breaches at 700Credit and Jaguar Land Rover expose millions of records, while new SantaStealer MaaS bypasses Chrome encryption to steal browser data and crypto wallets.
---

# Daily Threat Intel Digest - 2025-12-16

## 🔴 Critical Threats & Active Exploitation

**[NEW] Apple patches two actively exploited WebKit zero-days**  
Apple released emergency security updates for two vulnerabilities being used in targeted attacks: CVE-2025-43529 and CVE-2025-14174. Both flaws affect WebKit across iOS, macOS, and other Apple platforms, enabling remote code execution or memory corruption via malicious web content. The vulnerabilities were exploited in sophisticated attacks against specific individuals, though Apple hasn't disclosed attribution details. All Apple users should update immediately to iOS 18.2.1, macOS Sequoia 15.2, or corresponding patched versions [[BleepingComputer](https://www.bleepingcomputer.com/news/security/apple-issues-security-updates-after-two.html); [Check Point Research](https://research.checkpoint.com/2025/15th-december-threat-intelligence-report/)].

**[NEW] ShinyHunters extorts PornHub with 200M+ stolen user records**  
The ShinyHunters extortion gang is threatening to release 201 million records containing PornHub Premium users' search histories, video views, and downloads after allegedly stealing data from analytics vendor Mixpanel. The data includes email addresses, locations, video URLs, and timestamps – highly sensitive information extortionists could use for blackmail or public exposure. While PornHub claims the data is historical (pre-2021) and no passwords/financial details were compromised, the scale represents a significant privacy disaster [[BleepingComputer](https://www.bleepingcomputer.com/news/security/pornhub-extorted-after-hackers-steal-premium-user-activity-data/)]. This follows ShinyHunters' related extortion of SoundCloud [[BleepingComputer](https://www.bleepingcomputer.com/news/security/soundcloud-confirms-breach-after-member-data-stolen-vpn-access-disrupted/)].

**[NEW] 700Credit breach exposes 5.8M dealership customers' PII**  
A vulnerability in 700Credit's API exposed full names, addresses, dates of birth, and Social Security Numbers of 5.8 million individuals who purchased vehicles through U.S. dealerships. Attackers exploited the flaw between May-October 2025 after compromising an integration partner's credentials, stealing ~20% of consumer data before detection. The fintech firm is offering 12 months of credit monitoring, while the breach underscores risks of interconnected automotive industry supply chains [[BleepingComputer](https://www.bleepingcomputer.com/news/security/700credit-data-breach-impacts-58-million-vehicle-dealership-customers/); [Check Point Research](https://research.checkpoint.com/2025/15th-december-threat-intelligence-report/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Five China-nexus APTs join React2Shell exploitation spree**  
Google's Threat Intelligence Group identified five additional Chinese state-backed groups actively exploiting the critical React2Shell vulnerability (CVE-2025-55182): UNC6600 (deploying MINOCAT tunneling), UNC6586 (SNOWLIGHT downloader), UNC6588 (COMPOOD backdoor), UNC6603 (HISONIC variant), and UNC6595 (ANGRYREBEL.LINUX). These join earlier attackers like Earth Lamia and Jackpot Panda in leveraging the flaw to steal AWS credentials and deploy backdoors against unpatched React/Next.js servers. Shadowserver reports 116,000 vulnerable IPs remain globally [[Google Threat Intel](https://cloud.google.com/blog/topics/threat-intelligence/threat-actors-exploit-react2shell-cve-2025-55182/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/google-links-more-chinese-hacking-groups-to-react2shell-attacks/)].

**[NEW] ShinyHunters claims responsibility for SoundCloud breach**  
The extortion group behind the PornHub data theft has also claimed responsibility for SoundCloud's breach, which affected ~28 million users (20% of its user base). ShinyHunters accessed an ancillary service dashboard, exfiltrating email addresses and publicly visible profile data. SoundCloud's response – including VPN blocking configurations – inadvertently disrupted legitimate user access, triggering subsequent DDoS attacks. The group is also linked to Salesforce/Drift attacks and the Oracle EBS zero-day (CVE-2025-61884) [[BleepingComputer](https://www.bleepingcomputer.com/news/security/soundcloud-confirms-breach-after-member-data-stolen-vpn-access-disrupted/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/pornhub-extorted-after-hackers-steal-premium-user-activity-data/)].

## ⚠️ Vulnerabilities & Patches

**[UPDATE] React2Shell exploitation widens as 80K U.S. servers remain vulnerable**  
While CVE-2025-55182 was previously reported, new intelligence reveals expanded exploitation: beyond Chinese APTs, Iranian actors and financially motivated attackers deploying XMRig miners now target the flaw. The vulnerability allows unauthenticated RCE via React Server Components in React 19.0-19.2.0 and affected Next.js deployments. With 80,000+ vulnerable U.S. IPs and 116,000 globally, organizations using React/Next.js must patch immediately or implement WAF rules against suspicious HTTP requests [[Google Threat Intel](https://cloud.google.com/blog/topics/threat-intelligence/threat-actors-exploit-react2shell-cve-2025-55182/); [GreyNoise](https://viz.greynoise.io/query/tags:%22React%20Server%20Components%20Unsafe%20Deserialization%20CVE-2025-55182%20RCE%20Attempt%22%20last_seen:1d)].

**[NEW] Critical JumpCloud agent flaw enables SYSTEM-level privilege escalation**  
JumpCloud Remote Assist for Windows versions prior to 0.317.0 contain CVE-2025-34352 (CVSS 8.5), allowing any low-privileged user to gain NT AUTHORITY\SYSTEM privileges or crash the machine. The flaw exists in the agent's handling of privileged operations, creating a local attack path in environments using JumpCloud for DaaS or endpoint management. Admins should update agents immediately and review for suspicious escalation attempts [[GBHackers](https://gbhackers.com/jumpcloud-remote-assist-windows-agent-vulnerability/)].

## 🛡️ Defense & Detection

**[NEW] SantaStealer MaaS emerges with Chrome App-Bound Encryption bypass**  
Rapid7 researchers uncovered SantaStealer, a new info-stealer rebranded from BluelineStealer, sold as MaaS for $175-$300/month via Telegram. Notably, it uses an embedded executable to bypass Chrome's App-Bound Encryption (introduced July 2024) and steals browser data, crypto wallets, and Discord credentials. While operational security is poor (samples leaked with debug symbols), its 14-threaded data exfiltration modules and CIS-region exclusion suggest professionalization. Defenders should monitor for process injection attempts and unusual ZIP exfiltration on port 6767 [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-santastealer-malware-steals-data-from-browsers-crypto-wallets/); [GBHackers](https://gbhackers.com/santastealer-malware/)].

## 📋 Policy & Industry News

**[NEW] Google discontinues dark web monitoring tool in January 2026**  
Google will sunset its "dark web report" feature on January 15, 2026, citing user feedback that it lacked actionable guidance. The tool notified users if their email/data appeared on dark web forums, but Google is shifting focus to Password Manager and Passkey solutions. This removes a free monitoring option for personal users, though enterprise Google Workspace admins retain advanced breach alerts via the Security Center [[BleepingComputer](https://www.bleepingcomputer.com/news/google/google-is-shutting-down-its-dark-web-report-feature-in-january/)].

**[NEW] Jaguar Land Rover confirms employee data theft in August cyberattack**  
JLR finally admitted its August cyberattack – previously described only as a "production shutdown" – resulted in the theft of current and former employees' personal data. The incident cost hundreds of millions in operational disruption. While full victim counts weren't disclosed, the disclosure highlights delayed breach reporting and escalating risks to automotive sector supply chains [[GBHackers](https://gbhackers.com/jaguar-land-rover-confirms-august-cyberattack/)].