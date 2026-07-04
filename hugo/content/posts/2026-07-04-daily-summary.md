---
title: "🎯 ARToken PhaaS, 🐛 LLM-Fuzzed Zero-Days, 🤖 Ollama/LiteLLM Vulns, 📧 KDDI Breach, 🎭 Poisoned Tenant Attack"
date: 2026-07-04
tags: ["artoken","eviltokens","phishing","microsoft-365","ollama","litellm","vulnerabilities","open-source","kddi","data-breach","influence-operations"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "ARToken PhaaS platform exposes EvilTokens' Microsoft 365 phishing toolkit; researcher publishes LLM-fuzzed zero-days across multiple open source projects; five Ollama and LiteLLM vulnerabilities disclosed via Huntr; KDDI data breach impacts 14.2 million email accounts."
---
*5 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.*

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] ARToken PhaaS Exposes EvilTokens' Microsoft 365 Phishing Toolkit with Advanced BEC Capabilities**

Cisco Talos discovered a new phishing-as-a-service platform dubbed ARToken that operates as an affiliate of the EvilTokens phishing ecosystem. The React-based management panel exposed more than 80 API endpoints during an incident response investigation, revealing capabilities far beyond standard phishing kits.

ARToken enables attackers to steal Microsoft 365 authentication tokens, establish persistent access using Primary Refresh Tokens (PRTs), and access Outlook mailboxes, SharePoint sites, and OneDrive files. The platform deploys phishing infrastructure through Cloudflare Workers and automates business email compromise (BEC) operations — including multi-mailbox keyword monitoring, automatic content localization based on victim geography, and AI-assisted mailbox scoring for financial exposure.

The platform uses device code authentication phishing (Microsoft's OAuth 2.0 Device Authorization Grant workflow) that bypasses MFA by tricking victims into entering a legitimate Microsoft-issued code on Microsoft's official login page — causing Microsoft to issue authentication tokens directly to the attacker. Multiple technical similarities strongly tie ARToken to the EvilTokens platform documented by Sekoia in March. Push Security recently reported a 37-fold surge in device code phishing attacks over the past year, with at least 11 phishing kits now offering this technique. [[BleepingComputer/Cisco Talos](https://www.bleepingcomputer.com/news/security/artoken-phaas-exposes-eviltokens-microsoft-365-phishing-toolkit/)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Researcher Publishes LLM-Fuzzed Zero-Days Across Multiple Open Source Projects**

A researcher known as Bikini published proof-of-concept exploit code targeting dozens of zero-day vulnerabilities in widely used open source projects, including FFmpeg, Gogs, Gitea, Ghidra, 7-Zip, OpenVPN, and VLC. Nine of the security defects have received CVE identifiers. The vulnerabilities were discovered through LLM-assisted fuzzing, demonstrating the rapidly accelerating capability of AI-augmented vulnerability discovery against foundational open source infrastructure. Organizations using any of the affected projects should monitor for vendor patches. [[SecurityWeek](https://www.securityweek.com/in-other-news-canadian-hacker-jailed-open-source-zero-days-two-sentenced-for-atm-jackpotting/)]

**[NEW] Five Vulnerabilities Disclosed in Ollama and LiteLLM via Huntr Program**

Independent security researcher Regaan published full technical details of five vulnerabilities reported through Huntr's 90-day coordinated disclosure program. In Ollama, two denial-of-service issues were identified: a GGUF String Length Panic and an unbounded vocab_size resource exhaustion flaw causing excessive memory and CPU consumption. In LiteLLM, the findings include a Pass-the-Hash authentication bypass, server-side request forgery (SSRF) through custom guardrails, and a Unicode normalization issue enabling sandbox escape scenarios. The disclosures highlight recurring security gaps in AI infrastructure — particularly around model parsing pipelines, authentication logic, and trust boundary handling. [[GitHub](https://github.com/regaan/ollama-security-research); [GitHub](https://github.com/regaan/litellm-vulnerability-research)]

---

## ⚡ Quick Hits

- **KDDI Data Breach Impacts 14.2 Million Email Accounts** — Japanese telecommunications giant KDDI disclosed unauthorized access to its shared email infrastructure system, exposing email addresses and passwords across six internet service providers including BIGLOBE, Chubu Telecommunications, and NIFTY Corporation. [[SecurityWeek](https://www.securityweek.com/in-other-news-canadian-hacker-jailed-open-source-zero-days-two-sentenced-for-atm-jackpotting/)]

- **Push Security Targeted by Its Own 'Poisoned Tenant' Research Technique** — Push Security, the firm that originally documented the poisoned tenant attack vector, was itself targeted using the technique via OpenAI's organization invitation feature. Multiple employees received invitations to join a fraudulent Push Security Inc. OpenAI tenant. [[SecurityWeek](https://www.securityweek.com/in-other-news-canadian-hacker-jailed-open-source-zero-days-two-sentenced-for-atm-jackpotting/)]

- **Pro-Russia Influence Operations Expand Beyond Ukraine** — Google's Threat Analysis Group reports that covert pro-Russia influence operations are shifting focus from Ukraine-centered narratives to broader geopolitical targets including the US, EU member states, NATO, the Middle East, and Africa, with increasing reliance on generative AI tools for content creation. [[SecurityWeek](https://www.securityweek.com/in-other-news-canadian-hacker-jailed-open-source-zero-days-two-sentenced-for-atm-jackpotting/)]
