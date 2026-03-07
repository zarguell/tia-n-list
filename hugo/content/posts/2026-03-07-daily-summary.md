---
title: Claude AI Firefox exploits 🤖, Fake Meet MDM hijacking 🎯, Coruna iOS spyware 📱, DPRK crypto theft 💰, North Korean AI operations 🇰🇵
date: 2026-03-07
tags: ["ai vulnerabilities","mobile exploits","phishing","apt groups","cryptocurrency","authentication bypass","mdm abuse","zero-day","threat actors","supply chain"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Claude AI's discovery of 22 Firefox vulnerabilities demonstrates accelerating automated vulnerability research, while attackers distribute fake Google Meet updates that enroll devices in attacker-controlled MDM servers with a single click. North Korean threat groups are operationalizing AI across attack lifecycles to enhance crypto theft campaigns and fake worker schemes, showcasing how AI tools enhance sophisticated espionage operations.
---

# Daily Threat Intel Digest - 2026-03-07

## 🔴 Critical Threats & Active Exploitation

**[NEW] Claude AI Discovers 22 Firefox Vulnerabilities in 14 Days**  
Anthropic's Claude Opus 4.6 identified 22 novel Firefox vulnerabilities during a two-week period in February 2026, accounting for nearly 20% of all high-severity Firefox flaws fixed in the previous year. Mozilla deployed fixes for most issues in Firefox 148.0 after validating 112 crash reports, with 14 classified as high-severity including a Use-After-Free memory corruption flaw. While AI-generated exploits remained crude and ineffective against real-world sandbox protections, researchers developed functional exploits in two test cases at $4,000 in API costs, demonstrating accelerating automated vulnerability research capabilities [[Cyberpress](https://cyberpress.org/claude-ai-discovers-22-major-vulnerabilities/); [GBHackers](https://gbhackers.com/claude-ai-exposes-22-firefox-vulnerabilities/)].

**[NEW] Fake Google Meet Updates Enroll Devices in Attacker MDM**  
Attackers are distributing phishing pages impersonating Google Meet update notifications that use Windows' `ms-device-enrollment` URI scheme to hijack device management. A single click triggers native Windows enrollment dialogs pointing to attacker-controlled MDM servers on legitimate platforms like Esper, granting full device control including software installation, data access, and remote wiping. The campaign bypasses traditional security detection by abusing legitimate OS features rather than deploying malware, with no credential theft required [[Malwarebytes Blog](https://www.malwarebytes.com/blog/threat-intel/2026/03/one-click-on-this-fake-google-meet-update-can-give-attackers-control-of-your-pc)].

**[UPDATE] Coruna iOS Exploit Kit Added to CISA KEV List**  
CISA has added three iOS vulnerabilities from the Coruna exploit kit to its Known Exploited Vulnerabilities catalog, requiring federal agencies to patch by March 26. The kit contains 23 exploits and five full chains affecting iOS 13.0-17.2.1, with GTIG tracking its proliferation from nation-state espionage (Operation Triangulation) through Russian APT UNC6353 to Chinese financially-motivated UNC6691 using fake crypto sites. While Apple addressed core flaws in iOS 17.3, the scale (42,000+ devices) and sophistication highlight government-grade exploits entering criminal ecosystems [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-warns-of-apple-flaws-exploited-in-spyware-crypto-theft-attacks/); [SecurityWeek](https://www.securityweek.com/cisa-adds-ios-flaws-from-coruna-exploit-kit-to-kev/)].

**[NEW] pac4j-jwt Authentication Bypass Enables Full Impersonation**  
CVE-2026-29000 allows unauthenticated attackers to bypass JWT authentication in the pac4j-jwt Java library when processing encrypted JWTs (JWE). By knowing the server's RSA public key, attackers can impersonate arbitrary users including administrators across deployments using the vulnerable JwtAuthenticator component. The flaw received a maximum severity rating from Arctic Wolf following pac4j's March 3 patches [[Arctic Wolf](https://arcticwolf.com/resources/blog/cve-2026-29000/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] North Korean Groups Operationalize AI Across Attack Lifecycle**  
Microsoft Threat Intelligence reports Coral Sleet, Sapphire Sleet, and Jasper Sleet are using AI to accelerate fake worker schemes, with Jasper Sleet leveraging generative AI to research job postings, generate tailored personas, and craft professional communications that sustain long-term employment. Actors use AI tools like Faceswap for identity document forgery and prompt models to produce code snippets meeting performance expectations. The research also observes early experimentation with agentic AI for semi-autonomous workflows [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/03/06/ai-as-tradecraft-how-threat-actors-operationalize-ai/); [CyberScoop](https://cyberscoop.com/microsoft-north-korea-ai-operations/)].

**[NEW] DPRK Campaign Steals Crypto Keys via Cloud Exploitation**  
Suspected North Korean actors exploited the React2Shell vulnerability (CVE-2025-55182) and compromised AWS credentials to target cryptocurrency organizations. Attackers escalated privileges via AWS IAM roles, accessed Kubernetes clusters by modifying kubeconfig files, and exfiltrated Docker images containing proprietary exchange software and secrets. The campaign used VShell and FRP reverse proxies for persistence and leveraged South Korean VPN infrastructure for obfuscation [[Cyberpress](https://cyberpress.org/dprk-hackers-steal-crypto-keys/)].

**[NEW] Middle East Conflict Drives Multi-Vector Cyber Campaigns**  
Zscaler ThreatLabz tracks 8,000+ newly registered domains exploiting geopolitical tensions, including: LOTUSLITE backdoor distribution via conflict-themed lures targeting GCC regions; StealC malware delivery through fake news blogs; and credential harvesting sites impersonating US SSA portals and Israeli toll systems. Persian-language code artifacts suggest Iran-aligned involvement in some campaigns. Threat actors also deploy conflict-themed donation scams and meme-coin pump-and-dump schemes [[Zscaler](https://www.zscaler.com/blogs/security-research/middle-east-conflict-fuels-opportunistic-cyber-attacks)].

## 📋 Policy & Industry News

**[NEW] Trump Administration Releases Offensive Cyber Strategy**  
The White House issued a 7-page national cyber strategy emphasizing "unleashing the private sector" to disrupt adversaries and adopting offensive cyber capabilities. Six pillars include: shaping adversary behavior through offensive operations; securing critical infrastructure with U.S.-made products; sustaining AI and quantum superiority; and building cyber talent. The document references recent operations against Iran's nuclear infrastructure and Maduro's capture, while explicitly rejecting "partial measures" of prior administrations. A concurrent executive order combats cybercrime and establishes a fraud victim restoration program [[Nextgov/FCW](https://www.nextgov.com/cybersecurity/2026/03/trumps-s-new-cyber-strategy-details-more-offensive-response-cyber-threats/411963/); [CyberScoop](https://cyberscoop.com/trump-cybersecurity-strategy/)].

**[NEW] Anthropic Exits Pentagon Contracts Over Safety Restrictions**  
Anthropic ended its DoD partnership after refusing to allow AI use for "mass surveillance" or "fully autonomous weapons," prompting Defense Secretary Pete Hegseth to label safety provisions "woke." The administration then barred federal agencies from using Anthropic models and designated the company a supply-chain risk. OpenAI subsequently secured the displaced contracts, vowing to maintain similar safety constraints while working with defense systems [[Schneier on Security](https://www.schneier.com/blog/archives/2026/03/anthropic-and-the-pentagon.html)].

**[NEW] Congress Advances Rural Utility Cybersecurity Act**  
The House Energy Committee unanimously passed legislation reauthorizing the Rural and Municipal Utility Advanced Cybersecurity program with $250 million in funding over five years. The program provides critical cyber assistance to under-resourced electric cooperatives, addressing gaps highlighted by Volt Typhoon's targeting of energy infrastructure. Companion bills clarify DOE's cybersecurity leadership role and mandate state-level energy cyber planning [[CyberScoop](https://cyberscoop.com/house-committee-advances-rural-utility-cybersecurity-act/)].