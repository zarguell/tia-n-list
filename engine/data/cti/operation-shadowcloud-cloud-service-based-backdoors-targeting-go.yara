rule GraphDoor_Operation_ShadowCloud {
    meta:
        author = "Tia N. List"
        date = "2026-11-18"
        status = "experimental"
        description = "Hunts the GraphDoor backdoor Kaspersky documented in Operation ShadowCloud (MD5 14ec33ea808e697870d00c5e434c2952): a PE that formats a PID-derived pipe name from the string \\\\.\\pipe\\p%lu, creates C:\\ProgramData\\Intel_Log\\<GUID>, and pulls scr.ts / pr.ts / kl.ts plug-ins for screenshots, process listing and keylogging. Derived from case analysis - NOT validated against a live sample."
        reference = "https://securelist.com/operation-shadowcloud-graphdoor/122005/ https://securelist.com/operation-shadowcloud-gitdoor/122004/"
        falsepositives = "Unlikely on its own: the pipe format string and Intel_Log staging path are specific to this implant, but a file that merely embeds the literal Intel_Log path will also match - require the PE header and review the sibling GUID directory"
    strings:
        $pipe_a = "\\\\.\\pipe\\p%lu" ascii
        $pipe_w = "\\\\.\\pipe\\p%lu" wide
        $intel_log = "Intel_Log" ascii wide
        $config_ini = "config.ini" ascii wide
        $plug_scr = "scr.ts" ascii
        $plug_pr = "pr.ts" ascii
        $plug_kl = "kl.ts" ascii
    condition:
        uint16(0) == 0x5A4D and ($pipe_a or $pipe_w) and ($intel_log or 2 of ($plug_*, $config_ini))
}
