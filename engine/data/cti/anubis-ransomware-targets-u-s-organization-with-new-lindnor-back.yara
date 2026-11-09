rule Lindnor_Anubis_Backdoor_Artifacts {
    meta:
        author = "Tia N. List"
        date = "2026-11-09"
        status = "experimental"
        description = "Hunts the artifacts Symantec documented for Backdoor.Lindnor (Anubis ransomware intrusion): the backdoor DLL masquerading as a Chrome component (healthcontroller64.exe) or a VMware file (svchelper.exe), and the Anubis encryption payload's ransom notes (restore files.txt / restore files.html) alongside the .anubis extension. Derived from case analysis - NOT validated against a live sample."
        reference = "https://www.security.com/threat-intelligence/lindnor-new-backdoor-anubis-ransomware"
        falsepositives = "Backup or recovery tooling that writes literal 'restore files' notes, and unrelated software shipping a binary named healthcontroller64.exe or svchelper.exe; require the paired filenames or the .anubis marker before acting"
    strings:
        $note_txt = "restore files.txt" ascii nocase
        $note_html = "restore files.html" ascii nocase
        $ext = ".anubis" ascii nocase
        $bin_chrome = "healthcontroller64.exe" ascii nocase
        $bin_vmware = "svchelper.exe" ascii nocase
    condition:
        all of ($note_*) or ($ext and any of ($bin_*))
}
