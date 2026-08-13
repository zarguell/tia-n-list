rule DeadLock_Ransomware_Encryptor_Artifacts {
    meta:
        author = "Tia N. List"
        date = "2026-08-13"
        status = "experimental"
        description = "DeadLock ransomware (Rust-based encryptor, first observed July 2025, Microsoft Threat Intelligence Aug 2026): the dDlK footer magic embedded in encrypted files, the .dlock encrypted-file extension, the HOW_RECOVER text ransom note and RECOVERY_CHAT HTML recovery-chat names, and the leak-site domain family. Derived from Microsoft Threat Intelligence case analysis — NOT validated against a live sample."
        reference = "https://www.microsoft.com/en-us/security/blog/2026/08/10/deadlock-ransomware-breaking-down-a-rust-based-encryptor-with-decentralized-recovery-infrastructure/"
        falsepositives = "The .dlock extension and HOW_RECOVER/RECOVERY_CHAT note names are unique to DeadLock; dDlK magic and the leak domains are distinctive. Require the PE context plus at least two of the documented strings and corroborate with file/network telemetry"
    strings:
        $magic = "dDlK" ascii
        $ext = ".dlock" ascii nocase
        $note_txt = "HOW_RECOVER" ascii
        $note_html = "RECOVERY_CHAT" ascii
        $leak1 = "liveblog365.com" ascii nocase
        $leak2 = "deadlockblog" ascii nocase
    condition:
        uint16(0) == 0x5A4D and 2 of them
}
