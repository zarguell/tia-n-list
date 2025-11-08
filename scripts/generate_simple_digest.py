#!/usr/bin/env python3
"""
Simple digest generation script.
Replaces complex enterprise blog generation with streamlined RSS→digest workflow.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.simple_digest_generator import SimpleDigestGenerator
from datetime import date


def main():
    """Generate a simple daily threat intelligence digest."""
    print("🚀 Starting Simple Digest Generation")
    print("=" * 50)

    try:
        # Initialize the simple digest generator
        generator = SimpleDigestGenerator()

        # Generate today's digest
        target_date = date.today()
        hugo_filename = generator.generate_daily_digest(target_date)

        if hugo_filename:
            print(f"\n✅ Simple digest generated successfully!")
            print(f"📄 Hugo post: {hugo_filename}")

            # Show memory statistics
            stats = generator.get_memory_statistics()
            print(f"\n📊 Memory Statistics:")
            print(f"   Total days tracked: {stats['total_days']}")
            print(f"   Total articles used: {stats['total_articles']}")
            print(f"   Recent articles (7d): {stats['recent_articles_7d']}")

            if stats['oldest_date']:
                print(f"   Date range: {stats['oldest_date']} to {stats['newest_date']}")

        else:
            print("\nℹ️  No digest generated - no fresh content available")
            return 1

    except Exception as e:
        print(f"\n❌ Error generating simple digest: {e}")
        return 1

    print("=" * 50)
    print("🎉 Simple Digest Generation Complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())