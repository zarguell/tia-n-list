OpenCode, an open-source AI coding agent, disclosed a security breach tied to a large-scale distillation attack that impacted 1.4% of OpenCode Console users who had linked external providers such as Anthropic, OpenAI, and Google. Affected users reported unauthorized API charges and suspended Google Cloud projects, with some seeing more than $1,700 in charges overnight. OpenCode notified impacted users by email and stated unaffected users received no notification.

Distillation is a legitimate technique for training smaller models from larger ones, but here it was abused to extract API responses at scale. The incident highlights risks of exposing API keys through AI coding tools and agent infrastructure.

Users should rotate any API keys used with OpenCode, review provider billing and usage logs, and limit key scopes. Organizations running OpenCode should audit linked providers and enforce key rotation policies.
