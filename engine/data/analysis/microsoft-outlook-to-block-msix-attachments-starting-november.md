Microsoft will block MSIX attachments in Outlook starting in November. Coverage from fawkes.rocks and BleepingComputer frames the change as a response to attackers packaging malware inside MSIX files, the Windows app package format that can carry installers and scripts past naive attachment filters.

Default-deny on a whole file class is a structural improvement rather than a detection tweak: it removes the delivery path instead of trying to score each sample. The tradeoff is operational, since legitimate software distributors who ship MSIX packages by email will need to move to download links or store distribution.

Watch for attackers pivoting to adjacent container formats that are not yet blocked, and for Microsoft extending the same treatment to other executable packaging types. Organizations that still need to receive MSIX files should pre-arrange an approved alternate channel before the November change takes effect.
