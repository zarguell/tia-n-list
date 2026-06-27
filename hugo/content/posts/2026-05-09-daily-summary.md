---
title: "Dirty Frag Exploitation, Polish Water ICS Breaches, CISA 4-Day Ivanti Patch, ShinyHunters Extends Deadline"
date: 2026-05-09
tags: ["dirty-frag","linux-kernel","ivanti","cisa","shinyhunters","canvas","trellix","ransomhouse","pam-backdoor","poland","ics","ai-security","claude"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Microsoft confirms active Dirty Frag Linux kernel exploitation in the wild while CVE-2026-43500 remains unpatched. Polish intelligence reports ICS breaches at five water treatment plants attributed to APT28/APT29. CISA gives federal agencies four days to patch Ivanti EPMM zero-day."
---

# Tia N. List — Daily Threat Intelligence Digest
### May 9, 2026

**~48 articles ingested from Miniflux Cyber feeds across the past 24 hours.**

*Previous 5 days reporting summary:* Yesterday's digest covered Dirty Frag Linux kernel LPE (CVE-2026-43284, CVE-2026-43500) as a new zero-day class related to Copy Fail, ShinyHunters defacing 330 Canvas login portals in a second Instructure breach, ClaudeBleed Chrome extension takeover, PAN-OS CVE-2026-0300 CISA KEV addition with Chinese state-sponsored hallmarks, PCPJack worm targeting cloud infrastructure, Microsoft Semantic Kernel AI agent RCE (two CVEs), Ivanti EPMM zero-day CVE-2026-6973, Next.js critical vulnerability cluster, Rancher Fleet multi-tenant isolation bypass, Claude Code OAuth token theft via MCP hijacking, and TCLBanker banking trojan. Earlier this week: Copy Fail CISA KEV listing, Weaver E-cology RCE, Microsoft "code of conduct" AiTM phishing, Argo CD Kubernetes secret extraction, DarkSword iOS exploit kit, DAEMON Tools supply-chain breach, Instructure Canvas breach (280M records), PAN-OS zero-day, DAEMON Tools trojanized installers, and the Trellix source code breach.

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Dirty Frag — Microsoft confirms active exploitation, CVE-2026-43284 patched but CVE-2026-43500 remains unpatched with no fix timeline**

Microsoft Defender is observing limited in-the-wild exploitation of Dirty Frag, with telemetry showing external SSH connections spawning interactive shells followed by execution of an ELF binary (`./update`) that triggers privilege escalation via `su`. Post-exploitation activity includes modification of GLPI LDAP authentication files, reconnaissance of system configuration, deletion of PHP session files, and harvesting of session contents — a blend of credential theft and operational disruption. As of May 8, CVE-2026-43284 (xfrm-ESP Page-Cache Write) has been patched in mainline Linux, but CVE-2026-43500 (RxRPC Page-Cache Write) has no available patches. The RxRPC vector is particularly dangerous because it requires only normal user privileges — no user-namespace creation needed — meaning it works on hardened Ubuntu systems where AppArmor blocks the ESP path. Qualys notes that the exploit does not touch files on disk: malicious changes persist only in RAM page caches until reboot or cache flush, making file-hash-based detection tools blind to exploitation. Organizations should disable `esp4`, `esp6`, and `rxrpc` kernel modules where operationally feasible, clear page caches (`echo 3 > /proc/sys/vm/drop_caches`), and prioritize kernel patches as vendors release them. Canada's Cyber Centre has issued alert AL26-011 with distribution-specific guidance. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/08/active-attack-dirty-frag-linux-vulnerability-expands-post-compromise-risk/); [Qualys](https://blog.qualys.com/product-tech/vulnmgmt-detection-response/2026/05/09/dirty-frag-using-the-page-caches-as-an-attack-surface); [Tenable](https://www.tenable.com/blog/dirty-frag-cve-2026-43284-cve-2026-43500-frequently-asked-questions-linux-kernel-lpe)]

**[UPDATE] Ivanti EPMM CVE-2026-6973 — CISA adds to KEV with 4-day patch deadline as 850+ appliances remain exposed**

CISA has added CVE-2026-6973 to its Known Exploited Vulnerabilities catalog, requiring federal agencies to patch by midnight Sunday, May 10 — just four days after disclosure. The flaw allows remote attackers with admin privileges to execute arbitrary code on Ivanti EPMM 12.8.0.0 and earlier. Shadowserver tracks over 850 internet-exposed EPMM instances (508 in Europe, 182 in North America). Ivanti describes exploitation as "very limited" and notes that customers who rotated credentials after January's CVE-2026-1281 and CVE-2026-1340 EPMM zero-days have significantly reduced risk. This brings CISA's total count of exploited Ivanti vulnerabilities to 33, with 12 also abused by ransomware operations. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-gives-feds-four-days-to-patch-ivanti-flaw-exploited-as-zero-day/)]

