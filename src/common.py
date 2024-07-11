from dataclasses import dataclass
import re
import copy
from funcy import lmap


@dataclass
class BenchmarkTask:
    task_id: str
    signature: str
    code: str
    poly_type: str
    dependencies: list[str] | None


def clean_tab_spaces(task: BenchmarkTask) -> BenchmarkTask:
    def clean(s: str) -> str:
        return re.sub(r"[ \t]+", " ", s)

    new_task = copy.copy(task)
    new_task.code = clean(task.code)
    new_task.dependencies = lmap(clean, task.dependencies)
    new_task.signature = clean(task.signature)

    return new_task
