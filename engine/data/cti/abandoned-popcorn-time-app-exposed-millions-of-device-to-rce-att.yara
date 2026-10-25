rule Time4Popcorn_Hijacked_Updater_CVE_2026_30612 {
    meta:
        author = "Tia N. List"
        date = "2026-10-25"
        status = "experimental"
        description = "Hunts the abandoned Time4Popcorn (Popcorn Time fork) updater components behind CVE-2026-30612: the unencrypted HTTP updater that polled the dead popcorntimeupd.xyz update domain and executed downloaded binaries with no signature check, its Windows service ('Update service') and macOS privileged helper (PT.updd). Derived from case analysis (Eye Security, Operation IXIM) - NOT validated against a live sample."
        reference = "https://labs.eye.security/cve-2026-30612-a-vulnerability-in-time4popcorn-popcorntime/ (Operation IXIM write-up: https://labs.eye.security/operation-ixim-preventing-a-botnet-of-millions-of-popcorn-time-users/)"
        falsepositives = "Legacy and abandoned Popcorn Time forks legitimately embed the same update host and service name; a hit means an exposed or already-hijacked updater is present, not that attacker tooling was found"
    strings:
        $upd_host = "popcorntimeupd.xyz" ascii nocase
        $upd_host_wide = "popcorntimeupd" ascii wide nocase
        $helper = "PT.updd" ascii nocase
        $app_a = "Time4Popcorn" ascii nocase
        $app_b = "Time4Popcorn" ascii wide nocase
        $svc = "Update service" ascii wide nocase
    condition:
        ($upd_host or $upd_host_wide or $helper) and any of ($app_*, $svc)
}
