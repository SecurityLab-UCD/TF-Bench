from returns.result import Result, Success, Failure
from tfbench.ghc import ghc_prove_equiv, get_prover, reorder_type_classes


def _equiv(
    truth: str,
    answer: str,
    new_types: list[str] | None = None,
    should_pass: bool = True,
):
    equiv = get_prover(truth, answer, new_types).alt(str).bind(ghc_prove_equiv)
    match equiv:
        case Success(_):
            assert should_pass
        case Failure(err):
            assert not should_pass, err


def _not_equiv(
    truth: str,
    answer: str,
    new_types: list[str] | None = None,
):
    _equiv(truth, answer, new_types, should_pass=False)


def test_monomorphic():
    """test GHC type equivalence prover for monomorphic types"""

    _equiv("f::Int -> Int", "g ::Int -> Int")
    _equiv("f::(Int, Bool) -> Int", "g ::(Int, Bool) -> Int")
    _equiv("f::Int -> Bool -> Int", "g ::Int -> Bool -> Int")
    _equiv(
        "f::(Int -> Bool) -> [Int] -> [Bool]",
        "g ::(Int -> Bool) -> [Int] -> [Bool]",
    )
    _equiv(
        "f::(Int -> Bool) -> [Int] -> Maybe Bool",
        "g ::(Int -> Bool) -> [Int] -> Maybe Bool",
    )

    # negative cases
    _not_equiv("f::Int -> Int", "g ::Bool -> Bool")
    _not_equiv("f::(Int, Bool) -> Int", "g ::(Bool, Int) -> Int")
    _not_equiv(
        "f::(Int -> Bool) -> [Int] -> [Bool]",
        "g ::(Bool -> Int) -> [Int] -> [Bool]",
    )

    # check with type after rewriting,
    # i.e. T1, ... T_n
    _equiv("f:: T1-> T1", "g ::T1 -> T1", new_types=["T1"])
    _not_equiv(
        "f:: T1-> T1",
        "g ::T2 -> T2",
        new_types=["T1", "T2"],
    )

    _equiv(
        "f:: (T1, T2) -> T1",
        "g ::(T1, T2) -> T1",
        new_types=["T1", "T2"],
    )
    _equiv(
        "f:: (Int, T2) -> Int",
        "g ::(Int, T2) -> Int",
        new_types=["T2"],
    )
    _not_equiv(
        "f:: (Int, T2) -> Int",
        "g ::(Int, T2) -> T2",
        new_types=["T2"],
    )


def test_parametric():
    """test GHC type equivalence prover for parametric types"""

    _equiv("f :: a -> a", "g :: b -> b")
    _equiv("f :: a -> b -> a", "g :: x -> y -> x")
    _equiv("f :: (a, b) -> (b, a)", "g :: (x, y) -> (y, x)")
    _equiv("f :: (a -> b) -> [a] -> [b]", "g :: (x -> y) -> [x] -> [y]")
    _equiv(
        "f :: (a -> b) -> [a] -> Maybe b",
        "g :: (x -> y) -> [x] -> Maybe y",
    )
    _equiv("g :: t1 -> t2 -> (t1, t2)", "h :: u1 -> u2 -> (u1, u2)")
    _equiv(
        "h :: (m -> n) -> (n -> o) -> m -> o",
        "k :: (x -> y) -> (y -> z) -> x -> z",
    )
    _equiv(
        "k :: (a -> b) -> (b -> c) -> (c -> d) -> a -> d",
        "m :: (x -> y) -> (y -> z) -> (z -> w) -> x -> w",
    )
    _equiv(
        "m :: (x -> y) -> [x] -> Maybe y",
        "n :: (a -> b) -> [a] -> Maybe b",
    )
    _equiv(
        "n :: (f a -> f b) -> [a] -> [b]",
        "p :: (g x -> g y) -> [x] -> [y]",
    )

    # although it is very rare to have these kinds of function types,
    # the following should still hold, since a, b, c,d are arbitrary type variables
    # it is not really possible to write a function that return any type variable
    _equiv("f :: a -> b", "g :: b -> a")
    _equiv("f :: a -> b", "g :: c -> d")

    # however, the following should not hold
    # although a, b are arbitrary type variables
    # `g` requires both input and output to be the same type variable,
    # whereas `f` does not.
    _not_equiv("f :: a -> b", "g :: a -> a")

    # negative cases
    _not_equiv("f :: a -> a", "g :: a -> b")
    _not_equiv("f :: a -> b", "g :: a -> a")

    _not_equiv("f :: a -> b", "g :: Int-> Int")
    _not_equiv(
        "f :: (a, b) -> c",
        "g :: (Int, Int) -> Int",
    )


