"""
(deprecated) Experiment script for OSS models using Ollama
This script reproduce legacy results for OSS models using Ollama in our paper's Appendix.
New models should use our vLLM option instead.
"""

from typing import Union
import os
import json

from ollama import Client as OllamaClient, ResponseError
import fire
from dacite import from_dict
from tqdm import tqdm
from funcy_chain import Chain

from tfbench.lm import get_sys_prompt
from tfbench.common import BenchmarkTask, get_prompt
from tfbench.postprocessing import postprocess, RESPONSE_STRATEGIES
from tfbench.evaluation import evaluate

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


def get_ollama_model(
    client: OllamaClient,
    model: str = "llama3:8b",
    pure: bool = False,
):
    """
    Configure and return a function to generate type signatures using an Ollama model.

    Parameters:
        client (OllamaClient): The Ollama client instance used for sending requests to the model.

        model (str): Name of the model to use for generating type signatures.
                    Must be one of the predefined models in OLLAMA_MODELS.
                    Default is "llama3:8b".

        pure (bool): If True, uses the original variable naming in type inference.
                     If False, uses rewritten variable naming (e.g., `v1`, `v2`, ...). Default is False.

    Returns:
        Callable[[str], Union[str, None]]:
            A function that takes a prompt string as input and returns the generated type
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
            )
        except ResponseError as e:
            print(e)
            return None

        message = response.message
        if message.content:
            return str(message.content)

        return None

    return generate_type_signature


def main(
    model: str = "llama3:8b",
    pure: bool = False,
    port: int = 11434,
    output_file: str | None = None,
    log_file: str = "evaluation_log.jsonl",
):
    """
    Run an experiment using various AI models to generate and evaluate type signatures.

    Parameters:
        model (str): Name of the model to use for generating type signatures. Must be one of OLLAMA_MODELS

        port (int): Port number for connecting to the Ollama server.
                    Ignored for other models. Default is 11434.

        pure (bool): If True, uses the original variable naming in type inference.
                     If False, uses rewritten variable naming (e.g., `v1`, `v2`, ...). Default is False.
    """
    assert model in OLLAMA_MODELS, f"{model} is not supported."

    # hard-coding benchmark file path for experiment
    input_file = "tfb.pure.json" if pure else "tfb.json"
    input_file = os.path.abspath(input_file)
    assert os.path.exists(
        input_file
    ), f"{input_file} does not exist! Please download or build it first."

    if output_file is None:
        os.makedirs("result", exist_ok=True)
        output_file = f"result/{model}.txt"

    client = OllamaClient(host=f"http://localhost:{port}")
    generate = get_ollama_model(client, model, pure)

    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    prompts = map(get_prompt, tasks)
    responses = map(generate, tqdm(prompts, desc=model))
    gen_results = (
        Chain(responses)
        .map(lambda x: x if x is not None else "")  # convert None to empty string
        .map(lambda s: postprocess(s, RESPONSE_STRATEGIES))
        .map(str.strip)
        .value
    )

    with open(output_file, "w", errors="ignore") as file:
        file.write("\n".join(gen_results))

    eval_acc = evaluate(tasks, gen_results)
    print(eval_acc)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(log_file, "a") as fp:
        logging_result = {"model_name": model, **eval_acc, "pure": pure}
        fp.write(f"{json.dumps(logging_result)}\n")


if __name__ == "__main__":
    fire.Fire(main)
