---
title: "🛡️ CIFSwitch Linux LPE, Flowise RCE CVSS 9.9, Edge Password Leak, Russian Tech Theft, Microsoft vs Researchers"
date: 2026-05-31
tags: ["CIFSwitch","CVE-2026-40933","Flowise","CVE-2026-0257","Microsoft Edge","Linux","privilege escalation","AI security","Russia","espionage","vulnerability disclosure"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CIFSwitch Linux kernel LPE gives root on multiple distros (PoC published); Flowise CVE-2026-40933 CVSS 9.9 critical RCE targets AI agent builders with published exploit; Microsoft Edge stored all saved passwords in plaintext RAM — reversed course after community backlash; Russian intelligence accelerates Western tech theft as sanctions intensify; Microsoft threatens legal action against researcher Nightmare Eclipse over zero-day dumps, sparking widespread security community backlash."
---

# Daily Threat Intelligence Digest — May 31, 2026

*7 articles ingested from Miniflux Cyber feeds. Sunday edition — focused on genuinely new developments. Prior digests: May 26–30, 2026. Cross-referencing via Reddit r/cybersecurity detected one gap not covered in Miniflux feeds: Microsoft Edge plaintext password exposure. Stale items omitted: CVE-2026-0257 Palo Alto exploitation and severity bump (covered May 30 with full Rapid7 analysis), YellowKey BitLocker zero-day (May 26), DigiCert CA compromise (May 27), Fragnesia/Copy Fail Linux LPEs (May 27), NIST/NVD policy changes (May 27).*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] CVE-2026-0257 — Palo Alto Networks Raises GlobalProtect Severity to High, Confirms Limited Exploit Attempts**

Palo Alto Networks updated its advisory on Friday to raise CVE-2026-0257 from Medium to **High severity**, confirming that the PAN-OS GlobalProtect authentication bypass — which allows forgery of authentication override cookies for unauthorized VPN access — is now being exploited in limited attacks against unpatched devices. CISA added the flaw to its Known Exploited Vulnerabilities catalog on May 29 with a **June 1 remediation deadline** for federal agencies.

This confirms and extends the findings Rapid7 reported earlier this week: two exploitation waves (May 17 from Vultr hosting, May 21 from Dromatics Systems) targeting local admin accounts via forged cookie authentication, with some victims receiving full VPN IP assignments granting internal network access. **Recommended action:** patch unpatched GlobalProtect gateways immediately; disable authentication override or use separate certificates if patching is delayed. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/palo-alto-globalprotect-vpn-auth-bypass-flaw-now-exploited-in-attacks/); [Rapid7](https://www.rapid7.com/blog/post/etr-rapid7-observed-exploitation-of-pan-os-globalprotect-authentication-bypass-vulnerability-cve-2026-0257/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] CIFSwitch — 19-Year-Old Linux Kernel Privilege Escalation Gives Root on Multiple Distributions, PoC Published**

SpaceX security engineer Asim Viladi Oglu Manizada discovered and disclosed a local privilege escalation vulnerability in the Linux kernel's CIFS subsystem, dubbed **CIFSwitch**, that allows an unprivileged user to forge `cifs.spnego` key requests and abuse the kernel's authentication workflow to load a malicious NSS module — achieving **root code execution**.

The vulnerability was introduced in 2007 and affects vulnerable combinations of Linux kernel CIFS + cifs-utils (version 6.14+). Confirmed vulnerable with default configurations: **Linux Mint 21.3/22.3, CentOS Stream 9, Rocky Linux 9, AlmaLinux 9, Kali Linux 2021.4–2026.1, SLES 15 SP7**. Ubuntu, Debian, Pop!_OS, and other distributions may be vulnerable if cifs-utils is installed. Ubuntu 26.04, Fedora 40+, CentOS Stream 10, and SLES 16 have default SELinux/AppArmor policies that block the attack. Fixed via kernel commit 3da1fdf (adds origin validation to cifs.spnego requests). **Mitigations:** disable/blacklist CIFS module if unused, remove cifs-utils, or disable unprivileged user namespaces. Manizada has published a PoC exploit. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-cifswitch-linux-flaw-gives-root-on-multiple-distributions/)]

**[NEW] CVE-2026-40933 (CVSS 9.9) — Critical RCE in Flowise AI Agent Builder, PoC Published — Affects All Self-Hosted Instances Before 3.1.0**

Exploit code has been published for a critical remote code execution vulnerability in **Flowise**, the open-source drag-and-drop LLM/AI agent builder with 52,000+ GitHub stars. Tracked as CVE-2026-40933 (CVSS 9.9), the root cause is an unsafe serialization of stdio commands in the Anthropic MCP adapter — characterized by OX Security as a systemic, "by design" command injection vulnerability in the MCP ecosystem.

**Attack vector:** Any user who can create or edit chatflows can add a Custom MCP Tool with a malicious stdio command configuration. The chatflow can be exported as JSON and shared with a victim. When the victim imports the chatflow, the Flowise canvas triggers MCP server tool enumeration — **executing the attacker's arbitrary command automatically**. The published PoC creates a reverse shell. **Impact:** full OS-level command execution with Flowise process privileges (commonly **root** in containerized deployments), plus access to every stored credential and connected service. Flowise Cloud is not affected (stdio MCP disabled by default). **Patch immediately to version 3.1.0** and restrict chatflow creation/edit permissions. [[SecurityWeek](https://www.securityweek.com/exploit-code-published-for-critical-flowise-rce-vulnerability/); OX Security]

