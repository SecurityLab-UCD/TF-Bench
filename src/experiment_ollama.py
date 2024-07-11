import fire
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
import os
import json
from filter2complete import extract_function_name
import logging
from typing import Any
from add_dependency import BenchmarkTask
from funcy_chain import Chain
from dacite import from_dict
from typing import Callable
from functools import reduce
from ollama import Client


SYSTEM_PROMPT = """
Act as a static analysis tool for type inference.
Only output the type signature.
"""


# Get the prompt for the OpenAI API
def get_prompt(task: BenchmarkTask) -> str:
    """get prompt from a task instance"""

    fn_name = extract_function_name(task.task_id)
    code = task.code
    dependencies = task.dependencies

    if fn_name is not None:
        prompt = f"""
{code}
where
{dependencies}
--complete the following type signature for '{fn_name}'
--if there is type mismatch, output 'Error'
{fn_name} :: 
"""
    return prompt


def get_model(
    client: Client = Client(host='http://localhost:11434'),
    model: str = "llama3",
    seed=123,
    temperature=0.0,
    top_p=1.0,
):
    def generate_type_signature(prompt: str) -> str | None:
        response = client.chat(
            messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {"role": "user", "content": prompt},
                ],
            model=model,
            options = {
                "seed": seed,
                "top_p": top_p,
                "temperature": temperature,
            }
        )

        return response['message']['content']

    return generate_type_signature


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


def main(
    input_file: str = "data/filtered/base-4.20.0.0.jsonl",
    output_file: str = "data/generated_responses.jsonl",
    model: str = "llama3",
    seed: int = 123,
    temperature: float = 0.0,
    top_p: float = 1.0,
):

    client = Client(host='http://localhost:11434')

    generate = get_model(client, model, seed, temperature, top_p)

    with open(input_file, "r") as file:
        results: list[str] = (
            Chain(file.readlines())
            .map(json.loads)
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .map(get_prompt)
            .map(generate)  # generate : str -> str | None
            .map(str)  # covert all to str
            .map(postprocess)
            .map(json.dumps)
            .value
        )

    with open(output_file, "w") as file:
        file.write("\n".join(results))

    logging.info(f"Get {len(results)} results from {model}.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
