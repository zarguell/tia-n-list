rule DPRK_XCTDH_HashHiding_JS_Payload {
    meta:
        author = "Tia N. List"
        date = "2026-09-29"
        status = "experimental"
        description = "JavaScript/Node.js payload of the DPRK-linked XCTDH HashHiding campaign: the base-91, control-flow-flattened _Z module decoded from the C2 /init response that decodes a C2 endpoint from Ethereum recipient-address bytes. Keys on the campaign marker, decode substrings, campaign marker string and operator signal-wallet prefix published by Ransom-ISAC and OpenSourceMalware. Derived from case analysis - NOT validated against a live sample."
        reference = "https://ransom-isac.org/blog/xctdh-adopts-hash-hiding/"
        falsepositives = "Threat-intelligence writeups, YARA repositories and sandbox reports that quote these indicator strings verbatim; confirm the file is executable JavaScript on a developer host before acting"
    strings:
        $marker = "RS260605" ascii
        $campaign = "global.i = '5-3-132'" ascii nocase
        $decode = ".to.substring(2,10)" ascii
        $wallet = "33ff3edaf55a8e03dcbc7cb40d498a49" ascii nocase
        $boot = "/$/boot" ascii
    condition:
        3 of them
}
