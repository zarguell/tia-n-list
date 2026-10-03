rule TIKTouk_WordPress_Credential_Harvester {
    meta:
        author = "Tia N. List"
        date = "2026-10-03"
        status = "experimental"
        description = "TIKTOUK WordPress credential-collection toolkit components: the Python workers wp2s_poll.py and wp2s_crack.py and the stripped Go crawler jscrawl-amd64 pull targets from a central HTTP hub, probe WordPress REST batch routes, harvest exposed configuration files, and report back to /v1/ingest or /api/crack/report. Derived from case analysis (LevelBlue SpiderLabs) - NOT validated against a live sample."
        reference = "https://www.levelblue.com/blogs/spiderlabs-blog/tiktouk-tracing-a-wordpress-credential-collection-toolkit"
        falsepositives = "Vulnerability scanners and WordPress administration scripts referencing the same exposed-file paths or REST routes; require multiple toolkit markers before acting"
    strings:
        $toolkit_poll = "wp2s_poll.py" ascii nocase
        $toolkit_crack = "wp2s_crack.py" ascii nocase
        $toolkit_crawler = "jscrawl-amd64" ascii nocase
        $hub_ingest = "/v1/ingest" ascii
        $hub_report = "/api/crack/report" ascii
        $probe_batch = "http://:" ascii
        $probe_route = "wp/v2/block-renderer/core/paragraph" ascii
        $harvest_config = "wp-config.php.bak" ascii nocase
        $harvest_debug = "wp-content/debug.log" ascii nocase
    condition:
        any of ($toolkit*)
        or
        (
            any of ($hub*)
            and any of ($probe*)
            and any of ($harvest*)
        )
}
