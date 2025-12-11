---
title: React2Shell critical RCE 🔥, Chrome zero-day exploited 🌐, AI conversation scams 🤖, Docker credential leaks 🐳, Spiderman bank phishing 🏦
date: 2025-12-11
tags: ["react2shell","zero-day","ai scams","container security","banking phishing","malware","critical infrastructure","web vulnerabilities","social engineering","android ransomware"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: React2Shell vulnerability affects hundreds of thousands of web systems with unauthenticated RCE, while Chrome's eighth zero-day enables browser-based attacks without user interaction. Attackers are leveraging AI conversations to deliver AMOS infostealer and 10,000+ Docker containers are leaking production credentials alongside sophisticated banking phishing services targeting European financial institutions.
---

# Daily Threat Intel Digest - December 11, 2025

## 🔴 Critical Threats

**React2Shell Exploitation Surpasses 50 Confirmed Victims**  
The critical CVE-2025-55182 vulnerability in React Server Components (dubbed "React2Shell") has reached epidemic proportions, with Palo Alto Networks Unit 42 reporting over 50 confirmed organizations compromised. Shadowserver Foundation scanning revealed 644,000 domains and 165,000 unique IPs remain vulnerable, with two-thirds located in the United States. The flaw, rated CVSS 10.0, allows unauthenticated remote code execution and is being exploited by diverse threat actors including China-nexus groups, ransomware operators, and opportunistic botnets. CISA has shortened the federal patching deadline to December 13, underscoring the severity.  
**So What?** This is a Log4Shell-level event affecting modern web infrastructure. Any organization using React Server Components or Next.js App Router should treat this as an emergency patching situation before attackers achieve full system compromise. [Attacks pinned to critical React2Shell defect surge, surpass 50 confirmed victims](https://cyberscoop.com/react2shell-attacks-surge-50-victims/)

**Google Patches Eighth Chrome Zero-Day of 2025**  
Google released emergency updates for Chrome (143.0.7499.109/110) to patch a high-severity vulnerability tracked as bug 466192044, confirmed exploited in the wild. The flaw exists in the LibANGLE graphics library's Metal renderer and could allow memory corruption leading to arbitrary code execution. This marks the eighth Chrome zero-day patched this year, following two others addressed in November and July. Google has restricted access to bug details while users update.  
**So What?** Browser-based attacks remain a primary infection vector. Users should update Chrome immediately or enable automatic updates, as attackers are actively exploiting this to compromise systems without user interaction. [Google fixes eighth Chrome zero-day exploited in attacks in 2025](https://www.bleepingcomputer.com/news/security/google-fixes-eighth-chrome-zero-day-exploited-in-attacks-in-2025/)

**AI Conversation Scams Deploy AMOS Infostealer**  
A sophisticated campaign is abusing Google search ads to direct users to malicious ChatGPT and Grok conversations containing instructions to install the Atomic macOS Stealer (AMOS). Huntress researchers reproduced the attack across multiple macOS troubleshooting queries, where victims execute base64-encoded scripts from AI chats, leading to AMOS deployment with root privileges. The malware targets cryptocurrency wallets, browser data, and macOS Keychain, with persistence achieved via LaunchDaemons.  
**So What?** This represents an evolution of social engineering using trusted AI platforms. Users should never execute terminal commands from unknown sources, even within AI conversations, and security teams should monitor for unusual DNS beaconing and credential theft from macOS systems. [Google ads for shared ChatGPT, Grok guides push macOS infostealer malware](https://www.bleepingcomputer.com/news/security/google-ads-for-shared-chatgpt-grok-guides-push-macos-infostealer-malware/)

## ⚠️ Vulnerabilities & Exploits

**Fortinet Patches Critical Authentication Bypass Flaws**  
Fortinet released patches for critical CVE-2025-59718 and CVE-2025-59719 vulnerabilities allowing unauthenticated attackers to bypass FortiCloud SSO authentication via crafted SAML responses. The flaws affect FortiOS, FortiProxy, FortiSwitchManager, and FortiWeb products. While FortiCloud SSO is not enabled by default, many organizations activate it during device registration. CISA has added these CVEs to its Known Exploited Vulnerabilities catalog.  
**So What?** These authentication bypasses could allow attackers to gain administrative access to network infrastructure. Organizations should immediately apply patches and disable FortiCloud SSO if not actively used. [Fortinet: Critical vulnerabilities — Different Products](https://socfortress.medium.com/fortinet-critical-vulnerabilities-different-products-7432631af2f4)

**10,000+ Docker Hub Images Expose Production Credentials**  
Security researchers at Flare discovered 10,456 Docker Hub container images leaking sensitive data, including live credentials to production systems, CI/CD databases, and AI model keys. The exposed secrets impact over 100 organizations, including a Fortune 500 company and major national bank. Analysis revealed 42% of affected images contained five or more sensitive values, with AI model access tokens being the most frequent.  
**So What?** Container image secrecy is fundamentally broken in many development workflows. DevOps teams should implement secrets scanning across the entire software development lifecycle and avoid storing secrets in container images entirely. [Over 10,000 Docker Hub images found leaking credentials, auth keys](https://www.bleepingcomputer.com/news/security/over-10-000-docker-hub-images-found-leaking-credentials-auth-keys/)

**ValleyRAT Analysis Reveals Sophisticated Kernel Rootkit**  
Check Point Research disclosed details of ValleyRAT's embedded kernel-mode rootkit, which retains valid signatures and can load on fully updated Windows 11 systems. The rootkit includes capabilities for stealth installation, user-mode shellcode injection via APCs, and forceful deletion of AV/EDR drivers. Approximately 85% of detected ValleyRAT samples appeared in the last six months, correlating with the builder's public release.  
**So What?** The combination of a modular backdoor with kernel-level stealth presents significant detection challenges. Security teams should monitor for unusual driver loading activity and implement behavioral detection for APC-based injection techniques. [Cracking ValleyRAT: From Builder Secrets to Kernel Rootkits](https://research.checkpoint.com/2025/cracking-valleyrat-from-builder-secrets-to-kernel-rootkits/)

## 👤 Threat Actor Activity

**Spiderman Phishing Service Targets European Banks**  
A new phishing-as-a-service kit called "Spiderman" enables attackers to create pixel-perfect replicas of banking sites targeting institutions across five European countries. The modular platform supports real-time victim interaction, PhotoTAN interception, and cryptocurrency wallet theft. Varonis researchers observed one Spiderman group on Signal with 750 members, indicating widespread adoption.  
**So What?** Banking customers should verify domain authenticity before entering credentials, and financial institutions should implement browser-in-the-browser detection and transaction monitoring to counter these sophisticated attacks. [New Spiderman phishing service targets dozens of European banks](https://www.bleepingcomputer.com/news/security/new-spiderman-phishing-service-targets-dozens-of-european-banks/)

**US Charges Ukrainian Aiding Russian Hacktivist Groups**  
Victoria Dubranova, a Ukrainian national, faces charges for supporting Russian state-backed hacktivist groups NoName057(16) and CyberArmyofRussia_Reborn (CARR). The groups conducted over 1,500 DDoS attacks and breached critical infrastructure including US water systems and a meat processing facility. CARR, with over 75,000 Telegram followers, caused physical damage including ammonia leaks and water spillage.  
**So What?** This highlights how state-sponsored cyber operations blur lines between hacktivism and military objectives. Critical infrastructure organizations should expect continued targeting and implement operational technology security measures. [US charges hacker tied to Russian groups that targeted water systems and meat plants](https://cyberscoop.com/us-charges-russian-backed-hacker-critical-infrastructure-attacks-carr-noname05716/)

**New DroidLock Ransomware Targets Android Users**  
Zimperium researchers identified DroidLock, a new Android ransomware targeting Spanish-speaking users and distributed through malicious websites. The malware can lock devices, steal lock patterns via overlay attacks, and deploy 15 different commands including file wiping and camera activation. DroidLock demands ransom within 24 hours under threat of permanent data destruction.  
**So What?** Android users should avoid sideloading apps from untrusted sources and verify app permissions. Security teams should implement mobile threat defense to detect overlay attacks and unusual administrative behavior. [New DroidLock malware locks Android devices and demands a ransom](https://www.bleepingcomputer.com/news/security/new-droidlock-malware-locks-android-devices-and-demands-a-ransom/)

## 🛡️ Security Tools & Defenses

**Microsoft Teams to Monitor External Domain Anomalies**  
Microsoft announced a new "External Domains Anomalies Report" for Teams, launching February 2026. The feature will analyze messaging trends to detect sharp spikes in activity, communications with new domains, and abnormal engagement patterns with external entities. This provides IT administrators with visibility into potential data sharing or security threats.  
**So What?** This addresses the growing challenge of detecting lateral movement and data exfiltration through collaboration platforms. Security teams should plan to integrate this reporting into their insider threat and data loss prevention strategies. [Microsoft Teams to warn of suspicious traffic with external domains](https://www.bleepingcomputer.com/news/security/microsoft-teams-to-warn-of-suspicious-traffic-with-external-domains/)

**HTTPS Certificate Industry Phases Out Weak Validation**  
The Chrome Root Program and CA/Browser Forum adopted new requirements phasing out 11 legacy domain validation methods by March 2028. The changes eliminate weaker verification signals like physical mail, phone calls, and WHOIS-based validation in favor of automated, cryptographically verifiable methods like DNS-based challenges.  
**So What?** This represents a fundamental improvement in web PKI security that will reduce certificate fraud opportunities. Organizations should prepare for more stringent certificate validation requirements and review their certificate management processes. [HTTPS certificate industry phasing out less secure domain validation methods](https://security.googleblog.com/2025/12/https-certificate-industry-phasing-out.html)

**OWASP Releases Top 10 for Agentic AI Applications**  
The OWASP Foundation released its first Top 10 list for agentic AI applications, addressing risks unique to autonomous systems that can execute actions without human oversight. Key risks include tool misuse, identity abuse, supply chain vulnerabilities, and memory injection attacks. The framework provides guidance for securing AI agents that increasingly operate in enterprise environments.  
**So What?** As AI agents become integral to business operations, security teams must evolve from static application security to continuous monitoring of autonomous behaviors. This framework provides a roadmap for implementing appropriate controls. [OWASP Top 10 for Agentic Applications 2026 Is Here – Why It Matters and How to Prepare](https://www.paloaltonetworks.com/blog/cloud-security/owasp-agentic-ai-security/)

## 📰 Industry Developments

**Microsoft's 2025 Patch Tuesday Review Shows Rising Vulnerabilities**  
Microsoft addressed 1,130 CVEs in 2025 Patch Tuesday releases, a 12% increase from 2024 and the second consecutive year exceeding 1,000 vulnerabilities. Of these, 41 were zero-days with 24 exploited in the wild. Elevation of Privilege vulnerabilities dominated at 38.3%, followed by Remote Code Execution at 30.8%. October set a new monthly record with 167 CVEs patched.  
**So What?** The increasing vulnerability volume challenges traditional patching cycles. Organizations should implement risk-based prioritization and automation to manage the growing patch workload effectively. [Microsoft Patch Tuesday 2025 Year in Review](https://www.tenable.com/blog/microsoft-patch-tuesday-2025-year-in-review)

**White House Moves to Send AI Chips to China**  
President Trump announced plans to allow NVIDIA H200 chip sales to China with unspecified conditions, while the DOJ simultaneously prosecuted chip smugglers. Alan Hao Hsu pleaded guilty to funneling over 7,000 high-performance GPUs worth $160 million to Chinese companies through shell corporations and falsified shipping documents.  
**So What?** This creates a confusing policy landscape where legitimate sales may coexist with enforcement actions. Technology companies should carefully review export compliance programs and monitor for regulatory changes. [As White House moves to send AI chips to China, Trump's DOJ prosecutes chip smugglers](https://cyberscoop.com/white-house-sends-ai-chips-to-china-trump-doj-prosecutes-chip-smugglers/)