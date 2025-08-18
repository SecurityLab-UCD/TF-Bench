import logging
from typing import Literal, get_args, cast, TypeAlias

from returns.result import ResultE, Success, Failure, Result

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

from openai.types.shared.reasoning_effort import ReasoningEffort as OAIReasoningEffort
from ._google import GeminiReasoningEffort
from ._types import ReasoningEffort


def _assert_valid_effort(model: str, effort: str | None, effort_cls):
    """Check if the given effort is valid for the model."""
    if effort:
        assert effort in get_args(
            effort_cls
        ), f"`{effort}` is not a valid reasoning effort for {model}."


def router(model_name: str, pure: bool, effort: str | None = None) -> LM | None:
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

    return None


def is_supported(model_name: str) -> bool:
    """check if the model is supported"""
    all_models = (
        OAI_MODELS + OAI_TTC_MODELS + OAI_O5 + GEMINI_MODELS + GEMINI_TTC_MODELS
    )
    return model_name in all_models


def extract_response(response: ResultE[LMAnswer]) -> str:
    """Extract the answer from the LMAnswer or return an empty string if None."""
    match response:
        case Success(r):
            return r.answer or ""
        case Failure(e):
            logging.error(f"Error generating response: {e}")
            return ""
    return ""
