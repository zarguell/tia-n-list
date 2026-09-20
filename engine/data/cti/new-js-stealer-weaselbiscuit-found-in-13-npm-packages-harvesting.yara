rule WeaselBiscuit_npm_Stealer {
    meta:
        author = "Tia N. List"
        date = "2026-09-20"
        status = "experimental"
        description = "Detects WeaselBiscuit JavaScript stealer that harvests Chrome extension storage data, linked to DPRK Contagious Interview campaign"
        reference = "https://thehackernews.com, https://cyberworldops.com"
        falsepositives = "Legitimate npm packages accessing Chrome extension directories"
    strings:
        $ext1 = "Extension State" ascii
        $ext2 = "chrome/extensions" ascii
        $ext3 = "leveldb" ascii
        $ext4 = "IndexedDB" ascii
        $harvest1 = "Local Storage" ascii
        $harvest2 = "Session Storage" ascii
        $harvest3 = "cookies" ascii nocase
        $exfil1 = "XMLHttpRequest" ascii
        $exfil2 = "fetch(" ascii
        $exfil3 = "https://" ascii
    condition:
        (
            ($ext1 or $ext2 or $ext3 or $ext4) and
            2 of ($harvest*) and
            1 of ($exfil*)
        ) or
        (
            $ext2 and
            $harvest1 and
            $exfil3
        )
}
