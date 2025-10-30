"""Tests for blog generation integration with external prompt configuration system."""

import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from datetime import date, datetime

from src.enhanced_json_blog_generator import EnhancedJSONBlogGenerator
from src.prompt_loader import PromptLoader, PromptVersionManager


class TestBlogPromptIntegration:
    """Test suite for blog generation integration with prompt configuration."""

    @pytest.fixture
    def mock_config_dir(self):
        """Create a mock config directory."""
        return Path("config/prompts")

    @pytest.fixture
    def mock_storage(self):
        """Mock JSON storage."""
        storage = MagicMock()

        # Mock article with proper structure
        article = {
            'id': 'test-article-1',
            'title': 'Critical Vulnerability in Microsoft Products',
            'url': 'https://example.com/article1',
            'source_id': 'source1',
            'score': 85,
            'published_at': datetime.now().isoformat(),
            'content': {
                'raw': 'A critical vulnerability discovered in Microsoft products allows remote code execution.',
                'processed': 'Critical vulnerability with high confidence score.'
            },
            'processed_content': 'Critical vulnerability with high confidence score.',
            'analysis': {
                'threat_category': 'vulnerabilities',
                'iocs': ['CVE-2025-1234'],
                'ttps': ['initial_access']
            }
        }

        storage.get_articles_by_date_range.return_value = [article]
        storage.get_top_articles.return_value = [
            {
                'title': 'Critical Microsoft Vulnerability',
                'source': 'Test Source',
                'score': 85,
                'summary': 'Critical vulnerability discovered'
            }
        ]
        storage.get_all_sources.return_value = [
            {'id': 'source1', 'name': 'Krebs on Security'}
        ]
        storage.get_recently_mentioned_articles.return_value = []
        storage.get_statistics.return_value = {
            'articles': {'sources': ['Krebs on Security']}
        }
        return storage

    @pytest.fixture
    def enhanced_prompt_config(self):
        """Sample enhanced prompt configuration with confidence guidance."""
        return {
            "version": "2.0.0",
            "description": "Enhanced enterprise-grade CTI synthesis prompt",
            "persona": {
                "name": "Tia N. List",
                "role": "Enterprise Threat Intelligence Analyst"
            },
            "metadata": {
                "created_at": "2025-10-30T10:00:00Z",
                "author": "system",
                "tags": ["enterprise", "confidence", "att&ck"],
                "changelog": [
                    "Added confidence level guidance (Low/Medium/High)",
                    "Integrated MITRE ATT&CK technique identification",
                    "Enhanced industry impact analysis for executive audience"
                ],
                "ab_test_config": {
                    "enabled": False  # For stable generation
                }
            },
            "variables": ["{{current_date}}", "{{articles_data}}", "{{factual_constraints}}"],
            "sections": {
                "opening": {
                    "template": "You are Tia N. List, Enterprise Threat Intelligence Analyst. Today: {{current_date}}.\n\nTASK: Generate professional enterprise CTI briefing with confidence assessments and industry impact analysis.",
                    "required": True
                },
                "intelligence_data": {
                    "template": "{{articles_data}}",
                    "required": True
                },
                "constraints": {
                    "template": "{{factual_constraints}}\n\nCONFIDENCE ASSESSMENT GUIDANCE:\n- Assign confidence levels (Low/Medium/High) using industry-standard language\n- Include rationale for confidence assessments\n- Use conditional probability language\n\nMITRE ATT&CK INTEGRATION:\n- Include relevant technique IDs (T1190, T1566, etc.)\n- Reference tactics and procedures where applicable\n- Provide technique descriptions for executive context\n\nINDUSTRY IMPACT ASSESSMENT:\n- Emphasize sector-specific exposure and business impact\n- Identify most affected industries and vendor ecosystems\n- Provide executive-level risk context",
                    "required": True
                },
                "format_requirements": {
                    "template": "FORMAT:\n- Executive Summary with confidence-weighted priorities\n- 2-4 thematic sections by threat category\n- Each section: 3-5 specific bullet points with confidence indicators\n- Intelligence Gaps section identifying missing information\n- MITRE ATT&CK technique references where applicable\n- Industry impact analysis with sector-specific exposure\n- Closing \"What Matters Today\" with confidence-weighted action items\n- Markdown format, professional executive tone",
                    "required": True
                },
                "analytical_requirements": {
                    "template": "ANALYTICAL REQUIREMENTS:\n- Assign confidence levels (High/Medium/Low) to all assessments\n- Include MITRE ATT&CK technique references where relevant\n- Emphasize industry-specific impact and exposure analysis\n- Explicitly state intelligence gaps and uncertainties\n- Use standard analytic confidence language\n- ⚡ for critical severity, 🔥 for actively exploited threats\n- If no new threats, start with \"No newly disclosed threats fitting today's criteria\"",
                    "required": True
                }
            }
        }

    def test_enhanced_blog_generator_with_prompt_config(self, mock_config_dir, enhanced_prompt_config, mock_storage):
        """Test enhanced blog generator using prompt configuration."""
        mock_file_content = json.dumps(enhanced_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=enhanced_prompt_config):

            # Initialize prompt loader
            prompt_loader = PromptLoader(mock_config_dir)
            prompt_version_manager = PromptVersionManager(mock_config_dir)

            # Initialize enhanced generator with mocked storage
            generator = EnhancedJSONBlogGenerator(
                storage=mock_storage,
                context_builder=MagicMock(),
                title_generator=MagicMock(),
                tag_generator=MagicMock(),
                prompt_loader=prompt_loader
            )

            # Generate daily summary
            target_date = date.today()
            result = generator.generate_daily_summary(target_date=target_date)

            assert result['success'] is True
            assert 'filepath' in result
            assert 'content_length' in result
            assert 'dynamic_title_used' in result
            assert 'dynamic_tags_used' in result
            assert 'intelligent_synthesis_used' in result

            # Verify Hugo file was created
            assert 'hugo/content/posts' in result['filepath']
            assert target_date.strftime('%Y-%m-%d') in result['filepath']

    def test_blog_generator_without_prompt_loader(self, mock_storage):
        """Test that blog generator works without prompt loader (backward compatibility)."""
        generator = EnhancedJSONBlogGenerator(
            storage=mock_storage,
            context_builder=MagicMock(),
            title_generator=MagicMock(),
            tag_generator=MagicMock()
            # No prompt_loader provided
        )

        target_date = date.today()
        result = generator.generate_daily_summary(target_date=target_date)

        # Should still work with fallback mechanisms
        assert result['success'] is True
        assert 'filepath' in result

    def test_prompt_versioning_integration(self, mock_config_dir, enhanced_prompt_config):
        """Test integration with prompt versioning system."""
        mock_file_content = json.dumps(enhanced_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=enhanced_prompt_config):

            prompt_loader = PromptLoader(mock_config_dir)
            version_manager = PromptVersionManager(mock_config_dir)

            # Initialize generator with prompt versioning
            generator = EnhancedJSONBlogGenerator(
                storage=MagicMock(),
                context_builder=MagicMock(),
                title_generator=MagicMock(),
                tag_generator=MagicMock(),
                prompt_loader=prompt_loader
            )

            # Test version management
            versions = version_manager.list_available_versions("threat_intelligence_synthesis")
            assert "2.0.0" in versions

            # Test loading specific version
            template = version_manager.load_versioned_prompt("threat_intelligence_synthesis", "2.0.0")
            assert template.version == "2.0.0"
            assert template.metadata['tags'] == ["enterprise", "confidence", "att&ck"]

    def test_ab_testing_integration(self, mock_config_dir, enhanced_prompt_config):
        """Test A/B testing integration."""
        # Enable A/B testing in config
        enhanced_prompt_config['metadata']['ab_test_config']['enabled'] = True
        enhanced_prompt_config['metadata']['ab_test_config']['variants'] = [
            {"name": "control", "weight": 0.5},
            {"name": "experimental", "weight": 0.5}
        ]
        mock_file_content = json.dumps(enhanced_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=enhanced_prompt_config):

            prompt_loader = PromptLoader(mock_config_dir)
            generator = EnhancedJSONBlogGenerator(
                storage=MagicMock(),
                context_builder=MagicMock(),
                title_generator=MagicMock(),
                tag_generator=MagicMock(),
                prompt_loader=prompt_loader
            )

            # Mock multiple generations to test A/B distribution
            variants = []
            for _ in range(50):  # Generate 50 times to test distribution
                result = generator.generate_daily_summary(target_date=date.today())
                if result.get('ab_test_variant'):
                    variants.append(result['ab_test_variant'])

            # Should have both variants
            assert "control" in variants
            assert "experimental" in variants

            # Distribution should be approximately even
            control_count = variants.count("control")
            experimental_count = variants.count("experimental")

            # Allow for some variance, but should be roughly equal
            assert abs(control_count - experimental_count) < 20  # Should be around 25/25 split

    def test_prompt_fallback_mechanisms(self, mock_storage):
        """Test fallback mechanisms when prompt configuration fails."""
        # Test with no prompt loader
        generator1 = EnhancedJSONBlogGenerator(storage=mock_storage)

        # Test with prompt loader that raises exceptions
        with patch('src.prompt_loader.PromptLoader', side_effect=Exception("Config error")):
            generator2 = EnhancedJSONBlogGenerator(
                storage=mock_storage,
                prompt_loader=MagicMock()  # This will raise exceptions
            )

        # Both should still work with fallbacks
        target_date = date.today()
        result1 = generator1.generate_daily_summary(target_date=target_date)
        result2 = generator2.generate_daily_summary(target_date=target_date)

        assert result1['success'] is True
        assert result2['success'] is True

    def test_enhanced_prompt_content_generation(self, mock_storage):
        """Test that enhanced prompt content is properly formatted."""
        # Mock enhanced prompt with confidence and ATT&CK guidance
        with patch('src.enhanced_json_blog_generator.AIContextBuilder') as mock_context, \
             patch('src.enhanced_json_blog_generator.PromptLoader') as mock_loader:

            # Setup mocks to return enhanced prompt content
            mock_context_instance = MagicMock()
            mock_context_instance.build_ai_context_for_enhanced_synthesis.return_value = {
                'articles': [],
                'constraints': {'cves': ['CVE-2025-1234']},
                'sources': ['Krebs on Security']
            }

            mock_loader_instance = MagicMock()
            enhanced_prompt = """You are Tia N. List, Enterprise Threat Intelligence Analyst. Today: 2025-10-30.

CONFIDENCE ASSESSMENT GUIDANCE:
- Assign confidence levels (Low/Medium/High) using industry-standard language
- Include rationale for confidence assessments
- Use conditional probability language

MITRE ATT&CK INTEGRATION:
- Include relevant technique IDs (T1190, T1566, etc.)
- Reference tactics and procedures where applicable
- Provide technique descriptions for executive context

INDUSTRY IMPACT ASSESSMENT:
- Emphasize sector-specific exposure and business impact
- Identify most affected industries and vendor ecosystems
- Provide executive-level risk context"""
            mock_loader_instance.build_enhanced_synthesis_prompt.return_value = enhanced_prompt

            generator = EnhancedJSONBlogGenerator(
                storage=mock_storage,
                context_builder=mock_context_instance,
                prompt_loader=mock_loader_instance
            )

            result = generator.generate_daily_summary(target_date=date.today())

            # Should use enhanced prompt when available
            assert result['intelligent_synthesis_used'] is True
            assert 'ab_test_variant' in result  # Should track which variant was used

    def test_error_handling_and_recovery(self, mock_storage):
        """Test error handling and graceful recovery."""
        # Test with various failure scenarios
        generator = EnhancedJSONBlogGenerator(storage=mock_storage)

        # Mock different failure scenarios
        with patch('src.enhanced_json_blog_generator.AIContextBuilder') as mock_context:
            mock_context_instance = MagicMock()

            # Test database failure
            mock_context_instance.build_ai_context_for_enhanced_synthesis.side_effect = Exception("Database failure")

            result1 = generator.generate_daily_summary(target_date=date.today())

            # Should have fallback mode
            assert result1['success'] is True
            assert result1.get('fallback_mode') is True