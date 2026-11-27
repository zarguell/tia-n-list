rule PolinRider_PythonLoader_EthereumC2
{
    meta:
        author = "Tia N. List"
        date = "2026-11-27"
        status = "experimental"
        description = "Detects the PolinRider Python loader planted in utils packages and conftest.py inside poisoned GitHub repositories (SafeDep / Apiiro, November 2026). The loader is 58 lines of standard-library Python that resolves the newest self-addressed transaction of operator wallets through the Ethplorer API and an Ethereum RPC node, decodes the next stage from transaction calldata and runs it in a detached interactive Node REPL. Derived from published case analysis - wallet addresses are perishable and rotate."
        reference = "https://safedep.io/polinrider-ethereum-c2-github-repositories"
        falsepositives = "Ethereum tooling, blockchain tracers and research notebooks legitimately reference api.ethplorer.io. Require a known operator wallet address or the loader's import-time execution pattern (conftest.py or utils package writing to a node -i process) before alerting on the API string alone"
    strings:
        $wallet_a = "0x3b1574417524c11a7403c4b232CAcBb320CceBC6" ascii nocase
        $wallet_b = "0x1eEf0849EDa15d87f64e51C73C8442Cf3c8bCEF3" ascii nocase
        $ethplorer = "api.ethplorer.io" ascii nocase
        $ethplorer_path = "getAddressTransactions" ascii nocase
    condition:
        all of ($wallet_*) or ($ethplorer and any of ($wallet_*, $ethplorer_path))
}
