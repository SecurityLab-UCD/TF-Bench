from returns.result import Result, Success, Failure
from funcy import lmap
from tfbench.ghc import ghc_prove_equiv, get_prover, reorder_constraints
from tfbench.type_def import def_new_type, def_new_type_constructor


def _equiv(
    truth: str,
    answer: str,
    new_types: list[str] | None = None,
    should_pass: bool = True,
):
    equiv = get_prover(truth, answer, new_types or []).alt(str).bind(ghc_prove_equiv)
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


def test_mono():
    """test GHC type equivalence prover for monomorphic types after rewriting"""
    # check with type after rewriting,
    # i.e. T1, ... T_n
    _equiv("f:: T1-> T1", "g ::T1 -> T1", new_types=[def_new_type("T1")])
    _not_equiv(
        "f:: T1-> T1",
        "g ::T2 -> T2",
        new_types=lmap(def_new_type, ["T1", "T2"]),
    )

    _equiv(
        "f:: (T1, T2) -> T1",
        "g ::(T1, T2) -> T1",
        new_types=lmap(def_new_type, ["T1", "T2"]),
    )
    _equiv(
        "f:: (Int, T2) -> Int",
        "g ::(Int, T2) -> Int",
        new_types=lmap(def_new_type, ["T2"]),
    )
    _not_equiv(
        "f:: (Int, T2) -> Int",
        "g ::(Int, T2) -> T2",
        new_types=lmap(def_new_type, ["T2"]),
    )


def test_typeclass_in_body():
    f = "f :: T1 -> T2 T3"
    _equiv(
        f,
        f,
        new_types=[
            def_new_type("T1"),
            def_new_type("T3"),
            def_new_type_constructor("T2", ["a"]),
        ],
    )


def test_constructor():
    _not_equiv(
        "f :: Maybe T1 -> T1",
        "g :: Maybe T2 -> T2",
        new_types=[
            def_new_type("T1"),
            def_new_type("T2"),
        ],
    )

    _equiv(
        "f :: T3 T1 -> T1",
        "g :: T3 T1 -> T1",
        new_types=[
            def_new_type("T1"),
            def_new_type_constructor("T3", ["a"]),
        ],
    )

    _equiv(
        "f::[a] -> T1 a",
        "g::[b] -> T1 b",
        new_types=[
            def_new_type_constructor("T1", ["a"]),
        ],
    )
    _equiv(
        "f::[T1] -> [a]",
        "g::[T1] -> [b]",
        new_types=[
            def_new_type("T1"),
        ],
    )

    _not_equiv(
        "f::[T1] -> [a]",
        "g::[T2] -> [b]",
        new_types=[
            def_new_type("T1"),
            def_new_type("T2"),
        ],
    )
