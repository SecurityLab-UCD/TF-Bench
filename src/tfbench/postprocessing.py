import re
from functools import reduce
from typing import Callable

# pylint: disable=missing-function-docstring
# function docstring for postprocessing is disable since too simple


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


def remove_space_after_comma(text: str) -> str:
    return re.sub(r",\s", ",", text)


def remove_space_between_arrow(text: str) -> str:
    return re.sub(r"\s*->\s*", "->", text)


def remove_backtick(text: str) -> str:
    return text.strip("`")


def postprocess(result: str, strategies: list[Callable[[str], str]]) -> str:
    """
    1. Replace "[Char]" with "String" and remove the markdown symbols
    2. remove Markdown code block
    3. remove `{func_name} ::` if included
    """

    return reduce(lambda acc, f: f(acc), strategies, result)


TASK_STRATEGIES: list[Callable[[str], str]] = [
    char_list_to_str,
    rm_md_block,
    rm_func_name,
    str.strip,
    rm_new_line,
    remove_space_after_comma,
    remove_space_between_arrow,
    remove_backtick,
]

RESPONSE_STRATEGIES: list[Callable[[str], str]] = [
    char_list_to_str,
    rm_md_block,
    rm_func_name,
    str.strip,
    rm_new_line,
    remove_space_after_comma,
    remove_space_between_arrow,
    remove_backtick,
]
