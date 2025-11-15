+++
title = "\u26a0\ufe0f Critical Vulnerabilities Patched in Major Software - November 15, 2025"
date = "2025-11-15"
tags = ["threat-intelligence", "daily-digest", "cybersecurity", "qualys security blog", "security affairs securityaffairs co", "the hacker news feeds feedburner com"]
categories = ["Threat Intelligence"]
summary = "Daily threat intelligence digest covering 3 recent security developments."
draft = false
author = "Tia N. List"
lastmod = "2025-11-15T11:19:02.404263"
sources = ["qualys-security-blog", "security-affairs-securityaffairs-co", "the-hacker-news-feeds-feedburner-com"]
+++

# Daily Threat Intelligence Digest – November 15, 2025  

In the past 24 hours the cybersecurity community has witnessed two major developments that underscore how quickly critical vulnerabilities can transition from discovery to widespread exploitation, and how state‑backed actors continue to leverage social engineering and insider tactics to breach U.S. enterprises. The first is a new authentication bypass flaw in Fortinet’s FortiWeb web‑application firewalls, now being actively used in the wild and added to the U.S. Cybersecurity and Infrastructure Security Agency’s (CISA) Known Exploited Vulnerabilities (KEV) catalog. The second involves a U.S. Department of Justice (DoJ) announcement that five citizens pleaded guilty to aiding North Korean information‑technology workers in infiltrating 136 companies, a reminder that geopolitical conflicts are increasingly fought in the digital domain.

### FortiWeb’s Critical Authentication Bypass – From Vulnerability to Exploit  

Fortinet’s FortiWeb 7.x and 8.x families have long been a staple of enterprise security stacks, providing application‑level protection for web services. However, a newly disclosed flaw, identified as CVE‑2025‑64446, has caused alarm. The vulnerability is a dual‑stage authentication bypass that lets an unauthenticated attacker create an administrative account on any FortiWeb device exposed to the internet. The first stage exploits a path‑traversal weakness in the FortiWeb API, while the second stage abuses a CGI authentication routine that accepts base‑64 encoded user data from the client. Together, these flaws allow the attacker to impersonate an administrator and gain full control of the firewall.

CISA’s inclusion of CVE‑2025‑64446 in the KEV catalog on November 15 signals that the threat is already being used in the field. The agency has set a remediation deadline of November 21, urging organizations to either upgrade to patched versions or temporarily disable HTTP/HTTPS access on publicly exposed interfaces. Fortinet has released a patch for the affected firmware releases, but the window for remediation is narrow. Additionally, the vulnerability’s CVSS v3.1 score of 9.8 (critical) places it among the most severe threats in the current landscape.

### The DOJ’s North Korean IT Infiltration Case – A New Chapter in State‑Sponsored Espionage  

While the FortiWeb incident demonstrates the speed with which a software flaw can go from discovery to exploitation, the DoJ case highlights a different, but equally dangerous, attack vector: insider facilitation. Five U.S. citizens have pleaded guilty to assisting North Korean IT workers in infiltrating 136 companies to support illicit revenue generation schemes. The individuals—ranging in age from 24 to 34—were found to have provided technical support, credentials, and guidance that enabled North Korean actors to bypass corporate firewalls and access sensitive data.

This case underscores the persistent threat of state‑backed actors leveraging the skills of private citizens to conduct cyber‑espionage and sabotage. The DOJ’s statement stresses that the defendants knowingly violated both U.S. sanctions and the Computer Fraud and Abuse Act, illustrating how legal frameworks are being used to prosecute these crimes. The involvement of relatively young, tech‑savvy individuals signals that the talent pool for such operations remains broad and accessible.

### Emerging Trends and What They Mean for Your Organization  

1. **Rapid Exploitation of High‑Impact Vulnerabilities**  
   The FortiWeb flaw demonstrates how quickly a critical vulnerability can be exploited once it becomes known. The fact that attackers are already creating admin accounts on exposed devices shows that attackers are not only scanning for vulnerabilities but actively leveraging them in real time. This trend highlights the importance of maintaining an up‑to‑date inventory of all security appliances, particularly those that are internet‑exposed, and ensuring that patches are applied in a timely manner.

2. **Evolving Insider‑Assisted State‑Backed Operations**  
   The DOJ’s guilty plea announcement illustrates a growing pattern where state actors outsource cyber‑operations to individuals in the private sector. These individuals often have legitimate credentials and knowledge of corporate networks, making them valuable assets for foreign adversaries. Organizations must therefore strengthen personnel vetting, monitor insider activity, and enforce strict separation between privileged accounts and public interfaces.

3. **CISA’s KEV Catalog as a Strategic Tool**  
   CISA’s KEV catalog is becoming a central reference point for organizations to identify and prioritize risks that are actively being exploited. The addition of CVE‑2025‑64446 to this catalog signals that the vulnerability is not just theoretical but already a real threat. By aligning internal vulnerability management processes with the KEV catalog, organizations can more effectively allocate resources to the most pressing threats.

### Actionable Recommendations

- **Patch Immediately**: If you run FortiWeb 7.x or 8.x, apply Fortinet’s patch before the November 21 deadline. If a patch is not yet available, disable HTTP/HTTPS on all publicly exposed interfaces until you can upgrade.
  
- **Validate Access Controls**: Conduct an audit of all administrative accounts on FortiWeb devices and other critical appliances. Look for any newly created or unauthorized accounts and delete or disable them.

- **Strengthen Insider Monitoring**: Implement user behavior analytics (UBA) to detect anomalous activity that may indicate insider assistance. Review privileged account usage logs for unexpected patterns.

- **Align with KEV Catalog**: Incorporate CISA’s KEV catalog into your vulnerability management workflow. Prioritize remediation of vulnerabilities listed therein, and keep stakeholders informed of compliance status.

- **Review Third‑Party Relationships**: Given the DOJ case, assess the security posture of vendors, contractors, and other third‑party partners. Ensure they adhere to strict security controls and do not provide access that could be leveraged by foreign actors.

### Forward‑Looking Statement

As we move into the second half of 2025, we can expect attackers to continue targeting a mix of software vulnerabilities and insider-assisted operations. The rapid exploitation of FortiWeb’s authentication bypass serves as a stark reminder that even well‑established security products are not immune. Simultaneously, state‑backed actors are refining their tactics by recruiting and leveraging individuals with technical expertise. Organizations that adopt a proactive, layered defense—combining swift patching, rigorous access controls, and robust insider threat monitoring—will be better positioned to withstand these evolving threats.

## References
1. Unauthenticated Authentication Bypass in Fortinet FortiWeb (CVE-2025-64446) Exploited in the Wild. qualys-security-blog. [https://blog.qualys.com/category/vulnerabilities-threat-research](https://blog.qualys.com/category/vulnerabilities-threat-research)
2. U.S. CISA adds Fortinet FortiWeb flaw to its Known Exploited Vulnerabilities catalog. security-affairs-securityaffairs-co. [https://securityaffairs.com/184652/hacking/u-s-cisa-adds-fortinet-fortiweb-flaw-to-its-known-exploited-vulnerabilities-catalog-2.html](https://securityaffairs.com/184652/hacking/u-s-cisa-adds-fortinet-fortiweb-flaw-to-its-known-exploited-vulnerabilities-catalog-2.html)
3. Five U.S. Citizens Plead Guilty to Helping North Korean IT Workers Infiltrate 136 Companies. the-hacker-news-feeds-feedburner-com. [https://thehackernews.com/2025/11/five-us-citizens-plead-guilty-to.html](https://thehackernews.com/2025/11/five-us-citizens-plead-guilty-to.html)