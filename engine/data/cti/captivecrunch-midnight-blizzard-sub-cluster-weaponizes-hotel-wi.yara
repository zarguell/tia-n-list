rule CaptiveCrunch_CornFlake_ChocoShell {
    meta:
        author = "Tia N. List"
        date = "2026-08-12"
        status = "experimental"
        description = "CornFlake Go RAT and ChocoShell infostealer from the CaptiveCrunch campaign (Storm-2945 / Midnight Blizzard): fake-update dropper UI text, Cloud Sync Service persistence name (svchost32.exe), and masquerading Microsoft 365 C2 infrastructure. Derived from Microsoft Threat Intelligence case analysis — NOT validated against a live sample."
        reference = "https://www.microsoft.com/en-us/security/blog/2026/07/31/captivecrunch-midnight-blizzard-targets-travelers-worldwide-for-malware-delivery-and-credential-theft/"
        falsepositives = "Windows Update and installer UX commonly display 'Don't turn off your computer' and generic sync services use similar branding; require the PE context plus at least two of the documented strings and corroborate with process/network telemetry"
    strings:
        $update_ui = "Don't turn off your computer" ascii
        $service_name = "Cloud Sync Service" ascii
        $svc_bin = "svchost32" ascii
        $c2_domain1 = "ms365-device.com" ascii nocase
        $c2_domain2 = "ms365-live.com" ascii nocase
        $c2_ip = "213.145.86.112" ascii
    condition:
        uint16(0) == 0x5A4D and 2 of them
}
