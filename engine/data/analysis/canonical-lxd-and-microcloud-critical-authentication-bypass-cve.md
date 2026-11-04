Canonical published fixes for CVE-2026-112816, a critical authentication bypass with CVSS 10.0 affecting LXD versions 4.0.14, 5.0.10, 5.21.8 and earlier. Improper certificate validation in the HTTPS listener allows an unauthenticated attacker who reaches the API to authenticate as any trusted client through a crafted certificate chain, gaining full cluster and virtual machine access. Fixed versions include 4.0.15, 5.0.11, 5.21.9, and 6.10.1. Ubuntu rates the vulnerability Medium priority.

This is a complete cluster compromise path for container and VM infrastructure running Canonical LXD. Any external exposure of the HTTPS listener should be treated as a critical exposure.

Administrators should upgrade to the fixed releases immediately and restrict HTTPS API access to trusted networks only. Monitor for unexpected client certificate usage on LXD clusters.
