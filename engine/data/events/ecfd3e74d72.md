PT Swarm researchers uncovered two memory safety issues in PHP's core `ext/standard` extension: CVE-2025-14177 (CVSS 6.3), a heap memory disclosure in `getimagesize()` when parsing JPEG APP segments with multi-chunk reads, and a heap buffer overflow in `iptcembed()` when handling non-standard files like pipes where `fstat()` reports size as zero. The `iptcembed()` overflow is the more severe of the two, potentially leading to code execution. Both issues have been patched in recent PHP releases.

---
