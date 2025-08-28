from os.path import join as pjoin, abspath
import os

import fire
import orjson
from returns.result import Success, Failure

from tfbench import run_one_model, analysis_multi_runs


def main(
    model: str,
    effort: str | None = None,
    n_repeats: int = 3,
    log_file: str = "evaluation_log.jsonl",
):
    """Main script to run experiments reported in the paper"""

    def _run(pure: bool):
        results = []
        split = "pure" if pure else "base"
        for i in range(n_repeats):
            result_dir = abspath(pjoin("results", model, split))
            os.makedirs(result_dir, exist_ok=True)
            result_file = pjoin(result_dir, f"run-{i}.jsonl")
            match run_one_model(
                model, pure=pure, output_file=result_file, effort=effort
            ):
                case Success(r):
                    results.append(r)
                case Failure(e):
                    return Failure(e)
        return Success(analysis_multi_runs(results))

    def _eval(pure: bool):
        split = "pure" if pure else "base"
        print(f"Running {model} on TF-Bench ({split}):")
        match _run(pure=pure):
            case Success((mean, std)):
                print(f"Accuracy: {mean:.4f} ± {std:.4f}")
                print("====================================")
                with open(log_file, "ab") as f:
                    f.write(
                        orjson.dumps(
                            {
                                "model": model,
                                "split": split,
                                "effort": effort,
                                "n_repeats": n_repeats,
                                "mean": mean,
                                "std": std,
                            },
                            option=orjson.OPT_APPEND_NEWLINE,
                        )
                    )
            case Failure(e):
                print(f"Error in base run: {e}")
                return

    _eval(pure=False)
    _eval(pure=True)


if __name__ == "__main__":
    fire.Fire(main)