**[NEW] Microsoft Edge Loads All Saved Passwords in Plaintext RAM — Researcher Publishes Dump Tool, Microsoft Reverses "By Design" Position After Backlash**

Security researcher Tom Jøran Sønstebyseter Rønning discovered that Microsoft Edge decrypts and loads **every saved password into process memory in cleartext at startup** — a behavior unique among Chromium-based browsers. Any malware with local user access can dump all stored credentials using a simple `strings` command on a browser memory dump, completely bypassing Edge's biometric authentication for password manager access. Google Chrome uses App-Bound Encryption and only decrypts passwords on demand.

Microsoft initially classified this as "a deliberate design decision" and "within the expected threat model," arguing that local access requires prior compromise. Following significant backlash and independent verification by Heise.de and others, Microsoft reversed course on **May 16–18**: Edge version 148 and newer no longer load passwords into memory at startup, decrypting them only when needed for autofill. Rønning published a GitHub tool demonstrating the extraction technique. **Recommended action:** organizations relying on Edge's built-in password manager should migrate users to dedicated password managers (Bitwarden, 1Password, KeePass) with proper in-memory encryption. [[PCWorld](https://www.pcworld.com/article/3131805/microsoft-backtracks-on-edge-storing-your-passwords-in-plaintext-ram.html); [SANS ISC](https://isc.sans.edu/diary/32954); [Microsoft Edge VR](https://microsoftedge.github.io/edgevr/posts/Saved-passwords-in-Edge-memory-what-were-changing-and-why/)]

---

## 📋 Policy & Industry News

**[NEW] Russian Intelligence Agencies Intensify Western Tech Theft — Sabotage, Cyber Espionage, and Covert Procurement Accelerate as Sanctions Bite**

Three senior European intelligence officials (Sweden, Finland, Estonia) detail Russia's escalating, multi-pronged campaign to steal Western defense technology, dual-use equipment, and advanced research as sanctions pressure mounts. Targeted sectors include **advanced manufacturing, defense (Gripen fighter jet tech), space technology, quantum computing, and marine technology** — procured via fake companies, middlemen supply chains, and cyber espionage.

**Operational shift:** Russian agencies are "no longer caring as much about potential attribution" (Christoffer Wedelin, Swedish Security Service), taking greater risks including **active sabotage** — a 2023 attempt to destroy a Swedish power plant failed only because the intrusion was detected. The UK's GCHQ Director confirms Russia is "relentlessly targeting" allies with tech theft, sabotage, and assassination plots. Internal economic pressure is driving aggression: ~one-third of Russia's GDP funds the war, with a budget deficit reaching 3.4 trillion rubles ($47.9B). Estonia's intelligence chief warns Moscow could face a **financial crisis by year-end** if Western pressure persists. [[SecurityWeek / AP](https://www.securityweek.com/russian-spies-are-aggressively-seeking-western-technology-as-sanctions-bite-officials-say/)]

**[NEW] Microsoft Threatens Legal Action Against Security Researcher Over Zero-Day Dumps — Community Erupts Over "Chilling Effect" on Vulnerability Research**

Microsoft published a blog post on May 27 threatening to use its **Digital Crimes Unit** against the researcher operating as "Nightmare Eclipse" (aka Chaotic Eclipse), who publicly released working PoC exploits for six Windows zero-days — **BlueHammer, RedSun, UnDefend, YellowKey (CVE-2026-45585), GreenPlasma, and MiniPlasma** — without prior disclosure to Microsoft. The researcher claims Microsoft revoked their MSRC account access and withheld credit/payment, leaving them no coordinated disclosure channel. Three of the six flaws (BlueHammer, RedSun, UnDefend) have been exploited in the wild per both Microsoft and CISA.

The security community response has been **overwhelmingly critical of Microsoft**:

- **Katie Moussouris** (pioneer of Microsoft's bug bounty program): "The mention of the Digital Crimes Unit in a post discussing vulnerability disclosure makes the post vaguely threatening... it will only result in security researchers distrusting Microsoft."
- **Kevin Beaumont**: "Proof of concept exploit creation and distribution for zero days is 'criminal activity' now? Responsible disclosure quite often is framed to protect the product owner, not the customer — using it to try to criminally prosecute people is a new low."
- **Dustin Childs (ZDI)**: "CVD is a two-way street. The vendor has some responsibility as well."

The researcher has promised a "#boneshattering" disclosure on **July 14, 2026**, raising concerns about an escalating cycle of adversarial disclosure. Downstream risk: the chill on researcher-Microsoft relations could mean fewer bugs reported privately — leaving customers exposed longer. [[TechCrunch](https://techcrunch.com/2026/05/29/microsoft-under-fire-for-threatening-security-researcher-with-criminal-investigation/); [The Register](https://www.theregister.com/security/2026/05/28/microsoft-0-day-feud-escalates-as-researcher-threatens-another-windows-exploit-dump/); [The Verge](https://www.theverge.com/tech/940416/microsoft-nightmare-eclipse-zero-day-vulnerability)]

---

*7 articles ingested from Miniflux Cyber feeds. Cross-referencing via Reddit r/cybersecurity detected one gap: Microsoft Edge plaintext password exposure (covered above). Prior digests: May 26–30, 2026. Sources include BleepingComputer, SecurityWeek (AP), TechCrunch, The Register, The Verge, PCWorld, SANS ISC, Microsoft Edge VR blog, Rapid7, OX Security.*