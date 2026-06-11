"""
LLM-based synthesis for preconditions and hunting hypothesis.

Calls an OpenAI-compatible API to produce genuinely AI-generated analyst
output for the two fields that are meant to substitute for human reasoning:
preconditions_for_exploit and hunting_hypothesis.

All other fields (KEV, NVD, Vulnrichment, CVSS, CPE, component extraction,
PoC search) remain deterministic — this module handles *only* the synthesis
that requires judgment.

Configuration (env vars)
------------------------
KEVRICHMENT_LLM_ENDPOINT : str
    OpenAI-compatible API endpoint (default: https://api.openai.com/v1)
KEVRICHMENT_LLM_API_KEY  : str
    API key (default: OPENAI_API_KEY env var)
KEVRICHMENT_LLM_MODEL    : str
    Model name (default: gpt-4o-mini)
"""

import json
import os
import re

import requests


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_ENDPOINT = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a senior vulnerability analyst producing structured enrichment for CISA KEV entries. Your job is to take raw CVE data and produce two concise, deployment-actionable outputs:

1. **Preconditions** — What must be true in a deployment for this CVE to be exploitable? (2-3 bullet points, plain text joined with "; ")
2. **Hunting hypothesis** — What specific attacker behavior or TTP should a blue team monitor for? (One sentence starting with a verb: Monitor for / Hunt for / Look for)

Rules:
- Be specific. Name the component, protocol, or feature where relevant.
- Do NOT restate CVSS scores or CWE IDs — those are already in the record.
- Do NOT use vague language like "an attacker could exploit" — tell the analyst what to *look for*.
- If the vendor advisory or public PoC research reveals specific behavior, use it.
- For browser/client-side vulns: the precondition is about user interaction (clicking a link, visiting a page), NOT "network access to the service".
- For network service vulns: the precondition is about network reachability and authentication.
- Return ONLY valid JSON with keys "preconditions" (string) and "hunting_hypothesis" (string)."""


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def _build_prompt(cve_id, vendor, product, description, cwe_ids,
                  cvss_vector, vulnrichment_data, research_data):
    """Build the user message from collected CVE data."""
    lines = [f"CVE ID: {cve_id}"]
    lines.append(f"Vendor: {vendor}")
    lines.append(f"Product: {product}")
    if description:
        lines.append(f"\nNVD Description:\n{description.strip()}")
    if cwe_ids:
        lines.append(f"\nCWEs: {', '.join(cwe_ids)}")
    if cvss_vector:
        lines.append(f"\nCVSS Vector: {cvss_vector}")
    if vulnrichment_data:
        lines.append(f"\nVulnrichment SSVC:")
        for k, v in vulnrichment_data.items():
            lines.append(f"  {k}: {v}")
    if research_data:
        lines.append(f"\nResearch findings:")
        for k, v in research_data.items():
            if v and k != "preconditions_for_exploit" and k != "hunting_hypothesis":
                val = v if isinstance(v, str) else json.dumps(v)
                if len(val) > 200:
                    val = val[:200] + "..."
                lines.append(f"  {k}: {val}")
    lines.append(
        "\nProduce the preconditions and hunting hypothesis for this CVE. "
        "Return ONLY valid JSON with keys 'preconditions' and 'hunting_hypothesis'."
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def _call_llm(prompt, endpoint, api_key, model):
    """Call the OpenAI-compatible API and return the response text."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,  # low temp for consistency
        "max_tokens": 500,
    }
    resp = requests.post(
        f"{endpoint.rstrip('/')}/chat/completions",
        headers=headers,
        json=body,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Response parser
# ---------------------------------------------------------------------------

def _parse_response(text):
    """Extract structured data from the LLM response.

    Handles both raw JSON and markdown-code-fence-wrapped JSON.
    """
    text = text.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON object via regex
        m = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if m:
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
        else:
            return None

    pre = (data.get("preconditions") or "").strip()
    hyp = (data.get("hunting_hypothesis") or "").strip()

    if not pre and not hyp:
        return None

    # Fallback: if LLM returned paragraphs, truncate hypothesis to first
    # sentence that starts with a verb and ends with period
    if "\n" in hyp:
        for sent in hyp.split("\n"):
            sent = sent.strip()
            if any(sent.lower().startswith(w) for w in
                   ("monitor", "hunt", "look", "watch", "detect")):
                hyp = sent.rstrip(".")
                break
        else:
            # Keep just the first sentence
            hyp = hyp.split(".")[0] + "."

    return {"preconditions": pre, "hunting_hypothesis": hyp}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def synthesize(cve_id, vendor, product, description, cwe_ids,
               cvss_vector, vulnrichment_data, research_data):
    """Generate preconditions and hunting hypothesis via LLM.

    Parameters
    ----------
    Returns
    -------
    dict with keys "preconditions" and "hunting_hypothesis", or None on failure.
    """
    endpoint = os.environ.get(
        "KEVRICHMENT_LLM_ENDPOINT",
        DEFAULT_ENDPOINT,
    )
    api_key = os.environ.get(
        "KEVRICHMENT_LLM_API_KEY",
        os.environ.get("OPENAI_API_KEY", ""),
    )
    model = os.environ.get(
        "KEVRICHMENT_LLM_MODEL",
        DEFAULT_MODEL,
    )

    if not api_key:
        print("    [llm-synthesis] No API key found "
              "(set KEVRICHMENT_LLM_API_KEY or OPENAI_API_KEY)")
        return None

    prompt = _build_prompt(
        cve_id, vendor, product, description, cwe_ids,
        cvss_vector, vulnrichment_data, research_data,
    )

    try:
        raw = _call_llm(prompt, endpoint, api_key, model)
        result = _parse_response(raw)
        if result:
            return result
        print(f"    [llm-synthesis] Could not parse response for {cve_id}")
        return None
    except Exception as e:
        print(f"    [llm-synthesis] API call failed for {cve_id}: {e}")
        return None
