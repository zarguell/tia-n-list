rule NuGet_FakeJobAssessment_OskSupport_Sideload {
    meta:
        author = "Tia N. List"
        date = "2026-11-26"
        status = "experimental"
        description = "MSBuild targets and staged artifacts from the 13 malicious NuGet packages that posed as WinUI 3 / WPF controls in fake .NET job assessments (Socket, November 2026). The campaign ships a repository-local restore source, a deliberately typo'd ForceExecuteNonExistenFile target that keeps the analyzer running on every build, and stages OskSupport.dll into %LOCALAPPDATA%\\osk\\ beside a copied osk.exe. Derived from published case analysis - NOT validated against a live sample."
        reference = "https://socket.dev/blog/malicious-nuget-packages-fake-job-assessments"
        falsepositives = "Benign .NET job-assessment repositories can reuse restore sources and shadow the msbuild property name; require at least two of the campaign strings and correlate with a dotnet.exe build that later starts osk.exe from the user profile"
    strings:
        $typo_target = "ForceExecuteNonExistenFile" ascii
        $sideload_dll = "OskSupport.dll" ascii nocase
        $restore_source = "RestoreAdditionalProjectSources" ascii
        $osk_dir = "\\osk\\OskSupport" ascii nocase
    condition:
        2 of them
}
