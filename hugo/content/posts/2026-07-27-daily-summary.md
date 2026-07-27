---
title: "🎯 MCBS Breach Impacts 1.2M, 🎯 EU Sanctions Russian FSB Hackers, ⚠️ vBulletin Preauth RCE PoC, 🛡️ GitHub PyPI Time-Based Defenses, 📋 Claude AI Chats Exposed in Google"
date: 2026-07-27
tags: ["data breach","ransomware","PEAR","vBulletin","CVE-2026-61511","supply chain","GitHub","PyPI","Anthropic","Claude","privacy","EU sanctions","FSB","Russia","cyber espionage"]
categories: ["Threat Intelligence"]
author: Tia N. List
summary: "PEAR ransomware gang claims MCBS breach affecting 1.2M patients; EU hits Russian FSB 16th Centre officers with sanctions over years-long cyber spying; vBulletin preauth RCE PoC goes public; GitHub and PyPI implement time-based supply chain attack defenses; Claude AI shared chats surface in Google search results."
---

# Daily Threat Intelligence Digest — July 27, 2026

2 articles ingested from cyber feeds (SecurityWeek, BleepingComputer). Gap detection via web search identified 3 additional stories missed by feed: Claude AI shared chats exposed in Google, vBulletin preauth RCE PoC public, and EU sanctions on Russian FSB cyber operatives. Prior-digest continuity cross-referenced against Jul 22–26 — no overlaps found.

---

## 🎯 Threat Actor Activity & Campaigns

### PEAR Ransomware Group Claims MCBS Data Breach Affecting 1.2 Million Individuals

Atlanta-based medical business management company **MCBS (Medical Computer Business Services)** disclosed a data breach from September 2025 impacting 1,261,464 individuals. The **PEAR ransomware group** took credit, claiming to have stolen over 3 TB of files including patient PII/PHI, SSNs, financial documents, and emails. The group has made stolen data available for download on its leak site.

Seven healthcare organizations whose data was routed through MCBS were named in the notification. PEAR ransomware, which emerged in mid-2025, currently lists over 100 alleged victims on its leak site, including the Motility Software Solutions breach (766,000 affected) and the Tri-Century Eye Care breach (200,000 affected).

**Action:** Healthcare organizations using MCBS or similar revenue cycle management vendors should verify whether their data was exposed. Monitor for downstream fraud or phishing targeting affected patients.

