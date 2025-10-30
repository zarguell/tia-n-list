"""Tests for enhanced prompt versioning and A/B testing capabilities."""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open
from src.prompt_loader import PromptTemplate, PromptVersionManager


class TestPromptVersioning:
    """Test suite for prompt versioning functionality."""

    @pytest.fixture
    def mock_config_dir(self):
        """Create a mock config directory structure."""
        return Path("config/prompts")

    @pytest.fixture
    def versioned_prompt_config(self):
        """Sample versioned prompt configuration."""
        return {
            "version": "1.1.0",
            "description": "Test prompt template with versioning",
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
            },
            "metadata": {
                "created_at": "2025-10-30T10:00:00Z",
                "author": "system",
                "changelog": ["Added confidence assessment guidance", "Improved executive tone"],
                "tags": ["synthesis", "enterprise"],
                "ab_test_config": {
                    "enabled": True,
                    "test_name": "executive_tone_test",
                    "variants": [
                        {"name": "control", "weight": 0.5},
                        {"name": "experimental", "weight": 0.5}
                    ]
                }
            }
        }

    def test_prompt_template_with_version_metadata(self, versioned_prompt_config):
        """Test PromptTemplate with enhanced version metadata."""
        template = PromptTemplate.from_config(versioned_prompt_config)

        assert template.version == "1.1.0"
        assert template.description == "Test prompt template with versioning"
        assert hasattr(template, 'metadata')
        assert template.metadata['author'] == 'system'
        assert template.metadata['tags'] == ["synthesis", "enterprise"]
        assert template.metadata['ab_test_config']['enabled'] is True

    def test_prompt_version_manager_init(self, mock_config_dir):
        """Test PromptVersionManager initialization."""
        with patch('os.path.exists', return_value=True):
            manager = PromptVersionManager(mock_config_dir)
            assert manager.config_dir == mock_config_dir

    def test_load_versioned_prompt(self, mock_config_dir, versioned_prompt_config):
        """Test loading versioned prompt."""
        mock_file_content = json.dumps(versioned_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=versioned_prompt_config):

            manager = PromptVersionManager(mock_config_dir)
            template = manager.load_versioned_prompt("threat_intelligence_synthesis", "1.1.0")

            assert template.version == "1.1.0"
            assert template.metadata['ab_test_config']['enabled'] is True

    def test_list_available_versions(self, mock_config_dir):
        """Test listing available versions for a prompt."""
        mock_files = [
            "threat_intelligence_synthesis.json",
            "threat_intelligence_synthesis_v1.1.0.json",
            "threat_intelligence_synthesis_v1.2.0.json",
            "other_prompt.json"
        ]

        with patch('os.path.exists', return_value=True), \
             patch('os.listdir', return_value=mock_files):

            manager = PromptVersionManager(mock_config_dir)
            versions = manager.list_available_versions("threat_intelligence_synthesis")

            assert "1.0.0" in versions  # Default version
            assert "1.1.0" in versions
            assert "1.2.0" in versions
            assert len(versions) == 3

    def test_compare_versions(self, mock_config_dir):
        """Test semantic version comparison."""
        with patch('os.path.exists', return_value=True):
            manager = PromptVersionManager(mock_config_dir)

            assert manager.compare_versions("1.2.0", "1.1.0") > 0
            assert manager.compare_versions("1.1.0", "1.2.0") < 0
            assert manager.compare_versions("1.1.0", "1.1.0") == 0
            assert manager.compare_versions("2.0.0", "1.9.9") > 0

    def test_get_latest_version(self, mock_config_dir):
        """Test getting the latest version of a prompt."""
        versions = ["1.0.0", "1.1.0", "1.2.0", "2.0.0-beta"]

        with patch('os.path.exists', return_value=True):
            manager = PromptVersionManager(mock_config_dir)
            with patch.object(manager, 'list_available_versions', return_value=versions):
                latest = manager.get_latest_version("threat_intelligence_synthesis")
                assert latest == "2.0.0-beta"

    def test_ab_test_variant_selection(self, mock_config_dir, versioned_prompt_config):
        """Test A/B test variant selection."""
        versioned_prompt_config['metadata']['ab_test_config']['variants'] = [
            {"name": "control", "weight": 0.7},
            {"name": "experimental", "weight": 0.3}
        ]
        mock_file_content = json.dumps(versioned_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=versioned_prompt_config):

            manager = PromptVersionManager(mock_config_dir)
            template = manager.load_versioned_prompt("threat_intelligence_synthesis", "1.1.0")

            # Test multiple selections to verify distribution
            variants = []
            for _ in range(100):
                variant = manager.select_ab_test_variant(template)
                variants.append(variant)

            # Should have both variants
            assert "control" in variants
            assert "experimental" in variants

            # Control should appear more often (70% vs 30%)
            control_count = variants.count("control")
            experimental_count = variants.count("experimental")

            # Allow for some variance in testing
            assert control_count > 40  # Should be around 70
            assert experimental_count > 10  # Should be around 30

    def test_ab_test_disabled_returns_none(self, mock_config_dir, versioned_prompt_config):
        """Test that disabled A/B tests return None."""
        versioned_prompt_config['metadata']['ab_test_config']['enabled'] = False
        mock_file_content = json.dumps(versioned_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=versioned_prompt_config):

            manager = PromptVersionManager(mock_config_dir)
            template = manager.load_versioned_prompt("threat_intelligence_synthesis", "1.1.0")

            variant = manager.select_ab_test_variant(template)
            assert variant is None

    def test_create_version_backup(self, mock_config_dir, versioned_prompt_config):
        """Test creating version backups."""
        mock_file_content = json.dumps(versioned_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=versioned_prompt_config), \
             patch('builtins.open', mock_open()) as mock_file:

            manager = PromptVersionManager(mock_config_dir)
            backup_path = manager.create_version_backup("threat_intelligence_synthesis", versioned_prompt_config)

            # Should create backup with version in filename
            assert "v1.1.0" in backup_path.name
            mock_file.assert_called_once()

    def test_validate_version_format(self, mock_config_dir):
        """Test version format validation."""
        with patch('os.path.exists', return_value=True):
            manager = PromptVersionManager(mock_config_dir)

            # Valid versions
            assert manager.validate_version_format("1.0.0") is True
            assert manager.validate_version_format("2.1.3") is True
            assert manager.validate_version_format("1.0.0-beta") is True
            assert manager.validate_version_format("1.0.0-alpha.1") is True

            # Invalid versions
            assert manager.validate_version_format("1.0") is False
            assert manager.validate_version_format("v1.0.0") is False
            assert manager.validate_version_format("1.0.0.0") is False
            assert manager.validate_version_format("invalid") is False

    def test_get_prompt_changelog(self, mock_config_dir, versioned_prompt_config):
        """Test retrieving prompt changelog."""
        mock_file_content = json.dumps(versioned_prompt_config)

        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=mock_file_content)), \
             patch('json.load', return_value=versioned_prompt_config):

            manager = PromptVersionManager(mock_config_dir)
            template = manager.load_versioned_prompt("threat_intelligence_synthesis", "1.1.0")
            changelog = manager.get_prompt_changelog(template)

            assert "Added confidence assessment guidance" in changelog
            assert "Improved executive tone" in changelog

    def test_prompt_version_upgrade_path(self, mock_config_dir):
        """Test getting version upgrade path."""
        versions = ["1.0.0", "1.1.0", "1.2.0", "2.0.0"]

        with patch('os.path.exists', return_value=True):
            manager = PromptVersionManager(mock_config_dir)
            with patch.object(manager, 'list_available_versions', return_value=versions):
                path = manager.get_upgrade_path("threat_intelligence_synthesis", "1.0.0", "2.0.0")

                assert path == ["1.1.0", "1.2.0", "2.0.0"]

    def test_no_upgrade_path_available(self, mock_config_dir):
        """Test when no upgrade path is available."""
        versions = ["1.0.0"]

        with patch('os.path.exists', return_value=True):
            manager = PromptVersionManager(mock_config_dir)
            with patch.object(manager, 'list_available_versions', return_value=versions):
                path = manager.get_upgrade_path("threat_intelligence_synthesis", "1.0.0", "2.0.0")

                assert path == []