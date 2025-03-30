import os
from typing import Callable
import json
from funcy_chain import Chain
from funcy import lmap
from tqdm import tqdm
from dacite import from_dict


from openai import OpenAI
from ollama import Client as OllamaClient
from anthropic import Anthropic

import fire
from src.common import (
    BenchmarkTask,
    SEED,
    TEMPERATURE,
    get_prompt,
)

from src.experiment import (
    O1_MODELS,
    GPT_MODELS,
    CLAUDE_MODELS,
    DEEPSEEK_MODELS,
    get_ant_model,
    get_ant_ttc_model,
    get_oai_model,
    get_o1_model,
)
from src.experiment_ollama import OLLAMA_MODELS, get_model as get_ollama_model
from src.postprocessing import postprocess, RESPONSE_STRATEGIES
from src.evaluation import evaluate


def main(
    input_file: str = "Benchmark-F.removed.json",
    output_file: str | None = None,
    log_file: str | None = None,
    full_type: bool = True,
    model: str = "gpt-3.5-turbo",
    seed: int = SEED,
    temperature: float = TEMPERATURE,
    port: int = 11434,
    pure: bool = False,
    reasoning: bool = False,
):
    """
    Run an experiment using various AI models to generate and evaluate type signatures.

    Parameters:
        input_file (str): Path to the input JSON file containing benchmark tasks.
                          Default is "Benchmark-F.removed.json".

        output_file (str | None): Path to the output file where generated type signatures will be saved.
                                  If None, the output will be saved to "result/{model}.txt". Default is None.

        log_file (str | None): Path to the log file where evaluation metrics will be appended.
                               If None, defaults to "evaluation_log.jsonl". Default is None.

        full_type (bool): Determines whether to ask the model to predict the full type signature in the prompt.
                          If True, the model will be asked to complete full type signature.
                          If False, the model will be asked to complete the return type in type signature. Default is True.

        model (str): Name of the model to use for generating type signatures. Must be one of:
                     - GPT_MODELS: ["gpt-3.5-turbo-0125", "gpt-4-turbo-2024-04-09", ...]
                     - OLLAMA_MODELS, CLAUDE_MODELS, or O1_MODELS.
                     Default is "gpt-3.5-turbo".

        seed (int): Random seed to ensure reproducibility in experiments. Default is 0.

        temperature (float): Sampling temperature for the model's outputs. Higher values
                             produce more diverse outputs. Default is 0.0 (deterministic outputs).

        port (int): Port number for connecting to the Ollama server (if using Ollama models).
                    Ignored for other models. Default is 11434.

        pure (bool): If True, uses the original variable naming in type inference.
                     If False, uses rewritten variable naming (e.g., `v1`, `v2`, ...). Default is False.

        reasoning (bool): If True, uses the reasoning prompt for the model. NOTE: this is not for claude-3-7-sonnet.
    """
    assert (
        model
        in GPT_MODELS + OLLAMA_MODELS + CLAUDE_MODELS + O1_MODELS + DEEPSEEK_MODELS
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
        generate = get_oai_model(client, model, seed, temperature, pure)
    elif model in O1_MODELS:
        assert "OPENAI_API_KEY" in os.environ, "Please set OPEN_API_KEY in environment!"
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        generate = get_o1_model(client, model, seed, temperature, pure)
    elif model in CLAUDE_MODELS:
        assert (
            "ANTHROPIC_API_KEY" in os.environ
        ), "Please set ANTHROPIC_API_KEY in environment!"
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        if reasoning:
            generate = get_ant_ttc_model(client, model, pure)
        else:
            generate = get_ant_model(client, model, pure)
    elif model in DEEPSEEK_MODELS:
        assert (
            "DEEPSEEK_API_KEY" in os.environ
        ), "Please set DEEPSEEK_API_KEY in environment!"
        client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com"
        )
        generate = get_oai_model(client, model, seed, temperature, pure)
    else:
        client = OllamaClient(host=f"http://localhost:{port}")
        generate = get_ollama_model(client, model, seed, temperature, pure)

    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    prompts = lmap(lambda x: get_prompt(x, full_type), tasks)
    responses = lmap(generate, tqdm(prompts, desc=model))
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
        logging_result = {"model_name": model, **eval_acc}
        fp.write(f"{json.dumps(logging_result)}\n")


if __name__ == "__main__":
    fire.Fire(main)
