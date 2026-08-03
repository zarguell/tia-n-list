---
title: "🔴 Water Attacks Spread to 7 States, 🔴 N-able RMM God-Mode Exploit, ⚠️ COLDCARD RNG $88M Theft, 🎯 Larva-24009 Phishing Campaign, 🛡️ Chrome Blocks New Tab Hijackers"
date: 2026-08-03
tags: ["threat-intel","ot-security","ransomware","supply-chain","cryptocurrency","apt","phishing","ai-security"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "US water-sector attacks expand to at least 7 states; N-able N-central RMM auth bypass is under active exploitation with an incomplete first fix; a COLDCARD firmware RNG flaw likely enabled an $88.6M Bitcoin theft; plus new Larva-24009 phishing analysis and AI-noise data from CrowdStrike's threat hunting report."
---
# Daily Threat Intelligence Digest — August 3, 2026

8 articles ingested from curated cyber feeds. External gap detection surfaced 2 substantive stories missed by the feeds: the actively exploited N-able N-central RMM authentication bypass (CVE-2026-18556/18577) and CRPx0's Hyundai Turkey leak-site claim. CISA KEV: no new additions detected since the Jul 29 baseline (Cisco FMC CVE-2026-20316 was last). Continuity cross-referenced against Jul 29–Aug 2 digests.

---

## 🔴 Critical Threats & Active Exploitation

### [UPDATE] US Water Cyberattacks Extend Beyond Minnesota to at Least 7 States — Michigan, South Dakota, Georgia Confirm Incidents

*Minnesota attacks covered Jul 28–Aug 1. New today: the campaign's geographic scope expands to at least seven states, with new state-level confirmations and a TLP:Amber WaterISAC report tying the activity to Iran-linked campaigns.*

The water-sector campaign that hit 30+ Minnesota community systems on July 26–27 was **never limited to one state**. Reporting today establishes:

- **At least seven states** are now known to be affected, per mainstream outlets citing sources; Georgia is named by ABC News, with the other states unnamed at publication time.
- **Michigan** officially confirmed that a "small number" of communities saw malicious cyber activity, stating all systems operated safely with no public health concerns.
- **Rapid City, South Dakota** reported a cyber incident involving **one of its wastewater lift stations** — a description consistent with the same campaign. The city said water/wastewater infrastructure was never jeopardized.
- **WaterISAC** circulated a report (obtained by Wired, marked **TLP:Amber** and not intended for public release) in which **Minnesota's Fusion Center found the attacks "aligned" with hacking campaigns previously linked by the US to Iran**. The US government has still not publicly blamed Iran; the WaterISAC document is the strongest on-record alignment signal to date.
- Few technical details have been released by affected cities; the Minnesota cellular-connected-equipment vector remains the leading hypothesis, consistent with Iran-linked targeting of Israeli water facilities via cellular routers in 2020. **Infracritical maintains a continuously updated technical summary** for OT defenders.

**Context:** Censys (covered Aug 1) quantified ~10,000 internet-exposed Rockwell/Siemens/Schneider PLCs; CISA's sector alert (Jul 30) documented PLC password-lockout and IP-reassignment tactics; CISA/FBI advisory AA26-097A ties this profile to Iranian-affiliated actors (CyberAv3ngers, Handala).

**Action:** The campaign is broader and more persistent than initially reported. Treat any water/wastewater entity with cellular-connected OT as a target: audit for undocumented cellular modems, remove internet-exposed PLCs, enforce VPN-gated remote access with allowlists, and change default credentials. Review AA26-097A IOCs and Infracritical's report for hunt leads.

**Sources:** [SecurityWeek](https://www.securityweek.com/us-water-cyberattacks-extend-beyond-minnesota-to-at-least-6-other-states/) · Wired (WaterISAC TLP:Amber report) · ABC News

### [GAP] N-able N-central Critical Auth Bypass (CVE-2026-18556/18577) Actively Exploited — First Fix Was Incomplete; MSPs Urged to Hotfix Now

*Missed by today's feeds; surfaced via external monitoring. N-able disclosed Aug 1–2 with confirmed in-the-wild exploitation.*

N-able disclosed a critical vulnerability in **N-central**, its flagship RMM platform used by MSPs to monitor and remotely administer every downstream customer endpoint. Key facts:

- **CVE-2026-18556** (initial advisory) → **CVE-2026-18577** ("an incomplete patch for CVE-2026-18556 allows for authentication bypass and account takeover in N-central versions through 2026.3.1"). **All currently supported versions are affected, including builds initially believed safe** — both cloud-hosted and on-premises.
- An unauthenticated attacker gains **full administrative "god-mode" access to the RMM console** — the same control level as trusted NOC/engineering staff. From there they can push scripts/jobs to managed endpoints, deploy dual-use tools via the N-able agent, and (per Huntress) abuse the built-in **Take Control** feature to pivot into managed endpoints and deploy **Cloudflare-based tunnels for persistence**.
- N-able shipped hotfix **2026.3.1.7 on August 2** as the first unaffected build. Huntress reports **55.6% of reachable cloud N-central servers were still unpatched** as of Aug 3, and notes the server runs a custom **AlmaLinux 9 appliance that frequently has no EDR** deployed.
- **IOCs:** attacker traffic observed from `87.249.138[.]34` (NordVPN exit node), `37.19.210[.]32` (Mullvad exit node, previously abused for brute-forcing/spam), plus `37.153.90[.]88` and `92.118.112[.]181` (added by N-able in a follow-up advisory).

**Why it matters:** This is the Kaseya-VSA-shaped nightmare for the MSP supply chain — RMM compromise means downstream access to every managed customer, and the incomplete-first-fix pattern means orgs that patched to the original advisory version are still exposed.

**Action:** Apply **2026.3.1.7 immediately**; if N-central is reachable from untrusted networks, consider taking it offline until patched behind strict network controls. Audit for suspicious logins, new remote-control/Take Control sessions, and unexpected Cloudflare tunnel processes on the N-central host. Hunt for the four IOCs.

**Sources:** [Huntress Rapid Response](https://www.huntress.com/blog/n-able-vulnerability-exploitation) · [The Hacker News](https://thehackernews.com/2026/08/n-able-says-attackers-take-over-n.html) · N-able advisory

### COLDCARD Hardware Wallet RNG Flaw Likely Behind $88.6M Bitcoin Theft — 4,585 Wallets Drained

Researchers suspect a firmware RNG flaw in **COLDCARD** hardware wallets enabled the theft of an estimated **$88.6 million in Bitcoin (1,367 BTC) from 4,585 addresses** across three automated sweep waves (July 30–August 1). Galaxy Research identified the first wave — **1,083 BTC (~$70.2M) from 1,196 addresses in a 41-minute automated sweep on July 30**, roughly 30 hours before Coinkite publicly disclosed the flaw. Every transaction used an identical hardcoded 30 sat/vB fee (a 30–75× overpay vs. that week's median) with no change output — "an automated tool spending keys it already held, not owners moving funds." Chainalysis found the attacker **prioritized high-value wallets** (~$30M taken in the first ten minutes; one victim lost $1.8M), suggesting the affected wallets were identified and studied in advance. The funds remained in attacker-controlled addresses at last report.

**Root cause:** Block's Bitcoin Engineering and Security teams traced the issue to an **RNG integration error**: a faulty check in COLDCARD firmware makes `ngu.random` fall back to **MicroPython's deterministic Yasmarang generator** instead of the STM32 hardware RNG. The deterministic fallback was seeded by the device's microcontroller identifier and timing values — **observable or reconstructable** — letting attackers generate candidate seeds offline and match derived addresses against the blockchain.

**Affected:** Mk2/Mk3 firmware 4.0.1–4.1.9; Mk4/Mk5 before standard 5.6.0 or Edge 6.6.0X; Q before standard 1.5.0Q or Edge 6.6.0QX. Fixed in 4.2.0+ / 5.6.0+ / 1.5.0Q+ / 6.6.0X / 6.6.0QX. **Updating firmware does not repair a previously generated seed** — affected users must verify backups, install fixed firmware, generate and record a new seed, verify the address on-device, test with a small transaction, then migrate remaining funds (retain old backups until migration is confirmed). Seeds supplemented with ≥50 fair, independent, private dice rolls are not considered at risk from this flaw alone; a strong unique BIP-39 passphrase mitigates but does not repair the seed. TAPSIGNER, OPENDIME, and SATSCARD use different codebases and are unaffected; Coinkite destroyed all affected unsold devices.

**Sources:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/coldcard-wallet-rng-flaw-likely-linked-to-88-million-bitcoin-theft/) · Galaxy Research · Block · Coinkite

---

## 🎯 Threat Actor Activity & Campaigns

### Larva-24009 (aka "HeptaX") Continues 2026 Phishing Campaigns: LNK Lures → PowerShell Backdoor → QuasarRAT/UltraVNC

ASEC (AhnLab) published an analysis of 2026 attacks by **Larva-24009** — active since at least 2023, previously disclosed in 2024 and independently tracked by Cyble under the name **"HeptaX"**. The 2026 tooling is essentially unchanged from 2024, with similar file names:

- **Initial access:** phishing emails carrying **LNK malware disguised as document files**, themed for enterprise targets — hospital surveys, blockchain, project proposals, and resumes (recent samples: `NovaCX_Agency_Updated_..._version_1_8.Docx.Lnk`, `NovaCX_Interview_QA+Updated_..._version_4_4.Docx.Lnk`). Executing the LNK runs an obfuscated PowerShell command that drops a decoy document to %TEMP% while downloading a second-stage script from C&C.
- **Backdoor & persistence:** PowerShell scripts download and execute further payloads from C&C (`aonexa[.]shop/res/get-command.php`, `/post_proc.php`, `/index.php`, `/new-upload.php`), register **Task Scheduler persistence** under masquerading names ("Intel(R) Ethernet3 Connection 1219-LM", "GoogleUpdateTaskMachineCoreUA*"), capture screenshots, and disable Windows Defender. A "Notifier" component (v2.1) now reports infection status to the operator **via the Telegram API**.
- **Remote control:** **QuasarRAT** and **UltraVNC Server** (ports 5800/5900) for live screen control, plus RDP; the download server also hosts a batch script that adds a backdoor account named `_BootUEFI_`.
- **Credential theft:** NirSoft utilities (ChromePassView, WebBrowserBookmarksView, Network Password Recovery, LastActivityView) plus a custom keylogger writing to `%ALLUSERSPROFILE%\Microsoft\OneDrive\log.log` / `logv.Log`.

**IOCs:** C&C domains `aonexa[.]shop`, `final[.]mainsec2[.]site`, `mainsec[.]site`, `pozeny[.]shop`, `serverdock[.]online`; IP `217[.]77[.]6[.]50`; MD5s published in the ASEC report.

**Action:** Block the IOCs; enforce LNK/script execution controls on email (this is a pure document-disguised-LNK chain — attachment filtering and ASR-style rules stop it); treat unsolicited "survey/recruitment/project" attachments as hostile, especially in orgs with Korea/APAC business exposure.

**Source:** [ASEC (AhnLab)](https://asec.ahnlab.com/en/94786/)

### [GAP] CRPx0 Ransomware Claims Hyundai Turkey Breach — 1.5GB of Assessment Data Listed

Double-extortion group **CRPx0** listed **Hyundai's Turkish operations** on its leak site (August 1), claiming **1.5GB of exfiltrated assessment data**. Details are thin — no confirmation from Hyundai, no disclosed access vector — but the claim adds to a busy week for automotive-sector ransomware targeting. Treat as unverified until Hyundai responds; monitor for downstream phishing leveraging any leaked employee/customer data.

**Source:** GBHackers weekly roundup (Jul 27–Aug 1) · CRPx0 leak site

---

## 🛡️ Defense & Detection

### CrowdStrike Threat Hunting Report: AI Is Now Both the Weapon and the Target — AI-Driven Detections Exceed Human-Triggered 2:1

CrowdStrike's annual threat hunting report (year ending June 2026) quantifies the AI inflection point from the defender's seat: the company's hunting team and systems triaged an **average of 14 million detection leads daily**, yielding ~36,000 customer alerts — and **AI agent-driven behaviors have surged past human triggers**, creating more than twice as much potentially-malicious noise as human activity. "AI has driven the detections significantly above what humans are causing… it's being used everywhere," said Adam Meyers. Other headline data:

- **AI-enabled malicious activity surged 89% year-over-year** as adversaries use the technology to scale operations, accelerate tradecraft, and target AI infrastructure — "AI is now a tool, a target, and a force multiplier."
- Attackers are using frontier models for **vulnerability discovery** and to generate **scripts, payloads, and commands**, and to design more creative automated attack flows.
- Enterprise AI adoption itself is the new attack surface: every deployed AI tool adds agentic entry points defenders must inventory.

**Action:** The 2:1 AI-to-human noise ratio means detection triage must assume agentic behavior is now the baseline, not the anomaly. Baseline normal agent behavior per tool, treat agent identities as first-class (non-human identity) inventory, and scope agent permissions tightly (see Jul 30 digest on least-privilege for agents).

**Source:** [CyberScoop](https://cyberscoop.com/crowdstrike-annual-threat-hunting-report-2026/) · CrowdStrike Threat Hunting Report 2026

### Google Chrome to Block New Tab Hijacker Extensions by Default

Google is preparing a new Chrome security feature that would **block policy-installed extensions from hijacking the New Tab page or changing the default search engine**. Spotted by BleepingComputer in work-in-progress Chromium Gerrit changes (not yet shipped), the protection targets an abuse pattern where, "in low-trust environments (unmanaged consumer devices), enterprise policy force-installs and recommendations are abused to lock in search engines" — the same ClickFix/policy-abuse ecosystem pushing unwanted browser modifications. Google plans to enable it by default once approved. **Action:** enterprise admins relying on policy-installed extensions for legitimate New Tab/search configuration should review whether the change affects their managed deployments.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/google/google-chrome-may-soon-block-new-tab-hijacker-extensions-by-default/)

---

## Gap Detection

| Source | Story | Status | Action |
|--------|-------|--------|--------|
| Huntress / THN / N-able | **N-able N-central CVE-2026-18556/18577** — actively exploited RMM auth bypass, incomplete first fix, hotfix 2026.3.1.7 | ✅ Not in feeds | Added to Critical Threats |
| GBHackers weekly | **CRPx0 claims Hyundai Turkey breach** (Aug 1) — 1.5GB assessment data | ✅ Not in prior digests | Added to Threat Actor section |
| CISA KEV | No new additions since Jul 29 (Cisco FMC CVE-2026-20316 was last); SharePoint RCE CVE-2026-58644 coverage dates to Jul 17 — already handled | No action | |
| SecurityWeek (feed) | Russian Wi-Fi gateway hacking — re-report of Microsoft's CaptiveCrunch disclosure (Storm-2945), fully covered Aug 1; no material new facts | Already covered | Omitted |
| SOCFortress (feed) | STAC4749 Teams vishing/Chaos ransomware — vendor rehash of campaign covered Jul 30–31 (Sophos confirmation) | Already covered | Omitted |
| r/cybersecurity / weekly | Ruflo MCP bridge flaw (Jul 29), SonicWall SMA zero-days (Jul 17 disclosure), Windows WalletService LPE, SolarWinds WHD SAML bypass | Stale (>24–48h, outside digest window) or prior coverage | Skipped |

---

*Digest generated August 3, 2026. 8 feed articles reviewed; prior digests Jul 29–Aug 2 cross-referenced for continuity; CISA KEV monitored. Two gap stories incorporated (N-able N-central, CRPx0/Hyundai). Excluded as prior-digest repeats or non-threat-intel: CaptiveCrunch re-report (covered Aug 1), SOCFortress STAC4749 rehash (covered Jul 30–31), OpenAI Astra model tease (not threat intelligence).*
