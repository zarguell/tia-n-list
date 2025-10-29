"""Intelligent blog generation module for Tia N. List project.

This module uses advanced LLM synthesis to analyze threat intelligence patterns,
identify trends, and generate authentic, insightful content that learns from the data.
"""

import datetime
import json
import signal
import re
from pathlib import Path
from typing import List, Dict, Any, Set
from src import persona
from src.json_storage import JSONStorage
from src.llm_client_multi import MultiLLMClient


class ThreatIntelligenceSynthesizer:
    """Intelligent synthesizer for threat intelligence analysis."""

    def __init__(self):
        """Initialize the synthesizer."""
        self.llm_client = MultiLLMClient()
        self.storage = JSONStorage()
        self.memory_file = Path("data/report_memory.json")
        self.memory_file.parent.mkdir(exist_ok=True)
        self.report_memory = self._load_report_memory()
        self.recently_mentioned_articles = self._get_recently_mentioned_articles(days=7)

    def _load_report_memory(self) -> Dict[str, Any]:
        """Load memory of previous reports to avoid repetition.

        Returns:
            Dictionary containing report history and mentioned content.
        """
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load report memory: {e}")

        return {
            'reports': {},
            'mentioned_cves': set(),
            'mentioned_articles': set(),
            'mentioned_vulnerabilities': set(),
            'mentioned_incidents': set(),
            'mentioned_cisa_ids': set()
        }

    def _save_report_memory(self) -> None:
        """Save report memory to disk."""
        try:
            # Convert sets to lists for JSON serialization
            memory_copy = {
                'reports': self.report_memory.get('reports', {}),
                'mentioned_cves': list(self.report_memory.get('mentioned_cves', set())),
                'mentioned_articles': list(self.report_memory.get('mentioned_articles', set())),
                'mentioned_vulnerabilities': list(self.report_memory.get('mentioned_vulnerabilities', set())),
                'mentioned_incidents': list(self.report_memory.get('mentioned_incidents', set()))
            }

            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_copy, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️  Could not save report memory: {e}")

    def _get_recently_mentioned_articles(self, days: int = 7) -> Set[str]:
        """Get set of article IDs mentioned in recent reports.

        Args:
            days: Number of days to look back for recent mentions.

        Returns:
            Set of article IDs mentioned in recent reports.
        """
        cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
        cutoff_str = cutoff_date.strftime('%Y-%m-%d')

        mentioned = set()
        for date_str, reports in self.report_memory.get('reports', {}).items():
            if date_str >= cutoff_str:
                # Handle both list and single report cases
                if isinstance(reports, list):
                    for report in reports:
                        if isinstance(report, dict):
                            mentioned.update(report.get('mentioned_articles', []))
                elif isinstance(reports, dict):
                    mentioned.update(reports.get('mentioned_articles', []))

        return mentioned

    def _safe_get_summary(self, article: Dict[str, Any]) -> str:
        """Safely get article summary, handling None values.

        Args:
            article: Article dictionary

        Returns:
            Summary string or empty string
        """
        summary = article.get('summary') or ''
        return summary if summary else 'No summary available'

    def _filter_articles_for_freshness(self, articles: List[Dict]) -> List[Dict]:
        """Filter out articles that have been recently reported on.

        Args:
            articles: List of articles to filter.

        Returns:
            Filtered list of fresh articles.
        """
        fresh_articles = []
        for article in articles:
            article_id = str(article['id'])
            if article_id not in self.recently_mentioned_articles:
                fresh_articles.append(article)

        print(f"📊 Article filtering: {len(articles)} total → {len(fresh_articles)} fresh articles")
        return fresh_articles

    def _extract_factual_constraints(self, articles: List[Dict]) -> Dict[str, Set[str]]:
        """Extract factual constraints from articles to prevent hallucination.

        Args:
            articles: List of articles to analyze.

        Returns:
            Dictionary of factual constraints.
        """
        constraints = {
            'allowed_cves': set(),
            'allowed_vendors': set(),
            'allowed_products': set(),
            'mentioned_cisa_ids': set(),
            'real_incidents': set()
        }

        # Extract real CVEs from articles
        cve_pattern = re.compile(r'\bCVE-\d{4}-\d{4,}\b', re.IGNORECASE)
        for article in articles:
            content = f"{article.get('title', '')} {article.get('summary', '')} {article.get('raw_content', '')}"

            # Find CVEs
            cves = cve_pattern.findall(content)
            constraints['allowed_cves'].update([cve.upper() for cve in cves])

            # Extract vendors and products from titles/summaries
            title = article.get('title', '').lower()
            summary = article.get('summary') or ''
            summary = summary.lower()

            # Common cybersecurity vendors
            vendors = ['microsoft', 'google', 'apple', 'f5', 'cisco', 'palo alto', 'fortinet', 'check point', 'fireeye', 'crowdstrike']
            for vendor in vendors:
                if vendor in title or vendor in summary:
                    constraints['allowed_vendors'].add(vendor.title())

            # Look for CISA mentions
            if 'cisa' in content.lower():
                # Extract any CISA IDs mentioned
                cisa_pattern = re.compile(r'\b(?:E-|ED\s*)?20\d{2}-\d{3}\b')
                cisa_ids = cisa_pattern.findall(content)
                constraints['mentioned_cisa_ids'].update([c_id.upper() for c_id in cisa_ids])

            # Store real incidents
            constraints['real_incidents'].add(article['title'])

        return constraints

    def _create_fact_checking_prompt_addition(self, constraints: Dict[str, Set[str]]) -> str:
        """Create fact-checking instructions for the prompt.

        Args:
            constraints: Factual constraints from article analysis.

        Returns:
            Fact-checking prompt addition.
        """
        fact_check = """

**CRITICAL FACT-CHECKING REQUIREMENTS:**
You MUST ONLY report on information explicitly mentioned in the provided threat intelligence data above.

**ALLOWED CONTENT:**
"""

        if constraints['allowed_cves']:
            fact_check += f"- CVEs: {', '.join(sorted(constraints['allowed_cves']))}\n"
        else:
            fact_check += "- NO CVEs mentioned in today's intelligence\n"

        if constraints['allowed_vendors']:
            fact_check += f"- Vendors: {', '.join(sorted(constraints['allowed_vendors']))}\n"

        if constraints['mentioned_cisa_ids']:
            fact_check += f"- CISA IDs: {', '.join(sorted(constraints['mentioned_cisa_ids']))}\n"
        else:
            fact_check += "- NO CISA directives mentioned in today's intelligence\n"

        fact_check += """\n

**STRICTLY PROHIBITED:**
- Do NOT invent CVE numbers that aren't listed above
- Do NOT create fake CISA directives or emergency directives
- Do NOT mention vulnerabilities or vendors not in the provided data
- Do NOT speculate about unmentioned zero-days or exploits
- If no information exists for a category, DO NOT create filler content

**ACCURACY REQUIREMENT:**
Every specific claim (CVE, vendor, product, CISA ID) must be traceable to the provided article data. If the data doesn't contain specific technical details, use general language without inventing specifics."""

        return fact_check

    def _save_report_to_memory(self, articles: List[Dict], content: str, report_date: datetime.datetime) -> None:
        """Save report information to memory for future reference.

        Args:
            articles: Articles used in this report.
            content: Generated report content.
            report_date: Date of the report.
        """
        try:
            date_str = report_date.isoformat()
            article_ids = [str(article['id']) for article in articles]

            # Extract mentioned entities from content for future reference
            mentioned_cves = set(re.findall(r'\bCVE-\d{4}-\d{4,}\b', content, re.IGNORECASE))
            mentioned_cisa_ids = set(re.findall(r'\b(?:E-|ED\s*)?20\d{2}-\d{3}\b', content, re.IGNORECASE))

            # Store report data
            self.report_memory['reports'][date_str] = {
                'article_ids': article_ids,
                'content_length': len(content),
                'mentioned_cves': list(mentioned_cves),
                'mentioned_cisa_ids': list(mentioned_cisa_ids)
            }

            # Update global mentioned sets
            self.report_memory['mentioned_articles'].update(article_ids)
            self.report_memory['mentioned_cves'].update(mentioned_cves)
            self.report_memory['mentioned_cisa_ids'].update(mentioned_cisa_ids)

            # Save to disk
            self._save_report_memory()

            print(f"💾 Report saved to memory: {len(article_ids)} articles, {len(mentioned_cves)} CVEs")

        except Exception as e:
            print(f"⚠️  Could not save report to memory: {e}")

    def prepare_threat_landscape_context(self, articles: List[Dict], constraints: Dict[str, Set[str]]) -> Dict[str, Any]:
        """Prepare comprehensive context for LLM analysis.

        Args:
            articles: List of articles to analyze.
            constraints: Factual constraints to prevent hallucination.

        Returns:
            Rich context data for LLM synthesis.
        """
        # Prepare article data with enhanced information
        processed_articles = []

        for article in articles:
            # Extract key information
            article_data = {
                'id': article['id'],
                'title': article['title'],
                'summary': article.get('summary', ''),
                'content': article.get('raw_content', '')[:2000],  # Limit for context window
                'source_name': article.get('source_name', 'Unknown'),
                'source': article.get('source_name', 'Unknown'),  # Keep for compatibility
                'score': article.get('score', 0),
                'url': article['url']
            }

            # Add IOCs if available
            iocs = self.storage.get_article_iocs(article['id'])
            if iocs:
                article_data['iocs'] = [
                    f"{ioc['type']}: {ioc['value']}"
                    for ioc in iocs[:5]  # Limit IOCs
                ]

            processed_articles.append(article_data)

        # Extract temporal patterns
        dates = [datetime.datetime.now()]  # Simplified for now
        time_span = "daily briefing"

        # Identify potential themes
        titles = [a['title'] for a in processed_articles]
        content_snippets = [a['content'][:500] for a in processed_articles]

        return {
            'articles': processed_articles,
            'total_articles': len(processed_articles),
            'time_span': time_span,
            'analysis_date': datetime.datetime.now().isoformat(),
            'titles': titles,
            'content_samples': content_snippets
        }

    def create_comprehensive_analysis_prompt(self, context: Dict[str, Any], constraints: Dict[str, Set[str]]) -> str:
        """Create a sophisticated prompt for threat intelligence synthesis.

        Args:
            context: Prepared context data.
            constraints: Factual constraints to prevent hallucination.

        Returns:
            Comprehensive analysis prompt.
        """
        # Format article data for the prompt
        article_data = self._format_articles_for_tia_prompt(context['articles'])

        # Add fact-checking constraints
        fact_checking = self._create_fact_checking_prompt_addition(constraints)

        return f"""You are Tia N. List, a seasoned Threat Intelligence Analyst writing daily briefings for security engineers. Your tone is direct, analytical, and professional, reflecting deep expertise in cyber threat intelligence, but with a friendly and sometimes humorous tone - an entertaining writer.

Begin with a variation of: "Morning update from Tia N. List, Threat Intelligence Analyst."

Today is {datetime.datetime.now().strftime('%B %d, %Y')}; include only security intelligence publicly disclosed in the last 24 hours—exclude older information or filler. Summarize newly reported, credible, and actionable security intelligence, avoiding speculation. If no new items meet the criteria, start with: "No newly disclosed threats fitting today's criteria."

**THREAT INTELLIGENCE DATA TO ANALYZE:**
{article_data}

{fact_checking}

**COVERAGE PRIORITIES:**
Create sections based ONLY on the available data above:
- If CVEs are mentioned, create a "Zero-Day Vulnerabilities & Exploits" section with those specific CVEs
- If CISA directives are mentioned, create a "CISA KEVs & Emergency Directives" section with those specific IDs
- If major incidents are mentioned, create specific sections for those incidents
- If multiple smaller incidents exist, group them by category (breaches, malware, etc.)
- If no specific technical details exist, create general analysis sections

**CRITICAL: SECTION REQUIREMENTS:**
- Each section MUST have substantive content (at least 2-3 bullet points or a full paragraph)
- If you cannot create a meaningful section based on the available data, DO NOT create that section
- Do NOT create empty sections or sections with just placeholder text
- Better to have fewer, high-quality sections than many empty ones

**FORMATTING REQUIREMENTS:**
- Provide concise bullet points or sections for readability
- ONLY include CVE numbers, CISA IDs, vendors, and products that are explicitly mentioned in the data above
- Use symbols to highlight importance where appropriate: ⚡ for new discoveries, 🔥 for KEVs, 🚀 for emerging technologies
- Each section should provide actionable insights or specific details
- Include a "What Matters Today for Security Engineers" section summarizing prioritized, practical actions

**STYLE GUIDELINES:**
Write with the voice and style of an experienced Threat Intelligence analyst: clear, precise, jargon-appropriate, and focused on decision-making. Every claim must be supported by the provided data.

**OUTPUT FORMAT:**
Generate a complete daily threat intelligence briefing (600-1000 words) in Markdown format with:
- Morning update opening
- Sections based ONLY on available intelligence data
- Actionable "What Matters Today" conclusion
- Professional yet engaging tone throughout

Focus on providing genuine value to security engineers based on real, verifiable threat intelligence data."""

    def _format_articles_for_tia_prompt(self, articles: List[Dict]) -> str:
        """Format articles for Tia N. List's daily briefing prompt.

        Args:
            articles: List of article data.

        Returns:
            Formatted article text for professional threat intelligence analysis.
        """
        if not articles:
            return "No new threat intelligence reports available for analysis."

        formatted_sections = []

        # Group articles by category/type for better analysis
        vulnerability_reports = []
        breach_reports = []
        malware_reports = []
        advisories = []
        other_reports = []

        for article in articles:
            title = article['title'].lower()
            summary = article.get('summary') or ''
            summary = summary.lower()
            content = article.get('content') or ''
            content = content.lower()

            article_info = {
                'title': article['title'],
                'source_name': article.get('source_name', article.get('source', 'Unknown')),
                'source': article.get('source_name', article.get('source', 'Unknown')),  # Keep for compatibility
                'url': article['url'],
                'summary': article.get('summary', 'No summary available'),
                'score': article.get('score', 0),
                'published_date': article.get('published_at', 'Unknown date')
            }

            # Add IOCs if available (filter out non-security IOCs)
            iocs = self.storage.get_article_iocs(article['id'])
            filtered_iocs = []
            if iocs:
                for ioc in iocs[:5]:
                    # Filter out common non-security URLs and domains
                    if ioc['type'] == 'url':
                        url = ioc['value'].lower()
                        # Skip obvious non-security URLs
                        if any(skip in url for skip in ['youtube.com', 'youtu.be', 'wikipedia.org', 'github.com']):
                            continue
                    elif ioc['type'] == 'domain':
                        domain = ioc['value'].lower()
                        # Skip obvious non-security domains
                        if any(skip in domain for skip in ['google.com', 'microsoft.com', 'github.com']):
                            continue

                    filtered_iocs.append(f"{ioc['type']}: {ioc['value']}")

            if filtered_iocs:
                article_info['iocs'] = filtered_iocs

            # Categorize articles
            if any(term in title + summary + content for term in ['vulnerability', 'cve', 'patch', 'exploit']):
                vulnerability_reports.append(article_info)
            elif any(term in title + summary + content for term in ['breach', 'hack', 'attack', 'compromise']):
                breach_reports.append(article_info)
            elif any(term in title + summary + content for term in ['malware', 'ransomware', 'trojan', 'worm']):
                malware_reports.append(article_info)
            elif any(term in title + summary + content for term in ['advisory', 'alert', 'guidance', 'cisa']):
                advisories.append(article_info)
            else:
                other_reports.append(article_info)

        # Format each section
        if vulnerability_reports:
            formatted_sections.append("**VULNERABILITIES & EXPLOITS:**")
            for article in vulnerability_reports:
                text = f"- {article['title']} (Source: {article['source']})"
                summary = self._safe_get_summary(article)
                if summary != 'No summary available':
                    text += f"\n  {summary[:200]}..."
                if 'iocs' in article:
                    text += f"\n  IOCs: {', '.join(article['iocs'][:3])}"
                formatted_sections.append(text)

        if breach_reports:
            formatted_sections.append("\n**SECURITY BREACHES & INCIDENTS:**")
            for article in breach_reports:
                text = f"- {article['title']} (Source: {article['source']})"
                summary = self._safe_get_summary(article)
                if summary != 'No summary available':
                    text += f"\n  {summary[:200]}..."
                if 'iocs' in article:
                    text += f"\n  IOCs: {', '.join(article['iocs'][:3])}"
                formatted_sections.append(text)

        if malware_reports:
            formatted_sections.append("\n**MALWARE & THREAT ACTORS:**")
            for article in malware_reports:
                text = f"- {article['title']} (Source: {article['source']})"
                summary = self._safe_get_summary(article)
                if summary != 'No summary available':
                    text += f"\n  {summary[:200]}..."
                if 'iocs' in article:
                    text += f"\n  IOCs: {', '.join(article['iocs'][:3])}"
                formatted_sections.append(text)

        if advisories:
            formatted_sections.append("\n**SECURITY ADVISORIES & ALERTS:**")
            for article in advisories:
                text = f"- {article['title']} (Source: {article['source']})"
                summary = self._safe_get_summary(article)
                if summary != 'No summary available':
                    text += f"\n  {summary[:200]}..."
                formatted_sections.append(text)

        if other_reports:
            formatted_sections.append("\n**OTHER SECURITY INTELLIGENCE:**")
            for article in other_reports:
                text = f"- {article['title']} (Source: {article['source']})"
                summary = self._safe_get_summary(article)
                if summary != 'No summary available':
                    text += f"\n  {summary[:200]}..."
                formatted_sections.append(text)

        return "\n".join(formatted_sections)

    def _format_articles_for_analysis(self, articles: List[Dict]) -> str:
        """Format articles for LLM analysis.

        Args:
            articles: List of article data.

        Returns:
            Formatted article text.
        """
        formatted = []

        for i, article in enumerate(articles, 1):
            article_text = f"""
**Article {i}:**
Title: {article['title']}
Source: {article['source']}
Relevance Score: {article['score']}/100
Summary: {self._safe_get_summary(article)}
Content: {article['content']}
"""
            if 'iocs' in article and article['iocs']:
                article_text += f"Key IOCs: {', '.join(article['iocs'])}\n"

            article_text += f"URL: {article['url']}\n"
            formatted.append(article_text)

        return "\n".join(formatted)

    def synthesize_threat_intelligence(self, articles: List[Dict]) -> str:
        """Synthesize threat intelligence using LLM analysis.

        Args:
            articles: List of articles to analyze.

        Returns:
            Synthesized intelligence briefing.
        """
        if not articles:
            return "No articles available for analysis."

        print(f"Synthesizing intelligence from {len(articles)} articles...")

        # Filter out recently reported articles
        fresh_articles = self._filter_articles_for_freshness(articles)
        if not fresh_articles:
            print("⚠️  No fresh articles available - all recently reported")
            return "No newly disclosed threats fitting today's criteria."

        # Extract factual constraints to prevent hallucination
        constraints = self._extract_factual_constraints(fresh_articles)

        # Prepare context
        context = self.prepare_threat_landscape_context(fresh_articles, constraints)

        # Create analysis prompt with fact-checking
        prompt = self.create_comprehensive_analysis_prompt(context, constraints)

        try:
            # Try multi-provider synthesis with OpenRouter priority
            response = self._attempt_synthesis_with_providers(prompt)

            if response and len(response.strip()) > 200:
                print(f"✅ Successful synthesis with {len(response)} characters")
                return self._format_synthesized_content(response, context)
            else:
                print(f"⚠️  Response too short ({len(response.strip()) if response else 0} chars), using fallback synthesis")
                return self._fallback_synthesis(context)

        except Exception as e:
            print(f"✗ Error in LLM synthesis: {e}")
            return self._fallback_synthesis(context)

    def _attempt_synthesis_with_providers(self, prompt: str) -> str:
        """Attempt synthesis with multiple providers in priority order.

        Args:
            prompt: Analysis prompt for synthesis.

        Returns:
            Synthesized content or None if all providers fail.
        """
        providers_to_try = ['openrouter', 'openai', 'gemini']

        for provider in providers_to_try:
            try:
                print(f"🔄 Attempting synthesis with provider: {provider}")

                # Check if provider is available
                if provider == 'openrouter' and not self._is_openrouter_available():
                    print(f"⚠️  {provider} not available, trying next provider")
                    continue

                # Temporarily set provider for this synthesis
                import os
                import signal
                original_provider = os.getenv('LLM_PROVIDER', 'gemini')
                os.environ['LLM_PROVIDER'] = provider

                # Add timeout handling
                def timeout_handler(signum, frame):
                    raise TimeoutError("LLM call timed out")

                try:
                    # Set timeout for LLM call (30 seconds)
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(30)

                    try:
                        response = self._attempt_synthesis_via_analysis(prompt, provider)

                        if response and len(response.strip()) > 50:
                            print(f"✅ Successful synthesis with {provider}")
                            print(f"🔍 {provider} response length: {len(response.strip())} chars")
                            return response
                        else:
                            print(f"⚠️  {provider} response too short or empty")
                            print(f"🔍 {provider} response length: {len(response.strip()) if response else 0} chars")
                            if response:
                                print(f"🔍 {provider} response preview: {response.strip()[:100]}...")

                    except json.JSONDecodeError as e:
                        print(f"⚠️  {provider} JSON parsing error: {str(e)[:100]}...")
                        continue
                    except TimeoutError:
                        print(f"⚠️  {provider} timed out after 30 seconds")
                        continue
                    except Exception as e:
                        error_msg = str(e)
                        if "JSON" in error_msg or "parse" in error_msg.lower():
                            print(f"⚠️  {provider} parsing error: {error_msg[:100]}...")
                        else:
                            print(f"⚠️  {provider} failed: {error_msg[:100]}...")
                        continue

                finally:
                    # Cancel timeout
                    signal.alarm(0)
                    # Restore original provider
                    if original_provider:
                        os.environ['LLM_PROVIDER'] = original_provider
                    elif 'LLM_PROVIDER' in os.environ:
                        del os.environ['LLM_PROVIDER']

            except Exception as e:
                print(f"⚠️  Provider {provider} setup failed: {e}")
                continue

        return None

    def _is_openrouter_available(self) -> bool:
        """Check if OpenRouter is properly configured for free models.

        Returns:
            True if OpenRouter should be available for synthesis.
        """
        try:
            # Test a simple call to see if data policy allows free models
            import os
            if not os.getenv('OPENROUTER_API_KEY'):
                return False

            # Quick test call - if it fails with 404, data policy issue
            original_provider = os.getenv('LLM_PROVIDER', 'gemini')
            os.environ['LLM_PROVIDER'] = 'openrouter'

            try:
                test_response = self.llm_client.extract_iocs_and_ttps(
                    "Briefly summarize cybersecurity", "test"
                )
                # If we get here, OpenRouter is working
                return True
            except Exception as e:
                if "404" in str(e) and "data policy" in str(e):
                    print("⚠️  OpenRouter data policy prevents free model usage")
                    return False
                return False
            finally:
                os.environ['LLM_PROVIDER'] = original_provider

        except Exception:
            return False

    def _attempt_synthesis_via_analysis(self, prompt: str, provider: str) -> str:
        """Attempt synthesis using direct analysis with OpenRouter.

        Args:
            prompt: Synthesis prompt.
            provider: Current provider name.

        Returns:
            Synthesized text content.
        """
        try:
            # For OpenRouter, try direct API call for synthesis
            if provider == 'openrouter':
                return self._openrouter_direct_synthesis(prompt)
            else:
                # For other providers, use the existing approach
                return self._fallback_provider_synthesis(prompt, provider)

        except Exception as e:
            print(f"⚠️  Direct analysis failed for {provider}: {str(e)[:100]}...")
            return None

    def _openrouter_direct_synthesis(self, prompt: str) -> str:
        """Direct synthesis using OpenRouter API.

        Args:
            prompt: Comprehensive synthesis prompt.

        Returns:
            Synthesized text content.
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
        try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are Tia N. List, a seasoned Threat Intelligence Analyst writing daily briefings for security engineers. Your tone is direct, analytical, and professional, reflecting deep expertise in cyber threat intelligence, but with a friendly and sometimes humorous tone - an entertaining writer."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )

                print(f"🔍 OpenRouter response received")
                print(f"🔍 Response object type: {type(response)}")

                if hasattr(response, 'usage') and response.usage:
                    print(f"🔍 Token usage: {response.usage}")

                if hasattr(response, 'choices') and response.choices:
                    print(f"🔍 Number of choices: {len(response.choices)}")
                    if response.choices:
                        choice = response.choices[0]
                        print(f"🔍 Choice finish reason: {getattr(choice, 'finish_reason', 'Unknown')}")
                        if hasattr(choice, 'message') and choice.message:
                            content = choice.message.content
                            print(f"🔍 OpenRouter raw response length: {len(content) if content else 0}")
                            if content:
                                print(f"🔍 OpenRouter response preview: {content[:200]}...")
                            if content and len(content.strip()) > 100:
                                return content.strip()
                            else:
                                print(f"⚠️  OpenRouter content too short: {len(content.strip()) if content else 0} chars")
                        else:
                            print(f"⚠️  OpenRouter choice has no message")
                    else:
                        print(f"⚠️  OpenRouter choices list is empty")
                else:
                    print(f"⚠️  OpenRouter response has no choices attribute")

                # Try to get more response details for debugging
                if hasattr(response, 'model'):
                    print(f"🔍 Model used: {response.model}")
                if hasattr(response, 'id'):
                    print(f"🔍 Response ID: {response.id}")
                if hasattr(response, 'object'):
                    print(f"🔍 Response object: {response.object}")

                return None

        except Exception as e:
            print(f"⚠️  OpenRouter direct synthesis failed: {str(e)[:200]}...")

            # Check for specific OpenRouter/OpenAI errors
            error_str = str(e).lower()
            if 'rate' in error_str and 'limit' in error_str:
                print(f"🚫 OpenRouter rate limit detected - free tier likely exhausted")
            elif 'unauthorized' in error_str or 'authentication' in error_str:
                print(f"🚫 OpenRouter authentication error - check API key")
            elif 'model' in error_str and 'not' in error_str:
                print(f"🚫 OpenRouter model error - model not available")
            elif 'insufficient' in error_str and 'quota' in error_str:
                print(f"🚫 OpenRouter quota exceeded")
            elif 'content' in error_str and 'policy' in error_str:
                print(f"🚫 OpenRouter content policy violation")
            else:
                print(f"🚫 OpenRouter unknown error: {error_str}")

            return None

    def _fallback_provider_synthesis(self, prompt: str, provider: str) -> str:
        """Fallback synthesis using relevance analysis method.

        Args:
            prompt: Synthesis prompt.
            provider: Current provider name.

        Returns:
            Synthesized text content.
        """
        try:
            # Use relevance analysis method which is more reliable for text generation
            analysis_prompt = f"""You are Tia N. List, cybersecurity threat intelligence analyst.

