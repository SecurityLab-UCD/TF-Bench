from itertools import starmap
import re
from typing import TypedDict
from multiprocessing import Pool, cpu_count

import numpy as np
from deprecated import deprecated
from returns.result import Success, Failure, Result

from .common import BenchmarkTask
from .postprocessing import postprocess, TASK_STRATEGIES, RESPONSE_STRATEGIES
from .lm import LMAnswer
from .ghc import get_prover, ghc_prove_equiv
from .type_def import get_type_defs


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


@deprecated(reason="Use `ghc_prove_equiv` instead", version="0.1.0")
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


@deprecated(reason="Use `prove_one_task` instead", version="0.1.0")
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


@deprecated(reason="Use `prover_evaluate` instead", version="0.1.0")
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


def prove_one_task(
    task: BenchmarkTask, result: LMAnswer | None, pure: bool = False
) -> Result[None, str]:
    """prove two type signatures are equivalent using GHC"""
    if result is None:
        return Failure("Generation Failed")

    predicted_body = postprocess(result.answer, RESPONSE_STRATEGIES).strip()
    predicted = f"f :: {predicted_body}"
    defs = get_type_defs(task) if pure else []
    # only failing case from get_prover is syntax error of generated type signature
    equiv = (
        get_prover(task.signature, predicted, defs)
        .alt(lambda _: "Syntax Error: Tree-Sitter Parsing Failed")
        .bind(ghc_prove_equiv)
    )
    return equiv


def prover_evaluate(
    tasks: list[BenchmarkTask],
    results: list[LMAnswer | None],
    pure: bool = False,
    nproc: int = cpu_count(),
) -> EvalResult:
    """evaluate all generation results using GHC to prove equivalence

    NOTE: currently only support the `base` split

    Args:
        tasks (list[BenchmarkTask]): list of benchmark tasks
        results (list[LMAnswer | None]): list of generation results
        pure (bool, optional): whether to evaluate on the `pure` split or not.
            Since we use TypeOperators to *prove type equivalence,
            we need to define all custom types in the `pure` split.
            Defaults to False.
        nproc (int, optional): number of processes to use.
            Defaults to cpu_count() to use all available CPUs.
    """
    assert len(tasks) == len(results)

    with Pool(processes=nproc) as pool:
        eval_results = pool.starmap(
            prove_one_task, zip(tasks, results, [pure] * len(tasks))
        )

    n_correct = sum(1 for r in eval_results if isinstance(r, Success))
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
    tasks: list[BenchmarkTask],
    results: list[LMAnswer | None],
    pure: bool = False,
    nproc: int = cpu_count(),
) -> list[tuple[BenchmarkTask, LMAnswer | None, str]]:
    """Get a list of tasks that were incorrectly answered."""

    assert len(tasks) == len(results)

    with Pool(processes=nproc) as pool:
        eval_results = pool.starmap(
            prove_one_task, zip(tasks, results, [pure] * len(tasks))
        )

    incorrect = []
    for task, result, eval_result in zip(tasks, results, eval_results):
        match eval_result:
            case Success(_):
                continue
            case Failure(message):
                incorrect.append((task, result, message))
    return incorrect
