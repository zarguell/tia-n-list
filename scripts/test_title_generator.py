#!/usr/bin/env python3
"""Test script for dynamic title generation."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.title_generator import TitleGenerator
from src.json_storage import JSONStorage
from datetime import date, timedelta

def test_title_generation():
    """Test title generation with real article data."""
    print("🎯 TESTING DYNAMIC TITLE GENERATION")
    print("=" * 50)

    # Initialize components
    storage = JSONStorage()
    title_generator = TitleGenerator()

    # Get recent articles
    end_date = date.today()
    start_date = end_date - timedelta(days=1)

    articles = storage.get_articles_by_date_range(
        start_date=start_date,
        end_date=end_date,
        status="processed"
    )

    if not articles:
        print("❌ No processed articles found for testing")
        print("   Running some sample tests with dummy data...")

        # Test with sample articles
        sample_articles = [
            {
                "id": "test-1",
                "title": "Critical CVE-2025-24893 actively exploited in ransomware attacks",
                "source_name": "Krebs on Security",
                "score": 95,
                "content": {
                    "processed": "Critical vulnerability CVE-2025-24893 is being actively exploited by ransomware groups"
                }
            },
            {
                "id": "test-2",
                "title": "Microsoft releases emergency patch for zero-day vulnerability",
                "source_name": "SecurityWeek",
                "score": 90,
                "content": {
                    "processed": "Microsoft has released an emergency security update for a zero-day vulnerability"
                }
            }
        ]
        articles = sample_articles

    print(f"📊 Found {len(articles)} articles for testing")

    # Test title generation
    print(f"\n🎯 Generating title for {end_date.strftime('%B %d, %Y')}...")

    generated_title = title_generator.generate_title(articles, end_date)

    print(f"\n✅ Generated Title:")
    print(f"   {generated_title}")
    print(f"   Length: {len(generated_title)} characters")

    # Test theme analysis
    themes = title_generator._analyze_articles_for_themes(articles)
    print(f"\n🔍 Identified Themes:")
    for theme, items in themes.items():
        if items:
            print(f"   {theme}: {items}")

    # Test template fallback
    print(f"\n🔄 Testing template-based title fallback...")

    # Save original LLM client
    original_client = title_generator.llm_client
    title_generator.llm_client = None  # Force template fallback

    template_title = title_generator.generate_title(articles, end_date)
    print(f"✅ Template Title: {template_title}")

    # Restore LLM client
    title_generator.llm_client = original_client

    # Test title uniqueness checking
    print(f"\n🔍 Testing title uniqueness...")
    test_titles = [
        "Critical CVE-2025-24893 Exploited - October 29, 2025",
        "Critical CVE-2025-24893 Exploited - October 29, 2025",  # Same as above
        "Different Title About Security - October 29, 2025"
    ]

    for title in test_titles:
        is_unique = title_generator._check_title_uniqueness(title)
        status = "✅ Unique" if is_unique else "❌ Duplicate"
        print(f"   {title[:50]}...: {status}")

    # Test statistics
    stats = title_generator.get_title_statistics()
    print(f"\n📊 Title Generator Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print(f"\n🎉 Title generation test completed!")


def test_llm_title_generation():
    """Test LLM-powered title generation specifically."""
    print("\n" + "=" * 50)
    print("🤖 TESTING LLM-POWERED TITLE GENERATION")
    print("=" * 50)

    try:
        from src.llm_client_multi import MultiLLMClient
        llm_client = MultiLLMClient()

        # Check provider configuration
        provider_info = llm_client.get_provider_info()
        print(f"🔗 LLM Provider: {provider_info}")
        print(f"   Has provider: {llm_client.provider is not None}")
        print(f"   Has fallback: {llm_client.fallback_provider is not None}")

        if provider_info['primary_provider'] == 'none':
            print("⚠️  No LLM provider configured - will use template fallback only")
            return

        # Get articles for testing
        storage = JSONStorage()
        end_date = date.today()
        start_date = end_date - timedelta(days=1)

        articles = storage.get_articles_by_date_range(
            start_date=start_date,
            end_date=end_date,
            status="processed"
        )

        if not articles:
            print("❌ No articles found for LLM testing")
            return

        # Sort by score and use top 3 for faster processing
        articles.sort(key=lambda x: x.get("analysis", {}).get("score", 0), reverse=True)
        articles = articles[:3]

        print(f"📊 Using top {len(articles)} articles for LLM testing")

        # Test LLM client directly
        print(f"🧪 Testing LLM client directly...")
        test_prompt = "Generate a short title for today's cybersecurity briefing:"
        try:
            direct_response = llm_client._execute_with_fallback(
                "generate_text",
                prompt=test_prompt,
                max_tokens=50,
                temperature=0.8
            )
            print(f"✅ Direct LLM test successful: {direct_response[:50]}...")
        except Exception as e:
            print(f"❌ Direct LLM test failed: {e}")

        # Generate LLM title
        title_generator = TitleGenerator(llm_client=llm_client)
        themes = title_generator._analyze_articles_for_themes(articles)

        print(f"🎯 Generating LLM-powered title...")
        llm_title = title_generator._generate_llm_title(articles, themes, end_date)

        if llm_title:
            print(f"✅ LLM Title Generated:")
            print(f"   {llm_title}")
            print(f"   Length: {len(llm_title)} characters")
            print(f"   Has emoji: {any(c in llm_title for c in '⚠️🔥🏢📊🎯🔍🚨')}")
        else:
            print("❌ LLM title generation failed")

    except Exception as e:
        print(f"❌ LLM testing failed: {e}")


if __name__ == "__main__":
    test_title_generation()
    test_llm_title_generation()