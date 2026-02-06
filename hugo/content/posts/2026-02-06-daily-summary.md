---
title: React Native CLI exploitation 💻, ShadowSyndicate EclipseShift 💣, China DKnife AitM framework 🇨🇳, Windows screensaver RMM attacks 🪟
date: 2026-02-06
tags: ["command injection","ransomware","apt activity","man-in-the-middle","android malware","spearphishing","privilege escalation","supply chain","china nexus","manufacturing sector"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical vulnerabilities in React Native CLI and SmarterMail are being actively exploited for remote code execution and ransomware deployment, while ShadowSyndicate's new EclipseShift malware uses dynamic server transition techniques to target manufacturing and logistics organizations. China-linked threat actors continue deploying the DKnife AitM framework against Linux infrastructure, and attackers are increasingly abusing Windows screensavers and fake PDFs to install legitimate RMM tools for persistent access.
---

# Daily Threat Intel Digest - 2026-02-06

## 🔴 Critical Threats & Active Exploitation

**[NEW] CISA adds React Native CLI flaw to KEV catalog amid active exploitation**  
Attackers are actively exploiting CVE-2025-11953, a critical OS command injection vulnerability in the React Native Community CLI that allows unauthenticated remote code execution on development servers. The flaw stems from unsafe input handling in the Metro Development Server, where crafted POST requests can execute arbitrary system commands with full control on Windows systems. CISA has given federal agencies until February 26, 2026 to patch, but warns that exploitation is already ongoing in development environments, putting source code and credentials at immediate risk [[Cyberpress](https://cyberpress.org/react-native-community-command-injection-vulnerability/); [GBHackers](https://gbhackers.com/cisa-alerts-exploited-react-native-community-security-flaw/)].

**[NEW] SmarterMail zero-day actively exploited in ransomware attacks**  
CISA has added CVE-2026-24423 to its KEV catalog after confirming active exploitation in ransomware campaigns. The critical vulnerability stems from missing authentication in SmarterMail's ConnectToHub API method, allowing unauthenticated attackers to force the mail server to connect to malicious HTTP endpoints and execute OS commands with system privileges. Attackers are leveraging this flaw to deploy ransomware across enterprise networks, making immediate patching essential for organizations running vulnerable SmarterMail instances [[Cyberpress](https://cyberpress.org/cisa-warns-of-actively-exploited-smartertools-smartermail-vulnerability-used-in-ransomware-attacks/); [GBHackers](https://gbhackers.com/cisa-advisory-highlights-exploited-smartertools-vulnerability/)].

**[NEW] CentOS 9 kernel LPE vulnerability with public PoC**  
A newly discovered Use-After-Free vulnerability in CentOS Stream 9's networking subsystem allows local users to escalate privileges to root, with a fully functional proof-of-concept exploit already publicly available. The flaw resides in the sch_cake packet scheduler's cake_enqueue() function, which incorrectly returns success after packet drops under buffer pressure, creating dangling references that attackers can exploit for arbitrary code execution. Despite responsible disclosure over 90 days ago, Red Hat lists the fix as "in progress," leaving production systems vulnerable to full compromise until patches are released [[Cyberpress](https://cyberpress.org/centos-9-vulnerability/); [GBHackers](https://gbhackers.com/centos-9-security-flaw/)].

## 🎯 Threat Actor Activity & Campaigns  

**[NEW] ShadowSyndicate deploys novel server transition technique in ransomware attacks**  
The ShadowSyndicate ransomware group has launched a sophisticated campaign targeting manufacturing and logistics sectors across North America and Europe, infecting over 150 organizations in the first week. Their new "EclipseShift" ransomware employs a dynamic server transition technique that shifts C2 communications between multiple compromised servers via DNS TXT record lookups, frustrating network defenses that rely on static infrastructure blocking. The campaign demands average ransoms of $2.5 million and uses living-off-the-land techniques to minimize forensic footprints, with attackers exploiting CVE-2025-1234 for lateral movement [[Cyberpress](https://cyberpress.org/shadowsyndicate-unleashes-server-transition/)].

**[NEW] China-nexus hackers deploy 'DKnife' AitM framework targeting Linux infrastructure**  
A China-linked threat actor is actively deploying "DKnife," a sophisticated adversary-in-the-middle framework that compromises Linux-based routers and edge devices for surveillance and traffic redirection. Active since at least 2019, the campaign employs seven distinct Linux implants that inspect network traffic, hijack legitimate software downloads, and deliver additional malware. The framework remains active as of January 2026, targeting personal computers and mobile devices through compromised network infrastructure, enabling persistent man-in-the-middle capabilities against organizations using vulnerable Linux edge devices [[GBHackers](https://gbhackers.com/china-nexus-hackers/); [SecurityWeek](https://www.securityweek.com/dknife-implant-used-by-chinese-threat-actor-for-adversary-in-the-middle-attacks/)].

**[NEW] Sophisticated Android malware campaign abuses fake RTO challan notifications**  
Seqrite Labs has uncovered an advanced three-stage Android malware campaign targeting Indian users through WhatsApp messages impersonating RTO (Regional Transport Office) challan notifications. The campaign combines cryptocurrency mining with comprehensive data theft, stealing PII, financial credentials, and OTPs through fake government UIs. The malware uses Google Firebase for C2 communications and has already compromised approximately 7,400 devices, with backend analysis revealing active collection of sensitive victim data including Aadhaar numbers, UPI PINs, and banking credentials [[Cyberpress](https://cyberpress.org/fake-rto-alerts-spread-malware/)].

**[NEW] Attackers weaponize Windows screensavers and fake PDFs to deploy RMM tools**  
Two converging spearphishing campaigns are abusing overlooked file formats to deploy legitimate Remote Monitoring and Management (RMM) tools for persistent access. The first campaign uses Windows screensaver (.scr) files disguised as documents to silently install RMM agents like SimpleHelp, while the second employs fake PDFs that prompt users to download fraudulent Adobe Reader updates. Both techniques exploit legitimate IT administration tools to bypass traditional security controls, creating persistent remote access that blends with normal operations and enables escalation to credential theft or ransomware [[Cyberpress](https://cyberpress.org/windows-screensaver-grants-remote-access/); [Cyberpress](https://cyberpress.org/fake-pdfs-install-remote-access/); [GBHackers](https://gbhackers.com/windows-screensaver/)].

## ⚠️ Vulnerabilities & Patches  

**[NEW] F5 releases urgent fixes for BIG-IP and NGINX vulnerabilities**  
F5 has issued its quarterly security notification addressing multiple vulnerabilities across BIG-IP Advanced WAF and NGINX products. While F5 classifies the primary vulnerabilities as "Medium" severity internally, CVSS v4.0 scoring assigns them a score of 8.2, indicating high risk to enterprise environments. The flaws require immediate attention as they could potentially allow attackers to bypass security controls or execute unauthorized actions on vulnerable systems [[GBHackers](https://gbhackers.com/f5-releases-urgent-security-fixes-for-critical-vulnerabilities-in-big-ip-and-nginx/)].

**[NEW] OAuth token vulnerabilities enable full Microsoft 365 compromise**  
Security researchers have disclosed a chain of medium-severity vulnerabilities in Microsoft 365 that, when combined, enable attackers to bypass all email security controls and achieve persistent access. The attack exploits an unsecured email API endpoint and verbose error messages that expose OAuth tokens, allowing authenticated phishing campaigns that appear legitimate despite failing SPF, DKIM, and DMARC checks. The technique demonstrates how seemingly minor flaws can chain together to provide full account takeover capabilities [[GBHackers](https://gbhackers.com/microsoft-365-breach/)].

## 🛡️ Defense & Detection  

**[NEW] OpenAI launches Trusted Access framework for AI cybersecurity**  
OpenAI has introduced Trusted Access for Cyber, a new identity- and trust-based framework designed to enhance cybersecurity defenses while mitigating risks from advanced AI models. The initiative centers on GPT-5.3-Codex, OpenAI's most cyber-capable frontier model, which can operate autonomously for hours to complete complex security tasks. The framework aims to provide organizations with safer access to powerful AI capabilities while implementing controls against misuse and prompt injection attacks [[GBHackers](https://gbhackers.com/openai-launches-trusted-access/)].

**[NEW] CISA orders agencies to remove end-of-life devices amid active exploitation**  
CISA has issued a binding operational directive requiring federal civilian agencies to identify and remove unsupported, internet-facing edge devices within 18 months due to widespread exploitation by advanced threat actors, some with nation-state ties. The directive responds to active campaigns targeting EOS equipment, giving agencies three months to inventory devices and requiring immediate updates where supported. CISA urges private sector organizations to follow suit, emphasizing that unsupported devices should never remain on enterprise networks [[Malware.News](https://malware.news/t/cisa-orders-agencies-to-patch-and-replace-end-of-life-devices-citing-active-exploitation/103906#post_1)].

## 📋 Policy & Industry News  

**[NEW] Betterment breach exposes 1.4 million customers in social engineering attack**  
Investment platform Betterment has disclosed a data breach affecting approximately 1.4 million customers following a sophisticated social engineering attack in January 2026. Attackers manipulated employees to gain access to third-party operational platforms, exfiltrating PII including names, dates of birth, contact information, and professional details. The breach was followed by a DDoS attack investigators believe was a diversion tactic. Betterment has revoked unauthorized tokens and enhanced access controls while monitoring for leaked data distribution [[Cyberpress](https://cyberpress.org/betterment-data-breach-exposes-personal-details-of-1-4-million-customers/); [GBHackers](https://gbhackers.com/betterment-data-breach/)].

**[NEW] Zscaler acquires SquareX to enhance browser security**  
Zscaler has completed its acquisition of browser security firm SquareX, extending Zero Trust capabilities directly into the web browser. The strategic move, which closed on February 5, 2026, focuses on redefining security for the "AI era" of enterprise work by providing stronger protections against web-based threats, particularly for unmanaged devices [[GBHackers](https://gbhackers.com/zscaler-integrates-squarex/); [SecurityWeek](https://www.securityweek.com/zscaler-acquires-browser-security-firm-squarex/)].