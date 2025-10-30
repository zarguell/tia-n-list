"""Prompt configuration loader for dynamic prompt management."""

import json
import os
import random
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class PromptTemplate:
    """Represents a loaded prompt template with metadata."""

    def __init__(self,
                 version: str,
                 description: str,
                 persona: Dict[str, str],
                 sections: Dict[str, Dict[str, Any]],
                 variables: Optional[List[str]] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """Initialize prompt template.

        Args:
            version: Template version
            description: Template description
            persona: Persona configuration
            sections: Template sections with content
            variables: List of template variables
            metadata: Additional metadata including A/B test configuration
        """
        self.version = version
        self.description = description
        self.persona = persona
        self.sections = sections
        self.variables = variables or self.extract_variables()
        self.metadata = metadata or {}

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'PromptTemplate':
        """Create PromptTemplate from configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            PromptTemplate instance
        """
        return cls(
            version=config.get("version", "1.0.0"),
            description=config.get("description", ""),
            persona=config.get("persona", {}),
            sections=config.get("sections", {}),
            variables=config.get("variables"),
            metadata=config.get("metadata", {})
        )

    def extract_variables(self) -> List[str]:
        """Extract template variables from all sections.

        Returns:
            List of unique template variables
        """
        variables = set()
        variable_pattern = r'\{\{([^}]+)\}\}'

        for section_data in self.sections.values():
            if isinstance(section_data, dict):
                template = section_data.get("template", "")
                if template:
                    found_vars = re.findall(variable_pattern, template)
                    variables.update(found_vars)

        return [f"{{{{{var}}}}}" for var in sorted(variables)]

    def validate(self) -> bool:
        """Validate template structure and content.

        Returns:
            True if template is valid, False otherwise
        """
        # Check if required sections have templates
        for section_name, section_data in self.sections.items():
            if isinstance(section_data, dict):
                if section_data.get("required", False) and not section_data.get("template"):
                    return False

        return True

    def get_required_variables(self) -> List[str]:
        """Get list of variables from required sections.

        Returns:
            List of required variables
        """
        required_variables = set()
        variable_pattern = r'\{\{([^}]+)\}\}'

        for section_name, section_data in self.sections.items():
            if isinstance(section_data, dict) and section_data.get("required", False):
                template = section_data.get("template", "")
                if template:
                    found_vars = re.findall(variable_pattern, template)
                    required_variables.update(found_vars)

        return [f"{{{{{var}}}}}" for var in sorted(required_variables)]


class PromptLoader:
    """Loads and manages prompt configuration files."""

    def __init__(self, config_dir: Path):
        """Initialize prompt loader.

        Args:
            config_dir: Path to prompt configuration directory

        Raises:
            FileNotFoundError: If config directory doesn't exist
        """
        if not os.path.exists(config_dir):
            raise FileNotFoundError(f"Prompt configuration directory not found: {config_dir}")

        self.config_dir = config_dir

    def load_main_prompt(self) -> PromptTemplate:
        """Load the main threat intelligence synthesis prompt template.

        Returns:
            Loaded PromptTemplate

        Raises:
            FileNotFoundError: If main prompt file doesn't exist
            ValueError: If template configuration is invalid
        """
        config_path = self.config_dir / "threat_intelligence_synthesis.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Main prompt template not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        template = PromptTemplate.from_config(config)

        if not template.validate():
            raise ValueError(f"Invalid prompt template configuration: {config_path}")

        return template

    def load_confidence_guidance(self) -> Dict[str, Any]:
        """Load confidence assessment guidance configuration.

        Returns:
            Confidence guidance configuration
        """
        config_path = self.config_dir / "confidence_assessment.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Confidence guidance config not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_mitre_attack_guidance(self) -> Dict[str, Any]:
        """Load MITRE ATT&CK guidance configuration.

        Returns:
            MITRE ATT&CK guidance configuration
        """
        config_path = self.config_dir / "mitre_attack_guidance.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"MITRE ATT&CK guidance config not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_industry_impact_guidance(self) -> Dict[str, Any]:
        """Load industry impact guidance configuration.

        Returns:
            Industry impact guidance configuration
        """
        config_path = self.config_dir / "industry_impact_guidance.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Industry impact guidance config not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_intelligence_gap_guidance(self) -> Dict[str, Any]:
        """Load intelligence gap analysis guidance configuration.

        Returns:
            Intelligence gap guidance configuration
        """
        config_path = self.config_dir / "intelligence_gap_guidance.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Intelligence gap guidance config not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_tlp_banner_config(self) -> Dict[str, Any]:
        """Load TLP banner and disclaimer configuration.

        Returns:
            TLP banner configuration
        """
        config_path = self.config_dir / "tlp_banner.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"TLP banner config not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def build_prompt(self, template: PromptTemplate, variables: Dict[str, str]) -> str:
        """Build a complete prompt by substituting variables into template.

        Args:
            template: PromptTemplate to use
            variables: Dictionary of variable values

        Returns:
            Complete prompt string

        Raises:
            ValueError: If required variables are missing
        """
        # Check for missing required variables
        required_vars = template.get_required_variables()
        for var in required_vars:
            var_name = var.strip("{}")
            if var_name not in variables:
                raise ValueError(f"Missing required variable: {var}")

        # Build prompt from sections
        prompt_parts = []

        for section_name, section_data in template.sections.items():
            if isinstance(section_data, dict):
                template_content = section_data.get("template", "")
                if template_content:
                    # Substitute variables
                    section_prompt = template_content
                    for var_name, var_value in variables.items():
                        # Replace both {{var_name}} and {{var_name}} patterns
                        section_prompt = section_prompt.replace(f"{{{{{var_name}}}}}", str(var_value))

                    prompt_parts.append(section_prompt)

        return "\n\n".join(prompt_parts)

    def build_enhanced_synthesis_prompt(self,
                                     articles_data: str,
                                     factual_constraints: str,
                                     current_date: str,
                                     additional_variables: Optional[Dict[str, str]] = None) -> str:
        """Build enhanced threat intelligence synthesis prompt with all guidance.

        Args:
            articles_data: Formatted article data
            factual_constraints: Factual constraints from articles
            current_date: Current date string
            additional_variables: Additional variables for substitution

        Returns:
            Complete synthesis prompt
        """
        # Load all guidance configurations
        template = self.load_main_prompt()
        confidence_guidance = self.load_confidence_guidance()
        attack_guidance = self.load_mitre_attack_guidance()
        industry_guidance = self.load_industry_impact_guidance()
        gap_guidance = self.load_intelligence_gap_guidance()

        # Build enhanced constraints string
        enhanced_constraints = f"{factual_constraints}\n\n"

        # Add confidence guidance
        if "application_template" in confidence_guidance:
            enhanced_constraints += f"CONFIDENCE ASSESSMENT GUIDANCE:\n{confidence_guidance['application_template']}\n\n"

        # Add MITRE ATT&CK guidance
        if "integration_template" in attack_guidance:
            enhanced_constraints += f"MITRE ATT&CK INTEGRATION:\n{attack_guidance['integration_template']}\n\n"

        # Add industry impact guidance
        if "impact_assessment_template" in industry_guidance:
            enhanced_constraints += f"INDUSTRY IMPACT ASSESSMENT:\n{industry_guidance['impact_assessment_template']}\n\n"

        # Add intelligence gap guidance
        if "gap_analysis_template" in gap_guidance:
            enhanced_constraints += f"INTELLIGENCE GAP ANALYSIS:\n{gap_guidance['gap_analysis_template']}\n\n"

        # Prepare variables
        variables = {
            # Persona variables from template
            "persona.name": template.persona.get("name", "Tia N. List"),
            "persona.role": template.persona.get("role", "Threat Intelligence Analyst"),
            "persona.expertise": template.persona.get("expertise", "Enterprise cybersecurity risk assessment"),
            "persona.tone": template.persona.get("tone", "Professional executive audience"),
            "task_definition": template.description or "Generate professional CTI briefing from threat intelligence data",
            # Data variables
            "current_date": current_date,
            "articles_data": articles_data,
            "factual_constraints": enhanced_constraints,
            # Guidance variables
            "confidence_guidance": "Include confidence assessments (High/Medium/Low) for all threat assessments with executive framing",
            "att&ck_guidance": "Include relevant MITRE ATT&CK technique references with detection guidance",
            "industry_impact_guidance": "Emphasize industry-specific impact and business exposure analysis",
            "intelligence_gap_guidance": "Explicitly identify intelligence gaps and information limitations"
        }

        # Add any additional variables
        if additional_variables:
            variables.update(additional_variables)

        return self.build_prompt(template, variables)

    def list_available_prompts(self) -> List[str]:
        """List all available prompt configuration files.

        Returns:
            List of prompt names (without .json extension)
        """
        if not os.path.exists(self.config_dir):
            return []

        prompts = []
        for file_name in os.listdir(self.config_dir):
            if file_name.endswith('.json'):
                prompt_name = file_name[:-5]  # Remove .json extension
                prompts.append(prompt_name)

        return sorted(prompts)

    def get_prompt_version(self, prompt_name: str) -> Optional[str]:
        """Get version information for a specific prompt.

        Args:
            prompt_name: Name of the prompt configuration

        Returns:
            Version string or None if not found
        """
        config_path = self.config_dir / f"{prompt_name}.json"

        if not os.path.exists(config_path):
            return None

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("version", "1.0.0")
        except (json.JSONDecodeError, IOError):
            return None


class PromptVersionManager:
    """Manages prompt versioning and A/B testing capabilities."""

    def __init__(self, config_dir: Path):
        """Initialize prompt version manager.

        Args:
            config_dir: Path to prompt configuration directory

        Raises:
            FileNotFoundError: If config directory doesn't exist
        """
        if not os.path.exists(config_dir):
            raise FileNotFoundError(f"Prompt configuration directory not found: {config_dir}")

        self.config_dir = config_dir

    def load_versioned_prompt(self, prompt_name: str, version: str) -> PromptTemplate:
        """Load a specific version of a prompt template.

        Args:
            prompt_name: Name of the prompt
            version: Version to load

        Returns:
            Loaded PromptTemplate

        Raises:
            FileNotFoundError: If specific version doesn't exist
        """
        # Try versioned filename first
        versioned_filename = f"{prompt_name}_v{version}.json"
        config_path = self.config_dir / versioned_filename

        # Fallback to default filename if versioned doesn't exist
        if not os.path.exists(config_path):
            config_path = self.config_dir / f"{prompt_name}.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Prompt version not found: {prompt_name} v{version}")

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        template = PromptTemplate.from_config(config)

        # Verify version matches requested version
        if template.version != version:
            raise ValueError(f"Version mismatch: requested {version}, found {template.version}")

        return template

    def list_available_versions(self, prompt_name: str) -> List[str]:
        """List all available versions for a prompt.

        Args:
            prompt_name: Name of the prompt

        Returns:
            List of available versions
        """
        versions = []
        base_pattern = f"{prompt_name}.json"
        versioned_pattern = f"{prompt_name}_v"

        if os.path.exists(self.config_dir):
            for file_name in os.listdir(self.config_dir):
                if file_name == base_pattern:
                    # Load default version from file
                    try:
                        with open(self.config_dir / file_name, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                            versions.append(config.get("version", "1.0.0"))
                    except (json.JSONDecodeError, IOError):
                        continue
                elif file_name.startswith(versioned_pattern) and file_name.endswith('.json'):
                    # Extract version from filename
                    version_part = file_name[len(versioned_pattern):-5]  # Remove _v and .json
                    if self.validate_version_format(version_part):
                        versions.append(version_part)

        return sorted(versions, key=lambda v: self._parse_version(v))

    def compare_versions(self, version1: str, version2: str) -> int:
        """Compare two semantic versions.

        Args:
            version1: First version
            version2: Second version

        Returns:
            -1 if version1 < version2
            0 if version1 == version2
            1 if version1 > version2
        """
        v1_parts = self._parse_version(version1)
        v2_parts = self._parse_version(version2)

        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0

            if v1_part < v2_part:
                return -1
            elif v1_part > v2_part:
                return 1

        return 0

    def get_latest_version(self, prompt_name: str) -> Optional[str]:
        """Get the latest version of a prompt.

        Args:
            prompt_name: Name of the prompt

        Returns:
            Latest version string or None if no versions found
        """
        versions = self.list_available_versions(prompt_name)
        return versions[-1] if versions else None

    def select_ab_test_variant(self, template: PromptTemplate) -> Optional[str]:
        """Select A/B test variant based on configuration.

        Args:
            template: PromptTemplate with A/B test configuration

        Returns:
            Selected variant name or None if A/B testing disabled
        """
        ab_config = template.metadata.get('ab_test_config', {})

        if not ab_config.get('enabled', False):
            return None

        variants = ab_config.get('variants', [])
        if not variants:
            return None

        # Select variant based on weights
        weights = [variant.get('weight', 1.0) for variant in variants]
        total_weight = sum(weights)

        if total_weight == 0:
            return None

        # Normalize weights
        normalized_weights = [w / total_weight for w in weights]

        # Select variant
        rand_value = random.random()
        cumulative_weight = 0.0

        for i, weight in enumerate(normalized_weights):
            cumulative_weight += weight
            if rand_value <= cumulative_weight:
                return variants[i].get('name')

        return variants[-1].get('name')

    def create_version_backup(self, prompt_name: str, config: Dict[str, Any]) -> Path:
        """Create a versioned backup of prompt configuration.

        Args:
            prompt_name: Name of the prompt
            config: Configuration to backup

        Returns:
            Path to created backup file
        """
        version = config.get('version', '1.0.0')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        backup_filename = f"{prompt_name}_v{version}_{timestamp}.json"
        backup_path = self.config_dir / backup_filename

        # Add backup metadata
        backup_config = config.copy()
        if 'metadata' not in backup_config:
            backup_config['metadata'] = {}

        backup_config['metadata']['backup_created'] = datetime.now().isoformat()
        backup_config['metadata']['backup_type'] = 'version_backup'

        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_config, f, indent=2)

        return backup_path

    def validate_version_format(self, version: str) -> bool:
        """Validate semantic version format.

        Args:
            version: Version string to validate

        Returns:
            True if version format is valid
        """
        # Semantic version pattern: X.Y.Z with optional pre-release
        pattern = r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?$'
        return bool(re.match(pattern, version))

    def get_prompt_changelog(self, template: PromptTemplate) -> List[str]:
        """Get changelog from prompt metadata.

        Args:
            template: PromptTemplate with metadata

        Returns:
            List of changelog entries
        """
        return template.metadata.get('changelog', [])

    def get_upgrade_path(self, prompt_name: str, from_version: str, to_version: str) -> List[str]:
        """Get upgrade path between versions.

        Args:
            prompt_name: Name of the prompt
            from_version: Starting version
            to_version: Target version

        Returns:
            List of versions representing upgrade path
        """
        available_versions = self.list_available_versions(prompt_name)

        try:
            from_index = available_versions.index(from_version)
            to_index = available_versions.index(to_version)
        except ValueError:
            return []

        if from_index >= to_index:
            return []

        return available_versions[from_index + 1:to_index + 1]

    def _parse_version(self, version: str) -> List[int]:
        """Parse semantic version into numeric components.

        Args:
            version: Version string

        Returns:
            List of numeric components
        """
        # Remove pre-release suffix for comparison
        main_version = version.split('-')[0]
        parts = main_version.split('.')

        parsed_parts = []
        for part in parts[:3]:  # Only major, minor, patch
            try:
                parsed_parts.append(int(part))
            except ValueError:
                parsed_parts.append(0)

        # Pad to 3 parts if needed
        while len(parsed_parts) < 3:
            parsed_parts.append(0)

        return parsed_parts