import fire
import os
import json
from tqdm import tqdm
from dataset import wrap_repo
import logging


def is_valid_func_type(func: dict[str, str]) -> bool:
    return func["poly_type"] in ["Monomorphic", "Parametric"]


def filter_functions(result_file_path: str) -> list[dict[str, str]]:
    with open(result_file_path, "r") as fp:
        all_functions = [json.loads(line) for line in fp]

    filtered_functions = list(filter(is_valid_func_type, all_functions))
    return filtered_functions


def main(
    input_repo_list_path: str = "data/meta/haskell.txt",
    source_root: str = "data/source/",
    output_root: str = "data/filtered/",
):
    with open(input_repo_list_path) as fp:
        repo_id_list = [l.strip() for l in fp.readlines()]

    def to_jsonl_file_name(repo_id: str) -> str:
        file_name: str = wrap_repo(repo_id) + ".jsonl"
        return file_name

    # todo: parallelize this if we move on to multiple repos
    for repo_id in tqdm(repo_id_list):
        source_path = os.path.join(source_root, to_jsonl_file_name(repo_id))
        output_file_path = os.path.join(output_root, to_jsonl_file_name(repo_id))
        filtered_functions = filter_functions(source_path)

        with open(output_file_path, "w") as fp:
            for function in filtered_functions:
                json.dump(function, fp)
                fp.write("\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
