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
from google import genai

import fire
from tfbench.common import (
    BenchmarkTask,
    get_prompt,
)

from tfbench.experiment import (
    OAI_MODELS,
    OAI_TTC_MODELS,
    CLAUDE_MODELS,
    CLAUDE_TTC_MODELS,
    DEEPSEEK_MODELS,
    GEMINI_MODELS,
    GEMINI_TTC_MODELS,
    get_ant_model,
    get_ant_ttc_model,
    get_oai_model,
    get_oai_ttc_model,
    get_gemini_model,
    get_gemini_ttc_model,
)
from tfbench.experiment_ollama import OLLAMA_MODELS, get_ollama_model
from tfbench.postprocessing import postprocess, RESPONSE_STRATEGIES
from tfbench.evaluation import evaluate


def main(
    model: str,
    port: int = 11434,
    pure: bool = False,
    thinking_budget: int = 1024,
    output_file: str | None = None,
    log_file: str = "evaluation_log.jsonl",
):
    """
    Run an experiment using various AI models to generate and evaluate type signatures.

    Parameters:
        model (str): Name of the model to use for generating type signatures. Must be one of:
                     - GPT_MODELS: ["gpt-3.5-turbo-0125", "gpt-4-turbo-2024-04-09", ...]
                     - OLLAMA_MODELS, CLAUDE_MODELS, or O1_MODELS.
                     Default is "gpt-3.5-turbo".

        port (int): Port number for connecting to the Ollama server (if using Ollama models).
                    Ignored for other models. Default is 11434.

        pure (bool): If True, uses the original variable naming in type inference.
                     If False, uses rewritten variable naming (e.g., `v1`, `v2`, ...). Default is False.
    """
    assert (
        model
        in OAI_MODELS
        + OAI_TTC_MODELS
        + OLLAMA_MODELS
        + DEEPSEEK_MODELS
        + CLAUDE_MODELS
        + CLAUDE_TTC_MODELS
        + GEMINI_MODELS
        + GEMINI_TTC_MODELS
    ), f"{model} is not supported."

    # hard-coding benchmark file path for experiment
    input_file = "tfb.pure.json" if pure else "tfb.json"
    input_file = os.path.abspath(input_file)
    assert os.path.exists(
        input_file
    ), f"{input_file} does not exist! Please download or build it first."

    if output_file is None:
        os.makedirs("result", exist_ok=True)
        output_file = f"result/{model}.txt"

    client: OpenAI | Anthropic | OllamaClient | genai.Client
    generate: Callable[[str], str | None]

    if model in OAI_MODELS:
        assert "OPENAI_API_KEY" in os.environ, "Please set OPEN_API_KEY in environment!"
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        generate = get_oai_model(client, model, pure)

    elif model in OAI_TTC_MODELS:
        assert "OPENAI_API_KEY" in os.environ, "Please set OPEN_API_KEY in environment!"
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        generate = get_oai_ttc_model(client, model, pure)
    elif model in CLAUDE_MODELS:
        assert (
            "ANTHROPIC_API_KEY" in os.environ
        ), "Please set ANTHROPIC_API_KEY in environment!"
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        generate = get_ant_model(client, model, pure)
    elif model in CLAUDE_TTC_MODELS:
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        generate = get_ant_ttc_model(client, model, pure, thinking_budget)

    elif model in DEEPSEEK_MODELS:
        assert (
            "DEEPSEEK_API_KEY" in os.environ
        ), "Please set DEEPSEEK_API_KEY in environment!"
        client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com"
        )
        generate = get_oai_model(client, model, pure)

    elif model in GEMINI_MODELS:
        assert (
            "GOOGLE_API_KEY" in os.environ
        ), "Please set GOOGLE_API_KEY in environment!"
        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        generate = get_gemini_model(client, model, pure)
    elif model in GEMINI_TTC_MODELS:
        assert (
            "GOOGLE_API_KEY" in os.environ
        ), "Please set GOOGLE_API_KEY in environment!"
        client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
        generate = get_gemini_ttc_model(client, model, pure, thinking_budget)

    else:
        client = OllamaClient(host=f"http://localhost:{port}")
        generate = get_ollama_model(client, model, pure)

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
