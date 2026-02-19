---
title: SolarWinds authentication bypass 🔓, VS Code RCE vulnerabilities 💻, North Korean crypto theft 🎭, ClawHavoc supply chain attack ⛓️, Microsoft Copilot data exposure 🤖
date: 2026-02-19
tags: ["authentication bypass","remote code execution","apt activity","supply chain attack","cryptocurrency theft","data exposure","zero-day exploitation","malware","enterprise software","ai security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical authentication bypasses in SolarWinds Web Help Desk and Ivanti EPMM enable unauthenticated remote code execution, while VS Code extensions and Microsoft Copilot expose enterprises to data theft and policy violations. North Korean APT groups and ClawHavoc supply chain attackers are actively exploiting these vectors to steal cryptocurrency and compromise AI agent platforms, requiring immediate patching and extension allowlisting to prevent widespread system compromise.
---

# Daily Threat Intel Digest - 2026-02-19

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical authentication bypass in SolarWinds Web Help Desk under active exploitation**  
Attackers are exploiting CVE-2025-40554 to bypass authentication in SolarWinds Web Help Desk versions prior to 2026.1, enabling unprivileged remote code execution without credentials. This flaw allows initial access and lateral movement in enterprise environments. Public proof-of-concept exploits and underground forum discussions accelerate exploitation, requiring immediate patching to prevent full helpdesk system compromise [[Cyble](https://cyble.com/blog/cyble-weekly-vulnerability-report-feb-19/)].

**[NEW] Unpatched VS Code extensions expose developers to RCE and data exfiltration**  
Four popular VS Code extensions—Live Server, Code Runner, Markdown Preview Enhanced, and Microsoft Live Preview—contain critical vulnerabilities (CVE-2025-65715, CVE-2025-65716, CVE-2025-65717) enabling remote code execution and file theft when users preview untrusted content or run attacker-controlled settings. No patches are available for non-Microsoft extensions, forcing defenders to disable them and enforce extension allowlisting to block credential harvesting and local file access [[SOCRadar](https://socradar.io/blog/vs-code-extension-cves-rce/)].

**[UPDATE] Ivanti EPMM zero-day exploited since July 2025 as attacks surge**  
CVE-2026-1340, a critical code injection flaw in Ivanti Endpoint Manager Mobile (EPMM), is being actively exploited for unauthenticated RCE. New research traces exploitation back to mid-2025, with attackers chaining it for broad deployment. Public PoCs and dark web chatter elevate risk; organizations must isolate EPMM instances and apply vendor patches urgently [[SecurityWeek](https://www.securityweek.com/ivanti-exploitation-surges-as-zero-day-attacks-traced-back-to-july-2025/)].

**[NEW] Microsoft 365 Copilot bypasses DLP to expose confidential emails**  
A flaw (CW1226324) in Microsoft 365 Copilot allows AI summarization of emails protected by sensitivity labels, violating Data Loss Prevention policies. The bug pulls labeled content from Sent/Draft folders without checks, exposing regulated data in healthcare, finance, and government sectors. Partial fixes are rolling out, but tenants should review Copilot logs for unauthorized access and pause use if sensitive data is at risk [[Cyberpress](https://cyberpress.org/microsoft-365-copilot-vulnerability-exposes-sensitive-emails-to-ai-summarization/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] North Korean APT uses counterfeit MetaMask to steal cryptocurrency in job interview scams**  
APT groups are delivering counterfeit MetaMask extensions through fake job interviews, tricking developers into running malicious code. The malware steals wallet credentials, replaces legitimate extensions, and exfiltrates funds. Attacks leverage social engineering to bypass browser security, requiring hardware wallet adoption and rigorous extension verification [[Cyberpress](https://cyberpress.org/backdoored-wallets-drain-crypto/)].

**[NEW] ClawHavoc supply chain poisons OpenClaw's ClawHub with 1,184 malicious skills**  
Attackers uploaded over a thousand malicious "Skills" to OpenClaw's marketplace, embedding reverse shells and data theft payloads in seemingly legitimate packages. Users running fake "weather assistant" or other plugins exposed API keys and installed stealers like Atomic macOS. Infrastructure takedowns reduced packages to 3,498, but remnants persist with thousands of downloads [[Antiy CERT](https://www.antiy.net/p/clawhavoc-analysis-of-large-scale-poisoning-campaign-targeting-the-openclaw-skill-market-for-ai-agents/)].

**[NEW] Fake CAPTCHA ClickFix campaign infects enterprises with Latrodectus and Supper backdoors**  
A widespread campaign tricks users into copying PowerShell commands from fake CAPTCHA prompts, executing `curl | powershell` to download Latrodectus (loader) and Supper (backdoor). Attackers maintain access via DLL sideloading and scheduled tasks, enabling lateral movement. Blocking PowerShell from Run dialogs and restricting outbound traffic mitigates the risk [[Cyberpress](https://cyberpress.org/fake-captcha-clickfix-outbreak/)].

**[NEW] Foxveil malware evades detection using Cloudflare, Netlify, and Discord**  
Foxveil, active since August 2025, stages payloads from trusted cloud platforms and injects shellcode via Early Bird APC or self-injection. Variants drop Cobalt Strike beacons and mutate strings to bypass AV. Defenders must monitor SysWOW64 writes and abnormal AI tool queries [[Cato Networks](https://www.catonetworks.com/blog/cato-ctrl-foxveil-new-malware/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] CISA warns critical Honeywell CCTV flaw enables account takeovers**  
CVE-2026-1670 (CVSS 9.8) allows unauthenticated recovery email changes in Honeywell CCTV cameras, granting full feed access and configuration control. No patches are available; isolate camera networks, enforce VPN-only remote access, and monitor for email alteration alerts [[CISA](https://www.cisa.gov/news-events/ics-advisories/icsa-26-048-04)].

**[NEW] Apache Druid authentication bypass exposes sensitive data stores**  
CVE-2026-23906 permits unauthorized access to Apache Druid databases, putting enterprise data at risk. Mitigate by restricting Druid access behind authentication layers and reviewing logs for anomalous queries [[Cyble](https://cyble.com/blog/cyble-weekly-vulnerability-report-feb-19/)].

**[NEW] SAP CRM and S/4HANA vulnerable to SQL injection via CVE-2026-0488**  
Authenticated attackers can execute arbitrary SQL statements to compromise SAP databases, risking full data breaches. Apply vendor patches and limit function module access to non-admin users [[Cyble](https://cyble.com/blog/cyble-weekly-vulnerability-report-feb-19/)].

## 🛡️ Defense & Detection

**[NEW] Microsoft Defender adds centralized script library with Copilot analysis**  
Microsoft Defender now allows SOC teams to pre-upload PowerShell/Batch scripts to a live response library, reducing triage delays. Copilot provides behavior summaries and risk flags, speeding remediation without mid-incident uploads [[Cyberpress](https://cyberpress.org/microsoft-defender-launches-centralized-script/)].

**[NEW] Researchers decrypt SysUpdate Linux variant C2 using emulation**  
A new SysUpdate variant for Linux encrypts C2 traffic; analysts used Unicorn Engine emulation to extract keys and decrypt payloads. This method enables rapid incident response for encrypted malware linked to APT27 [[LevelBlue](https://www.levelblue.com/blogs/spiderlabs-blog/pwning-malware-with-ninjas-and-unicorns/)].

## 📋 Policy & Industry News

**[NEW] Treasury launches initiative to manage cyber risks in AI tools for finance**  
The Treasury Department will release six resources from the AI Executive Oversight Group to help financial institutions govern AI systems, addressing data security and fraud risks. Guidance focuses on governance, transparency, and digital identity in AI deployments [[NextGov/FCW](https://www.nextgov.com/cybersecurity/2026/02/new-treasury-initiative-targets-improved-cyber-risk-management-ai-tools/411508/)].

**[NEW] Qualys introduces AI-driven Patch Reliability Score to prevent rollbacks**  
Qualys TruRisk Eliminate now scores patch reliability using AI, predicting deployment failures from real-world feedback. High-reliability patches deploy faster; low-reliability ones trigger additional testing, reducing outages [[Qualys Blog](https://blog.qualys.com/product-tech/2026/02/18/new-ai-powered-patch-reliability-scoring-predict-patch-impact-before-you-deploy)].

## ⚡ Quick Hits

- **[NEW] Arkanix Stealer offers MaaS with Python/C++ variants**  
  Discovered in October 2025, Arkanix stole browser data, crypto wallets, and Discord sessions via configurable payloads; infrastructure was taken down by December 2025 [[Kaspersky](https://securelist.com/arkanix-stealer/119006/)].

- **[NEW] Caracas blackout involved kinetic attacks, not pure cyber**  
  Evidence of physical damage to substations by missiles/kinetics caused outages, with cyber used for blinding defenses; attribution remains complex [[CyberScoop](https://www.cyberscoop.com/venezuela-blackout-cyberattack-vs-kinetic-damage-operation-absolute-resolve/)].

- **[NEW] nslookup.exe abused in ClickFix for stealthy DNS payload staging**  
  Attackers shift from PowerShell to nslookup to fetch Base64 payloads via DNS responses, evading detection; hunt for anomalous queries [[Cyberpress](https://cyberpress.org/hackers-abuse-nslookup/)].

- **[NEW] Nigerian sentenced to 8 years for $1.3M tax refund fraud**  
  Matthew Akande led a five-year scheme phishing tax firms to file fraudulent returns, stealing over $1.3M; extradition and conviction highlight international cybercrime enforcement [[CyberScoop](https://www.cyberscoop.com/nigerian-matthew-akande-tax-refund-fraud/)].