JFrog disclosed **PixelSmash**, a heap out-of-bounds write vulnerability in FFmpeg's libavcodec library within the MagicYUV decoder. The flaw exists in slice handling — "caused by an inconsistency between how the frame allocator and the decoder compute chroma plane heights." A 50 KB AVI, MKV, or MOV file can deliver the exploit payload.

The attack surface is immense: any application using FFmpeg for media processing — desktop video players, file manager thumbnail generators (GNOME, KDE, XFCE via ffmpegthumbnailer), self-hosted media servers (Jellyfin, Emby, Plex), cloud transcoding pipelines, NAS appliances, and smart TVs. JFrog confirmed successful exploitation against Kodi, mpv, Jellyfin, Nextcloud, Immich, PhotoPrism, and OBS Studio. On Nextcloud, the flaw can be triggered as a near-zero-click attack via the Movie preview provider — the attacker only needs the file visible in a folder listing.

JFrog achieved code execution by targeting FFmpeg's `AVBuffer` struct — placing a NUL-terminated shell command at a specific out-of-bounds offset. FFmpeg version 8.1.2 contains the fix.

**Recommended action:** Update FFmpeg to 8.1.2 on all platforms. For media server operators: disable automatic thumbnail generation until patching is complete.

---
