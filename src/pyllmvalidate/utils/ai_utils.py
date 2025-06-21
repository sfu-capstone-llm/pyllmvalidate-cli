"""
AI utilities for code validation.
"""

from openai import OpenAI
from ..validators.core import DiffAnalysis, SYSTEM_PROMPT_TEMPLATE


def init_ai_client() -> OpenAI:
    """Initialize the AI client."""
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def get_ai_response(output_format: str, diff_analysis: DiffAnalysis, client: OpenAI) -> str:
    """Get response from AI for code validation."""
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(output_format=output_format)
    completion = client.chat.completions.create(
        model="",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diff_analysis.model_dump_json()},
        ],
    )
    return completion.choices[0].message.content 