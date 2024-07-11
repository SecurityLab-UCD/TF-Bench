import fire
import json
import logging
from src.common import BenchmarkTask
from src.experiment import postprocess
from funcy_chain import Chain
from dacite import from_dict
from itertools import starmap


def evaluate(task: BenchmarkTask, result: str) -> bool:
    ground_truth = postprocess(task.signature)
    result = postprocess(result)
    return ground_truth == result


def main(
    results_file: str,
    output_file: str | None = None,
    benchmark_file: str = "Benchmark-F.json",
):
    with open(benchmark_file, "r") as file:
        benchmark_f: list[BenchmarkTask] = (
            Chain(json.load(file))
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
    if output_file is not None:
        with open(output_file, "w") as fp:
            json.dump(d, fp)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
