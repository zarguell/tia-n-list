rule StarBlizzard_RedFlick_CosmicPulse {
    meta:
        author = "Tia N. List"
        date = "2026-10-02"
        status = "experimental"
        description = "Artifacts of the Star Blizzard (FSB Centre 18) RedFlick infection chain used to install the CosmicPulse Python backdoor: the three maintenance-lookalike scheduled task names installed by the chain MSI, the SecureDNSObserver task from the earlier URC-2026 lure, the HKCU registry staging key, and documented WebDAV/C2 infrastructure. Derived from Microsoft Threat Intelligence and Digital Security Lab Ukraine case analysis — NOT validated against a live sample."
        reference = "https://www.microsoft.com/en-us/security/blog/2026/09/29/star-blizzard-refines-phishing-and-malware-delivery-with-the-redflick-technique/"
        falsepositives = "Network Configuration Manager and System Health Monitor are generic task names used by legitimate tooling; require at least two matched strings and corroborate with process or network telemetry"
    strings:
        $task1 = "Internet Quality Test Connection" ascii nocase
        $task2 = "Network Configuration Manager" ascii nocase
        $task3 = "System Health Monitor" ascii nocase
        $task4 = "SecureDNSObserver" ascii
        $reg1 = "Software\\Classes\\.mollis" ascii nocase
        $c2a = "103.245.213.217" ascii
        $c2b = "89.125.66.183" ascii
        $c2c = "103.160.59.97" ascii
        $dom1 = "secure-dns-hub.com" ascii nocase
    condition:
        2 of ($task*) or (any of ($task*) and 2 of ($reg1, $c2a, $c2b, $c2c, $dom1))
}
