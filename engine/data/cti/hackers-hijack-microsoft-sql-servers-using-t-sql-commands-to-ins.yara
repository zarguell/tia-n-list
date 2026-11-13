rule SQLServer_Naabu_Loader_C2_Domain {
    meta:
        author = "Tia N. List"
        date = "2026-11-13"
        status = "experimental"
        description = "Hunts the UPX-packed Go loader named dllhost.exe used by the October 2026 Microsoft SQL Server campaign. The stage-one binary embeds the Naabu v2 port scanner and carries the hardcoded command-and-control URL hxxp://site.vietnam852[.]com:88/ip.php, from which it retrieves the target range before installing Gh0st RAT and a Monero miner. The rule matches the embedded C2 hostname in ASCII or UTF-16 form, so it catches the loader on disk or in memory regardless of packing. Derived from published campaign reporting (GBHackers, FortiGuard) - NOT validated against a live sample."
        reference = "https://gbhackers.com/microsoft-sql-servers-hijacked/ ; https://www.techfinitive.com/weak-passwords-and-sql-used-in-gh0st-rat-attack-against-microsoft-users/"
        falsepositives = "Threat-intel or forensic tooling that stores the reported C2 hostname in a notes file, PCAP-derived text dump or analysis report; sandbox artifacts that quote the indicator"
    strings:
        $c2_ascii = "site.vietnam852.com" ascii nocase
        $c2_wide = "site.vietnam852.com" wide nocase
    condition:
        any of them
}
