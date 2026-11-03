rule DarkBlinders_RuntimeBroker_Backdoor
{
    meta:
        author = "Tia N. List"
        date = "2026-11-03"
        status = "experimental"
        description = "Detects DarkBlinders (UNC5795) backdoor components: the RuntimeBroker.dll AppDomainManager loader and RuntimeBrokerApi.dll/PsProxy.dll second stage that poll the PeakyBlindersTeam GitHub repositories."
        reference = "https://dreamgroup.com/blog/darkblinders-inside-an-active-espionage-campaign"
        reference = "https://thehackernews.com/2026/11/darkblinders-compromises-israeli-target.html"
        falsepositives = "None expected; the PeakyBlindersTeam repository names and victim-identifier seed are campaign-specific"

    strings:
        $peaky_seed = "Peaky Blinders 2.1" ascii wide nocase
        $peaky_repo = "PeakyBlindersTeam" ascii wide nocase
        $peaky_lic = "myLic" ascii wide nocase
        $module_api = "RuntimeBrokerApi" ascii wide
        $module_proxy = "PsProxy.dll" ascii wide nocase

    condition:
        any of ($peaky_*) or all of ($module_*)
}
