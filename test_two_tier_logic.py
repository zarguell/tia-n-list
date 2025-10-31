#!/usr/bin/env python3
"""Simple test for two-tier logic without LLM calls."""

import sys
sys.path.insert(0, ".")

def main():
    """Test two-tier logic without LLM calls."""
    print("🧪 Testing two-tier logic...")

    # Clear Python module cache
    modules_to_clear = [k for k in sys.modules.keys() if k.startswith('src')]
    for module in modules_to_clear:
        del sys.modules[module]

    try:
        from src.two_tier_blog_generator import TwoTierBlogGenerator
        from datetime import date

        print("✅ TwoTierBlogGenerator imported successfully")

        # Create generator
        generator = TwoTierBlogGenerator()
        print("✅ Generator initialized successfully")

        # Test Tier 1 synthesis prompt building
        print("\n📝 Testing Tier 1 synthesis prompt building...")

        # Mock articles data
        mock_articles = [
            {
                'title': 'Critical vulnerability discovered',
                'source': 'TestSource',
                'content': {
                    'raw': 'Test content here',
                    'full': 'Full test content here'
                }
            },
            {
                'title': 'New malware variant detected',
                'source': 'TestSource2',
                'content': {
                    'raw': 'Test content 2',
                    'full': 'Full test content 2'
                }
            }
        ]

        mock_context = {
            'articles': mock_articles
        }

        # Test Tier 1 synthesis
        tier1_result = generator._tier1_synthesis(mock_context)
        print(f"📊 Tier 1 result: success={tier1_result['success']}, error={tier1_result.get('error', 'None')}")

        if tier1_result['success']:
            content_preview = tier1_result['content'][:200] if tier1_result['content'] else 'No content'
            print(f"📄 Tier 1 content preview: {content_preview}...")

        # Test Tier 2 enhancement if Tier 1 succeeded
        if tier1_result['success']:
            print("\n🎨 Testing Tier 2 enhancement prompt building...")
            tier2_result = generator._tier2_enhancement(tier1_result['content'], mock_context)
            print(f"📊 Tier 2 result: success={tier2_result['success']}, error={tier2_result.get('error', 'None')}")

            if tier2_result['success']:
                content_preview = tier2_result['content'][:200] if tier2_result['content'] else 'No content'
                print(f"📄 Tier 2 content preview: {content_preview}...")

        print("\n🎉 Two-tier logic test completed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()