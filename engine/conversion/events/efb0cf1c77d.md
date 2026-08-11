*Missed by today's feeds; surfaced via external monitoring. N-able disclosed Aug 1–2 with confirmed in-the-wild exploitation.*

N-able disclosed a critical vulnerability in **N-central**, its flagship RMM platform used by MSPs to monitor and remotely administer every downstream customer endpoint. Key facts:

- **CVE-2026-18556** (initial advisory) → **CVE-2026-18577** ("an incomplete patch for CVE-2026-18556 allows for authentication bypass and account takeover in N-central versions through 2026.3.1"). **All currently supported versions are affected, including builds initially believed safe** — both cloud-hosted and on-premises.

- An unauthenticated attacker gains **full administrative "god-mode" access to the RMM console** — the same control level as trusted NOC/engineering staff. From there they can push scripts/jobs to managed endpoints, deploy dual-use tools via the N-able agent, and (per Huntress) abuse the built-in **Take Control** feature to pivot into managed endpoints and deploy **Cloudflare-based tunnels for persistence**.

- N-able shipped hotfix **2026.3.1.7 on August 2** as the first unaffected build. Huntress reports **55.6% of reachable cloud N-central servers were still unpatched** as of Aug 3, and notes the server runs a custom **AlmaLinux 9 appliance that frequently has no EDR** deployed.

- **IOCs:** attacker traffic observed from `87.249.138[.]34` (NordVPN exit node), `37.19.210[.]32` (Mullvad exit node, previously abused for brute-forcing/spam), plus `37.153.90[.]88` and `92.118.112[.]181` (added by N-able in a follow-up advisory).

**Why it matters:** This is the Kaseya-VSA-shaped nightmare for the MSP supply chain — RMM compromise means downstream access to every managed customer, and the incomplete-first-fix pattern means orgs that patched to the original advisory version are still exposed.

**Action:** Apply **2026.3.1.7 immediately**; if N-central is reachable from untrusted networks, consider taking it offline until patched behind strict network controls. Audit for suspicious logins, new remote-control/Take Control sessions, and unexpected Cloudflare tunnel processes on the N-central host. Hunt for the four IOCs.
