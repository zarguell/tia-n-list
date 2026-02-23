---
title: BeyondTrust RCE exploits 🔥, OAuth token theft 🎭, North Korean crypto attacks 💰, PromptSpy AI malware 🤖, Hospitality ransomware 🏨
date: 2026-02-23
tags: ["rce exploitation","oauth attacks","north korean actors","android malware","ransomware","semiconductor attacks","critical infrastructure","mfa bypass","ai security","hospitality sector"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Attackers are actively exploiting BeyondTrust RCE vulnerabilities to deploy web shells and RATs across financial, healthcare, and tech organizations while North Korean operators intensify crypto-sector attacks following major exchange breaches. Sophisticated OAuth token theft campaigns bypass MFA in Microsoft 365 and novel PromptSpy malware abuses Google Gemini for Android persistence, as the hospitality sector faces continued ransomware targeting.
---

# Daily Threat Intel Digest - February 23, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] BeyondTrust RCE actively exploited with VShell and SparkRAT payloads**  
Attackers are exploiting CVE-2026-1731, a critical pre-authentication RCE flaw in BeyondTrust Remote Support and Privileged Remote Access products, by injecting commands via WebSocket handshake manipulation. Unit 42 confirms widespread deployment of web shells and RATs, with over 16,400 exposed instances vulnerable globally. Victims include financial, healthcare, and tech organizations across the US, France, and Germany. [[Cyberpress](https://cyberpress.org/beyondtrust-flaw-fuels-rats/)]

**[NEW] CISA adds Roundcube flaws to KEV amid active exploitation**  
Two critical Roundcube Webmail vulnerabilities (CVE-2025-49113, CVE-2025-68461) are being actively exploited after CISA added them to the KEV catalog. The popular open-source webmail client faces heightened risks as attackers target unpatched instances globally. [[GBHackers](https://gbhackers.com/cisa-exploited-roundcube-vulnerabilities/)]

**[NEW] OAuth token theft bypasses MFA in Microsoft 365 attacks**  
Attackers hijack OAuth 2.0 Device Authorization flows to steal persistent access tokens from Microsoft 365 accounts, bypassing MFA and credentials. The campaign targets tech/manufacturing/financial sectors with phishing lures mimicking payment confirmations and document shares, granting full access to emails, files, and admin functions until tokens are revoked. [[Cyberpress](https://cyberpress.org/microsoft-365-oauth-hijacking/)]

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] North Korean crypto attacks accelerate post-Bybit breach**  
DPRK-linked operators have intensified crypto-sector attacks one year after the $1.46B Bybit heist, with activity accelerating rather than slowing. Attribution remains consistent with Lazarus-group tactics, focusing on exchange compromises and DeFi protocol exploits. [[GBHackers](https://gbhackers.com/bybit-breach/)]

**[NEW] Japanese semiconductor giant hit by ransomware**  
Advantest Corporation, a major semiconductor test equipment supplier, confirmed a February 15 ransomware attack disrupting multiple systems. The incident raises supply chain concerns for global tech manufacturers dependent on Advantest's testing infrastructure. [[GBHackers](https://gbhackers.com/japanese-semiconductor-supplier-ransomware/); [Check Point](https://malware.news/t/23rd-february-threat-intelligence-report/104320#post_1)]

**[NEW] PromptSpy malware pioneers AI-driven persistence on Android**  
First-of-its-kind Android malware abuses Google's Gemini to dynamically automate UI interactions for persistence. By sending screen XML dumps to Gemini with natural-language prompts, attackers bypass traditional anti-uninstall techniques across device variants. Deployed via banking trojan droppers targeting Argentina, it includes VNC remote access and credential theft. [[Cyberpress](https://cyberpress.org/promptspy-uses-google-gemini/)]

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical flaws in VS Code extensions expose 128M users**  
Four popular VS Code extensions (CVE-2025-65715 to -65717) reveal IDEs as weak points in supply chain security, with flaws enabling arbitrary code execution and sensitive data exposure. Developers storing API keys/configs in workspaces are at immediate risk. [[GBHackers](https://gbhackers.com/128m-vs-code-extension-flaws/)]

**[NEW] jsPDF library vulnerable to object injection**  
CVE-2026-25755 in the widely used jsPDF JavaScript library allows attackers to perform PDF Object Injection via the addJS method, affecting countless web applications that generate dynamic PDFs. [[GBHackers](https://gbhackers.com/jspdf-millions-developers-exposed/)]

## 🛡️ Defense & Detection

**[NEW] pfSense hardening guide addresses firewall exploitation risks**  
A comprehensive CIS-aligned guide for pfSense deployments mitigates recent firewall-focused attacks, emphasizing management plane segregation, MFA enforcement, and egress filtering. Critical controls include disabling WAN WebGUI exposure, encrypting HA sync traffic, and centralized logging. [[SOCFortress](https://socfortress.medium.com/pfsense-secure-provisioning-hardening-guide-dfbd3fdcc89b?source=rss-36613248f635------2)]

## 📋 Policy & Industry News

**[NEW] NATO allies declare hospital cyberattacks as "acts of war"**  
Public polling in key NATO countries shows broad support for classifying hospital cyberattacks as acts of war, though formal policy responses remain restrained. This highlights growing pressure for unified retaliation frameworks against critical infrastructure targeting. [[DataBreaches.Net](https://malware.news/t/top-nato-allies-believe-cyberattacks-on-hospitals-are-an-act-of-war-theyre-still-struggling-to-fight-back/104311#post_1)]

**[NEW] Hospitality sector surges as ransomware target**  
Choice Hotels disclosed a January 14 social engineering breach, continuing a trend of hospitality attacks. Concurrent Booking.com phishing campaigns leverage IDN homographs and Cloudflare CAPTCHA to harvest credentials from hotel partners and guests. [[DataBreaches.Net](https://malware.news/t/the-hospitality-sector-continues-to-be-lucrative-targets/104310#post_1); [Check Point](https://malware.news/t/23rd-february-threat-intelligence-report/104320#post_1)]