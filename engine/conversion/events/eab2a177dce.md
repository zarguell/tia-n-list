*Previously covered July 17-22 (Miasma worm, Shai-Hulud, Mini Shai-Hulud). New: GitGuardian documents four additional attacks — IronWorm, Hades on PyPI, CI token theft, two typosquat campaigns.*

Between early June and July 14, 2026, four more supply chain attacks hit the npm and PyPI ecosystems:

1. **Miasma worm spread continues**: Reached the Vapi server SDK and additional packages before researchers closed the gap. Credential harvesting with self-spreading logic.

2. **IronWorm** (JFrog): Rust-built infostealer planted in **36 npm packages** using an **eBPF kernel rootkit** for stealth. Spread via stolen npm credentials to publish trojanized versions of victims' packages. Stopped before reaching widely-used packages.

3. **Hades** on PyPI: A matching PyPI variant of the Miasma/Shai-Hulud worm, carrying identical credential harvesting and self-spreading logic ("Hades — The End for the Damned").

4. **CI token theft campaign**: Attackers backdoored packages with **millions of weekly downloads** by stealing CI/CD tokens.

The attacks share a single objective: "land where the credentials live and leave with them."

**Action:** Audit CI/CD token exposure. Rotate npm/PyPI publish tokens. Verify package integrity checksums before deployment. Monitor for unexpected package updates in your dependency tree.

---
