GitLab patched CVE-2026-110264, a maximum-severity (CVSS 10.0) pre-authentication remote code execution flaw in its regex engine. The bug sat in the codebase for roughly twelve years and affected self-managed GitLab instances across more than a decade of releases.

The flaw allows an unauthenticated attacker to execute code on affected self-managed servers, and Censys reportedly observed roughly 82,000 instances on the day of disclosure. GitLab has released fixes; administrators of self-managed instances must patch promptly, as the vulnerability's pre-auth nature and long dwell time make it a high-value target.

Watch for exploitation in the wild and for additional downstream updates, since the regex-engine scope may affect other components and forked deployments.
