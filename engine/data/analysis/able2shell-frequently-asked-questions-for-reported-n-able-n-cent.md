N-able published seven CVEs and released N-central 2026.4 Hotfix 2 on November 10 after a researcher operating as "Oracle-Security" published "Able2Shell," a write-up describing 33 alleged vulnerabilities in N-central with proof-of-concept code, including an unauthenticated command-execution chain. Security firms reported exploitation attempts against N-central honeypots, but as of November 10 no confirmed compromise of a customer server had been reported.

The disclosure is contested: N-able does not confirm whether it was notified in advance and does not name the researcher. Tenable's Research Special Operations team published an FAQ. The gap between 33 alleged flaws and 7 fixed CVEs leaves residual exposure, so administrators should treat the hotfix as partial and monitor N-able advisories for follow-up CVEs.

N-central is widely deployed by managed service providers, so a working unauthenticated remote code execution chain would have broad downstream impact. Priority actions: apply 2026.4 Hotfix 2, restrict management interfaces, and watch for additional CVEs covering the remaining alleged issues.

