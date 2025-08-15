"""
Experiment script for OpenAI models
"""

from typing import Callable
import logging


from .lm import get_sys_prompt, MAX_TOKENS

DEEPSEEK_MODELS = [
    "deepseek-reasoner",
    "deepseek-chat",
]
