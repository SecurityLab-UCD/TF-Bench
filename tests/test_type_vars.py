from tfbench.hs_parser import get_type_vars


def test_monomorphic():
    """
    test type var extraction for monomorphic types,
    which should return empty set no matter how
    """
    candidates = [
        "f :: Int -> Int",
        "f::Int->Int",
        "f ::  Int  ->  Int  ",
        "f::  Int  ->  Int  ",
        "f::Int->  Int",
        "f  ::Int->Int",
        "g :: Int -> Int  -- with comment",
        "g::Int->Int--with comment",
        "g:: Int",
        "f1 :: Char -> Char\n",
        "f2 :: T1 -> T2",
        "f3 :: (Int, Char) -> (Char, Int)",
    ]

    ty_vars = map(get_type_vars, candidates)
    assert all(len(vs) == 0 for vs in ty_vars)


def _assert_equal(sig: str, expected: list[str]):
    ty_vars = get_type_vars(sig)
    assert ty_vars == expected, f"for {sig}, expected {expected}, got {ty_vars}"


def test_parametric():
    """test type var extraction for parametric types"""

    _assert_equal("f :: a -> a", ["a"])
    _assert_equal("f :: a -> b -> a", ["a", "b"])
    _assert_equal("f :: (a, b) -> (b, a)", ["a", "b"])
    _assert_equal("f :: (a -> b) -> [a] -> [b]", ["a", "b"])
    _assert_equal("f :: (a -> b) -> [a] -> Maybe b", ["a", "b"])
    _assert_equal("g :: t1 -> t2 -> (t1, t2)", ["t1", "t2"])
    _assert_equal("h :: (m -> n) -> (n -> o) -> m -> o", ["m", "n", "o"])
    _assert_equal(
        "k :: (a -> b) -> (b -> c) -> (c -> d) -> a -> d",
        ["a", "b", "c", "d"],
    )
    _assert_equal("m :: (x -> y) -> [x] -> Maybe y", ["x", "y"])
    _assert_equal("n :: (f a -> f b) -> [a] -> [b]", ["f", "a", "b"])

    # arbitrary order
    _assert_equal("p :: b -> a -> b", ["b", "a"])
    _assert_equal("q :: (b, a) -> (a, b)", ["b", "a"])
    _assert_equal("r :: (f b -> f a) -> [b] -> [a]", ["f", "b", "a"])


def test_mono_para_mixed():
    """test type var extraction for mixed monomorphic and parametric types"""

    _assert_equal("f :: a -> Int", ["a"])
    _assert_equal("f :: Int -> a", ["a"])
    _assert_equal("f :: (a, Int) -> (Int, a)", ["a"])
    _assert_equal("f :: (Int -> a) -> [Int] -> [a]", ["a"])
    _assert_equal("f :: (Int -> a) -> [Int] -> Maybe a", ["a"])
    _assert_equal("g :: t1 -> Int -> (t1, Int)", ["t1"])
    _assert_equal("h :: (Int -> n) -> (n -> Int) -> Int -> Int", ["n"])
    _assert_equal(
        "k :: (a -> Int) -> (Int -> c) -> (c -> d) -> a -> d",
        ["a", "c", "d"],
    )
    _assert_equal("m :: (x -> y) -> [Int] -> Maybe y", ["x", "y"])
    _assert_equal("n :: (f a -> f b) -> [Int] -> [b]", ["f", "a", "b"])

    # arbitrary order
    _assert_equal("p :: b -> Int -> b", ["b"])
    _assert_equal("q :: (b, Int) -> (Int, b)", ["b"])
    _assert_equal("r :: (f b -> f a) -> [Int] -> [a]", ["f", "b", "a"])


def test_adhoc():
    """test type var extraction for ad-hoc polymorphic types,
    i.e., with type class constraints
    """

    _assert_equal("f :: Eq a => a -> a", ["a"])
    _assert_equal("f :: (Eq a) => a -> a", ["a"])
    _assert_equal("f :: (Eq a, Show b) => a -> b -> a", ["a", "b"])
    _assert_equal("f :: (Ord a, Show b) => (a, b) -> (b, a)", ["a", "b"])
    _assert_equal(
        "f :: (Eq a, Show b) => (a -> b) -> [a] -> [b]",
        ["a", "b"],
    )
    _assert_equal(
        "f :: (Eq a, Show b) => (a -> b) -> [a] -> Maybe b",
        ["a", "b"],
    )
    _assert_equal(
        "m :: (Eq x, Show y) => (x -> y) -> [x] -> Maybe y",
        ["x", "y"],
    )
    _assert_equal(
        "n :: (Eq (f a), Show (f b)) => (f a -> f b) -> [a] -> [b]",
        ["f", "a", "b"],
    )


def test_para_adhoc_mix():
    """test type var extraction for mixed parametric and ad-hoc polymorphic types"""
    _assert_equal("g :: Eq t1 => t1 -> t2 -> (t1, t2)", ["t1", "t2"])
    _assert_equal(
        "h :: (Ord m, Eq n) => (m -> n) -> (n -> o) -> m -> o",
        ["m", "n", "o"],
    )
    # type class constraints order affects the order of type vars
    _assert_equal(
        "k :: (Eq a, Show c) => (a -> b) -> (b -> c) -> (c -> d) -> a -> d",
        ["a", "c", "b", "d"],
    )

    # arbitrary order
    _assert_equal("p :: Show b => b -> a -> b", ["b", "a"])
    _assert_equal("q :: Ord b => (b, a) -> (a, b)", ["b", "a"])
    _assert_equal(
        "r :: Eq (f b) => (f b -> f a) -> [b] -> [a]",
        ["f", "b", "a"],
    )
