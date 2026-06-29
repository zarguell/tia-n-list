---
title: "🔴 Netlogon 0-Click RCE Exploited, ⚠️ WP Maps Pro WordPress Admin Takeover, ⚠️ Google MCP Toolbox CVSS 9.4, 🎯 Kimsuky Binance Phishing, 📋 Microsoft Researcher Policy Reversal"
date: 2026-06-01
tags: ["windows","netlogon","rce","zero-click","wordpress","wp-maps-pro","mcp-toolbox","google","cve","langgraph","ai-security","kimsuky","north-korea","phishing","ransomware","qilin","everest","microsoft","nightmare-eclipse","entra-id","sspr"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "CVE-2026-41089 Windows Netlogon zero-click RCE confirmed under active exploitation against domain controllers — patch immediately. WordPress sites targeted via WP Maps Pro 0-day admin account creation (3,600+ exploit attempts blocked). Google MCP Toolbox CVSS 9.4, LangGraph AI checkpointing RCE, Kimsuky Binance phishing campaign, and Microsoft's Nightmare-Eclipse policy reversal round out today's intelligence."
---
# Daily Threat Intelligence Digest — June 1, 2026

*28 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] CVE-2026-41089 — Windows Netlogon 0-Click RCE Actively Exploited Against Domain Controllers — Patch Immediately**

A critical zero-click remote code execution vulnerability in the Windows Netlogon service, tracked as **CVE-2026-41089**, is now being actively exploited in the wild, confirmed by the Center for Cybersecurity Belgium (CCB). Unauthenticated remote attackers can execute arbitrary code with **SYSTEM-level privileges** by sending specially crafted Netlogon network requests — no user interaction, no credentials required.

This zero-click, pre-auth profile makes the flaw exceptionally attractive for automated exploitation, rapid lateral movement, and potential worm-like propagation across poorly segmented environments. Domain controller compromise cascades into full domain takeover: malware deployment via Group Policy, credential manipulation, security control bypass, and lateral movement into connected cloud resources.

**Scope:** All supported Windows Server versions from 2012 onward running as domain controllers. Patched in Microsoft's May 2026 Patch Tuesday (118 CVEs addressed, 16 critical). The CCB recommends prioritizing this as a top-tier emergency remediation item.

**Action:** Patch domain controllers first — particularly those with any internet exposure. Patching alone is insufficient given active exploitation; upscale monitoring for anomalous Netlogon traffic, unusual authentication patterns, sudden privileged group changes, and new admin account creation. Revisit network segmentation around domain controllers and ensure no direct internet exposure. [[Cyber Security News](https://cyberpress.org/windows-netlogon-0-click-rce-flaw/); [GBHackers](https://gbhackers.com/windows-netlogon-0-click-rce-vulnerability/)]

---

**[NEW] CVE-2026-8732 — WP Maps Pro Bug Exploited to Create Admin Accounts on 15,800+ WordPress Sites**

Hackers are actively targeting WordPress websites running WP Maps Pro — a premium interactive map plugin with **15,800+ sales** on Envato Market — exploiting a critical unauthenticated privilege escalation vulnerability tracked as **CVE-2026-8732**. The flaw lies in a "temporary access" AJAX endpoint intended for vendor support access, protected only by a publicly exposed nonce in frontend JavaScript.

Attackers send a crafted request with `check_temp` set to `false`, triggering `wp_insert_user()` to create a new WordPress administrator account with a randomized username, hardcoded email (`support@flippercode.com`), and a passwordless "magic login URL" returned in the response body. Wordfence researchers blocked **3,600+ exploitation attempts in 24 hours**.

**Impact:** Full site takeover — persistent backdoors, web shells, malicious plugin installation, private data access. All versions before 6.1.1 are vulnerable. The patch was released May 20 (vendor notified May 16 after proof of concept). Administrators should update immediately and audit for rogue admin accounts. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/wp-maps-pro-bug-exploited-to-create-admin-accounts-on-wordpress-sites/)]

---

**[NEW] Instagram Meta AI Support Chatbot Exploited for Account Takeover — Premium Handles Stolen, 2FA Not Affected**

Attackers manipulated Instagram's Meta AI-powered account recovery assistant into forwarding password reset codes without any identity verification — a pure AI logic-layer vulnerability rather than a backend breach. Researchers **ZachXBT** and **Dark Web Informer** first exposed the exploit, which targeted premium short-handle accounts (including @hey and @jowo, collectively valued at over **$1 million**) for resale on private Telegram channels.

**How it worked:** The AI chatbot lacked rate limiting and authentication enforcement on password reset requests. Anyone with knowledge of a target's username could prompt the AI to forward a reset link. Meta patched the flaw late Friday and confirmed no backend compromise. **Accounts with 2FA enabled were not affected.**

