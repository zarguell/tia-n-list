rule CWPdoor_Control_Web_Panel_Backdoored_cwpsrv {
    meta:
        author = "Tia N. List"
        date = "2026-11-07"
        status = "experimental"
        description = "Hunts the cwpdoor passive backdoor built into a recompiled Control Web Panel web server (cwpsrv). The implant answers only requests that carry the X-Ngx-Integrity-Time, X-Ngx-Integrity-Data and X-Ngx-Integrity-Sig headers validated against an embedded RSA key inside a 300-second window, and suppresses those requests from the access log. Derived from the QiAnXin XLab analysis of samples targeting cwpsrv 1.15.10 and 1.24.0 - NOT validated against a live sample."
        reference = "https://blog.xlab.qianxin.com/cwpdoor-the-invisible-backdoor-living-inside-control-web-panel/"
        falsepositives = "Legitimate builds of cwpsrv that ship an integrity helper with the same header names are possible; a hit means the on-disk binary deserves a hash comparison against the vendor build, not that the host is certainly compromised"
    strings:
        $hdr_time = "X-Ngx-Integrity-Time" ascii
        $hdr_data = "X-Ngx-Integrity-Data" ascii
        $hdr_sig = "X-Ngx-Integrity-Sig" ascii
        $path_bin = "/usr/local/cwpsrv/bin/cwpsrv" ascii
        $installer = "cwpsrv_update.sh" ascii
        $backup = "cwpsrv.prev-" ascii
    condition:
        all of ($hdr_*) and any of ($path_bin, $installer, $backup)
}
