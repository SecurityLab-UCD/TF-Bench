"""Util functions for using GHC"""

import os
import tempfile
import subprocess
from string import Template  # NOTE: use t-string after py3.14
from returns.result import Result, Success, Failure, safe

from .hs_parser import get_type_vars_from_src


def ghc_prove_equiv(code: str) -> Result[None, str]:
    """let GHC typecheck the given code snippet by compiling it

    Args:
        code: Haskell code snippet to typecheck
    Returns:
        Success(None) if typechecks, Failure(error_message) otherwise
    """
    file_name = "Check.hs"
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, file_name)
        with open(path, "w") as f:
            f.write(code)
        # -fno-code = typecheck only; -v0 = quiet
        process = subprocess.run(
            ["ghc", "-fno-code", "-v0", file_name],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )

        if process.returncode == 0:
            return Success(None)

        return Failure(process.stderr)


PROVER = Template(
    """
{-# LANGUAGE TypeOperators #-}
{-# LANGUAGE ImpredicativeTypes #-}
module Check where

import Data.Type.Equality

$new_types

$new_type_classes

type TRUTH $truth_vars = $truth_signature
type ANSWER $answer_vars = $answer_signature

proof :: TRUTH $truth_vars :~: ANSWER $truth_vars
proof = Refl
"""
)


def _get_var_str(source_code: str) -> str:
    ty_vars = get_type_vars_from_src(source_code)
    return " ".join(ty_vars)


def _get_body_str(source_code: str) -> str:
    assert "::" in source_code, "invalid type signature"
    return source_code.split("::", 1)[1].strip()


def _def_new_type(type_name: str) -> str:
    """construct a new, empty yet unique type definition for a given Monomorphic type name"""
    return f"data {type_name} = {type_name}"


def _def_new_type_class(class_name: str, type_vars: list[str]) -> str:
    """construct a new, empty yet unique type class definition for a given Ad-hoc type class name"""
    return f"class {class_name} {' '.join(type_vars)}"


@safe
def get_prover(
    ground_truth: str, answer: str, new_types: list[str] | None = None
) -> str:
    """Construct Prover program based on Haskell TypeOperators and Type.Equality,
    If this prover compiles, then the answer is equivalent to the ground truth.
    """
    new_types = new_types or []

    return PROVER.substitute(
        new_types="\n".join(map(_def_new_type, new_types)),
        new_type_classes="",  # todo: support new type classes
        truth_vars=_get_var_str(ground_truth),
        truth_signature=_get_body_str(ground_truth),
        answer_vars=_get_var_str(answer),
        answer_signature=_get_body_str(answer),
    )
