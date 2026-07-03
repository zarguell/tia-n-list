---
title: "🔴NetNut Takedown, 🎯Cursor AI RCE, ⚠️CitrixBleed Exploitation, 🎯Pegasus on Investigator, ⚠️Cisco Unified CM"
date: 2026-07-03
tags: ["netnut","cursor-ai","citrixbleed","pegasus","cisco","unified-cm","m365","consentfix","ransomware","kev","ai-security","infostealer","macos"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "Google/FBI dismantle 2M-device NetNut proxy network; critical Cursor AI DuneSlide flaws enable OS-level RCE; CitrixBleed-like CVE-2026-8451 exploited within 24h; Pegasus found on EU spyware investigator's phone; Cisco confirms Unified CM exploitation."
---

# Daily Threat Intelligence Digest — July 3, 2026

*19 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking. One new macOS infostealer identified via community cross-reference.*

---

## 🔴 Critical Threats & Active Exploitation

**[NEW] Google, FBI Disrupt NetNut Residential Proxy Network — 2 Million Compromised Devices Used for Cybercriminal and State-Sponsored Attacks**

Google, the FBI, and international partners coordinated a takedown of NetNut (also known as Popa), a massive residential proxy network consisting of more than 2 million Android devices — smart TVs, streaming boxes, and other IoT devices — infected through trojanized applications and malware including Badbox 2.0. The network's operator, linked to publicly-traded Israeli firm Alarum Technologies Ltd, rented access to these compromised devices to cybercriminal and espionage groups to mask their identities during attacks.

In a single week in June, Google observed 316 distinct threat clusters using NetNut to hide their locations in password-spray attacks and to access victim environments. The takedown disabled Google accounts and associated services used for command-and-control, dismantled the botnet's backend, disabled infected applications via Google Play Protect, and automatically warned victims. Google also operates a reseller program, allowing other brands to whitelabel the NetNut botnet.

"This follows the January disruption of IPIDEA and is expected to have a ripple effect across the ecosystem," Google noted, adding that "when faced with the degradation of their own botnet, proxy operators begin buying capacity from their competitors." [[SecurityWeek](https://www.securityweek.com/google-fbi-disrupt-netnut-residential-proxy-network-powered-by-millions-of-devices/)]

---

**[UPDATE] CitrixBleed-Like Vulnerability (CVE-2026-8451) Exploited Within 24 Hours of Disclosure — Two Threat Actor Groups Scanning NetScaler Instances**

Threat actors began exploiting CVE-2026-8451 (CVSS 8.8), an out-of-bounds read vulnerability in NetScaler ADC and Gateway appliances configured as SAML identity providers, less than 24 hours after public disclosure on June 30. Scottish security firm Lupovis reports that at least two distinct threat actors are now probing exposed NetScaler instances.

*Previously covered July 1 at disclosure. New today: Confirmed active exploitation by two groups within 24 hours of public PoC.*

The first scanning activity originated from an IP in Frankfurt, Germany, deploying a payload matching the overread variant from watchTowr's detection generator — a bare `<samlp:AuthnRequest>` tag padded with 476 spaces followed by a newline. A second actor was observed scanning from a Koapu Cloud HK IP address. Both groups probe for the SAML endpoint and deliver the exploit payload immediately upon receiving a 200 OK response.

The flaw exists in NetScaler's XML parser, which fails to terminate unquoted XML attribute values followed by a newline character, causing the parser to read past the intended buffer and return memory contents in the NSC_TASS cookie. [[SecurityWeek](https://www.securityweek.com/new-citrixbleed-vulnerability-exploited-immediately-after-public-disclosure/)]

**Recommended action:** Patch NetScaler appliances immediately. If patching is not possible, disable SAML IDP configuration. Monitor logs for `/saml/login` traffic and inspect NSC_TASS cookie values.

---

**[NEW] Cisco Confirms Attackers Exploiting Unified CM Vulnerability (CVE-2026-20230) — SSRF Flaw Enables Remote Server Takeover**

Cisco has finally confirmed that attackers are actively exploiting CVE-2026-20230, a server-side request forgery vulnerability in Cisco Unified Communications Manager (Unified CM, formerly CallManager) patched in early June. The flaw enables unauthenticated, low-complexity remote attacks via crafted HTTP requests. Cisco's PSIRT acknowledged PoC exploit code was publicly available at patch time (June 3) but only confirmed active exploitation on June 22, three weeks later, when threat intelligence firm Defused revealed attackers were using `file://` payloads to create files on targeted devices. Shadowserver currently tracks over 200 exposed Unified CM instances, most in Asia and North America. Cisco has shared mitigation measures including disabling the vulnerable WebDialer service. [[BleepingComputer](https://www.bleepingcomputer.com/news/security/cisco-finally-confirms-attackers-exploiting-unified-cm-flaw/)]

**Recommended action:** Apply Cisco Unified CM versions 14SU6 or 15SU5 immediately. Disable WebDialer service as a temporary mitigation if patching is delayed.

---

## 🎯 Threat Actor Activity & Campaigns

**[NEW] Pegasus Spyware Found on Phone of EU Spyware Investigator — Citizen Lab Identifies Double Infection of PEGA Committee Member**

The University of Toronto's Citizen Lab has revealed that someone used NSO Group's Pegasus spyware to infect the mobile phone of Stelios Kouloglou, a Greek journalist and former Member of the European Parliament who served as a substitute member of the PEGA Committee. The PEGA Committee was established in 2022 to investigate spyware abuses across the European Union following journalistic revelations about government deployment of Pegasus technology.

Citizen Lab concluded with "high confidence" that Kouloglou's phone was infected twice — once around October 2022 and once around March 2023 — during "crucial moments" of the committee's work, including the preparation of its final report and prominent hearings. During the first infection, Kouloglou was hospitalized and received a visit from another Greek journalist who had previously been targeted with spyware, raising concerns about health data exposure through the phone's audio capabilities.

This is the first time a member of the PEGA Committee has been publicly identified as a Pegasus victim. PEGA Committee member Hannah Neumann stated that "many of us were expecting some hacks during the committee, but it's still frustrating now to figure out it really happened." Citizen Lab's Ron Deibert called the case proof that "the still unregulated and highly abused mercenary spyware industry is poisonous to democratic processes." [[CyberScoop](https://cyberscoop.com/pegasus-spyware-pega-committee-member-targeted/)]

---

**[NEW] ConsentFix and ClickFix: Microsoft 365 Accounts Hijacked in 3 Seconds via OAuth Token Theft**

Huntress has published a detailed analysis of ConsentFix, a new attack variant targeting Microsoft 365 OAuth consent flows that can hijack accounts in seconds — bypassing both passwords and MFA. The attack lives in the gap between what security awareness training covers and what modern social engineering exploits.

The setup uses phishing lures delivered through trusted platforms like Dropbox or DocSend, sometimes password-protected to evade security inspection. Victims encounter a convincing Microsoft authentication screen and are instructed to drag a localhost callback link into their browser. That drag-and-drop step surrenders OAuth tokens to the attacker, granting session access to email and other Microsoft 365 services without any credential theft.

A detailed walkthrough of ConsentFix was posted to a public Russian cybercrime forum by early March 2026, complete with working code, infrastructure screenshots, and a video tutorial. ClickFix, the precursor technique using fake prompts to execute keyboard shortcuts, remains active. [[BleepingComputer/Huntress](https://www.bleepingcomputer.com/news/security/consentfix-and-clickfix-how-microsoft-365-accounts-are-hijacked-in-3-seconds/)]

**Recommended action:** Audit OAuth consent flows and implement Conditional Access policies covering non-interactive authentication. Monitor for unusual PowerShell activity from normal user processes and unexpected session logins.

---

**[NEW] Operation Endgame — The Rebuild Is the Test**

CSIRT Gadgets published a deep research analysis on the aftermath of Operation Endgame, the law enforcement disruption targeting SocGholish, Amadey, and StealC botnets. While the takedown gave defenders a "rare clean scoreboard" — servers and domains actioned, credentials recovered, crypto assets restricted — the harder question is whether these criminal enterprises became meaningfully weaker or simply absorbed the hit and began rebuilding.

The analysis emphasizes that cybercrime crews typically attempt reconstitution, and the useful metric is not disruption metrics but disruption effects: whether coming back is cheap, fast, and trusted, or expensive, noisy, and fragile. Measuring infrastructure reconstitution, traffic supply, affiliate trust, monetization, and downstream impact is where the real analytical work lies. [[CSIRT Gadgets](https://csirtgadgets.com/commits/2026/7/2/deep-research-operation-endgame-was-the-takedown-the-rebuild-is-the-test)]

---

## ⚠️ Vulnerabilities & Patches

**[NEW] DuneSlide: Critical Cursor AI Code Editor Flaws Enable OS-Level Remote Code Execution — CVSS 9.8, Sandbox Escape via Prompt Injection**

Cato Networks has disclosed two critical vulnerabilities in the popular Cursor AI code editor, tracked as CVE-2026-50548 and CVE-2026-50549 (both CVSS 9.8), collectively dubbed DuneSlide. The flaws enable zero-click prompt injection attacks that escape Cursor's sandbox and execute arbitrary code on the underlying operating system.

The first vulnerability exploits Cursor's automatic terminal command execution inside the sandbox, which does not prompt the user for approval. By setting a non-default value for the `working_directory` parameter via an innocuous MCP server request, an attacker can inject a prompt that redirects the working directory to an attacker-supplied path outside the project scope, then overwrite the `cursorsandbox` executable so that future commands run without sandbox restrictions — achieving non-sandboxed RCE.

The second, independent flaw affects the IDE's file path resolution logic and can be exploited via symbolic links to bypass out-of-bounds write protections. By creating a write-only symlink pointing outside the project directory, an attacker can force Cursor to fall back to the original symlink path, enabling out-of-bounds file writes — including overwriting the sandbox executable.

Cato reported both flaws to Cursor in February. Patches were included in Cursor 3.0, released April 2. CVE IDs were assigned in early June. [[SecurityWeek](https://www.securityweek.com/critical-cursor-ai-ide-flaws-could-lead-to-os-level-remote-code-execution/)]

**Recommended action:** Upgrade Cursor to version 3.0 or later immediately. Review MCP server configurations for unauthorized endpoint modifications.

---

**[NEW] Q2 2026 Attack Techniques Trend Report — CISA KEV Listings Up 27%, Ransomware Exploitation Doubles, AI Attack Surface Expands**

ASEC's Q2 2026 Attack Techniques Trend Report documents a notable shift in the threat landscape: CISA KEV listings reached 75 in Q2 2026, a 27% increase over Q2 2025, with the percentage of listings associated with ransomware rising from 8.5% to 16.0%. Primary targets included web and server applications, endpoints, network perimeter devices, and remote management tools, with growing attention to AI and supply chain vulnerabilities.

Key findings from the report:
- **Threat actors** frequently used T1190 (Exploit Public-Facing Application) to bypass authentication, targeting SimpleHelp, Check Point, Ivanti Sentry, Oracle PeopleSoft, Cisco, and Splunk
- **Identity attacks** included OAuth device code phishing, AiTM (man-in-the-middle) attacks, and stolen token/session exploitation targeting Microsoft Entra ID
- **AI-related exploits** expanded: SearchLeak (CVE-2026-42824) targets M365 Copilot Enterprise for data exfiltration; CVE-2026-26030 and CVE-2026-25592 in Microsoft Semantic Kernel enable prompt injection leading to RCE; CVE-2026-42271 in LiteLLM listed in KEV
- **Three Microsoft Defender zero-days** were listed in the KEV, with threat actors blocking legitimate processes and telemetry to evade detection
- **Malicious skill supply chain attacks** (OpenClaw, ClawHub) continued against AI agent platforms

The report recommends shifting from signature-based to behavior-based detection, focusing on memory injection, sensor telemetry disconnection, abnormal authentication sessions, and abnormal token issuance. [[ASEC](https://asec.ahnlab.com/en/94320/)]

---

## 🛡️ Defense & Detection

**[NEW] Rapid7 Formalizes Red Teaming as Multi-Agent AI Architecture — Built via Project Glasswing with Anthropic Mythos**

Rapid7's Red Team published a detailed technical post on how they formalized their penetration testing methodology as a structured multi-agent AI system. Rather than a monolithic agent, the system uses supervisor-style orchestration: a coordinator agent assesses engagement state, routes work to specialist agents (enumeration, code review, dynamic testing, reporting), and processes results — mirroring how human red teams operate.

The key design insight was reverse-engineering the agent architecture from the team's daily task lists: which tasks repeat, in what sequence, where decisions branch, and what triggers backtracking. Deliberate scope decomposition ensures each component receives full analytical attention rather than competing for context space. The system was validated as part of Anthropic's Project Glasswing initiative, using Claude Mythos for vulnerability analysis and exploit chain development with exceptional results.

Guardrails include tiered safety enforcement: scope validation before every action, action classification (non-destructive/destructive/ambiguous), and human-in-the-loop for all dynamic testing. The system also revealed practical insights about AI security: prompt injection can propagate between agents, trust boundaries blur when one agent's output becomes another's input, and guardrails can be bypassed through indirect manipulation. [[Rapid7](https://www.rapid7.com/blog/post/so-red-teaming-offensive-methodology-multi-agent-ai-architecture)]

---

**[NEW] Unit 42 Builds First Non-Windows RDP Client with WebAuthn Support — Reverse-Engineered Microsoft's Undocumented Code Paths**

Palo Alto Networks' Unit 42 published a detailed technical account of adding WebAuthn redirection to Prisma Browser's native RDP client, beating Microsoft's own macOS, iOS, and Linux clients to the feature. The project required reverse-engineering mstsc.exe with IDA Pro to discover that Microsoft's Windows implementation routes WebAuthn through private, undocumented code paths in webauthn.dll that accept a pre-computed 32-byte hash rather than the full clientDataJSON required by the public API.

The work revealed that older Windows servers (pre-25H2) transmit only the 32-byte hash over the wire, requiring a custom Chromium extension API that bypasses the standard `navigator.credentials` API to pass the hash directly to the authenticator. Since shipping, FreeRDP has added support in version 3.25.0. Microsoft has since updated the MS-RDPEWA spec (v3.0, March 2026) to document previously missing commands. [[Unit 42](https://unit42.paloaltonetworks.com/webauthn-added-to-browser-based-rdp/)]

---

## 📋 Policy & Industry News

**[NEW] Google Loses Final Appeal Against €4.1 Billion EU Antitrust Fine — CJEU Upholds Android Abuse of Dominance Ruling**

The Court of Justice of the European Union dismissed Google's final appeal against a €4.1 billion ($4.7 billion) antitrust fine over Android agreements that illegally promoted Google Search and Chrome. The ruling stems from a 2018 European Commission decision finding Google abused its dominant market position by requiring manufacturers to pre-install Google Search and Chrome to license the Play Store, restricting manufacturers from selling devices running non-approved Android versions, and offering revenue-sharing agreements tied to exclusive Google Search pre-installation.

Google argued the Commission underestimated competitive pressure from Apple's iOS and said it had revised its contractual practices since 2018, including adding user-choice screens in 2021 and implementing 20+ product changes after the Digital Markets Act took effect. The company noted it adapted its agreements following the initial 2018 decision. [[BleepingComputer](https://www.bleepingcomputer.com/news/legal/google-loses-final-appeal-to-overturn-41-billion-eu-fine/)]

---

**[NEW] Microsoft Overhauls Partner Ecosystem Security — Mandatory Security Requirements for Cloud Solution Providers**

Microsoft published a detailed post on its approach to securing the Cloud Solution Provider (CSP) ecosystem, revealing that nation-state actors have targeted CSPs as a vector to compromise downstream customers. The initiative focuses on four pillars: (1) partner vetting to verify legitimate organizations before they can operate as CSPs; (2) enhanced security posture requirements including mandatory security baselines as a condition of authorization; (3) least-privilege access via Granular Delegated Administrative Privileges (GDAP) with scope and duration constraints; and (4) strong monitoring and rapid-response capabilities, including the ability to revoke a CSP's GDAP access across all customers when needed.

The post highlights that attackers do not distinguish between "internal" and "external" systems — if a partner platform provides a path to customer compromise, it will be exploited. [[Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/07/02/improving-security-posture-across-the-microsoft-partner-ecosystem/)]

---

## ⚡ Quick Hits

- **[NEW] PamStealer macOS Infostealer Targets Mac Users via Fake Maccy Clipboard Manager Sites** — A Rust-based information stealer discovered by Jamf Threat Labs is distributed through lookalike websites (maccyapp[.]com) impersonating the legitimate Maccy clipboard manager. The two-stage attack uses a compiled AppleScript dropper that runs even with the `com.apple.quarantine` attribute intact, checks for Apple Silicon-only execution, and validates captured login passwords through macOS's PAM API before exfiltration. It targets browser credentials, cryptocurrency wallets, iCloud Keychain, and clipboard content. [[The Hacker News](https://thehackernews.com/2026/07/pamstealer-uses-fake-maccy-sites-and.html)]

- **[UPDATE] Claude Fable 5 Returns — Users Report Significant Performance Regression** — Anthropic restored access to Claude Fable 5 after the US government lifted export controls, but early adopters report notably degraded performance compared to the original release. The company stated Fable 5 will not be permanently removed from subscriptions and expects it to return outside the usage-based plan. *Previously covered June 29 (access restoration), July 1 (availability timeline).* [[BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/claude-fable-relaunch-disappoints-users-with-nerfed-performance/)]

- **[NEW] Prompt Injection as Role Confusion — ICML 2026 Paper Reveals Why LLMs Fail to Distinguish Trust Boundaries** — MIT researchers published work demonstrating that prompt injection succeeds not because attackers find clever phrasings but because LLMs perceive roles through writing style rather than structural trust tags. The CoT Forgery attack injects fake reasoning mimicking the LLM's own thinking style, raising attack success from near-zero to ~60% across frontier models. [[tl;dr sec #335](https://tldrsec.com/p/tldr-sec-335); [Paper](https://role-confusion.github.io/)]

- **[NEW] AWS Continuum: Agentic Security Platform for Code Vulnerability Management** — AWS announced Continuum, a multi-model agentic platform managing the full vulnerability lifecycle — discovery, prioritization, validation (with sandboxed exploit construction), and automated remediation — operating in "learn mode" with human oversight before graduating to "enforce mode." [[AWS Security Blog](https://aws.amazon.com/blogs/security/introducing-aws-continuum-security-at-machine-speed)]
