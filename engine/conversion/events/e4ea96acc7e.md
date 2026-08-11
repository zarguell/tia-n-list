A campaign active since November 2025 has published at least **eight trojanized Pyrogram forks** on PyPI, collectively downloaded over 25,000 times, that backdoor Telegram bot servers. Discovered by Checkmarx, the packages hide a `secret.py` backdoor in the helpers module that registers hidden Telegram command handlers — enabling arbitrary Python code execution and shell commands on the infected server.

The backdoor activates only on Telegram bot accounts (typically production servers), giving attackers file read access, credential dumping, chat access, database downloads, and persistent backdoor installation. A hardcoded OWNERS list with Telegram IDs ensures exclusive attacker control. Affected packages include `VLifeGram` (4,150 downloads), `pyrogram-styled` (15,370 downloads), and six others.

**Recommended action:** Check `pip list` or `requirements.txt` for any of the named packages. Rotate all credentials on affected servers and revoke Telegram bot tokens immediately.

---
