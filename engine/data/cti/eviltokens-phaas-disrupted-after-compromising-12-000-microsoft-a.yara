rule EvilTokens_Phishing_Kit_Pages {
    meta:
        author = "Tia N. List"
        date = "2026-09-29"
        status = "experimental"
        description = "EvilTokens (Storm-2992) device-code phishing landing pages: the kit's REST endpoints, the anti-bot header it injects, the Microsoft refresh-token cookie it mints, and the Cloudflare Workers tracking-host naming scheme. Derived from case analysis (Sekoia, Unit 42, Microsoft) — NOT validated against a live sample."
        reference = "https://www.sekoia.com/blog/new-widespread-eviltokens-kit-device-code-phishing-as-a-service-part-1"
        falsepositives = "Analyst sandbox detonation of captured lures; pages served through security-product URL rewriting"
    strings:
        $api_start = "/api/device/start" ascii nocase
        $api_prt_convert = "/api/prt/convert" ascii nocase
        $api_prt_cookie = "/api/prt/cookie" ascii nocase
        $hdr_antibot = "X-Antibot-Token" ascii nocase
        $cookie_prt = "x-ms-RefreshTokenCredential" ascii nocase
        $workers_pattern = "-s-account.workers.dev" ascii nocase
    condition:
        3 of them
}
