+++
title = "🔥 6 Ransomware Incidents Strike Global Targets - November 29, 2025"
date = "2025-11-29"
tags = ["threat-intelligence", "daily-digest", "cybersecurity", "bleeping computer", "revista de ciberseguridad y seguridad de la informacin para empresas y organismos pblicos ciberseguridadpyme es", "infosecurity magazine", "sans internet storm center infocon green isc sans edu"]
categories = ["Threat Intelligence"]
summary = "Daily threat intelligence digest covering 6 recent security developments."
draft = false
author = "Tia N. List"
lastmod = "2025-11-29T11:00:25.147905"
sources = ["bleeping-computer", "revista-de-ciberseguridad-y-seguridad-de-la-informacin-para-empresas-y-organismos-pblicos-ciberseguridadpyme-es", "infosecurity-magazine", "infosecurity-magazine", "infosecurity-magazine", "sans-internet-storm-center-infocon-green-isc-sans-edu"]
+++



# Daily Threat Intel Digest - 2025-11-29

## 🔴 Critical Threats

**New Metasploit Modules Deliver Multiple Attack Paths**  
Rapid7 dropped 10 new Metasploit modules this week, including a dangerous SMB-to-MSSQL NTLM relay module that opens lateral movement possibilities and unauthenticated RCE exploits for FortiWeb appliances. The SMB relay is particularly concerning as it can chain common authentication mechanisms into database access, potentially bypassing network segmentation. [Metasploit Wrap-Up 11/28/2025](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-11-28-2025)

**17,000+ Secrets Exposed in Public GitLab Repositories**  
A comprehensive scan of GitLab's 5.6 million public repositories revealed over 17,000 exposed secrets across 2,800+ domains. This represents a massive attack surface for credential stuffing and supply chain compromises, especially since 70% of leaked secrets from 2022 remain exploitable today. Time to check your git pre-commit hooks and repository scanning. [Public GitLab repositories exposed more than 17,000 secrets](https://www.bleepingcomputer.com/news/security/public-gitlab-repositories-exposed-more-than-17-000-secrets/)

**AI Models Vulnerable to Poetic Jailbreaking**  
Research shows converting malicious prompts into poetry achieves up to 90% jailbreak success rates against 25 major LLMs, including models from OpenAI, Google, and Anthropic. By embedding harmful instructions in verse, attackers bypass safety filters across CBRN, cyber-offense, and manipulation domains. This isn't just academic - it's a practical bypass for organizations relying on AI content moderation. [Prompt Injection Through Poetry](https://www.schneier.com/blog/archives/2025/11/prompt-injection-through-poetry.html)

## ⚠️ Vulnerabilities & Exploits

**FortiWeb Unauthenticated RCE in the Wild**  
The new FortiWeb RCE module chains CVE-2025-64446 and CVE-2025-58034 for pre-authenticated code execution. Given FortiWeb's prevalence in enterprise WAF deployments, this provides attackers a direct path behind perimeter defenses. Patch now if you haven't already. [Metasploit Wrap-Up 11/28/2025](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-11-28-2025)

**Flowise AI Platforms Under Active Attack**  
Two new RCE modules target Flowise AI platforms (CVE-2025-59528 and CVE-2025-8943), exploiting custom MCP and JS injection vulnerabilities. With Flowise's growing adoption for AI workflow automation, these exploits provide another avenue into AI/ML environments. [Metasploit Wrap-Up 11/28/2025](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-11-28-2025)

**iGEL OS Multiple Privilege Escalation Paths**  
Three new modules target iGEL OS endpoints, abusing SUID permissions in setup/date binaries for root access. Particularly relevant for organizations using thin clients in secure environments - these persistence mechanisms could survive OS reimages. [Metasploit Wrap-Up 11/28/2025](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-11-28-2025)

## 👤 Threat Actor Activity

**ShinyHunters Evolves into Ransomware-as-a-Service**  
The extortion group known for data theft is developing "ShinySp1d3r," their first in-house ransomware platform. This marks a dangerous evolution from pure data theft to encryption-based attacks, potentially combining their existing extortion tactics with destructive capabilities. [ShinyHunters Develop Sophisticated New Ransomware-as-a-Service Tool](https://gbhackers.com/ransomware-as-a-service-tool/)

**Holiday Scam Infrastructure Massively Scaled Up**  
Cybercriminals registered 18,000 new holiday-themed domains for seasonal phishing and scams. With Black Friday and Cyber Monday underway, expect sophisticated credential harvesting against retail employees and gift card fraud targeting consumers. [Cybercriminals Register 18,000 Holiday-Themed Domains to Launch Seasonal Scams](https://gbhackers.com/holiday-themed-domains/)

## 🛡️ Security Tools & Defenses

**GitGuardian's ML Delivers 3x Faster Alert Triage**  
GitGuardian's machine learning model for secret detection achieves 75% precision on critical alerts (vs. 15% for rules) while catching 72% of critical leaks. The system can safely auto-close 36.7% of low-risk incidents, helping security teams focus on what matters most. [How Machine Learning Transforms Security Alert Chaos into Actionable Intelligence](https://blog.gitguardian.com/how-machine-learning-transforms-security-alert-chaos-into-actionable-intelligence/)

**GreyNoise Launches Free IP Compromise Checker**  
GreyNoise released a simple web tool to check if your home network is part of a botnet. Useful for helping family members check their connections during holiday gatherings - though it won't fix the underlying infection, it's a first step toward awareness. [New GreyNoise IP Checker Helps Users Identify Botnet Activity](https://gbhackers.com/greynoise-ip-checker/)

## 📰 Industry Developments

**Microsoft Hardens Entra ID Against Script Injection**  
Microsoft is blocking external scripts during Entra ID logins as part of their Secure Future Initiative. This prevents malicious code injection on authentication pages, though some legitimate SSO integrations may need adjustments. [Microsoft Blocks External Scripts in Entra ID Logins to Boost Security](https://gbhackers.com/microsoft-blocks-external-scripts-in-entra-id-logins/)

**French Football Federation Falls to Compounded Credential**  
The FFF breach demonstrates that even sports organizations aren't immune - attackers used a compromised account to access administrative management software. A reminder that credential hygiene and MFA remain foundational defenses. [French Football Federation discloses data breach after cyberattack](https://www.bleepingcomputer.com/news/security/french-football-federation-fff-discloses-data-breach-after-cyberattack/)

**Windows Updates Hide Password Login Option**  
Microsoft acknowledged that recent Windows 11 updates may make the password sign-in option invisible on lock screens. The button still works if you can find it - another case of security features failing quietly. [Microsoft: Windows updates make password login option invisible](https://www.bleepingcomputer.com/news/microsoft/microsoft-windows-updates-hide-password-icon-on-lock-screen/)