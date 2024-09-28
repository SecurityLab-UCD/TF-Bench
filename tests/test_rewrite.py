from dacite import from_dict
from src.common import BenchmarkTask
from typing import Callable
from src.type_rewrite import (
    preprocess,
    manual_change,
    convert_upper_to_lower,
    remove_string_content,
    reverse_process,
    rewrite,
)
from src.postprocessing import postprocess


def test_rewrite():
    task_data = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromRational",
        "signature": "fromRational :: Rational -> a",
        "code": "fromRational (x:%y) =  fromInteger x % fromInteger y",
        "poly_type": "Parametric",
        "dependencies": [
            "(:%) :: a -> a -> Ratio a",
            "(%) :: Integral a => a -> a -> Ratio a",
            "fromInteger :: Num a => Integer -> a",
        ],
    }

    task = from_dict(data_class=BenchmarkTask, data=task_data)

    dependencies = task.dependencies if task.dependencies is not None else []
    signature = task.signature if task.signature is not None else ""
    code = task.code if task.code is not None else ""

    # put all code together
    combined_code = (
        "\n".join(dependencies)
        + "\n"
        + "-" * 20
        + "\n"
        + signature
        + "\n"
        + "-" * 20
        + "\n"
        + code
    )

    # process the raw code
    process_strategy: list[Callable[[str], str]] = [
        preprocess,
        manual_change,
        convert_upper_to_lower,
        remove_string_content,
        reverse_process,
    ]
    combined_code = postprocess(combined_code, process_strategy)

    rewritten_code = rewrite(combined_code)

    rewritten_parts = rewritten_code.split("\n" + "-" * 20 + "\n")
    task.dependencies = rewritten_parts[0].split("\n")
    task.signature = rewritten_parts[1]
    task.code = rewritten_parts[2]

    valid_result = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromRational",
        "signature": "f2::E -> a",
        "code": "f2 (v1:%v2) = f1 v1 % f1 v2",
        "poly_type": "Parametric",
        "dependencies": [
            "(:%)::a -> a -> A a",
            "(%)::B a => a -> a -> A a",
            "f1::C a => D -> a",
        ],
    }

    assert task.signature == valid_result["signature"]
    assert task.code == valid_result["code"]
    assert task.poly_type == valid_result["poly_type"]
    assert task.dependencies[0] == valid_result["dependencies"][0]


if __name__ == "__main__":
    test_rewrite()
