import fire
import os
import json
from dataset import wrap_repo
from filter2complete import extract_function_name
import logging
from typing import Any
from add_dependency import BenchmarkTask
from itertools import starmap
from dotenv import load_dotenv
from funcy_chain import Chain
from dacite import from_dict
from groq import Groq



load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key is None:
    raise ValueError("GROQ_API_KEY environment variable not set")

def get_prompt(task: BenchmarkTask) -> Any:
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
{fn_name}:: 
"""
    return prompt, fn_name

def generate_type_signature(prompt: str, fn_name:str ) -> Any:
    client = Groq(api_key=groq_api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content":
                "Act as a static analysis tool for type inference. Only output the type signature.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
        seed=123,
        temperature=0.0,
        top_p=1.0,
    )
    answer = chat_completion.choices[0].message.content
    if fn_name not in answer:
        answer = f"{fn_name} :: {answer}"

    return answer

def postprocess(result: str) -> str:
    return result.replace("[Char]", "String")

def main(
    input_file: str = "data/filtered/base-4.20.0.0.jsonl",
    output_file: str = "data/results/llama/base-4.20.0.0.jsonl"

):
    with open(input_file, "r") as fp:
        results: list[str] = (
            Chain(fp.readlines())
            .map(json.loads)
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .map(get_prompt)
            .value
        )

    prompts, fn_names = zip(*results)

    type_signatures = list(starmap(generate_type_signature, zip(prompts, fn_names)))

    final_results = list(map(postprocess, type_signatures))

    with open(output_file, "w") as out_fp:
        for result in final_results:
            out_fp.write(result + "\n")

    logging.info(
        f"Get {len(results)} results from LLAMA."
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
