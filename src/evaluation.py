import fire
import json
import logging
from src.common import BenchmarkTask
from src.postprocessing import (
    postprocess,
    char_list_to_str,
    rm_md_block,
    rm_func_name,
    rm_new_line,
    remove_space_after_comma,
    remove_space_between_arrow,
    remove_backtick,
)
from funcy_chain import Chain
from dacite import from_dict
from itertools import starmap
from typing import Callable


def evaluate_one_task(task: BenchmarkTask, result: str) -> bool:
    strategies: list[Callable[[str], str]] = [
        char_list_to_str,
        rm_md_block,
        rm_func_name,
        str.strip,
        rm_new_line,
        remove_space_after_comma,
        remove_space_between_arrow,
        remove_backtick,
    ]
    ground_truth = postprocess(task.signature, strategies)
    return ground_truth == result


def evaluate(
    benchmark_f: list[BenchmarkTask], results: list[str]
) -> dict[str, int | float]:

    assert len(benchmark_f) == len(results)
    eval_results = starmap(evaluate_one_task, zip(benchmark_f, results))
    n_correct = sum(eval_results)
    acc = n_correct / len(benchmark_f)

    return {
        "total": len(benchmark_f),
        "n_correct": n_correct,
        "accuracy": acc,
    }


def main(
    benchmark_file: str = "Benchmark-F.jsonl",
    results_file: str = "data/experiment/gpt_enerated_responses.jsonl",
):
    with open(benchmark_file, "r") as file:
        benchmark_f: list[BenchmarkTask] = (
            Chain(file.readlines())
            .map(json.loads)
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .value
        )
    with open(results_file, "r") as file:
        results: list[str] = Chain(file.readlines()).map(json.loads).value

    eval_acc = evaluate(benchmark_f, results)
    logging.info(eval_acc)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
