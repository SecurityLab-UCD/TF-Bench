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


# Load the API key from environment variables
load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPEN_API_KEY is not None, "OPENAI_API_KEY not in env"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
assert GROQ_API_KEY is not None, "GROQ_API_KEY not in env"


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
    client: OpenAI | Groq,
    model: str = "gpt3.5-turbo",
    seed=123,
    temperature=0.0,
    top_p=1.0,
):
    def generate_type_signature(prompt: str) -> str | None:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {"role": "user", "content": prompt},
            ],
            model=model,
            # Set parameters to ensure reproducibility
            seed=seed,
            temperature=temperature,
            top_p=top_p,
        )

        return completion.choices[0].message.content

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

    strategies: list[Callable[[str], str]] = [
        char_list_to_str,
        rm_md_block,
        rm_func_name,
        str.strip,
    ]
    # NOTE: Python `reduce` is a `foldl`
    # so the left most function is executed first
    return reduce(lambda acc, f: f(acc), strategies, result)


def main(
    input_file: str = "data/filtered/base-4.20.0.0.jsonl",
    output_file: str = "data/generated_responses.jsonl",
    model: str = "gpt3.5",
    api_key: str | None = None,
    seed: int = 123,
    temperature: float = 0.0,
    top_p: float = 0.0,
):
    assert model in ["gpt3.5-turbo", "llama3-8b-8192"], f"{model} is not supported."
    assert api_key is not None, "API key is not provided."

    client: OpenAI | Groq

    if model.startswith("gpt"):
        client = OpenAI(api_key=api_key)
    elif model.startswith("llama"):
        client = Groq(api_key=api_key)
    else:  # in case there is other models in the future
        exit(1)

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
