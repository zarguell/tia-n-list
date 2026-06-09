---
title: "🛡️ Check Point VPN CISA Mandate, LiteLLM RCE Exploited, Chrome 5th Zero-Day, Shai-Hulud PyPI, NSO Contempt"
date: 2026-06-09
tags: ["CVE-2026-50751","Check Point","Qilin","CISA","Chrome","CVE-2026-11645","LiteLLM","Shai-Hulud","PyPI","NSO Group","Pegasus","Gogs","Zcash","APT29","Teams phishing","AI scams"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CISA orders emergency Check Point VPN patching as Qilin ransomware exploits CVE-2026-50751. LiteLLM RCE chain (CVE-2026-42271 + CVE-2026-48710, CVSS 10.0) under active exploitation as AI supply chain threats intensify. Google patches 5th Chrome zero-day; Gogs critical RCE patched with 2,300+ instances exposed. Shai-Hulud PyPI campaign expands to bioinformatics tooling. Meta files contempt against NSO Group for renewed spyware attacks."
---
# Daily Threat Intelligence Digest — June 9, 2026

*68 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — old.reddit.com returned errors on both `/hot/` and `/new/` endpoints. External gap detection via web search identified one critical gap: LiteLLM RCE chain (CVSS 10.0) being actively exploited — zero Miniflux coverage. tl;dr sec #331 (June 4) skipped — 5 days stale. Prior digests: June 4–8, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] LiteLLM RCE Chain Actively Exploited — CVE-2026-42271 + CVE-2026-48710, CVSS 10.0, Unauthenticated RCE on AI Gateway Proxy** [web search gap]

Threat actors are actively exploiting a chained vulnerability in LiteLLM, the popular open-source AI gateway proxy, combining two flaws for a **CVSS 10.0 unauthenticated remote code execution** attack path requiring zero credentials. Horizon3.ai researchers confirmed the chain works end-to-end. [[CyberSecurityNews](https://cybersecuritynews.com/litellm-rce-vulnerability-exploited/)]

**How it works:** CVE-2026-42271 is a command injection flaw in LiteLLM's Model Context Protocol (MCP) server test endpoints — endpoints like `POST /mcp-rest/test/connection` and `POST /mcp-rest/test/tools/list` accept full server configurations (commands, args, environment variables) and spawn the supplied input as a subprocess on the host. When initially disclosed on April 20, the flaw was considered limited because exploitation required a valid proxy API key. That assumption fell when Horizon3.ai chained it with **CVE-2026-48710**, a Starlette "BadHost" Host Header validation bypass (Starlette ≤ 1.0.0). By manipulating the HTTP Host header, attackers sidestep LiteLLM's API key requirement entirely.

**Impact:** Once code execution is achieved, attackers can execute arbitrary OS commands on the LiteLLM host, steal API keys and model provider credentials stored by the proxy, access secrets and environment variables, and move laterally into connected AI infrastructure and downstream systems. The LiteLLM proxy sits at the gateway layer between organizations and LLM providers — compromising it means the attacker controls the choke point for all AI API traffic.

**Affected:** LiteLLM 1.74.2 through 1.83.6 with Starlette ≤ 1.0.0.

**Action:** Upgrade LiteLLM to 1.83.7+ and Starlette to 1.0.1+ as emergency priority. Block external access to MCP test endpoints. Rotate all credentials and API keys stored by the proxy. Monitor for requests targeting `/mcp-rest/test/connection` or `/mcp-rest/test/tools/list` with anomalous Host header values.

---

**[UPDATE] CISA Orders Feds to Patch Check Point VPN Zero-Day by June 11 — Qilin Ransomware Gang Confirmed Exploiting CVE-2026-50751**

CISA added **CVE-2026-50751** (CVSS 9.3) to its Known Exploited Vulnerabilities catalog on Monday, ordering Federal Civilian Executive Branch agencies to patch by June 11 under BOD 22-01. The authentication bypass in Check Point Remote Access VPN and Mobile Access deployments (IKEv1-only) has been exploited in zero-day attacks since May 7, with a surge in early June. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-orders-feds-to-patch-check-point-flaw-exploited-by-ransomware-gangs/); [Rapid7](https://www.rapid7.com/blog/post/etr-critical-check-point-vpn-zero-day-exploited-in-the-wild-cve-2026-50751); [BleepingComputer](https://www.bleepingcomputer.com/news/security/check-point-links-vpn-zero-day-attacks-to-qilin-ransomware-gang/)]

Check Point Research confirmed at least one breach has been linked to a **Qilin ransomware affiliate**, with post-compromise activity including ELF payload retrieval from attacker VPS infrastructure (providers: Kaupo Cloud HK, Shock Hosting, Vultr Holdings). The attacks have affected "a few dozen" organizations globally, with VPS regions matching target geography.

While investigating the flaw, Check Point discovered a second vulnerability — **CVE-2026-50752** (CVSS 7.4) — in the same IKEv1 code path enabling man-in-the-middle attacks against site-to-site VPN tunnels. No exploitation observed yet.

**IOCs:** Attacker IPs include 45.77.149.152, 209.182.225.136, 38.60.157.139, 162.33.177.101, 45.76.26.42, 144.208.127.155, 38.54.88.201, 38.54.107.167, 66.42.99.200. MD5 hashes: 52fda5c1b9704544f32ee98d9060e689, 51d39aa39478beeac94f2d12f682ecce.

**Mitigation:** Apply hotfixes immediately — four of the nine affected version branches (R80.20.X, R80.40, R81, R81.10) are End of Support and require migration. Compensating controls: disable legacy remote access client, force IKEv2 only, require machine certificate authentication, enable IPS signatures.

---

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] Shai-Hulud PyPI Supply Chain Expands — 19 Bioinformatics Packages Trojanized, 37 Malicious Releases**

A new wave of the Shai-Hulud supply-chain campaign compromised **19 packages on PyPI** — many popular bioinformatics tools including Dynamo, Spateo, CoolBox, U-FISH, and Napari-UFISH — collectively downloaded hundreds of thousands of times. Socket discovered **37 malicious releases** from what appears to be a single maintainer. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-shai-hulud-attack-trojanizes-19-science-focused-pypi-packages/)]

