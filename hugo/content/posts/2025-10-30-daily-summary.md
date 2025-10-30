---
title: Daily Threat Intelligence Briefing - October 30, 2025
date: 2025-10-30
tags: ["cve-2022-47945", "cve-2021-3129", "cve-2024-3721", "cve-2022-22947", "zero-day", "remote-code-execution", "botnet", "spyware", "mirai", "google", "amazon", "government"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Daily cybersecurity briefing covering 25 articles with 12 indicators of compromise
statistics:
  date: 2025-10-30
  total_articles: 25
  total_iocs: 12
  unique_sources: 7
  dynamic_title_used: False
  dynamic_tags_used: True
  intelligent_synthesis_used: True
  generated_tags_count: 12
sources: ["infosecurity-magazine", "krebs-on-security", "bleeping-computer", "securityweek", "qualys-security-blog", "cyberscoop", "erev0scom-personal-blog-page"]
generation_metadata:
  dynamic_title_used: False
  dynamic_tags_used: True
  intelligent_synthesis_used: True
  generated_tags_count: 12
---


Thursday, October 30, 2025 — Security Briefing

---

### Emerging Malware & Botnets

- ⚡ **Atroposia RAT**: A newly surfaced modular Remote Access Trojan (RAT) named *Atroposia* is making waves on underground forums. It offers a comprehensive toolkit including hidden remote desktop takeover (HRDP Connect), credential and cryptocurrency wallet theft, DNS hijacking, local vulnerability scanning, and fileless data exfiltration. Communication with command-and-control (C2) servers is encrypted to evade detection. The RAT automates privilege escalation and persistence, enabling long-term stealthy access. It is marketed affordably, lowering the skill barrier for attackers. Notably, it integrates well with other criminal toolkits like SpamGPT (AI-driven phishing automation) and MatrixPDF (weaponized PDFs) — demonstrating the increasing commoditization of sophisticated cybercrime tools[1][2][3][4].

- 🔥 **PhantomRaven NPM Malware Campaign**: An active malware campaign dubbed PhantomRaven is exploiting npm’s package ecosystem using an advanced technique called Remote Dynamic Dependencies (RDD). This allows malicious code to be loaded dynamically from attacker-controlled servers during installation, bypassing npm’s security scans. Over 126 malicious npm packages have been identified, collectively downloaded more than 86,000 times, with at least 80 still active as of October 29. The malware steals credentials including npm tokens, GitHub credentials, and CI/CD secrets from Windows, Linux, and macOS developers globally. This campaign underlines ongoing supply chain risks in open-source ecosystems[8].

- ⚡ **Aisuru Botnet Pivot**: The Aisuru botnet, previously infamous for record-breaking DDoS attacks, has shifted focus to monetizing residential proxy services. This pivot enables attackers to rent out compromised residential IPs, supporting anonymity and evasion in subsequent attacks. This operational change indicates a diversification in botnet monetization strategies and may increase proxy-related abuse in threat landscapes.

---

### Vulnerabilities & Exploits

- 🔥 **CISA Warnings on Dassault DELMIA Vulnerabilities**: The Cybersecurity and Infrastructure Security Agency (CISA) issued urgent advisories about two actively exploited high-severity vulnerabilities in Dassault Systèmes’ DELMIA Factory Software:  
  - CVE-2025-6204  
  - CVE-2025-6205  
  These vulnerabilities allow remote code execution and privilege escalation, posing critical risks to manufacturing environments and supply chains depending on DELMIA. Immediate patching and mitigation are strongly recommended.

- ⚡ **XWiki RCE Exploitation for Cryptomining**: The critical remote code execution vulnerability CVE-2025-24893 in the SolrSearch macro of XWiki has been exploited in cryptocurrency mining operations. Attackers leverage this flaw to deploy mining malware on compromised servers, degrading performance and increasing operational costs.

- ⚡ **WordPress Plugin Data Exposure**: The Anti-Malware Security and Brute-Force Firewall WordPress plugin suffers from vulnerability CVE-2025-11705, which exposes private data to site subscribers. This flaw could allow unauthorized access to sensitive information, escalating risks in WordPress-based environments.

- ⚡ **Qilin Ransomware Abuses Windows Subsystem for Linux (WSL)**: The Qilin ransomware group has innovated by running Linux-based encryptors on Windows systems via WSL, complicating detection and forensic analysis. This cross-platform technique enhances ransomware stealth and evasion capabilities.

- ⚡ **New Physical Attack on DDR5 Memory TEEs**: Researchers from Purdue University and Georgia Tech unveiled *TEE.fail*, a novel physical attack targeting Trusted Execution Environments (TEEs) in Intel and AMD processors by exploiting DDR5 memory vulnerabilities. This attack can extract cryptographic keys, seriously threatening hardware-level security assumptions.

---

### Breaches & Insider Threats

- ⚡ **Massive Data Exposure: Proton Breach Data**: Over 300 million records tied to nearly 800 data breaches have been identified by researchers analyzing Proton-related compromises this year. The scale signals ongoing data aggregation and resale risks impacting a broad range of enterprises and individuals.

- ⚡ **Ex-Defense Contractor Guilty Plea for Zero-Day Sales to Russia**: A former U.S. defense contractor executive pleaded guilty to stealing and selling zero-day vulnerabilities to Russian cyber brokers. This insider threat case highlights ongoing risks in sensitive sectors where zero-days are weaponized against national security and critical infrastructure.

- ⚡ **Dentsu/Merkle Data Breach**: The Japanese advertising giant Dentsu disclosed a breach affecting its subsidiary Merkle, where attackers accessed confidential corporate data. Details remain limited, but this incident emphasizes continued targeting of marketing and PR firms for intellectual property and customer data.

- 🔥 **Canadian Infrastructure Hacktivist Breach**: Canadian authorities confirmed hacktivist intrusions into multiple critical water and energy facilities. Although the extent and impact remain under investigation, this signals increasing hacktivist interest and capability in critical infrastructure sectors.

---

### Advisory & Industry Updates

- **Google Chrome HTTPS Mandate**: Starting October 2026, Google Chrome will enforce HTTPS by default for all websites, improving baseline web security and pushing site operators to adopt encrypted communications.

- **MITRE ATT&CK v18 Released**: The latest ATT&CK framework version 18 introduces updated detection methods, analytics, and expanded coverage for mobile and Industrial Control Systems (ICS), aiding defenders in adapting to evolving TTPs.

- **Surge in PHP and IoT Exploits**: Automated attacks targeting PHP servers and IoT devices are increasing, often involving botnets exploiting known vulnerabilities and weak configurations. Security teams should prioritize patching and network segmentation for these assets.

---

### What Matters Today

- **Immediately patch CVE-2025-6204 and CVE-2025-6205 in Dassault DELMIA** to prevent exploitation in manufacturing and supply chain environments.

- **Audit npm package usage and implement supply chain security controls** to mitigate risks from PhantomRaven and similar malware campaigns leveraging invisible remote dependencies.

- **Monitor for Atroposia RAT activity and related plug-and-play criminal toolkits** by enhancing detection of encrypted C2 traffic, privilege escalation attempts, and DNS hijacking behavior.

- **Assess exposure to insider threats and zero-day vulnerabilities** in sensitive sectors, reinforcing insider risk programs and vulnerability management.

- **Prepare for Chrome’s HTTPS enforcement** by ensuring all web assets support HTTPS to avoid disruptions in late 2026.

---

This briefing consolidates actionable intelligence from the past 24 hours, emphasizing new threats and critical vulnerabilities requiring immediate attention.

## 🎭 Intelligence Perspective

While analyzing serious threats, remember to maintain perspective:

_What do you call a thieving alligator? A crookodile!_

A balanced mindset leads to better decision-making.

---

## 📚 References

**Primary Sources:**

1. **New Atroposia RAT Surfaces on Dark Web**
   - Source: Infosecurity Magazine (Relevance: 92/100)
   - URL: https://www.infosecurity-magazine.com/news/new-atroposia-rat-surfaces-on-dark/

2. **Aisuru Botnet Shifts from DDoS to Residential Proxies**
   - Source: Krebs on Security (Relevance: 92/100)
   - URL: https://krebsonsecurity.com/2025/10/aisuru-botnet-shifts-from-ddos-to-residential-proxies/

3. **Proton Claims 300 Million Records Compromised So Far This Year**
   - Source: Infosecurity Magazine (Relevance: 90/100)
   - URL: https://www.infosecurity-magazine.com/news/proton-300-million-records/

4. **Defense Contractor Boss Pleads Guilty to Selling Zero-Day Exploits to Russia**
   - Source: Infosecurity Magazine (Relevance: 90/100)
   - URL: https://www.infosecurity-magazine.com/news/defense-contractor-guilty-selling/

5. **PhantomRaven attack floods npm with credential-stealing packages**
   - Source: Bleeping Computer (Relevance: 90/100)
   - URL: https://www.bleepingcomputer.com/news/security/phantomraven-attack-floods-npm-with-credential-stealing-packages/

6. **Npm Malware Uses Invisible Dependencies to Infect Dozens of Packages**
   - Source: Infosecurity Magazine (Relevance: 90/100)
   - URL: https://www.infosecurity-magazine.com/news/npm-malware-invisible-dependencies/

7. **CISA Warns of Exploited DELMIA Factory Software Vulnerabilities**
   - Source: SecurityWeek (Relevance: 90/100)
   - URL: https://www.securityweek.com/cisa-warns-of-exploited-delmia-factory-software-vulnerabilities/

8. **Qilin ransomware abuses WSL to run Linux encryptors in Windows**
   - Source: Bleeping Computer (Relevance: 90/100)
   - URL: https://www.bleepingcomputer.com/news/security/qilin-ransomware-abuses-wsl-to-run-linux-encryptors-in-windows/

9. **What Security Teams Need to Know as PHP and IoT Exploits Surge**
   - Source: Qualys Security Blog (Relevance: 85/100)
   - URL: https://blog.qualys.com/category/vulnerabilities-threat-research

10. **Malicious NPM packages fetch infostealer for Windows, Linux, macOS**
   - Source: Bleeping Computer (Relevance: 85/100)
   - URL: https://www.bleepingcomputer.com/news/security/malicious-npm-packages-fetch-infostealer-for-windows-linux-macos/

11. **Canada says hacktivists breached water and energy facilities**
   - Source: Bleeping Computer (Relevance: 85/100)
   - URL: https://www.bleepingcomputer.com/news/security/canada-says-hacktivists-breached-water-and-energy-facilities/

12. **Ex-L3Harris exec pleads guilty to selling zero-day exploits to Russian broker**
   - Source: CyberScoop (Relevance: 85/100)
   - URL: https://cyberscoop.com/peter-williams-guilty-selling-zero-day-exploits-russian-broker-operation-zero/

13. **Chrome to Make HTTPS Mandatory by Default in 2026**
   - Source: Infosecurity Magazine (Relevance: 85/100)
   - URL: https://www.infosecurity-magazine.com/news/chrome-https-mandatory-2026/

14. **MITRE Unveils ATT&CK v18 With Updates to Detections, Mobile, ICS**
   - Source: SecurityWeek (Relevance: 85/100)
   - URL: https://www.securityweek.com/mitre-unveils-attck-v18-with-updates-to-detections-mobile-ics/

15. **PHP Servers and IoT Devices Face Growing Cyber-Attack Risks**
   - Source: Infosecurity Magazine (Relevance: 85/100)
   - URL: https://www.infosecurity-magazine.com/news/php-servers-and-iot-devices-cyber/

16. **XWiki Vulnerability Exploited in Cryptocurrency Mining Operation**
   - Source: SecurityWeek (Relevance: 85/100)
   - URL: https://www.securityweek.com/xwiki-vulnerability-exploited-in-cryptocurrency-mining-operation/

17. **Ad and PR Giant Dentsu Says Hackers Stole Merkle Data**
   - Source: SecurityWeek (Relevance: 85/100)
   - URL: https://www.securityweek.com/ad-and-pr-giant-dentsu-says-hackers-stole-merkle-data/

18. **New Attack Targets DDR5 Memory to Steal Keys From Intel and AMD TEEs**
   - Source: SecurityWeek (Relevance: 85/100)
   - URL: https://www.securityweek.com/new-attack-targets-ddr5-memory-to-steal-keys-from-intel-and-amd-tees/

19. **CISA warns of two more actively exploited Dassault vulnerabilities**
   - Source: Bleeping Computer (Relevance: 85/100)
   - URL: https://www.bleepingcomputer.com/news/security/cisa-warns-of-two-more-actively-exploited-dassault-vulnerabilities/

20. **WordPress security plugin exposes private data to site subscribers**
   - Source: Bleeping Computer (Relevance: 80/100)
   - URL: https://www.bleepingcomputer.com/news/security/wordpress-security-plugin-exposes-private-data-to-site-subscribers/

21. **Statistics from the Static and Dynamic analysis of more than 14,000 APKs from Play Store**
   - Source: erev0s.com personal blog page (Relevance: 80/100)
   - URL: https://erev0s.com/blog/statistics-from-the-static-and-dynamic-analysis-of-more-than-14000-apks-from-play-store/

22. **Visibility Gaps: Streamlining Patching and Vulnerability Remediation**
   - Source: Bleeping Computer (Relevance: 80/100)
   - URL: https://www.bleepingcomputer.com/news/security/visibility-gaps-streamlining-patching-and-vulnerability-remediation/

23. **CyberRidge Emerges From Stealth With $26 Million for Photonic Encryption Solution**
   - Source: SecurityWeek (Relevance: 80/100)
   - URL: https://www.securityweek.com/cyberridge-emerges-from-stealth-with-26-million-for-photonic-encryption-solution/

24. **Advertising giant Dentsu reports data breach at subsidiary Merkle**
   - Source: Bleeping Computer (Relevance: 80/100)
   - URL: https://www.bleepingcomputer.com/news/security/advertising-giant-dentsu-reports-data-breach-at-subsidiary-merkle/

25. **F5 asserts limited impact from prolonged nation-state attack on its systems**
   - Source: CyberScoop (Relevance: 80/100)
   - URL: https://cyberscoop.com/f5-attack-limited-impact-earnings-call/

---

*Sources analyzed: 25 articles*