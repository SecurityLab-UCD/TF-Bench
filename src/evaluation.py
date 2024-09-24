import fire
import json
import logging
from src.common import BenchmarkTask
from src.postprocessing import (
    postprocess,
    TASK_STRATEGIES,
    RESPONSE_STRATEGIES,
)
from funcy_chain import Chain
from dacite import from_dict
from itertools import starmap
from tree_sitter import Language, Parser
import tree_sitter
import tree_sitter_haskell
from typing import Generator


def relevant_code_nodes(
    node: tree_sitter.Node, source_code: str
) -> Generator[str, None, None]:
    """
    Traverse the tree, yielding only the relevant nodes (ignoring whitespace and comments).
    """
    for child in node.children:
        if child.type in ["comment", "whitespace"]:  # Ignore these types of nodes
            continue
        if child.children:
            yield from relevant_code_nodes(child, source_code)
        else:
            # Yield the text of the node, skipping irrelevant ones
            yield source_code[child.start_byte : child.end_byte]


def normalize_signature(signature: str) -> str:
    parser = Parser()
    parser.language = Language(tree_sitter_haskell.language())
    # Parse the signature into a tree
    tree = parser.parse(signature.encode("utf-8"))
    # Traverse and collect relevant parts of the tree
    root_node = tree.root_node
    relevant_parts = list(relevant_code_nodes(root_node, signature))
    # Join the relevant parts into a single string
    return "".join(relevant_parts)


def compare_signatures(sig1: str, sig2: str) -> bool:
    # Normalize both signatures by extracting relevant parts of the AST
    normalized_sig1 = normalize_signature(sig1)
    normalized_sig2 = normalize_signature(sig2)

    # Compare the normalized versions
    return normalized_sig1 == normalized_sig2


def evaluate_one_task(task: BenchmarkTask, result: str) -> bool:
    result = postprocess(result, RESPONSE_STRATEGIES)
    ground_truth = postprocess(task.signature, TASK_STRATEGIES)
    # print(result)
    # print(ground_truth)
    # print(compare_signatures(result, ground_truth))
    # print('\n')

    return compare_signatures(result, ground_truth)


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
    benchmark_file: str = "Benchmark-F.removed.jsonl",
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
