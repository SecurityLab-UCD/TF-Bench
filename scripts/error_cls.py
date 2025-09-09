from os.path import abspath, basename, join as pjoin
import os

import orjson
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

What mistake did I make?
"""

INSTRUCTION = """
You are a programming language and logic expert.
You will be shown a Haskell type inference task, 
an incorrect answer, and the reasoning behind it.
Your job is to identify the mistake in the answer,
and classify the mistake in one word.
The current error categories are:
{categories}.
Choose one category, or construct a new one if you are sure that
none of the current categories fit.
Only output the one-word classification and a short definition of the class.
NOTE that the short definition should be generalized to other tasks that fall in the same category.
"""


class ClsResponse(BaseModel):
    category: str
    definition: str

    def __hash__(self):
        return hash(self.category)


def get_prompt(task: BenchmarkTask, answer: LMAnswer) -> str:
    prompt = PROMPT_TEMPLATE.format(
        task=get_task_prompt(task),
        correct_answer=task.signature,
        wrong_answer=answer.answer,
        reasoning=answer.reasoning_steps,
    )
    return prompt


def categories_str(categories: set[ClsResponse]) -> str:
    """dump all categories in jsonl format string"""
    return "\n".join(orjson.dumps(c.__dict__).decode() for c in categories)


def classify_run(
    client: OpenAI,
    categories: set[ClsResponse],
    tasks: list[BenchmarkTask],
    run_result: list[LMAnswer | None],
) -> set[ClsResponse]:
    incorrect = get_incorrect(tasks, run_result)

    categories_: set[ClsResponse] = categories.copy()
    for task, answer in tqdm(incorrect):
        assert answer is not None
        response = client.responses.parse(
            model="gpt-5",
            instructions=INSTRUCTION.format(categories=categories_str(categories_)),
            input=get_prompt(task, answer),
            reasoning={"effort": "medium"},
            text_format=ClsResponse,
        )
        assert response.output_parsed is not None
        categories_.add(response.output_parsed)
    return categories_


def main(result_file_dir: str):

    client = OpenAI()
    categories: set[ClsResponse] = set()

    split = basename(abspath(result_file_dir))
    print(split)
    base = load_tfb_from_hf(split)

    for file in os.listdir(result_file_dir):
        if not file.endswith(".jsonl"):
            continue
        result_file_path = pjoin(result_file_dir, file)
        run_result = load_gen_results_jsonl(result_file_path)
        print(f"Processing {result_file_path}")
        run_categories = classify_run(
            client,
            categories,
            base,
            run_result,
        )
        categories.update(run_categories)

    with open("error_categories.json", "wb") as f:
        f.write(
            orjson.dumps(
                [c.model_dump(mode="json") for c in categories],
                option=orjson.OPT_INDENT_2,
            )
        )


if __name__ == "__main__":
    fire.Fire(main)
