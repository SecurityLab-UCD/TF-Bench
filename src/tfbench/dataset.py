"""main script to build Haskell dataset"""

from enum import IntEnum
import os
import logging
import json

import fire
from returns.result import Success, Failure
from returns.io import IOResult, IOSuccess, IOFailure
from funcy_chain import Chain
from tqdm import tqdm
from funcy import lmap

from tfbench.hs_parser import AST, HaskellFunction
from tfbench.hs_parser.type_util import get_polymorphic_type
from tfbench.common import remove_comments


def wrap_repo(s: str) -> str:
    """NOTE: this is a placeholder function"""
    return s


class CollectionErrorCode(IntEnum):
    REPO_NOT_FOUND = 0
    FUNC_NOT_FOUND = 1
    SKIPPED = 2


def collect_hs_files(root: str):
    """Get all files end with .hs in the given root directory

    Args:
        root (str): path to repo root
    """
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".hs") and os.path.isfile(
                p := os.path.join(dirpath, filename)
            ):
                yield p


def collect_from_file(file_path: str) -> list[dict[str, str]]:
    """extract benchmark tasks from a Haskell file"""
    with open(file_path, "r", errors="replace") as fp:
        code = fp.read()

    ast = AST(code)

    def _to_json(func: HaskellFunction) -> dict[str, str]:
        func_id = f"{file_path}--{ast.get_fn_name(func.type_signature).value_or(None)}"
        signature, code = ast.func2src(func)
        return {
            "task_id": func_id,
            "signature": remove_comments(signature),
            "code": remove_comments(code),
            "poly_type": get_polymorphic_type(func.type_signature),
        }

    fs: list[dict[str, str]] = lmap(_to_json, ast.get_functions())
    return fs


def collect_from_repo(
    repo_id: str, repo_root: str, source_root: str
) -> IOResult[int, CollectionErrorCode]:
    """Collect all tasks from a Haskell repository"""
    repo_path = os.path.join(repo_root, wrap_repo(repo_id))
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        return IOFailure(CollectionErrorCode.REPO_NOT_FOUND)

    source_path = os.path.join(source_root, wrap_repo(repo_id) + ".jsonl")

    # skip if already exist
    if os.path.exists(source_path):
        return IOFailure(CollectionErrorCode.SKIPPED)

    # collect potential functions
    all_functions = (
        Chain(collect_hs_files(repo_path))
        .mapcat(collect_from_file)
        .map(json.dumps)
        .value
    )

    if not all_functions:
        return IOFailure(CollectionErrorCode.FUNC_NOT_FOUND)

    # save to disk
    with open(source_path, "w") as fp:
        fp.write("\n".join(all_functions) + "\n")
    return IOSuccess(len(all_functions))


def main(
    input_repo_list_path: str = "data/meta/haskell.txt",
    repo_root: str = "data/repos",
    oroot: str = "data/source",
):
    """script to extract benchmark tasks from Haskell repositories"""
    with open(input_repo_list_path) as fp:
        repo_id_list = [line.strip() for line in fp.readlines()]

    logging.info(f"Loaded {len(repo_id_list)} repos to be processed")
    num_func = 0
    failed = [0, 0, 0]
    for repo in tqdm(repo_id_list):
        match collect_from_repo(repo, repo_root, oroot):
            case IOSuccess(Success(n)):
                num_func += n
            case IOFailure(Failure(status)):
                failed[status] += 1

    if sum(failed):
        failed_types = ["repo not found", "function not found", "skipped"]
        failed_dict = {key: val for key, val in zip(failed_types, failed) if val != 0}
        logging.warning(f"Failed: {failed_dict}")

    logging.info(
        f"Collected {num_func} functions from {len(repo_id_list)} repositories."
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(main)
