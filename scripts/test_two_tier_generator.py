#!/usr/bin/env python3
"""Test script for the two-tier blog generator."""

import sys
import os
from datetime import date

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.two_tier_blog_generator import TwoTierBlogGenerator

def main():
    """Test the two-tier blog generator."""
    print("🧪 Testing Two-Tier Blog Generator")
    print("=" * 50)

    # Test with two-tier analysis enabled
    print("Test 1: Two-Tier Analysis ENABLED")
    generator = TwoTierBlogGenerator()

    result = generator.generate_daily_summary(
        target_date=date.today(),
        use_intelligent_synthesis=True,
        use_dynamic_title=True,
        use_dynamic_tags=True,
        use_two_tier_analysis=True
    )

    print(f"✅ Generation completed: {result['success']}")
    print(f"📄 Content length: {result.get('content_length', 0)} characters")
    print(f"🎯 Two-tier analysis used: {result.get('two_tier_analysis_used', False)}")
    print(f"🔧 Synthesis method: {result.get('metadata', {}).get('synthesis_method', 'unknown')}")

    if result.get('metadata'):
        metadata = result['metadata']
        print(f"📊 Tier 1 success: {metadata.get('tier_1_success', False)}")
        print(f"📊 Tier 2 success: {metadata.get('tier_2_success', False)}")
        print(f"🔤 Tier 1 tokens: {metadata.get('tier_1_tokens', 0)}")
        print(f"🔤 Tier 2 tokens: {metadata.get('tier_2_tokens', 0)}")
        print(f"🔄 Fallback used: {metadata.get('fallback_used', False)}")

    if result.get('filepath'):
        print(f"📝 Blog post: {result['filepath']}")

    print("\n" + "=" * 50)

    # Test with two-tier analysis disabled (fallback)
    print("Test 2: Two-Tier Analysis DISABLED (fallback test)")

    result2 = generator.generate_daily_summary(
        target_date=date.today(),
        use_intelligent_synthesis=True,
        use_dynamic_title=True,
        use_dynamic_tags=True,
        use_two_tier_analysis=False
    )

    print(f"✅ Generation completed: {result2['success']}")
    print(f"🎯 Two-tier analysis used: {result2.get('two_tier_analysis_used', False)}")
    print(f"🔧 Synthesis method: {result2.get('metadata', {}).get('synthesis_method', 'unknown')}")

    print("\n🎉 Two-tier generator testing completed!")

if __name__ == "__main__":
    main()