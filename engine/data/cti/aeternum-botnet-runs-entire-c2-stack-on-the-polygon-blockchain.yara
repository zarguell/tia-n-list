rule Aeternum_Blockchain_C2 {
    meta:
        author = "Tia N. List"
        date = "2026-08-11"
        status = "experimental"
        description = "C++ botnet loader moving command-and-control onto the public Polygon blockchain; infected devices query attacker-controlled smart contracts via public JSON-RPC endpoints. Derived from case analysis (Unit 42) — NOT validated against a live sample."
        reference = "https://unit42.paloaltonetworks.com/aeternum-blockchain-c2-analysis/"
        falsepositives = "Wallet/DeFi applications legitimately embed the same public RPC endpoints and JSON-RPC methods; combine with process/network context before acting"
    strings:
        $rpc1 = "polygon-rpc.com" ascii nocase
        $rpc2 = "rpc-mainnet.matic.network" ascii nocase
        $rpc3 = "rpc-mainnet.maticvigil.com" ascii nocase
        $rpc4 = "polygon.llamarpc.com" ascii nocase
        $method1 = "eth_blockNumber" ascii
        $method2 = "eth_getCode" ascii
        $method3 = "eth_call" ascii
    condition:
        uint16(0) == 0x5A4D and any of ($rpc*) and any of ($method*)
}
