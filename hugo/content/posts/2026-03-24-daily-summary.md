---
title: TeamPCP supply chain 📦, BYOVD tax malvertising 🎣, macOS/Android MaaS platforms 📱, critical software vulnerabilities 🔧
date: 2026-03-24
tags: ["supply chain attacks","byovd","stealer malware","maas","vulnerabilities","edr evasion","mobile malware","credential theft","developer tools","malvertising"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: TeamPCP attackers expanded their supply chain campaign to compromise Trivy images on Docker Hub and Checkmarx extensions, while threat actors leveraged BYOVD techniques through tax-themed malvertising to disable EDR platforms. MaaS providers simultaneously escalated operations with MioLab targeting macOS systems via ClickFix evasion and Oblivion RAT masquerading as Play Store updates on Android devices, alongside urgent patches for NetScaler, Roundcube, and Chrome vulnerabilities.
---
# Daily Threat Intel Digest - March 24, 2026

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] TeamPCP supply chain attack expands to Docker Hub and developer tools**
The ongoing TeamPCP supply chain campaign, initially identified yesterday via compromised GitHub Actions, has escalated with attackers pushing malicious images to Docker Hub and weaponizing the openVSX marketplace. Researchers confirmed that versions 0.69.5 and 0.69.6 of the popular Trivy security scanner on Docker Hub contain the TeamPCP infostealer, with the "latest" tag currently pointing to the compromised 0.69.6 build. Concurrently, threat actors published malicious versions of Checkmarx VS Code extensions (`ast-results-2.53.0.vsix` and `cx-dev-assist-1.7.0.vsix`) to openVSX, specifically targeting development environments to steal credentials, including GitHub Personal Access Tokens (PATs) and cloud secrets. Organizations must immediately rotate all CI/CD credentials, scan for indicators like `tpcp.tar.gz` or `payload.enc`, and revert to known-safe Trivy versions (e.g., 0.69.3) [[Cyber Security News](https://cyberpress.org/trivy-attack-hits-dockerhub/); [Checkmarx Blog](https://checkmarx.com/blog/checkmarx-security-update/)].

**[NEW] Tax-themed malvertising delivers BYOVD attack to blind EDRs**
A sophisticated malvertising campaign targeting U.S. taxpayers is weaponizing fake W-2 and W-9 tax form searches to deliver a "Bring Your Own Vulnerable Driver" (BYOVD) attack capable of neutralizing major endpoint detection and response (EDR) platforms. Attackers use commercial cloaking services to bypass Google Ads security scans, redirecting victims to a rogue ConnectWise ScreenConnect installer. Once installed, the payload—obfuscated by a multi-stage crypter named FatMalloc—drops a legitimate, signed Huawei audio driver (`HWAudioOs2Ec.sys`) which contains a vulnerability exploited by the "HwAudKiller" tool to terminate security processes from Microsoft Defender, SentinelOne, and Kaspersky. With defenses disabled, actors immediately dump LSASS memory for credentials and pivot laterally using tools like NetExec [[Cyber Security News](https://cyberpress.org/tax-ads-deploy-edr-killer/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] MioLab macOS stealer integrates ClickFix for evasion**
A commercial Malware-as-a-Service (MaaS) platform dubbed MioLab (aka Nova) has upgraded its capabilities to include ClickFix functionality, allowing it to bypass macOS Gatekeeper protections through sophisticated social engineering. The malware, heavily advertised on Russian-speaking forums, targets high-value macOS users—including software engineers and crypto investors—by generating fake system error dialogs and administrator password prompts to harvest credentials. The latest updates feature a command-and-control panel that automatically generates malicious Terminal commands for fake CAPTCHA pages, often distributed via cloned legitimate developer portals like Claude Code Docs. MioLab operators are also linking their infrastructure to Web3 Ethereum drainers to monetize residual traffic [[Cyber Security News](https://cyberpress.org/miolab-stealer-expands-tactics/)].

**[NEW] Oblivion RAT masquerades as Play Store updates on Android**
A new Android Remote Access Trojan (RAT) named Oblivion is being distributed via a polished $300/month MaaS platform that uses fake Google Play Store update sequences to trick users. The malware employs a multi-stage dropper that displays fabricated security scans and app listings to establish trust, ultimately requesting Accessibility Service permissions to gain deep system access. Once installed, Oblivion registers itself as the default messaging app to intercept SMS-based 2FA codes and includes a "wealth assessment" tool that categorizes installed banking and cryptocurrency apps to prioritize financial theft. The control panel allows operators to view the device screen in real-time and execute touch commands [[Cyber Security News](https://cyberpress.org/oblivion-rat-spreads-widely/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical NetScaler ADC flaws allow session hijacking**
Cloud Software Group has released security bulletins for two critical vulnerabilities, CVE-2026-3055 and CVE-2026-4368, affecting customer-managed NetScaler ADC and NetScaler Gateway appliances. These flaws could allow unauthenticated attackers to extract sensitive information from memory or gain unauthorized access to active user sessions. Given the role of these appliances in securing access to internal networks, administrators are urged to apply the available patches immediately to prevent potential session hijacking and data disclosure [[GBHackers](https://gbhackers.com/critical-netscaler-adc-and-gateway-flaws/)].

**[NEW] Roundcube Webmail patches critical security flaws**
The Roundcube project has released an urgent security update, version 1.6.14, to address eight distinct security vulnerabilities in its widely deployed webmail interface. While specific technical details are pending disclosure, the patch release is marked as urgent due to the platform's prevalence in processing sensitive corporate and personal communications. System administrators should prioritize updating to prevent potential exploitation of these flaws [[GBHackers](https://gbhackers.com/roundcube-releases-urgent-security-update/)].

**[NEW] Google Chrome fixes RCE vulnerabilities in latest update**
Google has patched eight high-severity vulnerabilities in its Chrome browser with the release of stable channel versions 146.0.7680.164 and 146.0.7680.165 for Windows, Mac, and Linux. The update addresses flaws that could enable remote code execution (RCE), prompting a recommendation for all users to update immediately to mitigate the risk of browser-based exploits [[GBHackers](https://gbhackers.com/chrome-security-update-fixes-8-vulnerabilities/)].

## 📋 Policy & Industry News

**[NEW] Google launches threat disruption unit at RSAC**
Google officially launched a new "Threat Disruption Unit" at the RSA Conference, signaling a shift toward proactive defense operations. While stopping short of "hacking back," the unit will leverage legal avenues, court orders, and technical control over Google infrastructure to dismantle adversary operations and block attack paths. The initiative aims to establish a standard of active disruption within the private sector, utilizing visibility into platforms abused by threat actors to cut off their resources before attacks can be launched [[Nextgov/FCW](https://www.nextgov.com/cybersecurity/2026/03/google-launches-threat-disruption-unit-stops-short-calling-it-offensive/412321/)].

**[NEW] NIST releases guide on cybersecurity workforce integration**
The National Institute of Standards and Technology (NIST) published Special Publication 1308, a quick-start guide designed to align cybersecurity risk management with enterprise workforce strategies. The guide addresses the need for organizations to dynamically adapt workforce capabilities to counter evolving cyber threats, bridging the gap between traditional HR functions and security operations [[GBHackers](https://gbhackers.com/nist-releases-quick-start-guide/)].