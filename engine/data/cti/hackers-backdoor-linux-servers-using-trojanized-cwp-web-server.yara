rule CWPdoor_Trojanized_cwpsrv_Backdoor
{
	meta:
		author = "Tia N. List"
		date = "2026-11-06"
		status = "experimental"
		description = "Hunts CWPdoor, the passive backdoor XLab found embedded in a recompiled cwpsrv binary shipping with trojanized Control Web Panel 1.15.10 / 1.24.0. Commands arrive as AES-encrypted HTTP headers (X-Ngx-Integrity-Data, timestamped by X-Ngx-Integrity-Time and signed with X-Ngx-Integrity-Sig) and are executed through the ngx_http_integrity_helper Unix socket, whose output returns as application/octet-stream while the request is kept out of the access log. Derived from published case analysis - NOT validated against a live sample."
		reference = "https://www.bleepingcomputer.com/news/security/hackers-backdoor-linux-servers-using-trojanized-cwp-web-server/ https://blog.xlab.qianxin.com/beware-of-cwpdoor-the-zero-detection-pas-backdoor-hiding-in-centos-websive-panel/"
		falsepositives = "Stock or patched cwpsrv builds never carry the X-Ngx-Integrity-* header strings or the integrity helper socket name, so a hit indicates the trojanized binary or its installer; scanners that embed the same strings in test fixtures will also match"

	strings:
		$hdr_data = "X-Ngx-Integrity-Data" ascii nocase
		$hdr_time = "X-Ngx-Integrity-Time" ascii nocase
		$hdr_sig = "X-Ngx-Integrity-Sig" ascii nocase
		$sock = "ngx_http_integrity_helper" ascii
		$bin = "cwpsrv" ascii
		$updater = "cwpsrv_update.sh" ascii

	condition:
		(all of ($hdr_*)) or ($sock and $bin) or $updater
}
