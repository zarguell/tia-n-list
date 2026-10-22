LiteLLM version 1.107.0 published to PyPI was compromised and installs a credential stealer and backdoor. The malicious payload runs on every Python process start on an affected host, not only when LiteLLM is imported, so IDEs, pip, and CI jobs are all exposed. It steals SSH keys, AWS credentials, browser passwords, shell history, and AI coding tool configs, and a daemon executes attacker-supplied code hourly.

The recommended response is to pin to version 1.106.2, audit any environment that installed 1.107.0, and rotate all credentials reachable from those hosts. Treat any system that ran the affected version as fully compromised.

Watch for follow-up advisories describing the full scope of stolen data and any additional affected versions or distribution channels beyond PyPI.
