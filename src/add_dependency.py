import fire
import funcy
from funcy_chain import Chain
import logging
import json
from dacite import from_dict
from dataclasses import dataclass
from src.filter2complete import extract_function_name
from src.hs_parser import HASKELL_LANGUAGE
from src.hs_parser.ast_util import AST
from src.hs_parser.ast_util import ASTLoc
import pprint


@dataclass
class BenchmarkTask:
    task_id: str
    signature: str
    code: str
    poly_type: str
    dependencies: str | None


def build_dependency_dict(tasks: list[BenchmarkTask]) -> dict[str, str]:
    return {
        fn_name: t.signature
        for t in tasks
        if (fn_name := extract_function_name(t.task_id)) is not None
    }


def get_func_calls(task: BenchmarkTask) -> set[str]:
    """extract function calls and operators as string"""
    fn_name = extract_function_name(task.task_id)
    assert fn_name is not None

    ast = AST(task.code, HASKELL_LANGUAGE)
    root = ast.root

    calls: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "variable"))
        .map(ast.get_src_from_node)
        .filter(lambda x: x != fn_name)
        .value
    )
    operators: list[str] = (
        Chain(ast.get_all_nodes_of_type(root, "operator"))
        .map(ast.get_src_from_node)
        .map(lambda x: f"({x})")  # infix operator . \equiv function (.)
        .value
    )

    return set(calls + operators)


def add_dependencies(dependency_dict: dict[str, str]):
    def add_for_task(task: BenchmarkTask) -> BenchmarkTask:
        calls = get_func_calls(task)
        type_deps = [dependency_dict[f] for f in calls if f in dependency_dict]
        task.dependencies = "\n".join(type_deps)
        return task

    return add_for_task

# Takes global location (original location in file) and the local location of some position in reference to the global position and returns the global position of the local location
def local_to_global_loc(global_root_loc: ASTLoc, local_loc: ASTLoc):
    # Check if lines are the same
    if(local_loc.lineno == 1):
        return ASTLoc(lineno = global_root_loc.lineno, 
                    col = global_root_loc + local_loc.col - 1)
    else:
        return ASTLoc(lineno = global_root_loc.lineno + local_loc.lineno - 1, 
                    col = local_loc.col)

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
    
    # Test value of open
    # pprint.pprint(list(map(lambda d: d.keys(), tasks)))

    dependency_dict = build_dependency_dict(tasks)
    tasks_w_dep = (
        Chain(tasks)
        .map(add_dependencies(dependency_dict))
        .map(lambda x: x.__dict__)
        .map(json.dumps)
        .value
    )

    # with open(output_file,"w") as fp:
    #     fp.write(tasks)

    with open(output_file, "w") as fp:
        fp.write("\n".join(tasks_w_dep))


if __name__ == "__main__":
    fire.Fire(main)
