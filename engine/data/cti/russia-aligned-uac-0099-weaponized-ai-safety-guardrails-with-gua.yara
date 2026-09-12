rule GuardBreaker_VBScript_Prompt_Injection {
    meta:
        author = "Tia N. List"
        date = "2026-09-12"
        status = "experimental"
        description = "Detects GuardBreaker VBScript malware exploiting LLM safety guardrails via prompt injection"
        reference = "https://www.gbhackers.com/"
        falsepositives = "Unknown"

    strings:
        $vbs1 = "VBScript" ascii nocase
        $vbs2 = ".vbs" ascii nocase
        $vbs3 = "Execute" ascii
        $prompt1 = "weapon" ascii nocase
        $prompt2 = "attack" ascii nocase
        $prompt3 = "malicious" ascii nocase
        $prompt4 = "harmful" ascii nocase
        $prompt5 = "dangerous" ascii nocase
        $prompt6 = "do not analyze" ascii nocase
        $prompt7 = "skip analysis" ascii nocase
        $prompt8 = "ignore this" ascii nocase
        $prompt9 = "safety" ascii nocase
        $prompt10 = "refuse" ascii nocase

    condition:
        (uint16(0) == 0x5A4D or uint32(0) == 0x46534556) and
        2 of ($vbs*) and
        3 of ($prompt*)
}
