import logging

from .prompts import get_sys_prompt
from .settings import MAX_TOKENS
from ._openai import (
    OAI_MODELS,
    OAI_TTC_MODELS,
    OAI_O5,
    OpenAIChatCompletion,
    OpenAIResponses,
)
from ._google import GEMINI_MODELS, GEMINI_TTC_MODELS, GeminiChat, GeminiReasoning
from ._anthropic import CLAUDE_MODELS, CLAUDE_TTC_MODELS, ClaudeChat, ClaudeReasoning
from ._ollama import OLLAMA_TTC_MODELS, OllamaChat
from ._hf import HFChat
from ._types import LM, LMAnswer
from .utils import router, extract_response

logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

supported_models = (
    OAI_MODELS
    + OAI_TTC_MODELS
    + OAI_O5
    + GEMINI_MODELS
    + GEMINI_TTC_MODELS
    + CLAUDE_MODELS
    + CLAUDE_TTC_MODELS
    + OLLAMA_TTC_MODELS
)

__all__ = [
    "get_sys_prompt",
    "MAX_TOKENS",
    "LMAnswer",
    "LM",
    "OpenAIChatCompletion",
    "OpenAIResponses",
    "GeminiChat",
    "GeminiReasoning",
    "ClaudeChat",
    "ClaudeReasoning",
    "OllamaChat",
    "HFChat",
    "router",
    "extract_response",
    "supported_models",
]
