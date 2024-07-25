# importing the requests library
from src.hs_parser.ast_util import AST
import json
from dacite import from_dict
import fire
from funcy_chain import Chain
import requests
from urllib.parse import quote
from src.common import BenchmarkTask
from src.filter2complete import extract_function_name
from src.hs_parser import HASKELL_LANGUAGE
from functools import lru_cache
from tree_sitter import Node
# Need to update requirements.txt

def get_func_calls(task: BenchmarkTask) -> set[str]:
    """extract function calls and operators as string"""
    fn_name = extract_function_name(task.task_id)
    assert fn_name is not None

    ast = AST(task.code, HASKELL_LANGUAGE)
    root = ast.root

    variables: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "variable"))
        .map(ast.get_src_from_node)
        .filter(lambda x: x != fn_name)
        .filter(lambda x: " " not in x)  # eliminate curried calls
        .value
    )
    # Idea, Need some way of getting only variables that are functions to be called
    # Also these functions need to be valid
    patterns: list[Node] = (
        Chain(ast.get_all_nodes_of_type(root, "patterns"))
        .value
    )

    bindings: list[Node] = (
        Chain(ast.get_all_nodes_of_type(root, "bind"))
        .map(lambda node: node.child(0))  # variable is first child of binding
        .value
    )

    generators: list[Node] = (
        Chain(ast.get_all_nodes_of_type(root, "generator"))
        .map(lambda node: node.child(0))  # variable is first child of binding
        .value
    )

    ban_list: list[str] = []
    for node in (patterns + bindings + generators):
        nodes = ast.get_all_nodes_of_type(node, "variable")
        ban_list += Chain(nodes).map(ast.get_src_from_node).value
        if node.type == "variable":
            ban_list += [ast.get_src_from_node(node)]

    print(ban_list)

    calls: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "apply"))
        .map(lambda node: node.child(0))  # invoked function is the first child of apply
        .map(ast.get_src_from_node)
        .filter(lambda x: x != fn_name)
        .filter(lambda x: " " not in x)  # eliminate curried calls
        .value
    )

    operators: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "operator"))
        .map(ast.get_src_from_node)
        .map(lambda x: f"({x})")  # infix operator . \equiv function (.)
        .filter(lambda x: x != fn_name)
        .value
    )

    final_list = (set(calls + operators + variables) - set(ban_list))

    filtered_final_list = (Chain(final_list)
    .filter(lambda d: not (len(d) == 1 and d.isalnum()))
    .filter(lambda d: d != "xs")
    .value)

    return filtered_final_list

def add_dependencies(task: BenchmarkTask)-> BenchmarkTask:
    depedencies = list(get_func_calls(task))
    length = len(depedencies)
    type_signature = [""] * length
    for i in range(length):
        sig = get_type_signature(depedencies[i])
        # Check type signature exists
        if sig == None:
            task.dependencies = None
            # Otherwise remove the valid task
            return task
        # Check if result is a type signature
        str_sig = str(sig)
        if "::" not in str_sig or "data " in str_sig:
            # Otherwise remove it as a valid task
            task.dependencies = None
            return task
        type_signature[i] = str_sig
    task.dependencies = type_signature
    return task

@lru_cache(maxsize=None)
def get_type_signature(name: str) -> str | None:
    # api-endpoint
    URL = "https://hoogle.haskell.org?mode=json&format=text&hoogle={0}+is%3Aexact&start=1&count=1".format(quote(name))

    # sending get request to get hoogle result
    r = requests.get(url = URL)
    
    # extracting data in json format
    data = r.json()

    type_signature = None

    # Check if valid result was found, if there is one, return the type signature
    if len(data) > 0:
        type_signature = data[0]["item"]
    
    return type_signature

def main(
    input_file: str = "Benchmark-F.json",
    output_file: str = "outv3.json",
):
    # For json files
    with open(input_file, "r") as fp:
        tasks: list[BenchmarkTask] = (
            Chain(json.load(fp))
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .value
        )

    # For jsonl files
    # with open(input_file, "r") as fp:
    #     tasks: list[BenchmarkTask] = (
    #         Chain(fp.readlines())
    #         .map(json.loads)
    #         .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
    #         .value
    #     )

    tasks_w_dep = (
        Chain(tasks)
        .map(add_dependencies)
        .value
    )

    filtered = (
        Chain(filter(lambda d: d.dependencies != None, tasks_w_dep))
        .map(lambda x: x.__dict__)
        .value
    )

    print(len(filtered))

    with open(output_file, "w") as fp:
        json.dump(filtered, fp)
    
if __name__ == "__main__":
    fire.Fire(main)