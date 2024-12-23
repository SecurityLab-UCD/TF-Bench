from src.evaluation import alpha_equiv


def test_simple():
    s1 = "a -> b -> c"
    s2 = "d -> e -> f"
    assert alpha_equiv(s1, s2)

    s3 = "a -> c -> b"
    assert alpha_equiv(s1, s3)
    assert alpha_equiv(s2, s3)


def test_simple_dep():
    s1 = "a -> b -> a -> b"
    s2 = "c -> d -> c -> d"
    assert alpha_equiv(s1, s2)

    s3 = "a -> c -> a -> c"
    assert alpha_equiv(s1, s3)
    assert alpha_equiv(s2, s3)


def test_fn():
    s1 = "(a -> b) -> a -> b"
    s2 = "(c -> d) -> c -> d"
    assert alpha_equiv(s1, s2)

    s3 = "(a -> c) -> a -> c"
    assert alpha_equiv(s1, s3)
    assert alpha_equiv(s2, s3)

    s4 = "(a -> b) -> [a] -> [b]"
    s5 = "(c -> d) -> [c] -> [d]"
    assert not alpha_equiv(s1, s4)
    assert alpha_equiv(s4, s5)
    s6 = "(a -> c) -> [a] -> [c]"
    assert alpha_equiv(s4, s6)
    assert alpha_equiv(s5, s6)


def test_adt():
    s1 = "pure :: a -> Either e a"
    s2 = "pure :: b -> Either e b"
    assert alpha_equiv(s1, s2)

    s3 = "f :: a -> Either d c"
    assert not alpha_equiv(s1, s3)
    assert not alpha_equiv(s2, s3)


def test_type_class():
    s1 = "Eq a => a -> a -> Bool"
    s2 = "Eq b => b -> b -> Bool"
    assert alpha_equiv(s1, s2)

    s3 = "Eq a => a -> b -> Bool"
    assert not alpha_equiv(s1, s3)


def test_tuple():
    s1 = "(a, b) -> a"
    s2 = "(c, d) -> c"
    assert alpha_equiv(s1, s2)

    s3 = "(a, b) -> b"
    assert not alpha_equiv(s1, s3)
    assert not alpha_equiv(s2, s3)


if __name__ == "__main__":
    test_simple()
    test_simple_dep()
    test_fn()
    test_adt()
    test_type_class()
    test_tuple()
