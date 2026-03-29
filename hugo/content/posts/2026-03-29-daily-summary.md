---
title: TeamPCP supply chain 🔗, Infinity Stealer macOS 🍎, Handala FBI breach 🕵️, EdTech healthcare attacks 🏥
date: 2026-03-29
tags: ["supply chain attack","infostealer","macos malware","apt activity","clickfix","ransomware","data breach","edtech security","healthcare sector","iran apt"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: TeamPCP's PyPI supply chain attack has entered a monetization phase while the Infinity Stealer campaign uses advanced ClickFix evasion to steal macOS credentials and keychain data. The Iran-linked Handala group compromised an FBI Director's email and multiple EdTech and healthcare organizations suffered data breaches, highlighting ongoing credential theft and sector-specific targeting risks.
---
# Daily Threat Intel Digest - March 29, 2026

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] TeamPCP supply chain campaign shifts to monetization phase**
The ongoing TeamPCP PyPI supply chain attack has transitioned from initial compromise to monetization, with intelligence indicating no new victims have been reported in the last 48 hours. This operational tempo shift suggests the threat actors are now focusing on exploiting the access they have already established—likely by deploying ransomware via their Vect partnership or selling credentials—rather than expanding their foothold. Security teams running compromised packages (such as `Telnyx` or `LiteLLM`) should assume that if they haven't detected lateral movement yet, the attackers are likely attempting to cash out on existing infections rather than probing new entry points [[SANS Diary](https://isc.sans.edu/diary/rss/32842)].

**[NEW] Infinity Stealer targets macOS users with advanced ClickFix evasion**
A new infostealer campaign dubbed "Infinity Stealer" is actively targeting macOS users using a sophisticated attack chain that combines "ClickFix" social engineering with Python malware compiled via the Nuitka compiler. By using Nuitka to convert Python payloads into native binaries, the malware achieves significantly higher resistance to static analysis compared to standard PyInstaller bundles. The attack tricks users into pasting a base64-encoded curl command into their terminal via a fake Cloudflare CAPTCHA, ultimately delivering a payload capable of stealing macOS Keychain entries, browser credentials, cryptocurrency wallets, and plaintext `.env` developer files. This campaign represents a notable escalation in macOS threat capabilities, moving beyond simple scripts to harder-to-detect native binaries [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-infinity-stealer-malware-grabs-macos-data-via-clickfix-lures/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Handala hack of FBI Director's email confirmed non-classified**
Following yesterday's report that the Iran-linked group Handala breached FBI Director Kash Patel's personal email, the FBI has confirmed that the exposed material consists of old, personal data and does not involve any government or classified information. While this reduces the immediate national security risk, the successful compromise of a high-profile target's personal Gmail underscores the effectiveness of the group's credential-gathering operations and highlights the ongoing blurred lines between state-sponsored operations and personal account targeting [[DataBreaches via Malware.news](https://databreaches.net/2026/03/28/iran-linked-group-handala-hacked-fbi-director-kash-patels-personal-email-account/)].

**[NEW] Infinite Campus breach analysis reveals lower data sensitivity**
An independent analysis of the data leaked by ShinyHunters following the Infinite Campus breach indicates that the exposure is less severe than initially feared. While the attackers claimed to have breached the EdTech provider, the downloaded tranche consists primarily of directory information rather than highly sensitive non-directory student data. This finding provides some relief to affected educational institutions, though IT teams should still remain vigilant against potential phishing attacks leveraging the exposed contact details [[DataBreaches via Malware.news](https://databreaches.net/2026/03/28/thankfully-the-infinite-campus-incident-did-not-involve-a-lot-of-non-directory-student-information/)].

## 📋 Policy & Industry News

**[NEW] Anthropic confirms leak of 'Claude Mythos' model details**
AI firm Anthropic has officially confirmed a leak involving its upcoming "Claude Mythos" model, originally uncovered by a Fortune report. The breach exposed internal details regarding the powerful new model's release, representing an intelligence disclosure rather than a direct compromise of user safety data or model weights [[DataBreaches via Malware.news](https://databreaches.net/2026/03/28/meet-claude-mythos-leaked-anthropic-post-reveals-the-powerful-upcoming-model/)].

**[NEW] Corewell Health notifies patients of 2024 vendor breach**
Corewell Health is notifying thousands of patients that their data was compromised in a 2024 breach involving Pinnacle Holdings, a former healthcare consulting vendor. The notification highlights the long tail of third-party risk, as the organization is only now disclosing the impact of an incident that occurred nearly a year ago [[DataBreaches via Malware.news](https://databreaches.net/2026/03/28/thousands-of-corewell-health-patients-affected-by-security-breach/)].

**[NEW] Woodfords Family Services discloses 2024 ransomware attack**
Woodfords Family Services, a Maine-based support provider for people with disabilities, has issued a notice regarding a ransomware attack discovered on April 8, 2024. The organization has completed its review and is currently notifying patients and families about the scope of the data exfiltrated during the incident [[DataBreaches via Malware.news](https://databreaches.net/2026/03/28/woodfords-family-services-notifying-patients-and-families-by-2024-ransomware-attack/)].