import fire
import json
import logging
from add_dependency import BenchmarkTask
from funcy_chain import Chain
from dacite import from_dict


def get_function_name(id_str: str) -> str | None:
    """Extract the function name from the signature field."""
    if "::" in id_str:
        return id_str.split("::")[0].strip()
    return None


def evaluation(benchmark_f: list[BenchmarkTask], results: list[str]):
    num_match = 0
    num_mismatch = 0
    total_levenshtein_distance = 0

    for benchmark, result in zip(benchmark_f, results):
        benchmark_func_name = get_function_name(benchmark.signature)
        result_func_name = get_function_name(result)
        
        if benchmark_func_name == result_func_name:
            if benchmark.signature == result:
                num_match += 1
            else:
                num_mismatch += 1
    
    total = num_match + num_mismatch
    accuracy = num_match / total if total > 0 else 0

    print(f"Match: {num_match}, Mismatch: {num_mismatch}")
    print(f"Accuracy: {accuracy:.2f}")


def main(
    benchmark_file: str = "data/filtered/base-4.20.0.0.jsonl",
    results_file: str = "data/experiment/gpt/base-4.20.0.0.jsonl",
):
    
    with open(benchmark_file, "r") as file:
        benchmark_f: list[BenchmarkTask] = (
            Chain(file.readlines())
            .map(json.loads)
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .value
        )
    
    with open(results_file, "r") as file:
        results: list[str] = (
            Chain(file.readlines())
            .map(json.loads)
            .value
        )

    evaluation(benchmark_f, results)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)