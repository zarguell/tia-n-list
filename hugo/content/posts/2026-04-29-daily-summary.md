---
title: cPanel auth bypass 🔴, GitHub RCE vulnerability 🔧, LiteLLM exploitation in 36 hours ⚡, VECT wiper-not-ransomware 💀, Lazarus macOS malware 🍎, SAP supply-chain attack 📦
date: 2026-04-29
tags: ["remote code execution","authentication bypass","sql injection","ransomware","apt activity","supply chain compromise","credential theft","malware","ics-ot security","ai security","oauth security","shadow it"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: A critical cPanel/WHM authentication bypass (CVE-2026-41940, CVSS 9.8) requires emergency manual patching while a GitHub RCE (CVE-2026-3854) put millions of private repositories at risk. LiteLLM's pre-auth SQL injection was exploited within 36 hours of disclosure. VECT 2.0 ransomware permanently destroys files due to a cryptographic flaw, making payment futile. Lazarus Group targets macOS users with a new ClickFix-driven malware kit, and over 1,000 SAP npm packages are compromised in an active self-propagating supply-chain attack. Defense teams should audit OAuth grants to AI applications following the Vercel breach and verify ICS/OT remote access isn't internet-exposed.
---
# Daily Threat Intel Digest - April 29, 2026

## 🔴 Critical Threats & Active Exploitation

**[NEW] cPanel/WHM critical authentication bypass (CVE-2026-41940, CVSS 9.8) requires emergency manual update**

A critical authentication bypass vulnerability in cPanel and WHM allows unauthenticated access to the hosting control panel on all supported versions except the very latest. With a CVSS score of 9.8, this is among the highest-severity vulnerabilities disclosed this week — and the emergency patch is not delivered through normal update channels. Administrators must manually run `/usr/local/cpanel/scripts/upcp` to pull the fix, meaning organizations relying on automatic updates will remain vulnerable. The severity of the issue is underscored by Namecheap's decision to temporarily block ports 2083 and 2087 (cPanel/WHM ports) at the network level to protect customers until patches were available. cPanel/WHM is among the most widely deployed hosting control panels globally, putting shared hosting providers and their customers at immediate risk. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cpanel-whm-emergency-update-fixes-critical-auth-bypass-bug/); [Namecheap advisory](https://www.namecheap.com/status-updates/ongoing-critical-security-vulnerability-in-cpanel-april-28-2026/)]

**[NEW] GitHub RCE (CVE-2026-3854) could have exposed millions of private repositories**

A critical remote code execution vulnerability in GitHub's git push pipeline could have granted attackers full read/write access to private repositories with as little as a single crafted `git push` command. The flaw exists in how GitHub handles user-supplied options during push operations — values were incorporated into internal server metadata without sufficient sanitization, allowing injection of additional trusted fields that bypass sandboxing protections. Affects GitHub.com, GitHub Enterprise Cloud (including Data Residency and Managed Users), and GitHub Enterprise Server. GitHub reproduced the vulnerability within 40 minutes of Wiz's March 4 report and deployed a fix in under two hours, but any Enterprise Server instances that haven't applied the patch remain vulnerable. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/github-fixes-rce-flaw-that-gave-access-to-millions-of-private-repos/); [GitHub blog](https://github.blog/security/securing-the-git-push-pipeline-responding-to-a-critical-remote-code-execution-vulnerability/)]

**[NEW] CISA adds ConnectWise ScreenConnect (CVE-2024-1708) to Known Exploited Vulnerabilities catalog**

CISA added the ConnectWise ScreenConnect path traversal vulnerability to its KEV catalog on April 28, confirming active in-the-wild exploitation. The pre-auth path traversal flaw (CWE-22) allows unauthenticated remote attackers to access sensitive system files, modify application data, and potentially achieve remote code execution — providing a direct pathway for lateral movement in enterprise environments. Federal agencies must remediate under BOD 22-01, and CISA is urging private sector organizations to treat it with equal urgency. ScreenConnect's privileged access to endpoints makes it a high-value target for initial access brokers and ransomware operators. [[Cyber Security News](https://cyberpress.org/connectwise-screenconnect-vulnerability/); [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)]

## 🎯 Threat Actor Activity & Campaigns

**[NEW] VECT 2.0 ransomware is broken — it destroys files instead of encrypting them**

VECT 2.0, a ransomware strain recently advertised on BreachForums and operated in partnership with TeamPCP (the supply-chain attackers behind the LiteLLM, Trivy, Telnyx, and CERT-EU compromises), has a critical flaw in its encryption nonce handling that permanently corrupts larger files rather than encrypting them. Check Point researchers confirmed that all three versions of VECT's ransomware suffer from the defect, meaning victims who pay the ransom still cannot recover their data. VECT operators announced plans to target organizations already compromised by TeamPCP's supply-chain attacks, deploying ransomware payloads in environments where access had already been established. The partnership between a supply-chain attack group and a ransomware operator represents an escalation in the attack chain lifecycle. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/broken-vect-20-ransomware-acts-as-a-data-wiper-for-large-files/); [Check Point Research](https://www.checkpoint.com/)]

**[NEW] Lazarus Group deploys "Mach-O Man" macOS malware kit via ClickFix social engineering**

North Korea's Lazarus Group is using ClickFix social engineering lures to deliver a new macOS malware kit dubbed "Mach-O Man," targeting the fintech and cryptocurrency sectors. The malware steals credentials, Keychain secrets, and session tokens, providing attackers with a foothold into corporate environments. The kit represents Lazarus's continued investment in macOS-specific tooling after years of Windows-focused campaigns, reflecting the group's targeting shift toward Apple-using professionals in financial services. [[GBHackers](https://gbhackers.com/lazarus-targets-macos-users/)]

**[NEW] U.S. charges 19-year-old Scattered Spider member arrested in Finland**

Peter Stokes, a dual U.S.-Estonian national known online as "Bouquet," has been charged for his alleged role in Scattered Spider (Octo Tempest). Stokes was arrested April 10 in Finland while boarding a flight to Japan. Court documents describe social engineering campaigns targeting corporate help desks to bypass MFA, including a 2023 incident where attackers impersonated employees to request MFA resets and gained access to systems containing sensitive employee data. Encrypted chat logs show real-time coordination with accomplices during intrusions. Scattered Spider's young, geographically distributed membership and social engineering tradecraft have made it one of the most impactful cybercriminal groups of the past two years. [[Cyber Security News](https://cyberpress.org/u-s-charges-suspected-scattered-spider-member-for-infiltrating-sensitive-computer-systems/)]

## ⚠️ Vulnerabilities & Patches

**[NEW] LiteLLM SQL injection (CVE-2026-42208, CVSS 9.3) exploited within 36 hours of disclosure**

A pre-auth SQL injection vulnerability in the open-source AI gateway LiteLLM was exploited approximately 36 hours after the April 20 advisory publication. The flaw exists in the proxy API key verification process, where database queries did not parameterize caller-supplied values. Attackers sent crafted `Authorization` headers to LLM API routes and extracted data via the proxy's error-handling path, targeting tables containing API keys, provider credentials, and proxy configuration environment variables. Sysdig observed automated scanning attempts with rotating IPs and textbook column-count enumeration sweeps. While no post-exploitation abuse of extracted credentials has been confirmed, the 36-hour window between disclosure and exploitation demonstrates the shrinking time defenders have to patch. Update to LiteLLM v1.83.7. [[SecurityWeek](https://www.securityweek.com/fresh-litellm-vulnerability-exploited-shortly-after-disclosure/)]

**[NEW] Two Cursor AI vulnerabilities expose developer workstations**

Two high-severity vulnerabilities in the Cursor AI IDE target the growing attack surface of AI-assisted development environments. CVE-2026-26268 (discovered by Novee) leverages embedded bare repositories with malicious Git hooks that execute when Cursor's autonomous AI agent performs Git operations like checkout — no user interaction required. Separately, LayerX disclosed "CursorJacking" (CVSS 8.2), where any installed extension can silently extract API keys and session tokens from an unencrypted local SQLite database due to a lack of extension isolation. Cursor has acknowledged the extension issue but stated extensions operate within the same trust boundary as local applications, effectively declining to fix it. Disclosed in February 2026, it remains unpatched as of April. [[Cyber Security News](https://cyberpress.org/cursor-ai-extension-token-access-flaw-could-lead-to-full-credential-compromise/); [Cyber Security News](https://cyberpress.org/cursor-rce-threatens-developers/)]

**[NEW] Ollama vulnerabilities (CVE-2026-42248, CVE-2026-42249) disclosed by CERT Polska**

CERT Polska has disclosed two vulnerabilities in Ollama, the popular open-source local LLM runtime. Details are limited at this time but organizations running self-hosted LLM infrastructure should monitor for patches and advisories. [[CERT Polska](https://cert.pl/en/posts/2026/04/CVE-2026-42248/)]

## 🛡️ Defense & Detection

**[NEW] Vercel breach demonstrates shadow AI OAuth risk — third-party app compromise as supply chain**

The Vercel breach, where a single employee's trial of Context.ai's AI app (connected via OAuth to their Google Workspace account) became an attack pathway when Context.ai itself was compromised, illustrates a growing class of supply-chain risk: OAuth-bridged shadow SaaS. When employees connect AI apps to core platforms like Google Workspace or Microsoft 365, they create persistent programmatic bridges that persist even after the employee stops using the app. If the third-party app is breached, the bridge becomes a direct pathway into the organization. This is distinct from traditional shadow IT because the attack surface isn't the app itself — it's the OAuth token that grants access to production systems. Organizations should inventory OAuth grants to AI applications and implement conditional access policies that can revoke third-party tokens when risk signals change. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/learning-from-the-vercel-breach-shadow-ai-and-oauth-sprawl/); [Push Security analysis](https://pushsecurity.com/blog/unpacking-the-vercel-breach/)]

**[NEW] 1,006+ repositories compromised in SAP supply-chain attack via malicious npm packages**

An active supply-chain attack has compromised over 1,000 npm packages in SAP's namespace with a self-propagating malware strain (dubbed "Mini Shai-Hulud" by Aikido/GitGuardian researchers). The malware adapts to CI environments by reading environment variables, steals GitHub personal access tokens, and uses them to propagate to additional repositories — a pattern consistent with the TeamPCP supply-chain attack methodology. The repository count grew from 847 to 1,006 during the analysis write-up alone. Organizations using SAP npm packages should audit their dependencies and rotate any GitHub tokens that may have been exposed in CI environments. [[GitGuardian](https://blog.gitguardian.com/a-mini-shai-hulud-targeting-the-sap-ecosystem/)]

**[NEW] 670 internet-facing VNC servers provide unauthenticated access to ICS/OT systems**

Forescout research identified 670 VNC servers that provide direct, unauthenticated access to industrial control systems and operational technology panels, with nearly 60,000 VNC servers total lacking any authentication. Over 19,000 exposed RDP servers remain vulnerable to the BlueKeep flaw. Russia-linked threat actors (Infrastructure Destruction Squad / Dark Engine) have been actively scanning for exposed RDP/VNC/OT protocols and have publicly shared screenshots of compromised SCADA systems in Israel, Turkey, and Czechia. The Redheberg botnet has infected nearly 40,000 exposed VNC servers since February. Any organization with ICS/OT environments should verify that remote access protocols are not internet-facing. [[SecurityWeek](https://www.securityweek.com/hundreds-of-internet-facing-vnc-servers-expose-ics-ot/)]

---

*45 articles ingested from Miniflux Cyber feeds. Prior digests: none (first run). Sources include BleepingComputer, SecurityWeek, GBHackers, Cyber Security News, GitGuardian, Malware.News, and Black Hills Information Security.*
