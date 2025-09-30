from tfbench.hs_parser import TypeExtractor


def test_real_cases():
    code = "f:: T1 t1 => t1"
    et = TypeExtractor(code)
    assert not et.type_constructors

    code = "f:: T1 t1 => T2 -> t1"
    et = TypeExtractor(code)
    assert not et.type_constructors
    assert et.names == {"T2"}

    code = "f:: T1 t1 => T2 T3 -> t1"
    et = TypeExtractor(code)
    assert et.type_constructors == {"T2": 1}
    assert et.names == {"T2", "T3"}

    code = "f:: T1 -> T2 T3 -> Either T1 T3 -> (T1, T3, T2 T3)"
    et = TypeExtractor(code)
    assert et.type_constructors == {"T2": 1, "Either": 2}
    assert et.names == {"T1", "T2", "T3", "Either"}

    code = "g:: Ord a  => Int -> Either String a -> T3 T1 T2 T4"
    et = TypeExtractor(code)
    assert et.type_constructors == {"Either": 2, "T3": 3}
    assert et.names == {"Int", "String", "T1", "T2", "T3", "T4", "Either"}


def test_list_tuple():
    code = "f :: [Int] -> T1 [Int]"
    et = TypeExtractor(code)
    assert et.type_constructors == {"T1": 1}
    assert et.names == {"Int", "T1"}

    code = "f :: (Int, T1) -> T2 (Int, T1)"
    et = TypeExtractor(code)
    assert et.type_constructors == {"T2": 1}
    assert et.names == {"Int", "T1", "T2"}

    code = "f :: Maybe a -> a"
    et = TypeExtractor(code)
    assert et.type_constructors == {"Maybe": 1}
    assert et.names == {"Maybe"}

    code = "f :: [Int] -> Int"
    et = TypeExtractor(code)
    assert not et.type_constructors
    assert et.names == {"Int"}
