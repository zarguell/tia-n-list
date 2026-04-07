---
title: Fortinet zero-day exploitation 🔴, Windows Defender LPE 🔨, Flowise AI flaw 🤖, Medusa ransomware escalation 💣, Iranian M365 campaigns 🎯
date: 2026-04-07
tags: ["zero-day exploitation","ransomware","credential attacks","ai infrastructure","privilege escalation","supply chain","healthcare sector","middle east","software vulnerabilities","ransomware affiliate"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Active exploitation of zero-day vulnerabilities in Fortinet FortiClient EMS, Windows Defender, and Flowise AI platforms is exposing thousands of internet-facing systems to remote code execution and full system compromise, while the Medusa ransomware affiliate Storm-1175 has escalated its tactics to weaponize zero-day flaws for rapid attacks against healthcare, education, and finance sectors. Iranian threat actors are conducting password-spraying campaigns against M365 tenants in the Middle East, and North Korean actors are leveraging malicious npm packages for software supply chain compromises targeting developer environments.
---
# Daily Threat Intel Digest - 2026-04-07

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] CISA adds Fortinet FortiClient EMS zero-day to KEV catalog; exploitation ramps up**
The FortiClient EMS zero-day (CVE-2026-35616) disclosed over the weekend is now officially added to CISA's Known Exploited Vulnerabilities catalog, confirming active abuse in the wild. While a hotfix was released on April 4, exploitation attempts have ramped up significantly following the disclosure, putting the estimated 2,000 publicly exposed instances at immediate risk of remote code execution. Federal agencies have until April 9 to remediate, but private sector organizations are urged to apply the hotfix immediately, as attackers are moving quickly during the holiday window. [[CISA Alert](https://cyberpress.org/fortinet-0-day-vulnerability/); [CyberScoop Analysis](https://cyberscoop.com/fortinet-forticlient-ems-zero-day-cve-2026-35616-hotfix-known-exploited/); [GBHackers](https://gbhackers.com/cisa-alerts-exploited-fortinet-zero-day-vulnerability/)]

