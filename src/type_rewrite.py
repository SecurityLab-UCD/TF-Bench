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

def fill_space(c: str, fill: str, length: int) -> str:
    return c + ((length - 1) * fill)

def replace_type(code: str, type_dictionary: dict) -> str:
    parsed_code = code.split("\n")
    # Generate Abstract Syntax Tree
    ast = AST(code, HASKELL_LANGUAGE)
    root = ast.root
    # Get both types and type classes
    types_classes = ast.get_all_nodes_of_type(root, "name")

    # Find which ones need to be replaced (to prevent if type in in a word like IntToGet)
    for type_node in types_classes:
        type = ast.get_src_from_node(type_node)
        if type in type_dictionary:
            # Helper variables
            curr_line = parsed_code[type_node.start_point.row]
            start_col = type_node.start_point.column
            end_col = type_node.end_point.column
            # Replace Type at llocation with chr(0) as padding to keep positions accurate
            parsed_code[type_node.start_point.row] = curr_line[:start_col] + fill_space(type_dictionary[type], chr(0), len(type)) + curr_line[end_col:]
    
    # Replace all the chr(0) characters with empty spaces
    return (("\n").join(parsed_code)).replace(chr(0), "")

def replace_functions(code: str, func_dictionary: dict) -> str:
    pass

def rewrite_functions(task: BenchmarkTask) -> BenchmarkTask:
    # Get all pieces of code together to determine all functions
    signatures = task.signature + "\n"
    if task.dependencies:
        signatures += ("\n").join(task.dependencies)

    # Generate Abstract Syntax Tree
    ast = AST(signatures, HASKELL_LANGUAGE)
    root = ast.root

    # Get both types and type classes
    functions = set(
        Chain(ast.get_all_nodes_of_type(root, "variable"))
        .map(ast.get_src_from_node)
        .value
    )

    # Populate the dictionary with the corresponding types
    func_dictionary = {}
    curr = ord('a')
    for func in functions:
        func_dictionary[func] = chr(curr)
        curr += 1

    


def rewrite_type(task: BenchmarkTask) -> BenchmarkTask:
    # New commit for merging purposes
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
    task.code = replace_type(task.code, type_dictionary)
    for i in range(len(task.dependencies)):
        task.dependencies[i] = replace_type(task.dependencies[i], type_dictionary)

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
    # ast = AST("chr :: Char -> Bool -> Int", HASKELL_LANGUAGE)
    # root = ast.root

    # calls = (
    #     Chain(ast.get_all_nodes_of_type(root, "name"))
    #     .map(ast.get_src_from_node)
    #     .value
    # )

    # print(calls)
    with open(dataset_path, "r") as fp:
        tasks: list[BenchmarkTask] = (
            Chain(json.loads(fp.read()))
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .map(rewrite_type)
            .value
        )
        totalTypeClassed = sum(has_type_class(task) for task in tasks)
        # print(totalTypeClassed)
        # print(len(tasks))

    with open(output_path, "w") as fp:
        fp.write("\n".join(json.dumps(t.__dict__) for t in tasks))


if __name__ == "__main__":
    fire.Fire(main)
