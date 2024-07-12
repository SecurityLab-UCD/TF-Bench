from dataclasses import dataclass
import re
import copy
from funcy import lmap
from functools import reduce
from typing import Callable


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


def postprocess(result: str) -> str:
    """
    1. Replace "[Char]" with "String" and remove the markdown symbols
    2. remove Markdown code block
    3. remove `{func_name} ::` if included
    """

    def char_list_to_str(text: str) -> str:
        return text.replace("[Char]", "String")

    def rm_md_block(text: str) -> str:
        return text.replace("```haskell\n", "").replace("\n```", "")

    def rm_func_name(text: str) -> str:
        if "::" in text:
            text = text.split("::")[1]
        return text

    def rm_new_line(text: str) -> str:
        return text.replace("\n", "")

    strategies: list[Callable[[str], str]] = [
        char_list_to_str,
        rm_md_block,
        rm_func_name,
        str.strip,
        rm_new_line,
    ]
    # NOTE: Python `reduce` is a `foldl`
    # so the left most function is executed first
    return reduce(lambda acc, f: f(acc), strategies, result)
