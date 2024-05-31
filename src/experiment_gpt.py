import fire
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from tqdm import tqdm
from dataset import wrap_repo
from filter2complete import extract_function_name
from returns.io import IOResult, IOSuccess, IOFailure
import logging


# Load the API key from enviroment variables
load_dotenv()
OPEN_API_KEY= os.getenv("OPENAI_API_KEY")


# Extract information for generating prompt
def extract_information(entry: dict) -> tuple[str, str, str]:
    task_id = entry["task_id"]
    func_name = extract_function_name(task_id)
    code = entry["code"]
    dependencies = entry["dependencies"]
    return func_name, code, dependencies


# Generate the prompt for the OpenAI API
def generate_prompt(entry: dict) -> str:
    func_name, code, dependencies = extract_information(entry)

    prompt = f"""
{code}

where
{dependencies}

--complete the following type signature for '{func_name}'
--if there is type mismatch, output 'Error'
{func_name}:: 
"""
    return prompt


# Call OpenAI API to generate type signature
def generate_type_signature(prompt: str, seed: int, temperature: float, top_p: float) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Act as a static analysis tool for type inference. Only output the type signature."},
            {"role": "user", "content": prompt}
        ],
        seed=seed,
        temperature=temperature,
        top_p=top_p
    )

    answer = completion.choices[0].message.content
    if not isinstance(answer, str):
        return TypeError("Expected a string response from the API.")
    
    return answer


# Replace '[Char]' with 'String' in the generated type signature
def replace_char_with_string(file_path: str) -> None:
    with open(file_path, "r") as file:
        content = file.read()

    content = content.replace("[Char]", "String")

    output_file_path = file_path.replace(".jsonl", "_replaced.jsonl")
    with open(output_file_path, "w") as file:
        file.write(content)


def main(
    input_repo_list_path: str = "data/meta/haskell.txt",
    source_root: str = "data/filtered/",
    output_root: str = "data/experiment/gpt",
):
    
    with open(input_repo_list_path) as fp:
        repo_id_list = [l.strip() for l in fp.readlines()]

    def to_jsonl_file_name(repo_id: str) -> str:
        file_name: str = wrap_repo(repo_id) + ".jsonl"
        return file_name

    for repo_id in tqdm(repo_id_list):
        source_path = os.path.join(source_root, to_jsonl_file_name(repo_id))
        output_path = os.path.join(output_root, to_jsonl_file_name(repo_id))

        with open(source_path, "r") as file:
            dataset = [json.loads(line) for line in file]
        
        logging.info(f"Loaded {len(dataset)} functions to be processed")

        with open(output_path, "w") as file:
            file.write("")
        
        # Set parameters to ensure reproducibility
        seed: int = 123
        temperature: float = 0.0
        top_p: float = 1.0

        num_ans = 0
        num_err = 0
        for entry in tqdm(dataset):
            prompt = generate_prompt(entry)
            answer = generate_type_signature(prompt, seed, temperature, top_p)
            
            with open(output_path, "a") as file:
                file.write(answer + "\n")

            match answer:
                case 'Error':
                    num_err += 1
                case _:
                    num_ans += 1
 
        replace_char_with_string(output_path)
            
        logging.info(
            f"Get {num_ans} answers and {num_err} 'Error' from {len(dataset)} functions."
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