def test_mono_para_mixed():
    """test GHC type equivalence prover for mixed monomorphic and parametric types"""

    _equiv("f :: a -> Int", "g :: b -> Int")
    _equiv("f :: Int -> a", "g :: Int -> b")
    _equiv("f :: (a, Int) -> (Int, a)", "g :: (b, Int) -> (Int, b)")
    _equiv(
        "f :: (a -> Int) -> [Int] -> [a]",
        "g :: (b -> Int) -> [Int] -> [b]",
    )
    _equiv(
        "f :: (a -> Int) -> [Int] -> Maybe a",
        "g :: (b -> Int) -> [Int] -> Maybe b",
    )
    _equiv(
        "g :: t1 -> Int -> (t1, Int)",
        "h :: u1 -> Int -> (u1, Int)",
    )
    _equiv(
        "h :: (Int -> n) -> (n -> Int) -> Int -> Int",
        "k :: (Int -> y) -> (y -> Int) -> Int -> Int",
    )
    _equiv(
        "k :: (a -> Int) -> (Int -> c) -> (c -> d) -> a -> d",
        "m :: (x -> Int) -> (Int -> y) -> (y -> z) -> x -> z",
    )
    _equiv(
        "m :: (x -> y) -> [Int] -> Maybe y",
        "n :: (a -> b) -> [Int] -> Maybe b",
    )
    _equiv(
        "n :: (f a -> f b) -> [Int] -> [b]",
        "p :: (g x -> g y) -> [Int] -> [y]",
    )

    # negative cases
    _not_equiv("f :: a -> Int", "g :: a-> a")
    _not_equiv("f :: a-> a", "g :: a-> Int")

    _not_equiv("f :: a-> Int", "g :: Int-> Int")
    _not_equiv(
        "f :: (a, Int) -> Int",
        "g :: (Int, Int) -> Int",
    )


def test_adhoc():
    """test GHC type equivalence prover for ad-hoc polymorphic types,
    i.e., with type class constraints
    """

    _equiv("f :: Eq a => a -> a", "g :: Eq b => b -> b")
    _equiv("f :: (Eq a) => a -> a", "g :: (Eq b) => b -> b")
    # test with parenthesis around constraints
    _equiv("f :: (Eq a) => a -> a", "g :: Eq b => b -> b")
    _equiv("f :: (Eq a, Show b) => a -> b -> a", "g :: (Eq x, Show y) => x -> y -> x")
    _equiv(
        "f :: (Ord a, Show b) => (a, b) -> (b, a)",
        "g :: (Ord x, Show y) => (x, y) -> (y, x)",
    )
    _equiv(
        "f :: (Eq a, Show b) => (a -> b) -> [a] -> [b]",
        "g :: (Eq x, Show y) => (x -> y) -> [x] -> [y]",
    )
    _equiv(
        "f :: (Eq a, Show b) => (a -> b) -> [a] -> Maybe b",
        "g :: (Eq x, Show y) => (x -> y) -> [x] -> Maybe y",
    )
    _equiv(
        "m :: (Eq x, Show y) => (x -> y) -> [x] -> Maybe y",
        "n :: (Eq a, Show b) => (a -> b) -> [a] -> Maybe b",
    )
    _equiv(
        "n :: (Eq (f a), Show (f b)) => (f a -> f b) -> [a] -> [b]",
        "p :: (Eq (g x), Show (g y)) => (g x -> g y) -> [x] -> [y]",
    )

    # negative cases
    _not_equiv("f :: Eq a => a -> a", "g :: a-> a")
    _not_equiv("f :: a-> a", "g :: Eq a => a-> a")

    _not_equiv("f :: Eq a => a-> Int", "g :: Int-> Int")
    _not_equiv(
        "f :: (Eq a, Show b) => (a, Int) -> Int",
        "g :: (Int, Int) -> Int",
    )


