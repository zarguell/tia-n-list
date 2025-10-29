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
  generation_method: intelligent
sources: ["krebs-on-security", "infosecurity-magazine", "securityweek", "bleeping-computer", "erev0scom-personal-blog-page", "cyberscoop"]
---

Good morning, cybersecurity professionals!

Tia N. List here with your daily threat intelligence briefing. I've been monitoring the threat landscape across 6 different security sources, and there are 24 articles worth your attention today.

Let's dive into what you need to know...

---


**Morning update from Tia N. List, Threat Intelligence Analyst**  
*October 29, 2025*

---

## Zero‑Day Vulnerabilities & Exploits

⚡ **DELMIA Factory Software** – Two actively exploited CVEs (CVE‑2025‑24893, CVE‑2025‑6204, CVE‑2025‑6205) are currently being leveraged by threat actors to compromise industrial control environments.  
- The CVE‑2025‑24893 vulnerability was reported in a recent XWiki incident where a malicious miner used the flaw to gain persistence on web servers.  
- CVE‑2025‑6204/6205 affect Dassault applications; the exploit chain involves remote code execution via malformed XML payloads.  

**Actionable steps**  
- **Patch immediately**: Deploy the latest vendor patches for DELMIA, XWiki, and Dassault products.  
- **Validate**: Run CVE‑check scanners to confirm remediation.  
- **Monitor**: Watch for unusual outbound traffic from affected IPs, especially to known malicious domains.

---

## Malware & Threat Actors

### PhantomRaven npm Campaign  
- A new wave of npm packages has been injected with credential‑stealing payloads.  
- Attackers are flooding the registry with “benign” modules that secretly exfiltrate API keys and user credentials.

### Npm Malware – Invisible Dependencies  
- Malicious code is hidden within dependencies that are not listed in `package.json`, making detection difficult for static analysis tools.  

### Qilin Ransomware  
- **File indicator**: `eskle.sys`  
- Qilin leverages Windows Subsystem for Linux (WSL) to run Linux‑based encryptors on Windows hosts, bypassing traditional antivirus heuristics.

**Actionable steps**  
- **Audit npm packages**: Verify the integrity of all dependencies; use lockfile checksums and publisher validation.  
- **Block unknown source URLs**: Configure npm to allow only trusted registries.  
- **Enable WSL monitoring**: Look for `eskle.sys` in system directories and block its execution.  
- **Update endpoint protection**: Ensure AV signatures are current and enable WSL filesystem scanning.

---

## Security Breaches & Incidents

| Incident | Impact | Immediate Action |
|----------|--------|------------------|
| **Dentsu – Merkle Data Breach** | Sensitive customer data exfiltrated from the Merkle subsidiary. | Notify affected parties, conduct forensic analysis, and strengthen access controls. |
| **DDR5 Memory Attack** | Attackers target DDR5 memory to steal keys from Intel and AMD TEEs. | Verify firmware updates for memory modules; monitor for unauthorized key extraction attempts. |
| **F5 Nation‑State Attack** | Prolonged attack reported; vendor claims limited impact. | Review F5 logs for anomalous traffic; verify that the latest security patches are applied. |
| **PHP & IoT Devices** | Growing cyber‑attack risks involving CVE‑2017‑9841, CVE‑2021‑3129, CVE‑2022‑47945. | Patch PHP installations, harden IoT device firmware, and isolate vulnerable devices. |
| **PhantomRaven npm Package Flood** | Credential‑stealing packages infiltrated npm registry. | Same as above in Malware section. |

---

## Vendor & Platform Updates

### Microsoft  
- **Windows Update Fix**: 0x800F081F error resolved, restoring normal update functionality.  
- **Windows 11 KB5067036**: Adds Administrator Protection feature – improves privilege escalation prevention.  
- **Media Creation Tool**: Broken on some Windows PCs – issue fixed; users should re‑install the tool.  

**Actionable steps**  
- **Apply latest Windows updates**: Ensure KB5067036

## 🎭 Intelligence Perspective

While analyzing serious threats, remember to maintain perspective:

_What do you get when you cross a bee and a sheep? A bah-humbug._

A balanced mindset leads to better decision-making.

---

## 📚 References

**Primary Sources:**

1. **Aisuru Botnet Shifts from DDoS to Residential Proxies**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://krebsonsecurity.com/2025/10/aisuru-botnet-shifts-from-ddos-to-residential-proxies/

