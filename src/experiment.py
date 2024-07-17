import fire
from openai import OpenAI
from groq import Groq
import json
from filter2complete import extract_function_name
import logging
from add_dependency import BenchmarkTask
from funcy_chain import Chain
from dacite import from_dict
import time
from src.evaluation import evaluate
from src.common import postprocess
from typing import Union, Callable

SYSTEM_PROMPT = """
Act as a static analysis tool for type inference.
"""

INSTRUCT_PROMPT = """
1. Use the lowercase alphabet [a..z] for type variables instead of numbers.

2. ONLY output the type signature. Do Not Provide any additional commentaries or explanations.
"""


# Get the prompt for the OpenAI API
def get_prompt(task: BenchmarkTask) -> str:
    """get prompt from a task instance"""

    fn_name = extract_function_name(task.task_id)
    code = task.code
    dependencies = (
        "where\n" + "\n".join(task.dependencies)
        if task.dependencies is not None
        else ""
    )

    if fn_name is not None:
        prompt = f"""
{code}
{dependencies}
--complete the following type signature for '{fn_name}'
{fn_name} :: 
"""
    return prompt


def get_model(
    client: Union[OpenAI, Groq],
    model: str = "gpt-3.5-turbo",
    seed=123,
    temperature=0.0,
    top_p=1.0,
) -> Callable[[str], Union[str, None]]:
    def generate_type_signature(prompt: str) -> Union[str, None]:
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

        if isinstance(client, Groq):
            # rate limit for Groq is 30 requests per minute
            time.sleep(2)

        content = completion.choices[0].message.content
        return content if isinstance(content, str) else None

    return generate_type_signature


def main(
    input_file: str = "Benchmark-F.json",
    output_file: str | None = None,
    model: str = "gpt-3.5-turbo",
    api_key: str | None = None,
    seed: int = 123,
    temperature: float = 0.2,
    top_p: float = 0.95,
):
    assert model in [
        "gpt-3.5-turbo",
        "gpt-4-turbo",
        "gpt-4o",
        "llama3-8b-8192",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it",
        "gemma2-9b-it",
    ], f"{model} is not supported."
    assert api_key is not None, "API key is not provided."

    if output_file is None:
        output_file = f"{model}.txt"

    client: Union[OpenAI, Groq]

    if model.startswith("gpt"):
        client = OpenAI(api_key=api_key)
    elif (
        model.startswith("llama")
        or model.startswith("gemma")
        or model.startswith("mixtral")
    ):
        client = Groq(api_key=api_key)
    else:  # in case there are other models in the future
        exit(1)

    generate = get_model(client, model, seed, temperature, top_p)
    with open(input_file, "r") as fp:
        tasks = [from_dict(data_class=BenchmarkTask, data=d) for d in json.load(fp)]

    gen_results: list[str] = (
        Chain(tasks)
        .map(get_prompt)
        .map(generate)  # generate: str -> Union[str, None]
        .map(lambda x: x if x is not None else "")  # convert None to empty string
        .map(postprocess)
        .value
    )

    with open(output_file, "w") as file:
        file.write("\n".join(gen_results))

    logging.info(f"Get {len(gen_results)} results from {model}.")
    eval_acc = evaluate(tasks, gen_results)
    logging.info(eval_acc)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
