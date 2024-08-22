from dacite import from_dict
from src.common import BenchmarkTask
from tree_sitter import Language
import tree_sitter_haskell
from src.hs_parser.ast_util import AST
from src.type_rewrite import (
    extract_and_modify_operators,
    move_line_up_after_arrow,
    postprocess,
    process,
    preprocess,
    rewrite,
)


def test_rewrite():
    lang = Language(tree_sitter_haskell.language())
    task_data = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromRational",
        "signature": "fromRational :: Rational -> a",
        "code": "fromRational (x:%y) = fromInteger x % fromInteger y",
        "poly_type": "Parametric",
        "dependencies": [
            "fromInteger :: Integer -> a",
            "(%) :: (Integral a) => a -> a -> Ratio a",
        ],
    }
    task = from_dict(data_class=BenchmarkTask, data=task_data)

    code = (
        "\n".join(task.dependencies)
        + "\n"
        + "-" * 20
        + "\n"
        + task.signature
        + "\n"
        + "-" * 20
        + "\n"
        + task.code
    )

    # process the raw code
    code = extract_and_modify_operators(code)
    code = move_line_up_after_arrow(code)
    code = "\n".join(
        [postprocess(process(preprocess(line))) for line in code.split("\n")]
    )

    ast = AST(code, lang)
    assert ast.is_valid_code(), f"Error in the Process for this item"

    # print the rewritten code
    rewritten_code = rewrite(code)
    print("#" * 50)
    print("rewritten code:")
    print("#" * 50)
    print(rewritten_code)
    print("\n" * 2)

    ast = AST(rewritten_code, lang)
    assert ast.is_valid_code(), f"Error in the Rewrite for this item"


if __name__ == "__main__":
    test_rewrite()
