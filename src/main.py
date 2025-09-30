from os.path import join as pjoin, abspath
import os

import fire
from orjsonl import orjsonl

from tfbench import run_one_model, analysis_multi_runs, EvalResult
from tfbench.lm import router


def main(
    model: str,
    effort: str | None = None,
    n_repeats: int = 3,
    log_file: str = "evaluation_log.jsonl",
):
    """Ready-to use evaluation script for a single model.

    Args:
        model (str): The model's name, please refer to `tfbench.lm.supported_models` for supported models.
        effort (str | None, optional): The effort level to use for evaluation. Defaults to None.
        n_repeats (int, optional): The number of times to repeat the evaluation. Defaults to 3.
        log_file (str, optional): The file to log results to. Defaults to "evaluation_log.jsonl".
    """

    def _run(pure: bool):
        client = router(model, pure, effort)
        results: list[EvalResult] = []
        split = "pure" if pure else "base"
        result_dir = abspath(pjoin("results", model, split))
        for i in range(n_repeats):
            os.makedirs(result_dir, exist_ok=True)
            result_file = pjoin(result_dir, f"run-{i}.jsonl")
            r = run_one_model(
                client,
                pure=pure,
                output_file=result_file,
            )
            results.append(r)
        return analysis_multi_runs(results)

    def _eval(pure: bool):
        split = "pure" if pure else "base"
        print(f"Running {model} on TF-Bench ({split}):")
        mean, std = _run(pure=pure)
        print(f"Accuracy: {mean:.4f} ± {std:.4f}")
        print("====================================")
        orjsonl.append(
            log_file,
            {
                "model": model,
                "split": split,
                "effort": effort,
                "n_repeats": n_repeats,
                "mean": mean,
                "std": std,
            },
        )

    _eval(pure=False)
    _eval(pure=True)


if __name__ == "__main__":
    fire.Fire(main)
