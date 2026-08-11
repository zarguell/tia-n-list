GitHub announced that npm v12 (expected next month) will fundamentally change how dependencies are installed: `preinstall`/`install`/`postinstall` scripts from dependencies will not run unless explicitly approved; Git repository dependencies and remote URL tarballs will no longer resolve automatically. Each of these behaviors has been abused in recent supply-chain attacks, including the Shai-Hulud campaign. npm 11.16.0+ shows warnings for workflows that will break under v12.

---
