---
title: Apple zero-day exploits 🍎, BeyondTrust RCE attacks 🔧, WordPress plugin vulnerabilities 📝, Muddled Libra VMware attacks ☁️, State-sponsored AI weaponization 🤖
date: 2026-02-13
tags: ["zero-day exploits","active exploitation","ransomware","apt groups","cloud security","supply chain","web vulnerabilities","ai threats","credential theft","vmware attacks"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical zero-day vulnerabilities in Apple iOS and BeyondTrust systems are being actively exploited, while widespread WordPress plugin flaws expose over 800,000 websites to complete compromise. State-sponsored threat actors are leveraging AI tools for cyberespionage and sophisticated ransomware groups like Muddled Libra are deploying rogue virtual machines to bypass enterprise defenses.
---

# Daily Threat Intel Digest - 2026-02-13

## 🔴 Critical Threats & Active Exploitation

**[NEW] Apple discloses first actively exploited zero-day of 2026**  
Apple fixed CVE-2026-20700, a memory corruption flaw in dyld exploited in highly targeted attacks against specific individuals via iOS versions before 26.3. The vulnerability enables arbitrary code execution with memory write capabilities and was discovered by Google Threat Intelligence Group. CISA added this to its KEV catalog, marking the first Apple zero-day actively exploited this year. Updates are available in iOS 26.3 and iPadOS 26.3, which also patch 37 additional vulnerabilities [[CyberScoop](https://cyberscoop.com/apple-zero-day-vulnerability-cve-2026-20700/)].  

**[NEW] BeyondTrust RCE flaw under active exploitation (CVE-2026-1731)**  
A critical pre-authentication remote code execution vulnerability affecting BeyondTrust Remote Support (RS) ≤25.3.1 and Privileged Remote Access (PRA) ≤24.3.4 carries a CVSS v4 score of 9.9. Unauthenticated attackers can execute arbitrary OS commands via crafted client requests, leading to full system compromise. With ~11,000 internet-facing instances at risk and confirmed exploitation, manual patching is required for on-premises deployments while SaaS environments are auto-patched [[CyberPress](https://cyberpress.org/patch-immediately-beyondtrust/); [GBHackers](https://gbhackers.com/beyondtrust-rce-vulnerability-under-active-exploitation/)].  

**[NEW] Critical WordPress backup plugin flaw exposes 800K+ sites to RCE**  
WPvivid Backup Plugin versions ≤0.9.123 suffer an unauthenticated arbitrary file-upload vulnerability (CVE-2026-1357, CVSS 9.8) enabling full site takeover via webshells. Attackers exploit poor RSA decryption handling and path sanitization when the "receive key" feature is enabled (off by default). Over 800,000 installations are affected. Patched in version 0.9.124; Wordfence firewall rules are available [[CyberPress](https://cyberpress.org/wordpress-backup-plugin-exploit/)].  

**[NEW] Microsoft Configuration Manager SQL injection exploited in the wild**  
CISA added a critical SQL injection vulnerability in Microsoft Configuration Manager to its KEV catalog, confirming active exploitation. The flaw enables command execution and poses immediate risk to enterprise management platforms. Vulnerable systems require urgent patching though specific CVE details remain undisclosed [[GBHackers](https://gbhackers.com/cisa-issues-urgent-warning-on-microsoft-configuration-manager/)].  

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Muddled Libra uses rogue VMs to compromise VMware vSphere**  
The financially motivated Muddled Libra group (Scattered Spider) deployed rogue VMs within VMware vSphere environments to evade endpoint detection and steal credentials. Attackers powered down virtualized domain controllers, exfiltrated NTDS.dit files, and used living-off-the-land tools like ADRecon and PsExec. Persistence was maintained via Chisel tunneling and data exfiltrated to cloud services like Dropbox [[CyberPress](https://cyberpress.org/rogue-vm-targets-vmware-vsphere/)].  

**[NEW] Fraudulent Olympics merchandise shops target global fans**  
Nearly 20 lookalike domains impersonating the official Milano Cortina 2026 store have emerged in the past week, using polished storefronts and discounted "Tina the stoat" plush toys (officially sold out) to steal payment details and personal information. Scam sites use .top/.shop TLDs and typosquatting (e.g., winter0lympicsstore). Victims span Ireland, US, Italy, China, and Czech Republic [[Malwarebytes](https://malware.news/t/fake-shops-target-winter-olympics-2026-fans/104095#post_1)].  

## ⚠️ Vulnerabilities & Patches

**[NEW] Malicious NPM package "duer-js" delivers Bada Stealer**  
A typosquatting package with 528+ downloads deploys Bada Stealer via obfuscated JavaScript. It steals Discord tokens, browser credentials (Chrome/Edge/Brave), crypto wallets (Exodus/MetaMask), and Steam data, exfiltrating via Discord webhooks and Gofile.io. A secondary payload hijacks Discord's Electron process to intercept logins and 2FA codes. Users should revoke compromised credentials and scan with JFrog Xray [[CyberPress](https://cyberpress.org/duer-js-delivers-bada-stealer/)].  

**[NEW] OysterLoader advances evasion tactics for Rhysida ransomware**  
The C++-based OysterLoader (aka Broomstick/CleanUp) employs advanced obfuscation and DLL hijacking to deliver Rhysida ransomware. Distributed via malvertising and trojanized installers for PuTTY, WinSCP, and Google Authenticator, it exploits legitimate tools to bypass detection [[GBHackers](https://gbhackers.com/oysterloader-evasion-tactics/)].  

## 📋 Policy & Industry News

**[NEW] UK government reverses mandatory digital ID plan**  
After public backlash and a 3M-signature petition, the UK scrapped mandatory "Brit Card" digital IDs for workers, citing civil liberties concerns. Voluntary programs will proceed, but centralized biometric databases remain controversial following breaches in Estonia (280K records, 2021) and India (815M records, 2023) [[Panda Security](https://malware.news/t/uk-s-digital-id-u-turn-what-it-means-for-security/104094#post_1)].  

**[NEW] Proofpoint acquires Acuvity to secure agentic AI**  
Proofpoint acquired AI security startup Acuvity to address risks from enterprise AI deployments. Acuvity’s platform monitors interactions with external AI services and secures custom models amid rising prompt injection threats. Terms were undisclosed, but Acuvity’s team will join Proofpoint [[CyberScoop](https://cyberscoop.com/proofpoint-acuvity-deal-agentic-ai-security/)].  

## ⚡ Quick Hits

- **Google reports state hackers using Gemini AI**: North Korean, Chinese, Russian, and Iranian APTs leverage Gemini for reconnaissance, malware generation, and social engineering [[Cyberwarzone](https://malware.news/t/ai-weaponization-state-hackers-using-google-gemini-for-espionage-and-malware-generation/104090#post_1); [CyberScoop](https://cyberscoop.com/state-hackers-using-gemini-google-ai/)].  
- **Chrome 145 patches 11 flaws**: Google fixed vulnerabilities across multiple components, though specifics remain minimal [[SecurityWeek](https://www.securityweek.com/chrome-145-patches-11-vulnerabilities/)].  
- **XWorm RAT campaign uses old Excel exploit**: Phishing emails deliver CVE-2018-0802 exploits to deploy XWorm RAT, enabling data theft and ransomware execution [[GBHackers](https://gbhackers.com/new-xworm-rat-campaign/)].