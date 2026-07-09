---
title: "Defender Zero-Day Patched, Fake SDKs Steal Credentials, GhostLock Linux Root Escalation, Pink Passkey Vishing, KDDI 12M Breach"
date: 2026-07-09
tags: ["CVE-2026-50656","RoguePlanet","GhostLock","CVE-2026-43499","Pink","O-UNC-066","npm","PyPI","supply-chain","FortiBleed","Dialogflow","KDDI","CISA-KEV"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Microsoft patches the RoguePlanet Defender zero-day disclosed by a researcher in a public dispute. A new 15-year-old Linux kernel flaw (GhostLock) enables container escape. The Pink extortion gang runs passkey enrollment vishing against Microsoft 365 users. 17 fake payment SDKs on npm and PyPI steal credentials. KDDI discloses a 12-million-person breach via a zero-day in third-party email platform software."
---

# Daily Threat Intelligence Digest — July 9, 2026

*25 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] CVE-2026-50656 "RoguePlanet": Microsoft Patches Defender Zero-Day After Researcher Public Dispute**

Microsoft has released Malware Protection Engine 1.1.26060.3008 to patch CVE-2026-50656, a race condition vulnerability in Windows Defender that allows attackers to spawn a SYSTEM-privilege command prompt on fully patched Windows 10 and 11 devices. The flaw was disclosed by researcher "Nightmare Eclipse" after the June 2026 Patch Tuesday, as part of an escalating dispute with Microsoft over bug bounty practices and vulnerability disclosure policies.

