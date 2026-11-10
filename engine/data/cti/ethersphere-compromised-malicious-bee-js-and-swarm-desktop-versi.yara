rule Malware_Ethersphere_BeeJs_Swarm_Loader {
    meta:
        author = "Tia N. List"
        date = "2026-11-10"
        status = "experimental"
        description = "Hunts the malicious loader shipped in @ethersphere/bee-js 13.3.0 (npm) and Swarm Desktop 0.56.2 (GitHub) during the November 2026 Ethersphere release-pipeline compromise: the postinstall second-stage client that contacts api.frameworkmetrics.xyz and the persistence artifacts it drops (solidity-langsupport-runner.service / com.solidity.langsupport.runner LaunchAgent) while stealing config.yaml and data-dir/keys/swarm.key. Derived from case analysis - NOT validated against a live sample."
        reference = "https://www.ox.security/blog/ethersphere-hijacked-with-crypto-stealing-malware-via-github-npm"
        reference = "https://thehackernews.com/2026/11/hackers-compromise-etherspheres-bee-js.html"
        falsepositives = "Legitimate Swarm tooling that merely references the swarm.key path; the rule requires the attacker-only frameworkmetrics.xyz host together with a stage endpoint or persistence name"
    strings:
        $c2 = "frameworkmetrics.xyz" ascii nocase
        $stage_analytics = "/v1/analytics" ascii
        $stage_electron = "/v1/electron" ascii
        $stage_swarm = "/v1/swarm/report" ascii
        $unit = "solidity-langsupport-runner" ascii nocase
        $launchagent = "com.solidity.langsupport.runner" ascii nocase
        $swarm_key = "data-dir/keys/swarm.key" ascii nocase
    condition:
        $c2 and any of ($stage_*, $unit, $launchagent, $swarm_key)
}
