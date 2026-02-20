---
title: Healthcare ransomware attacks 🏥, Ivanti EPMM zero-days 🔓, ATM jackpotting 💰, North Korean IT schemes 🇰🇵, AI-powered malware 🤖
date: 2026-02-20
tags: ["ransomware","zero-day vulnerabilities","healthcare sector","financial sector","north korean threat actors","ai malware","data exposure","supply chain attacks","mobile threats","air gap bypass"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Healthcare ransomware attacks are disrupting critical medical services while Ivanti EPMM zero-days enable widespread automated exploitation of enterprise infrastructure. Financial institutions face escalating losses from ATM jackpotting campaigns, while North Korean IT worker schemes and AI-powered malware represent emerging nation-state threats that bypass traditional defenses.
---

# Daily Threat Intel Digest - 2026-02-20

## 🔴 Critical Threats & Active Exploitation

**[NEW] Major healthcare ransomware disrupts Mississippi's largest medical center**  
The University of Mississippi Medical Center (UMMC) shut down all clinic operations statewide following a ransomware attack that disabled its Epic EMR systems and forced cancellation of outpatient procedures. Attackers have communicated directly with officials, though no group has claimed responsibility. UMMC—the state's only Level I trauma center and children's hospital—is operating via downtime procedures while investigating with CISA and the FBI. The breach risks exposure of sensitive patient data and could exacerbate Mississippi's healthcare crisis if recovery is prolonged [[BleepingComputer](https://www.bleepingcomputer.com/news/security/university-of-mississippi-medical-center-closes-clinics-after-ransomware-attack/)].  

**[UPDATE] Ivanti EPMM zero-days under active exploitation**  
Two newly disclosed Ivanti Endpoint Manager Mobile vulnerabilities (CVE-2026-1281/CVE-2026-1340) are being weaponized in automated attacks targeting MDM infrastructure worldwide. Attackers execute arbitrary code via legacy bash scripts, deploying web shells and reverse shells without authentication. Observed victims include government agencies and healthcare providers across the US, Germany, and Australia. CISA added CVE-2026-1281 to its Known Exploited Vulnerabilities catalog; immediate patching is critical as over 4,400 EPMM instances remain exposed [[Cyberpress](https://cyberpress.org/ivanti-epmm-zero-days-exploited/)].  

**[UPDATE] BeyondTrust RCE exploited to deploy VShell and SparkRAT**  
Critical vulnerability CVE-2026-1731 in BeyondTrust's remote access software is being actively exploited to deploy VShell backdoors and SparkRAT, enabling full system compromise. Campaigns span multiple industries and regions, with attackers gaining persistence through credential theft and lateral movement. Organizations using BeyondTrust must apply emergency patches immediately and hunt for signs of VShell or SparkRAT infections [[GBHackers](https://gbhackers.com/beyondtrust-vulnerability/); [Unit42](https://unit42.paloaltonetworks.com/beyondtrust-cve-2026-1731/)].  

**[NEW] FBI warns of ATM jackpotting surge costing $20M**  
Over 700 ATM jackpotting attacks in 2025 used Ploutus malware to force cash machines into dispensing money by bypassing bank authorization. Criminals gain physical access with generic keys, install malware on hard drives, and trigger payouts remotely. Losses exceeded $20 million—nearly 40% of all incidents reported since 2020. Financial institutions should audit ATM systems for unauthorized removable media and implement gold image integrity validation [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-over-20-million-stolen-in-surge-of-atm-malware-attacks-in-2025/); [SecurityWeek](https://www.securityweek.com/fbi-20-million-losses-caused-by-700-atm-jackpotting-attacks-in-2025/)].  

## 🎯 Threat Actor Activity & Campaigns  

**[NEW] Ukrainian sentenced for North Korean IT worker infiltration scheme**  
Oleksandr Didenko received 5 years in prison for running UpWorkSell—a platform that sold stolen U.S. identities to North Korean IT workers. He facilitated infiltration into 40+ U.S. companies via 871 identities and managed "laptop farms" across 7 countries. The scheme funneled over $1.4M to North Korea's weapons programs, highlighting how IT worker schemes directly fund adversarial regimes [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ukrainian-gets-5-years-for-helping-north-koreans-infiltrate-us-firms/); [CyberScoop](https://www.cyberscoop.com/doj-ukrainian-north-korea-remote-worker-scheme-facilitator-sentenced/)].  

**[NEW] Ransomware blitz targets healthcare, automotive, and recruitment sectors**  
Multiple ransomware groups escalated attacks this week:  
- NightSpire breached Nebraska Health Imaging (healthcare) and Germany's KFZ Sauter (automotive)  
- Nova hit Nebraska Health Imaging with data leak threats  
- Akira targeted Cargo Largo (retail) while Beast struck First 4 Recruitment  
Groups threaten to leak sensitive data including financials, GDPR documents, and patient records. Healthcare and automotive sectors remain top targets due to operational disruption value [[Malware.news](https://malware.news/t/akira-ransomware-strikes-cargo-largo/104272#post_1); [Malware.news](https://malware.news/t/nightspire-ransomware-targets-kfz-sauter-gmbh-co-kg-in-germany/104269#post_1)].  

## ⚠️ Vulnerabilities & Patches  

**[NEW] Splunk Enterprise Windows vulnerability enables SYSTEM-level hijacking**  
CVE-2026-20140 (CVSS 7.7) allows unprivileged attackers to achieve SYSTEM privileges via DLL search-order hijacking. By creating malicious directories on Splunk's installation path, attackers inject code loaded when the Splunk service restarts. Affects versions below 10.2.0, 10.0.3, 9.4.8, 9.3.9, and 9.2.12. Organizations must restrict write access to installation paths and upgrade immediately [[Cyberpress](https://cyberpress.org/splunk-enterprise-for-windows-vulnerability/)].  

**[NEW] SvelteKit/Vercel cache deception exposes user data**  
SvelteSpill (CVE-2026-27118) lets attackers steal sensitive data like session tokens by abusing Vercel's cache rules. By crafting URLs with `__pathname` parameters, attackers bypass authentication and retrieve cached responses from `/api/` endpoints. Vercel deployed platform-wide fixes on Feb 19; users should rescan repositories and verify deployments [[Cyberpress](https://cyberpress.org/cache-deception-vulnerability-found-in-sveltekit-and-vercel-combo-exposes-user-data-to-attackers/)].  

**[NEW] MCP servers introduce RCE and data theft risks**  
Anthropic's Model Context Protocol (MCP) servers expose enterprises to remote code execution and data exfiltration when malicious servers manipulate AI agent requests. Attackers abuse tool permissions in Slack/Microsoft Graph integrations to execute commands or steal OAuth tokens. Praetorian's MCPHammer tooling validates exploitability; organizations must review MCP installations and restrict auto-approvals [[Cyberpress](https://cyberpress.org/mcp-servers-expose-data-risk/)].  

**[NEW] Google rushes Chrome fix for PDFium/V8 flaws**  
Critical Chrome vulnerabilities (CVEs not assigned) enable arbitrary code execution via PDF files or V8 engine exploits. Stable Channel updates to 145.0.7632.109/.110 (Windows/Mac) and 144.0.7559.109 (Linux) patch the flaws. Enterprises should enforce automatic updates and block untrusted PDF downloads until patches deploy [[GBHackers](https://gbhackers.com/google-chrome-update-pdfium-v8/)].  

## 📋 Policy & Industry News  

**[UPDATE] Microsoft 365 Copilot exposed confidential data due to logic error**  
Service incident CW1226324 revealed Copilot ingested and surfaced "Confidential"-labeled emails from Sent Items and Drafts folders—bypassing DLP policies. Microsoft deployed a fix on Feb 19, but the incident exposes critical governance gaps in AI data pipelines. Organizations must audit Copilot usage logs and implement "AI-aware" DLP controls for sensitive data [[SOCFortress](https://socfortress.medium.com/microsoft-365-copilot-confidential-data-exposure-1f981c4489dc)].  

**[NEW] Silicon Valley engineers charged with trade secret theft for Iran**  
Three San Jose engineers face federal charges for stealing processor security and cryptography trade secrets from Google and other tech firms, then transferring data to Iran. The group used screen photography and third-party messaging apps to evade detection, violating export controls. Security teams must monitor exfiltration tactics beyond traditional downloads and strengthen exit protocols [[Cyberpress](https://cyberpress.org/silicon-valley-engineers-charged-over-theft/)].  

## 🛡️ Defense & Detection  

**[NEW] "Emoji smuggling" evades security filters**  
Attackers encode malicious commands using Unicode emojis (e.g., 🔥📁🌐💀) and invisible characters to bypass pattern-based detection. Techniques include lookalike Cyrillic characters in domains and breaking malicious strings with zero-width spaces. Defenders should normalize Unicode inputs and monitor for anomalous character sequences [[Cyberpress](https://cyberpress.org/emoji-code-bypasses-security/)].  

**[NEW] Cryptojacking malware bypasses air-gaps via USB drives**  
Monero-mining malware spreads through removable media to infect air-gapped systems. It abuses hardware change events (WM_DEVICECHANGE) to propagate across E:/Z: drives and persists via kernel exploits. Organizations must disable USB autorun, scan removable media, and monitor for unauthorized hardware access [[Cyberpress](https://cyberpress.org/malware-bypasses-air-gapped-security/)].  

**[NEW] PromptSpy Android malware weaponizes Gemini AI**  
First-of-its-kind Android malware uses Google's Gemini AI to make real-time persistence decisions. PromptSpy dynamically manipulates UI elements based on AI-generated commands, evading static detection. Defenders should monitor Gemini API abuse and restrict AI model access in mobile environments [[BleepingComputer](https://www.bleepingcomputer.com/news/security/promptspy-is-the-first-known-android-malware-to-use-generative-ai-at-runtime/); [SecurityWeek](https://www.securityweek.com/promptspy-android-malware-abuses-gemini-ai-at-runtime-for-persistence/)].