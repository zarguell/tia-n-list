rule PapRAT_BITTER_Campaign_Markers
{
    meta:
        author = "Tia N. List"
        date = "2026-11-03"
        status = "experimental"
        description = "Detects PapRAT/WmRAT artifacts from the BITTER (TA397) campaign documented by FortiGuard: hardcoded command-and-control hosts and the MicrosoftUpdates/BiosUpdates scheduled-task names the implants create."
        reference = "https://www.fortinet.com/blog/threat-research/bitter-expands-its-arsenal-with-paprat"
        reference = "https://gbhackers.com/paprat-malware/"
        falsepositives = "None expected; the C2 paths and scheduled-task names are campaign-specific"

    strings:
        $c2_banana = "rivingtonclarks.com/banana" ascii nocase
        $c2_wmrat = "netmansrvdns.com" ascii wide nocase
        $task_updates = "MicrosoftUpdates\\updates11678" ascii wide nocase
        $task_bios = "BiosUpdates\\update101" ascii wide nocase

    condition:
        any of ($c2_*) or all of ($task_*)
}
