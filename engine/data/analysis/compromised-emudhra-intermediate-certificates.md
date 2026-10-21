Several eMudhra intermediate certificates were compromised, prompting browsers and operating systems to block them and Debian to ship DSA-6572-1 removing the affected intermediates from ca-certificates. Firefox ESR updates also block the compromised intermediates, cutting off trust chains that relied on them.

Organizations using eMudhra-issued certificates should inventory dependent services and replace affected certs. Watch for further revocation actions from other distributions and browser vendors, plus any downstream outages from suddenly untrusted intermediates.
