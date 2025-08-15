import logging

from .prompts import get_sys_prompt
from .settings import MAX_TOKENS
from ._openai import OpenAIChatCompletion, OpenAIResponses
from ._types import LM, ReasoningEffort, LMAnswer
from .utils import router, is_supported, extract_response

logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

__all__ = [
    "get_sys_prompt",
    "MAX_TOKENS",
    "LMAnswer",
    "LM",
    "ReasoningEffort",
    "OpenAIChatCompletion",
    "OpenAIResponses",
    "router",
    "is_supported",
    "extract_response",
]
