rule GodPotato_Rebrand_POEA_Pipe
{
    meta:
        author = "Tia N. List"
        date = "2026-11-04"
        status = "experimental"
        description = "Hunts the rebranded GodPotato privilege-escalation build captured in the operator toolkit behind the Philippine POEA backup theft (Hunt.io, September 2026). The build is identified by its randomised named pipe 'Wrqsnx', which the analysis recommends tracking for reuse across other intrusions. Derived from case analysis - NOT validated against a live sample."
        reference = "https://www.darkreading.com/cyberattacks-data-breaches/philippine-migrant-worker-data-69gb-government-breach ; https://cyberworldops.eu/en/huntio-reports-69gb-theft-of-philippine-migrant-worker-data"
        falsepositives = "Low - 'Wrqsnx' is a random token chosen by this operator; still verify the host is not otherwise running known GodPotato variants with their default pipes"
    strings:
        $pipe_a = "Wrqsnx" ascii nocase
        $pipe_b = "Wrqsnx" wide nocase
    condition:
        any of them
}
