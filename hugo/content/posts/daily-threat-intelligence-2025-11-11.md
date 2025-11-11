+++
title = "Malware Dominate Latest Threat Intelligence - November 11, 2025"
date = "2025-11-11"
tags = ["threat-intelligence", "daily-digest", "cybersecurity", "cloud native security palo alto networks blog", "security affairs securityaffairs co", "revista de ciberseguridad y seguridad de la informacin para empresas y organismos pblicos ciberseguridadpyme es", "gbhackers security 1 globally trusted cyber security news platform gbhackers com"]
categories = ["Threat Intelligence"]
summary = "Daily threat intelligence digest covering 17 recent security developments."
draft = false
author = "Tia N. List"
lastmod = "2025-11-11T11:22:39.999945"
sources = ["cloud-native-security-palo-alto-networks-blog", "security-affairs-securityaffairs-co", "revista-de-ciberseguridad-y-seguridad-de-la-informacin-para-empresas-y-organismos-pblicos-ciberseguridadpyme-es", "security-affairs-securityaffairs-co", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com"]
+++

# Daily Threat Intelligence Digest – November 11, 2025  

The cyber‑security landscape continues to evolve at a brisk pace, with threat actors exploiting software flaws, expanding their toolkits, and refining social‑engineering tactics. The fresh intelligence released today paints a vivid picture of how attackers are leveraging both technical weaknesses and human psychology to compromise targets across a wide range of sectors. Below is a focused look at the most consequential developments and what they mean for defenders today.  

---

## 1. Samsung’s Zero‑Day RCE: A Mobile Front in a Global Campaign  

The U.S. Cybersecurity and Infrastructure Security Agency (CISA) has added the Samsung mobile‑device flaw CVE‑2025‑21042 to its Known Exploited Vulnerabilities (KEV) catalog. The vulnerability, a remote‑code‑execution (RCE) bug in the libimagecodec library, was actively abused months before Samsung patched it in April. Palo Alto Networks’ Unit 42 researchers linked the exploit to a sophisticated spyware campaign dubbed *LANDFALL*, which uses malicious DNG image files sent via WhatsApp to target Samsung Galaxy devices in the Middle East.  

Key points:  
- The flaw is rated CVSS 8.8, indicating a high risk to affected devices.  
- Attackers can install spyware that records audio, tracks location, and steals data without any user interaction.  
- The exploit is part of a broader pattern of similar mobile‑platform vulnerabilities, underscoring the need for rapid patch management and mobile‑device‑management (MDM) controls.  

Actionable advice: Keep all Samsung devices updated, especially those running the affected image‑processing library. Deploy an MDM solution that enforces the latest OS patches and monitors for anomalous outbound traffic that could indicate a compromised device.  

---

## 2. Triofox’s “Un‑auth” Bug Goes Live: Remote‑Access Tool Delivery via Antivirus  

Google’s Mandiant researchers uncovered a new exploitation of Triofox, a remote‑management platform used by many SMBs. CVE‑2025‑12480, rated CVSS 9.1, allows attackers to bypass authentication and upload malicious payloads through the platform’s antivirus feature. The bug was first observed on August 24 and has since been used to install remote‑access tools (RATs) via a PLINK‑based RDP tunnel.  

What does this mean?  
- Triofox users are effectively giving attackers a backdoor that bypasses all standard authentication controls.  
- The attackers chain this flaw with the platform’s antivirus feature to achieve code execution, a clever use of legitimate software components to hide malicious activity.  

Defensive recommendation: Immediately patch Triofox to the latest version. If patching is not yet possible, restrict access to the configuration portal and disable the antivirus upload feature until a fix is available.  

---

## 3. Ransomware‑as‑a‑Service Broader Than Ever: VanHelsing Hits Windows, Linux, ARM, BSD, ESXi  

A new ransomware operation dubbed *VanHelsing* has emerged as a fast‑scaling RaaS platform. First observed on March 7, the service licenses its capabilities to affiliated threat actors, enabling them to target a wide range of operating systems—including Windows, Linux, BSD, ARM, and VMware ESXi.  

Implications:  
- The breadth of supported platforms means that virtually any on‑prem or cloud environment is at risk.  
- RaaS lowers the barrier to entry, allowing even less‑experienced actors to launch devastating attacks.  

Defensive steps: Harden all endpoints with the latest security patches, employ file‑integrity monitoring, and segment critical assets to limit lateral movement. Consider ransomware‑specific detection solutions that look for known encryption patterns or abnormal file‑renaming activity.  

---

## 4. Banking Trojans Linked Across Borders: Maverick and Coyote Share DNA  

CyberProof researchers discovered deep technical similarities between the Maverick and Coyote banking trojans, both targeting Brazilian users through WhatsApp. The link points to a shared development lineage or shared code base, suggesting that threat actors are reusing or mutating malware rather than building from scratch.  

Why it matters:  
- Shared code bases can propagate known weaknesses, making it easier for defenders to detect multiple families with a single signature.  
- The use of WhatsApp—an everyday communication channel—illustrates the platform’s attractiveness for social‑engineering attacks.  

Mitigation: Monitor for suspicious file downloads from messaging apps, employ sandboxing for attachments, and educate users to verify the authenticity of links received through WhatsApp.  

---

## 5. Phishing Evolves: Quantum Route Redirect and Security‑Alert‑Themed Mails  

KnowBe4 Threat Labs identified a new phishing tool, *Quantum Route Redirect*, that automates the delivery of instant phishing campaigns to Microsoft 365. In parallel, a separate campaign uses convincing security‑alert emails that appear to come from an organization’s own domain, tricking recipients into revealing credentials.  

Takeaways:  
- Phishing tools are becoming more accessible, lowering the skill threshold for attackers.  
- The use of legitimate‑looking security alerts exploits users’ trust in internal communications.  

Defensive recommendations: Deploy email‑authentication protocols (DMARC, DKIM) to prevent spoofing, use advanced threat protection for Microsoft 365, and run regular phishing simulations that include these new tactics.  

---

## 6. A CDR Lens: Lessons From Ted Lasso  

Palo Alto Networks’ blog article draws parallels between the coaching style of Ted Lasso and the mindset needed for Cloud Detection and Response (CDR). The key message is that effective cloud security thrives on collaboration, curiosity, and a willingness to learn on the fly. By integrating data from AWS CloudTrail, Azure Activity Logs, and other sources into a unified view, analysts can see the full attack path without manual pivoting.  

Implications for practice:  
- Invest in tools that correlate data across cloud environments.  
- Foster cross‑functional teams that share insights and maintain a continuous learning culture.  

---

## Key Insights  

- **Mobile devices remain a high‑value target**: The Samsung RCE and LANDFALL spyware show that attackers are actively exploiting mobile flaws to plant persistent threats.  
- **Software supply chain and management tools are now attack vectors**: Triofox’s unauthenticated bug and the VanHelsing RaaS demonstrate how legitimate remote‑management and ransomware‑as‑a‑service platforms can be co‑opted for malicious use.  
- **Phishing sophistication is increasing**: Quantum Route Redirect and security‑alert‑themed emails illustrate new automation and social‑engineering tactics that are harder to spot, underscoring the need for robust email security and user awareness.  

---

### Looking Ahead  

As attackers continue to blend technical exploits with psychological manipulation, defenders must adopt a holistic approach that combines patch management, advanced detection, and user education. The next wave of threats will likely target emerging technology stacks—such as edge computing and hybrid cloud environments—while leveraging the same low‑barrier tactics seen today. Staying ahead will require continuous monitoring, rapid response, and a culture of curiosity reminiscent of a good coach: embrace what you don’t know, learn from it, and apply that knowledge to protect your organization.

## References
1. Lessons Ted Lasso Can Teach You About CDR. cloud-native-security-palo-alto-networks-blog. [https://www.paloaltonetworks.com/blog/cloud-security/lessons-ted-lasso-can-teach-you-about-cdr/](https://www.paloaltonetworks.com/blog/cloud-security/lessons-ted-lasso-can-teach-you-about-cdr/)
2. U.S. CISA adds Samsung mobile devices flaw to its Known Exploited Vulnerabilities catalog. security-affairs-securityaffairs-co. [https://securityaffairs.com/184452/hacking/u-s-cisa-adds-samsung-mobile-devices-flaw-to-its-known-exploited-vulnerabilities-catalog.html](https://securityaffairs.com/184452/hacking/u-s-cisa-adds-samsung-mobile-devices-flaw-to-its-known-exploited-vulnerabilities-catalog.html)
3. Principales herramientas de seguridad de MCP para 2025. revista-de-ciberseguridad-y-seguridad-de-la-informacin-para-empresas-y-organismos-pblicos-ciberseguridadpyme-es. [https://www.ciberseguridadpyme.es/actualidad/principales-herramientas-de-seguridad-de-mcp-para-2025/](https://www.ciberseguridadpyme.es/actualidad/principales-herramientas-de-seguridad-de-mcp-para-2025/)
4. Critical Triofox bug exploited to run malicious payloads via AV configuration. security-affairs-securityaffairs-co. [https://securityaffairs.com/184439/hacking/critical-triofox-bug-exploited-to-run-malicious-payloads-via-av-configuration.html](https://securityaffairs.com/184439/hacking/critical-triofox-bug-exploited-to-run-malicious-payloads-via-av-configuration.html)
5. Researchers Expose Deep Connections Between Maverick and Coyote Banking Malware. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/maverick-and-coyote/](https://gbhackers.com/maverick-and-coyote/)
6. New VanHelsing Ransomware-as-a-Service Hits Windows, Linux, BSD, ARM and ESXi. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/vanhelsing-ransomware/](https://gbhackers.com/vanhelsing-ransomware/)
7. CISA Issues Alert on Samsung 0-Day RCE Flaw Actively Exploited in Attacks. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/cisa-issues-alert-on-samsung-0-day-rce-flaw/](https://gbhackers.com/cisa-issues-alert-on-samsung-0-day-rce-flaw/)
8. Attackers Use Quantum Route Redirect to Launch Instant Phishing on M365. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/quantum-route-redirect/](https://gbhackers.com/quantum-route-redirect/)
9. Beware of Security Alert-Themed Malicious Emails that Steal Your Email Logins. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/email-logins/](https://gbhackers.com/email-logins/)
10. Lazarus Group Deploys Weaponized Documents Against Aerospace & Defense. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/lazarus-group/](https://gbhackers.com/lazarus-group/)
11. WatchGuard Firebox Flaw Allows Attackers to Gain Unauthorized SSH Access. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/watchguard-firebox-flaw/](https://gbhackers.com/watchguard-firebox-flaw/)
12. 65% of Top AI Firms Found Exposing Verified API Keys and Tokens on GitHub. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/65-of-top-ai-firms-found-exposing-verified-api-keys/](https://gbhackers.com/65-of-top-ai-firms-found-exposing-verified-api-keys/)
13. Danabot Malware Reemerges with Version 669 After Operation Endgame. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/danabot-malware/](https://gbhackers.com/danabot-malware/)
14. Devolutions Server Flaw Allows Attackers to Impersonate Users via Pre-MFA Cookie. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/devolutions-server-flaw/](https://gbhackers.com/devolutions-server-flaw/)
15. Everest Ransomware Group Lists Agfa-Gevaert and SIAD as Victims. daily-dark-web-rss-app. [https://dailydarkweb.net/everest-ransomware-group-lists-agfa-gevaert-and-siad-as-victims/](https://dailydarkweb.net/everest-ransomware-group-lists-agfa-gevaert-and-siad-as-victims/)