---
title: SharePoint zero-day exploitation 🎯, Russian router DNS hijacking 🌐, supply chain domain takeover ⚠️, Android proxy botnet 🤖, Active Directory RCE 🔐
date: 2026-04-15
tags: ["zero-day exploitation","dns hijacking","supply chain attack","android malware","ransomware","active directory","patch management","credential theft","router security","vulnerability disclosure"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Attackers are actively exploiting a Microsoft SharePoint zero-day vulnerability and Russian state-sponsored actors are hijacking home router DNS configurations to steal credentials, while supply chain flaws in Dragon Boss Solutions left over 25,000 endpoints vulnerable to complete takeover through an insecure update domain. Android malware campaigns are building residential proxy botnets through banking trojans, and critical vulnerabilities in Windows Active Directory and Fortinet products require immediate patching to prevent remote code execution and privilege escalation across enterprise environments.
---
# Daily Threat Intel Digest - April 15, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] Microsoft SharePoint zero-day under active exploitation**

Attackers are actively exploiting CVE-2026-32201, an improper input validation flaw in Microsoft SharePoint Server that enables unauthenticated remote attackers to conduct spoofing attacks over the network. The vulnerability carries a moderate CVSS score of 6.5, but Microsoft has confirmed functional exploit code exists and threat actors are leveraging it in the wild. Exploitation allows attackers to view sensitive data and make unauthorized changes to server content, though it does not impact system availability. Microsoft has released emergency patches for SharePoint Server Subscription Edition (KB5002853), SharePoint Server 2019 (KB5002854), and SharePoint Enterprise Server 2016 (KB5002861) [[Microsoft SharePoint Server Zero-Day Vulnerability Actively Exploited in Attacks](https://cyberpress.org/microsoft-sharepoint-server-zero-day-vulnerability/); [Microsoft Warns of Actively Exploited SharePoint Server Zero-Day](https://gbhackers.com/microsoft-warns-sharepoint-server-zero-day/); [Microsoft April 2026 Patch Tuesday Fixes 168 Flaws, Includes Actively Exploited Zero-Day](https://cyberpress.org/microsoft-april-2026-patch-tuesday-fixes-168-flaws-includes-actively-exploited-zero-day/)].

**[NEW] Russian espionage campaign hijacks home router DNS for credential theft**

A Russian state-sponsored threat actor is targeting unprotected home routers—primarily older MikroTik and TP-Link models—to manipulate DNS settings and redirect traffic through adversary-in-the-middle infrastructure. Rather than relying on phishing lures, attackers are compromising router DNS configurations to transparently intercept credentials and session tokens when victims access legitimate sites. This technique poses elevated risk for remote workers whose home networks lack enterprise-grade protections, as the attack bypasses endpoint controls entirely by operating at the network layer [[Russian Espionage Campaign Targets Home Routers](https://malware.news/t/russian-espionage-campaign-targets-home-routers/106084#post_1)].

**[NEW] Dragon Boss Solutions supply chain flaw exposed 25,000+ endpoints to $10 hijack**

An insecure update domain left more than 25,000 endpoints running Dragon Boss Solutions-signed software vulnerable to complete takeover. Researchers discovered that the domain `chromsterabrowser[.]com`—used by the "search monetization" company's update mechanism—was available for registration for approximately $10. Had an attacker registered it, they could have pushed arbitrary MSI payloads to all affected systems. The exposure spanned 124 countries and included at least 324 infections in sensitive environments such as universities, OT networks in energy and transport, government entities, healthcare providers, and Fortune 500 enterprises. The malware disabled antivirus protections via PowerShell payloads running with SYSTEM privileges [[25,000+ Endpoints Left Exposed In Dragon Boss Solutions Domain Update Breach](https://cyberpress.org/dragon-boss-update-breach/); [Dragon Boss Solutions Supply Chain Attack Exposes 25,000+ Endpoints](https://gbhackers.com/dragon-boss-solutions/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Mirax Android malware builds residential proxy network through banking trojan**

A new Android RAT dubbed Mirax is recruiting infected devices into a residential proxy botnet while simultaneously functioning as banking malware. Distributed via Meta ads for fake IPTV streaming apps, Mirax targets Spanish-speaking users and includes overlay attacks against 182 apps including Spanish banks and cryptocurrency wallets. The malware establishes persistent WebSocket connections on ports 8443-8445 for command and control, data exfiltration, and SOCKS5 proxy tunneling. Even if victims deny Accessibility permissions, the proxy functionality remains operational, allowing attackers to monetize infected devices for IP spoofing, DDoS attacks, or credential spraying campaigns. The operation is restricted to vetted Russian-speaking affiliates [[New Android Malware Recruits Phones as Residential Proxies in Stealth Campaign](https://cyberpress.org/android-malware-builds-proxy-network/)].

**[NEW] PlugX USB worm spreads globally via DLL sideloading**

A new PlugX USB worm variant is propagating across multiple continents including Papua New Guinea, Ghana, Mongolia, Zimbabwe, and Nigeria through DLL sideloading techniques. The malware abuses legitimate executables such as AvastSvc.exe to load malicious payloads, then spreads via USB drives using hidden files and shortcut manipulation to cross air-gapped environments. The worm collects system reconnaissance data including IP configuration, network state, and running processes before exfiltrating stolen files through a hidden RECYCLER.BIN directory structure [[PlugX USB Worm Goes Global DLL Sideloading Fuels Multi-Continent Rampage](https://cyberpress.org/plugx-worm-spreads-globally/)].

**[NEW] JanaWare ransomware targets Turkish users through customized Adwind RAT**

A geographically focused ransomware campaign is deploying JanaWare through a customized variant of the Adwind Java RAT, specifically targeting Turkish users and small organizations. The malware employs heavy obfuscation using Stringer and Allatori protectors, polymorphic file generation to evade hash-based detection, and Tor-based command and control infrastructure. The ransomware uses AES encryption with keys transmitted back to C2 servers over Tor, making decryption practically impossible without attacker cooperation. Ransom notes contain Turkish-language content with a fixed `_ONEMLI_NOT_` component indicating deliberate localization [[Customized Adwind RAT Delivers JanaWare Ransomware To Turkish Victims](https://cyberpress.org/adwind-delivers-janaware-ransomware/); [JanaWare Ransomware Hits Turkish Users via Customized Adwind RAT](https://gbhackers.com/janaware-ransomware/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Microsoft Patch Tuesday addresses 168 vulnerabilities including active zero-day**

Microsoft's April 2026 Patch Tuesday release fixes 168 vulnerabilities across Windows, cloud, and application products. Beyond the actively exploited SharePoint zero-day (CVE-2026-32201), notable patches include CVE-2024-26203 in Azure Data Studio allowing local privilege escalation, CVE-2024-28916 in Xbox Gaming Services enabling elevation of privilege, and CVE-2024-29059 in .NET Framework exposing sensitive information (CVSS 7.5). The release also incorporates Chromium security fixes for memory management flaws in WebCodecs, Dawn, Canvas, and ANGLE that could enable remote code execution through browser exploitation [[Microsoft April 2026 Patch Tuesday Fixes 168 Flaws, Includes Actively Exploited Zero-Day](https://cyberpress.org/microsoft-april-2026-patch-tuesday-fixes-168-flaws-includes-actively-exploited-zero-day/); [Microsoft Patch Tuesday April 2026 Fixes 168 Flaws, Including an Actively Exploited Zero-Day](https://gbhackers.com/microsoft-patch-tuesday-april-2026/)].

**[NEW] Critical Windows Active Directory vulnerability enables remote code execution**

Microsoft has disclosed CVE-2026-33826, a critical vulnerability in Windows Active Directory that allows authenticated attackers to execute malicious code remotely over an adjacent network. Given the central role of Active Directory in enterprise identity management, successful exploitation could enable lateral movement and domain-wide compromise [[Windows Active Directory Flaw Opens Door to Malicious Code Execution](https://gbhackers.com/windows-active-directory-flaw/)].

**[NEW] Fortinet patches 11 vulnerabilities including two critical flaws**

Fortinet has released security updates addressing 11 vulnerabilities across FortiSandbox, FortiOS, FortiAnalyzer, and FortiManager. Two critical vulnerabilities require immediate attention: CVE-2026-39808 allows unauthenticated attackers to execute arbitrary OS commands through FortiSandbox API endpoints, and CVE-2026-39813 enables authentication bypass and privilege escalation in FortiSandbox's JRPC API. Additional patches address heap-based buffer overflow (CVE-2026-22828), missing authentication for critical functions (CVE-2025-53847), and multiple path traversal, XSS, and SQL injection issues [[Fortinet Patches 11 Vulnerabilities Across FortiSandbox, FortiOS, FortiAnalyzer and FortiManager](https://cyberpress.org/fortinet-patches-11-vulnerabilities-across-fortisandbox-fortios-fortianalyzer-and-fortimanager/); [Fortinet Fixes 11 Security Flaws Affecting FortiSandbox, FortiOS, FortiAnalyzer, and FortiManager](https://gbhackers.com/fortinet-fixes-11-security-flaws/)].

**[NEW] Ivanti Neurons for ITSM vulnerabilities enable session hijack and persistent access**

Ivanti has patched two medium-severity vulnerabilities in Neurons for IT Service Management that could allow authenticated attackers to hijack user sessions and maintain access even after account deactivation. CVE-2026-4913 (CVSS 5.7) creates a "zombie access" condition where disabled accounts retain system access, while CVE-2026-4914 (CVSS 5.4) is a stored XSS vulnerability enabling session token theft. Cloud deployments received automatic patches in December 2025, but on-premise installations require manual update to version 2025.4 [[Ivanti Neurons for ITSM Vulnerabilities Let Remote Attackers Obtain User Sessions](https://cyberpress.org/ivanti-neurons-for-itsm-vulnerabilities/); [Ivanti Neurons for ITSM Vulnerabilities Let Remote Attackers Hijack User Sessions](https://gbhackers.com/ivanti-neurons-for-itsm-vulnerabilities/)].

## 🛡️ Defense & Detection

**[NEW] OpenAI launches GPT-5.4-Cyber for defensive security operations**

OpenAI has released GPT-5.4-Cyber, a specialized AI model fine-tuned for defensive cybersecurity workflows including binary reverse engineering, automated vulnerability discovery, and malware analysis. The model features reduced refusal boundaries for legitimate security research tasks while operating within the Trusted Access for Cyber (TAC) program framework, which requires Know Your Customer verification for individual researchers and enterprise teams. Access is granted through strict identity verification, with higher approval tiers unlocking unrestricted usage for verified defenders [[OpenAI Launches GPT-5.4-Cyber with Reverse Engineering and Malware Analysis Features](https://cyberpress.org/openai-launches-gpt-5-4-cyber/); [OpenAI Introduces GPT-5.4 for Reverse Engineering, Vulnerability Discovery, and Malware Analysis](https://gbhackers.com/openai-introduces-gpt-5-4-for-reverse-engineering/)].

**[NEW] AI-assisted research demonstrates Samsung TV root compromise via driver flaw**

Security researchers used AI assistance to achieve root access on Samsung smart TVs by exploiting a world-writable driver interface (`ntksys`) that exposed physical memory access to unprivileged processes. The research demonstrated how AI can chain discovery, validation, and exploitation when provided with source code access and a working lab environment—moving from browser-level execution to kernel credential modification. The work highlights the defensive challenge of verifying driver permissions and memory access controls in embedded systems [[AI Researcher Breaks Samsung TV Security, Gains Root Through Writable Drivers](https://cyberpress.org/samsung-tv-root-access-gained/)].

**[NEW] Booking.com breach enables hyper-realistic phishing attacks**

Booking.com has confirmed unauthorized access to reservation data, exposing full names, email addresses, phone numbers, postal addresses, and specific reservation details including hotel names and stay dates. While financial data was not compromised, the breach enables sophisticated vishing and smishing attacks where threat actors can reference specific trip details to defeat traditional phishing awareness. The company reset PIN codes for affected bookings, which security experts note serves as a confirmation indicator for compromised accounts [[Booking.com Data Breach](https://socfortress.medium.com/booking-com-data-breach-e651a790023f?source=rss-36613248f635------2)].

## 📋 Policy & Industry News

**[NEW] CISA cancels CyberCorps summer internships amid DHS funding crisis**

The Cybersecurity and Infrastructure Security Agency has canceled its 2026 summer internship program for CyberCorps Scholarship for Service students due to Department of Homeland Security funding lapses. The cancellation marks the second consecutive year of disrupted placement efforts for the program, which covers tuition and stipends in exchange for federal service commitments. The disruption exacerbates the federal government's technical talent pipeline challenges, with the U.S. facing an estimated 500,000 open cybersecurity positions and the Trump administration proposing $707 million in CISA budget cuts for fiscal 2027 [[CISA cancels summer internships for cyber scholarship students amid DHS funding lapse](https://cyberscoop.com/cisa-cancels-cybercorps-internships-dhs-funding-crisis/)].

**[NEW] European Commission flags four adult sites for inadequate age verification**

The European Commission has preliminarily found Pornhub, Stripchat, XNXX, and XVideos in breach of the Digital Services Act for failing to implement effective age verification mechanisms. The platforms relied on self-declaration methods such as single-click "I am over 18" confirmations that regulators deemed ineffective at preventing minor access. The finding signals movement toward mandatory privacy-preserving age verification requirements for adult content platforms operating in the EU [[EU flags four porn sites for failing to protect minors](https://malware.news/t/eu-flags-four-porn-sites-for-failing-to-protect-minors/106083#post_1)].