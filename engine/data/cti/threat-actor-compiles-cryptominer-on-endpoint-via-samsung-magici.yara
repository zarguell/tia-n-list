rule MagicInfo_OnHost_Compiled_XMR_Miner {
    meta:
        author = "Tia N. List"
        date = "2026-09-25"
        status = "experimental"
        description = "Monero miner compiled on the victim host after CVE-2025-4632 exploitation of Samsung MagicINFO 9 Server: Silent XMR Miner Builder drives csc.exe/cvtres.exe/tcc.exe/cc1.exe/gcc.exe on the host, and the launched miner carries RandomX flags pointing at the c3pool mining gateway. The incident sample hashes to 0d202e16408770e8b6cceb14e1e3e72946b154bf881d27fe33d0060315b30dd1. Derived from case analysis (Huntress) — NOT validated against a live sample."
        reference = "https://www.huntress.com/blog/threat-actor-compiles-cryptominer"
        falsepositives = "Other Monero miners configured against the public c3pool gateway; combine with the tomcat9.exe process tree before acting"
    strings:
        $c2a = "auto.c3pool.org" ascii nocase
        $c2b = "194.87.89.30" ascii
        $c2c = "185.225.226.53" ascii
        $m1 = "Silent XMR Miner Builder" ascii nocase
        $m2 = "oldadministrator" ascii nocase
        $m3 = "F@x2020!@#" ascii
        $m4 = "rx/0" ascii
        $m5 = "donut.exe" ascii nocase
    condition:
        uint16(0) == 0x5a4d and ((any of ($c2*) and any of ($m*)) or 3 of ($m*))
}
