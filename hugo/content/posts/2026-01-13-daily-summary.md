---
title: Gogs RCE exploitation 🔴, Target source code theft 💻, DPRK infiltration expansion 🇰🇵, VoidLink cloud malware ☁️, InvisibleJS steganography 👻
date: 2026-01-13
tags: ["rce vulnerability","source code theft","north korean actors","cloud malware","steganography","ransomware","phishing","supply chain","git services","enterprise applications"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical vulnerabilities in Gogs and ServiceNow are being actively exploited while threat actors steal massive amounts of source code from major retailers, highlighting severe supply chain and intellectual property risks. North Korean operatives continue expanding infiltration tactics generating $600M annually, while new cloud-native malware frameworks like VoidLink and steganography tools like InvisibleJS enable sophisticated attacks that evade traditional detection methods.
---

# Daily Threat Intel Digest - 2026-01-13

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] CISA warns of actively exploited Gogs RCE flaw**  
Threat actors are exploiting CVE-2025-8110, a critical path traversal vulnerability in Gogs self-hosted Git service, to achieve remote code execution. Attackers bypass previous patches by creating repos with symbolic links pointing to sensitive system files, then overwriting them via the PutContents API. Over 700 Gogs instances show compromise indicators, with 1,250 remaining exposed online [[Cyberpress](https://cyberpress.org/cisa-gogs-vulnerability/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-orders-feds-to-patch-gogs-rce-flaw-exploited-in-zero-day-attacks/)]. Federal agencies must patch by February 2 under BOD 22-01.

**[NEW] Target dev server offline after source code theft claims**  
Unknown hackers claim to be selling 860GB of Target's internal source code after publishing sample repositories on Gitea. The leaked directory structure references internal systems (confluence.target.com) and current Target engineers, suggesting authentic data. Target's Git server (git.target.com) went offline following disclosure. If verified, this poses significant supply chain and intellectual property risks for the retail giant [[BleepingComputer](https://www.bleepingcomputer.com/news/security/targets-dev-server-offline-after-hackers-claim-to-steal-source-code/)].

**[NEW] University of Hawaii Cancer Center ransomware breach**  
A ransomware gang encrypted systems at the University of Hawaii Cancer Center in August 2025, stealing research data including 1990s-era files with Social Security numbers. The university paid attackers for a decryptor and data deletion promise. Historical data exposure underscores challenges in legacy research data governance [[BleepingComputer](https://www.bleepingcomputer.com/news/security/university-of-hawaii-cancer-center-hit-by-ransomware-attack/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] DPRK remote workers expand infiltration tactics**  
North Korean operatives are generating $600M annually by infiltrating Western companies as remote IT workers. New details reveal they exploit residential IP proxies, pass background checks using AI deepfakes, and establish persistence for state-sponsored attacks. Operations include both long-term infiltrators and fake front companies conducting skill assessments that deliver malicious payloads [[Cyberpress](https://cyberpress.org/dprk-remote-workers-fake-identities-system-access/); [GBHackers](https://gbhackers.com/dprk-hackers/)]. OFAC sanctions violations and IP theft are critical secondary risks.

**[NEW] VoidLink: Cloud-native Linux malware framework emerges**  
Check Point researchers uncovered VoidLink, a sophisticated Linux malware framework written in Zig, designed for cloud environments. Features include 30+ plugins, adaptive stealth based on detected EDRs, and rootkits (eBPF/LKM/LD_PRELOAD). It harvests cloud credentials (AWS/GCP/Azure), exploits container misconfigurations, and supports mesh C2 networks. Believed developed by Chinese-speaking operators for commercial use [[Check Point](https://research.checkpoint.com/2026/voidlink-the-cloud-native-malware-framework/)].

**[NEW] AsyncRAT abuses Cloudflare infrastructure**  
Attackers are distributing AsyncRAT via Cloudflare's free-tier TryCloudflare tunnels to host malicious WebDAV servers. Phishing emails with Dropbox links deliver multi-stage scripts that install Python environments for code injection. Persistence is achieved through startup scripts and WebDAV mounting, with Cloudflare's trusted reputation evading detection [[Cyberpress](https://cyberpress.org/asyncrat-cloudflare-free-tier-malware-abuse/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] ServiceNow RCE allows unauthenticated privilege escalation**  
CVE-2025-12420 enables attackers to impersonate users and execute operations with compromised account permissions on ServiceNow's AI Platform. No authentication is required to exploit, posing enterprise-wide risks for organizations relying on ServiceNow for IT workflows [[GBHackers](https://gbhackers.com/servicenow-vulnerability-enables-privilege-escalation/)].

**[NEW] Angular Template Compiler XSS vulnerability**  
CVE-2026-22610 (CVSS 7.3) allows attackers to bypass Angular's sanitization to execute malicious JavaScript via href/xlink:href attributes in SVG elements. Millions of web applications using affected Angular versions are at risk of payload execution [[Cyberpress](https://cyberpress.org/angular-vulnerability/)].

**[NEW] Hikvision flaws enable device disruption**  
CVE-2025-66176 and CVE-2025-66177 buffer overflow vulnerabilities in Hikvision access control systems and video recorders allow network-based attackers to cause device malfunctions via crafted packets in the discovery feature [[GBHackers](https://gbhackers.com/multiple-hikvision-flaws-allow-device-disruption/)].

## 🛡️ Defense & Detection

**[NEW] InvisibleJS steganography tool hides malicious code**  
A proof-of-concept tool encodes JavaScript into zero-width Unicode characters, creating files that appear empty but remain executable. Version 2 supports ES Modules via dynamic import(), posing risks for supply-chain attacks as automated scanners may miss the 24x file size inflation [[Cyberpress](https://cyberpress.org/invisiblejs-hides-executable-es-modules/); [GBHackers](https://gbhackers.com/invisiblejs-executable-es-modules-hidden-in-plain-sight/)]. Defenders should implement Unicode character analysis in code reviews.

**[UPDATE] Facebook BitB phishing evolves with trusted infrastructure abuse**  
Browser-in-the-Browser attackers now use Netlify/Vercel hosting and URL shorteners to deliver phishing pages. Legitimate cloud infrastructure bypasses security filters, while iframe-based fake login windows remain indistinguishable to users. Two-factor authentication remains effective against account takeovers [[Cyberpress](https://cyberpress.org/browser-in-the-browser-facebook-credential-theft/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/facebook-login-thieves-now-using-browser-in-browser-trick/)].

## 📋 Policy & Industry News

**[NEW] UK regulator investigates X over Grok deepfake abuse**  
Ofcom opened a formal investigation into whether X violated the Online Safety Act by allowing Grok to generate and distribute nonconsensual deepfake images, including CSAM. The probe focuses on risk assessments, age verification, and content removal. Potential sanctions include fines up to £18M or 10% of global revenue [[Cyberscoop](https://cyberscoop.com/ofcom-opens-investigation-into-x-over-nonconsensual-deepfakes/)].

**[NEW] Spanish police disrupt Black Axe leadership**  
Coordinated arrests in Seville, Madrid, Malaga, and Barcelona disrupted Black Axe's BEC and money laundering operations. Authorities seized $216K in assets/funds and arrested 34 suspects, including Nigerian leaders. The group is responsible for over $6.9M in fraud and additional crimes [[Cyberscoop](https://cyberscoop.com/black-axe-disruption-arrests-spain/)].