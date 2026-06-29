---
title: "🛡️ Defender Zero-Days Exploited, 🔑 Linux SSH Key Flaw, ☁️ DigiCert CA Breach, 🎯 TeamPCP Supply Chain, 🛡️ NVIDIA Triton 9.8"
date: 2026-05-21
tags: ["Microsoft Defender", "CVE-2026-41091", "CVE-2026-45498", "SonicWall", "DigiCert", "TeamPCP", "Supply Chain", "DurableTask", "CloudZ RAT", "Linux Kernel", "CVE-2026-46333", "PinTheft", "Fragnesia", "NVIDIA Triton", "ExifTool", "GhostTree", "CISA", "Verizon DBIR", "Gremlin Stealer", "GraphWorm", "BadIIS", "WantToCry", "First VPN"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Microsoft warns of two actively exploited Defender zero-days (CVE-2026-41091, CVE-2026-45498) added to CISA KEV; DigiCert reveals 60 code-signing certificates stolen via malicious screenshot attack on customer support; TeamPCP supply chain campaign widens to Microsoft DurableTask Python client (400K monthly downloads) while Grafana confirms missed token rotation and GitHub details 3,800-repo breach via Nx Console VS Code extension; nine-year-old Linux kernel flaw (CVE-2026-46333) enables SSH key and shadow file exfiltration; NVIDIA Triton Inference Server patches 8 CVEs including 9.8 auth bypass; Drupal releases critical security update with expected public exploit within hours; CloudZ RAT abuses Microsoft Phone Link for SMS OTP interception; Verizon DBIR 2026 shows vulnerability exploitation overtaking credential theft as top breach vector."
---

# Daily Threat Intelligence Digest — May 21, 2026

*93 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] Microsoft Defender Zero-Days (CVE-2026-41091, CVE-2026-45498) — Actively Exploited, CISA Adds to KEV**

Microsoft rolled out emergency patches for two Microsoft Defender vulnerabilities that are being actively exploited in zero-day attacks. CVE-2026-41091 is a privilege escalation flaw in the Malware Protection Engine (versions ≤1.1.26030.3008) stemming from improper link resolution before file access — allowing attackers to gain SYSTEM privileges. CVE-2026-45498 affects the Microsoft Defender Antimalware Platform (≤4.18.26030.3011) and enables denial-of-service attacks against unpatched Windows devices. CISA added both to its Known Exploited Vulnerabilities catalog, ordering federal agencies to secure endpoints by June 3. Microsoft has released Malware Protection Engine versions 1.1.26040.8 and 4.18.26040.7; automatic updates should deliver the fix, but organizations should verify installation. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-warns-of-new-defender-zero-days-exploited-in-attacks/); [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)]

**[UPDATE] SonicWall VPN MFA Bypass (CVE-2024-12802) — Incomplete Patching Enables Ransomware Operations**

Threat actors brute-forced VPN credentials and bypassed MFA on SonicWall Gen6 SSL-VPN appliances to deploy tools used in ransomware attacks. ReliaQuest responded to multiple intrusions between February and March, assessing "with medium confidence" these represent the first in-the-wild exploitation of CVE-2024-12802. Crucially, the affected devices _appeared_ patched (running updated firmware) but remained vulnerable because the required post-update LDAP reconfiguration was never performed — a manual step that involves deleting and recreating the LDAP configuration without `userPrincipalName` in the login name field. Attackers completed network reconnaissance and RDP access within 30-60 minutes. Rogue login attempts appeared as normal MFA flows in logs, making detection dependent on the `sess="CLI"` signal and event IDs 238/1080. ReliaQuest assesses the threat actor is likely an initial access broker. Gen6 devices reached end-of-life on April 16 and no longer receive security updates. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-bypass-sonicwall-vpn-mfa-due-to-incomplete-patching/)]

**[NEW] DigiCert Breach: 60 Code-Signing Certificates Stolen via Malicious Screenshot — Microsoft Defender False Positives Follow**

