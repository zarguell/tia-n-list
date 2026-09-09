The sole event in this story links to a Dark Reading report on a multi-hop Google redirect phishing campaign. Attackers are chaining legitimate Google services (search redirects, OAuth consent flows) to route victims through multiple hops before landing on credential-harvesting pages. The technique evades traditional URL filtering because each hop uses a valid Google domain.

This is not a new class of attack, but the multi-hop approach complicates detection. Security teams relying on blocklists or reputation-based filters will miss the intermediate Google-hosted steps. The campaign appears to target corporate credentials rather than consumer accounts.

Watch for the specific redirect chains documented in the Dark Reading piece. Defenders should review CASB and email gateway rules for Google-hosted redirect patterns and consider blocking or flagging OAuth consent screens originating from unverified applications.
