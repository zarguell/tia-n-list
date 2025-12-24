---
title: Operation PCPcat server compromises 🔴, Evasive Panda DNS attacks 🎯, Critical enterprise vulnerabilities ⚠️, New EDR-bypassing malware 🛡️, GitHub-based malware distribution 📦
date: 2025-12-24
tags: ["apt activity","web framework vulnerabilities","supply chain attacks","edr evasion","ransomware","dns poisoning","credential theft","unauthenticated rce","malware distribution","enterprise security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Operation PCPcat is exploiting Next.js and React framework vulnerabilities through prototype pollution to achieve mass credential theft from thousands of servers while Evasive Panda continues refining DNS poisoning techniques to deliver stealthy MgBot implants. Security teams face mounting threats from multiple critical vulnerabilities in enterprise tools like M-Files, Net-SNMP, and MongoDB, alongside new malware families including NtKiller EDR-disabler, HardBit 4.0 ransomware, and Webrat infostealer distributed through fake GitHub repositories.
---

# Daily Threat Intel Digest - 2025-12-24

## 🔴 Critical Threats & Active Exploitation

**[NEW] Operation PCPcat compromises 59,000+ Next.js and React servers in 48 hours**  
Attackers are exploiting two critical vulnerabilities (CVE-2025-29927 and CVE-2025-66478) in Next.js and React frameworks to achieve remote code execution through prototype pollution, enabling mass credential theft. The campaign maintains a 64.6% success rate, harvesting between 300,000 and 590,000 sets of credentials from .env files, SSH keys, and cloud configurations. Organizations using Next.js must audit for unauthorized access, rotate exposed credentials, and block traffic to the Singapore-based C2 server at 67.217.57.240 [[Operation PCPcat Exploits Next.js and React, Impacting 59,000+ Servers](https://gbhackers.com/operation-pcpcat-exploits-next-js-and-react/); [Operation PCPcat Compromises 59,000+ Next.js and React Servers in Just 48 Hours](https://cyberpress.org/operation-pcpcat-compromises-next-js-and-react/)].  

**[UPDATE] Evasive Panda APT poisons DNS requests to deliver MgBot**  
The Evasive Panda group (aka Bronze Highland) has refined its adversary-in-the-middle attacks by poisoning DNS responses to deliver MgBot implants, using hybrid encryption and memory injection for stealth. New loaders target victims via fake update lures for apps like SohuVA and iQIYI, exploiting encrypted configuration buffers to bypass detection. This expands the group's persistence capabilities, affecting systems in Türkiye, China, and India since 2022. Defenders should hunt for injected svchost.exe processes and block C2 IPs like 60.28.124.21 [[Evasive Panda APT poisons DNS requests to deliver MgBot](https://malware.news/t/evasive-panda-apt-poisons-dns-requests-to-deliver-mgbot/102815#post_1)].

## ⚠️ Vulnerabilities & Patches

**[NEW] M-Files vulnerability (CVE-2025-13008) allows session token hijacking**  
A critical flaw in M-Files Server enables authenticated attackers to capture active session tokens via the Web interface, leading to account takeover and data exfiltration. The vulnerability (CVSS 8.6) stems from inadequate token protection and affects versions before 25.12.15491.7. Organizations must patch immediately and monitor for anomalous session activity, as exploitation requires no malware and leaves minimal traces [[M-Files Vulnerability Allows Attackers to Capture Session Tokens of Active Users](https://cyberpress.org/m-files-vulnerability/)].  

**[NEW] Net-SNMP vulnerability (CVE-2025-68615) enables unauthenticated RCE**  
A buffer overflow in Net-SNMP's snmptrapd daemon allows remote attackers to crash services and achieve arbitrary code execution without authentication, affecting all versions before 5.9.5 and 5.10.pre2. The flaw (CVSS 9.8) poses severe risks to network monitoring infrastructure, demanding immediate patching to prevent service disruption [[Net-SNMP Vulnerability Allows Buffer Overflow, Leading to Daemon Crash](https://cyberpress.org/net-snmp-vulnerability/)].  

**[NEW] Critical MongoDB vulnerability (CVE-2025-14847) exposes sensitive data**  
MongoDB servers are vulnerable to uninitialized memory exposure via zlib compression, allowing unauthenticated attackers to extract credentials, encryption keys, or query data from heap memory. The flaw affects versions 3.6 through 8.2.2 and carries critical severity. Vendors advise disabling zlib compression as a workaround while patching to versions like 8.2.3 [[Critical MongoDB Vulnerability Exposes Sensitive Data Through zlib Compression](https://cyberpress.org/critical-mongodb-vulnerability-2/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] NtKiller malware advertised as EDR/antivirus disabler**  
A new underground tool, NtKiller, is being promoted for $500–$1,100 on dark web forums to disable AV/EDR solutions like Microsoft Defender and Kaspersky. It features early-boot persistence, Silent UAC bypass, and anti-analysis techniques, potentially enabling ransomware operators to bypass enterprise defenses. Security teams should monitor for suspicious process termination and review EDR logs for evasion attempts [[Dark Web Listings Promote NtKiller Malware as an Antivirus and EDR Disabler](https://cyberpress.org/ntkiller-malware/)].  

**[NEW] HardBit 4.0 ransomware exploits RDP/SMB for long-term control**  
HardBit 4.0 introduces a Neshta-based dropper, wiper mode, and obfuscation techniques to encrypt or destroy data after credential theft via RDP brute-forcing. It disables Windows Defender and persistence mechanisms, increasing challenges for recovery. Defenders should isolate exposed RDP/SMB services and deploy behavioral detections for registry modifications [[HardBit 4.0 Exploits Exposed RDP and SMB Services for Long-Term Network Control](https://cyberpress.org/hardbit-4-0-exploits/)].  

**[NEW] Webrat malware spreads via GitHub fake PoC exploits**  
Attackers are distributing Webrat infostealer through GitHub repositories posing as proof-of-concept exploits for vulnerabilities like CVE-2025-59295. The malware steals credentials from browsers, crypto wallets, and messaging apps, using encrypted C2 channels to evade detection. Organizations must educate developers on verifying repository authenticity and scan downloads for malware [[WebRAT malware spread via fake vulnerability exploits on GitHub](https://www.bleepingcomputer.com/news/security/webrat-malware-spread-via-fake-vulnerability-exploits-on-github/)].