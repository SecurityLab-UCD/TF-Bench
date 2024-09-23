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
import tree_sitter_haskell


def are_trees_equal(tree1, tree2):
    def compare_nodes(node1, node2):
        # Check if node types are the same
        if node1.type != node2.type:
            return False
        # Check if the ranges (start and end positions) are the same
        if node1.start_point != node2.start_point or node1.end_point != node2.end_point:
            return False
        # Check if the number of children is the same
        if node1.child_count != node2.child_count:
            return False
        # Recursively check each child node
        for i in range(node1.child_count):
            child1 = node1.child(i)
            child2 = node2.child(i)
            if not compare_nodes(child1, child2):
                return False
        return True

    # Start comparison from the root nodes
    root1 = tree1.root_node
    root2 = tree2.root_node

    return compare_nodes(root1, root2)


def evaluate_one_task(task: BenchmarkTask, result: str) -> bool:
    result = postprocess(result, RESPONSE_STRATEGIES)
    print(result)
    ground_truth = postprocess(task.signature, TASK_STRATEGIES)
    print(ground_truth)
    print('\n')


    parser = Parser()
    parser.language = Language(tree_sitter_haskell.language())
    ground_truth_tree = parser.parse(bytes(ground_truth, "utf8"))
    result_tree = parser.parse(bytes(result, "utf8"))
    are_trees_equal(ground_truth_tree, result_tree)

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