**[UPDATE] ShinyHunters extends Canvas extortion deadline to May 12 — lists Harvard, MIT, Cambridge among ~9,000 affected institutions**

ShinyHunters has extended its extortion deadline from May 8 to May 12, providing additional details about the Instructure breach's scope. The group claims nearly 9,000 educational institutions are affected and is now directly pressuring individual schools to negotiate settlements, advising them to contact the group via Tox messaging. The published list includes school districts alongside major universities including Cambridge, Columbia, Cornell, Georgetown, Harvard, MIT, and UC Berkeley. Affected data reportedly includes names, email addresses, student ID numbers, and user communications — but not passwords, dates of birth, or financial information. Instructure has not responded to press inquiries about breach notifications to affected individuals. [[CyberScoop](https://edscoop.com/shinyhunters-claims-nearly-9000-schools-affected-by-canvas-data-breach/)]

**[NEW] Polish security agency reports ICS breaches at five water treatment plants — APT28 and APT29 attributed**

Poland's Internal Security Agency (ABW) has documented security breaches at five water treatment stations across the municipalities of Jabłonna Lacka, Szczytno, Małdyty, Tolkmicko, and Sierakowo. In some cases, attackers gained ICS access with the ability to modify operational parameters of equipment, creating direct risk to public water supply. The attack vectors were weak password policies and systems directly exposed to the internet. ABW attributes primary responsibility to Russian intelligence services — specifically APT28 and APT29 — operating through hacktivist personas, alongside UNC1151 (Belarus-linked). The incidents are part of a broader escalation targeting Polish critical infrastructure including energy, wastewater, and supply chains, with attackers seeking contract data, project documentation, and authentication credentials for downstream access. [[SecurityWeek](https://www.securityweek.com/polish-security-agency-reports-ics-breaches-at-five-water-treatment-plants/)]

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] RansomHouse claims Trellix source code breach — intrusion occurred April 17, screenshots published as proof**

