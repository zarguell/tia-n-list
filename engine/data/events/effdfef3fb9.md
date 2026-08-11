Three Microsoft UEFI certificates from 2011 expire starting June 27, 2026, and organizations that do not migrate to the 2023 certificate family will silently lose the ability to update Secure Boot revocation lists — permanently freezing their systems' trust state and leaving them exposed to future bootkit attacks.

**Timeline:**

- **June 27:** Microsoft KEK CA 2011 (DB/DBX update authorization) expires; Microsoft UEFI CA 2011 (Linux shim, third-party bootloader signatures) expires.

- **October 2026:** Microsoft Windows Production PCA 2011 (Windows Boot Manager) expires.

Systems left on the 2011 chain will continue to boot, but will never learn to distrust bootkits (BootHole, BlackLotus, Bombshell) discovered after the KEK expires. **Detection gap:** Standard vulnerability scanners and EDR agents do not enumerate UEFI variables, leaving most organizations blind to which devices still hold expiring keys. **Action:** Apply OEM firmware updates (embedding 2023 keys) before relying on Windows Update migration.

---
