import fire
import funcy
from funcy_chain import Chain
import logging
import json
from dacite import from_dict
from tfbench.common import extract_function_name
from tfbench.hs_parser import HASKELL_LANGUAGE
from tfbench.hs_parser.ast_util import AST
from tfbench.common import BenchmarkTask
from typing import Iterable


def build_dependency_dict(tasks: list[BenchmarkTask]) -> dict[str, str]:
    return {
        fn_name: t.signature
        for t in tasks
        if (fn_name := extract_function_name(t)) is not None
    }


def get_func_calls(task: BenchmarkTask) -> set[str]:
    """extract function calls and operators as string"""
    fn_name = extract_function_name(task)
    assert fn_name is not None

    ast = AST(task.code, HASKELL_LANGUAGE)
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
    inputs: list[list[str]] = (
        Chain(code.splitlines())
        .filter(lambda l: "=" in l)
        .map(lambda l: l.split("=")[0])
        .map(str.strip)
        .map(str.split)
        .value
    )
    return any(call in ii for ii in inputs)


def add_dependencies(dependency_dict: dict[str, str]):
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
