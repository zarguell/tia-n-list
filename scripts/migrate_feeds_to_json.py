#!/usr/bin/env python3
"""Migrate RSS feeds from YAML configuration to JSON source configurations.

This script converts feeds.yml to individual JSON source configuration files
in the data/sources/ directory for the new JSON-based architecture.
"""

import yaml
import json
from pathlib import Path
import sys
import re

def slugify(name: str) -> str:
    """Convert a name to a URL-safe slug."""
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def migrate_feeds():
    """Migrate feeds from YAML to JSON configuration."""
    config_file = Path("config/feeds.yml")

    if not config_file.exists():
        print(f"❌ Configuration file not found: {config_file}")
        return False

    # Load YAML configuration
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    feeds = config.get('feeds', [])
    if not feeds:
        print("❌ No feeds found in configuration")
        return False

    print(f"🔄 Migrating {len(feeds)} feeds from YAML to JSON...")

    # Ensure data/sources directory exists
    sources_dir = Path("data/sources")
    sources_dir.mkdir(parents=True, exist_ok=True)

    migrated_count = 0
    skipped_count = 0

    for feed in feeds:
        name = feed.get('name', '').strip()
        url = feed.get('url', '').strip()

        if not name or not url:
            print(f"⚠️  Skipping incomplete feed: {name}")
            skipped_count += 1
            continue

        # Generate source ID
        source_id = slugify(name)

        # Create JSON configuration
        source_config = {
            "id": source_id,
            "name": name,
            "url": url,
            "last_fetched": None,
            "fetch_interval_hours": 1,
            "quality_score": 50,  # Default score, will be updated based on performance
            "active": True,
            "created_at": "2025-10-29T00:00:00Z",
            "metadata": {
                "language": "en",
                "region": "global",
                "focus_areas": ["cybersecurity", "threat-intelligence"],
                "content_quality": "unknown",
                "description": f"{name} RSS feed for cybersecurity news and analysis"
            }
        }

        # Write JSON file
        json_file = sources_dir / f"{source_id}.json"

        # Check if file already exists
        if json_file.exists():
            print(f"⚠️  Skipping existing source: {name} ({source_id})")
            skipped_count += 1
            continue

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(source_config, f, indent=2, ensure_ascii=False)

        print(f"✅ Migrated: {name} → {source_id}.json")
        migrated_count += 1

    print(f"\n📊 Migration Summary:")
    print(f"   Total feeds in YAML: {len(feeds)}")
    print(f"   Successfully migrated: {migrated_count}")
    print(f"   Skipped (existing/incomplete): {skipped_count}")

    # Test the migration
    print(f"\n🧪 Testing migrated sources...")
    try:
        from src.json_storage import JSONStorage
        storage = JSONStorage()
        sources = storage.get_all_sources()
        print(f"✅ Found {len(sources)} sources in JSON storage")

        # Show first few sources
        for source in sources[:3]:
            print(f"   - {source['id']}: {source['name']} ({source['url']})")

    except ImportError as e:
        print(f"⚠️  Could not test JSON storage (missing dependencies): {e}")
    except Exception as e:
        print(f"❌ Error testing JSON storage: {e}")

    return migrated_count > 0

def main():
    """Main migration function."""
    print("🔄 YAML to JSON Feed Migration")
    print("=" * 40)

    success = migrate_feeds()

    if success:
        print(f"\n✅ Migration completed successfully!")
        print(f"\nNext steps:")
        print(f"1. Test the JSON-based ingestion:")
        print(f"   PYTHONPATH=. python -m src.json_ingestion")
        print(f"2. Review the migrated source configurations in data/sources/")
        print(f"3. Update quality scores based on source performance")
        print(f"4. Consider deprecating the old config/feeds.yml file")
    else:
        print(f"\n❌ Migration failed or no feeds were migrated")
        sys.exit(1)

if __name__ == "__main__":
    main()