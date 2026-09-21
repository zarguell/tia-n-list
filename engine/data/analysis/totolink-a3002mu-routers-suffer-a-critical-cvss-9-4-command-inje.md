CVE-2026-93742 is a critical command injection vulnerability in the formWsc function (/boafrm/formWsc) of Totolink A3002MU routers, rated CVSS 9.4 (some sources list 9.9). A public exploit is available, making this immediately actionable for anyone running the device.

The vulnerability allows unauthenticated remote attackers to execute arbitrary commands on the router by sending crafted HTTP requests to the WPS configuration endpoint. Totolink has not released a patch as of this writing. The recommended mitigation is to isolate affected devices from the network and disable remote management interfaces.

Totolink routers are common in consumer and small-business environments, particularly in Asia-Pacific markets. The availability of a public exploit means mass exploitation attempts are likely imminent. Organizations using Totolink gear should inventory their deployments and either replace the hardware or restrict WAN-side access immediately.
