---
title: "🛡️ Oracle PeopleSoft Victim Expands, 🇷🇺 $10M Russian Bounty, 🤖 OpenAI/Anthropic Restrictions, 🧠 GPT-5.6 Sol Debuts, 🔐 PQC Deadlines"
date: 2026-06-29
tags: ["Oracle","PeopleSoft","ShinyHunters","Nissan","CVE-2026-35273","UNC5792","UNC4221","Russia","OpenAI","Anthropic","GPT-5.6","Sol","Mythos","AI","PQC","bounty","messaging"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Nissan confirmed as the latest Oracle PeopleSoft breach victim in the ongoing ShinyHunters campaign exposing payroll data and SSNs. US offers $10M bounty for Russian state hackers targeting Signal and WhatsApp accounts. OpenAI launches GPT-5.6 Sol while both OpenAI and Anthropic restrict frontier AI models to Trump administration-approved customers."
---
# Daily Threat Intelligence Digest — June 29, 2026

*5 articles ingested and analyzed from curated cyber intelligence feeds, with one critical gap identified via web search.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Nissan Americas Confirms Oracle PeopleSoft Breach — Payroll Records, SSNs Exposed in Ongoing ShinyHunters Campaign**

Nissan Motor Co. has joined the growing list of Oracle PeopleSoft customers caught in the ShinyHunters exploitation wave, warning employees that Social Security numbers, bank account details, payroll records, and other personal data may have been stolen. [[The Register](https://www.theregister.com/security/2026/06/29/nissan-says-oracle-peoplesoft-break-in-may-have-spilled-payroll-records-ssns/5263534)]

In a filing submitted to the California Attorney General on Friday, Nissan Americas stated that Oracle had notified it of "a cyber event" involving the personnel records of hundreds of employees. The breach stems from the same ShinyHunters-orchestrated exploitation of an Oracle PeopleSoft zero-day (CVE-2026-35273) disclosed June 10, which has now impacted NAIC, Nissan, and potentially hundreds of other organizations running the HR and payroll platform. [[The Hacker News](https://thehackernews.com/2026/06/shinyhunters-exploits-oracle-peoplesoft.html)]

**Bottom line:** Any organization running Oracle PeopleSoft should assume credentials and configuration data are compromised and treat the Oracle June 10 patch as urgent. The victim list continues to expand more than two weeks after the initial disclosure.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] US Offers $10 Million Bounty for Russian Intelligence Hackers as Messaging App Attacks Evolve to Steal Backup Recovery Keys**

The U.S. Department of State is offering rewards of up to $10 million for information on individuals linked to **UNC5792** (FSB Border Guards) and **UNC4221** (Russian military services), two threat actor groups targeting current and former U.S. government officials, military leaders, allied personnel, and Ukrainian targets through phishing campaigns against commercial messaging applications. [[SecurityWeek](https://www.securityweek.com/us-offers-10-million-bounty-for-russian-state-hackers-as-messaging-app-attacks-evolve/)]

In a March alert, CISA and the FBI documented how the groups pose as automated support accounts for Signal and WhatsApp to trick victims into sharing verification codes and taking over accounts. A fresh update reveals the attackers have escalated tactics — they are now asking victims for their **Backup Recovery Keys**, granting access to historical private and group messages. Critically, even if a victim reclaims their account, the stolen recovery key remains valid for future re-compromise of any new account using the same phone number. The only remediation is generating a new Backup Recovery Key, though this does not prevent the attacker from already having downloaded the account's backup data.

---

## 📋 Policy & Industry News

**[NEW] OpenAI and Anthropic Restrict Frontier AI Models to Administration-Approved Customers — GPT-5.6 Sol, Mythos 5 in Limited Release**

Both OpenAI and Anthropic have agreed to sharply restrict access to their most advanced AI models as the Trump administration exercises its new executive order framework for vetting national security risks of frontier AI systems. [[SecurityWeek/AP](https://www.securityweek.com/openai-and-anthropic-limit-new-ai-models-to-trump-approved-customers-during-cybersecurity-review/)]

OpenAI announced GPT-5.6 **Sol** as its flagship model — described as its most capable cybersecurity AI, matching Anthropic's Mythos Preview on ExploitBench while using roughly one-third the output tokens. [[SecurityWeek](https://www.securityweek.com/openai-unveils-gpt-5-6-sol-as-its-most-advanced-cybersecurity-ai/)] The model is available only to approximately 20 administration-approved customers via API and Codex, with broader ChatGPT and API access planned for "coming weeks." OpenAI stated it allocated over 700,000 A100-equivalent GPU hours toward automated red-teaming to harden the model against systemic jailbreak vulnerabilities.

Anthropic simultaneously announced the Trump administration has approved limited re-deployment of **Mythos 5** to a small group of cyber defenders and infrastructure providers, two weeks after the Commerce Department effectively banned the model. The company's **Fable 5**, pitched as a safer alternative to Mythos, remains unavailable even after the government lifted restrictions on the more powerful Mythos.

The government actions — described by critics as "deciding company by company who gets access" without legislation or oversight — come as both OpenAI and Anthropic explore public offerings, and follow a June executive order establishing voluntary federal review of AI models for up to 30 days before release. Stanford cybersecurity expert Alex Stamos called the restrictions counterproductive, saying "if the administration is honest about wanting the United States to beat China in this race, this is about the dumbest thing they could possibly do."

---

## ⚡ Quick Hits

- **[UPDATE] Post-Quantum Cryptography Readiness — CISO Deadlines Loom** — An op-ed from Keyfactor's SVP lays out the operational reality of Executive Order 14409's PQC deadlines: federal high-value systems must transition key establishment by **December 31, 2030** and digital signatures by **December 31, 2031**. The piece emphasizes that the "Harvest Now, Decrypt Later" threat is already operational, and advises CISOs to establish cryptographic inventories and cross-functional PQC steering committees immediately. [[CyberScoop](https://cyberscoop.com/post-quantum-cryptography-readiness-ciso-deadlines-op-ed/)]

- **Robot Police Drone Disarms Suspect — A First** — The Sacramento County Sheriff's Office deployed a drone with a high-powered magnet to grab a knife from an armed suspect's hand inside a cluttered garage, marking a novel use of drone technology for police disarmament. [[Schneier on Security](https://www.schneier.com/blog/archives/2026/06/robot-police-officers.html)]
