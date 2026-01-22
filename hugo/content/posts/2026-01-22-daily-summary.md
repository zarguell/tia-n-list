---
title: Cisco zero-day 🚨, Fortinet SSO bypass 🔓, AI cloud takeover ☁️, LastPass phishing 🎣, Infrastructure ransomware 💥
date: 2026-01-22
tags: ["zero-day exploitation","authentication bypass","cloud vulnerabilities","phishing campaigns","ransomware","critical infrastructure","sso attacks","ai security","cisco vulnerabilities","fortinet attacks"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Critical zero-day vulnerabilities in Cisco Unified Communications and Fortinet SSO are being actively exploited to gain root access and create unauthorized admin accounts, enabling full system compromise. Attackers are simultaneously targeting cloud environments through AI framework flaws and conducting sophisticated phishing campaigns against LastPass users while TheGentlemen ransomware group escalates attacks on energy and automotive sectors.
---

# Daily Threat Intel Digest - 2026-01-22

## 🔴 Critical Threats & Active Exploitation

**[NEW] Critical Cisco Unified Communications Zero-Day Exploited for Root Access**  
Attackers are actively exploiting CVE-2026-20045, a critical RCE vulnerability in Cisco Unified Communications Manager, Unity Connection, and Webex Calling platforms, enabling unauthenticated remote command execution with root privilege escalation. The flaw stems from improper HTTP request validation in web-based management interfaces, affecting versions prior to 12.5, 14, and 15. CISA has added this to its KEV catalog with a Feb 11 remediation deadline for federal agencies, while Cisco has released patches and confirms active exploitation enables full system compromise and lateral movement. [[Cisco Advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-voice-rce-mORhqY4b)]; [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisco-fixes-unified-communications-rce-zero-day-exploited-in-attacks/)]

