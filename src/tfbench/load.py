from typing import Any, Mapping, cast
from datasets import load_dataset

from dacite import from_dict
from orjsonl import orjsonl

from .common import BenchmarkTask
from .lm import LMAnswer


def _cast(data_entry) -> BenchmarkTask:
    r = cast(Mapping[str, Any], data_entry)
    return BenchmarkTask(
        task_id=r["task_id"],
        poly_type=r["poly_type"],
        signature=r["signature"],
        code=r["code"],
        dependencies=r["dependencies"],
    )


def load_tfb_from_hf(split: str = "base") -> list[BenchmarkTask]:
    """Load TF-Bench dataset from HuggingFace Hub.

    Args:
        split (str): The dataset split to load. Options are "base" or "pure". Default is "base".

    Returns:
        list[BenchmarkTask]: A list of BenchmarkTask instances.
    """

    dataset = load_dataset("SecLabUCD/TF-Bench", split=split)
    return [_cast(d) for d in dataset]


def load_gen_results_jsonl(result_file: str) -> list[LMAnswer | None]:
    """load generation results from a jsonl file"""
    objs: list[dict[str, str]] = orjsonl.load(result_file)  # type: ignore
    return [from_dict(LMAnswer, obj) if "answer" in obj else None for obj in objs]
