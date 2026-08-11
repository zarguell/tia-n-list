AlphaHunt's deep-research note reframes SaaS incident response around a practical observation: SaaS incidents often *begin* with a human interaction, but the **operational center of data theft is a non-human identity** — an OAuth app, refresh token, integration user, service principal, or API key.

The analysis maps what recent public campaigns actually demonstrate (delegated authority converting a noisy user event into **durable, scriptable API access**) versus what remains unknown, then lays out the telemetry, authority graph, consent controls, and revocation proof defenders need. The goal is a working incident model for "finding the badge that still works after the visible door is closed."

**Action:** Inventory OAuth apps and refresh tokens with high privilege, map the authority graph from user → token → data, and verify you can actually revoke delegated access end-to-end before an incident demands it.

---
