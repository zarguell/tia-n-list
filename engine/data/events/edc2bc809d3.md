JFrog disclosed a heap out-of-bounds write in FFmpeg's **MagicYUV decoder** — dubbed **PixelSmash** — that enables remote code execution on Jellyfin media servers and denial-of-service conditions in Kodi, Emby, Nextcloud, PhotoPrism, and OBS Studio. The vulnerability (CVSS 8.8, CVE-2026-8461) stems from an inconsistency between how the frame allocator and decoder compute chroma plane heights in slice handling.

JFrog demonstrated full RCE against **Jellyfin 10.11.9** via the media library's automated ffprobe scan pipeline: a crafted MagicYUV AVI file downloaded into the library triggers `ffprobe` metadata extraction → OOB write fires → `AVBuffer.free` is hijacked to `system()` → attacker's command executes as the `jellyfin` service user. The exploit requires ASLR bypass via chaining with an FFmpeg FlashSV info-leak bug. An alternative attack vector via torrent download requires zero user interaction.

FFmpeg version **8.1.2** (released June 17) patches the flaw. Jellyfin has updated its bundled FFmpeg. The MagicYUV decoder's presence in hundreds of dependent projects creates a broad supply-chain attack surface — Slack, Discord, Telegram, and WhatsApp use FFmpeg for server-side video processing (not confirmed vulnerable but within scope).

**Hunting hypothesis:** Monitor for unexpected ffprobe/ffmpeg child processes on Jellyfin hosts, or anomalous network connections from the `jellyfin` service user shortly after media library scans.

---
