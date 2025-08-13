"""
Experiment script for OpenAI models
"""

from typing import Callable

from openai import OpenAI
from anthropic import Anthropic, InternalServerError
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig

from tfbench.common import get_sys_prompt, MAX_TOKENS

OAI_MODELS = [
    "gpt-3.5-turbo-0125",
    "gpt-4-turbo-2024-04-09",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini-2024-07-18",
]

OAI_TTC_MODELS = [
    "o1-mini-2024-09-12",
    "o1-preview-2024-09-12",
    "o1-2024-12-17",
    "o3-mini-2025-01-31",
    "o3-2025-04-16",
    "o4-mini-2025-04-16",
]

CLAUDE_MODELS = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
]

CLAUDE_TTC_MODELS = [
    "claude-3-7-sonnet-20250219",
]

DEEPSEEK_MODELS = [
    "deepseek-reasoner",
    "deepseek-chat",
]

GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
]

GEMINI_TTC_MODELS = [
    "gemini-2.5-flash-preview-04-17",
    "gemini-2.5-pro-preview-03-25",
]


def get_oai_ttc_model(
    client: OpenAI,
    model: str = "o1-preview-2024-09-12",
    pure: bool = False,
) -> Callable[[str], str | None]:
    """OpenAI Reasoning Models"""

    def generate_type_signature(prompt: str) -> str | None:
        completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": get_sys_prompt(pure) + "\n\n" + prompt},
            ],
            model=model,
        )

        content = completion.choices[0].message.content
        return content if isinstance(content, str) else None

    return generate_type_signature


def get_oai_model(
    client: OpenAI,
    model: str = "gpt-3.5-turbo",
    pure: bool = False,
) -> Callable[[str], str | None]:
    """Regular OpenAI Models"""

    def generate_type_signature(prompt: str) -> str | None:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": get_sys_prompt(pure),
                },
                {"role": "user", "content": prompt},
            ],
            model=model,
        )

        content = completion.choices[0].message.content
        return content if isinstance(content, str) else None

    return generate_type_signature


def get_ant_ttc_model(
    client: Anthropic,
    model: str = "claude-3-7-sonnet-20250219",
    pure: bool = False,
    thinking_budget: int = 1024,
) -> Callable[[str], str | None]:
    "Claude Reasoning Models"

    def generate_type_signature(prompt: str) -> str | None:
        try:
            message = client.beta.messages.create(
                model=model,
                thinking={"type": "enabled", "budget_tokens": thinking_budget},
                system=get_sys_prompt(pure),
                messages=[
                    {"role": "user", "content": prompt},
                ],
                max_tokens=thinking_budget + MAX_TOKENS,
                betas=["output-128k-2025-02-19"],
            )
        except InternalServerError as e:
            print(e)
            return None

        try:
            thinking, answer = message.content
            text = answer.text  # type: ignore
            return text if isinstance(text, str) else None
        except:
            return None

    return generate_type_signature


def get_ant_model(
    client: Anthropic,
    model: str = "claude-3-5-sonnet-20240620",
    pure: bool = False,
) -> Callable[[str], str | None]:
    """Claude regular Models"""

    def generate_type_signature(prompt: str) -> str | None:
        try:
            message = client.messages.create(
                system=get_sys_prompt(pure),
                messages=[
                    {"role": "user", "content": prompt},
                ],
                model=model,
                max_tokens=MAX_TOKENS,
            )
        except InternalServerError as e:
            print(e)
            return None
        contents = message.content
        if len(contents) > 0:
            text = contents[0].text  # type: ignore
            return text if isinstance(text, str) else None

        return None

    return generate_type_signature


def get_gemini_model(
    client: genai.Client,
    model: str = "gemini-2.0-flash-lite",
    pure: bool = False,
) -> Callable[[str], str | None]:
    """Gemini Models"""

    def generate_type_signature(prompt: str) -> str | None:
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=GenerateContentConfig(
                system_instruction=[get_sys_prompt(pure)],
            ),
        )
        return response.text if isinstance(response.text, str) else None

    return generate_type_signature


def get_gemini_ttc_model(
    client: genai.Client,
    model: str = "gemini-2.5-flash-preview-04-17",
    pure: bool = False,
    thinking_budget: int = 1024,
) -> Callable[[str], str | None]:
    """Gemini Reasoning Models"""

    def generate_type_signature(prompt: str) -> str | None:
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=GenerateContentConfig(
                system_instruction=[get_sys_prompt(pure)],
                thinking_config=ThinkingConfig(
                    thinking_budget=thinking_budget,
                    include_thoughts=False,
                ),
            ),
        )
        return response.text if isinstance(response.text, str) else None

    return generate_type_signature
