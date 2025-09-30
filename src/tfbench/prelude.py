import json
from os.path import join as pjoin, abspath, exists

import fire
from funcy import lmap
from funcy_chain import Chain
from dacite import from_dict

from tfbench.hs_parser import AST
from tfbench.add_dependency import add_dependencies
from tfbench.common import clean_tab_spaces, BenchmarkTask, task2md


def main(
    prelude: str = "data/repos/base-4.20.0.0/src/Prelude.hs",
    ghc_internal: str = "data/source/ghc-internal-9.1001.0.jsonl",
    output_dir: str = "benchmark",
):
    """extract tasks from Haskell prelude"""
    ghc_internal = abspath(ghc_internal)
    prelude = abspath(prelude)
    assert exists(ghc_internal) and exists(prelude)

    with open(prelude, "r") as fp:
        prelude_code = fp.read()

    ast = AST(prelude_code)
    root = ast.root
    prelude_vars = lmap(
        ast.get_src_from_node, ast.get_all_nodes_of_type(root, "variable")
    )
    prelude_operators = (
        Chain(ast.get_all_nodes_of_type(root, "operator"))
        .map(ast.get_src_from_node)
        .map(lambda op: f"({op})")
        .value
    )
    prelude_functions = prelude_vars + prelude_operators
    with open(ghc_internal, "r") as fp:
        ghc_internal_functions = lmap(json.loads, fp.read().splitlines())

    ghc_internal_dict = {
        fn_name: f
        for f in ghc_internal_functions
        if (fn_name := f["task_id"].split("--")[-1].strip()) is not None
    }

    dependency_dict = {k: v["signature"] for k, v in ghc_internal_dict.items()}

    tasks_w_dep = (
        Chain(prelude_functions)
        .filter(lambda f: f in ghc_internal_dict)
        .map(lambda f: ghc_internal_dict[f])
        .filter(lambda t: t["code"] != "")
        .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
        .map(add_dependencies(dependency_dict))
        .map(clean_tab_spaces)
        .value
    )

    print(f"Collected {len(tasks_w_dep)} for the benchmark.")

    for i, t in enumerate(tasks_w_dep):
        md_path = pjoin(output_dir, f"task_{i}.core.md")
        with open(md_path, "w") as fp:
            fp.write(task2md(t))


if __name__ == "__main__":
    fire.Fire(main)
