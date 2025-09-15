from typing import TypedDict, Literal

from pydantic import BaseModel
from openai import OpenAI

from .common import get_prompt as get_task_prompt, BenchmarkTask
from .lm import LMAnswer

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
Only output the one-word classification. 
"""

ErrorCategories = Literal[
    "OverGeneralization",
    "UnderGeneralization",
    "ArgOrderMismatch",
    "ArityMismatch",
    "ConstraintError",
    "SyntaxError",
    "InstructionFollowing",
    "ResponseError",
]


class ErrorAnalysisResponse(BaseModel):
    category: ErrorCategories


def get_error_analysis_prompt(
    task: BenchmarkTask, answer: LMAnswer, error_msg: str
) -> str:
    """construct classification prompt for one task and answer pair"""
    prompt = PROMPT_TEMPLATE.format(
        task=get_task_prompt(task),
        correct_answer=task.signature,
        wrong_answer=answer.answer,
        reasoning=answer.reasoning_steps,
        ghc_error=error_msg,
    )
    return prompt


def error_analysis(
    client: OpenAI,
    task: BenchmarkTask,
    answer: LMAnswer | None,
    error_msg: str,
    model: str = "gpt-5-mini",
) -> ErrorAnalysisResponse:
    """classify errors for all incorrect answers in the run_result"""
    if answer is None:
        return ErrorAnalysisResponse(category="ResponseError")

    response = client.responses.parse(
        model=model,
        instructions=INSTRUCTION,
        input=get_error_analysis_prompt(task, answer, error_msg=error_msg),
        reasoning={"effort": "medium"},
        text_format=ErrorAnalysisResponse,
    )
    assert response.output_parsed is not None
    return response.output_parsed


class ErrorAnalysisResult(TypedDict):
    model: str
    split: Literal["base", "pure"]
    task_id: str
    ground_truth: str
    predicted: str | None
    error_category: ErrorCategories
