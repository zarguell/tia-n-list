---
title: "🇯🇵 KDDI Breach 14.2M, 🎾 Kinahan Cartel Padel, 🐧 Linux Kernel PoCs"
date: 2026-06-28
tags: ["KDDI","data breach","Japan","ISP","Kinahan cartel","Bellingcat","OSINT","CVE-2026-46331","CVE-2026-43503","Linux kernel","privilege escalation"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "KDDI breach exposes up to 14.2M email logins across six Japanese ISPs. Bellingcat tracks sanctioned Kinahan cartel lieutenant via padel tournaments. PoCs published for two Linux kernel LPE flaws (pedit-cow, DirtyClone)."
---

# Daily Threat Intelligence Digest — June 28, 2026

*1 article ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] KDDI Data Breach Exposes Up to 14.2 Million Email Logins Across Six Japanese ISPs**

Japanese telecommunications giant KDDI Corporation disclosed a data breach in which threat actors gained access to its email infrastructure, potentially exposing the email addresses and passwords of up to 14.2 million customers across six internet service providers. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/data-breach-exposes-up-to-142-million-email-logins-at-six-isps/)]

KDDI discovered the compromise on June 17 and says attackers exploited a vulnerability in an unnamed third-party software component. The affected ISPs — STNet, JCOM, Chubu Telecommunications, NIFTY Corporation, and BIGLOBE — were notified starting June 17, along with Japan's Personal Information Protection Commission and the Ministry of Internal Affairs and Communications.

KDDI states that some passwords were stored in hashed and/or encrypted form, but did not disclose what percentage were stored in plaintext or which hashing algorithm was used. The company advises affected customers to reset their email passwords immediately and enable two-factor authentication where available. The investigation is ongoing, and the exact number of compromised accounts has not yet been determined.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Bellingcat Tracks Sanctioned Kinahan Cartel Lieutenant to Dubai Padel Tournaments — First Public Photos in Nearly a Decade**

Bellingcat and The Sunday Times published an investigation identifying Ian Thomas Dixon, a sanctioned lieutenant of the Kinahan Organized Crime Group, living openly in Dubai and competing in amateur padel tournaments under the alias "Ian Thomas." [[Bellingcat](https://www.bellingcat.com/news/2026/06/27/poster-boy-sanctioned-kinahan-cartel-lieutenant-found-playing-padel-in-dubai/)]

Dixon, 36, was sanctioned by the U.S. Treasury in 2022 alongside cartel leadership Christy Kinahan (69) and his sons Daniel (49) and Christopher Jr. (45). Authorities allege Dixon managed finances and moved bulk currency for Daniel Kinahan's drug trafficking operation — a network estimated at $1.5 billion with links to Iran's intelligence services and Hezbollah. The cartel's feuds have been linked to at least 18 murders across four countries.

Using facial recognition, Bellingcat matched Dixon to a padel club advertisement and traced his tournament participation through live-streamed matches, social media posts, and online tournament profiles. Footage shows Dixon at the Asia Pacific Padel Tour in December 2024, where he placed second in the amateur final. He was also seen with Stephen Jamieson, a Scottish criminal recently jailed for six years on organized crime and drug charges.

The investigation comes as cartel leader Daniel Kinahan awaits extradition to Ireland after his arrest in Dubai in April. Three of seven sanctioned Kinahan figures have now been arrested.

---

## ⚠️ Vulnerabilities & Patches

**[NEW] Exploit Code Published for Two Linux Kernel Privilege Escalation Flaws — pedit-cow and DirtyClone**

Public proof-of-concept exploits have been released for two Linux kernel local privilege escalation vulnerabilities, enabling unprivileged local users to gain root access across multiple distributions. [[SC Media](https://www.scworld.com/news/2-linux-kernel-flaw-pocs-published-enabling-local-privilege-escalation); [The CyberSec Guru](https://thecybersecguru.com/news/linux-lpe-pedit-cow-dirtyclone-cve-2026-46331-cve-2026-43503/)]

- **CVE-2026-46331 (pedit-cow):** An out-of-bounds write in the kernel's traffic control packet editing subsystem (act_pedit) causes corruption of shared page-cache memory instead of writing to a private copy. Affects RHEL 8/9/10, Debian 11/12/13, and Ubuntu 18.04–26.04. A working exploit appeared within 24 hours of CVE assignment.
- **CVE-2026-43503 (DirtyClone):** A high-severity (CVSS 8.8) flaw in skbuff shared-fragment handling lets local users gain root by corrupting file-backed memory through cloned network packets. Affects any distribution running a kernel without the complete DirtyFrag patch chain. [[JFrog Research](https://research.jfrog.com/post/dissecting-and-exploiting-linux-lpe-variant-dirtyclone-cve-2026-43503/); [The Hacker News](https://thehackernews.com/2026/06/new-dirtyclone-linux-kernel-flaw-lets.html)]

Mitigations: Blacklist the act_pedit module if tc pedit rules are not used, or disable unprivileged user namespaces. Ubuntu 24.04+ has partial AppArmor namespace restrictions but the underlying kernel vulnerability remains.
