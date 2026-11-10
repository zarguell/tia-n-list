Composer 2.11.2 and 2.2.32 fix three vulnerabilities, including a command execution flaw rated CVSS 8.8 that can be triggered through a crafted composer.lock file. Composer is the PHP dependency manager, and composer.lock is committed to repositories and consumed by automated build and deployment pipelines.

A crafted lock file can therefore reach a developer workstation or CI runner through a cloned repository or a malicious dependency update. Command execution at install or update time gives an attacker code execution in the build context, where secrets, tokens, and deployment credentials are commonly present.

The fixed versions are 2.11.2 for the current branch and 2.2.32 for the long-term support branch. Update both developer installations and CI images, and audit composer.lock files from untrusted sources before running install or update. Watch for the vendor to publish the remaining two CVEs and for exploit code that targets the lock-file parser.
