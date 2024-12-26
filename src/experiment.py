"""
Experiment script for OpenAI models
"""

import fire
import os
from openai import OpenAI
from ollama import Client as OllamaClient
from anthropic import Anthropic, InternalServerError
import json
from funcy_chain import Chain
from dacite import from_dict
from typing import Callable
from funcy import lmap
from tqdm import tqdm

from src.evaluation import evaluate
from src.common import (
    BenchmarkTask,
    SEED,
    TEMPERATURE,
    get_prompt,
    get_sys_prompt,
)
from src.experiment_ollama import OLLAMA_MODELS, get_model as get_ollama_model
from src.postprocessing import postprocess, RESPONSE_STRATEGIES

GPT_MODELS = [
    "gpt-3.5-turbo-0125",
    "gpt-4-turbo-2024-04-09",
    "gpt-4o-2024-11-20",
    "gpt-4o-mini-2024-07-18",
    "o1-mini-2024-09-12",
    "o1-preview-2024-09-12",
    "o1-2024-12-17",
]

CLAUDE_MODELS = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
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


def main(
    input_file: str = "Benchmark-F.removed.json",
    output_file: str | None = None,
    log_file: str | None = None,
    model: str = "gpt-3.5-turbo",
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    port: int = 11434,
    pure: bool = False,
):
    assert (
        model in GPT_MODELS + OLLAMA_MODELS + CLAUDE_MODELS
    ), f"{model} is not supported."

    if output_file is None:
        os.makedirs("result", exist_ok=True)
        output_file = f"result/{model}.txt"

    if log_file is None:
        log_file = "evaluation_log.jsonl"

    client: OpenAI | Anthropic | OllamaClient
    generate: Callable[[str], str | None]

    if model in GPT_MODELS:
        assert "OPENAI_API_KEY" in os.environ, "Please set OPEN_API_KEY in environment!"
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        if model.startswith("o1"):
            generate = get_o1_model(client, model, seed, temperature, pure)
        else:
            generate = get_oai_model(client, model, seed, temperature, pure)
    elif model in CLAUDE_MODELS:
        assert (
            "ANTHROPIC_API_KEY" in os.environ
        ), "Please set ANTHROPIC_API_KEY in environment!"
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        generate = get_ant_model(client, model, seed, temperature, pure)
    else:
        client = OllamaClient(host=f"http://localhost:{port}")
        generate = get_ollama_model(client, model, seed, temperature, pure)

    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    prompts = lmap(get_prompt, tasks)
    responses = lmap(generate, tqdm(prompts, desc=model))
    gen_results = (
        Chain(responses)
        .map(lambda x: x if x is not None else "")  # convert None to empty string
        .map(lambda s: postprocess(s, RESPONSE_STRATEGIES))
        .map(str.strip)
        .value
    )

    with open(output_file, "w") as file:
        file.write("\n".join(gen_results))

    eval_acc = evaluate(tasks, gen_results)
    print(eval_acc)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(log_file, "a") as fp:
        logging_result = {"model_name": model, **eval_acc}
        fp.write(f"{json.dumps(logging_result)}\n")


if __name__ == "__main__":
    fire.Fire(main)
