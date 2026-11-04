rule CyberStrikeAI_Implant_C2_Config
{
    meta:
        author = "Tia N. List"
        date = "2026-11-04"
        status = "experimental"
        description = "Hunts the CyberStrikeAI C2 implant documented by Kaspersky (November 2026): a conventional Go beacon that sends an X-Implant-Token HTTP header to attacker infrastructure (fastcdn.bar, media.fastcdn.bar, 185.186.245.144, 104.234.26.163). All LLM orchestration runs on the operator server, so a hit on these embedded artifacts indicates the implant or its configuration file. Derived from case analysis - NOT validated against a live sample."
        reference = "https://securelist.com/tr/cyberstrikeai-attacks/121715/ ; https://gbhackers.com/cyberstrikeai-framework/"
        falsepositives = "Unlikely - the token header name and the listed hosts are campaign-specific; a match means this implant family or its config is present"
    strings:
        $hdr_a = "X-Implant-Token" ascii nocase
        $hdr_b = "X-Implant-Token" wide nocase
        $c2_bar = "fastcdn.bar" ascii wide nocase
        $c2_ip1 = "185.186.245.144" ascii wide
        $c2_ip2 = "104.234.26.163" ascii wide
    condition:
        ($hdr_a or $hdr_b) and any of ($c2_*)
}
