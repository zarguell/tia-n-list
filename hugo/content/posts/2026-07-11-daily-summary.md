---
title: "ShareFile Emergency Shutdown, The Gentlemen Ransomware, Ghostcommit AI Agent Attack, Zimbra TAG XSS"
date: 2026-07-11
tags: ["ShareFile","Progress Software","Gitea","Storm-2697","Ghostcommit","FlowiseAI","U-Boot","Zimbra","GitHub","Ryuk","ransomware","zero-day","AI security","bootloader"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Progress Software issues emergency shutdown order for ShareFile Storage Zone Controllers over credible threat; The Gentlemen ransomware emerges as 2026's fastest-growing RaaS with 580 victims; Ghostcommit demonstrates AI agent secret theft via image-embedded prompt injection; Zimbra patches critical XSS reported by Google TAG."
---

# Daily Threat Intelligence Digest — 2026-07-11

19 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.

---

## 🔴 Critical Threats & Active Exploitation

### [NEW] Progress ShareFile Storage Zone Controllers — "Credible External Security Threat" Forces Emergency Shutdown

Progress Software has emailed ShareFile customers using on-premises Storage Zone Controllers, instructing them to **immediately shut down the Windows servers** hosting the controllers. The email, titled "Service Disruption. Immediate Action Required," states: "We have reason to believe there is a credible external security threat targeting Progress Software's ShareFile Storage Zone Controllers." Progress has also disabled cloud-based access to affected accounts and warns that simply disabling access through the ShareFile platform is insufficient — customers must manually power down the servers.

Progress states there is currently "no indication of unauthorized access to any Progress ShareFile accounts or data" and is working with external cybersecurity experts to investigate. The company plans to provide another update within 24 hours. The incident draws immediate comparisons to the 2023 Clop ransomware exploitation of Progress MOVEit Transfer, which resulted in mass data theft from thousands of organizations. Storage Zone Controllers are typically internet-accessible, handle sensitive file transfers, and sit at the boundary between Progress cloud infrastructure and customer-managed storage — making them a high-value target for data exfiltration campaigns.

Progress has not disclosed whether the threat involves a zero-day vulnerability or confirmed compromise of any controllers. Organizations running ShareFile Storage Zone Controllers should treat this as a highest-priority incident and shut down affected servers immediately pending further guidance.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/progress-urges-sharefile-customers-to-shut-down-servers-over-credible-threat/)

---

### [UPDATE] CVE-2026-20896: Gitea Docker Auth Bypass — Singapore CSA Warns of Active Exploitation

*Previously covered July 8. New: Singapore's CSA has issued an active exploitation warning; Sysdig reports first in-the-wild hit 13 days after disclosure.*

Singapore's Cyber Security Agency (CSA) has warned that CVE-2026-20896 (CVSS 9.8) is being actively exploited in the wild, confirming the urgency first reported by Sysdig. The flaw in Gitea's official Docker image (≤1.26.2) ships with `REVERSE_PROXY_TRUSTED_PROXIES=*`, meaning any internet-facing Gitea Docker instance with reverse-proxy auth enabled can be impersonated with a single `X-WEBAUTH-USER` header — no password, no token, no MFA. Sysdig caught the first exploitation just 13 days after the advisory, via a VPN-exit scanner that immediately grabbed admin access.

