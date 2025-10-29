---
title: 🏢 Microsoft Security Issues Widespread in Latest Intelligence - October 29, 2025
date: 2025-10-29
tags: ["cvss", "remote-code-execution", "ddos", "phishing", "malware", "botnet", "microsoft", "google", "government", "technology", "manufacturing", "critical"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Daily cybersecurity briefing covering 24 articles with 10 indicators of compromise
statistics:
  date: 2025-10-29
  total_articles: 24
  total_iocs: 10
  unique_sources: 6
  dynamic_title_used: True
  dynamic_tags_used: True
  intelligent_synthesis_used: True
  generated_tags_count: 12
sources: ["krebs-on-security", "infosecurity-magazine", "securityweek", "bleeping-computer", "erev0scom-personal-blog-page", "cyberscoop"]
generation_metadata:
  dynamic_title_used: True
  dynamic_tags_used: True
  intelligent_synthesis_used: True
  generated_tags_count: 12
---


Wednesday, October 29, 2025 — Security Briefing

---

### Vulnerabilities & Exploits

- ⚡ **CISA issues urgent warnings on two actively exploited Dassault Systèmes DELMIA factory software vulnerabilities**: CVE-2025-6204 and CVE-2025-6205 are high-severity flaws enabling remote code execution. These have been observed in targeted attacks impacting manufacturing environments, posing risks to industrial operations and supply chains. Mitigation through immediate patching is critical[1].

- 🔥 **XWiki critical RCE exploited in cryptocurrency mining campaign**: The recently disclosed CVE-2025-24893, a remote code execution vulnerability in the SolrSearch macro of XWiki, is actively exploited by threat actors to deploy crypto-mining malware on compromised servers, increasing risks of resource hijacking and lateral movement in enterprise networks.

- **PHP servers and IoT devices face intensified attacks from botnets like Mirai**: Qualys reports a surge in automated exploitation attempts targeting PHP web servers and IoT devices, leveraging known vulnerabilities for botnet recruitment, which exacerbates risks for web infrastructure and IoT ecosystems.

- **New physical attack on DDR5 memory exposes Intel and AMD Trusted Execution Environments (TEEs)**: University researchers disclosed "TEE.fail," a side-channel technique to extract cryptographic keys from DDR5 memory modules, undermining hardware-based security assurances in modern CPUs. While requiring physical access, this attack threatens hardware trust models.

---

### Malware & Botnets

- ⚡ **Aisuru Botnet pivots from record-breaking DDoS attacks to residential proxy rental model**: Operators of the Aisuru botnet, infamous for volumetric attacks exceeding 20 Tbps, have shifted focus to monetizing compromised IoT devices as residential proxies. This evolution enables cybercriminals to anonymize traffic for fraud, credential stuffing, and large-scale AI data scraping, generating millions in underground revenue. The botnet now controls over 700,000 IoT systems worldwide, complicating detection due to legitimate-appearing proxy traffic[1][2][3][4][5][6].

- 🔥 **PhantomRaven npm malware campaign escalates with 126 malicious packages**: Koi Security uncovered that PhantomRaven injects credential-stealing payloads via invisible dependencies in npm packages. These packages automatically download ransomware and steal sensitive developer credentials, significantly increasing supply chain risks in JavaScript ecosystems.

- **Atroposia RAT emerges on the dark web offering encrypted communications**: A new remote access trojan surfaced, providing operators with encrypted command-and-control channels and stealthy persistence. This malware poses a threat to targeted espionage and data exfiltration campaigns.

- **Qilin ransomware abuses Windows Subsystem for Linux (WSL) to run Linux encryptors on Windows hosts**: This innovative technique allows Qilin operators to deploy Linux-based encryptors stealthily on Windows systems, complicating detection and mitigation efforts in enterprise environments.

---

### Breaches & Incidents

- **Dentsu confirms data breach at Merkle subsidiary**: The Japan-based advertising giant disclosed unauthorized access affecting Merkle’s systems, involving theft of sensitive data. The breach forced the shutdown of some network operations while investigations continue. This incident highlights persistent targeting of marketing and ad-tech sectors.

- **F5 Networks reports limited impact from prolonged nation-state intrusion**: Despite a persistent attack compromising some customer configuration data, F5 asserts limited operational impact. Still, this incident underscores ongoing nation-state interest in high-value network infrastructure providers.

---

### Advisories & Industry Updates

- **MITRE releases ATT&CK v18 with expanded detection and analytic techniques**: The update enhances coverage for mobile, industrial control systems (ICS), and modern detection strategies, providing defenders with refined models to identify adversary behaviors more accurately.

- **Google Chrome to enable HTTPS by default for public sites starting October 2026**: The upcoming Chrome 154 release will enforce "Always Use Secure Connections," making HTTPS mandatory to enhance user privacy and security on the web. Organizations should prepare to avoid mixed content issues and ensure full HTTPS compliance.

- **Microsoft fixes 0x800F081F Windows 11 update errors**: A recent patch resolves language pack-related failures in Windows 11 24H2 updates, improving system stability and update success rates.

- **CyberRidge introduces photonic encryption for data-in-transit protection**: Emerging tech firm CyberRidge secured $26 million in funding to develop quantum-resistant photonic encryption solutions aimed at mitigating interception risks in sensitive communications.

---

### What Matters Today

1. **Patch DELMIA CVE-2025-6204 and CVE-2025-6205 immediately**—these factory software vulnerabilities are actively exploited and pose critical risks to industrial control environments.

2. **Review and restrict proxy usage in your networks**—with Aisuru’s shift to residential proxy rentals, malicious traffic is increasingly masked as legitimate user activity. Use behavioral analytics and endpoint detection to identify anomalous proxy traffic from IoT devices.

3. **Audit npm package dependencies for PhantomRaven infection signs** and tighten supply chain security practices, including dependency vetting and integrity verification, to prevent credential theft and malware deployment.

4. **Prepare for Chrome’s HTTPS enforcement** by auditing and migrating all public-facing web properties to HTTPS ahead of October 2026 to ensure uninterrupted service and compliance.

---

This briefing synthesizes critical developments within the last 24 hours to keep your defenses current and actionable. Stay vigilant.

## 🎭 Intelligence Perspective

While analyzing serious threats, remember to maintain perspective:

_Knock knock. 
 Who's there? 
 A broken pencil. 
 A broken pencil who? Never mind. It's pointless._

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