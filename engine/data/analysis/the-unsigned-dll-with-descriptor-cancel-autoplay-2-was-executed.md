The DFIR Report revisited a 2022 QBot intrusion that leveraged Zerologon (CVE-2020-1472) to gain domain admin, then deployed an unsigned DLL called "Cancel Autoplay 2" via regsvr32.exe for persistence. The technique hides execution behind a legitimate Windows autoplay handler name, making it harder to spot in process listings.

QBot (also called QakBot) has been one of the most prolific initial-access brokers since 2019. This particular campaign combined phishing emails with exploit kit payloads before pivoting to Active Directory compromise. The unsigned DLL approach avoids application allowlisting policies that might block known malicious binaries.

The report is useful for detection engineering teams looking at regsvr32-based persistence. IOCs and the full playbook are linked in the original DFIR Report writeup.
