rule Crypto_Wallet_ScreenConnect_Phishing_Lures {
    meta:
        author = "Tia N. List"
        date = "2026-11-17"
        status = "experimental"
        description = "Identifies the Coldcard and Ledger hardware-wallet phishing lures that chain legitimate newsletter delivery to ConnectWise ScreenConnect installation. Matches by the lure artifact names embedded in the .bat/.zip payloads and by the campaign's phishing domains found inside the scripts. Derived from the November 2026 report - archive-internal filenames are reported, the script bodies are not, so expect hits on the ZIP central directory and on any script embedding the domains."
        reference = "https://malware.news/t/crypto-hardware-wallet-users-under-attack/127349#post_1"
        falsepositives = "Copycat wallet-phishing kits reuse the same brand filenames; a hit identifies lure infrastructure, not a specific operator"
    strings:
        $coldcard_artifact = "V1.5.3Q-q1-coldcard" ascii nocase
        $ledger_artifact = "Ledger-wallet-Transition-Transcript" ascii nocase
        $coldcard_host = "coldcard.pro" ascii nocase
        $ledger_host = "ledger-wallet.net" ascii nocase
        $ledger_host_alt = "ledgeradvisorinfo.app" ascii nocase
    condition:
        any of them
}
