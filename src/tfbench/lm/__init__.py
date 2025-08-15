import logging

from .prompts import get_sys_prompt
from .settings import MAX_TOKENS
from ._openai import OpenAIChatCompletion, OpenAIResponses
from ._types import LMResponse, LM, ReasoningEffort
from .utils import router, is_supported

logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

__all__ = [
    "get_sys_prompt",
    "MAX_TOKENS",
    "LMResponse",
    "LM",
    "ReasoningEffort",
    "OpenAIChatCompletion",
    "OpenAIResponses",
    "router",
    "is_supported",
]
