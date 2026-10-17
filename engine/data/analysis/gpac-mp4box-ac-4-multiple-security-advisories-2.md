CVE-2025-60470 is an out-of-bounds read in GPAC MP4Box AC-4 Parser. The GitHub advisory notes the vulnerability exists in the AC-4 parsing code and could expose memory contents or trigger crashes when processing malformed media. No exploitation claims accompany the disclosure, so priority is patching before any observed attacks appear.

GPAC is embedded in downstream media tools, so a flaw in its AC-4 parser widens the attack surface wherever user-controlled files are parsed. Monitor the GPAC issue tracker for the fix release and verify that any products bundling GPAC apply updates promptly.
