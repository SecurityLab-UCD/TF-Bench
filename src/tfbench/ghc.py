"""Util functions for using GHC"""

import os
import tempfile
import subprocess

from returns.result import Result, Success, Failure

from .hs_parser import get_type_vars_from_src


def ghc_type_proof(code: str) -> Result[None, str]:
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


PROVER = """
{-# LANGUAGE TypeOperators #-}
{-# LANGUAGE ImpredicativeTypes #-}
module Check where

import Data.Type.Equality

type TRUTH {truth_vars} = {truth_signature}
type ANSWER {answer_vars} = {answer_signature}

proof :: TRUTH {truth_vars} :~: ANSWER {answer_vars}
proof = Refl
"""


def get_prover(ground_truth: str, answer: str) -> str:
    """Construct Prover program based on Haskell TypeOperators and Type.Equality,
    If this prover compiles, then the answer is equivalent to the ground truth.
    """
    return PROVER.format(
        truth_vars=get_type_vars_from_src(ground_truth),
        truth_signature=ground_truth,
        answer_vars=get_type_vars_from_src(answer),
        answer_signature=answer,
    )
