---
title: Payouts King ransomware VM evasion 💀, iTerm2 command injection flaw 🖥️, Windows Defender zero-days 🔴, data exposure incidents 📂, ransomware gang activity 💣
date: 2026-04-18
tags: ["ransomware","virtual machine evasion","terminal vulnerability","zero-day exploit","data exposure","threat actors","healthcare security","patch management","credential harvesting","endpoint security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Payouts King ransomware operators are leveraging hidden QEMU virtual machines to bypass endpoint security and establish covert tunnels, while critical trust boundary failures in iTerm2 and unpatched Windows Defender zero-days create severe exploitation risks for organizations. Ransomware groups continue targeting European and Middle Eastern businesses across multiple sectors, and widespread data exposures from misconfigured storage highlight ongoing gaps in security architecture and compliance.
---
# Daily Threat Intel Digest - April 18, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] Payouts King ransomware deploys hidden virtual machines to bypass endpoint security**
The Payouts King ransomware operation is using QEMU emulators to run hidden Alpine Linux virtual machines on compromised Windows systems, creating a covert environment invisible to host-based security tools where attackers can store payloads, execute commands, and establish persistent SSH tunnels. Sophos researchers documented two campaigns—STAC4713 (linked to Payouts King) and STAC3725—where attackers used scheduled tasks running as SYSTEM to launch QEMU VMs disguised as database files, enabling credential harvesting, Active Directory reconnaissance, and data exfiltration without detection. Initial access vectors include exposed SonicWall and Cisco SSL VPNs, SolarWinds Web Help Desk vulnerability CVE-2025-26399, and social engineering via Microsoft Teams posing as IT staff to trick employees into installing QuickAssist [BleepingComputer].

**[NEW] iTerm2 terminal escape sequence flaw enables arbitrary command execution from file preview**
A critical trust boundary failure in iTerm2's SSH integration allows malicious terminal output—such as a `cat readme.txt` command on a compromised file—to inject forged conductor protocol messages that trigger the terminal to execute arbitrary commands on the local system. The vulnerability (no CVE assigned) stems from iTerm2 accepting SSH conductor protocol messages from untrusted terminal output rather than only from legitimate SSH sessions, allowing attackers to forge DCS 2000p hooks and OSC 135 replies that push iTerm2 into executing attacker-controlled commands. The fix was committed March 31 but has not yet reached stable releases, meaning current production versions remain vulnerable [Calif.io research].

**[UPDATE] Microsoft Defender "RedSun" zero-day exploited without patch**
A second Windows local privilege escalation exploit from developer "Nightmare-Eclipse" was dropped on GitHub April 16, following the BlueHammer exploit released 13 days earlier. The RedSun exploit (no CVE assigned) abuses Windows Defender to deliver payloads, continuing the trend of security tools becoming attack vectors. Microsoft has not issued patches for either vulnerability, and both exploits are fully functional with no coordinated disclosure process [Cyderes analysis].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Scattered Spider member Tyler Robert Buchanan pleads guilty to conspiracy charges**
One of five defendants charged in the November 2024 Scattered Spider indictment has pleaded guilty to one count of conspiracy to commit wire fraud and one count of aggravated identity theft. This follows the April 2025 guilty plea and August 2025 sentencing of fellow defendant Noah Michael Urban ("King Bob") to ten years in prison and $13 million in restitution. Scattered Spider gained notoriety for sophisticated SIM-swapping and social engineering campaigns targeting telecommunications and cryptocurrency companies [DataBreaches.net].

**[NEW] Three ransomware groups claim new victims across Europe and Middle East**
The Qilin ransomware group claimed responsibility for an attack on Spanish hospitality leader HBX Group, threatening to leak sensitive data unless negotiations begin. Separately, Lamashtu ransomware targeted Romanian pharmaceutical company Biotehnos, while Payload ransomware struck Egyptian textile manufacturer Oriental Weavers. All three groups posted threats on dark web leak sites indicating data would be published without contact from company representatives [DeXpose; DeXpose; DeXpose].

**[UPDATE] Grinex crypto exchange blames $13.7M hack on Western intelligence**
Kyrgyzstan-based cryptocurrency exchange Grinex, believed to be a rebrand of sanctioned Russian exchange Garantex, suspended operations after losing $13.7 million in what it claims was a coordinated attack by Western intelligence agencies. Blockchain analysis firms Elliptic and TRM Labs traced stolen funds to TRON and Ethereum addresses, with TRM also identifying a second $15 million theft at Kyrgyzstan exchange TokenSpot. Neither exchange provided technical evidence supporting the Western intelligence attribution [BleepingComputer].

## ⚠️ Vulnerabilities & Patches

**[NEW] Fiverr user data exposed in Google search results for 40+ days**
Tax documents, IRS Form 1040s, and other sensitive customer files shared between freelancers and clients on Fiverr are publicly indexed in Google search results due to misconfigured Cloudinary storage buckets that lack authentication or signed URLs. A security researcher reported the architectural misconfiguration to Fiverr 40 days ago but received no response, prompting public disclosure. The exposure enables identity theft, financial fraud, and phishing campaigns against affected users, and potentially violates GLBA and FTC Safeguards Rule compliance for tax preparers advertising on the platform [Cyberpress].

**[NEW] SimplifyU E-Health platform riddled with severe vulnerabilities**
A penetration test of the SimplifyU quality management software for healthcare revealed 31 stored XSS instances (14 exploitable by lowest-permission users), CSV injection enabling arbitrary command execution, insufficient brute-force protection allowing report enumeration, and exposed EntraID secret keys. Eight CVEs were assigned (CVE-2025-69851 through CVE-2025-69800), and the vendor patched all vulnerabilities in February 2026 releases after coordinated disclosure [Cybersecurity research].

**[NEW] NIST scaling back CVE analysis amid overwhelming submission volume**
The National Institute of Standards and Technology is reducing its vulnerability analysis work due to being overwhelmed by the surge in CVE submissions, signaling that the federal government cannot keep pace with vulnerability discovery rates in the AI era. Security experts note that the private sector will need to fill the gap left by NIST's decision, which comes as AI-accelerated vulnerability discovery further strains the system [Security Boulevard].

**[NEW] Multiple vendor patches require immediate attention**
- **HashiCorp Vault** published two advisories: HCSEC-2026-05 addresses a KVv2 metadata and secret deletion policy bypass denial-of-service flaw; HCSEC-2026-06 fixes a server-side request forgery vulnerability in ACME challenge validation via attacker-controlled DNS [Canadian Cyber Centre].
- **JetBrains YouTrack** versions prior to 2025.3.131383 contain a vulnerability addressed in the April 17 security advisory [Canadian Cyber Centre].
- **Microsoft Edge** versions prior to 147.0.3912.72 require update for multiple vulnerabilities [Canadian Cyber Centre].
- **PAC4J** authentication software contains two vulnerabilities (CVE-2026-40458, CVE-2026-40459) disclosed by CERT Polska [CERT Polska].
- **TP-Link routers** (TL-WR940N v2/v4, TL-WR740N v1/v2) are being actively scanned for CVE-2023-33538 in Mirai malware distribution campaigns, though current exploit attempts are technically flawed [GBHackers].

**[NEW] Micropatches available for Windows Error Reporting Service elevation of privilege**
0patch released micropatches for CVE-2026-20817, a local privilege escalation vulnerability in Windows Error Reporting Service allowing non-admin users to execute arbitrary code as Local System. The patches cover Windows 7, Windows 10 through v1803, Windows 11 through v22H2, and Windows Server 2008 R2 through 2012 R2 for systems no longer receiving official Microsoft updates [0patch Blog].

## 📋 Policy & Industry News

**[NEW] CISA resources "more limited than I would like" amid DHS shutdown**
Acting CISA Director Nick Andersen told House appropriators that the agency cannot conduct normal outreach or preparatory cybersecurity activities during the ongoing Department of Homeland Security funding lapse. CISA canceled summer internship hiring for the CyberCorps scholarship program and cannot make non-salary expenditures without Antideficiency Act exceptions. The resource constraints come as Iran-aligned hackers continue targeting U.S. industrial control systems [Nextgov/FCW].

**[NEW] UK experiencing four nationally significant cyberattacks per week**
The UK's National Cyber Security Centre reported 204 nationally significant cyber incidents in the 12 months leading to September 2025—more than double the 89 recorded the previous year and the highest figure on record. Of 429 total incidents requiring NCSC intervention, 18 were classified as "highly significant" with potential to severely disrupt essential services. The NCSC is urging FTSE 350 executives to treat cyber resilience as a board-level responsibility and reassessing NIS Regulations to address gaps in coverage for decentralized energy infrastructure [NCSC; Cyble].

**[NEW] Congress extends FISA Section 702 surveillance powers for 10 days**
The House and Senate passed a 10-day extension of the Reforming Intelligence and Securing America Act, which reauthorizes warrantless surveillance of foreign targets under Section 702 of FISA. The Trump administration seeks a 180-day "clean" reauthorization, while privacy advocates point to unresolved questions about FBI query practices and expanded surveillance definitions. The Foreign Intelligence Surveillance Court issued an opinion re-certifying the program but took issue with filtering systems, prompting a planned administration appeal [CyberScoop].

**[NEW] Anthropic CEO to meet White House Chief of Staff over AI security concerns**
Anthropic CEO Dario Amodei will meet with White House Chief of Staff Susie Wiles amid concerns about the national security implications of the company's powerful new AI model, reportedly connected to fears about the "Mythos" AI capability and potential for accelerated exploitation. The meeting reflects growing government attention to AI-related security risks as vulnerability discovery timelines compress [DataBreaches.net].

**[NEW] Operation PowerOFF dismantles DDoS-for-hire infrastructure**
A coordinated international crackdown involving 21 countries disrupted over 75,000 users of DDoS-for-hire platforms, resulting in four arrests, 25 search warrants, and the takedown of 53 domains. Law enforcement accessed databases containing over 3 million user accounts and issued warning messages via blockchain transactions to deter future attacks. The operation targeted the "booter" ecosystem that enables low-skilled actors to launch attacks [Cyberpress].