import logging

from .prompts import get_sys_prompt
from .settings import MAX_TOKENS
from ._openai import OpenAIChatCompletion, OpenAIResponses
from ._google import GeminiChat, GeminiReasoning
from ._types import LM, LMAnswer
from .utils import router, extract_response

logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

__all__ = [
    "get_sys_prompt",
    "MAX_TOKENS",
    "LMAnswer",
    "LM",
    "OpenAIChatCompletion",
    "OpenAIResponses",
    "GeminiChat",
    "GeminiReasoning",
    "router",
    "extract_response",
]