**[NEW] Unpatched Windows Defender zero-day "BlueHammer" enables full system takeover**
A disgruntled security researcher publicly disclosed "BlueHammer," a local privilege escalation (LPE) vulnerability in Windows Defender that allows attackers to gain SYSTEM privileges. Because the exploit code is now public on GitHub and Microsoft has not yet issued a patch, threat actors can chain this flaw with initial access vectors to completely compromise affected machines. While the exploit requires local access, this is a common foothold for attackers who leverage social engineering or other malware to gain entry, making this a high-priority threat for defenders. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/disgruntled-researcher-leaks-bluehammer-windows-zero-day-exploit/); [Cyberpress](https://cyberpress.org/releases-windows-defender-0-day/); [GBHackers](https://gbhackers.com/windows-defender-0-day-published-online/)]

**[NEW] Flowise AI platform critical flaw exploited; 15,000 instances exposed**
Attackers are actively exploiting CVE-2025-59528, a critical code injection vulnerability in Flowise, a popular open-source AI development platform. The flaw carries a maximum CVSS score of 10.0 and allows unauthenticated remote attackers to execute arbitrary code, potentially giving them full control over the AI infrastructure. With 15,000 instances currently exposed to the internet, organizations developing large language models or other AI applications must patch immediately to prevent data theft or model manipulation. [[GBHackers](https://gbhackers.com/attackers-exploit-flowise-injection-vulnerability/)]

**[UPDATE] Medusa ransomware affiliate Storm-1175 escalates with zero-day exploitation**
Microsoft has identified that the financially motivated group Storm-1175 has evolved from leveraging N-day vulnerabilities to weaponizing zero-day flaws in high-velocity attacks. The group, which focuses on healthcare, education, and finance sectors, is now capable of moving from initial access to data exfiltration and ransomware deployment in under 24 hours. This shift significantly raises the stakes for perimeter defense, as attackers are no longer waiting for patches to be publicly available before striking. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-links-medusa-ransomware-affiliate-to-zero-day-attacks/); [GBHackers](https://gbhackers.com/microsoft-warns-storm-1175/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Iranian threat actors target M365 tenants in Middle East password spray**
A coordinated password-spraying campaign linked to Iran has targeted Microsoft 365 environments across Israel and the UAE in three distinct waves throughout March 2026. This activity highlights continued focus on credential-based attacks in the region, specifically aimed at organizations using cloud-based productivity suites. [[GBHackers](https://gbhackers.com/m365-tenants/)]

**[NEW] German authorities identify REvil and GandCrab ransomware leaders**
The German Federal Police (BKA) have identified two Russian nationals, Daniil Maksimovich Shchukin and Anatoly Sergeevitsch Kravchuk, as the leaders behind the GandCrab and REvil ransomware operations from 2019 to 2021. The pair is accused of at least 130 extortion cases in Germany, causing over $40 million in damages, and are currently believed to be residing in Russia. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/german-authorities-identify-revil-and-gandcrab-ransomware-bosses/)]

**[NEW] DPRK "OtterCookie" infrastructure mapped via npm supply chain**
New research has mapped the infrastructure for the DPRK-linked "OtterCookie" malware, revealing a sophisticated setup leveraging legitimate cloud platforms like Vercel to deliver NodeJS-based stealers. The campaign begins with malicious npm packages—such as "npm-doc-builder"—that establish persistence via SSH keys and scan for sensitive developer files, underscoring the persistent threat to software supply chains from North Korean actors. [[Malware News](https://malware.news/t/mapping-ottercookie-infrastructure/105768#post_1)]

## ⚠️ Vulnerabilities & Patches

**[NEW] Ninja Forms WordPress plugin vulnerable to critical RCE**
A critical unauthenticated arbitrary file upload vulnerability (CVE-2026-0740) has been discovered in the Ninja Forms File Upload plugin for WordPress. With a CVSS score of 9.8 and an estimated 50,000 sites running the vulnerable plugin, attackers can exploit the flaw to execute remote code on affected servers. Website administrators using Ninja Forms should update immediately. [[GBHackers](https://gbhackers.com/50000-sites-running-ninja-forms-vulnerable/)]

**[NEW] GPUBreach attack bypasses IOMMU for system takeover via GPU Rowhammer**
Researchers have demonstrated "GPUBreach," a new attack technique that induces Rowhammer bit-flips on GPU GDDR6 memories to escalate privileges and compromise systems even when Input-Output Memory Management Unit (IOMMU) protections are enabled. By exploiting memory-safety bugs in the NVIDIA driver, attackers can achieve root access, posing a risk to AI workloads and high-performance computing environments. A full technical paper will be released on April 13. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-gpubreach-attack-enables-system-takeover-via-gpu-rowhammer/)]

**[NEW] Progress ShareFile Storage Zones Controller pre-auth RCE chain**
Two critical vulnerabilities (CVE-2026-2699 and CVE-2026-2701) in Progress ShareFile Storage Zones Controller allow for a pre-authentication remote code execution chain. The flaws—an authentication bypass and a deserialization issue—enable unauthenticated attackers to take control of the application, requiring immediate patching for on-premises deployments. [[Malware News](https://malware.news/t/cve-2026-2699-cve-2026-2701-progress-sharefile-storage-zones-controller-pre-auth-rce-chain/105772#post_1)]

## 📋 Policy & Industry News

**[NEW] Government official impersonation scams doubled in 2025**
The FBI's 2025 Internet Crime Report reveals that complaints involving scammers impersonating government officials nearly doubled from 17,300 in 2024 to over 32,500 in 2025, resulting in $797 million in losses. The surge is largely attributed to AI-driven voice and messaging tools that allow fraudsters to convincingly mimic authority figures at scale. [[Malware News](https://malware.news/t/government-official-impersonation-scam-complaints-doubled-in-2025-fbi-report-shows/105774#post_1)]

**[NEW] Stalkerware maker pcTattleTale sentenced**
The creator of the stalkerware app pcTattleTale, Bryan Fleming, has been sentenced to supervised release and a $5,000 fine after pleading guilty to manufacturing and selling surreptitious interception devices. This marks the first successful prosecution of a stalkerware maker since 2014, signaling a continued but potentially slow-moving legal effort against the surveillance-for-hire industry. [[CyberScoop](https://cyberscoop.com/pctattletale-stalkerware-maker-sentence-includes-fine-supervised-release/)]