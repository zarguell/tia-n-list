GitGuardian found 474 leaked GitHub App private keys still active out of 4,802 tested, representing about 10% of exposed keys. These authenticated as 440 distinct Apps; 44 had full organization admin access, 72% could read private repositories, and 207 could write to repositories. The keys never expire. The event names exposed keys for GitHub Actions, BuildBuddy, Crusher.dev, and the CDC. A single compromised App can reach every repository it covers and potentially take over the organization.

Why it matters: exposed App keys are a persistent supply-chain vector, not a transient leak. Because the keys do not expire, forgotten leaks remain valid for years. Organizations with leaked keys that have write or admin access face full repository and organizational takeover.

Watch for rotation campaigns targeting these 474 keys and any follow-up reports linking specific leaked keys to observed abuse in CI/CD pipelines.
