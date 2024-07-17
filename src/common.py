from dataclasses import dataclass
import re
import copy
from funcy import lmap
from functools import reduce
from typing import Callable

from openai import OpenAI
import os


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

    def remove_extra(
        text: str,
        model: str = "gpt-3.5-turbo",
        seed=123,
        temperature=0.0,
        top_p=1.0,
    ):
        prompt = (
            "Below is a piece of text that includes a Haskell type signature "
            "may be along with explanations and commentaries. \n\n"
            "1. Remove all explanations and commentaries. ONLY output the type signature. \n\n"
            "2. If the text doesn't involve any additional explanations and commentaries and "
            "just has the type signature. Print what it is. \n\n"
            "Do not provide any additional commentaries or explanations. \n"
            "TEXT starts: \n\n"
        )
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {"role": "user", "content": prompt + text},
            ],
            model=model,
            # Set parameters to ensure reproducibility
            seed=seed,
            temperature=temperature,
            top_p=top_p,
        )
        return completion.choices[0].message.content

    strategies: list[Callable[[str], str]] = [
        char_list_to_str,
        rm_md_block,
        rm_func_name,
        str.strip,
        rm_new_line,
        remove_extra,
    ]
    # NOTE: Python `reduce` is a `foldl`
    # so the left most function is executed first
    return reduce(lambda acc, f: f(acc), strategies, result)
