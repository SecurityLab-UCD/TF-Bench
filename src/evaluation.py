import fire
import json
import logging
from src.common import BenchmarkTask
from src.postprocessing import postprocess, TASK_STRATEGIES, RESPONSE_STRATEGIES
from funcy_chain import Chain
from dacite import from_dict
from itertools import starmap
import re


def tokenize_type_signature(sig: str) -> list[str]:
    """
    A minimal tokenizer splitting on spaces, parentheses, commas, '->', [ and ], etc.
    This won't handle all Haskell syntax, but might suffice for simpler cases.

    Example: "(a -> b) -> [a] -> [b]"
      -> ["(", "a", "->", "b", ")", "->", "[", "a", "]", "->", "[", "b", "]"]
    """
    # Notice we've added \[ and \] to the group of delimiters
    pattern = r"(\s+|\(|\)|,|\[|\]|->)"
    tokens = re.split(pattern, sig)
    # Remove empty/whitespace-only tokens
    tokens = [t for t in tokens if t.strip()]
    return tokens


def normalize_type_vars(tokens: list[str]) -> list[str]:
    """
    Replace each unique lowercase token that looks like a type variable
    with a canonical 'v0', 'v1', etc., in the order encountered.
    """
    var_map = {}
    next_id = 0
    result = []

    for tok in tokens:
        # Very crude check: type variable starts with lowercase
        # (We exclude known symbols like '->', parentheses, brackets, commas, etc.)
        if re.fullmatch(r"[a-z]\w*", tok):
            if tok not in var_map:
                var_map[tok] = f"v{next_id}"
                next_id += 1
            result.append(var_map[tok])
        else:
            # Non-variable tokens remain as-is
            result.append(tok)

    return result


def alpha_equiv(s1: str, s2: str) -> bool:
    """
    Check if two type signatures are 'alpha-equivalent' under
    a naive textual approach.
    """
    t1 = tokenize_type_signature(s1)
    t2 = tokenize_type_signature(s2)

    n1 = normalize_type_vars(t1)
    n2 = normalize_type_vars(t2)

    return n1 == n2


def evaluate_one_task(task: BenchmarkTask, result: str) -> bool:
    ground_truth = postprocess(task.signature, TASK_STRATEGIES)
    result = postprocess(result, RESPONSE_STRATEGIES)
    return alpha_equiv(ground_truth, result)


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
    results_file: str = "data/experiment/gpt_generated_responses.jsonl",
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
    logging.info(json.dumps(eval_acc, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