RansomHouse has officially listed Trellix on its dark web extortion portal, claiming the intrusion occurred on April 17 and resulted in data encryption. The group published screenshots showing access to Trellix's appliance management system. Trellix confirmed awareness of the claims and stated its investigation continues. Initial forensics found no evidence that source code release or distribution processes were affected, and no indication of active exploitation of accessed code. RansomHouse has evolved from pure data extortion to deploying advanced encryption tools including 'Mario' (dual-encryption pass) and 'MrAgent' (VMware ESXi automation). The group's recent high-profile targets include Japanese e-commerce giant Askul Corporation (740,000 customer records stolen). [[BleepingComputer](https://www.bleepingcomputer.com/news/security/trellix-source-code-breach-claimed-by-ransomhouse-hackers/); [Cyber Security News](https://cyberpress.org/ransomhouse-claims-trellix-breach/)]

## ⚠️ Vulnerabilities & Patches

**[UPDATE] Claude Chrome extension vulnerability — partial fix bypassable by switching to "privileged" extension mode**

LayerX researcher Aviad Gispan has published additional details on the Claude Chrome extension vulnerability disclosed as "ClaudeBleed." Anthropic's May 6 fix introduced approval flows for "standard" mode extensions, but Gispan demonstrated that switching to "privileged" mode bypasses these checks entirely with no user notification or consent. The root cause remains Claude's reliance on origin-based trust rather than execution context validation — any JavaScript running on `claude.ai` can issue privileged commands. LayerX's proof of concept extracted files from Google Drive, sent emails on behalf of the user, and pilfered source code from GitHub repositories, all while Claude's UI was modified to hide sensitive labels and cover tracks by deleting evidence. Ax Sharma of Manifold Security characterized the attack as demonstrating why "monitoring AI agents at the prompt layer is fundamentally insufficient." [[CyberScoop](https://cyberscoop.com/claude-chrome-extension-allows-plugins-to-hijack-ai/)]

**[NEW] cPanel patches three new vulnerabilities — CVE-2026-29201, CVE-2026-29202, CVE-2026-29203**

cPanel has released security updates addressing three vulnerabilities tracked as CVE-2026-29201, CVE-2026-29202, and CVE-2026-29203. Details on severity and exploitation status are limited, but this comes just one week after mass exploitation of CVE-2026-41940 compromised over 40,000 servers worldwide. cPanel administrators should apply updates immediately given the active targeting of the platform. [[Malware.News](https://malware.news/t/cpanel-security-advisory-av26-437/106821#post_1)]

## 🛡️ Defense & Detection

**[NEW] PamDOORa — new Linux PAM backdoor harvests SSH credentials, sold for $900 on Russian forums**

Group-IB's DFIR team has documented a Linux persistence technique dubbed "PamDOORa" that weaponizes the `pam_exec` module to execute malicious code during SSH authentication events. By inserting a malicious entry with the `optional` control flag into `/etc/pam.d/sshd`, the backdoor collects usernames, timestamps, and environment variables (PAM_USER, PAM_RHOST, PAM_SERVICE) during every login attempt — even failed ones — and exfiltrates to a C2 server via netcat. The `optional` flag ensures the malicious execution doesn't disrupt normal authentication, leaving minimal traces in system logs. The technique is particularly insidious because logs show only failed SSH logins while credential harvesting runs silently in the background. The source code is being marketed by threat actor "darkworm" for $900 on Russian cybercrime forums. Organizations should audit PAM configurations, monitor for unauthorized changes in `/etc/pam.d/`, implement file integrity monitoring, and deploy SELinux or AppArmor policies. [[GBHackers](https://gbhackers.com/pam-backdoor-targets-linux-systems/); [SecurityWeek](https://www.securityweek.com/in-other-news-train-hacker-arrested-pamdoora-linux-backdoor-new-cisa-director-frontrunner/)]

**[NEW] NVIDIA confirms GeForce NOW data breach via Armenian partner — limited to regional operator GFN.am**

NVIDIA has confirmed that GeForce NOW user information was exposed in a data breach limited to the Armenian regional partner GFN.am, which operates the cloud gaming service across Armenia, Azerbaijan, Georgia, Kazakhstan, Moldova, Ukraine, and Uzbekistan. A threat actor using the ShinyHunters nickname — believed to be an imposter — posted the stolen database for $100,000 on a hacker forum (now removed). The breach occurred between March 20 and 26 and exposed full names, email addresses, phone numbers, dates of birth, and usernames. No passwords were exposed. NVIDIA's own network was not impacted. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/nvidia-confirms-geforce-now-data-breach-affecting-armenian-users/); [GBHackers](https://gbhackers.com/nvidia-confirms-geforce-data-breach/)]

## 📋 Policy & Industry News

**[NEW] Sen. Schumer calls on DHS to coordinate AI cyber defense with state and local governments**

Senate Minority Leader Chuck Schumer has written to DHS Secretary Markwayne Mullin urging the department to work with state, local, tribal, and territorial governments on defending against AI-strengthened cyberattacks. Schumer warned of "a race between cybersecurity defenders and AI-enabled hacking" and pressed DHS to ensure SLTT governments aren't left behind as AI models advance. The letter reflects growing concern that smaller government entities lack the resources to keep pace with AI-powered threats. [[CyberScoop](https://cyberscoop.com/chuck-schumer-seeks-dhs-plan-on-ai-cyber-coordination-with-state-local-governments/)]

**[NEW] IBM executive Tom Parker emerges as frontrunner for CISA director**

Tom Parker, IBM's security services lead and founder of Hubble, has emerged as the primary candidate to lead CISA under the Trump administration, following the withdrawal of Sean Plankey. Parker's private-sector background aligns with the administration's preference for industry experience. He would succeed acting director Nick Andersen. [[SecurityWeek](https://www.securityweek.com/in-other-news-train-hacker-arrested-pamdoora-linux-backdoor-new-cisa-director-frontrunner/)]

## ⚡ Quick Hits

- **Metasploit adds ARMLE Linux support for Copy Fail exploit** — Rapid7's Copy Fail module now supports ARM-based Linux targets and fixes payload execution bugs, expanding exploitation coverage for CVE-2026-31431 to embedded and IoT devices. [[Rapid7](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-05-08-2026)]

- **Vidar infostealer campaign uses trojanized Microsoft Toolkit with AutoIt loader** — A sophisticated multi-stage campaign delivers Vidar stealer via a pirated Microsoft Toolkit, using extension masquerading (.dot→.bat), AutoIt-based loading, and Telegram/Steam profile C2 discovery. The malware thoroughly destroys forensic artifacts post-execution. [[Cyber Security News](https://cyberpress.org/vidar-malware-campaign-targets-login-credentials/); [GBHackers](https://gbhackers.com/vidar-infostealer-campaign-steals-passwords-cookies/)]

- **PAN-OS CVE-2026-0300 exploitation recap — patches still May 13–28** — Truesec publishes a consolidated exploitation timeline showing unsuccessful attempts from April 9, successful shellcode injection one week later into nginx worker processes, with patches still 4+ days away. [[Malware.News](https://malware.news/t/active-exploitation-of-pan-os-authentication-portal-rce/106806#post_1)]

- **US may shift federal patch cycles from 14 days to 3 days** — Driven by AI models like Anthropic Mythos and OpenAI GPT-5.4-Cyber enabling faster weaponization, federal remediation timelines may shrink dramatically. CISA already instructs 3-day patches for some high-risk vulnerabilities. [[SecurityWeek](https://www.securityweek.com/in-other-news-train-hacker-arrested-pamdoora-linux-backdoor-new-cisa-director-frontrunner/)]

---

*48 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*
