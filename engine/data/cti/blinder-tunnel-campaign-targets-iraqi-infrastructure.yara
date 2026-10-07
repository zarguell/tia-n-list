rule BlinderTunnel_ShelbyLoader_V2_Artifacts {
    meta:
        author = "Tia N. List"
        date = "2026-10-07"
        status = "experimental"
        description = "ShelbyLoader V2 artifacts of the Iran-nexus Blinder Tunnel campaign (CL-STA-1178): the hard-coded RC4 key used to decrypt the Chisel tunneling configuration, the Blackwood.dll.conf configuration filename, the weaponized Visual Studio recruitment-lure project file, the GitHub dead-drop resolver repositories, and the MicrosoftRuntime Run-key persistence value. Derived from case analysis (Unit 42) - NOT validated against a live sample."
        reference = "https://unit42.paloaltonetworks.com/blinder-tunnel-targets-critical-infrastructure/"
        falsepositives = "Red-team or research tooling reusing the GitHub dead-drop names; single strings alone are weak, require at least two indicators"
    strings:
        $rc4_key = "My name is Blackwood !" ascii
        $conf = "Blackwood.dll.conf" ascii nocase
        $csproj = "FlightManager.csproj" ascii nocase
        $dead_drop_1 = "peakyblinders-tm" ascii nocase
        $dead_drop_2 = "GreenBeret0" ascii nocase
        $run_value = "CurrentVersion\\Run\\MicrosoftRuntime" ascii
    condition:
        uint16(0) == 0x5A4D and 2 of them
}
