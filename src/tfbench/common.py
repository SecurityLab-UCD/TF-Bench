from dataclasses import dataclass, field
import re
import copy
import sys
import io

from funcy import lmap
import markdown_to_json


@dataclass
class BenchmarkTask:
    task_id: str
    poly_type: str
    signature: str
    code: str
    dependencies: list[str] = field(default_factory=list)


def extract_function_name(task: BenchmarkTask) -> str | None:
    """get function name from a task
    For example, given a task with signature 'foo :: Int -> Int',
    it will return 'foo'.
    """
    return task.signature.split("::")[0].strip()


def clean_tab_spaces(task: BenchmarkTask) -> BenchmarkTask:
    """remove tab spaces from the code"""

    def clean(s: str) -> str:
        return re.sub(r"[ \t]+", " ", s)

    new_task = copy.copy(task)
    # new_task.code = clean(task.code)
    new_task.dependencies = lmap(clean, task.dependencies)
    new_task.signature = clean(task.signature)

    return new_task


def remove_comments(code: str) -> str:
    """remove Haskell comments"""
    # multi-line
    # code = re.sub(r"\{\-[\s\S]*?\-\}", "", code)
    code = re.sub(r"\{\-.*?\-\}", "", code, flags=re.DOTALL)
    # single-line
    code = re.sub(r"--.*", "", code)
    return code



def remove_return_type(sig: str) -> str:
    """
    Removes only the 'something' part after the last top-level '->',
    but keeps the arrow itself. Ignores arrows inside parentheses.
    """
    func_part, type_part = sig.split("::", 1)
    func_part = func_part.strip() + " ::"
    type_part = type_part.strip()

    # 2) Find the last top-level arrow by tracking parentheses
    paren_level = 0
    last_arrow_index = None
    i = 0
    while i < len(type_part) - 1:
        c = type_part[i]
        if c == "(":
            paren_level += 1
        elif c == ")":
            paren_level -= 1
        elif c == "-" and type_part[i + 1] == ">" and paren_level == 0:
            # Found a top-level arrow
            last_arrow_index = i
        i += 1

    # 3) Keep the arrow but remove everything after it
    if last_arrow_index is not None:
        # Keep '->' and discard what follows
        new_type = type_part[: last_arrow_index + 2]
        return func_part + " " + new_type.rstrip()

    # No top-level arrow found; return as-is
    return sig


def get_prompt(task: BenchmarkTask) -> str:
    """get prompt from a task instance"""

    fn_name = extract_function_name(task)
    assert fn_name is not None

    code = task.code
    dependencies = (
        "\n".join(map(str.strip, task.dependencies))
        if task.dependencies is not None
        else ""
    )

    prompt = f"""
{dependencies}
\n\n
{code}
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


def task2md(task: BenchmarkTask) -> str:
    """Convert a task object to markdown format, where key will be title and value will be content
    wrap code block with triple backticks"""

    md = f"""
# task_id
{task.task_id}

# poly_type
{task.poly_type}

# signature
```haskell
{task.signature}
```   

# code
```haskell
{task.code}
```

# dependencies
"""
    if task.dependencies is not None:
        for i, dep in enumerate(task.dependencies):
            md += f"## {i}\n```haskell\n{dep}\n```\n"
    return md


def md2task(md: str) -> BenchmarkTask:
    """Convert a markdown string to a task object"""

    raw_dict = markdown_to_json.dictify(md)

    def rm_md_block(text: str) -> str:
        return text.replace("```\n", "").replace("\n```", "")

    dependencies = []
    if isinstance(raw_dict["dependencies"], dict):
        for _, v in raw_dict["dependencies"].items():
            dependencies.append(rm_md_block(v))

    return BenchmarkTask(
        task_id=raw_dict["task_id"],
        poly_type=raw_dict["poly_type"],
        signature=rm_md_block(raw_dict["signature"]),
        code=rm_md_block(raw_dict["code"]),
        dependencies=dependencies,
    )
