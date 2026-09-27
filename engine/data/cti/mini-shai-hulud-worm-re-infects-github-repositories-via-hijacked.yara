rule Mini_Shai_Hulud_GitHub_Actions_Reinfection
{
    meta:
        author = "Tia N. List"
        date = "2026-09-27"
        status = "experimental"
        description = "Detects artifacts of the Mini Shai-Hulud worm re-infection: CI payload strings (C2 domain, command-search tag, backdoor name) and workflows pinned to the hijacked actions-cool GitHub Actions that re-executed the payload after September 16 2026"
        reference = "https://socket.dev/blog/mini-shai-hulud-actions"
        reference = "https://safedep.io/mini-shai-hulud-reinfection-github-repositories"
        falsepositives = "Legitimate repositories that legitimately reference the same domain, tag, or actions-cool actions"
    strings:
        $c2 = "t.m-kosche.com" ascii nocase
        $tag = "firedalazer" ascii nocase
        $kitty = "kitty-monitor" ascii nocase
        $action_helper = "actions-cool/issues-helper" ascii nocase
        $action_comment = "actions-cool/maintain-one-comment" ascii nocase
    condition:
        2 of them
}
