---
title: TeamPCP PyPI attacks 🔄, HackerOne breach 📊, PureHVNC RAT 🐀, Russian GRU 🇷🇺, malicious npm packages 📦
date: 2026-03-25
tags: ["supply chain attacks","teampcp","data breach","rat","apt activity","social engineering","npm registry","credential theft","cryptocurrency","phishing"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: TeamPCP continues supply chain attacks by compromising the LiteLLM PyPI package to harvest cloud credentials and tokens from millions of users while malicious npm packages steal cryptocurrency private keys from developers. Russian GRU's Sandworm unit targets Signal and WhatsApp accounts through social engineering, PureHVNC RAT distribution exploits trusted Google Forms, and a third-party breach exposes HackerOne staff data to potential phishing attacks.
---
# Daily Threat Intel Digest - 2026-03-25

## 🔴 Critical Threats & Active Exploitation

**[UPDATE] TeamPCP compromises LiteLLM PyPI package in ongoing supply chain spree**
Expanding on their recent attacks against Aqua Security's Trivy and Checkmarx, the TeamPCP threat actor has compromised the `litellm` Python package—a library with over 95 million monthly downloads. Malicious versions 1.82.7 and 1.82.8 contain multi-stage payloads designed to harvest cloud credentials (AWS, Azure, GCP), SSH keys, and Kubernetes tokens, exfiltrating them to attacker-controlled infrastructure including `models.litellm.cloud`. Users must immediately downgrade to version 1.82.6 and rotate all credentials exposed in environments where the affected versions ran [[GBHackers](https://gbhackers.com/compromised-litellm-package-with-95m-downloads/); [Cyberpress](https://cyberpress.org/teampcp-litellm-package/); [Malware.news](https://malware.news/t/malicious-pypi-package-litellm-supply-chain-compromise/105356#post_1)].

**[NEW] HackerOne employee data exposed in Navia third-party breach**
A breach of third-party benefits provider Navia has exposed the personal data of 287 HackerOne employees, including names and identifiers, following unauthorized access between December 22, 2025, and January 15, 2026. While HackerOne's bug bounty platform remained untouched, the incident highlights the risks of vendor-managed data supply chains. The stolen PII creates a high probability of targeted phishing attacks against security researchers and staff, necessitating heightened vigilance for social engineering attempts leveraging these details [[SecurityWeek](https://www.securityweek.com/hackerone-employee-data-exposed-in-massive-navia-breach/); [Cyberpress](https://cyberpress.org/hackerone-data-breach/); [GBHackers](https://gbhackers.com/hackerone-confirms-employee-data-stolen/)].

## 🎯 Threat Actor Activity & Campaigns

**[NEW] PureHVNC RAT distributed via trusted Google Forms**
Attackers are bypassing traditional email filters by using fraudulent Google Forms—impersonating job interviews and project summaries—to distribute the PureHVNC Remote Access Trojan. By exploiting the inherent trust of domains like `docs.google.com`, the campaign tricks professionals into downloading archives containing malicious loaders that use DLL sideloading to deploy the RAT. PureHVNC establishes deep persistence and systematically steals sensitive data from web browsers, cryptocurrency wallets, and messaging apps [[Cyberpress](https://cyberpress.org/google-forms-spreads-purehvnc/)].

**[NEW] SILENTCONNECT campaign delivers ScreenConnect RAT with stealth loaders**
Elastic Security Labs identified a new campaign using a custom loader, "SILENTCONNECT," to deliver the legitimate ScreenConnect RMM tool for malicious purposes. The attack chain begins with fake Cloudflare Turnstile CAPTCHA pages and uses a VBScript downloader to fetch a C# payload compiled in-memory via PowerShell. Notably, the malware employs Process Environment Block (PEB) masquerading to impersonate `winhlp32.exe`, effectively blinding EDR solutions that rely on trusted process names [[Cyberpress](https://cyberpress.org/silentconnect-delivers-screenconnect-rat/)].

**[NEW] Russian GRU unit targets Signal and WhatsApp via social engineering**
Dutch intelligence (AIVD) has warned that Russian APT group Sandworm (GRU Unit 74455) is actively conducting cyber espionage against government employees and journalists. Rather than exploiting app vulnerabilities, the actors use social engineering—masquerading as Signal support bots or abusing "linked devices" features—to hijack user accounts. Organizations must alert staff to verify all unsolicited contact requests and never share verification codes or SMS codes with third parties [[Malware.news](https://malware.news/t/dutch-intelligence-warns-of-russian-campaign-against-signal-and-whatsapp-users/105355#post_1)].

**[NEW] Malicious npm packages exfiltrate crypto keys via Telegram**
Five typosquatting packages on the npm registry are actively targeting Solana and Ethereum developers by stealing wallet private keys. The packages, which impersonate popular crypto libraries, send stolen keys directly to a Telegram bot-based command-and-control channel. This campaign highlights the persistent risk of dependency confusion in software supply chains, requiring developers to strictly audit package sources and names before installation [[GBHackers](https://gbhackers.com/five-malicious-npm-packages/)].

**[NEW] "TroyDen’s Lure Factory" pushes trojanized GitHub repos**
A large-scale malware operation tracked as "TroyDen’s Lure Factory" is abusing GitHub to deliver a custom LuaJIT-based trojan to developers and gamers. The campaign spans over 300 delivery packages and uses AI-assisted lures ranging from OpenClaw deployment tools to game cheats and Roblox scripts to trick users into executing malicious code [[GBHackers](https://gbhackers.com/ai-driven-openclaw/)].

## 📋 Policy & Industry News

**[NEW] FCC bans new foreign consumer routers over national security risks**
The U.S. Federal Communications Commission (FCC) has officially updated its "Covered List" to prohibit the authorization of new consumer-grade routers manufactured by certain foreign vendors. Citing severe cybersecurity risks and the potential for espionage—linked to campaigns like Volt Typhoon—this regulatory shift effectively blocks these devices from the U.S. market. Security teams must immediately update procurement policies to ensure new network edge devices comply with these restrictions [[Cyberpress](https://cyberpress.org/fcc-blocks-new-consumer-routers/); [GBHackers](https://gbhackers.com/fcc-blocks-new-consumer-router-models/)].

**[NEW] Azure AI Foundry strengthens security with model scanning safeguards**
Microsoft has announced new defensive capabilities for Azure AI Foundry and Azure OpenAI Service to address supply chain risks in generative AI. The platform now includes proactive vulnerability scanning, malware analysis, and integrity validation for third-party models before they reach the catalog. These updates treat all model inputs and outputs as secure customer content, ensuring strict tenant isolation and zero-trust architecture for AI workloads [[Cyberpress](https://cyberpress.org/azure-ai-enhances-generative-security/)].

## ⚡ Quick Hits

*   **Tooling Update:** Offensive Security released Kali Linux 2026.1, featuring 8 new tools (AdaptixC2, Atomic-Operator, SSTImap) and a nostalgic "BackTrack Mode" to celebrate the 20th anniversary of its predecessor [[Cyberpress](https://cyberpress.org/kali-linux-2026-1-released-featuring-8-new-security-tools/); [GBHackers](https://gbhackers.com/kali-linux-2026-1-launches-with-8-new-hacking-tools/)].
*   **Design Flaw:** Research indicates Google Authenticator's passkey design relies heavily on a cloud-side component, potentially exposing new attack vectors if the cloud trust anchor or recovery mechanisms are compromised [[GBHackers](https://gbhackers.com/google-authenticators-passkey/)].