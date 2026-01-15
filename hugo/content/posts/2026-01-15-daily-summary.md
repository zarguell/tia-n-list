---
title: Palo Alto DoS flaw 🔥, FortiSIEM exploit 🔓, Kimwolf botnet 📱, ransomware wave 💀
date: 2026-01-15
tags: ["firewall vulnerabilities","botnet","ransomware","ddos attacks","zero-day exploitation","unauthenticated attacks","android malware","critical infrastructure"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical vulnerabilities in Palo Alto firewalls and FortiSIEM devices enable unauthenticated attacks that can disable network protections and facilitate remote code execution. Large-scale ransomware campaigns continue targeting high-value sectors while the Kimwolf botnet demonstrates the growing threat of compromised consumer IoT devices for DDoS operations.
---

# Daily Threat Intel Digest - 2026-01-15

## 🔴 Critical Threats & Active Exploitation

**[NEW] Palo Alto Networks warns of critical DoS flaw in firewalls**  
Palo Alto Networks disclosed a high-severity vulnerability (CVE-2026-0227) allowing unauthenticated attackers to disable next-generation firewalls and Prisma Access instances via denial-of-service attacks. Exploitation forces devices into maintenance mode, effectively crippling network protections. With Shadowserver tracking ~6,000 exposed firewalls online and historical precedents of zero-day exploitation against PAN-OS, immediate patching is critical for affected versions (10.2+). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/palo-alto-networks-warns-of-dos-bug-letting-hackers-disable-firewalls/); [Palo Alto Advisory](https://security.paloaltonetworks.com/CVE-2026-0227)]  

**[NEW] Public exploit released for critical FortiSIEM command injection flaw**  
Exploit code published for CVE-2025-64155 enables unauthenticated remote code execution on Fortinet FortiSIEM devices via the exposed phMonitor service (port 7900). Impacted versions include 6.7 through 7.4.1, with FortiSIEM Cloud and 7.5 unaffected. Given Fortinet's frequent targeting by ransomware groups (e.g., Black Basta) and 23 of its CVEs on CISA's KEV catalog, attackers will likely weaponize this rapidly. [[Tenable](https://www.tenable.com/blog/cve-2025-64155-exploit-code-released-for-critical-fortinet-fortisiem-command-injection); [BleepingComputer](https://www.bleepingcomputer.com/news/security/exploit-code-public-for-critical-fortisiem-command-injection-flaw/)]  

**[NEW] Kimwolf botnet infects 2M Android TV devices for DDoS attacks**  
The Kimwolf botnet, spun off from the record-breaking Aisuru DDoS botnet, has compromised over 2 million Android TV devices by abusing residential proxy networks. Lumen Technologies has neutralized 550+ C2 servers, but the botnet continues launching short-burst DDoS attacks (up to hours-long) against targets like Minecraft servers. Its rapid growth via untapped device populations poses severe risks if repurposed against critical infrastructure. [[CyberScoop](https://cyberscoop.com/kimwolf-aisuru-botnet-lumen-technologies/); [XLab Research](https://blog.xlab.qianxin.com/kimwolf-botnet-en/)]  

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Microsoft disrupts $40M RedVDS cybercrime platform**  
Microsoft seized RedVDS infrastructure in coordinated global operations, dismantling a virtual desktop service sold to criminals for $24/month. The platform facilitated BEC, phishing, and AI-driven scams (e.g., ChatGPT-generated phishing, deepfake impersonation), causing $40M in U.S. losses alone since March 2025 and compromising 191K+ organizations. Its distinctive VM fingerprint (WIN-BUNS25TD77J) enabled tracking across campaigns. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-seizes-servers-disrupts-massive-redvds-cybercrime-platform/); [Microsoft Blog](https://www.microsoft.com/en-us/security/blog/2026/01/14/inside-redvds-how-a-single-virtual-desktop-provider-fueled-worldwide-cybercriminal-operations/)]  

**[UPDATE] Ransomware campaigns target high-value sectors**  
Ransomware groups accelerated attacks this week, with:  
- **Nova**: Hit Dubai Air Wing (UAE government VIP airline) and National Auto Loan Network (USA), exfiltrating employee and financial data [[DeXpose 1](https://www.dexpose.io/nova-ransomware-group-strikes-dubai-air-wing/); [DeXpose 2](https://www.dexpose.io/nova-ransomware-attack-on-national-auto-loan-network/)]  
- **Akira**: Targeted U.S. firms including TruGolf (37GB data), Rebars & Mesh, ImageWorks Display, and H2 Builders, threatening to leak corporate contracts and client data [[DeXpose 1](https://www.dexpose.io/akira-ransomware-strikes-trugolf-in-usa/); [DeXpose 2](https://www.dexpose.io/akira-strikes-rebars-mesh-in-ransomware-attack/)]  
- **Qilin**: Compromised U.S. entities (Pathology Associates, Lunsford Capital, Ernest Maier) and UK's Gtech, demanding ransom to prevent medical and financial data leaks [[DeXpose 1](https://www.dexpose.io/qilin-ransomware-strikes-pathology-associates-of-saint-thomas/); [DeXpose 2](https://www.dexpose.io/qilin-ransomware-targets-uk-consumer-services-firm-gtech/)]  

## ⚠️ Vulnerabilities & Patches

**[NEW] Industrial systems patched in ICS Patch Tuesday**  
Siemens, Schneider Electric, Aveva, and Phoenix Contact released fixes for multiple vulnerabilities in operational technology (OT) systems. While specifics are pending publication, the coordinated update cycle addresses flaws impacting critical infrastructure environments. [[SecurityWeek](https://www.securityweek.com/ics-patch-tuesday-vulnerabilities-fixed-by-siemens-schneider-aveva-phoenix-contact/)]  

**[NEW] Multiple vendors address critical flaws**  
- **Red Hat**: Patched Linux kernel vulnerabilities in Enterprise Linux variants affecting privilege escalation and memory corruption [[CCCS Advisory](https://cyber.gc.ca/en/alerts-advisories/red-hat-security-advisory-av26-031)]  
- **Drupal**: Fixed vulnerabilities in Group Invite, Role Delegation, and Microsoft Entra ID SSO Login modules enabling bypass and injection [[CCCS Advisory](https://cyber.gc.ca/en/alerts-advisories/drupal-security-advisory-av26-030)]  

## 📋 Policy & Industry News

**[NEW] FTC bans GM from selling driver location data for 5 years**  
The FTC finalized an order prohibiting GM and OnStar from sharing geolocation/driver behavior data with consumer reporting agencies after the company sold data from millions of vehicles without consent. GM must obtain explicit consent for data collection and allow users to disable tracking, reflecting heightened enforcement against automotive data abuses. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ftc-bans-general-motors-from-selling-drivers-location-data-for-five-years/)]  

**[NEW] DHS finalizes ANCHOR to replace CIPAC infrastructure council**  
The Department of Homeland Security is establishing the Alliance of National Councils for Homeland Operational Resilience (ANCHOR) to replace the disbanded Critical Infrastructure Partnership Advisory Council (CIPAC). The new body aims to streamline industry-government threat discussions with flexible liability protections, addressing gaps in cross-sector coordination. [[CyberScoop](https://cyberscoop.com/dhs-anchor-cipac-replacement-critical-infrastructure-cybersecurity-liability-protections/)]  

**[NEW] France fines Free Mobile €42M over 2024 breach**  
CNIL fined France's second-largest ISP for GDPR violations after a breach exposing 23M subscribers' data. Failures included weak VPN authentication, delayed breach notifications, and excessive data retention. The fine underscores global tightening of data breach accountability. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/france-fines-free-mobile-42-million-over-2024-data-breach-incident/)]  

## 🛡️ Defense & Detection

**[NEW] ANY.RUN integrates with Tines for SOC automation**  
The new integration enables automated malware detonation and threat intelligence enrichment within Tines workflows, reducing mean time to respond (MTTR) by pulling sandbox verdicts and IOCs directly into incident playbooks. SOC teams can scale validation without tool-switching, handling alert spikes without added headcount. [[ANY.RUN Blog](https://any.run/cyber-security-blog/anyrun-tines-integration/)]