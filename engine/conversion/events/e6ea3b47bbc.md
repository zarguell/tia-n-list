GitLab released critical security updates (versions **19.2.1, 19.1.3, 19.0.5**) addressing **13 vulnerabilities**:

- **CVE-2026-6267 (CVSS 8.5):** GitLab Workhorse flaw allowing authenticated users with Developer-level access to retrieve sensitive information in internal requests

- **CVE-2026-12436:** Mass-assignment bug in Pipeline Schedule API — attackers can modify CI/CD configurations belonging to other users

- **CVE-2026-15975:** Unauthenticated DoS via insufficient resource throttling in merge request discussions

- Additional medium-severity issues in authorization, project import, pipeline test reports, and confidential issue title exposure

**Action:** Self-managed GitLab instances should upgrade immediately. GitLab.com and GitLab Dedicated are already patched.
