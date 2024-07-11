from src.common import BenchmarkTask
from src.add_dependency import get_func_calls
from dacite import from_dict


if __name__ == "__main__":
    task_data = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--properFraction",
        "signature": "properFraction      :: (Integral b) => a -> (b,a)",
        "code": "properFraction (x:%y) = (fromInteger (toInteger q), r:%y)\n                          where (q,r) = quotRem x y",
        "poly_type": "Ad-hoc",
        "dependencies": "y :: TypeRep y\ntoInteger           :: a -> Integer\nx :: b\nquotRem             :: a -> a -> (a,a)\nfromInteger         :: Integer -> a",
    }

    task = from_dict(data_class=BenchmarkTask, data=task_data)
    calls = get_func_calls(task)
    assert len(calls) == 3
