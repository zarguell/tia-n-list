#!/usr/bin/env python3
"""Test basic import without new methods."""

import sys
sys.path.insert(0, ".")

def main():
    """Test basic import."""
    print("Testing basic PromptLoader import...")

    from src.prompt_loader import PromptLoader
    from pathlib import Path

    loader = PromptLoader(Path("config/prompts"))
    print("✅ PromptLoader imported successfully")

    # Test existing methods
    try:
        main_prompt = loader.load_main_prompt()
        print(f"✅ load_main_prompt works: {main_prompt.version}")
    except Exception as e:
        print(f"❌ load_main_prompt failed: {e}")

    # Check if new methods exist
    print(f"Has load_tier_coordination_config: {hasattr(loader, 'load_tier_coordination_config')}")
    print(f"Has load_synthesis_prompt: {hasattr(loader, 'load_synthesis_prompt')}")
    print(f"Has build_synthesis_prompt: {hasattr(loader, 'build_synthesis_prompt')}")

    # List all methods
    methods = [m for m in dir(loader) if not m.startswith('_') and callable(getattr(loader, m))]
    print(f"Available methods: {len(methods)}")
    for method in sorted(methods):
        print(f"  - {method}")

if __name__ == "__main__":
    main()