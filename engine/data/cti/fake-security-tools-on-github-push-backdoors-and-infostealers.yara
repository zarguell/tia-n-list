rule Fake_Infosec_Tool_Repo_Loader {
    meta:
        author = "Tia N. List"
        date = "2026-11-08"
        status = "experimental"
        description = "Hunts artifacts of the GitHub campaign that ships malware in repositories posing as security tooling (Fscan output parser, scan automation, log analysis). Doctor Web documented PowerShell staging under C:\\Users\\Public\\Pictures and an Electron-based modular loader named Microsoft.exe that establishes persistence, disables Windows security and recovery features and injects the next stage. Derived from case analysis (Doctor Web) - NOT validated against a live sample."
        reference = "https://news.drweb.com/show/?c=5&i=15311&lng=en (BleepingComputer: https://www.bleepingcomputer.com/news/security/fake-security-tools-on-github-push-backdoors-and-infostealers/)"
        falsepositives = "Unlikely to match clean software; a hit means an attacker staging path or the campaign domains are present in the scanned object (repository archive, project file, or sample)."
    strings:
        $dom1 = "muckanthropic.com" ascii nocase
        $dom2 = "muckdeveloper.com" ascii nocase
        $ip1 = "130.12.182.172" ascii
        $stage_a = "\\Users\\Public\\Pictures" ascii nocase
        $stage_w = "\\Users\\Public\\Pictures" ascii wide nocase
        $loader_a = "Microsoft.exe" ascii nocase
        $loader_w = "Microsoft.exe" ascii wide nocase
    condition:
        ($dom1 or $dom2 or $ip1) or ((any of ($stage_*)) and (any of ($loader_*)))
}
