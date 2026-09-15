Microsoft confirmed that the September 2026 security update KB5002914 for Excel breaks copy-and-paste functionality for some users. The issue affects Excel instances where the update was applied and manifests as a failure of the standard Ctrl+C/Ctrl+V workflow. Microsoft has acknowledged the bug and is working on a fix.

This is a functionality regression rather than a security vulnerability, but it is notable because KB5002914 was a security-mandated update. Organizations that enforce mandatory patching via WSUS or Intune may find their finance and operations teams unable to perform basic spreadsheet operations. The workaround involves rolling back the update, which reintroduces the security fixes it addressed.

The incident follows a pattern of Microsoft security updates causing operational disruptions. IT teams should test KB5002914 in non-production environments before broad deployment and monitor Microsoft's known issue tracker for an official fix timeline.
