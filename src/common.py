from dataclasses import dataclass
import re
import copy
from funcy import lmap
import sys
import io

# Default hyper-parameters
SEED = 123
TEMPERATURE = 0.0
TOP_P = 1.0

SYSTEM_PROMPT = """
Act as a static analysis tool for type inference.
"""

INSTRUCT_PROMPT = """
1. Use the lowercase alphabet [a..z] for type variables instead of numbers.

2. ONLY output the type signature. Do Not Provide any additional commentaries or explanations.
"""


@dataclass
class BenchmarkTask:
    task_id: str
    signature: str
    code: str
    poly_type: str
    dependencies: list[str] | None


def extract_function_name(id_str: str) -> str | None:
    """Extract the function name from the id field."""
    if "--" in id_str:
        return id_str.split("--")[-1].strip()
    return None


def clean_tab_spaces(task: BenchmarkTask) -> BenchmarkTask:
    def clean(s: str) -> str:
        return re.sub(r"[ \t]+", " ", s)

    new_task = copy.copy(task)
    new_task.code = clean(task.code)
    new_task.dependencies = lmap(clean, task.dependencies)
    new_task.signature = clean(task.signature)

    return new_task


def remove_comments(code: str) -> str:
    # multi-line
    # code = re.sub(r"\{\-[\s\S]*?\-\}", "", code)
    code = re.sub(r"\{\-.*?\-\}", "", code, flags=re.DOTALL)
    # single-line
    code = re.sub(r"--.*", "", code)
    return code


def get_prompt(task: BenchmarkTask) -> str:
    """get prompt from a task instance"""

    fn_name = extract_function_name(task.task_id)
    code = task.code
    dependencies = (
        "where\n" + "\n".join(task.dependencies)
        if task.dependencies is not None
        else ""
    )

    if fn_name is not None:
        prompt = f"""
{code}
{dependencies}
--complete the following type signature for '{fn_name}'
{fn_name} :: 
"""
    return prompt


def silence(func):
    """Execute a function with suppressed stdout."""

    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        try:
            # Redirect stdout to a dummy file-like object
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            return func(*args, **kwargs)
        finally:
            # Restore original stdout
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    return wrapper
