A critical flaw in SimpleHelp remote management software (versions ≤5.5.15, 6.0 pre-release) allows unauthenticated attackers to **create privileged technician accounts** on servers using OIDC authentication. The vulnerability in identity assertion validation enables bypassing MFA and gaining remote access to managed endpoints, with script execution capabilities. ~14,000 SimpleHelp servers are internet-exposed, with ~7.2% using OIDC. Patched in versions 5.5.16 and 6.0RC2 (June 9).

---
