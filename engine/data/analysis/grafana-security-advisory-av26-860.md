The Canadian Centre for Cyber Security issued advisory AV26-860 on August 28, 2026, reporting a vulnerability in Grafana Alloy affecting all versions up to and including 1.18.1. The flaw is tracked as CVE-2026-19516. Alloy is Grafana's open-source, composable observability agent for collecting and forwarding metrics, logs, and traces.

Grafana Alloy is widely deployed in Kubernetes and cloud-native monitoring stacks. A vulnerability here could affect telemetry pipelines across large fleets. The advisory urges users to upgrade to a patched version, though the specific fix version is not enumerated in this Canadian advisory.

This is distinct from advisory AV26-796 which covered a different Grafana product. Watch for Grafana Labs to publish full technical details and a CVSS score. Organizations running Alloy in production should prioritize patching pending further severity assessment.
