---
title: Fake Zoom/Teramind surveillance 💻, ransomware surge 💣, North Korean IT scheme 🎭, critical vulnerabilities 🔧
date: 2026-02-24
tags: ["surveillance malware","ransomware","north korean actors","apt activity","voip vulnerabilities","browser security","supply chain attacks","mfa bypass","android malware","telecom vulnerabilities"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Attackers are deploying increasingly sophisticated surveillance tools and ransomware campaigns, with fake Zoom updates installing Teramind monitoring software while Play and CipherForce groups target engineering and tech sectors. State-sponsored North Korean actors continue infiltrating organizations through fake developer profiles, while critical vulnerabilities in Chrome, Grandstream VoIP phones, and HPE telecom systems create additional entry points for exploitation.
---

# Daily Threat Intel Digest - 2026-02-24

## 🔴 Critical Threats & Active Exploitation

**[NEW] Fake Zoom Update Installs Teramind Surveillance Software via Silent Drive-by**
Attackers are abusing a convincing fake Zoom meeting page at uswebzoomus[.]com to silently install a stealth Teramind surveillance agent, enabling full keystroke logging, screen capture, and data exfiltration. The page automatically triggers a countdown to download a malicious MSI without user consent after displaying deliberate network glitches and a fake Microsoft Store installation prompt. The agent installs with no visible UI and persists as dwm.exe under ProgramData, with a hardcoded server linking to the attacker-controlled Teramind instance ID 941afee582cc71135202939296679e229dd7cced. This campaign highlights the growing abuse of legitimate commercial monitoring tools for targeted surveillance, bypassing traditional antivirus detection [[Malwarebytes](https://www.malwarebytes.com/blog/scams/2026/02/fake-zoom-meeting-update-silently-installs-surveillance-software)]; [IOC SHA-256: 644ef9f5eea1d6a2bc39a62627ee3c7114a14e7050bafab8a76b9aa8069425fa](https://www.malwarebytes.com/blog/scams/2026/02/fake-zoom-meeting-update-silently-installs-surveillance-software).

**[NEW] Play Ransomware Claims Attack Against Atlantic Design Engineers**
The Play ransomware group publicly extorted Atlantic Design Engineers, a U.S. engineering firm, threatening to leak stolen data unless negotiations begin. While technical details remain limited, this continues Play's trend of targeting professional services and manufacturing sectors with data-theft extortion. Organizations should prioritize monitoring for early indicators of Play activity, including Cobalt Strike beacons and PowerShell Empire payloads commonly used in initial access [[DeXpose](https://www.dexpose.io/play-ransomware-strikes-atlantic-design-engineers/)].

**[UPDATE] CipherForce Ransomware Spikes Activity Across Multiple Sectors**
CipherForce has claimed three new victims in 48 hours: TektTree Inc. (U.S. tech consulting), HiringSteps.com (U.S. recruitment platform), and FindNear (Vietnamese location-tech firm). The group's rapid-fire extortion suggests automated reconnaissance and opportunistic targeting of internet-exposed services. Defenders should assume any unpatched public-facing applications are at risk and enforce network segmentation to limit lateral movement [[DeXpose](https://www.dexpose.io/cipherforce-launches-ransomware-attack-on-tekttree-inc/)]; [[DeXpose](https://www.dexpose.io/cipherforce-strikes-recruitment-platform-hiringsteps-com/)]; [[DeXpose](https://www.dexpose.io/cipherforce-ransomware-attack-on-findnear/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] North Korean IT Worker Scheme Earns $1.6M via Fake Developer Profiles**
North Korean state-sponsored actors have generated over $1.6 million since 2022 by posing as IT workers on platforms like GitLab, using AI-generated headshots and stolen identities to infiltrate crypto, finance, and AI firms. One cell led by Kil-Nam Kang in Beijing used 21 fake personas across five countries, exploiting freelance contracts to plant backdoors and exfiltrate code. GitLab's report confirms automated persona generation and npm package abuse (passport-google-auth-token) for initial access. Organizations must verify hires via live video checks and geolock development environments [[CyberPress](https://cyberpress.org/dprk-poses-as-it/)].

**[NEW] SURXRAT Android RAT Adds AI Module for Performance Sabotage**
A commercial Android RAT sold as SURXRAT V5 is incorporating a large language model (LLM) module downloaded from Hugging Face to degrade device performance during targeted gaming sessions (e.g., Free Fire). The RAT also includes ransomware-style screen locking, real-time keylogging, and Firebase C2 infrastructure. With over 1,300 operator accounts advertised on Telegram, this reflects increasing MaaS sophistication for mobile surveillance and financial crime [[Cyble](https://cyble.com/blog/surxrat-downloads-large-llm-module-from-hugging-face/)].

**[NEW] GrayCharlie Campaign Deploys NetSupport RAT via WordPress Compromise**
The GrayCharlie group (active since mid-2023) is injecting JavaScript into compromised WordPress sites to redirect users to fake browser updates or ClickFix prompts, ultimately installing NetSupport RAT. The group bypasses MFA by capturing session cookies from live login pages and uses MivoCloud/HZ Hosting infrastructure for C2. Recent targets include law firms and universities, with YARA and Sigma rules available for detection [[Recorded Future via CyberPress](https://cyberpress.org/graycharlie-spreads-netsupport-rat/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Google Rushes Emergency Chrome Patch for Three High-Severity Flaws**
Google fixed CVE-2026-3061 (Media OOB read), CVE-2026-3062 (Tint OOB read/write), and CVE-2026-3063 (DevTools implementation flaw) in Chrome 145.0.7632.116/117. The Tint flaw enables remote code execution via shader translation, while DevTools could allow sandbox bypass. Users should restart browsers to apply patches immediately [[CyberPress](https://cyberpress.org/google-rushes-emergency-chrome-update/)]; [[BleepingComputer](https://www.bleepingcomputer.com/news/security/google-releases-emergency-chrome-patch-addressing-three-major-security-flaws/)].

**[NEW] Grandstream GXP1600 VoIP Phones Hit with Unauthenticated RCE**
A stack buffer overflow (CVE-2026-2329, CVSS 9.3) in Grandstream GXP1600 series VoIP phones allows unauthenticated RCE with root privileges via /cgi-bin/api.values.Get. Metasploit modules are now available, enabling credential harvesting and SIP interception. Firmware 1.0.7.81 patches the flaw; organizations should update immediately and isolate VoIP VLANs [[Rapid7 via CyberPress](https://cyberpress.org/grandstream-gxp1600-rce-exploit/)].

**[NEW] HPE Telco Service Activator Vulnerable to Host Header Bypass**
CVE-2025-12543 (CVSS 9.6) in HPE Telco Service Activator permits remote attackers to bypass access controls via malicious Host headers in Undertow HTTP server. No workarounds exist; version 10.5.0 patches the issue. Telecom providers should prioritize updates to prevent unauthorized provisioning and data alteration [[HPE Bulletin via CyberPress](https://cyberpress.org/hpe-telco-activator-vulnerability-exposed/)].

**[NEW] Ruby RubitMQ Workers Face RCE via Unsafe JSON Deserialization**
CVE-2024-XXXX (CVSS 9.8) enables RCE in RubitMQ job workers using the Oj gem's default JSON parsing. Attackers inject malicious objects to execute shell commands via find -exec chains. Mitigations include switching Oj to safe mode and sandboxing workers [[CyberPress](https://cyberpress.org/critical-ruby-worker-deserialization-flaw-opens-door-to-complete-system-takeover/)].

## 🛡️ Defense & Detection

**[NEW] WhatsApp Introduces Optional Account Passwords for Enhanced Login Protection**
WhatsApp's beta adds 6-20 character passwords layered after SMS verification and 2FA, mitigating SIM swap attacks. Feature remains in development; enterprises should prepare user education to prevent weak passwords [[CyberPress](https://cyberpress.org/whatsapp-adds-optional-account-passwords/)].

**[NEW] Starkiller Phishing Framework Bypasses MFA via Reverse Proxy**
The Starkiller platform proxies legitimate login pages through headless Chrome instances, stealing session tokens and MFA codes in real-time. Advertised with 99.7% success rate, it includes URL masking and fake update templates. Defenders should implement behavioral analytics to detect atypical login flows [[Abnormal Security via CyberPress](https://cyberpress.org/starkiller-bypasses-mfa-protection/)].

## 📋 Policy & Industry News

**[NEW] Spain Arrests Anonymous Fénix Members for DDoS Attacks**
Spanish authorities arrested four suspected hacktivists from Anonymous Fénix for DDoS attacks on government sites post-Valencia floods. The group used Telegram for recruitment and X for propaganda, with courts seizing associated accounts [[BleepingComputer](https://www.bleepingcomputer.com/news/security/spain-arrests-suspected-anonymous-fenix-hacktivists-for-ddosing-govt-sites/)].

**[NEW] Mental Health Apps with 14.7M Downloads Riddled with Flaws**
Oversecured found 1,575 vulnerabilities across 10 Android mental health apps, including high-severity Intent parsing flaws and insecure local data storage. Many lack root detection and use weak RNG for tokens, risking exposure of therapy data [[BleepingComputer](https://www.bleepingcomputer.com/news/security/android-mental-health-apps-with-147m-installs-filled-with-security-flaws/)].