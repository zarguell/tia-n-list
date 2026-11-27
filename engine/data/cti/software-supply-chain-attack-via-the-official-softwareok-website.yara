rule SoftwareOK_Trojanized_Installer_DSV2_PythonRAT
{
    meta:
        author = "Tia N. List"
        date = "2026-11-27"
        status = "experimental"
        description = "Strings from the DSV2 Python RAT stage delivered by trojanized Q-Dir and DesktopOK installers on SoftwareOK's official download and update paths (ASEC, November 2026). The wrapper executes the genuine signed utility from C:/Users/Public, fetches 7zr.exe and dsv2_py39_agent.7z, installs a Python RAT under C:/ProgramData/Microsoft/DeviceSync/b2 and beacons to 8.210.69.51:9876. Derived from published case analysis - NOT validated against a live sample."
        reference = "https://asec.ahnlab.com/en/96827/"
        falsepositives = "Unlikely in ordinary software: the campaign strings only appear together in the wrapper scripts, the dropped archive and the Python RAT. A single match on DeviceSyncUpdate_b2 alone should be reviewed against the file path and parent process before alerting"
    strings:
        $archive = "dsv2_py39_agent" ascii nocase
        $client = "py_client_dsv2.py" ascii nocase
        $runkey = "DeviceSyncUpdate_b2" ascii
        $guardlog = "vmbt_guard.log" ascii nocase
        $installlog = "Py39_install.log" ascii nocase
    condition:
        2 of them
}

rule SoftwareOK_Dropper_SevenZip_Stager
{
    meta:
        author = "Tia N. List"
        date = "2026-11-27"
        status = "experimental"
        description = "Detects the intermediate stager used by the trojanized SoftwareOK installers, which drops 7zr.exe next to dsv2_py39_agent.7z and then extracts the Python RAT into DeviceSync directories. Intended for scanning installer wrappers, dropped archives and staging directories rather than whole-disk scans."
        reference = "https://thehackernews.com/2026/11/hackers-trojanize-official-q-dir-and.html"
        falsepositives = "Legitimate 7-Zip redistribution bundles 7zr.exe; require the dsv2_py39_agent archive name or the DeviceSync staging path alongside it"
    strings:
        $archive = "dsv2_py39_agent" ascii nocase
        $sevenzip = "7zr.exe" ascii
        $stagepath = "Microsoft\\DeviceSync\\b2" ascii
        $taskname = "\\UPnp\\MicrosoftEdge_dcntel" ascii
    condition:
        $archive and any of ($sevenzip, $stagepath, $taskname)
}
