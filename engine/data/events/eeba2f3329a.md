Just one day after publishing RoguePlanet, the researcher operating as MSNightmare/Nightmare Eclipse (now "Chaotic Eclipse") released **GreatXML** — a BitLocker bypass that exploits the Windows Recovery Environment state left behind after Microsoft Defender Offline Scan runs on a system. The exploit uses a planted `unattend.xml` plus a modified `Recovery` directory at the root of the recovery partition. Any subsequent reboot into WinRE (via Shift+Restart from the lock screen) spawns an unrestricted shell with full access to the BitLocker-encrypted volume — no credentials required. Verified on Windows 11 24H2 with BitLocker active.

**Key implications:**

- **Precondition:** A Defender offline scan must have been run on the target at any prior point — triggering the vulnerable WinRE state.

- **Post-compromise persistence tool:** Requires admin rights to plant the files, but once planted, the bypass survives credential rotation, incident response, and loss of remote access. The attacker can return with physical access and unlock the disk.

- **No CVE, no patch.** This is the eighth tool from the Nightmare Eclipse cluster in roughly 10 weeks, and the second BitLocker bypass after YellowKey.

- **RoguePlanet context:** Also published this week (June 10), RoguePlanet is a separate LPE granting SYSTEM via a Microsoft Defender TOCTOU race condition on fully patched Windows 10/11. Not yet patched.

**Action:** Monitor for unexpected files at recovery partition root (`unattend.xml`, modified `Recovery/` directory). Organizations with high-value laptops should consider physical security controls and post-boot integrity verification.

---
