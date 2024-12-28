"""
Experiment script for OSS models using Ollama
"""

from ollama import Client as OllamaClient, ResponseError
from typing import Union
from src.common import SEED, TEMPERATURE, SYSTEM_PROMPT, INSTRUCT_PROMPT, get_sys_prompt

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
    "llama3.2:3b",
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
    "qwen2.5-coder:1.5b",
    "qwen2.5-coder:7b",
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
    model: str = "llama3:8b",
    seed=SEED,
    temperature=TEMPERATURE,
    pure: bool = False,
):
    """
    Configure and return a function to generate type signatures using an Ollama model.

    Parameters:
        client (OllamaClient): The Ollama client instance used for sending requests to the model.

        model (str): Name of the model to use for generating type signatures. Must be one of the predefined models in OLLAMA_MODELS.
                     Default is "llama3:8b".

        seed (int): Random seed to ensure reproducibility in experiments. Default is defined by SEED.

        temperature (float): Sampling temperature for the model's outputs. Higher values
                             produce more diverse outputs. Default is defined by TEMPERATURE.

        pure (bool): If True, uses the original variable naming in type inference.
                     If False, uses rewritten variable naming (e.g., `v1`, `v2`, ...). Default is False.

    Returns:
        Callable[[str], Union[str, None]]: A function that takes a prompt string as input and returns the generated type
                                           signature as a string, or None if the generation fails.
    """
    def generate_type_signature(prompt: str) -> Union[str, None]:
        try:
            response = client.chat(
                messages=[
                    {
                        "role": "system",
                        "content": get_sys_prompt(pure),
                    },
                    {"role": "user", "content": prompt},
                ],
                model=model,
                options={
                    "seed": seed,
                    "temperature": temperature,
                },
            )
        except ResponseError as e:
            print(e)
            return None

        if isinstance(response, dict) and "message" in response:
            message = response["message"]
            if isinstance(message, dict) and "content" in message:
                content = message["content"]
                if isinstance(content, str):
                    return content

        return None

    return generate_type_signature
