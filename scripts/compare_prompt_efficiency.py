#!/usr/bin/env python3
"""Compare current vs optimized prompt efficiency."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.json_storage import JSONStorage
from src.context_builder import AIContextBuilder
from src.intelligent_blog_generator import ThreatIntelligenceSynthesizer
from src.optimized_prompt_generator import OptimizedPromptGenerator
from datetime import date

def main():
    """Compare prompt efficiency."""
    print("🔬 PROMPT EFFICIENCY COMPARISON")
    print("=" * 50)

    # Set up components
    storage = JSONStorage()
    context_builder = AIContextBuilder(storage)
    synthesizer = ThreatIntelligenceSynthesizer()
    optimizer = OptimizedPromptGenerator()

    # Get recent articles
    articles = storage.get_articles_by_date_range(
        start_date=date.fromordinal(date.today().toordinal() - 3),
        end_date=date.today(),
        status="processed"
    )

    # Sort by score and limit
    articles.sort(key=lambda x: x.get("analysis", {}).get("score", 0), reverse=True)
    articles = articles[:24]

    print(f"📊 Dataset: {len(articles)} articles")

    if not articles:
        print("❌ No articles found for comparison")
        return

    # Test CURRENT prompt
    print("\n" + "=" * 50)
    print("📋 CURRENT PROMPT ANALYSIS")
    print("=" * 50)

    current_context = synthesizer.prepare_threat_landscape_context(articles, {})
    current_constraints = synthesizer._extract_factual_constraints(articles)
    current_prompt = synthesizer.create_comprehensive_analysis_prompt(current_context, current_constraints)

    current_tokens = len(current_prompt.split()) * 1.3
    current_chars = len(current_prompt)
    current_lines = len(current_prompt.split('\n'))

    print(f"📏 Current prompt:")
    print(f"   Characters: {current_chars:,}")
    print(f"   Lines: {current_lines}")
    print(f"   Estimated tokens: {current_tokens:.0f}")
    print(f"   Articles included: {len(articles)}")

    # Test OPTIMIZED prompt
    print("\n" + "=" * 50)
    print("⚡ OPTIMIZED PROMPT ANALYSIS")
    print("=" * 50)

    optimized_constraints = synthesizer._extract_factual_constraints(articles)
    optimized_prompt = optimizer.create_compact_prompt(articles, optimized_constraints)

    optimized_tokens = len(optimized_prompt.split()) * 1.3
    optimized_chars = len(optimized_prompt)
    optimized_lines = len(optimized_prompt.split('\n'))

    print(f"📏 Optimized prompt:")
    print(f"   Characters: {optimized_chars:,}")
    print(f"   Lines: {optimized_lines}")
    print(f"   Estimated tokens: {optimized_tokens:.0f}")
    print(f"   Articles included: {min(20, len(articles))}")

    # COMPARISON
    print("\n" + "=" * 50)
    print("📈 COMPARISON RESULTS")
    print("=" * 50)

    char_reduction = current_chars - optimized_chars
    token_reduction = current_tokens - optimized_tokens
    char_savings_pct = (char_reduction / current_chars) * 100
    token_savings_pct = (token_reduction / current_tokens) * 100

    print(f"💰 Cost Savings:")
    print(f"   Characters saved: {char_reduction:,} ({char_savings_pct:.1f}%)")
    print(f"   Tokens saved: {token_reduction:.0f} ({token_savings_pct:.1f}%)")
    print(f"   Estimated cost saved: ${token_reduction/1000 * 0.00015:.4f} per synthesis")

    print(f"\n📊 Quality Impact:")
    print(f"   Articles included: {len(articles)} → {min(20, len(articles))} ({min(20, len(articles))/len(articles)*100:.1f}%)")
    print(f"   Prompt complexity: {current_lines} → {optimized_lines} lines")

    # Content samples
    print(f"\n📝 PROMPT SAMPLES:")
    print(f"Current (first 200 chars): {current_prompt[:200]}...")
    print(f"Optimized (first 200 chars): {optimized_prompt[:200]}...")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if token_savings_pct > 20:
        print(f"   ✅ Excellent token savings ({token_savings_pct:.1f}%) - implement optimized prompt")
    elif token_savings_pct > 10:
        print(f"   ⚠️  Good token savings ({token_savings_pct:.1f}%) - consider optimization")
    else:
        print(f"   ❌ Minimal savings ({token_savings_pct:.1f}%) - keep current prompt")

    if min(20, len(articles)) < len(articles):
        print(f"   ⚠️  Optimized prompt includes fewer articles - may miss relevant content")
    else:
        print(f"   ✅ Same article coverage")

if __name__ == "__main__":
    main()