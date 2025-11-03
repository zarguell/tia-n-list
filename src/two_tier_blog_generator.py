"""Two-tier blog generator with focused synthesis and enterprise enhancement."""

import os
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from .enhanced_json_blog_generator import EnhancedJSONBlogGenerator
from .prompt_loader import PromptLoader
from .context_builder import AIContextBuilder
from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider
from .llm_registry import get_registry


class TwoTierBlogGenerator(EnhancedJSONBlogGenerator):
    """Enhanced blog generator with two-tier analysis architecture."""

    def __init__(self):
        """Initialize the two-tier blog generator."""
        super().__init__()

        # Load two-tier specific components
        self.prompt_loader = PromptLoader(Path("config/prompts"))
        self.context_builder = AIContextBuilder()
        self.storage = get_default_storage_provider()
        self.llm_registry = get_registry()

        # Load tier coordination configuration
        try:
            self.coordination_config = self.prompt_loader.load_tier_coordination_config()
            self.tier_config = self.coordination_config.get("tier_configurations", {})
        except FileNotFoundError:
            # Fallback configuration
            self.coordination_config = {
                "workflow_configuration": {
                    "enabled": True,
                    "fallback_strategy": "single_tier_on_failure"
                }
            }
            self.tier_config = {
                "synthesis": {"token_budget": 2400},
                "enhancement": {"token_budget": 800}
            }

    def _generate_dynamic_title(self, articles: List[Dict[str, Any]]) -> Optional[str]:
        """Generate dynamic title based on articles.

        Args:
            articles: List of articles to analyze

        Returns:
            Dynamic title or None if generation fails
        """
        try:
            from .title_generator import TitleGenerator
            title_generator = TitleGenerator(self.storage)
            return title_generator.generate_title(articles, date.today())
        except Exception as e:
            print(f"⚠️ Dynamic title generation failed: {e}")
            return None

    def _generate_dynamic_tags(self, target_date: date) -> List[str]:
        """Generate dynamic tags for the target date.

        Args:
            target_date: Target date for tag generation

        Returns:
            List of dynamic tags
        """
        try:
            from .tag_generator import TagGenerator
            tag_generator = TagGenerator(self.storage)
            return tag_generator.generate_tags_for_date(target_date, limit=15)
        except Exception as e:
            print(f"⚠️ Dynamic tag generation failed: {e}")
            return []

    def generate_daily_summary(self,
                             target_date: date = None,
                             use_intelligent_synthesis: bool = True,
                             use_dynamic_title: bool = True,
                             use_dynamic_tags: bool = True,
                             use_two_tier_analysis: bool = None) -> Dict[str, Any]:
        """Generate daily summary with optional two-tier analysis.

        Args:
            target_date: Target date for summary generation
            use_intelligent_synthesis: Use intelligent synthesis
            use_dynamic_title: Use dynamic title generation
            use_dynamic_tags: Use dynamic tag generation
            use_two_tier_analysis: Use two-tier analysis (None = check env var)

        Returns:
            Generation result dictionary
        """
        if target_date is None:
            target_date = date.today()

        # Check if two-tier analysis is enabled
        if use_two_tier_analysis is None:
            use_two_tier_analysis = os.getenv('USE_TWO_TIER_ANALYSIS', 'false').lower() == 'true'

        print(f"🚀 Starting two-tier enhanced blog generation for {target_date}...")
        print(f"📊 Two-tier analysis: {'✅ ENABLED' if use_two_tier_analysis else '❌ DISABLED'}")

        # Generate context
        context = self._build_generation_context(target_date)

        # Generate content using appropriate method
        if use_two_tier_analysis:
            content, metadata = self._two_tier_synthesis(context)
        else:
            # Fallback to original enhanced method
            content, metadata = self._intelligent_synthesis(context)

        # Add two-tier analysis flag to metadata
        metadata['two_tier_analysis_used'] = use_two_tier_analysis

        # Add dynamic elements
        if use_dynamic_title:
            dynamic_title = self._generate_dynamic_title(context['articles'])
            metadata['dynamic_title_used'] = dynamic_title is not None
        else:
            dynamic_title = f"Daily Threat Intelligence Briefing - {target_date.strftime('%B %d, %Y')}"
            metadata['dynamic_title_used'] = False

        if use_dynamic_tags:
            dynamic_tags = self._generate_dynamic_tags(target_date)
            metadata['dynamic_tags_used'] = len(dynamic_tags) > 0
            metadata['generated_tags_count'] = len(dynamic_tags)
        else:
            dynamic_tags = []
            metadata['dynamic_tags_used'] = False
            metadata['generated_tags_count'] = 0

        # Build complete Hugo post
        hugo_content = self._build_hugo_post(
            title=dynamic_title,
            content=content,
            target_date=target_date,
            tags=dynamic_tags,
            metadata=metadata
        )

        # Write to file
        filepath = self._write_hugo_post(hugo_content, target_date)

        return {
            'success': True,
            'filepath': filepath,
            'content_length': len(content),
            'dynamic_title_used': metadata.get('dynamic_title_used', False),
            'dynamic_tags_used': metadata.get('dynamic_tags_used', False),
            'intelligent_synthesis_used': metadata.get('intelligent_synthesis_used', False),
            'generated_tags_count': metadata.get('generated_tags_count', 0),
            'two_tier_analysis_used': use_two_tier_analysis,
            'metadata': metadata
        }

    def _two_tier_synthesis(self, context: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate content using two-tier analysis approach.

        Args:
            context: Generation context with articles and data

        Returns:
            Tuple of (content, metadata)
        """
        metadata = {
            'synthesis_method': 'two_tier',
            'tier_1_success': False,
            'tier_2_success': False,
            'tier_1_tokens': 0,
            'tier_2_tokens': 0,
            'tier_1_provider': None,
            'tier_2_provider': None,
            'fallback_used': False
        }

        try:
            print("🔧 Attempting two-tier synthesis...")

            # Tier 1: Pure Synthesis
            print("📊 Tier 1: Running pure threat intelligence synthesis...")
            tier1_result = self._tier1_synthesis(context)

            if tier1_result['success']:
                metadata.update({
                    'tier_1_success': True,
                    'tier_1_tokens': tier1_result['tokens_used'],
                    'tier_1_provider': tier1_result['provider']
                })
                print(f"✅ Tier 1 synthesis successful ({tier1_result['tokens_used']} tokens)")

                # Tier 2: Enterprise Enhancement
                print("🎨 Tier 2: Applying enterprise frameworks...")
                tier2_result = self._tier2_enhancement(
                    synthesis_output=tier1_result['content'],
                    context=context
                )

                if tier2_result['success']:
                    metadata.update({
                        'tier_2_success': True,
                        'tier_2_tokens': tier2_result['tokens_used'],
                        'tier_2_provider': tier2_result['provider']
                    })
                    print(f"✅ Tier 2 enhancement successful ({tier2_result['tokens_used']} tokens)")
                    print(f"🎉 Two-tier synthesis completed: {tier2_result['tokens_used'] + tier1_result['tokens_used']} total tokens")

                    return tier2_result['content'], metadata
                else:
                    print(f"⚠️ Tier 2 enhancement failed: {tier2_result.get('error', 'Unknown error')}")
                    print("🔄 Using Tier 1 output with basic formatting...")
                    metadata['fallback_used'] = True
                    return self._format_tier1_for_hugo(tier1_result['content']), metadata
            else:
                print(f"⚠️ Tier 1 synthesis failed: {tier1_result.get('error', 'Unknown error')}")
                metadata['fallback_used'] = True

        except Exception as e:
            print(f"❌ Two-tier synthesis failed: {str(e)}")
            metadata['fallback_used'] = True

        # Fallback to single-tier approach
        print("🔄 Falling back to single-tier enhanced synthesis...")
        try:
            return self._intelligent_synthesis(context)
        except Exception as fallback_error:
            print(f"❌ Single-tier fallback also failed: {str(fallback_error)}")
            # Final fallback to template generation
            return self._template_based_generation(context), metadata

    def _tier1_synthesis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Tier 1: Pure threat intelligence synthesis (focused technical analysis).

        Args:
            context: Generation context

        Returns:
            Tier 1 synthesis result
        """
        try:
            print("📝 Tier 1: Building focused technical analysis prompt...")

            # Create a focused synthesis prompt without enterprise formatting
            articles = context.get('articles', [])
            if not articles:
                return {
                    'success': False,
                    'error': 'No articles available for synthesis',
                    'content': '',
                    'tokens_used': 0,
                    'provider': None
                }

            # Prepare focused articles data for technical analysis
            articles_data = ""
            for i, article in enumerate(articles[:15], 1):  # Limit to 15 for Tier 1
                articles_data += f"{i}. **{article['title']}**\n"
                articles_data += f"   Source: {article.get('source', 'Unknown')}\n"

                # Extract content safely
                content_text = ""
                if isinstance(article.get('content'), dict):
                    content_dict = article['content']
                    processed = content_dict.get('processed') or ''
                    full = content_dict.get('full') or ''
                    raw = content_dict.get('raw') or ''
                    content_text = processed or full or raw
                elif isinstance(article.get('content'), str):
                    content_text = article['content']
                else:
                    content_text = str(article.get('content', '')) if article.get('content') else ""

                if not isinstance(content_text, str) or not content_text:
                    content_text = str(content_text) if content_text else ""

                # Shorter content for Tier 1 (more focused)
                articles_data += f"   Content: {content_text[:300]}...\n\n"

            # Build simple Tier 1 synthesis prompt directly
            tier1_prompt = f"""You are Tia N. List, a threat intelligence analyst focusing on technical analysis.

TASK: Generate a comprehensive technical threat intelligence analysis based on the provided articles.

FOCUS AREAS:
- New vulnerabilities and exploits
- Active threat campaigns and actor TTPs
- Malware families and delivery mechanisms
- Data breaches and compromise impacts
- Emerging attack patterns and trends

DATE: {datetime.now().strftime('%B %d, %Y')}

SOURCE ARTICLES:
{articles_data}

REQUIREMENTS:
1. Provide detailed technical analysis
2. Include specific IOCs, TTPs, and technical indicators
3. Focus on technical details and security implications
4. Structure analysis with clear sections
5. Do not invent information beyond the articles
6. Maintain technical accuracy and precision

OUTPUT FORMAT:
Generate structured technical analysis with these sections:
1. Executive Technical Summary
2. Critical Threats (detailed technical analysis)
3. Vulnerability Analysis (technical details)
4. Threat Actor Activity (TTPs and patterns)
5. Indicators and Findings (IOCs and security insights)

Focus on technical precision and actionable security insights."""

            # Use direct OpenRouter synthesis to get token usage
            print("🤖 Tier 1: Running LLM synthesis...")
            try:
                content, tokens_used, provider_used = self._direct_synthesis_with_token_tracking(
                    prompt=tier1_prompt,
                    max_tokens=2400,  # Tier 1 token budget
                    tier_name="Tier 1"
                )

                return {
                    'success': True,
                    'content': content,
                    'tokens_used': tokens_used,
                    'provider': provider_used
                }
            except Exception as e:
                print(f"❌ Tier 1 synthesis failed: {str(e)}")
                return {
                    'success': False,
                    'error': str(e),
                    'content': '',
                    'tokens_used': 0,
                    'provider': None
                }

        except Exception as e:
            print(f"❌ Tier 1 synthesis failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'tokens_used': 0,
                'provider': None
            }

    def _tier2_enhancement(self, synthesis_output: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Tier 2: Enterprise framework enhancement (apply enterprise formatting to Tier 1 output).

        Args:
            synthesis_output: Output from Tier 1 synthesis
            context: Generation context

        Returns:
            Tier 2 enhancement result
        """
        try:
            print("🎨 Tier 2: Applying enterprise frameworks to technical analysis...")

            # Build enterprise enhancement prompt that transforms Tier 1 technical output
            enhancement_prompt = f"""You are Tia N. List, a Senior Threat Intelligence Analyst preparing C-level executive briefings.

TASK: Transform the following technical threat intelligence analysis into an executive briefing with business impact framing.

TECHNICAL ANALYSIS INPUT:
{synthesis_output}

ENTERPRISE ENHANCEMENT REQUIREMENTS:

1. **Executive Summary Transformation**:
   - Convert technical details to business impact scenarios
   - Create risk-prioritized table with confidence levels
   - Focus on what executives need to know for decision-making

2. **Business Impact Analysis**:
   - Translate vulnerabilities to business risk scenarios
   - Quantify potential financial, operational, and regulatory impact
   - Assess industry-specific exposure

3. **Confidence Assessment**:
   - Apply High/Medium/Low confidence levels to all assessments
   - Provide clear rationale for business decision-making
   - Use standard confidence assessment framework

4. **MITRE ATT&CK Integration**:
   - Map TTPs to MITRE ATT&CK techniques with detection guidance
   - Include specific log sources and behavioral indicators
   - Provide response priorities based on technique categories

5. **Industry Impact Assessment**:
   - Identify specific industries at risk
   - Quantify exposure levels by sector
   - Provide sector-specific recommendations

6. **Intelligence Gap Analysis**:
   - Identify what we don't know and why it matters
   - Prioritize intelligence collection needs
   - Be transparent about information limitations

EXECUTIVE BRIEFING FORMAT:

**Date**: {datetime.now().strftime('%B %d, %Y')}
**Prepared by**: Tia N. List, Senior Threat Intelligence Analyst

---

## Executive Summary
[Risk-prioritized table with business impact and confidence levels]

## Threat Landscape Analysis
[Business impact framing with MITRE ATT&CK integration]

## Risk Quantification
[Financial, operational, and regulatory impact assessment]

## Intelligence Gaps
[Limitations and collection priorities]

## Strategic Recommendations
[Actionable guidance for executive decision-making]

STYLE REQUIREMENTS:
- Professional C-level tone throughout
- Business impact prioritized over technical details
- Clear confidence level annotations
- Strategic focus for decision-makers
- Concise but comprehensive analysis

Date: {datetime.now().strftime('%B %d, %Y')}"""

            # Use direct OpenRouter synthesis to get token usage
            print("🤖 Tier 2: Running LLM enhancement...")
            try:
                content, tokens_used, provider_used = self._direct_synthesis_with_token_tracking(
                    prompt=enhancement_prompt,
                    max_tokens=800,  # Tier 2 token budget
                    tier_name="Tier 2"
                )

                return {
                    'success': True,
                    'content': content,
                    'tokens_used': tokens_used,
                    'provider': provider_used
                }
            except Exception as e:
                print(f"❌ Tier 2 enhancement failed: {str(e)}")
                return {
                    'success': False,
                    'error': str(e),
                    'content': '',
                    'tokens_used': 0,
                    'provider': None
                }

        except Exception as e:
            print(f"❌ Tier 2 enhancement failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'tokens_used': 0,
                'provider': None
            }

    def _format_tier1_for_hugo(self, tier1_content: str) -> str:
        """Format Tier 1 output for Hugo with basic enterprise formatting.

        Args:
            tier1_content: Raw Tier 1 synthesis output

        Returns:
            Formatted content for Hugo
        """
        # Add basic enterprise formatting header
        header = f"""**Threat Intelligence Briefing – {datetime.now().strftime('%B %d, %Y')}**
*Prepared by: Tia N. List, Senior Threat Intelligence Analyst*

---

"""

        return header + tier1_content

    def _build_generation_context(self, target_date: date) -> Dict[str, Any]:
        """Build generation context for the target date.

        Args:
            target_date: Target date for generation

        Returns:
            Generation context dictionary
        """
        # Get recent articles
        articles = self.storage.get_articles_by_date_range(
            start_date=target_date,
            end_date=target_date,
            status='processed'
        )

        # Sort by score
        articles.sort(key=lambda x: x.get('analysis', {}).get('score', 0), reverse=True)

        return {
            'target_date': target_date,
            'articles': articles,
            'articles_string': self._format_articles_for_prompt(articles[:20])
        }

    def _format_articles_for_prompt(self, articles: List[Dict[str, Any]]) -> str:
        """Format articles for prompt inclusion.

        Args:
            articles: List of articles to format

        Returns:
            Formatted articles string
        """
        formatted = ""
        for i, article in enumerate(articles, 1):
            formatted += f"{i}. **{article['title']}**\n"
            formatted += f"   Source: {article.get('source', 'Unknown')}\n"

            # Extract content
            content_text = ""
            if isinstance(article.get('content'), dict):
                content_dict = article['content']
                content_text = (content_dict.get('processed') or
                              content_dict.get('full') or
                              content_dict.get('raw') or '')

            if content_text and len(content_text) > 100:
                formatted += f"   Content: {content_text[:300]}...\n\n"

        return formatted

    def _build_hugo_post(self, title: str, content: str, target_date: date,
                        tags: List[str], metadata: Dict[str, Any]) -> str:
        """Build complete Hugo post content.

        Args:
            title: Post title
            content: Post content
            target_date: Target date
            tags: List of tags
            metadata: Generation metadata

        Returns:
            Complete Hugo post content
        """
        # Get statistics
        stats = metadata.get('statistics', {})

        # Build Hugo frontmatter
        frontmatter = f"""---
title: {title}
date: {target_date.strftime('%Y-%m-%d')}
tags: {[str(tag) for tag in tags]}
categories: ["Threat Intelligence"]
author: Tia N. List
summary: Daily cybersecurity briefing covering {stats.get('total_articles', 0)} articles with {stats.get('total_iocs', 0)} indicators of compromise
statistics:
  date: {target_date.strftime('%Y-%m-%d')}
  total_articles: {stats.get('total_articles', 0)}
  total_iocs: {stats.get('total_iocs', 0)}
  unique_sources: {stats.get('unique_sources', 0)}
  dynamic_title_used: {metadata.get('dynamic_title_used', False)}
  dynamic_tags_used: {metadata.get('dynamic_tags_used', False)}
  intelligent_synthesis_used: {metadata.get('intelligent_synthesis_used', False)}
  ab_test_variant: {metadata.get('ab_test_variant', None)}
  prompt_version_used: {metadata.get('prompt_version_used', None)}
  generated_tags_count: {metadata.get('generated_tags_count', 0)}
  synthesis_method: {metadata.get('synthesis_method', 'unknown')}
  two_tier_analysis_used: {metadata.get('two_tier_analysis_used', False)}
sources: {stats.get('sources', [])}
generation_metadata:
  dynamic_title_used: {metadata.get('dynamic_title_used', False)}
  dynamic_tags_used: {metadata.get('dynamic_tags_used', False)}
  intelligent_synthesis_used: {metadata.get('intelligent_synthesis_used', False)}
  generated_tags_count: {metadata.get('generated_tags_count', 0)}
  two_tier_analysis_used: {metadata.get('two_tier_analysis_used', False)}
  tier_1_success: {metadata.get('tier_1_success', False)}
  tier_2_success: {metadata.get('tier_2_success', False)}
  tier_1_tokens: {metadata.get('tier_1_tokens', 0)}
  tier_2_tokens: {metadata.get('tier_2_tokens', 0)}
  fallback_used: {metadata.get('fallback_used', False)}
---

"""

        return frontmatter + content

    def _write_hugo_post(self, content: str, target_date: date) -> str:
        """Write Hugo post to file.

        Args:
            content: Hugo post content
            target_date: Target date

        Returns:
            File path
        """
        hugo_dir = Path("hugo/content/posts")
        hugo_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{target_date.strftime('%Y-%m-%d')}-daily-summary.md"
        filepath = hugo_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(filepath)

    def _direct_synthesis_with_token_tracking(self, prompt: str, max_tokens: int, tier_name: str) -> tuple[str, int, str]:
        """Direct synthesis using OpenRouter API with token usage tracking.

        Args:
            prompt: Synthesis prompt.
            max_tokens: Maximum tokens for the response.
            tier_name: Name of the tier for logging.

        Returns:
            Tuple of (content, tokens_used, provider_name)
        """
        import openai
        import os

        # Configure OpenAI client for OpenRouter
        client = openai.OpenAI(
            api_key=os.getenv('OPENROUTER_API_KEY'),
            base_url="https://openrouter.ai/api/v1"
        )

        # Use the analysis model
        model = os.getenv('OPENROUTER_ANALYSIS_MODEL', 'openai/gpt-oss-20b:free')
        print(f"🎯 Using OpenRouter model: {model}")

        # Make direct API call for synthesis
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are Tia N. List, a seasoned Threat Intelligence Analyst writing daily briefings for security engineers. Your tone is direct, analytical, and professional, reflecting deep expertise in cyber threat intelligence."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )

        print(f"🔍 OpenRouter response received")
        print(f"🔍 Response object type: {type(response)}")

        # Extract token usage
        tokens_used = 0
        if hasattr(response, 'usage') and response.usage:
            print(f"🔍 Token usage: {response.usage}")
            tokens_used = response.usage.total_tokens if response.usage.total_tokens else 0

        # Extract content
        content = ""
        if hasattr(response, 'choices') and response.choices:
            print(f"🔍 Number of choices: {len(response.choices)}")
            if response.choices:
                choice = response.choices[0]
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    content = choice.message.content or ""
                    print(f"🔍 {tier_name} synthesis successful: {len(content)} characters")
                    if tokens_used > 0:
                        print(f"💰 Cost estimate: ${tokens_used * 0.00000015:.4f}")

        return content, tokens_used, "openrouter"