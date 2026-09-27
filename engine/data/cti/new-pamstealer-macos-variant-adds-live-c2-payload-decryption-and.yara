rule PamStealer_Wavel_MacClient {
    meta:
        author = "Tia N. List"
        date = "2026-09-27"
        status = "experimental"
        description = "PamStealer Wavel-variant macOS infostealer (Jamf Threat Labs, September 22, 2026): live X25519 key exchange with the C2 host wavel.apple03cloudstore.com, the pkgunpack ECIES decryption utility, and the Swift second stage identified as MacClient / r8afup9un0. Derived from case analysis - NOT validated against a live sample."
        reference = "https://www.jamf.com/blog/pamstealer-wavel-macos-infostealer/"
        falsepositives = "Any file embedding the C2 domain (IOC lists, sandbox reports, blocklists) can match on $c2 alone - corroborate with network and persistence telemetry; the second-stage branch requires r8afup9un0 together with MacClient or pkgunpack"
    strings:
        $c2 = "wavel.apple03cloudstore.com" ascii nocase
        $stage = "r8afup9un0" ascii nocase
        $client = "MacClient" ascii nocase
        $decrypt = "pkgunpack" ascii nocase
    condition:
        $c2 or ($stage and ($client or $decrypt))
}
