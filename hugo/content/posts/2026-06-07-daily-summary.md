---
title: "🤖 Anthropic Engineers at NSA, 🐧 Copy Fail Linux LPE, 🧠 First AI-Developed Zero-Day, 🔓 Mythos Model, 🛡️ Google GTIG Q2 Report"
date: 2026-06-07
tags: ["Anthropic","Mythos","NSA","Copy Fail","CVE-2026-31431","Linux","LPE","GTIG","AI Threats","PROMPTSPY","Everest Forms","CVE-2026-3300","WordPress","CISA KEV","Project Glasswing","Supply Chain","AI Security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Anthropic embeds engineers at NSA for Mythos offensive cyber ops while battling DoD supply-chain ban. CISA KEV adds 'Copy Fail' Linux kernel LPE granting root in seconds via 732-byte Python script. Google GTIG identifies first AI-developed zero-day and documents PRC/DPRK AI-augmented vuln research pipelines. Everest Forms Pro exploitation continues with new attacker IP."
---
# Daily Threat Intelligence Digest — June 7, 2026

*4 articles ingested from Miniflux Cyber feeds. External cross-referencing via Reddit skipped — old.reddit.com returned errors on both `/hot/` and `/new/` endpoints. tl;dr sec #331 (published June 4, 3 days fresh) checked — identified two material gaps: CVE-2026-31431 "Copy Fail" (CISA KEV, zero Miniflux coverage) and Google GTIG Q2 2026 AI threat report. Prior digests: June 1–6, 2026. Stale CVE/topic blocklist applied.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Anthropic Engineers Embedded at NSA — Mythos Model Deployed for Offensive Cyber Operations, DoD "Supply Chain Risk" Paradox**

Anthropic has placed approximately six "forward-deployed" engineers inside the National Security Agency to customize and deploy its most capable AI model, **Mythos Preview**, for offensive cyber operations — including potential network infiltration against China and Iran, per the Financial Times. The arrangement runs concurrently with Anthropic's active lawsuit against the Department of Defense, which designated the company a "supply chain risk" in March 2026 after Anthropic refused to remove guardrails on Claude for mass domestic surveillance and autonomous weapons. [[SOCFortress via Medium](https://socfortress.medium.com/anthropic-engineers-embedded-at-nsa-for-mythos-cyber-operations-4a73a99cd551); [Bloomberg Law](https://news.bloomberglaw.com/artificial-intelligence/anthropic-helping-us-prepare-mythos-for-offensive-operations-ft); [the-decoder](https://the-decoder.com/anthropics-mythos-model-is-reportedly-powering-nsa-offensive-cyber-ops-against-china-and-iran/)]

**What Mythos can do:** Anthropic's red team confirmed Mythos can identify and exploit zero-day vulnerabilities in every major operating system and web browser. The model uses an agentic architecture that autonomously reads source code, forms vulnerability hypotheses, writes and executes test cases, and iteratively confirms exploitable bugs without human guidance at each step. A complete exploit pipeline for a complex target costs under **$2,000 and completes in under 24 hours**. Britain's AI Security Institute measured a **73% success rate** on expert-level vulnerability research tasks. [[the-decoder](https://the-decoder.com/anthropics-mythos-model-is-reportedly-powering-nsa-offensive-cyber-ops-against-china-and-iran/); [TechTimes](https://www.techtimes.com/articles/317873/20260605/anthropic-embeds-engineers-inside-nsa-offensive-cyber-ops-sues-pentagon-barring-claude.htm)]

**The paradox:** The Pentagon ordered a complete purge of Anthropic technology from DoD systems by August 2026, citing supply-chain risk — yet the NSA (a DoD agency) secured an explicit carve-out for Mythos operations. Anthropic balked at uses carrying domestic reputational and legal cost (mass surveillance of Americans, autonomous weapons) while staffing a deployment aimed outward at foreign networks. The Electronic Frontier Foundation and congressional oversight figures have warned the arrangement bypasses democratic checks.

**Project Glasswing expansion:** On June 2, Anthropic expanded Mythos access to **~150 organizations across 15+ countries**, up from 50 mostly-US partners in April. Named members include Okta, Samsung, NATO, and ENISA. Partners have surfaced over **10,000 high- or critical-severity software vulnerabilities**; an internal Anthropic scan of 1,000 open-source projects flagged 23,019 potential vulnerabilities, 6,202 estimated as high or critical. The program now covers power, water, healthcare, and communications infrastructure sectors. Anthropic filed confidentially for an IPO at a valuation near **$1 trillion**.

**Bottom line:** The nation's most capable offensive AI cyber tool is operational on classified networks, staffed by private-sector engineers, deployed by an agency whose parent department considers their employer a security threat, and is simultaneously being commercialized to 150 organizations globally — without any public congressional hearing or legislative framework governing its operation.

---

**[NEW] CVE-2026-31431 "Copy Fail" — Linux Kernel LPE Grants Root in Seconds via 700-Byte Python Script, CISA KEV, All Major Distros Affected** [tl;dr sec]

A Linux kernel local privilege escalation vulnerability dubbed **"Copy Fail"** (CVE-2026-31431, CVSS 7.8) allows any unprivileged local user to gain root access on every major enterprise distribution — Ubuntu 24.04, Amazon Linux 2023, RHEL 10.1, SUSE 16 — using a deterministic **732-byte Python script**. The bug has existed in every mainstream Linux kernel since **2017** (commit 72548b093ee3). CISA added it to the Known Exploited Vulnerabilities catalog on **May 1, 2026**. [[Sysdig](https://www.sysdig.com/blog/cve-2026-31431-copy-fail-linux-kernel-flaw-lets-local-users-gain-root-in-seconds); [Orca Security](https://orca.security/resources/blog/cve-2026-31431-linux-kernel-copy-fail-privilege-escalation/); [tl;dr sec #331](https://tldrsec.com/p/tldr-sec-331)]

**How it works:** The bug lives in the kernel's `algif_aead` module, which exposes AEAD ciphers to userspace through `AF_ALG` sockets. A 2017 in-place optimization set `req->src = req->dst`, causing the output scatterlist to point at the same page-cache pages supplied by `splice()`. During `authencesn(hmac(sha256),cbc(aes))` decryption, the algorithm writes a 4-byte Extended Sequence Number scratch value at `dst[assoclen + cryptlen]` — but because of the pointer aliasing, that write lands inside the cached pages of the spliced file (e.g., `/usr/bin/su`). The attacker repeats this primitive at successive offsets to stage shellcode into the cached binary, then runs `su` to spawn a root shell. No race conditions, no special hardware, no kernel symbols required. [[NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-31431); [oss-sec](https://seclists.org/oss-sec/2026/q2/281)]

**Container escape:** Because the Linux page cache is shared between host and all containers, a process inside a Docker or Kubernetes pod with `AF_ALG` access can corrupt the host's page cache — turning this into a container escape primitive. The exploit leaves no on-disk artifacts; only the in-memory page cache is modified, bypassing standard file-integrity monitoring.

**Patches:** Fixed in Linux 7.0, 6.19.12, and 6.18.22 (and corresponding distribution backports for older LTS lines). **Mitigation:** Restrict `AF_ALG` socket creation via seccomp profiles, or `rmmod algif_aead` / `echo "install algif_aead /bin/false" > /etc/modprobe.d/disable-algif.conf`. Deploy Falco/Sysdig rules to detect unexpected `AF_ALG SEQPACKET` socket creation from non-disk-encryption processes. Treat any local foothold on an unpatched kernel as root-equivalent.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Google GTIG Q2 2026: First AI-Developed Zero-Day Identified, PRC/DPRK Actors Running AI-Augmented Vuln Research Pipelines, PROMPTSPY Autonomous Android Backdoor** [tl;dr sec]

Google Threat Intelligence Group published its Q2 2026 AI Threat Tracker, documenting a maturation of AI-enabled adversarial operations across the attack lifecycle. [[Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access); [tl;dr sec #331](https://tldrsec.com/p/tldr-sec-331)]

**Key findings:**

**First AI-developed zero-day:** Cyber criminals used an LLM to discover and weaponize a zero-day 2FA bypass in a popular open-source web admin tool, exploiting a high-level semantic logic flaw (hardcoded trust assumption) — the type of bug that fuzzers miss but LLMs, capable of reading developer intent, are uniquely positioned to find. GTIG disrupted the operation before mass exploitation began.

**PRC/DPRK industrial-scale vuln research:** UNC2814 (PRC) used persona-driven jailbreaking of Gemini to research embedded devices (TP-Link firmware, Odette FTP). APT45 (DPRK) sent **thousands of repetitive prompts** recursively analyzing CVEs and validating PoC exploits — building a scaled exploit arsenal at machine speed. Actors are integrating specialized security datasets (e.g., the "wooyun-legacy" Claude skill, containing 85,000+ real-world bugs) to prime models.

**AI-generated defense evasion:** Russia-nexus malware **CANFAIL** and **LONGSTREAM** (targeting Ukrainian organizations) include LLM-generated decoy logic — unused inert code and daylight-saving status queries — to pad payloads and frustrate static analysis. **APT27 (PRC)** used Gemini to develop an ORB fleet management tool with hardcoded 3-hop routing through 4G/5G SIM cards.

**PROMPTSPY Android backdoor:** GTIG expanded on ESET's initial reporting of this Android backdoor embedding an autonomous AI agent (`GeminiAutomationAgent`) powered by `gemini-2.5-flash-lite`. The agent serializes the device UI hierarchy via Accessibility API into XML, sends it to Gemini API with a "User Goal," and executes returned JSON structured actions (CLICK, SWIPE). Extremely extensible architecture for various device interaction goals.

**TeamPCP/UNC6780 AI supply chain attacks:** The threat actor known for Shai-Hulud compromised **LiteLLM**, **BerriAI**, **Trivy**, and **Checkmarx** repositories to plant the SANDCLOCK credential stealer, extracting AWS keys and GitHub tokens from build environments. They're also industrializing LLM access through middleware (Claude-Relay-Service, CLIProxyAPI) and automated account-registration pipelines.

**Takeaway:** The orchestration layers around AI — wrapper libraries, API connectors, skill packages — are now a primary software supply chain attack surface. Teams should inventory all AI integrations for third-party dependencies and monitor for compromised tooling, not just direct model attacks.

---

## ⚡ Quick Hits

- **[UPDATE] Everest Forms Pro CVE-2026-3300 — Second Attacking IP Identified** — Wordfence telemetry reveals a second primary attacking IP (209.146.60.26) alongside the previously reported 202.56.2.126 in the ongoing mass exploitation of this WordPress plugin flaw. 29,300+ total blocked attempts; patched since v1.9.13 (March 18). Administrators should block both IPs and audit for rogue accounts with username pattern `diksimarina`. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/critical-everest-forms-pro-flaw-exploited-to-take-over-wordpress-sites/)]
- **[tl;dr sec] AI Exfiltration in 60 Seconds — Claude Code Given Leaked AWS Keys Exfiltrates Data in Under a Minute** — Researcher Adan Alvarez demonstrated a six-phase kill chain (`GetCallerIdentity` → Policy Enumeration → Credential Recovery → AssumeRole → Enumeration → Exfiltration) completing in ~60 seconds. CloudTrail's 5-minute log delivery delay means traditional alerting is too slow for sub-minute AI-driven attacks. Defensive recommendation: honeytokens and honeypots to waste agent time. [[tl;dr sec #331](https://tldrsec.com/p/tldr-sec-331); [GitHub PoC](https://github.com/adanalvarez/ai-aws-incident-response-demo)]

---

*4 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit skipped — old.reddit.com returned errors on both `/hot/` and `/new/` endpoints. tl;dr sec #331 checked (June 4, 3 days fresh) — identified two material gaps: CVE-2026-31431 "Copy Fail" (CISA KEV, zero Miniflux coverage) and Google GTIG Q2 2026 AI threat report. Prior digests: June 1–6, 2026. Sources include SOCFortress/Medium, BleepingComputer, Bloomberg Law, Financial Times (via secondary), Google GTIG, Sysdig, Orca Security, NVD, oss-sec, tl;dr sec, and independent researchers.*
