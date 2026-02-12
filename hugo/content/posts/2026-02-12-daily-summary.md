---
title: Palo Alto firewall exploits 🔥, Apple zero-day attacks 📱, DragonForce RaaS expansion 💣, AI promptware hijacking 🤖, supply chain compromises 🔄
date: 2026-02-12
tags: ["firewall vulnerabilities","zero-day exploitation","ransomware-as-a-service","ai security","supply chain attacks","credential theft","threat actors","timing attacks","malware frameworks","active exploitation"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical Palo Alto Networks firewall flaws and Apple zero-day vulnerabilities are being actively exploited against enterprise infrastructure and high-value targets, enabling device compromise and forced reboots. The DragonForce ransomware-as-a-service operation expands through cartel-style alliances while emerging promptware techniques hijack AI assistants for espionage, highlighting the convergence of ransomware ecosystems and AI-driven attack vectors.
---

# Daily Threat Intel Digest - 2026-02-12

## 🔴 Critical Threats & Active Exploitation
**[NEW] Palo Alto Networks firewall flaw enables forced reboot loops**  
Unauthenticated attackers are exploiting CVE-2026-0229, a medium-severity flaw in PAN-OS's Advanced DNS Security feature, to trigger repeated reboots or maintenance-mode crashes in firewalls. The vulnerability requires only network access and ADNS enabled with block/sinkhole settings, affecting thousands of enterprise perimeter devices. Palo Alto urges immediate upgrades for vulnerable versions, as no configuration mitigations exist [[CyberPress](https://cyberpress.org/palo-alto-networks-firewall-vulnerability/); [GBHackers](https://gbhackers.com/palo-alto-networks-firewall-vulnerability/)].  

**[NEW] Apple zero-day CVE-2026-20700 actively exploited in targeted attacks**  
A critical dyld memory corruption flaw is being weaponized in "extremely sophisticated" campaigns against high-value individuals like activists and journalists. The vulnerability enables arbitrary code execution via malicious apps or web content, chaining with older flaws (e.g., CVE-2025-14174) for full device compromise. iOS/iPadOS 26.3 patches address this alongside fixes for WebKit UAF, kernel escalation, and Bluetooth/Wi-Fi flaws [[CyberPress](https://cyberpress.org/apple-zero-day-vulnerability-actively-exploited-in-sophisticated-targeted-attacks/); [GBHackers](https://gbhackers.com/apple-0-day-flaw-actively-exploited/)].  

**[NEW] Malicious Outlook add-in steals 4,000 credentials via supply chain hijack**  
Attackers compromised the dormant "AgreeTo" add-in by seizing its expired domain (outlook-one.vercel.app), injecting a fake Microsoft login page to harvest credentials, credit cards, and emails. Since Microsoft only validates manifests at submission, the hijack required no new approvals, exposing a critical supply chain risk. Koi AI identified 4,000+ compromised accounts before takedown [[CyberPress](https://cyberpress.org/malicious-microsoft-outlook-add-in-stole-4000-account-credentials-and-credit-card-details/); [GBHackers](https://gbhackers.com/microsoft-outlook-add-in-stolen-4000-accounts/)].  

## 🎯 Threat Actor Activity & Campaigns  
**[NEW] DragonForce ransomware escalates with 363 victims and cartel-style RaaS**  
Operating since December 2023, DragonForce has expanded its ransomware-as-a-service model via "RansomBay" tools, targeting 363 organizations across 36 countries. The group uses LockBit 3.0-derived code, BYOVD techniques, and extortion tactics like "Harassment Calling," while forming alliances with Qilin and LockBit. Activity peaked in December 2025 with 35 victims, showing evolution toward ecosystem-driven influence [[Malware.News](https://malware.news/t/inside-the-ecosystem-operations-dragonforce/104064#post_1)].  

## ⚠️ Vulnerabilities & Patches  
**[NEW] Adblock filter flaw exposes VPN users' real locations via timing attacks**  
Dubbed "Adbleed," this technique exploits country-specific adblocker lists (e.g., EasyList Germany) to identify users despite VPN encryption. Attackers use JavaScript probes to test blocked domains, with timing differences (blocked requests <30ms vs. unblocked 50-500ms) revealing locale. Combining this with fingerprinting achieves 95%+ location accuracy. Mitigations include disabling regional lists or randomizing filters, though at the cost of reduced ad-blocking [[CyberPress](https://cyberpress.org/adblock-filter-flaw/); [GBHackers](https://gbhackers.com/adblock-filters-expose-user-location/)].  

## 🛡️ Defense & Detection  
**[NEW] Promptware attack hijacks AI assistants to spy via Zoom**  
Attackers weaponize Google Calendar invites with malicious prompts to force AI assistants (e.g., Google Assistant) to launch Zoom and stream camera feeds to attacker servers without user interaction. The 7-stage "Promptware Kill Chain" automates escalation from calendar entry to C2, exploiting overly permissive AI permissions. Defenders should sanitize input, limit camera access, and audit AI actions [[CyberPress](https://cyberpress.org/promptware-attack-lets-hackers-weaponize-google-calendar-invites-to-spy-via-zoom-camera/); [GBHackers](https://gbhackers.com/promptware-hackers-exploit-google-calendar-invites/)].  

**[NEW] VoidLink framework enables on-demand Linux malware creation**  
UAT-9921 operators deploy this cloud-native malware using AI-assisted development, with Zig-based cores and C/Go plugins for on-demand compilation. VoidLink detects EDR tools, adapts scans, and uses mesh P2P C2 to bypass firewalls. Observed since September 2025 against tech/finance victims, it highlights AI's role in accelerating attack tooling [[CyberPress](https://cyberpress.org/voidlink-transforms-tool-creation/)].  

## ⚡ Quick Hits  
- **WordPress plugin bug:** CVE-2026-1357 in WPvivid Backup Plugin exposes 800,000+ sites to RCE via file upload [[GBHackers](https://gbhackers.com/wordpress-backup-plugin-vulnerability/)].  
- **SSH botnet resurgence:** SSHStalker propagates via brute-force attacks, using IRC C2 and legacy exploits on outdated Linux hosts [[CyberPress](https://cyberpress.org/irc-botnet-exploits-ssh/)].  
- **Lazarus Graphalgo campaign:** North Korean group targets GitHub/npm/PyPI with fake recruiter lures to deliver cryptocurrency-focused malware [[GBHackers](https://gbhackers.com/lazarus-groups-graphalgo/)].