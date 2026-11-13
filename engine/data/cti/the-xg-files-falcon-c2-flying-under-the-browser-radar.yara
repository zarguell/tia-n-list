rule Falcon_XG_Browser_Implant_Artifacts {
    meta:
        author = "Tia N. List"
        date = "2026-11-13"
        status = "experimental"
        description = "Hunts Falcon (XG / Xiang Ge) browser C2 implant artifacts: the injected JavaScript served to compromised webmail and government portals and the companion Chrome extension directory. The markers are the extension ID mbidcmlcbgbphpoacojjbmfpohcimjji posing as 'PDF Viewer', the localStorage/cookie key Hm_lvt_$ (with a 2099 cookie expiry) that mimics Baidu Analytics, and the implant's storage keys popup_count, clipboard_replacer_rules and the remark field _domain_google_mark. The implant keeps a TLS WebSocket open and sends a {\"heartbeat\":\"1\"} beacon every minute. Derived from Unit 42 reporting - NOT validated against a live sample."
        reference = "https://unit42.paloaltonetworks.com/falcon-c2-browser-compromise/ ; https://blog.talosintelligence.com/china-nexus-uat-11587-targets-government-and-policy-organizations-across-asia-with-antino-backdoor/"
        falsepositives = "Threat-intel analysts or sandboxes that deliberately stage the reported extension ID and storage keys; pages that embed the same key names for unrelated telemetry. Requiring two of the distinctive implant keys, or the extension ID itself, keeps benign Baidu Analytics pages (which carry Hm_lvt_ alone) out of scope"
    strings:
        $ext_id = "mbidcmlcbgbphpoacojjbmfpohcimjji" ascii nocase
        $key_lvt = "Hm_lvt_$" ascii nocase
        $key_popup = "popup_count" ascii nocase
        $key_clip = "clipboard_replacer_rules" ascii nocase
        $key_mark = "_domain_google_mark" ascii nocase
        $heartbeat = "\"heartbeat\":\"1\"" ascii nocase
    condition:
        filesize < 5MB and ($ext_id or 2 of ($key_clip, $key_mark, $key_popup, $heartbeat) or ($key_lvt and $key_mark))
}