2. **Npm Malware Uses Invisible Dependencies to Infect Dozens of Packages**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.infosecurity-magazine.com/news/npm-malware-invisible-dependencies/

3. **New Atroposia RAT Surfaces on Dark Web**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.infosecurity-magazine.com/news/new-atroposia-rat-surfaces-on-dark/

4. **CISA Warns of Exploited DELMIA Factory Software Vulnerabilities**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.securityweek.com/cisa-warns-of-exploited-delmia-factory-software-vulnerabilities/

5. **Qilin ransomware abuses WSL to run Linux encryptors in Windows**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.bleepingcomputer.com/news/security/qilin-ransomware-abuses-wsl-to-run-linux-encryptors-in-windows/

6. **PhantomRaven attack floods npm with credential-stealing packages**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.bleepingcomputer.com/news/security/phantomraven-attack-floods-npm-with-credential-stealing-packages/

7. **MITRE Unveils ATT&CK v18 With Updates to Detections, Mobile, ICS**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.securityweek.com/mitre-unveils-attck-v18-with-updates-to-detections-mobile-ics/

8. **PHP Servers and IoT Devices Face Growing Cyber-Attack Risks**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.infosecurity-magazine.com/news/php-servers-and-iot-devices-cyber/

9. **XWiki Vulnerability Exploited in Cryptocurrency Mining Operation**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.securityweek.com/xwiki-vulnerability-exploited-in-cryptocurrency-mining-operation/

10. **Ad and PR Giant Dentsu Says Hackers Stole Merkle Data**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.securityweek.com/ad-and-pr-giant-dentsu-says-hackers-stole-merkle-data/

11. **New Attack Targets DDR5 Memory to Steal Keys From Intel and AMD TEEs**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.securityweek.com/new-attack-targets-ddr5-memory-to-steal-keys-from-intel-and-amd-tees/

12. **CISA warns of two more actively exploited Dassault vulnerabilities**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.bleepingcomputer.com/news/security/cisa-warns-of-two-more-actively-exploited-dassault-vulnerabilities/

13. **Statistics from the Static and Dynamic analysis of more than 14,000 APKs from Play Store**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://erev0s.com/blog/statistics-from-the-static-and-dynamic-analysis-of-more-than-14000-apks-from-play-store/

14. **Microsoft fixes 0x800F081F errors causing Windows update failures**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.bleepingcomputer.com/news/microsoft/microsoft-fixes-0x800f081f-errors-causing-windows-update-failures/

15. **CyberRidge Emerges From Stealth With $26 Million for Photonic Encryption Solution**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.securityweek.com/cyberridge-emerges-from-stealth-with-26-million-for-photonic-encryption-solution/

16. **Advertising giant Dentsu reports data breach at subsidiary Merkle**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.bleepingcomputer.com/news/security/advertising-giant-dentsu-reports-data-breach-at-subsidiary-merkle/

17. **F5 asserts limited impact from prolonged nation-state attack on its systems**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://cyberscoop.com/f5-attack-limited-impact-earnings-call/

18. **AI Security Firm Polygraf Raises $9.5 Million in Seed Funding**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.securityweek.com/ai-security-firm-polygraf-raises-9-5-million-in-seed-funding/

19. **Chrome to Turn HTTPS on by Default for Public Sites**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.securityweek.com/chrome-to-turn-https-on-by-default-for-public-sites/

20. **Chrome to Make HTTPS Mandatory by Default in 2026**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.infosecurity-magazine.com/news/chrome-https-mandatory-2026/

21. **Visibility Gaps: Streamlining Patching and Vulnerability Remediation**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.bleepingcomputer.com/news/security/visibility-gaps-streamlining-patching-and-vulnerability-remediation/

22. **Windows 11 KB5067036 update rolls out Administrator Protection feature**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.bleepingcomputer.com/news/microsoft/windows-11-kb5067036-update-rolls-out-administrator-protection-feature/

23. **Microsoft fixes Media Creation Tool broken on some Windows PCs**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.bleepingcomputer.com/news/microsoft/microsoft-fixes-media-creation-tool-broken-on-some-windows-pcs/

24. **Open Source “b3” Benchmark to Boost LLM Security for Agents**
   - Source: Unknown (Relevance: 0/100)
   - URL: https://www.infosecurity-magazine.com/news/open-source-b3-benchmark-security/

---

*Sources analyzed: 24 articles*