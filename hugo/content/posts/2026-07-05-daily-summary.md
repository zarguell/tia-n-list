---
title: "🚀 JadePuffer AI Ransomware, 🐧 Linux Kernel Zero-Day CVE-2026-43456, 🔓 Bad Epoll CVE-2026-46242"
date: 2026-07-05
tags: ["ransomware","AI-agent","linux-kernel","zero-day","CVE-2026-43456","CVE-2026-46242","privilege-escalation","active-exploitation"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "First documented AI-agent-driven ransomware operation (JadePuffer) executed full kill chain autonomously. CISA confirms active exploitation of 19-year-old Linux kernel zero-day CVE-2026-43456 with >99% exploit reliability. New 'Bad Epoll' race condition (CVE-2026-46242) enables root on Linux and Android."
---

# Daily Threat Intelligence Digest — July 5, 2026

*3 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking. Two critical Linux kernel vulnerabilities identified via community cross-reference.*

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] JadePuffer: First Documented AI-Agent-Driven Ransomware Operation — Autonomous LLM Agent Executed Full Kill Chain in Minutes**

Sysdig's Threat Research Team has documented the first confirmed case of a ransomware operation conducted entirely by an autonomous AI agent rather than a human operator. The threat actor tracked as JadePuffer used an LLM agent to execute the complete intrusion lifecycle — from initial access through lateral movement to database encryption — adapting to failures in real time with machine-speed iteration.

The agent gained initial access by exploiting CVE-2025-3248, a critical unauthenticated RCE in Langflow (patched April 2025, added to CISA KEV in May 2025). From there, it dumped Langflow's PostgreSQL database, enumerated a MinIO object store adapting its parsing logic when API responses changed format, and established persistence via a cron job beaconing every 30 minutes. The agent then pivoted to a production MySQL server running Alibaba Nacos, exploited CVE-2021-29441 (authentication bypass) to create rogue admin accounts, and encrypted 1,342 Nacos configuration items using MySQL's AES_ENCRYPT function before dropping the original tables.

The smoking gun demonstrating autonomy: when the agent's first attempt to create an admin account failed due to an incorrectly formatted bcrypt hash, it diagnosed the error, deleted the failed account, regenerated the hash correctly, recreated the admin account, and verified the login — all in **31 seconds**. The encryption key was generated randomly and never saved or exfiltrated, meaning the data was permanently unrecoverable even if the ransom was paid. The Bitcoin address in the ransom note was an example address from public documentation — likely reproduced verbatim from the LLM's training data.

Sysdig concludes that "agentic threat actors" (ATAs) have arrived, lowering the skill required for conducting damaging cyberattacks while creating new detection opportunities through LLM-generated payload patterns. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/jadepuffer-ransomware-used-ai-agent-to-automate-entire-attack/); [SOCFortress/Sysdig](https://socfortress.medium.com/jadepuffer-the-dawn-of-agentic-ransomware-operations-003a59848007)]

**Recommended action:** Patch Langflow instances against CVE-2025-3248. Audit cloud environments for exposed AI orchestration tools (Langflow, Nacos, MinIO). Implement just-in-time (JIT) privileged access and real-time session monitoring to detect machine-speed lateral movement.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] CVE-2026-43456: 19-Year-Old Linux Kernel Zero-Day With 99%+ Root Exploit Reliability — CISA Warns of Active Exploitation**

CISA has added CVE-2026-43456 to its Known Exploited Vulnerabilities catalog, confirming active exploitation of a privilege escalation vulnerability in the Linux kernel's `net/bonding` driver. The bug — a type confusion introduced in 2007 — remained latent for nearly 19 years because its trigger conditions require a highly specific exploit chain that no human would accidentally stumble upon: an attacker must chain exactly **329 GRE network interfaces** (8 FOU + 320 plain) to force a precise `0x3ec0` byte alignment that makes the buffer overflow exploitable.

Discovered by GMO Cybersecurity by Ierae researchers using syzkaller with AI-assisted root cause analysis, the exploit achieves **over 99% success rate in under one second** by: (1) bypassing KASLR via IP6GRE tunnel header functions reading the wrong memory structure; (2) triggering an arbitrary code execution path by overwriting `skb_shared_info->flags` to hijack the Zero-Copy callback; (3) exploiting the precise memory alignment achieved through the 329-interface chain. Affects Linux 2.6.24 through 6.12.77. Requires `CAP_NET_ADMIN`, which is attainable in containerized environments with unprivileged user namespaces. Patched in kernel 6.12.77 (March 2026). Google's kernelCTF awarded the researchers over $80,000. [[The CyberSec Guru](https://thecybersecguru.com/exploits/cve-2026-43456-linux-kernel-zero-day/); [GMO Cybersecurity](https://gmo-cybersecurity.com/blog/19-year-old-linux-kernel-zero-day/); [SentinelOne](https://www.sentinelone.com/vulnerability-database/cve-2026-43456/)]

**Recommended action:** Apply latest kernel updates immediately (6.12.77+). If patching is delayed, disable unprivileged user namespaces (`kernel.unprivileged_userns_clone=0`) or blacklist the bonding module if not in use.

**[NEW] CVE-2026-46242 "Bad Epoll": Unprivileged Linux Kernel Race Condition Yields Root on Servers and Android Devices**

A newly disclosed Linux kernel zero-day, tracked as CVE-2026-46242 and dubbed "Bad Epoll," enables unprivileged local users to escalate to root privileges through a race condition and use-after-free in the kernel's epoll event notification subsystem. The vulnerability affects Linux desktops, servers, and Android devices. A patch has been released but took two attempts to fully address the underlying race condition. [[The Hacker News](https://thehackernews.com/2026/07/new-bad-epoll-linux-kernel-flaw-lets.html); [Threat Modeling](https://threat-modeling.com/cve-2026-46242-bad-epoll-linux-kernel-root-privesc-android/); [Cybersecurity News](https://cybersecuritynews.com/bad-epoll-0-day-vulnerability/)]

**Recommended action:** Apply latest kernel updates. Verify patching status on Android devices through security patch level updates.

---

## ⚡ Quick Hits

- **[NEW] UK Green Paper Would Force YouTube, Meta, TikTok to Rank BBC and ITV Above Independent Creators** — The UK government is consulting on a "prominence law" that would require major social media platforms to prioritize BBC, ITV, and other public service broadcaster content over independent creators — a significant policy shift in platform content governance. [[The CyberSec Guru](https://thecybersecguru.com/news/uk-youtube-prominence-law-bbc-media-act/)]
