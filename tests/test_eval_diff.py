from os.path import abspath, dirname, basename, join as pjoin
import os
from itertools import starmap
from multiprocessing import Pool

import pytest
import fire
from orjsonl import orjsonl
from tqdm import tqdm
from tfbench import (
    analysis_multi_runs,
    load_tfb_from_hf,
    load_gen_results_jsonl,
    prover_evaluate,
)
from tfbench.ghc import get_prover
from tfbench.evaluation import evaluate_one_task, prove_one_task
from tfbench.common import task2md
from tfbench.type_def import get_type_defs
from tfbench.postprocessing import postprocess, TASK_STRATEGIES, RESPONSE_STRATEGIES


def diff_one_file(file_path: str, split: str):
    tasks = load_tfb_from_hf(split)
    answers = load_gen_results_jsonl(abspath(file_path))

    old_eval = starmap(evaluate_one_task, zip(tasks, answers))
    with Pool() as pool:
        new_eval = pool.starmap(
            prove_one_task, zip(tasks, answers, [split == "pure"] * len(tasks))
        )

    for t, a, o, n in zip(tasks, answers, old_eval, new_eval):
        if a is None:
            continue
        # if o:
        #     assert n, "both evaluations should return a result"
        if o and not n:
            print(task2md(t))
            defs = get_type_defs(t)

            predicted_body = postprocess(a.answer, RESPONSE_STRATEGIES).strip()
            predicted = f"f :: {predicted_body}"
            print(get_prover(t.signature, predicted, defs).unwrap())
            assert False


def test_diff_recorded():
    """different test evaluation function with recorded results
    Since the new prover evaluation fixes the false negative issue,
    we assume if an answer is determined as correct by the old evaluation,
    it should also be correct by the new evaluation.
    """

    result_path = abspath("results")
    # skip the test if there are not recorded results
    if not os.path.exists(result_path):
        pytest.skip("No recorded results found, skip the test.")

    # walk the result directory to find all jsonl files
    for b, _, f in os.walk(result_path):
        for file in f:
            if file.endswith(".jsonl"):
                file_path = pjoin(b, file)
                split = basename(b)
                print(f"Diffing {file_path} ...")
                diff_one_file(file_path, split)


if __name__ == "__main__":
    fire.Fire(test_diff_recorded)