This incident highlights a growing attack surface: AI-assisted support tools granted privileged access to sensitive account recovery functions. The "account-takeover-as-a-service" ecosystem monetized the vulnerability in hours. [[GBHackers](https://gbhackers.com/meta-ai-vulnerability/); [Cyber Security News](https://cyberpress.org/instagram-meta-ai-flaw/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Kimsuky Targets Korean Binance Users with BN_FIU_2026.chm Malware**

North Korean APT group **Kimsuky** is targeting South Korean cryptocurrency users with a Binance-themed malicious CHM file (`BN_FIU_2026.chm`, 1MB, MD5: `eb823d5448bc3d39e353a5fcf0feb91f`). The file masquerades as a financial regulatory document from Korea's Financial Intelligence Unit (FIU) related to Binance compliance — a social engineering lure designed to harvest credentials and cryptocurrency wallet access.

Kimsuky (also tracked as Velvet Chollima, Thallium) has a well-documented history of cryptocurrency-targeted operations using CHM files with embedded scripts. This campaign continues the group's focus on South Korean crypto investors following earlier operations using Coinbase and Kraken lures. [[Malware.News](https://malware.news/t/kimsuky-binance-bn-fiu-2026-chm/107448#post_1)]

---

**[NEW] Qilin Ransomware Hits Carton Craft Supply — U.S. Supply Chain Targeted**

The Qilin ransomware group claimed responsibility for an attack on **Carton Craft Supply** (US packaging supply chain company) on May 28, threatening to leak sensitive data. Qilin operates as a RaaS with a Rust-based encryptor, one of the more technically sophisticated ransomware strains. This follows Qilin's prior targeting of healthcare and manufacturing sectors. [[Malware.News](https://malware.news/t/qilin-ransomware-strikes-carton-craft-supply/107452#post_1)]

---

**[NEW] Everest Ransomware Strikes VVO Finance — German Financial Sector in Crosshairs**

**Everest** ransomware group claimed a May 28 attack on **VVO Finance**, a German financial services firm, threatening to release stolen data. Everest operates as a dual-extortion ransomware group with a history of targeting financial institutions across Europe. The attack underscores continued ransomware pressure on European financial services mid-market. [[Malware.News](https://malware.news/t/everest-ransomware-attack-on-vvo-finance-in-germany/107451#post_1)]

---

**[UPDATE] TheGentlemen Ransomware Adds Mexican Agribusiness Victim — Grupo Premier**

TheGentlemen ransomware (Storm-2697, analyzed in-depth by Microsoft Threat Intelligence on May 29) claimed a new victim: **Grupo Premier**, a Mexican nuts and dried fruits company (`grupopremier.com.mx`). The group threatened to leak data unless negotiations commenced. While TheGentlemen's technical capabilities were covered in the May 29 digest (self-propagating Go-based RaaS with per-file Curve25519+XChaCha20 encryption and 21 lateral-movement techniques per target), this victim is **the group's first confirmed Mexican target**, signaling geographic expansion into Latin America. [[Malware.News](https://malware.news/t/thegentlemen-ransomware-targets-grupo-premier-in-mexico/107450#post_1)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] CVE-2026-9739 (CVSS 9.4) — Google MCP Toolbox for Databases Exposed via Hardcoded Wildcard CORS — DNS Rebinding Attack Vector**

A critical vulnerability in Google's MCP Toolbox for Databases carries a **CVSS 4.0 score of 9.4** and enables unauthenticated DNS rebinding attacks against organizations using SSE (Server-Sent Events) transport. Root cause: a hardcoded `Access-Control-Allow-Origin: *` header inadvertently left in the SSE initialization handler during beta, silently overriding the `allowed-origins` and `allowed-hosts` security flags.

**Impact:** Unauthenticated attackers tricking Chrome users into visiting an attacker-controlled domain can bypass CORS protections, establish unauthorized SSE connections to the MCP Toolbox interface, and execute arbitrary commands against connected enterprise databases — **Cloud SQL, AlloyDB, and Spanner**.

**Broader pattern:** Two related CVEs in the MCP Go SDK (CVE-2026-34742) and Java SDK (CVE-2026-35568) indicate a systemic origin-validation weakness across the MCP ecosystem. Google acknowledged on May 27, patched by May 28 (GitHub issue #3053, PR #3054). **No public PoC or active exploitation confirmed yet.**

**Action:** Disable SSE-based Toolbox connections; enforce strict CORS headers; restrict Toolbox endpoints to trusted networks; audit all MCP-connected AI agent pipelines for exposed instances. [[Cyber Security News](https://cyberpress.org/mcp-toolbox-vulnerability-exposed/)]

---

**[NEW] LangGraph Checkpointing RCE (GHSA-wwqv-p2pp-99h55) — JsonPlusSerializer Unsafe Deserialization in AI State Persistence Layer**

A high-severity RCE vulnerability disclosed in the **LangGraph checkpointing library** (langgraph-checkpoint) allows attackers to execute arbitrary Python code via crafted checkpoint payloads. Published by LangChain contributor Eugene Yurtsev, the flaw resides in the **JsonPlusSerializer's fallback to constructor-style deserialization** when Unicode surrogate values cause serialization errors — enabling invocation of arbitrary Python functions like `os.system()`.

**Scope:** langgraph-checkpoint <3.0 using the default serializer with untrusted inputs. Impact is highest in **multi-tenant AI services**, shared workflows, and collaborative AI apps where one user's tainted checkpoint can compromise the host. LangChain patched in version 3.0 (late 2025) via a constructor allow-list. LangGraph API deployments 0.5+ include the fix automatically. Developers should verify they're not relying on the deprecated unsafe JSON fallback. [[Cyber Security News](https://cyberpress.org/hackers-target-signal-backups/)]

---

## 📋 Policy & Industry News

**[UPDATE] Microsoft Backs Down: "We Won't Sue Researchers" in Nightmare-Eclipse — But Structural Trust Damage Remains**

Following days of intense community backlash over its May 28 blog post threatening legal action against the "Nightmare Eclipse" zero-day researcher, Microsoft issued a follow-up statement clarifying it has **"no intention to pursue action against individuals conducting or publishing their security research."** The MSRC account tweeted: *"We recognize that [the vendor-researcher] relationship is both critical and, at times, fragile. We deeply value the security community."*

**The delta from May 31 coverage:** Microsoft explicitly acknowledged that "some interactions have fallen short" and pledged greater transparency and professionalism in future MSRC engagements. However, the underlying structural issues remain unaddressed: the researcher's MSRC account access was revoked, bug bounties were withheld, and the Digital Crimes Unit threat has been walked back with no policy changes. The promised "#boneshattering" disclosure date of **July 14, 2026** still looms.

The incident has exposed deep tensions around coordinated disclosure workflows, particularly for high-volume researchers whose bug reports can overwhelm traditional triage channels — a problem amplified by AI-assisted vulnerability discovery. [[Cyber Security News](https://cyberpress.org/microsoft-nightmare-eclipse-case/); Microsoft MSRC @msftsecresponse]

---

**[NEW] Microsoft Entra ID SSPR Overhaul — Closing Directory-Attribute-as-Recovery-Factor Gap, Enforcement Begins September 7**

Microsoft announced a significant security hardening for Entra ID Self-Service Password Reset (SSPR) under its Secure Future Initiative. For years, SSPR accepted directory-stored contact attributes (`mobilePhone`, `businessPhone`, `otherMails`) as recovery factors without requiring explicit user enrollment — meaning HR-system phone numbers functioned as de facto security recovery channels.

**The change:** Starting September 7, 2026, directory-sourced contact attributes will be **rejected** for SSPR verification. Users must register explicit authentication methods. A registration campaign launches July 6, 2026, prompting affected users automatically. Microsoft reports **86% of SSPR verifications already use registered methods** — the remaining 14% represents real exposure, potentially thousands of users in large enterprise tenants.

**Action:** Admins should audit registration coverage in Entra admin center → Authentication methods → User Registration Details. Prepare Temporary Access Pass workflows for fallback. Prioritize privileged account registration first — a failed recovery path for an admin mid-workday is an operational incident waiting to happen. [[Cyber Security News](https://cyberpress.org/microsoft-strengthens-entra-id-password-resets/)]

---

## ⚡ Quick Hits

- **Unidentified RAT Delivering NetSupport RAT:** SANS ISC reports a campaign where an unidentified initial access RAT (delivery vector not yet confirmed) drops the well-known **NetSupport RAT** as the implant payload. NetSupport RAT is a legitimate remote administration tool frequently abused by threat actors for persistence, screen capture, keylogging, and file transfer. Defenders should monitor for NetSupport Manager process execution and outbound connections on TCP 443. [[Malware.News via SANS ISC](https://malware.news/t/unidentified-rat-pushes-netsupport-rat-mon-jun-1st/107453#post_1)]

- **YARA-X 1.17.0 Released:** VirusTotal's next-generation YARA engine continues active development with release 1.17.0, adding new module capabilities and bug fixes. Defenders relying on YARA-based detection should test upgrade compatibility, particularly for custom rules using experimental modules. [[Malware.News](https://malware.news/t/yara-x-1-17-0-release-sun-may-31st/107447#post_1)]
