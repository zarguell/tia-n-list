---
title: FortiGate SSO exploits 🚨, Okta vishing kits ☎️, ransomware expansion 💰, active RCE campaigns 🎯, storage flaws 🔓
date: 2026-01-23
tags: ["sso attacks","vishing","ransomware","rce","firewall security","email security","storage vulnerabilities","multi-sector targeting","operational security","phishing kits"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Enterprise authentication systems face sophisticated attacks as threat actors exploit FortiOS SSO vulnerabilities and deploy real-time vishing kits against Okta accounts, enabling rapid configuration theft and MFA bypass. Ransomware operations like Clop and Qilin continue expanding their multi-sector targeting while critical RCE flaws in SmarterMail, Cisco Unified Communications, and HPE storage systems enable unauthenticated remote access to enterprise infrastructure.
---

# Daily Threat Intel Digest - 2026-01-23

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] FortiGate Firewalls Targeted in Automated Attacks**  
Attackers are exploiting FortiOS SSO vulnerabilities (CVE-2025-59718/CVE-2025-59719) through highly automated campaigns that harvest complete firewall configurations within seconds. The operation involves creating persistent backdoor accounts like "secadmin" and "itadmin" after initial access via malicious service accounts (cloud-init@mail.io, cloud-noc@mail.io). Critical IOCs include IPs 104.28.244[.]115, 104.28.212[.]114, and 217.119.139[.]50. Patches may be insufficient as attackers have adapted techniques beyond the original CVEs. Organizations should immediately reset credentials, disable FortiCloud SSO, and restrict management access to trusted networks only [[Cyberpress](https://cyberpress.org/fortigate-firewalls-targeted/); [Arctic Wolf](https://arcticwolf.com/resources/blog/arctic-wolf-observes-malicious-configuration-changes-fortinet-fortigate-devices-via-sso-accounts/)].

**[NEW] Okta SSO Accounts Targeted in Sophisticated Vishing Campaigns**  
A new "as-a-service" phishing kit enables real-time voice-based attacks that bypass MFA through live session manipulation. Attackers impersonate IT support, spoof corporate numbers, and guide victims through fake authentication pages while simultaneously triggering real MFA challenges that appear legitimate. Once authenticated, attackers access integrated platforms like Microsoft 365, Salesforce, and Slack for data exfiltration. Active campaigns target financial and wealth management sectors. Implement phishing-resistant MFA (FIDO2/passkeys) and monitor for authentication anomalies [[BleepingComputer](https://www.bleepingcomputer.com/news/security/okta-sso-accounts-targeted-in-vishing-based-data-theft-attacks/); [Okta Advisory](https://www.okta.com/blog/threat-intelligence/phishing-kits-adapt-to-the-script-of-callers/)].

**[NEW] SmarterMail Auth Bypass Flaw Actively Exploited**  
Unauthenticated attackers are resetting administrator passwords on SmarterMail email servers through CVE-less vulnerability in the force-reset-password API endpoint. The flaw enables SYSTEM-level RCE after account hijacking. Exploitation began within days of the January 15 patch release, suggesting reverse-engineering of fixes. All SmarterMail deployments must immediately upgrade to Build 9511 and monitor for suspicious password reset activity [[BleepingComputer](https://www.bleepingcomputer.com/news/security/smartermail-auth-bypass-flaw-now-exploited-to-hijack-admin-accounts/); [watchTowr Analysis](https://labs.watchtowr.com/attackers-with-decompilers-strike-again-smartertools-smartermail-wt-2026-0001-auth-bypass/)].

**[NEW] Cisco Unified Communications RCE Under Active Exploitation**  
Cisco has patched CVE-2026-20045, a high-severity flaw in Unified Communications products allowing unauthenticated RCE via improper HTTP request validation. The vulnerability is being actively exploited in the wild. Organizations should immediately apply vendor patches while monitoring for unusual web management interface activity [[Arctic Wolf](https://arcticwolf.com/resources/blog/cve-2026-20045/); [Cisco Advisory](https://arcticwolf.com/resources/blog/cve-2026-20045/)].

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Clop and Qilin Ransomware Expand Multi-Sector Targeting**  
Both ransomware operations claimed numerous new victims on January 22 across diverse sectors. Clop targeted Canadian mining firm Eastplats, legal firm TOMLLAWYERS.COM, aerospace supplier ECA-USA.COM, and UK firm Warranty First Limited. Qilin struck Argentina's Proleasing, Sri Lanka's SiNetCon, and Paraguay's industrial machinery firm Copetrol. Both groups threaten data leaks unless negotiations occur. The campaigns demonstrate ongoing expansion beyond traditional high-value targets into regional industrial and professional services firms [[DeXpose Reports](https://www.dexpose.io/qilin-ransomware-attack-on-copetrol-in-paraguay/); [DeXpose Reports](https://www.dexpose.io/clop-ransomware-strikes-canadian-mining-firm-eastplats/)].

**[NEW] INC Ransomware Opsec Failure Enables Data Recovery**  
An operational security mistake exposed INC Ransomware's Restic backup infrastructure, allowing researchers to recover stolen data from 12 unrelated US organizations in healthcare, manufacturing, and technology sectors. The exposure revealed hardcoded repository credentials and encryption keys stored in PowerShell scripts. Organizations using Restic should monitor for unusual backup processes and implement detection rules for renamed binaries [[BleepingComputer](https://www.bleepingcomputer.com/news/security/inc-ransomware-opsec-fail-allowed-data-recovery-for-12-us-orgs/); [Cyber Centaurs Report](http://cybercentaurs.com/blog/infiltration-into-the-inc-ransomware-groups-infrastructure/)].

## ⚠️ Vulnerabilities & Patches

**[NEW] HPE Alletra and Nimble Storage Critical Privilege Escalation**  
CVE-2026-23594 (CVSS 8.8) allows remote attackers with low privileges to gain full administrative control on HPE Alletra 6000/5000 and Nimble Storage arrays. The flaw affects versions prior to 6.1.2.800 and 6.1.3.300. Administrators should immediately upgrade to patched versions (6.1.2.800/6.1.3.300) and review management interface access controls [[Cyberpress](https://cyberpress.org/hpe-alletra-and-nimble-storage-vulnerability-allows-remote-attackers-to-gain-admin-access/); [HPE Advisory](https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbst04995en_us&docLocale=en_US)].

## 🛡️ Defense & Detection

**[NEW] OWASP ZAP Integrates PenTest Kit for Authenticated Testing**  
The new OWASP ZAP add-on automatically installs the PenTest Kit browser extension in Chrome/Edge/Firefox, enabling security testing within authenticated sessions. The tool treats browser activity as authoritative, capturing real user flows for DAST/IAST/SAST/SCA analysis. This simplifies testing for modern SPAs and authenticated applications [[Cyberpress](https://cyberpress.org/zap-unveils-owasp-pentest-kit-browser/); [ZAP Blog](https://www.zaproxy.org/blog/2026-01-19-owasp-ptk-add-on/)].

**[NEW] Microsoft Teams Adds Brand Impersonation Warnings**  
Rolling out in mid-February, this feature will alert users to first-contact external callers attempting to impersonate trusted organizations. The protection engages by default and complements existing malicious URL detection and file type protections. Admins should update support materials to handle user inquiries about the new warnings [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-teams-to-add-brand-impersonation-warnings-to-calls/); [Microsoft Message Center](https://admin.microsoft.com/#/MessageCenter/:/messages/MC1219793)].

## 📋 Policy & Industry News

**[NEW] TSA-ICE Data Sharing Partnership Under Legal Challenge**  
American Oversight has sued the TSA and ICE for records about passenger data sharing used for immigration enforcement. The lawsuit challenges the legal basis for sharing domestic travel data without Privacy Act compliance. The program was previously implicated in the controversial deportation of a student at Logan Airport [[CyberScoop](https://cyberscoop.com/american-oversight-sues-tsa-ice-over-data-sharing-partnership-fight-records/); [NY Times Investigation](https://www.nytimes.com/2025/12/12/us/politics/immigration-tsa-passenger-data.html)].

**[NEW] Ransomware Leader Pleads Guilty to Four-Year Crime Spree**  
Russian national Ianis Antropenko admitted leading ransomware operations that targeted over 50 victims using Zeppelin and GlobeImposter variants. The case is notable for Antropenko committing crimes while residing in the US. Authorities seized over $3.4M in cryptocurrency and cash. The plea highlights increasing international cooperation against ransomware operators [[CyberScoop](https://cyberscoop.com/ianis-antropenko-russian-ransomware-leader-guilty/); [Court Documents](https://cyberscoop.com/wp-content/uploads/sites/3/2026/01/Antropenko-FactualResume-1-6-2026.pdf)].