**[NEW] Fortinet SSO Authentication Bypass Bypasses Patches**  
Attackers are exploiting CVE-2025-59718, a critical FortiCloud SSO authentication flaw, to create unauthorized admin accounts even on patched FortiGate firewalls running FortiOS 7.4.9/7.4.10. Malicious SSO logins from IP 104.28.244.114 create persistent "helpdesk" accounts, with Shadowserver tracking ~11,000 exposed devices. Fortinet confirms 7.4.11 will fully address the flaw; admins should immediately disable `admin-forticloud-sso-login` via CLI as a temporary workaround. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fortinet-admins-report-patched-fortigate-firewalls-getting-hacked/)]; [Arctic Wolf](https://arcticwolf.com/resources/blog/arctic-wolf-observes-malicious-configuration-changes-fortinet-fortigate-devices-via-sso-accounts/)]

**[NEW] AI Framework Vulnerabilities Enable Cloud Takeover**  
Two critical flaws in Chainlit (CVE-2026-22218: Arbitrary File Read; CVE-2026-22219: SSRF), deployed across ~700k monthly PyPI downloads, allow unauthenticated cloud credential theft and lateral movement. Attackers exploit `/project/element` to read sensitive files (e.g., `/proc/self/environ`) and SSRF to access AWS IMDSv1 metadata, leaking keys for storage buckets and LLM services. Version 2.9.4 patches these flaws, but thousands of enterprise deployments remain at immediate risk. [[Cyberpress](https://cyberpress.org/critical-chainlit-ai-vulnerabilities/)]; [BleepingComputer](https://www.bleepingcomputer.com/news/security/chainlit-ai-framework-bugs-let-hackers-breach-cloud-environments/)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] LastPass Phishing Campaign Targets Master Passwords**  
Since Jan 19, attackers have sent spoofed "urgent vault backup" emails from addresses like `support@lastpass.server8`, redirecting users to `mail-lastpass.com` to steal master passwords. Leveraging compromised AWS S3 infrastructure (52.95.155.90) and timing with the US holiday weekend, this campaign bypasses security awareness by exploiting LastPass branding. LastPass confirms it never requests master passwords via email. [[LastPass Blog](https://blog.lastpass.com/posts/new-phishing-campaign-targeting-lastpass-customers/)]; [BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-lastpass-emails-pose-as-password-vault-backup-alerts/)]

**[NEW] TheGentlemen Ransomware Targets Energy, Auto Sectors**  
TheGentlemen group claims dual attacks: Rola Motor Group (South Africa) on Jan 20 and Sincere Corporation (Japan, environmental services) on Jan 21, threatening data leaks without ransom demands. These escalate the group’s multi-sector extortion spree, emphasizing critical infrastructure targeting. Sectors should monitor for data leak posts and validate backups. [[DeXpose](https://www.dexpose.io/thegentlemen-ransomware-attack-on-rola-motor-group/)]

**[NEW] Zendesk Spam Wave Abuses Open Ticket Policies**  
A global spam campaign exploits unverified Zendesk support ticket submissions to send mass emails from major brands (Discord, Dropbox, Tinder). Attackers abuse Zendesk’s automated responses to bypass filters using bizarre subjects (e.g., "FREE DISCORD NITRO!!"). Zendesk has deployed new safety features, but affected organizations must restrict ticket creation to verified users. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/zendesk-ticket-systems-hijacked-in-massive-global-spam-wave/)]

## ⚠️ Vulnerabilities & Patches

**[NEW] WordPress Plugin Backdoor Enables Admin Account Creation**  
A backdoor in LA-Studio Element Kit (≤v1.5.6.3, 20k+ sites) allows unauthenticated administrator account creation via `lakit_bkrole` parameter. Added by a terminated employee, CVE-2026-09220 (CVSS 9.8) enables full site compromise. Patched in v1.6.0; Wordfence users protected since Jan 13. [[Wordfence](https://www.wordfence.com/blog/2026/01/20000-wordpress-sites-affected-by-backdoor-vulnerability-in-la-studio-element-kit-for-elementor-wordpress-plugin/)]

**[NEW] HPE Storage Arrays Vulnerable to RCE**  
HPE Alletra 5000/6000 and Nimble Storage arrays expose a privilege escalation flaw (HPESBST04995) in OS versions <6.1.2.800. Attackers could achieve remote code execution via unauthenticated network access. Immediate patching to 6.1.3.300/6.1.2.800 is critical. [[Canadian Cyber Centre](https://cyber.gc.ca/en/alerts-advisories/hpe-security-advisory-av26-046)]

**[NEW] Atlassian Products Patched in Bulletin Wave**  
Atlassian fixed multiple RCE and privilege flaws across Bamboo, Bitbucket, Confluence, Crowd, Jira, and Jira Service Management. Crowd versions 7.1.0-7.1.2 and 6.3.0-6.3.3 are particularly affected. Apply patches immediately to prevent exploitation. [[Atlassian Advisory](https://confluence.atlassian.com/security/security-bulletin-january-20-2026-1712324819.html)]

## 🛡️ Defense & Detection

**[NEW] ANY.RUN-MISP Integration Accelerates Malware Triage**  
A new MISP module enables direct sample submission to ANY.RUN sandbox, returning enriched IOCs, MITRE ATT&CK mappings, and behavioral evidence without tool-switching. This reduces MTTR for evasive malware by integrating automated interactivity (e.g., clicking, file opening) to trigger delayed threats. [[ANY.RUN Blog](https://any.run/cyber-security-blog/anyrun-sandbox-misp-integration/)]

**[NEW] Sandfly 5.6 Automates Linux Drift Detection**  
Sandfly Security’s agentless drift detection now automatically identifies novel threats in Linux environments, detecting unauthorized changes without endpoint agents. Enhances coverage for stealthy persistence tactics. [[Sandfly Blog](https://sandflysecurity.com/blog/sandfly-5-6-automatic-drift-detection/)]

## 📋 Policy & Industry News

**[NEW] GCVE Launches as Decentralized Vulnerability Tracker**  
The Global CVE Allocation System (GCVE), maintained by Luxembourg’s CIRCL, offers an alternative to MITRE’s CVE program. Using independent numbering authorities (e.g., GCVE-0-2023-40224 for CVE-2023-40224), it addresses CVE’s funding fragility with decentralized ID allocation while maintaining backward compatibility. [[CyberScoop](https://cyberscoop.com/gcve-vulnerability-database-launches/)]

**[NEW] CISA Staffing Cuts Scrutinized by Lawmakers**  
House Homeland Security Committee pressed acting CISA director Madhu Gottumukkala over 998 employee departures (30% workforce reduction) since Jan 2025. Democrats highlighted weakened defenses, while Republicans claimed efficiency gains. No formal staffing analysis was provided. [[CyberScoop](https://cyberscoop.com/cisa-madhu-gottumukkala-house-homeland-hearing-workforce-staffing-levels/)]