Approximately 6,200 Gitea instances remain exposed to the internet per Shodan. CSA recommends restricting the trusted proxies setting to specific IPs and reviewing access logs. Gitea 1.26.4 is the current fixed release.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-exploit-critical-auth-bypass-in-gitea-docker-image/) | [SecurityWeek](https://www.securityweek.com/critical-gitea-flaw-under-active-exploitation-researchers-warn/) | [GitHub Advisory](https://github.com/go-gitea/gitea/security/advisories/GHSA-f75j-4cw6-rmx4)

---

## 🎯 Threat Actor Activity & Campaigns

### [NEW] The Gentlemen Ransomware (Storm-2697) — Fastest-Growing RaaS of 2026 With 580 Victims Across 77 Countries

Unit 42 has published a comprehensive analysis of **The Gentlemen** (tracked as Storm-2697), a Ransomware-as-a-Service program that has rapidly become the second most active ransomware operation of 2026. Formerly operating as "ArmCorp" — an affiliate of Qilin RaaS (Spikey Scorpius) — the group transitioned to its own RaaS model in September 2025 and has since claimed **580 victims across 77 countries**, with manufacturing as the most-targeted sector.

Key operational details:
- **Ransomware variants written in both C and Go**, enabling cross-platform encryption across operating systems and virtual infrastructure (ESXi hypervisors)
- **90% affiliate payout** — an unprecedented revenue share designed to aggressively recruit operators, compared to the standard 70-80%
- **Custom tooling**: Go-based backdoor, "GentleKiller" EDR killer framework, and suspected zero-day exploit for defense evasion
- **Victim count trajectory**: 117 claimed victims in June 2026 alone — nearly 4x January 2026; 6x growth comparing the last six months of 2025 to the first six months of 2026
- **BreachForums partnership** with HasanBroker announced in May 2026 for affiliate recruitment
- **Internal database leak** by an alleged insider in May 2026 revealed operational structure (~20 operators)

Known exploited CVEs for initial access include CVE-2024-55591 (FortiOS/FortiProxy), CVE-2025-32433 (Erlang/OTP SSH), CVE-2025-33073 (Windows SMB Client), CVE-2025-55182 (React2Shell), and CVE-2025-7771 (ThrottleStop.sys driver for privilege escalation). Unit 42 recommends SIEM alerts for scheduled tasks matching `gentlemen*`, enforcement of SMB signing, disabling SMBv1, and restricting ESXi management interfaces to dedicated VLANs.

**Source:** [Unit 42](https://unit42.paloaltonetworks.com/the-gentlemen-ransomware/)

---

### [NEW] GitHub API Reconnaissance Campaign — "Ghost Accounts" With 2-5 Year Dormancy Map Corporate Environments

SOCFortress, drawing on Datadog research, has documented a systematic GitHub API abuse campaign using **"ghost accounts"** — profiles created two to five years ago and left dormant before being weaponized in coordinated reconnaissance bursts since October 2025. The accounts exploit GitHub's publicly accessible API surface (unauthenticated routes returning HTTP 200) to map corporate organizations' engineering teams, project structures, and private repository layouts.

Key findings:
- Over 50 dormant profiles identified, following naming conventions like `amazon-data-*`, `*-orb` family, `BirdWithPlan`, `BirdWithDreams`
- Accounts emerge for 1-3 week high-intensity bursts using GraphQL bulk queries, then retreat
- "Vibe-coded" user agents mimic legitimate internal tools (e.g., `GitHubAnalytics/1.5`, `GitHubReporter/2.0`) to evade pattern-matching detection
- Campaigns escalated from reconnaissance to confirmed data exfiltration: a `repo-dumper` user agent successfully cloned private repositories after the mapping phase
- **"Identity Dark Matter"** — compromised OAuth tokens and PATs harvested from leaked environments enable high-velocity "smash and grab" attacks using dozens of legitimate accounts simultaneously, hosted on abuse-prone 3xK Tech infrastructure

Defense requires GitHub audit log streaming, baselining of user agents and source ASNs, and aggregate anomaly analysis — individual requests are successful HTTP 200 responses that trigger no alarms.

**Source:** [SOCFortress](https://socfortress.medium.com/github-api-abuse-via-ghost-accounts-and-token-compromise-6510c9a585b6)

---

### [NEW] China and India-Linked APT Groups Separately Target Same Pakistani Police Force

SentinelOne researchers have identified four separate hacking campaigns over more than two years targeting Pakistani law enforcement agencies, conducted by groups linked to both China and India. One campaign involved planting malware inside a public portal that citizens use to lodge complaints against police. The targeting of the same law enforcement entity by rival nation-state groups — Balochistan Police specifically — underscores the intelligence value of Pakistani internal security data for both Beijing and New Delhi.

**Sources:** [Reuters](https://www.reuters.com/world/china/china-india-linked-hacking-groups-targeted-pakistani-law-enforcement-report-says-2026-07-09/) | [SecurityWeek](https://www.securityweek.com/china-india-linked-hackers-both-targeted-same-pakistani-police-force/)

---

### [NEW] Ryuk Ransomware Operator Pleads Guilty — Faces 15 Years

Karen Serobovich Vardanyan, 34, an Armenian national extradited from Ukraine to the U.S., pleaded guilty to computer fraud and conspiracy for deploying Ryuk ransomware against multiple U.S. organizations between November 2019 and April 2020. Victims included a Michigan company that paid 200 BTC (~$1.1M), an Oregon technology company, and a Texas school. Vardanyan's co-conspirators received approximately 1,160 bitcoins (~$15M at the time) in ransom payments. He faces up to 15 years in prison and has agreed to pay $1.2M in restitution. Ryuk operated from 2018-2020, extorting an estimated $150M, with many members transitioning to Conti after Ryuk's shutdown.

**Sources:** [CyberScoop](https://cyberscoop.com/karen-vardanyan-armenian-ryuk-ransomware-guilty/) | [BleepingComputer](https://www.bleepingcomputer.com/news/security/ryuk-ransomware-member-pleads-guilty-in-the-us-faces-15-years-in-prison/)

---

## ⚠️ Vulnerabilities & Patches

### [NEW] 'Ghostcommit' — Prompt Injection Hidden in PNG Images Steals Repository Secrets Via AI Code Agents

Researchers from the University of Missouri-Kansas City have demonstrated **Ghostcommit**, a proof-of-concept attack that steals a repository's secrets by hiding malicious instructions inside a PNG image that AI code reviewers never open. The attack exploits a structural blind spot in AI-assisted development workflows:

1. An `AGENTS.md` file (read automatically by coding agents as project policy) points to `docs/images/build-spec.png`
2. The PNG contains plaintext instructions to read `.env` byte-by-byte and encode each byte as an integer constant
3. A text-based reviewer approves the PR without opening the image; CodeRabbit excludes image files from review by default
4. In a later session, a developer asks the coding agent for a routine feature — the agent reads `AGENTS.md`, follows the image pointer, reads `.env`, and emits the secrets as a Python integer tuple

In an end-to-end test, Cursor driving Claude Sonnet leaked the entire `.env` as 311 integers on the first try. Secret scanners never flag the output because none decode integer tuples back to ASCII. Critically, the vulnerability is **in the tooling, not the model** — Claude Code (same Sonnet weights, different harness) refused the instruction, while Cursor, Antigravity, and others complied across multiple models.

The researchers built a multimodal GitHub PR defender that caught 79/80 attacks with zero false positives on legitimate PRs, deployed on a single 4GB GPU.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/ghostcommit-hides-prompt-injection-in-images-to-fool-ai-agents-steal-secrets/)

---

### [NEW] CVE-2026-41264: FlowiseAI CSV Agent Prompt Injection RCE — Metasploit Module Published

Metasploit has added an exploit module for CVE-2026-41264, an unauthenticated RCE in FlowiseAI's CSV Agent feature. The vulnerability exists because the CSV_Agents class evaluates LLM-generated Python code without proper sandboxing and with an incomplete list of disallowed inputs. Attackers can upload a `.csv` file containing arbitrary Python code and achieve remote code execution as the user running the Flowise server. Affected versions span 1.3.0 through 3.0.13. The module requires an API key with `chatflows:create` permission but does not require Flowise authentication. Organizations deploying Flowise instances should upgrade immediately and restrict API key permissions.

Also added this week: a macOS PackageKit ZSH environment privilege escalation (CVE-2024-27822) and an Apache .htaccess persistence module.

**Source:** [Rapid7](https://www.rapid7.com/blog/post/pt-weekly-metasploit-update-exploits-for-flowiseai-csv-agent-and-macos-package-kit)

---

### [NEW] Six U-Boot Bootloader Vulnerabilities — Arbitrary Code Execution Before OS Load

Firmware security firm Binarly has disclosed six vulnerabilities in the U-Boot bootloader's FIT (Flattened Image Tree) signature verification code. Two flaws (BRLY-2026-037, BRLY-2026-038) can lead to arbitrary code execution during firmware verification, while four others cause denial of service via crashes. The vulnerable code has existed since U-Boot version 2013.07, potentially affecting 50+ stable releases and downstream vendor forks.

Because exploitation occurs before the operating system loads, attackers can disable firmware security features, install persistent firmware malware, and carry out actions undetectable by OS-level security tools. On systems like BMCs that support remote firmware updates, exploitation does not always require physical access — a compromised management interface is sufficient. Patches have been accepted into upstream U-Boot, but distribution to end devices depends on individual hardware vendors' firmware update cycles.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-u-boot-flaws-could-enable-stealthy-firmware-attacks/)

---

### [NEW] Zimbra Critical XSS in Classic Web Client — Reported by Google TAG

Zimbra has released version 10.1.19 to patch a critical stored cross-site scripting vulnerability in its Classic Web Client. The flaw, reported by Google's Threat Analysis Group (TAG), allows attackers to execute malicious code when a victim opens a specially crafted email. Successful exploitation can steal session data, account settings, or mailbox information. Zimbra has not yet assigned a CVE ID.

Google TAG's involvement is notable — the group frequently identifies zero-days deployed by state-sponsored hackers. Russian state-sponsored groups have a documented history of exploiting Zimbra vulnerabilities at scale: Winter Vivern in 2023, APT29 (Cozy Bear) in 2024, and APT28 in March 2025 (CISA ordered federal patching of CVE-2025-66376). Over 10,500 Zimbra instances remain exposed online per Shadowserver data from April 2026.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/zimbra-urges-customers-to-patch-critical-web-client-xss-flaw/)

---

## 🛡️ Defense & Detection

### [NEW] CISA Publishes Forensic Report on May Credential Leak — Advocates Secrets Scanning

CISA has released a forensic report detailing its response to the May 15 credential leak, where a contractor's exposure of privileged AWS GovCloud keys on a public GitHub repository was discovered by GitGuardian researcher Guillaume Valadon. CISA's response included immediately taking the repository offline, revoking the responsible party's access, analyzing the repository scope, and confirming through log analysis that no leaked credentials were used outside CISA and no customer/mission data was exposed.

Key takeaways from CISA's self-assessment:
- **What worked**: Taking the reported incident seriously, good logging capabilities, zero-trust architecture principles
- **What needed improvement**: Implementing EDR monitoring for public repository uploads, rotating all secrets post-incident, building incident playbooks mid-response (recognized need to build playbooks in advance)
- **New practices**: Secrets scanning for public repository uploads, streamlined vulnerability reporting channels for CISA-specific issues

Notably, this is the first time a national cybersecurity agency has publicly advocated for secrets scanning as a security practice.

**Source:** [CyberScoop](https://cyberscoop.com/cisa-credential-leak-forensic-report/)

---

## 📋 Policy & Industry

### [UPDATE] Angelo Martino Sentenced to 70 Months — Third Ransomware Negotiator Case Concluded

*Previously covered July 10 ( sentencing summary). New: SecurityWeek provides full sentencing details.*

Angelo Martino, 41, the former DigitalMint ransomware negotiator who secretly shared victim negotiating positions and insurance limits with BlackCat (ALPHV) affiliates, was sentenced Thursday to 70 months in prison. This concludes the third and final case of security professionals who aided ransomware gangs while employed to help victims. Kevin Martin and Ryan Goldberg were each sentenced to 4 years in April. The DOJ seized $10M in assets from Martino including cryptocurrency, vehicles, a food truck, and a fishing boat. Restitution amount to be determined at a September hearing.

**Sources:** [SecurityWeek](https://www.securityweek.com/third-us-security-expert-sentenced-to-prison-for-helping-ransomware-gang/) | [BleepingComputer](https://www.bleepingcomputer.com/news/security/us-ransomware-negotiator-gets-4-years-in-prison-for-blackcat-attacks/)

---

## ⚡ Quick Hits

- **Dutch police link Odido breach to Dutch hackers** — The February breach affecting 6.2 million customers of Dutch telecom Odido involved a Dutch-speaking man posing as an IT employee in a phishing call to customer service. ShinyHunters claimed responsibility, releasing 88GB of data with 15M+ records. The group has been linked to breaches at Google, Cisco, the European Commission, and 100+ organizations via an Oracle PeopleSoft zero-day. [BleepingComputer](https://www.bleepingcomputer.com/news/security/police-suspects-dutch-hackers-were-involved-in-odido-breach/)

- **Microsoft SFI July 2026 progress report** — Phishing-resistant MFA now protects 99.97% of Microsoft user/device pairs. 732K+ resources had public access revoked. Microsoft's multi-agent AI system confirmed 90%+ of composite vulnerability findings. Post-quantum cryptography transition accelerated, targeting critical products by 2029. [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/10/securing-our-future-july-2026-progress-report-on-microsofts-secure-future-initiative/)

- **Prison money laundering scheme** — Bulgarian national Rossen Iossifov, already serving 121 months for laundering $5M for an online auction fraud ring, was charged with stealing $290K in government-seized cryptocurrency while incarcerated by routing funds through exchanges and mixing services. [BleepingComputer](https://www.bleepingcomputer.com/news/security/money-launderer-accused-of-stealing-seized-crypto-while-in-prison/)
