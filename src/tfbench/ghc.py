"""Util functions for using GHC"""

import os
import tempfile
import subprocess
from string import Template  # NOTE: use t-string after py3.14
from returns.result import Result, Success, Failure, safe

from .hs_parser import get_type_vars, get_type_constraints


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

-- Some predefined types synonyms to avoid name clashes
type Int_ = Int
type Bool_ = Bool
type Char_ = Char
type Float_ = Float
type Double_ = Double
data Natural = Natural

$new_types

type TRUTH $truth_vars = $truth_signature
type ANSWER $answer_vars = $answer_signature

proof :: TRUTH $truth_vars :~: ANSWER $truth_vars
proof = Refl
"""
)


def _get_var_str(source_code: str) -> str:
    ty_vars = get_type_vars(source_code)
    return " ".join(ty_vars)


def _get_body_str(source_code: str) -> str:
    assert "::" in source_code, "invalid type signature"
    return source_code.split("::", 1)[1].strip()


def reorder_constraints(type_signature: str) -> str:
    """Reorder type classes constrains in a type signature to a canonical order"""
    # No type classes to reorder
    if "=>" not in type_signature:
        return type_signature

    assert "::" in type_signature, "invalid type signature"
    prefix, body = type_signature.split("::", 1)

    _, rest = body.split("=>", 1)
    constrains = get_type_constraints(type_signature)
    constrains.sort()  # Sort alphabetically
    return f"{prefix}:: ({', '.join(constrains)}) => {rest}"


@safe
def get_prover(
    ground_truth: str, answer: str, types_defs: list[str] | None = None
) -> str:
    """Construct Prover program based on Haskell TypeOperators and Type.Equality,
    If this prover compiles, then the answer is equivalent to the ground truth.
    """
    types_defs = types_defs or []
    ground_truth = reorder_constraints(ground_truth)
    answer = reorder_constraints(answer)
    return PROVER.substitute(
        new_types="\n".join(types_defs),
        truth_vars=_get_var_str(ground_truth),
        truth_signature=_get_body_str(ground_truth),
        answer_vars=_get_var_str(answer),
        answer_signature=_get_body_str(answer),
    )
