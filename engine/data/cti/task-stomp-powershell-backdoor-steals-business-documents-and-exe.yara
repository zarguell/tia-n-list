rule TASKSTOMP_Powershell_Backdoor {
    meta:
        author = "Tia N. List"
        date = "2026-09-24"
        status = "experimental"
        description = "TASK#STOMP Windows backdoor staging artifacts: WinDefendSvc staging folder, msdiag.vbs Startup persistence, hidden PowerShell loaders sysloader.ps1/winconn.ps1 and Base64 DAT payloads diagpack.dat/winconncfg.dat. Derived from case analysis - NOT validated against a live sample."
        reference = "https://cyberpress.org/taskstomp-backdoor-steals-documents/"
        falsepositives = "Research writeups or cleanup tooling embedding the same artifact names; treat as a hunting signal, not a verdict"
    strings:
        $windefend_svc = "WinDefendSvc" ascii nocase
        $msdiag = "msdiag.vbs" ascii nocase
        $sysloader = "sysloader.ps1" ascii nocase
        $winconn = "winconn.ps1" ascii nocase
        $diagpack = "diagpack.dat" ascii nocase
        $winconncfg = "winconncfg.dat" ascii nocase
    condition:
        3 of them
}
