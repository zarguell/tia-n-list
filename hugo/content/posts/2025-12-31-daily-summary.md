---
title: MongoBleed vulnerability exploitation 🔐, ErrTraffic ClickFix attacks 🎭, APT36 LNK RAT campaign 🎯, LockBit 5.0 ransomware 💣, Zoom Stealer extensions 📹
date: 2025-12-31
tags: ["vulnerability exploitation","clickfix attacks","apt activity","ransomware","data theft","credential harvesting","social engineering","fileless malware","browser extensions","industrial control systems"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: MongoBleed vulnerability exploitation accelerates with 74,000 exposed MongoDB instances while ErrTraffic industrializes ClickFix attacks with 60% conversion rates, demonstrating how adversaries commoditize social engineering techniques. APT36 advances fileless LNK-based attacks against Indian government targets and LockBit 5.0 escalates critical infrastructure breaches as Zoom Stealer extensions harvest corporate meeting data from millions of browsers, highlighting the growing sophistication of state-sponsored and cybercrime operations against high-value targets.
---

# Daily Threat Intel Digest - 2025-12-31

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] MongoBleed exploitation accelerates as CISA issues emergency directive**  
CISA has ordered federal agencies to patch the actively exploited MongoBleed vulnerability (CVE-2025-14847) by January 19, 2026, as Shadowserver reports over 74,000 exposed MongoDB instances worldwide. The flaw allows unauthenticated attackers to steal credentials, API keys, and session data from unpatched deployments. Wiz telemetry shows 42% of cloud environments contain vulnerable instances, with Elastic releasing a proof-of-concept exploit that confirms widespread risk. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-orders-federal-agencies-to-patch-mongobleed-flaw-actively-exploited-in-attacks/); [Databreaches.net](https://databreaches.net/2025/12/30/us-australia-say-mongobleed-bug-being-exploited/)]

**[NEW] ErrTraffic service industrializes ClickFix attacks with 60% conversion rates**  
A new cybercrime platform called ErrTraffic enables automated ClickFix attacks by injecting fake browser glitches into compromised websites, tricking users into executing malicious PowerShell commands. Sold on Russian forums for $800, the service delivers OS-specific payloads—including Lumma/Vidar stealers on Windows and Cerberus on Android—while geofencing CIS countries. The platform's emergence signals the growing commoditization of social engineering tactics that bypass traditional security controls. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-errtraffic-service-enables-clickfix-attacks-via-fake-browser-glitches/)]

## 🎯 Threat Actor Activity & Campaigns  

**[NEW] APT36 targets Indian government with fileless LNK-based RAT campaign**  
Pakistan-linked APT36 (Transparent Tribe) is deploying a sophisticated campaign using malicious 2MB+ Windows LNK files masquerading as Japanese exam PDFs. The shortcuts abuse mshta.exe to fetch HTA payloads that execute fileless DLLs, establishing encrypted C2 over port 8621. Notably, the malware detects installed AV tools to adapt persistence methods—using startup shortcuts for Kaspersky but registry entries for Avast. This represents an evolution in the group's living-off-the-land tradecraft targeting defense and academic sectors. [[Cyberpress.org](https://cyberpress.org/apt36-cyber-attack/)]

**[UPDATE] LockBit 5.0 escalates attacks on critical sectors**  
LockBit 5.0 claimed three high-profile victims in 24 hours: Collins Computing (US accounting software), Eros Elevators (Indian infrastructure), and Fortis Healthcare (Indian medical provider). The group maintains its strategy of threatening data leaks to force ransom negotiations, with DeXpose warning these attacks often follow credential theft from infostealers. The campaign underscores ransomware groups' continued focus on healthcare and critical infrastructure. [[DeXpose](https://www.dexpose.io/lockbit-5-0-ransomware-targets-collins-computing-inc/); [DeXpose](https://www.dexpose.io/lockbit-5-0-targets-indian-pioneer-eros-elevators/); [DeXpose](https://www.dexpose.io/lockbit-5-targets-indian-healthcare-giant-fortis-healthcare/)]

**[UPDATE] Two cybersecurity professionals plead guilty to BlackCat extortion**  
Former incident response employees from Sygnia and DigitalMint admitted to conducting BlackCat/ALPHV ransomware attacks as affiliates, extorting $1.2M from a medical device manufacturer. The pair leveraged their defensive expertise to breach networks between April–December 2023 before the FBI's December 2023 disruption. Their sentencing in March 2026 highlights the persistent insider threat risk within cybersecurity firms. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/us-cybersecurity-experts-plead-guilty-to-blackcat-alphv-ransomware-attacks/); [Cyberpress.org](https://cyberpress.org/two-u-s-cybersecurity-professionals-plead-guilty-to-working-asalphv-blackcat-affiliates/)]

**[NEW] Zoom Stealer campaign harvests corporate meeting data from 2.2M browsers**  
A China-linked threat actor tracked as DarkSpectre deployed 18 malicious browser extensions (Chrome/Firefox/Edge) to exfiltrate data from 28 videoconferencing platforms. The extensions harvest meeting links, participant lists, and embedded passwords via WebSocket connections—enabling corporate espionage or impersonation attacks. Active extensions like "Chrome Audio Capture" (800K+ installs) remain in official stores, demonstrating limitations of current extension vetting. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/zoom-stealer-browser-extensions-harvest-corporate-meeting-intelligence/)]

