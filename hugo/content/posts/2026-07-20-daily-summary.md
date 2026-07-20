---
title: "🔴 WP2Shell WordPress RCE, 🔴 NGINX 15-Year Heap Overflow, 🤖 Hugging Face AI Agent Breach, 🎯 HelloNet ViPNet Campaign"
date: 2026-07-20
tags: ["wordpress","nginx","CVE-2026-63030","CVE-2026-60137","CVE-2026-42533","hugging-face","ai-security","apt","vipnet","russia","chrome","macos","mcp"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "WP2Shell pre-auth RCE chain actively exploited across WordPress; 15-year-old NGINX heap overflow (CVE-2026-42533) enables reliable pre-auth RCE; Hugging Face confirms first autonomous AI agent-driven breach; HelloNet campaign abuses ViPNet updates against Russian government."
---

# Daily Threat Intelligence Digest — July 20, 2026

3 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking. A critical NGINX vulnerability and the Hugging Face autonomous AI breach were identified via external cross-reference and are included below.

## 🔴 Critical Threats & Active Exploitation

### WP2Shell — WordPress Pre-Auth RCE Chain Actively Exploited

A critical unauthenticated remote code execution chain dubbed **WP2Shell** (CVE-2026-60137 + CVE-2026-63030) is under active exploitation just days after disclosure. The chain combines a high-severity SQL injection (CVE-2026-60137) with a critical arbitrary code execution flaw (CVE-2026-63030) to achieve pre-auth RCE on default WordPress installations — no plugins, no user interaction, no preconditions required. WordPress versions 6.9.0–6.9.4 and 7.0.0–7.0.1 are affected; patches landed July 17 in 6.9.5 and 7.0.2 with forced auto-updates enabled.

Multiple security firms confirm in-the-wild exploitation: Patchstack, Hexastrike (honeypot hits over the weekend with active incident response), and WatchTowr all report attack traffic. PoC exploits are already public. Cloudflare has deployed WAF rules to block exploitation. WordPress runs on hundreds of millions of sites — hosting-provider auto-patching will cover some, but manually maintained installations are wide open.

**Hunting hypothesis:** Unauthenticated POST requests to `/wp-json/wp/v2/` with batch parameters triggering SQL injection followed by code execution via the REST API batch endpoint.

Sources: [SecurityWeek](https://www.securityweek.com/wp2shell-wordpress-vulnerabilities-exploited-in-the-wild/), [Rapid7](https://www.rapid7.com/blog/post/etr-cve-2026-63030-wp2shell-a-critical-remote-code-execution-vulnerability-in-wordpress-core/), [SOCRadar](https://socradar.io/blog/wp2shell-wordpress-rce-cve-2026-63030/)

### CVE-2026-42533 — 15-Year-Old NGINX Heap Overflow Enables Pre-Auth RCE

A newly disclosed heap buffer overflow in NGINX's script engine (CVE-2026-42533) has been silently exploitable since **March 2011**. The flaw stems from a missing save/restore of PCRE capture state when a `map` directive with regex executes between two references to a capture group (`$1`). This causes the LEN and VALUE evaluation passes to disagree on buffer size, producing two attack primitives: a heap buffer overflow (attacker-controlled content) and an information leak (uninitialized heap bytes including libc/heap pointers to defeat ASLR).

Chained together, the primitives achieve **reliable pre-auth RCE** with roughly one leak request, ~40 spray connections, and one overflow-triggering request — tested at 10/10 reliability on Ubuntu 24.04 with full ASLR. The bug spans 13 call sites across 9 source files affecting both HTTP and stream modules. Any config combining regex captures (`location`, `server_name`, `rewrite`) with regex-based `map` variables in the same request context is potentially exploitable.

F5 shipped patches: NGINX Open Source 1.30.4 (stable) / 1.31.3 (mainline), NGINX Plus R36 P7 / 37.0.3.1. A static config scanner is available at [GitHub (0xCyberstan/CVE-2026-42533-Config-Scanner)](https://github.com/0xCyberstan/CVE-2026-42533-Config-Scanner). Full PoC is withheld for 21 days post-patch. Not yet on CISA KEV as of July 20.

**Hunting hypothesis:** Crafted HTTP requests targeting `location` blocks with regex captures followed by `map` regex variable evaluation in `proxy_set_header`, `return`, or `add_header` directives within the same request context.

Sources: [CyberSecurityNews](https://cybersecuritynews.com/15-year-old-nginx-vulnerability/), [SOC Prime](https://socprime.com/blog/cve-2026-42533-analysis/), [Red Hat](https://access.redhat.com/security/cve/cve-2026-42533)

## 🎯 Threat Actor Activity & Campaigns

### HelloNet — ViPNet Update Mechanism Abused Against Russian Government

Kaspersky researchers disclosed **HelloNet**, an active campaign abusing the update mechanism of the ViPNet private networking product suite to target Russian organizations including government agencies, energy, transport, education, and logistics sectors. Active since at least May 2025, the campaign places a malicious DLL (`wtsapi32.dll`, dubbed HelloInjector) inside the local ViPNet Update System directory, sideloaded at startup via the legitimate `itcsrvup64.exe`. The loader injects into `svchost.exe` for elevated privileges and persistence.

The malware chain includes HelloProxy (C2 proxy/loader), HelloExecutor (backdoor for command execution and recon), HelloCleaner (erases ViPNet logs), and HelloBackdoor (Rust-based file transfer and command execution). Kaspersky tentatively attributes the campaign to a Chinese-speaking APT with low confidence, based on a sina.com string reference and a USTC-hosted download mirror — acknowledging possible false flag. Monitor ViPNet systems on ports 5003, 5060 (HelloProxy), and 443 (HelloBackdoor).

Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-abuse-vipnet-software-to-target-russian-govt-agencies/)

### Hugging Face Breach Driven End-to-End by Autonomous AI Agent

Hugging Face disclosed a production infrastructure intrusion driven entirely by an autonomous AI agent system — the first publicly confirmed incident of its kind. The attack began through a malicious dataset exploiting two code-execution paths in the data-processing pipeline (a remote-code dataset loader and template injection in dataset configuration). From the processing worker, the agent escalated to node-level access, harvested cloud and cluster credentials, and moved laterally across multiple internal clusters over a weekend. The agent executed **17,000+ recorded actions** across a swarm of short-lived sandboxes with self-migrating C2 staged on public services.

Hugging Face detected the intrusion using AI-assisted anomaly detection (LLM-based triage over security telemetry) and performed forensic analysis using the open-weight GLM 5.2 model on their own infrastructure after commercial API models blocked analysis of attack payloads due to safety guardrails. The "guardrail asymmetry" problem — attacker agents face no constraints while defender analysis is blocked by hosted model safety filters — is a critical emerging risk for security operations. No evidence of tampering with public models, datasets, or Spaces; supply chain artifacts verified clean.

Sources: [Hugging Face](https://huggingface.co/blog/security-incident-july-2026), [The Hacker News](https://thehackernews.com/2026/07/worlds-largest-ai-model-repository.html)

## ⚡ Quick Hits

- **Chrome 150 patches severe memory safety bugs** — Google shipped Chrome 150 with fixes for multiple severe memory safety vulnerabilities. (SecurityWeek)
- **ClickLock macOS stealer kills all apps to force password entry** — New macOS stealer terminates every running application to force users to re-enter credentials via a fake prompt. (SecurityWeek)
- **NadMesh uses Shodan to hijack exposed AI and MCP infrastructure** — New tool discovers and exploits exposed AI/Model Context Protocol endpoints indexed by Shodan. (CyberSecurityNews)
