---
title: OAuth phishing kits surge 📈, npm supply chain attacks 🔗, Vidar infostealer targets devs 🪝, telecom ransomware ☎️, healthcare data breach 🏥
date: 2026-04-05
tags: ["device code phishing","oauth vulnerability","phishing-as-a-service","supply chain attack","infostealer","ransomware","north korean apt","telecom sector","healthcare data breach","developer security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Phishing-as-a-service kits exploiting OAuth 2.0 device authorization flows have surged dramatically, democratizing MFA bypass techniques through platforms like EvilTokens while simultaneously enabling credential theft via fake Claude Code repositories delivering Vidar infostealer to developers. North Korean threat actor UNC1069 continues targeting open-source supply chains with sophisticated social engineering, as demonstrated by the Axios npm compromise, while ransomware operators like Netrunner escalate attacks on critical infrastructure sectors including telecommunications and healthcare.
---


# Daily Threat Intel Digest - 2026-04-05

## 🔴 Critical Threats & Active Exploitation

**[NEW] Device Code Phishing Attacks Surge 37x as EvilTokens Phishing-Kit Ecosystem Expands**

Device code phishing attacks exploiting the OAuth 2.0 Device Authorization Grant flow have surged 37 times year-over-year, with researchers at Push Security identifying over a dozen phishing-as-a-service (PhaaS) kits now offering this technique. The attack bypasses traditional MFA by tricking victims into authorizing an attacker's device through a legitimate login flow, granting persistent access via refresh tokens. The EvilTokens kit has emerged as the most prominent tool "democratizing" these attacks for low-skilled cybercriminals, but at least 10 competing platforms are now operational—including VENOM, SHAREFILE, CLURE, LINKID, and others—creating a robust marketplace for device code phishing. These kits use realistic SaaS-themed lures (Microsoft 365, DocuSign, Adobe), anti-bot protections, and abuse cloud platforms including Cloudflare, DigitalOcean, and workers.dev for hosting. Organizations should immediately implement conditional access policies to disable device code flows when not needed and monitor logs for unexpected device code authentication events from unusual IP addresses. [BleepingComputer](https://www.bleepingcomputer.com/news/security/device-code-phishing-attacks-surge-37x-as-new-kits-spread-online/)

---

**[NEW] Claude Code Leak Weaponized to Deliver Vidar Infostealer via Fake GitHub Repositories**

Threat actors are actively exploiting the recent Claude Code source code leak by creating fraudulent GitHub repositories that deliver Vidar infostealer malware. Claude Code, Anthropic's terminal-based AI agent capable of autonomous system interaction and direct LLM API access, became the lure after its source code was leaked. Attackers are hosting fake repositories containing the leaked code but modified to include Vidar, an established infostealer that harvests credentials, financial data, and browser information from compromised systems. Developers who download and execute these repositories risk infection of their local development environments, potentially exposing API keys, tokens, and source code to exfiltration. Security teams should verify the authenticity of any Claude Code implementations and ensure developer workstations have robust endpoint protection with behavioral monitoring. [malware.news](https://malware.news/t/claude-code-leak-used-to-push-infostealer-malware-on-github/105740)

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Netrunner Ransomware Group Claims Attack on Italian Telecom GEG Telecomunicazioni**

The ransomware group Netrunner has claimed responsibility for a cyberattack against GEG Telecomunicazioni (geg.it), a leading telecommunications provider in Italy. On April 3, 2026, the group posted an extortion notice on its leak site threatening to publish stolen sensitive data unless company representatives initiated negotiations. This attack follows Netrunner's observed pattern of targeting organizations across multiple sectors with double-extortion tactics—encrypting systems while simultaneously threatening data disclosure to pressure payment. Telecommunications providers represent high-value targets due to their critical infrastructure role and access to large volumes of customer communications data. Organizations should immediately audit ransomware group communications for references to their domains, validate backup integrity with offline and immutable copies, and ensure incident response teams are pre-staged given the telecommunications sector's continued targeting. [malware.news](https://malware.news/t/netrunner-targets-italian-telecom-leader-geg-telecomunicazioni/105745)

---

**[UPDATE] Axios npm Supply Chain Attack – North Korean UNC1069 Expands Targeting to Additional Node.js Maintainers**

New technical analysis confirms the Axios npm supply chain attack involved sophisticated social engineering targeting the project's lead maintainer, Jason Saayman, through a multi-stage campaign attributed to North Korean threat actor UNC1069. Attackers cloned a legitimate company's branding and created a fake Slack workspace with staged activity and realistic profiles before inviting the maintainer to a video call impersonating Microsoft Teams. During the call, a fake technical error prompted the victim to install a "Teams update" that was actually a remote access trojan, bypassing MFA by capturing authenticated sessions. Google Threat Intelligence Group has attributed the attack to UNC1069, noting use of WAVESHAPER.V2, an updated version of previously observed malware. Critically, additional maintainers across the Node.js ecosystem—including contributors to widely-used packages with billions of weekly downloads and Node.js core contributors—have reported being targeted by the same campaign, confirming this was a coordinated operation against high-trust open-source projects rather than a one-off attack. Systems that installed malicious Axios versions 1.14.1 or 0.30.4 during the three-hour window before removal should be considered fully compromised, with all credentials and authentication keys requiring immediate rotation. [BleepingComputer](https://www.bleepingcomputer.com/news/security/axios-npm-hack-used-fake-teams-error-fix-to-hijack-maintainer-account/)

---

## ⚠️ Vulnerabilities & Patches

*No new CVEs or patches requiring immediate coverage today. See previous days for ongoing coverage of Citrix NetScaler CVE-2026-3055, OpenSSH shell injection, F5 BIG-IP RCE (CVE-2025-53521), and Chrome zero-day (CVE-2026-5281).*

---

## 🛡️ Defense & Detection

**[NEW] Massachusetts Public Safety Communications Disrupted by Cyberattack Across Regional Emergency Center**

A cybersecurity incident has impacted the Patriot Regional Emergency Communications Center and associated Massachusetts towns (Ashby, Dunstable, Pepperell, and Townsend), disrupting police and fire department phone systems and public safety operations. The attack was identified early Tuesday, triggering emergency response procedures as affected municipalities reported degraded communications capabilities. Regional emergency communications centers represent critical infrastructure where even temporary disruption can delay response times for life-safety operations. Organizations operating shared communications infrastructure should review their incident response playbooks for failover scenarios and ensure out-of-band communication channels are tested and available. [malware.news](https://malware.news/t/serious-cyberattack-impacts-phones-public-safety-systems-in-several-massachusetts-towns/105741)

---

## 📋 Policy & Industry News

**[NEW] Meta Suspends Mercor Partnership Following Data Breach Exposing AI Industry Secrets**

Meta has indefinitely paused all work with data contracting firm Mercor following a major security breach that reportedly put AI industry secrets at risk. According to sources confirmed by WIRED, the breach has prompted other major AI laboratories to reevaluate their relationships with Mercor, suggesting the incident may have exposed sensitive proprietary information common across multiple AI organizations. Mercor provides data labeling and evaluation services that typically involve processing proprietary AI training data and model information—making a breach potentially far-reaching across the AI sector. Organizations contracting third-party data services should review data handling agreements and assess whether their proprietary AI assets may be co-mingled with contractor infrastructure. [malware.news](https://malware.news/t/meta-pauses-work-with-mercor-after-data-breach-puts-ai-industry-secrets-at-risk/105743)

---

**[NEW] Hong Kong Hospital Authority Data Breach Exposes 56,000 Patients to Unauthorized Access**

Hong Kong's Hospital Authority has apologized for a data breach affecting over 56,000 patients served by hospitals in Kowloon East, with the unauthorized retrieval of various patient information now under investigation by the privacy watchdog and police. The breach represents one of the larger healthcare data incidents reported in the Asia-Pacific region recently, compromising sensitive medical records that could be leveraged for identity theft, insurance fraud, or targeted phishing campaigns against affected patients. Healthcare organizations should ensure access controls are enforced with the principle of least privilege, particularly for systems containing large patient datasets, and maintain comprehensive audit logging to enable rapid breach detection and forensic analysis. [malware.news](https://malware.news/t/hong-kong-hospital-authority-apologises-for-data-breach-involving-56-000-patients/105739)

---

**[NEW] UK Education Authority IT System Targeted in Cyberattack Ahead of Northern Ireland Exam Season**

An IT system used by schools across Northern Ireland has been targeted in a cyberattack, prompting the Education Authority to execute mandatory password resets for all users. Schools received notification Thursday that the reset was part of "work to manage an IT security issue," indicating active incident response operations. The timing ahead of exam season amplifies operational impact, as educational institutions rely heavily on IT systems for administration, student records, and increasingly for digital examination delivery. Education sector organizations should prioritize backup verification and离线存储验证, as this sector has been consistently targeted by ransomware operators seeking to maximize pressure through academic calendar constraints. [malware.news](https://malware.news/t/uk-school-it-system-targeted-in-cyber-attack-ahead-of-exam-season/105742)

---

**[NEW] North Carolina Law Firm Auger & Auger Discloses 25-Minute Network Breach**

The personal injury law firm Auger & Auger has notified affected individuals of unauthorized network access that lasted only 25 minutes on February 17, 2026, with notification letters sent on March 30 offering one year of complimentary identity protection services through EPIC-Privacy D Solutions. While the brevity of the access window may suggest rapid detection, threat actors with pre-positioned access or well-defined objectives can extract significant value in minutes—including client case files, personal injury claim documentation, and financial records. Law firms remain attractive targets due to their access to sensitive litigation information, corporate client data, and privileged communications that could hold substantial monetary or strategic value. Legal organizations should assume that even short-duration breaches warrant comprehensive forensic investigation to rule out persistent access or data staging. [malware.news](https://malware.news/t/the-breach-lasted-25-minutes-how-long-will-the-litigation-last/105744)

---

## ⚡ Quick Hits

- The Axios maintainers have implemented changes to prevent similar incidents, including credential hygiene improvements and heightened verification for collaborative outreach.