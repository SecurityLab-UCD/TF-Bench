from dacite import from_dict
from src.common import BenchmarkTask
from src.hs_parser import HASKELL_LANGUAGE
from src.hs_parser.ast_util import AST, ASTLoc, HaskellFunction
from hypothesis import given
import hypothesis.strategies as st
from funcy_chain import Chain
from src.hs_parser.polymorphism import get_polymorphic_type, PolymorphicType
from src.type_rewrite import rewrite_functions, rewrite_type


def test_rewrite_type():
    task_data = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromRational",
        "signature": "fromRational :: Rational -> a",
        "code": "fromRational (x:%y) = fromInteger x % fromInteger y",
        "poly_type": "Parametric",
        "dependencies": [
            "fromInteger :: Integer -> a",
            "(%) :: (Integral a) => a -> a -> Ratio a"
        ]
    }
    result = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromRational", 
        "signature": "fromRational :: A -> a", 
        "code": "fromRational (x:%y) = fromInteger x % fromInteger y", "poly_type": "Parametric", 
        "dependencies": [
            "fromInteger :: B -> a", 
            "(%) :: (Integral a) => a -> a -> Ratio a"
        ]
    }

    task = from_dict(data_class=BenchmarkTask, data=task_data)

    task = rewrite_type(task)

    assert task.signature == result["signature"]
    assert task.code == result["code"]
    assert task.poly_type == result["poly_type"]
    assert task.dependencies[0] == task.dependencies[0]


def test_rewrite_func():
    task_data = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Maybe.hs--maybe",
        "signature": "maybe :: b -> (a -> b) -> Maybe a -> b",
        "code": "maybe _ f (Just x) = f x\nmaybe n _ Nothing = n",
        "poly_type": "Parametric",
        "dependencies": [
            "Just :: a -> Maybe a"
        ]
    }
    result = {
        "task_id": "data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Maybe.hs--maybe",
        "signature": "q :: b -> (a -> b) -> Maybe a -> b",
        "code": "q _ f (p x) = f x\q n _ Nothing = n",
        "poly_type": "Parametric",
        "dependencies": [
            "p :: a -> Maybe a"
        ]
    }

    task = from_dict(data_class=BenchmarkTask, data=task_data)

    task = rewrite_functions(task)

    assert task.signature == result["signature"]
    assert task.code == result["code"]
    assert task.poly_type == result["poly_type"]
    assert task.dependencies[0] == task.dependencies[0]


if __name__ == "__main__":
    test_rewrite_type()
    test_rewrite_func()
