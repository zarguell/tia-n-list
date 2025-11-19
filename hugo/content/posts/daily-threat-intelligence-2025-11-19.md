+++
title = "🔥 14 Ransomware Incidents Strike Global Targets - November 19, 2025"
date = "2025-11-19"
tags = ["threat-intelligence", "daily-digest", "cybersecurity", "securelist securelist com", "qualys security blog", "ciberseguridad latam ciberseguridadlatam com", "security affairs securityaffairs co", "daily dark web rss app"]
categories = ["Threat Intelligence"]
summary = "Daily threat intelligence digest covering 14 recent security developments."
draft = false
author = "Tia N. List"
lastmod = "2025-11-19T11:22:31.859756"
sources = ["securelist-securelist-com", "qualys-security-blog", "securelist-securelist-com", "ciberseguridad-latam-ciberseguridadlatam-com", "security-affairs-securityaffairs-co", "security-affairs-securityaffairs-co", "daily-dark-web-rss-app", "daily-dark-web-rss-app", "the-hacker-news-feeds-feedburner-com", "the-hacker-news-feeds-feedburner-com"]
+++

# Daily Threat Intelligence Digest – November 19, 2025

In a world where cyber‑attacks grow in both scale and sophistication, the latest intelligence reveals a stark picture of how threat actors are exploiting new vectors, while law‑enforcement agencies are finally catching up. This digest pulls together 10 fresh reports that highlight rising ransomware activity, a surge in mobile malware, high‑profile data breaches, and the dawning threat of AI‑driven attacks. Together, they paint a comprehensive snapshot of the challenges that organisations must face today.

---

## A Surge in Ransomware and Mining Attacks

Kaspersky’s quarterly security network report for Q3 2025 shows that defenders blocked more than **389 million** attacks across all platforms. Yet the sheer volume of new threats is staggering: **2,200** new ransomware families emerged in the last three months, and **85 000** users fell victim to ransomware attacks. Almost one‑fifth of those victims whose data appeared on threat‑actor leak sites were targeted by the Qilin ransomware gang, underscoring a shift toward more aggressive data‑exfiltration tactics.

In parallel, mining malware—software that hijacks computing resources for cryptocurrency mining—took a hit, with **254 000** users targeted. While the numbers may seem high, the true cost to organisations is hidden in the loss of bandwidth, battery life, and potential for credential theft that often accompanies mining activity.

These figures also come at a time when law‑enforcement agencies are making headlines. The UK’s National Crime Agency arrested a suspect linked to a HardBit ransomware incident that crippled several European airports in September. Meanwhile, U.S. authorities seized millions of dollars in cryptocurrency and launched charges against the leaders of the LockerGoga, MegaCortex, and Nefilim gangs—each responsible for multi‑million dollar losses worldwide.

---

## Mobile Malware Still Reigns

Kaspersky’s mobile‑specific report confirms that mobile threats remain as prevalent as ever. In Q3 2025, defenders thwarted **47 million** attacks that used malware, adware, or unwanted software. Trojans—malicious programs that masquerade as legitimate apps—accounted for **15.78 %** of all mobile attacks, with a notable 52 000 malicious banking Trojans discovered. Notably, **1 564** mobile ransomware Trojans were identified, indicating that ransomware is now also targeting smartphones and tablets.

These numbers highlight the importance of maintaining a robust mobile security strategy. Even as enterprises push for mobile‑first policies, the attack surface expands: users install apps from third‑party stores, share sensitive documents via messaging apps, and rely on cloud‑based services that can be compromised. Mobile-specific security controls, such as app vetting and endpoint detection, are now more critical than ever.

---

## Data Breaches Keep Scaling

The past 24 hours have seen a string of high‑impact data breaches:

1. **WhatsApp Exposure** – Researchers from the University of Vienna discovered a flaw that allowed anyone to repeatedly query the app for phone numbers. Meta knew of the issue in 2017 but failed to act, exposing **3.5 billion** phone numbers. The scale of this leak is unprecedented, and it underscores the need for continuous code‑review and rapid patching, especially for widely used messaging platforms.

