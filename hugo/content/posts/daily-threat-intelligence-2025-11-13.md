+++
title = "Malware Dominate Latest Threat Intelligence - November 13, 2025"
date = "2025-11-13"
tags = ["threat-intelligence", "daily-digest", "cybersecurity", "revista de ciberseguridad y seguridad de la informacin para empresas y organismos pblicos ciberseguridadpyme es", "security affairs securityaffairs co", "sans internet storm center infocon green isc sans edu", "gbhackers security 1 globally trusted cyber security news platform gbhackers com"]
categories = ["Threat Intelligence"]
summary = "Daily threat intelligence digest covering 21 recent security developments."
draft = false
author = "Tia N. List"
lastmod = "2025-11-13T11:24:49.532031"
sources = ["revista-de-ciberseguridad-y-seguridad-de-la-informacin-para-empresas-y-organismos-pblicos-ciberseguridadpyme-es", "security-affairs-securityaffairs-co", "sans-internet-storm-center-infocon-green-isc-sans-edu", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com"]
+++

# Daily Threat Intelligence Digest – November 13, 2025  

The past 24 hours have underscored a shifting threat landscape that blends classic cyber‑crime tactics with sophisticated, zero‑day exploitation and supply‑chain subterfuge. From large‑scale takedowns to targeted phishing campaigns, the latest intelligence signals that attackers are sharpening their focus on both high‑value systems and the everyday tools that organizations rely on for day‑to‑day operations.

---

### A New Wave of Zero‑Day Exploits

Amazon’s threat‑intel team released an advisory detailing an **advanced threat actor’s use of two previously unknown zero‑day vulnerabilities** in Cisco Identity Service Engine (ISE) and Citrix NetScaler ADC. The actor leveraged CVE‑2025‑20337 in Cisco ISE and CVE‑2025‑5777 (Citrix “Bleed Two”) to gain pre‑authentication remote code execution. What makes this incident particularly alarming is that the exploitation was active *before* Cisco had even assigned CVE numbers or released comprehensive patch bundles. The attacker deployed a custom in‑memory web shell that masqueraded as a legitimate IdentityAuditAction, leaving little footprint on disk and evading many traditional detection methods.

This case illustrates a broader trend: **attackers are monitoring the patch cycle and weaponising vulnerabilities the moment they surface, sometimes even before vendors have published advisories**. The need for rapid vulnerability disclosure, coordinated patching, and continuous monitoring cannot be overstated. Organizations that rely on network identity and application delivery platforms should verify that all branches of Cisco ISE and Citrix NetScaler are up‑to‑date and consider deploying runtime protection that watches for anomalous API calls or unexpected network traffic associated with known exploit signatures.

---

### The Rise of “Legitimate” Attack Surfaces

Three separate reports today highlighted the exploitation of trusted software and services:

| Source | Tool / Platform | Attack Method | Target |
|--------|-----------------|--------------|--------|
| GBHackers | LogMeIn Resolve / PDQ Connect | RMM abuse | Remote desktop, credential theft |
| GBHackers | ClickFix (search‑engine‑based) | Social‑engineering download | Windows / macOS infostealer |
| GBHackers | Malicious Chrome extension (“Safery”) | Supply‑chain crypto theft | Ethereum wallets |

LogMeIn Resolve and PDQ Connect, both remote‑monitoring and management (RMM) tools, were manipulated to install backdoors on target machines. ClickFix masqueraded as a search‑result for cracked software, leading users to a malicious payload that harvested credentials. The Chrome extension, hidden among legitimate wallet tools, siphoned seed phrases by embedding covert blockchain transactions.

These attacks demonstrate a **blurring line between legitimate administrative tools and malicious payloads**. As organizations increasingly adopt cloud‑based RMM solutions, attackers are turning to them as a low‑friction conduit for persistence and lateral movement. Likewise, social‑engineering campaigns that piggyback on legitimate search queries or extensions take advantage of the trust users place in familiar platforms.

**Actionable takeaway**: enforce least‑privilege policies on RMM deployments, audit installed extensions on all endpoints, and educate users to verify the provenance of software before installation, especially when the software claims to be a “trusted” wallet or management tool.

---

### Vulnerabilities in Network Appliances and DevOps Tools

Two critical vulnerabilities were disclosed that affect widely deployed network appliances and open‑source DevOps tools:

* **CVE‑2025‑12101** – a cross‑site scripting flaw in Citrix NetScaler ADC and NetScaler Gateway. Though considered moderate, it can be used for phishing or credential theft when attackers control a compromised web interface.
* **CVE‑2025‑6945** – a prompt injection flaw in GitLab Duo that could allow attackers to read confidential issue data and inject malicious code into public discussions.

These findings reinforce the **importance of securing the “infrastructure as code” layer**. Attackers are increasingly targeting the very tools that enable rapid deployment and scaling of services. Organizations should promptly apply patches for GitLab CE/EE releases 18.5.2, 18.4.4, or 18.3.6, and verify that their Citrix appliances are updated to the latest firmware.

---

### Global Law‑Enforcement Action

Operation Endgame, coordinated by Europol, successfully dismantled **1,025 servers** linked to the Rhadamanthys infostealer, VenomRAT remote‑access trojan, and the Elysium botnet. This operation highlights how **collaborative law‑enforcement efforts can neutralize large‑scale threat actor infrastructures**. While the takedown reduces immediate risk, the underlying malware families—particularly Rhadamanthys—continue to evolve. Security teams should remain vigilant for new variants that may bypass current detection signatures.

---

### The Regulatory Lens

A Spanish‑language article from *CiberseguridadPyme* underscores the **growing convergence of cybersecurity and quality management in regulated industries**—healthcare, energy, and finance. As data protection mandates tighten, the industry is shifting from protecting physical assets to safeguarding information integrity. The piece notes that secure networks “reduce the probability of failures that can lead to errors, which is essential for maintaining high quality in industry operations.”

This narrative signals a **policy‑driven shift**: compliance frameworks increasingly demand that security controls be embedded into the quality assurance cycle. Companies in regulated sectors must therefore treat cybersecurity not as an add‑on but as a core component of operational excellence.

---

## Key Insights

- **Zero‑day exploitation is moving ahead of patch cycles**; attackers are targeting vulnerabilities immediately upon discovery, even before advisories are issued. Rapid patching, coordinated vulnerability management, and runtime protection are critical.
- **Trusted tools and platforms—RMM software, search‑engine links, and browser extensions—are becoming legitimate attack vectors**. Organizations need stricter oversight of administrative tools and user‑education initiatives to mitigate social‑engineering risks.
- **Security in regulated industries is evolving into a quality‑management requirement**. Compliance demands that data integrity and system reliability be integral to operational processes, not an afterthought.

---

### Looking Ahead

In the coming weeks, we anticipate further exploitation of zero‑day flaws in widely used network services, as well as an uptick in sophisticated supply‑chain attacks that masquerade as legitimate administrative tools. Organizations must strengthen their vulnerability response, enforce stricter controls over privileged tools, and embed cybersecurity into every layer of their quality management frameworks to stay ahead of emerging threats.

## References
1. Cómo la ciberseguridad refuerza la gestión de calidad en industrias reguladas. revista-de-ciberseguridad-y-seguridad-de-la-informacin-para-empresas-y-organismos-pblicos-ciberseguridadpyme-es. [https://www.ciberseguridadpyme.es/actualidad/como-la-ciberseguridad-refuerza-la-gestion-de-calidad-en-industrias-reguladas/](https://www.ciberseguridadpyme.es/actualidad/como-la-ciberseguridad-refuerza-la-gestion-de-calidad-en-industrias-reguladas/)
2. Amazon alerts: advanced threat actor exploits Cisco ISE & Citrix NetScaler zero-days. security-affairs-securityaffairs-co. [https://securityaffairs.com/184561/hacking/amazon-alerts-advanced-threat-actor-exploits-cisco-ise-citrix-netscaler-zero-days.html](https://securityaffairs.com/184561/hacking/amazon-alerts-advanced-threat-actor-exploits-cisco-ise-citrix-netscaler-zero-days.html)
3. Formbook Delivered Through Multiple Scripts, (Thu, Nov 13th). sans-internet-storm-center-infocon-green-isc-sans-edu. [https://isc.sans.edu/diary/rss/32480](https://isc.sans.edu/diary/rss/32480)
4. Operation Endgame: Authorities Takedown 1,025 Servers Linked to Rhadamanthys, VenomRAT, and Elysium. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/operation-endgame-authorities-takedown-1025-server/](https://gbhackers.com/operation-endgame-authorities-takedown-1025-server/)
5. New ClickFix Attack Targeting Windows and macOS Users to Deploy Infostealer Malware. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/new-clickfix-attack/](https://gbhackers.com/new-clickfix-attack/)
6. Hackers Using RMM Tools LogMeIn and PDQ Connect to Deploy Malware as Legitimate Software. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/logmein-and-pdq-connect/](https://gbhackers.com/logmein-and-pdq-connect/)
7. GitLab Vulnerabilities Expose Users to Prompt Injection Attacks and Data Theft. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/gitlab-vulnerabilities-expose-users-to-prompt-injection/](https://gbhackers.com/gitlab-vulnerabilities-expose-users-to-prompt-injection/)
8. Citrix NetScaler ADC and Gateway Flaw Allows Cross-Site Scripting (XSS) Attacks. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/citrix-netscaler-adc-and-gateway-flaw/](https://gbhackers.com/citrix-netscaler-adc-and-gateway-flaw/)
9. CISA Warns of Active Exploitation of WatchGuard Firebox Out-of-Bounds Write Flaw. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/cisa-warns-watchguard-firebox-out-of-bounds-write-flaw/](https://gbhackers.com/cisa-warns-watchguard-firebox-out-of-bounds-write-flaw/)
10. Malicious Chrome Extension Grants Full Control Over Ethereum Wallet. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/malicious-chrome-extension-4/](https://gbhackers.com/malicious-chrome-extension-4/)
11. Kibana Vulnerabilities Expose Systems to SSRF and XSS Attacks. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/kibana-vulnerabilities-expose-systems/](https://gbhackers.com/kibana-vulnerabilities-expose-systems/)
12. Critical Dell Data Lakehouse Flaw Allows Remote Attackers to Escalate Privileges. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/critical-dell-data-lakehouse-flaw/](https://gbhackers.com/critical-dell-data-lakehouse-flaw/)
13. Beware of Fake Bitcoin Tools Concealing DarkComet RAT Malware. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/fake-bitcoin-tools/](https://gbhackers.com/fake-bitcoin-tools/)
14. Everest Group Claims Breach on KorPath, Vikor Scientific, and Korgene. daily-dark-web-rss-app. [https://dailydarkweb.net/everest-group-claims-breach-on-korpath-vikor-scientific-and-korgene/](https://dailydarkweb.net/everest-group-claims-breach-on-korpath-vikor-scientific-and-korgene/)
15. Black Shrantac Ransomware Group Hits Global Firms in New Attack. daily-dark-web-rss-app. [https://dailydarkweb.net/black-shrantac-ransomware-group-hits-global-firms-in-new-attack/](https://dailydarkweb.net/black-shrantac-ransomware-group-hits-global-firms-in-new-attack/)