from os.path import abspath, basename, join as pjoin
import os
from typing import Literal

from openai import OpenAI
import fire
from tqdm import tqdm
from orjsonl import orjsonl

from tfbench import (
    load_tfb_from_hf,
    load_gen_results_jsonl,
)
from tfbench.evaluation import get_incorrect
from tfbench.error_analysis import error_analysis, ErrorAnalysisResult


def analysis(result_file_dir: str, split: Literal["base", "pure"], output_file: str):
    """script to run error analysis fo incorrect TF-Bench tasks"""
    client = OpenAI()
    tasks = load_tfb_from_hf(split)
    model = basename(abspath(result_file_dir))

    split_result_dir = pjoin(result_file_dir, split)

    incorrect = []
    print(f"Collecting incorrect results from {split_result_dir} on split {split}")
    for file in os.listdir(split_result_dir):
        if not file.endswith(".jsonl"):
            continue
        result_file_path = pjoin(split_result_dir, file)
        run_result = load_gen_results_jsonl(result_file_path)

        incorrect_of_run = get_incorrect(tasks, run_result, split == "pure")
        incorrect.extend(incorrect_of_run)

    print(f"Running error classification on {len(incorrect)} incorrect results")
    for task, answer, msg in tqdm(incorrect):
        error = error_analysis(client, task, answer, error_msg=msg)
        log_obj: ErrorAnalysisResult = {
            "model": model,
            "split": split,
            "task_id": task.task_id,
            "ground_truth": task.signature,
            "predicted": answer.answer if answer else None,
            "error_category": error.category,
            "error_explanation": error.explanation,
        }
        orjsonl.append(output_file, log_obj)


def main(result_file_dir: str, output_file: str | None = None):
    """run result analysis on both base and pure splits"""

    model = basename(abspath(result_file_dir))
    print(f"Running error analysis for model {model}")
    if output_file is None:
        dir_name = "err_analysis"
        os.makedirs(dir_name, exist_ok=True)
        output_file = f"{dir_name}/{model}.jsonl"
    output_file = abspath(output_file)

    analysis(result_file_dir, "base", output_file)
    analysis(result_file_dir, "pure", output_file)


if __name__ == "__main__":
    fire.Fire(main)