2. **Eurofiber Ticket Portal Breach** – On November 13, attackers exploited a vulnerability in Eurofiber’s ticketing and customer portals, stealing data from users in France and initiating an extortion attempt. While the breach was geographically limited, it demonstrates how even infrastructure‑heavy organisations can become targets when a single software flaw is left unpatched.

3. **Telecom UK Customer Leak** – A dark‑web listing revealed that **230 105** telecom customers from the UK were up for sale. This leak could provide threat actors with valuable social‑engineering vectors, such as phishing campaigns that spoof legitimate callers.

4. **Ayuntamiento de Béjar Documents** – Internal documents from a Spanish municipal council were leaked, offering a taste of how local governments can become easy targets when standard security controls are lax.

These incidents collectively emphasize that data leaks are no longer limited to the “big‑name” sectors; any organisation with a digital footprint can become a target.

---

## Zero‑Day Exploits and DNS Hijacking

Fortinet’s FortiWeb web‑application firewall suffered a newly discovered zero‑day vulnerability, CVE‑2025‑58034, that attackers are already exploiting. The flaw allows authenticated users to execute arbitrary commands on the underlying system through crafted HTTP requests. Fortinet has released patches for all affected versions, but the rapid exploitation timeline underscores the importance of **automatic patch management**.

In a related vein, the threat actor group **PlushDaemon** deployed a Go‑based backdoor, EdgeStepper, that hijacks DNS queries for software‑update traffic. By rerouting legitimate update traffic to malicious nodes, attackers can deliver malware under the guise of a trusted update. Organisations should monitor DNS logs for unusual query patterns and ensure that software updates are signed and verified.

---

## AI‑Driven Prompt Injection

ServiceNow’s Now Assist AI platform has been found vulnerable to a sophisticated “second‑order prompt injection” attack. Attackers can send carefully crafted prompts that cause the AI agents to act against each other, potentially exfiltrating data or altering configurations. This is one of the first publicly documented cases of AI prompt injection that exploits agent‑to‑agent interactions. Defensive measures include tightening access controls for AI agents, using least‑privilege principles, and disabling unnecessary agent interactions in production environments.

---

## Actionable Recommendations

1. **Adopt Patch‑Management Automation** – Manual patching is no longer viable. Automation tools can continuously scan for vulnerabilities, prioritize them based on risk, test patches in a staging environment, and deploy updates across hybrid clouds without human oversight.

2. **Strengthen Mobile Security** – Deploy mobile device management (MDM) solutions that enforce app vetting, restrict sideloading, and provide endpoint detection for mobile ransomware and banking Trojans.

3. **Monitor DNS and Update Traffic** – Implement DNS monitoring and enforce signed, verified software updates to prevent hijacking attempts like EdgeStepper.

4. **Guard Against AI Prompt Injection** – Restrict AI agent permissions, audit agent interactions, and consider disabling default agent discovery features unless strictly needed.

5. **Keep an Eye on Data‑Leak Sites** – Many ransomware and phishing campaigns source victim lists from data‑leak sites. Regularly check whether employee data appears on such sites and take remediation steps if it does.

6. **Prioritise Incident Response for Insider‑Threats** – The leaks from Eurofiber and the Ayuntamiento de Béjar show that internal systems can be compromised with relatively little effort. Strengthen insider‑threat monitoring and enforce strict access controls.

---

## Forward‑Looking Statement

As the threat landscape evolves, attackers are increasingly blending traditional malware tactics with emerging technologies like AI and DNS‑based infection vectors. Organisations that invest early—by automating patch management, securing mobile endpoints, and hardening AI platforms—will be better positioned to mitigate the rising tide of ransomware, mining, and data‑exfiltration attacks that continue to grow in scale and complexity. The next few weeks will test the resilience of these controls, as threat actors look to exploit any remaining gaps in the digital perimeter.

