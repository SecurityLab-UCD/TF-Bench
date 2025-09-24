"""
Experiment script
"""

from tqdm import tqdm
from orjsonl import orjsonl

from .common import get_prompt
from .evaluation import prover_evaluate, EvalResult
from .lm import router, LMAnswer
from .load import load_tfb_from_hf


def run_one_model(
    model: str,
    pure: bool = False,
    output_file: str | None = None,
    effort: str | None = None,
) -> EvalResult:
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

    tasks = load_tfb_from_hf("pure" if pure else "base")
    gen_results: list[LMAnswer | None] = []
    for task in tqdm(tasks, desc=model):
        prompt = get_prompt(task)

        response = client.generate(prompt)
        r: LMAnswer | None = response.value_or(None)
        gen_results.append(r)
        if output_file:
            orjsonl.append(output_file, r if r else {"error": str(response.failure())})

    eval_acc = prover_evaluate(tasks, gen_results, pure=pure)
    return eval_acc
