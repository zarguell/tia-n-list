"""Robust response parser for handling imperfect LLM responses.

This module provides flexible parsing for LLM responses that may be:
- Perfect JSON
- Malformed JSON with extra tokens
- Partial JSON structures
- Plain text responses
- Mixed content
"""

import json
import re
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ParsedResponse:
    """Container for parsed response data."""
    success: bool
    data: Dict[str, Any]
    confidence: float  # 0.0 to 1.0
    raw_text: str
    parsing_method: str
    warnings: List[str]


class RobustResponseParser:
    """Parser that gracefully handles imperfect LLM responses."""

    def __init__(self):
        self.parsers = [
            self._try_perfect_json,
            self._try_cleaned_json,
            self._try_partial_json,
            self._try_structured_text,  # This now includes security regex extraction
            self._try_text_extraction
        ]

    def parse_response(self, response_text: str, expected_schema: Optional[Dict[str, Any]] = None) -> ParsedResponse:
        """Parse an LLM response using multiple fallback strategies.

        Args:
            response_text: Raw response text from LLM
            expected_schema: Optional expected JSON schema for validation

        Returns:
            ParsedResponse with extracted data and metadata
        """
        if not response_text or not response_text.strip():
            return ParsedResponse(
                success=False,
                data={},
                confidence=0.0,
                raw_text=response_text,
                parsing_method="empty_response",
                warnings=["Empty response received"]
            )

        cleaned_text = response_text.strip()
        warnings = []

        # Try each parsing strategy in order
        for i, parser in enumerate(self.parsers):
            try:
                result = parser(cleaned_text, expected_schema)
                if result.success:
                    result.warnings.extend(warnings)
                    logger.debug(f"Successfully parsed with {result.parsing_method} (confidence: {result.confidence:.2f})")
                    return result
                else:
                    warnings.extend(result.warnings)
            except Exception as e:
                warnings.append(f"Parser {i+1} failed: {str(e)}")
                continue

        # All parsers failed
        return ParsedResponse(
            success=False,
            data={},
            confidence=0.0,
            raw_text=response_text,
            parsing_method="none",
            warnings=warnings + ["All parsing strategies failed"]
        )

    def _try_perfect_json(self, text: str, expected_schema: Optional[Dict[str, Any]] = None) -> ParsedResponse:
        """Try to parse as perfect JSON."""
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                return ParsedResponse(
                    success=True,
                    data=data,
                    confidence=1.0,
                    raw_text=text,
                    parsing_method="perfect_json",
                    warnings=[]
                )
            else:
                return ParsedResponse(
                    success=False,
                    data={},
                    confidence=0.0,
                    raw_text=text,
                    parsing_method="perfect_json",
                    warnings=["JSON is not an object"]
                )
        except json.JSONDecodeError:
            return ParsedResponse(
                success=False,
                data={},
                confidence=0.0,
                raw_text=text,
                parsing_method="perfect_json",
                warnings=["Invalid JSON format"]
            )

    def _try_cleaned_json(self, text: str, expected_schema: Optional[Dict[str, Any]] = None) -> ParsedResponse:
        """Try to parse JSON after cleaning common issues."""
        # Remove markdown code blocks
        cleaned = re.sub(r'```(?:json)?\s*', '', text)
        cleaned = re.sub(r'```\s*$', '', cleaned)

        # Remove extra tokens (OpenRouter special tokens, XML tags, etc.)
        cleaned = re.sub(r'<｜[^｜]+｜>', '', cleaned)
        cleaned = re.sub(r'<[^>]+>', '', cleaned)
        cleaned = re.sub(r'[^{}]\s*$', '', cleaned)  # Remove trailing punctuation

        # Find JSON boundaries
        first_brace = cleaned.find('{')
        if first_brace == -1:
            return ParsedResponse(
                success=False,
                data={},
                confidence=0.0,
                raw_text=text,
                parsing_method="cleaned_json",
                warnings=["No JSON object found"]
            )

        last_brace = cleaned.rfind('}')
        if last_brace == -1:
            cleaned = cleaned[first_brace:]
        else:
            cleaned = cleaned[first_brace:last_brace + 1]

        # Try to fix common JSON issues
        cleaned = self._fix_common_json_issues(cleaned)

        try:
            data = json.loads(cleaned)
            if isinstance(data, dict):
                return ParsedResponse(
                    success=True,
                    data=data,
                    confidence=0.8,
                    raw_text=text,
                    parsing_method="cleaned_json",
                    warnings=["JSON required cleaning"]
                )
        except json.JSONDecodeError as e:
            return ParsedResponse(
                success=False,
                data={},
                confidence=0.0,
                raw_text=text,
                parsing_method="cleaned_json",
                warnings=[f"Cleaned JSON still invalid: {str(e)}"]
            )

    def _try_partial_json(self, text: str, expected_schema: Optional[Dict[str, Any]] = None) -> ParsedResponse:
        """Try to extract partial JSON structures from text."""
        # Look for JSON-like patterns
        json_patterns = [
            r'\{[^{}]*\{[^{}]*\}[^{}]*\}',  # Nested objects
            r'\{[^{}]*\}',  # Simple objects
            r'\[[^\[\]]*\]',  # Arrays
        ]

        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    data = json.loads(match)
                    if isinstance(data, dict):
                        return ParsedResponse(
                            success=True,
                            data=data,
                            confidence=0.6,
                            raw_text=text,
                            parsing_method="partial_json",
                            warnings=["Extracted partial JSON from text"]
                        )
                except json.JSONDecodeError:
                    continue

        return ParsedResponse(
            success=False,
            data={},
            confidence=0.0,
            raw_text=text,
            parsing_method="partial_json",
            warnings=["No valid JSON fragments found"]
        )

    def _try_structured_text(self, text: str, expected_schema: Optional[Dict[str, Any]] = None) -> ParsedResponse:
        """Try to extract structured information from plain text."""
        data = {}

        # Look for key-value patterns
        kv_patterns = [
            r'([A-Za-z_][A-Za-z0-9_]*)\s*[:=]\s*([^\n]+)',  # key: value
            r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"([^"]*)"',      # key = "value"
            r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\'([^\']*)\'',    # key = 'value'
        ]

        for pattern in kv_patterns:
            matches = re.findall(pattern, text)
            for key, value in matches:
                key = key.strip().lower()
                value = value.strip().strip('"\'')
                if key and value:
                    data[key] = value

        # Look for lists/bullet points
        list_patterns = [
            r'[-*+]\s*([^\n]+)',  # - item
            r'\d+\.\s*([^\n]+)',  # 1. item
        ]

        for pattern in list_patterns:
            matches = re.findall(pattern, text)
            if matches and 'items' not in data:
                data['items'] = [item.strip() for item in matches if item.strip()]

        # Try security-specific extraction
        security_data = self._extract_security_patterns(text)
        data.update(security_data)

        if data:
            return ParsedResponse(
                success=True,
                data=data,
                confidence=0.4,
                raw_text=text,
                parsing_method="structured_text",
                warnings=["Extracted from unstructured text"]
            )

        return ParsedResponse(
            success=False,
            data={},
            confidence=0.0,
            raw_text=text,
            parsing_method="structured_text",
            warnings=["No structured patterns found"]
        )

    def _extract_security_patterns(self, text: str) -> Dict[str, Any]:
        """Extract security-specific patterns from text using regex."""
        data = {}

        # Extract CVE numbers
        cve_pattern = r'(CVE-\d{4}-\d{4,7})'
        cves = re.findall(cve_pattern, text, re.IGNORECASE)
        if cves:
            data['cves'] = list(set(cves))  # Remove duplicates

        # Extract IP addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, text)
        if ips:
            data['ip_addresses'] = list(set(ips))

        # Extract domain names (basic pattern)
        domain_pattern = r'\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(?:/[^\s]*)?'
        domains = re.findall(domain_pattern, text)
        if domains:
            data['domains'] = list(set(domains))

        # Extract file hashes (MD5, SHA1, SHA256)
        hash_patterns = [
            (r'\b[a-fA-F0-9]{32}\b', 'md5_hashes'),
            (r'\b[a-fA-F0-9]{40}\b', 'sha1_hashes'),
            (r'\b[a-fA-F0-9]{64}\b', 'sha256_hashes')
        ]

        for pattern, key in hash_patterns:
            hashes = re.findall(pattern, text)
            if hashes:
                data[key] = list(set(hashes))

        # Extract security keywords and concepts
        security_keywords = {
            'threat_types': [
                r'\b(malware|ransomware|phishing|trojan|backdoor|rootkit|spyware|adware|worm|botnet)\b',
                r'\b(apt|advanced persistent threat)\b',
                r'\b(ddos|denial of service)\b',
                r'\b(sql injection|xss|cross-site scripting)\b',
                r'\b(zero-day|0day)\b',
                r'\b(man-in-the-middle|mitm)\b'
            ],
            'attack_vectors': [
                r'\b(spear phishing|whaling|vishing|smishing)\b',
                r'\b(social engineering)\b',
                r'\b(buffer overflow|heap overflow)\b',
                r'\b(privilege escalation|priv esc)\b',
                r'\b(remote code execution|rce)\b'
            ],
            'mitigation_terms': [
                r'\b(patch|patches|patching)\b',
                r'\b(update|updates|updating)\b',
                r'\b(firewall|antivirus|endpoint protection)\b',
                r'\b(multi-factor authentication|mfa|2fa)\b',
                r'\b(incident response|ir)\b',
                r'\b(threat hunting|threat intel)\b'
            ]
        }

        for category, patterns in security_keywords.items():
            found_terms = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                found_terms.extend(matches)

            if found_terms:
                data[category] = list(set([term.lower() for term in found_terms]))

        # Extract confidence/severity indicators
        confidence_pattern = r'\b(high|medium|low|critical|moderate|severe)\s+(confidence|risk|severity)\b'
        confidence_matches = re.findall(confidence_pattern, text, re.IGNORECASE)
        if confidence_matches:
            data['confidence_indicators'] = [match[0].lower() for match in confidence_matches]

        # Extract numeric scores/ratings
        score_pattern = r'\b(score|rating|severity|risk)\s*[:=]?\s*(\d+(?:\.\d+)?)(?:\s*/\s*(\d+))?'
        score_matches = re.findall(score_pattern, text, re.IGNORECASE)
        if score_matches:
            scores = []
            for match in score_matches:
                score = float(match[1])  # The second capture group is the number
                max_score = float(match[2]) if match[2] else 100
                normalized_score = (score / max_score) * 100 if max_score > 0 else score
                scores.append(normalized_score)

            if scores:
                data['numeric_scores'] = scores
                data['average_score'] = sum(scores) / len(scores)

        return data

    def _try_text_extraction(self, text: str, expected_schema: Optional[Dict[str, Any]] = None) -> ParsedResponse:
        """Fallback: extract basic text information."""
        # Extract any useful information from plain text
        data = {
            'raw_text': text,
            'word_count': len(text.split()),
            'char_count': len(text),
            'has_content': len(text.strip()) > 0
        }

        # Look for security-related keywords
        security_keywords = [
            'vulnerability', 'exploit', 'malware', 'ransomware', 'phishing',
            'attack', 'threat', 'security', 'breach', 'incident', 'ioc',
            'ttp', 'cve', 'patch', 'update', 'critical', 'risk'
        ]

        found_keywords = [kw for kw in security_keywords if kw.lower() in text.lower()]
        if found_keywords:
            data['security_keywords'] = found_keywords
            data['security_relevance'] = len(found_keywords) / len(security_keywords)

        return ParsedResponse(
            success=True,
            data=data,
            confidence=0.2,
            raw_text=text,
            parsing_method="text_extraction",
            warnings=["Only basic text extraction possible"]
        )

    def _fix_common_json_issues(self, json_str: str) -> str:
        """Fix common JSON formatting issues."""
        # Remove trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)

        # Fix unescaped quotes in values (simple heuristic)
        # This is a basic fix - more complex cases might need advanced parsing
        lines = json_str.split('\n')
        fixed_lines = []

        for line in lines:
            # Skip lines that are just braces or brackets
            if line.strip() in ['{', '}', '[', ']', '},', '],']:
                fixed_lines.append(line)
                continue

            # Basic quote fixing for simple key-value pairs
            if ':' in line and not line.strip().startswith('"'):
                # Try to fix unquoted keys or values
                line = re.sub(r'^(\s*)([^"{\[\],\s]+)(\s*:)', r'\1"\2"\3', line)  # Fix keys
                line = re.sub(r':\s*([^"{\[\],\s][^,{]*)(\s*[,\}])$', r': "\1"\2', line)  # Fix values

            fixed_lines.append(line)

        return '\n'.join(fixed_lines)


# Convenience function for quick parsing
def parse_llm_response(response_text: str, expected_schema: Optional[Dict[str, Any]] = None) -> ParsedResponse:
    """Quick parsing function for LLM responses.

    Args:
        response_text: Raw response from LLM
        expected_schema: Optional expected schema

    Returns:
        ParsedResponse object
    """
    parser = RobustResponseParser()
    return parser.parse_response(response_text, expected_schema)


# Function to extract specific fields with fallbacks
def extract_field_with_fallback(response: ParsedResponse, field_name: str, fallback_value: Any = None) -> Any:
    """Extract a field from parsed response with multiple fallback strategies.

    Args:
        response: ParsedResponse object
        field_name: Name of the field to extract
        fallback_value: Value to return if field not found

    Returns:
        Extracted value or fallback
    """
    if not response.success:
        return fallback_value

    # Direct field access
    if field_name in response.data:
        return response.data[field_name]

    # Case-insensitive search
    for key, value in response.data.items():
        if key.lower() == field_name.lower():
            return value

    # Partial match search
    for key, value in response.data.items():
        if field_name.lower() in key.lower():
            return value

    # If all else fails, return fallback
    return fallback_value