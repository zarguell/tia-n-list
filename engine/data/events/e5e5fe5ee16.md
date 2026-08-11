Ukraine's **CERT-UA** has uncovered attacks by threat cluster **UAC-0099** (previously linked to providing initial access for **Sandworm/APT44**) distributing a ZIP archive containing the legitimate Notepad++ application with a malicious **LunchPoke** DLL disguised as a plugin.

Attack chain:

1. VBS script disguised as a PDF document

2. Retrieves `Evernote.zip` containing Notepad++ 8.8.3, malicious `NppExport.dll`, password-protected `updater.rar`, and legitimate WinRAR

3. Launches Notepad++ which loads the malicious DLL via standard plugin mechanism

4. DLL establishes persistence and deploys further payloads

No vulnerability or supply-chain compromise is exploited — the attack relies on social engineering to deliver the trojanized archive.

---
