rule VOLTA_AUTODOXER_Infostealer
{
    meta:
        author = "Tia N. List"
        date = "2026-11-02"
        status = "experimental"
        description = "Hunts the VOLTA-AUTODOXER Windows infostealer described by Cisco Talos: a self-deleting stealer that collects browser credentials, OAuth tokens, cookies, cards, seed phrases and messenger sessions, packs the evidence bundle as volta_dox.zip with an LLM-written dossier AI_Analysis.txt, and ships it to a Telegram channel. The malware calls OpenRouter-hosted models (Claude Opus 4.6 by default, Kimi K2 and Gemini 2.5 Flash as fallbacks). Derived from case analysis and reporting - NOT validated against a live sample, and the strings are named artifacts rather than unique binary markers."
        reference = "https://thehackernews.com/2026/11/new-volta-infostealer-uses-claude.html https://www.wired.com/story/kernel-panic-volta-autodoxer-ai-infostealer-malware/ https://gbhackers.com/volta-infostealer/"
        falsepositives = "Security research, sandbox detonation notes, or analyst documentation that quotes the family name and its output filenames; the OpenRouter endpoint alone is legitimate developer traffic. Match on the self-name or on the archive plus report pair, not on the gateway string by itself."
    strings:
        $name = "VOLTA-AUTODOXER" ascii nocase
        $name_alt = "VOLTA_AUTODOXER" ascii nocase
        $report = "AI_Analysis.txt" ascii nocase
        $archive = "volta_dox.zip" ascii nocase
        $gateway = "openrouter.ai" ascii nocase
    condition:
        $name or $name_alt or ($report and $archive) or ($archive and $gateway)
}
