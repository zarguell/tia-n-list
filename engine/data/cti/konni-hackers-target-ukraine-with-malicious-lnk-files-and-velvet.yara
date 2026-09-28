rule Konni_OperationConflictCompass_LNK_Lure {
    meta:
        author = "Tia N. List"
        date = "2026-09-28"
        status = "experimental"
        description = "Operation Conflict Compass (Konni / TA406 / Opal Sleet) artifacts against Ukraine-focused entities: the OneDriveUpdateScheduler scheduled task created by the staged VBScript and the Olesia Tsvientukh decoy-CV LNK lure delivered inside ZIP attachments; the task launches the VelvetCake PowerShell payload every minute. Derived from case analysis (SOCRadar) - NOT validated against a live sample."
        reference = "https://malware.news/t/konni-cv-olesiatsvientukh-socialresearcher-sociologist-qualitativelnk/125920#post_1"
        falsepositives = "Security research, sandboxes or red-team tooling embedding the same campaign artifact names; treat as a hunting signal, not a verdict"
    strings:
        $task = "OneDriveUpdateScheduler" ascii nocase
        $lure = "OlesiaTsvientukh_SocialResearcher_Sociologist_Qualitative" ascii nocase
    condition:
        any of them
}
