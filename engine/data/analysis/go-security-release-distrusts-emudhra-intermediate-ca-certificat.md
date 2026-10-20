Go 1.27.3 and 1.26.10, released 2026-10-19, add explicit distrust in crypto/x509 for eight intermediate CA certificates belonging to eMudhra Technologies Limited, tracked as CVE-2026-111943 on the urgent track. The fix filters out the eight compromised intermediates so Go programs no longer chain trust through them.

The Chrome Root Program received a researcher report on Saturday 2026-10-17 at 18:05 UTC that private keys for the same eight eMudhra intermediates had been compromised. Those intermediates sit in multiple trust stores, so the distrust has to propagate across Go, Mozilla, and Chrome rather than a single vendor.

What to watch: whether other runtimes and trust stores adopt matching blocks, and whether sites still presenting certificates chained to the eight intermediates fail validation as the distrust lands in production Go builds.