def test_para_adhoc_mix():
    """test GHC type equivalence prover for mixed parametric and ad-hoc polymorphic types"""

    _equiv("f :: Eq a => a -> Int", "g :: Eq b => b -> Int")
    _equiv("f :: Int -> a", "g :: Int -> b")
    _equiv("f :: (Eq a) => (a, Int) -> (Int, a)", "g :: (Eq b) => (b, Int) -> (Int, b)")
    _equiv(
        "f :: (Ord a, Show b) => (a -> Int) -> [Int] -> [a]",
        "g :: (Ord x, Show y) => (x -> Int) -> [Int] -> [x]",
    )
    _equiv(
        "f :: (Eq a, Show b) => (a -> Int) -> [Int] -> Maybe a",
        "g :: (Eq x, Show y) => (x -> Int) -> [Int] -> Maybe x",
    )
    _equiv(
        "g :: Eq t1 => t1 -> Int -> (t1, Int)",
        "h :: Eq u1 => u1 -> Int -> (u1, Int)",
    )
    _equiv(
        "h :: (Int -> n) -> (n -> Int) -> Int -> Int",
        "k :: (Int -> y) -> (y -> Int) -> Int -> Int",
    )
    _equiv(
        "k :: (Eq a, Show c) => (a -> Int) -> (Int -> c) -> (c -> d) -> a -> d",
        "m :: (Eq x, Show y) => (x -> Int) -> (Int -> y) -> (y -> z) -> x -> z",
    )
    _equiv(
        "m :: (Eq x, Show y) => (x -> y) -> [Int] -> Maybe y",
        "n :: (Eq a, Show b) => (a -> b) -> [Int] -> Maybe b",
    )
    _equiv(
        "n :: (Eq (f a), Show (f b)) => (f a -> f b) -> [a] -> [b]",
        "p :: (Eq (g x), Show (g y)) => (g x -> g y) -> [x] -> [y]",
    )
    _not_equiv(
        "n :: (Eq (f a), Show (f b)) => (f a -> f b) -> [Int] -> [b]",
        "p :: (Eq (g x), Show (g y)) => (g x -> g y) -> [x] -> [y]",
    )


def test_tfb_real():
    """test cases from TF-Bench real tasks,
    where the deprecated evaluate failed
    """

    # type -> is right-associative
    _equiv(
        "uncurry :: (a -> b -> c) -> ((a, b) -> c)",
        "g::(a -> b -> c) -> (a, b) -> c",
    )
    _equiv(
        "(.) :: (b -> c) -> (a -> b) -> a -> c",
        "(.) :: (b -> c) -> (a -> b) -> (a -> c)",
    )
    _equiv("($) :: (a -> b) -> a -> b", "($) :: (a -> b) -> (a -> b)")

    # type class constraints are commutative
    _equiv(
        "elem :: (Foldable t, Eq a) => a -> t a -> Bool",
        "g :: (Eq a, Foldable t) => a -> t a -> Bool",
    )

    # type alias not expanded
    _equiv(
        "showList :: Show a => [a] -> ShowS",
        "g :: Show a => [a] -> String -> String",
    )


def test_reorder():
    """test reorder_type_classes function"""
    s1 = "f :: (Eq a, Show a) => a -> String"
    s2 = "f :: (Show a, Eq a) => a -> String"

    rs1 = reorder_type_classes(s1)
    rs2 = reorder_type_classes(s2)

    _equiv(rs1, rs2)
    _equiv(rs2, rs2)
    _equiv(rs1, rs1)

    _equiv(s1, rs2)
    _equiv(s2, rs1)
    _equiv(s1, s2)
