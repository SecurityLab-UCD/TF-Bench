from dacite import from_dict
from src.common import BenchmarkTask
from src.type_rewrite import (
    rewrite,
    extract_and_modify_operators,
    preprocess,
    process,
    postprocess,
)


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
    combined_code = extract_and_modify_operators(combined_code)

    combined_code = "\n".join(
        [postprocess(process(preprocess(line))) for line in combined_code.split("\n")]
    )

    rewritten_code = rewrite(combined_code)

    rewritten_parts = rewritten_code.split("\n" + "-" * 20 + "\n")
    task.dependencies = rewritten_parts[0].split("\n")
    task.signature = rewritten_parts[1]
    task.code = rewritten_parts[2]

    valid_result = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromRational",
        "signature": "f4 :: v3 -> v1",
        "code": "f4 (f9 f8 v4) = f3 f9 f1 f3 v4",
        "poly_type": "Parametric",
        "dependencies": [
            "f8 :: v1 -> v1 -> f7 v1",
            "f1 :: f5 v1 => v1 -> v1 -> f7 v1",
            "f3 :: f6 v1 => v2 -> v1",
        ],
    }

    assert task.signature == valid_result["signature"]
    assert task.code == valid_result["code"]
    assert task.poly_type == valid_result["poly_type"]
    assert task.dependencies[0] == valid_result["dependencies"][0]


if __name__ == "__main__":
    test_rewrite()
