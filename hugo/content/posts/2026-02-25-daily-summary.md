---
title: Chinese ChatGPT harassment 🤖, NuGet supply chain attack 📦, Apache ActiveMQ LockBit 🔐, Freight credential theft 🚚, Zero-day sanctions ⚖️
date: 2026-02-25
tags: ["state-sponsored threats","supply chain attacks","ransomware","phishing","credential theft","zero-day exploits","asp.net developers","freight industry","oauth vulnerabilities","malicious packages"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Chinese law enforcement is leveraging ChatGPT to orchestrate global harassment campaigns while supply chain attacks through NuGet packages compromise ASP.NET developer credentials, highlighting the dual threat of AI-enabled influence operations and poisoned development environments. Critical vulnerabilities in Apache ActiveMQ are being actively exploited to deploy LockBit ransomware, and threat actors are stealing freight industry credentials at scale, while international sanctions target zero-day exploit brokers disrupting the underground market for stolen cyber tools.
---

# Daily Threat Intel Digest - 2026-02-25

## 🔴 Critical Threats & Active Exploitation

**[NEW] Chinese law enforcement uses ChatGPT to facilitate global harassment campaign**  
OpenAI revealed a Chinese law enforcement agency leveraged ChatGPT to review and edit reports on "cyber special operations," inadvertently exposing a large-scale harassment campaign targeting critics worldwide. The operation involves hundreds of staff, thousands of fake social media accounts, and techniques including mass posting, bogus complaints to silence dissidents, document forgery, and even impersonation of U.S. officials. The same account attempted to use ChatGPT to plan a propaganda campaign against Japanese Prime Minister Sanae Takaichi, proceeding after the model refused. Separately, China-nexus actors used ChatGPT to research U.S. persons, federal building locations, and professional forums, then generated emails to state officials and financial analysts seeking to move conversations to WhatsApp, Zoom, or Teams [[CyberScoop](https://cyberscoop.com/chinese-chatgpt-online-harassment-campaign-against-critics-dissidents/)].

**[NEW] NuGet supply chain attack steals ASP.NET developer credentials**  
Four malicious NuGet packages targeting ASP.NET developers have been downloaded over 4,500 times since August 2024, delivering a sophisticated multi-stage attack that exfiltrates credentials and establishes persistent backdoors. The lead package NCryptYo typosquats the legitimate NCrypto library, installing JIT compiler hooks that deploy a localhost proxy on port 7152 for C2 communication. Associated packages DOMOAuth2_ and IRAOAuth2.0 steal ASP.NET Identity data including user accounts and permissions, while SimpleWriter_ enables arbitrary file writing and process execution. VirusTotal detection remains extremely low (1/72 vendors for the primary payload), highlighting evasion challenges against heavily obfuscated .NET malware. Developers should verify package authors, monitor for unusual localhost connections, and implement CI/CD scanning [[Cyberpress](https://cyberpress.org/nuget-exploit-steals-credentials/)].

**[NEW] Attackers exploit Apache ActiveMQ to deploy LockBit ransomware**  
Threat actors are actively exploiting CVE-2023-46604 in Apache ActiveMQ to gain initial access to Windows environments, then leveraging RDP to deploy LockBit ransomware. The attack chain demonstrates how failure to patch this critical vulnerability allows adversaries to maintain persistent footholds while escalating privileges to domain-wide impact. ActiveMQ instances exposed to the internet remain at immediate risk, requiring urgent patching and network segmentation [[GBHackers](https://gbhackers.com/apache-activemq-vulnerability-2/)].

**[NEW] Diesel Vortex phishing campaign steals 1,649 freight industry credentials**  
Armenian-speaking threat actors connected to Russian infrastructure have stolen 1,649 unique credentials from freight and logistics organizations across the U.S. and Europe since September 2025. The operation uses 52 domains and sophisticated multi-stage cloaking to target platforms including DAT Truckstop, TIMOCOM, Penske Logistics, and Electronic Funds Source. Attackers employ Cyrillic homoglyph tricks, voice phishing, and Telegram infiltration to harvest credentials, MC/DOT numbers, and payment details, subsequently facilitating freight impersonation and cargo diversion schemes. The campaign infrastructure was disrupted through coordinated action involving multiple security firms [[BleepingComputer](https://www.bleepingcomputer.com/news/security/phishing-campaign-targets-freight-and-logistics-orgs-in-the-us-europe/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Operation Zero sanctioned as executive sentenced for zero-day theft**  
The U.S. Treasury sanctioned Russian exploit broker Operation Zero and its leader Sergey Zelenyuk for trafficking stolen U.S. government cyber tools, following the 87-month prison sentence of former L3Harris executive Peter Williams for selling eight zero-day exploits to the broker. Williams stole the exploits from Trenchant, a specialized cybersecurity unit, receiving $1.3 million in cryptocurrency while causing $35 million in losses to L3Harris. The sanctions extend to UAE-based affiliate Special Technology Services and associates linked to Trickbot, marking the first enforcement under the Protecting American Intellectual Property Act and signaling escalating action against the commercial zero-day market [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ex-l3harris-exec-jailed-for-selling-zero-days-to-russian-exploit-broker/); [CyberScoop](https://cyberscoop.com/l3harris-executive-peter-williams-sentenced-zero-day-exploits-russia/); [Cyberpress](https://cyberpress.org/u-s-slaps-sanctions-on-exploit-brokers/)].

**[NEW] Incransom claims attack on Saudi engineering giant Larsen & Toubro**  
The Incransom ransomware group announced it breached Larsen & Toubro Limited, a prominent Saudi Arabian engineering and construction firm, threatening to leak 400GB of sensitive data. The claim follows a pattern of ransomware groups targeting critical infrastructure and industrial sectors, with Incransom previously emerging as a significant threat to manufacturing and engineering organizations. Affected entities should immediately check for compromise indicators and validate backup integrity [[DeXpose via Malware.news](https://malware.news/t/incransom-strikes-engineering-leader-larsen-toubro/104382#post_1)].

**[NEW] ShinyHunters publishes 12.4M CarGurus records after breach**  
The ShinyHunters extortion group leaked personal information from 12.4 million CarGurus accounts, including email addresses, phone numbers, physical addresses, and finance application data. The 6.1GB archive was published on February 21, with HaveIBeenPwned confirming approximately 3.7 million records were newly exposed. CarGurus has not issued an official statement, but users should be alert for targeted phishing leveraging the leaked automotive and financial data. ShinyHunters has been prolific recently, also claiming attacks on Odido, Optimizely, and Panera Bread [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cargurus-data-breach-exposes-information-of-124-million-accounts/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Azure CLI OAuth vulnerability could enable Microsoft account hijacking**  
Researchers demonstrated an OAuth consent attack in Microsoft Entra ID where threat actors exploit legitimate applications like ChatGPT to breach user email accounts. When users grant Microsoft Graph OAuth permissions to malicious service principals, attackers can gain persistent access to cloud email without MFA interference. This represents a significant risk in environments where users frequently approve OAuth requests without full scrutiny, requiring administrators to implement strict application consent policies and user education [[GBHackers](https://gbhackers.com/oauth-vulnerabilities-in-entra-id/)].

**[NEW] Multiple vendors patch critical vulnerabilities in industrial and enterprise products**  
- SolarWinds addressed CVE-2025-40538 in Serv-U (versions before 15.5.4), a broken access control vulnerability enabling RCE [[Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/solarwinds-security-advisory-av26-165)]  
- HPE fixed AMD-SB-7059 in ProLiant AMD DL/XL servers, preventing guest-initiated machine check errors causing denial of service [[Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/hpe-security-advisory-av26-164)]  
- ABB released updates for AC500 V3 firmware (before 3.9.0) addressing CVE-2025-2595, CVE-2025-41659, and CVE-2025-41691, plus Automation Builder (before 2.9.0) for CVE-2024-41975 [[Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/control-systems-abb-security-advisory-av26-163)]  
- VMware patched vulnerabilities in Cloud Foundation (before 9.0.2.0), vSphere Foundation (before 9.0.2.0), and Aria Operations (before 8.18.6) [[Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/vmware-security-advisory-av26-162)]

**[NEW] Malicious npm package 'ambar-src' compromises 50,000+ downloads**  
A malicious npm package reached 50,000 downloads before removal, using preinstall scripts to deploy OS-specific payloads: msinit.exe on Windows, reverse_ssh client on Linux, and Apfell JXA payload on macOS. The typosquatted package likely mimics 'ember-source' and leverages YandexCloud functions for C2 communication, representing the latest in escalating supply chain risks for JavaScript ecosystems. Organizations should scan for the package and treat any affected system as fully compromised, with immediate credential rotation required [[Tenable](https://www.tenable.com/blog/cybersecurity-research-faq-new-malicious-npm-package-ambar-src)].

## 🛡️ Defense & Detection

**[NEW] Microsoft expands Copilot DLP to cover local Office documents**  
Microsoft will extend Purview Data Loss Prevention controls to Microsoft 365 Copilot across all storage locations between late March and late April 2026 via the Augmentation Loop (AugLoop) component. This enhancement addresses a previous bug where Copilot summarized confidential emails despite DLP policies by enabling the client to provide sensitivity labels directly rather than relying on Microsoft Graph calls. The change automatically applies to organizations with existing DLP policies blocking Copilot from accessing labeled content, improving protection for locally stored Word, Excel, and PowerPoint files [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-adds-copilot-data-controls-to-all-storage-locations/)].

**[NEW] Australian Signals Directorate open-sources Azul malware analysis platform**  
The ASD released Azul 9.0.0 under MIT license, providing a scalable malware repository and analytical engine designed to handle hundreds of millions of samples. Unlike triage tools, Azul focuses on post-initial-analysis workflows, enabling reverse engineers to create plugins for automated analysis and clustering across massive datasets. The Kubernetes-powered platform continuously updates results as new detection logic is developed, significantly reducing manual reverse engineering time. Organizations should note that while Azul is MIT-licensed, included dependencies may have different licenses requiring compliance review [[SOCFortress](https://socfortress.medium.com/australian-signals-directory-open-sourced-azul-malware-analysis-ad4e3751bdbb?source=rss-36613248f635------2)].

## 📋 Policy & Industry News

**[NEW] UK fines Reddit £20 million for child safety failures**  
The UK Information Commissioner's Office fined Reddit $20 million for inadequate child safety protections on its platform, representing ongoing regulatory pressure on social media companies to implement stronger safeguards for minor users [[SecurityWeek](https://www.securityweek.com/reddit-hit-with-20-million-uk-data-privacy-fine-over-child-safety-failings/)].

**[NEW] Microsoft reveals Windows 11 preview update improvements**  
The optional KB5077241 preview update for Windows 11 introduces native System Monitor (Sysmon) functionality, BitLocker reliability improvements, and a built-in network speed test tool. The update also adds support for Remote Server Administration Tools on Arm64 devices and reduces resume-from-sleep times, with these features expected to roll out generally in next month's Patch Tuesday [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/windows-11-kb5077241-update-improves-bitlocker-adds-sysmon-tool/)].

## ⚡ Quick Hits

- Wynn Resorts confirmed an employee data breach after extortion threats, with ShinyHunters claiming theft of over 800k records containing SSNs [[BleepingComputer](https://www.bleepingcomputer.com/news/security/wynn-resorts-confirms-employee-data-breach-after-extortion-threat/)]
- Cybercriminals launched a sophisticated phishing site impersonating Avast to steal credit card information, using the legitimate logo from the company's CDN [[GBHackers](https://gbhackers.com/fake-avast-website/)]
- Microsoft warned of malicious Next.js repositories being used to compromise developers through fake projects and technical assessments [[GBHackers](https://gbhackers.com/malicious-next-js-repositories/)]
- Fake Huorong Security site (huoronga[.]com) distributes ValleyRAT backdoor via trojanized NSIS installers [[Cyberpress](https://cyberpress.org/fake-huorong-site-deploys-valleyrat/)]
- ZeroDayRAT MaaS targeting Android/iOS sold on Telegram with features including live GPS tracking, camera/mic activation, and crypto wallet theft [[Cyberpress](https://cyberpress.org/zerodayrat-targets-mobile-devices/)]
- OpenClaw malicious skills manipulate AI agents to install Atomic Stealer (AMOS) on macOS devices [[Cyberpress](https://cyberpress.org/openclaw-installs-amos-malware/)]
- SURXRAT Android MaaS sold on Telegram offering full device control and data exfiltration capabilities [[GBHackers](https://gbhackers.com/android-rat-surxrat/)]
- 1Campaign cybercrime service helps malicious Google Ads evade detection by filtering out researchers and automated scanners [[BleepingComputer](https://www.bleepingcomputer.com/news/security/1campaign-platform-helps-malicious-google-ads-evade-detection/)]
- CrowdStrike reports attackers average just 29 minutes from initial compromise to lateral movement in 2025 [[DataBreaches.Net via Malware.news](https://malware.news/t/attackers-can-own-your-network-in-a-matter-of-minutes/104381#post_1)]