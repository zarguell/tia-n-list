Researchers detailed the **GhostTree** attack technique, which abuses recursive NTFS junctions — file system features any user can create without admin privileges — to hide malware. NTFS junctions and symbolic links let one directory transparently point to another. In GhostTree, attackers create nested junction chains that make directory traversal loop infinitely, causing security tools to hang or skip the hidden content. The technique enables stealthy malware persistence that evades traditional file system scanning. Since any user can create junctions, no privilege escalation is needed.

---
