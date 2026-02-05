---
title: Amaranth-Dragon WinRAR espionage 🐉, VMware ESXi ransomware zero-day 💥, DNS TXT ClickFix attacks 📝, AI-driven AWS compromises 🤖
date: 2026-02-05
tags: ["apt activity","ransomware","zero-day exploits","espionage","dns abuse","cloud security","ai attacks","vulnerabilities","malware campaigns"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: China-linked APT-41 exploits critical WinRAR flaws to deliver persistent espionage malware across Southeast Asian government targets while ransomware operators actively weaponize VMware ESXi zero-days for mass VM encryption. Attackers are increasingly abusing legitimate services like DNS TXT records for PowerShell command delivery and leveraging AI to rapidly compromise AWS accounts, highlighting the need for immediate patch management and enhanced monitoring of protocol abuse.
---

# Daily Threat Intel Digest - 2026-02-05

## 🔴 Critical Threats & Active Exploitation

**[NEW] Amaranth-Dragon exploits WinRAR flaw for persistent espionage in Southeast Asia**  
China-linked APT-41 (Amaranth-Dragon) is weaponizing CVE-2025-8088, a critical path traversal flaw in WinRAR, to drop persistent payloads into Windows Startup folders. The group targets government and law enforcement agencies across Indonesia, Philippines, Thailand, and Singapore using geopolitically themed phishing lures (e.g., salary updates) hosted on Dropbox. Successful exploitation delivers Havoc C2 framework shellcode or TGAmaranth RAT, with C2 infrastructure behind Cloudflare geo-blocking to limit spread. Update WinRAR to v7.20 immediately, block observed Dropbox IOCs, and hunt for Amaranth Loader hashes [[CyberPress](https://cyberpress.org/amaranth-dragon-exploits-winrar-vulnerability/); [GBHackers](https://gbhackers.com/amaranth-dragon/)].

**[NEW] CISA confirms VMware ESXi zero-day exploited in ransomware campaigns**  
CVE-2025-22225, an arbitrary memory write flaw allowing VMX sandbox escape and host-level code execution, is actively weaponized by ransomware operators. Attackers with VMX privileges can overwrite kernel memory to compromise ESXi hosts, encrypting multiple VMs simultaneously. CISA added the flaw to its KEV catalog with a March 25 federal patch deadline. Isolate unpatched ESXi hosts, apply VMware patches immediately, and monitor VMX process anomalies [[CyberPress](https://cyberpress.org/exploited-vmware-esxi-zero-day/); [GBHackers](https://gbhackers.com/cisa-confirms-vmware-esxi-0-day-vulnerability/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Cisco Meeting Management flaw enables authenticated RCE as root**  
CVE-2026-20098 (CVSS 8.8) allows attackers with video operator privileges to upload arbitrary files via the Certificate Management component, leading to root-level command execution. No workarounds exist; upgrade to v3.12.1 MR immediately and restrict web interface access to trusted networks [[CyberPress](https://cyberpress.org/cisco-meeting-management-vulnerability/); [GBHackers](https://gbhackers.com/cisco-warns-of-meeting-management-flaw/); [Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/cisco-security-advisory-av26-087)].

**[NEW] DNS TXT records abused in ClickFix campaigns to hide PowerShell commands**  
KongTuke attackers encode malicious PowerShell commands in DNS TXT responses, bypassing network defenses. Queries to attacker-controlled domains retrieve Base64-encoded scripts that disable Windows Defender, drop ransomware, or steal data. Block suspicious DNS TXT queries, enable AMSI/ScribbleBlock logging, and monitor for oversized TXT responses [[CyberPress](https://cyberpress.org/dns-txt-exploited-for-powershell/); [GBHackers](https://gbhackers.com/dns-txt-records/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Stan Ghouls expands NetSupport RAT attacks against Uzbekistan finance**  
The financial-motivated group (aka Bloody Wolf) infected ~60 organizations in Uzbekistan's manufacturing, finance, and IT sectors using Uzbek-language phishing PDFs. Attackers switched from STRRAT to NetSupport RAT, delivered via custom Java loaders that enforce persistence via startup scripts, registry keys, and scheduled tasks. New domains (e.g., mysoliq-uz[.]com) support the campaign, with potential IoT expansion suggested by Mirai samples on linked infrastructure [[Malware.News](https://malware.news/t/stan-ghouls-targeting-russia-and-uzbekistan-with-netsupport-rat/103869#post_1)].

**[NEW] SystemBC botnet hijacks 10,000 devices for DDoS and ransomware precursors**  
A resilient botnet controls 10,340+ IPs, primarily hosted providers (AS19871, AS46606). Compromised government sites (e.g., Vietnam's Phutho.duchop[.]gov[.]vn) and WordPress scanning activity indicate lateral movement. Linux variants evade detection via Perl-based payloads, with C2 on bulletproof hosts. Block C2 IPs (36.255.98[.]159), monitor hosting ASNs, and hunt for SafeObject droppers [[CyberPress](https://cyberpress.org/systembc-botnet-hijacks-10000-devices/)].

**[NEW] Rublevka Team generates $10M via automated crypto-draining schemes**  
A Russian "traffer team" operates a service-based ecosystem draining Solana wallets via spoofed pages (e.g., Phantom, Bitget). Over 240,000 successful drains recorded, with transactions ranging from $0.16 to $20,000. Tools include Telegram bots for landing page generation and DDoS protection, targeting low-cost chains to maximize profit [[Malware.News](https://malware.news/t/rublevka-team-anatomy-of-a-russian-crypto-drainer-operation/103854#post_1)].

## 🛡️ Defense & Detection

**[NEW] Microsoft integrates Sysmon natively into Windows 11**  
Windows 11 Insider Build 26300.7733 adds Sysmon as an optional feature, enabling advanced process/network logging without standalone deployment. Admins must uninstall existing Sysmon instances before enabling via `DISM /Online /Enable-Feature /FeatureName:Sysmon`. This enhances SOC visibility with native support for custom XML configurations [[CyberPress](https://cyberpress.org/microsoft-to-integrate-sysmon-threat-detection-natively-into-windows-11/); [GBHackers](https://gbhackers.com/microsoft-to-integrate-sysmon-threat-detection/)].

## 📋 Policy & Industry News

**[NEW] AI-driven attacks compromise AWS accounts in under 10 minutes**  
Threat actors used LLMs to rapidly escalate from exposed S3 credentials to full admin control via Lambda code injection. Attackers (with hints at Serbian origins) exploited Bedrock, launched p4d.24xlarge GPU instances, and exfiltrated Secrets Manager data. Enforce least privilege Lambda roles, block UpdateFunctionCode abuse, and monitor Bedrock invocation anomalies [[CyberPress](https://cyberpress.org/ai-accelerates-aws-takeovers/)].