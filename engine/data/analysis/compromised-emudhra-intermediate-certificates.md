Cisco Talos disclosed that eight eMudhra intermediate CA certificates were generated with critically weak private keys, with entropy reduced from 384 bits to only 3-8 bits during an April 30, 2025 key generation ceremony. The flaw makes recovering the private keys trivial, allowing an attacker holding any compromised intermediate to impersonate any website or service. Six TLS certificates trusted by Chrome, Mozilla, and Apple have already been blocked by those vendors, and two codesigning certificates used by Microsoft were also blocked.

eMudhra has revoked the compromised certificates and stopped issuing under its G3 root. Talos expects further patches across technologies as applications remediate exposure. Administrators should verify their trust stores and certificate pinning configurations reflect the vendor blocks.

Watch for additional vendor advisories and any evidence of active misuse of the weak keys before revocation took effect.
