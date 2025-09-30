import logging
from typing import Literal, get_args, cast, Any, Union, get_origin
from types import UnionType

from returns.result import ResultE, Success, Failure
from openai.types.shared.reasoning_effort import ReasoningEffort as OAIReasoningEffort

from ._types import LM, LMAnswer
from ._openai import (
    OpenAIChatCompletion,
    OpenAIResponses,
    OAI_MODELS,
    OAI_TTC_MODELS,
    OAI_O5,
)
from ._google import GeminiChat, GeminiReasoning, GEMINI_MODELS, GEMINI_TTC_MODELS
from ._anthropic import ClaudeChat, ClaudeReasoning, CLAUDE_MODELS, CLAUDE_TTC_MODELS
from ._ollama import OllamaChat, OLLAMA_TTC_MODELS
from ._hf import HFChat

from ._google import GeminiReasoningEffort
from ._types import ReasoningEffort


def _literal_options(tp: Any) -> set[str]:
    """Collect string values from Literal[...] inside tp (handles Unions)."""
    origin = get_origin(tp)
    if origin is Literal:
        # Direct Literal["a", "b", ...]
        return set(get_args(tp))
    if origin is Union or (UnionType is not None and origin is UnionType):
        vals: set[str] = set()
        for arg in get_args(tp):
            vals |= _literal_options(arg)
        return vals
    return set()  # not a Literal or Union of Literals


def _assert_valid_effort(model: str, effort: str | None, effort_cls: Any) -> None:
    """Check if the given effort is valid for the model."""
    if effort is None:
        return
    allowed = _literal_options(effort_cls)
    assert effort in allowed, f"`{effort}` is not a valid reasoning effort for {model}."


def router(
    model_name: str,
    pure: bool,
    effort: str | None = None,
) -> LM:
    """Route the model name to the appropriate LM class."""
    if model_name in OAI_MODELS:
        return OpenAIChatCompletion(model_name=model_name, pure=pure)

    if model_name in OAI_TTC_MODELS:
        return OpenAIResponses(model_name=model_name, pure=pure)

    if model_name in OAI_O5:
        _assert_valid_effort(model_name, effort, OAIReasoningEffort)
        # cast is safe here after assertion
        return OpenAIResponses(
            model_name=model_name,
            pure=pure,
            effort=cast(OAIReasoningEffort, effort),
        )

    if model_name in GEMINI_MODELS:
        return GeminiChat(model_name=model_name, pure=pure)

    if model_name in GEMINI_TTC_MODELS:
        _assert_valid_effort(model_name, effort, GeminiReasoningEffort)
        return GeminiReasoning(
            model_name=model_name,
            pure=pure,
            effort=cast(GeminiReasoningEffort, effort),
        )

    if model_name in CLAUDE_MODELS:
        return ClaudeChat(model_name=model_name, pure=pure)

    if model_name in CLAUDE_TTC_MODELS:
        _assert_valid_effort(model_name, effort, ReasoningEffort)
        return ClaudeReasoning(
            model_name=model_name,
            pure=pure,
            effort=cast(ReasoningEffort, effort),
        )

    if model_name in OLLAMA_TTC_MODELS:
        return OllamaChat(model_name=model_name, pure=pure)

    return HFChat(model_name=model_name, pure=pure)


def extract_response(response: ResultE[LMAnswer]) -> str:
    """Extract the answer from the LMAnswer or return an empty string if None."""
    match response:
        case Success(r):
            return r.answer or ""
        case Failure(e):
            logging.error(f"Error generating response: {e}")
            return ""
    return ""
