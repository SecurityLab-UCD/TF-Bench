import json
import fire
import os
from os.path import join as pjoin, abspath, exists
from funcy import lmap
from funcy_chain import Chain
from dacite import from_dict

from src.hs_parser import HASKELL_LANGUAGE
from src.hs_parser.ast_util import AST
from src.common import extract_function_name
from src.add_dependency import add_dependencies
from src.common import clean_tab_spaces, BenchmarkTask


def main(
    prelude: str = "data/repos/base-4.20.0.0/src/Prelude.hs",
    ghc_internal: str = "data/source/ghc-internal-9.1001.0.jsonl",
    output_file: str = "Benchmark-F.json",
):
    ghc_internal = abspath(ghc_internal)
    prelude = abspath(prelude)
    assert exists(ghc_internal) and exists(prelude)

    with open(prelude, "r") as fp:
        prelude_code = fp.read()

    ast = AST(prelude_code, HASKELL_LANGUAGE)
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
        if (fn_name := extract_function_name(f["task_id"])) is not None
    }

    dependency_dict = {k: v["signature"] for k, v in ghc_internal_dict.items()}

    tasks_w_dep = (
        Chain(prelude_functions)
        .filter(lambda f: f in ghc_internal_dict)
        .map(lambda f: ghc_internal_dict[f])
        .filter(lambda t: t["code"] != "")
        .map(lambda d: from_dict(data_class=BenchmarkTask, data=d))
        .filter(lambda t: t.poly_type in ["Monomorphic", "Parametric"])
        .filter(lambda t: "Generics.hs" not in t.task_id) # Some functions in Generics.hs are mis-classified in the previous step
        .map(add_dependencies(dependency_dict))
        .map(clean_tab_spaces)
        .map(lambda x: x.__dict__)
        .value
    )

    print(f"Collected {len(tasks_w_dep)} for the benchmark.")

    with open(output_file, "w") as fp:
        json.dump(tasks_w_dep, fp)


if __name__ == "__main__":
    fire.Fire(main)
