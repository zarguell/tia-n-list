rule Linux_AnnobinDoor_Sparrow_Agent
{
    meta:
        author = "Tia N. List"
        date = "2026-11-12"
        status = "experimental"
        description = "Hunts the Linux side of the CopperDragon Sparrow framework. Check Point Research documented the OceanGate cluster deploying AnnobinDoor (internally named annobinagent) and SparrowShell on compromised internet-facing Linux servers, loading plugins from /tmp alongside trojanized SSH/SSHD components. The strings below are the operator-facing internal names published in the report; derived from case analysis - NOT validated against a live sample."
        reference = "https://research.checkpoint.com/2026/not-all-that-glitters-is-gold-tracking-copperdragons-sparrow-framework-around-the-globe/"
        falsepositives = "Security research, YARA development and malware-analysis repositories that store the internal names as text; the ELF header requirement keeps plain-text notes from matching"
    strings:
        $annobin = "annobinagent" ascii nocase
        $sparrowshell = "sparrowshell" ascii nocase
        $sparrowdoor = "sparrowdoor" ascii nocase
    condition:
        uint32(0) == 0x464c457f and any of them
}