**[NEW] AI-enhanced metamorphic crypter emerges on dark web**  
Threat actor ImpactSolutions is marketing "InternalWhisper," an AI-driven crypter claiming to rewrite its codebase with each build to evade Windows Defender. Sold via subscription, the tool delivers in-memory payloads with AES-256 encryption, process hollowing, and signed-binary sideloading. Its promotion reflects growing AI weaponization in malware development despite unverified efficacy claims. [[Cyberpress.org](https://cyberpress.org/ai-enhanced-metamorphic-crypter/); [GBHackers](https://gbhackers.com/ai-enhanced-crypter/)]

## ⚠️ Vulnerabilities & Patches  

**[NEW] Apache StreamPipes critical flaw enables admin hijacking**  
CVE-2025-47411 (CVSS 9.8) allows attackers with non-admin accounts to manipulate JWT tokens during user creation, escalating privileges to full admin control in versions 0.69.0–0.97.0. Exploitation could compromise streaming data pipelines or inject malicious data into downstream systems. Apache urges immediate upgrades to 0.98.0, with interim mitigations including network restrictions for admin interfaces. [[Cyberpress.org](https://cyberpress.org/critical-apache-streampipes-vulnerability/)]

**[NEW] IBM API Connect authentication bypass exposed**  
CVE-2025-13915 (CVSS 9.8) permits unauthenticated remote attackers to bypass authentication in IBM API Connect versions 10.0.8.0–10.0.8.5 and 10.0.11.0. IBM released iFixes for affected versions and recommends disabling self-service sign-up as a temporary measure. The flaw poses systemic risks to API-centric environments relying on the platform for access control. [[Cyberpress.org](https://cyberpress.org/critical-ibm-api-connect-vulnerability/)]

**[NEW] Vulnerability disclosures surge to alarming new levels**  
Cyble researchers tracked 1,782 new vulnerabilities in the final week of 2025—twice the historical average—with 282 already having proof-of-concept exploits. Critical flaws include Apache Tika XXE (CVE-2025-66516), Tenda router overflow (CVE-2025-15047), and actively exploited Cisco AsyncOS RCE (CVE-2025-20393). The trend underscores mounting patch management challenges heading into 2026. [[Malware.news](https://malware.news/t/the-week-in-vulnerabilities-the-year-ends-with-an-alarming-new-trend/102913#post_1)]

## 🛡️ Defense & Detection  

**[NEW] OpenAI warns prompt injection remains unsolvable for browser agents**  
OpenAI disclosed that its automated red teaming discovered new prompt-injection attacks against ChatGPT Atlas, where malicious content hijacks browser agents' workflows. The company implemented adversarial training for Atlas but acknowledges the technique may never be fully mitigated, urging organizations to limit agent permissions and monitor execution contexts. The UK NCSC previously warned of similar risks. [[Cyberscoop](https://cyberscoop.com/openai-chatgpt-atlas-prompt-injection-browser-agent-security-update-head-of-preparedness/)]

## 📋 Policy & Industry News  

**[NEW] Disney fined $10M for YouTube children's privacy violations**  
The DOJ fined Disney $10M for mislabeling kid-directed YouTube videos as "Not Made for Kids," enabling data collection for targeted advertising. The settlement requires Disney to implement parental alerts and proper content designation, following FTC actions against similar surveillance practices in education and social media sectors. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/disney-will-pay-10m-to-settle-claims-of-childrens-privacy-violations-on-youtube/)]

**[NEW] European Space Agency confirms breach of external servers**  
ESA acknowledged attackers accessed external servers supporting collaborative engineering, exfiltrating 200GB of data including source code and credentials from JIRA/Bitbucket instances. The agency claims only "unclassified" systems were impacted and has notified stakeholders, marking the second major ESA breach in 12 months after its 2024 web store compromise. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/european-space-agency-confirms-breach-of-external-servers/); [SecurityWeek](https://www.securityweek.com/european-space-agency-confirms-breach-after-hacker-offers-to-sell-data/)]