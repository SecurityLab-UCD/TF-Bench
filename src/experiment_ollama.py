"""
Experiment script for OSS models using Ollama
"""

from ollama import Client as OllamaClient
from typing import Union
from src.common import (
    SEED,
    TEMPERATURE,
    TOP_P,
    SYSTEM_PROMPT,
    INSTRUCT_PROMPT,
)

OLLAMA_OSS = [
    "gemma2:27b",
    "llama3",
    "llama3:70b",
    "mixtral:8x22b",
    "llama3.1:8b",
    "llama3.1:70b",
    "llama3.1:405b",
    "gemma:2b",
    "gemma:7b",
    "gemma2",
    "mistral",
    "mixtral:8x7b",
    "phi3",
    "phi3:medium",
    "qwen2:0.5b",
    "qwen2:1.5b",
    "qwen2:7b",
    "qwen2:72b",
    "qwen2.5:0.5b",
    "qwen2.5:1.5b",
    "qwen2.5:3b",
    "qwen2.5:7b",
    "qwen2.5:14b",
    "qwen2.5:32b",
    "qwen2.5:72b",
    "deepseek-v2:16b",
    "deepseek-v2:236b",
    "deepseek-v2.5:236b",
]


OLLAMA_CODE = [
    "deepseek-coder-v2:16b",
    "deepseek-coder-v2:236b",
    "codegemma:2b",
    "codegemma:7b",
    "codellama:7b",
    "codellama:13b",
    "codellama:70b",
    "qwen2.5-coder:1.5b",
    "qwen2.5-coder:7b",
    "granite-code:3b",
    "granite-code:8b",
    "granite-code:20b",
    "granite-code:34b",
    "codestral:22b",
]

OLLAMA_MODELS = OLLAMA_OSS + OLLAMA_CODE


def get_model(
    client: OllamaClient,
    model: str = "llama3",
    seed=SEED,
    temperature=TEMPERATURE,
    top_p=TOP_P,
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
                "top_p": top_p,
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
