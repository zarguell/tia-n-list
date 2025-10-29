#!/usr/bin/env python3
"""Enhance article content using the JSON-based system."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.json_processing import JSONProcessing

def main():
    """Main content enhancement function."""
    print("📰 Enhancing article content with full web scraping...")

    processor = JSONProcessing()
    result = processor.enhance_articles_content(max_articles=50)

    print(f"Content enhancement completed: {result['enhanced_articles']}/{result['total_articles']} articles enhanced")
    print("✅ Content enhancement completed")

if __name__ == "__main__":
    main()