from src.common import BenchmarkTask
from src.add_dependency import get_func_calls
from dacite import from_dict
import traceback


def test_len():
    task_data = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--properFraction",
        "signature": "properFraction      :: (Integral b) => a -> (b,a)",
        "code": "properFraction (x:%y) = (fromInteger (toInteger q), r:%y)\n                          where (q,r) = quotRem x y",
        "poly_type": "Ad-hoc",
        "dependencies": [],
    }

    task = from_dict(data_class=BenchmarkTask, data=task_data)
    calls = get_func_calls(task)
    assert len(calls) == 3


def test_call_extraction():
    task_data = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Maybe.hs--maybe",
        "signature": "maybe :: b -> (a -> b) -> Maybe a -> b",
        "code": "maybe _ f (Just x) = f x\nmaybe n _ Nothing = n",
        "poly_type": "Parametric",
        "dependencies": ["f :: Type -> Type", "Just :: a -> Maybe a"],
    }
    task = from_dict(data_class=BenchmarkTask, data=task_data)
    calls = get_func_calls(task)
    assert len(calls) == 2
    assert calls == {"f", "Just"}


if __name__ == "__main__":
    registered_tests = [test_len, test_call_extraction]
    for t in registered_tests:
        try:
            t()
        except AssertionError:
            print(f"Test case {t.__name__} failed:\n{traceback.format_exc()}")
