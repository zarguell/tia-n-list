---
title: "🟢 Operation Highland 10-Year Air-Gap Breach, 🔵 Anthropic Fable 5 Jailbreak Dispute, 📦 NPM 12 Supply Chain Fix"
date: 2026-06-14
tags: ["Velvet Ant","Operation Highland","Supply Chain","AI Safety","npm","Anthropic","Fable 5","NPM 12","APT"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Velvet Ant Chinese APT breached an air-gapped critical infrastructure network for 10 years by hijacking PAM and OpenSSH. New details emerge on the Anthropic Fable 5 export control dispute — Amazon allegedly flagged a narrow jailbreak. NPM 12 set for July release with supply chain protections."
---

# Daily Threat Intelligence Digest — June 14, 2026

*8 articles ingested and analyzed from Miniflux Cyber feeds, with prior-digest continuity tracking.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Operation Highland — Velvet Ant Chinese APT Hijacks Authentication Stack, Spies on Air-Gapped Critical Infrastructure Network for 10 Years**

Chinese hackers of the **Velvet Ant** cluster breached an isolated critical infrastructure network and maintained undetected access for a decade (2016–2026) by hijacking the organization's entire authentication infrastructure. Dubbed **"Operation Highland"** by Sygnia researchers, the intrusion represents one of the longest known persistent compromises of a truly air-gapped environment.

The attack chain began with the compromise of internet-facing servers, deploying a modified **GS-Netcat reverse shell** disguised as a legitimate system component, with persistence via malicious `systemd` services or startup scripts. A custom **SOCKS5 proxy** masquerading as `smbd -D` turned compromised servers into internal pivot points.

The most sophisticated element: Velvet Ant modified a compromised internet-facing **Nginx server** to proxy specially crafted HTTP POST requests through a **FastCGI wrapper (fcgiwrap)** into the isolated network — establishing a remote-execution bridge with no direct connection to the critical infrastructure environment. Inside, they:

- **Replaced `pam_unix.so` with 9 distinct backdoored variants** — each compiled in a separate build environment, indicating a well-resourced operation — accepting hardcoded passwords and harvesting user credentials
- **Trojanized OpenSSH components** (ssh, sshd, scp) to capture credentials and log SSH session commands
- Achieved persistence immune to password changes and session terminations, with full visibility into every administrative login and command

**Cleanup complexity:** Remediation required building a dedicated testing lab to validate binary replacement — removing tampered authentication components risked locking legitimate administrators out entirely.

**Recommendation:** Treat PAM, OpenSSH, and LSASS as critical security assets. Deploy file integrity monitoring, hardened privileged access, and offline recovery procedures with immutable backup snapshots. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/chinese-hackers-hijack-auth-flow-spy-on-isolated-network-for-a-decade/)]

---

## 📋 Policy & Industry News

**[UPDATE] Anthropic Fable 5 Export Controls — Amazon Allegedly Flagged Jailbreak to Commerce Department, Anthropic Says Capabilities Already Available in GPT-5.5**

New details emerged about the Trump administration's Friday directive ordering Anthropic to suspend foreign access to **Fable 5** and **Mythos 5** (covered June 13). The Commerce Department's letter cited a technique for "jailbreaking" Fable 5 — reportedly prompting the model to read a specific codebase and identify software flaws.

**Key new developments:**

- **Amazon is alleged to have flagged the security concern** to the Commerce Department, though the company did not respond to requests for comment
- Anthropic reviewed the report forming the basis of the directive and found the demonstrated capabilities **"were already available in other publicly accessible models, including OpenAI's GPT-5.5"** and are routinely used by cybersecurity professionals defensively
- The company called it a **"narrow, non-universal jailbreak"** and warned the standard would "essentially halt all new model deployments for all frontier model providers"
- **Katie Moussouris** (Luta Security) attributed the issue to **"Defense Oriented Prompting"** — treating natural language as code in model instruction security
- **Aaron Levie** (Box CEO) called it "a big turning point for AI regulation"
- **DOD CIO Kirsten Davies** publicly supported the action: *"Some things are simply more important than revenue cycles"*

Anthropic has disabled both models pending resolution and is working to restore access, disputing that the finding justifies a recall. The controversy underscores the growing tension between AI capability deployment and national security controls, with significant implications for how frontier models are vetted and distributed. [[CyberScoop](https://cyberscoop.com/us-government-anthropic-fable-5-mythos-5-export-controls/)]

---

## ⚠️ Vulnerabilities & Patches

**[UPDATE] NPM 12 Set for July Release — Script Execution Blocked by Default to Counter Supply-Chain Attacks**

GitHub finalized the security architecture for **npm v12** (targeting **July 2026** release), moving beyond the June 11 announcement with an explicit migration timeline. The changes will:

1. **Block default script execution** — `npm install` will no longer run `preinstall`/`install`/`postinstall` scripts from dependencies without project-level approval. This directly counters the **Shai-Hulud Miasma** campaign's weaponization of `binding.gyp` files
2. **Lock down git dependencies** — closing a code-execution path where a Git dependency's `.npmrc` could override the Git executable even with `--ignore-scripts`
3. **Block remote URL tarballs** — requiring the `--allow-remote` flag (available since npm 11.15.0)

**Migration path:** Upgrade to npm 11.16.0+, run install to review warnings, then use `npm approve-scripts --allow-scripts-pending` to generate an allowlist committed to `package.json`. [[SecurityWeek](https://www.securityweek.com/npm-12-will-change-script-execution-behavior-to-prevent-supply-chain-attacks/)]

---

## ⚡ Quick Hits

- **Ex-school district employee sentenced to 21 months:** Ezekiel Dean Potter, 34, a former senior IT support specialist for Iowa's Saydel Community School District, was sentenced June 11 after conducting a 21-month cyberattack against his former employer — deleting the district's Facebook page, stripping employees of access to Apple School Manager and Google accounts, and disrupting classroom operations. Potter must pay $59,668.81 in restitution. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/ex-school-district-employee-jailed-for-hacks-on-former-employer/)]
