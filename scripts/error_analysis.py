from os.path import abspath, basename, join as pjoin
import os
from typing import TypedDict, Literal

from orjsonl import orjsonl
from pydantic import BaseModel
from openai import OpenAI
import fire
from tqdm import tqdm

from tfbench import (
    load_tfb_from_hf,
    load_gen_results_jsonl,
    LMAnswer,
)
from tfbench.evaluation import get_incorrect
from tfbench.common import get_prompt as get_task_prompt, BenchmarkTask


PROMPT_TEMPLATE = """
The Haskell type inference task is as follows:
{task}

The ground-truth correct answer is:
{correct_answer}

My incorrect answer is:
{wrong_answer}

My reasoning behind my answer is:
{reasoning}

The error message from GHC's type  checker is:
{ghc_error}

What mistake did I make?
"""

INSTRUCTION = """
You are a programming language and logic expert.
You will be shown a Haskell type inference task, 
an incorrect answer, and the reasoning behind it.
The type signatures should be alpha-equivalent to the ground-truth answer.
Your job is to identify the mistake in the answer,
and classify the mistake in the following category.
The error categories and their definitions are:

- OverGeneralization: Choose a type that is too general—used broader polymorphism 
(e.g., different input/output type variables) where the most general valid type actually requires them to be the same.

- UnderGeneralization: Added an unnecessary/stronger type-class constraint that is not provided by the implementation, 
making the signature more specific than the most general valid type.

- ArgOrderMismatch: Right type variables but in the wrong parameter order; 
the type's argument sequence doesn't match the implementation (a permutation error, not a generality/constraint issue).

- ArityMismatch: Provided a type with the wrong number of arguments (too many or too few) compared to the implementation.

- ConstraintError: Used incorrect type-class constraints that don't align with the implementation's requirements.
The wrong type-class constraints were applied to the type variables.

- SyntaxError: Provided an answer that is not a valid Haskell type signature.

- InstructionFollowing: Failed to follow the instructions given in the prompt.

- ResponseError: No answer was provided, or the answer is completely unrelated to the task.

The prompt asked to only output the type signature,
but the answer contains additional text or explanation.
Choose one category from the above.
Only output the one-word classification and a short explanation of the why this category fits.
"""


class ClsResponse(BaseModel):
    category: Literal[
        "OverGeneralization",
        "UnderGeneralization",
        "ArgOrderMismatch",
        "ArityMismatch",
        "ConstraintError",
        "SyntaxError",
        "InstructionFollowing",
        "ResponseError",
    ]
    explanation: str


def get_prompt(task: BenchmarkTask, answer: LMAnswer, error_msg: str) -> str:
    """construct classification prompt for one task and answer pair"""
    prompt = PROMPT_TEMPLATE.format(
        task=get_task_prompt(task),
        correct_answer=task.signature,
        wrong_answer=answer.answer,
        reasoning=answer.reasoning_steps,
        ghc_error=error_msg,
    )
    return prompt


def classify(
    client: OpenAI,
    task: BenchmarkTask,
    answer: LMAnswer | None,
    error_msg: str,
) -> ClsResponse:
    """classify errors for all incorrect answers in the run_result"""
    if answer is None:
        return ClsResponse(category="ResponseError", explanation="No answer provided.")

    response = client.responses.parse(
        model="gpt-5",
        instructions=INSTRUCTION,
        input=get_prompt(task, answer, error_msg=error_msg),
        reasoning={"effort": "medium"},
        text_format=ClsResponse,
    )
    assert response.output_parsed is not None
    return response.output_parsed


def analysis(result_file_dir: str, split: str, output_file: str):
    """script to run error analysis fo incorrect TF-Bench tasks"""
    client = OpenAI()
    tasks = load_tfb_from_hf(split)

    split_result_dir = pjoin(result_file_dir, split)

    incorrect = []
    print(f"Collecting incorrect results from {split_result_dir} on split {split}")
    for file in os.listdir(split_result_dir):
        if not file.endswith(".jsonl"):
            continue
        result_file_path = pjoin(split_result_dir, file)
        run_result = load_gen_results_jsonl(result_file_path)

        incorrect_of_run = get_incorrect(tasks, run_result, split == "pure")
        incorrect.extend(incorrect_of_run)

    print(f"Running error classification on {len(incorrect)} incorrect results")
    for task, answer, msg in tqdm(incorrect):
        error = classify(client, task, answer, error_msg=msg)
        log_obj = {
            "split": split,
            "task_id": task.task_id,
            "ground_truth": task.signature,
            "predicted": answer.answer if answer else None,
            "error_category": error.category,
            "error_explanation": error.explanation,
        }
        orjsonl.append(output_file, log_obj)


def main(result_file_dir: str, output_file: str | None = None):
    """run result analysis on both base and pure splits"""

    model = basename(abspath(result_file_dir))
    print(f"Running error analysis for model {model}")
    if output_file is None:
        output_file = f"{model}.error_analysis.jsonl"

    analysis(result_file_dir, "base", output_file)
    analysis(result_file_dir, "pure", output_file)


if __name__ == "__main__":
    fire.Fire(main)
