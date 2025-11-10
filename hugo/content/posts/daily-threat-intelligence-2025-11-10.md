+++
title = "Malware Dominate Latest Threat Intelligence - November 10, 2025"
date = "2025-11-10"
tags = ["threat-intelligence", "daily-digest", "cybersecurity", "revista de ciberseguridad y seguridad de la informacin para empresas y organismos pblicos ciberseguridadpyme es", "security affairs securityaffairs co", "gbhackers security 1 globally trusted cyber security news platform gbhackers com"]
categories = ["Threat Intelligence"]
summary = "Daily threat intelligence digest covering 19 recent security developments."
draft = false
author = "Tia N. List"
lastmod = "2025-11-10T11:21:35.742576"
sources = ["revista-de-ciberseguridad-y-seguridad-de-la-informacin-para-empresas-y-organismos-pblicos-ciberseguridadpyme-es", "security-affairs-securityaffairs-co", "security-affairs-securityaffairs-co", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com", "gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com"]
+++

# Daily Threat Intelligence Digest – November 10, 2025  

A whirlwind of new developments today underscores how attackers are widening their attack surface—from the way we build software to the very tools we use to test it. In the last 24 hours, fresh reports revealed a wave of malicious NuGet packages that slip into legitimate projects, a series of zero‑day vulnerabilities exposed at Pwn2Own 2025, emerging AI‑powered penetration‑testing suites that rival traditional methods, and a sophisticated supply‑chain campaign that weaponised remote‑monitoring tools to deliver ransomware. Meanwhile, a language‑model framework’s deserialization flaw and an endpoint‑protection vulnerability have both been disclosed, and a data leak has spilled a trove of state‑sponsored cyber‑weapons. Together, these stories paint a picture of a threat landscape that is both more pervasive and more sophisticated than ever before.

## The Rise of Malicious Code in Legitimate Packages  

The most headline‑grabbing story today comes from Socket’s Threat Research Team, who uncovered nine malicious NuGet packages published by the alias “shanhai666.” These packages, released between 2023 and 2024, masquerade as harmless database helpers but actually harbor time‑delayed payloads that can disrupt SQL Server, PostgreSQL, SQLite, and even industrial PLCs. The most dangerous of them, *Sharp7Extend*, contains dual sabotage mechanisms: it can immediately terminate processes and, after a 30‑90‑minute delay, silently corrupt PLC data—an attack vector that could cripple manufacturing safety systems.  

What’s striking is the sheer stealth of the delivery: the packages were downloaded nearly 9,500 times before the vulnerability was discovered, and all of them were removed only after Socket alerted NuGet on November 5. This incident underscores the necessity of supply‑chain vigilance even for internal, trusted dependencies.  

## Zero‑Days Make the Cut at Pwn2Own 2025  

In a parallel development, QNAP has patched seven zero‑day vulnerabilities that were showcased at the Pwn2Own Ireland competition. The flaws affected a range of QNAP products—from the QTS operating system to the Hyper Data Protector backup suite. Among the most critical were CVE‑2025‑62847 through CVE‑2025‑62849, which allowed arbitrary code execution with system‑level privileges. QNAP’s advisory stresses that customers must upgrade to the latest firmware builds (e.g., QTS 5.2.7.3297 and QuTS hero h5.3.1.3292) to mitigate the risk.  

The fact that these vulnerabilities were demonstrated publicly before being addressed raises an important point: attackers are increasingly willing to expose their exploits in the wild to create a sense of urgency and to pressure vendors into swift remediation.  

## AI‑Driven Pen Testing and the New Threat Surface  

A new entrant, HackGPT Enterprise, has launched a cloud‑native AI‑powered penetration‑testing platform that leverages GPT‑4 and local language models. While the tool promises to automate many of the tedious parts of a penetration test, it also introduces a new attack surface: the very AI models can be co‑opted to generate realistic phishing vectors, craft credential‑dumping scripts, or even produce bespoke malware tailored to a target’s environment.  

Similarly, a recent vulnerability in LangGraph’s checkpoint serialization library (CVE‑2025‑64439) allows attackers to execute arbitrary Python code via malicious deserialization. As organizations adopt AI frameworks for productivity, they must also enforce strict controls over data serialization and model training pipelines.  

## RMM Exploitation and Ransomware Supply‑Chain Attacks  

Zensec’s investigation into the *SimpleHelp* Remote Monitoring and Management (RMM) tool reveals a dual‑stage attack: ransomware‑as‑a‑service groups Medusa and DragonForce first compromised the RMM platform, then leveraged its trusted connection to downstream customers in the UK. The campaign demonstrates how RMM tools—once considered benign utilities—can become a conduit for ransomware, especially when managed service providers are compromised.  

This trend is mirrored in the broader attack landscape, where supply‑chain hijacking is becoming the default attack vector. Whether it’s malicious NuGet packages or compromised RMM software, attackers now rely on the trust inherent in legitimate software ecosystems to spread their payloads.  

## Other Notable Incidents  

* **Construction Sector Targeting** – APT groups from China, Russia, Iran, and North Korea are increasingly focusing on construction firms, harvesting RDP, SSH, and Citrix credentials to gain footholds in their digital infrastructure.  
* **Paragon Spyware Expansion** – An Italian political adviser has been targeted by the Paragon Graphite spyware family, illustrating the continued expansion of surveillance tools into political opposition.  
* **Elastic Defend Vulnerability** – CVE‑2025‑37735 in Elastic Defend for Windows could allow privilege escalation through improper file‑permission handling.  
* **Data Leak of State‑Sponsored Arsenal** – A breach at the Chinese cybersecurity firm Knownsec exposed over 12,000 classified documents, revealing a comprehensive list of state‑sponsored cyber weapons and targets.  

These incidents collectively highlight the breadth of today's threat landscape—spanning industrial control, data protection, AI development, and geopolitical espionage.  

## Key Takeaways  

- **Supply‑chain vigilance is now mandatory.** Malicious code can hide inside legitimate packages, and RMM tools can serve as ransomware conduits.  
- **Zero‑day exposures are increasingly public.** Attackers use public demonstrations (e.g., Pwn2Own) to compel vendors to patch quickly.  
- **AI tools introduce new attack vectors.** Automation that saves time can also provide attackers with sophisticated means to craft targeted exploits if not properly secured.  

## Forward‑Looking Statement  

As enterprises continue to adopt cloud-native, AI‑driven workflows and rely on third‑party libraries for rapid development, the attack surface will expand further. Cyber defenders must move from reactive patching to proactive verification—implementing integrity checks for dependencies, hardening RMM configurations, and establishing strict controls around AI model training. The next wave of threats will likely intertwine supply‑chain compromise with AI‑generated attacks; staying ahead will require a holistic, zero‑trust approach to both software and data.

## References
1. ¿Está creando una aplicación para su negocio? Haga de la seguridad una máxima prioridad. revista-de-ciberseguridad-y-seguridad-de-la-informacin-para-empresas-y-organismos-pblicos-ciberseguridadpyme-es. [https://www.ciberseguridadpyme.es/actualidad/esta-creando-una-aplicacion-para-su-negocio-haga-de-la-seguridad-una-maxima-prioridad/](https://www.ciberseguridadpyme.es/actualidad/esta-creando-una-aplicacion-para-su-negocio-haga-de-la-seguridad-una-maxima-prioridad/)
2. Nine NuGet packages disrupt DBs and industrial systems with time-delayed payloads. security-affairs-securityaffairs-co. [https://securityaffairs.com/184383/malware/nine-nuget-packages-disrupt-dbs-and-industrial-systems-with-time-delayed-payloads.html](https://securityaffairs.com/184383/malware/nine-nuget-packages-disrupt-dbs-and-industrial-systems-with-time-delayed-payloads.html)
3. QNAP fixed multiple zero-days in its software demonstrated at Pwn2Own 2025. security-affairs-securityaffairs-co. [https://securityaffairs.com/184396/hacking/qnap-fixed-multiple-zero-days-in-its-software-demonstrated-at-pwn2own-2025.html](https://securityaffairs.com/184396/hacking/qnap-fixed-multiple-zero-days-in-its-software-demonstrated-at-pwn2own-2025.html)
4. HackGPT Launches as AI-Driven Penetration Testing Suite Using GPT-4 and Other Models. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/hackgpt-launches-as-ai-driven-penetration-testing-suite/](https://gbhackers.com/hackgpt-launches-as-ai-driven-penetration-testing-suite/)
5. Ransomware Operators Exploit RMM Tools to Deploy Medusa and DragonForce. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/medusa-and-dragonforce/](https://gbhackers.com/medusa-and-dragonforce/)
6. LangGraph Deserialization Flaw Enables Execution of Malicious Python Code. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/langgraph-deserialization-flaw/](https://gbhackers.com/langgraph-deserialization-flaw/)
7. APT Groups Target Construction Firms to Steal RDP, SSH, and Citrix Credentials. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/apt-groups/](https://gbhackers.com/apt-groups/)
8. Italian Adviser Becomes Latest Target in Expanding Paragon Graphite Spyware Surveillance Case. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/paragon-graphite-spyware/](https://gbhackers.com/paragon-graphite-spyware/)
9. Elastic Defend for Windows Vulnerability Allows Threat Actors to Gain Elevated Access. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/elastic-defend-for-windows-vulnerability/](https://gbhackers.com/elastic-defend-for-windows-vulnerability/)
10. Data Leak Exposes Chinese State-Sponsored Cyber Arsenal and Target Database. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/data-leak/](https://gbhackers.com/data-leak/)
11. Hackers Abuse runc Tool to Escape Containers and Compromise Hosts. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/hackers-abuse-runc-tool-to-escape-containers-and-compromise-hosts/](https://gbhackers.com/hackers-abuse-runc-tool-to-escape-containers-and-compromise-hosts/)
12. Ex-Intel Employee Hid 18,000 Sensitive Documents Prior to Leaving the Company. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/ex-intel-employee-hid-18000-sensitive-documents-prior-to-leaving-the-company/](https://gbhackers.com/ex-intel-employee-hid-18000-sensitive-documents-prior-to-leaving-the-company/)
13. Hackers Exploit Websites to Inject Malicious Links for SEO Manipulation. gbhackers-security-1-globally-trusted-cyber-security-news-platform-gbhackers-com. [https://gbhackers.com/hackers-exploit-websites/](https://gbhackers.com/hackers-exploit-websites/)
14. ENEA Data Breach: Swedish Telecom Software Firm's Source Code Leaked. daily-dark-web-rss-app. [https://dailydarkweb.net/enea-data-breach-swedish-telecom-software-firms-source-code-leaked/](https://dailydarkweb.net/enea-data-breach-swedish-telecom-software-firms-source-code-leaked/)
15. Defensoría del Pueblo de Colombia Hit by Data Breach. daily-dark-web-rss-app. [https://dailydarkweb.net/defensoria-del-pueblo-de-colombia-hit-by-data-breach/](https://dailydarkweb.net/defensoria-del-pueblo-de-colombia-hit-by-data-breach/)