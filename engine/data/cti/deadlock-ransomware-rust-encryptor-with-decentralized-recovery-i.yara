rule DeadLock_Ransomware {
    meta:
        author = "Tia N. List"
        date = "2026-08-11"
        status = "experimental"
        description = "Rust-based encryptor with decentralized recovery infrastructure. Pre-encryption routine disables Windows Defender, deletes backups, clears event logs; geofences RU/BY/UA/CIS plus IR/SY/OM/YE locales. Derived from case analysis — NOT validated against a live sample."
        reference = "https://www.microsoft.com/en-us/security/blog/2026/08/10/deadlock-ransomware-breaking-down-a-rust-based-encryptor-with-decentralized-recovery-infrastructure/"
        falsepositives = "Legitimate backup/admin tooling bundling the same command strings is possible; treat as a hunting signal, not a verdict"
    strings:
        $vssadmin = "vssadmin" ascii nocase
        $shadows = "delete shadows" ascii nocase
        $wbadmin = "wbadmin" ascii nocase
        $wevtutil = "wevtutil" ascii nocase
        $windefend = "WinDefend" ascii nocase
        $setmp = "Set-MpPreference" ascii nocase
    condition:
        uint16(0) == 0x5A4D and 2 of ($vssadmin, $shadows, $wbadmin, $wevtutil, $windefend, $setmp)
}
