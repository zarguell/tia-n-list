This cluster is a mechanical grouping of ENISA EUVD advisories, not a single vulnerability. The story anchors on EUVD-2026-72498, a CVSS 8.8 issue in JetBrains YouTrack published 2026-09-07 and updated 2026-09-22. The events actually attached are three separate advisories, all updated 2026-09-26: EUVD-2026-80006 in rsbuild (web-infra-dev, 7.1, published 2026-09-15), EUVD-2026-78584 in Ghostscript (Artifex Software, 9.3, published 2026-09-15), and EUVD-2026-82933 in clipbucket-v5 (MacWarrior, 7.1, published 2026-09-18).

The Ghostscript entry is the priority: a 9.3 score in a document-processing library that runs in server-side file pipelines and desktop stacks alike. None of the feed entries carries a CVE mapping or reports exploitation.

Treat this as a roundup of same-day EUVD updates rather than one story with four names. Watch the ENISA pages for CVE assignments and fix versions, and watch Ghostscript in particular given the score and how widely it ships bundled downstream.
