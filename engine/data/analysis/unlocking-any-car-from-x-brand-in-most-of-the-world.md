Shubham Shah and Sam Curry found a vulnerability chain in two automakers' ForgeRock-based customer login systems that yielded remote code execution on production SSO servers, letting them create valid sessions for any customer account.

From those sessions they could retrieve vehicle location and telemetry and issue remote commands including lock, unlock and engine start or stop. Both automakers fixed the issue within about two hours and rotated affected credentials; testing used US accounts and vehicles.

The affected automakers were not named. The chain combined a ForgeRock path confusion issue with access to OpenIDM and the SSO servers, and the researchers published a disclosure timeline and technical breakdown on samcurry.net in November 2026.
