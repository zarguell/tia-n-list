rule GhostFrame_ESXi_Implant_TAG218 {
    meta:
        author = "Tia N. List"
        date = "2026-11-11"
        status = "experimental"
        description = "Hunts the GhostFrame post-exploitation implant (vmhostd-core) that Recorded Future's Insikt Group attributed to TAG-218, a cluster overlapping Settra ransomware. The ELF implant persists at /opt/vmhostd-core by rewriting /etc/rc.local.d/local.sh and exposes remote-shell, SOCKS5 proxy (gfsox), credential-interception (sdkmon) and VMkatz credential-theft components. Derived from case analysis - NOT validated against a live sample."
        reference = "https://www.recordedfuture.com/blog/ghostframe-esxi-implant-settra-ransomware"
        falsepositives = "Low for /opt/vmhostd-core; the short component names (gfsox, sdkmon, VMkatz) only score when combined with an ELF header and the implant path or binary name"
    strings:
        $install_dir = "/opt/vmhostd-core" ascii
        $implant_name = "vmhostd-core" ascii
        $implant_name_wide = "vmhostd-core" wide
        $rc_local = "/etc/rc.local.d/local.sh" ascii
        $gfsox = "gfsox" ascii
        $sdkmon = "sdkmon" ascii
        $vmkatz = "VMkatz" ascii
    condition:
        (uint32(0) == 0x464c457f) and
        (
            $install_dir or
            $rc_local or
            (($implant_name or $implant_name_wide) and any of ($gfsox, $sdkmon, $vmkatz))
        )
}
