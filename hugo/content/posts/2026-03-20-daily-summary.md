---
title: IoT botnet takedown 🚫, SharePoint RCE exploitation 💥, Pyronut supply chain attack 🐍, Quest KACE compromise ⚠️, 2.7M data breach 🔓
date: 2026-03-20
tags: ["ddos","botnet","rce","supply chain attack","data breach","cisa kev","python malware","enterprise software","iot security","vulnerability exploitation"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: International authorities have neutralized four destructive IoT botnets that infected three million devices and generated massive DDoS attacks targeting defense networks. Active exploitation campaigns are targeting enterprise platforms including SharePoint servers and Quest KACE appliances, while a malicious Python package named Pyronut has backdoored Telegram developers through a supply chain attack.
---
# Daily Threat Intel Digest - 2026-03-20

**Good morning.** Today's briefing is dominated by a massive law enforcement takedown that has effectively neutralized the world's most powerful DDoS infrastructure, alongside a flurry of critical vulnerabilities being weaponized against enterprise platforms.

We are tracking active exploitation of SharePoint and Quest KACE appliances, a sophisticated supply chain attack targeting Python developers, and a significant data breach at a major benefits administrator.

Here is what you need to know to keep your network secure today.

***

## 🔴 Critical Threats & Active Exploitation

**[NEW] International Law Enforcement Dismantles 30+ Tbps IoT Botnets**
Authorities from the U.S., Germany, and Canada have seized the command-and-control (C2) infrastructure behind four of the most destructive IoT botnets in history: **Aisuru**, **KimWolf**, **JackSkid**, and **Mossad**. These botnets collectively infected over **three million devices**—including routers, DVRs, and web cameras—and were responsible for record-breaking Distributed Denial-of-Service (DDoS) attacks peaking at **31.4 Tbps**. The operation targeted the "cybercrime-as-a-service" model used by the operators, who leased access to these devices to other criminals for extortion campaigns. The disruption specifically targeted infrastructure used to attack U.S. Department of Defense networks, halting hundreds of thousands of active attack commands [[BleepingComputer](https://www.bleepingcomputer.com/news/security/aisuru-kimwolf-jackskid-and-mossad-botnets-disrupted-in-joint-action/); [KrebsOnSecurity](https://krebsonsecurity.com/2026/03/feds-disrupt-iot-botnet-behind-huge-ddos-attacks/); [Cyberpress](https://cyberpress.org/authorities-dismantle-iot-botnet-behind-massive-30-tbps-ddos-attacks/); [GBHackers](https://gbhackers.com/authorities-dismantle-iot-botnet/); [SecurityWeek](https://www.securityweek.com/aisuru-and-kimwolf-ddos-botnets-disrupted-in-international-operation/)].

**[NEW] Active Exploitation Detected in Microsoft SharePoint Deserialization Bug**
A critical deserialization vulnerability in Microsoft SharePoint, tracked as **CVE-2026-20963**, is being actively exploited in the wild to execute arbitrary code. The flaw affects SharePoint Server Subscription Edition, 2019, and 2016. CISA has added this vulnerability to its **Known Exploited Vulnerabilities (KEV)** catalog, requiring federal agencies to patch immediately. While specific threat actor attribution has not been confirmed, the addition to the KEV catalog signals reliable intelligence of active weaponization [[Malware.news](https://malware.news/t/actively-exploited-microsoft-sharepoint-deserialization-of-untrusted-data-vulnerability/105169#post_1)].

**[NEW] Pyronut Supply Chain Attack Backdoors Telegram Developers**
A malicious Python package named **"pyronut"** was discovered impersonating the popular "pyrogram" API framework to backdoor Telegram bot developers. Rather than simple typosquatting, the threat actors replicated the legitimate project's description verbatim and socially engineered victims via Telegram communities. The package stealthily imports a backdoor module that provides attackers with **Remote Code Execution (RCE)** capabilities via `/e` (code execution) and `/shell` (OS command) commands. Although the package was quarantined within hours of its March 18 publication, any developers who installed it must assume their local credentials, SSH keys, and environment variables are compromised [[Cyberpress](https://cyberpress.org/pyronut-backdoors-telegram-bots/)].

**[NEW] Arctic Wolf Observes Exploitation of Quest KACE SMA**
Arctic Wolf has detected malicious activity targeting unpatched **Quest KACE Systems Management Appliance (SMA)** instances exposed to the internet. The exploitation attempts leverage **CVE-2025-32975**, a vulnerability that was patched by the vendor in May 2025. Because KACE SMA holds elevated privileges for systems management, a successful compromise allows attackers to move laterally across the enterprise with significant ease. Organizations using this appliance should verify patching status immediately and scan for indicators of compromise [[Malware.news](https://malware.news/t/cve-2025-32975-arctic-wolf-observes-exploitation-of-quest-kace-systems-management-appliance/105153#post_1)].

**[NEW] Navia Benefit Solutions Confirms Data Breach Impacting 2.7 Million Users**
Navia Benefit Solutions disclosed a data breach exposing the sensitive personal and health information of **2.7 million individuals**. The breach was caused by a vulnerability in an **API endpoint** that allowed unauthorized read-only access to internal systems between December 22, 2025, and January 15, 2026. While no financial data or health claims were accessed, the exposed data includes full names, SSNs, dates of birth, and health plan participation details (FSA, HRA, COBRA), creating a high risk for targeted phishing and identity theft [[Cyberpress](https://cyberpress.org/navia-confirms-data-breach-exposing-sensitive-data-of-2-7-million-users/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/navia-discloses-data-breach-impacting-27-million-people/); [GBHackers](https://gbhackers.com/navia-confirms-data-breach/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] FBI Seizes Infrastructure of Pro-Iranian Handala Group**
Following the group's destructive wiper attack on Stryker earlier this week, the FBI has seized two websites associated with the **Handala** threat group, including their primary leak site. Handala, a pro-Iranian hacktivist group, recently utilized Microsoft Intune privileges to wipe data from approximately 80,000 devices. The seizure disrupts their ability to publicly extort victims or leak stolen data [[Security Boulevard](https://malware.news/t/fbi-seizes-two-websites-linked-to-pro-iranian-group-handala/105152#post_1)].

**[NEW] Open Directory Leak Exposes Iran-Linked Botnet Infrastructure**
Researchers at Hunt.io discovered an exposed file manager on an Iranian staging server that revealed a **15-node relay network** and a custom botnet framework. The discovery exposes the operational security failures of a threat actor using Farsi-language code comments and targeting gaming servers with DDoS tools. The infrastructure, which included 7 servers hosted on Hetzner in Finland, appears to be operated by a financially motivated individual rather than a state-sponsored entity, providing rare insight into the development of commercial censorship-evasion and attack tools [[Cyberpress](https://cyberpress.org/iran-botnet-relay-exposed/)].

**[NEW] Malicious Open VSX Extension Drops RAT via GitHub**
The "fast-draft" extension on the Open VSX registry has been weaponized to distribute a Remote Access Trojan (RAT) and information stealer. The malicious versions (0.10.89, 0.10.105, 0.10.106, 0.10.112) execute a shell script during editor startup that fetches a payload from a GitHub user named "BlokTrooper." The resulting malware grants attackers full remote desktop control, including mouse movement, keystroke logging, and file stealing, specifically targeting developer tools and AI coding environments like Cursor and Claude [[Cyberpress](https://cyberpress.org/open-vsx-drops-malware/)].

**[NEW] Insider Worker Convicted in $2.5 Million Extortion Scheme**
Cameron Curry, a former data analyst contractor, was found guilty of six counts of extortion for stealing sensitive corporate data from Brightly Software (Siemens). After his contract ended, Curry used the stolen payroll and compensation data to demand **$2.5 million** in ransom, threatening to release the information to employees and the SEC. Operational security failures, including linking personal Coinbase accounts to his mother and sister's debit cards, allowed authorities to quickly identify him [[BleepingComputer](https://www.bleepingcomputer.com/news/security/data-analyst-found-guilty-of-extorting-brightly-software-of-25-million/); [Cyberscoop](https://cyberscoop.com/cameron-curry-insider-attack-washington-tech-company/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] Atlassian Bamboo Patched Against Critical RCE Flaw**
Atlassian has released a fix for a high-severity **Remote Code Execution (RCE)** vulnerability, tracked as **CVE-2026-21570**, affecting Bamboo Data Center and Server. As a central hub for CI/CD pipelines, a compromise in Bamboo could allow attackers to inject malicious code into software builds, poisoning the software supply chain. Administrators are urged to apply the update immediately [[GBHackers](https://gbhackers.com/bamboo-data-center-and-server-vulnerability/)].

**[NEW] Jenkins Faces Multiple Security Flaws (RCE, Credential Theft)**
The Jenkins project released an advisory addressing multiple vulnerabilities in its core automation server and the LoadNinja plugin. The flaws expose CI/CD environments to severe risks including arbitrary file creation, credential exposure, and RCE. Given Jenkins controllers often hold elevated privileges, unpatched instances serve as high-value targets for initial access brokers [[GBHackers](https://gbhackers.com/new-critical-jenkins-vulnerabilities/)].

**[NEW] "PolyShell" Bug Allows Unauthenticated RCE on Magento Stores**
Researchers have disclosed "PolyShell," a new vulnerability affecting all Magento Open Source and Adobe Commerce version 2 installations. The flaw allows **unauthenticated code execution** or account takeover by uploading a polyglot file that behaves as both an image and a script. While no active exploitation has been confirmed yet, exploit methods are circulating, and a full patch is not yet available for production versions. Store administrators are advised to restrict access to the `pub/media/custom_options/` directory immediately [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-polyshell-flaw-allows-unauthenticated-rce-on-magento-e-stores/)].