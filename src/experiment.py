"""
Experiment script for OpenAI models
"""

from openai import OpenAI
from anthropic import Anthropic, InternalServerError
from typing import Callable

from src.common import (
    SEED,
    TEMPERATURE,
    get_sys_prompt,
)

GPT_MODELS = [
    "gpt-3.5-turbo-0125",
    "gpt-4-turbo-2024-04-09",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini-2024-07-18",
]

O1_MODELS = [
    "o1-mini-2024-09-12",
    "o1-preview-2024-09-12",
]

CLAUDE_MODELS = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-5-sonnet-20240620",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-3-7-sonnet-20250219",
]

DEEPSEEK_MODELS = [
    "deepseek-reasoner",
    "deepseek-chat",
]


def get_o1_model(
    client: OpenAI,
    model: str = "o1-preview-2024-09-12",
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    pure: bool = False,
) -> Callable[[str], str | None]:
    def generate_type_signature(prompt: str) -> str | None:
        completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": get_sys_prompt(pure) + "\n" + prompt},
            ],
            model=model,
        )

        content = completion.choices[0].message.content
        return content if isinstance(content, str) else None

    return generate_type_signature


def get_oai_model(
    client: OpenAI,
    model: str = "gpt-3.5-turbo",
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    pure: bool = False,
) -> Callable[[str], str | None]:
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
            # Set parameters to ensure reproducibility
            seed=seed,
            temperature=temperature,
        )

        content = completion.choices[0].message.content
        return content if isinstance(content, str) else None

    return generate_type_signature


def get_ant_ttc_model(
    client: Anthropic,
    model: str = "claude-3-7-sonnet-20250219",
    pure: bool = False,
) -> Callable[[str], str | None]:
    def generate_type_signature(prompt: str) -> str | None:
        try:
            message = client.beta.messages.create(
                model=model,
                thinking={"type": "enabled", "budget_tokens": 1024},
                system=get_sys_prompt(pure),
                messages=[
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2048,
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
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    pure: bool = False,
) -> Callable[[str], str | None]:
    def generate_type_signature(prompt: str) -> str | None:
        try:
            message = client.messages.create(
                system=get_sys_prompt(pure),
                messages=[
                    {"role": "user", "content": prompt},
                ],
                model=model,
                max_tokens=1024,
                # ! the following parameters are not supported by Claude API
                # seed=seed,
                # temperature=temperature,
                # top_p=top_p,
            )
        except InternalServerError as e:
            print(e)
            return None
        contents = message.content
        if len(contents) > 0:
            text = contents[0].text  # type: ignore
            return text if isinstance(text, str) else None
        else:
            return None

    return generate_type_signature