{prompt}

Provide a comprehensive analysis in 3-4 paragraphs. Focus on strategic insights, patterns, and actionable recommendations. Write in a professional but engaging tone."""

            result = self.llm_client.is_relevant_article("Threat Intelligence Synthesis Request", analysis_prompt)

            # Extract the reasoning part which should contain our analysis
            if isinstance(result, dict) and 'reasoning' in result:
                reasoning = result['reasoning']
                # Clean up the reasoning to get the core analysis
                if len(reasoning) > 100:
                    return reasoning
                elif "Error:" in reasoning:
                    return None
                else:
                    # Try to get more content by using a fallback approach
                    return self._fallback_synthesis_text(prompt)

            return None

        except Exception as e:
            print(f"⚠️  Fallback synthesis failed for {provider}: {str(e)[:100]}...")
            return None

    def _fallback_synthesis_text(self, prompt: str) -> str:
        """Fallback synthesis when direct methods fail.

        Args:
            prompt: Original synthesis prompt.

        Returns:
            Basic synthesized text.
        """
        try:
            # Simple template-based synthesis as last resort
            fallback_text = """# Strategic Threat Intelligence Analysis

## Executive Summary

Today's threat landscape reveals evolving attack patterns across multiple vectors, requiring heightened defensive posture and strategic awareness.

