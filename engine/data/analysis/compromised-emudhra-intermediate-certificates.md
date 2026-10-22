Cisco Talos found eight eMudhra intermediate CA certificates whose private keys had only single or double digit entropy instead of the required 384 bits. An attacker holding such a key can impersonate any website or service. Chrome, Mozilla, and Apple blocked six affected TLS certificates.

The weakness undermines trust in the CA chain and forces browsers to revoke. Watch for additional affected intermediates and any sites still relying on them.
