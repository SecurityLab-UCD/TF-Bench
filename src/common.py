from dataclasses import dataclass
import re
import copy
from funcy import lmap
from functools import reduce
from typing import Callable
from openai import OpenAI
import os
import openai
import tiktoken


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

    def trim_text(text: str, max_tokens: int = 4000) -> str:
        """
        Trims the input text to ensure it fits within the maximum token limit.
        """
        tokenizer = tiktoken.get_encoding("cl100k_base")
        # Tokenizing the text
        tokens = tokenizer.encode(text)
        # Trimming the text to fit within the token limit
        trimmed_tokens = tokens[:max_tokens]
        text = tokenizer.decode(trimmed_tokens)

        return text

    def reduce_repetition(text):
        def replace_repetition(match):
            pattern = match.group(1)
            return pattern

        # Find and replace patterns repeated 10 or more times
        return re.sub(r"(.+?)\1{9,}", replace_repetition, text)

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
        full_prompt = prompt + text
        trimmed_prompt = trim_text(full_prompt, max_tokens=4000)

        try:
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant.",
                    },
                    {"role": "user", "content": trimmed_prompt},
                ],
                model=model,
                seed=seed,
                temperature=temperature,
                top_p=top_p,
            )
            content = completion.choices[0].message.content

        except openai.APIError as e:
            # Instead of trying to parse the exception as JSON, check the string representation
            error_message = str(e)
            if (
                "invalid_request_error" in error_message
                and "invalid_prompt" in error_message
                and "repetitive patterns" in error_message
            ):

                # Apply reduce_repetition to the prompt
                reduced_prompt = reduce_repetition(trimmed_prompt)

                completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant.",
                        },
                        {"role": "user", "content": reduced_prompt},
                    ],
                    model=model,
                    seed=seed,
                    temperature=temperature,
                    top_p=top_p,
                )
                content = completion.choices[0].message.content
            else:
                # If it's not the specific error we're handling, re-raise the exception
                raise

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
