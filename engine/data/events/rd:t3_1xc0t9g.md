I did not validate, and info is scarce, but if it works it should be simple to apply with simple admin skills: > Apply the stopgap (best-intel, low-risk, reversible) > > In php.ini / .user.ini / .htaccess: >session.upload_progress.enabled = Off > Reload PHP-FPM or your web server. This closes both paths (session.c:3239). Needless to say, update ASAP or aimply.take the server down umtil it's available. submitted by /u/vjeuss [link] [comments]

via reddit r/cybersecurity: PHP2Shell - quick mitigation pre-patch
