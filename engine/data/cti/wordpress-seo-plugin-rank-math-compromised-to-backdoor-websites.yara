rule Rank_Math_Pro_Trojanized_Plugin_Backdoor
{
    meta:
        author = "Tia N. List"
        date = "2026-10-20"
        status = "experimental"
        description = "Trojanized Rank Math PRO 3.0.123 WordPress plugin files that beacon to rank1cdn.com and recreate hidden backdoors on page visits. Derived from case analysis (BleepingComputer, SecurityWeek, The Hacker News) - NOT validated against a live sample."
        reference = "https://www.bleepingcomputer.com/news/security/wordpress-seo-plugin-rank-math-compromised-to-backdoor-websites/"
        falsepositives = "Security tooling, honeypot captures, or threat-intel notes that quote the C2 domain; require the PHP marker (or plugin path) before acting on a hit"
    strings:
        $c2 = "rank1cdn.com" ascii nocase
        $php = "<?php" ascii
        $plugin_path = "rank-math-pro" ascii nocase
    condition:
        $c2 and ($php or $plugin_path)
}
