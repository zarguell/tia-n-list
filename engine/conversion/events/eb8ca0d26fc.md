Seqrite Labs documented a targeted campaign using region-specific lures: a Czech Social Security Administration appointment notice (ČSSZ) and a Traditional Chinese project review form. The infection chain delivers **AZUREVEIL**, a heavily modified Adaptix C2 agent with 36 post-exploitation commands, via a RUSTCLOAK loader that bypasses thread creation entirely using Windows fibers.

**Notable C2:** The malware communicates exclusively via Microsoft Azure Blob Storage with a SAS token valid March 2026 – March 2027. No direct C2 server — encrypted beacons and commands are exchanged through shared Azure containers, blending traffic with legitimate enterprise cloud activity. This mirrors the June 2 reported Operation Dragon Weave but with a refined fiber-based injection technique.

---
