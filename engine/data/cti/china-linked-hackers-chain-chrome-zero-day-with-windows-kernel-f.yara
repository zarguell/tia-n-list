import "pe"

rule China_APT_GRIMWEDGE_Backdoor {
    meta:
        author = "Tia N. List"
        date = "2026-09-12"
        status = "experimental"
        description = "Detects GRIMWEDGE JScript backdoor deployed by China-linked APT31/JungleBamboo"
        reference = "https://gbhackers.com/"
        falsepositives = "Unknown"

    strings:
        $name1 = "GRIMWEDGE" ascii nocase
        $name2 = "grimwedge" ascii
        $name3 = "LONGTALE" ascii nocase
        $name4 = "longtale" ascii
        $jscript = "JScript" ascii
        $wscript = "WScript" ascii
        $eval = "eval(" ascii
        $create = "CreateObject" ascii
        $shell = "WScript.Shell" ascii
        $fso = "Scripting.FileSystemObject" ascii

    condition:
        uint16(0) == 0x5A4D and
        filesize < 20MB and
        1 of ($name*) and
        2 of ($jscript, $wscript, $eval, $create, $shell, $fso)
}
