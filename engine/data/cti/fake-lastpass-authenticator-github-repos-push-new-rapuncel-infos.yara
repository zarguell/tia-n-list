import "hash"

rule Rapuncel_EDR_Killer_Driver {
    meta:
        author = "Tia N. List"
        date = "2026-09-20"
        status = "experimental"
        description = "Detects Rapuncel infostealer EDR-killing kernel driver (Alinubx.sys disguised as nvfsflt64.sys) that terminates 145 AV/EDR processes via ObOpenObjectByPointer"
        reference = "https://www.lastpass.com, https://www.bleepingcomputer.com"
        falsepositives = "Legitimate NVIDIA filesystem filter driver"
        hash = "8d50036510859956d20d1f50e43171be53417431104c6befb1352ff5187c248a"
    strings:
        $svc = "NvFsFilter" ascii nocase
        $driver = "nvfsflt64.sys" ascii nocase
        $real = "Alinubx" ascii nocase
        $edr1 = "MsMpEng.exe" ascii nocase
        $edr2 = "ekrn.exe" ascii nocase
        $edr3 = "bdagent.exe" ascii nocase
        $edr4 = "cb.exe" ascii nocase
        $edr5 = "crowdstrike" ascii nocase
    condition:
        uint16(0) == 0x5A4D and
        ($svc or $driver or $real) and
        3 of ($edr*)
}

rule Rapuncel_Infostealer_DLL {
    meta:
        author = "Tia N. List"
        date = "2026-09-20"
        status = "experimental"
        description = "Detects Rapuncel infostealer DLL sideloaded via renamed vsdbg.exe"
        reference = "https://www.lastpass.com"
        falsepositives = "Legitimate Visual Studio debugger"
    strings:
        $steal1 = "cookies" ascii nocase
        $steal2 = "passwords" ascii nocase
        $steal3 = "credentials" ascii nocase
        $side1 = "vsdbg.dll" ascii nocase
    condition:
        uint16(0) == 0x5A4D and
        $side1 and
        2 of ($steal*)
}
