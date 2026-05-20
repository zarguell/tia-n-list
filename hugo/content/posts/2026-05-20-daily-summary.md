---
title: "🔴 GitHub 3.8K Repos Breached, 💀 Shai-Hulud Hits 600+ Packages, ⚠️ YellowKey Mitigated, 🛡️ ChromaDB Max-Severity, 🎯 Fox Tempest Disrupted, 🔐 CISA Leak"
date: 2026-05-20
tags: ["GitHub", "Supply Chain", "Shai-Hulud", "TeamPCP", "YellowKey", "ChromaDB", "NGINX", "CISA", "Fox Tempest", "DirtyDecrypt", "FreePBX", "Android Malware", "Void Botnet", "Storm-2949", "7-Eleven"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "GitHub confirms 3,800 internal repos breached via malicious VS Code extension; new Shai-Hulud wave compromises 639 npm packages in one hour; Microsoft issues YellowKey (CVE-2026-45585) mitigations for BitLocker zero-day; max-severity ChromaDB flaw (CVE-2026-45829) remains unpatched with 73% of exposed instances vulnerable; Microsoft disrupts Fox Tempest malware-signing service; CISA credential leak triggers congressional demands for answers."
---
# Daily Threat Intelligence Digest — May 20, 2026

*97 articles ingested from Miniflux Cyber feeds. External cross-referencing via TLDR InfoSec API (Tuesday May 19 issue) and Reddit r/cybersecurity hot.*

---

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] GitHub Confirms 3,800 Internal Repos Breached via Malicious VS Code Extension — TeamPCP Claims Responsibility**

GitHub has confirmed that approximately 3,800 internal repositories were breached after an employee installed a trojanized VS Code extension. The attack was detected and contained by GitHub's security team, who removed the unnamed malicious extension from the marketplace and isolated the compromised endpoint. The TeamPCP hacker group is claiming responsibility and advertising the stolen data (reported as "~4,000 repos of private code") on the Breached cybercrime forum with a minimum asking price of $50,000. The company's assessment confirms the attacker's claims of ~3,800 repositories are "directionally consistent." No customer data from outside the affected repos is believed to have been compromised. TeamPCP is the same group behind the ongoing Mini Shai-Hulud supply chain campaign that previously impacted two OpenAI employees via compromised TanStack packages. Last year, malicious VS Code extensions with 9 million installs were pulled for security risks, and in January, two AI-based coding assistant extensions with 1.5 million installs exfiltrated data from developer systems. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/github-confirms-breach-of-3-800-repos-via-malicious-vscode-extension/); [Cyber Security News](https://cyberpress.org/github-source-code-breach-claimed/); [GBHackers](https://gbhackers.com/github-source-code-reportedly-compromised/)]

**[UPDATE] Microsoft Issues YellowKey (CVE-2026-45585) Mitigations for Windows BitLocker Zero-Day**

Microsoft has formally tracked the YellowKey BitLocker bypass vulnerability as CVE-2026-45585 and published mitigation guidance pending a permanent security update. The zero-day, disclosed last week by researcher "Nightmare Eclipse," exploits specially crafted FsTx files placed on a USB drive or EFI partition, triggered by rebooting into WinRE with the CTRL key held down. Microsoft's recommended mitigations: (1) remove the `autofstx.exe` entry from Session Manager's BootExecute registry value, (2) reestablish BitLocker trust for WinRE, and (3) configure encrypted devices from "TPM-only" to "TPM+PIN" mode via PowerShell, Intune, or Group Policy — requiring a pre-boot PIN to decrypt the drive at startup. Nightmare Eclipse previously disclosed BlueHammer (CVE-2026-33825), RedSun, GreenPlasma, and UnDefend zero-days, several of which are now being actively exploited. [[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-shares-mitigation-for-yellowkey-windows-zero-day/)]

**[UPDATE] Shai-Hulud Returns: 639 Malicious npm Packages Published in One-Hour Worm Attack**

