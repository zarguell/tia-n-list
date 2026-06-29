---
title: "🚨 YellowKey BitLocker Bypass, 7-Eleven Breach, 7-Zip RCE, Dragon Whistle, Angular Extension RCE"
date: 2026-05-26
tags: ["YellowKey","BitLocker","CVE-2026-45585","ShinyHunters","7-Eleven","7-Zip","CVE-2026-48095","Angular","VS Code","Operation Dragon Whistle","Cloud Atlas","UAC-0057","Ransomware","CERT-UA","Threat Intelligence"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "YellowKey BitLocker zero-day bypasses Windows 11 encryption with a USB stick — no patch, mitigation only. ShinyHunters breaches 7-Eleven, leaking 185K records. Critical 7-Zip heap overflow enables RCE from crafted archives. Operation Dragon Whistle targets Chinese university with Cobalt Strike. Cloud Atlas modifies termsrv.dll for covert RDP. Angular VS Code extension RCE disclosed."
---

# Daily Threat Intelligence Digest — May 26, 2026

*64 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[GAP] YellowKey (CVE-2026-45585) — Unpatched BitLocker Zero-Day Bypasses Windows 11 Encryption with a USB Stick — No Patch, Manual Mitigation Only**

A researcher operating as Chaotic Eclipse (Nightmare-Eclipse) has publicly released a working proof-of-concept exploit for a BitLocker security feature bypass on Windows 11 and Windows Server 2022/2025 that grants unrestricted access to encrypted drives using nothing more than a USB stick. The exploit, dubbed YellowKey (CVE-2026-45585, CVSS 6.8), involves copying a crafted `FsTx` folder into `System Volume Information` on a USB drive, rebooting into the Windows Recovery Environment (WinRE), and holding the CTRL key — which spawns an elevated command prompt with the drive already transparently decrypted by the TPM.

Multiple independent researchers, including **Kevin Beaumont** and **Will Dormann (Tharros Labs)**, have confirmed the exploit works as described. Dormann noted that the underlying mechanism exploits Transactional NTFS replay across volumes — a USB drive's NTFS transaction logs can delete `winpeshl.ini` on the recovery partition, causing WinRE to drop to `cmd.exe` instead of the locked-down recovery UI. The researcher claims TPM+PIN protection does not fully mitigate the issue (though the PIN-defeating PoC has not been released).

Microsoft has acknowledged the vulnerability and released **manual mitigation guidance** — not a patch. The mitigation involves mounting the WinRE image on each device, removing `autofstx.exe` from the BootExecute registry value, and re-establishing BitLocker trust. Organizations should also enable TPM+PIN and BIOS passwords as additional layers. This is the third zero-day Chaotic Eclipse has dropped in as many months, following BlueHammer (CVE-2026-33825, LPE, exploited in the wild) and RedSun. The exploit files self-delete after execution. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/windows-bitlocker-zero-day-gives-access-to-protected-drives-poc-released/); [Ars Technica](https://arstechnica.com/security/2026/05/zero-day-exploit-completely-defeats-default-windows-11-bitlocker-protections/); [SecurityWeek](https://www.securityweek.com/microsoft-rolls-out-mitigations-for-yellowkey-bitlocker-bypass/); [r/cybersecurity](https://old.reddit.com/r/cybersecurity/new/) — 1268↑]

**[NEW] 7-Eleven Breach — ShinyHunters Steals 185K Records from Salesforce Environment, Leaks 9.4GB**

The ShinyHunters extortion gang breached 7-Eleven's systems in early April 2026, stealing over 600,000 records (9.4GB) of franchisee documents from the company's Salesforce environment. Have I Been Pwned confirmed the exposure of **185,300 unique individuals' data**, including names, email addresses, phone numbers, physical addresses, and dates of birth. 7-Eleven disclosed the breach to affected customers on May 1, and ShinyHunters leaked the archive on their dark web leak site after the company refused to pay the ransom.

ShinyHunters has been systematically targeting Salesforce customers over the past year in what's been dubbed the "Salesforce Aura" campaign, claiming billions of records across hundreds of breaches including the European Commission, Vimeo, Zara, McGraw-Hill, ADT, PornHub, and Rockstar Games. The FBI has advised victims not to pay demands. 7-Eleven operates 86,000+ stores globally with 100M+ loyalty members. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/7-eleven-data-breach-exposes-personal-information-of-185-000-people/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Operation Dragon Whistle — UNG0002 Targets Chinese University with Cobalt Strike via Fitness-Testing Lure**

Seqrite Labs uncovered a highly targeted spear-phishing campaign dubbed "Operation Dragon Whistle" targeting Changzhou University in China. The attackers, identified with medium-high confidence as the **UNG0002 group**, exploit the mandatory 2026 fitness testing cycle as a social engineering lure — creating a severe sense of urgency since failing the assessment impacts graduation. The attackers demonstrate deep institutional knowledge, using real staff names, phone numbers, and official seals in decoy documents.

The infection chain uses a ZIP attachment containing a double-extension LNK file disguised as a PDF, which triggers a VBScript that weaponizes the legitimate **Bandizip archiving tool for DLL sideloading**. The malware checks for debugging tools and security environments before deploying a **Cobalt Strike Beacon entirely in memory**. Infrastructure is hosted on Alibaba Cloud with rotated hosting providers to evade ASN-based blocking. [[Cyber Security News](https://cyberpress.org/dragon-whistle-deploys-cobalt/); [GBHackers](https://gbhackers.com/pdf-lnk-files-deploy-cobalt-strike/)]

**[NEW] Cloud Atlas APT — Novel termsrv.dll Modification Enables Multiple RDP Sessions on Compromised Systems**

The Cloud Atlas APT group (active since 2014) has introduced a stealthy technique that modifies the Windows `termsrv.dll` library on compromised systems to enable multiple simultaneous RDP sessions. Observed throughout 2025 and continuing into 2026, the campaign primarily targets government and commercial entities in **Russia and Belarus**. The PowerShell script `rdp_new.ps1` takes ownership of the file, alters specific byte sequences, and restarts the RDP service — allowing attackers to maintain hidden concurrent access without disrupting legitimate users.

The group's broader toolset includes VBCloud (file-stealing implant), PowerShower (reconnaissance and Kerberoasting), PowerCloud (Google Sheets exfiltration), and modified OpenSSH binaries. Persistence uses reverse SSH tunnels, Tor hidden services, and RevSocks Go-based tunneling. [[GBHackers](https://gbhackers.com/apt-group-patches-termsrv-dll/)]

**[NEW] UAC-0057 (Ghostwriter) — Updated OYSTERFRESH/OYSTERSHUCK/OYSTERBLUES Malware Toolkit Targets Ukrainian State Organizations**

CERT-UA's May 21 advisory warns that the UAC-0057 threat cluster (aka Ghostwriter / UNC1151 / FrostyNeighbor) has updated its malware toolkit with a new OYSTER-branded family. The campaign, active since spring 2026, uses phishing emails sent from compromised employee accounts with lures about certificates from the Prometheus educational platform. The infection chain begins with a PDF containing a link to a ZIP archive with an OYSTERFRESH JavaScript file, which stores an encoded OYSTERBLUES payload in the Windows Registry and downloads OYSTERSHUCK as a decoder. Deobfuscation applies string reversal, ROT13, and URL decoding before executing arbitrary JavaScript via `eval`. The next stage commonly delivers Cobalt Strike. C2 infrastructure is masked behind Cloudflare with `.icu` zone domains. [[SOC Prime](https://socprime.com/blog/uac-0057-attack-detection/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Critical 7-Zip Heap Overflow (CVE-2026-48095) — NTFS Handler RCE via Crafted Archive, Fixed in 26.01**

GitHub Security Lab disclosed a critical heap buffer overflow in 7-Zip's NTFS archive handler (GHSL-2026-140 / CVE-2026-48095, CVSS 8.8) affecting all versions up to 26.00. The vulnerability stems from undefined behavior in a 32-bit shift computing the NTFS compression unit buffer size, allowing an attacker to force a 1-byte input buffer allocation and then write up to 256 MB of attacker-controlled data during decompression — overwriting a nearby stream object's vtable pointer for arbitrary code execution. The NTFS handler is auto-detected by signature, so any file extension with an NTFS signature can be routed to the vulnerable code path.

Eight additional memory safety issues (GHSL-2026-115–122) affect SquashFS (integer overflow, heap leak), UEFI capsules (up to 1 GiB heap leak), UDF, and WIM parsers. **Public PoC generators already exist** for several bugs. Fixed in 7-Zip 26.01 (April 27, 2026). Given 7-Zip's widespread deployment, administrators should prioritize patching — a crafted archive opened by any user on an affected system is sufficient for compromise. [[GBHackers](https://gbhackers.com/multiple-7-zip-vulnerabilities-arbitrary-code-execution/); [Cyber Security News](https://cyberpress.org/new-7-zip-vulnerabilities/)]

**[NEW] Angular Language Service VS Code Extension RCE — Two Attack Vectors, No CVE Assigned**

A high-severity vulnerability disclosed in the VS Code Angular Language Service extension (Angular.ng-template, versions before 21.2.4) allows attackers to execute arbitrary code on developer machines from a malicious project folder. Two independent attack vectors have been documented: (1) **JSDoc Hover Markdown Command Injection** — the extension configures VS Code's Markdown tooltip renderer with `isTrusted: true`, allowing embedded `command:` URIs in JSDoc comments to execute when a developer hovers over a symbol and clicks the tooltip link; (2) **Unsanitized tsdk Workspace Configuration** — the extension reads `typescript.tsdk` from `.vscode/settings.json` without Workspace Trust validation and passes it as a `--tsdk` argument to the language server, which dynamically loads `tsserverlibrary.js` from the attacker-controlled path at workspace initialization with zero user interaction.

Both vectors bypass VS Code's Workspace Trust boundary entirely. No CVE has been assigned. The disclosure follows the compromised Nx Console extension that breached 3,800 GitHub repos — underscoring the rapidly widening IDE supply chain attack surface. Organizations should immediately update to version 21.2.4 and audit all VS Code extensions across engineering endpoints. [[Cyber Security News](https://cyberpress.org/angular-language-service-flaws/)]

**[NEW] ConnectWise Automate CVE-2026-9089 (CVSS 8.8) — Plugin Integrity Verification Bypass Creates MSP Supply Chain Risk**

ConnectWise patched a high-severity vulnerability in ConnectWise Automate (RMM platform) where agent plugin loading and self-update processes may process components without full integrity checks before execution (CWE-494). The flaw requires no user interaction and has low attack complexity. While no active exploitation has been confirmed, RMM vulnerabilities are frequently weaponized for supply-chain-scale access. Cloud-hosted instances auto-updated; on-premises deployments must manually upgrade to Automate 2026.5. [[GBHackers](https://gbhackers.com/connectwise-automate-flaw/)]

---

## 📋 Policy & Industry News

**[NEW] Oncology Institute (TOI) Data Breach — Third-Party Vendor Incident via TriZetto/Cognizant Exposes Patient Data**

The Oncology Institute, a multi-state oncology provider with 100+ clinics, disclosed that a November 2025 breach at an unnamed third-party software vendor has now been confirmed to impact patient data. On May 20, Kroll (the vendor's third-party administrator) notified TOI that unauthorized access to TOI's information systems was detected. SecurityWeek identifies the vendor as **TriZetto Provider Solutions** (Cognizant-owned), which reported a separate breach affecting approximately 3.4 million individuals across multiple healthcare customers. Attribution remains unknown with no ransomware group claiming responsibility. [[SecurityWeek](https://www.securityweek.com/oncology-institute-discloses-third-party-data-breach/)]

**[NEW] PowerSchool Reaches $17.25M Settlement Over Multi-Year Student Data Tracking Practices**

PowerSchool agreed to a $17.25 million settlement related to a data tracking program dating back to 2021 — predating the widely-reported 2024 hacking incident affecting tens of millions of students. The settlement resolves claims over the education software provider's collection and sharing of student data without proper consent. [[Malware.News via DataBreaches.net](https://databreaches.net/2026/05/25/powerschools-17-25-million-settlement-exposes-years-of-student-data-tracking/)]

---

## ⚡ Quick Hits

- **DragonForce Ransomwave Hits 7 New Victims** — DragonForce listed BusinessRecord.com, Xchange Technology Rentals, Saver NV Waste Management, Goldklang Group CPAs, Enns & Company (Canadian accounting firm), and SPH Value on their leak site, continuing a wave targeting accounting, waste management, and business services sectors. [[Malware.News](https://malware.news/t/dragonforce-targets-businessrecord-com-in-ransomware-attack/107315)]
- **CISA ICS Advisories (AV26-506)** — Canadian Cyber Centre published ICS security advisories covering industrial control system vulnerabilities. Organizations with OT/ICS environments should review and patch accordingly. [[Malware.News](https://malware.news/t/control-systems-cisa-ics-security-advisories-av26-506/107304)]
- **Apache CXF CVE-2026-44930 — LDAP Injection** — Apache CXF framework vulnerability exposes systems to LDAP injection attacks. Details remain limited. [[GBHackers](https://gbhackers.com/apache-cxf-flaw-exposes-systems/)]
