ENISA's EUVD database carries two same-day advisories against Cap-go's capgo.app, a live-update platform for mobile apps. EUVD-2026-87717 scores 8.7 and affects capgo.app through version 12.129.0, described as a content-lock bypass. EUVD-2026-87770 scores 5.3 and affects versions through 12.128.2. Both entries were updated on 2026-09-26.

Two advisories against the same product on the same day points at a coordinated disclosure wave rather than isolated findings. The 8.7 is the serious one: a live-update platform sits directly in the code delivery path, and a content-lock bypass there is the kind of flaw that can turn a distribution channel into an attack channel.

Watch for patched releases past 12.129.0, CVE mappings being added to the ENISA entries, and any confirmation of update-channel abuse in the wild. Teams shipping apps through capgo should treat the 8.7 as priority triage.
