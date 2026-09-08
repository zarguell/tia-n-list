rule DPRK_HAProxy_Ted_Backdoor {
  meta:
    author = "Tia N. List"
    date = "2026-09-08"
    status = "experimental"
    description = "Detects the DPRK-linked 'ted backdoor' implanted in HAProxy binaries. The implant intercepts HTTP traffic, captures session cookies, and uses a hidden command channel triggered by a specific image path."
    reference = "https://gbhackers.com/dprk-linked-hackers-backdoor-haproxy-servers-to-spy-on-south-korean-organizations/"
    falsepositives = "None expected in production HAProxy binaries"
  strings:
    $trigger = "/favorite_list_2x_m500_ico.jpg"
    $haproxy_ref = "HAProxy" ascii nocase
    $cli_header = "X-CLI-Token" ascii
    $cmd_channel = "/cli/check" ascii
  condition:
    uint32(0) == 0x464C457F and
    $trigger and
    $haproxy_ref and
    1 of ($cli_header, $cmd_channel)
}
