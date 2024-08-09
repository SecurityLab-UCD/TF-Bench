"""
Experiment script for OSS models using Ollama
"""

import fire
import os
from ollama import Client as OllamaClient
from tqdm import tqdm  # Import tqdm for the progress bar
from dacite import from_dict
import json
import logging
from src.evaluation import evaluate
from src.postprocessing import postprocess, RESPONSE_STRATEGIES
from typing import Union, Callable
from src.common import (
    BenchmarkTask,
    SEED,
    TEMPERATURE,
    TOP_P,
    SYSTEM_PROMPT,
    INSTRUCT_PROMPT,
    get_prompt,
)


OLLAMA_MODELS = [
    "llama2:7b",
    "llama2:13b",
    "llama2:70b",
    "llama3",
    "llama3:70b",
    "phi3",
    "phi3:medium",
    "gemma:2b",
    "gemma:7b",
    "gemma2",
    "gemma2:27b",
    "mistral",
    "mixtral:8x22b",
    "mixtral:8x7b",
    "deepseek-coder-v2:16b",
    "deepseek-coder-v2:236b",
    "codegemma:2b",
    "codegemma:7b",
    "codellama:7b",
    "codellama:13b",
    "codellama:34b",
    "codellama:70b",
    "starcoder2:3b",
    "starcoder2:7b",
    "starcoder2:15b",
    "nous-hermes2:10.7b",
    "nous-hermes2:34b",
    "nous-hermes2-mixtral:8x7b",
    "codestral:22b",
    "stable-code:3b",
    "codeqwen:7b",
    "phind-codellama:34b",
    "granite-code:3b",
    "granite-code:8b",
    "granite-code:20b",
    "granite-code:34b",
    "codebooga:34b",
]


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
                {"role": "user", "content": INSTRUCT_PROMPT + "\n\n" + prompt},
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
