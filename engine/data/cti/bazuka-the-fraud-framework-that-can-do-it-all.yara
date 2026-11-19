rule Bazuka_Android_Fraud_Framework
{
    meta:
        author = "Tia N. List"
        date = "2026-11-19"
        status = "experimental"
        description = "Bazuka modular Android fraud framework: the TikTok18+ themed dropper package, the ADB wireless-debugging bridge and the in-memory DEX modules (NFC relay, accessibility rebind) described by ThreatFabric. Derived from case analysis - NOT validated against a live sample."
        reference = "https://www.threatfabric.com/blogs/bazuka-the-fraud-framework-that-can-do-it-all"
        falsepositives = "Threat-intel write-ups, mobile sandbox reports and DEX dumps that quote the package or module names; require the package name together with a module marker before promoting"
    strings:
        $pkg = "com.tiktok.premium.pro" ascii
        $nfc = "tapread-nfc_module" ascii
        $a11y = "com.guidocool.cryptomanager.action.A11Y_REBIND" ascii
        $adb = "self_adb" ascii
    condition:
        ($pkg and 1 of ($nfc, $a11y, $adb)) or ($nfc and $a11y)
}
