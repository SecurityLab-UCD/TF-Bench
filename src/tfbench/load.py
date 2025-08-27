from typing import Any, Mapping, cast
from datasets import load_dataset
from .common import BenchmarkTask


def _cast(data_entry) -> BenchmarkTask:
    r = cast(Mapping[str, Any], data_entry)
    return BenchmarkTask(
        task_id=r["task_id"],
        poly_type=r["poly_type"],
        signature=r["signature"],
        code=r["code"],
        dependencies=r["dependencies"],
    )


def load_from_hf(split: str = "base") -> list[BenchmarkTask]:
    """Load TF-Bench dataset from HuggingFace Hub.

    Args:
        split (str): The dataset split to load. Options are "base" or "pure". Default is "base".

    Returns:
        list[BenchmarkTask]: A list of BenchmarkTask instances.
    """

    dataset = load_dataset("SecLabUCD/TF-Bench", split=split)
    return [_cast(d) for d in dataset]
