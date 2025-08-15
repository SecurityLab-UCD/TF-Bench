import os
from typing import Callable
import json
import logging

from funcy_chain import Chain
from funcy import lmap
from tqdm import tqdm
from dacite import from_dict
from returns.result import ResultE, Success, Failure

import fire
from tfbench.common import (
    BenchmarkTask,
    get_prompt,
)

from tfbench.postprocessing import postprocess, RESPONSE_STRATEGIES
from tfbench.evaluation import evaluate
from tfbench.lm import is_supported, router, LMAnswer, extract_response


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
    assert is_supported(model), f"{model} is not supported."

    # hard-coding benchmark file path for experiment
    input_file = "tfb.pure.json" if pure else "tfb.json"
    input_file = os.path.abspath(input_file)
    assert os.path.exists(
        input_file
    ), f"{input_file} does not exist! Please download or build it first."

    if output_file is None:
        os.makedirs("result", exist_ok=True)
        output_file = os.path.abspath(f"result/{model}.txt")
    logging.info(f"Writing generation results in {output_file}.")

    client = router(model, pure)
    assert client, f"Failed to create client for {model}."

    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    prompts = lmap(get_prompt, tasks)
    responses: list[ResultE[LMAnswer]] = lmap(
        client.generate, tqdm(prompts, desc=model)
    )

    gen_results = (
        Chain(responses)
        .map(extract_response)
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
