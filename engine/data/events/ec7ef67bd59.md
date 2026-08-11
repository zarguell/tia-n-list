Flare researchers mapped the criminal business ecosystem around **BTMOB**, the Android RAT sold as malware-as-a-service (droppers, payload builder, Windows operator panel, server infrastructure, phishing/credential-stealing tooling). What began as a centrally operated service (early 2025: **$700/month, $3,000 lifetime, $5,000+ for private infrastructure**) has **splintered**: the apparent official operation keeps releasing versions and selling access while a secondary market of cheaper subscriptions, reseller panels, purported source-code sales, and impersonator accounts now trades under the BTMOB name.

- Infrastructure problems became a sales opportunity: within a month of launch the operator acknowledged server errors (claiming 4,000+ connected devices) and began selling private infrastructure — fragmenting control and attribution.

- Resellers undercut official pricing; authenticity of most offers is unverifiable, and impersonation is widespread.

- **Defender takeaway:** MaaS families like BTMOB are no longer single-codebase threats — the splintering produces custom variants, private builds, and unreliable-but-cheap access for low-skill actors. Android RAT detection must be behavioral (accessibility abuse, overlay/phishing patterns, device-admin abuse), not signature-based.

---
