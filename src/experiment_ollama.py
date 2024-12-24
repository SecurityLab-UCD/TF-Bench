"""
Experiment script for OSS models using Ollama
"""

from ollama import Client as OllamaClient
from typing import Union
from src.common import (
    SEED,
    TEMPERATURE,
    SYSTEM_PROMPT,
    INSTRUCT_PROMPT,
)

OLLAMA_OSS = [
    "phi3:3.8b",
    "phi3:14b",
    "mistral",
    "mixtral:8x7b",
    "mixtral:8x22b",
    "llama3:8b",
    "llama3:70b",
    "llama3.1:8b",
    "llama3.1:70b",
    "llama3.1:405b",
    "llama3.2:1b",
    "llama3.2:8b",
    "llama3.3:70b",
    "gemma:2b",
    "gemma:7b",
    "gemma2:9b",
    "gemma2:27b",
    "qwen2:1.5b",
    "qwen2:7b",
    "qwen2:72b",
    "qwen2.5:1.5b",
    "qwen2.5:7b",
    "qwen2.5:72b",
    "deepseek-v2:16b",
    "deepseek-v2:236b",
    "deepseek-v2.5:236b",
]


OLLAMA_CODE = [
    "codegemma:2b",
    "codegemma:7b",
    "qwen2.5-coder:1.5b",
    "qwen2.5-coder:7b",
    "codestral:22b",
    "codellama:7b",
    "codellama:13b",
    "codellama:70b",
    "granite-code:3b",
    "granite-code:8b",
    "granite-code:20b",
    "granite-code:34b",
    "deepseek-coder-v2:16b",
    "deepseek-coder-v2:236b",
]

OLLAMA_MODELS = OLLAMA_OSS + OLLAMA_CODE


def get_model(
    client: OllamaClient,
    model: str = "llama3",
    seed=SEED,
    temperature=TEMPERATURE,
):
    def generate_type_signature(prompt: str) -> Union[str, None]:
        response = client.chat(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {"role": "user", "content": INSTRUCT_PROMPT + "\n" + prompt},
            ],
            model=model,
            options={
                "seed": seed,
                "temperature": temperature,
            },
        )

        if isinstance(response, dict) and "message" in response:
            message = response["message"]
            if isinstance(message, dict) and "content" in message:
                content = message["content"]
                if isinstance(content, str):
                    return content

        return None

    return generate_type_signature
