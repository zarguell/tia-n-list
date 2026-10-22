FoxIO disclosed a QPACK implementation flaw in HTTP/3 that lets a tiny request trigger serious memory exhaustion on vulnerable servers. A single unauthenticated connection can force large allocations.

The issue affects QPACK header handling and is a denial of service risk for HTTP/3 deployments. Operators running HTTP/3 should review vendor advisories for patches or mitigations.

Watch for CVE assignment, affected product lists, and in the wild exploitation reports.
