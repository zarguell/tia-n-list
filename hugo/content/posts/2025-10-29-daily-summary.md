---
title: Daily Threat Intelligence Briefing - October 29, 2025
date: 2025-10-29
tags: ["cybersecurity", "threat-intelligence", "daily-briefing"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Daily cybersecurity briefing covering 24 articles with 10 indicators of compromise
statistics:
  date: 2025-10-29
  total_articles: 24
  total_iocs: 10
  unique_sources: 6
  dynamic_title_used: False
  dynamic_tags_used: False
  intelligent_synthesis_used: True
sources: ["krebs-on-security", "infosecurity-magazine", "securityweek", "bleeping-computer", "erev0scom-personal-blog-page", "cyberscoop"]
generation_metadata:
  dynamic_title_used: False
  dynamic_tags_used: False
  intelligent_synthesis_used: True
  generated_tags_count: 0
---


The article contains multiple recent, actionable threat intelligence items—new botnet pivot, npm package infection vectors, a newly surfaced RAT, high‑severity CVEs, ransomware leveraging WSL, and an updated ATT&CK framework. These provide immediate value for incident response, vulnerability management, and threat hunting, making the content highly relevant to security professionals.

## 🎭 Intelligence Perspective

While analyzing serious threats, remember to maintain perspective:

_Have you ever heard of a music group called Cellophane? They mostly wrap._

A balanced mindset leads to better decision-making.

---

## 📚 References

**Primary Sources:**

1. **Aisuru Botnet Shifts from DDoS to Residential Proxies**
   - Source: Krebs on Security (Relevance: 92/100)
   - URL: https://krebsonsecurity.com/2025/10/aisuru-botnet-shifts-from-ddos-to-residential-proxies/

2. **Npm Malware Uses Invisible Dependencies to Infect Dozens of Packages**
   - Source: Infosecurity Magazine (Relevance: 90/100)
   - URL: https://www.infosecurity-magazine.com/news/npm-malware-invisible-dependencies/

3. **New Atroposia RAT Surfaces on Dark Web**
   - Source: Infosecurity Magazine (Relevance: 90/100)
   - URL: https://www.infosecurity-magazine.com/news/new-atroposia-rat-surfaces-on-dark/

4. **CISA Warns of Exploited DELMIA Factory Software Vulnerabilities**
   - Source: SecurityWeek (Relevance: 90/100)
   - URL: https://www.securityweek.com/cisa-warns-of-exploited-delmia-factory-software-vulnerabilities/

5. **Qilin ransomware abuses WSL to run Linux encryptors in Windows**
   - Source: Bleeping Computer (Relevance: 90/100)
   - URL: https://www.bleepingcomputer.com/news/security/qilin-ransomware-abuses-wsl-to-run-linux-encryptors-in-windows/

6. **PhantomRaven attack floods npm with credential-stealing packages**
   - Source: Bleeping Computer (Relevance: 85/100)
   - URL: https://www.bleepingcomputer.com/news/security/phantomraven-attack-floods-npm-with-credential-stealing-packages/

7. **MITRE Unveils ATT&CK v18 With Updates to Detections, Mobile, ICS**
   - Source: SecurityWeek (Relevance: 85/100)
   - URL: https://www.securityweek.com/mitre-unveils-attck-v18-with-updates-to-detections-mobile-ics/

8. **PHP Servers and IoT Devices Face Growing Cyber-Attack Risks**
   - Source: Infosecurity Magazine (Relevance: 85/100)
   - URL: https://www.infosecurity-magazine.com/news/php-servers-and-iot-devices-cyber/

9. **XWiki Vulnerability Exploited in Cryptocurrency Mining Operation**
   - Source: SecurityWeek (Relevance: 85/100)
   - URL: https://www.securityweek.com/xwiki-vulnerability-exploited-in-cryptocurrency-mining-operation/

10. **Ad and PR Giant Dentsu Says Hackers Stole Merkle Data**
   - Source: SecurityWeek (Relevance: 85/100)
   - URL: https://www.securityweek.com/ad-and-pr-giant-dentsu-says-hackers-stole-merkle-data/

11. **New Attack Targets DDR5 Memory to Steal Keys From Intel and AMD TEEs**
   - Source: SecurityWeek (Relevance: 85/100)
   - URL: https://www.securityweek.com/new-attack-targets-ddr5-memory-to-steal-keys-from-intel-and-amd-tees/

12. **CISA warns of two more actively exploited Dassault vulnerabilities**
   - Source: Bleeping Computer (Relevance: 85/100)
   - URL: https://www.bleepingcomputer.com/news/security/cisa-warns-of-two-more-actively-exploited-dassault-vulnerabilities/

13. **Statistics from the Static and Dynamic analysis of more than 14,000 APKs from Play Store**
   - Source: erev0s.com personal blog page (Relevance: 80/100)
   - URL: https://erev0s.com/blog/statistics-from-the-static-and-dynamic-analysis-of-more-than-14000-apks-from-play-store/

14. **Microsoft fixes 0x800F081F errors causing Windows update failures**
   - Source: Bleeping Computer (Relevance: 80/100)
   - URL: https://www.bleepingcomputer.com/news/microsoft/microsoft-fixes-0x800f081f-errors-causing-windows-update-failures/

15. **CyberRidge Emerges From Stealth With $26 Million for Photonic Encryption Solution**
   - Source: SecurityWeek (Relevance: 80/100)
   - URL: https://www.securityweek.com/cyberridge-emerges-from-stealth-with-26-million-for-photonic-encryption-solution/

16. **Advertising giant Dentsu reports data breach at subsidiary Merkle**
   - Source: Bleeping Computer (Relevance: 80/100)
   - URL: https://www.bleepingcomputer.com/news/security/advertising-giant-dentsu-reports-data-breach-at-subsidiary-merkle/

17. **F5 asserts limited impact from prolonged nation-state attack on its systems**
   - Source: CyberScoop (Relevance: 80/100)
   - URL: https://cyberscoop.com/f5-attack-limited-impact-earnings-call/

18. **AI Security Firm Polygraf Raises $9.5 Million in Seed Funding**
   - Source: SecurityWeek (Relevance: 75/100)
   - URL: https://www.securityweek.com/ai-security-firm-polygraf-raises-9-5-million-in-seed-funding/

19. **Chrome to Turn HTTPS on by Default for Public Sites**
   - Source: SecurityWeek (Relevance: 75/100)
   - URL: https://www.securityweek.com/chrome-to-turn-https-on-by-default-for-public-sites/

20. **Chrome to Make HTTPS Mandatory by Default in 2026**
   - Source: Infosecurity Magazine (Relevance: 70/100)
   - URL: https://www.infosecurity-magazine.com/news/chrome-https-mandatory-2026/

21. **Visibility Gaps: Streamlining Patching and Vulnerability Remediation**
   - Source: Bleeping Computer (Relevance: 70/100)
   - URL: https://www.bleepingcomputer.com/news/security/visibility-gaps-streamlining-patching-and-vulnerability-remediation/

22. **Windows 11 KB5067036 update rolls out Administrator Protection feature**
   - Source: Bleeping Computer (Relevance: 68/100)
   - URL: https://www.bleepingcomputer.com/news/microsoft/windows-11-kb5067036-update-rolls-out-administrator-protection-feature/

23. **Microsoft fixes Media Creation Tool broken on some Windows PCs**
   - Source: Bleeping Computer (Relevance: 60/100)
   - URL: https://www.bleepingcomputer.com/news/microsoft/microsoft-fixes-media-creation-tool-broken-on-some-windows-pcs/

24. **Open Source “b3” Benchmark to Boost LLM Security for Agents**
   - Source: Infosecurity Magazine (Relevance: 60/100)
   - URL: https://www.infosecurity-magazine.com/news/open-source-b3-benchmark-security/

---

*Sources analyzed: 24 articles*