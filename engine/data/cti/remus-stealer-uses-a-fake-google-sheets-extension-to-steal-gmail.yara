rule Remus_Google_Sheets_Extension_Stealer
{
    meta:
        author = "Tia N. List"
        date = "2026-11-25"
        status = "experimental"
        description = "Remus Stealer Chrome extension masquerading as Google Sheets (v0.5.4) that reads Gmail through the victim's existing session and posts messages to prem1um.onl/m. Matches the unpacked extension bundle or its cached copies inside a Chrome profile. Derived from case analysis (Invoke RE, Hudson Rock) — NOT validated against a live sample."
        reference = "https://x.com/InvokeReversing/status/2125264524995645745"
        falsepositives = "Unlikely — the extension ID and collector host are campaign-specific; a benign Google Sheets extension uses a different ID"
    strings:
        $ext_id = "cfmepkojgnkahbmgablgdahdomjdppgf" ascii nocase
        $c2 = "prem1um.onl" ascii nocase
        $endpoint = "prem1um.onl/m" ascii nocase
        $campaign = "d7e027cf1c9989bd45ceeb3429e49cf5" ascii nocase
        $state = "mailForwardingV1" ascii
        $alarms = "chrome.alarms" ascii
        $atom = "gmail.com/feed/atom" ascii nocase
    condition:
        $ext_id or ($c2 and any of ($state, $alarms, $atom)) or ($endpoint and $campaign)
}
