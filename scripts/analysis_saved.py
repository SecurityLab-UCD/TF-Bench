from os.path import abspath, dirname, basename, join as pjoin
import os
import fire
from orjsonl import orjsonl
from tfbench import (
    analysis_multi_runs,
    load_tfb_from_hf,
    load_gen_results_jsonl,
    evaluate,
)


def main(result_dir: str, log_file: str | None = None):
    """
    Arguments:
        result_dir (str): assumed in format `/some/path/.../<model>/<split>/`.
            For example: results/gpt-5-nano-2025-08-07/base,
            where <model> is `gpt-5-nano-2025-08-07` and <split> is `base`.
            WARNING: we parse the  <model> and <split> in this way.
        log_file (str | None): path to the log file. If None, this script only prints to stdout.
    """

    result_dir = abspath(result_dir)
    model = basename(dirname(result_dir))
    split = basename(result_dir)

    tasks = load_tfb_from_hf(split)
    # load all jsonl files from `result_dir`
    jsonl_files = [
        pjoin(result_dir, f) for f in os.listdir(result_dir) if f.endswith(".jsonl")
    ]
    runs = [load_gen_results_jsonl(f) for f in jsonl_files]
    accs = [evaluate(tasks, run) for run in runs]
    mean, std = analysis_multi_runs(accs)

    print(f"Model: {model}")
    print(f"Split: {split}")
    print(f"Accuracy: {mean:.4f} ± {std:.4f}")

    if log_file is not None:
        log_obj = {
            "model": model,
            "split": split,
            "effort": None,
            "n_repeats": len(runs),
            "mean": mean,
            "std": std,
        }
        orjsonl.append(log_file, log_obj)


if __name__ == "__main__":
    fire.Fire(main)