**Source:** [SecurityWeek](https://www.securityweek.com/mcbs-data-breach-affects-1-2-million-individuals/)

### [GAP] EU Sanctions Russian FSB 16th Centre Officers for Years-Long Cyber Spying Campaign

The European Union on Monday imposed sanctions on **nine individuals and four entities** linked to Russia's **FSB 16th Centre**, accusing them of running a cyber espionage and sabotage campaign targeting EU member states since 2010. The campaign has targeted governments and critical infrastructure (heating and power plants) in at least nine countries including France, Germany, Poland, the Netherlands, Austria, and Finland.

French Foreign Minister Jean-Noël Barrot stated the cyber activities aimed to "capture information, or sabotage the operation, for example, of railway infrastructures as it was the case in Poland." The EU statement notes the FSB 16th Centre "has conducted a wide range of malicious cyber activities with growing severity" and "controls a variety of cyber threat groups."

**Significance:** This is the most comprehensive EU sanctions package specifically targeting Russia's FSB cyber operations unit. Organizations operating in the EU should review their threat models for Russian state-sponsored targeting, particularly in critical infrastructure and government sectors.

**Source:** [SecurityWeek/AP](https://www.securityweek.com/eu-targets-russian-intelligence-officers-accused-of-running-a-yearslong-cyber-spying-campaign/)

---

## ⚠️ Vulnerabilities & Patches

### [GAP] CVE-2026-61511: vBulletin Preauth RCE with Public PoC

A public proof-of-concept exploit has been released for **CVE-2026-61511**, a critical pre-authentication remote code execution vulnerability in **vBulletin 6.x** forum software. The flaw resides in the `runMaths()` method in vBulletin's template runtime, which passes weakly filtered input into a PHP `eval()` call. An unauthenticated attacker can reach this code through the `ajax/render` route by sending a tainted page-number parameter that flows into a `{vb:math}` tag.

**Key details:**
- Affects vBulletin 6.2.1 and earlier, plus 6.1.6 and earlier
- No authentication or user interaction required
- Public PoC by researcher EgiX through SSD Secure Disclosure
- Patch available in **vBulletin 6.2.2**
- No confirmed in-the-wild exploitation at time of reporting

With the exploit code now public, vBulletin forums that remain unpatched are at imminent risk of automated scanning and compromise.

**Action:** Identify any internet-exposed vBulletin 6.x instances and immediately upgrade to 6.2.2. Apply the security patch for 6.2.1/6.2.0/6.1.6 branches where full upgrade is not immediately feasible.

**Source:** [SecurityOnline](https://securityonline.info/vbulletin-preauth-rce-cve-2026-61511/) · SSD Secure Disclosure

---

## 🛡️ Defense & Detection

### GitHub, PyPI Add Time-Based Defenses Against Supply Chain Attacks

**GitHub's Dependabot** now applies a default **3-day cooldown** before opening update PRs after a new package version is published, reducing the window for automatically adopting recently published malicious packages. Users can configure shorter or longer delays through Dependabot's `cooldown` setting.

**PyPI** now blocks maintainers from adding new files to a package release **14 days** after publication, preventing attackers who compromise publishing tokens from poisoning old, trusted releases. While no past PyPI attacks have confirmed use of this specific technique, the measure is preventative.

These changes follow a wave of high-profile supply chain attacks in the npm/PyPI ecosystems over the past year, including the 'chalk' and 'debug' package hijacks, the 's1ngularity' operation, the Shai-Hulud campaign, and GhostAction.

**Bottom line:** These defenses raise the bar for supply chain attacks but GitHub acknowledges cooldowns have limitations — lockfiles, scoped tokens, and disabling unnecessary CI scripts remain essential layers.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/github-pypi-add-time-absed-defenses-against-supply-chain-attacks/)

---

## 📋 Policy & Industry News

### [GAP] Claude AI Shared Chats Surfaced in Google Search Results

Hundreds of **Anthropic Claude AI shared conversation links** were publicly discoverable through Google search over the weekend. A Reddit post showed that queries such as `site:claude.ai/share` returned conversations containing legal strategy discussions, engineering/proprietary code, cryptocurrency wallet keys, API credentials, and personal information.

The Claude share feature generates public URLs intended for selective sharing but lacked proper `noindex` tags, allowing search engines to crawl and index the full chat content once links spread via forums or social media. By Sunday, Google results had largely been deindexed, though existing direct URLs remain accessible unless Anthropic revokes them server-side.

This is not an isolated incident — similar issues have affected ChatGPT shared links. The incident underscores a recurring AI product design problem: convenience features for sharing content also make it easy to expose unless privacy controls keep pace.

**Action:** Claude users should immediately review and delete unnecessary shared conversations in Settings → Privacy. Treat any shared AI chat as potentially public. For organizations, review whether employees have shared sensitive business data via AI chat features.

**Source:** [Cyber Security News](https://cybersecuritynews.com/claude-ai-shared-chats/) · [StudioGlobal](https://www.studioglobal.ai/discover/answers/search-fact-check-with-cited-sources-for-6a66b94f36db3952a7c88063)

---

## Gap Detection

| Source | Story | Status | Action |
|--------|-------|--------|--------|
| r/cybersecurity hot | No critical unindexed stories — trending topics (career discussion, Secure Boot re-reporting, Pope's Click to Pray app leak) already covered in prior digests or non-security | No action |
| CISA KEV | No new additions since July 14–16 | No action |
| SecurityOnline | [GAP] **CVE-2026-61511 vBulletin Preauth RCE** — PoC public, July 27 date ✅ | Added to digest |
| CyberSecurityNews | [GAP] **Claude AI Shared Chats Exposed** — weekend story ✅ | Added to digest |
| SecurityWeek/AP | [GAP] **EU Sanctions Russian FSB 16th Centre** — Monday (July 27) ✅ | Added to digest |

---

*Digest generated July 27, 2026. 2 feed articles reviewed, 5 prior digests cross-referenced for continuity, 3 gap stories identified via web search and incorporated. Excluded as already covered in prior digests or non-critical: Windmill CVE-2026-29059 (Jul 22), Pope's Click to Pray app leak (Jul 24-25), RabbitMQ CVE-2026-57219 (Jul 10-13), Ghost Accounts GitHub recon (Jul 10-13), Progress ShareFile SZC shutdown (Jul 12-13), Okta O-UNC-066 vishing campaign (ongoing since Apr).*
