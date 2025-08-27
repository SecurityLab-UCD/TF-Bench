import os
import json
import logging

from funcy_chain import Chain
from funcy import lmap
from tqdm import tqdm
from returns.result import ResultE
import fire

from tfbench.common import get_prompt
from tfbench.postprocessing import postprocess, RESPONSE_STRATEGIES
from tfbench.evaluation import evaluate
from tfbench.lm import router, LMAnswer, extract_response
from tfbench.load import load_from_hf


def main(
    model: str,
    pure: bool = False,
    effort: str | None = None,
    output_file: str | None = None,
    log_file: str = "evaluation_log.jsonl",
    use_vllm_server: bool = False,
):
    """
    Run an experiment using various AI models to generate and evaluate type signatures.

    Parameters:
        model (str): Name of the model to use for generating type signatures. Must be one of:
                     - GPT_MODELS: ["gpt-3.5-turbo-0125", "gpt-4-turbo-2024-04-09", ...]
                     - OLLAMA_MODELS, CLAUDE_MODELS, or O1_MODELS.
                     Default is "gpt-3.5-turbo".

        pure (bool): If True, uses the original variable naming in type inference.
                     If False, uses rewritten variable naming (e.g., `v1`, `v2`, ...). Default is False.

    """

    if output_file is None:
        os.makedirs("result", exist_ok=True)
        if "/" in model:
            dir_name = model.split("/")[0]
            os.makedirs(f"result/{dir_name}", exist_ok=True)
        output_file = os.path.abspath(f"result/{model}.txt")
    logging.info(f"Writing generation results in {output_file}.")

    client = router(model, pure, effort, use_vllm_server)
    assert client, f"Failed to create client for {model}."

    tasks = load_from_hf("pure" if pure else "base")
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

    # writing results
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
