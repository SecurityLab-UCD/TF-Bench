import fire
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from filter2complete import extract_function_name
import logging
from typing import Any
from add_dependency import BenchmarkTask
from funcy_chain import Chain
from dacite import from_dict


# Load the API key from enviroment variables
load_dotenv()
OPEN_API_KEY= os.getenv("OPENAI_API_KEY")


# Get the prompt for the OpenAI API
def get_prompt(task: BenchmarkTask) -> str:
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
    return prompt


# Call OpenAI API to generate type signature
def generate_type_signature(prompt: str) -> Any:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Act as a static analysis tool for type inference. Only output the type signature."},
            {"role": "user", "content": prompt}
        ],
        # Set parameters to ensure reproducibility
        seed = 123,
        temperature = 0.0,
        top_p = 1.0
    )

    return completion.choices[0].message.content


# Replace "[Char]" with "String" and remove the markdown symbols
def postprocess(result: str) -> str:
    return result.replace("[Char]", "String").replace("```haskell\n", "").replace("\n```", "")


def main(
    input_file: str = "data/filtered/base-4.20.0.0.jsonl",
    output_file: str = "data/experiment/gpt/base-4.20.0.0.jsonl",
):
    with open(input_file, "r") as file:
        results: list[str] = (
            Chain(file.readlines())
            .map(json.loads)
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .map(get_prompt)
            .map(generate_type_signature)
            .map(postprocess)
            .map(json.dumps)
            .value
        )

    with open(output_file, "w") as file:
        file.write("\n".join(results))        
    logging.info(
        f"Get {len(results)} results from GPT 3.5."
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
