rule NIKKE_Launcher_K2F_Loader {
    meta:
        author = "Tia N. List"
        date = "2026/11/05"
        status = "experimental"
        description = "Tampered NIKKE PC launcher JavaScript loader and its K2F remote-access stage: the injected launcher script fetched code from insightjs.com and dropped the LuaJIT bundle insight.bundle, whose agent leaves the k2f_chan marker in Launcher/intl_service/debug.log alongside the persistence DLL platform_experience_helper.dll. Scans script and bundle text, not just PE files, because the tampered stage is JavaScript rendered inside the launcher's embedded Chromium. Derived from the MotherSphere technical analysis - NOT validated against a live sample."
        reference = "https://www.bleepingcomputer.com/news/security/nikke-pc-game-launcher-hacked-to-spread-remote-access-data-stealing-malware/"
        reference = "https://gist.github.com/MotherSphere/d6c049a09ba8ac3085c51ee9df24a4e5"
        falsepositives = "Launcher resource strings, patch notes or threat-intel write-ups that quote these names; require at least two of the documented strings and confirm the file lives in the launcher install or its tbs_cache directory before alerting"
    strings:
        $loader_host = "insightjs.com" ascii nocase
        $bundle_name = "insight.bundle" ascii nocase
        $channel = "k2f_chan" ascii nocase
        $persist_dll = "platform_experience_helper.dll" ascii nocase
    condition:
        2 of them
}
