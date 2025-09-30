"""This file contains the generic default prompts for the LLMs used in the project."""

SYSTEM_PROMPT = """
Act as a static analysis tool for type inference.
ONLY output the type signature. 
Do Not Provide any additional commentaries or explanations."""

INSTRUCT_PROMPT = """
Remember that in Haskell:
1. The list type `[a]` is a polymorphic type, defined as `data [] a = [] | (:) a [a]`,
so `(:)` is a constructor for list type.
2. The String type is a list of characters, defined as `type String = [Char]`."""

CORE_PROMPT = """
For polymorphic types variables, you can use type variables like `a`, `b`, `c`, etc.
You should start with `a` and increment the alphabet as needed."""

PURE_PROMPT = """
For polymorphic types variables, you can use type variables like `t1`, `t2`, `t3`, etc.
You should start with `t1` and increment the number as needed."""


def get_sys_prompt(pure: bool) -> str:
    """helper function to get system prompt for pure version of TF-Bench"""
    sys_prompt = SYSTEM_PROMPT + INSTRUCT_PROMPT
    sys_prompt += PURE_PROMPT if pure else CORE_PROMPT
    return sys_prompt
