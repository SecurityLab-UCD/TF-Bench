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

    def trim_text(text: str, max_tokens: int = 16385) -> str:
        """
        Trims the input text to ensure it fits within the maximum token limit.
        """
        # Tokenizing the text
        tokens = text.split()
        if len(tokens) <= max_tokens:
            return text
        
        # Trimming the text to fit within the token limit
        trimmed_tokens = tokens[:max_tokens]
        return ' '.join(trimmed_tokens)

    def remove_extra(
            text: str,
            model: str = "gpt-3.5-turbo",
            seed=123,
            temperature=0.0,
            top_p=1.0,
        ) -> str | None:
        prompt = (
            "Below is a piece of text that includes a Haskell type signature "
            "may be along with explanations and commentaries. \n\n"
            "1. Remove all explanations and commentaries. ONLY output the type signature. \n\n"
            "2. If the text doesn't involve any additional explanations and commentaries and "
            "just has the type signature. Print what it is. \n\n"
            "3. Do not provide any additional commentaries or explanations. \n"
            "TEXT starts: \n\n"
        )
        
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        
        # Trim the text to fit within the token limit
        full_text = prompt + text
        trimmed_text = trim_text(full_text, max_tokens=4000)
        
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {"role": "user", "content": trimmed_text},
            ],
            model=model,
            # Set parameters to ensure reproducibility
            seed=seed,
            temperature=temperature,
            top_p=top_p,
        )
        content = completion.choices[0].message.content
        return content if isinstance(content, str) else None

    def remove_extra_wrapper(text: str) -> str:
        result = remove_extra(text)
        return result if result is not None else ""

    strategies: list[Callable[[str], str]] = [
        char_list_to_str,
        rm_md_block,
        rm_func_name,
        str.strip,
        rm_new_line,
        remove_extra_wrapper,
    ]

    return reduce(lambda acc, f: f(acc), strategies, result)
