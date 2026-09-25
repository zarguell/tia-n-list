SafeDep, Socket, and deafnews.it all report that the Mini Shai-Hulud worm is still infecting GitHub repositories through hijacked GitHub Actions workflows. Per deafnews.it, two compromised Actions that had been dormant since May reactivated this week and began executing malicious payloads in CI/CD pipelines, and earlier containment efforts failed.

The mechanism is what makes this persistent: repositories that cleaned out malicious code but kept trusted, previously compromised workflow definitions get reinfected the moment those workflows run. Socket notes the reactivation exposes thousands of repositories, since CI secrets and publish credentials flow through the very pipelines the worm controls.

What to watch: updated indicators of compromise for the reactivated workflows, guidance on rotating CI/CD secrets and npm tokens, and whether maintainers identify how the Actions were compromised in the first place.
