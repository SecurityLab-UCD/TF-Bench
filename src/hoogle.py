# importing the requests library
from io import TextIOWrapper
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
from funcy import lmap
# Need to update requirements.txt

def get_where_blacklist(task: BenchmarkTask) -> set[str]:
    """extract function calls and operators as string"""
    fn_name = extract_function_name(task.task_id)
    assert fn_name is not None
    where_index = task.code.index("where")
    where_code = task.code[(where_index + 5):].strip()

    ast = AST(where_code, HASKELL_LANGUAGE)
    root = ast.root

    # Idea, Need some way of getting only variables that are functions to be called
    # Also these functions need to be valid
    # Remove variables that are already defined to leave only functions that need dependencies
    patterns: list[Node] = ast.get_all_nodes_of_type(root, "patterns")

    bindings: list[Node] = lmap(lambda node: node.child(0), ast.get_all_nodes_of_type(root, "bind"))

    generators: list[Node] = lmap(lambda node: node.child(0), ast.get_all_nodes_of_type(root, "generator"))

    alternatives: list[Node] = lmap(lambda node: node.child(0), ast.get_all_nodes_of_type(root, "alternative"))

    function_defs: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "function"))
        .map(lambda node: node.child(0))  # invoked function is the first child of apply
        .map(ast.get_src_from_node)
        .filter(lambda x: x != fn_name)
        .filter(lambda x: " " not in x)  # eliminate curried calls
        .value
    )

    ban_list: list[str] = []
    for node in (patterns + bindings + generators + alternatives):
        nodes = ast.get_all_nodes_of_type(node, "variable")
        ban_list += Chain(nodes).map(ast.get_src_from_node).value
        if node.type == "variable":
            ban_list += [ast.get_src_from_node(node)]

    return set(ban_list + function_defs)

    

def get_func_calls(task: BenchmarkTask) -> set[str]:
    """extract function calls and operators as string"""
    fn_name = extract_function_name(task.task_id)
    assert fn_name is not None
    print(f"Function: {fn_name}")

    ast = AST(task.code, HASKELL_LANGUAGE)
    root = ast.root

    variables: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "variable"))
        .map(ast.get_src_from_node)
        .filter(lambda x: x != fn_name)
        .filter(lambda x: " " not in x)  # eliminate curried calls
        .value
    )
    # Remove variables that are already defined to leave only functions that need dependencies
    patterns: list[Node] = ast.get_all_nodes_of_type(root, "patterns")

    bindings: list[Node] = lmap(lambda node: node.child(0), ast.get_all_nodes_of_type(root, "bind"))

    generators: list[Node] = lmap(lambda node: node.child(0), ast.get_all_nodes_of_type(root, "generator"))

    alternatives: list[Node] = lmap(lambda node: node.child(0), ast.get_all_nodes_of_type(root, "alternative"))

    ban_list: list[str] = []
    for node in (patterns + bindings + generators + alternatives):
        nodes = ast.get_all_nodes_of_type(node, "variable")
        ban_list += Chain(nodes).map(ast.get_src_from_node).value
        if node.type == "variable":
            ban_list += [ast.get_src_from_node(node)]
    # End of Generating Ban List

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

    # Filter out some common non-important variables patterns
    # 1. Single Letter variables and variations like s'' and x', etc.
    # 2. Any empty variables with nothing in them
    # 3. Common keywords like xs, ys, _, [], return, otherwise, (:)
    filtered_final_list = (Chain(final_list)
    .filter(lambda d: not (len(d.strip("'")) == 1 and d.strip("'").isalnum()))
    .filter(lambda d: not (len(d) == 0))
    .filter(lambda d: d not in ["(:)", "otherwise", "[]", "_", "xs", "ys", "return"])
    .value)

    print(f"Dependents: {filtered_final_list}")

    return set(filtered_final_list)

def add_dependencies(task: BenchmarkTask, banned_fp: TextIOWrapper)-> BenchmarkTask:
    fn_name = extract_function_name(task.task_id)
    depedencies = list(get_func_calls(task))
    length = len(depedencies)
    type_signature = [""] * length
    for i in range(length):
        sig = get_type_signature(depedencies[i])
        # Check if functions have same name
        # Check type signature exists
        # Check if result is a type signature
        str_sig = str(sig)
        if (depedencies[i] == fn_name or sig == None
            or "::" not in str_sig or "data " in str_sig):
            banned_fp.write(f"{fn_name}: '{depedencies[i]}'\n")
            print(f"Status: Invalid on '{depedencies[i]}'\n")
            task.dependencies = None
            # Otherwise remove the valid task
            return task
        # Change signature in List.foldr case
        fname = str_sig.index("::")
        if str_sig[:fname].strip() != depedencies[i]:
            str_sig = depedencies[i] + " " + str_sig[fname:]
        # Set the type signature
        type_signature[i] = str_sig
    task.dependencies = list(set(type_signature))
    print(f"Status: Valid\n")
    return task

@lru_cache(maxsize=None)
def get_type_signature(name: str) -> str | None:
    # Format using quote and strip
    url_string = quote(name.strip("()"))
    # api-endpoint
    URL = f"https://hoogle.haskell.org?mode=json&format=text&hoogle={url_string}+is%3Aexact&start=1&count=1"

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
    output_file: str = "outv5.json",
    banned_file: str = "banned.txt"
):
    banned_fp = open(banned_file, "w")
    # For json files
    with open(input_file, "r") as fp:
        tasks: Chain = (
            Chain(json.load(fp))
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
        )

    # For jsonl files
    # with open(input_file, "r") as fp:
    #     tasks: list[BenchmarkTask] = (
    #         Chain(fp.readlines())
    #         .map(json.loads)
    #         .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
    #     )

    tasks_w_dep = tasks.map(lambda d: add_dependencies(d, banned_fp))

    filtered = (
        (tasks_w_dep)
        .filter(lambda d: d.dependencies != None)
        .map(lambda x: x.__dict__)
        .value
    )

    print(f"Extracted {len(filtered)} / {len(tasks_w_dep.value)} functions from {input_file}")

    with open(output_file, "w") as fp:
        json.dump(filtered, fp)
    
if __name__ == "__main__":
    fire.Fire(main)