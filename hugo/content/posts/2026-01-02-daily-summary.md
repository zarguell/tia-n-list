---
title: Healthcare data breaches 🏥, medical device hijacking 🦽, Careto APT resurfaces 🎭, GlassWorm macOS malware 💻, critical software flaws 🐛
date: 2026-01-02
tags: ["healthcare sector","data breach","medical devices","apt activity","malware campaigns","macos security","software vulnerabilities","iot security","bluetooth attacks"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Healthcare organizations face dual threats with the Cognizant-TriZetto breach exposing patient data for nearly a year and WHILL wheelchairs vulnerable to remote hijacking via Bluetooth. The Careto APT group has resurfaced with novel email server exploits while GlassWorm malware expands to macOS targeting developers through malicious VSCode extensions and hardware wallets.
---

# Daily Threat Intel Digest - 2026-01-02

## 🔴 Critical Threats & Active Exploitation

**[NEW] Cognizant faces lawsuits after 11-month TriZetto breach**  
Hackers accessed Cognizant's healthcare subsidiary TriZetto starting November 2024, but the intrusion wasn't discovered until October 2025, exposing patient data including SSNs and financial records for nearly a year. Three class-action lawsuits allege negligence and delayed notification, with plaintiffs claiming Cognizant failed to implement standard security controls. The prolonged detection window puts affected individuals at high risk of identity theft, as the healthcare sector remains a prime target for data theft due to the sensitivity of patient information [[Cyber Press](https://cyberpress.org/rizetto-data-breach/)]. Healthcare entities using TriZetto services should immediately review access logs and notify potentially compromised patients.

**[NEW] WHILL wheelcars vulnerable to remote hijacking**  
CISA issued a critical advisory for WHILL Model C2 electric wheelchairs and Model F power chairs, warning attackers within Bluetooth range can take control without authentication. The flaw (CVE-2025-14346, CVSS 9.8) allows unexpected movement changes or sudden stops via unauthenticated Bluetooth commands. Healthcare facilities and wheelchair users should disable Bluetooth when not actively using companion apps and restrict physical access near devices. No patch was available at advisory publication [[Cyber Press](https://cyberpress.org/whill-model-c2-wheelchair-vulnerabilities/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Careto APT resurfaces with novel server abuse tactics**  
The Careto group (aka "The Mask"), inactive for a decade, has been active since 2019 with new techniques including compromising MDaemon email servers via WorldClient webmail component exploits. Attackers used malicious configuration parameters to deploy persistent backdoors and employ the FakeHMP implant via abused HitmanPro Alert drivers for keylogging and data theft. The group targets government agencies and research institutions, showing evolved TTPs while retaining toolset artifacts [[Cyber Press](https://cyberpress.org/careto-hacker-group/); [GBHackers](https://gbhackers.com/careto-hacker-group/)]. Organizations should investigate email server logs for unusual CGI execution and monitor driver abuse.

**[UPDATE] GlassWorm malware expands to macOS with hardware wallet targeting**  
The fourth GlassWorm campaign now targets macOS developers via malicious VSCode extensions, shifting from Windows-only attacks. The malware uses AES-encrypted JavaScript to replace hardware wallet apps (Ledger Live, Trezor Suite) with trojanized versions while stealing Keychain passwords. Over 33,000 installations of three malicious OpenVSX extensions are reported. Developers should uninstall `studio-velte-distributor.pro-svelte-extension`, `cudra-production.vsce-prettier-pro`, and `Puccin-development.full-access-catppuccin-pro-extension`, rotate credentials, and reinstall macOS [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-glassworm-malware-wave-targets-macs-with-trojanized-crypto-wallets/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] GNU Wget2 vulnerability enables arbitrary file overwrite**  
A high-severity flaw (CVE-2025-69194, CVSS 8.8) in Wget2's Metalink processing allows path traversal attacks via malicious filenames. Attackers can overwrite system files or inject malware by tricking users into downloading crafted Metalink documents. All automated download systems using Wget2 should update immediately and avoid untrusted Metalink sources [[Cyber Press](https://cyberpress.org/critical-gnu-wget2-vulnerability-allows-remote-attackers-to-overwrite-sensitive-files/)].

**[NEW] Apache NuttX RTOS bug enables remote system crashes**  
A memory corruption flaw (CVE-2025-48769) in NuttX's file rename function allows remote attackers to crash embedded devices with network-exposed filesystems (e.g., FTP servers). The "Use After Free" error affects versions 7.20 through 12.10.x, potentially causing kernel panics on IoT devices. Organizations must upgrade to NuttX 12.11.0, prioritizing devices with writable network file services [[Cyber Press](https://cyberpress.org/apache-nuttx-flaw/); [GBHackers](https://gbhackers.com/apache-nuttx-flaw-attackers-to-crash-embedded-systems/)].