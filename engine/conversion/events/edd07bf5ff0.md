The Howler Cell Threat Research Team identified **OnionDrop**, a multi-stage loader that has delivered 645+ unique DLL samples between February 28 and May 20, 2026. Its evasion depth rivals nation-state tooling, with a four-stage unpack chain (custom byte-pair → Xpress Huffman → AES-256-CBC → Donut shellcode), DLL sideloading via legitimate Adobe-signed executables, and execution via `TpPostWork` thread-pool callback abuse (bypassing standard CreateThread telemetry). Confirmed payloads include LegionLoader (CurlyGate), CGrabber, and Vidar Stealer. C2: `gainmsg[.]com`.

---
