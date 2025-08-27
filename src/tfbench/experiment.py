"""
Experiment script
"""

import logging

from tqdm import tqdm
from returns.result import Success, Failure, ResultE
import orjson

from .common import get_prompt
from .evaluation import evaluate, EvalResult
from .lm import router, LMAnswer
from .load import load_from_hf


def run_one_model(
    model: str,
    pure: bool = False,
    output_file: str | None = None,
    effort: str | None = None,
) -> ResultE[EvalResult]:
    """Running the generation & evaluation pipeline for one pre-supported model

    Args:
        model (str): name of the model to evaluate
        pure (bool, optional): To evaluate on the `pure` split or not. Defaults to False.
        output_file (str | None, optional): The file to save generation result. Defaults to None.
            Warning: If None, generation results will not be saved to disk.
        effort (str | None, optional): Reasoning effort. Defaults to None.
            Warning: Different model handles None(default) effort differently.

    Returns:
        EvalResult: evaluation result including accuracy
    """
    client = router(model, pure, effort)
    if not client:
        return Failure(Exception(f"Failed to create client for {model}."))

    tasks = load_from_hf("pure" if pure else "base")
    gen_results: list[LMAnswer] = []
    for task in tqdm(tasks, desc=model):
        prompt = get_prompt(task)
        match client.generate(prompt):
            case Success(r):
                gen_results.append(r)
                if output_file:
                    with open(output_file, "ab") as file:
                        file.write(orjson.dumps(r, option=orjson.OPT_APPEND_NEWLINE))
            case Failure(e):
                logging.error(f"Error generating response: {e}")
                return Failure(e)

    eval_acc = evaluate(tasks, gen_results)
    return Success(eval_acc)