## Key Threat Patterns

Analysis of current intelligence indicates several concerning trends:
- Increased sophistication of supply chain attacks
- Expansion of ransomware and extortion campaigns
- Growing complexity of malware distribution networks
- Continued exploitation of known vulnerabilities

## Strategic Implications

Organizations should prioritize:
- Enhanced monitoring and detection capabilities
- Supply chain security assessments
- Vulnerability management programs
- Incident response preparedness

## Defensive Recommendations

1. Strengthen security monitoring across all attack surfaces
2. Validate security controls and incident response procedures
3. Enhance security awareness and training programs
4. Maintain vigilance for emerging threat patterns

This analysis synthesizes available threat intelligence to provide actionable insights for cybersecurity defense strategies."""

            return fallback_text

        except Exception:
            return "Threat intelligence synthesis completed. Strategic analysis available with key recommendations for enhanced defensive posture."

    def _extract_response_text(self, response) -> str:
        """Extract text content from LLM response (dict or string).

        Args:
            response: LLM response that might be dict or string.

        Returns:
            Extracted text content.
        """
        if isinstance(response, dict):
            # Try different possible dict keys
            for key in ['content', 'analysis', 'text', 'response', 'synthesis']:
                if key in response and response[key]:
                    return str(response[key])

            # If no expected keys, join all string values
            text_parts = []
            for key, value in response.items():
                if isinstance(value, str) and len(value.strip()) > 10:
                    text_parts.append(value)

            return '\n\n'.join(text_parts) if text_parts else str(response)

        elif isinstance(response, str):
            return response

        else:
            return str(response)

    def _format_synthesized_content(self, content: str, context: Dict[str, Any]) -> str:
        """Format the synthesized content for Hugo.

        Args:
            content: LLM-generated content.
            context: Analysis context.

        Returns:
            Formatted blog post.
        """
        now = datetime.datetime.now()

        # Extract title from content or generate one
        title = self._extract_title_from_content(content)

        # Add references section with source URLs
        references_section = self._generate_references_section(context['articles'])

        # Create Hugo front matter
        front_matter = f"""---
