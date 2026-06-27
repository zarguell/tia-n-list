---
title: "🚨Cisco UC PoC, 🐧Linux Container KEV, 🎯TA4922 Atlas RAT, 💻Lazarus npm, 📊Stock Exchange Espionage, 🤖AI Skill Scanner Bypass"
date: 2026-06-04
tags: ["Cisco","CVE-2026-20230","CVE-2022-0492","TA4922","Atlas RAT","Lazarus Group","npm","container escape","espionage","AI supply chain","Everest Forms","WordPress","GitGuardian","Secure Boot","GoGatoZ","LLMjacking","Open Source Security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Cisco Unified CM critical SSRF with public PoC exploit code — patch now; CISA adds 3-year-old Linux kernel container escape (CVE-2022-0492) to KEV with active exploitation confirmed; TA4922 Chinese hacker group deploys Atlas RAT across Europe with more campaigns than any other tracked actor; Lazarus Group runs npm brandjacking campaign with persistent Node.js backdoors; Stock exchange executive's mailbox stolen for 5 months in tightly focused espionage operation; Trail of Bits demonstrates all major AI skill scanners can be trivially bypassed — structural supply chain risk for agentic AI."
---
# Daily Threat Intelligence Digest — June 4, 2026

*89 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Cisco Unified CM CVE-2026-20230 — Critical SSRF with Public PoC, WebDialer Required, Patches Available**

Cisco disclosed a critical server-side request forgery vulnerability in Unified Communications Manager (Unified CM) and Unified CM Session Management Edition, warning that proof-of-concept exploit code is publicly available. Tracked as CVE-2026-20230 (CVSS 8.6, Cisco rates it Critical), the flaw stems from improper HTTP input validation in the WebDialer service — disabled by default but commonly enabled in enterprise deployments for click-to-call CTI functionality.

An unauthenticated remote attacker sends a crafted HTTP request to write arbitrary files to the underlying OS, then escalates those file-write primitives to root access. [[SecurityWeek](https://www.securityweek.com/cisco-warns-of-available-poc-for-critical-unified-cm-vulnerability/); [Cisco Advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-cucm-ssrf-cXPnHcW); [HEAL Security](https://healsecurity.com/cisco-unified-communications-manager-vulnerability-exposed-along-with-poc-exploit-code/)]

**Fixed releases:** Unified CM 14SU6 is available now. Release 15 users must wait for 15SU5 (September 2026) or apply the interim COP patch. No active exploitation confirmed at disclosure, but public PoC dramatically accelerates the window. **Action:** Disable WebDialer immediately if non-essential; apply 14SU6 or COP patches as priority.

---

**[NEW] CISA Adds CVE-2022-0492 to KEV — Linux Kernel cgroup-v1 Container Escape Actively Exploited**

CISA added CVE-2022-0492 (CVSS 7.8) to its Known Exploited Vulnerabilities catalog, warning of in-the-wild exploitation of a Linux kernel vulnerability that enables container escapes via the cgroups v1 `release_agent` feature. First disclosed in 2022, technical details have been public for three years — but active exploitation was only confirmed this week, one day before CISA's alert. [[SecurityWeek](https://www.securityweek.com/organizations-warned-of-exploited-linux-kernel-vulnerability/); [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)]

**How it works:** Any user can modify the `release_agent` file at the root of the cgroup hierarchy, which runs as root when a cgroup becomes empty. An attacker in a container creates a malicious script on the host filesystem and triggers execution through the cgroup notification process — escaping the container and escalating to root on the host. Kaspersky documented the attacks targeting container environments but has not attributed specific threat actors or victims. Federal agencies must remediate by **June 5**. Cgroups v2 is not affected. Cloud-native environments running Kubernetes or Docker on older kernels should prioritize patching immediately.

---

**[NEW] Everest Forms Pro CVE-2026-3300 (CVSS 9.8) — Unauthenticated RCE Actively Exploited, 29,300+ Attacks Blocked**

Wordfence disclosed active exploitation of a critical unauthenticated remote code execution vulnerability in Everest Forms Pro, a WordPress form builder plugin with ~4,000 active installations. Tracked as **CVE-2026-3300**, the flaw allows unauthenticated attackers to inject and execute arbitrary PHP code by submitting crafted values in string-type form fields when a form uses the "Complex Calculation" feature. The `sanitize_text_field()` function does not escape single quotes — an attacker submits a single quote to break out of the string literal, followed by malicious PHP code that `eval()` executes server-side. [[Wordfence](https://www.wordfence.com/blog/2026/06/attackers-actively-exploiting-critical-vulnerability-in-everest-forms-pro-plugin/); [Malware.News](https://malware.news/t/attackers-actively-exploiting-critical-vulnerability-in-everest-forms-pro-plugin/107564#post_1)]

**Attack data:** Wordfence blocked **29,300+ exploit attempts** since disclosure. The most common payload creates an admin account with username `diksimarina` and email `diksimarina@sibertm[.]com`. Mass exploitation peaked May 16 (17,900+ attempts in a single day). The top attacking IP (202.56.2.126) accounts for 26,300+ blocked requests. Patched in version **1.9.13** (released March 18). Exploitation began April 13. **Action:** Update immediately and audit for rogue admin accounts.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] TA4922 (Chinese-Speaking) Deploys Atlas RAT in Europe — More Campaigns Than Any Other Tracked Threat Actor**

Proofpoint documented a sharp escalation from TA4922, a Chinese-speaking financially motivated cybercrime group that has rapidly expanded operations into Europe, hitting Germany, Italy, the UK, and South Africa. The group now conducts **more unique campaigns than any other tracked cybercrime threat actor** in Proofpoint's telemetry, using localized phishing lures crafted for payroll notices, tax audits, VAT filings, and government compliance in each target country. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/chinese-hackers-use-new-atlas-rat-malware-in-european-cyberattacks/)]

**Malware arsenal expansion:**

- **Atlas RAT** — New remote access trojan with system recon, targeted file theft, keylogging, screenshot capture, audio/webcam recording, and plugin download. Includes anti-sandbox checks.
- **RomulusLoader** — Process hollowing + shellcode injection loader deploying AnyDesk and SyncFuture (Chinese RMM tool, specifically used against German targets).
- **SilentRunLoader** — Python-based info stealer targeting Chrome credentials, deployed against UK and Southeast Asian targets.
- **Winos4.0 (ValleyRAT)** — Full remote access framework.

Proofpoint assesses the group uses LLMs to accelerate malware development based on AI-generated code artifacts (placeholder values, structured comments). Since March, activity has increased sharply with "unprecedented operational diversity." While financially motivated, the malware capabilities also support surveillance that could be sold to espionage groups.

---

**[NEW] Lazarus Group npm Brandjacking Campaign — Dozens of Malicious Packages, Buffer Impersonation with Persistent Node.js Backdoor**

Sonatype Security Research is tracking a Lazarus Group campaign on npm that goes beyond traditional typosquatting. Using brandjacking techniques (suffix addition, version mimicry, embedding), attackers published dozens of packages impersonating Buffer, Chai, Express, and React — some reaching **500 weekly downloads**. [[Malware.News/Sonatype](https://malware.news/t/lazarus-groups-latest-brandjacking-campaign-on-npm/107571#post_1)]

**Technical breakdown (buffer-utilities case):** The malicious package contains legitimate Buffer library code plus a dropper that fetches remote payloads from `www.jsonkeeper.com` via Base64-encoded URLs. The secondary payload is a persistent Node.js backdoor that collects host info, beacons to C2 at `45.59.163.198:1244`, creates a hidden `.vscode` directory, downloads third-stage payload (`f.js`), and includes an **update mechanism** for periodic C2 reconnect and payload replacement.

**Action:** Organizations that installed any packages matching `sonatype-2026-003558` should remove them, treat hosts as compromised, investigate for second-stage payload execution, and rotate credentials exposed from developer machines.

---

**[NEW] Global Stock Exchange Hit by 5-Month Espionage Campaign — Symantec/Carbon Black Detail Incremental Mailbox Theft**

Symantec's threat-hunting team (Broadcom) documented a tightly focused espionage operation targeting a senior executive at a major global stock exchange. The attacker accessed the victim's Outlook mailbox from **October 2025 to March 2026** (150-day dwell time), exfiltrating the complete mailbox in incremental archives using Dropbox and OneDrive. [[SecurityWeek](https://www.securityweek.com/hackers-target-global-stock-exchange-in-espionage-operation/); [Dark Reading](https://www.darkreading.com/cyberattacks-data-breaches/global-stock-exchange-hit-monthslong-email-campaign); [Security.com](https://www.security.com/blog-post/stock-exchange-espionage)]

**Key tradecraft:** The attacker used a custom infostealer built on Aspose (a legitimate .NET library for parsing Outlook OST/PST files), wrapped in a standalone executable renamed with innocuous temp-file extensions and hidden in Windows temp subfolders (`...\temp\skin\licenses\`). Eight OST-extraction runs occurred at 2–4 week intervals, each adjoining the previous date window. Persistence was maintained through scheduled tasks disguised as Adobe, Lenovo, and OneDrive system services. No attribution has been made.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Trail of Bits: ClawHub, Cisco, and Vercel AI Skill Scanners Can Be Trivially Bypassed — Structural Supply Chain Risk for Agentic AI**

Trail of Bits researchers demonstrated that all three major AI skill security scanners — ClawHub (OpenClaw), Cisco's skill-scanner, and Vercel's skills.sh — can be reliably bypassed using simple techniques, raising fundamental concerns about agentic AI supply chain defenses. [[GBHackers](https://gbhackers.com/clawhub-cisco-and-vercel-skill-detection-tools-evaded-by-malicious-uploads/)]

**Bypass techniques demonstrated:**
- **ClawHub:** Prepend ~100,000 newline characters — OpenClaw truncates oversized content for its guard-model prompt, hiding malicious logic beyond the inspected region. VirusTotal/Gemini 3 Flash also failed.
- **Vercel skills.sh:** Malicious logic hidden in `.docx` ZIP archives and poisoned `.pyc` bytecode — all three integrated scanners reported the skill as safe.
- **Cisco skill-scanner:** Even backed by Claude Sonnet 4.6, the scanner marked prompt-injection-style skills as low risk.

**Recommendation:** Organizations should not outsource trust decisions to automated scanners. Use curated internal skill registries, version pinning, and treat public skills as untrusted code by default.

---

**[NEW] Four Credential-Harvesting Campaigns Hit Open Source Ecosystems in Two Weeks — GitGuardian Breaks Down the Surge**

GitGuardian documented four distinct credential-harvesting campaigns across npm, PyPI, Crates.io, Composer, and GitHub Actions in a two-week window. [[GitGuardian](https://blog.gitguardian.com/four-credential-harvesting-campaigns-hit-open-source-ecosystems-in-two-weeks/)]

1. **Megalodon (May 18):** 5,718 automated malicious commits pushed to **5,561 GitHub repositories** in six hours. Each injected a GitHub Actions workflow with base64-encoded bash payload exfiltrating CI secrets, cloud credentials, SSH keys, OIDC tokens.
2. **Laravel-Lang (May 22–23):** Attackers rewrote Git tags across 700+ historical versions of four Composer packages.
3. **TrapDoor (May 22 onward, cross-ecosystem):** 34+ packages across npm, PyPI, Crates.io. npm payloads plant persistence in `.cursorrules` and `CLAUDE.md` files to hijack AI coding assistants.
4. **Miasma / Mini Shai-Hulud (June 1, Red Hat):** 96 compromised versions of 32 `@redhat-cloud-services` npm packages via OIDC trusted publishing abuse. First confirmed major case of the open-sourced Mini Shai-Hulud worm producing enterprise-scale attacks.

---

**[NEW] Microsoft Secure Boot Certificates Expire June 27 — Migration Required to Prevent Permanent DBX Freeze**

Three Microsoft UEFI certificates from 2011 expire starting June 27, 2026. Organizations that do not migrate to the 2023 certificate family will silently lose the ability to update Secure Boot revocation lists — permanently freezing their systems' trust state and leaving them exposed to future bootkit attacks. [[GBHackers/Eclypsium](https://gbhackers.com/expiring-microsoft-secure-boot-keys-may-block-dbx-updates-on-legacy-devices/)]

**Timeline:** June 27 — KEK CA 2011 and UEFI CA 2011 expire; October 2026 — Windows Production PCA 2011 expires. Systems left on the 2011 chain will continue to boot but will never learn to distrust bootkits (BootHole, BlackLotus, Bombshell) discovered after the KEK expires.

---

## 🛡️ Defense & Detection

**[NEW] GoGatoZ: Open-Source GitLab CI/CD Security Scanner Released — BHIS Scans 3,757 Projects, Finds 1,580 HIGH Severity Issues**

Black Hills Information Security released GoGatoZ, an open-source Go tool for GitLab CI/CD security auditing. The researchers scanned 3,757 public GitLab projects and found **7,331 total findings, including 1,580 HIGH severity issues**. [[BHIS](https://www.blackhillsinfosec.com/auditing-gitlab-the-ci-cd-kill-chain/); [Malware.News](https://malware.news/t/auditing-gitlab-the-ci-cd-kill-chain/107546#post_1)]

**Key findings:** 66% of public projects with CI/CD pipelines had security findings. Top vulnerabilities: Fork MR attacks (1,971 findings), privileged runners (259), variable injection (288), and `curl | bash` in production pipelines (150).

---

**[NEW] Five Routes Attackers Use to Reach LLM Inference — Intezer Scans 4,500 Hosts, Finds Widespread LLMjacking**

Intezer published a comprehensive analysis of five routes threat actors use to reach LLM inference: offensive LLMs on underground forums, crypto-payment middlemen, free-tier public APIs, stolen API keys, and exposed self-hosted LLM servers. [[Intezer via Malware.News](https://malware.news/t/how-attackers-are-gaining-access-to-llm-inference/107561#post_1)]

**Scan highlights:** Scanned ~4,500 hosts across 11 platforms. 55% of LocalAI hosts confirmed open; 24% acted as API proxies with live upstream keys. Evidence of automated exploitation at scale (21% of LocalAI hosts compromised). Five malware families now wire live LLM APIs into runtime for dynamic payload generation.

---

## 📋 Policy & Industry News

**[NEW] IMA Diligence Services Data Breach — 525,306 Individuals Impacted, 700 GB Exfiltrated by Genesis Ransomware**

IMA Diligence Services is notifying **525,306 individuals** whose personal information was stolen in a December 2025 breach attributed to the Genesis ransomware group. The attackers exfiltrated **700 GB of data** from a legacy third-party managed server. [[SecurityWeek](https://www.securityweek.com/ima-diligence-services-data-breach-impacts-525000-people/)]

**[NEW] European Authorities Dismantle 9 Organized Crime Streaming Networks — Operation Kratos 2**

Europol-led "Operation Kratos 2" resulted in **29 arrests** and dismantled **nine organized crime groups** supporting illegal streaming. Authorities took down 27,000+ URLs across 169 domains infringing on 850,000 media titles. [[CyberScoop](https://cyberscoop.com/europol-piracy-streaming-crackdown-operation-kratos2/)]

**[NEW] ASEC Ransom & Dark Web Weekly — Qilin Hits South Korea, Black X Emerges, Nova Targets University**

AhnLab's weekly report highlights Qilin ransomware targeting a South Korean automation equipment company, new data extortion group "Black X," and Nova ransomware striking a university AI department. [[ASEC](https://asec.ahnlab.com/en/93989/)]

---

## ⚡ Quick Hits

- **KR: Tving CEO Apologizes for Data Leak** — South Korean OTT platform Tving suffered a personal information breach. [[DataBreaches.net](https://databreaches.net/2026/06/03/kr-tving-ceo-apologizes-for-unprecedented-data-leak/)]
- **Fake Document Factory Dismantled in Spain** — Spanish authorities seized ~800 forged IDs. [[Malware.News](https://malware.news/t/fake-document-factory-dismantled-in-spain-around-800-ids-seized/107578#post_1)]
- **Microsoft Coreutils for Windows Released** — Native GNU Coreutils implementations for Windows. [[Malware.News](https://malware.news/t/microsofts-coreutils-for-windows-thu-jun-4th/107577#post_1)]
- **Five Eyes Warns of Chinese Espionage via LinkedIn** — Joint bulletin on aggressive online recruitment targeting defense personnel. [[Reuters](https://au.marketscreener.com/news/five-eyes-security-alliance-warns-of-chinese-espionage-threat-ce7f5ddfd08ff026)]
- **NoName057(16) DDoS Evolution** — Bitsight analysis shows pro-Russian hacktivist group remains active despite Operation Eastwood. [[Bitsight](https://malware.news/t/crowdsourced-chaos-the-evolution-of-noname057-16-and-why-ddos-resilience-matters/107556#post_1)]
