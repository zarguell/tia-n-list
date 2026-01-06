---
title: Kimwolf Botnet expansion 🤖, WhatsApp OS leak 📱, ShinySp1d3r RaaS 💣, FortiWeb exploits 🔧
date: 2026-01-06
tags: ["botnet","metadata leak","ransomware","web application firewall","social engineering","malware","data breach","telecom sector","mobile security","proxy abuse"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: The Kimwolf Botnet has infected over 2 million devices through residential proxy networks, while WhatsApp vulnerabilities expose OS data for 3 billion users, creating mass surveillance opportunities. Scattered Lapsus$' new ShinySp1d3r RaaS platform targets high-revenue organizations, and compromised FortiWeb appliances enable persistent Sliver C2 frameworks for attackers.
---

# Daily Threat Intel Digest - January 6, 2026

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Kimwolf Botnet Abuses Residential Proxies to Infect 2M Devices**  
The Kimwolf botnet has expanded to over 2 million compromised devices by exploiting vulnerabilities in residential proxy networks like IPIDEA. Attackers hijack DNS configurations to tunnel into private networks, then target Android TV boxes and digital frames with unauthenticated ADB access. This enables DDoS attacks, ad fraud, and proxy service monetization. Researchers found infections concentrated in India, Brazil, US, and Russia, with two-thirds of compromised devices being unsecured Android hardware. Users should check IPs at [synthient.com/check](https://synthient.com/check) and avoid cheap streaming devices. [[Cyberpress](https://cyberpress.org/kimwolf-botnet/); [SecurityWeek](https://www.securityweek.com/kimwolf-android-botnet-grows-through-residential-proxy-networks/)]

**[NEW] WhatsApp Metadata Leak Exposes OS Data of 3B Users**  
Critical vulnerabilities in WhatsApp's E2EE protocol allow attackers to fingerprint users' operating systems without interaction. By querying encryption keys, threat actors can distinguish Android from iOS devices, enabling targeted zero-day exploitation. Meta partially mitigated the flaw by randomizing some key IDs but left One-Time PK IDs vulnerable. The lack of CVE assignment undermines coordinated defense. Organizations with executives using WhatsApp for communications should assume OS-level targeting is possible until comprehensive fixes arrive. [[Cyberpress](https://cyberpress.org/whatsapp-vulnerabilities/)]

**[NEW] Brightspeed Investigating Breach Affecting 1M+ Customers**  
ISP Brightspeed is probing claims by Crimson Collective that they stole data from over 1 million residential customers, including PII, payment details, and service records. The group, previously linked to Red Hat breaches, claims to have session/user IDs and appointment data. If confirmed, this represents a major telecom breach enabling credential stuffing and SIM-swapping attacks. Affected users should monitor for phishing and consider password resets. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/us-broadband-provider-brightspeed-investigates-breach-claims/); [SecurityWeek](https://www.securityweek.com/brightspeed-investigating-cyberattack/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Scattered Lapsus$ Hunters Launch ShinySp1d3r RaaS**  
The Scattered Lapsus$ collective has resurfaced with a ransomware-as-a-service platform called "ShinySp1d3r" and expanded insider recruitment. Targeting orgs with >$500M revenue, they offer 25% commissions for Active Directory access and 10% for cloud credentials. Discussions indicate structured clusters for social engineering and data theft, with explicit exclusions for Russian/Chinese targets. This escalation signals broader extortion capabilities beyond their prior telecom breaches. Defenders should audit privileged access and enhance insider threat monitoring. [[Cyberpress](https://cyberpress.org/shinysp1d3r-raas/)]

**[UPDATE] GravityRAT Adopts Multi-Platform Evasion Tactics**  
Pakistan-linked GravityRAT malware expanded to Windows, Android, and macOS with AI-like evasion: CPU temperature checks to detect VMs, steganography, and multi-language payloads (Python/.NET/Electron). Targeting Indian defense/government entities via phishing, it exfiltrates WhatsApp backups and SIM data. New persistence via scheduled tasks and dynamic C2 rotation complicates detection. Security teams should block macro documents and monitor for WMI temperature queries. [[Cyberpress](https://cyberpress.org/gravityrat-remote-access-attacks/)]

## ⚠️ Vulnerabilities & Patches

**[UPDATE] ClickFix Campaign Deploys Fake BSOD Screens**  
Attackers evolved ClickFix tactics with fake Windows Blue Screen prompts targeting European hospitality firms. Malicious Booking.com clones trick users into pasting PowerShell commands that compile DCRAT loaders via MSBuild. This social engineering bypasses EDR by forcing manual code execution. Organizations should train staff to recognize atypical error recovery steps and restrict MSBuild usage. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/clickfix-attack-uses-fake-windows-bsod-screens-to-push-malware/)]

**[NEW] FortiWeb Appliances Exploited for Sliver C2 Persistence**  
Outdated FortiWeb WAFs (v5.4.202–6.1.62) are being compromised to deploy Sliver C2 frameworks disguised as "system-updater." Attackers use Fast Reverse Proxy (FRP) and Microsocks for lateral movement, with persistence via systemd services. Thirty victims across Bangladesh, Pakistan, and the US beaconed to C2 servers posing as Ubuntu packages/Bangladesh Air Force sites. Immediate patching and network segmentation are critical. [[Cyberpress](https://cyberpress.org/fortiweb-sliver-c2-attack/)]

## 🛡️ Defense & Detection

**[NEW] Automated AD Disablement for Brute-Force Attacks**  
Open-source SOAR workflow using Wazuh, Graylog, and Shuffle SOAR can auto-disable Active Directory accounts after 8 failed logins within 240 seconds. The solution triggers LDAP-based account locking via FastAPI, reducing credential theft windows. Organizations struggling with brute-force alerts can implement this via [SOCFortress GitHub](https://github.com/socfortress/ACTIVE-DIRECTORY-RESPONSE). [[Medium](https://socfortress.medium.com/automating-active-directory-account-disablement-after-failed-login-attempts-wazuh-graylog-9b639f719632)]

## 📋 Policy & Industry News

**[NEW] Gmail Discontinues POP3 Mail Fetching**  
Google removed POP3-based email fetching and Gmailify features, disrupting unified inbox workflows. Users lose cross-provider spam protection and mobile notifications for linked accounts. Organizations must migrate to IMAP or email forwarding, though forwarding lacks security controls. Admins should update user guides to prevent mail flow disruptions. [[Cyberpress](https://cyberpress.org/gmail-to-discontinue-pop3-mail-fetching-for-external-email-accounts/)]

**[NEW] Ledger Customers Exposed in Global-e Breach**  
Hardware wallet maker Ledger disclosed that a third-party payment processor breach exposed customer PII. While no crypto assets were compromised, attackers may launch phishing campaigns targeting wallet recovery phrases. Users should verify transaction sources and enable Clear Sign. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ledger-customers-impacted-by-third-party-global-e-data-breach/)]