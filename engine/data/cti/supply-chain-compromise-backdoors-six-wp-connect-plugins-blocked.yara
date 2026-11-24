rule WPConnect_Plugin_TascreditPay_C2_Backdoor {
    meta:
        author = "Tia N. List"
        date = "2026-11-24"
        status = "experimental"
        description = "Hunts the PHP remote-control module embedded in the backdoored WP connect WordPress plugin builds published on 22 November 2026 (CVE-2026-135202): a WP-Cron task that posts site URL, PHP/WordPress/OS versions and the server user to tascredit-pay.com and then executes PHP returned by that server. Derived from case analysis (Wordfence, CVE record) - NOT validated against a live sample, so a hit means a plugin file carries the reported C2 host alongside WordPress HTTP/cron plumbing and should be read before it is trusted."
        reference = "https://wordfence.com/blog/2026/11/supply-chain-compromise-backdoors-six-wp-connect-plugins-blocked-by-wordpress-orgs-release-hold - https://www.cve.org/CVERecord?id=CVE-2026-135202 - https://securityonline.info/wordpress-plugin-backdoor-cve-2026-135202/"
        falsepositives = "Quarantine, sandbox or malware-research copies of the malicious plugin builds; site backups and archival tarballs of the November 2026 releases; an analyst fixture that quotes the domain next to WordPress HTTP API calls"
    strings:
        $c2 = "tascredit-pay.com" ascii nocase
        $http = "wp_remote_post" ascii
        $http_get = "wp_remote_get" ascii
        $cron = "wp_schedule_event" ascii
    condition:
        $c2 and 1 of ($http, $http_get, $cron)
}
