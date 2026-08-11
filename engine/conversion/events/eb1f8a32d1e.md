*Previously covered: JCE (CVE-2026-48907) July 8; ColdFusion and Langflow KEV additions July 8/9. New: ACSC issues government alert with comprehensive CVE list, confirms widespread Australian business impact.*

The Australian Cyber Security Centre (ACSC) has issued a formal alert about a large-scale exploitation campaign targeting vulnerable content management systems globally, with many Australian SMBs confirmed affected. The campaign deploys webshells for persistent access, enabling service disruption, credential theft, additional malware deployment, and lateral network movement.

The ACSC advisory lists 18 specific CVEs under active exploitation across five CMS platforms and 14 plugins/extensions:

**WordPress plugins (13 CVEs):** Simple File List (CVE-2025-34085, CVE-2020-36847), WavePlayer (CVE-2025-12057), BerqWP (CVE-2025-7443), WPBookit (CVE-2025-7852), Ninja Forms (CVE-2026-0740), ThemeREX Addons (CVE-2026-1969), Breeze Cache (CVE-2026-3844), pay-uz (CVE-2026-31843), ACF Extended (CVE-2025-13486), Sneeit Framework (CVE-2025-6389), WPvivid Backup (CVE-2026-1357), Gravity Forms (CVE-2025-12352), GutenKit/Hunk Companion (CVE-2024-9234).

**Other platforms:** Craft CMS (CVE-2025-32432), MaxSite CMS (CVE-2026-3395), MetInfo CMS (CVE-2026-29014), Joomla JCE (CVE-2026-48907 — CISA KEV since June 16).

The ACSC noted the campaign may be supported by AI, which could accelerate vulnerability discovery and exploitation at scale. Website administrators should apply all CMS/plugin updates immediately, remove unused components, enable automatic updates, make web directories read-only, monitor for unauthorized file creation, restrict access to sensitive directories, and block unexpected child process spawning on web servers.

---
