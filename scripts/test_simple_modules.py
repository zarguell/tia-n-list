#!/usr/bin/env python3
"""
Simple test runner for the simplified digest system modules.
Does not require pytest - uses basic assertions.
"""

import sys
import tempfile
import json
from pathlib import Path
from datetime import date

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.simple_memory import SimpleMemory
from src.simple_digest_generator import SimpleDigestGenerator
from src.workflow_config import get_workflow_config


def test_simple_memory():
    """Test SimpleMemory functionality."""
    print("🧪 Testing SimpleMemory...")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = Path(f.name)

    try:
        # Test initialization
        memory = SimpleMemory(temp_file)
        assert "used_articles" in memory._memory_data
        assert "last_cleanup" in memory._memory_data
        print("  ✅ Memory initialization works")

        # Test marking articles as used
        target_date = date(2025, 11, 7)
        article_ids = ["article-1", "article-2"]
        memory.mark_articles_used(article_ids, target_date)

        used = memory.get_used_articles(target_date)
        assert used == {"article-1", "article-2"}
        print("  ✅ Marking articles as used works")

        # Test statistics
        stats = memory.get_statistics()
        assert stats["total_days"] == 1
        assert stats["total_articles"] == 2
        print("  ✅ Memory statistics work")

        # Test persistence across instances
        memory2 = SimpleMemory(temp_file)
        used2 = memory2.get_used_articles(target_date)
        assert used2 == {"article-1", "article-2"}
        print("  ✅ Memory persistence works")

        print("✅ SimpleMemory tests passed")
        return True

    except Exception as e:
        print(f"❌ SimpleMemory test failed: {e}")
        return False
    finally:
        if temp_file.exists():
            temp_file.unlink()


def test_workflow_config():
    """Test workflow configuration."""
    print("🧪 Testing WorkflowConfig...")

    try:
        # Test configuration loading
        config = get_workflow_config()
        assert config is not None
        print("  ✅ Configuration loading works")

        # Test getting settings
        workflow_settings = config.get_workflow_settings()
        assert isinstance(workflow_settings, dict)
        assert "max_articles_per_feed" in workflow_settings
        print("  ✅ Workflow settings retrieval works")

        # Test dot notation access
        max_articles = config.get('workflow_settings.max_articles_per_feed')
        assert isinstance(max_articles, int)
        assert max_articles > 0
        print("  ✅ Dot notation access works")

        # Test default values
        nonexistent = config.get('nonexistent.key', 'default')
        assert nonexistent == 'default'
        print("  ✅ Default value handling works")

        print("✅ WorkflowConfig tests passed")
        return True

    except Exception as e:
        print(f"❌ WorkflowConfig test failed: {e}")
        return False


def test_simple_digest_generator():
    """Test SimpleDigestGenerator functionality."""
    print("🧪 Testing SimpleDigestGenerator...")

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Create temp directories and files
            data_dir = Path(temp_dir) / "data"
            hugo_dir = Path(temp_dir) / "hugo" / "content" / "posts"
            config_dir = Path(temp_dir) / "config" / "prompts"

            data_dir.mkdir(parents=True)
            hugo_dir.mkdir(parents=True)
            config_dir.mkdir(parents=True)

            # Create sample prompt file
            prompt_file = config_dir / "simple_digest.json"
            prompt_template = {
                "version": "1.0.0",
                "description": "Test prompt template",
                "template": "Test prompt for {{current_date}} with {{articles_summary}}",
                "variables": ["current_date", "articles_summary"]
            }

            with open(prompt_file, 'w') as f:
                json.dump(prompt_template, f)

            # Test generator initialization
            memory_file = data_dir / "test_memory.json"
            generator = SimpleDigestGenerator(
                memory_file=memory_file,
                prompt_file=prompt_file
            )
            assert generator.storage is not None
            assert generator.llm_registry is not None
            print("  ✅ Generator initialization works")

            # Test prompt loading
            loaded_template = generator._load_prompt_template()
            assert "template" in loaded_template
            print("  ✅ Prompt template loading works")

            # Test theme extraction
            sample_articles = [
                {"title": "Critical Vulnerability in Enterprise Software"},
                {"title": "New Malware Campaign Targets Healthcare"},
                {"title": "Microsoft Security Update"}
            ]

            themes = generator._extract_themes(sample_articles)
            assert "Vulnerability" in themes
            assert "Malware" in themes
            assert "Tech Giants" in themes  # From Microsoft
            print("  ✅ Theme extraction works")

            # Test title generation
            target_date = date(2025, 11, 7)
            title = generator._generate_title(target_date, sample_articles)
            assert "November 07, 2025" in title
            print("  ✅ Title generation works")

            # Test metadata generation
            metadata = generator._generate_hugo_metadata(target_date, sample_articles)
            assert "title" in metadata
            assert "tags" in metadata
            assert "author" in metadata
            assert metadata["author"] == "Tia N. List"
            print("  ✅ Metadata generation works")

            print("✅ SimpleDigestGenerator tests passed")
            return True

        except Exception as e:
            print(f"❌ SimpleDigestGenerator test failed: {e}")
            return False


def test_configuration_constants():
    """Test configuration constants."""
    print("🧪 Testing configuration constants...")

    try:
        from src.simple_digest_generator import (
            MAX_ARTICLES_FOR_PROMPT, MAX_CONTENT_LENGTH, MIN_CONTENT_LENGTH,
            MAX_REFERENCES, MEMORY_DAYS_BACK, MEMORY_CLEANUP_DAYS, MAX_TOKENS
        )

        assert MAX_ARTICLES_FOR_PROMPT > 0
        assert MAX_CONTENT_LENGTH > 0
        assert MIN_CONTENT_LENGTH > 0
        assert MAX_REFERENCES > 0
        assert MEMORY_DAYS_BACK > 0
        assert MEMORY_CLEANUP_DAYS > 0
        assert MAX_TOKENS > 0

        print("  ✅ All configuration constants are positive")
        print("✅ Configuration constants tests passed")
        return True

    except Exception as e:
        print(f"❌ Configuration constants test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Simple Digest System Test Suite")
    print("=" * 50)

    tests = [
        test_workflow_config,
        test_configuration_constants,
        test_simple_memory,
        test_simple_digest_generator
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())