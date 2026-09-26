rule ClickFix_PlaceholderDomain_ThirdPartyCom {
    meta:
        author = "Tia N. List"
        date = "2026-09-26"
        status = "experimental"
        description = "ClickFix lure attributed to the third-party[.]com placeholder domain: a clipboard PowerShell one-liner and second-stage download artifacts (elxxvvx[.]xyz/f, update2.zip) documented by Manifold Security, BleepingComputer and VirusTotal. Derived from case analysis — NOT validated against a live sample."
        reference = "https://www.bleepingcomputer.com/news/security/placeholder-domain-used-in-dev-docs-now-serves-clickfix-attacks/"
        falsepositives = "Researchers, sandboxes or red teams reproducing the published ClickFix chain; combine with the fake Cloudflare verification page and Win+R execution context before acting"
    strings:
        $cmd1 = "Write-Host(&{iex(irm('" ascii nocase
        $cmd2 = "iex(irm('" ascii nocase
        $cmd3 = "Verify you are human" ascii nocase
        $stage1 = "elxxvvx" ascii nocase
        $stage2 = "update2.zip" ascii nocase
    condition:
        (any of ($cmd*) and any of ($stage*)) or 2 of ($stage*)
}
