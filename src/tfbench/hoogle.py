# importing the requests library
from io import TextIOWrapper
import json
from functools import lru_cache
from urllib.parse import quote

import requests
from dacite import from_dict
import fire
from tree_sitter import Node
from funcy import lmap
from funcy_chain import Chain

from tfbench.common import BenchmarkTask, extract_function_name
from tfbench.hs_parser import AST
from tfbench.manual import MANUAL_TASKS


def get_all_first_child(ast: AST, node_type: str) -> list[Node]:
    """Extract the first nodes of a specific type"""
    children: list[Node] = lmap(
        lambda node: node.child(0), ast.get_all_nodes_of_type(ast.root, node_type)
    )
    return children


def generate_variable_banlist(code: str):
    """
    Generates list of variables that are already defined in the code
    """
    ast = AST(code)
    root = ast.root

    # Remove variables that are already defined in the code
    patterns = ast.get_all_nodes_of_type(root, "patterns")

    bindings = get_all_first_child(ast, "bind")

    generators = get_all_first_child(ast, "generator")

    alternatives = get_all_first_child(ast, "alternative")

    ban_list: list[str] = []
    for node in patterns + bindings + generators + alternatives:
        nodes = ast.get_all_nodes_of_type(node, "variable")
        ban_list += Chain(nodes).map(ast.get_src_from_node).value
        if node.type == "variable":
            ban_list += [ast.get_src_from_node(node)]

    return ban_list


def get_where_blacklist(task: BenchmarkTask) -> set[str]:
    """
    Generates ban list of any functions / variables defined by "where" keyword
    """
    # extract function calls and operators as string
    fn_name = extract_function_name(task)
    assert fn_name is not None
    where_index = task.code.index("where")
    where_code = task.code[(where_index + 5) :].strip()

    ast = AST(where_code)
    root = ast.root

    ban_list: list[str] = generate_variable_banlist(where_code)

    function_defs: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "function"))
        .map(lambda node: node.child(0))  # invoked function is the first child of apply
        .map(ast.get_src_from_node)
        .filter(lambda x: x != fn_name)
        .filter(lambda x: " " not in x)  # eliminate curried calls
        .value
    )

    return set(ban_list + function_defs)


def get_func_calls(task: BenchmarkTask) -> set[str]:
    """
    Get all the dependent functions of a Benchmark Task
    """
    # extract function calls and operators as string
    fn_name = extract_function_name(task)
    assert fn_name is not None
    print(f"Function: {fn_name}")

    ast = AST(task.code)
    root = ast.root

    variables: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "variable"))
        .map(ast.get_src_from_node)
        .filter(lambda x: x != fn_name)
        .filter(lambda x: " " not in x)  # eliminate curried calls
        .value
    )

    ban_list: list[str] = generate_variable_banlist(task.code)

    print(f"Banlist: {ban_list}")

    # Get any function calls, operator calls, or constructor operator calls
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

    const_operators: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "constructor_operator"))
        .map(ast.get_src_from_node)
        .map(lambda x: f"({x})")
        .value
    )

    # Put everything together and remove anything on the ban list
    final_list = set(calls + operators + variables + const_operators)

    final_list = final_list - set(ban_list)

    # Filter out any functions defined in the where clause
    if "where" in task.code:
        where_blacklist = get_where_blacklist(task)
        final_list = final_list - where_blacklist

    # Filter out some common non-function variables
    # 1. Single Letter variables and variations like s'' and x', etc.
    # 2. Any empty variables with nothing in them
    # 3. Common keywords like xs, ys, _, [], return, otherwise, (:)
    filtered_final_list = (
        Chain(final_list)
        .filter(lambda d: not (len(d.strip("'")) == 1 and d.strip("'").isalnum()))
        .filter(lambda d: len(d) != 0)
        .filter(
            lambda d: d not in ["(:)", "otherwise", "[]", "_", "xs", "ys", "return"]
        )
        .value
    )

    print(f"Dependents: {filtered_final_list}")

    return set(filtered_final_list)


def add_dependencies(task: BenchmarkTask, banned_fp: TextIOWrapper) -> BenchmarkTask:
    """
    Gets all dependent functions of a task with their corresponding type signatures
    If Hoogle cannot find a certain type signature, it sets dependencies to None
    """
    fn_name = extract_function_name(task)
    depedencies = list(get_func_calls(task))
    length = len(depedencies)
    type_signature = [""] * length
    for i in range(length):
        sig = get_type_signature(depedencies[i])
        # Check's conditions for invalid type signature
        # 1. If functions have same name
        # 2. If result exists
        # 3. If result is a type signature
        str_sig = str(sig)
        if (
            depedencies[i] == fn_name
            or sig is None
            or "::" not in str_sig
            or "data " in str_sig
        ):
            banned_fp.write(f"{fn_name}: '{depedencies[i]}'\n")
            print(f"Status: Invalid on '{depedencies[i]}'\n")
            task.dependencies = []
            # Otherwise remove the valid task
            return task
        # Change signature in List.foldr case
        if "newtype" not in str_sig and "data" not in str_sig:
            fname = str_sig.index("::")
            if str_sig[:fname].strip() != depedencies[i]:
                str_sig = depedencies[i] + " " + str_sig[fname:]
        # Set the type signature
        type_signature[i] = str_sig
    task.dependencies = list(set(type_signature))
    print("Status: Valid\n")
    return task


@lru_cache(maxsize=None)
def get_type_signature(name: str) -> str | None:
    """
    Gets the type signature given the name of the function
    Cached to improve efficiency
    """
    # Format using quote and strip
    url_string = quote(name.strip("()"))
    # api-endpoint
    url = f"https://hoogle.haskell.org?mode=json&format=text&hoogle={url_string}+is%3Aexact&start=1&count=1"

    # sending get request to get hoogle result
    r = requests.get(url=url, timeout=60)

    # extracting data in json format
    data = r.json()

    # Check if valid result was found, if there is one, return the type signature
    if len(data) > 0:
        return str(data[0]["item"])

    # If no valid result was found return None
    return None


def main(
    input_file: str = "Benchmark-F-copy.json",
    output_file: str = "out.json",
    banned_file: str = "banned.txt",
):
    """mean script for dependency-solving using Hoogle"""
    # For reading json files (Benchmark-F.json)
    with open(input_file, "r") as fp:
        tasks: Chain = Chain(json.load(fp)).map(
            lambda d: from_dict(data_class=BenchmarkTask, data=d)
        )

    # For reading jsonl files (base-4.20.0.0.jsonl)
    # with open(input_file, "r") as fp:
    #     tasks: list[BenchmarkTask] = (
    #         Chain(fp.readlines())
    #         .map(json.loads)
    #         .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
    #     )

    # Generate dependencies
    with open(banned_file, "w") as banned_fp:
        tasks_w_dep = tasks.map(lambda d: add_dependencies(d, banned_fp))

    # Remove any tasks with dependencies that could not be found
    # Also transform them back into dictionaries for json format
    filtered = (
        (tasks_w_dep)
        .filter(lambda d: d.dependencies is not None)
        .map(lambda x: x.__dict__)
        .value
    )

    print(
        f"Extracted {len(filtered)} / {len(tasks_w_dep.value)} functions from {input_file}"
    )

    with open(output_file, "w") as fp:
        json.dump(filtered + MANUAL_TASKS, fp)


if __name__ == "__main__":
    fire.Fire(main)
