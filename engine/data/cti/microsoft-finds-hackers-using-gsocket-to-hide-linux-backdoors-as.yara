rule Linux_AnnobinDoor_Sparrow_Agent
{
    meta:
        author = "Tia N. List"
        date = "2026-11-12"
        status = "experimental"
        description = "Hunts the Linux side of the CopperDragon Sparrow framework. Check Point Research documented OceanGate deploying AnnobinDoor (internally named annobinagent) and SparrowShell on compromised internet-facing Linux servers, loading plugins from /tmp, alongside trojanized SSH/SSHD components. The strings below are the operator-facing internal names published in the report; derived from case analysis - NOT validated against a live sample."
        reference = "https://research.checkpoint.com/2026/not-all-that-glitters-is-gold-tracking-copperdragons-sparrow-framework-around-the-globe/ (Melofee rootkit context: https://blog.exatrack.com/melofee/)"
        falsepositives = "Security research, YARA development and malware-analysis repositories that store the internal names as text; the ELF header requirement keeps plain-text notes from matching"
    strings:
        $annobin = "annobinagent" ascii nocase
        $sparrowshell = "sparrowshell" ascii nocase
        $sparrowdoor = "sparrowdoor" ascii nocase
    condition:
        uint32(0) == 0x464c457f and any of them
}

rule Linux_GSocket_Relay_Client
{
    meta:
        author = "Tia N. List"
        date = "2026-11-12"
        status = "experimental"
        description = "Hunts GSocket / gs-netcat ELF binaries on Linux hosts. Microsoft Security Research reported unrelated actors installing this open-source relay client after web-application RCE to hold an encrypted, NAT-traversing channel that survives patching; it masquerades with kernel-thread-like process names and persists via cron, systemd units and shell startup files. GSocket is legitimate software, so a hit is a triage lead rather than proof of compromise. Derived from case analysis - NOT validated against a live sample."
        reference = "https://www.microsoft.com/en-us/security/blog/2026/11/11/global-socket-how-threat-actors-weaponizing-gsocket-stealthy-c2/"
        falsepositives = "Legitimate administrative use of GSocket/gs-netcat for NAT-traversing shell access, and lab or CTF images where the tool is deliberately installed"
    strings:
        $env_args = "GSOCKET_ARGS" ascii
        $state_dir = "/.gsocket" ascii
        $bin_name = "gs-netcat" ascii
        $relay_name = "gsocket" ascii nocase
    condition:
        uint32(0) == 0x464c457f and (($env_args and $state_dir) or ($bin_name and $relay_name))
}
