"""
Experiment script for OpenAI models
"""

import fire
import os
from openai import OpenAI
from ollama import Client as OllamaClient
import json
import logging
from funcy_chain import Chain
from dacite import from_dict
from typing import Callable

from src.evaluation import evaluate
from src.postprocessing import postprocess, RESPONSE_STRATEGIES
from src.common import (
    BenchmarkTask,
    SEED,
    TEMPERATURE,
    TOP_P,
    SYSTEM_PROMPT,
    INSTRUCT_PROMPT,
    get_prompt,
)
from src.experiment_ollama import OLLAMA_MODELS, get_model as get_ollama_model

GPT_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
]


def get_model(
    client: OpenAI,
    model: str = "gpt-3.5-turbo",
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    top_p: float = TOP_P,
) -> Callable[[str], str | None]:
    def generate_type_signature(prompt: str) -> str | None:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {"role": "user", "content": INSTRUCT_PROMPT + prompt},
            ],
            model=model,
            # Set parameters to ensure reproducibility
            seed=seed,
            temperature=temperature,
            top_p=top_p,
        )

        content = completion.choices[0].message.content
        return content if isinstance(content, str) else None

    return generate_type_signature


def main(
    input_file: str = "Benchmark-F.json",
    output_file: str | None = None,
    model: str = "gpt-3.5-turbo",
    api_key: str | None = None,
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    top_p: float = TOP_P,
    port: int = 11434,
):
    assert model in GPT_MODELS + OLLAMA_MODELS, f"{model} is not supported."
    assert api_key is not None, "API key is not provided."

    if output_file is None:
        os.makedirs("result", exist_ok=True)
        output_file = f"result/{model}.txt"

    client: OpenAI | OllamaClient
    generate: Callable[[str], str | None]
    if model.startswith("gpt"):
        client = OpenAI(api_key=api_key)
        generate = get_model(client, model, seed, temperature, top_p)
    else:
        client = OllamaClient(host=f"http://localhost:{port}")
        generate = get_ollama_model(client, model, seed, temperature, top_p)

    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    gen_results: list[str] = (
        Chain(tasks)
        .map(get_prompt)
        .map(generate)  # generate: str -> str | None
        .map(lambda x: x if x is not None else "")  # convert None to empty string
        .map(lambda x: postprocess(x, RESPONSE_STRATEGIES))
        .value
    )

    with open(output_file, "w") as file:
        file.write("\n".join(gen_results))

    logging.info(f"Get {len(gen_results)} results from {model}.")
    eval_acc = evaluate(tasks, gen_results)
    logging.info(eval_acc)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open("evaluation_log.txt", "a") as log_file:
        logging_result = {"model_name": model, **eval_acc}
        log_file.write(f"{logging_result}\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
