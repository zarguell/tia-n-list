SecurityWeek reports on a new Windows attack technique using bind links (NTFS reparse points) that can hide malicious executable content from EDR tools. Bind links allow an attacker to create a directory entry that points to an alternate data stream or location, causing EDR file scanning to miss the actual malicious payload while the OS still executes it. This represents an evolution in EDR evasion beyond traditional LOLBins and living-off-the-land techniques.

**Action:** Update EDR detection rules to account for NTFS bind link reparse point abuse. Monitor for abnormal reparse point creation via FsRtlCreateNotifyFilter or NtFsControlFile with FSCTL_SET_REPARSE_POINT.

---
