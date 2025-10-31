#!/usr/bin/env python3
"""Simple test for two-tier functionality."""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

def test_prompt_loader():
    """Test that the new PromptLoader methods work."""
    print("🧪 Testing PromptLoader two-tier methods...")

    try:
        from src.prompt_loader import PromptLoader

        loader = PromptLoader(Path("config/prompts"))

        # Test loading tier coordination config
        try:
            config = loader.load_tier_coordination_config()
            print("✅ Tier coordination config loaded successfully")
            print(f"   Workflow enabled: {config.get('workflow_configuration', {}).get('enabled', 'unknown')}")
        except Exception as e:
            print(f"❌ Tier coordination config failed: {e}")

        # Test loading synthesis template
        try:
            template = loader.load_synthesis_prompt()
            print("✅ Synthesis template loaded successfully")
            print(f"   Template version: {template.version}")
            print(f"   Description: {template.description}")
        except Exception as e:
            print(f"❌ Synthesis template failed: {e}")

        # Test loading enhancement template
        try:
            template = loader.load_enhancement_prompt()
            print("✅ Enhancement template loaded successfully")
            print(f"   Template version: {template.version}")
            print(f"   Description: {template.description}")
        except Exception as e:
            print(f"❌ Enhancement template failed: {e}")

        # Test building synthesis prompt
        try:
            prompt = loader.build_synthesis_prompt(
                articles_data="Test article data",
                factual_constraints="Test constraints",
                current_date="October 30, 2025"
            )
            print("✅ Synthesis prompt built successfully")
            print(f"   Prompt length: {len(prompt)} characters")
        except Exception as e:
            print(f"❌ Synthesis prompt building failed: {e}")

        print("🎉 PromptLoader two-tier methods test completed!")

    except Exception as e:
        print(f"❌ PromptLoader import failed: {e}")
        import traceback
        traceback.print_exc()

def test_two_tier_generator():
    """Test the TwoTierBlogGenerator class."""
    print("\n🧪 Testing TwoTierBlogGenerator...")

    try:
        # Clear Python module cache
        modules_to_clear = [k for k in sys.modules.keys() if k.startswith('src')]
        for module in modules_to_clear:
            del sys.modules[module]

        from src.two_tier_blog_generator import TwoTierBlogGenerator

        generator = TwoTierBlogGenerator()
        print("✅ TwoTierBlogGenerator initialized successfully")

        # Test tier coordination config loading
        if hasattr(generator, 'coordination_config'):
            print("✅ Tier coordination config loaded")
        else:
            print("❌ Tier coordination config not loaded")

        print("🎉 TwoTierBlogGenerator test completed!")

    except Exception as e:
        print(f"❌ TwoTierBlogGenerator test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prompt_loader()
    test_two_tier_generator()