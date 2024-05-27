import os
import json
from tqdm import tqdm
import fire

def extract_function_name(id_str):
    """Extract the function name from the id field."""
    if "--" in id_str:
        return id_str.split("--")[-1].strip()
    return None

def is_valid_entry(entry):
    """Check if the entry is valid based on the criteria."""
    func_name = extract_function_name(entry.get("id", ""))
    code = entry.get("code", "")
    return func_name and code.startswith(f"{func_name} ::")

def filter_functions(input_file):
    """Filter valid entries from a JSONL file."""
    filtered_entries = []
    with open(input_file, 'r') as infile:
        for line in infile:
            entry = json.loads(line)
            if is_valid_entry(entry):
                filtered_entries.append(entry)
    return filtered_entries

def wrap_repo(repo_id):
    """Wraps the repository ID for consistent file naming."""
    return repo_id.replace("/", "_")

def main(
    input_repo_list_path: str = "data/meta/haskell.txt",
    filter_root: str = "data/filtered/",
    output_root: str = "data/complete/"
):
    with open(input_repo_list_path) as fp:
        repo_id_list = [l.strip() for l in fp.readlines()]

    for repo_id in tqdm(repo_id_list):
        input_file_path = os.path.join(filter_root, wrap_repo(repo_id) + "_filtered.jsonl")
        filtered_functions = filter_functions(input_file_path)
    
        output_file_path = os.path.join(output_root, wrap_repo(repo_id) + "_complete.jsonl")
        with open(output_file_path, "w") as fp:
            for function in filtered_functions:
                json.dump(function, fp)
                fp.write('\n')

        print(f"Filtered {len(filtered_functions)} correct functions for repo: {repo_id}")

if __name__ == "__main__":
    fire.Fire(main)