A new wave of the Shai-Hulud supply chain campaign published 639 malicious versions across 323 unique npm packages in approximately one hour on May 19 (01:56–02:56 UTC). The attack began by compromising the `@antv` ecosystem maintainer account (atool), then spread to adjacent packages including `echarts-for-react`, `@antv/g2`, `@antv/g6`, `@antv/x6`, `timeago.js`, `size-sensor`, and `jest-canvas-mock` — the latter dormant for three years with 10M monthly downloads. This variant introduces several new capabilities: valid Sigstore provenance attestation via abused OIDC tokens (making malicious packages appear legitimately signed); persistence through backdoors planted in VS Code and Claude Code configurations; and data exfiltration over the Session P2P network (TCP/443, indistinguishable from legitimate Session app traffic). Stolen data targets GitHub, npm, cloud, Kubernetes, Vault, Docker, database, and SSH credentials. When GitHub tokens are available, the malware auto-creates repos under victim accounts to store stolen data — BleepingComputer found ~2,900 such repos at the time of reporting. Aikido Security warns the persistence mechanism suggests the attacker is "thinking about what happens after the initial compromise gets cleaned up." The Shai-Hulud source code leak by TeamPCP makes attribution of individual waves increasingly difficult. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/new-shai-hulud-malware-wave-compromises-600-npm-packages/); [Cyber Security News](https://cyberpress.org/600-npm-packages-hit/); [CyberScoop](https://cyberscoop.com/mini-shai-hulud-malware-npm-packages-compromised-again/)]

---

## 🎯 Threat Actor Activity & Campaigns

**[UPDATE] CISA Credential Leak Triggers Congressional Demands — State Actor Persistence Feared**

Congressional Democrats are demanding answers from CISA following the discovery of a public GitHub repository named "Private-CISA" that exposed highly privileged AWS GovCloud administrative credentials, plaintext passwords for internal systems, and CI/CD access tokens. Rep. Bennie Thompson (D-MS) and Sen. Maggie Hassan (D-NH) sent separate letters to CISA Acting Director Nick Andersen seeking briefings on how the leak occurred, forensic analysis of potential damage, and corrective actions. GitGuardian researcher Guillaume Valadon — who discovered the leak — expressed particular concern about state actors potentially gaining persistence. The repository, maintained by a Nightwing contractor, had been public since November 2025. CISA stated there is currently no indication that any sensitive data was compromised, but security professionals note the artifact repository access vector is especially dangerous. The incident has renewed focus on CISA's workforce attrition (one-third of staff lost since January) and the broader pattern of GitHub misconfiguration exposures. [[CyberScoop](https://cyberscoop.com/cisa-credential-leak-congress-demands-answers/)]

**[UPDATE] Microsoft Disrupts Fox Tempest — Malware-Signing-as-a-Service for Ransomware Gangs**

Microsoft's Digital Crimes Unit has detailed the takedown of Fox Tempest, a malware-signing-as-a-service operation that fabricated identities to abuse Microsoft's Artifact Signing platform. The operation created and sold more than 1,000 fraudulent code-signing certificates to ransomware affiliates for up to $9,500 per batch, enabling malicious binaries to pass Windows SmartScreen, AppLocker, and antivirus checks. Fox Tempest's service was linked to Rhysida, Vanilla Tempest, Storm-0501, Qilin, Akira, and INC ransomware, and dozens of malware families including Oyster, Lumma Stealer, MuddyWater, and Vidar. Microsoft evicted or deleted more than 1,000 accounts and subscriptions, seized the group's website, took hundreds of VMs offline, and blocked access to the underlying code repository. The takedown is a disruption rather than permanent removal. [[CyberScoop](https://cyberscoop.com/microsoft-digital-crimes-unit-disrupts-fox-tempest/); [BleepingComputer](https://www.bleepingcomputer.com/news/security/cybercrime-service-disrupted-for-abusing-microsoft-platform-to-sign-malware/)]

**[NEW] Void Botnet Leverages Ethereum Smart Contracts for Seizure-Resistant C2 Infrastructure**

A new Rust-native botnet is using Ethereum smart contracts to maintain a command-and-control network with no centralized server to seize. Discovered in March 2026, infected machines poll public Ethereum RPC endpoints every 3–5 minutes for task retrieval. Developed by threat actor "TheVoidStl," the botnet offers dual-mode operation: primary decentralized C2 via smart contracts with a speed-optimized direct web panel fallback. Priced at $600 ($50/build fee), it provides 14 task types including reflective code loading and reverse shells. This is the second blockchain-based botnet observed in as many months, signaling a growing trend toward decentralized, takedown-resistant C2 infrastructure. [[Cyber Security News](https://cyberpress.org/void-botnet-ethereum-c2/); [GBHackers](https://gbhackers.com/void-botnet-leverages-ethereum/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] ChromaDB CVE-2026-45829 (CVSS 10) — Max-Severity Unpatched Flaw Enables Server Hijacking**

A maximum-severity vulnerability in ChromaDB (14M monthly PyPI downloads) allows unauthenticated attackers to run arbitrary code on exposed servers. Reported to the maintainer on February 17, CVE-2026-45829 exploits an authentication-ordering flaw: a vulnerable API endpoint allows attackers to embed model settings before the authentication check fires, forcing ChromaDB to load a malicious model from Hugging Face and execute it locally. HiddenLayer researchers have been unable to contact the maintainer — 73% of internet-exposed instances run a vulnerable version per Shodan. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/max-severity-flaw-in-chromadb-for-ai-apps-allows-server-hijacking/)]

**[NEW] NGINX CVE-2026-8711 (CVSS 9.2) — Critical RCE in JavaScript Module**

A critical heap buffer overflow in NGINX JavaScript (njs) versions 0.9.4–0.9.8 allows unauthenticated remote attackers to achieve RCE when ASLR is disabled. The vulnerability exists in `ngx_http_js_module` and is triggered when `js_fetch_proxy` is configured with client-controlled variables. Fixed in njs 0.9.9. Distinct from the actively exploited NGINX Rift (CVE-2026-42945). [[Cyber Security News](https://cyberpress.org/nginx-allows-remote-code-execution/)]

**[UPDATE] DirtyDecrypt (CVE-2026-31635) PoC Released — Fourth Dirty-Frag-Class Linux Kernel LPE**

A working proof-of-concept exploit for DirtyDecrypt has been publicly released, targeting a missing copy-on-write guard in the Linux kernel's `rxgk_decrypt_skb()` function. Confirmed working on Fedora and mainline kernels; Arch Linux and openSUSE Tumbleweed also vulnerable. Stable enterprise distributions (Debian, Ubuntu LTS, RHEL 8/9) are not affected under standard configurations. The same module blacklist mitigation protecting against Dirty Frag and Fragnesia also covers DirtyDecrypt. [[Cyber Security News](https://cyberpress.org/poc-code-dirtydecrypt-linux-kernel/)]

**[NEW] FreePBX CVE-2026-46376 (CVSS 9.1) — Hard-Coded Credentials Exposed Since 2021**

A critical vulnerability in FreePBX's `userman` module carries hard-coded default credentials in the optional UCP generic template setup process, silently exposing systems since 2021. CVE-2026-46376 affects FreePBX 16 (<16.0.45) and 17 (<17.0.7). Exploitation requires no privileges, no user interaction, and no complex attack chain — any unauthenticated user on the network can gain portal access. Patched versions randomize all default passwords. [[Cyber Security News](https://cyberpress.org/freepbx-flaw-exposes-user-portals/)]

---

## 🛡️ Defense & Detection

**[NEW] VoidStealer Bypasses Chrome App-Bound Encryption via Debugger Hardware Breakpoints**

VoidStealer v2.0 introduces the first in-the-wild bypass of Chrome's App-Bound Encryption using a debugger-based technique. It spawns a hidden browser process, attaches as a debugger, and uses hardware breakpoints (DR0/DR7 registers) to capture the plaintext `v20_master_key` during startup decryption. No elevated privileges or code injection required. Adapted from the open-source ChromeKatz toolset. Defenders should monitor for `DebugActiveProcess` calls against browser processes. [[Cyber Security News](https://cyberpress.org/voidstealer-bypasses-chrome-protection/)]

**[NEW] Trapdoor Android Ad Fraud: 455 Apps, 659M Daily Bid Requests**

The "Trapdoor" campaign encompasses 455 malicious Android applications and 183 C2 domains, generating up to 659 million bid requests per day. Applications accumulated 24M+ downloads from Google Play. Uses two-stage distribution: initial clean utility apps from Play Store followed by targeted malvertising to deploy secondary weaponized payloads. Anti-analysis measures include root detection, VPN checks, native packing, and code virtualization. [[Cyber Security News](https://cyberpress.org/trapdoor-android-click-fraud/)]

**[NEW] Single-Letter Go Module Typosquat Operated 6 Years Before Dropping DNS Backdoor**

A Go typosquat (`shopsprint/decimal` vs `shopspring/decimal`) mirrored legitimate upstream updates for ~6 years before version v1.3.3 (August 2023) introduced a C2 loop using DNS TXT record polling. The malicious `init()` function executes automatically on import. The Go Module Proxy permanently caches the poisoned version. [[Cyber Security News](https://cyberpress.org/go-typosquat-spreads-backdoor/)]

---

## 📋 Policy & Industry News

**[NEW] NYC Health + Hospitals Breach: 1.8M Patients, Fingerprints and Biometric Data Exposed**

NYC Health + Hospitals disclosed a data breach affecting 1.8M individuals. Attackers accessed systems from November 2025 to February 2026 via a compromised third-party vendor. Stolen data includes medical records, SSNs, and biometric data (fingerprints, palm prints) — distinguishing this as one of the largest healthcare data breaches of 2026. [[TLDR InfoSec](https://tldr.tech/infosec/2026-05-19); [NYC Health + Hospitals](https://www.nychealthandhospitals.org/pressrelease/notice-of-data-breach/)]

**[NEW] INTERPOL Operation Ramz: 201 Arrests Across 13 MENA Nations**

INTERPOL's first large-scale MENA cybercrime operation concluded with 201 arrests, 53 servers seized, and 382 suspects identified across 13 countries. Targeted phishing infrastructure, malware networks, and financial fraud schemes. [[Cyber Security News](https://cyberpress.org/operation-ramz-seizes-53-servers/)]

---

## ⚡ Quick Hits

- **7-Eleven confirms breach, ShinyHunters leaks 9.4GB:** 86,000+ stores affected; 600K+ Salesforce records leaked after refused ransom. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/7-eleven-confirms-data-breach-claimed-by-the-shinyhunters-gang/)]
- **DevilNFC Android malware:** Uses kiosk mode for NFC relay attacks on banking customers. AI-assisted development observed. [[GBHackers](https://gbhackers.com/devilnfc-malware-traps-android-users/)]
- **UAC-0184 targets Ukrainian military:** Multi-stage Bitsadmin/HTA chain with DLL sideloading via VSLauncher.exe and PassMark Endpoint. [[GBHackers](https://gbhackers.com/uac-0184-uses-bitsadmin/)]
- **Storm-2949 SSPR abuse:** Full attack chain published — abused Azure SSPR, Graph API, Key Vault, and VM extensions for data theft. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/microsoft-self-service-password-reset-abused-in-azure-data-theft-attacks/)]
- **MSHTA abuse resurgence:** LummaStealer and Amatera delivered via CountLoader and Emmenhtal Loader through ClickFix tactics. [[Cyber Security News](https://cyberpress.org/mshta-abuse-delivers-malware/)]

---

*97 articles ingested from Miniflux Cyber feeds, supplemented by TLDR InfoSec (May 19 issue) and Reddit r/cybersecurity cross-referencing. Prior digests: May 15-19, 2026. Sources include BleepingComputer, CyberScoop, SecurityWeek, Cyber Security News, GBHackers, TLDR InfoSec, Kaspersky, Bitdefender, Qrator, Cleafy, Synaptisc, Socket, Endor Labs, HiddenLayer, Zellic/V12, and Microsoft Threat Intelligence.*
