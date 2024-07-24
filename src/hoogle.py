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

def get_func_calls(task: BenchmarkTask) -> set[str]:
    """extract function calls and operators as string"""
    fn_name = extract_function_name(task.task_id)
    assert fn_name is not None

    ast = AST(task.code, HASKELL_LANGUAGE)
    root = ast.root

    calls: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "apply"))
        .map(lambda node: node.child(0))  # invoked function is the first child of apply
        .map(ast.get_src_from_node)
        .filter(lambda x: x != fn_name)
        .filter(lambda x: " " not in x)  # eliminate curried calls
        .filter(lambda x: x != "f" and x != "g")
        .value
    )

    operators: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "operator"))
        .map(ast.get_src_from_node)
        .map(lambda x: f"({x})")  # infix operator . \equiv function (.)
        .filter(lambda x: x != fn_name)
        .filter(lambda x: x != "f" and x != "g")
        .value
    )

    return set(calls + operators)

def add_dependencies(task: BenchmarkTask)-> BenchmarkTask:
    depedencies = list(get_func_calls(task))
    length = len(depedencies)
    type_signature = [None] * length
    for i in range(length):
        type_signature[i] = get_type_signature(depedencies[i])
        if type_signature[i] == None:
            task.dependencies = [None]
            return task
    task.dependencies = type_signature
    return task

@lru_cache(maxsize=None)
def get_type_signature(name: str) -> str:
    # api-endpoint
    URL = "https://hoogle.haskell.org?mode=json&format=text&hoogle={0}&start=1&count=1".format(quote(name))

    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    
    # extracting data in json format
    data = r.json()

    type_signature = None

    if len(data) > 0:
        type_signature = data[0]["item"]
    
    return type_signature

def main(
    input_file: str = "data/source/Benchmark-F.json",
    output_file: str = "out.json",
):
    with open(input_file, "r") as fp:
        tasks: list[BenchmarkTask] = (
            Chain(json.load(fp))
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .value
        )

    tasks_w_dep = (
        Chain(tasks)
        .map(add_dependencies)
        .value
    )

    filtered = (
        Chain(filter(lambda d: d.dependencies != [None], tasks_w_dep))
        .map(lambda x: x.__dict__)
        .value
    )

    with open(output_file, "w") as fp:
        json.dump(filtered, fp)
    
if __name__ == "__main__":
    fire.Fire(main)