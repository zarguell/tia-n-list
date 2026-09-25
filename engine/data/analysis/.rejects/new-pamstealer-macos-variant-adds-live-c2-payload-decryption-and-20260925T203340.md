A new PamStealer macOS variant decrypts its payload live from its command-and-control server instead of staging it on disk, and adds multi-layer persistence for survival across reboots and cleanups. The JXA dropper used for delivery was also updated with a new lure and delivery chain, per The Hacker News coverage of the change.

In-memory, C2-driven payload decryption complicates both static detection and forensics, since analysts recover samples only by interacting with live infrastructure. Layered persistence means a partial cleanup leaves the stealer running. The changes fit the broader trend of macOS infostealers maturing past the assumption that Mac malware is simple and short-lived.

Watch for published indicators of compromise and dropper samples as researchers dissect the variant, the lures used in the new delivery chain, and whether the live-decryption model spreads to other macOS stealer families.
