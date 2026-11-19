rule Overlord_RAT_UAT_12643
{
    meta:
        author = "Tia N. List"
        date = "2026-11-19"
        status = "experimental"
        description = "Go-based Overlord RAT implant used by UAT-12643, identified by its command mutex, its %APPDATA%\\MsgEdgeUpdate.exe copy and the Zoipers / MsgEdgeUpdate Run values it registers. Derived from Cisco Talos case analysis relayed by the desk - NOT validated against a live sample."
        reference = "https://malware.news/t/uat-12643-suspected-north-korea-aligned-actor-blends-blockchain-resilience-with-targeted-infostealing/127417"
        falsepositives = "Threat-intel notes, sandbox reports or YARA test corpora that quote the mutex or Run value names; require the mutex or the paired Run values before acting on a hit"
    strings:
        $mutex = "UuuRjinBZPBMIjnc" ascii
        $run_msg = "MsgEdgeUpdate" ascii
        $run_zoip = "Zoipers" ascii
        $builder = "win-8oa3ccqae4d" ascii
    condition:
        $mutex or ($run_msg and $run_zoip) or ($run_zoip and $builder)
}