**Novel technique:** The malicious artifacts include a `*-setup.pth` file and an obfuscated `_index.js` payload. The `.pth` file executes automatically when **any Python process starts** — pip, pytest, Jupyter notebook, CI job — making it a delayed-execution trigger that evades traditional install-time scanners. On execution, it downloads the Bun JavaScript runtime from GitHub to run the bundled script.

**Credential targeting:** The JS payload harvests GitHub tokens/Actions secrets, npm/PyPI/RubyGems/JFrog publishing tokens, AWS/GCP/Azure/Kubernetes/Vault credentials, SSH keys, Docker credentials, `.env`/`.npmrc`/`.pypirc` files, shell histories, and **Claude/MCP configuration files** — continuing the pattern of targeting AI coding tooling credentials.

**Exfiltration:** Primary method uses auto-created GitHub repositories as dead-drops via GitHub Actions. Secondary HTTPS exfiltration targets a legitimate-but-invalid Anthropic API endpoint (`api.anthropic.com/v1/api`) as camouflage.

**Defense:** Look for Python packages containing executable `.pth` startup hooks, unexpected downloads of the Bun runtime, and process chains where Python launches Bun to execute `_index.js`. Rotate all secrets on any affected system.

---

**[UPDATE] NSO Group Defies Court Order — Meta Files Contempt Complaint, WhatsApp Disrupts New Spear-Phishing Campaigns**

