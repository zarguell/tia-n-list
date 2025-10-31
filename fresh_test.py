#!/usr/bin/env python3
"""Fresh test to bypass Python caching."""

import subprocess
import sys

def main():
    """Run a fresh test in a new process."""
    print("🔄 Testing two-tier generator in fresh process...")

    # Test code to run in new process
    test_code = '''
import sys
sys.path.insert(0, ".")
from src.two_tier_blog_generator import TwoTierBlogGenerator
from datetime import date

print("🧪 Testing Two-Tier Blog Generator in fresh process...")
generator = TwoTierBlogGenerator()
print("✅ TwoTierBlogGenerator initialized successfully!")

# Test basic functionality
result = generator.generate_daily_summary(
    target_date=date.today(),
    use_two_tier_analysis=True
)

print(f"✅ Generation completed: {result['success']}")
print(f"📄 Content length: {result.get('content_length', 0)} characters")
print(f"🎯 Two-tier analysis used: {result.get('two_tier_analysis_used', False)}")

if result.get('metadata'):
    metadata = result['metadata']
    print(f"📊 Tier 1 success: {metadata.get('tier_1_success', False)}")
    print(f"📊 Tier 2 success: {metadata.get('tier_2_success', False)}")
    print(f"🔤 Tier 1 tokens: {metadata.get('tier_1_tokens', 0)}")
    print(f"🔤 Tier 2 tokens: {metadata.get('tier_2_tokens', 0)}')
    print(f"🔄 Fallback used: {metadata.get('fallback_used', False)}")

if result.get('filepath'):
    print(f"📝 Blog post: {result['filepath']}")

print("🎉 Fresh process test completed!")
'''

    # Run in fresh Python process
    result = subprocess.run([
        sys.executable, '-c', test_code
    ], capture_output=True, text=True, cwd='.')

    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    print(f"Return code: {result.returncode}")

if __name__ == "__main__":
    main()