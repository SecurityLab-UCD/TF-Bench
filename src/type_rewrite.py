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
    return c + ((length - len(c)) * fill)

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
    parsed_code = code.split("\n")
    # Generate Abstract Syntax Tree
    ast = AST(code, HASKELL_LANGUAGE)
    root = ast.root
    # Get both types and type classes
    functions = ast.get_all_nodes_of_type(root, "variable")
    functions += (ast.get_all_nodes_of_type(root, "operator"))
    functions += (ast.get_all_nodes_of_type(root, "apply"))
    functions += (ast.get_all_nodes_of_type(root, "constructor"))

    # Find which ones need to be replaced (to prevent if type in in a word like IntToGet)
    for func_node in functions:
        func = ast.get_src_from_node(func_node)
        if func in func_dictionary:
            # Helper variables
            curr_line = parsed_code[func_node.start_point.row]
            start_col = func_node.start_point.column
            end_col = func_node.end_point.column
            # Replace Type at llocation with chr(0) as padding to keep positions accurate
            parsed_code[func_node.start_point.row] = curr_line[:start_col]
            + fill_space(func_dictionary[func], chr(0), len(func))
            + curr_line[end_col:]
    
    # Replace all the chr(0) characters with empty spaces
    return (("\n").join(parsed_code)).replace(chr(0), "")

def rewrite_functions(task: BenchmarkTask) -> BenchmarkTask:
    # Get all pieces of code together to determine all functions
    signatures = task.signature + "\n"
    if task.dependencies:
        signatures += ("\n").join(task.dependencies)

    # Generate Abstract Syntax Tree
    ast = AST(signatures, HASKELL_LANGUAGE)
    root = ast.root

    # Get only the function names called using function signatures
    functions = set(
        Chain(ast.get_all_nodes_of_type(root, "signature"))
        .map(ast.get_src_from_node)
        .map(lambda d: d[:d.index("::")].strip())
        .value
    )

    # Populate the dictionary with the corresponding types
    func_dictionary = {}
    curr = ord('p')
    for func in functions:
        func_dictionary[func] = chr(curr)
        curr += 1

    task.signature = replace_functions(task.signature, func_dictionary)
    task.code = replace_functions(task.code, func_dictionary)
    if task.dependencies:
        for i in range(len(task.dependencies)):
            task.dependencies[i] = replace_functions(task.dependencies[i], func_dictionary)
    return task
    


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

    # Populate the dictionary with the corresponding types
    type_dictionary = {}
    curr = ord('A')
    for type in types:
        type_dictionary[type] = chr(curr)
        curr += 1
    
    task.signature = replace_type(task.signature, type_dictionary)
    task.code = replace_type(task.code, type_dictionary)
    if task.dependencies:
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
    dataset_path: str = "data/source/Benchmark-F.json",
    output_path: str = "Benchmark-F.removed.json",
):
    with open(dataset_path, "r") as fp:
        tasks: list[BenchmarkTask] = (
            Chain(json.load(fp))
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .map(rewrite_type)
            .map(rewrite_functions)
            .value
        )
        totalTypeClassed = sum(has_type_class(task) for task in tasks)
        print("%d/%d tasks involved type classes" % (totalTypeClassed, len(tasks)))

    with open(output_path, "w") as fp:
        fp.write("\n".join(json.dumps(t.__dict__) for t in tasks))


if __name__ == "__main__":
    fire.Fire(main)
