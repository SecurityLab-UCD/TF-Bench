from tfbench.hs_parser import AST
from tfbench.type_def import is_class, is_data_type


def test_def_type_checker():
    type1 = "data T1 = T1"
    class1 = "class T1 a"
    f = "f :: Int -> Int"
    assert is_data_type(type1)
    assert not is_data_type(class1)
    assert is_class(class1)
    assert not is_class(type1)
    assert not is_class(f)
    assert not is_data_type(f)


def test_checker_after_rewrite():
    t1 = "data T1 a = Nothing | Just a"
    assert is_data_type(t1)
    assert not is_class(t1)
