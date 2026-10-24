LiteLLM 1.107.0 was compromised on PyPI: malicious wheels and container images included credential-stealing startup hooks. Socket reported the supply chain attack on October 21, 2026. The hooks could expose cloud credentials and AI auth tokens even without importing LiteLLM.

Users should rotate any secrets that touched systems with the malicious version and verify installed LiteLLM packages against known-good hashes. The incident highlights supply chain risk in AI tooling ecosystems.
