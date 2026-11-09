Shubham Shah and Sam Curry took over the login systems of two automakers' mobile apps in 2026 by finding default admin:admin credentials on their ForgeRock identity servers, reaching any customer account and the unlock and engine-start commands. The research, published on samcurry.net, shows the admin console was left at factory defaults, allowing full account takeover.

The Hacker News amplified the finding. No CVEs are assigned; the issue is a configuration failure rather than a software vulnerability, so remediation is operational: change default credentials, restrict admin console exposure, and audit identity providers.

The concrete risk is remote unlock and engine start for affected customers. Owners of the two brands should treat mobile-app account security as compromised until the automakers confirm remediation, and watch for unauthorized account access. The finding is a reminder that identity-provider defaults are a recurring source of vehicle-level exposure.