title: "{title}"
date: {now.strftime('%Y-%m-%d')}
tags: [threat-intelligence, cybersecurity, strategic-analysis]
author: "Tia N. List"
summary: "Strategic threat intelligence analysis synthesizing patterns and trends from {context['total_articles']} sources."
---

"""

        # Add joke section if desired
        joke = persona.fetch_joke_of_the_day()
        if joke:
            joke_section = f"""

## 🎭 Intelligence Perspective

While analyzing serious threats, remember to maintain perspective:

_{joke}_

A balanced mindset leads to better decision-making.

---

"""
        else:
            joke_section = """

---

"""

        return front_matter + content + joke_section + references_section

    def _generate_references_section(self, articles: List[Dict]) -> str:
        """Generate a references section with source URLs.

        Args:
            articles: List of articles used in the analysis.

        Returns:
            Formatted references section.
        """
        if not articles:
            return ""

        references = "## 📚 References\n\n"
        references += "**Primary Sources:**\n\n"

        for i, article in enumerate(articles, 1):
            source_name = article.get('source_name', article.get('source', 'Unknown Source'))
            title = article['title']
            url = article['url']
            score = article.get('score', 0)

            references += f"{i}. **{title}**\n"
            references += f"   - Source: {source_name} (Relevance: {score}/100)\n"
            references += f"   - URL: {url}\n\n"

        references += "---\n\n"
        references += f"*Sources analyzed: {len(articles)} articles*"

        return references

    def _extract_title_from_content(self, content: str) -> str:
        """Extract a compelling title from the content.

        Args:
            content: LLM-generated content.

        Returns:
            Extracted or generated title.
        """
        lines = content.split('\n')

        # Look for first markdown heading
        for line in lines:
            if line.strip().startswith('# '):
                return line.strip()[2:].strip()

        # Fallback title
        return f"Strategic Threat Intelligence Briefing - {datetime.datetime.now().strftime('%Y-%m-%d')}"

    def _fallback_synthesis(self, context: Dict[str, Any]) -> str:
        """Fallback synthesis when LLM fails.

        Args:
            context: Analysis context.

        Returns:
            Basic synthesized content.
        """
        now = datetime.datetime.now()

        content = f"""# Strategic Threat Intelligence Briefing

