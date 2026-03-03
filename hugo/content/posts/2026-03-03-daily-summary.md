---
title: UH Cancer ransomware breach 🏥, Android zero-day CVE-2026-21385 📱, RESURGE Ivanti malware 🔄, Iranian cyber counteroffensive ⚔️, Aeternum blockchain C2 botnet ⛓️
date: 2026-03-03
tags: ["ransomware","zero-day exploitation","malware persistence","apt activity","blockchain c2","oauth abuse","vulnerability exploitation","academic sector","mobile security","supply chain attacks"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: University of Hawaii Cancer Center ransomware breach exposed 1.2 million records with attackers receiving payment while Iranian threat actors prepare retaliatory cyberattacks following regional strikes. Android devices face active exploitation through Qualcomm display zero-day and RESURGE malware persists on Ivanti systems despite patches, while Aeternum demonstrates blockchain-based C2 infrastructure that evades traditional takedowns.
---

# Daily Threat Intel Digest - 2026-03-03

## 🔴 Critical Threats & Active Exploitation
**[NEW] UH Cancer Center breach exposes 1.2M after ransomware payment**  
Attackers stole data of 1.2 million individuals in an August 2025 ransomware attack on the University of Hawaii Cancer Center’s Epidemiology Division, with UH confirming payment to obtain decryption tools and data destruction assurances. Compromised data includes SSNs from 1998-2000 driver's license/voter records and health information from cancer studies, though clinical operations remained unaffected. This breach pattern mirrors UH's 2023 incident where ransom payments were made to prevent data leaks, highlighting persistent targeting of academic research institutions [[BleepingComputer](https://www.bleepingcomputer.com/news/security/university-of-hawaii-cancer-center-ransomware-attack-affects-nearly-12-million-people/)].  

**[UPDATE] Android zero-day (CVE-2026-21385) actively exploited in Qualcomm display flaw**  
Google’s March 2026 security bulletin patches 129 vulnerabilities—including an actively exploited Qualcomm display zero-day (CVE-2026-21385) enabling memory corruption for RCE via integer overflow. The flaw affects 235 Qualcomm chipsets and has been observed in limited, targeted attacks since December 2025. Alongside 10 critical RCE/EoP flaws in System/Framework components, this marks Android’s highest single-month patch volume since 2018. Android device users should prioritize updates, though vendor rollout delays may create exploitation windows [[BleepingComputer](https://www.bleepingcomputer.com/news/security/google-patches-android-zero-day-actively-exploited-in-attacks/); [CyberPress](https://cyberpress.org/android-security-update-fixes-129-vulnerabilities/); [CyberScoop](https://www.cyberscoop.com/android-security-update-march-2026/)].  

**[UPDATE] RESURGE malware persists despite Ivanti patches via boot disk infection**  
CISA warns RESURGE malware—a SPAWNCHIMERA variant—exploits Ivanti Connect Secure CVE-2025-0282 (stack-based buffer overflow) to deploy web shells, harvest credentials, and achieve persistence by modifying coreboot images. The malware survives reboots, complicating remediation. Despite patches, organizations must perform factory resets using external clean images and reset domain credentials (e.g., krbtgt twice). YARA/SIGMA rules are available for detection [[CyberPress](https://cyberpress.org/resurge-malware-targets-ivanti-vulnerabilities/); [CISA](https://www.cisa.gov/news-events/alerts/2025/03/28/cisa-releases-malware-analysis-report-resurge-malware-associated-ivanti-connect-secure)].  

## 🎯 Threat Actor Activity & Campaigns  
**[UPDATE] Iran-linked actors ramp up for cyber counteroffensive post-Epic Fury**  
Following US-Israeli strikes killing Iran’s leadership, threat groups like HANDALA and Cotton Sandstorm are gearing for retaliatory attacks targeting critical infrastructure. Expected TTPs include DDoS, botnet activity, and destructive malware exploiting known vulnerabilities (e.g., CVE-2021-44228). Organizations should heighten monitoring, enforce MFA, and audit third-party risks in energy/transportation sectors [[Tenable](https://www.tenable.com/blog/operation-epic-fury-potential-iranian-cyber-counteroffensive-operations); [Talos](https://blog.talosintelligence.com/talos-developing-situation-in-the-middle-east/); [Unit 42](https://unit42.paloaltonetworks.com/iranian-cyberattacks-2026/); [Recorded Future](https://www.recordedfuture.com/blog/ongoing-iran-conflict-what-you-need-to-know)].  

**[NEW] Aeternum C2 uses Polygon blockchain for unkillable botnet infrastructure**  
Aeternum botnet eliminates centralization by storing commands on Polygon blockchain smart contracts, queried via public RPC endpoints. This prevents takedowns, with $1 in MATIC funding 100+ transactions. Operators deploy varied payloads (clippers, RATs) and include anti-VM/antivirus checks. Defenders must shift focus from infrastructure takedowns to network-level detection of RPC queries and contract interaction patterns [[CyberPress](https://cyberpress.org/aeternum-c2-evasion-exposed/)].  

**[NEW] OAuth redirection abuse bypasses phishing defenses via silent flows**  
Attackers exploit OAuth error redirects (e.g., invalid scope + prompt=none) to route victims from Entra ID/Google to malicious domains, delivering malware like PowerShell-side-loaded payloads. Techniques include encoding emails in state parameters and abusing legitimate redirect URIs. Mitigations include restricting app consent, reviewing redirect URIs, and monitoring URLs with scope=invalid [[Microsoft](https://www.microsoft.com/en-us/security/blog/2026/03/02/oauth-redirection-abuse-enables-phishing-malware-delivery/)].  

## ⚠️ Vulnerabilities & Patches  
**[NEW] Angular XSS (CVE-2026-27970) enables code injection via translation files**  
A high-severity XSS flaw in Angular’s i18n pipeline allows malicious script injection through compromised .xliff/.xtb translation files. Attackers can steal cookies/localStorage or deface apps, with enterprises in finance/e-commerce most at risk. Patch to Angular 19.2.19+, 20.3.17+, or 21.1.6+; interim mitigations include CSP headers (script-src 'self') and manual translation vetting [[CyberPress](https://cyberpress.org/severe-xss-vulnerability/); [GBHackers](https://gbhackers.com/angular-i18n-flaw/); [GitHub](https://github.com/angular/angular/security/advisories/GHSA-prjf-86w9-mfqv)].  

**[NEW] Chrome Gemini flaw (CVE-2026-0628) let extensions hijack camera/mic**  
A patched vulnerability allowed malicious Chrome extensions to abuse the Gemini Live side panel’s elevated privileges via declarativeNetRequests API, enabling camera/mic access, file theft, and screenshots. Users should update Chrome (patched Jan 2026) and audit extensions. This underscores risks in agentic AI integrations [[CyberPress](https://cyberpress.org/critical-flaw-in-google-chrome-gemini/); [GBHackers](https://gbhackers.com/chrome-gemini-vulnerability/)].  

## 🛡️ Defense & Detection  
**[NEW] Pixel Perfect extension analysis reveals CSP bypass via 1x1 GIF C2**  
The once-legitimate QuickLens extension was weaponized post-acquisition (v5.8+) to strip CSP headers via declarativeNetRequest rules, enabling silent script injection through 1x1 GIF onload attributes. Detection requires monitoring extension updates and CSP header modifications, with 7,000 users affected [[CyberPress](https://cyberpress.org/pixel-perfect-exploit-enables-injection/)].  

## ⚡ Quick Hits  
- **Android patches**: 129 flaws fixed across 2026-03-01/05 patch levels, including 10 critical System/Framework RCE/EoP bugs [[BleepingComputer](https://www.bleepingcomputer.com/news/security/google-patches-android-zero-day-actively-exploited-in-attacks/)].  
- **Chrome Gemini C2**: Malicious PWA apps proxy traffic through victims’ browsers to intercept OTPs and scan networks [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-google-security-site-uses-pwa-app-to-steal-credentials-mfa-codes/)].  
- **Veeam advisory**: Kasten for Kubernetes vulnerabilities patched across multiple versions [[Canadian Centre](https://cyber.gc.ca/en/alerts-advisories/veeam-security-advisory-av26-188)].