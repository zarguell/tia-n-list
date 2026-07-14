---
title: "🌏 ACSC CMS 18 CVEs, 🕵️ GitHub Ghost Recon, 📋 Joomla KEV Additions"
date: 2026-07-12T07:00:00-04:00
tags: ["threat-intelligence", "cms-exploitation", "cisa-kev", "github-recon", "wordpress", "joomla", "acsc"]
categories: ["Threat Intelligence", "Daily Digest"]
author: "Tia N. List"
summary: "Light-volume weekend edition. ACSC issues alert on global CMS exploitation campaign targeting 18 CVEs across WordPress, Craft CMS, Joomla, and other platforms. CISA KEV adds two more Joomla extensions (iCagenda, Balbooa Forms). Datadog publishes technical analysis of GitHub ghost account reconnaissance campaign."
---

# Daily Threat Intelligence Digest — 2026-07-12

2 articles ingested and analyzed from curated cyber intelligence feeds, with prior-digest continuity tracking.

---

## ⚠️ Vulnerabilities & Patches

### [UPDATE] ACSC Warns of Global CMS Exploitation Campaign — 18 CVEs Across WordPress, Craft CMS, Joomla, and Others

*Previously covered: JCE (CVE-2026-48907) July 8; ColdFusion and Langflow KEV additions July 8/9. New: ACSC issues government alert with comprehensive CVE list, confirms widespread Australian business impact.*

The Australian Cyber Security Centre (ACSC) has issued a formal alert about a large-scale exploitation campaign targeting vulnerable content management systems globally, with many Australian SMBs confirmed affected. The campaign deploys webshells for persistent access, enabling service disruption, credential theft, additional malware deployment, and lateral network movement.

The ACSC advisory lists 18 specific CVEs under active exploitation across five CMS platforms and 14 plugins/extensions:

**WordPress plugins (13 CVEs):** Simple File List (CVE-2025-34085, CVE-2020-36847), WavePlayer (CVE-2025-12057), BerqWP (CVE-2025-7443), WPBookit (CVE-2025-7852), Ninja Forms (CVE-2026-0740), ThemeREX Addons (CVE-2026-1969), Breeze Cache (CVE-2026-3844), pay-uz (CVE-2026-31843), ACF Extended (CVE-2025-13486), Sneeit Framework (CVE-2025-6389), WPvivid Backup (CVE-2026-1357), Gravity Forms (CVE-2025-12352), GutenKit/Hunk Companion (CVE-2024-9234).

**Other platforms:** Craft CMS (CVE-2025-32432), MaxSite CMS (CVE-2026-3395), MetInfo CMS (CVE-2026-29014), Joomla JCE (CVE-2026-48907 — CISA KEV since June 16).

The ACSC noted the campaign may be supported by AI, which could accelerate vulnerability discovery and exploitation at scale. Website administrators should apply all CMS/plugin updates immediately, remove unused components, enable automatic updates, make web directories read-only, monitor for unauthorized file creation, restrict access to sensitive directories, and block unexpected child process spawning on web servers.

**Source:** [BleepingComputer](https://www.bleepingcomputer.com/news/security/australia-warns-of-global-campaign-targeting-vulnerable-cms-platforms/)

---

### [UPDATE] CISA KEV: Two New Joomla Extension Entries Added July 10 — iCagenda and Balbooa Forms

*Previously covered: JoomShaper SP Page Builder (CVE-2026-48908) and Joomlack Page Builder (CVE-2026-56290) July 8/10. New: Two additional Joomla extension vulnerabilities added to KEV on July 10.*

CISA added two more Joomla ecosystem vulnerabilities to the Known Exploited Vulnerabilities catalog on July 10, continuing the pattern of CMS-targeted exploitation reflected in the ACSC alert:

- **CVE-2026-48939** (CVSS 9.8) — iCagenda unrestricted file upload, EPSS 2%
- **CVE-2026-56291** (CVSS 9.8) — Balbooa Forms unrestricted file upload, EPSS 1%

Both are file upload vulnerabilities enabling unauthenticated remote code execution — the same attack class driving the broader CMS exploitation campaign. Organizations running Joomla installations should audit all third-party extensions and update or remove any running vulnerable versions. CISA confirmed 6 newly exploited CVEs this week across all vendors, with 20 new KEV entries in the last 30 days.

**Sources:** [Senserva KEV Tracker](https://senserva.com/exploited-this-week.html) | [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

---

## 🎯 Threat Actor Activity & Campaigns

### [UPDATE] GitHub Ghost Account Reconnaissance Campaign — Datadog Publishes Technical Analysis

*Previously covered July 11 via SOCFortress. New: Datadog publishes original research with additional operational detail.*

Datadog Security Labs has published the primary technical analysis of the GitHub API reconnaissance campaign first covered yesterday. Since October 2025, over 50 dormant ghost accounts (registered 2–5 years ago) have been activated in coordinated 1–3 week bursts to enumerate organizations, repositories, members, and project structures via GitHub's unauthenticated public API surface.

Key findings from the Datadog report:
- Accounts use "vibe-coded" user agents mimicking analytics tools (`GitHubAnalytics/1.5`, `GitHubReporter/2.0`) to blend with legitimate traffic
- GraphQL bulk queries are the primary enumeration vector, with some REST route targeting
- One campaign leveraged inadvertently exposed tokens from legitimate GitHub users, targeting private repository commit paths from dozens of accounts simultaneously — an "Identity Dark Matter" pattern
- In rare cases, reconnaissance escalated to confirmed private repository data exfiltration

Defense requires enabling GitHub audit log streaming, baselining user agents and source ASNs, and aggregate anomaly detection. Individual requests return HTTP 200 with no authentication failure signals, making per-request detection ineffective.

**Sources:** [SecurityWeek](https://www.securityweek.com/ghost-accounts-abuse-github-api-in-mass-recon-campaign/) | [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/coordinated-github-api-enumeration/)