A threat actor contacted DigiCert's customer support via chat on April 2, sending a ZIP file disguised as a screenshot containing a `.scr` executable. Despite CrowdStrike blocking four delivery attempts, a fifth compromised one analyst's endpoint (ENDPOINT1). A second analyst's machine (ENDPOINT2) was also compromised — this one lacked CrowdStrike entirely, remaining undetected for 10 days. Using access to DigiCert's internal support portal via a "customer impersonation" feature, the attacker obtained initialization codes for previously approved EV code-signing certificate orders. DigiCert revoked 60 certificates total: 27 linked to the Zhong Stealer malware campaign (11 confirmed by community malware reports, 16 identified internally), plus 33 additional certificates revoked preemptively. Affected customers include Tencent, Lenovo, Palit, Shuttle, and organizations across 13 countries. On April 30, Microsoft Defender began falsely flagging legitimate DigiCert root certificates as `Trojan:Win32/Cerdigent.A!dha`, removing them from the Windows trust store and breaking TLS connections — a detection linked to the incident. Microsoft corrected the false positives within hours. The incident underscores how even certificate authorities with mature security programs can be compromised through social engineering when secondary endpoints lack full sensor coverage. [[r/cybersecurity](https://www.reddit.com/r/cybersecurity/) (634↑); [BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-defender-wrongly-flags-digicert-certs-as-trojan-win32-cerdigentadha/); [DigiCert Incident Report](https://bugzilla.mozilla.org/show_bug.cgi?id=2033170)]

---

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] TeamPCP Supply Chain Campaign Widens: Microsoft DurableTask, GitHub 3,800 Repos, Grafana Missed Token Rotation**

The ongoing Mini Shai-Hulud / TeamPCP supply chain campaign has escalated dramatically across multiple fronts:

- **Microsoft DurableTask Python Client Compromised:** Three malicious versions (v1.4.1–1.4.3) of the `durabletask` PyPI package (400K+ monthly downloads) were published in a 35-minute window on May 19 using stolen PyPI API tokens. The 28 KB payload targets AWS (19 regions), Azure (all subscriptions), GCP, Kubernetes, HashiCorp Vault, Bitwarden, and 1Password credentials, with lateral movement via AWS SSM `SendCommand` and `kubectl exec`. Infection markers at `~/.cache/.sys-update-check`. [[Cyber Security News](https://cyberpress.org/microsoft-durabletask-python-client-compromised/); [GBHackers](https://gbhackers.com/microsoft-durabletask-python-client-targeted-teampcp/)]

- **GitHub Confirms 3,800 Repos Breached via Nx Console VS Code Extension:** GitHub CISO Alexis Wales confirmed the TeamPCP-claimed breach originated from a malicious Nx Console VS Code extension (version 18.95.0, available for ~18 minutes on VS Marketplace). The extension was weaponized via compromised TanStack npm packages that exfiltrated a contributor's GitHub credentials. The payload targets npm, AWS, Kubernetes, GitHub, GCP, and Docker credentials. GitHub rotated critical secrets Monday-Tuesday and continues investigating. TeamPCP is asking $50,000+ for the stolen data on Breached. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/github-links-repo-breach-to-tanstack-npm-supply-chain-attack/)]

- **Grafana Missed Token Rotation:** Grafana confirmed a single workflow token was missed during their post-TanStack rotation on May 1, allowing attackers to access private repositories, exfiltrate source code, and business contact information. No customer production systems were compromised. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/grafana-breach-caused-by-missed-token-rotation-after-tanstack-attack/)]

- **@antv npm Wave:** 639 malicious package versions across 323 unique npm packages were published in a one-hour worm attack against the @antv ecosystem, with valid Sigstore provenance attestation via abused OIDC tokens. [[GBHackers](https://gbhackers.com/antv-npm-packages/)]

TeamPCP's 2026 campaign has now claimed TanStack, Mistral AI, Guardrails AI, LiteLLM, @antv, Nx Console, Checkmarx, Trivy, and Microsoft's durabletask — making it the most prolific software supply chain campaign in recent memory.

**[NEW] CloudZ RAT Abuses Microsoft Phone Link to Intercept SMS OTPs Without Compromising the Phone**

Cisco Talos disclosed an intrusion active since January 2026 deploying a previously undocumented plugin called "Pheno" for the CloudZ RAT. Pheno hijacks the Microsoft Phone Link application's PC-to-phone bridge, monitoring for active `YourPhone`/`PhoneExperienceHost` processes and accessing its local SQLite database (`PhoneExperiences-*.db`) to steal SMS-based OTPs and authenticator app notifications. The attack chain begins with a fake ScreenConnect update dropping a Rust-based loader, then a .NET loader deploying CloudZ. The technique shifts OTP interception risk from mobile devices to enterprise-managed Windows systems, bypassing mobile-focused security controls. Notably, the CloudZ RAT also performs broad credential harvesting from browser data and supports file operations and remote command execution. Defenders should monitor for unexpected `YourPhone` process activity and consider eliminating SMS-based OTP in favor of hardware security keys. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cloudz-malware-abuses-microsoft-phone-link-to-steal-sms-and-otps/); [Cisco Talos](https://blog.talosintelligence.com/cloudz-pheno-infostealer/)]

---

## ⚠️ Vulnerabilities & Patches

**[UPDATE] CVE-2026-46333: Nine-Year-Old Linux Kernel Flaw Enables SSH Key Exfiltration and Root (Qualys TRU)**

Qualys TRU disclosed a critical logic flaw in the Linux kernel's `__ptrace_may_access()` function, present since November 2016 (v4.10-rc1), that allows unprivileged local attackers to steal SSH host private keys, read `/etc/shadow` password hashes, and execute arbitrary commands as root. The race condition exploits a window during process exit where memory maps are nulled before file descriptors close — `pidfd_getfd()` (introduced v5.6) pairs with this to hijack open FDs from dying privileged processes like `ssh-keysign`, `chage`, `pkexec`, and `accounts-daemon`. At default `ptrace_scope=1`, YAMA LSM permits access because the attacker is the parent of a spawned SUID child. Qualys confirmed working exploits on Debian 13, Ubuntu 24.04/26.04, Fedora 43/44. A public fix landed on May 14, with distribution patches following. Interim mitigation: set `kernel.yama.ptrace_scope=2` (irreversible without reboot, breaks cross-process debuggers). Organizations should apply kernel updates urgently and rotate SSH host keys. [[Cyber Security News](https://cyberpress.org/nine-year-old-linux-kernel-flaw/); [Qualys Blog](https://blog.qualys.com/vulnerabilities-threat-research/2026/05/20/cve-2026-46333-local-root-privilege-escalation-and-credential-disclosure-in-the-linux-kernel-ptrace-path); [GBHackers](https://gbhackers.com/nine-year-old-kernel-flaw/)]

**[NEW] PinTheft: Linux Kernel LPE PoC Released — RDS Zerocopy + io_uring Fixed Buffers Chain Achieves Deterministic Root**

Researcher Aaron Esau (V12) released a working PoC for PinTheft, a Linux LPE exploiting a double-free bug in the RDS zerocopy send path (`rds_message_zcopy_from_user()`). The exploit chains 1,024 failing RDS sends with io_uring fixed buffers to exhaust FOLL_PIN references, reclaim the page-cache entry of a SUID-root binary, and overwrite it with a malicious ELF payload. No race condition required — the exploit is deterministic. Requires `CONFIG_RDS`, `CONFIG_RDS_TCP`, and `CONFIG_IO_URING` enabled. The RDS module is only enabled by default on Arch Linux among major distributions, but systems with RDS manually loaded remain fully at risk. Mitigation: `rmmod rds_tcp rds` and block modules via modprobe config. This is the fourth Dirty-Frag-class vulnerability disclosed in recent weeks, alongside Dirty Frag, Fragnesia, and DirtyDecrypt. [[Cyber Security News](https://cyberpress.org/pintheft-linux-vulnerability/); [GBHackers](https://gbhackers.com/poc-released-for-pintheft-linux-flaw/)]

**[UPDATE] Drupal Critical Security Release — Patch Window Closed, Exploit Code Expected Within Hours**

Drupal issued a highly critical security release (severity 20/25) on May 20 between 17:00–21:00 UTC. The Drupal Security Team warned exploit code may be developed within hours of disclosure. Affects Drupal 8+ (excluding Drupal 7). Security updates released for Drupal 11.3.x, 11.2.x, 11.1.9, 10.6.x, 10.5.x, and 10.4.9. EOL versions 9.5 and 8.9 receive hotfix files only. The flaw is rated "highly critical," suggesting potential impact on confidentiality, integrity, and availability. Sites using Drupal Steward were protected against known attack vectors prior to patch release. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/drupal-critical-update-to-fix-bug-with-high-exploitation-risk/); [GBHackers](https://gbhackers.com/critical-drupal-vulnerability-could-leave-sites-open-to-cyberattack/)]

**[NEW] NVIDIA Triton Inference Server: 8 CVEs Including Critical 9.8 Authentication Bypass**

NVIDIA patched eight vulnerabilities in Triton Inference Server (r26.03), led by CVE-2026-24207 (CVSS 9.8, CWE-288) — an authentication bypass requiring no privileges, no user interaction, and network-only access, enabling unauthenticated remote code execution, privilege escalation, and data tampering. Three additional flaws affect the DALI backend: OOB read (CVE-2026-24213, CVSS 8.0), integer overflow (CVE-2026-24214, CVSS 8.0), and resource exhaustion (CVE-2026-24215, CVSS 5.7). Two path-traversal vulnerabilities (CVE-2026-24209, CVE-2026-24208) and an additional integer overflow (CVE-2026-24210) enable DoS. Given that PoC code for prior Triton CVEs was publicly released shortly after disclosure, patching CVE-2026-24207 should be treated as critical priority — particularly for exposed inference endpoints. [[Cyber Security News](https://cyberpress.org/nvidia-triton-server-flaw/); [GBHackers](https://gbhackers.com/nvidia-triton-inference-server-flaw-raises-risk-of-unauthorized-access/)]

**[NEW] ExifTool CVE-2026-3102 — macOS Command Injection via Image Metadata**

Kaspersky GReAT disclosed CVE-2026-3102, a command injection vulnerability in ExifTool (≤13.49) allowing attackers to execute arbitrary shell commands on macOS by crafting malicious image metadata. The flaw exploits unsanitized date values passed to a `system()` call when the `-n` flag bypasses formatting validation. Fixed in version 13.50 which switches to argument-based system calls. Particularly dangerous for automated image processing pipelines and digital asset management systems. [[GBHackers](https://gbhackers.com/exiftool-vulnerability-2/); [Cyber Security News](https://cyberpress.org/exiftool-flaw-compromise-mac/)]

---

## 🛡️ Defense & Detection

**[NEW] GhostTree Attack Causes EDR Tools to Hang via Malicious NTFS Junctions**

Varonis Threat Labs disclosed GhostTree, an attack technique abusing NTFS junctions to create recursive directory structures that cause security tools to hang indefinitely while scanning. By creating loops where child directories point back to parents, GhostTree generates a combinatorial path explosion — up to 2¹²⁶¹²⁶ theoretical valid paths to the same file. Two variants: GhostBranch (linear recursion) and GhostTree (multi-branch recursion). The technique was confirmed to interfere with Microsoft Defender's scanning capabilities. Since creating junctions doesn't require admin privileges, any user with write access can deploy this evasion. Mitigations include monitoring abnormal junction creation, detecting recursive directory structures, and implementing behavioral analysis. Microsoft has addressed the issue with a patch. [[GBHackers](https://gbhackers.com/new-ghosttree-attack-causes-edr-tools/)]

**[NEW] Gremlin Stealer Evolves: Encrypted .NET Resources Hide C2, Disk-to-Memory Execution**

Palo Alto Unit 42 documented a new Gremlin stealer variant using XOR-encrypted payloads hidden in .NET resource sections, protected by commercial packing with instruction virtualization. The malware targets browser credentials, session tokens, cryptocurrency wallets, clipboard data, and VPN/FTP credentials. New features include Discord token extraction, clipboard hijacking (crypto clipper), and WebSocket-based session hijacking. The XOR-obfuscated C2 endpoint at `194.87.92[.]109` showed zero detections on VirusTotal at discovery. The shift toward encrypted resource execution and staged loading marks Gremlin's evolution toward evasion-as-a-feature. [[GBHackers](https://gbhackers.com/gremlin-stealer-hides-c2/)]

---

## 📋 Policy & Industry News

**[UPDATE] CISA Credential Leak — House Homeland Dems Demand Briefing, Contractor Blamed**

House Homeland Security Committee Ranking Member Bennie Thompson (D-MS) and Rep. Delia Ramirez (D-IL) sent a formal letter to CISA Acting Director Nick Andersen demanding a briefing on the Nightwing contractor leak exposing AWS GovCloud keys on a public GitHub repository. The letter states the leak created "the conditions that allowed such a significant security lapse to occur" and raises concerns that workforce cuts (one-third of CISA staff lost since January) may have been a contributing factor. Sen. Maggie Hassan (D-NH) sent a separate letter. The repository, maintained by a Nightwing contractor, was public since November 2025 and included authentication credentials, AWS GovCloud information, and internal deployment documentation. [[Nextgov/FCW](https://www.nextgov.com/); [Malware.News](https://malware.news/t/house-homeland-dems-request-cisa-briefing-amid-report-of-leaked-agency-credentials/107170#post_1)]

**[NEW] Verizon DBIR 2026: Vulnerability Exploitation Overtakes Credential Theft as #1 Breach Vector**

The annual Verizon Data Breach Investigations Report analyzed 31,000 incidents and 22,000 confirmed breaches (nearly double 2024's count). Key findings: vulnerability exploitation has overtaken credential theft as the top breach vector for the first time; ransomware appears in 48% of breaches; median patching time increased to 43 days; only 26% of CISA KEV-listed flaws were patched in time. [[TLDR InfoSec](https://tldr.tech/infosec/2026-05-20)]

---

## ⚡ Quick Hits

- **WantToCry Ransomware:** New operation exploits exposed SMB ports (139/445) for remote file encryption — no local malware dropped, making EDR detection difficult. Ransoms range $400-$1,800. No double extortion observed. [[Cyber Security News](https://cyberpress.org/wanttocry-exploits-smb-remotely/); [GBHackers](https://gbhackers.com/wanttocry-ransomware-exploits-smb/)]

- **BadIIS Malware MaaS Evolution:** Chinese-speaking cybercrime groups operate a commercial IIS hijacking malware with PDB artifacts mapping development from September 2021 through January 2026. Builder tool offers traffic redirection, SEO manipulation, and content hijacking. [[Cyber Security News](https://cyberpress.org/badiis-abuses-iis-redirection/); [GBHackers](https://gbhackers.com/badiis-malware-hijacks-iis/)]

- **GraphWorm/Webworm APT:** China-aligned APT Webworm uses Microsoft OneDrive Graph API for stealth C2, with AES-256-CBC encrypted communication. Targets European governments. Also uses Discord-based EchoCreep backdoor. [[GBHackers](https://gbhackers.com/graphworm-malware-abuses-microsoft-onedrive/)]

- **First VPN Cybercriminal Takedown:** Europol-led operation dismantled "First VPN," a service deeply embedded in ransomware infrastructure, appearing in almost every major Europol-supported cybercrime investigation. [[Malware.News](https://malware.news/t/cybercriminal-vpn-used-by-ransomware-actors-dismantled-in-global-crackdown/107187#post_1)]

- **Fake Invitation Phishing:** Large-scale campaign targets US organizations with event-themed lures, CAPTCHA verification, credential harvesting, and RMM tool abuse (ScreenConnect, Datto RMM). Nearly 160 suspicious links and ~80 phishing domains identified. [[GBHackers](https://gbhackers.com/fake-invitation-phishing-campaign/)]

- **SEO Poisoning Impersonates Gemini + Claude Code:** EclecticIQ identified infostealer campaigns using typosquatted domains and SEO poisoning to deliver in-memory PowerShell infostealers targeting developer workstations. [[Malware.News](https://malware.news/t/seo-poisoning-campaign-leverages-gemini-and-claude-code-impersonation-to-deliver-infostealer/107188#post_1)]

- **Ukraine Identifies 18-Year-Old Infostealer Operator:** Ukrainian cyberpolice identified an 18-year-old from Odesa tied to 28,000 stolen accounts and $721,000 in fraudulent purchases from a California online store. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ukraine-identifies-infostealer-operator-tied-to-28-000-stolen-accounts/)]

- **Apache HTTP Server RCE (CVE-2026-23918):** Double-free in mod_http2 (HTTP/2), CVSS 8.8, affects Apache 2.4.66, fixed in 2.4.67. PoC exists for both DoS and code execution. [[r/cybersecurity](https://www.reddit.com/r/cybersecurity/)]

- **Android ADB Auth Bypass (CVE-2026-0073):** `EVP_PKEY_cmp()` type confusion in `adbd` enables zero-click RCE over local network on devices with wireless ADB enabled. CVSS 8.8, fixed in May 2026 Android Security Bulletin. PoCs released. [[r/cybersecurity](https://www.reddit.com/r/cybersecurity/)]

- **Microsoft Edge Cleartext Passwords Fix:** Microsoft reversed its "by design" stance and will stop Edge from loading all saved passwords into process memory at startup. Fix rolling to all channels (build 148+). [[r/cybersecurity](https://www.reddit.com/r/cybersecurity/) (486↑)]

---

*93 articles ingested from Miniflux Cyber feeds, supplemented by TLDR InfoSec (May 20 issue), Reddit r/cybersecurity hot, and targeted web searches for cross-reference gap stories. Prior digests: May 16-20, 2026. Sources include BleepingComputer, Qualys TRU, Cisco Talos, Cyber Security News, GBHackers, SecurityWeek, CyberScoop, Varonis, Palo Alto Unit 42, Malware.News, Kaspersky GReAT, DigiCert Incident Report, TLDR InfoSec, and ReliaQuest.*
