#!/usr/bin/env python3
"""Test script for multi-provider LLM client."""

import os
import sys
sys.path.insert(0, '.')

from src.llm_client_multi import MultiLLMClient

def test_provider_info():
    """Test getting provider information."""
    print("Testing multi-provider client...")

    try:
        client = MultiLLMClient()
        info = client.get_provider_info()

        print(f"Available providers: {info['available_providers']}")
        print(f"Primary provider: {info['primary_provider']}")
        print(f"Primary available: {info['primary_available']}")
        print(f"Fallback provider: {info['fallback_provider']}")
        print(f"Fallback available: {info['fallback_available']}")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def test_relevance_analysis():
    """Test relevance analysis."""
    print("\nTesting relevance analysis...")

    try:
        client = MultiLLMClient()

        title = "Critical Windows Vulnerability Allows Remote Code Execution"
        content = """
        Microsoft has released an emergency security update to address a critical vulnerability
        in Windows that could allow remote code execution. The vulnerability tracked as CVE-2025-1234
        affects Windows 10, 11, and Server versions. Attackers could exploit this by sending
        specially crafted packets to target systems. Organizations are urged to apply the patch
        immediately as proof-of-concept exploits are publicly available.
        """

        result = client.is_relevant_article(title, content)
        print(f"Relevance result: {result}")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def test_ioc_extraction():
    """Test IOC extraction."""
    print("\nTesting IOC extraction...")

    try:
        client = MultiLLMClient()

        title = "Malware Campaign Uses C2 Domain evil.example.com"
        content = """
        Security researchers have discovered a new malware campaign that uses the command and control
        domain evil.example.com with IP address 203.0.113.42. The malware samples have the following
        hashes: SHA256: a1b2c3d4e5f6... and MD5: 098f6bcd4621d373cade4e832627b4f6.
        Attackers are using phishing emails with subject "Invoice Attached" to distribute the malware.
        """

        result = client.extract_iocs_and_ttps(title, content)
        print(f"IOC extraction result: {result}")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Multi-Provider LLM Client")
    print("=" * 50)

    # Check environment variables
    print("Environment variables:")
    print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER', 'Not set (defaults to gemini)')}")
    print(f"GEMINI_API_KEY: {'Set' if os.getenv('GEMINI_API_KEY') else 'Not set'}")
    print(f"OPENROUTER_API_KEY: {'Set' if os.getenv('OPENROUTER_API_KEY') else 'Not set'}")
    print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    print()

    tests = [
        test_provider_info,
        test_relevance_analysis,
        test_ioc_extraction,
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "=" * 50)
    print(f"Tests passed: {sum(results)}/{len(results)}")

    if all(results):
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())