import json
from typing import Iterable

import fire
from funcy_chain import Chain
from dacite import from_dict

from tfbench.common import extract_function_name
from tfbench.hs_parser import AST
from tfbench.common import BenchmarkTask


def build_dependency_dict(tasks: list[BenchmarkTask]) -> dict[str, str]:
    """dependency mapping from function names to their signatures"""
    return {
        fn_name: t.signature
        for t in tasks
        if (fn_name := extract_function_name(t)) is not None
    }


def get_func_calls(task: BenchmarkTask) -> set[str]:
    """extract function calls and operators as string"""
    fn_name = extract_function_name(task)
    assert fn_name is not None

    ast = AST(task.code)
    root = ast.root

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

    return set(calls + operators)


def _is_input(code: str, call: str) -> bool:
    """check if a function call is an input to the task"""
    inputs: list[list[str]] = (
        Chain(code.splitlines())
        .filter(lambda line: "=" in line)
        .map(lambda line: line.split("=")[0])
        .map(str.strip)
        .map(str.split)
        .value
    )
    return any(call in ii for ii in inputs)


def add_dependencies(dependency_dict: dict[str, str]):
    """add dependencies to benchmark tasks"""

    def add_for_task(task: BenchmarkTask) -> BenchmarkTask:
        calls: Iterable[str] = get_func_calls(task)
        calls = filter(lambda c: not _is_input(task.code, c), calls)
        task.dependencies = [dependency_dict[f] for f in calls if f in dependency_dict]
        return task

    return add_for_task


def main(
    input_file: str = "data/source/base-4.20.0.0.jsonl",
    output_file: str = "out.jsonl",
):
    """add dependency to a task json file"""
    with open(input_file, "r") as fp:
        tasks: list[BenchmarkTask] = (
            Chain(fp.readlines())
            .map(json.loads)
            .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
            .value
        )

    dependency_dict = build_dependency_dict(tasks)
    tasks_w_dep = (
        Chain(tasks)
        .map(add_dependencies(dependency_dict))
        .map(lambda x: x.__dict__)
        .map(json.dumps)
        .value
    )
    with open(output_file, "w") as fp:
        fp.write("\n".join(tasks_w_dep))


if __name__ == "__main__":
    fire.Fire(main)
