The Hacker News reports a new PamStealer macOS variant that decrypts its payload live from its command and control server rather than embedding it in the file, and adds multi-layer persistence. The JXA dropper used for initial delivery was updated with a new lure and delivery chain.

Fetching and decrypting the payload at runtime keeps the intact malware off disk, which complicates static analysis, signature writing and sandbox detonation. Multi-layer persistence means defenders must find and remove every foothold or the infection returns, and JXA droppers remain an effective macOS access route because they run through native scripting tools that look routine.

Watch for published IOCs covering the dropper, lure documents and C2 endpoints, evidence on whether PamStealer is sold or rented to multiple operators, and detection updates from macOS security vendors as samples circulate.
