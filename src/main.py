from os.path import join as pjoin, abspath
import os

import fire
from orjsonl import orjsonl
from returns.result import Success, Failure

from tfbench import run_one_model, analysis_multi_runs, EvalResult


def main(
    model: str,
    effort: str | None = None,
    n_repeats: int = 3,
    log_file: str = "evaluation_log.jsonl",
):
    """Main script to run experiments reported in the paper"""

    def _run(pure: bool):
        results: list[EvalResult] = []
        split = "pure" if pure else "base"
        for i in range(n_repeats):
            result_dir = abspath(pjoin("results", model, split))
            os.makedirs(result_dir, exist_ok=True)
            result_file = pjoin(result_dir, f"run-{i}.jsonl")
            r = run_one_model(
                model,
                pure=pure,
                output_file=result_file,
                effort=effort,
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

    # _eval(pure=False)
    _eval(pure=True)


if __name__ == "__main__":
    fire.Fire(main)
