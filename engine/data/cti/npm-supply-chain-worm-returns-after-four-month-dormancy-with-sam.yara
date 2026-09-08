rule ShaiHulud_NPM_Worm_Payload {
  meta:
    author = "Tia N. List"
    date = "2026-09-08"
    status = "experimental"
    description = "Detects the Shai-Hulud npm supply-chain worm payload. The malware harvests npm tokens, GitHub tokens, cloud credentials, SSH keys, and CI/CD secrets from compromised development environments."
    reference = "https://gbhackers.com/known-npm-worm-returns-after-111-days-and-security-scanning-still-let-it-through/"
    falsepositives = "None expected; payload hash e37e3ddeeaaa9e0c4fdbcb829b4895a6521031c80053fc436625b61e6ee5b1a6 is known malicious"
  strings:
    $s1 = "npm_token" ascii
    $s2 = "github_token" ascii
    $s3 = "ssh_keyscan" ascii
    $s4 = "docker_config" ascii
    $s5 = "ci_cd" ascii nocase
    $hook = "preinstall" ascii
    $bun = "bun run index.js" ascii
  condition:
    $hook and $bun and 3 of ($s*)
}
