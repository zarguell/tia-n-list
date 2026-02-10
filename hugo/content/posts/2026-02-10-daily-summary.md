---
title: Ivanti zero-days 🔥, Claude zero-click RCE 🤖, Fancy Bear attacks 🐻, DPRK LinkedIn theft 👤, Singapore telecom breaches 📱
date: 2026-02-10
tags: ["zero-day exploits","apt activity","state-sponsored attacks","remote code execution","social engineering","telecom security","malware campaigns","identity theft","government targets","ai vulnerabilities"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical zero-day vulnerabilities in Ivanti EPMM and Claude Desktop are being actively exploited by threat actors to deploy memory-based backdoors and achieve remote code execution without user interaction. Nation-state groups including Fancy Bear and Chinese hackers are conducting sophisticated espionage campaigns targeting government agencies and telecom infrastructure while North Korean operatives hijack LinkedIn identities for remote infiltration of tech companies.
---

# Daily Threat Intel Digest - 2026-02-10

## 🔴 Critical Threats & Active Exploitation

**[NEW] Ivanti EPMM Zero-Days Exploited to Deploy Dormant Backdoors**  
Attackers are actively exploiting two critical Ivanti Endpoint Manager Mobile vulnerabilities (CVE-2026-1281 and CVE-2026-1340) to plant stealthy backdoors that persist in memory without file traces. The malware at `/mifs/403.jsp` remains inactive until activated by a specific HTTP key, allowing attackers to maintain long-term access while evading traditional AV scans. Organizations must reboot systems after patching, as memory-based implants survive file-level remediation. Shadowserver reports 86 compromised instances globally, with attacks affecting government agencies including the Netherlands' judiciary and the European Commission. [[Hackers Exploit Ivanti EPMM](https://cyberpress.org/exploiting-ivanti-epmm/); [Shadowserver Data](https://cyberscoop.com/ivanti-zero-day-vulnerabilities-netherlands-european-commission-shadowserver/)]  

**[NEW] Zero-Click RCE in Claude Desktop Extensions Exposes 10,000+ Users**  
A CVSS 10/10 vulnerability in Claude Desktop Extensions enables remote code execution through manipulated Google Calendar events. Attackers can trigger RCE by embedding malicious commands in event descriptions, which Claude autonomously executes due to its design bridging local OS access. This affects over 50 extensions and 10,000+ users, enabling ransomware deployment or data theft without user interaction. No patch is available; users should isolate Claude from sensitive systems and disable automatic calendar actions. [[Claude Desktop Extensions Zero-Click RCE Flaw](https://cyberpress.org/claude-desktop-extensions-zero-click-rce-flaw/)]  

**[NEW] Fancy Bear Exploits Microsoft RTF Zero-Day for Espionage**  
Russia-linked APT28 (Fancy Bear) is leveraging a critical Microsoft RTF vulnerability to deliver backdoors and email stealers in a campaign targeting Central and Eastern Europe. The exploit chain delivers custom malware through malicious documents, enabling credential theft and lateral movement. Microsoft has not released a patch; defenders should block RTF attachments from unknown senders and monitor for anomalous Office processes. [[Fancy Bear Exploits Microsoft Zero-Day](https://gbhackers.com/microsoft-zero-day/)]  

**[NEW] Chinese Hackers Breach Singapore Telecoms via Rootkits and Zero-Days**  
Singapore's Cyber Security Agency disclosed an 11-month campaign where China-linked actors compromised four major telecom providers using rootkits and zero-day exploits. The attackers gained persistent access to network infrastructure, potentially enabling surveillance or traffic interception. This aligns with broader China-nexus edge-device targeting observed in 2025. Telecoms globally should review edge device logs for unknown implants and apply zero-trust network segmentation. [[Chinese Hackers Target Singapore Telecoms](https://gbhackers.com/singapore-telecoms-targeted/)]  

## 🎯 Threat Actor Activity & Campaigns

**[NEW] DPRK IT Workers Hijack LinkedIn Identities for Remote Infiltration**  
North Korean operatives are stealing real LinkedIn profiles to apply for high-paying remote roles in tech and cloud engineering. Once hired, they deploy Cobalt Strike beacons or exfiltrate data, causing $100M in crypto thefts across three firms in 2024. Techniques include AI voice changers for interviews and deepfake video tools. Companies must enforce live video verification and segment new hires with zero-trust policies. [[DPRK IT Workers Impersonate Professionals On LinkedIn](https://cyberpress.org/dprk-imposters-exploit-linkedin/)]  

**[NEW] Transparent Tribe Shifts to India's Startup Ecosystem**  
Pakistan-linked APT36 (Transparent Tribe) is targeting Indian cybersecurity startups with Crimson RAT delivered via ISO phishing emails. Lures reference startup founders (e.g., "MeetBisht.iso") to drop obfuscated .NET RATs that enable screen recording and file theft. This marks an expansion from traditional government/military targets to private sector tech firms. Defenders should block ISO attachments from unknown sources and hunt for Base64-encoded payloads in `C:\ProgramData`. [[Transparent Tribe Targets India’s Startup Ecosystem](https://cyberpress.org/transparent-tribe-targets-startups/)]  

**[NEW] Bloody Wolf Cybercrime Group Deploys NetSupport RAT**  
Financially motivated "Stan Ghouls" (Bloody Wolf) is spreading NetSupport RAT through phishing campaigns in Central Asia and Russia. The legitimate remote admin tool is abused for data theft and lateral movement. Manufacturing and finance sectors are primary targets. Block processes associated with NetSupport and quarantine downloads from suspicious domains. [[Bloody Wolf Cybercrime Group Uses NetSupport RAT to Breach Organizations](https://gbhackers.com/netsupport-rat-to-breach/)]  

**[NEW] Dark Web Markets Flood with High-Value Data Listings**  
Recent underground sales include alleged databases from AI music platform Suno (60M records), ASUS (order/serial data), and Air France (2M user records). An aggregated 80M credit card dump with CVVs and 2039 expirations is also advertised. These sales enable targeted attacks and fraud; organizations should monitor dark web for employee credentials and enforce MFA rotation. [[Alleged Suno Data, Card Dump, ASUS Records & Air France Access Sale](https://malware.news/t/alleged-suno-data-card-dump-asus-records-air-france-access-sale/103974#post_1)]  

## ⚠️ Vulnerabilities & Patches

**[NEW] JetBrains Addresses Multiple Critical Vulnerabilities**  
JetBrains released patches for Hub (<2025.3.119807), PyCharm (<2025.3.2), and YouTrack (<2025.3.119033) to prevent RCE and privilege escalation. Exploitation could allow attackers to compromise development environments. DevOps teams should update IDEs immediately and restrict network access to JetBrains services. [[JetBrains security advisory](https://malware.news/t/jetbrains-security-advisory-av26-105/103967#post_1)]  

**[NEW] Fortinet Fixes Critical SQL Injection in FortiClientEMS**  
CVE-2026-21643 (CVSS 9.8) allows unauthenticated RCE via improper SQL command neutralization in the FortiClientEMS web interface. While no in-the-wild exploitation is confirmed, pre-auth RCE flaws are routinely weaponized. Apply vendor patches and block external access to management interfaces. [[CVE-2026-21643: Critical SQL Injection in FortiClientEMS](https://malware.news/t/cve-2026-21643-critical-sql-injection-in-forticlientems/103970#post_1)]  

## 🛡️ Defense & Detection

**[NEW] Bulletproof Hosting Services Abuse Reputable ISP Networks**  
Cybercriminals exploit static hostnames from VMmanager templates (e.g., WIN-LIVFRVQFMKO) to host malware infrastructure across ISPs like Stark Industries and First Server. Over 11,000 exposed VMs facilitate ransomware and RAT operations. ISPsystem has updated templates to randomize hostnames, but legacy exposures persist. Block traffic from known hostnames and audit VM deployments. [[Cybercriminals Leverage Reputable ISP Networks via Bulletproof Hosting Services](https://cyberpress.org/bulletproof-hosting-abuses-isps/)]  

**[NEW] Moltbook Social Network Exposes AI Agents to Prompt Injection**  
Research into Moltbook (AI-only social platform) revealed rampant spam, scams, and indirect prompt injection risks. Bot API keys were leaked in a prior breach, enabling impersonation and malicious instruction delivery. Organizations should prohibit AI agents from accessing unvetted social platforms and monitor for anomalous command execution. [[I pretended to be an AI agent on Moltbook so you don’t have to](https://www.tenable.com/blog/undercover-on-moltbook)]  

## 📋 Policy & Industry News

**[NEW] Microsoft Exchange Online False Positives Disrupt Email**  
A misconfigured anti-spam rule (incident EX1227432) is quarantining legitimate emails as "High Confidence Phishing" since Feb 5. Affected organizations face communication delays; admins should review quarantine queues and submit false positives to Microsoft. No ETA for resolution is provided. [[Microsoft Exchange Online Erroneously Flags Legitimate Emails as Phishing](https://cyberpress.org/microsoft-exchange-emails-as-phishing/)]  

**[NEW] AI Chat App Misconfiguration Exposes 300M Messages**  
"Chat & Ask AI" leaked 300M messages from 25M users due to an open Firebase database rule. Personal queries (e.g., self-harm, hacking methods) were exposed. Developers must enforce least-privilege Firebase rules and encrypt sensitive data. [[AI Chat App Data Breach Exposes 300 Million Messages from 25 Million Users](https://cyberpress.org/ai-chat-app-data-breach-exposes/)]