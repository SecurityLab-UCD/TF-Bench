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

import urllib.request
import ssl

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
    api_key,
    url,
    model: str = "meta-llama-3-8b-4",
    seed=123,
    temperature=0.0,
    top_p=1.0,
):
    def generate_type_signature(prompt_list:list[str]) -> list[str] | None:
        data = {
            "input_data": prompt_list,
            "params": {
                "temperature": temperature,
                "top_p": top_p,
                "seed": seed,
            }
        }
        
        body = str.encode(json.dumps(data))
        
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': model }
        req = urllib.request.Request(url, body, headers)
        
        response = urllib.request.urlopen(req)
        result = response.read()
        # Decode the byte string to a regular string
        result_decoded = result.decode('utf-8')
        
        # Convert the string representation of a list to a Python list
        result_list = json.loads(result_decoded)
        
        return result_list
    
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
    model: str = "meta-llama-3-8b-4",
    api_key: str | None = None,
    url: str | None = None,
    seed: int = 123,
    temperature: float = 0.0,
    top_p: float = 1.0,
):
    assert model in ["meta-llama-3-8b-4"], f"{model} is not supported."
    assert api_key is not None, "API key is not provided."
    assert url is not None, "API key is not provided."

    # Setup the function to call the API
    generate = get_model(api_key, url, model, seed, temperature, top_p)

    with open(input_file, "r") as file:
        # Read all tasks and convert them to BenchmarkTask objects
        tasks = [from_dict(data_class=BenchmarkTask, data=json.loads(line)) for line in file]
        
        # Generate prompts for all tasks
        prompts = [SYSTEM_PROMPT + '\n' + get_prompt(task) for task in tasks]

        # Generate type signatures for all prompts at once
        results = generate(prompts)  # generate now receives a list of prompts
        
        # Postprocess and save results
        processed_results = [postprocess(result) for result in results if result is not None]
        with open(output_file, "w") as outfile:
            for result in processed_results:
                outfile.write(json.dumps(result) + "\n")
                
    logging.info(f"Get {len(results)} results from {model}.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
