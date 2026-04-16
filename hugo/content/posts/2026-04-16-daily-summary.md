---
title: Nginx-UI auth bypass exploitation 🚨, Cisco critical patches 🔧, Booking.com data breach 📧, AgingFly malware targeting Ukraine 🎯
date: 2026-04-16
tags: ["authentication bypass","critical vulnerabilities","data breach","phishing campaigns","malware","supply chain compromise","remote code execution","identity theft","exploitation in the wild","patch management"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Active exploitation of a critical Nginx-UI authentication bypass vulnerability threatens full server takeover across thousands of exposed instances, while new Cisco ISE and Webex flaws enable remote code execution and complete user impersonation in enterprise environments. A Booking.com breach exposing guest reservation data enables sophisticated impersonation attacks, and the AgingFly malware campaign targets Ukrainian government and healthcare organizations with dynamically compiled payloads.
---
# Daily Threat Intel Digest - April 16, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] Nginx-UI authentication bypass actively exploited for full server takeover**

Attackers are actively exploiting a critical authentication bypass vulnerability in nginx-ui, a popular open-source web interface for managing Nginx servers. Tracked as CVE-2026-33032 with a CVSS score of 9.8, the flaw allows unauthenticated remote attackers to invoke privileged Model Context Protocol (MCP) tools through an unprotected `/mcp_message` endpoint. The endpoint fails open with no IP whitelist by default, enabling attackers to modify Nginx configurations, reload services, and achieve complete server control without credentials. Over 2,600 publicly exposed instances have been identified via Shodan, with the library seeing more than 430,000 Docker downloads. Recorded Future has confirmed active exploitation in the wild. Administrators must immediately update to version 2.3.4 or later and configure IP whitelists to restrict access to the MCP interface [[BleepingComputer](https://www.bleepingcomputer.com/news/security/critical-nginx-ui-auth-bypass-flaw-now-actively-exploited-in-the-wild/); [Cyberpress](https://cyberpress.org/nginx-ui-flaw-actively-exploited-to-enable-full-server-takeover/); [GBHackers](https://gbhackers.com/nginx-ui-flaw-actively-exploited/)].

**[UPDATE] Adobe Acrobat/Reader zero-day - Korean-language sources confirm December exploitation timeline**

Building on yesterday's reporting of active Adobe Acrobat/Reader exploitation, Korean-language security sources have confirmed that CVE-2026-34621 has been exploited in the wild since December 2025. The vulnerability enables malicious PDF files to bypass sandbox protections. Adobe has released an emergency security update to address the flaw, which had been under active attack for approximately four months before patch availability. Organizations running Adobe Acrobat or Reader should apply the emergency update immediately and restrict PDF handling to isolated environments where possible [[Korean Security Report](https://wezard4u.tistory.com/429757)].

**[NEW] Booking.com breach exposes guest data for targeted phishing campaigns**

Booking.com has begun notifying customers that unauthorized third parties accessed guest reservation data, including booking details, names, email addresses, physical addresses, and phone numbers. Attackers compromised the data by breaching Booking.com's hotel partners using the ClickFix phishing technique, which tricks hotel employees into installing malware disguised as a computer "fix." Microsoft attributes the campaign to a threat group tracked as Storm-1865. The exposed data provides attackers with everything needed for convincing impersonation attacks—scammers can hijack reservations, message guests posing as hotels, and demand fraudulent payments or credit card details for "verification." The attack mirrors a 2018 incident where Booking.com was fined €475,000 for delayed breach reporting. Customers should be extremely wary of messages requesting payment verification, even when they arrive through the platform itself [[Malwarebytes via Malware.news](https://malware.news/t/booking-com-breach-gives-scammers-what-they-need-to-target-guests/106125#post_1)].

**[NEW] North Korean "laptop farm" operators sentenced to prison**

Two U.S. nationals have been sentenced to prison for operating a "laptop farm" scheme that helped North Korean IT workers pose as U.S. residents and secure employment at over 100 companies, including Fortune 500 firms. Kejia Wang received 108 months and Zhenxing Wang received 92 months for their roles in generating more than $5 million in illicit revenue for the DPRK government between 2021 and October 2024. The pair created fake websites and shell companies, hosted company-issued laptops at U.S. residences, and used stolen identities of more than 80 U.S. citizens. The scheme caused an estimated $3 million in damages to victim companies. Nine other defendants remain at large, with the State Department offering up to $5 million for information leading to their capture. Organizations should strengthen identity verification processes for remote IT workers and monitor for multiple employees accessing resources from the same physical location [[BleepingComputer](https://www.bleepingcomputer.com/news/security/us-nationals-behind-north-korean-it-worker-laptop-farm-sent-to-prison/)].

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Cisco ISE critical vulnerabilities enable remote code execution**

Cisco has released urgent patches for two critical vulnerabilities in its Identity Services Engine (ISE) and ISE Passive Identity Connector products. CVE-2026-20147 (CVSS 9.9) allows authenticated attackers to execute arbitrary commands on the underlying operating system through improper input validation in HTTP requests, potentially escalating to root privileges and triggering denial-of-service conditions in single-node deployments. CVE-2026-20148 (CVSS 4.9) enables path traversal for unauthorized file reading. No workarounds exist—organizations must upgrade to the latest patches (3.1 Patch 11, 3.2 Patch 10, 3.3 Patch 11, 3.4 Patch 6, or 3.5 Patch 3) immediately. The flaws were responsibly reported by Jonathan Lein of TrendAI Research, and no public proof-of-concept or active exploitation has been detected yet [[Cisco Advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ise-rce-traversal-8bYndVrZ); [Cyberpress](https://cyberpress.org/critical-cisco-ise-vulnerabilities-let-remote-attackers-execute-malicious-code/); [GBHackers](https://gbhackers.com/critical-cisco-ise-flaws/)].

**[NEW] Cisco Webex SSO flaw allows complete user impersonation**

Cisco has patched a critical vulnerability (CVE-2026-20184, CVSS 9.8) in Webex Services that allows unauthenticated remote attackers to impersonate any registered user. The flaw stems from improper certificate validation in single sign-on connections with Cisco Control Hub—attackers can send malicious digital tokens that trick Webex servers into treating them as legitimate users, granting access to meetings, files, and private communications. Cisco has patched its cloud infrastructure, but enterprise administrators must manually reconfigure SSO setups by generating and uploading new SAML certificates through the Control Hub dashboard. The Cisco PSIRT team reports no active exploitation or known proof-of-concept attacks [[Cisco Advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-webex-cui-cert-8jSZYhWL); [Cyberpress](https://cyberpress.org/cisco-webex-services-vulnerability/); [GBHackers](https://gbhackers.com/cisco-webex-vulnerability-2/)].

**[NEW] Chrome 147 patches 31 vulnerabilities including 5 critical RCE flaws**

Google has released Chrome version 147.0.7727.101/102 for Windows and macOS (147.0.7727.101 for Linux) to address 31 vulnerabilities, including five rated critical. The most severe flaws include heap buffer overflows in ANGLE (CVE-2026-6296, $90,000 bounty) and Skia (CVE-2026-6298), plus use-after-free vulnerabilities in Proxy (CVE-2026-6297), Prerender (CVE-2026-6299), and XR (CVE-2026-6358). All could enable arbitrary code execution through maliciously crafted HTML pages. Users should update immediately via Help → About Google Chrome [[Google Chrome Releases](https://chromereleases.googleblog.com/2026/04/stable-channel-update-for-desktop_15.html); [Cyberpress](https://cyberpress.org/critical-chrome-vulnerabilities-3/); [GBHackers](https://gbhackers.com/critical-chrome-flaws-allow-arbitrary-code-execution/); [Canadian Centre for Cyber Security](https://cyber.gc.ca/en/alerts-advisories/google-chrome-security-advisory-av26-358)].

**[NEW] Splunk Enterprise and Cloud exposed to remote code execution**

Splunk has disclosed a high-severity vulnerability (CVE-2026-20204, CVSS 7.1) affecting both Enterprise and Cloud Platform environments that allows remote attackers to execute arbitrary code. System administrators should apply the latest patches immediately. Technical details remain limited while patches roll out [[GBHackers](https://gbhackers.com/splunk-enterprise-and-cloud-platform-rce-vulnerability/)].

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] AgingFly malware targets Ukrainian government and hospitals**

Ukraine's CERT-UA has identified a new malware family called "AgingFly" deployed by threat cluster UAC-0247 against local governments and hospitals. The attack chain begins with phishing emails offering humanitarian aid, redirecting to compromised legitimate sites or AI-generated fake sites. Victims receive an archive containing an LNK file that launches an HTA handler, ultimately deploying AgingFly—a C# malware with a unique design: it contains no built-in command handlers, instead receiving them as source code from the C2 server and compiling them on the host at runtime. This approach reduces initial payload size and enables capability changes on demand. The malware steals authentication data from Chromium-based browsers using the ChromElevator tool and extracts WhatsApp data via ZAPiDESK. Organizations should block LNK, HTA, and JS file execution where possible [[CERT-UA via BleepingComputer](https://www.bleepingcomputer.com/news/security/new-agingfly-malware-used-in-attacks-on-ukraine-govt-hospitals/)].

**[NEW] WordPress plugin supply chain compromise backdoors thousands of sites**

Over 30 WordPress plugins in the EssentialPlugin package have been compromised with a backdoor planted after the project was acquired in a six-figure deal in August 2025. The backdoor remained dormant until recently, when it began fetching malicious payloads from an Ethereum-based C2 address for evasion. The malware injects spam links, redirects, and fake pages that are only shown to Googlebot, making them invisible to site owners. WordPress.org has closed the plugins and pushed forced updates to disable the backdoor's communication path, but the malware may persist in wp-config.php and other files. Site administrators running any EssentialPlugin product should audit their installations and check for unauthorized files, particularly anything named `wp-comments-posts.php` (resembling the legitimate `wp-comments-post.php`) [[BleepingComputer](https://www.bleepingcomputer.com/news/security/wordpress-plugin-suite-hacked-to-push-malware-to-thousands-of-sites/)].

**[NEW] Russian infrastructure hosts 1,250+ command-and-control servers**

Infrastructure analytics have identified more than 1,250 active command-and-control servers distributed across 165 Russian hosting providers in the past three months. The mapping effort used Host Radar and HuntSQL to expose the hidden backbone of cyber threats operating inside Russian networks, revealing a concentration of malicious infrastructure that provides threat actors with reliable hosting for ransomware, data theft, and espionage operations. Organizations should consider blocking or closely monitoring traffic to known Russian hosting IP ranges [[GBHackers](https://gbhackers.com/1250-c2-servers/)].

---

## 🛡️ Defense & Detection

**[NEW] AI-generated content abuse manipulates Google Discover for malware delivery**

Researchers from HUMAN's Satori Threat Intelligence team have uncovered "Pushpaganda," a sophisticated campaign leveraging AI-generated news articles to manipulate Google Discover feeds and push malicious notifications. The operation created 113 domains hosting AI-written articles with sensational headlines designed to appear in personalized Discovery feeds alongside legitimate news. At peak, HUMAN observed more than 240 million ad bid requests linked to Pushpaganda-controlled domains in a single week. The campaign uses JavaScript-based tab rotation to inflate engagement metrics and serves scareware, fake alerts, and deepfaked celebrity endorsements. Google has implemented fixes to prevent low-quality AI-generated content from surfacing in Discover, but the campaign demonstrates how AI is scaling social engineering attacks. Defenders should monitor for employees clicking through from Discover feeds to unknown domains [[HUMAN Security via Cyberpress](https://cyberpress.org/google-discover-push-scam/); [GBHackers](https://gbhackers.com/ai-content-hijacks-google/)].

**[NEW] Agentic LLM browsers vulnerable to prompt injection and session hijacking**

A technical analysis of agentic LLM browsers (Perplexity Comet, OpenAI Atlas, Edge Copilot, Brave Leo) reveals that classic web vulnerabilities like XSS can now escalate to full-session takeover through AI agent bridges. In Comet, XSS on any allowed externally_connectable origin can invoke `chrome.runtime.sendMessage` to drive agent tools that read tabs, click UI elements, or send emails as the user. Atlas faces similar risks where XSS on an authorized openai.com subdomain can expose the global Mojo object, allowing attackers to push low-level commands bypassing LLM guardrails. The core paradox: for agentic browsers to be useful, they must cross security boundaries that traditional browsers spent decades hardening. Defenders should monitor extension permissions and consider restricting agentic browser use in high-security environments until architectural safeguards mature [[Varonis Threat Labs via Cyberpress](https://cyberpress.org/agentic-browsers-face-injection/)].

---

## 📋 Policy & Industry News

**[NEW] NIST narrows CVE analysis scope amid vulnerability deluge**

The National Institute of Standards and Technology has announced it will narrow the scope of CVE analysis for the National Vulnerability Database (NVD) to achieve long-term sustainability. NIST will now prioritize analysis only for CVEs appearing in CISA's Known Exploited Vulnerabilities catalog, software used by the federal government, and critical software defined under Executive Order 14028. CVEs not meeting these criteria will still be listed but won't receive automatic enrichment with severity scores and other metadata. NIST analyzed nearly 42,000 vulnerabilities last year while CVE submissions surged 263% from 2020 to 2025, with Q1 2026 submissions one-third higher than the same period last year. The agency still hasn't cleared a backlog from a 2024 funding lapse. This shift effectively forces organizations to rely more heavily on CNAs and private vulnerability intelligence sources for comprehensive coverage [[CyberScoop](https://cyberscoop.com/nist-narrows-cve-analysis-nvd/)].

**[NEW] OpenAI limits access to GPT-5.4-Cyber model for security professionals**

OpenAI has announced GPT-5.4-Cyber, an AI model designed to rapidly detect software vulnerabilities but restricted to a vetted set of security professionals. The move mirrors Anthropic's earlier decision to limit access to its Mythos model. Both models can identify vulnerabilities in software but could similarly accelerate exploit development if misused. OpenAI is permitting access to a larger pool of security professionals than Anthropic, but the controlled rollout reflects growing industry concerns about dual-use AI capabilities in cybersecurity [[Security Boulevard via Malware.news](https://malware.news/t/openai-follows-anthropic-in-limiting-access-to-its-cyber-focused-model/106114#post_1)].

**[NEW] March 2026 cyber attack statistics show sharp increase in incidents**

Analysis of 282 cyber attacks in March 2026 shows a sharp increase compared to 176 events in February. Cyber Crime continued to dominate motivations at 64%, followed by Cyber Espionage at 15%, Hacktivism at 6%, and Cyber Warfare at 3%. The data reflects continued high-volume criminal activity alongside persistent state-sponsored espionage operations [[Hackmageddon via Malware.news](https://malware.news/t/march-2026-cyber-attacks-statistics/106126#post_1)].

---

## ⚡ Quick Hits

- **Microsoft April Windows Server 2025 update failing to install**: Microsoft is investigating an issue causing KB5082063 security update failures on Windows Server 2025 systems, with users reporting 0x800F0983 install errors. A limited number of servers are affected [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-april-windows-server-2025-update-may-fail-to-install/)].

- **DragonForce ransomware hits multiple targets**: The ransomware group claimed attacks against McCOR (Canadian real estate), Bela-Pharm GmbH (German veterinary pharmaceuticals), and Curtis Design Group (U.S. architecture), threatening data leaks if negotiations aren't initiated [[DeXpose via Malware.news](https://malware.news/t/dragonforce-ransomware-attack-on-canadian-real-estate-leader-mccor/106119#post_1); [DeXpose via Malware.news](https://malware.news/t/dragonforce-targets-bela-pharm-gmbh-in-ransomware-attack/106118#post_1); [DeXpose via Malware.news](https://malware.news/t/dragonforce-targets-architecture-firm-curtis-design-group-in-ransomware-attack/106116#post_1)].

- **Qilin ransomware targets Italian construction leader**: Qilin claimed responsibility for an attack against Gruppo ICM SPA, an Italian construction firm, threatening to leak sensitive data [[DeXpose via Malware.news](https://malware.news/t/qilin-ransomware-targets-italian-construction-leader-gruppo-icm-spa/106117#post_1)].

- **Akira ransomware hits U.S. auto dealership**: Akira ransomware claimed an attack against Fletcher Chrysler Products, threatening to release 28GB of data including employee personal information and financial records [[DeXpose via Malware.news](https://malware.news/t/akira-ransomware-hits-fletcher-chrysler-products/106115#post_1)].

- **AI coding tools vulnerable to prompt injection via comments**: Claude Code, Gemini CLI, and GitHub Copilot Agents are vulnerable to prompt injection attacks delivered through code comments, potentially allowing attackers to manipulate AI-assisted development workflows [[SecurityWeek](https://www.securityweek.com/claude-code-gemini-cli-github-copilot-agents-vulnerable-to-prompt-injection-via-comments/)].