from itertools import starmap
import re
from typing import TypedDict

import numpy as np
from deprecated import deprecated

from .common import BenchmarkTask
from .postprocessing import postprocess, TASK_STRATEGIES, RESPONSE_STRATEGIES
from .lm import LMAnswer


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


@deprecated(reason="Use GHC for evaluation instead", version="0.1.0")
def evaluate_one_task(task: BenchmarkTask, result: LMAnswer | None) -> bool:
    """evaluate a single task against its result by alpha equivalence"""
    if result is None:
        return False

    ground_truth = postprocess(task.signature, TASK_STRATEGIES).strip()
    predicted = postprocess(result.answer, RESPONSE_STRATEGIES).strip()
    return alpha_equiv(ground_truth, predicted)


class EvalResult(TypedDict):
    total: int
    n_correct: int
    accuracy: float


def evaluate(tasks: list[BenchmarkTask], results: list[LMAnswer | None]) -> EvalResult:
    """evaluate all generation results"""

    assert len(tasks) == len(results)
    eval_results = starmap(evaluate_one_task, zip(tasks, results))
    n_correct = sum(eval_results)
    acc = n_correct / len(tasks)

    return {
        "total": len(tasks),
        "n_correct": n_correct,
        "accuracy": acc,
    }


def analysis_multi_runs(results: list[EvalResult]) -> tuple[float, float]:
    """calculate mean and std of accuracy of multiple runs"""
    accs = list(map(lambda r: r["accuracy"], results))
    return np.mean(accs).item(), np.std(accs).item()


def get_incorrect(
    tasks: list[BenchmarkTask], results: list[LMAnswer | None]
) -> list[tuple[BenchmarkTask, LMAnswer | None]]:
    """Get a list of tasks that were incorrectly answered."""
    incorrect = []
    for task, result in zip(tasks, results):
        if not evaluate_one_task(task, result):
            incorrect.append((task, result))
    return incorrect
