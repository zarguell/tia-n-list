---
title: React2Shell RCE vulnerability 🔴, Marquis bank breach 💰, DragonForce cartel partnership 🤝, Windows LNK zero-day 🔗
date: 2025-12-04
tags: ["rce","ransomware","financial sector","apt groups","supply chain attack","insider threat","zero-day","vulnerability","threat actors","web applications"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: The React2Shell RCE vulnerability threatens millions of web applications while the DragonForce-Scattered Spider cartel partnership demonstrates an evolving ransomware model that combines social engineering expertise with encryption capabilities. Windows LNK zero-day exploitation and the Marquis bank breach highlight ongoing risks from legacy vulnerabilities and supply chain attacks targeting critical financial infrastructure.
---

# Daily Threat Intel Digest - 2025-12-04

## 🔴 Critical Threats

**React2Shell RCE Vulnerability Sparks Global Patch Rush**  
A critical vulnerability (CVE-2025-55182, CVSS 10) in React Server Components enables unauthenticated remote code execution, affecting apps even without explicit Server Functions usage. Researchers warn exploitation is "inevitable" given React's 82% adoption rate. Impacted frameworks include Next.js (CVE-2025-66478), React Router, and others. Fixed versions are available for react-server-dom packages (19.0.1+, 19.1.2+, 19.2.1+) and Next.js (15.0.5+, 16.0.7+). [Developers scramble as critical React flaw threatens major apps](https://cyberscoop.com/react-server-vulnerability-critical-severity-security-update/)  
*So What?* This is the next Log4Shell – act now if your stack uses React. Immediate patching is required for all servers supporting RSC, as default configurations are vulnerable.

**Marquis Breach Exposes 400k+ Bank Customers**  
Ransomware attack against financial software provider Marquis compromised data from 74 US banks/credit unions via SonicWall firewall exploitation. Stolen data includes SSNs, account numbers, and DOBs. Marquis paid ransom per reports, with Akira group likely responsible due to SonicWall VPN targeting tactics. New security controls include mandatory MFA and geo-IP filtering. [Marquis data breach impacts over 74 US banks, credit unions](https://www.bleepingcomputer.com/news/security/marquis-data-breach-impacts-over-74-us-banks-credit-unions/)  
*So What?* FI/CM teams: Verify Marquis customer notifications, monitor for fraud, and audit third-party vendor access controls. This breach highlights systemic risk in fintech supply chains.

## ⚠️ Vulnerabilities & Exploits

**Windows LNK Zero-Day "Mitigated" But Not Fixed**  
CVE-2025-9491, actively exploited by 11 APT groups since 2017, allows hiding malicious commands in .LNK files. Microsoft silently altered display behavior in Nov updates but didn't patch core issue. Unofficial 0patch available for EOL systems. [Microsoft "mitigates" Windows LNK flaw exploited as zero-day](https://www.bleepingcomputer.com/news/microsoft/microsoft-mitigates-windows-lnk-flaw-exploited-as-zero-day/)  
*So What?* This remains dangerous for social engineering attacks. Block .LNK attachments and implement detection for unusually long target paths in shortcuts.

**WordPress Plugins Under Active Attack**  
- King Addons for Elementor (CVE-2025-8489): Exploited in 48k+ attacks to create admin accounts. Patch to v51.1.35.  
- Advanced Custom Fields: Extended (CVE-2025-13486): Unauthenticated RCE in 0.9.0.5-0.9.1.1. Patch to v0.9.2.  
[Critical flaw in WordPress add-on for Elementor exploited in attacks](https://www.bleepingcomputer.com/news/security/critical-flaw-in-wordpress-add-on-for-elementor-exploited-in-attacks/)  
*So What?* WordPress admins: Audit plugins immediately. Active exploitation is ongoing against unpatched sites.

**Android Zero-Days Added to CISA KEV**  
CISA flagged CVE-2025-48572 and CVE-2025-48633 for active exploitation. Apply Android security updates urgently. [CISA Issues Alert on Actively Exploited Android Zero-Day Vulnerability](https://gbhackers.com/android-zero-day/)  
*So What?* Mobile security teams: Prioritize patching Android devices, especially in BYOD environments.

**VSCode Extension Supply Chain Attack**  
Malicious Prettier extension deployed Anivia Loader and OctoRAT via official marketplace. [Malicious VSCode Extension Deploys Anivia Loader and OctoRAT](https://gbhackers.com/vscode-extension/)  
*So What?* DevSecOps: Implement extension review policies. This demonstrates developer tool ecosystems as high-value targets.

## 👤 Threat Actor Activity

**Akhter Twins Charged in Gov Data Sabotage**  
Previously convicted hackers allegedly deleted 96 federal databases and stole IRS/EEOC data after being fired from contractor Opexus. Muneeb Akhter used AI for log destruction tactics. [Twins with hacking history charged in insider data breach affecting multiple federal agencies](https://cyberscoop.com/muneeb-sohaib-akhter-government-contractors-insider-attack/)  
*So What?* Insider threat programs: Reassess termination protocols for privileged users. Monitor AI-assisted anti-forensic techniques.

**DragonForce-Scattered Spider "Cartel" Emerges**  
RaaS operator partners with social engineering specialists for attacks like Marks & Spencer breach. Scattered Spider provides initial access via MFA fatigue/SIM swapping; DragonForce handles encryption. [Deep dive into DragonForce ransomware and its Scattered Spider connection](https://www.bleepingcomputer.com/news/security/deep-dive-into-dragonforce-ransomware-and-its-scattered-spider-connection/)  
*So What?* Defenders: Implement phishing-resistant MFA (FIDO2/WebAuthn) and monitor RMM tool deployments. This cartel model lowers barriers for attackers.

## 🛡️ Security Tools & Defenses

**Google Expands In-Call Scam Protection to US**  
Android now warns users when opening banking apps (Chase, Cash App) during screen sharing with unknown contacts. Pilot program blocks social engineering attacks. [Google expands Android scam protection feature to Chase, Cash App in U.S.](https://www.bleepingcomputer.com/news/security/google-expands-android-scam-protection-feature-to-chase-cash-app-in-us/)  
*So What?* Mobile security teams: Enable this feature for Android 11+ devices. It effectively disrupts vishing campaigns.

**Let's Encrypt Reduces Certificate Lifespan to 45 Days**  
Validity period shortens in 2026 to improve security, requiring automation. [Let’s Encrypt Cutting Certificate Lifespan from 90 Days to 45 Days](https://gbhackers.com/lets-encrypt-cutting-certificate-lifespan-from-90-days-to-45-days/)  
*So What?* DevOps: Prep for increased renewal frequency by implementing ACME automation now.

## 📰 Industry Developments

**Russia Blocks Roblox Over "Propaganda" Claims**  
Roskomnadzor restricted access for alleged LGBT content distribution amid broader app crackdowns. [Russia blocks Roblox over distribution of LGBT "propaganda"](https://www.bleepingcomputer.com/news/security/russia-blocks-roblox-over-distribution-of-lgbt-propaganda/)  
*So What?* International teams: Update geo-blocking policies for Russian users. Expect increased fragmentation of internet services.

**Clop's Oracle Zero-Day Campaign Continues**  
University of Phoenix latest victim in ongoing attacks on Oracle EBS. Extortion group has hit 100+ orgs since Aug 2025. [University of Phoenix discloses data breach after Oracle hack](https://www.bleepingcomputer.com/news/security/university-of-phoenix-discloses-data-breach-after-oracle-hack/)  
*So What?* Oracle EBS admins: Patch CVE-2025-61882 immediately and review EBS exposure logs. Clop systematically exploits unpatched instances.