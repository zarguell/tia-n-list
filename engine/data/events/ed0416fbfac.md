Two Joomla extensions — **Balbooa Forms** (CVE-2026-56291) and **iCagenda** (CVE-2026-48939) — both carry CVSS 10.0 scores for unauthenticated arbitrary file upload vulnerabilities enabling remote code execution. Both were exploited as zero-days before patches were available, and CISA added them to the Known Exploited Vulnerabilities catalog on July 10 with a 3-day remediation deadline under BOD 26-04.

- **Balbooa Forms** (CVE-2026-56291): Affects versions ≤2.4.0. Exploits the frontend attachment upload endpoint to upload PHP webshells. Patched in v2.4.1 (July 9), but threat actors exploited it in the wild prior to the patch.

- **iCagenda** (CVE-2026-48939): Affects file attachment feature. Developer JoomliC observed in-the-wild exploitation on June 15. Patched in v4.0.8 and v3.9.15 (June 15–16).

**Action:** Audit any Joomla deployments for these extensions immediately. If present, update to patched versions now — both flaws require no authentication to exploit.
