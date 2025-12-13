---
title: Coupang data breach 🔐, Apple zero-days ⚡, React2Shell RCE 💻, Phantom Stealer campaign 🎣
date: 2025-12-13
tags: ["data breach","insider threats","zero-day vulnerabilities","remote code execution","phishing","information stealers","malware delivery","vulnerability exploitation","supply chain"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: A massive Coupang data breach exposed 33.7 million customer records through insider access abuse while Apple rushed to patch two actively exploited WebKit zero-day vulnerabilities used in sophisticated attacks. The React2Shell RCE vulnerability was added to CISA's KEV catalog as attackers deliver Phantom Stealer malware through targeted phishing campaigns and hide AgentTesla in fake movie torrents.
---

# Daily Threat Intel Digest - 2025-12-13

## 🔴 Critical Threats & Active Exploitation

**[NEW] Coupang data breach impacts 33.7 million after insider access abuse**
A data breach at South Korean e-commerce giant Coupang, affecting 33.7 million customers, has been traced to a former employee who retained system access after leaving the company. The breach, which occurred in June but was only discovered in November, exposed names, email addresses, physical addresses, and order histories. The incident has already led to the resignation of the company's CEO and sparked a nationwide wave of phishing campaigns impersonating Coupang, affecting an estimated two-thirds of the country's population and putting millions at risk of follow-on attacks [[BleepingComputer](https://www.bleepingcomputer.com/news/security/coupang-data-breach-traced-to-ex-employee-who-retained-system-access/)].

**[NEW] Apple patches two zero-days exploited in sophisticated attacks**
Apple has issued emergency updates for two actively exploited WebKit zero-day vulnerabilities, CVE-2025-43529 and CVE-2025-14174. These flaws, which could allow remote code execution via maliciously crafted web content, were used in an "extremely sophisticated attack" against specific individuals. Notably, CVE-2025-14174 is the same flaw Google recently patched in Chrome, indicating a coordinated exploitation effort. All modern Apple devices—including iPhone, iPad, and Mac—are affected, making immediate application of OS updates critical to prevent further targeted intrusions [[BleepingComputer](https://www.bleepingcomputer.com/news/security/apple-fixes-two-zero-day-flaws-exploited-in-sophisticated-attacks/)].

**[UPDATE] React2Shell RCE vulnerability added to CISA's Known Exploited Vulnerabilities catalog**
Following its public disclosure last week, the critical React2Shell vulnerability (CVE-2025-55182) has been added to CISA's Known Exploited Vulnerabilities (KEV) catalog. The flaw, which enables unauthenticated remote code execution in React Server Components (RSC), is seeing a surge in scanning and exploitation attempts worldwide. Its addition to the KEV catalog mandates that U.S. federal civilian agencies patch the vulnerability by January 2, 2026, and serves as a strong indicator of active, widespread exploitation that requires immediate prioritization for all organizations running vulnerable RSC-enabled services [[GBHackers](https://gbhackers.com/critical-react2shell-vulnerability-cve-2025-55182-analysis-surge-in-attacks-targeting-rsc-enabled-services-worldwide/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Phantom Stealer delivered via ISO files in Russian phishing campaign**
Attackers are conducting an active phishing campaign in Russia that delivers the Phantom information-stealing malware through malicious ISO files. The campaign targets finance and accounting professionals using fake payment confirmation emails as a lure. Once executed, the payload steals a wide range of sensitive data, including credentials, cryptocurrency wallets, and browser information, putting financial departments at direct risk of corporate account takeover and financial fraud [[GBHackers](https://gbhackers.com/hackers-target-windows-systems-using-phantom-stealer/)].

**[NEW] Fake movie torrent hides AgentTesla malware in subtitle files**
A sophisticated malware distribution campaign is using a fake torrent for the new movie 'One Battle After Another' to deliver the Agent Tesla remote access trojan. In a notable twist, the infection chain hides malicious PowerShell commands within a `.srt` subtitle file, which are executed when a user clicks a deceptive shortcut masquerading as a movie launcher. This stealthy technique ultimately infects systems with a well-known infostealer, demonstrating the continued risk of piracy-related malware for users who download from untrusted sources [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-one-battle-after-another-torrent-hides-malware-in-subtitles/)].

## 🛡️ Defense, Tools & Industry News

**[NEW] Windows clients leak AD Domain Controller DNS queries on public Wi-Fi**
Security observations reveal that Windows clients can expose sensitive Active Directory DNS queries over untrusted public Wi-Fi networks. This leak, which can include queries for domain controllers, allows attackers on the same network to perform OSINT and potentially harvest NTLM hashes or facilitate credential-thealing attacks. This common misconfiguration puts remote workers at significant risk whenever they connect to public networks without a VPN, which encrypts DNS traffic and prevents this information disclosure [[Feedpress.me](https://feedpress.me/link/23535/17231631/windows-ad-dns-public-vpn)].

**[NEW] Kali Linux 2025.4 released with AI agent tooling**
The Kali Linux team has released its final 2025 update, version 2025.4, introducing three new tools for security professionals. The most notable addition is `hexstrike-ai`, an MCP (Model Context Protocol) server designed to let AI agents autonomously run security tools. The release also includes `bpf-linker`, a BPF static linker, and `evil-winrm-py`, a Python-based WinRM client, expanding the platform's capabilities for penetration testing and red teaming, particularly as AI integration into security workflows accelerates [[BleepingComputer](https://www.bleepingcomputer.com/news/security/kali-linux-20254-released-with-3-new-tools-desktop-updates/)].

**[NEW] DOJ sues Fulton County over refusal to turn over 2020 voter data**
The U.S. Department of Justice is suing Fulton County, Georgia, for failing to comply with a subpoena for all 2020 election records, including used ballots and signature envelopes. This lawsuit is part of a larger, nationwide effort by the DOJ to collect extensive voter and election data from state and local governments ahead of the 2026 and 2028 elections. The push to centralize vast amounts of sensitive voter data at the federal level raises significant data security and privacy concerns, as it creates a high-value target for nation-state and cybercriminal actors [[CyberScoop](https://cyberscoop.com/doj-sues-fulton-county-georgia-over-2020-voter-data/)].