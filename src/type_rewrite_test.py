import fire
import funcy
from funcy_chain import Chain
import logging
import json
from dacite import from_dict
from src.filter2complete import extract_function_name
from src.hs_parser import HASKELL_LANGUAGE
from src.hs_parser.ast_util import AST
from src.common import BenchmarkTask
from typing import Iterable
from pprint import pprint

def replace_type(code: str, type_dictionary: dict) -> str:
    parsed_code = code.split("\n")
    # Generate Abstract Syntax Tree
    ast = AST(code, HASKELL_LANGUAGE)
    root = ast.root
    # Get both types and type classes
    types_classes = ast.get_all_nodes_of_type(root, "name")

    # print(types_classes)

    # Find which ones need to be replaced (to prevent if type in in a word like IntToGet)
    for type_node in types_classes:
        type = ast.get_src_from_node(type_node)
        if type in type_dictionary:
            # Putting in chr(1) to indicate valid replacements
            curr_line = parsed_code[type_node.start_point.row]
            col = type_node.start_point.column
            parsed_code[type_node.start_point.row] = curr_line[:col] + "M" + curr_line[col + 1:]
    
    # Need to actually replace them here! TODO
    return ("\n").join(parsed_code)


def rewrite_type(task: BenchmarkTask) -> BenchmarkTask:
    # Get all pieces of code together to determine all types
    signatures = task.signature + "\n" + task.code + "\n"
    if task.dependencies:
        signatures += ("\n").join(task.dependencies)

    # Generate Abstract Syntax Tree
    ast = AST(signatures, HASKELL_LANGUAGE)
    root = ast.root

    # Get both types and type classes
    types_classes = (
        Chain(ast.get_all_nodes_of_type(root, "name"))
        .map(ast.get_src_from_node)
        .value
    )

    # Get only type classes
    applies = (
        Chain(ast.get_all_nodes_of_type(root, "apply"))
        .map(ast.get_src_from_node)
        .map(lambda d: d.split()[0])
        .value
    )

    # Filter out the type classes from both types and type classes
    types = (set(types_classes) - set(applies))
    # print(types)

    # Populate the dictionary with the corresponding types
    type_dictionary = {}
    curr = ord('A')
    for type in types:
        type_dictionary[type] = chr(curr)
        curr += 1
    
    task.signature = replace_type(task.signature, type_dictionary)

    print(task.signature)

    return task

def has_type_class(task: BenchmarkTask) -> bool:
    # Get all pieces of code together to determine all types
    signatures = task.signature + "\n"
    if task.dependencies:
        signatures += ("\n").join(task.dependencies)

    # Generate Abstract Syntax Tree
    ast = AST(signatures, HASKELL_LANGUAGE)
    root = ast.root

    # Get only type classes
    applies = (
        Chain(ast.get_all_nodes_of_type(root, "apply"))
        .map(ast.get_src_from_node)
        .map(lambda d: d.split()[0])
        .value
    )

    if len(applies) != 0:
        return True

    return False


def main(
    dataset_path: str = "data/source/Benchmark-F.jsonl",
    output_path: str = "Benchmark-F.removed.jsonl",
):
    ast = AST("chr :: Char -> Bool -> Int", HASKELL_LANGUAGE)
    root = ast.root

    calls = (
        Chain(ast.get_all_nodes_of_type(root, None))
        .map(lambda d: [d, ast.get_src_from_node(d)])
        .value
    )

    pprint(calls)
    # test = "lines :: String -> [String]"
    # # Generate Abstract Syntax Tree
    # ast = AST(test, HASKELL_LANGUAGE)
    # root = ast.root

    # # Get both types and type classes
    # types_classes = (
    #     Chain(ast.get_all_nodes_of_type(root, "name"))
    #     .map(ast.get_src_from_node)
    #     .value
    # )

    # # Get only type classes
    # applies = (
    #     Chain(ast.get_all_nodes_of_type(root, "apply"))
    #     .map(ast.get_src_from_node)
    #     .map(lambda d: d.split()[0])
    #     .value
    # )

    # # Filter out the type classes from both types and type classes
    # types = (set(types_classes) - set(applies))
    # # print(types)
    # print(types)
    # # Populate the dictionary with the corresponding types
    # type_dictionary = {}
    # curr = ord('A')
    # for type in types:
    #     type_dictionary[type] = chr(curr)

    
    # print(replace_type(test, type_dictionary))


if __name__ == "__main__":
    fire.Fire(main)
