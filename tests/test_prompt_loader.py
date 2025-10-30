"""Tests for the prompt configuration loader module."""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open

from src.prompt_loader import PromptLoader, PromptTemplate


class TestPromptLoader:
    """Test suite for PromptLoader class."""

    @pytest.fixture
    def mock_config_dir(self):
        """Create a mock config directory structure."""
        return Path("config/prompts")

    @pytest.fixture
    def sample_prompt_config(self):
        """Sample prompt configuration for testing."""
        return {
            "version": "1.0.0",
            "description": "Test prompt template",
            "persona": {
                "name": "Test Analyst",
                "role": "Security Analyst"
            },
            "variables": ["{{date}}", "{{articles}}"],
            "sections": {
                "opening": {
                    "template": "Hello, today is {{date}}.",
                    "required": True
                }
            }
        }

    @pytest.fixture
    def confidence_config(self):
        """Sample confidence assessment configuration."""
        return {
            "version": "1.0.0",
            "confidence_levels": {
                "high": {
                    "description": "High confidence assessment",
                    "language": ["We assess with high confidence"]
                }
            }
        }

    def test_init_with_valid_directory(self, mock_config_dir):
        """Test PromptLoader initialization with valid directory."""
        with patch('os.path.exists', return_value=True):
            loader = PromptLoader(mock_config_dir)
            assert loader.config_dir == mock_config_dir

    def test_init_with_invalid_directory(self):
        """Test PromptLoader initialization with invalid directory."""
        with pytest.raises(FileNotFoundError, match="Prompt configuration directory not found"):
            PromptLoader(Path("nonexistent/directory"))

    def test_load_main_prompt_template(self, mock_config_dir, sample_prompt_config):
        """Test loading main prompt template."""
        mock_file_content = json.dumps(sample_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=sample_prompt_config):

            loader = PromptLoader(mock_config_dir)
            template = loader.load_main_prompt()

            assert isinstance(template, PromptTemplate)
            assert template.version == "1.0.0"
            assert template.persona["name"] == "Test Analyst"
            assert "opening" in template.sections

    def test_load_confidence_guidance(self, mock_config_dir, confidence_config):
        """Test loading confidence assessment guidance."""
        mock_file_content = json.dumps(confidence_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=confidence_config):

            loader = PromptLoader(mock_config_dir)
            confidence = loader.load_confidence_guidance()

            assert confidence["version"] == "1.0.0"
            assert "high" in confidence["confidence_levels"]

    def test_load_mitre_attack_guidance(self, mock_config_dir):
        """Test loading MITRE ATT&CK guidance."""
        attack_config = {
            "version": "1.0.0",
            "common_techniques": {
                "T1190": "Exploit Public-Facing Application"
            }
        }
        mock_file_content = json.dumps(attack_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=attack_config):

            loader = PromptLoader(mock_config_dir)
            attack_guidance = loader.load_mitre_attack_guidance()

            assert attack_guidance["version"] == "1.0.0"
            assert "T1190" in attack_guidance["common_techniques"]

    def test_load_industry_impact_guidance(self, mock_config_dir):
        """Test loading industry impact guidance."""
        industry_config = {
            "version": "1.0.0",
            "industry_mappings": {
                "technology": {"indicators": ["software", "SaaS"]}
            }
        }
        mock_file_content = json.dumps(industry_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=industry_config):

            loader = PromptLoader(mock_config_dir)
            industry_guidance = loader.load_industry_impact_guidance()

            assert industry_guidance["version"] == "1.0.0"
            assert "technology" in industry_guidance["industry_mappings"]

    def test_load_tlp_banner_config(self, mock_config_dir):
        """Test loading TLP banner configuration."""
        tlp_config = {
            "version": "1.0.0",
            "tlp_markings": {
                "white": {
                    "description": "TLP:WHITE Information",
                    "banner_template": "TLP:WHITE - Disclosure is not limited"
                }
            }
        }
        mock_file_content = json.dumps(tlp_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=tlp_config):

            loader = PromptLoader(mock_config_dir)
            tlp_config = loader.load_tlp_banner_config()

            assert tlp_config["version"] == "1.0.0"
            assert "white" in tlp_config["tlp_markings"]

    def test_build_prompt_with_variables(self, mock_config_dir, sample_prompt_config):
        """Test building prompt with variable substitution."""
        mock_file_content = json.dumps(sample_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=sample_prompt_config):

            loader = PromptLoader(mock_config_dir)
            template = loader.load_main_prompt()

            variables = {
                "date": "2025-10-30"
            }

            prompt = loader.build_prompt(template, variables)

            assert "2025-10-30" in prompt
            assert "Hello, today is 2025-10-30" in prompt

    def test_build_prompt_missing_required_variable(self, mock_config_dir, sample_prompt_config):
        """Test building prompt with missing required variable."""
        mock_file_content = json.dumps(sample_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=sample_prompt_config):

            loader = PromptLoader(mock_config_dir)
            template = loader.load_main_prompt()

            variables = {
                # Missing 'date' variable which is required
                "other_var": "some value"
            }

            with pytest.raises(ValueError, match="Missing required variable"):
                loader.build_prompt(template, variables)

    def test_list_available_prompts(self, mock_config_dir):
        """Test listing available prompt configurations."""
        with patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=[
                "threat_intelligence_synthesis.json",
                "confidence_assessment.json",
                "mitre_attack_guidance.json"
            ]):

            loader = PromptLoader(mock_config_dir)
            prompts = loader.list_available_prompts()

            assert "threat_intelligence_synthesis" in prompts
            assert "confidence_assessment" in prompts
            assert "mitre_attack_guidance" in prompts
            assert len(prompts) == 3


class TestPromptTemplate:
    """Test suite for PromptTemplate class."""

    def test_prompt_template_creation(self):
        """Test creating a PromptTemplate from configuration."""
        config = {
            "version": "1.0.0",
            "description": "Test template",
            "persona": {"name": "Test Analyst", "role": "Analyst"},
            "variables": ["{{date}}"],
            "sections": {
                "opening": {"template": "Hello {{date}}", "required": True}
            }
        }

        template = PromptTemplate.from_config(config)

        assert template.version == "1.0.0"
        assert template.description == "Test template"
        assert template.persona["name"] == "Test Analyst"
        assert "{{date}}" in template.variables
        assert "opening" in template.sections

    def test_extract_variables_from_template(self):
        """Test extracting variables from template sections."""
        config = {
            "version": "1.0.0",
            "description": "Test template",
            "persona": {"name": "Test Analyst"},
            "sections": {
                "opening": {"template": "Hello {{date}} and {{user}}", "required": True},
                "closing": {"template": "Goodbye {{date}}", "required": False}
            }
        }

        template = PromptTemplate.from_config(config)
        variables = template.extract_variables()

        assert "{{date}}" in variables
        assert "{{user}}" in variables
        assert len(variables) == 2

    def test_validate_template_sections(self):
        """Test validation of template sections."""
        config = {
            "version": "1.0.0",
            "description": "Test template",
            "persona": {"name": "Test Analyst"},
            "sections": {
                "opening": {"template": "Hello {{date}}", "required": True}
            }
        }

        template = PromptTemplate.from_config(config)

        # Should pass validation
        assert template.validate()

        # Test missing template in section
        template.sections["opening"]["template"] = ""
        assert not template.validate()