## References
1. IT threat evolution in Q3 2025. Non-mobile statistics. securelist-securelist-com. [https://securelist.com/malware-report-q3-2025-pc-iot-statistics/118020/](https://securelist.com/malware-report-q3-2025-pc-iot-statistics/118020/)
2. What is Patch Management Automation and Why It Matters. qualys-security-blog. [https://blog.qualys.com/category/product-tech](https://blog.qualys.com/category/product-tech)
3. IT threat evolution in Q3 2025. Mobile statistics. securelist-securelist-com. [https://securelist.com/malware-report-q3-2025-mobile-statistics/118013/](https://securelist.com/malware-report-q3-2025-mobile-statistics/118013/)
4. WhatsApp: 8 Años de negligencia y 3500  millones de números telefónicos expuestos. ciberseguridad-latam-ciberseguridadlatam-com. [https://ciberseguridadlatam.com/whatsapp-8-anos-de-negligencia-y-3500-millones-de-numeros-telefonicos-expuestos/](https://ciberseguridadlatam.com/whatsapp-8-anos-de-negligencia-y-3500-millones-de-numeros-telefonicos-expuestos/)
5. Eurofiber confirms November 13 hack, data theft, and extortion attempt. security-affairs-securityaffairs-co. [https://securityaffairs.com/184822/data-breach/eurofiber-confirms-november-13-hack-data-theft-and-extortion-attempt.html](https://securityaffairs.com/184822/data-breach/eurofiber-confirms-november-13-hack-data-theft-and-extortion-attempt.html)
6. New FortiWeb zero-day CVE-2025-58034 under attack patched by Fortinet. security-affairs-securityaffairs-co. [https://securityaffairs.com/184806/hacking/new-fortiweb-zero-day-cve-2025-58034-under-attack-patched-by-fortinet.html](https://securityaffairs.com/184806/hacking/new-fortiweb-zero-day-cve-2025-58034-under-attack-patched-by-fortinet.html)
7. BRSK Data Breach: 230,105 Records of Telecom UK Customers for Sale. daily-dark-web-rss-app. [https://dailydarkweb.net/brsk-data-breach-230105-records-of-telecom-uk-customers-for-sale/](https://dailydarkweb.net/brsk-data-breach-230105-records-of-telecom-uk-customers-for-sale/)
8. Ayuntamiento de Béjar Internal Documents Leaked Following Breach. daily-dark-web-rss-app. [https://dailydarkweb.net/ayuntamiento-de-bejar-internal-documents-leaked-following-breach/](https://dailydarkweb.net/ayuntamiento-de-bejar-internal-documents-leaked-following-breach/)
9. EdgeStepper Implant Reroutes DNS Queries to Deploy Malware via Hijacked Software Updates. the-hacker-news-feeds-feedburner-com. [https://thehackernews.com/2025/11/edgestepper-implant-reroutes-dns.html](https://thehackernews.com/2025/11/edgestepper-implant-reroutes-dns.html)
10. ServiceNow AI Agents Can Be Tricked Into Acting Against Each Other via Second-Order Prompts. the-hacker-news-feeds-feedburner-com. [https://thehackernews.com/2025/11/servicenow-ai-agents-can-be-tricked.html](https://thehackernews.com/2025/11/servicenow-ai-agents-can-be-tricked.html)
11. Fortinet Warns of New FortiWeb CVE-2025-58034 Vulnerability Exploited in the Wild. the-hacker-news-feeds-feedburner-com. [https://thehackernews.com/2025/11/fortinet-warns-of-new-fortiweb-cve-2025.html](https://thehackernews.com/2025/11/fortinet-warns-of-new-fortiweb-cve-2025.html)
12. Anatomy of an Akira Ransomware Attack: When a Fake CAPTCHA Led to 42 Days of Compromise. unit-42. [https://unit42.paloaltonetworks.com/fake-captcha-to-compromise/](https://unit42.paloaltonetworks.com/fake-captcha-to-compromise/)
13. Cloudflare blames this week's massive outage on database issues. bleeping-computer. [https://www.bleepingcomputer.com/news/technology/cloudflare-blames-this-weeks-massive-outage-on-database-issues/](https://www.bleepingcomputer.com/news/technology/cloudflare-blames-this-weeks-massive-outage-on-database-issues/)
14. China-aligned threat actor is conducting widespread cyberespionage campaigns. the-record-from-recorded-future-news-therecord-media. [https://therecord.media/china-aligned-threat-actor-espionage-network-devices](https://therecord.media/china-aligned-threat-actor-espionage-network-devices)