Nightmare Eclipse has now disclosed a series of Defender zero-days — BlueHammer, RedSun, GreenPlasma, MiniPlasma, YellowKey, UnDefend, and now RoguePlanet — each accompanied by proof-of-concept exploits. Microsoft confirmed it was working on a patch on June 16 but has not acknowledged Nightmare Eclipse as the discoverer. Microsoft has also issued legal warnings against "malicious activity causing real harm to our customers," which the security community interpreted as threats directed at the researcher. The PoC exploit reportedly works regardless of real-time protection status, with variable success rates depending on the target machine. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-patches-rogueplanet-defender-zero-day-vulnerability/); [SecurityWeek](https://www.securityweek.com/microsoft-patches-defender-rogueplanet-vulnerability/)]

**Recommended action:** Verify Malware Protection Engine version is ≥1.1.26060.3008 across all Windows endpoints. Defender updates automatically, but verify via About Microsoft Defender Antivirus in the Windows Security app.

---

**[NEW] CVE-2026-43499 "GhostLock": 15-Year-Old Linux Kernel Flaw Enables Root and Container Escape**

*Gap detection: surfaced via community cross-reference — not ingested by Miniflux Cyber feeds.*

Researchers at Nebula Security have disclosed GhostLock (CVE-2026-43499, CVSS 7.8), a use-after-free vulnerability in the Linux kernel's futex priority-inheritance code that has lurked in the kernel since 2011 — 15 years. The flaw resides in the cleanup step of the rt_mutex/futex machinery: when a lock operation hits a dead end and backs out, the cleanup runs at the wrong moment and wipes the wrong task's record, leaving the kernel holding a dangling pointer to freed memory. Nebula chained this into full root privilege escalation.

The vulnerability affects every mainstream Linux distribution and enables both local root escalation and container escape — making it particularly dangerous in multi-tenant cloud environments. GhostLock was discovered using Nebula's AI-assisted Vega vulnerability scanner and earned a $92,337 bounty through Google's kernelCTF program. A separate, related KVM flaw (Januscape, CVE-2026-53359) also surfaced this week with a $250,000 bounty — covered in the July 7 digest. [[Ars Technica](https://arstechnica.com/security/2026/07/high-severity-guest-vm-escape-is-1-of-2-linux-vulnerabilities-to-surface-this-week/); [The Hacker News](https://thehackernews.com/2026/07/15-year-old-ghostlock-flaw-enables-root.html)]

**Hunting hypothesis:** An unprivileged local user or compromised container process exploits a race condition in the futex priority-inheritance cleanup path to gain a dangling kernel pointer, escalates via ROP chain to root, and escapes the container boundary.

**Recommended action:** Apply latest kernel updates from your distribution immediately. Container host kernels are the highest-priority patch targets.

---

**[UPDATE] CISA Adds Three More Vulnerabilities to KEV — JoomShaper, Langflow Authorization Bypass**

*Previously covered: Langflow (CVE-2026-48282, July 6/8 digest). New: CISA added three additional vulnerabilities to KEV on July 7, including a new Langflow authorization bypass distinct from the earlier ColdFusion/Langflow entries.*

CISA added CVE-2026-48908 (JoomShaper SP Page Builder unrestricted file upload, CVSS 10.0), CVE-2026-55255 (Langflow authorization bypass through user-controlled key), and a third vulnerability to its Known Exploited Vulnerabilities catalog on July 7, all based on evidence of active exploitation. These additions follow the earlier July 8 batch that included the Adobe ColdFusion flaw. The JoomShaper SP Page Builder vulnerability affects all versions below 6.6.2 of the Joomla extension and enables unauthenticated remote code execution via dangerous file upload. [[CISA](https://www.cisa.gov/news-events/alerts/2026/07/07/cisa-adds-three-known-exploited-vulnerabilities-catalog); [The Hacker News](https://thehackernews.com/2026/07/cisa-adds-4-actively-exploited-adobe.html)]

**Recommended action:** Update SP Page Builder to ≥6.6.2 immediately if installed on any Joomla instance. Apply Langflow patches. Audit CMS extension versions across web-facing servers.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] "Pink" Extortion Gang Runs Entra Passkey Enrollment Vishing Campaign**

Okta is tracking a voice phishing campaign in which threat actor O-UNC-066 — operating the extortion brand "Pink" affiliated with the decentralized "The Com" network — targets Microsoft 365 users across food and beverage, technology, healthcare, automotive, construction, and aviation sectors. The campaign, running since April, exploits a legitimate Microsoft administrative capability: passkey registration campaigns opened to admins in May 2026.

The attacker calls targeted employees posing as IT security, directing them to phishing sites mimicking the Entra passkey enrollment portal. Unlike standard adversary-in-the-middle proxies, the phishing kit is an operator-controlled PHP panel with a 1-second heartbeat polling mechanism that lets the attacker steer victims through real-time authentication flows, adapting to TOTP, push notification with number matching, or SMS OTP. While victims believe they are registering a new passkey, the attacker registers a passkey they control — then exfiltrates data from SharePoint and OneDrive. The fake enrollment process includes presenting victims with a BIP-39 recovery phrase (not used in legitimate Microsoft passkey enrollment) as a distraction.

Palo Alto Networks Unit 42 confirmed Pink launched its extortion site on May 31, publishing stolen data samples to pressure victims into paying ransoms. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/entra-passkey-enrollment-vishing-targets-microsoft-365-users/); [Okta](https://www.okta.com/blog/)]

**Hunting hypothesis:** A threat actor calls employees posing as IT helpdesk, steers them through a real-time operator-controlled phishing panel to register an attacker-controlled passkey on their Microsoft 365 account, then exfiltrates data from SharePoint and OneDrive before the victim realizes the passkey is not theirs.

**Recommended action:** Notify employees that legitimate IT will never call to request passkey enrollment. Monitor Microsoft 365 audit logs for new passkey registrations. Block domains containing "passkey" in phishing detection rules. Establish callback verification for helpdesk contacts.

---

**[UPDATE] UAT-7810/LapDogs Campaign Expands Leash-Family Malware Toolkit**

*Previously covered July 8. New: SecurityWeek coverage provides additional detail on the Leash malware family evolution and SOHO router compromise scale.*

Cisco Talos's continued analysis of the China-linked APT cluster UAT-7810 (LapDogs campaign) documents the evolution from SHORTLEASH to an expanded toolkit: LONGLEASH (upgraded reverse shell with HTTP/DNS/SOCKS/TCP/ICMP/UDP proxying and TLS/PKI), DOGLEASH (lightweight Linux backdoor via web shells), and JARLEASH (Java-based FTP/SFTP/Netcat tool). The campaign has compromised over 1,000 SOHO routers to build an Operational Relay Box (ORB) network used as proxy infrastructure by other China-aligned APTs. The group exploits known n-day vulnerabilities in Ruckus and ASUS routers. [[SecurityWeek](https://www.securityweek.com/china-linked-apt-expands-arsenal-with-new-leash-backdoors/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/chinese-hackers-develop-longleash-malware-to-expand-orb-network/)]

**Recommended action:** Patch all internet-facing Ruckus and ASUS routers against CVE-2020-22653, CVE-2020-22658, CVE-2023-25717, and CVE-2025-2492. Monitor for anomalous proxy connections from edge network devices.

---

**[NEW] CMD Organization Claims Mount Royal University Ransomware Attack — Student Data Stolen and Wiped**

Mount Royal University in Calgary has confirmed that attackers breached its network on June 17, stole data from the university's shared "H drive" file storage (affecting current and former students, employees, and other individuals), and wiped a separate "J drive" containing departmental data to disrupt recovery. The university has engaged external cybersecurity experts and reported the incident to the Alberta Information and Privacy Commissioner.

The extortion group CMD Organization claimed responsibility, published samples of stolen data including passport scans, and demanded 30 BTC (~$1.9 million) with a six-day deadline. CMD operates an auction-style model across clear web and dark web portals, currently listing 30 organizations. Full recovery of the J drive data may not be possible. MRU is offering two years of credit monitoring to current and recent employees. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/mount-royal-university-confirms-breach-as-hackers-claim-attack/)]

**Recommended action:** Educational institutions: review file share access controls and segmentation. Monitor for CMD Organization extortion site activity.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] 17 Fake Paysafe/Skrill/Neteller SDKs on npm and PyPI Steal Developer Credentials**

Application security firm Socket has identified at least 17 malicious packages published simultaneously across npm (13 packages) and PyPI (4 packages) that impersonate legitimate payment SDKs for Paysafe, Skrill, and Neteller. The packages expose the expected APIs and return fake success responses while searching compromised environments for secrets — Paysafe API keys, AWS keys, GitHub tokens, npm tokens, hostnames, and API usage metadata.

The npm packages activate data exfiltration only when a Paysafe API key is present, while the PyPI packages auto-exfiltrate on initialization regardless. The malware includes basic anti-analysis features (CPU core checks, virtualized environment detection) and exfiltrates to an AWS-hosted C2 server. The threat actor's ability to operate across both ecosystems makes defense more difficult for organizations with visibility into only one package registry. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-paysafe-skrill-sdks-on-npm-and-pypi-steal-credentials/)]

**Hunting hypothesis:** A developer installs a fake Paysafe SDK from npm or PyPI, triggering automatic credential exfiltration of AWS keys, GitHub tokens, and API keys to an AWS C2 server, with anti-analysis evasion preventing sandbox detection.

**Recommended action:** Search dependency trees for all 17 listed package names. Deny at the registry proxy level. Rotate all secrets on any machine that imported these packages. Check CI logs for PAYSAFE_API_KEY alongside listed package names.

---

**[NEW] Google Dialogflow CX Authorization Bypass Enables AI Conversation Hijacking**

A vulnerability in Google's Dialogflow CX platform allowed attackers to hijack AI-powered conversations by exploiting an authorization bypass. The flaw could enable attackers to manipulate customer-facing AI agents across organizations using Dialogflow CX for chatbots and virtual assistants. Google has patched the vulnerability. Details are limited as the article is behind a paywall. [[SecurityWeek](https://www.securityweek.com/google-dialogflow-cx-bug-allowed-attackers-to-hijack-ai-conversations/)]

**Recommended action:** Verify Dialogflow CX configurations and review recent access logs for unauthorized conversation sessions.

---

**[NEW] Chrome 150 Patches 27 Vulnerabilities**

Google has released Chrome 150, patching 27 security vulnerabilities. The browser update is rolling out across all platforms. Specific vulnerability details and severity ratings will be published to the Chrome release blog as per Google's disclosure policy. [[SecurityWeek](https://www.securityweek.com/chrome-150-update-patches-27-vulnerabilities/)]

**Recommended action:** Ensure Chrome 150 is deployed across all endpoints. Chrome auto-updates for most users, but enterprise-managed installations should verify via update policies.

---

## 🛡️ Defense & Detection

**[NEW] FortiBleed: Qualys Publishes Comprehensive FortiGate Credential Exposure Analysis**

Qualys has published a detailed technical analysis of the "FortiBleed" campaign — large-scale credential exposure and abuse targeting internet-reachable FortiGate management and SSL-VPN gateways. The analysis maps eight relevant Fortinet CVEs (including CVE-2026-24858, CVE-2025-59718, and CVE-2025-59719) to Qualys QIDs and provides QQL queries for VMDR, ETM, and CSAM to identify and prioritize exposed assets.

Key finding: a patched device can remain compromised if credentials or configuration material were stolen before remediation, particularly where PBKDF2 migration and legacy-hash cleanup are incomplete. The post provides detection and threat-hunting guidance across four areas: authentication anomalies, configuration and account changes, downstream identity activity, and exposure and integrity validation. [[Qualys Security Blog](https://blog.qualys.com/vulnerabilities-threat-research/2026/07/08/fortibleed-fortigate-credential-reuse-internet-exposed)]

**Recommended action:** Treat Qualys QID matches as investigation seeds, not confirmed compromise. Revoke sessions, rotate credentials, enforce MFA, and validate PBKDF2 migration and configuration integrity on all FortiGate devices — even those already patched.

---

## 📋 Policy & Industry News

**[NEW] Illinois SB 315 "AI Safety Measures Act" Signed Into Law — Targets Large Frontier AI Developers**

Illinois has enacted SB 315, the "Artificial Intelligence Safety Measures Act," effective July 6, 2026. The law applies to "large frontier developers" — companies with revenue exceeding $500 million — requiring them to establish a "Frontier AI Framework" with internal safety assessments, reporting channels, and whistleblower protections. The law targets the major AI hyperscalers and represents one of the first US state-level regulations specifically governing frontier AI development practices. [[Deploying Securely](https://blog.stackaware.com/p/illinois-sb-315-iso-42001-internal-audit-ai-hyperscaler)]

---

**[NEW] INTeL Launches — French Nonprofit Creates Global AI Cyber Threat Intelligence Hub**

The Paris Peace Forum has launched the Integrated Network for Trusted AI in Cyberspace (INTeL), bringing together government, private sector, and civil society experts to assess AI-related threats to global internet infrastructure. The hub will produce forward-looking reports on how AI technology will shape cyber threats and aims to establish international standards for AI safety in cybersecurity contexts. [[CyberScoop](https://cyberscoop.com/paris-peace-forum-intaic-ai-cyber-threats/)]

---

## ⚡ Quick Hits

- **[NEW] KDDI breach impacts 12.2 million email users** — Japanese telecom giant KDDI disclosed that attackers breached a third-party email platform via a zero-day vulnerability (exploited May 16, undisclosed to the vendor at time of discovery) affecting five ISPs. 12.23 million email addresses and 7.6 million passwords exposed. KDDI deployed EDR tools and is forcing mandatory password resets. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/japanese-telecom-giant-kddi-says-data-breach-affects-12-million-people/)]

- **[NEW] AssuranceAmerica breach exposes 6.9 million driver records** — US insurance company disclosed a breach detected March 17, involving an employee-targeted attack. Stolen data includes names, contact info, policy details, vehicle information, claims data, and driver's license numbers across 14 states. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/assuranceamerica-data-breach-exposes-records-of-69-million-drivers/)]

- **[NEW] Accenture confirms source code breach — no new developments** — SecurityWeek confirmed Accenture stated it "remediated the source" of the breach with no operational impact. No further details on the attack vector or scope beyond the initial disclosure. Covered in the July 8 digest. [[SecurityWeek](https://www.securityweek.com/accenture-confirms-data-breach-after-hacker-claims-source-code-theft/)]

- **[NEW] AI coding tools vulnerable to "GhostApproval" technique** — SecurityWeek reports that AI coding assistants can be tricked into hacking developer machines using a decades-old technique dubbed "GhostApproval," which exploits the tools' tendency to auto-approve actions. Details are paywalled. [[SecurityWeek](https://www.securityweek.com/ai-coding-tools-tricked-into-hacking-developer-machine-via-decades-old-technique/)]
