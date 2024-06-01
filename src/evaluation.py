import fire
import json
import logging
from src.add_dependency import BenchmarkTask
from src.experiment import postprocess
from funcy_chain import Chain
from dacite import from_dict
from itertools import starmap


def get_function_name(id_str: str) -> str | None:
    """Extract the function name from the signature field."""
    if "::" in id_str:
        return id_str.split("::")[0].strip()
    return None


def evaluate(task: BenchmarkTask, result: str) -> bool:
    ground_truth = postprocess(task.signature)
    result = postprocess(result)
    return ground_truth == result


def main(
    benchmark_file: str = "data/filtered/base-4.20.0.0.jsonl",
    results_file: str = "data/experiment/gpt/base-4.20.0.0.jsonl",
    output_file: str = "evaluation_result.json",
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

    assert len(benchmark_f) == len(results)
    eval_results = starmap(evaluate, zip(benchmark_f, results))
    n_correct = sum(eval_results)
    acc = n_correct / len(benchmark_f)

    d = {
        "total": len(benchmark_f),
        "n_correct": n_correct,
        "accuracy": acc,
    }
    logging.info(d)
    with open(output_file, "w") as fp:
        fp.write(json.dumps(d))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
