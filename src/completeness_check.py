import fire
import json
import os
import logging
import sys
from enum import IntEnum
from funcy_chain import Chain
from pathos.multiprocessing import ProcessPool
from tqdm import tqdm


from src.hs_parser.ast_util import AST
from src.hs_parser import HASKELL_LANGUAGE
from returns.io import IOResult, IOSuccess, IOFailure
from returns.result import Success, Failure


class FilterErrorCode(IntEnum):
    FILE_NOT_FOUND = 0
    INVALID_CODE = 1


def is_valid_code(code_fragment: str) -> bool:
    try:
        ast = AST(code_fragment, HASKELL_LANGUAGE)
        return True  # If AST can be constructed without errors, code is valid
    except Exception as e:
        return False  # If any error occurs, code is invalid


def filter_code_entries(
    input_file: str, output_file: str
) -> IOResult[int, FilterErrorCode]:
    if not os.path.exists(input_file):
        return IOFailure(FilterErrorCode.FILE_NOT_FOUND)

    valid_entries = []
    with open(input_file, "r") as infile:
        for line in infile:
            entry = json.loads(line)
            code = entry.get("code", "")
            if is_valid_code(code):
                valid_entries.append(entry)

    if not valid_entries:
        return IOFailure(FilterErrorCode.INVALID_CODE)

    with open(output_file, "w") as outfile:
        for entry in valid_entries:
            json.dump(entry, outfile)
            outfile.write("\n")

    return IOSuccess(len(valid_entries))


def main(
    input_repo_list_path: str = "data/meta/haskell.txt",
    filtered_root: str = "data/filtered",
    complete_root: str = "data/complete",
):
    with open(input_repo_list_path) as fp:
        repo_id_list = [l.strip() for l in fp.readlines()]

    logging.info(f"Loaded {len(repo_id_list)} repos to be processed")
    num_valid_entries = 0
    failed = [0, 0]
    for repo_id in tqdm(repo_id_list):
        input_file = os.path.join(filtered_root, f"{repo_id}_filtered.jsonl")
        output_file = os.path.join(complete_root, f"{repo_id}_complete.jsonl")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        match filter_code_entries(input_file, output_file):
            case IOSuccess(Success(n)):
                num_valid_entries += n
            case IOFailure(Failure(error_code)):
                failed[error_code] += 1

    if sum(failed):
        failed_types = ["file not found", "invalid code"]
        failed_dict = {key: val for key, val in zip(failed_types, failed) if val != 0}
        logging.warning(f"Failed: {failed_dict}")
    logging.info(
        f"Filtered {num_valid_entries} valid code entries from {len(repo_id_list)} repositories."
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
