Researchers published a local root exploit for OpenBSD 7.9 that chains a roughly 37-year-old integer overflow in shared-memory handling with a separate kernel bug to escalate privileges. The integer overflow dates back decades in the OpenBSD shared-memory code, illustrating how latent memory-safety defects survive long maintenance cycles.

This is a local-privilege flaw, not a remote entry point, so the risk is highest on multi-user or hostile-tenant OpenBSD systems where an attacker already holds a low-privilege account. Still, the depth of the bug and the strength of OpenBSD's security posture make it a notable research result.

Watch for the official errata and fixed kernel builds, backported patches for prior releases still in support, and any weaponization that combines this with a separate remote code execution entry bug.
