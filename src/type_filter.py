import os
import json
from tqdm import tqdm

def wrap_repo(s):
    # NOTE: this is a placeholder function
    # the implementation depends on how the repo is downloaded
    # please refer to HMTypes4Py repo
    return s


def filter_func_type(func: dict[str, str]) -> bool:
    return func['type'] in ['Monomorphic', 'Parametric']


def filter_functions(result_file_path: str) -> list[dict[str, str]]:
    with open(result_file_path, "r") as fp:
        all_functions = [json.loads(line) for line in fp]

    filtered_functions = list(filter(filter_func_type, all_functions))
    return filtered_functions


def main(
    input_repo_list_path: str = "data/meta/haskell.txt",
    source_root: str = "data/source/",
    output_root: str = "data/filtered"
):
    with open(input_repo_list_path) as fp:
        repo_id_list = [l.strip() for l in fp.readlines()]

    for repo_id in tqdm(repo_id_list):
        source_path = os.path.join(source_root, wrap_repo(repo_id) + ".jsonl")
        filtered_functions = filter_functions(source_path)
    
    output_file_path = os.path.join(output_root, wrap_repo(repo_id) + "_filtered.jsonl")
    with open(output_file_path, "w") as fp:
        for function in filtered_functions:
            json.dump(function, fp)
            fp.write('\n')

    print(f"Number of filtered functions: {len(filtered_functions)}")


if __name__ == "__main__":
    main()