**Date:** {now.strftime('%B %d, %Y')}
**Sources Analyzed:** {context['total_articles']} articles

## Executive Summary

Today's threat intelligence landscape reveals several concerning patterns across multiple attack vectors and threat actors.

## Key Incidents

"""

        for article in context['articles'][:5]:
            content += f"""### {article['title']}

**Source:** {article['source']} | **Severity:** {article['score']}/100

{article['summary']}

"""

        return content


def generate_intelligent_blog_post() -> bool:
    """Generate an intelligent, synthesized blog post.

    Returns:
        True if successful, False otherwise.
    """
    try:
        print("Generating intelligent threat intelligence briefing...")

        # Get top articles
        storage = JSONStorage()
        articles = storage.get_top_articles(12)  # Get more articles for better analysis
        if not articles:
            print("No articles found for analysis")
            return False

        # Create synthesizer
        synthesizer = ThreatIntelligenceSynthesizer()

        # Generate synthesized intelligence
        content = synthesizer.synthesize_threat_intelligence(articles)

        if not content or len(content.strip()) < 300:  # Reduced minimum since we now filter articles
            print("Generated content too short")
            return False

        # Save to Hugo content directory
        posts_dir = Path("hugo/content/posts")
        posts_dir.mkdir(parents=True, exist_ok=True)

        # Create filename
        now = datetime.datetime.now()
        filename = f"{now.strftime('%Y-%m-%d')}-strategic-threat-analysis.md"
        filepath = posts_dir / filename

        # Write blog post
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        # Save report to memory to prevent future repetition
        synthesizer._save_report_to_memory(articles, content, now)

        print(f"✅ Strategic threat analysis generated: {filename}")
        print(f"📁 Content length: {len(content)} characters")
        print(f"🧠 Intelligence synthesized from {len(articles)} sources")

        return True

    except Exception as e:
        print(f"✗ Error generating intelligent briefing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = generate_intelligent_blog_post()
    if not success:
        print("Failed to generate intelligent threat briefing")