Meta has filed a contempt of court complaint against NSO Group after detecting new spear-phishing campaigns targeting WhatsApp users, despite a 2025 permanent injunction and $168 million judgment barring the spyware vendor from targeting the platform. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/whatsapp-says-it-disrupted-new-nso-spyware-phishing-attacks/); [CyberScoop](https://cyberscoop.com/meta-contempt-complaint-nso-group-spyware/); [SecurityWeek](https://www.securityweek.com/whatsapp-catches-spyware-firm-nso-defying-no-hacking-court-order/)]

WhatsApp detected 1-click phishing campaigns using malicious links to drive targets to external websites — similar to NSO operations linked to infections of journalists and activists in Jordan (2019–2023). Meta also caught attackers creating test accounts and groups on WhatsApp. **IOC domains:** `ikhwancast[.]com`, `ghazacast[.]com`, `fr24cast[.]com`.

Meta argues this defiance proves NSO Group should remain on the U.S. Entity List (sanctioned since November 2021). Citizen Lab's John Scott-Railton: "NSO's own actions make the strongest argument for why they should stay on the Entity list."

---

**[UPDATE] TeamPCP Supply Chain Campaign — Activity Through June 7, U.S. Government Formally Engaged**

The SANS ISC published its latest tracking diary on the TeamPCP supply chain campaign, noting two major developments: the **United States government has formally engaged** with the campaign, and a wider population of attackers is now weaponizing the open-sourced Mini Shai-Hulud framework that TeamPCP released in May. [[Malware.News/SANS](https://malware.news/t/teampcp-supply-chain-campaign-activity-through-2026-06-07-mon-jun-8th/107662#post_1)]

This update follows the Miasma worm's June 5 attack on 73 Microsoft GitHub repositories (covered June 8) and the ongoing Phantom Gyp/Shai-Hulud waves hitting npm and PyPI. The open-sourcing of the worm framework is enabling a democratization of supply chain attacks — the barrier to entry for worm-based credential harvesting has dropped dramatically.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Google Patches 5th Chrome Zero-Day of 2026 (CVE-2026-11645) — V8 Engine OOB Read/Write Exploited in the Wild**

Google released emergency updates for Chrome Stable Desktop (Windows 149.0.7827.102, Mac 149.0.7827.103, Linux 149.0.7827.102) to patch **CVE-2026-11645**, a high-severity out-of-bounds read/write vulnerability in the V8 JavaScript engine exploited in the wild. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/google-patches-fifth-chrome-zero-day-bug-exploited-in-attacks-this-year/); [SecurityWeek](https://www.securityweek.com/google-patches-5th-chrome-zero-day-exploited-in-2026/)]

The zero-day allows remote code execution inside Chrome's sandbox via crafted HTML pages, with potential to bypass ASLR. This is the **5th Chrome zero-day exploited in 2026**, following CVE-2026-2441 (Feb), CVE-2026-3909/CVE-2026-3910 (Mar), and CVE-2026-5281 (Apr). Google has not disclosed attack details. **Action:** Update Chrome immediately on all endpoints.

---

**[NEW] Gogs Patches Critical Zero-Day RCE — 2,300+ Exposed Instances at Risk**

Gogs released version 0.14.3 on June 7 to patch a critical argument injection vulnerability (no CVE yet) that allows any authenticated user to achieve remote code execution and access any repository — including private ones. Discovered by Rapid7's Jonah Burgess. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/gogs-patches-critical-zero-day-enabling-remote-code-execution/)]

**Key risk:** Gogs ships with open registration **enabled by default**. Any unauthenticated attacker can create an account, create a repo, enable rebase merging, and trigger the exploit — no admin interaction needed. ShadowServer tracks **2,300+ internet-exposed Gogs instances** (1,839 in Asia, 312 in Europe).

This is similar to prior Gogs flaws (CVE-2024-39933, CVE-2024-39932, CVE-2026-26194) but affects a previously unpatched code path. In December 2025, a different Gogs RCE (CVE-2025-8110) was exploited in zero-day attacks to compromise hundreds of servers. **Action:** Update to 0.14.3 immediately; disable open registration in `app.ini` as compensating control.

---

**[NEW] Critical Zcash Vulnerability Found and Fixed — Orchard Pool Bug Could Generate ZEC from Nothing**

Security researcher Taylor Hornby discovered a critical vulnerability in Zcash's **Orchard privacy pool** using Claude Opus 4.8 — a flaw that could have allowed an attacker to generate ZEC from nothing by feeding false inputs into a transaction validation check. The zero-knowledge proof system would have blessed the fraudulent transaction as valid. [[Schneier on Security](https://www.schneier.com/blog/archives/2026/06/critical-zcash-vulnerability-found-and-fixed.html)]

The bug was found on May 29 during a targeted audit engagement. It has been patched, but there is no way to determine if it was exploited prior to discovery. The Orchard pool is Zcash's newest shielded transaction system, introduced in 2022 for private transactions.

---

## 🛡️ Defense & Detection

**[NEW] Cloaked Ursa (APT29) Abusing Microsoft Teams for Social Engineering — Unit 42 Documents 42% of Phishing Alerts Now From Collaboration Tools**

Palo Alto Networks Unit 42 published a deep dive on threat actors weaponizing Microsoft Teams for social engineering, documenting recent activity by **Cloaked Ursa (APT29/Cozy Bear/Midnight Blizzard)** and the Mandiant-tracked **UNC6692**. [[Unit 42](https://unit42.paloaltonetworks.com/microsoft-teams-phishing/)]

**The shift:** In the first four months of 2026, phishing alerts from collaboration tools represented **42% of all phishing alerts** in Cortex — up from 30% in the preceding four months. Email gateways have improved detection, so attackers are moving to trusted internal tools.

**Attack flow:** Attackers initiate external Teams chats impersonating IT helpdesk, using typosquatted domains or compromised legitimate service provider accounts. They convince employees to approve MFA prompts or click credential-harvesting links. In many organizations, Teams federation is enabled by default, allowing communication with any external tenant.

**Recommendation:** Restrict Teams federation to an allowlist of known external domains; disable communication with unmanaged Teams accounts; train users that Teams messages can originate externally; monitor external chat initiation as a high-fidelity detection signal.

---

**[NEW] AI Brands as Bait — Microsoft Documents Large-Scale AI-Themed Phishing and Malvertising Ecosystem**

Microsoft Threat Intelligence published a comprehensive report on threat actors using AI brand names — **ChatGPT, Claude, DeepSeek, Copilot** — as social engineering lures across phishing, malvertising, and SEO-driven campaigns. These are brand-abuse campaigns, not compromises of the AI services themselves. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/06/08/ai-brands-as-bait-how-threat-actors-are-using-the-ai-hype-in-social-engineering/)]

**Key campaigns detailed:**
- **ChatGPT payment phishing (May 5):** 4,500+ emails targeting South Africa (97%) pretending to be ChatGPT Plus subscription renewal; multi-hop redirect chain through Bitrix24, AWS track, Rebrandly, to a compromised domain; collected credit card data.
- **Claude AUP phishing (April 20-22):** 2,000+ organizations targeted (62% US, 18% UK, 9% India); PDF attachment with "Claude Appeal Request" linking to AiTM credential harvesting pages; used CAPTCHA-gating to evade automated analysis.
- **"Awesome AI Windows Plugin" malvertising:** Storm-3075 initial access broker delivered Vidar, Lumma, Hijack Loader, and Oyster via fake AI plugin downloads from free movie streaming sites. A single March 13 campaign hit **66,000 devices**. Malware was signed with fraudulently obtained Microsoft code-signing certificates attributed to **Fox Tempest** (MSaaS operation disrupted in May 2026).
- **Fake DeepSeek V4 installers on GitHub:** Within hours of DeepSeek's V4 announcement, attackers created a fraudulent GitHub repository with stolen branding and real benchmark data. Delivered Vidar stealer via 102 MB .7z archives. Same shared loader hash appears under filenames impersonating GPT-5.5, Claude Code, Kimi, Manus AI, and more.

**Bottom line:** AI-brand lures are becoming the dominant social engineering theme of 2026. The same infrastructure and payloads rotate through whichever AI tool is trending. Defenders should inventory AI tool usage and treat AI-themed download/search results as high-risk surfaces.

---

## 📋 Policy & Industry News

**[NEW] Americans Lost Nearly $900 Million to AI-Powered Scams in 2025, FBI Reports**

The FBI's 2025 Internet Crime Report documented **$893,346,472 in AI-related scam losses** from 22,364 complaints — likely the tip of the iceberg. [[Malware.News/Malwarebytes](https://malware.news/t/americans-lost-nearly-900-million-to-ai-powered-scams-fbi-says/107658#post_1)]

The main drivers: **voice cloning, deepfake images/videos, and AI-generated scripts** supercharging classic fraud (romance scams, kidnapping/extortion calls, government impersonation). A particular concern is government impersonation scams evolving from crude IRS gift-card calls into sophisticated multi-channel operations combining spoofed caller ID, stolen agency logos, and AI-generated audio/video of public officials. AI is also accelerating business email compromise (BEC), with losses reaching tens of millions per incident.

---

## ⚡ Quick Hits

- **[NEW] NFCShare Android malware targets European banks via fake GitHub APK updates** — New variants distributed as fake banking app updates on GitHub, stealing NFC payment card data via Android's IsoDep interface. Targets primarily Italian and Spanish banks. 56 unique malicious APKs since April 10. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/nfcshare-android-malware-spreads-via-fake-banking-app-updates-on-github/)]
- **[NEW] SoFi Hong Kong confirms third-party data breach** — Hackers accessed a customer database at a third-party vendor. Breach discovered April 30; scope still unknown. SoFi warning customers of phishing risk. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/sofi-confirms-third-party-data-breach-at-hong-kong-subsidiary/)]
- **[NEW] TheGentlemen ransomware hits 6+ new victims globally** — New DeXpose victim listings including Yao Yuan Technology (Taiwan), Trigon America, The Clinic (North Dakota), Integrated Distribution Inc, Institucion Cervantes, and Tress (Danish sports equipment supplier). Low-analytical-value DeXpose entries; included for victim tracking. [[Malware.News](https://malware.news/t/thegentlemen-target-taiwanese-tech-firm-yao-yuan-technology/107672#post_1)]
- **[NEW] Payload ransomware targets Hansoll Textile in Vietnam** — Threat actors warn data will be leaked unless demands are met. [[Malware.News/DeXpose](https://malware.news/t/payload-ransomware-targets-hansoll-textile-in-vietnam/107671#post_1)]
- **[NEW] Essex NHS hospitals: 2,380 patient records compromised** — Mid and South Essex NHS Foundation Trust confirms data theft linked to third-party provider Synnovis. [[Malware.News/DataBreaches.net](https://malware.news/t/essex-nhs-hospitals-records-compromised-in-cyber-attack/107639#post_1)]
- **[NEW] Cyberattack closes Evanston Township High School** — Ransomware forces cancellation of summer school, sports camps, and on-campus activities. [[Malware.News/DataBreaches.net](https://malware.news/t/cyberattack-closes-evanston-township-high-school/107638#post_1)]
- **[NEW] 174,000 impacted by Lansing Community College data breach** [[SecurityWeek](https://www.securityweek.com/174000-impacted-by-lansing-community-college-data-breach/)]
- **[NEW] Handala claims Israeli radar disruption — SOCRadar analysis finds evidence unsubstantiated** — The Iranian-linked group's Telegram claims of disrupting Israeli radar systems coincide with missile exchanges but lack supporting evidence. Shared screenshots show municipal phone system access, not military radar. [[Malware.News/SOCRadar](https://malware.news/t/handala-claims-it-disrupted-israeli-radar-systems-here-s-what-we-actually-know/107644#post_1)]
- **[NEW] Cybersecurity M&A Roundup: 26 deals in May 2026** — SecurityWeek's monthly tally. [[SecurityWeek](https://www.securityweek.com/cybersecurity-ma-roundup-26-deals-announced-in-may-2026/)]
- **[NEW] Hokkaido hospitals data leak may hit 510,000 — HDDs sold online blamed** [[Malware.News](https://malware.news/t/jp-hokkaido-hospitals-data-leak-may-hit-510k-hdds-sold-online-blamed/107665#post_1)]

---

*68 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — old.reddit.com returned errors on both `/hot/` and `/new/` endpoints. External gap detection via web search identified one critical gap: LiteLLM RCE chain (CVE-2026-42271 + CVE-2026-48710) actively exploited, zero Miniflux coverage. Prior digests: June 4–8, 2026. Sources include BleepingComputer, Rapid7, CyberSecurityNews, SecurityWeek, CyberScoop, Unit 42, Microsoft Security Blog, Schneier on Security, SANS ISC, Malware.News/DataBreaches.net, SOCRadar, Malwarebytes/FBI, and independent researchers.*